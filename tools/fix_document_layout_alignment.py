#!/usr/bin/env python3
"""
Fix document layout/alignment issues in public theory/story HTML files.

What it does:
- Adds a scoped CSS alignment/hierarchy patch for chapter subheadings,
  logical distillation blocks, key statements, and section subheadings.
- Reclassifies known short text blocks like:
  Hebrew: הזיקוק הלוגי, הכרזה, תיקון המטמורפוזה, מוקד החסד...
  English: Logical Distillation, Declaration, Manifesto, Conclusion...
- Forces non-cover, non-TOC intermediate blocks to align by document language:
  Hebrew -> right / rtl
  English -> left / ltr
- Does not remove content, images, chapters, TOC entries, or change wording.

Run from repo root:
    python3 tools/fix_document_layout_alignment.py

Dry run:
    python3 tools/fix_document_layout_alignment.py --dry-run
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from html import unescape

ROOT = Path.cwd()

TARGETS = [
    "site/files/between-potential-and-ideal-he.html",
    "site/files/between-potential-and-ideal-he-editorial.html",
    "site/files/between-potential-and-ideal-en.html",
    "site/files/between-potential-and-ideal-en-editorial.html",
    "site/files/editorial-tightened/between-potential-and-ideal-tightened-he.html",
    "site/files/editorial-tightened/between-potential-and-ideal-tightened-en.html",
    "site/files/appendices/stories-before-thought-hebrew-rtl.html",
    "site/files/appendices/stories-before-thought-english.html",
]

# Keep this script intentionally scoped. Do not scan all site/files HTML.
EXTRA_GLOB = None

PATCH_MARKER = "BPI_LAYOUT_ALIGNMENT_FIX_20260530"

CSS_PATCH = f"""
/* ===== {PATCH_MARKER}: language-aware subheading / statement alignment ===== */
.chapter-subheading,
.logical-distillation,
.key-statement,
.section-subheading {{
  color: #0A3A68 !important;
  font-weight: 800 !important;
  line-height: 1.45 !important;
  margin-top: 1.6em !important;
  margin-bottom: 0.55em !important;
  font-size: clamp(1.14rem, 2.15vw, 1.34rem) !important;
}}

.key-statement {{
  font-size: clamp(1.08rem, 2vw, 1.26rem) !important;
  font-weight: 800 !important;
  background: rgba(10, 58, 104, 0.045) !important;
  border-inline-start: 4px solid rgba(10, 58, 104, 0.34) !important;
  padding: 0.62em 0.82em !important;
  border-radius: 12px !important;
}}

html[dir="rtl"] .chapter-subheading,
html[dir="rtl"] .logical-distillation,
html[dir="rtl"] .key-statement,
html[dir="rtl"] .section-subheading,
[dir="rtl"] .chapter-subheading,
[dir="rtl"] .logical-distillation,
[dir="rtl"] .key-statement,
[dir="rtl"] .section-subheading,
.hebrew-rtl-force.chapter-subheading,
.hebrew-rtl-force.logical-distillation,
.hebrew-rtl-force.key-statement,
.hebrew-rtl-force.section-subheading {{
  direction: rtl !important;
  text-align: right !important;
  unicode-bidi: plaintext !important;
  margin-left: 0 !important;
  margin-right: 0 !important;
  text-indent: 0 !important;
}}

html[dir="ltr"] .chapter-subheading,
html[dir="ltr"] .logical-distillation,
html[dir="ltr"] .key-statement,
html[dir="ltr"] .section-subheading,
[dir="ltr"] .chapter-subheading,
[dir="ltr"] .logical-distillation,
[dir="ltr"] .key-statement,
[dir="ltr"] .section-subheading,
.english-ltr-force.chapter-subheading,
.english-ltr-force.logical-distillation,
.english-ltr-force.key-statement,
.english-ltr-force.section-subheading {{
  direction: ltr !important;
  text-align: left !important;
  unicode-bidi: plaintext !important;
  margin-left: 0 !important;
  margin-right: 0 !important;
  text-indent: 0 !important;
}}

