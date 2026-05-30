from pathlib import Path
from html import escape, unescape
import re

EN_HTML = Path("site/files/appendices/stories-before-thought-english.html")
HE_HTML = Path("site/files/appendices/stories-before-thought-hebrew-rtl.html")
EN_MD = Path("site/files/appendices/stories-before-thought-english.md")
EN_TXT = Path("site/files/appendices/stories-before-thought-english.txt")

TRANS = {
    "shalosh-sheelot-iska-bankait": Path("site/files/appendices/shalosh_sheelot_iska_bankait_full_story_en.txt"),
    "haemet-hamavchila-eifo-hatzlalim": Path("site/files/appendices/haemet_hamavchila_eifo_hatzlalim_full_story_en.txt"),
}

STORY_META = {
    "story-1": {
        "title": "How Truth Remains Honest",
        "subtitle": "Check Yourself First",
    },
    "story-2": {
        "title": "True, But Not Just",
        "subtitle": "The Air Seller",
    },
    "story-3": {
        "title": "Red Causes Dread",
        "subtitle": "Nothing Is Unimportant",
    },
    "story-4": {
        "title": "Quantum Intelligence",
        "subtitle": "Who loves being wrong?",
    },
    "story-5": {
        "title": "A Place at the End of the Road",
        "subtitle": "",
    },
    "story-6": {
        "title": "Super Mirrors",
        "subtitle": "",
    },
    "story-7": {
        "title": "Self Confidence",
        "subtitle": "",
    },
    "story-8": {
        "title": "Serial Healer",
        "subtitle": "",
    },
    "story-9": {
        "title": "Maxideal",
        "subtitle": "",
    },
    "story-10": {
        "title": "To Speak with Consciousness",
        "subtitle": "",
    },
    "story-11": {
        "title": "Heretic from Abroad",
        "subtitle": "",
    },
    "story-12": {
        "title": "Puzzle",
        "subtitle": "",
    },
    "story-13": {
        "title": "To Fear Intruders, or Talk to Computers",
        "subtitle": "",
    },
    "story-14": {
        "title": "A Few Strings and a Knot",
        "subtitle": "",
    },
    "shalosh-sheelot-iska-bankait": {
        "title": "Three Queries",
        "subtitle": "A Banking Deal",
    },
    "haemet-hamavchila-eifo-hatzlalim": {
        "title": "The Nauseating Truth",
        "subtitle": "Where Are the Shadows",
    },
}

KNOWN_ORDER = [
    "story-1",
    "story-2",
    "story-3",
    "story-4",
    "story-5",
    "story-6",
    "story-7",
    "story-8",
    "story-9",
    "story-10",
    "story-11",
    "story-12",
    "story-13",
    "story-14",
    "shalosh-sheelot-iska-bankait",
    "haemet-hamavchila-eifo-hatzlalim",
]

VISIBLE_TRANSLATIONS = {
    "בדוק את עצמך קודם": "Check Yourself First",
    "על שום מה": "For What Reason",
    "שום דבר אינו לא חשוב": "Nothing Is Unimportant",
}

FINAL_CSS_ID = "bpi-english-appendix-final-layout-v16"

