#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path.cwd()
SITE = ROOT / "site"
CSS_REL = "assets/bpi-home-card-equal-width.css"
CSS_PATH = SITE / CSS_REL

CSS_CONTENT = r"""/* BPI home equal-width cards fix
   Scope: homepage only, by body.bpi-home-width-scope.
   Goal:
   - desktop: all main homepage cards/visual blocks use the width of the widest card.
   - mobile: start-here and hero/thought cards are centered and slightly narrower, then all major cards match that width.
   - does not affect theory documents, appendices, or file documents.
*/

body.bpi-home-width-scope {
  --bpi-home-card-width: min(1220px, calc(100vw - 96px));
  --bpi-home-card-width-mobile: min(760px, calc(100vw - 34px));
}

/* Desktop/tablet: normalize the major homepage blocks/cards to one width. */
@media (min-width: 769px) {
  body.bpi-home-width-scope :is(
    main > section,
    main > article,
    .home-section,
    .home-card,
    .hero-card,
    .home-hero-card,
    .bpi-hero-card,
    .thought-experiment-card,
    .bpi-thought-card,
    .bpi-start-here,
    .bpi-start-here-card,
    .start-here,
    .start-here-card,
    .recommended-start,
    .recommended-start-card,
    .reading-path,
    .reading-path-card,
    .quote-card,
    .bpi-quote-card,
    .visual-card,
    .image-card,
    .feature-card,
    .section-card,
    .method-card,
    .source-card,
    .witness-card,
    .application-card,
    .archive-card,
    .file-card,
    .route-card,
    .document-card,
    .card,
    figure.image-frame
  ) {
    width: var(--bpi-home-card-width) !important;
    max-width: var(--bpi-home-card-width) !important;
    margin-left: auto !important;
    margin-right: auto !important;
    box-sizing: border-box !important;
  }

  /* Keep inner grids inside the normalized card width, not wider than the card. */
  body.bpi-home-width-scope :is(
    .cards-grid,
    .home-grid,
    .reading-grid,
    .files-grid,
    .feature-grid,
    .archive-grid
  ) {
    width: var(--bpi-home-card-width) !important;
    max-width: var(--bpi-home-card-width) !important;
    margin-left: auto !important;
    margin-right: auto !important;
    box-sizing: border-box !important;
  }

  /* The blue opening/hero card should match the white start card above it. */
  body.bpi-home-width-scope :is(
    .hero,
    .hero-panel,
    .hero-card,
    .home-hero-card,
    .bpi-hero-card,
    .thought-experiment-card,
    .bpi-thought-card
  ) {
    width: var(--bpi-home-card-width) !important;
    max-width: var(--bpi-home-card-width) !important;
  }
}

/* Mobile: center and slightly tighten the start-here + thought/hero cards, then make all cards match. */
@media (max-width: 768px) {
  body.bpi-home-width-scope :is(
    main > section,
    main > article,
    .home-section,
    .home-card,
    .hero-card,
    .home-hero-card,
    .bpi-hero-card,
    .thought-experiment-card,
    .bpi-thought-card,
    .bpi-start-here,
    .bpi-start-here-card,
    .start-here,
    .start-here-card,
    .recommended-start,
    .recommended-start-card,
    .reading-path,
    .reading-path-card,
    .quote-card,
    .bpi-quote-card,
    .visual-card,
    .image-card,
    .feature-card,
    .section-card,
    .method-card,
    .source-card,
    .witness-card,
    .application-card,
    .archive-card,
    .file-card,
    .route-card,
    .document-card,
    .card,
    figure.image-frame
  ) {
    width: var(--bpi-home-card-width-mobile) !important;
    max-width: var(--bpi-home-card-width-mobile) !important;
    margin-left: auto !important;
    margin-right: auto !important;
    box-sizing: border-box !important;
  }

  body.bpi-home-width-scope :is(
    .bpi-start-here,
    .bpi-start-here-card,
    .start-here,
    .start-here-card,
    .recommended-start,
    .recommended-start-card,
    .hero,
    .hero-panel,
    .hero-card,
    .home-hero-card,
    .bpi-hero-card,
    .thought-experiment-card,
    .bpi-thought-card
  ) {
    width: var(--bpi-home-card-width-mobile) !important;
    max-width: var(--bpi-home-card-width-mobile) !important;
    margin-left: auto !important;
    margin-right: auto !important;
    text-align: center;
  }

  /* Three buttons should stay available; allow clean wrapping without shrinking the card. */
  body.bpi-home-width-scope :is(
    .bpi-start-here-actions,
    .start-here-actions,
    .recommended-start-actions,
    .hero-actions,
    .cta-row
  ) {
    display: flex !important;
    flex-wrap: wrap !important;
    justify-content: center !important;
    align-items: center !important;
    gap: 12px !important;
    width: 100% !important;
    max-width: 100% !important;
    box-sizing: border-box !important;
  }

  body.bpi-home-width-scope :is(
    .bpi-start-here-actions a,
    .start-here-actions a,
    .recommended-start-actions a,
    .hero-actions a,
    .cta-row a,
    .bpi-start-here-actions button,
    .start-here-actions button,
    .recommended-start-actions button,
    .hero-actions button,
    .cta-row button
  ) {
    max-width: 100% !important;
    box-sizing: border-box !important;
  }
}
"""

