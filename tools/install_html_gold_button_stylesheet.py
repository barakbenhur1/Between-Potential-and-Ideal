#!/usr/bin/env python3
from __future__ import annotations

import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
ASSET = SITE / "assets" / "bpi-html-document-buttons-direct.css"
LINK_ID = "bpi-html-document-buttons-direct"
VERSION = "20260606-final-gold-html-v1"
LINK_RE = re.compile(
    rf'<link\b[^>]*\bid=["\']{re.escape(LINK_ID)}["\'][^>]*>\s*',
    re.IGNORECASE,
)


def public_page_html(path: Path, text: str) -> bool:
    if path.suffix.lower() != ".html":
        return False
    return "public-page" in text and 'id="main"' in text and "</head>" in text.lower()


def stylesheet_href(path: Path) -> str:
    relative = os.path.relpath(ASSET, path.parent).replace(os.sep, "/")
    return f"{relative}?v={VERSION}"


def update_page(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if not public_page_html(path, text):
        return False

    cleaned = LINK_RE.sub("", text)
    link = (
        f'<link id="{LINK_ID}" '
        f'href="{stylesheet_href(path)}" rel="stylesheet"/>'
    )

    updated, count = re.subn(
        r"</head>",
        link + "</head>",
        cleaned,
        count=1,
        flags=re.IGNORECASE,
    )
    if count != 1:
        raise RuntimeError(f"Could not insert stylesheet link in {path}")

    if updated == text:
        return False

    path.write_text(updated, encoding="utf-8")
    return True


def main() -> None:
    if not ASSET.exists():
        raise FileNotFoundError(ASSET)

    changed: list[str] = []
    for path in sorted(SITE.rglob("*.html")):
        if update_page(path):
            changed.append(str(path.relative_to(ROOT)))

    print(f"Updated {len(changed)} public HTML pages")
    for item in changed:
        print(item)


if __name__ == "__main__":
    main()
