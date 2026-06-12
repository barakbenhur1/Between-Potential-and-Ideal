#!/usr/bin/env python3
from pathlib import Path
import sys

FILES = (
    "site/pages/he/glossary.html",
    "site/pages/en/glossary-en.html",
    "site/pages/he/potential-ideal-optimal.html",
    "site/pages/en/potential-ideal-optimal-en.html",
    "site/pages/he/ai-as-witness.html",
    "site/pages/en/ai-as-witness-en.html",
)
REQUIRED = (
    "<title>",
    "canonical",
    "hreflang=",
    "og:title",
    "og:description",
    "twitter:card",
    "name=\"author\"",
    "id=\"main\"",
    "bpi-language-menu",
)


def main():
    errors = []
    for filename in FILES:
        path = Path(filename)
        if not path.is_file():
            errors.append(f"missing: {filename}")
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for marker in REQUIRED:
            if marker not in text:
                errors.append(f"{filename}: {marker}")
    if errors:
        print("FAIL: gateway pages")
        for error in errors:
            print("-", error)
        return 1
    print("OK: gateway pages baseline passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
