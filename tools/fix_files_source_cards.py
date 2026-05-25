#!/usr/bin/env python3
"""Fix duplicated source-format buttons on public reader pages.

Visible product rule:
- "Inside the theory" / "בתוך התאוריה" is the reader path and may show HTML/PDF.
- "Source files" / "קבצי מקור" is the source/editing path and should show only formats
  that are not already duplicated there: DOCX and MD.

This script patches both places where these cards can appear:
- Files pages
- Applied / יישום pages

It does not change blurbs, theory text, document exports, or files under site/files.
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

HE_LINKS = [
    ("DOCX מלא", "../../files/between-potential-and-ideal-he.docx"),
    ("MD מלא", "../../files/between-potential-and-ideal-he.md"),
    ("DOCX לוגי", "../../files/editorial-tightened/between-potential-and-ideal-tightened-he.docx"),
    ("MD לוגי", "../../files/editorial-tightened/between-potential-and-ideal-tightened-he.md"),
]
EN_LINKS = [
    ("Full DOCX", "../../files/between-potential-and-ideal-en.docx"),
    ("Full MD", "../../files/between-potential-and-ideal-en.md"),
    ("Logical DOCX", "../../files/editorial-tightened/between-potential-and-ideal-tightened-en.docx"),
    ("Logical MD", "../../files/editorial-tightened/between-potential-and-ideal-tightened-en.md"),
]
EN_SOURCE_TITLES = ["source files", "source text files", "full source files", "complete source files"]

PAGES = [
    {
        "path": ROOT / "site" / "pages" / "he" / "files.html",
        "source_title_parts": ["קבצי מקור"],
        "source_desc": "כאן נשארים רק קבצי מקור ועריכה שלא מופיעים כבר בכרטיס בתוך התאוריה: DOCX ו־MD בגרסה המלאה והלוגית.",
        "compact_links": HE_LINKS,
    },
    {
        "path": ROOT / "site" / "pages" / "he" / "applied.html",
        "source_title_parts": ["קבצי מקור"],
        "source_desc": "כאן נשארים רק קבצי מקור ועריכה שלא מופיעים כבר בכרטיס בתוך התאוריה: DOCX ו־MD בגרסה המלאה והלוגית.",
        "compact_links": HE_LINKS,
    },
    {
        "path": ROOT / "site" / "pages" / "en" / "files-en.html",
        "source_title_parts": EN_SOURCE_TITLES,
        "source_desc": "Only source/editing formats that are not already shown in the reading path remain here: DOCX and MD.",
        "compact_links": EN_LINKS,
    },
    {
        "path": ROOT / "site" / "pages" / "en" / "applied-en.html",
        "source_title_parts": EN_SOURCE_TITLES,
        "source_desc": "Only source/editing formats that are not already shown in the reading path remain here: DOCX and MD.",
        "compact_links": EN_LINKS,
    },
]

SOURCE_EXTS = (".docx", ".md")
READER_EXTS = (".html", ".pdf")
HEADING_TAGS = ["h2", "h3", "h4"]
CARD_TAGS = ["section", "article", "div"]


def norm(text: str) -> str:
    return " ".join(text.split()).strip()


def classes(tag) -> list[str]:
    raw = tag.get("class") or []
    if isinstance(raw, str):
        raw = raw.split()
    return list(raw)


def clean_href(href: str) -> str:
    return href.split("#", 1)[0].split("?", 1)[0].lower()


def is_source_href(href: str) -> bool:
    return clean_href(href).endswith(SOURCE_EXTS)


def is_reader_href(href: str) -> bool:
    return clean_href(href).endswith(READER_EXTS)


def heading_text(tag) -> str:
    h = tag.find(HEADING_TAGS)
    return norm(h.get_text(" ", strip=True)) if h else ""


def title_matches(title: str, parts: list[str]) -> bool:
    low = title.lower()
    return any(part.lower() in low for part in parts)


def is_source_section(tag, config: dict) -> bool:
    if tag.get("id") == "source-files":
        return True
    if "source-files-section" in classes(tag):
        return True
    return title_matches(heading_text(tag), config["source_title_parts"])


def is_theory_article(article) -> bool:
    title = heading_text(article).lower()
    if any(word in title for word in ["appendix", "stories", "סיפורים", "נספח"]):
        return False
    hrefs = [a.get("href", "") for a in article.find_all("a", href=True)]
    theory_href = any("between-potential-and-ideal" in href or "editorial-tightened" in href for href in hrefs)
    source_or_reader = any(is_source_href(href) or is_reader_href(href) for href in hrefs)
    return theory_href and source_or_reader


def make_actions(soup: BeautifulSoup, links: list[tuple[str, str]], cls: str):
    div = soup.new_tag("div")
    div["class"] = cls
    for label, href in links:
        a = soup.new_tag("a", href=href)
        a["class"] = "download-button"
        a["target"] = "_blank"
        a["rel"] = "noopener noreferrer"
        a.string = label
        div.append(a)
        div.append("\n")
    return div


def find_actions_container(parent):
    candidates = []
    for tag in parent.find_all(["div", "p", "nav"]):
        if not tag.find("a", href=True):
            continue
        cls = classes(tag)
        if any("download" in c or "actions" in c or "formats" in c or "row" in c for c in cls):
            candidates.append(tag)
    return candidates[-1] if candidates else None


def replace_first_paragraph(parent, text: str) -> bool:
    for p in parent.find_all("p"):
        if norm(p.get_text(" ", strip=True)):
            if norm(p.get_text(" ", strip=True)) != text:
                p.string = text
                return True
            return False
    return False


def patch_source_section(soup: BeautifulSoup, section, config: dict) -> tuple[bool, int]:
    changed = False
    touched = 0
    changed = replace_first_paragraph(section, config["source_desc"]) or changed

    articles = section.find_all("article")
    if articles:
        for article in articles:
            if not is_theory_article(article):
                continue
            actions = find_actions_container(article)
            if actions is None:
                continue
            kept = []
            for a in actions.find_all("a", href=True):
                href = a.get("href", "")
                if is_source_href(href):
                    kept.append((norm(a.get_text(" ", strip=True)), href))
            if not kept:
                continue
            new_actions = make_actions(soup, kept, "download-row")
            if str(actions) != str(new_actions):
                actions.replace_with(new_actions)
                changed = True
                touched += 1
        return changed, touched

    # Compact card without nested articles: replace all actions with the canonical source-only set.
    actions = find_actions_container(section)
    if actions is not None:
        new_actions = make_actions(soup, config["compact_links"], "appendix-actions source-only-actions")
        if str(actions) != str(new_actions):
            actions.replace_with(new_actions)
            changed = True
            touched += 1
    return changed, touched


def patch_page(config: dict) -> tuple[bool, str]:
    path = config["path"]
    if not path.exists():
        return False, f"missing: {path.relative_to(ROOT)}"

    old = path.read_text(encoding="utf-8")
    soup = BeautifulSoup(old, "html.parser")
    sections = []
    for tag in soup.find_all(CARD_TAGS):
        if is_source_section(tag, config):
            # Avoid duplicate descendants by keeping only the outer useful section/card.
            if not any(tag in parent.find_all(CARD_TAGS) for parent in sections):
                sections.append(tag)

    if not sections:
        return False, f"source card/section not found: {path.relative_to(ROOT)}"

    changed = False
    touched_total = 0
    for section in sections:
        section_changed, touched = patch_source_section(soup, section, config)
        changed = changed or section_changed
        touched_total += touched

    new = str(soup)
    if changed and new != old:
        path.write_text(new, encoding="utf-8")
        return True, f"patched: {path.relative_to(ROOT)} ({touched_total} card/action group(s))"
    return False, f"no visible change needed: {path.relative_to(ROOT)}"


def main() -> int:
    lines = [
        "# BPI V88 - תיקון כרטיס קבצי מקור",
        "",
        f"Generated: {datetime.utcnow().isoformat(timespec='seconds')}Z",
        "",
        "הכלל: קבצי מקור מציגים רק פורמטים שלא מופיעים כבר במסלול הקריאה: DOCX/MD ולא HTML/PDF.",
        "ההחלה כוללת את עמודי הקבצים ואת עמודי היישום בעברית ובאנגלית.",
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