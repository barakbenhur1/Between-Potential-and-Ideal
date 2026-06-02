from pathlib import Path
import json
import re
import sys

BASE_URL = "https://between-potential-and-ideal.onrender.com"
REPORT_DIR = Path("reports/production_next")

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


def write_report(items, errors):
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    payload = {"status": "OK" if not errors else "FAIL", "errors": errors, "items": items}
    (REPORT_DIR / "gateway_pages_audit.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    lines = [
        "# Gateway Pages Audit",
        "",
        f"- Status: `{payload['status']}`",
        f"- Pages checked: {len(items)}",
        f"- Errors: {len(errors)}",
        "",
    ]
    if errors:
        lines.append("## Errors")
        for error in errors:
            lines.append(f"- {error}")
        lines.append("")
    lines.append("## Pages")
    for item in items:
        lines.append(f"- `{item['path']}` — missing fragments: {len(item['missing_fragments'])}; meta description: `{item['has_meta_description']}`")
    (REPORT_DIR / "gateway_pages_audit.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    errors = []
    items = []

    for item in GATEWAYS:
        path = item["path"]
        page_result = {
            "path": str(path),
            "exists": path.exists(),
            "missing_fragments": [],
            "has_meta_description": False,
        }
        if not path.exists():
            errors.append(f"missing gateway page: {path}")
            items.append(page_result)
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
                page_result["missing_fragments"].append(fragment)
                errors.append(f"{path} missing fragment: {fragment}")

        page_result["has_meta_description"] = has_meta_description(text)
        if not page_result["has_meta_description"]:
            errors.append(f"{path} missing useful meta description")
        items.append(page_result)

    write_report(items, errors)

    if errors:
        print("FAIL: gateway pages audit found issues")
        for error in errors:
            print("-", error)
        print("Report: reports/production_next/gateway_pages_audit.md")
        return 1

    print("OK: gateway pages baseline passed.")
    print("Report: reports/production_next/gateway_pages_audit.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
