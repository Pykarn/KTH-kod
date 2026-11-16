"""
Organize downloaded Canvas files into KTH_KOD/<COURSE>/<category>/ and build
HTML pages that link to every file.

HOW FILES ARE SORTED
  1. Every file gets points per category from keyword rules (Swedish and
     English) applied to: the filename, the Canvas module/folder it came
     from, the Canvas item that linked it (e.g. an assignment), and the
     first page of its text. canvas_download.py records where each file
     came from in .canvas_index.json, which is the strongest clue.
  2. If the rules are clearly sure, that decides (fast, consistent).
  3. Otherwise a local Ollama model decides, with all of the above plus the
     rules' guess as context. Without Ollama the rules' best guess is used.
  Files from a linked GitHub repo are kept together, with their folder
  structure, under KTH_KOD/<COURSE>/repos/<repo>/ (see GITHUB_REPO_MODE).

SAFE BY DESIGN: this script NEVER deletes anything in KTH_KOD/.
  - New files from Canvas are added.
  - Files you already have (same content, wherever you put them) are left alone.
  - Files you added by hand, moved by hand, or that disappeared from Canvas
    stay where they are and are still listed on the web page.
  - A file that was updated on Canvas replaces the old copy only if you
    have not edited that copy yourself; otherwise the new version is saved
    next to it with a _1, _2 ... suffix.

Prerequisites:
1. Install Ollama: https://ollama.com/download   (optional but recommended)
2. Pull a model:  ollama pull llama3.2      (a bigger one such as
   llama3.1:8b or qwen2.5:7b is noticeably more accurate)
3. Make sure Ollama is running (`ollama serve` if it isn't).
4. Run this AFTER canvas_download.py has filled ./canvas_downloads/.

Run:  pip install requests pypdf      (pypdf is optional but recommended)
      python organize_and_build_site.py               (courses in COURSES)
      python organize_and_build_site.py DD1368        (only some courses)
      python organize_and_build_site.py --dry-run     (show, change nothing)
      python organize_and_build_site.py --explain     (show why, per file)
      python organize_and_build_site.py --pages-only  (only rebuild index.html)
"""

import argparse
import fnmatch
import hashlib
import html
import json
import logging
import os
import re
import shutil
import time
import unicodedata
import zipfile
from datetime import datetime
from urllib.parse import quote

import requests

# ----------------------------------------------------------------------
# SETTINGS - edit these
# ----------------------------------------------------------------------

# Only these course folders (inside SOURCE_DIR) will be organized.
COURSES = ["DD1385", "DD1368", "SF1811"]

SOURCE_DIR = "canvas_downloads"   # where canvas_download.py saved the files
SITE_DIR = "KTH_KOD"              # output folder (the one you push to GitHub)

OLLAMA_MODEL = "llama3.2"
OLLAMA_URL = "http://localhost:11434"

# Read the start of each file (PDF, PowerPoint, Word, notebooks, code, text)
# and use it for sorting. Filenames like "F4_AF.pdf" say little, but the
# first page ("Lecture 4: Bode Plot") usually settles it.
USE_PREVIEW = True

# When the keyword rules are this sure, Ollama is not asked (faster, and
# consistent). Higher = ask Ollama more often. Lower = trust rules more.
RULES_CONFIDENT_SCORE = 3   # the winning category needs at least this many points
RULES_CONFIDENT_MARGIN = 3  # ... and this many more than the runner-up

# Files named alike (F1, F2 ... or ak191021, ak191218 ...) end up in the same
# category: when most earlier files with the same name pattern went to one
# category, a new one follows them (unless the rules are sure otherwise).
KEEP_SIMILAR_TOGETHER = True

# False (recommended): a file that is already in KTH_KOD is never moved, so
#   files you sorted by hand stay put, and re-runs are fast.
# True: files that THIS SCRIPT placed earlier are re-classified and MOVED
#   (never deleted) if the new sorting picks another category. Files you
#   added or moved yourself are never touched, even with True.
#   (Same as running with --reclassify.)
RECLASSIFY = False

# "folder": files from a linked GitHub repo stay together in
#           <course>/repos/<repo>/ with their own folder structure.
# "sort":   every repo file is sorted on its own, like Canvas files.
# "skip":   GitHub repos are ignored.
GITHUB_REPO_MODE = "folder"

# --- Filters: what the script is allowed to sort -----------------------
# Files with these extensions are sorted. Set to None to allow every type.
ALLOWED_EXTENSIONS = {
    # documents
    ".pdf", ".ppt", ".pptx", ".doc", ".docx", ".xls", ".xlsx", ".odt", ".odp",
    ".ods", ".txt", ".md", ".tex", ".bib", ".zip", ".html", ".drawio",
    # code and data (MATLAB, Python, Java, SQL, notebooks ...)
    ".m", ".mlx", ".mat", ".py", ".ipynb", ".java", ".c", ".cpp", ".h",
    ".hpp", ".cs", ".js", ".ts", ".kt", ".scala", ".rs", ".hs", ".go", ".r",
    ".rmd", ".jl", ".sh", ".sql", ".csv", ".tsv", ".json", ".xml",
    # images (assignment figures, ER diagrams, screenshots)
    ".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp",
}

