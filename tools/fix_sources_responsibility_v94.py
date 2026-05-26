#!/usr/bin/env python3
"""BPI V94 — Add source/claim responsibility maps.

Critic-driven goal:
- The Sources page should defend the project by clarifying how risky scientific,
  logical, AI and philosophical references are being used.
- Do not turn the page into a dry academic proof.
- Do not change existing source text, titles, images, or document exports.
- Add a compact responsibility table near the top of the sources pages.
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

from bs4 import BeautifulSoup  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "_product_docs" / "reports" / "BPI_V94_SOURCES_RESPONSIBILITY_REPORT_HE.md"
REPORT.parent.mkdir(parents=True, exist_ok=True)

PAGES = [
    {
        "path": ROOT / "site" / "pages" / "he" / "sources.html",
        "title": "מפת אחריות לפי שימוש",
        "intro": "המקורות כאן אינם מוצגים כהוכחה לתאוריה. הם מסמנים גבולות, שפות עבודה והבדלים בין מקור, השראה, מטאפורה, אנלוגיה וטענה פורמלית.",
        "headers": ["אזור", "איך הוא משמש", "סייג קרוב", "רמת סיכון"],
        "rows": [
            ["פיזיקה וקוסמולוגיה", "מטאפורה מבנית ומודל קריאה לגבול, מדידה ואופק.", "לא הוכחה פיזיקלית לפוטנציאל או אידיאל.", "גבוהה", "source-risk-high"],
            ["לוגיקה וחישוביות", "שפה להבחנות, אילוצים, בדיקות וקושי פורמלי.", "לא מעבר אוטומטי מטענה פורמלית לטענה מטפיזית.", "בינונית", "source-risk-medium"],
            ["AI ושפה", "מראה לשונית, בדיקת לחץ וכלי פרשני.", "לא סמכות, לא תודעה, לא עדות חיה.", "גבוהה", "source-risk-high"],
            ["פילוסופיה ומסורת", "הקשר רעיוני והשוואה בין שאלות קיימות.", "לא בעלות על מקור, לא החלפה של מסורת קיימת.", "בינונית", "source-risk-medium"],
            ["סיפורים ועדות", "חומר חי שמחזיק מרחק, חיכוך וניסיון.", "לא הוכחה כללית; עדות נשארת מקומית וחלקית.", "נמוכה", "source-risk-low"],
        ],
    },
    {
        "path": ROOT / "site" / "pages" / "en" / "sources-en.html",
        "title": "Responsibility map by use",
        "intro": "The sources here are not presented as proof of the theory. They mark boundaries, working languages, and the difference between source, influence, metaphor, analogy, and formal claim.",
        "headers": ["Area", "How it is used", "Close caution", "Risk level"],
        "rows": [
            ["Physics and cosmology", "Structural metaphor and reading model for boundary, measurement, and horizon.", "Not physical proof of potential or ideal.", "High", "source-risk-high"],
            ["Logic and computation", "A language for distinctions, constraints, tests, and formal difficulty.", "No automatic move from formal claim to metaphysics.", "Medium", "source-risk-medium"],
            ["AI and language", "Linguistic mirror, stress test, and interpretive tool.", "Not authority, not consciousness, not living witness.", "High", "source-risk-high"],
            ["Philosophy and tradition", "Conceptual context and comparison with existing questions.", "Not ownership of a source and not replacement of existing traditions.", "Medium", "source-risk-medium"],
            ["Stories and witness", "Living material that carries distance, friction, and experience.", "Not general proof; witness remains local and partial.", "Low", "source-risk-low"],
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


def make_section(soup: BeautifulSoup, cfg: dict):
    section = soup.new_tag("section")
    section["class"] = "reader-card media-card accent-sources source-responsibility-map"

    h2 = soup.new_tag("h2")
    h2.string = cfg["title"]
    section.append(h2)

    intro = soup.new_tag("p")
    intro.string = cfg["intro"]
    section.append(intro)

    wrapper = soup.new_tag("div")
    wrapper["class"] = "table-wrap"
    table = soup.new_tag("table")
    table["class"] = "source-responsibility-table"

    thead = soup.new_tag("thead")
    trh = soup.new_tag("tr")
    for header in cfg["headers"]:
        th = soup.new_tag("th")
        th.string = header
        trh.append(th)
    thead.append(trh)
    table.append(thead)

    tbody = soup.new_tag("tbody")
    for row in cfg["rows"]:
        tr = soup.new_tag("tr")
        for idx, value in enumerate(row[:4]):
            td = soup.new_tag("td")
            td["data-label"] = cfg["headers"][idx]
            if idx == 3:
                span = soup.new_tag("span")
                span["class"] = row[4]
                span.string = value
                td.append(span)
            else:
                td.string = value
            tr.append(td)
        tbody.append(tr)
    table.append(tbody)
    wrapper.append(table)
    section.append(wrapper)
    return section


def find_anchor(soup: BeautifulSoup):
    for section in soup.find_all("section"):
        if "page-title" in class_list(section):
            return section
    main = soup.find("main")
    if main:
        for child in main.find_all(recursive=False):
            if getattr(child, "name", None):
                return child
    return None


def patch_page(cfg: dict) -> tuple[bool, list[str]]:
    path = cfg["path"]
    if not path.exists():
        return False, [f"missing: `{path.relative_to(ROOT)}`"]

    old = path.read_text(encoding="utf-8")
    soup = BeautifulSoup(old, "html.parser")
    changed = False
    notes: list[str] = []

    body = soup.find("body")
    if body is not None and add_class(body, "section-sources"):
        changed = True
        notes.append("added `section-sources` body class")

    if soup.find("section", class_="source-responsibility-map") is None:
        anchor = find_anchor(soup)
        if anchor is None:
            return changed, ["could not find insertion anchor"]
        anchor.insert_after(make_section(soup, cfg))
        changed = True
        notes.append("inserted responsibility map")
    else:
        notes.append("responsibility map already exists")

    new = str(soup)
    if changed and new != old:
        path.write_text(new, encoding="utf-8")
        return True, notes
    return False, notes or ["no change needed"]


def main() -> int:
    changed_count = 0
    lines = [
        "# BPI V94 - מפת אחריות בדף המקורות",
        "",
        f"Generated: {datetime.utcnow().isoformat(timespec='seconds')}Z",
        "",
        "מטרה: לחזק את ההגנה המדעית/לוגית בלי להפוך את האתר למאמר יבש. הטבלה מבחינה בין מקור, השראה, מטאפורה, אנלוגיה וטענה פורמלית.",
        "לא שונו כותרות, תתי־כותרות, תמונות, סיפורים, בלארבים או קבצי ייצוא.",
        "",
        "## תוצאות",
    ]

    for cfg in PAGES:
        did_change, notes = patch_page(cfg)
        changed_count += int(did_change)
        lines.append(f"### `{cfg['path'].relative_to(ROOT)}`")
        lines.append(f"- changed: {did_change}")
        lines.extend(f"- {note}" for note in notes)
        lines.append("")

    lines.extend([
        "## בדיקת הצלחה ידנית",
        "- בדף המקורות מופיעה מפת אחריות קצרה לפני רשימת המקורות המלאה.",
        "- פיזיקה/לוגיקה/AI מקבלים סייג קרוב בלי למחוק את הפואטיקה.",
        "- עברית ואנגלית מקבילות ברמת תפקיד, לא בהכרח מילה במילה.",
    ])

    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"changed pages: {changed_count}")
    print(f"report: {REPORT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
