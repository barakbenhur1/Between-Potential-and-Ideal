#!/usr/bin/env python3
"""BPI V96 — user-requested reverts and order fixes.

User rules applied:
- AI labels must remain exactly: אין / יש / יש מאין, and English equivalents No / Yes / Being from Nothing.
- Do not change the text of blurbs; remove the homepage blurbs section entirely as requested.
- Move tab visuals above the newly added recommended-start/source-responsibility blocks.
- Keep design structure and existing file/archive content intact.
- For files page logical English card: keep the card size but move its action row up with a class hook.
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

from bs4 import BeautifulSoup  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "_product_docs" / "reports" / "BPI_V96_USER_REQUESTED_REVERTS_REPORT_HE.md"
REPORT.parent.mkdir(parents=True, exist_ok=True)

HOME_PAGES = [ROOT / "site" / "index.html", ROOT / "site" / "en.html"]
AI_REPLACEMENTS = {
    ROOT / "site" / "pages" / "he" / "ai.html": [
        ("שאלת האין", "אין"),
        ("שאלת היש", "יש"),
        ("שאלת המעבר מן האין אל היש", "יש מאין"),
    ],
    ROOT / "site" / "pages" / "en" / "ai-en.html": [
        ("Question of Nothingness", "No"),
        ("Question of Being", "Yes"),
        ("Being from Nothing / The Passage Question", "Being from Nothing"),
    ],
}
TAB_ORDER_PAGES = [
    ROOT / "site" / "pages" / "he" / "files.html",
    ROOT / "site" / "pages" / "en" / "files-en.html",
    ROOT / "site" / "pages" / "he" / "sources.html",
    ROOT / "site" / "pages" / "en" / "sources-en.html",
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


def patch_ai_labels() -> tuple[int, list[str]]:
    changed = 0
    notes: list[str] = []
    for path, replacements in AI_REPLACEMENTS.items():
        if not path.exists():
            notes.append(f"missing: `{path.relative_to(ROOT)}`")
            continue
        text = path.read_text(encoding="utf-8")
        old_text = text
        for old, new in replacements:
            if old in text:
                text = text.replace(old, new)
                notes.append(f"`{path.relative_to(ROOT)}`: `{old}` → `{new}`")
        if text != old_text:
            path.write_text(text, encoding="utf-8")
            changed += 1
    return changed, notes


def remove_home_blurbs() -> tuple[int, list[str]]:
    changed = 0
    notes: list[str] = []
    for path in HOME_PAGES:
        if not path.exists():
            notes.append(f"missing: `{path.relative_to(ROOT)}`")
            continue
        old = path.read_text(encoding="utf-8")
        soup = BeautifulSoup(old, "html.parser")
        removed = 0
        for section in soup.find_all("section"):
            classes = class_list(section)
            if "signature-blurbs" in classes or "refined-blurbs" in classes:
                section.decompose()
                removed += 1
        if removed:
            path.write_text(str(soup), encoding="utf-8")
            changed += 1
            notes.append(f"`{path.relative_to(ROOT)}`: removed homepage blurbs section ({removed})")
        else:
            notes.append(f"`{path.relative_to(ROOT)}`: no homepage blurbs section found")
    return changed, notes


def find_page_title(soup: BeautifulSoup):
    for section in soup.find_all("section"):
        if "page-title" in class_list(section):
            return section
    main = soup.find("main")
    if main:
        for child in main.find_all(recursive=False):
            if getattr(child, "name", None):
                return child
    return None


def is_tab_visual(tag) -> bool:
    if getattr(tag, "name", None) != "figure":
        return False
    classes = class_list(tag)
    if "tab-visual" in classes or "compact-section-visual" in classes:
        return True
    img = tag.find("img")
    src = img.get("src", "") if img else ""
    return "tab_" in src


def move_tab_visuals() -> tuple[int, list[str]]:
    changed = 0
    notes: list[str] = []
    for path in TAB_ORDER_PAGES:
        if not path.exists():
            notes.append(f"missing: `{path.relative_to(ROOT)}`")
            continue
        old = path.read_text(encoding="utf-8")
        soup = BeautifulSoup(old, "html.parser")
        title = find_page_title(soup)
        visual = None
        for figure in soup.find_all("figure"):
            if is_tab_visual(figure):
                visual = figure
                break
        if title is None or visual is None:
            notes.append(f"`{path.relative_to(ROOT)}`: page title or tab visual not found")
            continue
        node = title.next_sibling
        while node is not None and getattr(node, "name", None) is None and not str(node).strip():
            node = node.next_sibling
        if node is not visual:
            visual.extract()
            title.insert_after(visual)
            path.write_text(str(soup), encoding="utf-8")
            changed += 1
            notes.append(f"`{path.relative_to(ROOT)}`: moved tab visual directly under page title")
        else:
            notes.append(f"`{path.relative_to(ROOT)}`: tab visual already directly under page title")
    return changed, notes


def mark_logical_file_card_actions() -> tuple[int, list[str]]:
    changed = 0
    notes: list[str] = []
    for path in [ROOT / "site" / "pages" / "he" / "files.html", ROOT / "site" / "pages" / "en" / "files-en.html"]:
        if not path.exists():
            continue
        old = path.read_text(encoding="utf-8")
        soup = BeautifulSoup(old, "html.parser")
        local_changed = False
        for heading in soup.find_all(["h2", "h3", "h4"]):
            text = heading.get_text(" ", strip=True)
            if ("גרסה לוגית" in text or "הגרסה הלוגית" in text or "Logical" in text) and ("English" in text or "אנגלית" in text or "לוגית" in text or "version" in text):
                card = heading.find_parent(["article", "section", "div"])
                while card and not any(c in class_list(card) for c in ["file-card", "appendix-card", "hub-card", "media-card", "reading-path-card"]):
                    card = card.find_parent(["article", "section", "div"])
                if card and add_class(card, "source-card-actions-top"):
                    local_changed = True
        if local_changed:
            path.write_text(str(soup), encoding="utf-8")
            changed += 1
            notes.append(f"`{path.relative_to(ROOT)}`: marked logical file card for top-aligned actions")
        else:
            notes.append(f"`{path.relative_to(ROOT)}`: no logical card class change needed/found")
    return changed, notes


def main() -> int:
    sections = []
    total_changed = 0
    for title, func in [
        ("AI labels", patch_ai_labels),
        ("Homepage blurbs", remove_home_blurbs),
        ("Tab visual order", move_tab_visuals),
        ("Files logical card actions", mark_logical_file_card_actions),
    ]:
        count, notes = func()
        total_changed += count
        sections.append((title, count, notes))

    lines = [
        "# BPI V96 - תיקוני משתמש: טקסטים מקוריים, סדר תמונות, והסרת בלרבים",
        "",
        f"Generated: {datetime.utcnow().isoformat(timespec='seconds')}Z",
        "",
        "בוצעו רק תיקונים לפי בקשת המשתמש: החזרת טקסטי AI המקוריים, הסרת בלרבים מדף הבית, הזזת תמונות טאב למיקום התקני, וסימון כרטיסי גרסה לוגית ליישור כפתורים. לא שונו כותרות/תתי־כותרות/תמונות.",
        "",
        f"Changed groups: {total_changed}",
        "",
    ]
    for title, count, notes in sections:
        lines.append(f"## {title}")
        lines.append(f"- changed files/groups: {count}")
        lines.extend(f"- {note}" for note in notes)
        lines.append("")

    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"changed groups: {total_changed}")
    print(f"report: {REPORT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