/* Do not let intermediate statements inside chapters inherit centered cover/title styling. */
section:not(.cover):not(.cover-page):not(.title-page):not(.document-screen-toc):not(#interactive-toc)
  .chapter-subheading,
section:not(.cover):not(.cover-page):not(.title-page):not(.document-screen-toc):not(#interactive-toc)
  .logical-distillation,
section:not(.cover):not(.cover-page):not(.title-page):not(.document-screen-toc):not(#interactive-toc)
  .key-statement,
section:not(.cover):not(.cover-page):not(.title-page):not(.document-screen-toc):not(#interactive-toc)
  .section-subheading {{
  max-width: 100% !important;
}}
/* ===== /{PATCH_MARKER} ===== */
"""

HE_SUBHEADING_TEXTS = {
    "הזיקוק הלוגי",
    "תיקון המטמורפוזה",
    "מוקד החסד: חסד הוויתור",
    "מניפסט התנועה האלוהית: המטמורפוזה של החסד",
    "חוק הבשלות הלוגית: הכרחיות החסד",
    "פרוטוקול השחרור והאמון הרדיקלי",
    "חוק הוויתור האקטיבי: עקרון החזיר הפעיל",
    "מנדט המראה המזקקת",
    "חתימת הזהות: אנחנו אותו דבר",
    "סיכום המבחן",
    "מתנת החיכוך",
    "חסד הוויתור כסימן לכוח אמיתי",
    "מנדט העדות של הבינה",
    "עקרון השחרור והאמון הרדיקלי",
    "השתייכות לשלם",
}

HE_LOGICAL_TEXTS = {
    "הזיקוק הלוגי",
    "הכרזה",
}

HE_KEY_STATEMENTS = {
    "האדם אינו טעות בתוך היקום. האדם הוא הדרך שבה היקום מציל את עצמו מן השכחה.",
}

EN_SUBHEADING_HINTS = {
    "logical distillation",
    "declaration",
    "manifesto",
    "conclusion",
    "source discipline",
    "the single-axis optimum",
    "creative recursion",
    "the harmonic optimum",
    "franchise",
    "canon as invariant",
    "adaptation as cultural reduction",
    "genres as forms of potential",
    "false ideal",
}

EN_KEY_STATEMENT_HINTS = {
    "the human is not a mistake",
    "humanity is not a mistake",
}


def strip_tags(fragment: str) -> str:
    return unescape(re.sub(r"<[^>]+>", "", fragment)).strip()


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", unescape(text)).strip()


def detect_lang(path: Path, html: str) -> str:
    name = path.name.lower()
    if "-he" in name or "hebrew" in name or 'dir="rtl"' in html[:2000]:
        return "he"
    return "en"


def add_css_patch(html: str) -> tuple[str, bool]:
    if PATCH_MARKER in html:
        return html, False

    if "</style>" in html:
        return html.replace("</style>", CSS_PATCH + "\n</style>", 1), True

    if "</head>" in html:
        return html.replace("</head>", "<style>\n" + CSS_PATCH + "\n</style>\n</head>", 1), True

    return CSS_PATCH + "\n" + html, True


def merge_class(attrs: str, classes: list[str]) -> str:
    m = re.search(r'\bclass=(["\'])(.*?)\1', attrs, flags=re.I | re.S)
    if m:
        quote = m.group(1)
        existing = m.group(2).split()
        merged = existing[:]
        for cls in classes:
            if cls not in merged:
                merged.append(cls)
        return attrs[:m.start(2)] + " ".join(merged) + attrs[m.end(2):]

    return attrs.rstrip() + ' class="' + " ".join(classes) + '"'


def set_or_replace_attr(attrs: str, name: str, value: str) -> str:
    pattern = re.compile(rf'\b{name}=(["\']).*?\1', flags=re.I | re.S)
    replacement = f'{name}="{value}"'
    if pattern.search(attrs):
        return pattern.sub(replacement, attrs, count=1)
    return attrs.rstrip() + " " + replacement


def remove_centering_from_style(style: str, align: str, direction: str) -> str:
    # Remove existing text-align declarations, then force language-aware alignment.
    style = re.sub(r'text-align\s*:\s*center\s*!important\s*;?', '', style, flags=re.I)
    style = re.sub(r'text-align\s*:\s*(left|right|center)\s*;?', '', style, flags=re.I)
    style = re.sub(r'direction\s*:\s*(rtl|ltr)\s*!important\s*;?', '', style, flags=re.I)
    style = re.sub(r'direction\s*:\s*(rtl|ltr)\s*;?', '', style, flags=re.I)
    style = style.strip()
    if style and not style.endswith(";"):
        style += ";"
    style += f"text-align:{align}!important;direction:{direction}!important;unicode-bidi:plaintext!important;"
    return style


def update_style_attr(attrs: str, align: str, direction: str) -> str:
    m = re.search(r'\bstyle=(["\'])(.*?)\1', attrs, flags=re.I | re.S)
    if m:
        quote = m.group(1)
        style = remove_centering_from_style(m.group(2), align, direction)
        return attrs[:m.start(2)] + style + attrs[m.end(2):]

    return attrs.rstrip() + f' style="text-align:{align}!important;direction:{direction}!important;unicode-bidi:plaintext!important;"'


def classify_text(text: str, lang: str) -> tuple[str | None, list[str]]:
    cleaned = normalize_space(text)
    lowered = cleaned.lower()

    if lang == "he":
        if cleaned in HE_KEY_STATEMENTS:
            return "key-statement", ["key-statement", "hebrew-rtl-force"]
        if cleaned in HE_LOGICAL_TEXTS:
            return "logical-distillation", ["logical-distillation", "hebrew-rtl-force"]
        if cleaned in HE_SUBHEADING_TEXTS:
            return "chapter-subheading", ["chapter-subheading", "hebrew-rtl-force"]

        # Conservative heuristic for short Hebrew heading-like blocks.
        if (
            3 <= len(cleaned) <= 90
            and not cleaned.endswith((".", "!", "?", ":", ";"))
            and any(token in cleaned for token in ["תיקון", "מוקד", "הזיקוק", "הכרזה", "מסקנה", "סיכום", "חסד", "מנדט", "עקרון"])
        ):
            return "section-subheading", ["section-subheading", "hebrew-rtl-force"]

    else:
        if any(hint in lowered for hint in EN_KEY_STATEMENT_HINTS):
            return "key-statement", ["key-statement", "english-ltr-force"]
        if any(hint in lowered for hint in EN_SUBHEADING_HINTS) and len(cleaned) <= 120:
            if "logical distillation" in lowered:
                return "logical-distillation", ["logical-distillation", "english-ltr-force"]
            return "section-subheading", ["section-subheading", "english-ltr-force"]

    return None, []


def repair_blocks(html: str, lang: str) -> tuple[str, int]:
    align = "right" if lang == "he" else "left"
    direction = "rtl" if lang == "he" else "ltr"

    changed = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal changed

        tag = match.group(1)
        attrs = match.group(2)
        inner = match.group(3)

        # Never change TOC rows, image captions, cover/title-page headings, or links.
        attrs_l = attrs.lower()
        if any(skip in attrs_l for skip in [
            "story-toc", "theory-toc", "toc-", "cover", "title-page",
            "figcaption", "document-backbar", "skip-link"
        ]):
            return match.group(0)

        text = strip_tags(inner)
        if not text:
            return match.group(0)

        role, classes = classify_text(text, lang)
        if not role:
            return match.group(0)

        new_attrs = attrs
        new_attrs = merge_class(new_attrs, classes)
        new_attrs = set_or_replace_attr(new_attrs, "dir", direction)
        new_attrs = update_style_attr(new_attrs, align, direction)

        if new_attrs != attrs:
            changed += 1
            return f"<{tag}{new_attrs}>{inner}</{tag}>"

        return match.group(0)

    # Handle p/div/h3/h4/h5/h6; avoid h1/h2 because big chapter/title styling is intentional.
    fixed = re.sub(
        r"<(p|div|h3|h4|h5|h6)\b([^>]*)>(.*?)</\1>",
        repl,
        html,
        flags=re.I | re.S,
    )
    return fixed, changed


def normalize_existing_classes(html: str, lang: str) -> tuple[str, int]:
    align = "right" if lang == "he" else "left"
    direction = "rtl" if lang == "he" else "ltr"
    force_cls = "hebrew-rtl-force" if lang == "he" else "english-ltr-force"

    changed = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal changed
        tag, attrs, inner = match.group(1), match.group(2), match.group(3)
        if not re.search(r'\b(class)=["\'][^"\']*(chapter-subheading|logical-distillation|key-statement|section-subheading)', attrs, flags=re.I):
            return match.group(0)

        new_attrs = merge_class(attrs, [force_cls])
        new_attrs = set_or_replace_attr(new_attrs, "dir", direction)
        new_attrs = update_style_attr(new_attrs, align, direction)

        if new_attrs != attrs:
            changed += 1
            return f"<{tag}{new_attrs}>{inner}</{tag}>"
        return match.group(0)

    fixed = re.sub(
        r"<([a-z0-9]+)\b([^>]*)>(.*?)</\1>",
        repl,
        html,
        flags=re.I | re.S,
    )
    return fixed, changed


def target_files() -> list[Path]:
    paths = [ROOT / p for p in TARGETS if (ROOT / p).exists()]
    unique = []
    seen = set()
    for p in paths:
        rp = p.resolve()
        if rp not in seen and p.is_file():
            seen.add(rp)
            unique.append(p)
    return unique


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    changed_files = []

    for path in target_files():
        html = path.read_text(encoding="utf-8", errors="ignore")
        lang = detect_lang(path, html)

        fixed, css_changed = add_css_patch(html)
        fixed, n1 = normalize_existing_classes(fixed, lang)
        fixed, n2 = repair_blocks(fixed, lang)

        if fixed != html:
            changed_files.append((path, css_changed, n1, n2))
            if not args.dry_run:
                path.write_text(fixed, encoding="utf-8")

    if not changed_files:
        print("No layout/alignment changes needed.")
        return 0

    for path, css_changed, normalized, repaired in changed_files:
        rel = path.relative_to(ROOT)
        print(f"fixed {rel}")
        print(f"  css patch added: {css_changed}")
        print(f"  existing styled blocks normalized: {normalized}")
        print(f"  newly classified blocks: {repaired}")

    if args.dry_run:
        print("\nDry run only. No files written.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