FINAL_CSS = f"""
<style id="{FINAL_CSS_ID}">
html,
html body {{
  direction:ltr!important;
  text-align:left!important;
}}

body {{
  background:#f7efe1!important;
}}

main.page {{
  width:min(920px, calc(100% - 36px))!important;
  max-width:920px!important;
  margin:28px auto!important;
  padding:56px 64px!important;
  background:#fffaf0!important;
  direction:ltr!important;
  text-align:left!important;
  border-left:8px solid #c5791d!important;
  border-right:0!important;
}}

.cover,
.cover *,
.image-frame,
.image-frame *,
figure,
figcaption {{
  text-align:center!important;
}}

.story-toc-page {{
  direction:ltr!important;
  text-align:left!important;
  margin:56px 0 72px!important;
  padding:0!important;
}}

.story-toc-page h2 {{
  direction:ltr!important;
  text-align:left!important;
  color:#0A3A68!important;
}}

.story-toc-page ol {{
  columns:1!important;
  padding-left:1.35rem!important;
  padding-right:0!important;
  margin-left:0!important;
  margin-right:auto!important;
}}

.story-toc-page li {{
  direction:ltr!important;
  text-align:left!important;
  margin:.55rem 0!important;
  break-inside:avoid!important;
}}

.story-toc-row,
.story-toc-row *,
.story-toc-entry,
.story-toc-entry * {{
  direction:ltr!important;
  text-align:left!important;
  unicode-bidi:plaintext!important;
}}

.story {{
  direction:ltr!important;
  text-align:left!important;
  break-before:auto!important;
  page-break-before:auto!important;
  break-after:auto!important;
  page-break-after:auto!important;
  margin:64px 0 0!important;
  padding:42px 0 0!important;
  border-top:1px solid rgba(10,58,104,.14)!important;
}}

.story:first-of-type {{
  border-top:0!important;
}}

.story-head,
.story-head *,
.story h1,
.story h2,
.story h3,
.story h4,
.story p,
.story li,
.story blockquote,
.story-subtitle,
.back-to-toc,
.back-to-toc * {{
  direction:ltr!important;
  text-align:left!important;
  unicode-bidi:plaintext!important;
  margin-left:0!important;
  margin-right:auto!important;
}}

.story h2 {{
  color:#0A3A68!important;
  font-size:clamp(2rem,4.5vw,3.15rem)!important;
  line-height:1.12!important;
  margin-top:0!important;
  margin-bottom:.45em!important;
}}

.story-subtitle {{
  color:#253244!important;
  font-size:clamp(1.15rem,2.3vw,1.55rem)!important;
  font-weight:800!important;
  font-style:italic!important;
  margin-top:0!important;
  margin-bottom:1.35rem!important;
}}

.story p {{
  color:#253244!important;
  font-size:1.08rem!important;
  line-height:1.75!important;
}}

.back-to-toc {{
  margin-top:28px!important;
}}

@media print {{
  .story {{
    break-before:page!important;
    page-break-before:always!important;
  }}
}}
</style>
"""

def clean_visible(html: str) -> str:
    html = re.sub(r"<style\b[^>]*>.*?</style>", " ", html, flags=re.I | re.S)
    html = re.sub(r"<script\b[^>]*>.*?</script>", " ", html, flags=re.I | re.S)
    html = re.sub(r"<[^>]+>", " ", html)
    return re.sub(r"\s+", " ", unescape(html)).strip()

def get_hebrew_order() -> list[str]:
    he = HE_HTML.read_text(encoding="utf-8", errors="ignore")

    found = []
    for m in re.finditer(r'<section\b[^>]*\bid=["\']([^"\']+)["\']', he, flags=re.I):
        sid = m.group(1)
        if sid in STORY_META and sid not in found:
            found.append(sid)

    for sid in KNOWN_ORDER:
        if sid not in found:
            found.append(sid)

    return found

def section_pattern(sid: str):
    return re.compile(
        r'<section\b(?=[^>]*\bid=["\']' + re.escape(sid) + r'["\'])[^>]*>.*?</section>',
        flags=re.I | re.S,
    )

def strip_inline_layout_attrs(section: str) -> str:
    section = re.sub(r'\sdir=["\']rtl["\']', ' dir="ltr"', section, flags=re.I)
    section = re.sub(r'\sdir=["\']ltr["\']', ' dir="ltr"', section, flags=re.I)
    section = section.replace("hebrew-rtl-force", "english-ltr-force")

    # Remove inline style attributes inside story sections; final CSS owns layout.
    section = re.sub(r'\sstyle=["\'][^"\']*["\']', "", section, flags=re.I | re.S)

    for old, new in VISIBLE_TRANSLATIONS.items():
        section = section.replace(old, new)

    return section

def update_heading_and_subtitle(section: str, sid: str) -> str:
    meta = STORY_META[sid]
    title = meta["title"]
    subtitle = meta.get("subtitle", "")

    # Replace first h2/h1 in the section.
    if re.search(r"<h[1-3]\b[^>]*>.*?</h[1-3]>", section, flags=re.I | re.S):
        section = re.sub(
            r"<h[1-3]\b[^>]*>.*?</h[1-3]>",
            f'<h2 class="english-ltr-force">{escape(title)}</h2>',
            section,
            count=1,
            flags=re.I | re.S,
        )
    else:
        section = section.replace(">", f'><h2 class="english-ltr-force">{escape(title)}</h2>', 1)

    # Normalize subtitle if we have one.
    if subtitle:
        if re.search(r'<p\b[^>]*class=["\'][^"\']*story-subtitle[^"\']*["\'][^>]*>.*?</p>', section, flags=re.I | re.S):
            section = re.sub(
                r'<p\b[^>]*class=["\'][^"\']*story-subtitle[^"\']*["\'][^>]*>.*?</p>',
                f'<p class="story-subtitle english-ltr-force">{escape(subtitle)}</p>',
                section,
                count=1,
                flags=re.I | re.S,
            )
        else:
            section = re.sub(
                r'(</h2>)',
                r'\1' + f'\n<p class="story-subtitle english-ltr-force">{escape(subtitle)}</p>',
                section,
                count=1,
                flags=re.I,
            )

    # Normalize back to toc.
    if "Back to table of contents" not in section:
        section = section.replace(
            "</section>",
            '<p class="back-to-toc"><a href="#table-of-contents">Back to table of contents</a></p>\n</section>',
        )
    else:
        section = re.sub(
            r'<p\b[^>]*class=["\'][^"\']*back-to-toc[^"\']*["\'][^>]*>.*?</p>',
            '<p class="back-to-toc"><a href="#table-of-contents">Back to table of contents</a></p>',
            section,
            flags=re.I | re.S,
        )

    return section

