#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"

GOLD_STYLE = (
    "background:linear-gradient(135deg,#b98726,#e6b84a,#f5d06b)!important;"
    "background-color:#e6b84a!important;"
    "background-image:linear-gradient(135deg,#b98726,#e6b84a,#f5d06b)!important;"
    "color:#07101d!important;"
    "-webkit-text-fill-color:#07101d!important;"
    "border:1.5px solid transparent!important;"
    "box-shadow:0 8px 18px rgba(184,135,38,.18)!important;"
    "text-decoration:none!important;"
    "text-shadow:none!important;"
    "opacity:1!important;"
    "filter:none!important;"
)

ANCHOR_RE = re.compile(r"<a\b(?P<attrs>[^>]*)>(?P<body>.*?)</a>", re.IGNORECASE | re.DOTALL)
STYLE_RE = re.compile(r"\sstyle=(?P<q>[\"'])(?P<style>.*?)(?P=q)", re.IGNORECASE | re.DOTALL)
CLASS_RE = re.compile(r"\sclass=(?P<q>[\"'])(?P<class>.*?)(?P=q)", re.IGNORECASE | re.DOTALL)
HREF_RE = re.compile(r"\shref=(?P<q>[\"'])(?P<href>.*?)(?P=q)", re.IGNORECASE | re.DOTALL)


def strip_tags(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def should_gold(attrs: str, body: str) -> bool:
    href_match = HREF_RE.search(attrs)
    class_match = CLASS_RE.search(attrs)
    href = href_match.group("href") if href_match else ""
    classes = class_match.group("class") if class_match else ""
    text = strip_tags(body)

    if "site-nav" in attrs or "language-switch" in attrs or "breadcrumb" in attrs:
        return False

    is_visual_button = any(
        token in classes.split()
        for token in ("download-button", "card-link", "primary-format", "html-format", "is-html")
    )
    is_html_doc = ".html" in href.lower()
    says_html = "html" in text.lower()

    return is_visual_button and is_html_doc and says_html


def force_gold(anchor: re.Match[str]) -> str:
    attrs = anchor.group("attrs")
    body = anchor.group("body")

    if not should_gold(attrs, body):
        return anchor.group(0)

    attrs = re.sub(r"\sdata-bpi-html-gold=(['\"]).*?\1", "", attrs, flags=re.IGNORECASE | re.DOTALL)

    style_match = STYLE_RE.search(attrs)
    if style_match:
        current_style = style_match.group("style")
        merged = current_style.rstrip().rstrip(";") + ";" + GOLD_STYLE
        attrs = attrs[:style_match.start()] + f' style="{merged}"' + attrs[style_match.end():]
    else:
        attrs += f' style="{GOLD_STYLE}"'

    attrs += ' data-bpi-html-gold="true"'
    return f"<a{attrs}>{body}</a>"


def update_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if "download-button" not in text and "card-link" not in text and "HTML" not in text:
        return False

    updated = ANCHOR_RE.sub(force_gold, text)
    if updated == text:
        return False

    path.write_text(updated, encoding="utf-8")
    return True


def main() -> None:
    changed: list[str] = []
    for path in sorted(SITE.rglob("*.html")):
        if update_file(path):
            changed.append(str(path.relative_to(ROOT)))

    print(f"Updated {len(changed)} HTML files")
    for item in changed:
        print(item)


if __name__ == "__main__":
    main()
