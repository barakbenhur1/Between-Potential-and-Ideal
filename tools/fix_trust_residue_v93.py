#!/usr/bin/env python3
"""BPI V93 — Trust-residue scan and safe fixes.

Critic-driven goal:
- Remove visible metadata leftovers and broken formal tokens when they appear in public text.
- Do not rewrite stories/theory unless the issue is a clear typo, spacing break, or export artifact.
- Do not touch headings, subtitles, images, design structure, document exports, or file names.

This script performs only conservative exact replacements in HTML/MD/TXT source files.
It also reports risky chapter markers (`פרק ?`, `Chapter ?`) without changing them,
because those may be intentional and require framing rather than automatic correction.
"""
from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "_product_docs" / "reports" / "BPI_V93_TRUST_RESIDUE_REPORT_HE.md"
REPORT.parent.mkdir(parents=True, exist_ok=True)

SCAN_EXTS = {".html", ".md", ".txt"}
SKIP_PARTS = {
    "/.git/",
    "/node_modules/",
    "/_product_docs/reports/",
}

# Exact residue replacements. Conservative by design.
EXACT_REPLACEMENTS = [
    ("Completed AI English files", "English AI documents"),
    ("Completed English AI documents in all public formats.", "English AI documents are available in the formats below."),
    ("אידיאל י", "אידיאלי"),
    ("שה אידיאל", "שהאידיאל"),
    ("ה אידיאל", "האידיאל"),
]

# Broken formal tokens seen in RTL/LTR exports. Replace only separated standalone forms.
TOKEN_REPLACEMENTS = [
    (re.compile(r"\bN\s+P\b"), "NP"),
    (re.compile(r"\bc\s+o\s+N\s+P\b", re.IGNORECASE), "coNP"),
    (re.compile(r"\bQ\s+B\s+F\b"), "QBF"),
    (re.compile(r"\bP\s+S\s+P\s+A\s+C\s+E\b"), "PSPACE"),
    (re.compile(r"\bP\s+H\b"), "PH"),
    (re.compile(r"\bS\s+A\s+T\b"), "SAT"),
    (re.compile(r"\bU\s+N\s+S\s+A\s+T\b"), "UNSAT"),
]

RISKY_PATTERNS = [
    re.compile(r"פרק\s+[?*•][:.↓]?"),
    re.compile(r"Chapter\s+[?*•][:.↓]?", re.IGNORECASE),
    re.compile(r"\bTODO\b|\bplaceholder\b|\bdraft\b|\btemp\b", re.IGNORECASE),
]


def should_skip(path: Path) -> bool:
    rel = "/" + path.relative_to(ROOT).as_posix()
    return any(part in rel for part in SKIP_PARTS)


def iter_files():
    for path in sorted((ROOT / "site").rglob("*")):
        if path.is_file() and path.suffix.lower() in SCAN_EXTS and not should_skip(path):
            yield path


def patch_file(path: Path) -> tuple[bool, list[str], list[str]]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    original = text
    changes: list[str] = []
    risks: list[str] = []

    for old, new in EXACT_REPLACEMENTS:
        count = text.count(old)
        if count:
            text = text.replace(old, new)
            changes.append(f"`{old}` → `{new}` ({count})")

    for pattern, new in TOKEN_REPLACEMENTS:
        text, count = pattern.subn(new, text)
        if count:
            changes.append(f"formal token normalized to `{new}` ({count})")

    for pattern in RISKY_PATTERNS:
        for match in pattern.finditer(text):
            snippet_start = max(0, match.start() - 40)
            snippet_end = min(len(text), match.end() + 40)
            snippet = " ".join(text[snippet_start:snippet_end].split())
            risks.append(snippet)

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True, changes, risks
    return False, changes, risks


def main() -> int:
    changed_files = 0
    total_changes: list[str] = []
    risk_lines: list[str] = []

    for path in iter_files():
        changed, changes, risks = patch_file(path)
        rel = path.relative_to(ROOT).as_posix()
        if changed:
            changed_files += 1
            total_changes.append(f"### `{rel}`")
            total_changes.extend(f"- {change}" for change in changes)
        if risks:
            risk_lines.append(f"### `{rel}`")
            risk_lines.extend(f"- {risk}" for risk in risks[:20])
            if len(risks) > 20:
                risk_lines.append(f"- ... ועוד {len(risks)-20} מופעים")

    lines = [
        "# BPI V93 - סריקת שאריות אמון ותיקונים שמרניים",
        "",
        f"Generated: {datetime.utcnow().isoformat(timespec='seconds')}Z",
        "",
        "העיקרון: לתקן רק שאריות ברורות, מונחים מפורקים ושגיאות ריווח נקודתיות. לא שונו כותרות/תתי־כותרות/תמונות/עיצוב, ולא בוצע שכתוב רעיוני רחב.",
        "",
        f"Changed files: {changed_files}",
        "",
        "## תיקונים שבוצעו",
    ]
    lines.extend(total_changes or ["- לא נמצאו תיקונים שמרניים לביצוע."])
    lines.extend([
        "",
        "## מופעים שדורשים בדיקה ידנית ולא תוקנו אוטומטית",
    ])
    lines.extend(risk_lines or ["- לא נמצאו מופעים מסוכנים לפי הסריקה הנוכחית."])
    lines.extend([
        "",
        "## בדיקת הצלחה ידנית",
        "- אין שאריות `Completed AI English files` גלויה באתר הציבורי.",
        "- מונחים פורמליים אינם מפורקים כמו `N P` או `P S P A C E`.",
        "- אם נמצאו `פרק ?` או `Chapter ?`, הם מופיעים בדוח בלבד ולא תוקנו אוטומטית.",
    ])

    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"changed files: {changed_files}")
    print(f"report: {REPORT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
