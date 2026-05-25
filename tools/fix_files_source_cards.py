#!/usr/bin/env python3
"""Fix Files page source-card duplication.

Rule:
- The "Inside the theory" card exposes reader formats: full HTML/PDF and logical HTML/PDF.
- The "Source files" card must expose only formats that are not already shown there:
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
        "lang": "he",
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
        "lang": "en",
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


def has_card_class(tag) -> bool:
    classes = tag.get("class") or []
    if isinstance(classes, str):
        classes = classes.split()
    return any("card" in c or "media" in c or "reader" in c or "file" in c for c in classes)


def card_heading(tag) -> str:
    heading = tag.find(HEADING_TAGS)
    return norm(heading.get_text(" ", strip=True)) if heading else ""


def find_exact_card(soup: BeautifulSoup, titles: set[str]):
    candidates = []
    for tag in soup.find_all(CARD_TAGS):
        if not has_card_class(tag):
            continue
        title = card_heading(tag)
        if title in titles:
            candidates.append(tag)
    if candidates:
        return candidates[0]
    return None


def find_actions_container(soup: BeautifulSoup, card):
    for tag in card.find_all(["div", "p", "nav"]):
        classes = tag.get("class") or []
        if isinstance(classes, str):
            classes = classes.split()
        if any("actions" in c or "download" in c or "formats" in c for c in classes) and tag.find("a"):
            return tag
    # fallback: group all direct/action links into a new clean action row
    container = soup.new_tag("div")
    container["class"] = "appendix-actions source-only-actions"
    card.append(container)
    return container


def replace_description(card, text: str):
    paragraphs = [p for p in card.find_all("p") if norm(p.get_text(" ", strip=True))]
    if paragraphs:
        paragraphs[0].string = text


def replace_actions(soup: BeautifulSoup, actions, links: list[tuple[str, str]]):
    actions.clear()
    classes = actions.get("class") or []
    if isinstance(classes, str):
        classes = classes.split()
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
    source_card = find_exact_card(soup, config["source_titles"])
    if source_card is None:
        return False, f"source card not found: {path.relative_to(ROOT)}"

    theory_card = find_exact_card(soup, config["theory_titles"])
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
