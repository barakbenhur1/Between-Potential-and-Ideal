#!/usr/bin/env python3
"""
Between Potential and Ideal — V72 safe appendix subtitle + image centering fix.

What this script does:
1. HTML: styles and positions the document subtitle directly under the title.
2. HTML: centers all figures/images in appendix/story pages.
3. MD/TXT: moves the subtitle line directly under the title when possible.
4. DOCX: safely patches existing DOCX XML in place, without regenerating the file and without touching media assets:
   - subtitle paragraph is moved directly after the title paragraph when possible;
   - subtitle paragraph becomes centered, italic, bold/semi-bold-like, and larger;
   - paragraphs containing images are centered.

What this script intentionally does NOT do:
- does not rebuild DOCX with pandoc;
- does not rebuild PDF;
- does not delete, rename, or replace images;
- does not edit story text content.
"""
from __future__ import annotations

import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import Iterable
import xml.etree.ElementTree as ET

STYLE_ID = "bpi-v72-appendix-subtitle-image-center-fix"
CSS_FILENAME = "BPI_V72_APPENDIX_SUBTITLE_IMAGE_CENTER_FIX.css"

HE_SUBTITLE = "סיפורים שסיפרתי לאימי"
EN_SUBTITLES = (
    "Stories I Told My Mother",
    "Stories I Told My Mother Before Sleep",
    "Stories I Told My Mother at Bedtime",
)
TITLE_MARKERS = (
    "סיפורים לפני המחשבה",
    "Stories Before Thought",
    "Stories before Thought",
)

EXCLUDED_DIRS = {".git", "node_modules", ".next", "dist", "build", ".cache", "__MACOSX", "bpi_appendix_layout_fix_package"}

CSS_BODY = r'''
/* V72 — safe appendix-only subtitle + image centering fix.
   No content, navigation, asset, or rebuild changes. */
.cover .subtitle,
.cover-subtitle,
.document-subtitle,
.bpi-document-subtitle,
.bpi-doc-subtitle,
.bpi-v72-document-subtitle,
.title + .subtitle,
h1 + .subtitle,
h1 + .document-subtitle,
h1 + .bpi-v72-document-subtitle {
  display: block !important;
  width: min(760px, 100%) !important;
  margin: .18rem auto 1.08rem !important;
  text-align: center !important;
  font-size: clamp(1.18rem, 2.35vw, 1.82rem) !important;
  line-height: 1.28 !important;
  font-style: italic !important;
  font-weight: 600 !important;
  letter-spacing: .01em !important;
  color: #31465d !important;
  opacity: .98 !important;
}
html[dir="rtl"] .cover .subtitle,
html[dir="rtl"] .cover-subtitle,
html[dir="rtl"] .document-subtitle,
html[dir="rtl"] .bpi-document-subtitle,
html[dir="rtl"] .bpi-doc-subtitle,
html[dir="rtl"] .bpi-v72-document-subtitle {
  font-family: "Noto Sans Hebrew", "Rubik", "Assistant", Arial, sans-serif !important;
  font-weight: 600 !important;
}
html[dir="ltr"] .cover .subtitle,
html[dir="ltr"] .cover-subtitle,
html[dir="ltr"] .document-subtitle,
html[dir="ltr"] .bpi-document-subtitle,
html[dir="ltr"] .bpi-doc-subtitle,
html[dir="ltr"] .bpi-v72-document-subtitle {
  font-family: Georgia, "Times New Roman", serif !important;
  font-weight: 600 !important;
}
.cover .title,
.cover h1,
.title,
h1 { margin-bottom: .16rem !important; }
.cover-title-block,
.cover .title-block,
.document-title-block,
.story-head,
.cover hgroup,
hgroup {
  text-align: center !important;
  break-inside: avoid !important;
  page-break-inside: avoid !important;
}
.cover figure,
.cover .image-frame,
.cover .cover-image-frame,
.cover .cover-figure,
.story figure,
.story .image-frame,
.chapter-figure,
.image-frame,
figure.image-frame,
figure.chapter-figure,
figure {
  float: none !important;
  clear: both !important;
  display: block !important;
  margin-left: auto !important;
  margin-right: auto !important;
  text-align: center !important;
}
.cover img,
.cover-image,
.cover-figure img,
.cover .image-frame img,
.story img,
.story figure img,
.story .image-frame img,
.chapter-figure img,
.image-frame img,
figure img,
main img,
article img {
  float: none !important;
  display: block !important;
  margin-left: auto !important;
  margin-right: auto !important;
  object-position: center center !important;
}
.image-frame figcaption,
.chapter-figure figcaption,
figure figcaption { text-align: center !important; }
@media print {
  .cover .subtitle,
  .cover-subtitle,
  .document-subtitle,
  .bpi-document-subtitle,
  .bpi-doc-subtitle,
  .bpi-v72-document-subtitle,
  .title + .subtitle,
  h1 + .subtitle,
  h1 + .document-subtitle,
  h1 + .bpi-v72-document-subtitle {
    margin-top: .12rem !important;
    margin-bottom: .9rem !important;
  }
  .cover-title-block,
  .cover .title-block,
  .document-title-block,
  .story-head,
  .image-frame,
  .chapter-figure,
  figure.image-frame,
  figure.chapter-figure {
    break-inside: avoid !important;
    page-break-inside: avoid !important;
  }
}
'''.strip()
CSS_BLOCK = f'<style id="{STYLE_ID}">\n{CSS_BODY}\n</style>'

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
ET.register_namespace("w", W_NS)
W = f"{{{W_NS}}}"


