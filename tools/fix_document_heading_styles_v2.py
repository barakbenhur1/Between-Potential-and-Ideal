#!/usr/bin/env python3
"""
Second-pass heading/subheading visual repair.

Purpose:
- Fix every real heading/subheading in the selected public HTML documents so it has:
  blue color, correct font weight, correct hierarchy, and language-aware alignment.
- Apply a broad but scoped style to h2-h6 inside document body sections.
- Promote short heading-like paragraphs inside theory documents to section-subheading.
- Avoid TOC, cover/title pages, image captions, navigation, and story dialogue/body paragraphs.

Run from repository root:
    python3 tools/fix_document_heading_styles_v2.py --dry-run
    python3 tools/fix_document_heading_styles_v2.py

Optional, only if you explicitly want broader coverage:
    python3 tools/fix_document_heading_styles_v2.py --all-site-files
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from html import unescape

ROOT = Path.cwd()

DEFAULT_TARGETS = [
    "site/files/between-potential-and-ideal-he.html",
    "site/files/between-potential-and-ideal-he-editorial.html",
    "site/files/between-potential-and-ideal-en.html",
    "site/files/between-potential-and-ideal-en-editorial.html",
    "site/files/editorial-tightened/between-potential-and-ideal-tightened-he.html",
    "site/files/editorial-tightened/between-potential-and-ideal-tightened-en.html",
    "site/files/appendices/stories-before-thought-hebrew-rtl.html",
    "site/files/appendices/stories-before-thought-english.html",
]

PATCH_MARKER = "BPI_HEADING_ALIGNMENT_FIX_V2_20260530"

CSS_PATCH = f"""
/* ===== {PATCH_MARKER}: real document heading/subheading visual hierarchy ===== */
.document-heading-aligned,
.chapter-subheading,
.section-subheading,
.logical-distillation,
.key-statement {{
  color: #0A3A68 !important;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans Hebrew", Arial, sans-serif !important;
  text-indent: 0 !important;
  max-width: 100% !important;
}}

.document-heading-aligned {{
  color: #0A3A68 !important;
  font-weight: 900 !important;
  line-height: 1.12 !important;
  margin-top: 1.55em !important;
  margin-bottom: 0.55em !important;
}}

h2.document-heading-aligned {{
  font-size: clamp(2rem, 4.5vw, 3.15rem) !important;
}}

h3.document-heading-aligned,
.chapter-subheading,
.logical-distillation {{
  font-size: clamp(1.35rem, 2.7vw, 1.85rem) !important;
  font-weight: 850 !important;
  line-height: 1.24 !important;
  margin-top: 1.7em !important;
  margin-bottom: 0.55em !important;
}}

h4.document-heading-aligned,
h5.document-heading-aligned,
h6.document-heading-aligned,
.section-subheading {{
  font-size: clamp(1.14rem, 2.15vw, 1.38rem) !important;
  font-weight: 800 !important;
  line-height: 1.36 !important;
  margin-top: 1.55em !important;
  margin-bottom: 0.48em !important;
}}

.key-statement {{
  color: #0A3A68 !important;
  font-size: clamp(1.08rem, 2.05vw, 1.3rem) !important;
  font-weight: 800 !important;
  line-height: 1.5 !important;
  margin-top: 1.25em !important;
  margin-bottom: 1.05em !important;
  background: rgba(10, 58, 104, 0.045) !important;
  border-inline-start: 4px solid rgba(10, 58, 104, 0.34) !important;
  padding: 0.65em 0.85em !important;
  border-radius: 12px !important;
}}

html[dir="rtl"] .document-heading-aligned,
html[dir="rtl"] .chapter-subheading,
html[dir="rtl"] .section-subheading,
html[dir="rtl"] .logical-distillation,
html[dir="rtl"] .key-statement,
[dir="rtl"] .document-heading-aligned,
[dir="rtl"] .chapter-subheading,
[dir="rtl"] .section-subheading,
[dir="rtl"] .logical-distillation,
[dir="rtl"] .key-statement,
.hebrew-rtl-force.document-heading-aligned,
.hebrew-rtl-force.chapter-subheading,
.hebrew-rtl-force.section-subheading,
.hebrew-rtl-force.logical-distillation,
.hebrew-rtl-force.key-statement {{
  direction: rtl !important;
  text-align: right !important;
  unicode-bidi: plaintext !important;
  margin-left: 0 !important;
  margin-right: 0 !important;
}}

