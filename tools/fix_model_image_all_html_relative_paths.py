from pathlib import Path
import os
import re
from html import unescape

ROOT = Path.cwd()
SITE = ROOT / "site"
FILES_ROOT = SITE / "files"
FIGURES = SITE / "figures"

MODEL_IMAGE_NAME = "chapter_model_not_final_declaration_v1.png"
SUMMARY_IMAGE_NAME = "summary-theory-overview-v2.png"

MODEL_TITLES = [
    "זהו מודל, לא הכרזה סופית",
    "This Is a Model, Not a Final Declaration",
]

SUMMARY_TITLES = [
    "תקציר",
    "Abstract",
    "Summary",
]

MODEL_IDS = [
    "זהו-מודל-לא-הכרזה-סופית",
    "This-Is-a-Model-Not-a-Final-Declaration",
    "this-is-a-model-not-a-final-declaration",
]

SUMMARY_IDS = [
    "תקציר",
    "Abstract",
    "abstract",
    "Summary",
    "summary",
]

if not (FIGURES / MODEL_IMAGE_NAME).exists():
    raise SystemExit(f"ERROR: missing image asset: {FIGURES / MODEL_IMAGE_NAME}")

if not (FIGURES / SUMMARY_IMAGE_NAME).exists():
    print(f"WARNING: missing summary image asset: {FIGURES / SUMMARY_IMAGE_NAME}")
    print("Summary/Abstract TOC thumbnails will not be changed.")
    HAS_SUMMARY_IMAGE = False
else:
    HAS_SUMMARY_IMAGE = True

def rel_figure_src(html_file: Path, image_name: str) -> str:
    return os.path.relpath(FIGURES / image_name, html_file.parent).replace(os.sep, "/")

def clean_text(html: str) -> str:
    text = re.sub(r"<[^>]+>", " ", html)
    text = unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def replace_first_img_src(region: str, new_src: str) -> tuple[str, int]:
    return re.subn(r'src=["\'][^"\']*["\']', f'src="{new_src}"', region, count=1)

def replace_all_img_srcs_in_region(html: str, start: int, end: int, new_src: str) -> tuple[str, int]:
    region = html[start:end]
    fixed, n = replace_first_img_src(region, new_src)
    if n:
        return html[:start] + fixed + html[end:], n
    return html, 0

def patch_toc_li_by_title_or_href(html: str, html_file: Path, titles: list[str], ids: list[str], image_name: str) -> tuple[str, int]:
    new_src = rel_figure_src(html_file, image_name)
    total = 0

    # Patch every <li> that is a TOC row for the requested title/id.
    li_pattern = re.compile(r"<li\b[^>]*>.*?</li>", re.I | re.S)

    pieces = []
    last = 0

    for m in li_pattern.finditer(html):
        li = m.group(0)
        li_text = clean_text(li)
        is_match = False

        if any(title in li_text for title in titles):
            is_match = True

        if any(f'href="#{id_}"' in li or f"href='#{id_}'" in li for id_ in ids):
            is_match = True

        if not is_match or "<img" not in li:
            continue

        fixed_li, n = replace_first_img_src(li, new_src)
        if n:
            pieces.append(html[last:m.start()])
            pieces.append(fixed_li)
            last = m.end()
            total += n

    if total:
        pieces.append(html[last:])
        html = "".join(pieces)

    return html, total

def find_chapter_heading_match(html: str, titles: list[str], ids: list[str]):
    # First prefer IDs.
    for id_ in ids:
        m = re.search(
            r"<h[1-6]\b[^>]*\bid=[\"']" + re.escape(id_) + r"[\"'][^>]*>.*?</h[1-6]>",
            html,
            flags=re.I | re.S,
        )
        if m:
            return m

    # Fallback by visible text.
    for m in re.finditer(r"<h[1-6]\b[^>]*>.*?</h[1-6]>", html, flags=re.I | re.S):
        txt = clean_text(m.group(0))
        if any(title == txt for title in titles):
            return m

    return None