def root_from_cwd() -> Path:
    cwd = Path.cwd().resolve()
    if (cwd / "site").is_dir():
        return cwd
    for parent in cwd.parents:
        if (parent / "site").is_dir():
            return parent
    return cwd


def skip(path: Path) -> bool:
    return any(part in EXCLUDED_DIRS for part in path.parts)


def iter_files(root: Path, patterns: Iterable[str]) -> Iterable[Path]:
    seen: set[Path] = set()
    for base in (root / "site", root):
        if not base.exists():
            continue
        for pattern in patterns:
            for path in base.rglob(pattern):
                if path in seen or skip(path) or not path.is_file():
                    continue
                seen.add(path)
                yield path


def contains_subtitle(text: str) -> bool:
    return HE_SUBTITLE in text or any(s in text for s in EN_SUBTITLES)


def contains_title(text: str) -> bool:
    return any(t in text for t in TITLE_MARKERS)


def relevant_path(path: Path) -> bool:
    p = str(path).replace("\\", "/").lower()
    return "appendices" in p or "stories" in p or "appendix" in p


def is_relevant_text(path: Path, text: str) -> bool:
    return relevant_path(path) or contains_subtitle(text)


def inject_css(text: str) -> str:
    if STYLE_ID in text:
        return text
    if "</head>" in text:
        return text.replace("</head>", CSS_BLOCK + "\n</head>", 1)
    return CSS_BLOCK + "\n" + text


def add_class_to_tag_attrs(attrs: str) -> str:
    marker_classes = "subtitle document-subtitle bpi-v72-document-subtitle"
    class_re = re.compile(r'class\s*=\s*(["\'])(.*?)\1', flags=re.I | re.S)
    m = class_re.search(attrs)
    if m:
        existing = m.group(2)
        needed = [c for c in marker_classes.split() if c not in existing.split()]
        if not needed:
            return attrs
        return attrs[:m.start(2)] + existing + " " + " ".join(needed) + attrs[m.end(2):]
    return attrs + f' class="{marker_classes}"'


def add_class_to_subtitle_tags(text: str) -> str:
    subtitle_texts = [HE_SUBTITLE, *EN_SUBTITLES]
    union = "|".join(re.escape(s) for s in subtitle_texts)
    pattern = re.compile(rf"<(p|div|span|h2|h3)([^>]*)>([\s\S]*?(?:{union})[\s\S]*?)</\1>", flags=re.I)

    def repl(match: re.Match[str]) -> str:
        tag, attrs, body = match.group(1), match.group(2) or "", match.group(3)
        attrs2 = add_class_to_tag_attrs(attrs)
        return f"<{tag}{attrs2}>{body}</{tag}>"

    return pattern.sub(repl, text)


