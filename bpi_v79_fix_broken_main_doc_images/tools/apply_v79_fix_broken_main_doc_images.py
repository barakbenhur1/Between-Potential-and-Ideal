#!/usr/bin/env python3
from pathlib import Path
import re
import shutil
import sys
from collections import defaultdict

APPLY = "--apply" in sys.argv
ROOT = Path.cwd()
SITE = ROOT / "site"
FIGURES = SITE / "figures"
REPORT = ROOT / "_product_docs" / "reports" / "BPI_V79_FIX_BROKEN_MAIN_DOC_IMAGES_REPORT_HE.md"

MAIN_DOCS = [
    SITE / "files" / "between-potential-and-ideal-en-editorial.html",
    SITE / "files" / "between-potential-and-ideal-he-editorial.html",
    SITE / "files" / "between-potential-and-ideal-en.md",
    SITE / "files" / "between-potential-and-ideal-he.md",
    SITE / "files" / "editorial-tightened" / "between-potential-and-ideal-tightened-en.html",
    SITE / "files" / "editorial-tightened" / "between-potential-and-ideal-tightened-he.html",
    SITE / "files" / "editorial-tightened" / "between-potential-and-ideal-tightened-en.md",
    SITE / "files" / "editorial-tightened" / "between-potential-and-ideal-tightened-he.md",
]

BROKEN_NAME_HINTS = (
    "tab_",
    "thumb_",
    "banner",
    "compact",
)
LOW_QUALITY_EXACT = {
    "v25_chapter_locality-nonlocality-contextuality.png",
}
REPEATED_BUT_ALLOWED_FOR_COVER_ONLY = {
    "cover_logical_recursion_whole_diagram.png",
    "cover_philosophical_recursion_whole_diagram.png",
}

# Chapter slug aliases by title/id/alt text.
TITLE_TO_SLUG = {
    "Artificial Intelligence and Open Problems": "ai-open-problems",
    "בינה מלאכותית ובעיות פתוחות": "ai-open-problems",
    "I Have No Mouth, and I Must Scream": "i-have-no-mouth",
    "אין לי פה ואני חייב לצרוח": "i-have-no-mouth",
    "Education of Potential": "education-of-potential",
    "חינוך של פוטנציאל": "education-of-potential",
    "Science, Physics, and Mathematics as Boundary Discipline": "science-physics-math-boundary-discipline",
    "Science, Physics, and Mathematics as a Boundary Discipline": "science-physics-math-boundary-discipline",
    "מדע, פיזיקה ומתמטיקה כמשמעת גבול": "science-physics-math-boundary-discipline",
    "Locality, Non-locality, and Contextuality": "locality-nonlocality-contextuality",
    "לוקליות, אי־לוקליות וקונטקסטואליות": "locality-nonlocality-contextuality",
    "Art of Potential": "art-of-potential",
    "אומנות של פוטנציאל": "art-of-potential",
    "Music of Potential": "music-of-potential",
    "מוזיקה של פוטנציאל": "music-of-potential",
    "Law of Potential": "law-of-potential",
    "משפט של פוטנציאל": "law-of-potential",
    "Medicine of Potential": "medicine-of-potential",
    "רפואה של פוטנציאל": "medicine-of-potential",
    "Boundary Horizons": "boundary-horizons",
    "אופקי גבול": "boundary-horizons",
    "Universe Structure / Geometry of the Universe and the Shape of Potential": "shape-of-the-universe-and-potential",
    "מבנה היקום / צורת היקום וצורת הפוטנציאל": "shape-of-the-universe-and-potential",
    "High-Energy Physics": "high-energy-physics",
    "פיזיקה באנרגיות גבוהות": "high-energy-physics",
    "Black Holes, Event Horizons, and the Holographic Principle": "black-holes-horizons-holography",
    "חורים שחורים, אופקי אירועים והעיקרון ההולוגרפי": "black-holes-horizons-holography",
    "The Recursive Edge": "recursive-edge",
    "הקצה הרקורסיבי": "recursive-edge",
}

