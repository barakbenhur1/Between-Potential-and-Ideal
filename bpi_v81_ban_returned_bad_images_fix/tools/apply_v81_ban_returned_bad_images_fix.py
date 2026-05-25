#!/usr/bin/env python3
from pathlib import Path
import re
import sys
import os
import shutil

APPLY = "--apply" in sys.argv
ROOT = Path.cwd()
SITE = ROOT / "site"
FIGURES = SITE / "figures"
REPORT = ROOT / "_product_docs" / "reports" / "BPI_V81_BAN_RETURNED_BAD_IMAGES_FIX_REPORT_HE.md"

MAIN_DOCS = [
    SITE / "files" / "editorial-tightened" / "between-potential-and-ideal-tightened-he.html",
    SITE / "files" / "editorial-tightened" / "between-potential-and-ideal-tightened-en.html",
    SITE / "files" / "editorial-tightened" / "between-potential-and-ideal-tightened-he.md",
    SITE / "files" / "editorial-tightened" / "between-potential-and-ideal-tightened-en.md",
    SITE / "files" / "between-potential-and-ideal-he-editorial.html",
    SITE / "files" / "between-potential-and-ideal-en-editorial.html",
    SITE / "files" / "between-potential-and-ideal-he.md",
    SITE / "files" / "between-potential-and-ideal-en.md",
]

# These are the two images shown by the user as still wrong/returned.
BANNED_MAIN_CHAPTER_IMAGES = {
    "v25_chapter_science-physics-math-boundary-discipline.png",
    "cover_logical_recursion_whole_diagram.png",
}

# Also keep prior bad/bannery sources out of chapter-opening.
BANNED_PATTERNS = (
    "tab_",
    "thumb_",
    "banner",
    "unique_reuse/",
)

# Replacement selection by the actual chapter/caption context.
# Use only full non-tab assets. If a preferred asset is missing, fallback to another full concept image.
RULES = [
    {
        "keys": [
            "מדע, פיזיקה ומתמטיקה כמשמעת גבול",
            "Science, Physics, and Mathematics as Boundary Discipline",
            "Science, Physics, and Mathematics as a Boundary Discipline",
            "נוסחאות, מדידה ומודלים",
            "formulas, measurement, and models",
        ],
        # Do NOT use the banned v25 science image. Use high-energy physics as full-quality science image.
        "image": "v25_chapter_high-energy-physics.png",
        "fallbacks": [
            "v25_chapter_black-holes-horizons-holography.png",
            "v25_chapter_boundary-horizons.png",
            "17_engineering_architecture_potential.png",
        ],
        "reason": "replace returned low-standard science/boundary image",
    },
    {
        "keys": [
            "המבנה הרקורסיבי האינסופי",
            "The Architecture of Infinite Recursion",
            "מודל לוגי של האצלה",
            "A Logical Model of Delegation",
            "המבנה הרקורסיבי במודל הלוגי",
            "The recursive structure in the logical model",
        ],
        # Do NOT use cover_logical_recursion_whole_diagram. Use recursive-edge full chapter image.
        "image": "v25_chapter_recursive-edge.png",
        "fallbacks": [
            "02_navigation_between_banks.png",
            "04_ai_mirror_awareness.png",
            "cover_philosophical_recursion_whole_diagram.png",
        ],
        "reason": "replace returned repeated logical-recursion cover image inside chapter",
    },
    {
        "keys": [
            "הקצה הרקורסיבי",
            "The Recursive Edge",
            "שכבות רקורסיביות",
            "recursive layers",
        ],
        "image": "v25_chapter_boundary-horizons.png",
        "fallbacks": [
            "02_navigation_between_banks.png",
            "04_ai_mirror_awareness.png",
        ],
        "reason": "avoid reusing recursive-edge image if architecture uses it",
    },
    {
        "keys": [
            "לוקליות, אי־לוקליות וקונטקסטואליות",
            "Locality, Non-locality, and Contextuality",
            "קשרים מקומיים ולא־מקומיים",
            "local and non-local relations",
        ],
        # Avoid the earlier low-quality locality asset and avoid tab_core.
        "image": "v25_chapter_boundary-horizons.png",
        "fallbacks": [
            "v25_chapter_black-holes-horizons-holography.png",
            "v25_chapter_high-energy-physics.png",
            "02_navigation_between_banks.png",
        ],
        "reason": "replace low-quality/locality or tab image",
    },
]

