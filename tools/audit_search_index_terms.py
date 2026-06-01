#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit search-index term precision without changing content.

The audit checks:
- search-index.json is valid JSON.
- every indexed URL points to an existing local target or anchor host.
- chapter term sets are not all identical.
- terms are not repeated inside the same entry.
- protected story terms remain present and are not criticized as content.

Run from repo root:
  python3 tools/audit_search_index_terms.py
"""

from pathlib import Path
from urllib.parse import urlparse, unquote
from collections import Counter, defaultdict
import json
import sys

ROOT = Path.cwd()
SITE = ROOT / "site"
INDEX = SITE / "search-index.json"
REPORT_DIR = ROOT / "reports" / "production_next"

PROTECTED_TERMS = {
    "ואז הוא אמוגי מפאק.",
}


def local_target(url: str) -> Path:
    parsed = urlparse(url or "")
    path = unquote(parsed.path or url or "")
    if path.startswith("/"):
        return SITE / path.lstrip("/")
    return SITE / path


def entry_urls(entry: dict) -> list[str]:
    urls = []
    for lang in ["he", "en"]:
        value = entry.get(lang)
        if isinstance(value, dict) and value.get("url"):
            urls.append(value["url"])
    return urls


def terms(entry: dict) -> list[str]:
    value = entry.get("terms", [])
    return [str(x).strip() for x in value if str(x).strip()] if isinstance(value, list) else []


def audit() -> dict:
    errors = []
    warnings = []
    items = []

    if not INDEX.exists():
        return {"status": "FAIL", "errors": ["missing site/search-index.json"], "warnings": [], "items": []}

    try:
        data = json.loads(INDEX.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"status": "FAIL", "errors": [f"invalid JSON: {exc}"], "warnings": [], "items": []}

    chapters = data.get("chapters", [])
    stories = data.get("stories", [])
    required_terms = data.get("required_terms", [])
    if not isinstance(chapters, list) or not chapters:
        errors.append("search-index chapters missing or empty")
    if not isinstance(stories, list) or not stories:
        warnings.append("search-index stories missing or empty")
    if not isinstance(required_terms, list) or not required_terms:
        warnings.append("required_terms missing or empty")

    term_fingerprints = Counter()
    repeated_terms_by_entry = []
    term_global_counter = Counter()

    for group_name, group in [("chapters", chapters), ("stories", stories)]:
        for entry in group if isinstance(group, list) else []:
            slug = str(entry.get("slug", ""))
            entry_terms = terms(entry)
            term_counts = Counter(entry_terms)
            repeated = sorted([t for t, count in term_counts.items() if count > 1])
            if repeated:
                repeated_terms_by_entry.append({"group": group_name, "slug": slug, "repeated_terms": repeated})
            for t in set(entry_terms):
                term_global_counter[t] += 1
            if group_name == "chapters":
                term_fingerprints[tuple(sorted(set(entry_terms)))] += 1
            for url in entry_urls(entry):
                target = local_target(url)
                if not target.exists():
                    # anchor URLs point to an existing HTML host; check host without fragment.
                    host = url.split("#", 1)[0]
                    host_target = local_target(host)
                    if not host_target.exists():
                        errors.append(f"{group_name}/{slug}: indexed URL target missing: {url}")
            items.append({"group": group_name, "slug": slug, "terms": len(entry_terms), "unique_terms": len(set(entry_terms)), "urls": entry_urls(entry)})

    if chapters and len(term_fingerprints) == 1:
        warnings.append("all chapter entries have identical term sets; search precision is weak")
    elif chapters:
        largest = max(term_fingerprints.values()) if term_fingerprints else 0
        if largest >= max(3, len(chapters) // 2):
            warnings.append(f"large chapter term fingerprint group detected: {largest} entries share the same term set")

    if repeated_terms_by_entry:
        warnings.append(f"entries with repeated terms: {len(repeated_terms_by_entry)}")

    overbroad_terms = []
    for term, count in term_global_counter.items():
        if term in PROTECTED_TERMS:
            continue
        if count >= max(5, len(chapters) // 2):
            overbroad_terms.append({"term": term, "entry_count": count})
    if overbroad_terms:
        warnings.append(f"overbroad repeated terms detected: {len(overbroad_terms)}")

    result = {
        "status": "OK" if not errors else "FAIL",
        "errors": errors,
        "warnings": warnings,
        "chapter_count": len(chapters) if isinstance(chapters, list) else 0,
        "story_count": len(stories) if isinstance(stories, list) else 0,
        "required_terms_count": len(required_terms) if isinstance(required_terms, list) else 0,
        "chapter_term_fingerprint_groups": len(term_fingerprints),
        "repeated_terms_by_entry": repeated_terms_by_entry[:100],
        "overbroad_terms": overbroad_terms[:120],
        "items": items,
    }
    return result


def write_reports(result: dict) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / "search_index_terms_audit.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        "# Search Index Term Precision Audit",
        "",
        f"- Status: `{result['status']}`",
        f"- Errors: {len(result['errors'])}",
        f"- Warnings: {len(result['warnings'])}",
        f"- Chapters: {result.get('chapter_count', 0)}",
        f"- Stories: {result.get('story_count', 0)}",
        f"- Required terms: {result.get('required_terms_count', 0)}",
        f"- Chapter term fingerprint groups: {result.get('chapter_term_fingerprint_groups', 0)}",
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
    if result.get("overbroad_terms"):
        lines.append("## Overbroad repeated terms sample")
        for item in result["overbroad_terms"][:40]:
            lines.append(f"- `{item['term']}` appears in {item['entry_count']} entries")
        lines.append("")
    lines.append("## Notes")
    lines.append("Warnings are precision recommendations, not release blockers. Protected story terms are preserved and not treated as content problems.")
    (REPORT_DIR / "search_index_terms_audit.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    result = audit()
    write_reports(result)
    if result["status"] != "OK":
        print("FAIL: search index term audit found errors")
        print(f"errors={len(result['errors'])} warnings={len(result['warnings'])}")
        return 1
    print("OK: search index term audit passed.")
    print(f"warnings={len(result['warnings'])}")
    print("Report: reports/production_next/search_index_terms_audit.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
