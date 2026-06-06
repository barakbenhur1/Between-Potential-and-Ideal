#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"

OLD_RUNTIME_RE = re.compile(
    r'<script\b[^>]*\bid="bpi-he-header-match-en-runtime"[^>]*>\s*</script>\s*',
    re.I,
)
MOBILE_CSS_RE = re.compile(
    r'<link\b[^>]*\bid="bpi-he-mobile-header-only"[^>]*>\s*',
    re.I,
)
VERSION = "20260606-he-mobile-header-grid-parity-v5"
ASSET = "bpi-he-mobile-header-only-v2.css"


def is_hebrew(path: Path) -> bool:
    return path == SITE / "index.html" or path.parent == SITE / "pages" / "he"


def asset_prefix(path: Path) -> str:
    return "" if path.parent == SITE else "../../"


def patch(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    old = text

    text = OLD_RUNTIME_RE.sub("", text)
    text = MOBILE_CSS_RE.sub("", text)

    if is_hebrew(path):
        link = (
            f'<link id="bpi-he-mobile-header-only" '
            f'href="{asset_prefix(path)}assets/{ASSET}?v={VERSION}" '
            f'rel="stylesheet"/>'
        )
        if "</head>" not in text:
            raise RuntimeError(f"missing </head>: {path}")
        text = text.replace("</head>", link + "</head>", 1)

    expected = 1 if is_hebrew(path) else 0
    if text.count('id="bpi-he-mobile-header-only"') != expected:
        raise RuntimeError(f"bad Hebrew mobile CSS count: {path}")
    if 'id="bpi-he-header-match-en-runtime"' in text:
        raise RuntimeError(f"legacy Hebrew header runtime remains: {path}")

    if text != old:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    targets = [SITE / "index.html", SITE / "en.html"]
    targets += sorted((SITE / "pages" / "he").glob("*.html"))
    targets += sorted((SITE / "pages" / "en").glob("*.html"))

    changed = []
    for path in targets:
        if path.exists() and patch(path):
            changed.append(str(path.relative_to(ROOT)))

    print("\n".join(changed) if changed else "No changes")


if __name__ == "__main__":
    main()