def first_subtitle_tag(text: str) -> re.Match[str] | None:
    union = "|".join(re.escape(s) for s in [HE_SUBTITLE, *EN_SUBTITLES])
    return re.search(rf"<(p|div|span|h2|h3)[^>]*\b(?:subtitle|document-subtitle|bpi-v72-document-subtitle)\b[^>]*>[\s\S]*?(?:{union})[\s\S]*?</\1>", text, flags=re.I)


def first_title_tag(text: str) -> re.Match[str] | None:
    # Prefer h1. Fall back to simple .title paragraphs/divs/spans, but avoid section.page-title wrappers.
    h1 = re.search(r"<h1\b[^>]*>[\s\S]*?</h1>", text, flags=re.I)
    if h1:
        return h1
    return re.search(r"<(p|div|span)\b[^>]*class=[\"'][^\"']*\btitle\b[^\"']*[\"'][^>]*>[\s\S]*?</\1>", text, flags=re.I)


def move_subtitle_under_title(text: str) -> str:
    head_limit = 120000
    head = text[:head_limit]
    tail = text[head_limit:]
    sub = first_subtitle_tag(head)
    title = first_title_tag(head)
    if not sub or not title:
        return text
    # If subtitle is already immediately after title with only whitespace/small punctuation, keep it.
    between = head[title.end():sub.start()] if title.end() <= sub.start() else ""
    if title.end() <= sub.start() and len(re.sub(r"\s+", "", between)) < 24:
        return text
    subtitle_html = sub.group(0)
    head_without = head[:sub.start()] + head[sub.end():]
    title2 = first_title_tag(head_without)
    if not title2:
        return text
    fixed_head = head_without[:title2.end()] + "\n" + subtitle_html + head_without[title2.end():]
    return fixed_head + tail


def process_html(path: Path) -> bool:
    original = path.read_text(encoding="utf-8", errors="replace")
    if not is_relevant_text(path, original):
        return False
    fixed = original
    fixed = add_class_to_subtitle_tags(fixed)
    fixed = move_subtitle_under_title(fixed)
    fixed = inject_css(fixed)
    if fixed != original:
        path.write_text(fixed, encoding="utf-8")
        return True
    return False


def normalize_subtitle_line(line: str, markdown: bool) -> str:
    raw = line.strip()
    raw_clean = raw.strip("*_ ")
    if HE_SUBTITLE in raw_clean:
        subtitle = HE_SUBTITLE
    else:
        subtitle = next((s for s in EN_SUBTITLES if s in raw_clean), raw_clean)
    if markdown:
        return f"***{subtitle}***"
    return subtitle


def process_md_txt(path: Path) -> bool:
    original = path.read_text(encoding="utf-8", errors="replace")
    if not is_relevant_text(path, original) or not contains_subtitle(original):
        return False
    lines = original.splitlines()
    subtitle_indices = [i for i, line in enumerate(lines[:80]) if contains_subtitle(line)]
    if not subtitle_indices:
        return False
    title_indices = [i for i, line in enumerate(lines[:80]) if line.strip().lstrip("# ").strip() in TITLE_MARKERS]
    if not title_indices:
        title_indices = [i for i, line in enumerate(lines[:20]) if line.strip().startswith("#")]
    if not title_indices:
        return False
    si = subtitle_indices[0]
    ti = title_indices[0]
    markdown = path.suffix.lower() == ".md"
    subtitle_line = normalize_subtitle_line(lines[si], markdown)
    if si == ti + 1 and lines[si] == subtitle_line:
        return False
    lines.pop(si)
    if si < ti:
        ti -= 1
    lines.insert(ti + 1, subtitle_line)
    fixed = "\n".join(lines) + ("\n" if original.endswith("\n") else "")
    if fixed != original:
        path.write_text(fixed, encoding="utf-8")
        return True
    return False


def qn(name: str) -> str:
    return W + name


