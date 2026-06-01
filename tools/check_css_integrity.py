#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Check CSS files for basic structural integrity.

This is intentionally lightweight and dependency-free:
- balanced curly braces outside comments and strings
- no obvious unfinished CSS blocks at EOF
- required protected patch markers remain paired

It does not criticize design choices, blurbs, arrows, symbolic markers, or any
approved visual styling.

Run from repo root:
  python3 tools/check_css_integrity.py
"""

from pathlib import Path
import json
import sys

ROOT = Path.cwd()
SITE = ROOT / "site"
REPORT_DIR = ROOT / "reports" / "production_next"

REQUIRED_MARKER_PAIRS = [
    ("BPI_STORIES_EN_COVER_MATCH_HE_V1_20260530", "/BPI_STORIES_EN_COVER_MATCH_HE_V1_20260530"),
    ("BPI_AI_APPENDIX_EN_SUBTITLE_TEXT_FIX_V1_20260531", "/BPI_AI_APPENDIX_EN_SUBTITLE_TEXT_FIX_V1_20260531"),
    ("BPI_AI_ACCESSIBLE_SKIP_LINK_V3_20260601", "/BPI_AI_ACCESSIBLE_SKIP_LINK_V3_20260601"),
    ("BPI_AI_INDEX_CARD_TITLE_MATCH_DOC_TITLE_V1_20260531", "/BPI_AI_INDEX_CARD_TITLE_MATCH_DOC_TITLE_V1_20260531"),
    ("BPI_HE_SELECTED_TABS_AI_NAV_LABEL_FIX_V1_20260531", "/BPI_HE_SELECTED_TABS_AI_NAV_LABEL_FIX_V1_20260531"),
    ("BPI_WITNESS_EN_PAGE_LAYOUT_FIX_V4_20260531", "/BPI_WITNESS_EN_PAGE_LAYOUT_FIX_V4_20260531"),
]


def strip_comments_and_strings(text: str) -> str:
    out = []
    i = 0
    n = len(text)
    in_string = None
    while i < n:
        ch = text[i]
        nxt = text[i + 1] if i + 1 < n else ""
        if in_string:
            if ch == "\\":
                i += 2
                continue
            if ch == in_string:
                in_string = None
            i += 1
            continue
        if ch in {'"', "'"}:
            in_string = ch
            i += 1
            continue
        if ch == "/" and nxt == "*":
            end = text.find("*/", i + 2)
            if end == -1:
                return "".join(out)
            i = end + 2
            continue
        out.append(ch)
        i += 1
    return "".join(out)


def check_file(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="ignore")
    structural = strip_comments_and_strings(text)
    errors = []
    warnings = []
    balance = 0
    min_balance = 0
    for ch in structural:
        if ch == "{":
            balance += 1
        elif ch == "}":
            balance -= 1
            min_balance = min(min_balance, balance)
    if balance != 0:
        errors.append(f"unbalanced curly braces: final balance {balance}")
    if min_balance < 0:
        errors.append("closing brace appears before matching opening brace")
    stripped = structural.rstrip()
    if stripped.endswith("{") or stripped.endswith(":") or stripped.endswith(","):
        errors.append("file appears to end inside an unfinished CSS rule")
    if path.name == "document-reading-direction-fix.css":
        for start, end in REQUIRED_MARKER_PAIRS:
            if start not in text:
                errors.append(f"missing marker {start}")
            if end not in text:
                errors.append(f"missing marker {end}")
    return {"path": str(path.relative_to(ROOT)).replace("\\", "/"), "errors": errors, "warnings": warnings}


def main() -> int:
    items = []
    errors = []
    for path in sorted(SITE.rglob("*.css")) if SITE.exists() else []:
        item = check_file(path)
        items.append(item)
        for error in item["errors"]:
            errors.append(f"{item['path']}: {error}")
    result = {"status": "OK" if not errors else "FAIL", "css_files_checked": len(items), "errors": errors, "items": items}
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / "css_integrity_check.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = ["# CSS Integrity Check", "", f"- Status: `{result['status']}`", f"- CSS files checked: {len(items)}", f"- Errors: {len(errors)}", ""]
    if errors:
        lines.append("## Errors")
        for error in errors:
            lines.append(f"- {error}")
    else:
        lines.append("All checked CSS files passed basic structural integrity checks.")
    (REPORT_DIR / "css_integrity_check.md").write_text("\n".join(lines), encoding="utf-8")
    if errors:
        print("FAIL: CSS integrity check found errors")
        for error in errors[:50]:
            print("-", error)
        return 1
    print("OK: CSS integrity check passed.")
    print(f"css_files_checked={len(items)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
