#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Update site/build-info.json from the current Git checkout.

Important:
A committed static JSON file cannot contain the SHA of the commit that contains
that same JSON content, because the commit SHA is calculated from the tree that
includes the file. Therefore this tool records the current HEAD at generation
time. In a normal local pre-commit flow, the committed build-info file may point
at the parent/source commit. In the deployed Render build, this tool should run
at build time so the live generated build-info reflects the deployed checkout.

Run from repo root:
  python3 tools/update_build_info.py
"""

from __future__ import annotations

from pathlib import Path
import datetime
import json
import subprocess

OUT = Path("site/build-info.json")


def run(cmd: list[str]) -> str:
    try:
        return subprocess.check_output(cmd, text=True).strip()
    except Exception:
        return "unknown"


def main() -> None:
    commit = run(["git", "rev-parse", "HEAD"])
    short_commit = run(["git", "rev-parse", "--short", "HEAD"])
    branch = run(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    generated_at = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat()

    data = {
        "project": "Between Potential and Ideal",
        "branch": branch,
        "commit": commit,
        "short_commit": short_commit,
        "generated_at_utc": generated_at,
        "source": "tools/update_build_info.py",
        "build_info_mode": "generated-from-current-git-head",
        "deployment_verification_note": (
            "This file is generated from the current Git HEAD. A committed static JSON file cannot "
            "contain the SHA of the commit that contains itself, so a repo copy may point at the "
            "source/parent commit when generated immediately before commit. The deployed Render build "
            "should regenerate this file during build. If a live deployment appears stale, verify Render "
            "logs, page source, hard refresh, incognito, and cache before declaring a deployment blocker."
        ),
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote", OUT)
    print("commit", commit)
    print("short_commit", short_commit)
    print("generated_at_utc", generated_at)


if __name__ == "__main__":
    main()
