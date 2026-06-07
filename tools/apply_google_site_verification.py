#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
TOKEN = "k9pkXnawOQjzQix9l81lijToZj9Xp6EVWw6lHRqaeOA"
TAG = f'<meta name="google-site-verification" content="{TOKEN}" />'
META_RE = re.compile(
    r'<meta\b[^>]*\bname=["\']google-site-verification["\'][^>]*>\s*',
    re.I,
)


def patch(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    old = text

    text = META_RE.sub("", text)
    if "<head>" not in text:
        raise RuntimeError(f"missing <head>: {path}")

    text = text.replace("<head>", f"<head>{TAG}", 1)

    if text.count('name="google-site-verification"') != 1:
        raise RuntimeError(f"bad verification tag count: {path}")
    if TOKEN not in text:
        raise RuntimeError(f"verification token missing: {path}")

    if text != old:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed: list[str] = []
    for path in (SITE / "index.html", SITE / "en.html"):
        if patch(path):
            changed.append(str(path.relative_to(ROOT)))

    print("\n".join(changed) if changed else "No changes")


if __name__ == "__main__":
    main()