TARGETS = [
    SITE / "index.html",
    SITE / "en.html",
]

BODY_CLASS = "bpi-home-width-scope"
LINK_MARKER = "bpi-home-card-equal-width.css"


def add_body_class(html: str) -> str:
    m = re.search(r"<body\b([^>]*)>", html, flags=re.I)
    if not m:
        return html

    attrs = m.group(1)
    body_tag = m.group(0)

    class_m = re.search(r'class=(["\'])(.*?)\1', attrs, flags=re.I | re.S)
    if class_m:
        classes = class_m.group(2).split()
        if BODY_CLASS in classes:
            return html
        new_classes = " ".join(classes + [BODY_CLASS])
        new_attrs = attrs[:class_m.start()] + f'class="{new_classes}"' + attrs[class_m.end():]
        new_tag = "<body" + new_attrs + ">"
    else:
        new_tag = "<body" + attrs + f' class="{BODY_CLASS}">'

    return html[:m.start()] + new_tag + html[m.end():]


def add_css_link(html: str) -> str:
    if LINK_MARKER in html:
        return html

    link = f'<link rel="stylesheet" href="{CSS_REL}?v=20260527-home-equal-width-cards">'
    if "</head>" in html:
        return html.replace("</head>", link + "\n</head>", 1)
    if "</HEAD>" in html:
        return html.replace("</HEAD>", link + "\n</HEAD>", 1)
    return link + "\n" + html


def main():
    if not SITE.exists():
        raise SystemExit("ERROR: run this from the repository root, the directory that contains site/")

    CSS_PATH.parent.mkdir(parents=True, exist_ok=True)
    CSS_PATH.write_text(CSS_CONTENT, encoding="utf-8")

    changed = []
    missing = []
    for path in TARGETS:
        if not path.exists():
            missing.append(str(path))
            continue

        original = path.read_text(encoding="utf-8", errors="ignore")
        html = original
        html = add_body_class(html)
        html = add_css_link(html)

        if html != original:
            path.write_text(html, encoding="utf-8")
            changed.append(str(path))

    report = [
        "BPI home equal-width cards fix",
        "",
        "Changed files:",
        *[f"- {p}" for p in changed],
        "",
        "Created/updated:",
        f"- {CSS_PATH}",
        "",
        "Missing targets:",
        *[f"- {p}" for p in missing],
        "",
        "Manual QA:",
        "- Desktop: start-here card appears once and all major cards match the widest card width.",
        "- Desktop: blue opening card width equals the white start card width.",
        "- Mobile: start-here and thought/hero cards are centered and slightly tightened.",
        "- Mobile: all major cards match that corrected width.",
        "- Three buttons remain visible in start-here in Hebrew and English.",
    ]
    (ROOT / "BPI_HOME_EQUAL_WIDTH_CARDS_FIX_REPORT.txt").write_text("\n".join(report) + "\n", encoding="utf-8")

    print("\n".join(report))


if __name__ == "__main__":
    main()
