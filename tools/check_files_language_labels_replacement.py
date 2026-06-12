#!/usr/bin/env python3
from pathlib import Path
import re
import sys

PAGES = (
    (Path("site/pages/en/files-en.html"), ("\u05e2\u05d1\u05e8\u05d9\u05ea", "\u05d0\u05e0\u05d2\u05dc\u05d9\u05ea")),
    (Path("site/pages/he/files.html"), ("English", "Mixed/source", "All languages", "All formats")),
)
MENU = re.compile(r'<details\b[^>]*class=["\'][^"\']*bpi-language-menu[^"\']*["\'][^>]*>.*?</details>', re.I | re.S)
LEGACY = re.compile(r'<a\b[^>]*class=["\'][^"\']*language-switch[^"\']*["\'][^>]*>.*?</a>', re.I | re.S)


def main():
    errors = []
    for path, labels in PAGES:
        if not path.is_file():
            errors.append(f"missing file: {path}")
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        text = MENU.sub("", LEGACY.sub("", text))
        for label in labels:
            if re.search(r">\s*" + re.escape(label) + r"\s*<", text, re.I):
                errors.append(f"{path}: label outside language navigation: {label}")
    if errors:
        print("FAIL: files language labels")
        for error in errors:
            print("-", error)
        return 1
    print("OK: files language labels match page language outside language navigation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