def read_translation_file(sid: str) -> str:
    path = TRANS.get(sid)
    if not path or not path.exists():
        raise SystemExit(f"Missing translation file for {sid}: {path}")

    text = path.read_text(encoding="utf-8", errors="ignore").strip()
    meta = STORY_META[sid]

    # Remove duplicate title/subtitle at top if present.
    text = re.sub(r"^\s*" + re.escape(meta["title"]) + r"\s*", "", text, flags=re.I)
    if meta.get("subtitle"):
        text = re.sub(r"^\s*" + re.escape(meta["subtitle"]) + r"\s*", "", text, flags=re.I)

    return text.strip()

def first_image_from_hebrew(sid: str) -> tuple[str, str]:
    he = HE_HTML.read_text(encoding="utf-8", errors="ignore")
    m = section_pattern(sid).search(he)
    if not m:
        return "", ""

    sec = m.group(0)
    img = re.search(r'<img\b[^>]*src=["\']([^"\']+)["\'][^>]*>', sec, flags=re.I | re.S)
    if not img:
        return "", ""

    src = img.group(1)
    alt_m = re.search(r'\balt=["\']([^"\']*)["\']', img.group(0), flags=re.I | re.S)
    alt = alt_m.group(1) if alt_m else STORY_META[sid]["title"]
    return src, alt

def make_section(sid: str) -> str:
    meta = STORY_META[sid]
    body = read_translation_file(sid)
    src, alt = first_image_from_hebrew(sid)

    out = []
    out.append(f'<section class="story files-appendix-story" id="{sid}">')
    out.append('<header class="story-head">')
    out.append(f'<h2 class="english-ltr-force">{escape(meta["title"])}</h2>')
    if meta.get("subtitle"):
        out.append(f'<p class="story-subtitle english-ltr-force">{escape(meta["subtitle"])}</p>')
    out.append('</header>')

    if src:
        out.append('<figure class="image-frame">')
        out.append(f'<img alt="{escape(alt)}" decoding="async" loading="lazy" src="{escape(src)}"/>')
        out.append(f'<figcaption>{escape(alt)}</figcaption>')
        out.append('</figure>')

    for block in re.split(r"\n\s*\n", body):
        block = block.strip()
        if not block:
            continue
        out.append(f'<p>{escape(block)}</p>')

    out.append('<p class="back-to-toc"><a href="#table-of-contents">Back to table of contents</a></p>')
    out.append('</section>')
    return "\n".join(out)

def build_toc(order: list[str]) -> str:
    out = []
    out.append('<section class="story-toc-page" id="table-of-contents">')
    out.append('<h2>Table of Contents</h2>')
    out.append('<ol>')
    for sid in order:
        meta = STORY_META[sid]
        title = meta["title"]
        subtitle = meta.get("subtitle", "")
        label = f"{title} — {subtitle}" if subtitle else title
        out.append(f'<li class="story-toc-row"><a class="story-toc-entry" href="#{sid}">{escape(label)}</a></li>')
    out.append('</ol>')
    out.append('</section>')
    return "\n".join(out)

def remove_old_final_css(s: str) -> str:
    for css_id in [
        FINAL_CSS_ID,
        "bpi-final-stories-english-layout-cleanup",
        "bpi-final-stories-english-ltr-fix",
    ]:
        s = re.sub(
            r'<style id=["\']' + re.escape(css_id) + r'["\']>.*?</style>',
            "",
            s,
            flags=re.I | re.S,
        )
    return s

