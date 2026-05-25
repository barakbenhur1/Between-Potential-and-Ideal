#!/usr/bin/env python3
from pathlib import Path
import re
import sys
import os
from collections import defaultdict

APPLY = "--apply" in sys.argv
ROOT = Path.cwd()
SITE = ROOT / "site"
FIGURES = SITE / "figures"
REPORT = ROOT / "_product_docs" / "reports" / "BPI_V80_EXACT_TAB_IMAGE_REPLACEMENT_FIX_REPORT_HE.md"

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

# Exact chapter-title/subtitle/caption driven replacements.
# Only fixes main chapter-opening images that are currently tab/thumb/banner/low-quality or explicitly wrong.
# Same conceptual chapter gets the same image across Hebrew/English and HTML/MD.
CHAPTER_IMAGE_RULES = [
    # Tightened/logical main chapters that currently use tab_* images.
    {
        "keys": [
            "מרחק, סבל, מגבלה ומשמעות",
            "Distance, Suffering, Limitation",
            "Good, evil, suffering",
            "רוע, סבל, טוב ומשמעות",
        ],
        "image": "15_good_evil_responsibility.png",
        "reason": "replace tab_* banner in suffering/meaning chapter with full chapter-quality image",
    },
    {
        "keys": [
            "המבנה הרקורסיבי האינסופי",
            "The Architecture of Infinite Recursion",
            "recursive structure",
            "המבנה הרקורסיבי",
        ],
        "image": "cover_logical_recursion_whole_diagram.png",
        "reason": "replace tab_* banner in recursive architecture with logical recursion full diagram",
    },
    {
        "keys": [
            "הקצה הרקורסיבי",
            "The Recursive Edge",
            "recursive layers",
            "שכבות רקורסיביות",
        ],
        "image": "v25_chapter_recursive-edge.png",
        "reason": "replace tab_* banner with recursive-edge chapter image",
    },
    {
        "keys": [
            "מדע, פיזיקה ומתמטיקה כמשמעת גבול",
            "Science, Physics, and Mathematics as Boundary Discipline",
            "Science, Physics, and Mathematics as a Boundary Discipline",
            "formulas, measurement",
            "נוסחאות, מדידה",
        ],
        "image": "v25_chapter_science-physics-math-boundary-discipline.png",
        "reason": "replace tab_files banner with science/physics/mathematics chapter image",
    },
    {
        "keys": [
            "לוקליות, אי־לוקליות וקונטקסטואליות",
            "Locality, Non-locality, and Contextuality",
            "local and non-local relations",
            "קשרים מקומיים ולא־מקומיים",
        ],
        # Do NOT use v25_chapter_locality-nonlocality-contextuality.png because user marked it low quality.
        "image": "v25_chapter_boundary-horizons.png",
        "reason": "replace tab_core/low-quality locality image with stronger existing chapter-quality asset",
    },
    {
        "keys": [
            "המדומה, הווירטואלי, הכבידה והאופק",
            "The Imaginary, the Virtual, Gravity",
            "The imaginary, the virtual",
            "המדומה, הווירטואלי והאופק",
        ],
        "image": "02_navigation_between_banks.png",
        "reason": "replace tab/incorrect image in imaginary/virtual/horizon chapter with full image already used for that concept",
    },
    {
        "keys": [
            "מפת השוואות פיזיקלית",
            "Physical Comparison Map",
            "קוונטים, יחסות, אופק ומידע",
            "Quantum theory, relativity, horizon, and information",
        ],
        "image": "05_flow_toward_the_ideal.png",
        "reason": "replace tab_* banner in physical comparison map with full concept image",
    },
    # Philosophical theory chapters that currently use tab_* images.
    {
        "keys": [
            "אלוהים כפוטנציאל",
            "God as Potential",
            "Divine Risk",
            "הסיכון האלוהי",
        ],
        "image": "01_potential_ideal_axis.png",
        "fallbacks": ["v25_chapter_shape-of-the-universe-and-potential.png", "cover_philosophical_recursion_whole_diagram.png"],
        "reason": "replace tab image in opening philosophical chapter with full conceptual figure",
    },
    {
        "keys": [
            "Self, Ego, and Non-Erasing Unity",
            "עצמי, אגו ואחדות",
            "preserving perspective",
            "שימור נקודת",
        ],
        "image": "06_self_ego_unity.png",
        "fallbacks": ["cover_philosophical_recursion_whole_diagram.png"],
        "reason": "replace tab_sources banner with full self/ego/unity image",
    },
    {
        "keys": [
            "הבינה המלאכותית כראי",
            "AI as Mirror",
            "הבינה כראי",
            "AI Mirror",
        ],
        "image": "04_ai_mirror_awareness.png",
        "reason": "keep AI mirror chapter on full image asset, never tab banner",
    },
    {
        "keys": [
            "מסה־אנרגיה ותווך",
            "Mass-Energy and Medium",
            "Form, light, and matter",
            "צורה, אור וחומר",
        ],
        "image": "08_mass_energy_medium.png",
        "reason": "replace any tab with full mass-energy-medium asset",
    },
]

