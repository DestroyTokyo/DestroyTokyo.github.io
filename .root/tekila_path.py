from __future__ import annotations
from pathlib import Path

SOURCE_DIR = Path(__file__).resolve().parent.parent
IGNORE = [".git", ".root", ".gitignore"]
OUTPUT_FILE = Path(__file__).resolve().parent / "tekila.txt"


def collect_files(source_dir: Path, output_file: Path | None = None) -> list[Path]:
    if not source_dir.exists():
        raise FileNotFoundError(f"Cant found: {source_dir}")

    all_files = []
    for item in source_dir.rglob("*"):
        if item.is_file():
            ii = False
            rel = item.relative_to(source_dir)
            if any(ign in rel.parts for ign in IGNORE):
                ii = True
            if not ii:
                all_files.append(item)

    return sorted(set(all_files))


def write_combined_file(file_paths: list[Path], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as out_f:
        for file_path in file_paths:
            rel_path = file_path.relative_to(SOURCE_DIR)
            out_f.write(f"{rel_path}\n")


def main() -> None:
    files = collect_files(SOURCE_DIR, OUTPUT_FILE)

    print(f"Found: {len(files)}")
    write_combined_file(files, OUTPUT_FILE)


if __name__ == "__main__":
    main()