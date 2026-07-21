#!/usr/bin/env python3
import json, re, requests
from os import environ

GH_TOKEN = environ.get("GITHUB_TOKEN")
RELEASES_URL = "https://api.github.com/repos/{}/releases?per_page=100&page={}"

FILE_NAME = "repo.json"

global session

def download_asset(url, filename):
    with session.get(url, stream=True) as r:
        r.raise_for_status()
        with open(filename, "wb") as f:
            for chunk in r.iter_content(8192):
                f.write(chunk)

def process_repo(repo_path, patterns):
    page = 1
    while True:
        resp = session.get(RELEASES_URL.format(repo_path, page))

        if resp.status_code != 200:
            print(f"{repo_path} error: {resp.status_code}.")
            return
        
        resp.raise_for_status()
        releases = resp.json()

        if not releases: break
        for release in releases:
            for asset in release.get("assets", []):
                name = asset["name"]
                if all(re.search(p, name) for p in patterns):
                    download_asset(asset["browser_download_url"], name)
        if len(releases) < 100: break
        page += 1

def traverse(obj):
    if isinstance(obj, dict):
        if "url" in obj and "pattern" in obj:
            m = re.match(r"https://github\.com/([^/]+/[^/]+)/releases", obj["url"])
            if m: process_repo(m.group(1), obj["pattern"])
        else:
            for v in obj.values():
                traverse(v)
    elif isinstance(obj, list):
        for item in obj:
            traverse(item)

def main():
    with open(FILE_NAME) as f:
        traverse(json.load(f))

def setSession():
    global session
    session = requests.Session()
    session.headers.update({
        "Authorization": f"token {GH_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    })

if __name__ == "__main__":
    if not GH_TOKEN: raise ValueError("GITHUB_TOKEN is empty.")
    setSession()
    main()
