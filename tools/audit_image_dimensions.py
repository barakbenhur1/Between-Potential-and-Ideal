#!/usr/bin/env python3
from pathlib import Path
import json, re, sys
ROOT = Path.cwd()
REPORT = ROOT / "reports" / "audit_image_dimensions.json"
IMG_RE = re.compile(r"<img\b([^>]*)>", re.I|re.S)
ATTR_RE = re.compile(r"([\w:-]+)\s*=\s*([\"'])(.*?)\2", re.S)
findings = []
def attrs(raw):
    return {m.group(1).lower(): m.group(3) for m in ATTR_RE.finditer(raw)}
site = ROOT / "site"
if site.exists():
    for p in site.rglob("*.html"):
        s = p.read_text(encoding="utf-8", errors="ignore")
        for m in IMG_RE.finditer(s):
            a = attrs(m.group(1))
            src = a.get("src","")
            cls = a.get("class","")
            alt = a.get("alt","")
            important = any(x in (src + " " + cls + " " + alt).lower() for x in ["hero", "cover", "homepage", "opening"])
            if important and ("width" not in a or "height" not in a):
                findings.append({"path": str(p.relative_to(ROOT)), "src": src, "issue": "important image missing width/height"})
REPORT.parent.mkdir(parents=True, exist_ok=True)
REPORT.write_text(json.dumps({"status": "fail" if findings else "ok", "findings": findings}, ensure_ascii=False, indent=2), encoding="utf-8")
if findings:
    print(f"FAIL: important images missing dimensions: {len(findings)}")
    for f in findings[:80]:
        print("-", f["path"], f["src"])
    sys.exit(1)
print("OK: important images include width/height")
