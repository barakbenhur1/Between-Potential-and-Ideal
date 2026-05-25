#!/usr/bin/env python3
from pathlib import Path
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime

ROOT = Path.cwd()
SITE = ROOT / "site"
REPORT = ROOT / "_product_docs" / "reports" / "BPI_V85_LOGICAL_COVER_BLANK_PAGES_FIX_REPORT_HE.md"

TARGETS = [
    {
        "name": "Logical Hebrew",
        "html": SITE / "files" / "editorial-tightened" / "between-potential-and-ideal-tightened-he.html",
        "pdf": SITE / "files" / "editorial-tightened" / "between-potential-and-ideal-tightened-he.pdf",
        "docx": SITE / "files" / "editorial-tightened" / "between-potential-and-ideal-tightened-he.docx",
        "dir": "rtl",
    },
    {
        "name": "Logical English",
        "html": SITE / "files" / "editorial-tightened" / "between-potential-and-ideal-tightened-en.html",
        "pdf": SITE / "files" / "editorial-tightened" / "between-potential-and-ideal-tightened-en.pdf",
        "docx": SITE / "files" / "editorial-tightened" / "between-potential-and-ideal-tightened-en.docx",
        "dir": "ltr",
    },
]

STYLE_ID = "v85-logical-cover-blank-page-fix"

