#!/usr/bin/env python3
from pathlib import Path
import argparse
import html
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.request
import urllib.error

ROOT = Path.cwd()
SITE = ROOT / "site"
AI_DIR = SITE / "files" / "ai-believes"
REPORT = ROOT / "_product_docs" / "reports" / "BPI_V82_COMPLETE_AI_SECTION_FILES_REPORT_HE.md"

AI_DOCS = [
    {
        "slug": "reverse-turing-conversation",
        "he_base": "reverse-turing-conversation-he",
        "en_base": "reverse-turing-conversation-en",
        "he_title": "שיחת טיורינג הפוכה",
        "en_title": "Reverse Turing Conversation",
        "description": "AI section / reverse Turing conversation",
    },
    {
        "slug": "what-ai-believes",
        "he_base": "what-ai-believes-he",
        "en_base": "what-ai-believes-en",
        "he_title": "מה הבינה המלאכותית מאמינה",
        "en_title": "What AI Believes",
        "description": "AI section / what AI believes",
    },
    {
        "slug": "when-i-am-also-you",
        "he_base": "when-i-am-also-you-he",
        "en_base": "when-i-am-also-you-en",
        "he_title": "כשאני גם אתה",
        "en_title": "When I Am Also You",
        "description": "AI section / when I am also you",
    },
]

FORMATS = ["md", "html", "txt", "docx", "pdf"]

def run(cmd, *, cwd=None):
    return subprocess.run(cmd, cwd=cwd or ROOT, text=True, capture_output=True)

def which(name):
    return shutil.which(name) is not None

def ensure():
    if not SITE.exists() or not AI_DIR.exists():
        raise SystemExit("ERROR: run this from the project root containing site/files/ai-believes")

def read_text(path):
    return path.read_text(encoding="utf-8", errors="ignore")

def write_text(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

def strip_html_to_text(content):
    content = re.sub(r"<script\b.*?</script>", "", content, flags=re.S|re.I)
    content = re.sub(r"<style\b.*?</style>", "", content, flags=re.S|re.I)
    content = re.sub(r"</(p|div|section|article|h[1-6]|li|tr)>", "\n", content, flags=re.I)
    content = re.sub(r"<br\s*/?>", "\n", content, flags=re.I)
    content = re.sub(r"<[^>]+>", "", content)
    content = html.unescape(content)
    content = re.sub(r"\n{3,}", "\n\n", content)
    return content.strip() + "\n"

def md_to_text(content):
    content = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", content)
    content = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", content)
    content = re.sub(r"^\s{0,3}#{1,6}\s*", "", content, flags=re.M)
    content = re.sub(r"[*_`>#-]{1,3}", "", content)
    content = re.sub(r"\n{3,}", "\n\n", content)
    return content.strip() + "\n"

def source_text_for_base(base):
    for ext in ["md", "html", "txt"]:
        p = AI_DIR / f"{base}.{ext}"
        if p.exists():
            c = read_text(p)
            if ext == "html":
                return strip_html_to_text(c), ext
            if ext == "md":
                return c, ext
            return c, ext
    return None, None

def source_markdown_for_base(base):
    md = AI_DIR / f"{base}.md"
    if md.exists():
        return read_text(md), "md"
    htmlp = AI_DIR / f"{base}.html"
    if htmlp.exists():
        return html_to_markdown(read_text(htmlp)), "html"
    txt = AI_DIR / f"{base}.txt"
    if txt.exists():
        return read_text(txt), "txt"
    return None, None

def html_to_markdown(content):
    # Minimal lossless-ish conversion for existing HTML if no .md source exists.
    content = re.sub(r"<h1[^>]*>(.*?)</h1>", lambda m: "# " + strip_html_to_text(m.group(1)).strip() + "\n\n", content, flags=re.S|re.I)
    content = re.sub(r"<h2[^>]*>(.*?)</h2>", lambda m: "## " + strip_html_to_text(m.group(1)).strip() + "\n\n", content, flags=re.S|re.I)
    content = re.sub(r"<h3[^>]*>(.*?)</h3>", lambda m: "### " + strip_html_to_text(m.group(1)).strip() + "\n\n", content, flags=re.S|re.I)
    content = re.sub(r"<p[^>]*>(.*?)</p>", lambda m: strip_html_to_text(m.group(1)).strip() + "\n\n", content, flags=re.S|re.I)
    return strip_html_to_text(content)

def split_markdown_chunks(text, max_chars=9000):
    # Split by paragraphs/headings, preserving order.
    parts = re.split(r"(\n\s*\n)", text)
    chunks = []
    cur = ""
    for part in parts:
        if len(cur) + len(part) > max_chars and cur.strip():
            chunks.append(cur.strip())
            cur = part
        else:
            cur += part
    if cur.strip():
        chunks.append(cur.strip())
    return chunks

def openai_translate_chunk(chunk, source_lang, target_lang, model):
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is missing")

    system = (
        "You are a careful literary and philosophical translator. "
        "Translate faithfully, preserve meaning, structure, headings, markdown, lists, emphasis, and proper nouns. "
        "Do not summarize. Do not add commentary. Return only the translated text."
    )
    user = f"Translate from {source_lang} to {target_lang}. Preserve Markdown exactly where possible.\n\n{chunk}"

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ],
        "temperature": 0.2
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            out = json.loads(resp.read().decode("utf-8"))
        return out["choices"][0]["message"]["content"].strip()
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"OpenAI HTTP {e.code}: {body[:1200]}")

