#!/usr/bin/env python3
from pathlib import Path
import json, sys
ROOT = Path.cwd()
REPORT = ROOT / "reports" / "audit_document_backbars_i18n.json"
findings = []
base = ROOT / "site/files"
if base.exists():
    for p in base.rglob("*.html"):
        s = p.read_text(encoding="utf-8", errors="ignore")
        rel = str(p.relative_to(ROOT))
        if rel.endswith("-en.html") or "/en" in rel:
            if 'href="../../index.html">Back to site' in s or "href='../../index.html'>Back to site" in s:
                findings.append({"path": rel, "issue": "English document backbar points to Hebrew home"})
            if 'href="../../pages/en/files.html">All files' in s or "href='../../pages/en/files.html'>All files" in s:
                findings.append({"path": rel, "issue": "English document All files points to pages/en/files.html instead of files-en.html"})
REPORT.parent.mkdir(parents=True, exist_ok=True)
REPORT.write_text(json.dumps({"status": "fail" if findings else "ok", "findings": findings}, ensure_ascii=False, indent=2), encoding="utf-8")
if findings:
    print(f"FAIL: i18n backbar findings: {len(findings)}")
    for f in findings[:80]:
        print("-", f["path"], f["issue"])
    sys.exit(1)
print("OK: document backbars match expected language routing")