# General exact source replacements when context matching fails.
EXACT_SOURCE_FALLBACKS = {
    "v25_chapter_science-physics-math-boundary-discipline.png": "v25_chapter_high-energy-physics.png",
    "cover_logical_recursion_whole_diagram.png": "v25_chapter_recursive-edge.png",
}

def ensure_project():
    if not SITE.exists() or not FIGURES.exists():
        raise SystemExit("ERROR: run from the project root containing site/ and site/figures/")

def figure_exists(name: str) -> bool:
    return (FIGURES / name).exists()

def pick(rule):
    for name in [rule.get("image")] + rule.get("fallbacks", []):
        if name and figure_exists(name) and Path(name).name not in BANNED_MAIN_CHAPTER_IMAGES:
            return name
    return None

def rel_to_doc(doc: Path, fig_name: str) -> str:
    return Path(os.path.relpath(FIGURES / fig_name, doc.parent)).as_posix()

def clean_text(s: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s or "")).strip()

def matching_rule(block: str):
    text = clean_text(block)
    for rule in RULES:
        for key in rule["keys"]:
            if key in text or key in block:
                return rule
    return None

def is_banned_src(src: str) -> bool:
    base = Path(src).name
    if base in BANNED_MAIN_CHAPTER_IMAGES:
        return True
    if base == "v25_chapter_locality-nonlocality-contextuality.png":
        return True
    return any(pattern in src or pattern in base for pattern in BANNED_PATTERNS)

def patch_src_in_block(doc: Path, block: str, rule):
    m = re.search(r'(<img\b[^>]*\bsrc=")([^"]+)("[^>]*>)', block, flags=re.S)
    if not m:
        return block, None
    old_src = m.group(2)
    old_base = Path(old_src).name

    replacement = None
    reason = None

    if rule and is_banned_src(old_src):
        replacement = pick(rule)
        reason = rule["reason"]

    # Exact fallback if a banned image remains in a context not matched.
    if replacement is None and old_base in EXACT_SOURCE_FALLBACKS:
        candidate = EXACT_SOURCE_FALLBACKS[old_base]
        if figure_exists(candidate) and candidate not in BANNED_MAIN_CHAPTER_IMAGES:
            replacement = candidate
            reason = "exact banned image fallback replacement"

    # Tab/banner fallback: use rule if possible.
    if replacement is None and rule and is_banned_src(old_src):
        replacement = pick(rule)
        reason = rule["reason"]

    if not replacement:
        return block, None

    new_src = rel_to_doc(doc, replacement)
    if new_src == old_src:
        return block, None

    new_block = block[:m.start(2)] + new_src + block[m.end(2):]
    return new_block, (old_src, new_src, replacement, reason or "replacement")

def patch_html(doc: Path):
    text = doc.read_text(encoding="utf-8", errors="ignore")
    original = text
    changes = []

    def repl(m):
        block = m.group(0)
        rule = matching_rule(block)
        new_block, change = patch_src_in_block(doc, block, rule)
        if change:
            changes.append(change)
        return new_block

    patched = re.sub(r'<div class="chapter-opening">.*?</div>', repl, text, flags=re.S)

    if APPLY and patched != original:
        doc.write_text(patched, encoding="utf-8")
    return changes, patched != original

