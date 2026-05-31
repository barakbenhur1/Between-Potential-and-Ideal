#!/usr/bin/env python3
from pathlib import Path
import json, re, sys
ROOT = Path.cwd()
REPORT = ROOT / "reports" / "audit_public_backup_files.json"
PATTERNS = [
    re.compile(r"\.bak($|\.)", re.I),
    re.compile(r"\.old($|\.)", re.I),
    re.compile(r"\.orig($|\.)", re.I),
    re.compile(r"(^|[-_. ])backup(s)?($|[-_. ])", re.I),
    re.compile(r"(^|[-_. ])tmp($|[-_. ])", re.I),
    re.compile(r" copy(\.|$)", re.I),
    re.compile(r"\.DS_Store$", re.I),
]
findings = []
site = ROOT / "site"
if site.exists():
    for p in site.rglob("*"):
        if p.is_file() and any(rx.search(p.name) for rx in PATTERNS):
            findings.append({"path": str(p.relative_to(ROOT)), "reason": "backup/temp-like file under public site/"})
REPORT.parent.mkdir(parents=True, exist_ok=True)
REPORT.write_text(json.dumps({"status": "fail" if findings else "ok", "findings": findings}, ensure_ascii=False, indent=2), encoding="utf-8")
if findings:
    print(f"FAIL: public backup/temp-like files found: {len(findings)}")
    for f in findings[:80]:
        print("-", f["path"])
    sys.exit(1)
print("OK: no public backup/temp-like files under site/")