# Prefer direct chapter-quality images. Never choose tab/thumb images for a main chapter figure.
PREFERRED = {
    "ai-open-problems": ["v25_chapter_ai-open-problems.png"],
    "i-have-no-mouth": ["v25_chapter_i-have-no-mouth.png"],
    "education-of-potential": ["v25_chapter_education-of-potential.png"],
    "science-physics-math-boundary-discipline": ["v25_chapter_science-physics-math-boundary-discipline.png"],
    # The original locality image is visually weak, so do not use it.
    "locality-nonlocality-contextuality": [
        "v25_chapter_high-energy-physics.png",
        "v25_chapter_boundary-horizons.png",
        "v25_chapter_black-holes-horizons-holography.png",
        "v25_chapter_recursive-edge.png",
        "v25_chapter_science-physics-math-boundary-discipline.png",
    ],
    "art-of-potential": ["v25_chapter_art-of-potential.png"],
    "music-of-potential": ["v25_chapter_music-of-potential.png"],
    "law-of-potential": ["v25_chapter_law-of-potential.png"],
    "medicine-of-potential": ["v25_chapter_medicine-of-potential.png"],
    "boundary-horizons": ["v25_chapter_boundary-horizons.png"],
    "shape-of-the-universe-and-potential": ["v25_chapter_shape-of-the-universe-and-potential.png"],
    "high-energy-physics": ["v25_chapter_high-energy-physics.png"],
    "black-holes-horizons-holography": ["v25_chapter_black-holes-horizons-holography.png"],
    "recursive-edge": ["v25_chapter_recursive-edge.png"],
}

def ensure():
    if not SITE.exists() or not FIGURES.exists():
        raise SystemExit("ERROR: run from project root containing site/ and site/figures/")

def rel_to_doc(doc: Path, figure_name: str) -> str:
    target = FIGURES / figure_name
    return Path(os.path.relpath(target, doc.parent)).as_posix()

def exists(name: str) -> bool:
    return (FIGURES / name).exists()

def is_bad_image_name(name: str) -> bool:
    base = Path(name).name
    if base in LOW_QUALITY_EXACT:
        return True
    if base.startswith(BROKEN_NAME_HINTS):
        return True
    if "/tab_" in name or "/thumb_" in name:
        return True
    # unique_reuse copies from earlier attempts may be visually duplicates or accidental crops.
    if "unique_reuse/" in name:
        return True
    return False

def find_unused_chapter_assets(all_refs):
    used_basenames = {Path(ref).name for ref in all_refs}
    candidates = []
    for p in sorted(FIGURES.glob("*.png")):
        name = p.name
        if not name.startswith("v25_chapter_"):
            continue
        if name in used_basenames:
            continue
        if name in LOW_QUALITY_EXACT:
            continue
        candidates.append(name)
    return candidates

def extract_refs(text):
    refs = []
    refs += re.findall(r'src="([^"]*figures/[^"]+\.(?:png|jpg|jpeg|webp))"', text, flags=re.I)
    refs += re.findall(r'!\[[^\]]*\]\(([^)]*figures/[^)]+\.(?:png|jpg|jpeg|webp))\)', text, flags=re.I)
    return refs

def slug_from_block(block):
    # Try h2 text.
    m = re.search(r'<h2[^>]*>(.*?)</h2>', block, flags=re.S)
    if m:
        title = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        title = re.sub(r'\s+', ' ', title)
        if title in TITLE_TO_SLUG:
            return TITLE_TO_SLUG[title]
        # Remove prefixes.
        title2 = re.sub(r'^(?:\d+\.\s*|פרק\s+[^:]+:\s*)', '', title).strip()
        if title2 in TITLE_TO_SLUG:
            return TITLE_TO_SLUG[title2]
    # Try alt text.
    m = re.search(r'alt="([^"]+)"', block)
    if m:
        alt = m.group(1).strip()
        if alt in TITLE_TO_SLUG:
            return TITLE_TO_SLUG[alt]
    # Try id.
    m = re.search(r'<h2[^>]*id="([^"]+)"', block)
    if m:
        ident = m.group(1).strip()
        ident = ident.replace("--", "-")
        # rough english id to slug
        lowered = ident.lower()
        for title, slug in TITLE_TO_SLUG.items():
            if title and re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-') in lowered:
                return slug
    return None