def patch_md(doc: Path):
    text = doc.read_text(encoding="utf-8", errors="ignore")
    original = text
    changes = []
    patched = text
    offset = 0

    img_re = re.compile(r'(<img\b[^>]*\bsrc=")([^"]+)("[^>]*>)', flags=re.S)
    for m in list(img_re.finditer(text)):
        old_src = m.group(2)
        if not is_banned_src(old_src):
            continue
        context = text[max(0, m.start() - 1400): min(len(text), m.end() + 500)]
        rule = matching_rule(context)

        replacement = None
        reason = None
        if rule:
            replacement = pick(rule)
            reason = rule["reason"]
        if replacement is None and Path(old_src).name in EXACT_SOURCE_FALLBACKS:
            candidate = EXACT_SOURCE_FALLBACKS[Path(old_src).name]
            if figure_exists(candidate):
                replacement = candidate
                reason = "exact banned image fallback replacement"

        if not replacement:
            continue

        new_src = rel_to_doc(doc, replacement)
        start = m.start(2) + offset
        end = m.end(2) + offset
        patched = patched[:start] + new_src + patched[end:]
        offset += len(new_src) - len(old_src)
        changes.append((old_src, new_src, replacement, reason or "replacement"))

    if APPLY and patched != original:
        doc.write_text(patched, encoding="utf-8")
    return changes, patched != original

def remaining_bad(docs):
    rows = []
    for doc in docs:
        if not doc.exists():
            continue
        text = doc.read_text(encoding="utf-8", errors="ignore")
        # HTML chapter openings
        for m in re.finditer(r'<div class="chapter-opening">.*?</div>', text, flags=re.S):
            block = m.group(0)
            img = re.search(r'src="([^"]+)"', block)
            if img and is_banned_src(img.group(1)):
                title = re.search(r'<h2[^>]*>(.*?)</h2>', block, flags=re.S)
                title_txt = clean_text(title.group(1)) if title else ""
                rows.append((doc, title_txt, img.group(1)))
        # MD image refs
        for m in re.finditer(r'<img\b[^>]*\bsrc="([^"]+)"', text, flags=re.S):
            src = m.group(1)
            if is_banned_src(src):
                rows.append((doc, "MD image context", src))
    return rows

def main():
    ensure_project()
    docs = [p for p in MAIN_DOCS if p.exists()]
    all_changes = []
    changed_docs = []

    for doc in docs:
        if doc.suffix.lower() == ".html":
            changes, changed = patch_html(doc)
        elif doc.suffix.lower() == ".md":
            changes, changed = patch_md(doc)
        else:
            changes, changed = [], False
        if changes:
            all_changes.append((doc, changes))
        if changed:
            changed_docs.append(doc)

    bad = remaining_bad(docs)

    lines = []
    lines.append("# BPI V81 — איסור שתי התמונות שחזרו והחלפתן במסמכים הראשיים")
    lines.append("")
    lines.append(f"Mode: {'APPLY' if APPLY else 'AUDIT ONLY'}")
    lines.append("")
    lines.append("## תמונות אסורות כתמונת פרק")
    for name in sorted(BANNED_MAIN_CHAPTER_IMAGES):
        lines.append(f"- `{name}`")
    lines.append("- `v25_chapter_locality-nonlocality-contextuality.png`")
    lines.append("- כל `tab_*`, `thumb_*`, `banner`, `unique_reuse` בתוך chapter-opening")
    lines.append("")
    lines.append("## החלפות")
    if not all_changes:
        lines.append("לא נמצאו החלפות.")
    else:
        for doc, changes in all_changes:
            lines.append(f"### `{doc.relative_to(ROOT)}`")
            for old, new, asset, reason in changes:
                lines.append(f"- from: `{old}`")
                lines.append(f"  - to: `{new}`")
                lines.append(f"  - asset: `{asset}`")
                lines.append(f"  - reason: {reason}")
    lines.append("")
    lines.append("## קבצים ששונו בפועל")
    if APPLY and changed_docs:
        for d in changed_docs:
            lines.append(f"- `{d.relative_to(ROOT)}`")
    elif APPLY:
        lines.append("לא השתנו קבצים.")
    else:
        lines.append("Audit only — לא נכתבו שינויים.")
    lines.append("")
    lines.append("## שאריות בעייתיות")
    if not bad:
        lines.append("לא נמצאו שאריות של התמונות האסורות במסמכים הראשיים.")
    else:
        for doc, title, src in bad[:250]:
            lines.append(f"- `{doc.relative_to(ROOT)}` — `{title}` — `{src}`")
        if len(bad) > 250:
            lines.append(f"- ועוד {len(bad)-250} שורות.")

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    if APPLY or not REPORT.exists():
        REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("\n".join(lines))
    print("")
    print("Report:", REPORT)

if __name__ == "__main__":
    main()
