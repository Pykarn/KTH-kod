"""
Organize downloaded Canvas files into KTH_KOD/<COURSE>/<category>/ using a
local Ollama model, and build simple HTML pages that link to every file.

Prerequisites:
1. Install Ollama: https://ollama.com/download
2. Pull a model:  ollama pull llama3.2      (a bigger one such as
   llama3.1:8b or qwen2.5:7b is noticeably more accurate)
3. Make sure Ollama is running (`ollama serve` if it isn't).
4. Run this AFTER canvas_download.py has filled ./canvas_downloads/.

Run:  pip install requests pypdf      (pypdf is optional but recommended)
      python organize_and_build_site.py

Edit the COURSES list below to choose which course folders to process.
"""

import html
import json
import os
import re
import shutil
from urllib.parse import quote

import requests

# ----------------------------------------------------------------------
# SETTINGS - edit these
# ----------------------------------------------------------------------

# Only these course folders (inside SOURCE_DIR) will be organized.
COURSES = ["EL1000"]

SOURCE_DIR = "canvas_downloads"   # where canvas_download.py saved the files
SITE_DIR = "KTH_KOD"              # output folder (the one you push to GitHub)

OLLAMA_MODEL = "llama3.2"
OLLAMA_URL = "http://localhost:11434"

# Delete the old category folders of a course before rebuilding it, so files
# that were misplaced in an earlier run don't stay behind. Only the category
# folders and index.html inside SITE_DIR/<course> are touched.
CLEAN_OLD_OUTPUT = True

# Give the model the first-page text of PDFs. Filenames like "F4_AF.pdf" say
# little, but the first page ("Lecture 4: Bode Plot") usually settles it.
USE_PDF_PREVIEW = True

# --- Filters: what the script is allowed to sort -----------------------
# Only files with these extensions are sorted; everything else (html, css,
# js, images, ...) is ignored. Add e.g. ".py", ".java", ".ipynb" if you want
# code files too. Set to None to allow every file type.
ALLOWED_EXTENSIONS = {
    ".pdf", ".ppt", ".pptx", ".doc", ".docx", ".xls", ".xlsx",
    ".txt", ".md", ".tex", ".zip",
}

# Download folders starting with "github_" come from GitHub repos that a
# teacher linked (see canvas_download.py). They often contain a whole
# website or code project. Set to False to skip them completely.
INCLUDE_GITHUB_REPOS = True

# Folders that are never entered, and filenames that are never copied.
SKIP_DIR_NAMES = {".git", ".github", "node_modules", "__pycache__"}
SKIP_FILE_NAMES = {"index.html", "download", "preview", ".ds_store", "thumbs.db"}

# category name -> description shown to the model. Change names/descriptions
# freely; the folders and the website follow this dict.
CATEGORIES = {
    "exam": "old exams, exam solutions, tentamen, re-exams, practice exams",
    "lecture": "lecture slides, lecture notes, presentations, 'Lecture N' / 'Föreläsning N'",
    "exercise": "exercise sheets, problem sets, labs, assignments, homework, tutorials and their solutions",
    "literature": "textbooks, book chapters, compendiums, reference sheets, formula sheets, articles",
    "other": "anything that clearly fits none of the above (syllabus, schedules, admin info)",
}

# ----------------------------------------------------------------------

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None


def pdf_preview(path, max_chars=700):
    """Return the first-page text of a PDF (empty string if unavailable)."""
    if not (USE_PDF_PREVIEW and PdfReader and path.lower().endswith(".pdf")):
        return ""
    try:
        text = PdfReader(path).pages[0].extract_text() or ""
        return re.sub(r"\s+", " ", text).strip()[:max_chars]
    except Exception:
        return ""


def ollama_ready():
    """Check that Ollama is running and the model is installed."""
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        r.raise_for_status()
        names = [m["name"] for m in r.json().get("models", [])]
        if not any(n == OLLAMA_MODEL or n.startswith(OLLAMA_MODEL + ":") for n in names):
            print(f"Model '{OLLAMA_MODEL}' not found. Run: ollama pull {OLLAMA_MODEL}")
            return False
        return True
    except requests.RequestException as e:
        print(f"Ollama is not reachable at {OLLAMA_URL}: {e}")
        return False


def classify_with_ollama(filename, subfolder, preview):
    """Ask the model for a category. The JSON schema forces one valid value."""
    category_help = "\n".join(f"- {c}: {d}" for c, d in CATEGORIES.items())
    prompt = (
        "You sort university course files (KTH) into folders.\n"
        f"Categories:\n{category_help}\n\n"
        "Hints: 'tenta', 'exam', 'omtenta' => exam. Files named F1, F2, "
        "'lecture', 'föreläsning', 'slides' => lecture. 'ovn', 'övning', "
        "'lab', 'hw', 'problem' => exercise.\n\n"
        f"Filename: {filename}\n"
    )
    if subfolder:
        prompt += f"Original Canvas folder: {subfolder}\n"
    if preview:
        prompt += f"Start of the first page: {preview}\n"
    prompt += "\nChoose the single best category."

    payload = {
        "model": OLLAMA_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        "options": {"temperature": 0},
        "format": {
            "type": "object",
            "properties": {"category": {"type": "string", "enum": list(CATEGORIES)}},
            "required": ["category"],
        },
    }
    resp = requests.post(f"{OLLAMA_URL}/api/chat", json=payload, timeout=180)
    resp.raise_for_status()
    answer = json.loads(resp.json()["message"]["content"])["category"]
    return answer if answer in CATEGORIES else "other"


