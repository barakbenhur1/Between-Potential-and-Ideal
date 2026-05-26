#!/usr/bin/env python3
"""BPI V91 — AI section product polish.

Purpose:
- Fix the highest-risk QA issue: AI pages still exposing raw metadata labels.
- Preserve the AI section, stories, blurbs, headings, images, and document links.
- Change text only where justified by the critique: labels/caution copy around AI.

This script intentionally does not touch design structure, images, titles, subtitles,
PDF/DOCX/MD exports, stories, or theory body text.
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "_product_docs" / "reports" / "BPI_V91_AI_SECTION_PRODUCT_POLISH_REPORT_HE.md"
REPORT.parent.mkdir(parents=True, exist_ok=True)

PAGES = {
    ROOT / "site" / "pages" / "he" / "ai.html": [
        (
            "הדיאלוגים כאן אינם טענה שלמכונה יש חוויה או אמונה. הם משמשים כמראה לשונית ולוגית: דרך לבדוק איך רעיונות חוזרים אלינו כשהם עוברים דרך מערכת שמחשבת שפה בלי לחיות אותה.",
            "AI משמש כאן כמראה, עדשה, בדיקת לחץ לשונית־לוגית וכלי פרשני — לא כהוכחה, לא כסמכות ולא כהאנשה. הדיאלוגים בודקים כיצד רעיונות חוזרים אלינו דרך מערכת שמחשבת שפה בלי לחיות אותה.",
            "חיזוק סייג קרוב במדור AI בעברית",
        ),
        (
            '<div class="ai-mode-title file-mode-label">אין</div>',
            '<div class="ai-mode-title file-mode-label">שאלת האין</div>',
            "אין → שאלת האין",
        ),
        (
            '<div class="ai-mode-title file-mode-label">יש</div>',
            '<div class="ai-mode-title file-mode-label">שאלת היש</div>',
            "יש → שאלת היש",
        ),
        (
            '<div class="ai-mode-title file-mode-label">יש מאין</div>',
            '<div class="ai-mode-title file-mode-label">שאלת המעבר מן האין אל היש</div>',
            "יש מאין → שאלת המעבר מן האין אל היש",
        ),
    ],
    ROOT / "site" / "pages" / "en" / "ai-en.html": [
        (
            "The dialogues here use AI as a linguistic and logical mirror: a way to test how ideas return after passing through a system that calculates language without living it.",
            "AI is used here as a mirror, lens, linguistic/logical stress test, and interpretive tool — not as proof, authority, or personhood. The dialogues test how ideas return after passing through a system that calculates language without living it.",
            "Strengthened close AI caution in English",
        ),
        (
            '<div class="ai-mode-title file-mode-label">No</div>',
            '<div class="ai-mode-title file-mode-label">Question of Nothingness</div>',
            "No → Question of Nothingness",
        ),
        (
            '<div class="ai-mode-title file-mode-label">Yes</div>',
            '<div class="ai-mode-title file-mode-label">Question of Being</div>',
            "Yes → Question of Being",
        ),
        (
            '<div class="ai-mode-title file-mode-label">Being from Nothing</div>',
            '<div class="ai-mode-title file-mode-label">Being from Nothing / The Passage Question</div>',
            "Being from Nothing → Being from Nothing / The Passage Question",
        ),
    ],
}


def patch_page(path: Path, replacements: list[tuple[str, str, str]]) -> tuple[bool, list[str]]:
    if not path.exists():
        return False, [f"missing: `{path.relative_to(ROOT)}`"]

    text = path.read_text(encoding="utf-8")
    original = text
    notes: list[str] = []

    for old, new, label in replacements:
        if old in text:
            text = text.replace(old, new)
            notes.append(label)
        elif new in text:
            notes.append(f"already applied: {label}")
        else:
            notes.append(f"not found: {label}")

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True, notes
    return False, notes


def main() -> int:
    changed_count = 0
    report_lines = [
        "# BPI V91 - ליטוש מדור AI כמוצר ולא File Dump",
        "",
        f"Generated: {datetime.utcnow().isoformat(timespec='seconds')}Z",
        "",
        "העיקרון: תיקון טקסטואלי ממוקד בלבד במדור AI. לא שונו בלארבים, סיפורים, כותרות, תתי־כותרות, תמונות, מבנה עמוד או קבצי ייצוא.",
        "",
        "## שינויים",
    ]

    for path, replacements in PAGES.items():
        did_change, notes = patch_page(path, replacements)
        if did_change:
            changed_count += 1
        report_lines.append(f"### `{path.relative_to(ROOT)}`")
        report_lines.append(f"- changed: {did_change}")
        report_lines.extend(f"- {note}" for note in notes)
        report_lines.append("")

    report_lines.extend([
        "## בדיקת הצלחה ידנית",
        "- עברית: במדור AI לא צריכות להופיע תוויות גולמיות `אין`, `יש`, `יש מאין` בפני עצמן; הן צריכות להיות ממוסגרות כשאלות.",
        "- אנגלית: `No`, `Yes`, `Being from Nothing` לא צריכות להופיע כ־metadata גולמי, אלא כשמות שאלה מוסברים.",
        "- הסייג על AI צריך להבהיר שה־AI הוא מראה/עדשה/בדיקת לחץ ולא הוכחה, סמכות או האנשה.",
    ])

    REPORT.write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    print(f"changed pages: {changed_count}")
    print(f"report: {REPORT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
