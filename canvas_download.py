"""
Download files from a Canvas LMS course using the Canvas API.
 
This script tries multiple sources, in order, and never crashes if one
of them isn't available:
 
1. The course's "Files" tab (fastest, if the professor left it enabled).
2. If Files is disabled: scans Modules, Pages, Assignments, Announcements,
   and the Syllabus for:
     a. Direct Canvas file-download links.
     b. GitHub repo links (e.g. a professor linking course code/materials
        from a GitHub repo instead of uploading to Canvas). If found, the
        entire repo's contents are downloaded automatically.
 
This is plain pattern-matching against Canvas's own API responses --
no AI/Ollama involved in this script (Ollama is only used later, in
organize_and_build_site.py, to sort files you already have).
 
If nothing is found anywhere for a course, the script just says so and
moves on to the next course -- it will not fail or stop the whole run.
 
Setup:
1. Log in to Canvas -> Account -> Settings -> "New Access Token"
   Copy the generated token (you will only see it once).
2. Fill in CANVAS_URL and CANVAS_TOKEN below (or set them as environment
   variables of the same name instead of hardcoding).
3. Find your course ID(s): open the course in Canvas, look at the URL:
   https://canvas.kth.se/courses/12345  -> course ID is 12345
4. Add each course to COURSE_IDS below with a friendly folder name.
5. Run:  pip install requests
         python canvas_download.py
"""
 
import os
import re
from urllib.parse import urlparse
 
import requests
 
CANVAS_URL = os.environ.get("CANVAS_URL", "https://canvas.kth.se")
CANVAS_TOKEN = os.environ.get("CANVAS_TOKEN", "PASTE_YOUR_TOKEN_HERE")
 
# Add one entry per course you want to pull down.
COURSE_IDS = {
   "EL1000": 64209,
   "DD1385": 63900,
   "SF1930": 65047,



}


OUTPUT_DIR = "canvas_downloads"
HEADERS = {"Authorization": f"Bearer {CANVAS_TOKEN}"}
 
GITHUB_LINK_RE = re.compile(r'https?://github\.com/[\w.-]+/[\w.-]+')
# Capture just the numeric file ID out of a Canvas file link, e.g.
# ".../files/10027078/download" or ".../files/10027078/preview" -> "10027078"
CANVAS_FILE_ID_RE = re.compile(r'/files/(\d+)')
 
 
def api_get(url, params=None):
    """GET a Canvas API url. Returns (json_or_None, response_or_None); never raises."""
    try:
        resp = requests.get(url, headers=HEADERS, params=params)
    except requests.RequestException as e:
        print(f"    request failed: {e}")
        return None, None
    if not resp.ok:
        return None, resp
    return resp.json(), resp
 
 
def get_all_pages(url, params=None):
    """Follow Canvas pagination. Returns [] (not an error) if unavailable."""
    results = []
    while url:
        try:
            resp = requests.get(url, headers=HEADERS, params=params)
        except requests.RequestException as e:
            print(f"    request failed: {e}")
            return results
        if not resp.ok:
            return results
        results.extend(resp.json())
        params = None  # only needed on the first request
        url = resp.links.get("next", {}).get("url")
    return results
 
 
def download_canvas_file(file_info, dest_folder):
    os.makedirs(dest_folder, exist_ok=True)
    filename = file_info["display_name"]
    dest_path = os.path.join(dest_folder, filename)
    if os.path.exists(dest_path):
        print(f"    already have: {filename}")
        return True
    try:
        resp = requests.get(file_info["url"], headers=HEADERS)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"    could not download {filename}: {e}")
        return False
    with open(dest_path, "wb") as f:
        f.write(resp.content)
    print(f"    downloaded: {filename}")
    return True
 
 
def try_files_api(course_id, dest_folder):
    """Primary method: the Files tab. Returns True if anything was downloaded."""
    files_url = f"{CANVAS_URL}/api/v1/courses/{course_id}/files"
    files = get_all_pages(files_url, params={"per_page": 100})
    if not files:
        return False
    got_any = False
    for file_info in files:
        if download_canvas_file(file_info, dest_folder):
            got_any = True
    return got_any
 
 
