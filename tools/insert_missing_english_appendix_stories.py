#!/usr/bin/env python3
from pathlib import Path
from html import escape, unescape
import re

ROOT = Path.cwd()
APP = ROOT / "site/files/appendices"

EN_HTML = APP / "stories-before-thought-english.html"
EN_MD = APP / "stories-before-thought-english.md"
EN_TXT = APP / "stories-before-thought-english.txt"
HE_HTML = APP / "stories-before-thought-hebrew-rtl.html"

ALIGN_MARKER = "BPI_FINAL_STORIES_ENGLISH_LTR_FIX_20260530"

STORIES = [
    {
        "id": "shalosh-sheelot-iska-bankait",
        "title": "Three Queries",
        "subtitle": "A Banking Deal",
        "source": APP / "shalosh_sheelot_iska_bankait_full_story_en.txt",
        "fallback_img": "../../figures/appendix-stories/shalosh_sheelot_iska_bankait.png",
        "fallback_alt": "Illustration for Three Queries — a poor fisherman facing a glowing ATM by the sea at night",
    },
    {
        "id": "haemet-hamavchila-eifo-hatzlalim",
        "title": "The Nauseating Truth",
        "subtitle": "Where Are the Shadows",
        "source": APP / "haemet_hamavchila_eifo_hatzlalim_full_story_en.txt",
        "fallback_img": "../../figures/appendix-stories/haemet_hamavchila_eifo_hatzlalim.png",
        "fallback_alt": "Illustration for The Nauseating Truth — a train station, a missing shadow, and a hovering many-mouthed creature",
    },
]