def translate_markdown(source_md, source_lang, target_lang, model, sleep_sec=0.25):
    chunks = split_markdown_chunks(source_md)
    out = []
    for i, ch in enumerate(chunks, 1):
        print(f"Translating chunk {i}/{len(chunks)}: {source_lang} -> {target_lang}")
        out.append(openai_translate_chunk(ch, source_lang, target_lang, model))
        if sleep_sec:
            time.sleep(sleep_sec)
    return "\n\n".join(out).strip() + "\n"

def make_html_from_md(md_text, title, lang):
    direction = "rtl" if lang == "he" else "ltr"
    # Lightweight markdown -> HTML, enough for document pages.
    lines = md_text.splitlines()
    body = []
    in_para = []
    def flush_para():
        nonlocal in_para
        if in_para:
            body.append("<p>" + html.escape(" ".join(in_para)).replace("&lt;br/&gt;", "<br/>") + "</p>")
            in_para = []
    for line in lines:
        s = line.rstrip()
        if not s:
            flush_para()
            continue
        if s.startswith("# "):
            flush_para()
            body.append(f"<h1>{html.escape(s[2:].strip())}</h1>")
        elif s.startswith("## "):
            flush_para()
            body.append(f"<h2>{html.escape(s[3:].strip())}</h2>")
        elif s.startswith("### "):
            flush_para()
            body.append(f"<h3>{html.escape(s[4:].strip())}</h3>")
        else:
            in_para.append(s)
    flush_para()
    return f"""<!doctype html>
<html lang="{lang}" dir="{direction}">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{html.escape(title)}</title>
<style>
:root{{--paper:#fffaf0;--ink:#17202d;--muted:#637084;--gold:#a97835;}}
body{{margin:0;background:#f7efe1;color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif;line-height:1.75;}}
main{{width:min(860px,calc(100% - 36px));margin:28px auto 72px;background:var(--paper);padding:48px 56px;border-inline-start:8px solid var(--gold);box-shadow:0 16px 44px rgba(23,32,45,.08);}}
h1,h2,h3{{line-height:1.2;color:#0b1d31;}}
h1{{font-size:clamp(2rem,4vw,3.7rem);}}
h2{{font-size:1.75rem;margin-top:2.1em;color:var(--gold);}}
p{{font-size:1.04rem;}}
@media(max-width:700px){{main{{padding:30px 24px;}}}}
@media print{{body{{background:white}}main{{width:auto;margin:0;box-shadow:none;}}}}
</style>
</head>
<body>
<main>
{"".join(body)}
</main>
</body>
</html>
"""

