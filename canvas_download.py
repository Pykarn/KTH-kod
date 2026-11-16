"""
Download files from Canvas LMS courses using the Canvas API.

The script crawls a course the way a student clicks through it, and collects
every file it can reach:

1. Modules (the "Home" page in many courses) -- every module item:
     File        -> downloaded directly (even if the Files tab is hidden)
     Page        -> saved as an .html file, and every link in it followed
     Assignment  -> instructions saved as .html, links followed
     Discussion / Quiz -> text read, attachments downloaded, links followed
     ExternalUrl -> downloaded if it points to a file (PDF, zip, ...)
2. The front page, the syllabus, all Pages, Assignments, Discussions
   (including replies), Announcements and Quizzes, with attached files.
3. The Files tab, with its folder structure (if the teacher left it enabled).
4. Links found anywhere above are followed:
     - Canvas files, pages, assignments, discussions, quizzes and module
       items in the same course (so a page that is only linked from the
       home page is still found)
     - direct links to files on other sites (e.g. a PDF on kth.se)
     - course web pages on kth.se / github.io: files linked from them
     - public Google Docs / Slides / Sheets / Drive files
     - GitHub repos (downloaded as one zip, not file by file)
   Links that can't be downloaded (YouTube, Kattis, Drive folders, ...) are
   written to canvas_downloads/<course>/.found_links.txt so you can check
   them by hand.

Files from a module are saved in a folder named after the module. A hidden
index (.canvas_index.json) remembers what was downloaded, plus where each
file came from (module, assignment, ...), which organize_and_build_site.py
uses to sort better. A re-run only fetches new and updated files.

No AI/Ollama is used here (Ollama is only used later, in
organize_and_build_site.py, to sort the files).

Setup:
1. Log in to Canvas -> Account -> Settings -> "New Access Token"
   Copy the generated token (you will only see it once).
2. Set the token as an environment variable (or paste it below):
     $env:CANVAS_TOKEN = "ditt-token-här"      # Windows PowerShell
     export CANVAS_TOKEN="ditt-token-här"      # macOS / Linux
3. Find your course IDs:   python canvas_download.py --list-courses
4. Add each course to COURSE_IDS below with a friendly folder name.
5. Run:  pip install requests
         python canvas_download.py              (all courses in COURSE_IDS)
         python canvas_download.py DD1368       (only some courses)
         python canvas_download.py 12345        (any course ID, ad hoc)

Optional: set GITHUB_TOKEN as well for private GitHub repos.


kurser tidigare använda:
 "DD1385": 63900,
 "SF1930": 65047,
 "EL1000": 64209,

"""

import argparse
import html
import json
import os
import re
import sys
import tempfile
import threading
import time
import zipfile
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from urllib.parse import parse_qs, unquote, urljoin, urlparse

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ============================== SETTINGS ===================================

CANVAS_URL = os.environ.get("CANVAS_URL", "https://canvas.kth.se").rstrip("/")
CANVAS_TOKEN = os.environ.get("CANVAS_TOKEN", "PASTE_YOUR_TOKEN_HERE")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")  # optional

# Add one entry per course you want to pull down.
COURSE_IDS = {
    "DD1385": 63900,
    "DD1368": 65330,
    "SF1811": 65491,
}

OUTPUT_DIR = "canvas_downloads"

USE_MODULE_FOLDERS = True       # save module files in a folder per module
SAVE_PAGES_AS_HTML = True       # save Canvas pages / assignment texts as .html
DOWNLOAD_EXTERNAL_FILES = True  # direct file links to other websites
DOWNLOAD_GOOGLE_FILES = True    # public Google Docs/Slides/Sheets/Drive files
DOWNLOAD_GITHUB_REPOS = True    # GitHub repos linked from the course
INCLUDE_DISCUSSION_REPLIES = True  # attachments/links in discussion replies
# Web pages on these sites (and their subdomains) that the course links to
# are opened, and files linked from them are downloaded (one level deep).
FOLLOW_PAGES_ON = ("kth.se", "github.io")
MAX_FILE_MB = 500               # skip single files bigger than this
PARALLEL_DOWNLOADS = 4          # files downloaded at the same time

# A link to another website is downloaded only if it ends in one of these.
EXTERNAL_FILE_EXTS = {
    ".pdf", ".zip", ".tar", ".gz", ".tgz", ".7z", ".rar",
    ".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx", ".odt", ".odp", ".ods",
    ".csv", ".tsv", ".json", ".xml", ".txt", ".md", ".tex", ".bib",
    ".py", ".ipynb", ".java", ".c", ".h", ".cpp", ".hpp", ".cs", ".js", ".ts",
    ".go", ".rs", ".hs", ".m", ".mlx", ".mat", ".r", ".rmd", ".sql", ".db",
    ".sqlite", ".jar", ".png", ".jpg", ".jpeg", ".gif", ".svg",
}

# ===========================================================================

