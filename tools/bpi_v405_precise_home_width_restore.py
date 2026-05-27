#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path.cwd()
SITE = ROOT / "site"
HTML_FILES = [SITE / "index.html", SITE / "en.html"]
CSS_FILE = SITE / "styles.css"
BAD_CSS_FILE = SITE / "assets" / "bpi-home-card-equal-width.css"

HOME_BODY_CLASS = "bpi-home-width-clean"
BAD_BODY_CLASS = "bpi-home-width-scope"
BAD_LINK_RE = re.compile(r'\s*<link[^>]+bpi-home-card-equal-width\.css[^>]*>\s*', re.I)

START_CLARITY_RE = re.compile(
    r'<section\b[^>]*\bid=["\']bpi-start-here-clarity["\'][^>]*>.*?</section>',
    re.S | re.I
)
START_NOTE_RE = re.compile(
    r'<section\b[^>]*\bid=["\']bpi-start-here-note["\'][^>]*>.*?</section>',
    re.S | re.I
)

HE_TEXT = "זהו ניסוי מחשבתי דו־לשוני שמחבר מסה פילוסופית, מבנה לוגי, סיפורים ויישומים. הדרך המומלצת היא להתחיל בתקציר, לעבור לגרסה המהודקת, ואז לפתוח את המסמך המלא או הנספחים."
EN_TEXT = "This is a bilingual thought experiment combining a philosophical essay, a logical structure, stories, and applications. The recommended path is to start with the summary, continue to the tightened version, and then open the full document or appendices."

HE_NOTE = f"""<section class="notice-box bpi-start-here-note media-card accent-core" id="bpi-start-here-note">
<h2>התחל כאן</h2>
<p>{HE_TEXT}</p>
<div class="download-row bpi-start-here-buttons">
<a class="download-button primary" href="pages/he/summary.html">תקציר</a>
<a class="download-button" href="files/editorial-tightened/between-potential-and-ideal-tightened-he.html">גרסה מהודקת</a>
<a class="download-button" href="files/between-potential-and-ideal-he-editorial.html">המסמך המלא</a>
</div>
</section>"""

EN_NOTE = f"""<section class="notice-box bpi-start-here-note media-card accent-core" id="bpi-start-here-note">
<h2>Start here</h2>
<p>{EN_TEXT}</p>
<div class="download-row bpi-start-here-buttons">
<a class="download-button primary" href="pages/en/summary-en.html">Summary</a>
<a class="download-button" href="files/editorial-tightened/between-potential-and-ideal-tightened-en.html">Tightened version</a>
<a class="download-button" href="files/between-potential-and-ideal-en-editorial.html">Full document</a>
</div>
</section>"""