def collect_text_blobs(course_id):
    """Gather text/HTML from Modules, Pages, Syllabus, Assignments, and
    Announcements -- anywhere a professor might drop a link or file."""
    blobs = []
 
    data, _ = api_get(
        f"{CANVAS_URL}/api/v1/courses/{course_id}",
        params={"include[]": "syllabus_body"},
    )
    if data and data.get("syllabus_body"):
        blobs.append(data["syllabus_body"])
 
    pages = get_all_pages(
        f"{CANVAS_URL}/api/v1/courses/{course_id}/pages", params={"per_page": 100}
    )
    for page in pages:
        url_name = page.get("url")
        if not url_name:
            continue
        detail, _ = api_get(f"{CANVAS_URL}/api/v1/courses/{course_id}/pages/{url_name}")
        if detail and detail.get("body"):
            blobs.append(detail["body"])
 
    modules = get_all_pages(
        f"{CANVAS_URL}/api/v1/courses/{course_id}/modules",
        params={"per_page": 100, "include[]": "items"},
    )
    for module in modules:
        for item in module.get("items", []):
            if item.get("type") == "ExternalUrl" and item.get("external_url"):
                blobs.append(item["external_url"])
            if item.get("type") == "Page" and item.get("page_url"):
                detail, _ = api_get(
                    f"{CANVAS_URL}/api/v1/courses/{course_id}/pages/{item['page_url']}"
                )
                if detail and detail.get("body"):
                    blobs.append(detail["body"])
 
    assignments = get_all_pages(
        f"{CANVAS_URL}/api/v1/courses/{course_id}/assignments", params={"per_page": 100}
    )
    for a in assignments:
        if a.get("description"):
            blobs.append(a["description"])
 
    announcements = get_all_pages(
        f"{CANVAS_URL}/api/v1/announcements",
        params={"context_codes[]": f"course_{course_id}", "per_page": 100},
    )
    for a in announcements:
        if a.get("message"):
            blobs.append(a["message"])
 
    return blobs
 
 
def extract_links(blobs):
    github_links = set()
    canvas_file_ids = set()
    for blob in blobs:
        for link in GITHUB_LINK_RE.findall(blob):
            github_links.add(link.rstrip("/"))
        for file_id in CANVAS_FILE_ID_RE.findall(blob):
            canvas_file_ids.add(file_id)
    return github_links, canvas_file_ids
 
 
def download_github_repo(repo_url, dest_folder, subpath=""):
    """Recursively download all files from a public GitHub repo via the API."""
    parts = urlparse(repo_url).path.strip("/").split("/")
    if len(parts) < 2:
        return 0
    owner, repo = parts[0], parts[1]
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{subpath}"
    try:
        resp = requests.get(api_url)
    except requests.RequestException as e:
        print(f"    could not reach GitHub: {e}")
        return 0
    if not resp.ok:
        print(f"    could not list {repo_url}: {resp.status_code}")
        return 0
    count = 0
    for entry in resp.json():
        if entry["type"] == "dir":
            count += download_github_repo(repo_url, dest_folder, entry["path"])
        elif entry["type"] == "file":
            dest_path = os.path.join(dest_folder, entry["path"])
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            if os.path.exists(dest_path):
                continue
            file_resp = requests.get(entry["download_url"])
            if file_resp.ok:
                with open(dest_path, "wb") as f:
                    f.write(file_resp.content)
                print(f"    (from GitHub) downloaded: {entry['path']}")
                count += 1
    return count
 
 
def try_fallback_scan(course_id, dest_folder):
    """When Files is disabled: scan for GitHub links or direct file links instead."""
    print("  Files tab unavailable -- scanning Modules/Pages/Assignments for links...")
    blobs = collect_text_blobs(course_id)
    github_links, canvas_file_ids = extract_links(blobs)
 
    got_any = False
 
    for link in github_links:
        print(f"  Found GitHub link: {link}")
        repo_name = link.split("/")[-1]
        n = download_github_repo(link, os.path.join(dest_folder, f"github_{repo_name}"))
        if n:
            got_any = True
 
    for file_id in canvas_file_ids:
        # Look up real metadata (proper filename, content type) instead of
        # guessing from the URL -- this also naturally skips preview pages,
        # submission pages, and anything that isn't an actual file object.
        file_info, resp = api_get(f"{CANVAS_URL}/api/v1/files/{file_id}")
        if not file_info or "display_name" not in file_info:
            continue
        if download_canvas_file(file_info, dest_folder):
            got_any = True
 
    if not got_any:
        print("  Nothing downloadable found for this course (that's OK, moving on).")
    return got_any
 
 
def main():
    if CANVAS_TOKEN == "PASTE_YOUR_TOKEN_HERE":
        print("Set CANVAS_TOKEN first (edit the script or set an env var).")
        return
 
    for course_name, course_id in COURSE_IDS.items():
        print(f"Course: {course_name}")
        dest_folder = os.path.join(OUTPUT_DIR, course_name)
 
        got_files = try_files_api(course_id, dest_folder)
        if not got_files:
            try_fallback_scan(course_id, dest_folder)
 
    print("\nDone. Check ./canvas_downloads/ -- some courses may have found nothing, that's OK.")
 
 
if __name__ == "__main__":
    main()