def patch_html():
    if not EN_HTML.exists():
        raise SystemExit(f"Missing {EN_HTML}")

    s = EN_HTML.read_text(encoding="utf-8", errors="ignore")
    order = get_hebrew_order()

    s = re.sub(r"<html\b[^>]*>", '<html dir="ltr" lang="en">', s, count=1, flags=re.I | re.S)

    for old, new in VISIBLE_TRANSLATIONS.items():
        s = s.replace(old, new)

    s = s.replace("hebrew-rtl-force", "english-ltr-force")

    s = remove_old_final_css(s)

    # Extract or create all story sections.
    sections = {}
    for sid in order:
        m = section_pattern(sid).search(s)
        if m:
            sec = m.group(0)
            sec = strip_inline_layout_attrs(sec)
            sec = update_heading_and_subtitle(sec, sid)
            sections[sid] = sec
        else:
            sections[sid] = make_section(sid)

    # Remove all existing story sections from the file.
    for sid in order:
        s = section_pattern(sid).sub("", s)

    # Remove old TOC section.
    s = re.sub(
        r'<section\b[^>]*(?:id=["\']table-of-contents["\']|class=["\'][^"\']*story-toc-page[^"\']*["\'])[^>]*>.*?</section>',
        "",
        s,
        count=1,
        flags=re.I | re.S,
    )

    toc = build_toc(order)
    story_html = "\n\n".join(sections[sid] for sid in order)

    # Insert TOC + stories after cover if possible.
    cover_m = re.search(r'<section\b[^>]*class=["\'][^"\']*cover[^"\']*["\'][^>]*>.*?</section>', s, flags=re.I | re.S)
    if cover_m:
        insert_at = cover_m.end()
        s = s[:insert_at] + "\n\n" + toc + "\n\n" + story_html + "\n" + s[insert_at:]
    else:
        body_m = re.search(r"<main\b[^>]*>", s, flags=re.I | re.S)
        if body_m:
            insert_at = body_m.end()
            s = s[:insert_at] + "\n\n" + toc + "\n\n" + story_html + "\n" + s[insert_at:]
        else:
            s += "\n\n" + toc + "\n\n" + story_html

    if "</head>" in s:
        s = s.replace("</head>", FINAL_CSS + "\n</head>", 1)
    else:
        s = FINAL_CSS + "\n" + s

    EN_HTML.write_text(s, encoding="utf-8")
    print("patched:", EN_HTML)
    print("order:", " -> ".join(order))

def append_missing_to_md_txt():
    # Do not rebuild; only ensure the two new stories exist in MD/TXT.
    for sid in ["shalosh-sheelot-iska-bankait", "haemet-hamavchila-eifo-hatzlalim"]:
        meta = STORY_META[sid]
        body = read_translation_file(sid)

        if EN_MD.exists():
            s = EN_MD.read_text(encoding="utf-8", errors="ignore")
            if meta["title"] not in s:
                block = f'\n\n<a id="{sid}"></a>\n\n## {meta["title"]}\n\n'
                if meta.get("subtitle"):
                    block += f'*{meta["subtitle"]}*\n\n'
                block += body + "\n"
                EN_MD.write_text(s.rstrip() + block, encoding="utf-8")
                print("patched:", EN_MD)

        if EN_TXT.exists():
            s = EN_TXT.read_text(encoding="utf-8", errors="ignore")
            if meta["title"] not in s:
                block = f'\n\n{meta["title"]}\n'
                if meta.get("subtitle"):
                    block += meta["subtitle"] + "\n"
                block += "\n" + body + "\n"
                EN_TXT.write_text(s.rstrip() + block, encoding="utf-8")
                print("patched:", EN_TXT)

def audit():
    s = EN_HTML.read_text(encoding="utf-8", errors="ignore")
    order = get_hebrew_order()

    missing = []
    for sid in order:
        meta = STORY_META[sid]
        if f'id="{sid}"' not in s:
            missing.append(f"missing body {sid}")
        if f'href="#{sid}"' not in s:
            missing.append(f"missing toc {sid}")
        if meta["title"] not in s:
            missing.append(f"missing title {meta['title']}")

    visible = re.sub(r"<style\b[^>]*>.*?</style>", " ", s, flags=re.I | re.S)
    visible = re.sub(r"<script\b[^>]*>.*?</script>", " ", visible, flags=re.I | re.S)
    visible = re.sub(r"<[^>]+>", " ", visible)
    visible = re.sub(r"\s+", " ", unescape(visible)).strip()
    hebrew = re.findall(r"[\u0590-\u05FF][\u0590-\u05FF\s,.:;!?״׳־-]{0,120}", visible)
    if hebrew:
        missing.append("visible Hebrew left: " + " | ".join(sorted(set(x.strip() for x in hebrew))[:20]))

    if missing:
        print("\nAUDIT FAILED:")
        for x in missing:
            print("-", x)
        raise SystemExit(1)

    print("AUDIT OK: 16 English stories, TOC entries, titles, and no visible Hebrew.")

def main():
    patch_html()
    append_missing_to_md_txt()
    audit()

if __name__ == "__main__":
    main()
