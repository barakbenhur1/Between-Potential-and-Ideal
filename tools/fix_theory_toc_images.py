from pathlib import Path
import re

FILES = [
    Path("site/files/between-potential-and-ideal-he.html"),
    Path("site/files/between-potential-and-ideal-en.html"),
    Path("site/files/between-potential-and-ideal-he-editorial.html"),
    Path("site/files/between-potential-and-ideal-en-editorial.html"),
    Path("site/files/editorial-tightened/between-potential-and-ideal-tightened-he.html"),
    Path("site/files/editorial-tightened/between-potential-and-ideal-tightened-en.html"),
]

SUMMARY_IMG = "../figures/summary-theory-overview-v2.png"
MODEL_IMG = "../figures/chapter_model_not_final_declaration_v1.png"
OLD_COVER_IMG = "../figures/cover_philosophical_recursion_whole_diagram.png"

SUMMARY_HREFS = [
    "#תקציר",
    "#Abstract",
    "#abstract",
    "#Summary",
    "#summary",
]

MODEL_HREFS = [
    "#זהו-מודל-לא-הכרזה-סופית",
    "#This-Is-a-Model-Not-a-Final-Declaration",
    "#this-is-a-model-not-a-final-declaration",
]

MODEL_IDS = [
    'id="זהו-מודל-לא-הכרזה-סופית"',
    'id="This-Is-a-Model-Not-a-Final-Declaration"',
    'id="this-is-a-model-not-a-final-declaration"',
]

def replace_first_img_src(html: str, start: int, end: int, new_src: str) -> tuple[str, bool]:
    chunk = html[start:end]
    fixed = re.sub(r'src="\.\./figures/[^"]+"', f'src="{new_src}"', chunk, count=1)
    if fixed == chunk:
        return html, False
    return html[:start] + fixed + html[end:], True

def patch_toc_entry(html: str, href: str, new_src: str) -> tuple[str, int]:
    changed = 0
    pos = 0

    while True:
        idx = html.find(f'href="{href}"', pos)
        if idx == -1:
            break

        # Find the surrounding TOC entry, not the later chapter body.
        li_start = html.rfind("<li", 0, idx)
        li_end = html.find("</li>", idx)

        if li_start == -1 or li_end == -1:
            pos = idx + len(href)
            continue

        li_end += len("</li>")
        region = html[li_start:li_end]

        if "theory-toc-thumb" in region and "<img" in region:
            html2, did = replace_first_img_src(html, li_start, li_end, new_src)
            if did:
                html = html2
                changed += 1
                pos = li_end
                continue

        pos = idx + len(href)

    return html, changed

def patch_chapter_figure(html: str, id_marker: str, new_src: str) -> tuple[str, int]:
    idx = html.find(id_marker)
    if idx == -1:
        return html, 0

    # Only patch the first figure/image after the chapter heading.
    end = html.find("</figure>", idx)
    if end == -1:
        return html, 0

    end += len("</figure>")
    region = html[idx:end]

    if "<img" not in region:
        return html, 0

    html2, did = replace_first_img_src(html, idx, end, new_src)
    return html2, 1 if did else 0

def validate_file(path: Path, html: str):
    errors = []

    for href in SUMMARY_HREFS:
        idx = html.find(f'href="{href}"')
        if idx != -1:
            li_start = html.rfind("<li", 0, idx)
            li_end = html.find("</li>", idx)
            if li_start != -1 and li_end != -1:
                region = html[li_start:li_end]
                if "theory-toc-thumb" in region and MODEL_IMG in region:
                    errors.append(f"Summary/Abstract TOC still uses model image: {href}")

    for href in MODEL_HREFS:
        idx = html.find(f'href="{href}"')
        if idx != -1:
            li_start = html.rfind("<li", 0, idx)
            li_end = html.find("</li>", idx)
            if li_start != -1 and li_end != -1:
                region = html[li_start:li_end]
                if "theory-toc-thumb" in region and MODEL_IMG not in region:
                    errors.append(f"Model TOC does not use model image: {href}")

    for marker in MODEL_IDS:
        idx = html.find(marker)
        if idx != -1:
            end = html.find("</figure>", idx)
            if end != -1:
                region = html[idx:end]
                if "<img" in region and MODEL_IMG not in region:
                    errors.append(f"Model chapter figure does not use model image: {marker}")

    if errors:
        raise SystemExit(
            "VALIDATION FAILED in " + str(path) + ":\n" + "\n".join(" - " + e for e in errors)
        )

def main():
    total = 0

    for path in FILES:
        if not path.exists():
            print("skip missing:", path)
            continue

        html = path.read_text(encoding="utf-8", errors="ignore")
        original = html

        for href in SUMMARY_HREFS:
            html, n = patch_toc_entry(html, href, SUMMARY_IMG)
            total += n

        for href in MODEL_HREFS:
            html, n = patch_toc_entry(html, href, MODEL_IMG)
            total += n

        for marker in MODEL_IDS:
            html, n = patch_chapter_figure(html, marker, MODEL_IMG)
            total += n

        validate_file(path, html)

        if html != original:
            path.write_text(html, encoding="utf-8")
            print("patched:", path)
        else:
            print("no change:", path)

    print("total image replacements:", total)

if __name__ == "__main__":
    main()
