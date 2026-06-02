from pathlib import Path
import re
import sys

BASE_URL = "https://between-potential-and-ideal.onrender.com"

GATEWAYS = [
    {
        "lang": "he",
        "path": Path("site/pages/he/glossary.html"),
        "canonical": f"{BASE_URL}/pages/he/glossary.html",
        "alternate": f"{BASE_URL}/pages/en/glossary-en.html",
    },
    {
        "lang": "en",
        "path": Path("site/pages/en/glossary-en.html"),
        "canonical": f"{BASE_URL}/pages/en/glossary-en.html",
        "alternate": f"{BASE_URL}/pages/he/glossary.html",
    },
    {
        "lang": "he",
        "path": Path("site/pages/he/potential-ideal-optimal.html"),
        "canonical": f"{BASE_URL}/pages/he/potential-ideal-optimal.html",
        "alternate": f"{BASE_URL}/pages/en/potential-ideal-optimal-en.html",
    },
    {
        "lang": "en",
        "path": Path("site/pages/en/potential-ideal-optimal-en.html"),
        "canonical": f"{BASE_URL}/pages/en/potential-ideal-optimal-en.html",
        "alternate": f"{BASE_URL}/pages/he/potential-ideal-optimal.html",
    },
    {
        "lang": "he",
        "path": Path("site/pages/he/ai-as-witness.html"),
        "canonical": f"{BASE_URL}/pages/he/ai-as-witness.html",
        "alternate": f"{BASE_URL}/pages/en/ai-as-witness-en.html",
    },
    {
        "lang": "en",
        "path": Path("site/pages/en/ai-as-witness-en.html"),
        "canonical": f"{BASE_URL}/pages/en/ai-as-witness-en.html",
        "alternate": f"{BASE_URL}/pages/he/ai-as-witness.html",
    },
]

META_RE = re.compile(r"<meta\b[^>]*>", re.I | re.S)
NAME_RE = re.compile(r"\bname\s*=\s*[\"']description[\"']", re.I)
CONTENT_RE = re.compile(r"\bcontent\s*=\s*[\"']([^\"']{40,})[\"']", re.I | re.S)


def has_meta_description(text: str) -> bool:
    for tag in META_RE.findall(text):
        if NAME_RE.search(tag) and CONTENT_RE.search(tag):
            return True
    return False


def main() -> int:
    errors = []

    for item in GATEWAYS:
        path = item["path"]
        if not path.exists():
            errors.append(f"missing gateway page: {path}")
            continue

        text = path.read_text(encoding="utf-8", errors="ignore")
        lang = item["lang"]
        opposite = "en" if lang == "he" else "he"

        required_fragments = [
            f'lang="{lang}"',
            "<title>",
            'property="og:title"',
            'property="og:description"',
            'name="twitter:card"',
            'name="author"',
            f'rel="canonical" href="{item["canonical"]}"',
            f'hreflang="{lang}"',
            f'hreflang="{opposite}"',
            'hreflang="x-default"',
            item["alternate"],
            'class="language-switch"',
            'id="main"',
        ]
        for fragment in required_fragments:
            if fragment not in text:
                errors.append(f"{path} missing fragment: {fragment}")

        if not has_meta_description(text):
            errors.append(f"{path} missing useful meta description")

    if errors:
        print("FAIL: gateway pages audit found issues")
        for error in errors:
            print("-", error)
        return 1

    print("OK: gateway pages baseline passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
