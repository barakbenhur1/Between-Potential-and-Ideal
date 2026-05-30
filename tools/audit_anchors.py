from pathlib import Path
from html import unescape
import re
import json

SITE = Path("site")
REPORT = Path("reports/audit_anchors.json")

ID_RE = re.compile(r'\bid=["\']([^"\']+)["\']', re.I)
HREF_RE = re.compile(r'\bhref=["\']#([^"\']+)["\']', re.I)

def main():
    results = []
    total_missing = 0
    total_duplicate_ids = 0

    for path in sorted(SITE.rglob("*.html")):
        html = path.read_text(encoding="utf-8", errors="ignore")
        ids_raw = [unescape(x) for x in ID_RE.findall(html)]
        ids = set(ids_raw)

        duplicates = sorted(set(x for x in ids_raw if ids_raw.count(x) > 1))
        missing = []

        for href in [unescape(x) for x in HREF_RE.findall(html)]:
            if href and href not in ids and href not in missing:
                missing.append(href)

        if missing or duplicates:
            results.append({
                "file": str(path),
                "missing_anchor_targets": missing,
                "duplicate_ids": duplicates,
            })
            total_missing += len(missing)
            total_duplicate_ids += len(duplicates)

    report = {
        "files_with_issues": len(results),
        "total_missing_anchor_targets": total_missing,
        "total_duplicate_ids": total_duplicate_ids,
        "issues": results,
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    if results:
        print("FAIL: anchor issues found")
        for r in results[:80]:
            print(r["file"])
            for x in r["missing_anchor_targets"][:20]:
                print("  missing:", "#" + x)
            for x in r["duplicate_ids"][:20]:
                print("  duplicate id:", x)
        print("Report:", REPORT)
        raise SystemExit(1)

    print("OK: all same-page anchors point to existing IDs and no duplicate IDs found.")
    print("Report:", REPORT)

if __name__ == "__main__":
    main()
