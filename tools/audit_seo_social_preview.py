from pathlib import Path
from html import unescape
import re
import json

SITE = Path("site")
REPORT = Path("reports/audit_seo_social_preview.json")
BASE_URL = "https://between-potential-and-ideal.onrender.com"

META_RE = re.compile(r'<meta\b[^>]*>', re.I | re.S)
LINK_RE = re.compile(r'<link\b[^>]*>', re.I | re.S)

def attr(tag, name):
    m = re.search(r'\b' + re.escape(name) + r'=["\']([^"\']*)["\']', tag, re.I)
    return unescape(m.group(1).strip()) if m else ""

def is_html_page(path):
    return path.suffix.lower() == ".html"

def is_absolute_url(value):
    return value.startswith("https://") or value.startswith("http://")

def is_root_relative(value):
    return value.startswith("/")

def resolve_from_page(path, value):
    if not value or is_absolute_url(value) or value.startswith("data:"):
        return None
    if value.startswith("/"):
        return SITE / value.lstrip("/")
    return path.parent / value

def main():
    issues = []

    for path in sorted(SITE.rglob("*.html")):
        html = path.read_text(encoding="utf-8", errors="ignore")

        title = re.search(r"<title\b[^>]*>(.*?)</title>", html, re.I | re.S)
        if not title or not re.sub(r"\s+", " ", unescape(title.group(1))).strip():
            issues.append({"file": str(path), "type": "missing_title"})

        metas = META_RE.findall(html)
        links = LINK_RE.findall(html)

        has_description = False
        og_image_values = []
        twitter_image_values = []
        canonical_values = []

        for tag in metas:
            name = attr(tag, "name").lower()
            prop = attr(tag, "property").lower()
            content = attr(tag, "content")

            if name == "description" and content:
                has_description = True

            if prop == "og:image":
                og_image_values.append(content)

            if name == "twitter:image":
                twitter_image_values.append(content)

        for tag in links:
            rel = attr(tag, "rel").lower()
            href = attr(tag, "href")
            if rel == "canonical":
                canonical_values.append(href)

        if not has_description:
            issues.append({"file": str(path), "type": "missing_meta_description"})

        if not canonical_values:
            issues.append({"file": str(path), "type": "missing_canonical"})
        else:
            for href in canonical_values:
                if not is_absolute_url(href):
                    issues.append({"file": str(path), "type": "canonical_not_absolute", "value": href})

        for field, values in [("og:image", og_image_values), ("twitter:image", twitter_image_values)]:
            if not values:
                issues.append({"file": str(path), "type": f"missing_{field}"})
                continue

            for value in values:
                if not is_absolute_url(value):
                    issues.append({"file": str(path), "type": f"{field}_not_absolute", "value": value})

                resolved = resolve_from_page(path, value)
                if resolved is not None and not resolved.exists():
                    issues.append({
                        "file": str(path),
                        "type": f"{field}_local_target_missing",
                        "value": value,
                        "resolved": str(resolved),
                    })

    report = {
        "base_url": BASE_URL,
        "issue_count": len(issues),
        "issues": issues,
    }

    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    if issues:
        print("FAIL: SEO/social preview issues found")
        for item in issues[:120]:
            print(item)
        print("Report:", REPORT)
        raise SystemExit(1)

    print("OK: SEO/social preview audit passed")
    print("Report:", REPORT)

if __name__ == "__main__":
    main()