# Filenames matching any of these patterns are ALWAYS copied, whatever the
# extension (case-insensitive, * = anything). Add your own, e.g. "lab*".
ALWAYS_INCLUDE = ["ex*", "*.m", "makefile", "readme*"]

# Folders that are never entered, and filenames that are never copied.
SKIP_DIR_NAMES = {".git", ".github", "node_modules", "__pycache__", ".idea", ".vscode"}
SKIP_FILE_NAMES = {"index.html", "download", "preview", ".ds_store", "thumbs.db"}

# category name -> description shown to the model. Change names/descriptions
# freely; the folders and the website follow this dict. Keep "other" last.
CATEGORIES = {
    "exam": "old exams, exam solutions, tentamen, re-exams, practice exams, "
            "kontrollskrivningar, duggor",
    "lecture": "lecture slides, lecture notes, presentations, 'Lecture N' / "
               "'Föreläsning N', code examples shown in lectures",
    "exercise": "exercise sheets, problem sets, labs, assignments, homework, "
                "projects, tutorials, their solutions, and code or data for them",
    "literature": "textbooks, book chapters, compendiums, reference sheets, "
                  "formula sheets, articles, reading lists",
    "other": "course info that is none of the above: syllabus, course PM, "
             "schedules, grading rubrics, installation guides, admin info",
}

# Headings on the web page (the folder names stay as in CATEGORIES).
DISPLAY_NAMES = {
    "exam": "Tentor",
    "lecture": "Föreläsningar",
    "exercise": "Övningar, labbar & uppgifter",
    "literature": "Litteratur",
    "other": "Övrigt",
    "repos": "Kod från GitHub",
}

# Files added within this many days get a "ny" badge on the web page.
NEW_BADGE_DAYS = 14

# ----------------------------------------------------------------------

MANIFEST_NAME = ".organize_manifest.json"
CANVAS_INDEX_NAME = ".canvas_index.json"
GENERATED_MARK = "<!-- generated by organize_and_build_site.py -->"
REPOS_DIR = "repos"

try:
    from pypdf import PdfReader
    logging.getLogger("pypdf").setLevel(logging.ERROR)  # silence warnings about odd PDFs
except ImportError:
    PdfReader = None


# --- helpers ------------------------------------------------------------

def file_hash(path):
    h = hashlib.sha1()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def wanted(filename):
    """Decide whether a source file should be copied at all."""
    low = filename.lower()
    if filename.startswith(".") or low in SKIP_FILE_NAMES:
        return False
    if any(fnmatch.fnmatch(low, p.lower()) for p in ALWAYS_INCLUDE):
        return True
    if ALLOWED_EXTENSIONS is None:
        return True
    return os.path.splitext(low)[1] in ALLOWED_EXTENSIONS


def site_files(course_out):
    """All files currently in the course's site folder (relative paths)."""
    result = []
    for root, dirs, files in os.walk(course_out):
        dirs[:] = sorted(d for d in dirs if not d.startswith("."))
        for f in sorted(files):
            rel = os.path.relpath(os.path.join(root, f), course_out)
            if rel == "index.html" or f.startswith("."):
                continue
            result.append(rel.replace(os.sep, "/"))
    return result