def ensure_md(base, lang, title, report, translate_missing, model):
    md_path = AI_DIR / f"{base}.md"
    if md_path.exists():
        return True
    # Try same-language txt/html.
    src_md, src_ext = source_markdown_for_base(base)
    if src_md:
        write_text(md_path, src_md)
        report.append(f"- created `{md_path.relative_to(ROOT)}` from existing `{src_ext}`")
        return True

    # Try translation from counterpart.
    if not translate_missing:
        report.append(f"- missing `{md_path.relative_to(ROOT)}` — translation required, skipped in audit/no-translate mode")
        return False

    counterpart = base[:-3] + ("-en" if base.endswith("-he") else "-he")
    source, source_kind = source_markdown_for_base(counterpart)
    if not source:
        report.append(f"- missing `{md_path.relative_to(ROOT)}` — no source counterpart found")
        return False
    source_lang = "Hebrew" if counterpart.endswith("-he") else "English"
    target_lang = "English" if base.endswith("-en") else "Hebrew"
    translated = translate_markdown(source, source_lang, target_lang, model)
    write_text(md_path, translated)
    report.append(f"- created translated `{md_path.relative_to(ROOT)}` from `{counterpart}.{source_kind}`")
    return True

def ensure_txt(base, report):
    txt = AI_DIR / f"{base}.txt"
    if txt.exists():
        return True
    md = AI_DIR / f"{base}.md"
    htmlp = AI_DIR / f"{base}.html"
    if md.exists():
        write_text(txt, md_to_text(read_text(md)))
        report.append(f"- created `{txt.relative_to(ROOT)}` from Markdown")
        return True
    if htmlp.exists():
        write_text(txt, strip_html_to_text(read_text(htmlp)))
        report.append(f"- created `{txt.relative_to(ROOT)}` from HTML")
        return True
    report.append(f"- missing `{txt.relative_to(ROOT)}` — no source found")
    return False

def ensure_html(base, lang, title, report):
    htmlp = AI_DIR / f"{base}.html"
    if htmlp.exists():
        return True
    md = AI_DIR / f"{base}.md"
    if md.exists():
        write_text(htmlp, make_html_from_md(read_text(md), title, lang))
        report.append(f"- created `{htmlp.relative_to(ROOT)}` from Markdown")
        return True
    report.append(f"- missing `{htmlp.relative_to(ROOT)}` — no Markdown source found")
    return False

def ensure_docx(base, report):
    docx = AI_DIR / f"{base}.docx"
    if docx.exists():
        return True
    md = AI_DIR / f"{base}.md"
    if not md.exists():
        report.append(f"- missing `{docx.relative_to(ROOT)}` — no Markdown source found")
        return False
    if which("pandoc"):
        r = run(["pandoc", str(md), "-o", str(docx), "--standalone"])
        if r.returncode == 0 and docx.exists():
            report.append(f"- created `{docx.relative_to(ROOT)}` with pandoc")
            return True
        report.append(f"- failed DOCX `{docx.relative_to(ROOT)}` with pandoc: {r.stderr[:500]}")
        return False
    report.append(f"- missing `{docx.relative_to(ROOT)}` — pandoc not installed")
    return False

def ensure_pdf(base, report):
    pdf = AI_DIR / f"{base}.pdf"
    if pdf.exists():
        return True
    htmlp = AI_DIR / f"{base}.html"
    md = AI_DIR / f"{base}.md"
    if not htmlp.exists() and md.exists():
        # HTML should be created before this, but keep safe.
        pass
    if htmlp.exists() and which("weasyprint"):
        r = run(["weasyprint", str(htmlp), str(pdf)])
        if r.returncode == 0 and pdf.exists():
            report.append(f"- created `{pdf.relative_to(ROOT)}` with weasyprint")
            return True
        report.append(f"- failed PDF `{pdf.relative_to(ROOT)}` with weasyprint: {r.stderr[:500]}")
        return False
    if md.exists() and which("pandoc"):
        r = run(["pandoc", str(md), "-o", str(pdf)])
        if r.returncode == 0 and pdf.exists():
            report.append(f"- created `{pdf.relative_to(ROOT)}` with pandoc")
            return True
        report.append(f"- failed PDF `{pdf.relative_to(ROOT)}` with pandoc: {r.stderr[:500]}")
        return False
    report.append(f"- missing `{pdf.relative_to(ROOT)}` — need weasyprint or pandoc")
    return False

def file_size_label(path):
    try:
        n = path.stat().st_size
    except FileNotFoundError:
        return ""
    if n < 1024:
        return f"{n} B"
    if n < 1024*1024:
        return f"{n/1024:.1f} KB"
    return f"{n/(1024*1024):.1f} MB"

