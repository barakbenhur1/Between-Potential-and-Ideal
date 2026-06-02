from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

ROBOTS = Path("site/robots.txt")
SITEMAP = Path("site/sitemap.xml")
BASE_URL = "https://between-potential-and-ideal.onrender.com"

REQUIRED_URLS = [
    f"{BASE_URL}/",
    f"{BASE_URL}/en.html",
    f"{BASE_URL}/pages/he/files.html",
    f"{BASE_URL}/pages/en/files-en.html",
    f"{BASE_URL}/files/appendices/stories-before-thought-hebrew-rtl.html",
    f"{BASE_URL}/files/appendices/stories-before-thought-english.html",
    f"{BASE_URL}/pages/en/glossary-en.html",
    f"{BASE_URL}/pages/he/glossary.html",
    f"{BASE_URL}/pages/en/potential-ideal-optimal-en.html",
    f"{BASE_URL}/pages/he/potential-ideal-optimal.html",
    f"{BASE_URL}/pages/en/ai-as-witness-en.html",
    f"{BASE_URL}/pages/he/ai-as-witness.html",
]

def main() -> int:
    errors = []

    if not ROBOTS.exists():
        errors.append("missing site/robots.txt")
    else:
        robots = ROBOTS.read_text(encoding="utf-8", errors="ignore")

        if not re.search(r"(?im)^User-agent:\s*\*", robots):
            errors.append("robots.txt missing User-agent: *")

        if not re.search(r"(?im)^Allow:\s*/\s*$", robots):
            errors.append("robots.txt missing Allow: /")

        if re.search(r"(?im)^Disallow:\s*/\s*$", robots):
            errors.append("robots.txt blocks the whole site with Disallow: /")

        expected_sitemap = f"Sitemap: {BASE_URL}/sitemap.xml"
        if expected_sitemap not in robots:
            errors.append(f"robots.txt missing exact sitemap line: {expected_sitemap}")

    if not SITEMAP.exists():
        errors.append("missing site/sitemap.xml")
    else:
        try:
            root = ET.parse(SITEMAP).getroot()
            urls = [
                loc.text.strip()
                for loc in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
                if loc.text
            ]

            if not urls:
                errors.append("sitemap.xml has no URLs")

            for url in REQUIRED_URLS:
                if url not in urls:
                    errors.append(f"sitemap.xml missing important public URL: {url}")

            bad = [url for url in urls if not url.startswith(BASE_URL + "/") and url != BASE_URL]
            if bad:
                errors.append("sitemap.xml contains URLs outside canonical base: " + ", ".join(bad[:10]))

        except Exception as e:
            errors.append(f"sitemap.xml is not valid XML: {e}")

    if errors:
        print("FAIL: SEO metadata / robots audit found issues")
        for e in errors:
            print("-", e)
        return 1

    print("OK: SEO metadata / robots baseline passed.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