V85_CSS = f"""
<style id="{STYLE_ID}">
/* V85 - logical PDF/DOCX export repair.
   Purpose: keep logical cover compact, centered and printable; prevent accidental blank pages. */

@media screen {{
  body.logical-document-page .cover,
  body.logical-document-page .title-page,
  body.logical-document-page .document-cover,
  body.logical-document-page .front-cover,
  body.logical-document-page section.cover,
  body .logical-cover,
  body .cover.logical-cover {{
    box-sizing: border-box !important;
    width: min(900px, 92vw) !important;
    max-width: 900px !important;
    min-height: 0 !important;
    height: auto !important;
    margin: 32px auto 42px !important;
    padding: 42px 42px 34px !important;
    text-align: center !important;
    overflow: visible !important;
  }}

  body.logical-document-page .cover h1,
  body.logical-document-page .title-page h1,
  body.logical-document-page .document-cover h1,
  body.logical-document-page .front-cover h1,
  body .logical-cover h1 {{
    text-align: center !important;
    margin: 16px auto 12px !important;
    max-width: 760px !important;
    line-height: 1.12 !important;
    white-space: normal !important;
  }}

  body.logical-document-page .cover figure,
  body.logical-document-page .title-page figure,
  body.logical-document-page .document-cover figure,
  body.logical-document-page .front-cover figure,
  body .logical-cover figure,
  body.logical-document-page .cover .image-frame,
  body.logical-document-page .title-page .image-frame,
  body.logical-document-page .document-cover .image-frame,
  body.logical-document-page .front-cover .image-frame,
  body .logical-cover .image-frame {{
    width: min(560px, 80%) !important;
    max-width: 560px !important;
    margin: 28px auto 24px !important;
    padding: 14px !important;
    box-sizing: border-box !important;
    text-align: center !important;
    overflow: hidden !important;
  }}

  body.logical-document-page .cover img,
  body.logical-document-page .title-page img,
  body.logical-document-page .document-cover img,
  body.logical-document-page .front-cover img,
  body .logical-cover img {{
    display: block !important;
    width: auto !important;
    max-width: 100% !important;
    max-height: 340px !important;
    height: auto !important;
    object-fit: contain !important;
    margin: 0 auto !important;
  }}
}}

@media print {{
  @page {{
    size: A4;
    margin: 14mm 16mm;
  }}

  html, body {{
    width: auto !important;
    min-width: 0 !important;
    max-width: none !important;
    overflow: visible !important;
    background: #fffaf0 !important;
  }}

  body {{
    margin: 0 !important;
    padding: 0 !important;
  }}

  /* Cover must fit one page and not push an empty page after it. */
  body.logical-document-page .cover,
  body.logical-document-page .title-page,
  body.logical-document-page .document-cover,
  body.logical-document-page .front-cover,
  body.logical-document-page section.cover,
  body .logical-cover,
  body .cover.logical-cover {{
    box-sizing: border-box !important;
    display: block !important;
    position: static !important;
    width: 100% !important;
    max-width: 100% !important;
    min-width: 0 !important;
    min-height: 0 !important;
    height: auto !important;
    max-height: none !important;
    margin: 0 auto !important;
    padding: 10mm 0 7mm !important;
    overflow: visible !important;
    text-align: center !important;
    page-break-inside: avoid !important;
    break-inside: avoid !important;
    page-break-after: always !important;
    break-after: page !important;
  }}

  body.logical-document-page .cover + *,
  body.logical-document-page .title-page + *,
  body.logical-document-page .document-cover + *,
  body.logical-document-page .front-cover + *,
  body .logical-cover + * {{
    page-break-before: auto !important;
    break-before: auto !important;
  }}

  body.logical-document-page .cover h1,
  body.logical-document-page .title-page h1,
  body.logical-document-page .document-cover h1,
  body.logical-document-page .front-cover h1,
  body .logical-cover h1 {{
    display: block !important;
    width: 100% !important;
    max-width: 160mm !important;
    margin: 8mm auto 4mm !important;
    padding: 0 !important;
    text-align: center !important;
    line-height: 1.12 !important;
    font-size: 29pt !important;
    white-space: normal !important;
    overflow: visible !important;
  }}

  body.logical-document-page .cover h2,
  body.logical-document-page .title-page h2,
  body.logical-document-page .document-cover h2,
  body.logical-document-page .front-cover h2,
  body .logical-cover h2,
  body.logical-document-page .cover p,
  body.logical-document-page .title-page p,
  body.logical-document-page .document-cover p,
  body.logical-document-page .front-cover p,
  body .logical-cover p {{
    max-width: 150mm !important;
    margin-left: auto !important;
    margin-right: auto !important;
    text-align: center !important;
    line-height: 1.35 !important;
    white-space: normal !important;
    overflow: visible !important;
  }}

  body.logical-document-page .cover figure,
  body.logical-document-page .title-page figure,
  body.logical-document-page .document-cover figure,
  body.logical-document-page .front-cover figure,
  body .logical-cover figure,
  body.logical-document-page .cover .image-frame,
  body.logical-document-page .title-page .image-frame,
  body.logical-document-page .document-cover .image-frame,
  body.logical-document-page .front-cover .image-frame,
  body .logical-cover .image-frame {{
    display: block !important;
    float: none !important;
    clear: both !important;
    box-sizing: border-box !important;
    width: 125mm !important;
    max-width: 125mm !important;
    min-height: 0 !important;
    height: auto !important;
    max-height: none !important;
    margin: 8mm auto 6mm !important;
    padding: 3mm !important;
    text-align: center !important;
    page-break-inside: avoid !important;
    break-inside: avoid !important;
    overflow: hidden !important;
  }}

  body.logical-document-page .cover img,
  body.logical-document-page .title-page img,
  body.logical-document-page .document-cover img,
  body.logical-document-page .front-cover img,
  body .logical-cover img {{
    display: block !important;
    float: none !important;
    width: auto !important;
    max-width: 116mm !important;
    height: auto !important;
    max-height: 62mm !important;
    object-fit: contain !important;
    object-position: center center !important;
    margin: 0 auto !important;
  }}

  body.logical-document-page .cover figcaption,
  body.logical-document-page .title-page figcaption,
  body.logical-document-page .document-cover figcaption,
  body.logical-document-page .front-cover figcaption,
  body .logical-cover figcaption {{
    display: block !important;
    width: 100% !important;
    max-width: 118mm !important;
    margin: 3mm auto 0 !important;
    text-align: center !important;
    line-height: 1.35 !important;
    font-size: 9.5pt !important;
  }}

  /* Avoid accidental empty pages from empty spacer elements. */
  section:empty,
  div:empty,
  p:empty {{
    display: none !important;
    min-height: 0 !important;
    height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
    page-break-before: auto !important;
    page-break-after: auto !important;
    break-before: auto !important;
    break-after: auto !important;
  }}

  .empty-page,
  .blank-page,
  .page-spacer,
  .spacer-page {{
    display: none !important;
    page-break-before: auto !important;
    page-break-after: auto !important;
    break-before: auto !important;
    break-after: auto !important;
  }}
}}
</style>
"""

