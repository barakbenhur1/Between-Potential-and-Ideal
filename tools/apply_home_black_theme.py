#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
VERSION = "20260606-home-black-theme-v1"
ASSET = "assets/bpi-home-black-theme-v1.css"
LINK_RE = re.compile(
    r'<link\b[^>]*\bid="bpi-home-black-theme"[^>]*>\s*',
    re.I,
)


def patch(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    old = text
    text = LINK_RE.sub("", text)

    link = (
        f'<link id="bpi-home-black-theme" '
        f'href="{ASSET}?v={VERSION}" rel="stylesheet"/>'
    )

    if "</head>" not in text:
        raise RuntimeError(f"missing </head>: {path}")

    text = text.replace("</head>", link + "</head>", 1)

    if text.count('id="bpi-home-black-theme"') != 1:
        raise RuntimeError(f"bad homepage black-theme link count: {path}")

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
