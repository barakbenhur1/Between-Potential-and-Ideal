#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Repo-local final release QA command for Between Potential and Ideal.

This is the single command contributors should run before pushing/releasing:

  python3 tools/final_release_qa.py --scan

It intentionally wraps the existing production guard instead of replacing it:
- tools/audit_release_guard.py remains the canonical detailed guard.
- this script adds a stable high-level final gate, report output, and git hygiene checks.

Reports:
- reports/production_next/final_release_qa.md
- reports/production_next/final_release_qa.json
"""

from __future__ import annotations

from pathlib import Path
import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "reports" / "production_next"


def run(cmd: list[str], timeout: int = 240) -> dict:
    try:
        proc = subprocess.run(
            cmd,
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout,
        )
        return {
            "cmd": cmd,
            "returncode": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
            "ok": proc.returncode == 0,
        }
    except Exception as exc:
        return {
            "cmd": cmd,
            "returncode": None,
            "stdout": "",
            "stderr": f"{type(exc).__name__}: {exc}",
            "ok": False,
        }


def tail(text: str, n: int = 80) -> str:
    return "\n".join((text or "").splitlines()[-n:])


def command_output(cmd: dict, n: int = 160) -> str:
    return tail(((cmd.get("stdout") or "") + (cmd.get("stderr") or "")).strip(), n)


def run_scan() -> dict:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    status = run(["git", "status", "--short"])
    diff_check = run(["git", "diff", "--check"])
    log = run(["git", "log", "--oneline", "-5"])
    build_info = run(["python3", "tools/check_build_info_matches_head.py"])
    release_guard = run(["python3", "tools/audit_release_guard.py"], timeout=600)

    blockers: list[str] = []
    warnings: list[str] = []

    dirty_lines = []
    if status["ok"]:
        for line in status["stdout"].splitlines():
            stripped = line.strip()
            if stripped.startswith("?? reports/") or stripped.startswith("M reports/") or " reports/" in line:
                continue
            dirty_lines.append(line)
    else:
        blockers.append("GIT_STATUS_FAILED")

    if dirty_lines:
        blockers.append("WORKTREE_NOT_CLEAN_EXCLUDING_REPORTS")
    if not diff_check["ok"] or diff_check["stdout"].strip() or diff_check["stderr"].strip():
        blockers.append("GIT_DIFF_CHECK_FAILED")
    if not build_info["ok"]:
        blockers.append("BUILD_INFO_GUARD_FAILED")
    elif "WARNINGS:" in build_info["stdout"]:
        warnings.append("BUILD_INFO_HEAD_MISMATCH_WARNING_ONLY")
    if not release_guard["ok"]:
        blockers.append("AUDIT_RELEASE_GUARD_FAILED")

    result = {
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "status": "RELEASE_READY" if not blockers else "RELEASE_BLOCKED",
        "blockers": blockers,
        "warnings": warnings,
        "git_status_clean_excluding_reports": not dirty_lines,
        "dirty_lines_excluding_reports": dirty_lines,
        "diff_check_ok": not ("GIT_DIFF_CHECK_FAILED" in blockers),
        "build_info_ok": build_info["ok"],
        "release_guard_ok": release_guard["ok"],
        "last_commits": log["stdout"].strip(),
        "commands": {
            "git_status": status,
            "diff_check": diff_check,
            "build_info": build_info,
            "release_guard": release_guard,
        },
    }

    write_reports(result)
    return result


def write_reports(result: dict) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / "final_release_qa.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    lines = [
        "# BPI Final Release QA",
        "",
        f"- Generated at UTC: `{result['generated_at_utc']}`",
        f"- Status: `{result['status']}`",
        f"- Blockers: {len(result['blockers'])}",
    ]
    for blocker in result["blockers"]:
        lines.append(f"  - `{blocker}`")
    if result["warnings"]:
        lines += ["", "## Warnings"]
        for warning in result["warnings"]:
            lines.append(f"- `{warning}`")

    lines += [
        "",
        "## Summary",
        f"- Worktree clean excluding reports: `{result['git_status_clean_excluding_reports']}`",
        f"- git diff --check OK: `{result['diff_check_ok']}`",
        f"- build-info guard OK: `{result['build_info_ok']}`",
        f"- audit release guard OK: `{result['release_guard_ok']}`",
        "",
        "## Last commits",
        "```text",
        result["last_commits"] or "(not available)",
        "```",
    ]

    if result["dirty_lines_excluding_reports"]:
        lines += [
            "",
            "## Dirty worktree excluding reports",
            "```text",
            "\n".join(result["dirty_lines_excluding_reports"]),
            "```",
        ]

    for label, key in [
        ("git diff --check", "diff_check"),
        ("build-info guard", "build_info"),
        ("audit release guard", "release_guard"),
    ]:
        cmd = result["commands"][key]
        lines += [
            "",
            f"## {label}",
            f"- OK: `{cmd['ok']}`",
            f"- Return code: `{cmd['returncode']}`",
            "```text",
            command_output(cmd, 160) or "(no output)",
            "```",
        ]

    lines += ["", "## Final decision"]
    if result["status"] == "RELEASE_READY":
        lines.append("The repository passes the repo-local final release QA gate.")
    else:
        lines.append("Release is blocked. Fix the listed blockers and rerun `python3 tools/final_release_qa.py --scan`.")

    (REPORT_DIR / "final_release_qa.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scan", action="store_true", help="Run the final release QA scan.")
    args = parser.parse_args()

    if not args.scan:
        print("ERROR: use --scan", file=sys.stderr)
        sys.exit(1)

    result = run_scan()
    print("BPI Final Release QA")
    print("status:", result["status"])
    print("blockers:", result["blockers"])
    print("warnings:", result["warnings"])
    print("release guard ok:", result["release_guard_ok"])
    print("build info ok:", result["build_info_ok"])
    print("Report:", REPORT_DIR / "final_release_qa.md")

    if result["status"] != "RELEASE_READY":
        print("\n--- audit release guard output tail ---")
        print(command_output(result["commands"]["release_guard"], 220) or "(no output)")
        print("--- end audit release guard output tail ---")
        sys.exit(2)


if __name__ == "__main__":
    main()
