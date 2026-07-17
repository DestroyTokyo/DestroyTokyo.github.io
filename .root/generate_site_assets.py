import json, os

output_dir = "site/jsons"
background_assets_dir = "site/assets/screens/backgrounds"
styles_assets_dir = "site/assets/themes"

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

def generate_backgrounds():
    files = get_files(background_assets_dir, ["gif", "png", "jpeg", "jpg"])
    save_to_json(files, "backgrounds.json")


def generate_themes():
    files = get_files(styles_assets_dir, ["css"])
    save_to_json(files, "themes.json")


if __name__ == "__main__":
    generate_backgrounds()
    generate_themes()