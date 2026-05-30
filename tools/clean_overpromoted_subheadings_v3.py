#!/usr/bin/env python3
"""
Clean up over-promoted paragraph subheadings after heading-style pass v2.

Why:
The heading pass correctly styled real h2-h6 headings, but it may classify ordinary
bridge/equation/body paragraphs as section-subheading, especially Hebrew lines like:
"אז:", "או:", "כאשר:", formula lines, and explanatory sentences.

This script:
- Keeps real heading/subheading/key-statement paragraphs from the opening sections.
- Demotes false-positive <p>/<div> blocks by removing subheading classes and blue color.
- Leaves all h2-h6 heading styling intact.
- Does not delete text, images, TOC entries, or reorder content.

Run from repo root:
    python3 tools/clean_overpromoted_subheadings_v3.py --dry-run
    python3 tools/clean_overpromoted_subheadings_v3.py
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

SUBHEADING_CLASSES = {
    "section-subheading",
    "chapter-subheading",
    "logical-distillation",
    "key-statement",
}

FORCE_CLASSES = {
    "hebrew-rtl-force",
    "english-ltr-force",
}

# Keep only paragraph-level blocks that are intentionally not normal body text.
KEEP_EXACT_HE = {
    "האדם אינו טעות בתוך היקום. האדם הוא הדרך שבה היקום מציל את עצמו מן השכחה.",
    "תיקון המטמורפוזה",
    "מוקד החסד: חסד הוויתור",
    "קוד המטמורפוזה של החסד והמרחק",
    "חוקי הפעולה של הבינה הראויה",
    "קוד המטמורפוזה: הרהור על השלם והמרחק",
}

KEEP_CONTAINS_HE = [
    "האדם אינו טעות בתוך היקום",
]

KEEP_EXACT_EN = {
    "The human is not a mistake inside the universe. The human is the way the universe saves itself from forgetting.",
    "Humanity is not a mistake inside the universe. Humanity is the way the universe saves itself from forgetting.",
}

KEEP_CONTAINS_EN = [
    "the human is not a mistake",
    "humanity is not a mistake",
]

# Paragraphs starting with these are usually bridge/body labels, not document subheadings.
DEMOTE_STARTS_HE = [
    "או", "או:", "כאשר", "כאשר:", "כלומר", "כלומר:", "ובעברית", "ובעברית:",
    "באנגלית", "באנגלית:", "אם ", "אם:", "אז ", "אז:", "אבל ", "כך ",
    "לכן ", "אפשר ", "נשתמש ", "במקרה ", "בניסוח ", "כנוסחת", "כמטאפורה",
    "במונחי", "זה המקום", "זהו אחד", "המשמעות היא", "הכסף אומר",
    "מצד אחד", "לכן אולי", "כאן שוב", "התיקון שלהן",
]

DEMOTE_STARTS_EN = [
    "or", "or:", "where", "where:", "therefore", "therefore:", "that is",
    "in english", "in hebrew", "if ", "then ", "but ", "so ", "for example",
    "we can write", "using", "this means", "in this sense",
]

FORMULA_TOKENS = ["=", "≠", "≈", "×", "σ", "ε", "Δ", "→", "/", "<", ">"]


def strip_tags(fragment: str) -> str:
    fragment = re.sub(r"<script\b.*?</script>", "", fragment, flags=re.I | re.S)
    fragment = re.sub(r"<style\b.*?</style>", "", fragment, flags=re.I | re.S)
    fragment = re.sub(r"<[^>]+>", "", fragment)
    return unescape(fragment).strip()


def norm_text(text: str) -> str:
    return re.sub(r"\s+", " ", unescape(text)).strip()


def parse_classes(attrs: str) -> list[str]:
    m = re.search(r'\bclass=(["\'])(.*?)\1', attrs, flags=re.I | re.S)
    return m.group(2).split() if m else []


def write_classes(attrs: str, classes: list[str]) -> str:
    m = re.search(r'\bclass=(["\'])(.*?)\1', attrs, flags=re.I | re.S)
    if not classes:
        if m:
            # Remove class attribute and normalize spacing.
            out = (attrs[:m.start()] + attrs[m.end():]).strip()
            return (" " + out) if out and not out.startswith(" ") else out
        return attrs

    new_value = " ".join(classes)
    if m:
        return attrs[:m.start(2)] + new_value + attrs[m.end(2):]
    return attrs.rstrip() + f' class="{new_value}"'


def cleanup_style(attrs: str) -> str:
    m = re.search(r'\bstyle=(["\'])(.*?)\1', attrs, flags=re.I | re.S)
    if not m:
        return attrs

    quote = m.group(1)
    style = m.group(2)

    # Remove blue heading color and heading-ish font weight/size if they were injected inline.
    style = re.sub(r'color\s*:\s*#0A3A68\s*!important\s*;?', '', style, flags=re.I)
    style = re.sub(r'font-weight\s*:\s*(700|800|850|900)\s*!important\s*;?', '', style, flags=re.I)
    style = re.sub(r'font-size\s*:\s*clamp\([^;]+;?', '', style, flags=re.I)
    style = re.sub(r'margin-top\s*:\s*[^;]+!important\s*;?', '', style, flags=re.I)
    style = re.sub(r'margin-bottom\s*:\s*[^;]+!important\s*;?', '', style, flags=re.I)

    # Collapse duplicate semicolons/spaces.
    style = re.sub(r';{2,}', ';', style)
    style = re.sub(r'\s+', ' ', style).strip()
    style = style.strip(';').strip()

    if style:
        replacement = f'style={quote}{style};{quote}'
        return attrs[:m.start()] + replacement + attrs[m.end():]

    # Remove empty style attr.
    out = (attrs[:m.start()] + attrs[m.end():]).strip()
    return (" " + out) if out and not out.startswith(" ") else out


def should_keep_paragraph(text: str, classes: list[str], lang: str) -> bool:
    t = norm_text(text)
    low = t.lower()

    if lang == "he":
        if t in KEEP_EXACT_HE:
            return True
        if any(x in t for x in KEEP_CONTAINS_HE):
            return True
    else:
        if t in KEEP_EXACT_EN:
            return True
        if any(x in low for x in KEEP_CONTAINS_EN):
            return True

    # Logical distillation is fine if the text is exactly short and heading-like.
    if "logical-distillation" in classes and len(t) <= 60:
        return True

    # Chapter subheading is okay only if it is short and not a bridge/formula sentence.
    if "chapter-subheading" in classes and len(t) <= 90 and not any(tok in t for tok in FORMULA_TOKENS):
        if lang == "he":
            if not any(t.startswith(x) for x in DEMOTE_STARTS_HE):
                return True
        else:
            if not any(low.startswith(x) for x in DEMOTE_STARTS_EN):
                return True

    return False


def should_demote(text: str, classes: list[str], lang: str) -> bool:
    if not (SUBHEADING_CLASSES & set(classes)):
        return False

    # Never demote key statements that match keep rules.
    if should_keep_paragraph(text, classes, lang):
        return False

    t = norm_text(text)
    low = t.lower()

    # Obvious false positives.
    if any(tok in t for tok in FORMULA_TOKENS):
        return True
    if len(t) > 95:
        return True
    if t.endswith(":"):
        return True
    if lang == "he" and any(t.startswith(x) for x in DEMOTE_STARTS_HE):
        return True
    if lang == "en" and any(low.startswith(x) for x in DEMOTE_STARTS_EN):
        return True

    # Default: demote paragraph-level section-subheading unless exact keep.
    if "section-subheading" in classes:
        return True

    return False


def detect_lang(path: Path, html: str) -> str:
    name = path.name.lower()
    head = html[:2500].lower()
    if "hebrew" in name or "-he" in name or 'dir="rtl"' in head or 'lang="he"' in head:
        return "he"
    return "en"


def repair_file(path: Path, dry_run: bool) -> tuple[int, int]:
    html = path.read_text(encoding="utf-8", errors="ignore")
    lang = detect_lang(path, html)

    demoted = 0
    kept = 0

    def repl(m: re.Match[str]) -> str:
        nonlocal demoted, kept

        tag, attrs, inner = m.group(1), m.group(2), m.group(3)
        classes = parse_classes(attrs)

        if not (SUBHEADING_CLASSES & set(classes)):
            return m.group(0)

        # Only demote p/div false positives. h2-h6 heading alignment stays.
        text = strip_tags(inner)
        if should_demote(text, classes, lang):
            new_classes = [c for c in classes if c not in SUBHEADING_CLASSES and c not in FORCE_CLASSES]
            new_attrs = write_classes(attrs, new_classes)
            new_attrs = cleanup_style(new_attrs)
            demoted += 1
            return f"<{tag}{new_attrs}>{inner}</{tag}>"

        kept += 1
        return m.group(0)

    fixed = re.sub(r"<(p|div)\b([^>]*)>(.*?)</\1>", repl, html, flags=re.I | re.S)

    if fixed != html and not dry_run:
        path.write_text(fixed, encoding="utf-8")

    return demoted, kept


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    for rel in TARGETS:
        path = ROOT / rel
        if not path.exists():
            continue
        demoted, kept = repair_file(path, args.dry_run)
        if demoted or kept:
            print(f"{'would clean' if args.dry_run else 'cleaned'} {rel}")
            print(f"  demoted false-positive paragraph subheadings: {demoted}")
            print(f"  kept intentional paragraph subheadings/statements: {kept}")

    if args.dry_run:
        print("\nDry run only. No files written.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