CSS_BLOCK = "/* BPI V405 - precise homepage card width normalization.\n   Restores the desktop/mobile visual behavior after the overly broad equal-width fix.\n   Scope is limited to index.html/en.html through body.bpi-home-width-clean.\n   It changes width/centering only; it does not redesign cards, grids, colors, typography, images, or content. */\nbody.bpi-home-width-clean{\n  --bpi-home-card-width: min(1680px, calc(100vw - 144px));\n}\n\n/* Let the homepage cards use the intended wide card width on desktop. */\n@media (min-width: 769px){\n  body.bpi-home-width-clean .site-main{\n    width:100%!important;\n    max-width:none!important;\n    box-sizing:border-box!important;\n  }\n\n  body.bpi-home-width-clean .site-main > :is(\n    .bpi-start-here-note,\n    .hero.concise-hero,\n    .opening-visual,\n    .signature-blurbs.refined-blurbs,\n    .signature-blurbs,\n    .reading-path-cta,\n    .language-status-note,\n    .hub-grid.three,\n    .content-grid,\n    .notice-box,\n    .method-note,\n    .media-card\n  ){\n    width:var(--bpi-home-card-width)!important;\n    max-width:var(--bpi-home-card-width)!important;\n    margin-left:auto!important;\n    margin-right:auto!important;\n    box-sizing:border-box!important;\n  }\n\n  /* Keep the blue theory/hero card exactly as designed, only match the white card width. */\n  body.bpi-home-width-clean .site-main > .hero.concise-hero{\n    width:var(--bpi-home-card-width)!important;\n    max-width:var(--bpi-home-card-width)!important;\n  }\n\n  body.bpi-home-width-clean .site-main > .opening-visual{\n    width:var(--bpi-home-card-width)!important;\n    max-width:var(--bpi-home-card-width)!important;\n  }\n}\n\n/* Mobile: 8px from each side, centered, and every major card uses the same corrected width. */\n@media (max-width: 768px){\n  body.bpi-home-width-clean .site-main{\n    width:100%!important;\n    max-width:none!important;\n    padding-left:8px!important;\n    padding-right:8px!important;\n    box-sizing:border-box!important;\n  }\n\n  body.bpi-home-width-clean .site-main > :is(\n    .bpi-start-here-note,\n    .hero.concise-hero,\n    .opening-visual,\n    .signature-blurbs.refined-blurbs,\n    .signature-blurbs,\n    .reading-path-cta,\n    .language-status-note,\n    .hub-grid.three,\n    .content-grid,\n    .notice-box,\n    .method-note,\n    .media-card\n  ){\n    width:100%!important;\n    max-width:100%!important;\n    margin-left:auto!important;\n    margin-right:auto!important;\n    box-sizing:border-box!important;\n  }\n\n  body.bpi-home-width-clean .site-main > .bpi-start-here-note,\n  body.bpi-home-width-clean .site-main > .hero.concise-hero{\n    text-align:center;\n  }\n\n  body.bpi-home-width-clean .bpi-start-here-buttons{\n    display:flex!important;\n    flex-wrap:wrap!important;\n    justify-content:center!important;\n    align-items:center!important;\n    gap:12px!important;\n    width:100%!important;\n  }\n\n  body.bpi-home-width-clean .bpi-start-here-buttons .download-button{\n    box-sizing:border-box!important;\n    justify-content:center!important;\n    text-align:center!important;\n  }\n}"

def remove_class_from_body(html: str, class_name: str) -> str:
    body_re = re.compile(r"<body\b([^>]*)>", re.I | re.S)
    m = body_re.search(html)
    if not m:
        return html
    attrs = m.group(1)
    cm = re.search(r'class=(["\'])(.*?)\1', attrs, re.I | re.S)
    if not cm:
        return html
    classes = [c for c in cm.group(2).split() if c != class_name]
    new_attrs = attrs[:cm.start()] + f'class="{" ".join(classes)}"' + attrs[cm.end():]
    return html[:m.start()] + "<body" + new_attrs + ">" + html[m.end():]

def add_class_to_body(html: str, class_name: str) -> str:
    body_re = re.compile(r"<body\b([^>]*)>", re.I | re.S)
    m = body_re.search(html)
    if not m:
        return html
    attrs = m.group(1)
    cm = re.search(r'class=(["\'])(.*?)\1', attrs, re.I | re.S)
    if cm:
        classes = cm.group(2).split()
        if class_name in classes:
            return html
        classes.append(class_name)
        new_attrs = attrs[:cm.start()] + f'class="{" ".join(classes)}"' + attrs[cm.end():]
    else:
        new_attrs = attrs + f' class="{class_name}"'
    return html[:m.start()] + "<body" + new_attrs + ">" + html[m.end():]

def fix_start_card(html: str, is_he: bool) -> str:
    html = START_CLARITY_RE.sub("", html)
    note = HE_NOTE if is_he else EN_NOTE
    if START_NOTE_RE.search(html):
        html = START_NOTE_RE.sub(note, html, count=1)
    return html

