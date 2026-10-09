#!/usr/bin/env python3
from pathlib import Path
import re
import sys

# These public gateway pages use the current single-language-switch header,
# not the retired bpi-language-menu component.
PAIRS = (
    ("site/pages/he/glossary.html", "../en/glossary-en.html"),
    ("site/pages/en/glossary-en.html", "../he/glossary.html"),
    ("site/pages/he/potential-ideal-optimal.html", "../en/potential-ideal-optimal-en.html"),
    ("site/pages/en/potential-ideal-optimal-en.html", "../he/potential-ideal-optimal.html"),
    ("site/pages/he/ai-as-witness.html", "../en/ai-as-witness-en.html"),
    ("site/pages/en/ai-as-witness-en.html", "../he/ai-as-witness.html"),
)
REQUIRED = (
    "<title>",
    "canonical",
    "hreflang=",
    "og:title",
    "og:description",
    "twitter:card",
    'name="author"',
    'id="main"',
)


def main():
    errors = []
    for filename, expected_href in PAIRS:
        path = Path(filename)
        if not path.is_file():
            errors.append(f"missing: {filename}")
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for marker in REQUIRED:
            if marker not in text:
                errors.append(f"{filename}: {marker}")

        # Verify the language switch actually links to the paired edition,
        # rather than merely checking that an obsolete CSS class appears.
        links = re.findall(r'<a\\b[^>]*\\bclass=["\\\']language-switch["\\\'][^>]*>', text, re.I)
        valid_links = [
            tag for tag in links
            if re.search(r'\\bhref=["\\\']' + re.escape(expected_href) + r'["\\\']', tag)
        ]
        if len(valid_links) != 1:
            errors.append(f"{filename}: expected exactly one language-switch to {expected_href}")
        elif not (path.parent / expected_href).is_file():
            errors.append(f"{filename}: missing language switch target {expected_href}")

    if errors:
        print("FAIL: gateway pages")
        for error in errors:
            print("-", error)
        return 1
    print("OK: gateway pages baseline passed, including current language switches.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
