#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path.cwd()
SITE = ROOT / "site"
CSS_FILE = SITE / "styles.css"
TOOL_FILE = ROOT / "tools" / "bpi_v405_precise_home_width_restore.py"

def replace_margin_text(text: str) -> tuple[str, int]:
    count = 0

    replacements = [
        ("padding-left:8px!important;", "padding-left:12px!important;"),
        ("padding-right:8px!important;", "padding-right:12px!important;"),
        ("padding-left: 8px!important;", "padding-left:12px!important;"),
        ("padding-right: 8px!important;", "padding-right:12px!important;"),
        ("padding-left: 8px !important;", "padding-left:12px!important;"),
        ("padding-right: 8px !important;", "padding-right:12px!important;"),
        ("8px margin on each side", "12px margin on each side"),
        ("8px from each side", "12px from each side"),
        ("8px מכל צד", "12px מכל צד"),
    ]

    for old, new in replacements:
        n = text.count(old)
        if n:
            text = text.replace(old, new)
            count += n

    # Also catch calc expressions if a prior variant used them.
    text2, n = re.subn(r"calc\(100vw\s*-\s*16px\)", "calc(100vw - 24px)", text)
    text = text2
    count += n

    return text, count

def main():
    if not SITE.exists():
        raise SystemExit("ERROR: run from repository root — the directory that contains site/")

    changes = []

    if CSS_FILE.exists():
        original = CSS_FILE.read_text(encoding="utf-8", errors="ignore")
        updated, count = replace_margin_text(original)
        if updated != original:
            CSS_FILE.write_text(updated, encoding="utf-8")
        changes.append(f"{CSS_FILE}: replacements={count}")
    else:
        raise SystemExit("ERROR: site/styles.css not found")

    # Keep the generator script in sync if it exists, so future reruns don't revert to 8px.
    if TOOL_FILE.exists():
        original = TOOL_FILE.read_text(encoding="utf-8", errors="ignore")
        updated, count = replace_margin_text(original)
        if updated != original:
            TOOL_FILE.write_text(updated, encoding="utf-8")
        changes.append(f"{TOOL_FILE}: replacements={count}")
    else:
        changes.append(f"{TOOL_FILE}: not found, skipped")

    css = CSS_FILE.read_text(encoding="utf-8", errors="ignore")
    problems = []
    if "BPI V405" not in css:
        problems.append("V405 block not found in styles.css")
    if "padding-left:8px!important" in css or "padding-right:8px!important" in css:
        problems.append("8px mobile padding still exists in styles.css")
    if "padding-left:12px!important" not in css or "padding-right:12px!important" not in css:
        problems.append("12px mobile padding not found in styles.css")

    report = [
        "BPI V406 mobile homepage margin update",
        "",
        "Change:",
        "- Mobile homepage cards now use 12px from each side instead of 8px.",
        "- No layout redesign.",
        "- No content changes.",
        "",
        "Files touched if present:",
        *changes,
    ]

    if problems:
        report.append("")
        report.append("FAILED:")
        report.extend([f"- {p}" for p in problems])
        (ROOT / "BPI_V406_MOBILE_12PX_MARGIN_REPORT.txt").write_text("\n".join(report) + "\n", encoding="utf-8")
        print("\n".join(report))
        raise SystemExit(1)

    report.append("")
    report.append("OK")
    (ROOT / "BPI_V406_MOBILE_12PX_MARGIN_REPORT.txt").write_text("\n".join(report) + "\n", encoding="utf-8")
    print("\n".join(report))

if __name__ == "__main__":
    main()
