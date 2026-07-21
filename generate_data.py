import re
import hashlib
import shutil
from pathlib import Path

JARS_ROOT = Path("./jars")
OUTPUT_DIR = Path("./maven-repo")

POM_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <groupId>{group_id}</groupId>
  <artifactId>{artifact_id}</artifactId>
  <version>{version}</version>
  <packaging>jar</packaging>
  <name>{artifact_id}</name>
</project>
"""

def sha1_file(filepath):
    with open(filepath, "rb") as f:
        return hashlib.sha1(f.read()).hexdigest()

def process_jar(jar_path, group_id, artifact_id):
    filename = jar_path.name
    base = filename[:-4]

    classifier = ""
    for suffix in ["-javadoc", "-sources"]:
        if suffix in base:
            classifier = suffix
            base = base.replace(suffix, "")
            break

    match = re.search(r"-v(.+)$", base)
    if match: version = match.group(1)
    else: version = "0.0.0"

    artifact = artifact_id

    group_path = group_id.replace(".", "/")
    target_dir = OUTPUT_DIR / group_path / artifact / version
    target_dir.mkdir(parents=True, exist_ok=True)

    base_name = f"{artifact}-{version}"
    target_jar = target_dir / f"{base_name}{classifier}.jar"
    shutil.copy2(jar_path, target_jar)

    if not classifier:
        pom_content = POM_TEMPLATE.format(
            group_id=group_id,
            artifact_id=artifact,
            version=version
        )
        pom_path = target_dir / f"{base_name}.pom"
        with open(pom_path, "w", encoding="utf-8") as f:
            f.write(pom_content)

        for f in [target_jar, pom_path]:
            sha = sha1_file(f)
            sha_path = f.with_suffix(f.suffix + ".sha1")
            with open(sha_path, "w") as sf:
                sf.write(sha)
        print(f"+ {group_id}:{artifact}:{version}")
    else:
        sha = sha1_file(target_jar)
        sha_path = target_jar.with_suffix(target_jar.suffix + ".sha1")
        with open(sha_path, "w") as sf:
            sf.write(sha)
            
def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    if not JARS_ROOT.exists(): return
    for jar_path in JARS_ROOT.rglob("*.jar"):
        rel_path = jar_path.relative_to(JARS_ROOT)
        parts = rel_path.parts
        if len(parts) < 2: continue
        group_path = "/".join(parts[:-1])
        artifact = parts[-2] if len(parts) >= 2 else parts[0]
        group_id = group_path.replace("/", ".")
        process_jar(jar_path, group_id, artifact)

if __name__ == "__main__":
    main()