CANVAS_HOST = urlparse(CANVAS_URL).netloc.lower()
INDEX_NAME = ".canvas_index.json"
LINKS_NAME = ".found_links.txt"
PRINT_LOCK = threading.Lock()


def log(msg):
    with PRINT_LOCK:
        print(msg, flush=True)


def make_session():
    s = requests.Session()
    retry = Retry(
        total=4,
        backoff_factor=1.5,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
        respect_retry_after_header=True,
    )
    adapter = HTTPAdapter(max_retries=retry, pool_maxsize=max(10, PARALLEL_DOWNLOADS * 2))
    s.mount("https://", adapter)
    s.mount("http://", adapter)
    s.headers["User-Agent"] = "KTH-kod canvas_download.py"
    return s


SESSION = make_session()


def auth_headers(url):
    """The Canvas token is only ever sent to Canvas itself, never to other sites."""
    host = urlparse(url).netloc.lower()
    if host == CANVAS_HOST:
        return {"Authorization": f"Bearer {CANVAS_TOKEN}"}
    if GITHUB_TOKEN and host == "api.github.com":
        return {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    return {}


def http_get(url, params=None, stream=False):
    """GET with retries (including Canvas' own 403 rate limit). Never raises."""
    resp = None
    for attempt in range(5):
        try:
            resp = SESSION.get(url, headers=auth_headers(url), params=params,
                               stream=stream, timeout=(15, 120))
        except requests.RequestException as e:
            log(f"    request failed: {e}")
            return None
        if resp.status_code == 403 and "rate limit" in resp.text.lower():
            time.sleep(2 * (attempt + 1))
            continue
        return resp
    return resp


def api_json(url, params=None):
    resp = http_get(url, params)
    if resp is None or not resp.ok:
        return None
    try:
        return resp.json()
    except ValueError:
        return None


def api_list(url, params=None):
    """Follow Canvas pagination. Returns (items, status) -- status is the HTTP
    code of the first request, or None if it could not be reached."""
    params = dict(params or {})
    params.setdefault("per_page", 100)
    results, status = [], None
    while url:
        resp = http_get(url, params)
        if resp is None:
            break
        if status is None:
            status = resp.status_code
        if not resp.ok:
            break
        try:
            data = resp.json()
        except ValueError:
            break
        if isinstance(data, list):
            results.extend(data)
        else:
            break
        params = None  # the "next" link already carries the parameters
        url = resp.links.get("next", {}).get("url")
    return results, status


# ----------------------------- filenames -----------------------------------

_BAD_CHARS = re.compile(r'[<>:"/\\|?*\x00-\x1f]')
_WIN_RESERVED = {"CON", "PRN", "AUX", "NUL", *(f"COM{i}" for i in range(1, 10)),
                 *(f"LPT{i}" for i in range(1, 10))}


def safe_name(name, fallback="file"):
    """Make a name that works as a file/folder name on Windows, macOS and Linux."""
    name = html.unescape(unquote(str(name or ""))).strip()
    name = _BAD_CHARS.sub("_", name)
    name = re.sub(r"\s+", " ", name).strip(" .")
    if not name:
        name = fallback
    stem, ext = os.path.splitext(name)
    if stem.upper() in _WIN_RESERVED:
        stem = "_" + stem
    if len(stem) > 120:
        stem = stem[:120].rstrip(" .")
    return stem + ext


def filename_from_response(resp, url, fallback="download"):
    cd = resp.headers.get("Content-Disposition", "")
    m = re.search(r"filename\*\s*=\s*[^']*''([^;]+)", cd, re.I)
    if m:
        return safe_name(unquote(m.group(1)), fallback)
    m = re.search(r'filename\s*=\s*"?([^";]+)"?', cd, re.I)
    if m:
        return safe_name(m.group(1), fallback)
    base = os.path.basename(urlparse(resp.url or url).path)
    return safe_name(base, fallback)


def text_length(html_text):
    return len(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html_text or "")).strip())


def host_matches(host, suffixes):
    host = host.lower()
    return any(host == s or host.endswith("." + s) for s in suffixes)


# ----------------------------- link parsing --------------------------------

ATTR_LINK_RE = re.compile(
    r'''(?:href|src|data-api-endpoint|data-url)\s*=\s*["']([^"']+)["']''', re.I)
BARE_LINK_RE = re.compile(r'''https?://[^\s"'<>()\[\]{}]+''')

RE_FILE = re.compile(r"^/(?:api/v1/)?(?:(courses|users|groups)/(\d+)/)?files/(\d+)")
RE_PAGE = re.compile(r"^/(?:api/v1/)?courses/(\d+)/(?:pages|wiki)/([^/?#]+)")
RE_MODITEM = re.compile(r"^/(?:api/v1/)?courses/(\d+)/modules/items/(\d+)")
RE_MODULE = re.compile(r"^/(?:api/v1/)?courses/(\d+)/modules(?:/|$)")
RE_ASSIGN = re.compile(r"^/(?:api/v1/)?courses/(\d+)/assignments/(\d+)")
RE_DISC = re.compile(r"^/(?:api/v1/)?courses/(\d+)/(?:discussion_topics|announcements)/(\d+)")
RE_QUIZ = re.compile(r"^/(?:api/v1/)?courses/(\d+)/quizzes/(\d+)")