def patch_chapter_figure(html: str, html_file: Path, titles: list[str], ids: list[str], image_name: str) -> tuple[str, int]:
    new_src = rel_figure_src(html_file, image_name)
    h = find_chapter_heading_match(html, titles, ids)

    if not h:
        return html, 0

    section_start = h.end()

    # End before next h2 only, because this chapter contains h3 subsections.
    next_h2 = re.search(r"<h2\b", html[section_start:], flags=re.I)
    section_end = section_start + next_h2.start() if next_h2 else len(html)

    section = html[section_start:section_end]

    fig = re.search(r"<figure\b[^>]*>.*?</figure>", section, flags=re.I | re.S)

    if fig:
        abs_start = section_start + fig.start()
        abs_end = section_start + fig.end()
        return replace_all_img_srcs_in_region(html, abs_start, abs_end, new_src)

    # If the chapter has no figure, add the approved existing image. No image generation.
    is_he = "זהו מודל" in " ".join(titles)
    if any("זהו" in t for t in titles):
        alt = "איור פרק: זהו מודל, לא הכרזה סופית"
        caption = "תיאור תמונה: מבנה רעיוני חצי־בנוי, מצפן ודרך פתוחה אל אופק מואר; הדימוי מדגיש מודל אחראי, זמני, פתוח וניתן לביקורת."
    else:
        alt = "Chapter illustration: This Is a Model, Not a Final Declaration"
        caption = "Image description: a half-built conceptual structure, a compass, and an open path toward a bright horizon; the image emphasizes a responsible, provisional, criticizable model, not a final declaration."

    figure_html = (
        f'\n<figure class="chapter-figure image-frame">\n'
        f'<img alt="{alt}" decoding="async" loading="lazy" src="{new_src}"/>\n'
        f"<figcaption>{caption}</figcaption>\n"
        f"</figure>\n"
    )

    html = html[:section_start] + figure_html + html[section_start:]
    return html, 1

def validate(html: str, html_file: Path):
    model_src = rel_figure_src(html_file, MODEL_IMAGE_NAME)
    errors = []

    # Model chapter body must use the model image.
    h = find_chapter_heading_match(html, MODEL_TITLES, MODEL_IDS)
    if h:
        section_start = h.end()
        next_h2 = re.search(r"<h2\b", html[section_start:], flags=re.I)
        section_end = section_start + next_h2.start() if next_h2 else len(html)
        section = html[section_start:section_end]
        if "<figure" in section and model_src not in section:
            errors.append(f"chapter body still does not use {model_src}")

    # Model TOC row must use the model image.
    for id_ in MODEL_IDS:
        for q in [f'href="#{id_}"', f"href='#{id_}'"]:
            idx = html.find(q)
            if idx != -1:
                li_start = html.rfind("<li", 0, idx)
                li_end = html.find("</li>", idx)
                if li_start != -1 and li_end != -1:
                    li = html[li_start:li_end]
                    if "<img" in li and model_src not in li:
                        errors.append(f"TOC row {id_} still does not use {model_src}")

    if HAS_SUMMARY_IMAGE:
        summary_src = rel_figure_src(html_file, SUMMARY_IMAGE_NAME)
        for id_ in SUMMARY_IDS:
            for q in [f'href="#{id_}"', f"href='#{id_}'"]:
                idx = html.find(q)
                if idx != -1:
                    li_start = html.rfind("<li", 0, idx)
                    li_end = html.find("</li>", idx)
                    if li_start != -1 and li_end != -1:
                        li = html[li_start:li_end]
                        if "<img" in li and model_src in li:
                            errors.append(f"Summary/Abstract TOC still wrongly uses model image in {id_}")
                        if "<img" in li and summary_src not in li:
                            errors.append(f"Summary/Abstract TOC does not use {summary_src} in {id_}")

    if errors:
        raise SystemExit("VALIDATION FAILED in " + str(html_file) + "\n" + "\n".join(" - " + e for e in errors))

def main():
    changed_files = 0
    replacements = 0

    files = sorted(FILES_ROOT.rglob("*.html"))

    for html_file in files:
        html = html_file.read_text(encoding="utf-8", errors="ignore")
        original = html

        html, n = patch_toc_li_by_title_or_href(html, html_file, MODEL_TITLES, MODEL_IDS, MODEL_IMAGE_NAME)
        replacements += n

        if HAS_SUMMARY_IMAGE:
            html, n = patch_toc_li_by_title_or_href(html, html_file, SUMMARY_TITLES, SUMMARY_IDS, SUMMARY_IMAGE_NAME)
            replacements += n

        html, n = patch_chapter_figure(html, html_file, MODEL_TITLES, MODEL_IDS, MODEL_IMAGE_NAME)
        replacements += n

        # Validate only files that contain the relevant chapter/TOC references.
        if any(x in html for x in MODEL_IDS + MODEL_TITLES + SUMMARY_IDS + SUMMARY_TITLES):
            validate(html, html_file)

        if html != original:
            html_file.write_text(html, encoding="utf-8")
            changed_files += 1
            print("patched:", html_file)

    print("changed files:", changed_files)
    print("image replacements/insertions:", replacements)

if __name__ == "__main__":
    main()
