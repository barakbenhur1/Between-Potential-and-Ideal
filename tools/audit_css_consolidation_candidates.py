#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit CSS consolidation opportunities without changing protected design.

Phase 14 is intentionally conservative. This audit reports safe candidates for
future consolidation, but does not rewrite HTML/CSS. It checks:
- total CSS files
- embedded <style> blocks in HTML
- inline style attributes
- exact and normalized duplicate embedded style blocks
- exact and normalized duplicate inline style values
- very large style blocks / high !important density

Protected-elements policy:
This tool must not criticize or rewrite approved body content, blurbs, arrows,
Author's Note styling, story symbols, TOC markers, or document wording. It only
reports technical CSS duplication and risk so future changes can be reviewed
visually before applying.

Run from repo root:
  python3 tools/audit_css_consolidation_candidates.py
"""

from __future__ import annotations

from pathlib import Path
from collections import defaultdict, Counter
import hashlib
import html
import json
import re
import sys

ROOT = Path.cwd()
SITE = ROOT / "site"
REPORT_DIR = ROOT / "reports" / "production_next"
STYLE_BLOCK_RE = re.compile(r"<style\b(?P<attrs>[^>]*)>(?P<body>.*?)</style>", re.I | re.S)
STYLE_ATTR_RE = re.compile(r"\bstyle\s*=\s*(['\"])(?P<value>.*?)\1", re.I | re.S)
COMMENT_RE = re.compile(r"/\*.*?\*/", re.S)
WS_RE = re.compile(r"\s+")

# Pages/files whose visual layout has repeatedly been intentionally protected.
PROTECTED_HINTS = [
    "author-note",
    "gveret",
    "stories-before-thought",
    "appendices",
    "between-potential-and-ideal",
    "document-reading-direction-fix.css",
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def stable_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8", errors="ignore")).hexdigest()[:12]


def normalize_css(value: str) -> str:
    value = html.unescape(value or "")
    value = COMMENT_RE.sub("", value)
    value = value.replace("\r\n", "\n").replace("\r", "\n")
    value = WS_RE.sub(" ", value).strip()
    value = re.sub(r"\s*([{}:;,>+~])\s*", r"\1", value)
    return value.lower()


def is_protected_path(path: Path) -> bool:
    r = rel(path).lower()
    return any(hint in r for hint in PROTECTED_HINTS)


def collect() -> dict:
    css_files = list(sorted(SITE.rglob("*.css"))) if SITE.exists() else []
    html_files = list(sorted(SITE.rglob("*.html"))) if SITE.exists() else []

    exact_style_blocks: dict[str, list[dict]] = defaultdict(list)
    normalized_style_blocks: dict[str, list[dict]] = defaultdict(list)
    exact_inline_styles: dict[str, list[dict]] = defaultdict(list)
    normalized_inline_styles: dict[str, list[dict]] = defaultdict(list)

    style_block_count = 0
    inline_attr_count = 0
    embedded_chars = 0
    inline_chars = 0
    important_count = 0
    large_style_blocks = []
    many_inline_style_pages = []

    for path in html_files:
        text = path.read_text(encoding="utf-8", errors="ignore")
        page_inline_count = 0
        for idx, m in enumerate(STYLE_BLOCK_RE.finditer(text), start=1):
            body = m.group("body") or ""
            style_block_count += 1
            embedded_chars += len(body)
            important_count += body.count("!important")
            exact_key = stable_hash(body)
            norm = normalize_css(body)
            norm_key = stable_hash(norm)
            rec = {"path": rel(path), "index": idx, "chars": len(body), "important": body.count("!important"), "protected_hint": is_protected_path(path)}
            exact_style_blocks[exact_key].append(rec)
            normalized_style_blocks[norm_key].append(rec)
            if len(body) >= 5000 or body.count("!important") >= 50:
                large_style_blocks.append(rec)
        for idx, m in enumerate(STYLE_ATTR_RE.finditer(text), start=1):
            value = m.group("value") or ""
            inline_attr_count += 1
            page_inline_count += 1
            inline_chars += len(value)
            important_count += value.count("!important")
            exact_key = stable_hash(value)
            norm = normalize_css(value)
            norm_key = stable_hash(norm)
            rec = {"path": rel(path), "index": idx, "chars": len(value), "important": value.count("!important"), "protected_hint": is_protected_path(path)}
            exact_inline_styles[exact_key].append(rec)
            normalized_inline_styles[norm_key].append(rec)
        if page_inline_count >= 50:
            many_inline_style_pages.append({"path": rel(path), "inline_style_attrs": page_inline_count, "protected_hint": is_protected_path(path)})

    def selected_groups(groups: dict[str, list[dict]], min_count: int, min_chars: int = 0) -> list[dict]:
        out = []
        for key, rows in groups.items():
            if len(rows) < min_count:
                continue
            max_chars = max((r["chars"] for r in rows), default=0)
            if max_chars < min_chars:
                continue
            out.append({
                "hash": key,
                "count": len(rows),
                "max_chars": max_chars,
                "total_chars": sum(r["chars"] for r in rows),
                "protected_occurrences": sum(1 for r in rows if r["protected_hint"]),
                "sample": rows[:8],
            })
        return sorted(out, key=lambda g: (-g["total_chars"], -g["count"], g["hash"]))

    result = {
        "status": "OK",
        "css_files": len(css_files),
        "html_files": len(html_files),
        "style_blocks": style_block_count,
        "inline_style_attrs": inline_attr_count,
        "embedded_style_chars": embedded_chars,
        "inline_style_chars": inline_chars,
        "important_declarations_estimate": important_count,
        "large_style_blocks": large_style_blocks[:120],
        "many_inline_style_pages": many_inline_style_pages[:120],
        "exact_duplicate_style_block_groups": selected_groups(exact_style_blocks, min_count=2, min_chars=300),
        "normalized_duplicate_style_block_groups": selected_groups(normalized_style_blocks, min_count=2, min_chars=300),
        "exact_duplicate_inline_style_groups": selected_groups(exact_inline_styles, min_count=25, min_chars=20),
        "normalized_duplicate_inline_style_groups": selected_groups(normalized_inline_styles, min_count=25, min_chars=20),
    }
    return result


def write_reports(result: dict) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / "css_consolidation_candidates_audit.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# CSS Consolidation Candidates Audit",
        "",
        f"- Status: `{result['status']}`",
        f"- CSS files: {result['css_files']}",
        f"- HTML files: {result['html_files']}",
        f"- Embedded `<style>` blocks: {result['style_blocks']}",
        f"- Inline `style=` attributes: {result['inline_style_attrs']}",
        f"- Embedded style chars: {result['embedded_style_chars']}",
        f"- Inline style chars: {result['inline_style_chars']}",
        f"- `!important` estimate: {result['important_declarations_estimate']}",
        f"- Exact duplicate style-block groups: {len(result['exact_duplicate_style_block_groups'])}",
        f"- Normalized duplicate style-block groups: {len(result['normalized_duplicate_style_block_groups'])}",
        f"- Exact duplicate inline-style groups: {len(result['exact_duplicate_inline_style_groups'])}",
        f"- Normalized duplicate inline-style groups: {len(result['normalized_duplicate_inline_style_groups'])}",
        "",
        "## Risk policy",
        "This audit is advisory. Do not consolidate CSS touching Author's Note, story documents, TOC, Gveret Levin, or long document layout without visual QA.",
        "",
    ]

    if result["large_style_blocks"]:
        lines.append("## Large/high-important style blocks sample")
        for row in result["large_style_blocks"][:40]:
            prot = " protected-hint" if row["protected_hint"] else ""
            lines.append(f"- `{row['path']}` style#{row['index']} chars={row['chars']} important={row['important']}{prot}")
        lines.append("")

    for title, key in [
        ("Normalized duplicate style-block groups", "normalized_duplicate_style_block_groups"),
        ("Normalized duplicate inline-style groups", "normalized_duplicate_inline_style_groups"),
    ]:
        groups = result[key]
        if not groups:
            continue
        lines.append(f"## {title} sample")
        for group in groups[:30]:
            lines.append(f"- hash=`{group['hash']}` count={group['count']} total_chars={group['total_chars']} protected_occurrences={group['protected_occurrences']}")
            for sample in group["sample"][:3]:
                prot = " protected-hint" if sample["protected_hint"] else ""
                lines.append(f"  - `{sample['path']}` #{sample['index']} chars={sample['chars']}{prot}")
        lines.append("")

    lines.append("## Recommendation")
    lines.append("Continue with scan-first consolidation only. Extract a group only if it has low protected-occurrence risk and visual QA confirms no layout regression.")
    (REPORT_DIR / "css_consolidation_candidates_audit.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    result = collect()
    write_reports(result)
    print("OK: CSS consolidation candidates audit completed.")
    print(f"css_files={result['css_files']} html_files={result['html_files']} style_blocks={result['style_blocks']} inline_styles={result['inline_style_attrs']}")
    print("Report: reports/production_next/css_consolidation_candidates_audit.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
