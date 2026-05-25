#!/usr/bin/env python3
"""Fix Files page source-card duplication.

Rule:
- The visible "Inside the theory" card exposes reader formats: full HTML/PDF and logical HTML/PDF.
- The visible "Source files" card must expose only formats that are not already shown there:
  full DOCX/MD and logical DOCX/MD.

This script patches the Hebrew and English public Files pages without touching blurbs,
main theory text, document exports, or archive files.
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

try:
    from bs4 import BeautifulSoup  # type: ignore
except Exception as exc:  # pragma: no cover
    raise SystemExit("Missing dependency: beautifulsoup4. Install with: python3 -m pip install beautifulsoup4") from exc

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "_product_docs" / "reports" / "BPI_V88_FILES_SOURCE_CARD_DEDUPE_REPORT_HE.md"
REPORT.parent.mkdir(parents=True, exist_ok=True)

PAGES = [
    {
        "path": ROOT / "site" / "pages" / "he" / "files.html",
        "source_titles": {"קבצי מקור"},
        "theory_titles": {"בתוך התאוריה"},
        "description": "כאן נשארים רק קבצי מקור ועריכה שלא מופיעים כבר בכרטיס בתוך התאוריה: DOCX ו־MD בגרסה המלאה והלוגית.",
        "links": [
            ("DOCX מלא", "../../files/between-potential-and-ideal-he.docx"),
            ("MD מלא", "../../files/between-potential-and-ideal-he.md"),
            ("DOCX לוגי", "../../files/editorial-tightened/between-potential-and-ideal-tightened-he.docx"),
            ("MD לוגי", "../../files/editorial-tightened/between-potential-and-ideal-tightened-he.md"),
        ],
    },
    {
        "path": ROOT / "site" / "pages" / "en" / "files-en.html",
        "source_titles": {"Source files", "Source Files"},
        "theory_titles": {"Inside the theory", "Within the theory", "In the theory"},
        "description": "Only source/editing formats that are not already shown in the Inside the theory card remain here: full and logical DOCX/MD.",
        "links": [
            ("Full DOCX", "../../files/between-potential-and-ideal-en.docx"),
            ("Full MD", "../../files/between-potential-and-ideal-en.md"),
            ("Logical DOCX", "../../files/editorial-tightened/between-potential-and-ideal-tightened-en.docx"),
            ("Logical MD", "../../files/editorial-tightened/between-potential-and-ideal-tightened-en.md"),
        ],
    },
]

CARD_TAGS = ["section", "article", "div"]
HEADING_TAGS = ["h2", "h3", "h4"]


def norm(text: str) -> str:
    return " ".join(text.split()).strip()


def class_list(tag) -> list[str]:
    classes = tag.get("class") or []
    if isinstance(classes, str):
        classes = classes.split()
    return list(classes)


def is_big_archive_section(tag) -> bool:
    title = first_heading_text(tag)
    return title in {"קבצי מקור מלאים", "Full source files", "Complete source files"}


def first_heading_text(tag) -> str:
    heading = tag.find(HEADING_TAGS)
    return norm(heading.get_text(" ", strip=True)) if heading else ""


def closest_card_for_heading(heading):
    """Return the smallest useful visual card around a heading.

    The previous version required card classes and missed the actual visible card.
    This version starts from the exact visible heading and climbs only until it finds
    a compact parent with action/download links, while avoiding the large archive section.
    """
    cur = heading
    best = None
    while cur and getattr(cur, "name", None) != "main":
        if cur.name in CARD_TAGS:
            links = cur.find_all("a", href=True)
            classes = class_list(cur)
            title = first_heading_text(cur)
            if len(links) >= 2 and title == norm(heading.get_text(" ", strip=True)) and not is_big_archive_section(cur):
                best = cur
                if any("card" in c or "media" in c or "reader" in c or "file" in c for c in classes):
                    return cur
        cur = cur.parent
    return best


def find_card_by_exact_heading(soup: BeautifulSoup, titles: set[str]):
    for heading in soup.find_all(HEADING_TAGS):
        if norm(heading.get_text(" ", strip=True)) in titles:
            card = closest_card_for_heading(heading)
            if card is not None:
                return card
    return None


def find_actions_container(soup: BeautifulSoup, card):
    preferred = []
    fallback = []
    for tag in card.find_all(["div", "p", "nav"]):
        if not tag.find("a", href=True):
            continue
        classes = class_list(tag)
        if any("actions" in c or "download" in c or "formats" in c or "row" in c for c in classes):
            preferred.append(tag)
        else:
            fallback.append(tag)
    if preferred:
        return preferred[-1]
    if fallback:
        return fallback[-1]
    container = soup.new_tag("div")
    container["class"] = "appendix-actions source-only-actions"
    card.append(container)
    return container


def replace_description(card, text: str):
    heading = card.find(HEADING_TAGS)
    for p in card.find_all("p"):
        if heading and p.sourceline and heading.sourceline and p.sourceline < heading.sourceline:
            continue
        if norm(p.get_text(" ", strip=True)):
            p.string = text
            return


def replace_actions(soup: BeautifulSoup, actions, links: list[tuple[str, str]]):
    actions.clear()
    classes = class_list(actions)
    for cls in ["appendix-actions", "source-only-actions"]:
        if cls not in classes:
            classes.append(cls)
    actions["class"] = classes
    for label, href in links:
        a = soup.new_tag("a", href=href)
        a.string = label
        a["rel"] = "noopener noreferrer"
        a["target"] = "_blank"
        actions.append(a)
        actions.append("\n")


def patch_page(config: dict) -> tuple[bool, str]:
    path = config["path"]
    if not path.exists():
        return False, f"missing: {path.relative_to(ROOT)}"

    html = path.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")
    source_card = find_card_by_exact_heading(soup, config["source_titles"])
    if source_card is None:
        return False, f"source card not found: {path.relative_to(ROOT)}"

    theory_card = find_card_by_exact_heading(soup, config["theory_titles"])
    theory_hrefs = {a.get("href") for a in theory_card.find_all("a", href=True)} if theory_card else set()
    links = [(label, href) for label, href in config["links"] if href not in theory_hrefs]

    actions = find_actions_container(soup, source_card)
    replace_description(source_card, config["description"])
    replace_actions(soup, actions, links)

    new_html = str(soup)
    if new_html != html:
        path.write_text(new_html, encoding="utf-8")
        return True, f"patched: {path.relative_to(ROOT)} -> {', '.join(label for label, _ in links)}"
    return False, f"no change: {path.relative_to(ROOT)}"


def main() -> int:
    lines = [
        "# BPI V88 - תיקון כרטיס קבצי מקור",
        "",
        f"Generated: {datetime.utcnow().isoformat(timespec='seconds')}Z",
        "",
        "הכלל: כרטיס קבצי מקור מציג רק פורמטים שלא מופיעים כבר בכרטיס בתוך התאוריה.",
        "לכן נשארים בו DOCX/MD מלאים ולוגיים, ולא HTML/PDF שכבר מוצגים בכרטיס הקריאה.",
        "",
    ]
    changed = 0
    for config in PAGES:
        did_change, msg = patch_page(config)
        if did_change:
            changed += 1
        lines.append(f"- {msg}")

    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"changed pages: {changed}")
    for line in lines[7:]:
        print(line)
    print(f"report: {REPORT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
