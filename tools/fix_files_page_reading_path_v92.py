#!/usr/bin/env python3
"""BPI V92 — Add a recommended reading path to the Files pages.

Critic-driven goal:
- The files pages should not feel like a raw archive/file dump.
- Keep every file, archive table, search/filter, license and transparency layer intact.
- Add a small product-level "what to open first" section near the top.

Protected choices:
- No blurbs, stories, theory body, titles, subtitles, images, export files or tables are deleted.
- This patch adds one guided section to each Files page and adds a scoped body class for CSS.
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

from bs4 import BeautifulSoup  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "_product_docs" / "reports" / "BPI_V92_FILES_READING_PATH_REPORT_HE.md"
REPORT.parent.mkdir(parents=True, exist_ok=True)

PAGES = [
    {
        "path": ROOT / "site" / "pages" / "he" / "files.html",
        "dir": "rtl",
        "section_label": "התחלה מומלצת",
        "intro": "לפני הארכיון המלא, זהו מסלול קצר לקורא חדש: פתיחה, נוסח מהודק, ואז הליבה. כל הקבצים נשארים זמינים בהמשך הדף.",
        "cards": [
            {
                "title": "תקציר",
                "body": "פתיחה מהירה למסלול הקריאה, המושגים המרכזיים ומה כדאי לפתוח קודם.",
                "links": [("קרא", "summary.html", True)],
            },
            {
                "title": "הגרסה הלוגית",
                "body": "קריאה מהודקת יותר של המבנה, ההבחנות והתנאים — בלי להיכנס מיד לארכיון כולו.",
                "links": [
                    ("HTML", "../../files/editorial-tightened/between-potential-and-ideal-tightened-he.html", True),
                    ("PDF", "../../files/editorial-tightened/between-potential-and-ideal-tightened-he.pdf", False),
                ],
            },
            {
                "title": "ליבה",
                "body": "הדרך הישירה לשלושת המושגים: פוטנציאל, אידיאל ואופטימלי.",
                "links": [("קרא", "core.html", True)],
            },
        ],
    },
    {
        "path": ROOT / "site" / "pages" / "en" / "files-en.html",
        "dir": "ltr",
        "section_label": "Recommended start",
        "intro": "Before the full archive, this is the short path for a new reader: orientation, the tighter logical version, then the core. All files remain available below.",
        "cards": [
            {
                "title": "Summary",
                "body": "A quick orientation to the reading path, the central terms, and what to open first.",
                "links": [("Read", "summary-en.html", True)],
            },
            {
                "title": "Logical version",
                "body": "A tighter reading of the structure, distinctions and conditions without entering the full archive first.",
                "links": [
                    ("HTML", "../../files/editorial-tightened/between-potential-and-ideal-tightened-en.html", True),
                    ("PDF", "../../files/editorial-tightened/between-potential-and-ideal-tightened-en.pdf", False),
                ],
            },
            {
                "title": "Core",
                "body": "The direct path into the three central terms: potential, ideal and optimal.",
                "links": [("Read", "core-en.html", True)],
            },
        ],
    },
]


def class_list(tag) -> list[str]:
    raw = tag.get("class") or []
    if isinstance(raw, str):
        raw = raw.split()
    return list(raw)


def add_class(tag, name: str) -> bool:
    classes = class_list(tag)
    if name in classes:
        return False
    classes.append(name)
    tag["class"] = classes
    return True


def make_section(soup: BeautifulSoup, config: dict):
    section = soup.new_tag("section")
    section["class"] = "reader-card media-card accent-files files-reading-path"
    section["aria-labelledby"] = "files-reading-path-title"

    h2 = soup.new_tag("h2", id="files-reading-path-title")
    h2.string = config["section_label"]
    section.append(h2)

    p = soup.new_tag("p")
    p["class"] = "ai-section-lead"
    p.string = config["intro"]
    section.append(p)

    grid = soup.new_tag("div")
    grid["class"] = "reading-path-grid"

    for card in config["cards"]:
        article = soup.new_tag("article")
        article["class"] = "reading-path-card"
        title = soup.new_tag("h3")
        title.string = card["title"]
        article.append(title)
        body = soup.new_tag("p")
        body.string = card["body"]
        article.append(body)
        actions = soup.new_tag("div")
        actions["class"] = "reading-path-actions"
        for label, href, primary in card["links"]:
            a = soup.new_tag("a", href=href)
            if primary:
                a["class"] = "primary-format"
            a.string = label
            actions.append(a)
        article.append(actions)
        grid.append(article)

    section.append(grid)
    return section


def find_insert_after(soup: BeautifulSoup):
    # Prefer the visible page title block. Fallback to first child in main.
    for section in soup.find_all("section"):
        if "page-title" in class_list(section):
            return section
    main = soup.find("main")
    if main:
        for child in main.find_all(recursive=False):
            if getattr(child, "name", None):
                return child
    return None


def patch_page(config: dict) -> tuple[bool, list[str]]:
    path = config["path"]
    if not path.exists():
        return False, [f"missing: `{path.relative_to(ROOT)}`"]

    old = path.read_text(encoding="utf-8")
    soup = BeautifulSoup(old, "html.parser")
    notes: list[str] = []

    changed = False
    body = soup.find("body")
    if body is not None and add_class(body, "section-files"):
        changed = True
        notes.append("added `section-files` body class")

    existing = soup.find("section", class_="files-reading-path")
    if existing is None:
        anchor = find_insert_after(soup)
        if anchor is None:
            return changed, ["could not find insertion anchor"]
        anchor.insert_after(make_section(soup, config))
        changed = True
        notes.append("inserted recommended reading path section")
    else:
        notes.append("recommended reading path already exists")

    new = str(soup)
    if changed and new != old:
        path.write_text(new, encoding="utf-8")
        return True, notes
    return False, notes or ["no change needed"]


def main() -> int:
    changed_count = 0
    lines = [
        "# BPI V92 - מסלול קריאה בדף הקבצים",
        "",
        f"Generated: {datetime.utcnow().isoformat(timespec='seconds')}Z",
        "",
        "מטרה: להפוך את דף הקבצים ממפגש ראשון ארכיוני למסך מוצרי מדורג, בלי למחוק קבצים, בלי להסתיר את הארכיון ובלי לשנות כותרות/תמונות/תוכן תאורטי.",
        "",
        "## תוצאות",
    ]

    for config in PAGES:
        did_change, notes = patch_page(config)
        changed_count += int(did_change)
        lines.append(f"### `{config['path'].relative_to(ROOT)}`")
        lines.append(f"- changed: {did_change}")
        lines.extend(f"- {note}" for note in notes)
        lines.append("")

    lines.extend([
        "## בדיקת הצלחה ידנית",
        "- בראש דף הקבצים מופיע מסלול קצר: תקציר / גרסה לוגית / ליבה.",
        "- הטבלה, החיפוש, הסינון, הארכיון והקבצים הקיימים נשארים במקום.",
        "- העמוד מרגיש כמו מסלול קריאה לפני שהוא מרגיש כמו ארכיון.",
    ])
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"changed pages: {changed_count}")
    print(f"report: {REPORT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
