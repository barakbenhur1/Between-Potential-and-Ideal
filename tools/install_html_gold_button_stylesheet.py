#!/usr/bin/env python3
from pathlib import Path
import os

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
ASSET = SITE / "assets" / "bpi-html-document-buttons-direct.css"
OLD = "20260606-final-gold-html-v1"
NEW = "20260606-final-gold-html-ai-actions-v2"


def public_page(path: Path, text: str) -> bool:
    return path.suffix == ".html" and "public-page" in text and 'id="main"' in text


def update(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if not public_page(path, text):
        return False

    relative = os.path.relpath(ASSET, path.parent).replace(os.sep, "/")
    old_link = f'<link id="bpi-html-document-buttons-direct" href="{relative}?v={OLD}" rel="stylesheet"/>'
    new_link = f'<link id="bpi-html-document-buttons-direct" href="{relative}?v={NEW}" rel="stylesheet"/>'

    if old_link in text:
        text = text.replace(old_link, new_link)
    elif new_link not in text:
        text = text.replace("</head>", new_link + "</head>", 1)
    else:
        return False

    path.write_text(text, encoding="utf-8")
    return True


def main() -> None:
    changed = []
    for path in sorted(SITE.rglob("*.html")):
        if update(path):
            changed.append(str(path.relative_to(ROOT)))

    print(f"Updated {len(changed)} public HTML pages")
    for item in changed:
        print(item)


if __name__ == "__main__":
    main()