def choose_replacement(slug, current_base, global_used_by_chapter, unused_pool):
    # Direct preferred image when available and not current broken one.
    for candidate in PREFERRED.get(slug, []):
        if not exists(candidate):
            continue
        if candidate in LOW_QUALITY_EXACT:
            continue
        # For locality, don't reuse a candidate already used by its own natural chapter unless we have unused assets.
        if slug == "locality-nonlocality-contextuality" and candidate in global_used_by_chapter and global_used_by_chapter[candidate] != slug:
            continue
        if candidate != current_base:
            return candidate, "preferred chapter-quality asset"

    # Use unused v25 chapter asset, if available.
    if unused_pool:
        candidate = unused_pool.pop(0)
        return candidate, "unused chapter-quality asset"

    # Last resort: if no unused assets, choose a stable non-tab chapter asset and copy it to a dedicated name.
    for candidate in PREFERRED.get(slug, []):
        if exists(candidate) and candidate not in LOW_QUALITY_EXACT:
            dedicated_dir = FIGURES / "dedicated_reuse"
            dedicated_dir.mkdir(exist_ok=True)
            new_name = f"dedicated_reuse/v79_{slug}_{Path(candidate).stem}.png"
            new_path = FIGURES / new_name
            if APPLY and not new_path.exists():
                shutil.copy2(FIGURES / candidate, new_path)
            return new_name, "last-resort dedicated copy; visual duplicate, but not broken/tab"
    return None, "no safe replacement found"

def patch_html_doc(doc, all_refs, global_used_by_chapter):
    text = doc.read_text(encoding="utf-8", errors="ignore")
    original = text
    changes = []

    unused_pool = find_unused_chapter_assets(all_refs)

    # Patch each chapter-opening block independently.
    def repl_block(m):
        block = m.group(0)
        slug = slug_from_block(block)
        if not slug:
            return block
        src_m = re.search(r'src="([^"]*figures/[^"]+\.(?:png|jpg|jpeg|webp))"', block, flags=re.I)
        if not src_m:
            return block
        src = src_m.group(1)
        base = Path(src).name

        # bad if tab/thumb/low-quality/copy/cropped OR repeated forbidden image in a wrong chapter
        bad = is_bad_image_name(src)
        if base == "v25_chapter_i-have-no-mouth.png" and slug != "i-have-no-mouth":
            bad = True
        if not bad:
            return block

        replacement, reason = choose_replacement(slug, base, global_used_by_chapter, unused_pool)
        if not replacement:
            changes.append((slug, src, "", reason))
            return block
        new_src = rel_to_doc(doc, replacement)
        changes.append((slug, src, new_src, reason))
        return block[:src_m.start(1)] + new_src + block[src_m.end(1):]

    patched = re.sub(r'<div class="chapter-opening">.*?</div>', repl_block, text, flags=re.S)

    if APPLY and patched != original:
        doc.write_text(patched, encoding="utf-8")
    return changes, patched != original

def patch_md_doc(doc, all_refs, global_used_by_chapter):
    text = doc.read_text(encoding="utf-8", errors="ignore")
    original = text
    changes = []
    unused_pool = find_unused_chapter_assets(all_refs)

    # We'll patch image tags by looking backward for nearby heading text.
    img_re = re.compile(r'(<img\b[^>]*?src=")([^"]*figures/[^"]+\.(?:png|jpg|jpeg|webp))("[^>]*>)', re.I | re.S)
    spans = list(img_re.finditer(text))
    offset = 0
    patched = text

    for m in spans:
        # account for previous replacements by searching around original positions in current patched string approximately
        start = m.start() + offset
        end = m.end() + offset
        src = m.group(2)
        base = Path(src).name

        # nearby heading/title in original text before image
        window = text[max(0, m.start()-900):m.start()]
        headings = re.findall(r'^(?:#{1,4}\s+|<h2[^>]*>)(.*?)(?:</h2>)?$', window, flags=re.M | re.S)
        slug = None
        # Simpler: scan all known title strings in nearby window.
        for title, candidate_slug in TITLE_TO_SLUG.items():
            if title in window:
                slug = candidate_slug
        if not slug:
            # use base filename slug if possible
            stem = base
            if stem.startswith("v25_chapter_"):
                slug = stem[len("v25_chapter_"):].rsplit(".", 1)[0]
        if not slug:
            continue

        bad = is_bad_image_name(src)
        if base == "v25_chapter_i-have-no-mouth.png" and slug != "i-have-no-mouth":
            bad = True
        if not bad:
            continue

        replacement, reason = choose_replacement(slug, base, global_used_by_chapter, unused_pool)
        if not replacement:
            changes.append((slug, src, "", reason))
            continue
        new_src = rel_to_doc(doc, replacement)
        new = m.group(1) + new_src + m.group(3)
        old = patched[start:end]
        # replace only the src in the current matched block, not arbitrary text
        new_block = re.sub(r'src="[^"]*"', f'src="{new_src}"', old, count=1)
        patched = patched[:start] + new_block + patched[end:]
        offset += len(new_block) - (end-start)
        changes.append((slug, src, new_src, reason))

    if APPLY and patched != original:
        doc.write_text(patched, encoding="utf-8")
    return changes, patched != original

