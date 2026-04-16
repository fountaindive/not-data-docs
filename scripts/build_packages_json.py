#!/usr/bin/env python3
"""Rebuild packages.json by scanning the docs/ directory."""

import json
import os
import sys


def build_packages_json(docs_dir: str, output_file: str) -> None:
    packages = []

    if not os.path.isdir(docs_dir):
        print(f"docs/ directory not found at {docs_dir}")
        sys.exit(1)

    for package_name in sorted(os.listdir(docs_dir)):
        package_dir = os.path.join(docs_dir, package_name)
        if not os.path.isdir(package_dir):
            continue

        build_numbers = sorted(
            [b for b in os.listdir(package_dir) if os.path.isdir(os.path.join(package_dir, b))],
            reverse=True,
        )

        if not build_numbers:
            continue

        builds = [{"buildNumber": b} for b in build_numbers]

        packages.append({"name": package_name, "builds": builds})

    with open(output_file, "w") as f:
        json.dump({"packages": packages}, f, indent=2)
        f.write("\n")

    print(f"Written {len(packages)} package(s) to {output_file}")


if __name__ == "__main__":
    docs_dir = sys.argv[1] if len(sys.argv) > 1 else "docs"
    output_file = sys.argv[2] if len(sys.argv) > 2 else "packages.json"
    build_packages_json(docs_dir, output_file)