GITHUB_RESERVED = {
    "orgs", "settings", "features", "topics", "marketplace", "sponsors",
    "login", "logout", "join", "about", "pricing", "apps", "explore",
    "collections", "trending", "enterprise", "customer-stories", "security",
    "site", "contact", "search", "notifications", "new", "codespaces",
}


def extract_links(text, base=None):
    """All URLs in an HTML/text blob, absolute, de-duplicated, in order."""
    if not text:
        return []
    text = html.unescape(text)
    base = base or CANVAS_URL + "/"
    seen, out = set(), []
    for raw in ATTR_LINK_RE.findall(text) + BARE_LINK_RE.findall(text):
        raw = raw.strip().rstrip(".,;:!")
        if not raw or raw.startswith(("#", "mailto:", "tel:", "javascript:", "data:")):
            continue
        url = urljoin(base, raw).split("#")[0]
        if url and url not in seen:
            seen.add(url)
            out.append(url)
    return out


# ----------------------------- the crawler ---------------------------------

class CourseCrawler:
    def __init__(self, name, course_id):
        self.name = name
        self.cid = str(course_id)
        self.dest = os.path.join(OUTPUT_DIR, name)
        self.api = f"{CANVAS_URL}/api/v1/courses/{self.cid}"
        os.makedirs(self.dest, exist_ok=True)

        self.index = self._load_index()
        self.lock = threading.Lock()
        self.pool = ThreadPoolExecutor(max_workers=max(1, PARALLEL_DOWNLOADS))
        self.jobs = []
        self.reserved = set()         # paths picked for downloads still running
        self.done_files = set()       # Canvas file ids handled this run
        self.done_content = set()     # ("page", slug), ("assignment", id), ...
        self.done_external = set()    # external URLs handled this run
        self.module_items = {}        # module item id -> (item, module folder)
        self.github = {}              # (owner, repo) -> {"ref": ..., "subs": set}
        self.other_links = {}         # url -> where it was found
        self.problems = []            # human-readable notes
        self.stats = {"new": 0, "updated": 0, "unchanged": 0, "failed": 0}

    # ----- index -------------------------------------------------------
    def _load_index(self):
        path = os.path.join(self.dest, INDEX_NAME)
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
        except (OSError, ValueError):
            data = {}
        for table in ("files", "external", "pages"):
            data.setdefault(table, {})
        return data

    def _save_index(self):
        path = os.path.join(self.dest, INDEX_NAME)
        self.index["updated"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(self.index, f, indent=1, ensure_ascii=False, sort_keys=True)
        os.replace(tmp, path)

    def _claimed_paths(self):
        paths = set(self.reserved)
        for table in ("files", "external", "pages"):
            paths |= {rec.get("path") for rec in self.index[table].values()}
        return paths

    def _count(self, key):
        with self.lock:
            self.stats[key] += 1

    def _problem(self, msg):
        with self.lock:
            self.problems.append(msg)

    # ----- low-level download -----------------------------------------
    def _stream_to(self, resp, rel_path):
        """Write a streamed response to dest/rel_path via a temp file, so an
        interrupted download never leaves a half-written file behind."""
        abs_path = os.path.join(self.dest, rel_path)
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)
        limit = MAX_FILE_MB * 1024 * 1024
        written = 0
        fd, tmp = tempfile.mkstemp(prefix=".part_", dir=os.path.dirname(abs_path))
        try:
            with os.fdopen(fd, "wb") as f:
                for chunk in resp.iter_content(chunk_size=1 << 16):
                    written += len(chunk)
                    if written > limit:
                        raise ValueError(f"bigger than {MAX_FILE_MB} MB")
                    f.write(chunk)
            os.replace(tmp, abs_path)
        except BaseException:
            if os.path.exists(tmp):
                os.remove(tmp)
            raise
        finally:
            resp.close()
        return written

    def _pick_path(self, subdir, filename, size=None, key=None, table="files"):
        """Where to save a file. Re-uses the path from the index; adopts a file
        an older version of this script saved at the top level; otherwise
        picks a free name in subdir. Returns (path, already_exists)."""
        rec = self.index[table].get(key) if key else None
        if rec and os.path.exists(os.path.join(self.dest, rec["path"])):
            return rec["path"], True
        claimed = self._claimed_paths()
        legacy = filename
        if (table == "files" and legacy not in claimed and size is not None
                and os.path.isfile(os.path.join(self.dest, legacy))
                and os.path.getsize(os.path.join(self.dest, legacy)) == size):
            return legacy, True
        rel = os.path.join(subdir, filename) if subdir else filename
        rel = rel.replace(os.sep, "/")
        stem, ext = os.path.splitext(rel)
        n = 2
        while rel in claimed or os.path.exists(os.path.join(self.dest, rel)):
            rel = f"{stem} ({n}){ext}"
            n += 1
        return rel, False

    # ----- Canvas files ------------------------------------------------
    def get_file_info(self, file_id, course_id=None):
        for url in (f"{CANVAS_URL}/api/v1/courses/{course_id or self.cid}/files/{file_id}",
                    f"{CANVAS_URL}/api/v1/files/{file_id}"):
            info = api_json(url)
            if info and "display_name" in info:
                return info
        return None

    def download_file_id(self, file_id, subdir, origin, course_id=None, direct_url=None):
        file_id = str(file_id)
        if file_id in self.done_files:
            return
        info = self.get_file_info(file_id, course_id)
        if info:
            self.download_file_info(info, subdir, origin)
        elif direct_url and "verifier=" in direct_url:
            # Not visible through the API, but a public "verifier" link works.
            self.done_files.add(file_id)
            if not self._download_plain(direct_url, subdir, origin, key=f"canvas:{file_id}"):
                self._problem(f"file {file_id} (linked from {origin}) is not accessible")
        else:
            self.done_files.add(file_id)
            self._problem(f"file {file_id} (linked from {origin}) is not accessible")

    def download_file_info(self, info, subdir, origin):
        """Decide where a Canvas file goes (here, in order) and queue the
        actual download, which runs in parallel."""
        fid = str(info.get("id"))
        if fid in self.done_files:
            return
        self.done_files.add(fid)
        name = safe_name(info.get("display_name") or info.get("filename"), f"file_{fid}")
        url = info.get("url")
        if info.get("locked_for_user") or info.get("hidden_for_user") or not url:
            reason = info.get("lock_explanation") or "locked or hidden"
            reason = re.sub(r"<[^>]+>", "", reason).strip()
            self._problem(f"{name}: {reason} (from {origin})")
            return
        size = info.get("size")
        if size and size > MAX_FILE_MB * 1024 * 1024:
            self._problem(f"{name}: skipped, {size // 2**20} MB > MAX_FILE_MB")
            return

        version = info.get("modified_at") or info.get("updated_at")
        rec = self.index["files"].get(fid) or {}
        rel, existing = self._pick_path(subdir, name, size, key=fid)
        meta = {"path": rel, "version": version, "size": size,
                "module": rec.get("module", subdir), "origin": rec.get("origin", origin),
                "content_type": info.get("content-type") or info.get("mime_class")}
        abs_path = os.path.join(self.dest, rel)
        if existing and os.path.exists(abs_path):
            same_size = size is None or os.path.getsize(abs_path) == size
            same_version = not rec or rec.get("version") == version
            if same_size and same_version:
                with self.lock:
                    self.index["files"][fid] = meta
                self._count("unchanged")
                return

        self.reserved.add(rel)
        self.jobs.append(self.pool.submit(self._download_job, fid, name, url, rel, existing, meta))

    def _download_job(self, fid, name, url, rel, existing, meta):
        error = None
        for attempt in range(3):
            resp = http_get(url, stream=True)
            if resp is None or not resp.ok:
                error = resp.status_code if resp is not None else "no response"
                if resp is not None and resp.status_code in (401, 403, 404):
                    break
                continue
            try:
                self._stream_to(resp, rel)
                error = None
                break
            except ValueError as e:      # too big
                error = e
                break
            except (requests.RequestException, OSError) as e:
                error = e                 # connection dropped: try again
                time.sleep(2 * (attempt + 1))
        if error is not None:
            self._problem(f"{name}: download failed ({error})")
            self._count("failed")
            return
        with self.lock:
            self.index["files"][fid] = meta
        if existing:
            self._count("updated")
            log(f"    updated:    {rel}")
        else:
            self._count("new")
            log(f"    downloaded: {rel}")

    def wait_for_downloads(self):
        for job in self.jobs:
            try:
                job.result()
            except Exception as e:  # never let one file stop the run
                self._problem(f"download crashed: {e}")
        self.jobs = []
        self.reserved = set()

    # ----- Canvas pages / assignment texts saved as HTML --------------
    def save_html(self, key, title, body, subdir, origin, version=None, extra=""):
        if not SAVE_PAGES_AS_HTML or text_length(body) < 200:
            return
        rec = self.index["pages"].get(key)
        if rec and rec.get("version") == version and version and \
                os.path.exists(os.path.join(self.dest, rec["path"])):
            return
        name = safe_name(title, "page") + ".html"
        rel, _ = self._pick_path(subdir, name, key=key, table="pages")
        doc = (
            "<!DOCTYPE html><html><head><meta charset='utf-8'>"
            f"<base href='{html.escape(CANVAS_URL)}/'>"
            f"<title>{html.escape(title)}</title>"
            "<style>body{font-family:system-ui,sans-serif;max-width:50rem;margin:2rem auto;"
            "padding:0 1rem;line-height:1.5}img{max-width:100%}</style></head><body>"
            f"<h1>{html.escape(title)}</h1>{extra}\n{body}\n</body></html>"
        )
        abs_path = os.path.join(self.dest, rel)
        self.index["pages"][key] = {"path": rel, "version": version, "module": subdir,
                                    "origin": origin}
        if os.path.exists(abs_path):
            with open(abs_path, encoding="utf-8", errors="ignore") as f:
                if f.read() == doc:
                    return
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)
        with open(abs_path, "w", encoding="utf-8") as f:
            f.write(doc)
        log(f"    saved page: {rel}")

    # ----- other websites ---------------------------------------------
    def _download_plain(self, url, subdir, origin, key=None, fallback_name="download"):
        """Download a file from a URL without the Canvas API. Returns True if a
        real file (not an HTML page) was saved or already present."""
        key = key or url
        rec = self.index["external"].get(key)
        if rec and os.path.exists(os.path.join(self.dest, rec["path"])):
            self._count("unchanged")
            return True
        resp = http_get(url, stream=True)
        if resp is None or not resp.ok:
            return False
        ctype = resp.headers.get("Content-Type", "").lower()
        if "text/html" in ctype:
            resp.close()
            return False  # a web page / login page, not a file
        name = filename_from_response(resp, url, fallback_name)
        if not os.path.splitext(name)[1]:
            ext = {"application/pdf": ".pdf", "application/zip": ".zip"}.get(ctype.split(";")[0])
            name += ext or ""
        rel, _ = self._pick_path(subdir, name, table="external")
        try:
            self._stream_to(resp, rel)
        except Exception as e:
            self._problem(f"{url}: download failed ({e})")
            self._count("failed")
            return False
        self.index["external"][key] = {"path": rel, "url": url, "module": subdir,
                                       "origin": origin}
        self._count("new")
        log(f"    downloaded: {rel}  (from {urlparse(url).netloc})")
        return True

    def handle_external(self, url, subdir, origin, depth=0):
        if url in self.done_external:
            return
        self.done_external.add(url)
        p = urlparse(url)
        host = (p.hostname or "").lower()
        if host.startswith("www."):
            host = host[4:]
        ext = os.path.splitext(unquote(p.path))[1].lower()

        if host == "github.com":
            if self._note_github(p):
                return
        elif host in ("docs.google.com", "drive.google.com"):
            if DOWNLOAD_GOOGLE_FILES and self._download_google(p, url, subdir, origin):
                return
        elif host == "raw.githubusercontent.com" or ext in EXTERNAL_FILE_EXTS:
            if DOWNLOAD_EXTERNAL_FILES and self._download_plain(url, subdir, origin):
                return
        elif depth == 0 and DOWNLOAD_EXTERNAL_FILES and host_matches(host, FOLLOW_PAGES_ON):
            if self._scan_external_page(url, subdir, origin):
                return
        self.other_links.setdefault(url, origin)

    def _scan_external_page(self, url, subdir, origin):
        """Open a course web page (e.g. on kth.se) and fetch the files it links."""
        resp = http_get(url)
        if resp is None or not resp.ok or "text/html" not in resp.headers.get("Content-Type", ""):
            return False
        found = 0
        for link in extract_links(resp.text[:3_000_000], base=resp.url)[:300]:
            lp = urlparse(link)
            link_ext = os.path.splitext(unquote(lp.path))[1].lower()
            is_github = (lp.hostname or "").lower() in ("github.com", "www.github.com")
            if link_ext in EXTERNAL_FILE_EXTS or is_github:
                self.handle_external(link, subdir, f"{origin} -> {url}", depth=1)
                found += link in self.index["external"] or is_github
        if found:
            log(f"    {found} files from web page {url}")
        return found > 0

    def _download_google(self, p, url, subdir, origin):
        m = re.search(r"/(document|presentation|spreadsheets|file)/d/([\w-]+)", p.path)
        gid = m.group(2) if m else parse_qs(p.query).get("id", [None])[0]
        if not gid:
            return False
        kind = m.group(1) if m else "file"
        export = {
            "document": f"https://docs.google.com/document/d/{gid}/export?format=pdf",
            "presentation": f"https://docs.google.com/presentation/d/{gid}/export/pdf",
            "spreadsheets": f"https://docs.google.com/spreadsheets/d/{gid}/export?format=xlsx",
            "file": f"https://drive.google.com/uc?export=download&id={gid}",
        }[kind]
        return self._download_plain(export, subdir, origin, key=f"google:{gid}",
                                    fallback_name=f"google_{kind}_{gid}")

    # ----- GitHub ------------------------------------------------------
    def _note_github(self, p):
        if not DOWNLOAD_GITHUB_REPOS:
            return False
        parts = [x for x in p.path.split("/") if x]
        if len(parts) < 2 or parts[0].lower() in GITHUB_RESERVED:
            return False
        owner, repo = parts[0], re.sub(r"\.git$", "", parts[1])
        ref, sub = None, None
        if len(parts) >= 4 and parts[2] in ("tree", "blob"):
            ref, sub = parts[3], "/".join(parts[4:]) or None
        entry = self.github.setdefault((owner, repo), {"ref": ref, "subs": set()})
        entry["subs"].add(sub)  # None means "the whole repo"
        if ref and not entry["ref"]:
            entry["ref"] = ref
        return True

    def download_github_repos(self):
        for (owner, repo), entry in sorted(self.github.items()):
            log(f"  GitHub: {owner}/{repo}")
            subs = None if None in entry["subs"] else entry["subs"]
            n = self._download_github(owner, repo, entry["ref"], subs)
            if n is None and entry["ref"]:
                n = self._download_github(owner, repo, None, subs)
            if n is None:
                self.other_links.setdefault(f"https://github.com/{owner}/{repo}",
                                            "GitHub (could not download)")

    def _download_github(self, owner, repo, ref, subs):
        """Download a repo as one zip. Returns number of new/changed files,
        or None if the repo could not be downloaded."""
        # The archive link has no API rate limit; the API is the fallback
        # (and works for private repos when GITHUB_TOKEN is set).
        resp = None
        for url in (f"https://github.com/{owner}/{repo}/archive/{ref or 'HEAD'}.zip",
                    f"https://api.github.com/repos/{owner}/{repo}/zipball" + (f"/{ref}" if ref else "")):
            resp = http_get(url, stream=True)
            if resp is not None and resp.ok:
                break
        if resp is None or not resp.ok:
            code = resp.status_code if resp is not None else "no response"
            log(f"    could not download ({code})")
            return None
        folder = os.path.join(self.dest, f"github_{safe_name(repo)}")
        fd, tmp = tempfile.mkstemp(suffix=".zip")
        os.close(fd)
        changed = 0
        try:
            with open(tmp, "wb") as f:
                for chunk in resp.iter_content(1 << 16):
                    f.write(chunk)
            with zipfile.ZipFile(tmp) as z:
                for member in z.infolist():
                    if member.is_dir():
                        continue
                    rel = member.filename.split("/", 1)[-1]  # drop "repo-sha/"
                    if subs and not any(rel == s or rel.startswith(s.rstrip("/") + "/")
                                        for s in subs):
                        continue
                    raw_parts = [x for x in rel.split("/") if x not in ("", ".", "..")]
                    if not raw_parts or ".git" in raw_parts:
                        continue
                    parts = [safe_name(x) for x in raw_parts]
                    out = os.path.join(folder, *parts)
                    data = z.read(member)
                    if os.path.isfile(out):
                        with open(out, "rb") as f:
                            if f.read() == data:
                                continue
                    os.makedirs(os.path.dirname(out), exist_ok=True)
                    with open(out, "wb") as f:
                        f.write(data)
                    changed += 1
        except (zipfile.BadZipFile, OSError, requests.RequestException) as e:
            log(f"    could not unpack: {e}")
            return None
        finally:
            os.remove(tmp)
        log(f"    {changed} new/changed files in github_{safe_name(repo)}/")
        self.stats["new"] += changed
        return changed

    # ----- following links in HTML ------------------------------------
    def scan_html(self, text, subdir, origin):
        for url in extract_links(text):
            self.follow_link(url, subdir, origin)

    def follow_link(self, url, subdir, origin):
        p = urlparse(url)
        if p.netloc.lower() != CANVAS_HOST:
            if p.scheme in ("http", "https"):
                self.handle_external(url, subdir, origin)
            return
        path = unquote(p.path)

        m = RE_FILE.match(path)
        if m:
            course_id = m.group(2) if m.group(1) == "courses" else None
            self.download_file_id(m.group(3), subdir, origin, course_id, direct_url=url)
            return
        preview = parse_qs(p.query).get("preview", [""])[0]
        if "/files" in path and preview.isdigit():  # /courses/1/files?preview=123
            self.download_file_id(preview, subdir, origin, direct_url=url)
            return

        m = RE_MODITEM.match(path)
        if m and m.group(1) == self.cid:
            found = self.module_items.get(m.group(2))
            if found:
                item, module_folder = found
                self.visit_module_item(item, module_folder)
            return
        if RE_MODULE.match(path):
            return  # modules are all crawled anyway
        for regex, kind in ((RE_PAGE, "page"), (RE_ASSIGN, "assignment"),
                            (RE_DISC, "discussion"), (RE_QUIZ, "quiz")):
            m = regex.match(path)
            if m:
                if m.group(1) == self.cid:
                    self.visit(kind, m.group(2), subdir)
                return

    # ----- Canvas content ---------------------------------------------
    def visit(self, kind, ident, subdir, data=None):
        key = (kind, str(ident))
        if key in self.done_content:
            return
        self.done_content.add(key)
        if kind == "page":
            data = data if data and "body" in data else api_json(f"{self.api}/pages/{ident}")
            if data and not data.get("locked_for_user"):
                title = data.get("title") or str(ident)
                origin = f"page '{title}'"
                self.save_html(f"page:{data.get('url', ident)}", title, data.get("body"),
                               subdir, origin, data.get("updated_at"))
                self.scan_html(data.get("body"), subdir, origin)
        elif kind == "assignment":
            data = data or api_json(f"{self.api}/assignments/{ident}")
            if data:
                title = data.get("name") or str(ident)
                origin = f"assignment '{title}'"
                due = data.get("due_at")
                extra = f"<p><b>Deadline:</b> {html.escape(due)}</p>" if due else ""
                self.save_html(f"assignment:{ident}", title, data.get("description"),
                               subdir, origin, data.get("updated_at"), extra)
                self.scan_html(data.get("description"), subdir, origin)
        elif kind == "discussion":
            data = data or api_json(f"{self.api}/discussion_topics/{ident}")
            if data:
                self._visit_discussion(data, subdir)
        elif kind == "quiz":
            data = data or api_json(f"{self.api}/quizzes/{ident}")
            if data:
                self.scan_html(data.get("description"), subdir,
                               f"quiz '{data.get('title', ident)}'")

    def _visit_discussion(self, data, subdir):
        title = data.get("title") or str(data.get("id"))
        origin = f"discussion '{title}'"
        self.scan_html(data.get("message"), subdir, origin)
        for att in data.get("attachments") or []:
            self.download_file_info(att, subdir, origin)
        if INCLUDE_DISCUSSION_REPLIES and data.get("discussion_subentry_count"):
            view = api_json(f"{self.api}/discussion_topics/{data.get('id')}/view") or {}
            stack = list(view.get("view") or [])
            while stack:
                entry = stack.pop()
                self.scan_html(entry.get("message"), subdir, f"{origin} (reply)")
                atts = entry.get("attachments") or ([entry["attachment"]] if entry.get("attachment") else [])
                for att in atts:
                    self.download_file_info(att, subdir, f"{origin} (reply)")
                stack.extend(entry.get("replies") or [])

    def visit_module_item(self, item, subdir):
        kind = item.get("type")
        origin = f"module item '{item.get('title')}'"
        if kind == "File":
            info = api_json(item["url"]) if item.get("url") else None
            if info and "display_name" in info:
                self.download_file_info(info, subdir, origin)
            elif item.get("content_id"):
                self.download_file_id(item["content_id"], subdir, origin)
        elif kind == "Page" and item.get("page_url"):
            self.visit("page", item["page_url"], subdir)
        elif kind == "Assignment" and item.get("content_id"):
            self.visit("assignment", item["content_id"], subdir)
        elif kind == "Discussion" and item.get("content_id"):
            self.visit("discussion", item["content_id"], subdir)
        elif kind == "Quiz" and item.get("content_id"):
            self.visit("quiz", item["content_id"], subdir)
        elif kind == "ExternalUrl" and item.get("external_url"):
            self.follow_link(item["external_url"], subdir, origin)
        elif kind == "ExternalTool":
            self.other_links.setdefault(item.get("html_url") or item.get("title"),
                                        f"{origin} (external tool, open in Canvas)")

    # ----- the sources, in order ---------------------------------------
    def crawl_modules(self):
        modules, status = api_list(f"{self.api}/modules", {"include[]": "items"})
        if status and status >= 400:
            log(f"  Modules: not available ({status})")
            return
        log(f"  Modules: {len(modules)}")
        for module in modules:
            items = module.get("items")
            if items is None and module.get("items_url"):  # big modules
                items, _ = api_list(module["items_url"])
            module["items"] = items or []
            folder = safe_name(module.get("name"), "module") if USE_MODULE_FOLDERS else ""
            for item in module["items"]:
                self.module_items[str(item.get("id"))] = (item, folder)
        for module in modules:
            folder = safe_name(module.get("name"), "module") if USE_MODULE_FOLDERS else ""
            for item in module["items"]:
                self.visit_module_item(item, folder)

    def crawl_front_and_syllabus(self, course):
        if course.get("syllabus_body"):
            log("  Syllabus")
            self.save_html("syllabus", "Syllabus", course["syllabus_body"], "", "syllabus")
            self.scan_html(course["syllabus_body"], "", "syllabus")
        front = api_json(f"{self.api}/front_page")
        if front and front.get("body"):
            log("  Front page")
            self.visit("page", front.get("url") or "front_page", "", data=front)

    def crawl_lists(self):
        pages, _ = api_list(f"{self.api}/pages")
        assignments, _ = api_list(f"{self.api}/assignments")
        discussions, _ = api_list(f"{self.api}/discussion_topics")
        announcements, _ = api_list(f"{CANVAS_URL}/api/v1/announcements",
                                    {"context_codes[]": f"course_{self.cid}",
                                     "start_date": "2000-01-01", "end_date": "2100-01-01"})
        quizzes, _ = api_list(f"{self.api}/quizzes")
        log(f"  Pages: {len(pages)}, assignments: {len(assignments)}, "
            f"discussions: {len(discussions)}, announcements: {len(announcements)}, "
            f"quizzes: {len(quizzes)}")
        for page in pages:
            if page.get("url"):
                self.visit("page", page["url"], "")
        for a in assignments:
            self.visit("assignment", a.get("id"), "", data=a)
        for d in discussions + announcements:
            self.visit("discussion", d.get("id"), "", data=d)
        for q in quizzes:
            self.visit("quiz", q.get("id"), "", data=q)

    def crawl_files_tab(self):
        files, status = api_list(f"{self.api}/files")
        if status and status >= 400:
            log(f"  Files tab: hidden/not available ({status}) -- using links instead")
            return
        folders, _ = api_list(f"{self.api}/folders")
        folder_path = {}
        for fo in folders:
            parts = (fo.get("full_name") or "").split("/")[1:]  # drop "course files"
            folder_path[fo.get("id")] = "/".join(safe_name(x) for x in parts)
        log(f"  Files tab: {len(files)} files")
        for info in files:
            folder = folder_path.get(info.get("folder_id"), "")
            self.download_file_info(info, folder, f"Files tab{' / ' + folder if folder else ''}")

    # ----- run ---------------------------------------------------------
    def run(self):
        log(f"\nCourse: {self.name} ({self.cid})")
        course = api_json(self.api, {"include[]": "syllabus_body"})
        if not course:
            log("  Could not open the course -- check the course ID and your token.")
            return
        log(f"  {course.get('name', '')}")
        self.index["course_name"] = course.get("name")
        self.index["course_code"] = course.get("course_code")
        try:
            self.crawl_modules()           # first: gives files their module folder
            self.crawl_front_and_syllabus(course)
            self.crawl_lists()
            self.crawl_files_tab()
            self.wait_for_downloads()
            self.download_github_repos()
        except KeyboardInterrupt:
            self.pool.shutdown(wait=True, cancel_futures=True)
            raise
        finally:
            self.pool.shutdown(wait=True)
            self._save_index()
            self._write_links()
        s = self.stats
        log(f"  => {s['new']} new, {s['updated']} updated, {s['unchanged']} unchanged, "
            f"{s['failed']} failed")
        if self.problems:
            log(f"  Not downloaded ({len(self.problems)}):")
            for p in self.problems[:15]:
                log(f"    - {p}")
            if len(self.problems) > 15:
                log(f"    ... and {len(self.problems) - 15} more (see {LINKS_NAME})")
        if self.other_links:
            log(f"  {len(self.other_links)} other links (videos, tools, web pages) "
                f"listed in {os.path.join(self.dest, LINKS_NAME)}")

    def _write_links(self):
        path = os.path.join(self.dest, LINKS_NAME)
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"Links in {self.name} that were not downloaded automatically.\n\n")
            for url, origin in sorted(self.other_links.items(), key=lambda kv: str(kv[0])):
                f.write(f"{url}\n    found in: {origin}\n")
            if self.problems:
                f.write("\nFiles that could not be downloaded:\n")
                for p in self.problems:
                    f.write(f"  - {p}\n")


