#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit runtime JavaScript scope before splitting page scripts.

This is the safe Phase 13 guard. It does not rewrite HTML yet. It reports:
- inline script counts per HTML page
- pages that use MutationObserver
- pages that inject runtime CSS with createElement('style')
- whether the English Files UI runtime guard is scoped only to files-en.html

Protected-elements policy:
The audit does not inspect or criticize blurbs, arrows, symbolic markers,
Author's Note styling, or approved document wording.

Run from repo root:
  python3 tools/audit_runtime_js_scope.py
"""

from pathlib import Path
import json
import re
import sys

ROOT = Path.cwd()
SITE = ROOT / "site"
REPORT_DIR = ROOT / "reports" / "production_next"
SCRIPT_RE = re.compile(r"<script\b(?P<attrs>[^>]*)>(?P<body>.*?)</script>", re.I | re.S)
SRC_RE = re.compile(r"\bsrc\s*=\s*['\"]([^'\"]+)['\"]", re.I)

ENGLISH_FILES_GUARD = "data-bpi-english-files-ui-runtime-guard"


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def script_items(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    items = []
    for match in SCRIPT_RE.finditer(text):
        attrs = match.group("attrs") or ""
        body = match.group("body") or ""
        src_match = SRC_RE.search(attrs)
        items.append({
            "external": bool(src_match),
            "src": src_match.group(1) if src_match else "",
            "attrs": re.sub(r"\s+", " ", attrs).strip()[:240],
            "chars": len(body),
            "uses_mutation_observer": "MutationObserver" in body,
            "uses_style_injection": "createElement(\"style\")" in body or "createElement('style')" in body,
            "has_english_files_guard": ENGLISH_FILES_GUARD in attrs or ENGLISH_FILES_GUARD in body,
        })
    return items


def audit() -> dict:
    errors = []
    warnings = []
    items = []
    guard_hosts = []
    style_injection_hosts = []
    mutation_hosts = []
    inline_script_pages = []

    for path in sorted(SITE.rglob("*.html")) if SITE.exists() else []:
        scripts = script_items(path)
        if not scripts:
            continue
        inline_count = sum(1 for s in scripts if not s["external"])
        external_count = sum(1 for s in scripts if s["external"])
        if inline_count:
            inline_script_pages.append(rel(path))
        if any(s["has_english_files_guard"] for s in scripts):
            guard_hosts.append(rel(path))
        if any(s["uses_style_injection"] for s in scripts):
            style_injection_hosts.append(rel(path))
        if any(s["uses_mutation_observer"] for s in scripts):
            mutation_hosts.append(rel(path))
        items.append({
            "path": rel(path),
            "inline_scripts": inline_count,
            "external_scripts": external_count,
            "uses_mutation_observer": any(s["uses_mutation_observer"] for s in scripts),
            "uses_style_injection": any(s["uses_style_injection"] for s in scripts),
            "has_english_files_guard": any(s["has_english_files_guard"] for s in scripts),
        })

    expected_guard_host = "site/pages/en/files-en.html"
    if guard_hosts != [expected_guard_host]:
        errors.append(f"English files runtime guard should be scoped only to {expected_guard_host}; found {guard_hosts}")
    if style_injection_hosts:
        warnings.append(f"runtime CSS injection hosts: {len(style_injection_hosts)}")
    if inline_script_pages:
        warnings.append(f"pages with inline scripts: {len(inline_script_pages)}")
    if mutation_hosts:
        warnings.append(f"MutationObserver hosts: {len(mutation_hosts)}")

    return {
        "status": "OK" if not errors else "FAIL",
        "errors": errors,
        "warnings": warnings,
        "pages_with_scripts": len(items),
        "inline_script_pages": inline_script_pages[:200],
        "style_injection_hosts": style_injection_hosts[:200],
        "mutation_hosts": mutation_hosts[:200],
        "guard_hosts": guard_hosts,
        "items": items,
    }


def write_reports(result: dict) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / "runtime_js_scope_audit.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        "# Runtime JavaScript Scope Audit",
        "",
        f"- Status: `{result['status']}`",
        f"- Errors: {len(result['errors'])}",
        f"- Warnings: {len(result['warnings'])}",
        f"- Pages with scripts: {result['pages_with_scripts']}",
        f"- English files guard hosts: {result['guard_hosts']}",
        f"- MutationObserver hosts: {len(result['mutation_hosts'])}",
        f"- Runtime CSS injection hosts: {len(result['style_injection_hosts'])}",
        "",
    ]
    if result["errors"]:
        lines.append("## Errors")
        for error in result["errors"]:
            lines.append(f"- {error}")
        lines.append("")
    if result["warnings"]:
        lines.append("## Warnings")
        for warning in result["warnings"]:
            lines.append(f"- {warning}")
        lines.append("")
    if result["style_injection_hosts"]:
        lines.append("## Runtime CSS injection hosts")
        for path in result["style_injection_hosts"][:80]:
            lines.append(f"- `{path}`")
        lines.append("")
    if result["mutation_hosts"]:
        lines.append("## MutationObserver hosts")
        for path in result["mutation_hosts"][:80]:
            lines.append(f"- `{path}`")
        lines.append("")
    lines.append("## Recommendation")
    lines.append("Do not split scripts blindly. First preserve behavior with page-scoped external files, then remove inline code only after visual and release QA pass.")
    (REPORT_DIR / "runtime_js_scope_audit.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    result = audit()
    write_reports(result)
    if result["status"] != "OK":
        print("FAIL: runtime JS scope audit found errors")
        print(f"errors={len(result['errors'])} warnings={len(result['warnings'])}")
        return 1
    print("OK: runtime JS scope audit passed.")
    print(f"warnings={len(result['warnings'])}")
    print("Report: reports/production_next/runtime_js_scope_audit.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