def patch_html(path: Path) -> dict:
    if not path.exists():
        return {"path": str(path), "missing": True}

    original = path.read_text(encoding="utf-8", errors="ignore")
    html = original

    html = BAD_LINK_RE.sub("\n", html)
    html = remove_class_from_body(html, BAD_BODY_CLASS)
    html = add_class_to_body(html, HOME_BODY_CLASS)
    html = fix_start_card(html, is_he=(path.name == "index.html"))

    path.write_text(html, encoding="utf-8")
    return {
        "path": str(path),
        "changed": html != original,
        "start_here_note_count": html.count('id="bpi-start-here-note"'),
        "bad_link_present": "bpi-home-card-equal-width.css" in html,
        "bad_scope_present": BAD_BODY_CLASS in html,
    }

def patch_css() -> dict:
    if not CSS_FILE.exists():
        return {"path": str(CSS_FILE), "missing": True}
    original = CSS_FILE.read_text(encoding="utf-8", errors="ignore")
    css = original

    css = re.sub(
        r'\n/\* BPI V405 - precise homepage card width normalization\..*?(?=\n/\*|\Z)',
        '\n',
        css,
        flags=re.S
    )

    css = css.rstrip() + "\n" + CSS_BLOCK.strip() + "\n"
    CSS_FILE.write_text(css, encoding="utf-8")
    return {"path": str(CSS_FILE), "changed": css != original}

def main():
    if not SITE.exists():
        raise SystemExit("ERROR: run from repository root — the directory that contains site/")

    results = [patch_html(p) for p in HTML_FILES]
    results.append(patch_css())

    removed_bad_asset = False
    if BAD_CSS_FILE.exists():
        BAD_CSS_FILE.unlink()
        removed_bad_asset = True

    problems = []
    for p in HTML_FILES:
        if p.exists():
            html = p.read_text(encoding="utf-8", errors="ignore")
            if html.count('id="bpi-start-here-note"') != 1:
                problems.append(f"{p}: expected exactly one bpi-start-here-note")
            if 'id="bpi-start-here-clarity"' in html:
                problems.append(f"{p}: duplicate bpi-start-here-clarity still exists")
            if "bpi-home-card-equal-width.css" in html:
                problems.append(f"{p}: bad broad equal-width css still linked")
            if BAD_BODY_CLASS in html:
                problems.append(f"{p}: bad broad body class still present")
            if HOME_BODY_CLASS not in html:
                problems.append(f"{p}: new narrow body class missing")
            if p.name == "index.html" and "המסמך המלא" not in html:
                problems.append(f"{p}: Hebrew third button missing")
            if p.name == "en.html" and "Full document" not in html:
                problems.append(f"{p}: English third button missing")

    css = CSS_FILE.read_text(encoding="utf-8", errors="ignore") if CSS_FILE.exists() else ""
    if "BPI V405" not in css:
        problems.append("styles.css: V405 css missing")

    report = [
        "BPI V405 precise homepage width restoration",
        "",
        "What this does:",
        "- Removes the previous overly broad equal-width CSS link/body scope.",
        "- Keeps only one Start Here card.",
        "- Keeps the second Start Here design with the full first-card content.",
        "- Keeps 3 buttons in Hebrew and English.",
        "- Desktop: restores normal look and only normalizes card widths.",
        "- Desktop: blue theory/hero card and opening image card match the white Start Here card width.",
        "- Mobile: cards are centered with 8px margin on each side and share the same width.",
        "",
        "Results:",
        *[str(r) for r in results],
        f"removed_bad_asset={removed_bad_asset}",
    ]

    if problems:
        report.append("")
        report.append("FAILED:")
        report.extend([f"- {p}" for p in problems])
        (ROOT / "BPI_V405_HOME_WIDTH_RESTORE_REPORT.txt").write_text("\n".join(report) + "\n", encoding="utf-8")
        print("\n".join(report))
        raise SystemExit(1)

    report.append("")
    report.append("OK")
    (ROOT / "BPI_V405_HOME_WIDTH_RESTORE_REPORT.txt").write_text("\n".join(report) + "\n", encoding="utf-8")
    print("\n".join(report))

if __name__ == "__main__":
    main()
