#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BPI V78 — precise main-docs image fix

Scope:
- Main theory documents only.
- Logical/tightened documents only.
- Hebrew + English.
- HTML + MD patched directly.
- DOCX/PDF rebuilt from corrected HTML only when required tools are installed.
- Does NOT touch AI appendices, story appendices, site pages, or unrelated files.

Rule:
- Same chapter across languages/formats may use the same image.
- Different chapters must not use the same chapter image.
- Bad/low-quality locality image is forbidden and must be replaced.
- "I Have No Mouth" image may stay only for that chapter; if it appears elsewhere it is replaced.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set


BAD_VISUAL_IMAGES = {
    "v25_chapter_locality-nonlocality-contextuality.png",
}

# The first screenshot Barak sent: visually strong but over-repeated.
# It may remain only for the I Have No Mouth chapter.
FORBIDDEN_REPEAT_IMAGES = {
    "v25_chapter_i-have-no-mouth.png",
}

ALLOWED_KEEP_SLUG_BY_IMAGE = {
    "v25_chapter_i-have-no-mouth.png": {"i-have-no-mouth"},
}

TARGETS = [
    {
        "name": "philosophical-en",
        "html": "site/files/between-potential-and-ideal-en-editorial.html",
        "md": "site/files/between-potential-and-ideal-en.md",
        "docx": "site/files/between-potential-and-ideal-en.docx",
        "pdf": "site/files/between-potential-and-ideal-en-editorial.pdf",
        "dir": "ltr",
    },
    {
        "name": "philosophical-he",
        "html": "site/files/between-potential-and-ideal-he-editorial.html",
        "md": "site/files/between-potential-and-ideal-he.md",
        "docx": "site/files/between-potential-and-ideal-he.docx",
        "pdf": "site/files/between-potential-and-ideal-he-editorial.pdf",
        "dir": "rtl",
    },
    {
        "name": "tightened-en",
        "html": "site/files/editorial-tightened/between-potential-and-ideal-tightened-en.html",
        "md": "site/files/editorial-tightened/between-potential-and-ideal-tightened-en.md",
        "docx": "site/files/editorial-tightened/between-potential-and-ideal-tightened-en.docx",
        "pdf": "site/files/editorial-tightened/between-potential-and-ideal-tightened-en.pdf",
        "dir": "ltr",
    },
    {
        "name": "tightened-he",
        "html": "site/files/editorial-tightened/between-potential-and-ideal-tightened-he.html",
        "md": "site/files/editorial-tightened/between-potential-and-ideal-tightened-he.md",
        "docx": "site/files/editorial-tightened/between-potential-and-ideal-tightened-he.docx",
        "pdf": "site/files/editorial-tightened/between-potential-and-ideal-tightened-he.pdf",
        "dir": "rtl",
    },
]


@dataclass
class ChapterImage:
    doc_name: str
    file_path: Path
    title: str
    slug: str
    src: str
    image_name: str


def normalize_title_to_slug(title: str) -> str:
    t = html.unescape(title)
    t = re.sub(r"<[^>]+>", "", t)
    t = t.replace("־", "-").replace("–", "-").replace("—", "-")
    t = re.sub(r"\s+", " ", t).strip()

    # Explicit Hebrew/English chapter equivalences.
    known = [
        (r"locality|לוקליות|אי.?לוקליות|קונטקסטואליות", "locality-nonlocality-contextuality"),
        (r"i have no mouth|אין לי פה|חייב לצרוח", "i-have-no-mouth"),
        (r"science.*physics.*mathematics|מדע.*פיזיקה.*מתמטיקה", "science-physics-math-boundary-discipline"),
        (r"art of potential|אומנות של פוטנציאל|אמנות של פוטנציאל", "art-of-potential"),
        (r"music of potential|מוזיקה של פוטנציאל", "music-of-potential"),
        (r"education of potential|חינוך של פוטנציאל", "education-of-potential"),
        (r"artificial intelligence.*open problems|בינה מלאכותית.*בעיות פתוחות", "ai-open-problems"),
        (r"recursive edge|הקצה הרקורסיבי", "recursive-edge"),
        (r"boundary horizons|אופקי גבול", "boundary-horizons"),
        (r"black holes.*holographic|חורים שחורים.*הולוגרפי", "black-holes-horizons-holography"),
        (r"universe structure|shape of the universe|מבנה היקום|צורת היקום", "shape-of-the-universe-and-potential"),
        (r"high-energy physics|פיזיקה באנרגיות גבוהות", "high-energy-physics"),
        (r"law of potential|משפט של פוטנציאל", "law-of-potential"),
        (r"medicine of potential|רפואה של פוטנציאל", "medicine-of-potential"),
    ]
    lower = t.lower()
    for pat, slug in known:
        if re.search(pat, lower, flags=re.I):
            return slug

    # Generic fallback for Latin titles.
    asciiish = re.sub(r"[^a-zA-Z0-9]+", "-", lower).strip("-")
    if asciiish:
        return asciiish[:80]

    # Generic Hebrew fallback.
    return re.sub(r"[^\wא-ת]+", "-", t).strip("-")[:80]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def rel_from(doc_path: Path, asset_path: Path, root: Path) -> str:
    return os.path.relpath(asset_path, start=doc_path.parent).replace(os.sep, "/")


