#!/usr/bin/env python3
from pathlib import Path
from urllib.parse import urlparse
import json, sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "localization/config.json"
MANIFEST = ROOT / "localization/translation-manifest.json"
REPORT = ROOT / "reports/localization/parity.json"
NS = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}


def rel(path):
    return path.relative_to(ROOT).as_posix()


def exists(path):
    return {"path": rel(path), "exists": path.is_file(), "bytes": path.stat().st_size if path.is_file() else 0}


def source_status(path):
    if not path.is_file():
        return "missing"
    text = path.read_text(encoding="utf-8", errors="ignore")
    if not text.startswith("---\n"):
        return "invalid"
    try:
        meta = text.split("---\n", 2)[1]
    except IndexError:
        return "invalid"
    for line in meta.splitlines():
        key, sep, value = line.partition(":")
        if sep and key.strip() == "status":
            return value.strip()
    return "missing-status"


def page_pairs(sitemap):
    paths = {
        urlparse(node.text.strip()).path or "/"
        for node in ET.parse(sitemap).findall("s:url/s:loc", NS)
        if node.text
    }
    he = {p[10:-5] for p in paths if p.startswith("/pages/he/") and p.endswith(".html")}
    en = {p[10:-8] for p in paths if p.startswith("/pages/en/") and p.endswith("-en.html")}
    errors = []
    if "/" not in paths or "/en.html" not in paths:
        errors.append("sitemap home pair is incomplete")
    pairs = [("home", ROOT / "site/index.html", ROOT / "site/en.html")]
    for slug in sorted(he | en):
        if slug not in he:
            errors.append(f"missing Hebrew sitemap partner: {slug}")
        if slug not in en:
            errors.append(f"missing English sitemap partner: {slug}")
        pairs.append((slug, ROOT / f"site/pages/he/{slug}.html", ROOT / f"site/pages/en/{slug}-en.html"))
    return pairs, errors


def audit_language(code, cfg, manifest, pairs):
    lang = cfg["languages"][code]
    missing, source_issues, page_items, packages = [], [], [], []
    for slug, _, _ in pairs:
        target = ROOT / lang["home"] if slug == "home" else ROOT / lang["pages_dir"] / f"{slug}.html"
        item = exists(target); item["id"] = slug; page_items.append(item)
        if not item["exists"]: missing.append(item["path"])
    for package in manifest["document_packages"]:
        source = ROOT / f"localization/sources/{code}/{package}-{code}.md"
        status = source_status(source)
        if status != "approved": source_issues.append(f"{rel(source)} status={status}")
        formats = []
        for fmt in cfg["required_download_formats"]:
            item = exists(ROOT / lang["files_dir"] / f"{package}-{code}.{fmt}")
            formats.append(item)
            if not item["exists"]: missing.append(item["path"])
        packages.append({"package": package, "source_status": status, "formats": formats})
    incomplete = missing + source_issues
    return {
        "code": code,
        "publish": bool(lang.get("publish")),
        "required_pages": len(pairs),
        "pages": page_items,
        "packages": packages,
        "missing_files": missing,
        "source_issues": source_issues,
        "blockers": incomplete if lang.get("publish") else [],
        "warnings": [] if lang.get("publish") else incomplete,
    }


def main():
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    pairs, source_errors = page_pairs(ROOT / manifest["public_pages_source"])
    for slug, he, en in pairs:
        if not he.is_file(): source_errors.append(f"missing source: {rel(he)}")
        if not en.is_file(): source_errors.append(f"missing source: {rel(en)}")
    languages = [audit_language(code, cfg, manifest, pairs) for code in ("tlh", "qya")]
    blockers = source_errors + [x for lang in languages for x in lang["blockers"]]
    result = {"status": "FAIL" if blockers else "OK", "source_pairs": len(pairs), "source_errors": source_errors, "languages": languages, "blockers": blockers}
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"source_pairs={len(pairs)} source_errors={len(source_errors)}")
    for lang in languages:
        print(f"{lang['code']}: publish={lang['publish']} missing={len(lang['missing_files'])} source_issues={len(lang['source_issues'])}")
    print("Report:", rel(REPORT))
    return 1 if blockers else 0


if __name__ == "__main__":
    sys.exit(main())
