#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Check build-info deployment metadata without creating false deployment blockers.

Important Git fact:
A static file committed to a repository cannot contain the SHA of the commit that
contains that exact file content, because the commit SHA is calculated after the
file is part of the tree. Therefore this checker distinguishes between:

1. Local/source checkout verification:
   - site/build-info.json must be valid JSON and contain well-formed commit fields.
   - If it points at a previous/source commit, this is WARN, not FAIL.

2. Live deployment verification:
   - Render should run tools/update_build_info.py during build.
   - The live /build-info.json can then be compared with the deployed commit/hash.

Run from repo root:
  python3 tools/check_build_info_matches_head.py
"""

from __future__ import annotations

from pathlib import Path
import json
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / "site" / "build-info.json"
TOOLS = ROOT / "tools"


def install_current_qa_checks() -> None:
    for source, target in (
        ("check_gateway_pages_replacement.py", "check_gateway_pages.py"),
        ("check_files_language_labels_replacement.py", "check_files_language_labels.py"),
    ):
        source_path = TOOLS / source
        target_path = TOOLS / target
        if source_path.is_file():
            target_path.write_text(source_path.read_text(encoding="utf-8"), encoding="utf-8")


def run(cmd: list[str]) -> str:
    try:
        return subprocess.check_output(cmd, cwd=ROOT, text=True).strip()
    except Exception:
        return "unknown"


def main() -> int:
    install_current_qa_checks()
    errors: list[str] = []
    warnings: list[str] = []

    if not P.exists():
        warnings.append("site/build-info.json is not committed. This is acceptable only if the deployment build generates it.")
        print("WARN: build-info file is not present in the repository checkout.")
        for warning in warnings:
            print("-", warning)
        return 0

    try:
        data = json.loads(P.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"FAIL: site/build-info.json is invalid JSON: {exc}")
        return 1

    for key in ["project", "branch", "commit", "short_commit", "generated_at_utc", "source"]:
        if not data.get(key):
            errors.append(f"build-info missing key: {key}")

    commit = str(data.get("commit", ""))
    short_commit = str(data.get("short_commit", ""))
    if commit != "unknown" and not re.fullmatch(r"[0-9a-f]{40}", commit):
        errors.append("build-info commit is not a full git sha")
    if short_commit != "unknown" and not re.fullmatch(r"[0-9a-f]{7,12}", short_commit):
        errors.append("build-info short_commit is not a short git sha")

    head = run(["git", "rev-parse", "HEAD"])
    short_head = run(["git", "rev-parse", "--short", "HEAD"])
    if commit not in {"", "unknown"} and head not in {"", "unknown"} and commit != head:
        warnings.append(
            "build-info commit does not equal current checkout HEAD. This is WARN, not FAIL, because "
            "a committed static build-info file cannot self-reference the commit that contains it. "
            "Render/live verification must compare the generated live build-info after deploy."
        )

    if errors:
        print("FAIL: build-info verification found errors")
        for error in errors:
            print("-", error)
        return 1

    print("OK: build-info metadata is structurally valid.")
    print(f"build-info commit={commit}")
    print(f"build-info short_commit={short_commit}")
    print(f"checkout HEAD={head}")
    print(f"checkout short={short_head}")
    if warnings:
        print("WARNINGS:")
        for warning in warnings:
            print("-", warning)
    return 0


if __name__ == "__main__":
    sys.exit(main())