def load_json(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def save_manifest(course_out, manifest):
    os.makedirs(course_out, exist_ok=True)
    path = os.path.join(course_out, MANIFEST_NAME)
    with open(path + ".tmp", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=1, ensure_ascii=False, sort_keys=True)
    os.replace(path + ".tmp", path)


def unique_path(directory, filename):
    """Never overwrite: add _1, _2 ... if the name is taken."""
    base, ext = os.path.splitext(filename)
    path = os.path.join(directory, filename)
    n = 1
    while os.path.exists(path):
        path = os.path.join(directory, f"{base}_{n}{ext}")
        n += 1
    return path


def natural_key(text):
    """Sort "F2" before "F10" and ignore case."""
    return [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", text.lower())]


def human_size(n):
    for unit in ("B", "kB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return f"{n:.0f} {unit}" if unit == "B" else f"{n:.1f} {unit}"
        n /= 1024


def fold(text):
    """Lowercase; also give an ASCII version so 'Föreläsning' matches 'forelasning'."""
    text = (text or "").lower()
    ascii_text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return text if ascii_text == text else f"{text} {ascii_text}"


# --- reading the start of a file ----------------------------------------

TEXT_EXTS = {".txt", ".md", ".tex", ".bib", ".csv", ".tsv", ".json", ".xml", ".html",
             ".py", ".java", ".c", ".cpp", ".h", ".hpp", ".cs", ".js", ".ts", ".kt",
             ".scala", ".rs", ".hs", ".go", ".r", ".rmd", ".jl", ".sh", ".sql", ".m"}


def _xml_text(z, names, tag_re, limit):
    out = []
    for name in names:
        try:
            xml = z.read(name).decode("utf-8", "ignore")
        except KeyError:
            continue
        out.extend(tag_re.findall(xml))
        if sum(len(x) for x in out) > limit:
            break
    return " ".join(html.unescape(x) for x in out)


def preview_text(path, max_chars=900):
    """The first page/slide/lines of a file as plain text ('' if unknown)."""
    if not USE_PREVIEW:
        return ""
    ext = os.path.splitext(path)[1].lower()
    text = ""
    try:
        if ext == ".pdf" and PdfReader:
            reader = PdfReader(path)
            text = " ".join((p.extract_text() or "") for p in reader.pages[:2])
        elif ext in (".pptx", ".docx", ".xlsx", ".odp", ".odt"):
            with zipfile.ZipFile(path) as z:
                if ext == ".pptx":
                    slides = sorted((n for n in z.namelist()
                                     if re.match(r"ppt/slides/slide\d+\.xml$", n)), key=natural_key)
                    text = _xml_text(z, slides[:3], re.compile(r"<a:t>([^<]*)</a:t>"), max_chars)
                elif ext == ".docx":
                    text = _xml_text(z, ["word/document.xml"], re.compile(r"<w:t[^>]*>([^<]*)</w:t>"), max_chars)
                elif ext == ".xlsx":
                    text = _xml_text(z, ["xl/sharedStrings.xml"], re.compile(r"<t[^>]*>([^<]*)</t>"), max_chars)
                else:
                    text = _xml_text(z, ["content.xml"], re.compile(r">([^<]{2,})<"), max_chars)
        elif ext == ".ipynb":
            nb = load_json(path)
            text = " ".join("".join(c.get("source", [])) for c in nb.get("cells", [])[:6])
        elif ext in TEXT_EXTS or os.path.getsize(path) < 200_000 and not ext:
            with open(path, encoding="utf-8", errors="ignore") as f:
                text = f.read(4000)
            if ext == ".html":
                text = re.sub(r"<(script|style)\b.*?</\1>", " ", text, flags=re.S | re.I)
                text = html.unescape(re.sub(r"<[^>]+>", " ", text))
    except Exception:
        return ""
    return re.sub(r"\s+", " ", text).strip()[:max_chars]


# --- classification: keyword rules ---------------------------------------

# A word that starts a match must not be glued to other letters before it.
_B = r"(?<![a-zåäö])"
_E = r"(?![a-zåäö])"

KEYWORDS = {
    "exam": [
        r"tenta(men|mina|or|n)?", r"omtenta\w*", r"omexam\w*", r"re-?exam\w*",
        r"exam(s|en|ination)?", r"midterm", r"final exam", r"kontrollskrivning\w*",
        r"ks\d*", r"dugg(a|or|an)", r"past papers?", r"old exams?", r"tentamensuppgift\w*",
        r"tentafr[aå]g\w*", r"övningstenta\w*", r"ovningstenta\w*", r"exam prep\w*",
        r"quiz\w*", r"provtenta\w*", r"mock exam\w*",
    ],
    "lecture": [
        r"f[öo]rel[äa]sning\w*", r"lectures?", r"lec\d*", r"slides?", r"bilder",
        r"f\d{1,2}", r"f[öo]\d{1,2}", r"frl\d*", r"le\d{1,2}", r"session\s?\d+",
        r"presentation\w*", r"lecture notes?", r"föreläsningsanteckning\w*", r"handouts?",
        r"week\s?\d+", r"vecka\s?\d+",
    ],
    "exercise": [
        r"[öo]vning\w*", r"[öo]\d{1,2}", r"ex\d+\w*", r"exercises?", r"labb?(ar|arna|en|s)?\d*",
        r"labb?-?pm", r"laboration\w*", r"homeworks?", r"hw\d*", r"assignments?",
        r"uppgift\w*", r"inl[äa]mning\w*", r"problems?", r"problem sets?",
        r"tutorials?", r"seminari\w*", r"projekt\w*", r"projects?", r"case stud(y|ies)",
        r"workshop\w*", r"r[äa]kne[öo]vning\w*", r"övningsuppgift\w*", r"instructions?",
        r"skeleton", r"starter( code)?", r"template", r"kodskelett",
    ],
    "literature": [
        r"books?", r"bok(en)?", r"kursbok\w*", r"textbook\w*", r"kompendi\w*",
        r"compendi\w*", r"chapters?", r"kapitel", r"ch\d+", r"formelsamling\w*",
        r"formula sheets?", r"formulas?", r"cheat ?sheets?", r"articles?", r"papers?",
        r"reading\w*", r"l[äa]sanvisning\w*", r"ordlista", r"glossary", r"handbook\w*",
        r"lecture notes? book", r"reference", r"manual", r"summary", r"sammanfattning\w*",
    ],
    "other": [
        r"syllabus", r"kurs-?pm", r"course ?(memo|pm|info\w*|plan)", r"kursplan",
        r"schedule", r"schema(?!\.sql)", r"rubrics?", r"grading", r"bed[öo]mning\w*",
        r"betyg\w*", r"faq\w*", r"installation\w*", r"install\w*", r"setup",
        r"local lab setup", r"regler", r"rules", r"information", r"admin\w*",
        r"welcome", r"v[äa]lkommen", r"deadlines?", r"timeline",
    ],
}
SOLUTION_WORDS = [r"l[öo]sning(ar|sförslag)?\w*", r"l[öo]sn", r"lsg", r"sol\d*", r"solutions?",
                  r"facit", r"answers?", r"svar"]

COMPILED = {c: [re.compile(_B + p + _E) for p in pats] for c, pats in KEYWORDS.items()}
SOLUTION_RE = [re.compile(_B + p + _E) for p in SOLUTION_WORDS]

CODE_EXTS = {".py", ".java", ".c", ".cpp", ".h", ".hpp", ".cs", ".js", ".ts", ".kt",
             ".scala", ".rs", ".hs", ".go", ".r", ".rmd", ".jl", ".sh", ".sql", ".m",
             ".mlx", ".ipynb", ".mat", ".csv", ".tsv"}
SLIDE_EXTS = {".ppt", ".pptx", ".odp", ".key"}

# How much each clue is worth.
WEIGHTS = {"filename": 3, "module": 2, "origin": 2, "preview": 1}


def rule_scores(filename, module, origin, preview):
    """Points per category, and a list of reasons (for --explain)."""
    scores = {c: 0 for c in CATEGORIES}
    reasons = []
    ext = os.path.splitext(filename)[1].lower()
    stem = os.path.splitext(filename)[0]
    sources = {
        "filename": fold(re.sub(r"[_\-.+]+", " ", stem)),
        "module": fold(re.sub(r"[_\-.+/]+", " ", module or "")),
        "origin": fold(origin or ""),
        "preview": fold((preview or "")[:300]),
    }
    for source, text in sources.items():
        if not text.strip():
            continue
        for cat, regexes in COMPILED.items():
            if cat not in scores:
                continue
            if cat in ("other", "literature") and source == "filename" and ext in CODE_EXTS:
                continue  # "schema.sql" is a database schema, "Book.java" is code
            for rx in regexes:
                m = rx.search(text)
                if m:
                    scores[cat] += WEIGHTS[source]
                    reasons.append(f"{source} '{m.group(0)}' -> {cat}")
                    break
        # "solution" belongs with whatever it is a solution to (exam/exercise)
        if any(rx.search(text) for rx in SOLUTION_RE) and "exercise" in scores:
            scores["exercise"] += 1
            reasons.append(f"{source} 'solution' -> exercise +1")

    origin_low = (origin or "").lower()
    if origin_low.startswith("assignment") and "exercise" in scores:
        scores["exercise"] += 2
        reasons.append("linked from an assignment -> exercise")
    if ext in SLIDE_EXTS and "lecture" in scores:
        scores["lecture"] += 2
        reasons.append(f"{ext} -> lecture")
    if ext in CODE_EXTS and "exercise" in scores:
        scores["exercise"] += 1
        reasons.append(f"{ext} -> exercise")
    return scores, reasons


def rules_decision(scores):
    ranked = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
    (best, top), (_, second) = ranked[0], ranked[1] if len(ranked) > 1 else (None, 0)
    confident = top >= RULES_CONFIDENT_SCORE and top - second >= RULES_CONFIDENT_MARGIN
    fallback = "other" if "other" in CATEGORIES else list(CATEGORIES)[-1]
    return (best if top > 0 else fallback), confident


# --- classification: Ollama ----------------------------------------------

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


EXAMPLES = """Examples:
- "EL1000_F4_AF.pdf" in module "Föreläsningar" -> lecture
- "tenta_2022-10-24_lsg.pdf" -> exam
- "Lab1 - NEW.pdf" linked from assignment 'Lab 1' -> exercise
- "INST_ 2026 Homework 2.pdf" -> exercise
- "Formelsamling.pdf" -> literature
- "PostgreSQL Installation Guide.pdf" -> other
- "Point.java" in module "Week 3: Lecture code" -> lecture
- "ShutTheBox.java" in folder "Övning 2" -> exercise"""


def classify_with_ollama(filename, module, origin, preview, guess):
    """Ask the model for a category. The JSON schema forces one valid value."""
    category_help = "\n".join(f"- {c}: {d}" for c, d in CATEGORIES.items())
    prompt = (
        "You sort university course files (KTH, Sweden) into folders. "
        "Files may be in Swedish or English.\n"
        f"Categories:\n{category_help}\n\n{EXAMPLES}\n\n"
        "The Canvas module or folder a file sits in, and the Canvas item that "
        "links to it, are usually the strongest clues.\n\n"
        f"Filename: {filename}\n"
    )
    if module:
        prompt += f"Canvas module/folder: {module}\n"
    if origin:
        prompt += f"Linked from: {origin}\n"
    if preview:
        prompt += f"Start of the file: {preview}\n"
    prompt += f"Keyword rules suggest: {guess} (may be wrong)\n\nChoose the single best category."

    payload = {
        "model": OLLAMA_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        "keep_alive": "10m",
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
    return answer if answer in CATEGORIES else guess


class Classifier:
    def __init__(self, use_ollama, explain=False):
        self.use_ollama = use_ollama
        self.explain = explain
        self.counts = {"rules": 0, "ollama": 0, "similar": 0}

    def __call__(self, filename, module, origin, src_path, similar=None):
        preview = preview_text(src_path)
        scores, reasons = rule_scores(filename, module, origin, preview)
        guess, confident = rules_decision(scores)
        how = "rules"
        category = guess
        if similar and not confident:
            category, how = similar, "similar"
        elif self.use_ollama and not confident:
            try:
                category = classify_with_ollama(filename, module, origin, preview, guess)
                how = "ollama"
            except (requests.RequestException, KeyError, ValueError) as e:
                print(f"  (Ollama failed for {filename}: {e}; using rules)")
        self.counts[how] += 1
        if self.explain:
            shown = ", ".join(f"{c}={s}" for c, s in scores.items() if s)
            print(f"      [{how}] {shown or 'no keywords'}"
                  + (f" | {'; '.join(reasons)}" if reasons else ""))
        return category, how


def name_shape(filename):
    """'ak191021.pdf' -> 'ak#.pdf', 'EL1000_F4_AF.pdf' -> 'el#_f#_af.pdf'.
    None if the name has no digits or (almost) no letters."""
    shape = re.sub(r"\d+", "#", filename.lower())
    letters = re.sub(r"[^a-zåäö]", "", os.path.splitext(shape)[0])
    return shape if "#" in shape and len(letters) >= 1 else None


class SimilarNames:
    """Remembers which category files with the same name pattern went to."""

    def __init__(self, manifest):
        self.votes = {}
        for src, v in manifest.items():
            if isinstance(v, dict) and v.get("dest"):
                self.add(os.path.basename(src), v["dest"].split("/")[0])

    def add(self, filename, category):
        shape = name_shape(filename)
        if shape and category in CATEGORIES:
            counts = self.votes.setdefault(shape, {})
            counts[category] = counts.get(category, 0) + 1

    def suggest(self, filename):
        counts = self.votes.get(name_shape(filename) or "")
        if not KEEP_SIMILAR_TOGETHER or not counts:
            return None
        best, n = max(counts.items(), key=lambda kv: kv[1])
        total = sum(counts.values())
        return best if n >= 2 and n / total >= 0.6 else None


# --- where did a downloaded file come from? ------------------------------

def canvas_metadata(course_src):
    """Map relative path -> {"module", "origin"} from canvas_download.py's index."""
    index = load_json(os.path.join(course_src, CANVAS_INDEX_NAME))
    meta = {}
    for table in ("files", "external", "pages"):
        for rec in (index.get(table) or {}).values():
            if isinstance(rec, dict) and rec.get("path"):
                meta[rec["path"]] = rec
    return meta, index.get("course_name") or ""


# --- main work ----------------------------------------------------------

def organize_course(course, classify, dry_run=False, reclassify=False):
    course_src = os.path.join(SOURCE_DIR, course)
    course_out = os.path.join(SITE_DIR, course)
    if not os.path.isdir(course_src):
        print(f"[skip] {course_src} not found")
        return False

    print(f"\nOrganizing {course}{' (dry run, nothing is changed)' if dry_run else ''}...")
    os.makedirs(course_out, exist_ok=True)
    manifest = load_json(os.path.join(course_out, MANIFEST_NAME))  # src -> {"dest","sha1",...}
    meta, course_name = canvas_metadata(course_src)
    if course_name:
        manifest["_course_name"] = course_name

    # Everything already in the site folder, indexed by content.
    by_hash = {}
    for rel in site_files(course_out):
        by_hash.setdefault(file_hash(os.path.join(course_out, rel)), rel)

    similar = SimilarNames(manifest)
    stats = {"new": 0, "updated": 0, "moved": 0, "kept": 0, "skipped": 0}
    skipped_exts = {}
    now = datetime.now().isoformat(timespec="seconds")

    def place(src_path, src_key, filename, subfolder, repo_rel):
        """Return the destination directory and label for a new file."""
        if repo_rel is not None:
            return os.path.join(course_out, REPOS_DIR, os.path.dirname(repo_rel)), "repos", "repo"
        info = meta.get(src_key, {})
        module = info.get("module") or subfolder
        category, how = classify(filename, module, info.get("origin", ""), src_path,
                                 similar.suggest(filename))
        similar.add(filename, category)
        return os.path.join(course_out, category), category, how

    for root, dirs, files in os.walk(course_src):
        rel_root = os.path.relpath(root, course_src)
        rel_root = "" if rel_root == "." else rel_root.replace(os.sep, "/")
        dirs[:] = sorted(
            d for d in dirs
            if d not in SKIP_DIR_NAMES and not d.startswith(".")
            and not (GITHUB_REPO_MODE == "skip" and not rel_root and d.startswith("github_"))
        )
        in_repo = GITHUB_REPO_MODE == "folder" and rel_root.startswith("github_")
        for filename in sorted(files, key=natural_key):
            if filename.startswith("."):
                continue  # index files and unfinished downloads
            if not wanted(filename):
                stats["skipped"] += 1
                ext = os.path.splitext(filename)[1].lower() or "(no extension)"
                skipped_exts[ext] = skipped_exts.get(ext, 0) + 1
                continue

            src_path = os.path.join(root, filename)
            src_key = f"{rel_root}/{filename}" if rel_root else filename
            repo_rel = None
            if in_repo:  # github_<repo>/a/b.py -> repos/<repo>/a/b.py
                repo_rel = src_key[len("github_"):]
            sha = file_hash(src_path)
            entry = manifest.get(src_key)

            # 1) Same content already somewhere in the site folder: keep it.
            if sha in by_hash:
                existing = by_hash[sha]
                placed_by_us = bool(entry and entry.get("own") and entry.get("dest") == existing)
                if reclassify and placed_by_us and repo_rel is None:
                    dest_dir, category, how = place(src_path, src_key, filename, rel_root, None)
                    if existing.split("/")[0] != category:
                        new_path = unique_path(dest_dir, os.path.basename(existing))
                        new_rel = os.path.relpath(new_path, course_out).replace(os.sep, "/")
                        print(f"  {filename}  moved  {existing}  ->  {new_rel}  [{how}]")
                        if not dry_run:
                            os.makedirs(dest_dir, exist_ok=True)
                            shutil.move(os.path.join(course_out, existing), new_path)
                        by_hash[sha] = existing = new_rel
                        stats["moved"] += 1
                added = (entry or {}).get("added")
                manifest[src_key] = {"dest": existing, "sha1": sha, "own": placed_by_us}
                if added:
                    manifest[src_key]["added"] = added
                stats["kept"] += 1
                continue

            # 2) Canvas has a newer version of a file we placed earlier.
            if entry and entry.get("own"):
                old_abs = os.path.join(course_out, entry["dest"])
                if os.path.exists(old_abs) and file_hash(old_abs) == entry["sha1"]:
                    dest_rel = entry["dest"]
                    print(f"  {filename}  updated  {dest_rel}")
                    if not dry_run:
                        shutil.copy2(src_path, old_abs)  # you never edited it
                    stats["updated"] += 1
                    manifest[src_key] = {"dest": dest_rel, "sha1": sha, "own": True, "added": now}
                    by_hash[sha] = dest_rel
                    continue
                # You edited or removed our copy: fall through and add the
                # new version as a separate file instead.

            # 3) New file: classify and copy (never overwriting anything).
            dest_dir, category, how = place(src_path, src_key, filename, rel_root, repo_rel)
            dest_path = unique_path(dest_dir, filename)
            dest_rel = os.path.relpath(dest_path, course_out).replace(os.sep, "/")
            if not dry_run:
                os.makedirs(dest_dir, exist_ok=True)
                shutil.copy2(src_path, dest_path)
            manifest[src_key] = {"dest": dest_rel, "sha1": sha, "own": True, "added": now}
            by_hash[sha] = dest_rel
            stats["new"] += 1
            if repo_rel is None:
                print(f"  {src_key}  ->  {category}  [{how}]")

    repo_new = sum(1 for v in manifest.values()
                   if isinstance(v, dict) and v.get("added") == now
                   and str(v.get("dest", "")).startswith(REPOS_DIR + "/"))
    if repo_new:
        print(f"  ({repo_new} files from GitHub repos -> {REPOS_DIR}/)")
    print(
        f"  new: {stats['new']}, updated: {stats['updated']}, moved: {stats['moved']}, "
        f"already there: {stats['kept']}, skipped by filters: {stats['skipped']}"
    )
    if skipped_exts:
        summary = ", ".join(f"{e} x{n}" for e, n in sorted(skipped_exts.items()))
        print(f"  skipped types: {summary}")
        print("  (add an extension to ALLOWED_EXTENSIONS or a pattern to ALWAYS_INCLUDE to keep them)")
    if not dry_run:
        save_manifest(course_out, manifest)
        build_course_page(course)
    return True


# --- web pages ----------------------------------------------------------

CSS = """
:root{--bg:#fff;--fg:#1d1d1f;--muted:#6e6e73;--line:#e5e5ea;--accent:#1954a6;--chip:#f2f2f7}
@media (prefers-color-scheme:dark){:root{--bg:#121214;--fg:#f2f2f7;--muted:#a1a1a6;
--line:#2c2c2e;--accent:#7fb0ff;--chip:#1f1f22}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);
font:15px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}
main{max-width:60rem;margin:0 auto;padding:1.5rem 1rem 4rem}
a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}
h1{font-size:1.6rem;margin:.3rem 0}.sub{color:var(--muted);margin:0 0 1rem}
input[type=search]{width:100%;padding:.6rem .8rem;font:inherit;color:inherit;
background:var(--chip);border:1px solid var(--line);border-radius:.5rem;margin:.5rem 0 1rem}
nav.toc{display:flex;flex-wrap:wrap;gap:.4rem;margin-bottom:1rem}
nav.toc a{background:var(--chip);border-radius:1rem;padding:.15rem .7rem;font-size:.9rem}
details{border-top:1px solid var(--line);padding:.4rem 0}
summary{cursor:pointer;font-weight:600;font-size:1.1rem;padding:.3rem 0}
summary .n{color:var(--muted);font-weight:400}
h3{font-size:.95rem;color:var(--muted);margin:.8rem 0 .2rem}
ul{list-style:none;margin:0;padding:0}
li{display:flex;gap:.6rem;align-items:baseline;padding:.25rem 0;border-bottom:1px solid var(--line)}
li a{flex:1;word-break:break-word}
.meta{color:var(--muted);font-size:.8rem;white-space:nowrap}
.ext{font-size:.7rem;text-transform:uppercase;background:var(--chip);border-radius:.3rem;
padding:0 .35rem;color:var(--muted);min-width:2.6rem;text-align:center}
.new{font-size:.7rem;background:#2e7d32;color:#fff;border-radius:.3rem;padding:0 .35rem}
.card{display:block;border:1px solid var(--line);border-radius:.6rem;padding:.8rem 1rem;margin:.5rem 0}
.card:hover{text-decoration:none;border-color:var(--accent)}
.card b{font-size:1.05rem}.card .sub{margin:0}.hidden{display:none}
"""

SEARCH_JS = """
<script>
const q=document.getElementById('q');
q&&q.addEventListener('input',()=>{const t=q.value.toLowerCase().trim();
document.querySelectorAll('li[data-n]').forEach(li=>li.classList.toggle('hidden',
t&&!li.dataset.n.includes(t)));
document.querySelectorAll('details').forEach(d=>{const any=[...d.querySelectorAll('li[data-n]')]
.some(li=>!li.classList.contains('hidden'));d.classList.toggle('hidden',!any);if(t)d.open=true;});});
</script>"""


def write_page(path, title, body_lines):
    """Write an index.html, but never overwrite one we didn't generate."""
    if os.path.exists(path):
        with open(path, encoding="utf-8", errors="ignore") as f:
            old = f.read()
        # Pages from the old version of this script had no marker.
        old_style = old.startswith('<!DOCTYPE html><html><head><meta charset="utf-8"><title>') and (
            "&larr; All courses" in old or "<h1>My Courses</h1>" in old
        )
        if GENERATED_MARK not in old and not old_style:
            print(f"  (kept your own {path}, not overwritten)")
            return
    page = (
        f'<!DOCTYPE html>{GENERATED_MARK}<html lang="sv"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f"<title>{html.escape(title)}</title><style>{CSS}</style></head><body><main>\n"
        + "\n".join(body_lines)
        + f"\n</main>{SEARCH_JS}</body></html>"
    )
    with open(path, "w", encoding="utf-8") as f:
        f.write(page)


def build_course_page(course):
    """List EVERYTHING in the course folder, including files you added yourself."""
    course_out = os.path.join(SITE_DIR, course)
    manifest = load_json(os.path.join(course_out, MANIFEST_NAME))
    added = {v["dest"]: v.get("added") for v in manifest.values()
             if isinstance(v, dict) and v.get("dest")}
    course_name = manifest.get("_course_name", "")
    cutoff = time.time() - NEW_BADGE_DAYS * 86400

    groups = {}
    for rel in site_files(course_out):
        top = rel.split("/")[0] if "/" in rel else ""
        groups.setdefault(top, []).append(rel)

    order = [c for c in CATEGORIES if c in groups]
    order += sorted((g for g in groups if g not in CATEGORIES and g), key=natural_key)
    if "" in groups:
        order.append("")

    total = sum(len(v) for v in groups.values())
    lines = ['<p><a href="../index.html">&larr; Alla kurser</a></p>',
             f"<h1>{html.escape(course)}</h1>",
             f'<p class="sub">{html.escape(course_name)}{" · " if course_name else ""}'
             f"{total} filer · uppdaterad {datetime.now():%Y-%m-%d}</p>",
             '<input id="q" type="search" placeholder="Sök fil…" autocomplete="off">',
             '<nav class="toc">']
    for group in order:
        label = DISPLAY_NAMES.get(group, group.title() if group in CATEGORIES else group or "Filer")
        lines.append(f'<a href="#g-{quote(group or "root")}">{html.escape(label)} ({len(groups[group])})</a>')
    lines.append("</nav>")

    for group in order:
        files = groups[group]
        label = DISPLAY_NAMES.get(group, group.title() if group in CATEGORIES else group or "Filer")
        lines.append(f'<details open id="g-{quote(group or "root")}"><summary>'
                     f'{html.escape(label)} <span class="n">({len(files)})</span></summary>')
        # Sub-folders inside a category (e.g. repos/<repo>/...) get small headings.
        by_sub = {}
        for rel in files:
            inner = rel[len(group) + 1:] if group else rel
            sub = os.path.dirname(inner)
            by_sub.setdefault(sub, []).append((inner, rel))
        for sub in sorted(by_sub, key=natural_key):
            if sub:
                lines.append(f"<h3>{html.escape(sub)}</h3>")
            lines.append("<ul>")
            for inner, rel in sorted(by_sub[sub], key=lambda x: natural_key(x[0])):
                abs_path = os.path.join(course_out, rel)
                name = os.path.basename(inner)
                ext = os.path.splitext(name)[1].lstrip(".")[:5] or "fil"
                size = human_size(os.path.getsize(abs_path))
                is_new = False
                stamp = added.get(rel)
                if stamp:
                    try:
                        is_new = datetime.fromisoformat(stamp).timestamp() >= cutoff
                    except ValueError:
                        pass
                href = "/".join(quote(p) for p in rel.split("/"))
                lines.append(
                    f'<li data-n="{html.escape(fold(rel))}"><span class="ext">{html.escape(ext)}</span>'
                    f'<a href="{href}">{html.escape(name)}</a>'
                    + ('<span class="new">ny</span>' if is_new else "")
                    + f'<span class="meta">{size}</span></li>'
                )
            lines.append("</ul>")
        lines.append("</details>")
    write_page(os.path.join(course_out, "index.html"), course, lines)


def build_root_index():
    """Link every course folder in SITE_DIR, not only the ones in COURSES."""
    os.makedirs(SITE_DIR, exist_ok=True)
    lines = ["<h1>Mina kurser</h1>",
             f'<p class="sub">Uppdaterad {datetime.now():%Y-%m-%d}</p>']
    managed, own = [], []
    for name in sorted(os.listdir(SITE_DIR), key=natural_key):
        folder = os.path.join(SITE_DIR, name)
        if name.startswith(".") or not os.path.isdir(folder):
            continue
        (managed if os.path.exists(os.path.join(folder, "index.html")) else own).append(name)
    for name in managed:
        folder = os.path.join(SITE_DIR, name)
        full = load_json(os.path.join(folder, MANIFEST_NAME)).get("_course_name", "")
        n = len(site_files(folder))
        lines.append(f'<a class="card" href="{quote(name)}/index.html"><b>{html.escape(name)}</b>'
                     f'<div class="sub">{html.escape(full)}{" · " if full else ""}{n} filer</div></a>')
    if own:
        lines.append('<input id="q" type="search" placeholder="Sök i egna mappar…" autocomplete="off">')
    for name in own:
        # Folder you manage yourself: list its files right here.
        files = site_files(os.path.join(SITE_DIR, name))
        lines.append(f'<details><summary>{html.escape(name)} <span class="n">({len(files)})</span>'
                     "</summary><ul>")
        for rel in sorted(files, key=natural_key):
            href = quote(name) + "/" + "/".join(quote(p) for p in rel.split("/"))
            ext = os.path.splitext(rel)[1].lstrip(".")[:5] or "fil"
            lines.append(f'<li data-n="{html.escape(fold(rel))}"><span class="ext">{html.escape(ext)}</span>'
                         f'<a href="{href}">{html.escape(rel)}</a></li>')
        lines.append("</ul></details>")
    write_page(os.path.join(SITE_DIR, "index.html"), "Mina kurser", lines)


def main():
    parser = argparse.ArgumentParser(description="Sort Canvas downloads and build the website.")
    parser.add_argument("courses", nargs="*", help="course folders (default: COURSES)")
    parser.add_argument("--dry-run", action="store_true", help="show what would happen, change nothing")
    parser.add_argument("--explain", action="store_true", help="show the keyword points per file")
    parser.add_argument("--reclassify", action="store_true",
                        help="re-sort files this script placed earlier (never yours)")
    parser.add_argument("--no-ollama", action="store_true", help="use only the keyword rules")
    parser.add_argument("--pages-only", action="store_true", help="only rebuild the index.html pages")
    args = parser.parse_args()
    courses = args.courses or COURSES

    if args.pages_only:
        for course in courses:
            if os.path.isdir(os.path.join(SITE_DIR, course)):
                build_course_page(course)
        build_root_index()
        print("Pages rebuilt.")
        return

    if not os.path.isdir(SOURCE_DIR):
        print(f"No {SOURCE_DIR}/ folder found. Run canvas_download.py first.")
        return

    use_ollama = not args.no_ollama and ollama_ready()
    if not use_ollama:
        print("Using the keyword rules only (start Ollama for unclear files).\n")
    classify = Classifier(use_ollama, explain=args.explain)

    done = sum(1 for course in courses
               if organize_course(course, classify, args.dry_run, args.reclassify or RECLASSIFY))

    if not args.dry_run:
        build_root_index()
    c = classify.counts
    print(f"\nDone. Organized {done} course(s). Sorted by rules: {c['rules']}, "
          f"like similar files: {c['similar']}, by Ollama: {c['ollama']}. Nothing was deleted. Site files are in ./{SITE_DIR}/")


if __name__ == "__main__":
    main()