def p_text(p: ET.Element) -> str:
    return "".join(t.text or "" for t in p.iter(qn("t")))


def has_image(p: ET.Element) -> bool:
    xml = ET.tostring(p, encoding="unicode")
    return "<w:drawing" in xml or "<w:pict" in xml or "<pic:pic" in xml or "<wp:inline" in xml or "<wp:anchor" in xml


def ensure_child(parent: ET.Element, tag: str, first: bool = False) -> ET.Element:
    found = parent.find(tag)
    if found is not None:
        return found
    child = ET.Element(tag)
    if first:
        parent.insert(0, child)
    else:
        parent.append(child)
    return child


def set_attr(el: ET.Element, local: str, value: str) -> None:
    el.set(qn(local), value)


def center_paragraph(p: ET.Element) -> None:
    ppr = p.find(qn("pPr"))
    if ppr is None:
        ppr = ET.Element(qn("pPr"))
        p.insert(0, ppr)
    jc = ppr.find(qn("jc"))
    if jc is None:
        jc = ET.SubElement(ppr, qn("jc"))
    set_attr(jc, "val", "center")


def style_subtitle_paragraph(p: ET.Element) -> None:
    center_paragraph(p)
    ppr = p.find(qn("pPr"))
    assert ppr is not None
    spacing = ppr.find(qn("spacing"))
    if spacing is None:
        spacing = ET.SubElement(ppr, qn("spacing"))
    # Close under title, with enough after-spacing to read as subtitle.
    set_attr(spacing, "before", "40")
    set_attr(spacing, "after", "220")
    pr_rpr = ppr.find(qn("rPr"))
    if pr_rpr is None:
        pr_rpr = ET.SubElement(ppr, qn("rPr"))
    for tag in ("b", "i"):
        if pr_rpr.find(qn(tag)) is None:
            ET.SubElement(pr_rpr, qn(tag))
    sz = pr_rpr.find(qn("sz"))
    if sz is None:
        sz = ET.SubElement(pr_rpr, qn("sz"))
    set_attr(sz, "val", "30")
    color = pr_rpr.find(qn("color"))
    if color is None:
        color = ET.SubElement(pr_rpr, qn("color"))
    set_attr(color, "val", "31465D")
    for r in p.findall(qn("r")):
        rpr = r.find(qn("rPr"))
        if rpr is None:
            rpr = ET.Element(qn("rPr"))
            r.insert(0, rpr)
        for tag in ("b", "i"):
            if rpr.find(qn(tag)) is None:
                ET.SubElement(rpr, qn(tag))
        sz2 = rpr.find(qn("sz"))
        if sz2 is None:
            sz2 = ET.SubElement(rpr, qn("sz"))
        set_attr(sz2, "val", "30")
        color2 = rpr.find(qn("color"))
        if color2 is None:
            color2 = ET.SubElement(rpr, qn("color"))
        set_attr(color2, "val", "31465D")