def list_courses():
    courses, status = api_list(f"{CANVAS_URL}/api/v1/courses",
                               {"include[]": "term", "state[]": ["available", "completed"]})
    if not courses:
        print(f"Could not list courses ({status}). Check CANVAS_TOKEN.")
        return 1
    print(f"{'ID':>8}  {'Code':<10} {'Term':<12} Name")
    for c in sorted(courses, key=lambda c: str((c.get("term") or {}).get("name", "")), reverse=True):
        if not c.get("name"):
            continue
        term = (c.get("term") or {}).get("name", "")
        print(f"{c.get('id'):>8}  {str(c.get('course_code', ''))[:10]:<10} {term[:12]:<12} {c['name']}")
    print('\nAdd a line like  "DD1368": 65330,  to COURSE_IDS in this file.')
    return 0


def main():
    parser = argparse.ArgumentParser(description="Download course files from Canvas.")
    parser.add_argument("courses", nargs="*",
                        help="course names from COURSE_IDS, or Canvas course IDs "
                             "(default: all courses in COURSE_IDS)")
    parser.add_argument("--list-courses", action="store_true",
                        help="show your Canvas courses and their IDs")
    args = parser.parse_args()

    if CANVAS_TOKEN == "PASTE_YOUR_TOKEN_HERE":
        print("Set CANVAS_TOKEN first (edit the script or set an env var).")
        return 1
    if args.list_courses:
        return list_courses()

    selected = {}
    for c in args.courses or COURSE_IDS:
        if c in COURSE_IDS:
            selected[c] = COURSE_IDS[c]
        elif str(c).isdigit():
            name = next((k for k, v in COURSE_IDS.items() if str(v) == c), c)
            selected[name] = int(c)
        else:
            print(f"Unknown course '{c}' -- add it to COURSE_IDS or give the course ID.")
            return 1

    for name, course_id in selected.items():
        try:
            CourseCrawler(name, course_id).run()
        except KeyboardInterrupt:
            print("\nStopped. Files downloaded so far are kept.")
            return 1

    print(f"\nDone. Check ./{OUTPUT_DIR}/ -- then run organize_and_build_site.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