def list_figure_assets(root: Path) -> List[Path]:
    fig = root / "site" / "figures"
    if not fig.exists():
        return []
    files = []
    for ext in ("*.png", "*.jpg", "*.jpeg", "*.webp"):
        files.extend(fig.rglob(ext))
    return sorted([p for p in files if p.is_file()])


def asset_quality_score(p: Path, topic_slug: Optional[str] = None) -> int:
    name = p.name.lower()
    path = p.as_posix().lower()
    score = 0
    if "/unique_reuse/" in path or "/v76_unique" in path or "/v77_" in path:
        score -= 500
    if name in BAD_VISUAL_IMAGES:
        score -= 1000
    if name.startswith("v25_chapter_"):
        score += 200
    if name.startswith("cover_"):
        score += 140
    if name.startswith("tab_") and "unique" in name:
        score += 80
    elif name.startswith("tab_"):
        score += 35
    if name.startswith("thumb_"):
        score -= 120
    if "favicon" in name or "apple" in name or "logo" in name:
        score -= 300
    if topic_slug:
        for token in topic_slug.split("-"):
            if len(token) >= 4 and token in name:
                score += 25
    return score


def extract_html_chapter_images(root: Path, doc: dict) -> List[ChapterImage]:
    path = root / doc["html"]
    if not path.exists():
        return []
    text = read_text(path)

    # Look for explicit chapter-opening blocks.
    out: List[ChapterImage] = []
    pattern = re.compile(
        r'(<div\s+class="chapter-opening"[^>]*>)(?P<body>.*?)(</div>)',
        re.S | re.I,
    )
    for m in pattern.finditer(text):
        body = m.group("body")
        h = re.search(r"<h2\b[^>]*>(?P<title>.*?)</h2>", body, re.S | re.I)
        im = re.search(r'<img\b[^>]*\bsrc="(?P<src>[^"]+)"[^>]*>', body, re.S | re.I)
        if not h or not im:
            continue
        title = re.sub(r"<[^>]+>", "", h.group("title"))
        slug = normalize_title_to_slug(title)
        src = im.group("src")
        out.append(ChapterImage(
            doc_name=doc["name"],
            file_path=path,
            title=title.strip(),
            slug=slug,
            src=src,
            image_name=Path(src).name,
        ))
    return out


def build_usage(root: Path) -> Tuple[List[ChapterImage], Dict[str, Set[str]]]:
    all_chapters: List[ChapterImage] = []
    image_to_slugs: Dict[str, Set[str]] = {}
    for doc in TARGETS:
        chapters = extract_html_chapter_images(root, doc)
        all_chapters.extend(chapters)
        for ch in chapters:
            image_to_slugs.setdefault(ch.image_name, set()).add(ch.slug)
    return all_chapters, image_to_slugs


