#!/usr/bin/env python3
"""
BPI V86 - close the large visual gap between theory covers and the interactive TOC.

Safe default:
- patches generated theory HTML files only;
- does not rebuild PDF/DOCX unless --rebuild-exports is explicitly passed;
- avoids the WeasyPrint image-path regression that can replace images with text.

This is intentionally narrow:
- targets generated theory document HTML files, especially the logical/editorial-tightened version;
- does not touch story blurbs or body text;
- keeps print/PDF cover page separation, but prevents an extra blank/gap before the TOC.
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "_product_docs" / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)
REPORT = REPORT_DIR / "BPI_V86_CLOSE_THEORY_COVER_TOC_GAP_REPORT_HE.md"

STYLE_ID = "bpi-v86-close-theory-cover-toc-gap"
STYLE_BLOCK = f"""
<style id=\"{STYLE_ID}\">
/* BPI V86 - close cover-to-TOC gap in theory documents.
   Scope: generated theory documents only. Does not affect story blurbs/content. */
@media screen {{
  body.design-prompt-theme:not(.public-page) main,
  main {{
    padding-top: 28px !important;
    padding-bottom: 48px !important;
  }}

  /* The logical exports had an explicit spacer paragraph after the cover.
     Hide it even if an older generated file still contains it. */
  .logical-cover-spacer,
  p.logical-cover-spacer,
  .cover-spacer,
  p.cover-spacer {{
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
    min-height: 0 !important;
    max-height: 0 !important;
    line-height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
    overflow: hidden !important;
    break-before: auto !important;
    page-break-before: auto !important;
    break-after: auto !important;
    page-break-after: auto !important;
  }}

  .logical-cover-spacer + div[style*="page-break-after"],
  p.logical-cover-spacer + div[style*="page-break-after"],
  .cover-spacer + div[style*="page-break-after"] {{
    display: none !important;
    height: 0 !important;
    min-height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
    break-before: auto !important;
    page-break-before: auto !important;
    break-after: auto !important;
    page-break-after: auto !important;
  }}

  body.design-prompt-theme:not(.public-page) .cover,
  body.design-prompt-theme:not(.public-page) .logical-cover,
  body.design-prompt-theme:not(.public-page) .document-cover,
  body.design-prompt-theme:not(.public-page) .page.cover,
  main > .cover:first-child,
  main > .logical-cover:first-child,
  main > .document-cover:first-child,
  main > .page.cover:first-child {{
    min-height: 0 !important;
    height: auto !important;
    max-height: none !important;
    padding-top: 46px !important;
    padding-bottom: 38px !important;
    margin-bottom: 22px !important;
    break-after: auto !important;
    page-break-after: auto !important;
  }}

  body.design-prompt-theme:not(.public-page) .cover + .document-screen-toc,
  body.design-prompt-theme:not(.public-page) .logical-cover + .document-screen-toc,
  body.design-prompt-theme:not(.public-page) .document-cover + .document-screen-toc,
  body.design-prompt-theme:not(.public-page) .page.cover + .document-screen-toc,
  main > .cover:first-child + .document-screen-toc,
  main > .logical-cover:first-child + .document-screen-toc,
  main > .document-cover:first-child + .document-screen-toc,
  main > .page.cover:first-child + .document-screen-toc,
  .logical-cover + .document-screen-toc,
  .logical-cover + .logical-cover-spacer + .document-screen-toc,
  .logical-cover + .logical-cover-spacer + div + .document-screen-toc,
  .document-screen-toc,
  #interactive-toc {{
    break-before: auto !important;
    page-break-before: auto !important;
    margin-top: 18px !important;
  }}
}}
@media print {{
  .logical-cover-spacer,
  p.logical-cover-spacer,
  .cover-spacer,
  p.cover-spacer,
  .logical-cover-spacer + div[style*="page-break-after"],
  p.logical-cover-spacer + div[style*="page-break-after"] {{
    display: none !important;
    height: 0 !important;
    min-height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
  }}

  body.design-prompt-theme:not(.public-page) .cover,
  body.design-prompt-theme:not(.public-page) .logical-cover,
  body.design-prompt-theme:not(.public-page) .document-cover,
  body.design-prompt-theme:not(.public-page) .page.cover,
  main > .cover:first-child,
  main > .logical-cover:first-child,
  main > .document-cover:first-child,
  main > .page.cover:first-child {{
    height: auto !important;
    min-height: calc(297mm - 36mm) !important;
    max-height: none !important;
    padding: 16mm 14mm 12mm !important;
    margin-bottom: 0 !important;
    break-after: page !important;
    page-break-after: always !important;
    overflow: hidden !important;
  }}
  body.design-prompt-theme:not(.public-page) .document-screen-toc,
  body.design-prompt-theme:not(.public-page) #interactive-toc,
  .document-screen-toc,
  #interactive-toc {{
    break-before: auto !important;
    page-break-before: auto !important;
    margin-top: 0 !important;
  }}
}}
</style>
""".strip()

TARGET_GLOBS = [
    "site/files/editorial-tightened/between-potential-and-ideal-tightened-*.html",
    "site/files/**/between-potential-and-ideal*.html",
    "site/files/**/between_potential_and_ideal*.html",
]
EXCLUDE_PARTS = ("/appendices/", "/ai-believes/", "/stories/")


def is_theory_doc(path: Path, text: str) -> bool:
    rel = "/" + path.relative_to(ROOT).as_posix()
    if any(part in rel for part in EXCLUDE_PARTS):
        return False
    if "document-screen-toc" not in text and "interactive-toc" not in text:
        return False
    hay = (str(path).lower() + "\n" + text[:8000].lower())
    return "potential" in hay or "פוטנציאל" in hay or "ideal" in hay or "אידיאל" in hay


def remove_cover_spacers(text: str) -> tuple[str, int]:
    count = 0

    patterns = [
        r"\s*<p\b[^>]*class=[\"'][^\"']*logical-cover-spacer[^\"']*[\"'][^>]*>.*?</p>\s*<div\b[^>]*style=[\"'][^\"']*(?:page-break-after|break-after)\s*:\s*(?:always|page)[^\"']*[\"'][^>]*>\s*</div>",
        r"\s*<p\b[^>]*class=[\"'][^\"']*logical-cover-spacer[^\"']*[\"'][^>]*>.*?</p>",
        r"\s*<div\b[^>]*style=[\"'][^\"']*(?:page-break-after|break-after)\s*:\s*(?:always|page)[^\"']*height\s*:\s*0[^\"']*[\"'][^>]*>\s*</div>",
    ]

    for pattern in patterns:
        text, n = re.subn(pattern, "\n", text, flags=re.S | re.I)
        count += n

    def clean_toc_style(match: re.Match[str]) -> str:
        nonlocal count
        tag = match.group(0)
        cleaned = re.sub(r"\s*style=[\"'][^\"']*(?:page-break-before|break-before)\s*:\s*(?:always|page)[^\"']*[\"']", "", tag, flags=re.I)
        if cleaned != tag:
            count += 1
        return cleaned

    text = re.sub(r"<section\b[^>]*(?:document-screen-toc|interactive-toc)[^>]*>", clean_toc_style, text, flags=re.I)
    return text, count


def patch_html(path: Path) -> tuple[bool, int]:
    text = path.read_text(encoding="utf-8")
    if not is_theory_doc(path, text):
        return False, 0

    text2, removed = remove_cover_spacers(text)
    text2 = re.sub(rf"\n?<style id=[\"']{re.escape(STYLE_ID)}[\"']>.*?</style>", "", text2, flags=re.S)
    if "</head>" in text2:
        text2 = text2.replace("</head>", STYLE_BLOCK + "\n</head>", 1)
    else:
        text2 = STYLE_BLOCK + "\n" + text2
    if text2 != text:
        path.write_text(text2, encoding="utf-8")
        return True, removed
    return False, removed


def rebuild_pdf(html_path: Path, report: list[str]) -> None:
    pdf_path = html_path.with_suffix(".pdf")
    try:
        from weasyprint import HTML  # type: ignore
    except Exception:
        report.append(f"- PDF skipped, weasyprint unavailable: `{pdf_path.relative_to(ROOT)}`")
        return
    try:
        if pdf_path.exists():
            shutil.copy2(pdf_path, pdf_path.with_suffix(pdf_path.suffix + ".v86.bak"))
        HTML(filename=str(html_path)).write_pdf(str(pdf_path))
        report.append(f"- PDF rebuilt: `{pdf_path.relative_to(ROOT)}`")
    except Exception as exc:
        report.append(f"- PDF rebuild failed for `{pdf_path.relative_to(ROOT)}`: {exc}")


def rebuild_docx(html_path: Path, report: list[str]) -> None:
    pandoc = shutil.which("pandoc")
    docx_path = html_path.with_suffix(".docx")
    if not pandoc:
        report.append(f"- DOCX skipped, pandoc unavailable: `{docx_path.relative_to(ROOT)}`")
        return
    try:
        if docx_path.exists():
            shutil.copy2(docx_path, docx_path.with_suffix(docx_path.suffix + ".v86.bak"))
        subprocess.run([pandoc, str(html_path), "--from", "html", "--to", "docx", "--standalone", "-o", str(docx_path)], check=True, cwd=ROOT)
        report.append(f"- DOCX rebuilt: `{docx_path.relative_to(ROOT)}`")
    except Exception as exc:
        report.append(f"- DOCX rebuild failed for `{docx_path.relative_to(ROOT)}`: {exc}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rebuild-exports", action="store_true", help="Also rebuild PDF/DOCX. Off by default to avoid image-path regressions.")
    args = parser.parse_args()

    candidates: list[Path] = []
    for pattern in TARGET_GLOBS:
        candidates.extend(ROOT.glob(pattern))
    unique = sorted(set(p for p in candidates if p.is_file()))

    patched: list[Path] = []
    report: list[str] = [
        "# BPI V86 - סגירת הרווח בין שער התאוריה לתוכן העניינים",
        "",
        f"Generated: {datetime.utcnow().isoformat(timespec='seconds')}Z",
        "",
        "היקף: קבצי התאוריה בלבד, עם דגש על הגרסה הלוגית / editorial-tightened.",
        "ברירת המחדל בטוחה: HTML בלבד. PDF/DOCX לא נבנים מחדש כדי לא להחליף תמונות בתיאורי טקסט בגלל נתיבי assets.",
        "התיקון מסיר spacer מפורש אחרי השער הלוגי ומנטרל page-break-before מיותר בתוכן העניינים.",
        "",
    ]

    for path in unique:
        changed, removed = patch_html(path)
        if changed:
            patched.append(path)
            report.append(f"- HTML patched: `{path.relative_to(ROOT)}`")
            if removed:
                report.append(f"  - removed/neutralized cover spacer artifacts: {removed}")
            if args.rebuild_exports:
                rebuild_pdf(path, report)
                rebuild_docx(path, report)

    if not patched:
        report.append("- No matching theory HTML files required changes.")

    REPORT.write_text("\n".join(report) + "\n", encoding="utf-8")
    print(f"Patched HTML files: {len(patched)}")
    for p in patched:
        print(f" - {p.relative_to(ROOT)}")
    print(f"Report: {REPORT.relative_to(ROOT)}")
    if not args.rebuild_exports:
        print("PDF/DOCX rebuild skipped by default. Use --rebuild-exports only after verifying image paths.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
