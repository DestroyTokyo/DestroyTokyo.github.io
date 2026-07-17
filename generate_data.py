import re, hashlib, shutil
from pathlib import Path

GROUP_ID = "delta.cion"
SOURCE_DIR = Path("./jars")
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

def process_jar(jar_path):
    filename = jar_path.name
    base = filename[:-4]

    classifier = ""
    for suffix in ["-javadoc", "-sources"]:
        if suffix in base:
            classifier = suffix
            base = base.replace(suffix, "")
            break

    match = re.search(r"-v(.+)$", base)
    if match:
        version = match.group(1)
        artifact = base[:match.start()]
    else:
        version = "0.0.0"
        artifact = base

    artifact = "tokyo"

    target_dir = OUTPUT_DIR / GROUP_ID.replace(".", "/") / artifact / version

    target_dir.mkdir(parents=True, exist_ok=True)

    base_name = f"{artifact}-{version}"
    target_jar = target_dir / f"{base_name}{classifier}.jar"

    shutil.copy2(jar_path, target_jar)

    if not classifier:
        pom_content = POM_TEMPLATE.format(
            group_id=GROUP_ID,
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

        print(f"Sucess: {artifact}:{version}")
    else:
        sha = sha1_file(target_jar)
        sha_path = target_jar.with_suffix(target_jar.suffix + ".sha1")
        with open(sha_path, "w") as sf:
            sf.write(sha)
        print(f"Sucess: {classifier} for {artifact}:{version}")

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for jar in SOURCE_DIR.glob("*.jar"):
        process_jar(jar)
        
if __name__ == "__main__":
    main()
