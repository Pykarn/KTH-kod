"""
Organize downloaded Canvas files using a local Ollama model, and build
simple HTML pages (for GitHub Pages) that link to each file for download.

Prerequisites:
1. Install Ollama: https://ollama.com/download
2. Pull a small model:  ollama pull llama3.2
3. Make sure Ollama is running (it starts automatically after install,
   otherwise run `ollama serve` in a terminal).
4. Run this AFTER canvas_download.py has filled ./canvas_downloads/.

Run:  pip install requests
      python organize_and_build_site.py

Output: a ./docs folder containing one subfolder per course, each with
its files sorted into exam/lecture/exercise/literature/other, plus an
index.html per course and a root index.html linking them all. Point
GitHub Pages at the /docs folder to publish this as a website.
"""

import os
import re
import shutil
import requests

SOURCE_DIR = "canvas_downloads"
SITE_DIR = "KTH_KOD"  # GitHub Pages can serve directly from a /docs folder
OLLAMA_MODEL = "llama3.2"
OLLAMA_URL = "http://localhost:11434/api/generate"

CATEGORIES = ["exam", "lecture", "exercise", "literature", "other"]


def classify_filename(filename):
    """Ask the local model to sort a filename into one of CATEGORIES."""
    prompt = (
        "Classify this file into exactly one word from this list: "
        f"{', '.join(CATEGORIES)}.\n"
        f"Filename: {filename}\n"
        "Answer with only the single category word, nothing else."
    )
    try:
        resp = requests.post(
            OLLAMA_URL,
            json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
            timeout=30,
        )
        resp.raise_for_status()
        answer = resp.json().get("response", "").strip().lower()
        for cat in CATEGORIES:
            if cat in answer:
                return cat
    except requests.RequestException as e:
        print(f"  (Ollama unavailable, using filename rules instead: {e})")

    # Fallback if Ollama isn't running: simple keyword rules
    name = filename.lower()
    if re.search(r"exam|tenta", name):
        return "exam"
    if re.search(r"lecture|f\d+|forel", name):
        return "lecture"
    if re.search(r"exercise|lab|assignment|uppgift", name):
        return "exercise"
    if re.search(r"book|chapter|literature|reading", name):
        return "literature"
    return "other"


def organize_course(course_name):
    course_src = os.path.join(SOURCE_DIR, course_name)
    if not os.path.isdir(course_src):
        return None
    print(f"Organizing {course_name}...")
    files_by_category = {cat: [] for cat in CATEGORIES}

    for filename in os.listdir(course_src):
        src_path = os.path.join(course_src, filename)
        if not os.path.isfile(src_path):
            continue
        category = classify_filename(filename)
        dest_dir = os.path.join(SITE_DIR, course_name, category)
        os.makedirs(dest_dir, exist_ok=True)
        shutil.copy2(src_path, os.path.join(dest_dir, filename))
        files_by_category[category].append(filename)
        print(f"  {filename} -> {category}")

    build_course_page(course_name, files_by_category)
    return files_by_category


def build_course_page(course_name, files_by_category):
    lines = [f"<h1>{course_name}</h1>"]
    for category in CATEGORIES:
        files = files_by_category.get(category, [])
        if not files:
            continue
        lines.append(f"<h2>{category.title()}</h2><ul>")
        for filename in files:
            href = f"{category}/{filename}"
            lines.append(f'<li><a href="{href}">{filename}</a></li>')
        lines.append("</ul>")
    html = "<html><body>\n" + "\n".join(lines) + "\n</body></html>"
    with open(os.path.join(SITE_DIR, course_name, "index.html"), "w") as f:
        f.write(html)


def build_root_index(course_names):
    lines = ["<h1>My Courses</h1><ul>"]
    for name in course_names:
        lines.append(f'<li><a href="{name}/index.html">{name}</a></li>')
    lines.append("</ul>")
    html = "<html><body>\n" + "\n".join(lines) + "\n</body></html>"
    os.makedirs(SITE_DIR, exist_ok=True)
    with open(os.path.join(SITE_DIR, "index.html"), "w") as f:
        f.write(html)


def main():
    if not os.path.isdir(SOURCE_DIR):
        print(f"No {SOURCE_DIR}/ folder found. Run canvas_download.py first.")
        return
    course_names = [
        d for d in os.listdir(SOURCE_DIR)
        if os.path.isdir(os.path.join(SOURCE_DIR, d))
    ]
    for course_name in course_names:
        organize_course(course_name)
    build_root_index(course_names)
    print(f"\nDone. Site files are in ./{SITE_DIR}/")


if __name__ == "__main__":
    main()