def classify_with_rules(filename, subfolder=""):
    """Keyword fallback, only used if Ollama is unavailable or errors."""
    name = f"{subfolder}/{filename}".lower()
    if re.search(r"exam|tenta|omtenta|kontrollskrivning", name):
        return "exam"
    if re.search(r"lecture|slides|forel|föreläsning|(^|[^a-z])f\d+([^a-z]|$)", name):
        return "lecture"
    if re.search(r"exercise|övning|ovn|lab|assignment|uppgift|homework|problem", name):
        return "exercise"
    if re.search(r"book|chapter|literature|reading|compendium|kompendium|formula", name):
        return "literature"
    return "other"


def unique_path(directory, filename):
    """Avoid overwriting when two files from different subfolders share a name."""
    base, ext = os.path.splitext(filename)
    path = os.path.join(directory, filename)
    n = 1
    while os.path.exists(path):
        path = os.path.join(directory, f"{base}_{n}{ext}")
        n += 1
    return path


def clean_course_output(course):
    course_out = os.path.join(SITE_DIR, course)
    for cat in CATEGORIES:
        shutil.rmtree(os.path.join(course_out, cat), ignore_errors=True)
    index = os.path.join(course_out, "index.html")
    if os.path.exists(index):
        os.remove(index)


def organize_course(course, use_ollama):
    course_src = os.path.join(SOURCE_DIR, course)
    if not os.path.isdir(course_src):
        print(f"[skip] {course_src} not found")
        return None

    print(f"\nOrganizing {course}...")
    if CLEAN_OLD_OUTPUT:
        clean_course_output(course)

    files_by_category = {cat: [] for cat in CATEGORIES}

    skipped = 0
    for root, dirs, files in os.walk(course_src):
        # Don't descend into unwanted folders
        dirs[:] = [
            d for d in dirs
            if d not in SKIP_DIR_NAMES
            and not (not INCLUDE_GITHUB_REPOS and d.startswith("github_"))
        ]
        subfolder = os.path.relpath(root, course_src)
        subfolder = "" if subfolder == "." else subfolder
        for filename in sorted(files):
            ext = os.path.splitext(filename)[1].lower()
            if (
                filename.startswith(".")
                or filename.lower() in SKIP_FILE_NAMES
                or (ALLOWED_EXTENSIONS is not None and ext not in ALLOWED_EXTENSIONS)
            ):
                skipped += 1
                continue
            src_path = os.path.join(root, filename)

            category = None
            if use_ollama:
                try:
                    category = classify_with_ollama(
                        filename, subfolder, pdf_preview(src_path)
                    )
                except (requests.RequestException, KeyError, ValueError) as e:
                    print(f"  (Ollama failed for {filename}: {e}; using rules)")
            if category is None:
                category = classify_with_rules(filename, subfolder)

            dest_dir = os.path.join(SITE_DIR, course, category)
            os.makedirs(dest_dir, exist_ok=True)
            dest_path = unique_path(dest_dir, filename)
            shutil.copy2(src_path, dest_path)
            files_by_category[category].append(os.path.basename(dest_path))
            print(f"  {filename}  ->  {category}")

    print(f"  ({skipped} files skipped by the filters)")
    build_course_page(course, files_by_category)
    return files_by_category


def build_course_page(course, files_by_category):
    lines = [f"<h1>{html.escape(course)}</h1>", '<p><a href="../index.html">&larr; All courses</a></p>']
    for category in CATEGORIES:
        files = files_by_category.get(category, [])
        if not files:
            continue
        lines.append(f"<h2>{html.escape(category.title())} ({len(files)})</h2><ul>")
        for filename in sorted(files):
            href = f"{quote(category)}/{quote(filename)}"
            lines.append(f'<li><a href="{href}">{html.escape(filename)}</a></li>')
        lines.append("</ul>")
    page = (
        '<!DOCTYPE html><html><head><meta charset="utf-8">'
        f"<title>{html.escape(course)}</title></head><body>\n"
        + "\n".join(lines)
        + "\n</body></html>"
    )
    with open(os.path.join(SITE_DIR, course, "index.html"), "w", encoding="utf-8") as f:
        f.write(page)


def build_root_index(courses):
    lines = ["<h1>My Courses</h1><ul>"]
    for name in courses:
        lines.append(f'<li><a href="{quote(name)}/index.html">{html.escape(name)}</a></li>')
    lines.append("</ul>")
    page = (
        '<!DOCTYPE html><html><head><meta charset="utf-8">'
        "<title>My Courses</title></head><body>\n"
        + "\n".join(lines)
        + "\n</body></html>"
    )
    os.makedirs(SITE_DIR, exist_ok=True)
    with open(os.path.join(SITE_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(page)


def main():
    if not os.path.isdir(SOURCE_DIR):
        print(f"No {SOURCE_DIR}/ folder found. Run canvas_download.py first.")
        return

    use_ollama = ollama_ready()
    if not use_ollama:
        print("Falling back to simple keyword rules for ALL files.\n")

    done = []
    for course in COURSES:
        if organize_course(course, use_ollama) is not None:
            done.append(course)

    build_root_index(done)
    print(f"\nDone. Organized {len(done)} course(s). Site files are in ./{SITE_DIR}/")


if __name__ == "__main__":
    main()