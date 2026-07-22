import json, os

output_dir = "site/jsons"

background_assets_dir = "site/assets/screens/backgrounds"
styles_assets_dir = "site/assets/themes"

repo_file = "repo.json"

# Collectors

def get_files(path: str, extensions: list):
    returned_files = []
    if not os.path.isdir(path): 
        return returned_files

    for f in os.listdir(path):
        parts = f.rsplit(".", 1)
        if len(parts) == 2 and parts[1] in extensions:
            returned_files.append(f)
    return returned_files

def save_to_json(data, filename: str):
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# Generators

def generate_backgrounds():
    files = get_files(background_assets_dir, ["gif", "png", "jpeg", "jpg"])
    save_to_json(files, "backgrounds.json")

def generate_themes():
    files = get_files(styles_assets_dir, ["css"])
    save_to_json(files, "themes.json")

def generate_versions():
    save_to_json(get_pathes(), "versions.json")

# Just contain artifacts

def get_pathes():
    pathes = []
    versions = {}
    with open(repo_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        collect_paths(data, [], pathes)
    for path in pathes:
        print(f"Checking versions for ./maven-repo/{path}")
        if os.path.exists(f"./maven-repo/{path}"):
            versions[path] = get_versions(f"./maven-repo/{path}")
        else: print("Not found")
    print(versions)
    return versions

def collect_paths(data, current_path, result):
    if isinstance(data, dict):
        if "url" in data:
            result.append("/".join(current_path))
        else:
            for key, value in data.items():
                collect_paths(value, current_path + [key], result)

# Check versions in repo

def get_versions(path):
    if os.path.isdir(path):
        list = []
        for d in os.listdir(path):
            if os.path.isdir(d): list.append(d)
        return list

# Main

if __name__ == "__main__":
    # For themes
    generate_backgrounds()
    generate_themes()
    # For versions on page
    generate_versions()