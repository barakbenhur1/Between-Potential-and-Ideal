#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
THEME_VERSION = "20260606-home-black-theme-v6"
CARDS_VERSION = "20260606-home-dark-cards-v6"
THEME_ASSET = "assets/bpi-home-black-theme-v1.css"
CARDS_ASSET = "assets/bpi-home-dark-cards-v2.css"
THEME_RE = re.compile(
    r'<link\b[^>]*\bid="bpi-home-black-theme"[^>]*>\s*',
    re.I,
)
CARDS_RE = re.compile(
    r'<link\b[^>]*\bid="bpi-home-dark-cards"[^>]*>\s*',
    re.I,
)
INLINE_RE = re.compile(
    r'<style\b[^>]*\bid="bpi-home-blurb-typography-v6"[^>]*>.*?</style>\s*',
    re.I | re.S,
)

INLINE_STYLE = r'''<style id="bpi-home-blurb-typography-v6">
html body.public-page.design-prompt-theme.bpi-home-page main.site-main .signature-main-blurb p,
html body.public-page.design-prompt-theme.bpi-home-page main.site-main .signature-blurb-card p,
html body.public-page.design-prompt-theme.bpi-home-page main.site-main .signature-main-blurb strong,
html body.public-page.design-prompt-theme.bpi-home-page main.site-main .signature-blurb-card strong {
  background-image: none !important;
  -webkit-background-clip: border-box !important;
  background-clip: border-box !important;
}
html body.public-page.design-prompt-theme.bpi-home-page main.site-main .signature-main-blurb p:nth-of-type(1) {
  color: #f2c45e !important;
  -webkit-text-fill-color: #f2c45e !important;
  font-weight: 820 !important;
  font-size: clamp(1.16rem, 1.8vw, 1.42rem) !important;
}
html body.public-page.design-prompt-theme.bpi-home-page main.site-main .signature-main-blurb p:nth-of-type(2) {
  color: #63d4cf !important;
  -webkit-text-fill-color: #63d4cf !important;
  font-weight: 820 !important;
  font-size: clamp(1.12rem, 1.65vw, 1.34rem) !important;
}
html body.public-page.design-prompt-theme.bpi-home-page main.site-main .signature-main-blurb p:nth-of-type(4) {
  color: #9f8cff !important;
  -webkit-text-fill-color: #9f8cff !important;
  font-weight: 800 !important;
  font-size: clamp(1.08rem, 1.5vw, 1.26rem) !important;
}
html body.public-page.design-prompt-theme.bpi-home-page main.site-main .signature-main-blurb p:nth-of-type(6) {
  color: #63d4cf !important;
  -webkit-text-fill-color: #63d4cf !important;
  font-weight: 800 !important;
  font-size: clamp(1.08rem, 1.5vw, 1.26rem) !important;
}
html body.public-page.design-prompt-theme.bpi-home-page main.site-main .signature-main-blurb p:nth-of-type(8) {
  color: #f2c45e !important;
  -webkit-text-fill-color: #f2c45e !important;
  font-weight: 820 !important;
  font-size: clamp(1.08rem, 1.5vw, 1.24rem) !important;
}
html body.public-page.design-prompt-theme.bpi-home-page main.site-main .signature-blurb-card strong {
  color: var(--blurb-accent, #f2c45e) !important;
  -webkit-text-fill-color: var(--blurb-accent, #f2c45e) !important;
  font-weight: 820 !important;
}
html body.public-page.design-prompt-theme.bpi-home-page main.site-main .signature-blurbs article.question-card p:first-of-type {
  color: #c7b6ff !important;
  -webkit-text-fill-color: #c7b6ff !important;
  font-weight: 720 !important;
}
html body.public-page.design-prompt-theme.bpi-home-page main.site-main .signature-blurbs article.vessel-card p:first-of-type {
  color: #75d9d2 !important;
  -webkit-text-fill-color: #75d9d2 !important;
  font-weight: 700 !important;
}
html body.public-page.design-prompt-theme.bpi-home-page main.site-main .signature-blurbs article.paradox-card p:first-of-type {
  color: #e8a6b8 !important;
  -webkit-text-fill-color: #e8a6b8 !important;
  font-weight: 700 !important;
}
html body.public-page.design-prompt-theme.bpi-home-page main.site-main .signature-blurbs article.minimal-card p {
  color: #f2c45e !important;
  -webkit-text-fill-color: #f2c45e !important;
  font-weight: 820 !important;
}
html body.public-page.design-prompt-theme.bpi-home-page main.site-main .signature-blurbs article.ellipsis-card p {
  color: #8fcff8 !important;
  -webkit-text-fill-color: #8fcff8 !important;
  font-weight: 760 !important;
}
</style>'''


def patch(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    old = text
    text = THEME_RE.sub("", text)
    text = CARDS_RE.sub("", text)
    text = INLINE_RE.sub("", text)

    links = (
        f'<link id="bpi-home-black-theme" '
        f'href="{THEME_ASSET}?v={THEME_VERSION}" rel="stylesheet"/>'
        f'<link id="bpi-home-dark-cards" '
        f'href="{CARDS_ASSET}?v={CARDS_VERSION}" rel="stylesheet"/>'
        f'{INLINE_STYLE}'
    )

    if "</head>" not in text:
        raise RuntimeError(f"missing </head>: {path}")

    text = text.replace("</head>", links + "</head>", 1)

    if text.count('id="bpi-home-black-theme"') != 1:
        raise RuntimeError(f"bad homepage black-theme link count: {path}")
    if text.count('id="bpi-home-dark-cards"') != 1:
        raise RuntimeError(f"bad homepage dark-card link count: {path}")
    if text.count('id="bpi-home-blurb-typography-v6"') != 1:
        raise RuntimeError(f"bad inline blurb typography count: {path}")

    if text != old:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    targets = [SITE / "index.html", SITE / "en.html"]
    changed: list[str] = []

    for path in targets:
        if path.exists() and patch(path):
            changed.append(str(path.relative_to(ROOT)))

    print("\n".join(changed) if changed else "No changes")


if __name__ == "__main__":
    main()
