#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit sitemap URLs against local public HTML files and canonical URL rules.

This tool is conservative and does not inspect protected body content.
It only checks sitemap structure, canonical base URLs, duplicate URLs,
index.html duplication, local target existence, and lastmod presence.

Run from repo root:
  python3 tools/audit_sitemap_canonical_parity.py
"""

from pathlib import Path
from urllib.parse import urlparse, unquote
import json
import sys
import xml.etree.ElementTree as ET

ROOT = Path.cwd()
SITE = ROOT / "site"
SITEMAP = SITE / "sitemap.xml"
REPORT_DIR = ROOT / "reports" / "production_next"
BASE_URL = "https://between-potential-and-ideal.onrender.com"
NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def local_path_for_url(url: str) -> Path:
    parsed = urlparse(url)
    path = unquote(parsed.path or "/")
    if path in {"", "/"}:
        return SITE / "index.html"
    return SITE / path.lstrip("/")


def extract_canonical(html_path: Path) -> str:
    text = html_path.read_text(encoding="utf-8", errors="ignore")
    lower = text.lower()
    pos = 0
    while True:
        start = lower.find("<link", pos)
        if start == -1:
            return ""
        end = lower.find(">", start)
        if end == -1:
            return ""
        tag = text[start:end + 1]
        tag_lower = tag.lower()
        if "canonical" in tag_lower:
            for quote in ['"', "'"]:
                marker = "href=" + quote
                href_start = tag_lower.find(marker)
                if href_start != -1:
                    href_start += len(marker)
                    href_end = tag.find(quote, href_start)
                    if href_end != -1:
                        return tag[href_start:href_end].strip()
        pos = end + 1


def main() -> int:
    errors = []
    warnings = []
    items = []

    if not SITEMAP.exists():
        print("FAIL: missing site/sitemap.xml")
        return 1

    try:
        root = ET.parse(SITEMAP).getroot()
    except Exception as exc:
        print(f"FAIL: sitemap XML parse failed: {exc}")
        return 1

    urls = []
    for url_node in root.findall("sm:url", NS):
        loc_node = url_node.find("sm:loc", NS)
        lastmod_node = url_node.find("sm:lastmod", NS)
        loc = (loc_node.text or "").strip() if loc_node is not None else ""
        lastmod = (lastmod_node.text or "").strip() if lastmod_node is not None else ""
        if not loc:
            errors.append("sitemap url entry missing loc")
            continue
        urls.append(loc)
        local = local_path_for_url(loc)
        item_errors = []
        item_warnings = []

        if not loc.startswith(BASE_URL + "/") and loc != BASE_URL:
            item_errors.append("URL outside canonical base")
        if "/index.html" in loc:
            item_errors.append("index.html URL should not be in sitemap")
        if not local.exists():
            item_errors.append("local target missing")
        elif local.suffix.lower() == ".html":
            canonical = extract_canonical(local)
            if canonical and canonical != loc:
                item_warnings.append(f"canonical differs: {canonical}")
        if not lastmod:
            item_warnings.append("missing lastmod")

        for e in item_errors:
            errors.append(f"{loc}: {e}")
        for w in item_warnings:
            warnings.append(f"{loc}: {w}")
        items.append({"loc": loc, "local": rel(local) if local.exists() else str(local), "lastmod": lastmod, "errors": item_errors, "warnings": item_warnings})

    seen = set()
    for url in urls:
        if url in seen:
            errors.append(f"duplicate sitemap URL: {url}")
        seen.add(url)

    result = {"status": "OK" if not errors else "FAIL", "url_count": len(urls), "errors": errors, "warnings": warnings, "items": items}
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / "sitemap_canonical_parity_audit.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = ["# Sitemap Canonical Parity Audit", "", f"- Status: `{result['status']}`", f"- URLs: {len(urls)}", f"- Errors: {len(errors)}", f"- Warnings: {len(warnings)}", ""]
    if errors:
        lines.append("## Errors")
        for e in errors[:120]:
            lines.append(f"- {e}")
        lines.append("")
    if warnings:
        lines.append("## Warnings")
        for w in warnings[:120]:
            lines.append(f"- {w}")
        lines.append("")
    (REPORT_DIR / "sitemap_canonical_parity_audit.md").write_text("\n".join(lines), encoding="utf-8")

    if errors:
        print("FAIL: sitemap canonical parity audit found errors")
        print(f"errors={len(errors)} warnings={len(warnings)}")
        return 1
    print("OK: sitemap canonical parity audit passed.")
    print(f"urls={len(urls)} warnings={len(warnings)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
