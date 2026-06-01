#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Audit the public Files pages and document sibling packages.

Scope:
- Checks local hrefs on `site/pages/en/files-en.html` and `site/pages/he/files.html`.
- Ensures local download targets exist, are files, and are not empty.
- Checks document packages under `site/files/**.html`: if any sibling download format
  exists for a document, all required sibling formats must exist:
  `.txt`, `.md`, `.docx`, `.pdf`.

Protected-elements policy:
This audit does not inspect or criticize blurbs, arrows, symbolic markers, or
approved document styling. It only checks file/link integrity.

Run from repo root:
  python3 tools/audit_file_download_links.py
"""

from __future__ import annotations

from pathlib import Path
from urllib.parse import unquote, urlparse
import html
import json
import re
import sys

ROOT = Path.cwd()
SITE = ROOT / "site"
REPORT_DIR = ROOT / "reports" / "production_next"
FILES_PAGES = [
    SITE / "pages" / "en" / "files-en.html",
    SITE / "pages" / "he" / "files.html",
]
REQUIRED_DOCUMENT_FORMATS = [".txt", ".md", ".docx", ".pdf"]
A_RE = re.compile(r"<a\b(?P<attrs>[^<>]*?)>(?P<body>.*?)</a>", re.I | re.S)
ATTR_RE = re.compile(r'([\w:-]+)\s*=\s*(["\'])(.*?)\2', re.S)
TAG_RE = re.compile(r"<[^>]+>", re.S)


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def parse_attrs(attrs: str) -> dict[str, str]:
    return {m.group(1).lower(): html.unescape(m.group(3)) for m in ATTR_RE.finditer(attrs or "")}


def strip_tags(value: str) -> str:
    value = TAG_RE.sub(" ", value or "")
    return re.sub(r"\s+", " ", html.unescape(value)).strip()


def is_external(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https", "mailto", "tel", "data", "javascript"}


def resolve_local_href(page: Path, href: str) -> Path | None:
    href = html.unescape(href or "").strip()
    if not href or href.startswith("#") or is_external(href):
        return None
    parsed = urlparse(href)
    path_part = unquote(parsed.path or "")
    if not path_part:
        return None
    if path_part.startswith("/"):
        target = SITE / path_part.lstrip("/")
    else:
        target = page.parent / path_part
    return target.resolve()


def audit_files_pages() -> dict:
    items = []
    errors = []
    local_link_count = 0

    for page in FILES_PAGES:
        if not page.exists():
            errors.append({"page": rel(page), "error": "missing Files page"})
            continue
        content = read(page)
        page_items = []
        for match in A_RE.finditer(content):
            attrs = parse_attrs(match.group("attrs") or "")
            href = attrs.get("href", "")
            target = resolve_local_href(page, href)
            if target is None:
                continue
            local_link_count += 1
            text = strip_tags(match.group("body") or "")
            item = {
                "page": rel(page),
                "href": href,
                "text": text[:160],
                "target": str(target),
                "exists": target.exists(),
                "is_file": target.is_file() if target.exists() else False,
                "bytes": target.stat().st_size if target.exists() and target.is_file() else 0,
            }
            if not item["exists"]:
                item["error"] = "missing target"
                errors.append(item)
            elif not item["is_file"]:
                item["error"] = "target is not a file"
                errors.append(item)
            elif item["bytes"] <= 0:
                item["error"] = "target file is empty"
                errors.append(item)
            page_items.append(item)
        items.extend(page_items)

    return {
        "files_pages": [rel(p) for p in FILES_PAGES],
        "local_link_count": local_link_count,
        "errors": errors,
        "items_sample": items[:200],
    }


def is_public_document_html(path: Path) -> bool:
    if not path.is_file() or path.suffix.lower() != ".html":
        return False
    parts = path.parts
    if "site" not in parts or "files" not in parts:
        return False
    name = path.name.lower()
    if any(token in name for token in [".bak", ".old", ".orig", ".tmp", "preview"]):
        return False
    return True


def audit_document_packages() -> dict:
    items = []
    errors = []
    for html_path in sorted((SITE / "files").rglob("*.html")) if (SITE / "files").exists() else []:
        if not is_public_document_html(html_path):
            continue
        siblings = {ext: html_path.with_suffix(ext) for ext in REQUIRED_DOCUMENT_FORMATS}
        exists = {ext: path.exists() for ext, path in siblings.items()}
        # Skip HTML helper pages that do not participate in downloads.
        if not any(exists.values()):
            continue
        missing = [ext for ext, ok in exists.items() if not ok]
        empty = [ext for ext, path in siblings.items() if path.exists() and path.is_file() and path.stat().st_size <= 0]
        item = {
            "html": rel(html_path),
            "exists": exists,
            "missing": missing,
            "empty": empty,
        }
        if missing or empty:
            errors.append(item)
        items.append(item)
    return {
        "documents_checked": len(items),
        "errors": errors,
        "items": items,
    }


def write_reports(result: dict) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / "file_download_links_audit.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    lines = [
        "# File Download Links Audit",
        "",
        f"- Status: `{result['status']}`",
        f"- Errors: {len(result['errors'])}",
        f"- Files-page local links checked: {result['files_pages']['local_link_count']}",
        f"- Document packages checked: {result['document_packages']['documents_checked']}",
        "",
    ]
    if result["errors"]:
        lines.append("## Errors")
        for error in result["errors"][:200]:
            lines.append(f"- `{error.get('page') or error.get('html')}`: {error.get('error') or ''} {error.get('missing') or ''} {error.get('empty') or ''}")
        lines.append("")

    lines += [
        "## Files pages",
        f"- Pages: {', '.join('`' + p + '`' for p in result['files_pages']['files_pages'])}",
        f"- Local links checked: {result['files_pages']['local_link_count']}",
        f"- Link errors: {len(result['files_pages']['errors'])}",
        "",
        "## Document packages",
        f"- Documents checked: {result['document_packages']['documents_checked']}",
        f"- Package errors: {len(result['document_packages']['errors'])}",
        "",
    ]
    if result["status"] == "OK":
        lines.append("All checked file download links and document sibling packages passed.")
    else:
        lines.append("Fix listed errors and rerun `python3 tools/audit_file_download_links.py`.")

    (REPORT_DIR / "file_download_links_audit.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    errors = []
    if not SITE.exists():
        print("FAIL: missing site/ directory")
        return 1

    files_pages = audit_files_pages()
    document_packages = audit_document_packages()
    errors.extend(files_pages["errors"])
    errors.extend(document_packages["errors"])

    result = {
        "status": "OK" if not errors else "FAIL",
        "errors": errors,
        "files_pages": files_pages,
        "document_packages": document_packages,
    }
    write_reports(result)

    if errors:
        print("FAIL: file download audit found issues")
        print(f"errors={len(errors)}")
        print("Report: reports/production_next/file_download_links_audit.md")
        return 1

    print("OK: file download links and document packages passed.")
    print(f"files-page local links checked: {files_pages['local_link_count']}")
    print(f"document packages checked: {document_packages['documents_checked']}")
    print("Report: reports/production_next/file_download_links_audit.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
