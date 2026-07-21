#!/usr/bin/env python3
import json
import re
import os
import requests
from os import environ

GH_TOKEN = environ.get("GITHUB_TOKEN")
RELEASES_URL = "https://api.github.com/repos/{}/releases?per_page=100&page={}"

FILE_NAME = "repo.json"
JARS_ROOT = "jars"

session = None

def download_asset(url, target_dir, filename):
    os.makedirs(target_dir, exist_ok=True)
    filepath = os.path.join(target_dir, filename)
    with session.get(url, stream=True) as r:
        r.raise_for_status()
        with open(filepath, "wb") as f:
            for chunk in r.iter_content(8192):
                f.write(chunk)

def process_repo(repo_path, patterns, group_path, artifact):
    page = 1
    while True:
        resp = session.get(RELEASES_URL.format(repo_path, page))
    
        if resp.status_code != 200:
            print(f"{repo_path} error: {resp.status_code}")
            return
    
        resp.raise_for_status()
        releases = resp.json()
        if not releases:
            break

        for release in releases:
            for asset in release.get("assets", []):
                name = asset["name"]
                if all(re.search(p, name) for p in patterns):
                    target_dir = os.path.join(JARS_ROOT, group_path, artifact)
                    download_asset(asset["browser_download_url"], target_dir, name)

        if len(releases) < 100:
            break
        page += 1

def traverse(obj, path=None):
    if path is None: path = []
    if isinstance(obj, dict):
        if "url" in obj and "pattern" in obj:
            group_path = "/".join(path[:-1])
            artifact = path[-1]
            m = re.match(r"https://github\.com/([^/]+/[^/]+)/releases", obj["url"])
            if m: process_repo(m.group(1), obj["pattern"], group_path, artifact)
            else: print(f"Не удалось извлечь репозиторий из URL: {obj['url']}")
        else:
            for k, v in obj.items():
                traverse(v, path + [k])
    elif isinstance(obj, list):
        for item in obj:
            traverse(item, path)

def set_session():
    global session
    session = requests.Session()
    session.headers.update({
        "Authorization": f"token {GH_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    })

def main():
    if not GH_TOKEN:
        raise ValueError("GITHUB_TOKEN не задан в переменных окружения.")
    set_session()
    with open(FILE_NAME) as f:
        data = json.load(f)
    traverse(data)

if __name__ == "__main__":
    main()