#!/usr/bin/env python3
from pathlib import Path
import json, re, sys
ROOT = Path.cwd()
REPORT = ROOT / "reports" / "audit_static_blank_targets.json"
A_RE = re.compile(r"<a\b([^>]*)>", re.I|re.S)
ATTR_RE = re.compile(r"([\w:-]+)\s*=\s*([\"'])(.*?)\2", re.S)
findings=[]
def attrs(raw):
    return {m.group(1).lower(): m.group(3) for m in ATTR_RE.finditer(raw)}
site = ROOT / "site"
if site.exists():
    for p in site.rglob("*.html"):
        s=p.read_text(encoding="utf-8", errors="ignore")
        for m in A_RE.finditer(s):
            a=attrs(m.group(1))
            if a.get("target") == "_blank":
                rel=a.get("rel","")
                if "noopener" not in rel or "noreferrer" not in rel:
                    findings.append({"path": str(p.relative_to(ROOT)), "href": a.get("href",""), "rel": rel, "issue": "_blank missing noopener noreferrer"})
REPORT.parent.mkdir(parents=True, exist_ok=True)
REPORT.write_text(json.dumps({"status":"fail" if findings else "ok","findings":findings}, ensure_ascii=False, indent=2), encoding="utf-8")
if findings:
    print(f"FAIL: _blank rel findings: {len(findings)}")
    for f in findings[:80]:
        print("-", f["path"], f["href"], f["rel"])
    sys.exit(1)
print("OK: all target=_blank links include noopener noreferrer")
