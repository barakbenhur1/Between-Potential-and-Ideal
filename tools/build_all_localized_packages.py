#!/usr/bin/env python3
from __future__ import annotations

from argparse import ArgumentParser
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "localization" / "sources"
PUBLIC_OUTPUTS = ROOT / "site" / "files"
PREVIEW_OUTPUTS = ROOT / "reports" / "localization" / "previews"
BUILDER = ROOT / "tools" / "build_localized_package.py"
TARGETS = ("tlh", "qya")


def source_status(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return "invalid"
    try:
        _, raw_meta, _ = text.split("---\n", 2)
    except ValueError:
        return "invalid"
    for line in raw_meta.splitlines():
        key, sep, value = line.partition(":")
        if sep and key.strip() == "status":
            return value.strip()
    return "missing"


def build_language(code: str, preview: bool) -> tuple[int, list[str], list[str]]:
    source_dir = SOURCES / code
    output_dir = (PREVIEW_OUTPUTS if preview else PUBLIC_OUTPUTS) / code
    if not source_dir.exists():
        print(f"SKIP: no source directory for {code}")
        return 0, [], []

    built: list[str] = []
    skipped: list[str] = []
    failures = 0
    for source in sorted(source_dir.glob("*.md")):
        if source.name.startswith("_"):
            continue
        status = source_status(source)
        if not preview and status != "approved":
            skipped.append(f"{source.name} ({status})")
            continue

        output_stem = output_dir / source.stem
        mode = "preview" if preview else "public"
        print(f"\n==> {code} [{mode}, {status}]: {source.name}")
        cmd = [sys.executable, str(BUILDER), str(source), str(output_stem)]
        if preview:
            cmd.append("--allow-draft")
        result = subprocess.run(cmd, cwd=ROOT)
        if result.returncode:
            failures += 1
        else:
            built.append(output_stem.relative_to(ROOT).as_posix())
    return failures, built, skipped


def main() -> int:
    parser = ArgumentParser(description="Build reviewed public packages or private draft previews.")
    parser.add_argument("--language", choices=TARGETS, action="append")
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Build non-public review files under reports/localization/previews.",
    )
    args = parser.parse_args()

    languages = tuple(args.language or TARGETS)
    failures = 0
    built: list[str] = []
    skipped: list[str] = []
    for code in languages:
        count, items, omitted = build_language(code, args.preview)
        failures += count
        built.extend(items)
        skipped.extend(f"{code}: {item}" for item in omitted)

    print(f"\nBuilt packages: {len(built)}")
    for item in built:
        print("-", item)
    if skipped:
        print(f"Skipped non-approved sources: {len(skipped)}")
        for item in skipped:
            print("-", item)
    if failures:
        print(f"Failed packages: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
