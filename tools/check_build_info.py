#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validate site/build-info.json without creating false deployment blockers.

This baseline check verifies that build-info exists, is valid JSON, and has
well-formed commit metadata. It intentionally does not fail when the committed
build-info commit differs from the current checkout HEAD, because a committed
static JSON file cannot contain the SHA of the commit that contains itself.

For a stronger explanatory check, run:
  python3 tools/check_build_info_matches_head.py
"""

from pathlib import Path
import json
import re
import sys

P = Path("site/build-info.json")


def main() -> int:
    errors = []
    warnings = []

    if not P.exists():
        errors.append("missing site/build-info.json")
        data = {}
    else:
        try:
            data = json.loads(P.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"site/build-info.json is invalid JSON: {exc}")
            data = {}

    if data:
        for key in ["project", "branch", "commit", "short_commit", "generated_at_utc", "source"]:
            if not data.get(key):
                errors.append(f"build-info missing key: {key}")

        commit = str(data.get("commit", ""))
        if commit != "unknown" and not re.fullmatch(r"[0-9a-f]{40}", commit):
            errors.append("build-info commit is not a full git sha")

        short_commit = str(data.get("short_commit", ""))
        if short_commit != "unknown" and not re.fullmatch(r"[0-9a-f]{7,12}", short_commit):
            errors.append("build-info short_commit is not a short git sha")

        if data.get("deployment_verification_note"):
            warnings.append("deployment verification note present")

    if errors:
        print("FAIL: build-info audit found issues")
        for error in errors:
            print("-", error)
        return 1

    print("OK: build-info baseline passed.")
    for warning in warnings:
        print("NOTE:", warning)
    return 0


if __name__ == "__main__":
    sys.exit(main())