def choose_replacements(root: Path, chapters: List[ChapterImage], image_to_slugs: Dict[str, Set[str]]) -> Tuple[Dict[str, str], List[str]]:
    """
    Returns slug -> target image path relative to site/figures, e.g. "v25_chapter_x.png" or "v78_unique/slug.png"
    """
    assets = list_figure_assets(root)
    if not assets:
        return {}, ["ERROR: no assets found under site/figures"]

    # Images currently used by main-doc chapter openings.
    used_image_names = set(image_to_slugs.keys())
    unused_assets = [p for p in assets if p.name not in used_image_names and p.name not in BAD_VISUAL_IMAGES]

    # Track candidate consumption by visual file path.
    consumed: Set[Path] = set()

    slug_to_current_images: Dict[str, Set[str]] = {}
    for ch in chapters:
        slug_to_current_images.setdefault(ch.slug, set()).add(ch.image_name)

    # Start with current image for each slug when valid.
    slug_to_target: Dict[str, str] = {}
    warnings: List[str] = []

    # Determine duplicates: same image used by >1 chapter.
    duplicate_images = {img for img, slugs in image_to_slugs.items() if len(slugs) > 1}

    for slug, images in sorted(slug_to_current_images.items()):
        # Prefer existing v25_chapter_<slug>.png if used and not bad/repeated by other chapter.
        selected: Optional[str] = None

        # Explicit bad locality must be replaced.
        requires_replace = False
        for img in images:
            if img in BAD_VISUAL_IMAGES:
                requires_replace = True
            if img in FORBIDDEN_REPEAT_IMAGES and slug not in ALLOWED_KEEP_SLUG_BY_IMAGE.get(img, set()):
                requires_replace = True
            if img in duplicate_images:
                # Keep duplicate only if image semantically belongs to this slug.
                belongs = slug in img or slug in ALLOWED_KEEP_SLUG_BY_IMAGE.get(img, set())
                if not belongs:
                    requires_replace = True

        # If multiple images for same slug, unify.
        if len(images) > 1:
            requires_replace = True

        if not requires_replace:
            # Keep the best current image for this slug.
            valid_current = [img for img in images if img not in BAD_VISUAL_IMAGES]
            if valid_current:
                # If exact semantic image exists, prefer it.
                semantic = [img for img in valid_current if slug in img]
                selected = sorted(semantic or valid_current)[0]

        if selected is None:
            # Choose a genuinely unused asset first.
            candidates = sorted(
                [p for p in unused_assets if p not in consumed],
                key=lambda p: asset_quality_score(p, slug),
                reverse=True,
            )
            candidates = [p for p in candidates if asset_quality_score(p, slug) > -100]
            if candidates:
                chosen = candidates[0]
                consumed.add(chosen)
                selected = chosen.relative_to(root / "site" / "figures").as_posix()
            else:
                # Last resort: copy a visually strong asset to a dedicated path.
                # This gives a unique file path, but the report marks it explicitly.
                fallback_candidates = sorted(
                    [p for p in assets if p.name not in BAD_VISUAL_IMAGES and p.name not in FORBIDDEN_REPEAT_IMAGES],
                    key=lambda p: asset_quality_score(p, slug),
                    reverse=True,
                )
                if fallback_candidates:
                    chosen = fallback_candidates[0]
                    unique_dir = root / "site" / "figures" / "v78_unique"
                    ext = chosen.suffix.lower()
                    target_name = f"v78_unique_{slug}{ext}"
                    selected = f"v78_unique/{target_name}"
                    warnings.append(f"FALLBACK COPY for {slug}: no unused visual asset remained; will copy {chosen.relative_to(root)} -> site/figures/{selected}")
                else:
                    warnings.append(f"ERROR: no usable replacement image found for chapter slug {slug}")
                    continue

        slug_to_target[slug] = selected

    # Force locality replacement even if no chapter list recognized it.
    if "locality-nonlocality-contextuality" in slug_to_current_images:
        target = slug_to_target.get("locality-nonlocality-contextuality")
        if target and Path(target).name in BAD_VISUAL_IMAGES:
            warnings.append("ERROR: locality still points to the bad image after selection.")

    return slug_to_target, warnings


