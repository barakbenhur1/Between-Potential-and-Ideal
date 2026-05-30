from pathlib import Path
import re
import sys

ROOT = Path.cwd()
SITE = ROOT / "site"
FIG_DIR = SITE / "figures"
MODEL_IMG = "../figures/chapter_model_not_final_declaration_v1.png"
SUMMARY_IMG = "../figures/summary-theory-overview-v2.png"

if not (FIG_DIR / "chapter_model_not_final_declaration_v1.png").exists():
    raise SystemExit("Missing site/figures/chapter_model_not_final_declaration_v1.png")

MODEL_ANCHORS = [
    "#זהו-מודל-לא-הכרזה-סופית",
    "#This-Is-a-Model-Not-a-Final-Declaration",
    "#this-is-a-model-not-a-final-declaration",
]

SUMMARY_ANCHORS = [
    "#תקציר",
    "#Abstract",
    "#abstract",
    "#Summary",
    "#summary",
]

MODEL_ID_MARKERS = [
    'id="זהו-מודל-לא-הכרזה-סופית"',
    "id='זהו-מודל-לא-הכרזה-סופית'",
    'id="This-Is-a-Model-Not-a-Final-Declaration"',
    "id='This-Is-a-Model-Not-a-Final-Declaration'",
    'id="this-is-a-model-not-a-final-declaration"',
    "id='this-is-a-model-not-a-final-declaration'",
]

def replace_first_src(chunk: str, new_src: str):
    fixed, n = re.subn(r'src="\.\./figures/[^"]+"', f'src="{new_src}"', chunk, count=1)
    return fixed, n

def patch_toc_region(html: str, hrefs, target_src: str):
    total = 0
    for href in hrefs:
        pos = 0
        while True:
            idx = html.find(f'href="{href}"', pos)
            if idx == -1:
                break

            # Prefer TOC list item wrapper if present
            li_start = html.rfind("<li", 0, idx)
            li_end = html.find("</li>", idx)

            if li_start != -1 and li_end != -1:
                li_end += len("</li>")
                region = html[li_start:li_end]
                if "<img" in region:
                    fixed, n = replace_first_src(region, target_src)
                    if n:
                        html = html[:li_start] + fixed + html[li_end:]
                        total += n
                        pos = li_start + len(fixed)
                        continue

            # fallback local window
            start = max(0, idx - 300)
            end = min(len(html), idx + 2000)
            region = html[start:end]
            if "<img" in region:
                fixed, n = replace_first_src(region, target_src)
                if n:
                    html = html[:start] + fixed + html[end:]
                    total += n

            pos = idx + len(href)
    return html, total

def patch_chapter_region(html: str, markers, target_src: str):
    total = 0
    for marker in markers:
        idx = html.find(marker)
        if idx == -1:
            continue

        # Look for the first figure after the chapter heading/id
        fig_start = html.find("<figure", idx)
        if fig_start != -1:
            fig_end = html.find("</figure>", fig_start)
            if fig_end != -1:
                fig_end += len("</figure>")
                region = html[fig_start:fig_end]
                if "<img" in region:
                    fixed, n = replace_first_src(region, target_src)
                    if n:
                        html = html[:fig_start] + fixed + html[fig_end:]
                        total += n
                        continue

        # fallback: first image in a local window after heading
        start = idx
        end = min(len(html), idx + 4000)
        region = html[start:end]
        if "<img" in region:
            fixed, n = replace_first_src(region, target_src)
            if n:
                html = html[:start] + fixed + html[end:]
                total += n

    return html, total

def validate(path: Path, html: str):
    errors = []

    # Model chapter must use model image
    for marker in MODEL_ID_MARKERS:
        idx = html.find(marker)
        if idx != -1:
            region = html[idx:idx + 5000]
            if MODEL_IMG not in region:
                errors.append("model chapter image still not updated")

    # Model TOC must use model image
    for href in MODEL_ANCHORS:
        idx = html.find(f'href="{href}"')
        if idx != -1:
            region = html[max(0, idx - 300):idx + 2000]
            if MODEL_IMG not in region:
                errors.append(f"model TOC thumbnail not updated for {href}")

    # Summary TOC must NOT use model image
    for href in SUMMARY_ANCHORS:
        idx = html.find(f'href="{href}"')
        if idx != -1:
            region = html[max(0, idx - 300):idx + 2000]
            if MODEL_IMG in region:
                errors.append(f"summary/abstract TOC wrongly uses model image for {href}")

    if errors:
        raise SystemExit(f"VALIDATION FAILED: {path}\n - " + "\n - ".join(errors))

def main():
    candidates = sorted((SITE / "files").rglob("*.html"))
    total_changes = 0

    for path in candidates:
        html = path.read_text(encoding="utf-8", errors="ignore")
        original = html

        html, n1 = patch_toc_region(html, MODEL_ANCHORS, MODEL_IMG)
        html, n2 = patch_toc_region(html, SUMMARY_ANCHORS, SUMMARY_IMG)
        html, n3 = patch_chapter_region(html, MODEL_ID_MARKERS, MODEL_IMG)

        # Only validate files that mention the chapter or TOC anchors
        if any(x in html for x in [
            "זהו-מודל-לא-הכרזה-סופית",
            "This-Is-a-Model-Not-a-Final-Declaration",
            "#תקציר", "#Abstract", "#Summary"
        ]):
            validate(path, html)

        if html != original:
            path.write_text(html, encoding="utf-8")
            print(f"patched: {path} | toc_model={n1} toc_summary={n2} chapter={n3}")
            total_changes += (n1 + n2 + n3)
        else:
            print(f"no change: {path}")

    print("total replacements:", total_changes)

if __name__ == "__main__":
    main()
