#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
import json
import re
import sys

ROOT = Path.cwd()
REPORT_DIR = ROOT / "reports" / "production_next"
BASE_URL = "https://between-potential-and-ideal.onrender.com"
LT = chr(60)
GT = chr(62)
TARGETS = [
    "site/files/between-potential-and-ideal-en.html",
    "site/files/between-potential-and-ideal-he.html",
    "site/files/between-potential-and-ideal-en-editorial.html",
    "site/files/between-potential-and-ideal-he-editorial.html",
    "site/files/editorial-tightened/between-potential-and-ideal-tightened-en.html",
    "site/files/editorial-tightened/between-potential-and-ideal-tightened-he.html",
    "site/files/appendices/stories-before-thought-english.html",
    "site/files/appendices/stories-before-thought-hebrew-rtl.html",
]

def rel(path):
    return str(path.relative_to(ROOT)).replace("\\", "/")

def has(content, needle):
    return needle.lower() in content.lower()

def title_value(content):
    m = re.search(LT + r"title\b[^" + GT + r"]*" + GT + r"(.*?)" + LT + r"/title" + GT, content, re.I | re.S)
    if not m:
        return ""
    return re.sub(r"\s+", " ", re.sub(LT + r"[^" + GT + r"]+" + GT, " ", m.group(1))).strip()

def canonical_value(content):
    for m in re.finditer(LT + r"link\b([^" + GT + r"]*)" + GT, content, re.I | re.S):
        tag = m.group(0).lower()
        if "canonical" in tag:
            h = re.search(r"href\s*=\s*['\"]([^'\"]+)['\"]", m.group(0), re.I)
            return h.group(1).strip() if h else ""
    return ""

def meta_content(content, key):
    for m in re.finditer(LT + r"meta\b([^" + GT + r"]*)" + GT, content, re.I | re.S):
        tag = m.group(0)
        low = tag.lower()
        if key.lower() in low:
            c = re.search(r"content\s*=\s*['\"]([^'\"]*)['\"]", tag, re.I | re.S)
            return c.group(1).strip() if c else ""
    return ""

def audit_one(path):
    content = path.read_text(encoding="utf-8", errors="ignore")
    title = title_value(content)
    desc = meta_content(content, 'name="description"') or meta_content(content, "name='description'")
    canonical = canonical_value(content)
    errors = []
    warnings = []
    if not title:
        errors.append("missing title")
    if not desc:
        errors.append("missing meta description")
    if not canonical:
        errors.append("missing canonical")
    elif not canonical.startswith(BASE_URL + "/") and canonical != BASE_URL:
        errors.append("canonical outside base URL")
    for label in ["property=\"og:title\"", "property='og:title'", "property=\"og:url\"", "property='og:url'", "name=\"twitter:card\"", "name='twitter:card'"]:
        if label in content:
            break
    else:
        warnings.append("missing social metadata group")
    return {"path": rel(path), "title": title, "description_chars": len(desc), "canonical": canonical, "errors": errors, "warnings": warnings}

def main():
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    items = []
    for target in TARGETS:
        path = ROOT / target
        items.append(audit_one(path) if path.exists() else {"path": target, "title": "", "description_chars": 0, "canonical": "", "errors": ["target missing"], "warnings": []})
    error_pages = sum(1 for i in items if i["errors"])
    warning_pages = sum(1 for i in items if i["warnings"])
    result = {"status": "OK" if error_pages == 0 else "FAIL", "targets_checked": len(items), "error_pages": error_pages, "warning_pages": warning_pages, "items": items}
    (REPORT_DIR / "document_seo_metadata_audit.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = ["# Document SEO Metadata Audit", "", f"- Status: `{result['status']}`", f"- Targets checked: {len(items)}", f"- Error pages: {error_pages}", f"- Warning pages: {warning_pages}", ""]
    for item in items:
        if item["errors"] or item["warnings"]:
            lines += [f"## `{item['path']}`", f"- Title: `{item['title']}`", f"- Canonical: `{item['canonical']}`", f"- Description chars: {item['description_chars']}"]
            if item["errors"]: lines.append(f"- Errors: {item['errors']}")
            if item["warnings"]: lines.append(f"- Warnings: {item['warnings']}")
            lines.append("")
    (REPORT_DIR / "document_seo_metadata_audit.md").write_text("\n".join(lines), encoding="utf-8")
    if error_pages:
        print("FAIL: document SEO metadata audit found errors")
        return 1
    print("OK: document SEO metadata core audit passed.")
    print(f"warning_pages={warning_pages}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