def apply_html_replacements(root: Path, doc: dict, slug_to_target: Dict[str, str], apply: bool) -> List[str]:
    path = root / doc["html"]
    if not path.exists():
        return []
    text = read_text(path)
    original = text
    notes: List[str] = []

    def repl_block(m: re.Match) -> str:
        nonlocal notes
        whole = m.group(0)
        body = m.group("body")
        h = re.search(r"<h2\b[^>]*>(?P<title>.*?)</h2>", body, re.S | re.I)
        im = re.search(r'<img\b[^>]*\bsrc="(?P<src>[^"]+)"[^>]*>', body, re.S | re.I)
        if not h or not im:
            return whole
        title = re.sub(r"<[^>]+>", "", h.group("title")).strip()
        slug = normalize_title_to_slug(title)
        target_rel_fig = slug_to_target.get(slug)
        if not target_rel_fig:
            return whole
        target_asset = root / "site" / "figures" / target_rel_fig
        new_src = rel_from(path, target_asset, root)
        old_src = im.group("src")
        if old_src == new_src:
            return whole
        notes.append(f"{path.relative_to(root)} :: {slug}: {old_src} -> {new_src}")
        return whole.replace(f'src="{old_src}"', f'src="{new_src}"', 1)

    text = re.sub(
        r'(<div\s+class="chapter-opening"[^>]*>)(?P<body>.*?)(</div>)',
        repl_block,
        text,
        flags=re.S | re.I,
    )

    # If needed, update og:image only when it points to a bad visual image.
    for bad in BAD_VISUAL_IMAGES:
        if bad in text:
            # Do NOT globally replace beyond chapter openings. This only helps if remaining bad is meta or accidental.
            replacement = slug_to_target.get("locality-nonlocality-contextuality")
            if replacement:
                target_asset = root / "site" / "figures" / replacement
                new_src = rel_from(path, target_asset, root)
                text = re.sub(rf'(?P<prefix>content=")[^"]*{re.escape(bad)}(?P<suffix>")', rf'\g<prefix>{new_src}\g<suffix>', text)
                text = re.sub(rf'(?P<prefix>src=")[^"]*{re.escape(bad)}(?P<suffix>")', rf'\g<prefix>{new_src}\g<suffix>', text)

    if apply and text != original:
        write_text(path, text)
    return notes


def extract_md_sections(text: str) -> List[Tuple[int, int, str, str]]:
    """
    Returns section ranges with headings and slugs.
    Handles markdown headings and raw HTML h2 in MD.
    """
    matches = []
    # markdown headings
    for m in re.finditer(r'(?m)^(#{1,3})\s+(.+?)\s*$', text):
        title = re.sub(r"<[^>]+>", "", m.group(2)).strip()
        matches.append((m.start(), title))
    # raw html h2 headings
    for m in re.finditer(r'<h2\b[^>]*>(?P<title>.*?)</h2>', text, re.S | re.I):
        title = re.sub(r"<[^>]+>", "", m.group("title")).strip()
        matches.append((m.start(), title))

    matches = sorted(matches, key=lambda x: x[0])
    sections = []
    for i, (start, title) in enumerate(matches):
        end = matches[i + 1][0] if i + 1 < len(matches) else len(text)
        sections.append((start, end, title, normalize_title_to_slug(title)))
    return sections


def apply_md_replacements(root: Path, doc: dict, slug_to_target: Dict[str, str], apply: bool) -> List[str]:
    path = root / doc["md"]
    if not path.exists():
        return []
    text = read_text(path)
    original = text
    notes: List[str] = []
    sections = extract_md_sections(text)
    if not sections:
        return []

    pieces = []
    last = 0
    for start, end, title, slug in sections:
        pieces.append(text[last:start])
        block = text[start:end]
        target_rel_fig = slug_to_target.get(slug)
        if target_rel_fig:
            target_asset = root / "site" / "figures" / target_rel_fig
            new_src = rel_from(path, target_asset, root)

            # Replace first raw HTML img src in this section.
            def img_repl(m: re.Match) -> str:
                old_src = m.group("src")
                if old_src == new_src:
                    return m.group(0)
                notes.append(f"{path.relative_to(root)} :: {slug}: {old_src} -> {new_src}")
                return m.group(0).replace(f'src="{old_src}"', f'src="{new_src}"', 1)

            block2 = re.sub(r'<img\b[^>]*\bsrc="(?P<src>[^"]+)"[^>]*>', img_repl, block, count=1, flags=re.S | re.I)

            # Replace first markdown image in this section if no raw HTML image was changed.
            if block2 == block:
                def md_img_repl(m: re.Match) -> str:
                    old_src = m.group("src")
                    if old_src == new_src:
                        return m.group(0)
                    notes.append(f"{path.relative_to(root)} :: {slug}: {old_src} -> {new_src}")
                    return m.group(0).replace(f']({old_src}', f']({new_src}', 1)
                block2 = re.sub(r'!\[[^\]]*\]\((?P<src>[^)\s]+)', md_img_repl, block, count=1)

            block = block2

        pieces.append(block)
        last = end
    pieces.append(text[last:])
    text = "".join(pieces)

    if apply and text != original:
        write_text(path, text)
    return notes


def ensure_fallback_copies(root: Path, warnings: List[str], slug_to_target: Dict[str, str], apply: bool) -> List[str]:
    notes = []
    fig = root / "site" / "figures"
    # Parse warning copy lines and create copies.
    for w in warnings:
        m = re.search(r"will copy (?P<src>site/figures/.*?) -> site/figures/(?P<dst>.+)$", w)
        if not m:
            continue
        src = root / m.group("src")
        dst = fig / m.group("dst")
        if apply:
            dst.parent.mkdir(parents=True, exist_ok=True)
            if src.exists() and not dst.exists():
                shutil.copy2(src, dst)
        notes.append(f"fallback copy: {src.relative_to(root)} -> {dst.relative_to(root)}")
    return notes