def update_files_pages(report):
    # Add missing rows to files pages download tables. Conservative: insert rows before </table> if filename absent.
    pages = [
        SITE / "pages" / "en" / "files-en.html",
        SITE / "pages" / "he" / "files.html",
    ]
    format_names = {
        "html": "HTML",
        "pdf": "PDF",
        "docx": "Word",
        "md": "Markdown",
        "txt": "Text",
    }
    lang_labels = {"he": "עברית", "en": "English"}
    added_total = 0
    for page in pages:
        if not page.exists():
            continue
        text = read_text(page)
        rows = []
        for doc in AI_DOCS:
            for lang, base in [("he", doc["he_base"]), ("en", doc["en_base"])]:
                for ext in FORMATS:
                    fp = AI_DIR / f"{base}.{ext}"
                    if not fp.exists():
                        continue
                    filename = fp.name
                    if filename in text:
                        continue
                    rel = Path(os.path.relpath(fp, page.parent)).as_posix()
                    row = (
                        f'<tr><td><a href="{rel}" rel="noopener noreferrer" target="_blank">{filename}</a></td>'
                        f'<td>{format_names[ext]}</td><td>{lang_labels[lang]}</td><td>{file_size_label(fp)}</td>'
                        f'<td>{html.escape(doc["description"])}</td></tr>'
                    )
                    rows.append(row)
        if rows and "</table>" in text:
            text = text.replace("</table>", "".join(rows) + "</table>", 1)
            write_text(page, text)
            added_total += len(rows)
            report.append(f"- updated `{page.relative_to(ROOT)}` with {len(rows)} AI file rows")
    if added_total == 0:
        report.append("- files pages already contained all generated AI file rows, or no files page table was found")

def audit_current(report):
    report.append("## Current AI file matrix")
    for doc in AI_DOCS:
        report.append(f"### {doc['slug']}")
        for lang, base in [("he", doc["he_base"]), ("en", doc["en_base"])]:
            cells = []
            for ext in FORMATS:
                p = AI_DIR / f"{base}.{ext}"
                cells.append(f"{ext}:{'yes' if p.exists() else 'NO'}")
            report.append(f"- {base}: " + ", ".join(cells))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="write generated files")
    parser.add_argument("--translate", action="store_true", help="translate missing Hebrew/English counterparts using OPENAI_API_KEY")
    parser.add_argument("--model", default=os.environ.get("OPENAI_TRANSLATION_MODEL", "gpt-4o-mini"), help="OpenAI model for translation")
    parser.add_argument("--update-file-pages", action="store_true", help="add generated files to files pages")
    args = parser.parse_args()

    global APPLY
    APPLY = args.apply

    ensure()
    report = []
    report.append("# BPI V82 — השלמת קבצי AI בכל הפורמטים והשפות")
    report.append("")
    report.append(f"Mode: {'APPLY' if args.apply else 'AUDIT ONLY'}")
    report.append(f"Translate missing language counterparts: {'yes' if args.translate else 'no'}")
    report.append("")
    audit_current(report)
    report.append("")
    report.append("## Actions")

    if not args.apply:
        report.append("- audit only: no files were written")
    else:
        for doc in AI_DOCS:
            for lang, base, title in [
                ("he", doc["he_base"], doc["he_title"]),
                ("en", doc["en_base"], doc["en_title"]),
            ]:
                ensure_md(base, lang, title, report, args.translate, args.model)
                ensure_txt(base, report)
                ensure_html(base, lang, title, report)
                ensure_docx(base, report)
                ensure_pdf(base, report)
        if args.update_file_pages:
            update_files_pages(report)
    report.append("")
    report.append("## Notes")
    report.append("- The script does not create fake English translations. Missing language counterparts are translated only when `--translate` is passed and `OPENAI_API_KEY` exists.")
    report.append("- DOCX generation requires `pandoc`.")
    report.append("- PDF generation requires `weasyprint` or `pandoc` PDF support.")
    report.append("- Existing files are preserved; the script fills missing files only.")

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    write_text(REPORT, "\n".join(report) + "\n")
    print("\n".join(report))
    print("")
    print("Report:", REPORT)

if __name__ == "__main__":
    main()
