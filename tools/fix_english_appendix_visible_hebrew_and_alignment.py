from pathlib import Path
import re
from html import unescape

EN_FILES = [
    Path("site/files/appendices/stories-before-thought-english.html"),
    Path("site/files/appendices/stories-before-thought-english.md"),
    Path("site/files/appendices/stories-before-thought-english.txt"),
]

EN_HTML = Path("site/files/appendices/stories-before-thought-english.html")
HE_HTML = Path("site/files/appendices/stories-before-thought-hebrew-rtl.html")
REPORT_DIR = Path("reports")
REPORT_DIR.mkdir(exist_ok=True)

TRANSLATIONS = {
    "בדוק את עצמך קודם": "Check yourself first",
    "על שום מה": "For what reason",
    "שום דבר אינו לא חשוב": "Nothing is unimportant",
}

ALIGN_MARKER = "BPI_FINAL_STORIES_ENGLISH_LTR_FIX_20260530"

CSS = f"""
<style id="bpi-final-stories-english-ltr-fix">
/* ===== {ALIGN_MARKER} ===== */
html[dir="ltr"],
html[dir="ltr"] body,
html[dir="ltr"] main,
html[dir="ltr"] .page {{
  direction: ltr !important;
  text-align: left !important;
}}

html[dir="ltr"] .story,
html[dir="ltr"] .story *,
html[dir="ltr"] .story-head,
html[dir="ltr"] .story-head *,
html[dir="ltr"] .story-toc-page,
html[dir="ltr"] .story-toc-page *,
html[dir="ltr"] .story-toc-row,
html[dir="ltr"] .story-toc-row *,
html[dir="ltr"] .back-to-toc,
html[dir="ltr"] .back-to-toc * {{
  direction: ltr !important;
  text-align: left !important;
  unicode-bidi: plaintext !important;
  margin-left: 0 !important;
  margin-right: auto !important;
}}

html[dir="ltr"] .cover,
html[dir="ltr"] .cover *,
html[dir="ltr"] figure,
html[dir="ltr"] figcaption,
html[dir="ltr"] .image-frame {{
  text-align: center !important;
}}

html[dir="ltr"] .hebrew-rtl-force {{
  direction: ltr !important;
  text-align: left !important;
}}
/* ===== /{ALIGN_MARKER} ===== */
</style>
"""

def clean_section_html(html: str) -> str:
    html = re.sub(r"<style\b[^>]*>.*?</style>", " ", html, flags=re.I | re.S)
    html = re.sub(r"<script\b[^>]*>.*?</script>", " ", html, flags=re.I | re.S)
    html = re.sub(r"<figure\b[^>]*>.*?</figure>", " ", html, flags=re.I | re.S)
    html = re.sub(r"<[^>]+>", "\n", html)
    html = unescape(html)
    html = re.sub(r"\n\s*\n+", "\n\n", html)
    return html.strip() + "\n"

def extract_section_by_id(html: str, sid: str) -> str:
    id_pos = html.find(f'id="{sid}"')
    if id_pos == -1:
        id_pos = html.find(f"id='{sid}'")
    if id_pos == -1:
        return ""

    section_start = html.rfind("<section", 0, id_pos)
    if section_start == -1:
        section_start = html.rfind("<article", 0, id_pos)

    if section_start == -1:
        return ""

    section_end = html.find("</section>", id_pos)
    if section_end != -1:
        return html[section_start:section_end + len("</section>")]

    article_end = html.find("</article>", id_pos)
    if article_end != -1:
        return html[section_start:article_end + len("</article>")]

    return ""

def patch_english_files():
    for path in EN_FILES:
        if not path.exists():
            print("skip missing:", path)
            continue

        s = path.read_text(encoding="utf-8", errors="ignore")
        original = s

        for he, en in TRANSLATIONS.items():
            s = s.replace(he, en)

        if path.suffix == ".html":
            s = re.sub(r"<html\b[^>]*>", '<html dir="ltr" lang="en">', s, count=1, flags=re.I | re.S)

            s = re.sub(
                r'<style id="bpi-final-stories-english-ltr-fix">.*?</style>',
                "",
                s,
                flags=re.I | re.S,
            )

            if "</head>" in s:
                s = s.replace("</head>", CSS + "\n</head>", 1)
            else:
                s = CSS + "\n" + s

        if s != original:
            path.write_text(s, encoding="utf-8")
            print("patched:", path)

def extract_missing_hebrew_sources():
    if not HE_HTML.exists():
        raise SystemExit(f"missing Hebrew appendix file: {HE_HTML}")

    he = HE_HTML.read_text(encoding="utf-8", errors="ignore")

    for sid in ["shalosh-sheelot-iska-bankait", "haemet-hamavchila-eifo-hatzlalim"]:
        sec = extract_section_by_id(he, sid)
        if not sec:
            raise SystemExit(f"missing Hebrew story section: {sid}")

        out = REPORT_DIR / f"{sid}_hebrew_source_for_translation.txt"
        out.write_text(clean_section_html(sec), encoding="utf-8")
        print("wrote:", out)

def main():
    patch_english_files()
    extract_missing_hebrew_sources()

if __name__ == "__main__":
    main()