def run(cmd):
    return subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)

def has_cmd(name):
    return shutil.which(name) is not None

def backup(path, report):
    if path.exists():
        bak = path.with_suffix(path.suffix + ".v85.bak")
        shutil.copy2(path, bak)
        report.append(f"  - backup: `{bak.relative_to(ROOT)}`")

def ensure_project():
    if not SITE.exists():
        raise SystemExit("ERROR: run from project root containing site/")

def read(path):
    return path.read_text(encoding="utf-8", errors="ignore")

def write(path, text):
    path.write_text(text, encoding="utf-8")

def ensure_body_class(text):
    # Add logical-document-page to body for CSS targeting.
    def repl(m):
        tag = m.group(0)
        if "logical-document-page" in tag:
            return tag
        if "class=" in tag:
            return re.sub(r'class="([^"]*)"', lambda x: f'class="{x.group(1)} logical-document-page"', tag, count=1)
        return tag[:-1] + ' class="logical-document-page">'
    return re.sub(r"<body\b[^>]*>", repl, text, count=1, flags=re.I)

def patch_html_cover_layout(html_path, report):
    if not html_path.exists():
        report.append(f"- missing HTML: `{html_path.relative_to(ROOT)}`")
        return False
    text = read(html_path)
    original = text

    # Remove previous V85 block if rerun.
    text = re.sub(rf"\n?<style id=\"{STYLE_ID}\">.*?</style>\n?", "\n", text, flags=re.S)

    # Add robust targeting class.
    text = ensure_body_class(text)

    # Mark the likely first cover element as logical-cover if not already marked.
    # This is conservative: only the first .cover/title-page/document-cover/front-cover section.
    def mark_first_cover(t):
        pattern = r'(<(?:section|div)\b[^>]*class="([^"]*(?:cover|title-page|document-cover|front-cover)[^"]*)"[^>]*>)'
        m = re.search(pattern, t, flags=re.I)
        if not m:
            return t
        tag = m.group(1)
        if "logical-cover" in tag:
            return t
        new_tag = tag.replace(m.group(2), m.group(2) + " logical-cover")
        return t[:m.start(1)] + new_tag + t[m.end(1):]
    text = mark_first_cover(text)

    # Inject CSS into head.
    if "</head>" in text:
        text = text.replace("</head>", V85_CSS + "\n</head>", 1)
    else:
        text = V85_CSS + "\n" + text

    if text != original:
        backup(html_path, report)
        write(html_path, text)
        report.append(f"- patched cover/export CSS in `{html_path.relative_to(ROOT)}`")
        return True
    report.append(f"- no HTML patch needed: `{html_path.relative_to(ROOT)}`")
    return False

def rebuild_pdf(html_path, pdf_path, report):
    if not html_path.exists():
        report.append("  - PDF skipped: HTML source missing")
        return False

    if has_cmd("weasyprint"):
        backup(pdf_path, report)
        r = run(["weasyprint", str(html_path), str(pdf_path)])
        if r.returncode == 0 and pdf_path.exists() and pdf_path.stat().st_size > 1000:
            report.append(f"  - PDF rebuilt with weasyprint: `{pdf_path.relative_to(ROOT)}`")
            return True
        report.append(f"  - PDF weasyprint failed: {r.stderr[:1200].strip()}")

    r = run([sys.executable, "-m", "weasyprint", "--version"])
    if r.returncode == 0:
        backup(pdf_path, report)
        r = run([sys.executable, "-m", "weasyprint", str(html_path), str(pdf_path)])
        if r.returncode == 0 and pdf_path.exists() and pdf_path.stat().st_size > 1000:
            report.append(f"  - PDF rebuilt with python -m weasyprint: `{pdf_path.relative_to(ROOT)}`")
            return True
        report.append(f"  - PDF python -m weasyprint failed: {r.stderr[:1200].strip()}")

    report.append("  - PDF skipped: install WeasyPrint with `python3 -m pip install weasyprint`")
    return False

