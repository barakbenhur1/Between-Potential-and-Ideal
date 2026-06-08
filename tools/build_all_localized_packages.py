#!/usr/bin/env python3
from __future__ import annotations

from argparse import ArgumentParser
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "localization" / "sources"
OUTPUTS = ROOT / "site" / "files"
BUILDER = ROOT / "tools" / "build_localized_package.py"
TARGETS = ("tlh", "qya")


def build_language(code: str) -> tuple[int, list[str]]:
    source_dir = SOURCES / code
    output_dir = OUTPUTS / code
    if not source_dir.exists():
        print(f"SKIP: no source directory for {code}")
        return 0, []

    built: list[str] = []
    failures = 0
    for source in sorted(source_dir.glob("*.md")):
        if source.name.startswith("_"):
            continue
        output_stem = output_dir / source.stem
        print(f"\n==> {code}: {source.name}")
        result = subprocess.run(
            [sys.executable, str(BUILDER), str(source), str(output_stem)],
            cwd=ROOT,
        )
        if result.returncode:
            failures += 1
        else:
            built.append(output_stem.relative_to(ROOT).as_posix())
    return failures, built


def main() -> int:
    parser = ArgumentParser(description="Build all reviewed localized document sources.")
    parser.add_argument("--language", choices=TARGETS, action="append")
    args = parser.parse_args()

    languages = tuple(args.language or TARGETS)
    failures = 0
    built: list[str] = []
    for code in languages:
        count, items = build_language(code)
        failures += count
        built.extend(items)

    print(f"\nBuilt packages: {len(built)}")
    for item in built:
        print("-", item)
    if failures:
        print(f"Failed packages: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