def run_cmd(cmd: List[str], cwd: Path) -> Tuple[int, str]:
    try:
        proc = subprocess.run(cmd, cwd=str(cwd), text=True, capture_output=True)
        return proc.returncode, (proc.stdout + proc.stderr).strip()
    except FileNotFoundError:
        return 127, f"command not found: {cmd[0]}"


def rebuild_docx_and_pdf(root: Path, target_docs: List[dict], apply: bool, rebuild_docx: bool, rebuild_pdf: bool) -> List[str]:
    notes = []
    if not apply:
        return notes

    for doc in target_docs:
        html_path = root / doc["html"]
        docx_path = root / doc["docx"]
        pdf_path = root / doc["pdf"]
        if not html_path.exists():
            continue

        if rebuild_docx:
            if shutil.which("pandoc"):
                cmd = [
                    "pandoc",
                    str(html_path),
                    "--from=html",
                    "--to=docx",
                    f"--resource-path={html_path.parent}:{root / 'site'}:{root / 'site' / 'figures'}",
                    "-o", str(docx_path),
                ]
                code, out = run_cmd(cmd, root)
                if code == 0:
                    notes.append(f"rebuilt DOCX: {docx_path.relative_to(root)}")
                else:
                    notes.append(f"DOCX rebuild failed for {docx_path.relative_to(root)}: {out[:1000]}")
            else:
                notes.append(f"DOCX skipped: pandoc not installed for {docx_path.relative_to(root)}")

        if rebuild_pdf:
            # Prefer weasyprint CLI to preserve HTML/CSS.
            if shutil.which("weasyprint"):
                cmd = ["weasyprint", str(html_path), str(pdf_path)]
                code, out = run_cmd(cmd, root)
                if code == 0:
                    notes.append(f"rebuilt PDF: {pdf_path.relative_to(root)}")
                else:
                    notes.append(f"PDF rebuild failed for {pdf_path.relative_to(root)}: {out[:1000]}")
            else:
                notes.append(f"PDF skipped: weasyprint not installed for {pdf_path.relative_to(root)}")

    return notes


