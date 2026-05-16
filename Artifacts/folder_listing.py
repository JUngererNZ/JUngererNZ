#!/usr/bin/env python3
from pathlib import Path
import json
import yaml
import argparse
from datetime import datetime

def build_tree(path: Path, include_files: bool = True):
    node = {
        "name": path.name,
        "path": str(path),
        "type": "directory",
        "children": []
    }

    for child in sorted(path.iterdir(), key=lambda p: (p.is_file(), p.name.lower())):
        if child.is_dir():
            node["children"].append(build_tree(child, include_files=include_files))
        elif include_files:
            node["children"].append({
                "name": child.name,
                "path": str(child),
                "type": "file",
                "size_bytes": child.stat().st_size
            })

    return node

def main():
    parser = argparse.ArgumentParser(description="Create recursive folder listing in JSON and YAML")
    parser.add_argument("source", help="Source directory to scan")
    parser.add_argument("-o", "--output-dir", default="output", help="Output directory")
    parser.add_argument("--no-files", action="store_true", help="List directories only")
    args = parser.parse_args()

    source = Path(args.source).resolve()
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    if not source.exists() or not source.is_dir():
        raise SystemExit(f"Invalid source directory: {source}")

    data = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "source": str(source),
        "tree": build_tree(source, include_files=not args.no_files)
    }

    json_path = output_dir / f"{source.name}_listing.json"
    yaml_path = output_dir / f"{source.name}_listing.yaml"

    with json_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    with yaml_path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)

    print(f"JSON written to: {json_path}")
    print(f"YAML written to: {yaml_path}")

if __name__ == "__main__":
    main()