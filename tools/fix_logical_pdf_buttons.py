#!/usr/bin/env python3
"""Replace misleading logical MD CTA buttons with logical PDF CTA buttons.

The visible product rule: when the user is presented with paired full/logical document
buttons, the primary readable formats should be HTML and PDF. Markdown can still exist
in the archive, but it should not replace the logical PDF button in the main reader UI.

This script is intentionally narrow:
- scans public/site HTML only;
- updates links that point to editorial-tightened / tightened logical Markdown files;
- only changes anchors whose visible label says logical + MD;
- does not touch document body text, blurbs, stories, or Markdown files.
"""
from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "_product_docs" / "reports" / "BPI_V87_LOGICAL_PDF_BUTTONS_REPORT_HE.md"
REPORT.parent.mkdir(parents=True, exist_ok=True)

ANCHOR_RE = re.compile(r"<a\b(?P<attrs>[^>]*?href=[\"'](?P<href>[^\"']+\.md)(?P<tail>[^\"']*)[\"'][^>]*)>(?P<label>.*?)</a>", re.I | re.S)

def strip_tags(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html).strip()

def is_logical_md_button(href: str, label_html: str) -> bool:
    href_l = href.lower()
    label = strip_tags(label_html).lower()
    label_he = strip_tags(label_html)
    if "tightened" not in href_l and "editorial-tightened" not in href_l and "logical" not in href_l:
        return False
    if not href_l.endswith(".md"):
        return False
    has_md = "md" in label or "markdown" in label
    has_logical = "logical" in label or "לוגי" in label_he or "מהודק" in label_he
    return has_md and has_logical

def replacement_label(label_html: str) -> str:
    plain = strip_tags(label_html)
    if "לוגי" in plain:
        return "PDF לוגי"
    if "מהודק" in plain:
        return "PDF מהודק"
    if "Logical" in plain or "logical" in plain:
        return "Logical PDF"
    return "PDF"

def patch_text(text: str) -> tuple[str, int]:
    count = 0
    def repl(m: re.Match[str]) -> str:
        nonlocal count
        href = m.group("href")
        label = m.group("label")
        if not is_logical_md_button(href, label):
            return m.group(0)
        new_attrs = m.group("attrs").replace(href + m.group("tail"), href[:-3] + ".pdf" + m.group("tail"), 1)
        count += 1
        return f"<a{new_attrs}>{replacement_label(label)}</a>"
    return ANCHOR_RE.sub(repl, text), count

def main() -> int:
    changed: list[tuple[Path, int]] = []
    for path in sorted((ROOT / "site").rglob("*.html")):
        text = path.read_text(encoding="utf-8", errors="ignore")
        new_text, n = patch_text(text)
        if n:
            path.write_text(new_text, encoding="utf-8")
            changed.append((path, n))

    lines = [
        "# BPI V87 - החלפת כפתורי MD לוגי ב-PDF לוגי",
        "",
        f"Generated: {datetime.utcnow().isoformat(timespec='seconds')}Z",
        "",
        "הסיבה: במסך הראשי לקורא, 'MD לוגי' לא צריך להחליף את ה-PDF הלוגי. Markdown יכול להישאר בארכיון, אבל כפתור הקריאה הראשי צריך להיות PDF.",
        "",
    ]
    if changed:
        for path, n in changed:
            lines.append(f"- `{path.relative_to(ROOT)}`: {n} button(s) changed from logical MD to logical PDF")
    else:
        lines.append("- No matching logical MD buttons found.")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("changed files:", len(changed))
    for path, n in changed:
        print(path.relative_to(ROOT), n)
    print("report:", REPORT.relative_to(ROOT))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
