#!/usr/bin/env python3
"""Load the global skip-link leak fix on homepage entry files.

The tab/content pages use site/styles.css, which imports bpi-skip-link-fix.css.
The homepage files use styles-home-original.css directly, so they need the same
fix linked explicitly.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIX_LINK = '<link href="assets/bpi-skip-link-fix.css?v=20260526-skip-link-fix" rel="stylesheet"/>'
HOME_STYLE = '<link href="styles-home-original.css?v=v17-exact" rel="stylesheet"/>'
HOME_STYLE_BUMPED = '<link href="styles-home-original.css?v=v17-exact-skipfix" rel="stylesheet"/>'
PAGES = [ROOT / "site" / "index.html", ROOT / "site" / "en.html"]


def patch(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text

    # Bump the home stylesheet query to avoid stale browser cache on the homepage.
    text = text.replace(HOME_STYLE, HOME_STYLE_BUMPED)

    if FIX_LINK not in text:
        if HOME_STYLE_BUMPED in text:
            text = text.replace(HOME_STYLE_BUMPED, HOME_STYLE_BUMPED + FIX_LINK, 1)
        elif HOME_STYLE in text:
            text = text.replace(HOME_STYLE, HOME_STYLE_BUMPED + FIX_LINK, 1)
        else:
            text = text.replace("</head>", FIX_LINK + "\n</head>", 1)

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> int:
    changed = []
    for path in PAGES:
        if patch(path):
            changed.append(path.relative_to(ROOT).as_posix())
    print(f"changed pages: {len(changed)}")
    for item in changed:
        print(f"- {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