def process_docx(path: Path) -> bool:
    try:
        with zipfile.ZipFile(path, "r") as zin:
            try:
                xml_bytes = zin.read("word/document.xml")
            except KeyError:
                return False
            all_entries = {info.filename: zin.read(info.filename) for info in zin.infolist()}
            infos = zin.infolist()
        root = ET.fromstring(xml_bytes)
    except Exception as exc:  # noqa: BLE001
        print(f"[WARN] DOCX skipped {path}: {exc}")
        return False

    body = root.find(qn("body"))
    if body is None:
        return False
    children = list(body)
    paragraphs = [el for el in children if el.tag == qn("p")]
    if not paragraphs:
        return False

    subtitle_p = next((p for p in paragraphs if contains_subtitle(p_text(p))), None)
    if subtitle_p is None:
        return False
    title_p = next((p for p in paragraphs if any(t in p_text(p) for t in TITLE_MARKERS)), None)

    changed = False
    before = ET.tostring(root, encoding="utf-8")

    style_subtitle_paragraph(subtitle_p)
    for p in paragraphs:
        if has_image(p):
            center_paragraph(p)

    if title_p is not None:
        current_children = list(body)
        try:
            subtitle_index = current_children.index(subtitle_p)
            title_index = current_children.index(title_p)
            if subtitle_index != title_index + 1:
                body.remove(subtitle_p)
                current_children = list(body)
                title_index = current_children.index(title_p)
                body.insert(title_index + 1, subtitle_p)
        except ValueError:
            pass

    after = ET.tostring(root, encoding="utf-8", xml_declaration=True)
    if after == before:
        return False

    all_entries["word/document.xml"] = after
    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
        tmp_path = Path(tmp.name)
    try:
        with zipfile.ZipFile(tmp_path, "w", compression=zipfile.ZIP_DEFLATED) as zout:
            written: set[str] = set()
            for info in infos:
                if info.filename in written:
                    continue
                data = all_entries[info.filename]
                zi = zipfile.ZipInfo(info.filename, date_time=info.date_time)
                zi.compress_type = zipfile.ZIP_DEFLATED
                zi.external_attr = info.external_attr
                zout.writestr(zi, data)
                written.add(info.filename)
        shutil.move(str(tmp_path), path)
        changed = True
    finally:
        if tmp_path.exists():
            tmp_path.unlink(missing_ok=True)
    return changed


def write_css_file(root: Path) -> Path | None:
    targets = [root / "site/files/appendices", root / "files/appendices"]
    for target in targets:
        if target.exists():
            target.mkdir(parents=True, exist_ok=True)
            css = target / CSS_FILENAME
            css.write_text("/* Generated by apply_appendix_v72_safe_fix.py */\n" + CSS_BODY + "\n", encoding="utf-8")
            return css
    return None


def main() -> int:
    root = root_from_cwd()
    changed: list[str] = []
    css_path = write_css_file(root)
    if css_path:
        changed.append(str(css_path.relative_to(root)))

    for path in iter_files(root, ["*.html"]):
        if process_html(path):
            changed.append(str(path.relative_to(root)))

    for path in iter_files(root, ["*.md", "*.txt"]):
        if process_md_txt(path):
            changed.append(str(path.relative_to(root)))

    for path in iter_files(root, ["*.docx"]):
        # Safe in-place patch only. No rebuilding. No media extraction. No pandoc.
        if relevant_path(path) and process_docx(path):
            changed.append(str(path.relative_to(root)))

    report_dir = root / "_product_docs" / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    report = report_dir / "BPI_V72_SAFE_APPENDIX_SUBTITLE_IMAGE_CENTER_FIX_REPORT_HE.md"
    report.write_text(
        "# BPI V72 — תיקון בטוח לתת־כותרת ומרכוז תמונות בנספחים\n\n"
        "בוצע תיקון ממוקד בלבד:\n\n"
        "- תת־הכותרת `סיפורים שסיפרתי לאימי` נשמרת/מועברת מיד מתחת לכותרת המסמך.\n"
        "- התת־כותרת מקבלת עיצוב תת־כותרת אמיתי: קרובה לכותרת, ממורכזת, סמי־בולד, איטליק, גודל מובחן וצבע משני.\n"
        "- כל התמונות ב־HTML ממורכזות: תמונת שער, figures, image-frame ותמונות סיפורים.\n"
        "- קבצי DOCX תוקנו בצורה בטוחה בתוך ה־XML: ללא בנייה מחדש, ללא החלפת תמונות בתיאורים, וללא נגיעה בקבצי media.\n"
        "- קבצי PDF לא נבנו מחדש בכוונה. כדי לעדכן PDF צריך להריץ את export/build הרשמי של הפרויקט אחרי בדיקת HTML/DOCX.\n\n"
        "## קבצים ששונו\n\n"
        + ("\n".join(f"- `{c}`" for c in changed) if changed else "לא נמצאו קבצים לשינוי.")
        + "\n",
        encoding="utf-8",
    )
    print(f"Root: {root}")
    print(f"Changed files: {len(changed)}")
    for c in changed:
        print(f" - {c}")
    print(f"Report: {report}")
    print("NOTE: PDF rebuild intentionally skipped. No pandoc/weasyprint was called.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
