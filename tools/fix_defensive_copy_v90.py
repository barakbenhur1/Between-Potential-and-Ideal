#!/usr/bin/env python3
"""BPI V90 — reduce repeated defensive framing without weakening safeguards.

Rules:
- Do not touch blurbs, stories, AI tags such as אין/יש/יש מאין, or theory body text.
- Keep methodological safeguards, but move the homepage tone from apology/negation to a
  clearer reading-path frame.
- Shorten the repeated global footer line so it no longer repeats "not a closed doctrine"
  on every page; methodology/critique pages still carry the actual safeguards.
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "_product_docs" / "reports" / "BPI_V90_DEFENSIVE_COPY_POLISH_REPORT_HE.md"
REPORT.parent.mkdir(parents=True, exist_ok=True)

HOME_REPLACEMENTS = {
    ROOT / "site" / "index.html": [
        (
            "אין כאן טענה שהמדע מוכיח מטפיזיקה, וגם לא ניסיון לתת לפואטיקה להחליף דיוק. זה מודל קריאה: שפה שמבדילה בין ליבה, עדות ויישום, בלי לסגור את השאלה מהר מדי.",
            "האתר מציע מסלול קריאה: ליבה, עדות ויישום. המדע, הפואטיקה והסיפורים נשארים מובחנים, כדי שהרעיון יוכל להיבחן בלי להפוך להוכחה סגורה.",
        ),
    ],
    ROOT / "site" / "en.html": [
        (
            "There is no claim here that science proves metaphysics, or that poetic language can replace precision. It offers a reading model: a language that separates core, witness and application without closing the question too quickly.",
            "The site offers a reading path: core, witness and application. Science, poetics and stories remain distinct, so the idea can be examined without pretending to be a closed proof.",
        ),
    ],
}

FOOTER_REPLACEMENTS = [
    (
        "זה ניסוי מחשבתי פתוח לביקורת, לא דוקטרינה סגורה.",
        "ניסוי מחשבתי פתוח לקריאה, ביקורת והמשך עבודה.",
    ),
    (
        "This is an open thought experiment, not a closed doctrine.",
        "An open thought experiment for reading, critique and continued work.",
    ),
]

# Keep the actual methodological/critical safeguards where they belong.
SKIP_FOOTER_PATH_PARTS = {
    "/files/",  # document exports, not public page chrome
}


def replace_many(path: Path, replacements: list[tuple[str, str]]) -> tuple[bool, list[str]]:
    if not path.exists():
        return False, [f"missing: `{path.relative_to(ROOT)}`"]
    text = path.read_text(encoding="utf-8")
    original = text
    notes: list[str] = []
    for old, new in replacements:
        if old in text:
            text = text.replace(old, new)
            notes.append(f"replaced copy in `{path.relative_to(ROOT)}`")
    if text != original:
        path.write_text(text, encoding="utf-8")
        return True, notes
    return False, notes


def patch_home_method_notes() -> tuple[int, list[str]]:
    changed = 0
    notes: list[str] = []
    for path, replacements in HOME_REPLACEMENTS.items():
        did_change, local_notes = replace_many(path, replacements)
        changed += int(did_change)
        notes.extend(local_notes or [f"no homepage method-note change needed: `{path.relative_to(ROOT)}`"])
    return changed, notes


def patch_public_footers() -> tuple[int, list[str]]:
    changed_files = 0
    notes: list[str] = []
    for path in sorted((ROOT / "site").rglob("*.html")):
        rel = "/" + path.relative_to(ROOT).as_posix()
        if any(part in rel for part in SKIP_FOOTER_PATH_PARTS):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        original = text
        for old, new in FOOTER_REPLACEMENTS:
            text = text.replace(old, new)
        if text != original:
            path.write_text(text, encoding="utf-8")
            changed_files += 1
            notes.append(f"footer softened: `{path.relative_to(ROOT)}`")
    if not notes:
        notes.append("no footer changes needed")
    return changed_files, notes


def main() -> int:
    home_count, home_notes = patch_home_method_notes()
    footer_count, footer_notes = patch_public_footers()

    lines = [
        "# BPI V90 - צמצום התגוננות חוזרת בלי להחליש הגנות",
        "",
        f"Generated: {datetime.utcnow().isoformat(timespec='seconds')}Z",
        "",
        "העיקרון: הסייגים המתודולוגיים נשארים, אבל דף הבית והפוטר לא צריכים להישמע כאילו האתר מתנצל מראש בכל מקום.",
        "לא שונו בלארבים, סיפורים, תגיות AI כגון אין/יש/יש מאין, או גוף התאוריה.",
        "",
        "## שינויים",
        f"- homepage method-note files changed: {home_count}",
        f"- public footer files changed: {footer_count}",
        "",
        "## פירוט",
    ]
    lines.extend(f"- {note}" for note in home_notes)
    lines.extend(f"- {note}" for note in footer_notes)
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"homepage files changed: {home_count}")
    print(f"footer files changed: {footer_count}")
    print(f"report: {REPORT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