html[dir="ltr"] .document-heading-aligned,
html[dir="ltr"] .chapter-subheading,
html[dir="ltr"] .section-subheading,
html[dir="ltr"] .logical-distillation,
html[dir="ltr"] .key-statement,
[dir="ltr"] .document-heading-aligned,
[dir="ltr"] .chapter-subheading,
[dir="ltr"] .section-subheading,
[dir="ltr"] .logical-distillation,
[dir="ltr"] .key-statement,
.english-ltr-force.document-heading-aligned,
.english-ltr-force.chapter-subheading,
.english-ltr-force.section-subheading,
.english-ltr-force.logical-distillation,
.english-ltr-force.key-statement {{
  direction: ltr !important;
  text-align: left !important;
  unicode-bidi: plaintext !important;
  margin-left: 0 !important;
  margin-right: 0 !important;
}}

/* Keep covers, title pages and TOCs visually independent. */
.cover .document-heading-aligned,
.cover-page .document-heading-aligned,
.title-page .document-heading-aligned,
.document-screen-toc .document-heading-aligned,
#interactive-toc .document-heading-aligned,
#table-of-contents .document-heading-aligned,
.story-toc-row .document-heading-aligned {{
  text-align: inherit !important;
}}
/* ===== /{PATCH_MARKER} ===== */
"""

HEADING_HINTS_HE = [
    "תיקון", "מוקד", "הזיקוק", "הכרזה", "מסקנה", "סיכום", "חסד", "מנדט",
    "עקרון", "חוק", "פרוטוקול", "חתימת", "מתנת", "השתייכות", "משמעת",
    "מקורות", "נוסחת", "תכנית", "חומר", "עומס", "מקדם", "מאמץ", "סדק",
    "יסודות", "ארכיטקטורה", "פונקציה", "תנועה", "אור", "תהודה", "יתירות",
    "תחזוקה", "כשל", "יופי", "עיר", "כסף", "זהב", "פיאט", "אינפלציה",
    "השוק", "אשראי", "ריבית", "עבודה", "רווח", "חיצוניות", "בועה",
    "צמיחה", "משבר", "מצב טבע", "לגיטימיות", "ריבונות", "בחירות",
    "זכויות", "חובות", "מוסד", "בירוקרטיה", "שחיתות", "מסים", "חירום",
]

HE_KEY_STATEMENTS = [
    "האדם אינו טעות בתוך היקום",
]

HE_ALWAYS_SUBHEADINGS = [
    "הזיקוק הלוגי",
    "תיקון המטמורפוזה",
    "מוקד החסד: חסד הוויתור",
]

HEADING_HINTS_EN = [
    "logical distillation", "declaration", "manifesto", "conclusion",
    "source discipline", "single-axis", "creative recursion", "harmonic optimum",
    "franchise", "canon", "adaptation", "genres", "false ideal",
    "standard model", "bell", "kochen", "specker",
]

EN_KEY_STATEMENTS = [
    "the human is not a mistake",
    "humanity is not a mistake",
]


def strip_tags(fragment: str) -> str:
    fragment = re.sub(r"<script\b.*?</script>", "", fragment, flags=re.I | re.S)
    fragment = re.sub(r"<style\b.*?</style>", "", fragment, flags=re.I | re.S)
    fragment = re.sub(r"<[^>]+>", "", fragment)
    return unescape(fragment).strip()


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", unescape(text)).strip()


def detect_lang(path: Path, html: str) -> str:
    low = path.name.lower()
    prefix = html[:3000].lower()
    if "hebrew" in low or "-he" in low or 'dir="rtl"' in prefix or "lang=\"he\"" in prefix:
        return "he"
    return "en"


def add_css_patch(html: str) -> tuple[str, bool]:
    if PATCH_MARKER in html:
        return html, False
    if "</style>" in html:
        return html.replace("</style>", CSS_PATCH + "\n</style>", 1), True
    if "</head>" in html:
        return html.replace("</head>", "<style>\n" + CSS_PATCH + "\n</style>\n</head>", 1), True
    return "<style>\n" + CSS_PATCH + "\n</style>\n" + html, True


def merge_class(attrs: str, classes: list[str]) -> str:
    m = re.search(r'\bclass=(["\'])(.*?)\1', attrs, flags=re.I | re.S)
    if m:
        existing = m.group(2).split()
        merged = existing[:]
        for cls in classes:
            if cls not in merged:
                merged.append(cls)
        return attrs[:m.start(2)] + " ".join(merged) + attrs[m.end(2):]
    return attrs.rstrip() + ' class="' + " ".join(classes) + '"'


def set_attr(attrs: str, name: str, value: str) -> str:
    pat = re.compile(rf'\b{name}=(["\']).*?\1', flags=re.I | re.S)
    repl = f'{name}="{value}"'
    if pat.search(attrs):
        return pat.sub(repl, attrs, count=1)
    return attrs.rstrip() + " " + repl


def set_style_alignment(attrs: str, lang: str, *, heading: bool) -> str:
    align = "right" if lang == "he" else "left"
    direction = "rtl" if lang == "he" else "ltr"
    color = "#0A3A68"

    m = re.search(r'\bstyle=(["\'])(.*?)\1', attrs, flags=re.I | re.S)
    if m:
        style = m.group(2)
        style = re.sub(r'text-align\s*:\s*(left|right|center)\s*!important\s*;?', '', style, flags=re.I)
        style = re.sub(r'text-align\s*:\s*(left|right|center)\s*;?', '', style, flags=re.I)
        style = re.sub(r'direction\s*:\s*(rtl|ltr)\s*!important\s*;?', '', style, flags=re.I)
        style = re.sub(r'direction\s*:\s*(rtl|ltr)\s*;?', '', style, flags=re.I)
        if heading:
            style = re.sub(r'color\s*:\s*[^;]+;?', '', style, flags=re.I)
        style = style.strip()
        if style and not style.endswith(";"):
            style += ";"
        style += f"text-align:{align}!important;direction:{direction}!important;unicode-bidi:plaintext!important;"
        if heading:
            style += f"color:{color}!important;"
        return attrs[:m.start(2)] + style + attrs[m.end(2):]

    style = f'text-align:{align}!important;direction:{direction}!important;unicode-bidi:plaintext!important;'
    if heading:
        style += f'color:{color}!important;'
    return attrs.rstrip() + f' style="{style}"'


def context_is_skipped(html: str, pos: int) -> bool:
    # Skip if inside nav/style/script/TOC/cover/title/caption blocks.
    window_start = max(0, pos - 4000)
    before = html[window_start:pos].lower()
    after = html[pos:pos + 1000].lower()

    # Inside a style/script block.
    if before.rfind("<style") > before.rfind("</style>"):
        return True
    if before.rfind("<script") > before.rfind("</script>"):
        return True

    # Inside nav/figcaption/link heavy TOC regions.
    if before.rfind("<nav") > before.rfind("</nav>"):
        return True
    if before.rfind("<figcaption") > before.rfind("</figcaption>"):
        return True

    # Nearest section context.
    sec_open = before.rfind("<section")
    sec_close = before.rfind("</section")
    if sec_open > sec_close:
        sec_tag_end = before.find(">", sec_open)
        sec_tag = before[sec_open:sec_tag_end if sec_tag_end != -1 else len(before)]
        skip_tokens = [
            "document-screen-toc", "interactive-toc", "table-of-contents",
            "story-toc", "cover", "cover-page", "title-page"
        ]
        if any(tok in sec_tag for tok in skip_tokens):
            return True

    # Skip explicit TOC/list classes around the element.
    local = before[-800:] + after[:800]
    if any(tok in local for tok in [
        "theory-toc", "story-toc", "toc-main", "toc-sub",
        "document-backbar", "skip-link"
    ]):
        return True

    return False


def should_promote_paragraph(text: str, lang: str, path: Path) -> tuple[bool, str]:
    cleaned = normalize_space(text)
    lowered = cleaned.lower()

    if not cleaned:
        return False, ""

    if any(k in lowered for k in ["href=", "src=", "http://", "https://"]):
        return False, ""

    # Avoid story dialogue/body lines in appendices. For appendices, only known title-ish lines.
    is_appendix = "appendices" in path.as_posix()

    if lang == "he":
        if any(k in cleaned for k in HE_KEY_STATEMENTS):
            return True, "key-statement"
        if cleaned in HE_ALWAYS_SUBHEADINGS:
            return True, "logical-distillation" if "הזיקוק" in cleaned else "chapter-subheading"

        if is_appendix:
            return False, ""

        # Generic theory-document subheading heuristic.
        if 3 <= len(cleaned) <= 115:
            has_heading_word = any(h in cleaned for h in HEADING_HINTS_HE)
            has_colon_title_shape = ":" in cleaned and len(cleaned) <= 120
            no_sentence_end = not cleaned.endswith((".", "!", "?", "…"))
            too_much_body = cleaned.count(",") >= 2 or cleaned.count(";") >= 1

            if (has_heading_word or has_colon_title_shape) and no_sentence_end and not too_much_body:
                return True, "section-subheading"

    else:
        if any(k in lowered for k in EN_KEY_STATEMENTS):
            return True, "key-statement"

        if is_appendix:
            return False, ""

        if 3 <= len(cleaned) <= 115:
            has_hint = any(h in lowered for h in HEADING_HINTS_EN)
            has_colon = ":" in cleaned and len(cleaned) <= 120
            no_sentence_end = not cleaned.endswith((".", "!", "?", "…"))
            too_much_body = cleaned.count(",") >= 2 or cleaned.count(";") >= 1

            if (has_hint or has_colon) and no_sentence_end and not too_much_body:
                return True, "section-subheading"

    return False, ""


def repair_headings(html: str, lang: str) -> tuple[str, int]:
    force = "hebrew-rtl-force" if lang == "he" else "english-ltr-force"
    direction = "rtl" if lang == "he" else "ltr"
    changed = 0

    def repl(m: re.Match[str]) -> str:
        nonlocal changed
        tag, attrs, inner = m.group(1), m.group(2), m.group(3)
        if context_is_skipped(html, m.start()):
            return m.group(0)
        text = strip_tags(inner)
        if not text:
            return m.group(0)

        new_attrs = attrs
        new_attrs = merge_class(new_attrs, ["document-heading-aligned", force])
        new_attrs = set_attr(new_attrs, "dir", direction)
        new_attrs = set_style_alignment(new_attrs, lang, heading=True)

        if new_attrs != attrs:
            changed += 1
            return f"<{tag}{new_attrs}>{inner}</{tag}>"
        return m.group(0)

    fixed = re.sub(r"<(h2|h3|h4|h5|h6)\b([^>]*)>(.*?)</\1>", repl, html, flags=re.I | re.S)
    return fixed, changed


def repair_paragraph_subheadings(html: str, lang: str, path: Path) -> tuple[str, int]:
    force = "hebrew-rtl-force" if lang == "he" else "english-ltr-force"
    direction = "rtl" if lang == "he" else "ltr"
    changed = 0

    def repl(m: re.Match[str]) -> str:
        nonlocal changed
        tag, attrs, inner = m.group(1), m.group(2), m.group(3)
        if context_is_skipped(html, m.start()):
            return m.group(0)

        # Avoid paragraphs containing complex inline structures/images.
        if re.search(r"<(img|figure|table|ul|ol|li|a)\b", inner, flags=re.I):
            return m.group(0)

        text = strip_tags(inner)
        promote, role = should_promote_paragraph(text, lang, path)
        if not promote:
            return m.group(0)

        new_attrs = attrs
        new_attrs = merge_class(new_attrs, [role, force])
        new_attrs = set_attr(new_attrs, "dir", direction)
        new_attrs = set_style_alignment(new_attrs, lang, heading=True)

        if new_attrs != attrs:
            changed += 1
            return f"<{tag}{new_attrs}>{inner}</{tag}>"

        return m.group(0)

    fixed = re.sub(r"<(p|div)\b([^>]*)>(.*?)</\1>", repl, html, flags=re.I | re.S)
    return fixed, changed


def candidate_files(all_site_files: bool) -> list[Path]:
    if all_site_files:
        raw = list((ROOT / "site/files").glob("**/*.html"))
    else:
        raw = [ROOT / p for p in DEFAULT_TARGETS]

    out = []
    seen = set()
    for p in raw:
        if p.exists() and p.is_file():
            rp = p.resolve()
            if rp not in seen:
                out.append(p)
                seen.add(rp)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--all-site-files", action="store_true")
    args = ap.parse_args()

    changed_files = []

    for path in candidate_files(args.all_site_files):
        html = path.read_text(encoding="utf-8", errors="ignore")
        lang = detect_lang(path, html)

        fixed, css_added = add_css_patch(html)
        fixed, h_count = repair_headings(fixed, lang)
        fixed, p_count = repair_paragraph_subheadings(fixed, lang, path)

        if fixed != html:
            changed_files.append((path, css_added, h_count, p_count))
            if not args.dry_run:
                path.write_text(fixed, encoding="utf-8")

    if not changed_files:
        print("No heading style changes needed.")
        return 0

    for path, css_added, h_count, p_count in changed_files:
        print(f"fixed {path.relative_to(ROOT)}")
        print(f"  css patch added: {css_added}")
        print(f"  headings aligned/styled: {h_count}")
        print(f"  paragraph subheadings promoted: {p_count}")

    if args.dry_run:
        print("\nDry run only. No files written.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