def main():
    ensure()
    docs = [p for p in MAIN_DOCS if p.exists()]
    all_refs = []
    for d in docs:
        all_refs.extend(extract_refs(d.read_text(encoding="utf-8", errors="ignore")))

    # Map natural chapter images by slug so locality won't steal images still used by their natural chapter.
    global_used_by_chapter = {}
    for ref in all_refs:
        base = Path(ref).name
        if base.startswith("v25_chapter_"):
            slug = base[len("v25_chapter_"):].rsplit(".", 1)[0]
            global_used_by_chapter[base] = slug

    report_lines = []
    report_lines.append("# BPI V79 — תיקון תמונות שבורות במסמכים הראשיים")
    report_lines.append("")
    report_lines.append(f"Mode: {'APPLY' if APPLY else 'AUDIT ONLY'}")
    report_lines.append("")
    report_lines.append("## כלל התיקון")
    report_lines.append("- לא משתמשים ב־tab/thumb/banner כתמונת פרק ראשית.")
    report_lines.append("- לא משתמשים בתמונת הלוקליות החלשה.")
    report_lines.append("- תמונת I Have No Mouth נשארת רק בפרק שלה.")
    report_lines.append("- התיקון מוגבל למסמכים הראשיים בלבד.")
    report_lines.append("- לא נוגעים בטקסט, סיפורים, AI appendices או עמודי אתר רגילים.")
    report_lines.append("")

    all_changes = []
    changed_docs = []
    for doc in docs:
        if doc.suffix.lower() == ".html":
            changes, changed = patch_html_doc(doc, all_refs, global_used_by_chapter)
        elif doc.suffix.lower() == ".md":
            changes, changed = patch_md_doc(doc, all_refs, global_used_by_chapter)
        else:
            changes, changed = [], False
        if changes:
            all_changes.append((doc, changes))
        if changed:
            changed_docs.append(doc)

    report_lines.append("## החלפות / החלפות מוצעות")
    if not all_changes:
        report_lines.append("לא נמצאו תמונות בעייתיות לפי הכללים.")
    else:
        for doc, changes in all_changes:
            report_lines.append(f"### `{doc.relative_to(ROOT)}`")
            for slug, old, new, reason in changes:
                report_lines.append(f"- chapter: `{slug}`")
                report_lines.append(f"  - from: `{old}`")
                report_lines.append(f"  - to: `{new or 'NO CHANGE'}`")
                report_lines.append(f"  - reason: {reason}")

    report_lines.append("")
    report_lines.append("## קבצים ששונו בפועל")
    if APPLY and changed_docs:
        for d in changed_docs:
            report_lines.append(f"- `{d.relative_to(ROOT)}`")
    elif APPLY:
        report_lines.append("לא השתנו קבצים.")
    else:
        report_lines.append("Audit only — לא נכתבו שינויים.")

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    if APPLY or not REPORT.exists():
        REPORT.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    print("\n".join(report_lines))
    print("")
    print("Report:", REPORT)

if __name__ == "__main__":
    main()
