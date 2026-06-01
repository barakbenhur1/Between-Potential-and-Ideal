#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit bilingual hreflang readiness.

This is a conservative audit for the bilingual site. It builds a pair map from:
- home pair: site/index.html <-> site/en.html
- search-index chapter pairs
- search-index story collection anchors

It checks that paired local targets exist and reports whether the HTML host pages
contain hreflang links. Missing hreflang is a warning, not a release blocker,
because adding hreflang to every generated long document should be reviewed in a
separate apply step.

Protected-elements policy:
This audit does not inspect, criticize, or modify protected body content such as
blurbs, arrows, symbolic markers, Author's Note styling, or approved document
wording.

Run from repo root:
  python3 tools/audit_hreflang_links.py
"""

from pathlib import Path
from urllib.parse import urlparse, unquote
import json
import re
import sys

ROOT = Path.cwd()
SITE = ROOT / "site"
INDEX = SITE / "search-index.json"
REPORT_DIR = ROOT / "reports" / "production_next"
BASE_URL = "https://between-potential-and-ideal.onrender.com"
LINK_RE = re.compile(r"<link\b[^>]*rel=[\"'][^\"']*alternate[^\"']*[\"'][^>]*>", re.I | re.S)
HREFLANG_RE = re.compile(r"hreflang\s*=\s*[\"']([^\"']+)[\"']", re.I)
HREF_RE = re.compile(r"href\s*=\s*[\"']([^\"']+)[\"']", re.I)


def local_path(url: str) -> Path:
    host = (url or "").split("#", 1)[0]
    parsed = urlparse(host)
    path = unquote(parsed.path if parsed.scheme else host)
    if path.startswith("/"):
        return SITE / path.lstrip("/")
    return SITE / path


def absolute_url(local_url: str) -> str:
    host = (local_url or "").split("#", 1)[0]
    if host.startswith("http://") or host.startswith("https://"):
        return host
    return BASE_URL + "/" + host.lstrip("/")


def parse_hreflang(path: Path) -> dict[str, str]:
    if not path.exists() or path.suffix.lower() != ".html":
        return {}
    text = path.read_text(encoding="utf-8", errors="ignore")
    found = {}
    for tag in LINK_RE.findall(text):
        lm = HREFLANG_RE.search(tag)
        hm = HREF_RE.search(tag)
        if lm and hm:
            found[lm.group(1).strip().lower()] = hm.group(1).strip()
    return found


def load_pairs() -> list[dict]:
    pairs = [{"slug": "home", "he": "index.html", "en": "en.html", "source": "home"}]
    if not INDEX.exists():
        return pairs
    try:
        data = json.loads(INDEX.read_text(encoding="utf-8"))
    except Exception:
        return pairs
    for group_name in ["chapters", "stories"]:
        group = data.get(group_name, [])
        if not isinstance(group, list):
            continue
        for entry in group:
            if not isinstance(entry, dict):
                continue
            he = entry.get("he", {}) if isinstance(entry.get("he"), dict) else {}
            en = entry.get("en", {}) if isinstance(entry.get("en"), dict) else {}
            he_url = he.get("url")
            en_url = en.get("url")
            if he_url and en_url:
                pairs.append({"slug": str(entry.get("slug", "")), "he": he_url, "en": en_url, "source": group_name})
    # Deduplicate by host URL pair; story anchors share the same collection host but remain useful in report only once.
    unique = []
    seen = set()
    for pair in pairs:
        key = (pair["he"].split("#", 1)[0], pair["en"].split("#", 1)[0])
        if key in seen:
            continue
        seen.add(key)
        unique.append(pair)
    return unique


def audit() -> dict:
    errors = []
    warnings = []
    items = []
    pairs = load_pairs()
    for pair in pairs:
        he_path = local_path(pair["he"])
        en_path = local_path(pair["en"])
        item_errors = []
        item_warnings = []
        if not he_path.exists():
            item_errors.append("missing Hebrew local target")
        if not en_path.exists():
            item_errors.append("missing English local target")
        he_links = parse_hreflang(he_path)
        en_links = parse_hreflang(en_path)
        expected_he = absolute_url(pair["he"])
        expected_en = absolute_url(pair["en"])
        if he_path.exists() and he_path.suffix.lower() == ".html":
            if "he" not in he_links:
                item_warnings.append("Hebrew page missing self hreflang=he")
            if "en" not in he_links:
                item_warnings.append("Hebrew page missing alternate hreflang=en")
            if "x-default" not in he_links:
                item_warnings.append("Hebrew page missing hreflang=x-default")
        if en_path.exists() and en_path.suffix.lower() == ".html":
            if "en" not in en_links:
                item_warnings.append("English page missing self hreflang=en")
            if "he" not in en_links:
                item_warnings.append("English page missing alternate hreflang=he")
            if "x-default" not in en_links:
                item_warnings.append("English page missing hreflang=x-default")
        for e in item_errors:
            errors.append(f"{pair['slug']}: {e}")
        for w in item_warnings:
            warnings.append(f"{pair['slug']}: {w}")
        items.append({
            "slug": pair["slug"],
            "source": pair["source"],
            "he": pair["he"],
            "en": pair["en"],
            "expected_he_absolute": expected_he,
            "expected_en_absolute": expected_en,
            "he_hreflang_keys": sorted(he_links.keys()),
            "en_hreflang_keys": sorted(en_links.keys()),
            "errors": item_errors,
            "warnings": item_warnings,
        })
    return {"status": "OK" if not errors else "FAIL", "pair_count": len(pairs), "errors": errors, "warnings": warnings, "items": items}


def write_reports(result: dict) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / "hreflang_links_audit.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        "# Bilingual Hreflang Links Audit",
        "",
        f"- Status: `{result['status']}`",
        f"- Pairs checked: {result['pair_count']}",
        f"- Errors: {len(result['errors'])}",
        f"- Warnings: {len(result['warnings'])}",
        "",
    ]
    if result["errors"]:
        lines.append("## Errors")
        for error in result["errors"][:160]:
            lines.append(f"- {error}")
        lines.append("")
    if result["warnings"]:
        lines.append("## Warning summary")
        warning_counts = {}
        for warning in result["warnings"]:
            key = warning.split(": ", 1)[1] if ": " in warning else warning
            warning_counts[key] = warning_counts.get(key, 0) + 1
        for key, count in sorted(warning_counts.items(), key=lambda kv: (-kv[1], kv[0])):
            lines.append(f"- {count}× {key}")
        lines.append("")
        lines.append("## Warning sample")
        for warning in result["warnings"][:80]:
            lines.append(f"- {warning}")
        lines.append("")
    lines.append("## Notes")
    lines.append("Missing hreflang is reported as warning so the current release is not blocked while pair coverage is being completed deliberately.")
    (REPORT_DIR / "hreflang_links_audit.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    result = audit()
    write_reports(result)
    if result["status"] != "OK":
        print("FAIL: hreflang audit found broken pairs")
        print(f"errors={len(result['errors'])} warnings={len(result['warnings'])}")
        return 1
    print("OK: hreflang pair targets passed.")
    print(f"pairs={result['pair_count']} warnings={len(result['warnings'])}")
    print("Report: reports/production_next/hreflang_links_audit.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
