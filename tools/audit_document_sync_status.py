#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Final document sync status audit.

Phase 15 guard:
- verifies known public HTML document packages have expected sibling formats
- verifies sibling files are non-empty and roughly plausible in size
- verifies TXT/MD siblings are not older-looking tiny placeholders
- does not rewrite or inspect protected literary/philosophical body content

This is a structural sync check, not a content editor. It deliberately avoids
criticizing blurbs, arrows, Author's Note styling, story endings, symbols,
markers, or approved design choices.

Run from repo root:
  python3 tools/audit_document_sync_status.py
"""

from __future__ import annotations

from pathlib import Path
import json
import sys

ROOT = Path.cwd()
SITE = ROOT / "site"
REPORT_DIR = ROOT / "reports" / "production_next"
FORMATS = [".html", ".txt", ".md", ".docx", ".pdf"]

# Core public document packages that should remain synchronized across formats.
TARGET_STEMS = [
    "site/files/between-potential-and-ideal-en",
    "site/files/between-potential-and-ideal-he",
    "site/files/between-potential-and-ideal-en-editorial",
    "site/files/between-potential-and-ideal-he-editorial",
    "site/files/editorial-tightened/between-potential-and-ideal-tightened-en",
    "site/files/editorial-tightened/between-potential-and-ideal-tightened-he",
    "site/files/editorial-tightened/editorial-report-en",
    "site/files/editorial-tightened/editorial-report-he",
    "site/files/appendices/stories-before-thought-english",
    "site/files/appendices/stories-before-thought-hebrew-rtl",
    "site/files/appendices/haemet_hamavchila_final_publication_he",
    "site/files/ai-believes/what-ai-believes-en",
    "site/files/ai-believes/what-ai-believes-he",
    "site/files/ai-believes/when-i-am-also-you-en",
    "site/files/ai-believes/when-i-am-also-you-he",
    "site/files/ai-believes/reverse-turing-conversation-en",
    "site/files/ai-believes/reverse-turing-conversation-he",
]

# Minimum sizes are intentionally conservative; they catch empty/broken outputs only.
MIN_BYTES = {
    ".html": 1000,
    ".txt": 500,
    ".md": 500,
    ".docx": 5000,
    ".pdf": 5000,
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def audit_package(stem: str) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    files = {}
    for ext in FORMATS:
        path = ROOT / (stem + ext)
        info = {"path": rel(path), "exists": path.exists(), "bytes": path.stat().st_size if path.exists() and path.is_file() else 0}
        files[ext] = info
        if not path.exists():
            errors.append(f"missing {ext}")
        elif not path.is_file():
            errors.append(f"{ext} is not a file")
        elif info["bytes"] < MIN_BYTES[ext]:
            errors.append(f"{ext} is suspiciously small: {info['bytes']} bytes")

    html_bytes = files[".html"]["bytes"]
    txt_bytes = files[".txt"]["bytes"]
    md_bytes = files[".md"]["bytes"]
    if html_bytes and txt_bytes and txt_bytes < max(500, int(html_bytes * 0.05)):
        warnings.append("TXT is much smaller than HTML; verify this is intentional")
    if html_bytes and md_bytes and md_bytes < max(500, int(html_bytes * 0.05)):
        warnings.append("MD is much smaller than HTML; verify this is intentional")

    return {"stem": stem, "files": files, "errors": errors, "warnings": warnings}


def main() -> int:
    items = [audit_package(stem) for stem in TARGET_STEMS]
    errors = [f"{item['stem']}: {error}" for item in items for error in item["errors"]]
    warnings = [f"{item['stem']}: {warning}" for item in items for warning in item["warnings"]]

    result = {
        "status": "OK" if not errors else "FAIL",
        "packages_checked": len(items),
        "errors": errors,
        "warnings": warnings,
        "items": items,
    }

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / "document_sync_status_audit.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Final Document Sync Status Audit",
        "",
        f"- Status: `{result['status']}`",
        f"- Packages checked: {len(items)}",
        f"- Errors: {len(errors)}",
        f"- Warnings: {len(warnings)}",
        "",
    ]
    if errors:
        lines.append("## Errors")
        for error in errors:
            lines.append(f"- {error}")
        lines.append("")
    if warnings:
        lines.append("## Warnings")
        for warning in warnings[:120]:
            lines.append(f"- {warning}")
        lines.append("")
    lines.append("## Notes")
    lines.append("This audit checks structural package sync only. It does not alter or judge protected content, blurbs, arrows, symbols, or approved design details.")
    (REPORT_DIR / "document_sync_status_audit.md").write_text("\n".join(lines), encoding="utf-8")

    if errors:
        print("FAIL: document sync status audit found errors")
        print(f"errors={len(errors)} warnings={len(warnings)}")
        return 1
    print("OK: document sync status audit passed.")
    print(f"packages_checked={len(items)} warnings={len(warnings)}")
    print("Report: reports/production_next/document_sync_status_audit.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