BAD_BASENAMES = {
    "tab_ai.png",
    "tab_ai_unique.png",
    "tab_applied.png",
    "tab_applied_unique.png",
    "tab_core.png",
    "tab_core_unique.png",
    "tab_critique.png",
    "tab_critique_unique.png",
    "tab_files.png",
    "tab_files_unique.png",
    "tab_methodology.png",
    "tab_methodology_unique.png",
    "tab_sources.png",
    "tab_sources_unique.png",
    "tab_witness.png",
    "tab_witness_unique.png",
    "v25_chapter_locality-nonlocality-contextuality.png",
}

def require_project():
    if not SITE.exists() or not FIGURES.exists():
        raise SystemExit("ERROR: run from project root containing site/ and site/figures/")

def rel_to_doc(doc: Path, figure_name: str) -> str:
    target = FIGURES / figure_name
    return Path(os.path.relpath(target, doc.parent)).as_posix()

def pick_image(rule):
    image = rule.get("image")
    if image and (FIGURES / image).exists():
        return image
    for fb in rule.get("fallbacks", []):
        if (FIGURES / fb).exists():
            return fb
    return None

def matching_rule(block_text: str):
    compact = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", block_text))
    for rule in CHAPTER_IMAGE_RULES:
        for key in rule["keys"]:
            if key in compact or key in block_text:
                return rule
    return None

def should_replace(src: str, rule) -> bool:
    base = Path(src).name
    if base in BAD_BASENAMES:
        return True
    if "tab_" in base or "thumb_" in base or "banner" in base or "unique_reuse" in src:
        return True
    # For rule-driven exact chapters, if the chosen image differs and the existing source is clearly not the rule image,
    # replace only if current is known low quality/wrong.
    if rule and rule.get("image") == "v25_chapter_boundary-horizons.png" and base == "v25_chapter_locality-nonlocality-contextuality.png":
        return True
    return False

def patch_html(doc: Path):
    text = doc.read_text(encoding="utf-8", errors="ignore")
    original = text
    changes = []

    def repl(m):
        block = m.group(0)
        rule = matching_rule(block)
        if not rule:
            return block
        img = re.search(r'(<img\b[^>]*\bsrc=")([^"]+)("[^>]*>)', block, flags=re.S)
        if not img:
            return block
        old_src = img.group(2)
        if not should_replace(old_src, rule):
            return block
        chosen = pick_image(rule)
        if not chosen:
            changes.append(("NO_IMAGE_FOUND", old_src, "", rule["reason"]))
            return block
        new_src = rel_to_doc(doc, chosen)
        if new_src == old_src:
            return block
        new_block = block[:img.start(2)] + new_src + block[img.end(2):]
        changes.append((chosen, old_src, new_src, rule["reason"]))
        return new_block

    patched = re.sub(r'<div class="chapter-opening">.*?</div>', repl, text, flags=re.S)

    if APPLY and patched != original:
        doc.write_text(patched, encoding="utf-8")
    return changes, patched != original