def write_report(root: Path, report: str) -> None:
    report_dir = root / "_product_docs" / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / "BPI_V78_PRECISE_MAIN_DOCS_IMAGE_FIX_REPORT_HE.md").write_text(report, encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="Actually write changes. Without this flag, audit only.")
    ap.add_argument("--rebuild-docx", action="store_true", help="Rebuild DOCX from corrected HTML using pandoc.")
    ap.add_argument("--rebuild-pdf", action="store_true", help="Rebuild PDF from corrected HTML using weasyprint.")
    ap.add_argument("--cleanup-packages", action="store_true", help="Remove old bpi_v7x package folders after successful apply.")
    args = ap.parse_args()

    root = Path.cwd()
    if not (root / "site" / "figures").exists():
        print("ERROR: run from project root containing site/figures", file=sys.stderr)
        return 2

    chapters, image_to_slugs = build_usage(root)
    slug_to_target, warnings = choose_replacements(root, chapters, image_to_slugs)

    # Ensure fallback copy files exist before applying text references.
    fallback_notes = ensure_fallback_copies(root, warnings, slug_to_target, args.apply)

    notes = []
    for doc in TARGETS:
        notes.extend(apply_html_replacements(root, doc, slug_to_target, args.apply))
        notes.extend(apply_md_replacements(root, doc, slug_to_target, args.apply))

    rebuild_notes = rebuild_docx_and_pdf(
        root,
        TARGETS,
        apply=args.apply,
        rebuild_docx=args.rebuild_docx,
        rebuild_pdf=args.rebuild_pdf,
    )

    if args.apply and args.cleanup_packages:
        for pat in ("bpi_v73_*", "bpi_v74_*", "bpi_v75_*", "bpi_v76_*", "bpi_v77_*", "bpi_v78_*"):
            for p in root.glob(pat):
                if p.is_dir() and p.name != "bpi_v78_precise_main_docs_image_fix":
                    shutil.rmtree(p, ignore_errors=True)

    # Re-read after possible application for final audit.
    chapters_after, image_to_slugs_after = build_usage(root)
    duplicate_after = {img: sorted(slugs) for img, slugs in image_to_slugs_after.items() if len(slugs) > 1}
    bad_after = [ch for ch in chapters_after if ch.image_name in BAD_VISUAL_IMAGES]
    forbidden_wrong_after = [
        ch for ch in chapters_after
        if ch.image_name in FORBIDDEN_REPEAT_IMAGES and ch.slug not in ALLOWED_KEEP_SLUG_BY_IMAGE.get(ch.image_name, set())
    ]

    report_lines = []
    report_lines.append("# BPI V78 — תיקון מדויק לתמונות במסמכים הראשיים\n")
    report_lines.append(f"מצב: {'APPLY — נכתבו שינויים' if args.apply else 'AUDIT ONLY — לא נכתבו שינויים'}\n")
    report_lines.append("## כלל התיקון\n")
    report_lines.append("- אותו פרק בעברית/אנגלית וב־HTML/MD/DOCX/PDF צריך להשתמש באותה תמונת פרק.")
    report_lines.append("- פרקים שונים לא אמורים להשתמש באותה תמונת פרק.")
    report_lines.append("- תמונת `v25_chapter_locality-nonlocality-contextuality.png` אסורה כי אינה עומדת בסטנדרט.")
    report_lines.append("- תמונת `v25_chapter_i-have-no-mouth.png` יכולה להישאר רק בפרק I Have No Mouth / אין לי פה.\n")

    report_lines.append("## מיפוי פרקים → תמונות יעד\n")
    for slug in sorted(slug_to_target):
        report_lines.append(f"- `{slug}` → `site/figures/{slug_to_target[slug]}`")

    if notes:
        report_lines.append("\n## החלפות טקסט מתוכננות/שבוצעו\n")
        for n in notes:
            report_lines.append(f"- {n}")
    else:
        report_lines.append("\n## החלפות טקסט\n- לא נמצאו החלפות נדרשות או שהמסמכים כבר תואמים למיפוי.")

    if fallback_notes or warnings:
        report_lines.append("\n## אזהרות / fallback\n")
        for w in warnings:
            report_lines.append(f"- {w}")
        for n in fallback_notes:
            report_lines.append(f"- {n}")

    if rebuild_notes:
        report_lines.append("\n## DOCX / PDF\n")
        for n in rebuild_notes:
            report_lines.append(f"- {n}")
    else:
        report_lines.append("\n## DOCX / PDF\n- לא נבנו מחדש. כדי לעדכן אותם הרץ עם `--apply --rebuild-docx --rebuild-pdf` אחרי בדיקת HTML/MD.")

    report_lines.append("\n## בדיקת חזרות אחרי התיקון\n")
    if duplicate_after:
        report_lines.append("עדיין יש תמונות שמשויכות ליותר מפרק אחד:")
        for img, slugs in sorted(duplicate_after.items()):
            report_lines.append(f"- `{img}` → {', '.join(slugs)}")
    else:
        report_lines.append("- אין תמונת פרק אחת שמשויכת ליותר מפרק אחד במסמכי HTML הראשיים.")

    if bad_after:
        report_lines.append("\n## שגיאה: התמונה החלשה עדיין קיימת")
        for ch in bad_after:
            report_lines.append(f"- `{ch.file_path.relative_to(root)}` / `{ch.slug}` / `{ch.src}`")
    else:
        report_lines.append("\n## בדיקת התמונה החלשה\n- `v25_chapter_locality-nonlocality-contextuality.png` לא מופיעה יותר כתמונת פתיחת פרק ב־HTML הראשי.")

    if forbidden_wrong_after:
        report_lines.append("\n## שגיאה: תמונת I Have No Mouth מופיעה בפרקים אחרים")
        for ch in forbidden_wrong_after:
            report_lines.append(f"- `{ch.file_path.relative_to(root)}` / `{ch.slug}` / `{ch.src}`")
    else:
        report_lines.append("\n## בדיקת forbidden-repeat\n- `v25_chapter_i-have-no-mouth.png` לא מופיעה בפרקים אחרים לפי ה־HTML הראשי.")

    report = "\n".join(report_lines) + "\n"
    write_report(root, report)

    print(report)
    print("Report:", root / "_product_docs" / "reports" / "BPI_V78_PRECISE_MAIN_DOCS_IMAGE_FIX_REPORT_HE.md")

    if (bad_after or forbidden_wrong_after) and args.apply:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