def remove_blank_pdf_pages(pdf_path, report):
    if not pdf_path.exists():
        return False
    try:
        import fitz
    except Exception:
        report.append("  - blank-page cleanup skipped: PyMuPDF missing; install with `python3 -m pip install pymupdf`")
        return False

    doc = fitz.open(pdf_path)
    to_delete = []
    for i, page in enumerate(doc):
        if i == 0:
            continue
        text = page.get_text("text").strip()
        images = page.get_images(full=True)
        # If page has no text and no raster image, it is almost always a spacer/blank page.
        if not text and not images:
            to_delete.append(i)

    if not to_delete:
        report.append("  - blank-page cleanup: no blank pages detected")
        doc.close()
        return False

    backup(pdf_path, report)
    # Delete from end to start.
    for i in reversed(to_delete):
        doc.delete_page(i)
    tmp = pdf_path.with_suffix(".v85.cleaned.pdf")
    doc.save(tmp, garbage=4, deflate=True)
    doc.close()
    tmp.replace(pdf_path)
    report.append(f"  - removed blank PDF pages: {', '.join(str(i+1) for i in to_delete)}")
    return True

def rebuild_docx(html_path, docx_path, report):
    if not html_path.exists():
        report.append("  - DOCX skipped: HTML source missing")
        return False
    if not has_cmd("pandoc"):
        report.append("  - DOCX skipped: install pandoc with `brew install pandoc`")
        return False

    backup(docx_path, report)
    resource_path = os.pathsep.join([
        str(html_path.parent),
        str(SITE / "files" / "editorial-tightened"),
        str(SITE / "files"),
        str(SITE),
        str(SITE / "figures"),
    ])
    r = run(["pandoc", str(html_path), "-o", str(docx_path), "--standalone", f"--resource-path={resource_path}"])
    if r.returncode == 0 and docx_path.exists() and docx_path.stat().st_size > 1000:
        report.append(f"  - DOCX rebuilt with pandoc: `{docx_path.relative_to(ROOT)}`")
        return True
    report.append(f"  - DOCX pandoc failed: {r.stderr[:1200].strip()}")
    return False

def main():
    ensure_project()
    report = []
    report.append("# BPI V85 - תיקון דף שער ודפים ריקים בגרסה הלוגית")
    report.append("")
    report.append(f"Generated: {datetime.now().isoformat(timespec='seconds')}")
    report.append("")
    report.append("הבעיה נוצרה מבניית PDF/DOCX מתוך HTML עם CSS שלא כפה דף שער קומפקטי וגרם לשבירת עמודים/עמודים ריקים.")
    report.append("V85 מוסיף CSS ייעודי לייצוא, בונה מחדש PDF/DOCX של הגרסה הלוגית ומנקה עמודים ריקים ב-PDF.")
    report.append("")

    for target in TARGETS:
        report.append(f"## {target['name']}")
        html_path = target["html"]
        pdf_path = target["pdf"]
        docx_path = target["docx"]

        patch_html_cover_layout(html_path, report)
        rebuilt_pdf = rebuild_pdf(html_path, pdf_path, report)
        if rebuilt_pdf:
            remove_blank_pdf_pages(pdf_path, report)
        rebuild_docx(html_path, docx_path, report)
        report.append("")

    report.append("## בדיקות מומלצות")
    report.append("```bash")
    report.append("open site/files/editorial-tightened/between-potential-and-ideal-tightened-he.html")
    report.append("open site/files/editorial-tightened/between-potential-and-ideal-tightened-he.pdf")
    report.append("open site/files/editorial-tightened/between-potential-and-ideal-tightened-en.pdf")
    report.append("git status --short")
    report.append("git diff --stat")
    report.append("```")

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(report) + "\n", encoding="utf-8")
    print("\n".join(report))
    print("")
    print("Report:", REPORT)

if __name__ == "__main__":
    main()