FINAL_CSS = f"""
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

VISIBLE_TRANSLATIONS = {
    "בדוק את עצמך קודם": "Check yourself first",
    "על שום מה": "For what reason",
    "שום דבר אינו לא חשוב": "Nothing is unimportant",
}

def read(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="ignore") if p.exists() else ""

def write_if_changed(p: Path, s: str):
    old = read(p)
    if s != old:
        p.write_text(s, encoding="utf-8")
        print("patched:", p)
    else:
        print("no change:", p)

def strip_tags(x: str) -> str:
    x = re.sub(r"<style\b[^>]*>.*?</style>", " ", x, flags=re.I | re.S)
    x = re.sub(r"<script\b[^>]*>.*?</script>", " ", x, flags=re.I | re.S)
    x = re.sub(r"<[^>]+>", " ", x)
    return re.sub(r"\s+", " ", unescape(x)).strip()

def split_body(story_text: str, title: str, subtitle: str):
    blocks = [b.strip() for b in re.split(r"\n\s*\n", story_text.strip()) if b.strip()]
    # Drop duplicated title/subtitle from the source file.
    if blocks and blocks[0].strip().lower() == title.lower():
        blocks = blocks[1:]
    if blocks and blocks[0].strip().lower() == subtitle.lower():
        blocks = blocks[1:]
    return blocks

def find_section(html: str, sid: str) -> str:
    id_pos = html.find(f'id="{sid}"')
    if id_pos == -1:
        id_pos = html.find(f"id='{sid}'")
    if id_pos == -1:
        return ""
    start = html.rfind("<section", 0, id_pos)
    if start == -1:
        return ""
    end = html.find("</section>", id_pos)
    if end == -1:
        return ""
    return html[start:end + len("</section>")]

def extract_figure_from_hebrew(st):
    he = read(HE_HTML)
    sec = find_section(he, st["id"])
    if not sec:
        return st["fallback_img"], st["fallback_alt"]

    fig = re.search(r"<figure\b[^>]*>.*?</figure>", sec, flags=re.I | re.S)
    if not fig:
        return st["fallback_img"], st["fallback_alt"]

    src = re.search(r'src=["\']([^"\']+)["\']', fig.group(0), flags=re.I)
    alt = re.search(r'alt=["\']([^"\']*)["\']', fig.group(0), flags=re.I)

    return (
        src.group(1) if src else st["fallback_img"],
        unescape(alt.group(1)) if alt else st["fallback_alt"],
    )

def build_toc_row(st):
    img_src, alt = extract_figure_from_hebrew(st)
    label = f'{st["title"]} — {st["subtitle"]}'
    return (
        f'<p class="story-toc-row" dir="ltr" style="direction:ltr!important;text-align:left!important;">'
        f'<a class="story-toc-entry" href="#{st["id"]}" style="direction:ltr!important;text-align:left!important;display:inline-flex!important;flex-direction:row!important;align-items:center!important;gap:10px!important;">'
        f'<img alt="{escape(alt)}" class="story-toc-thumb" decoding="async" loading="lazy" src="{escape(img_src)}"/>'
        f'<span class="story-toc-title" style="display:block!important;min-width:0!important;color:#08737a!important;font-size:22px!important;line-height:1.25!important;font-weight:700!important;direction:ltr!important;text-align:left!important;white-space:normal!important;">{escape(label)}</span>'
        f'</a></p>'
    )

def build_story_section(st):
    text = read(st["source"])
    if not text.strip():
        raise SystemExit(f"Missing or empty translation file: {st['source']}")

    img_src, alt = extract_figure_from_hebrew(st)
    blocks = split_body(text, st["title"], st["subtitle"])

    out = []
    out.append(f'<section class="page story files-appendix-story" data-v39-story-layout="clean" dir="ltr" id="{st["id"]}" style="direction:ltr!important;text-align:left!important;page-break-before:always;break-before:page;">')
    out.append(f'<header class="story-head" dir="ltr" style="direction:ltr!important;text-align:left!important;">')
    out.append(f'<h2 dir="ltr" style="text-align:left!important;direction:ltr!important;color:#0A3A68!important;font-family:-apple-system,BlinkMacSystemFont,\'Segoe UI\',Arial,sans-serif!important;font-size:clamp(48px,5.8vw,70px)!important;line-height:1.04!important;font-weight:900!important;letter-spacing:-0.035em!important;margin:0 0 18px 0!important;page-break-after:avoid!important;break-after:avoid!important;">{escape(st["title"])}</h2>')
    out.append(f'<p class="story-subtitle" dir="ltr" style="text-align:left!important;direction:ltr!important;unicode-bidi:plaintext!important;margin-left:0!important;margin-right:auto!important;">{escape(st["subtitle"])}</p>')
    out.append('</header>')
    out.append(f'<figure class="image-frame"><img alt="{escape(alt)}" decoding="async" loading="lazy" src="{escape(img_src)}"/><figcaption>{escape(alt)}</figcaption></figure>')

    for b in blocks:
        if not b.strip():
            continue
        # Keep obvious section-like short lines as h3, otherwise paragraphs.
        if len(b) < 85 and "\n" not in b and not b.endswith((".", "?", "!", "”", '"')):
            out.append(f'<h3 dir="ltr" style="direction:ltr!important;text-align:left!important;">{escape(b)}</h3>')
        else:
            out.append(f'<p dir="ltr" style="direction:ltr!important;text-align:left!important;unicode-bidi:plaintext!important;">{escape(b)}</p>')

    out.append('<p class="back-to-toc" dir="ltr" style="text-align:left!important;direction:ltr!important;margin-top:24px;"><a href="#table-of-contents">Back to table of contents</a></p>')
    out.append("</section>")
    return "\n".join(out)

def patch_html():
    if not EN_HTML.exists():
        raise SystemExit(f"Missing English appendix HTML: {EN_HTML}")

    s = read(EN_HTML)
    s = re.sub(r"<html\b[^>]*>", '<html dir="ltr" lang="en">', s, count=1, flags=re.I | re.S)

    for he, en in VISIBLE_TRANSLATIONS.items():
        s = s.replace(he, en)

    # Remove previous final CSS block, then re-add it as the last stylesheet in head.
    s = re.sub(r'<style id="bpi-final-stories-english-ltr-fix">.*?</style>', "", s, flags=re.I | re.S)
    if "</head>" in s:
        s = s.replace("</head>", FINAL_CSS + "\n</head>", 1)
    else:
        s = FINAL_CSS + "\n" + s

    # Add missing TOC rows before the end of the table-of-contents section.
    toc_start = s.find('id="table-of-contents"')
    if toc_start == -1:
        toc_start = s.find("id='table-of-contents'")
    if toc_start == -1:
        raise SystemExit("Could not find table-of-contents section in English HTML")

    toc_end = s.find("</section>", toc_start)
    if toc_end == -1:
        raise SystemExit("Could not find end of table-of-contents section in English HTML")

    rows = []
    for st in STORIES:
        if f'href="#{st["id"]}"' not in s and f"href='#{st['id']}'" not in s:
            rows.append(build_toc_row(st))

    if rows:
        s = s[:toc_end] + "\n" + "\n".join(rows) + "\n" + s[toc_end:]

    # Add missing story bodies before closing main/body.
    sections = []
    for st in STORIES:
        if f'id="{st["id"]}"' not in s and f"id='{st['id']}'" not in s:
            sections.append(build_story_section(st))

    if sections:
        insert_at = s.rfind("</main>")
        if insert_at == -1:
            insert_at = s.rfind("</body>")
        if insert_at == -1:
            s += "\n" + "\n".join(sections) + "\n"
        else:
            s = s[:insert_at] + "\n" + "\n".join(sections) + "\n" + s[insert_at:]

    write_if_changed(EN_HTML, s)

def patch_md():
    if not EN_MD.exists():
        print("skip missing:", EN_MD)
        return

    s = read(EN_MD)

    for st in STORIES:
        text = read(st["source"]).strip()
        body = "\n\n".join(split_body(text, st["title"], st["subtitle"]))

        # Add TOC line if a table exists and entry is missing.
        if st["title"] not in s:
            # Try to add after A Few Strings, otherwise after Table of Contents heading.
            toc_line = f'- [{st["title"]} — {st["subtitle"]}](#{st["id"]})'
            anchor_line = f'<a id="{st["id"]}"></a>\n\n## {st["title"]}\n\n*{st["subtitle"]}*\n\n{body}\n'
            pos = s.find("A Few Strings and a Knot")
            if pos != -1:
                line_end = s.find("\n", pos)
                if line_end != -1:
                    s = s[:line_end+1] + toc_line + "\n" + s[line_end+1:]
            elif "Table of Contents" in s:
                pos = s.find("Table of Contents")
                line_end = s.find("\n", pos)
                s = s[:line_end+1] + "\n" + toc_line + "\n" + s[line_end+1:]
            s = s.rstrip() + "\n\n" + anchor_line

    write_if_changed(EN_MD, s)

def patch_txt():
    if not EN_TXT.exists():
        print("skip missing:", EN_TXT)
        return

    s = read(EN_TXT)

    for st in STORIES:
        text = read(st["source"]).strip()
        blocks = split_body(text, st["title"], st["subtitle"])
        story_block = st["title"] + "\n" + st["subtitle"] + "\n\n" + "\n\n".join(blocks)

        if st["title"] not in s:
            # Add title to top TOC if recognizable.
            pos = s.find("A Few Strings and a Knot")
            if pos != -1:
                line_end = s.find("\n", pos)
                if line_end != -1:
                    s = s[:line_end+1] + st["title"] + "\n" + s[line_end+1:]
            s = s.rstrip() + "\n\n" + story_block + "\n"

    write_if_changed(EN_TXT, s)

def audit():
    s = read(EN_HTML)

    errors = []
    for st in STORIES:
        if f'id="{st["id"]}"' not in s and f"id='{st['id']}'" not in s:
            errors.append(f"missing HTML body: {st['id']}")
        if f'href="#{st["id"]}"' not in s and f"href='#{st['id']}'" not in s:
            errors.append(f"missing HTML TOC: {st['id']}")
        if st["title"] not in s:
            errors.append(f"missing HTML title: {st['title']}")

    visible = re.sub(r"<style\b[^>]*>.*?</style>", " ", s, flags=re.I | re.S)
    visible = re.sub(r"<script\b[^>]*>.*?</script>", " ", visible, flags=re.I | re.S)
    visible = re.sub(r"<[^>]+>", " ", visible)
    visible = re.sub(r"\s+", " ", unescape(visible)).strip()
    hebrew = sorted(set(re.findall(r"[\u0590-\u05FF][\u0590-\u05FF\s,.:;!?״׳־-]{0,120}", visible)))
    if hebrew:
        errors.append("visible Hebrew remains: " + " | ".join(x.strip() for x in hebrew[:20]))

    if errors:
        print("VALIDATION FAILED:")
        for e in errors:
            print(" -", e)
        raise SystemExit(1)

    print("OK: missing English appendix stories inserted and validated.")

def main():
    patch_html()
    patch_md()
    patch_txt()
    audit()

if __name__ == "__main__":
    main()
