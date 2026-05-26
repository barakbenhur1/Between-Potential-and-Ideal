#!/usr/bin/env python3
"""Hard-hide leaked homepage skip-link accent.

The tab/content pages use site/styles.css, which imports bpi-skip-link-fix.css.
The homepage files use styles-home-original.css directly. On some browsers, after
language-direction changes, the hidden skip link can visually leak as an orange
clipped pill at the top edge. This patch keeps the accessibility link in the DOM,
loads the shared CSS fix, and adds a home-page inline fallback so it cannot leak
before CSS finishes loading.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIX_LINK = '<link href="assets/bpi-skip-link-fix.css?v=20260526-skip-link-fix2" rel="stylesheet"/>'
HOME_STYLE = '<link href="styles-home-original.css?v=v17-exact" rel="stylesheet"/>'
HOME_STYLE_BUMPED = '<link href="styles-home-original.css?v=v17-exact-skipfix2" rel="stylesheet"/>'
INLINE_HIDE = (
    'style="position:fixed!important;top:0!important;inset-inline-start:0!important;'
    'width:1px!important;height:1px!important;overflow:hidden!important;'
    'clip:rect(0 0 0 0)!important;clip-path:inset(50%)!important;'
    'opacity:0!important;pointer-events:none!important;transform:translateY(-200%)!important;"'
)
PAGES = [ROOT / "site" / "index.html", ROOT / "site" / "en.html"]


def patch_skip_link(text: str) -> str:
    def repl(match: re.Match[str]) -> str:
        tag = match.group(0)
        tag = re.sub(r'\sstyle="[^"]*"', "", tag)
        tag = tag.replace(' class="skip-link"', f' class="skip-link" {INLINE_HIDE}', 1)
        return tag

    return re.sub(r'<a\s+class="skip-link"\b[^>]*>', repl, text, count=1)


def patch(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text

    # Bump the home stylesheet query to avoid stale browser cache on the homepage.
    text = text.replace(HOME_STYLE, HOME_STYLE_BUMPED)
    text = text.replace('styles-home-original.css?v=v17-exact-skipfix', 'styles-home-original.css?v=v17-exact-skipfix2')
    text = text.replace('assets/bpi-skip-link-fix.css?v=20260526-skip-link-fix', 'assets/bpi-skip-link-fix.css?v=20260526-skip-link-fix2')

    if 'assets/bpi-skip-link-fix.css' not in text:
        if HOME_STYLE_BUMPED in text:
            text = text.replace(HOME_STYLE_BUMPED, HOME_STYLE_BUMPED + FIX_LINK, 1)
        else:
            text = text.replace("</head>", FIX_LINK + "\n</head>", 1)

    text = patch_skip_link(text)

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