def patch_md(doc: Path):
    text = doc.read_text(encoding="utf-8", errors="ignore")
    original = text
    changes = []
    img_pattern = re.compile(r'(<img\b[^>]*\bsrc=")([^"]+)("[^>]*>)', flags=re.S)

    # Patch by scanning each image and using nearby text before it as context.
    offset = 0
    patched = text
    for m in list(img_pattern.finditer(text)):
        old_src = m.group(2)
        base = Path(old_src).name
        # Context around the image in original text.
        context = text[max(0, m.start() - 1200): min(len(text), m.end() + 300)]
        rule = matching_rule(context)
        if not rule:
            continue
        if not should_replace(old_src, rule):
            continue
        chosen = pick_image(rule)
        if not chosen:
            changes.append(("NO_IMAGE_FOUND", old_src, "", rule["reason"]))
            continue
        new_src = rel_to_doc(doc, chosen)
        if new_src == old_src:
            continue
        start = m.start(2) + offset
        end = m.end(2) + offset
        patched = patched[:start] + new_src + patched[end:]
        offset += len(new_src) - len(old_src)
        changes.append((chosen, old_src, new_src, rule["reason"]))

    if APPLY and patched != original:
        doc.write_text(patched, encoding="utf-8")
    return changes, patched != original

def scan_remaining_bad_refs(docs):
    rows = []
    for doc in docs:
        if not doc.exists():
            continue
        text = doc.read_text(encoding="utf-8", errors="ignore")
        for m in re.finditer(r'<div class="chapter-opening">.*?</div>', text, flags=re.S):
            block = m.group(0)
            img = re.search(r'src="([^"]+)"', block)
            if not img:
                continue
            src = img.group(1)
            base = Path(src).name
            if base in BAD_BASENAMES or "tab_" in base or "thumb_" in base or "banner" in base or "unique_reuse" in src:
                title = re.search(r'<h2[^>]*>(.*?)</h2>', block, flags=re.S)
                title_txt = re.sub(r'<[^>]+>', '', title.group(1)).strip() if title else ""
                title_txt = re.sub(r"\s+", " ", title_txt)
                rows.append((doc, title_txt, src))
    return rows

def main():
    require_project()
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

    remaining = scan_remaining_bad_refs(docs)

    lines = []
    lines.append("# BPI V80 — החלפת תמונות tab/banner מדויקות במסמכים הראשיים")
    lines.append("")
    lines.append(f"Mode: {'APPLY' if APPLY else 'AUDIT ONLY'}")
    lines.append("")
    lines.append("## מה תוקן")
    lines.append("- מחליף רק תמונות בתוך `chapter-opening` של המסמכים הראשיים.")
    lines.append("- מחליף `tab_*`, `tab_*_unique`, `thumb_*`, `banner`, `unique_reuse` ותמונת הלוקליות החלשה.")
    lines.append("- לא נוגע בטקסט.")
    lines.append("- לא נוגע ב־stories או ב־AI appendices.")
    lines.append("- לא בונה DOCX/PDF בשלב הזה.")
    lines.append("")
    lines.append("## החלפות")
    if not all_changes:
        lines.append("לא נמצאו החלפות לפי הכללים.")
    else:
        for doc, changes in all_changes:
            lines.append(f"### `{doc.relative_to(ROOT)}`")
            for chosen, old, new, reason in changes:
                lines.append(f"- from: `{old}`")
                lines.append(f"  - to: `{new or 'NO CHANGE'}`")
                lines.append(f"  - asset: `{chosen}`")
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
    lines.append("## שאריות בעייתיות שעדיין נמצאו")
    if not remaining:
        lines.append("לא נמצאו `tab/thumb/banner/unique_reuse` בתוך `chapter-opening` במסמכים הראשיים.")
    else:
        for doc, title, src in remaining[:200]:
            lines.append(f"- `{doc.relative_to(ROOT)}` — `{title}` — `{src}`")
        if len(remaining) > 200:
            lines.append(f"- ועוד {len(remaining)-200} שורות.")

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    if APPLY or not REPORT.exists():
        REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("\n".join(lines))
    print("")
    print("Report:", REPORT)

if __name__ == "__main__":
    main()
