#!/usr/bin/env python3
from html.parser import HTMLParser
from pathlib import Path
import sys

# Gateway pages use the current header language-switch, not the retired
# bpi-language-menu component. Check actual paired targets, not class text alone.
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


class LanguageSwitchParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.targets = []

    def handle_starttag(self, tag, attrs):
        if tag != "a":
            return
        values = dict(attrs)
        if "language-switch" in (values.get("class") or "").split():
            self.targets.append(values.get("href"))


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

        parser = LanguageSwitchParser()
        parser.feed(text)
        if parser.targets != [expected_href]:
            errors.append(
                f"{filename}: expected one language switch to {expected_href}, "
                f"found {parser.targets}"
            )
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
