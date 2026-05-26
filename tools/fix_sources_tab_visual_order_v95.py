#!/usr/bin/env python3
"""BPI V95 — Keep Sources tab visual directly under the page title.

Product rule:
- The tab hero image belongs immediately below the page title, before any content cards.
- This matches the other tabs (Witness, Core, Application, AI, Files).
- Do not change text, headings, subtitles, images, or the responsibility map content.
- Only move the existing tab visual if it appears lower on the page.
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

from bs4 import BeautifulSoup  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "_product_docs" / "reports" / "BPI_V95_SOURCES_TAB_VISUAL_ORDER_REPORT_HE.md"
REPORT.parent.mkdir(parents=True, exist_ok=True)

PAGES = [
    ROOT / "site" / "pages" / "he" / "sources.html",
    ROOT / "site" / "pages" / "en" / "sources-en.html",
]


def class_list(tag) -> list[str]:
    raw = tag.get("class") or []
    if isinstance(raw, str):
        raw = raw.split()
    return list(raw)


def find_page_title(soup: BeautifulSoup):
    for section in soup.find_all("section"):
        if "page-title" in class_list(section):
            return section
    return None


def is_tab_visual(tag) -> bool:
    if getattr(tag, "name", None) != "figure":
        return False
    classes = class_list(tag)
    if "tab-visual" in classes or "compact-section-visual" in classes:
        return True
    img = tag.find("img")
    src = img.get("src", "") if img else ""
    return "tab_sources" in src or "tab_sources_unique" in src


def find_sources_tab_visual(soup: BeautifulSoup):
    for figure in soup.find_all("figure"):
        if is_tab_visual(figure):
            return figure
    return None


def patch_page(path: Path) -> tuple[bool, str]:
    if not path.exists():
        return False, f"missing: `{path.relative_to(ROOT)}`"

    old = path.read_text(encoding="utf-8")
    soup = BeautifulSoup(old, "html.parser")

    title = find_page_title(soup)
    visual = find_sources_tab_visual(soup)

    if title is None:
        return False, "page-title section not found"
    if visual is None:
        return False, "tab visual figure not found"

    # Already directly after page title except for whitespace/text nodes.
    node = title.next_sibling
    while node is not None and getattr(node, "name", None) is None and not str(node).strip():
        node = node.next_sibling
    if node is visual:
        return False, "tab visual already directly below page title"

    visual.extract()
    title.insert_after(visual)

    new = str(soup)
    if new != old:
        path.write_text(new, encoding="utf-8")
        return True, "moved tab visual directly below page title"
    return False, "no visible change"


def main() -> int:
    changed_count = 0
    lines = [
        "# BPI V95 - מיקום תמונת הטאב בדף המקורות",
        "",
        f"Generated: {datetime.utcnow().isoformat(timespec='seconds')}Z",
        "",
        "מטרה: בדף המקורות תמונת הטאב צריכה להופיע מיד מתחת לכותרת הדף, כמו בשאר הטאבים. לא שונו טקסטים, כותרות, תתי־כותרות, תמונות או תוכן מפת האחריות.",
        "",
        "## תוצאות",
    ]

    for path in PAGES:
        changed, note = patch_page(path)
        changed_count += int(changed)
        lines.append(f"- `{path.relative_to(ROOT)}`: {note}")

    lines.extend([
        "",
        "## בדיקת הצלחה ידנית",
        "- בדף המקורות בעברית ובאנגלית: כותרת הדף → תמונת הטאב → מפת אחריות/שאר התוכן.",
        "- התמונה עצמה לא השתנתה; רק המיקום שלה בסדר הדף.",
    ])
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"changed pages: {changed_count}")
    print(f"report: {REPORT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
