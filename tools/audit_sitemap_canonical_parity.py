#!/usr/bin/env python3
from pathlib import Path
from urllib.parse import urlparse
import json, re, sys
ROOT = Path.cwd()
BASE = "https://between-potential-and-ideal.onrender.com"
sitemap = ROOT / "site/sitemap.xml"
REPORT = ROOT / "reports" / "audit_sitemap_canonical_parity.json"
findings = []
if not sitemap.exists():
    findings.append({"path": "site/sitemap.xml", "issue": "missing sitemap"})
else:
    xml = sitemap.read_text(encoding="utf-8", errors="ignore")
    locs = re.findall(r"<loc>(.*?)</loc>", xml)
    seen = set()
    for loc in locs:
        if loc in seen:
            findings.append({"url": loc, "issue": "duplicate sitemap URL"})
        seen.add(loc)
        parsed = urlparse(loc)
        path = parsed.path
        local = ROOT / "site" / path.lstrip("/")
        if path in ("", "/"):
            local = ROOT / "site/index.html"
        elif path.endswith("/"):
            local = ROOT / "site" / path.lstrip("/") / "index.html"
        if local.suffix == "":
            local = local.with_suffix(".html")
        if not local.exists():
            findings.append({"url": loc, "issue": "local file missing for sitemap URL"})
            continue
        if local.suffix.lower() == ".html":
            s = local.read_text(encoding="utf-8", errors="ignore")
            m = re.search(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)["\']', s, flags=re.I)
            if m and m.group(1).rstrip("/") != loc.rstrip("/"):
                findings.append({"url": loc, "issue": f"canonical mismatch: {m.group(1)}", "path": str(local.relative_to(ROOT))})
    if BASE + "/index.html" in locs and BASE + "/" in locs:
        findings.append({"url": BASE + "/index.html", "issue": "sitemap contains both / and /index.html"})
REPORT.parent.mkdir(parents=True, exist_ok=True)
REPORT.write_text(json.dumps({"status": "fail" if findings else "ok", "findings": findings}, ensure_ascii=False, indent=2), encoding="utf-8")
if findings:
    print(f"FAIL: sitemap/canonical findings: {len(findings)}")
    for f in findings[:80]:
        print("-", f)
    sys.exit(1)
print("OK: sitemap canonical parity passed")
