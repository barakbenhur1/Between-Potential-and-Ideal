#!/usr/bin/env python3
from pathlib import Path
import json, re
ROOT = Path.cwd()
REPORT = ROOT / "reports" / "audit_css_patch_blocks.json"
STYLE_RE = re.compile(r"<style\b([^>]*)>(.*?)</style>", re.I|re.S)
ID_RE = re.compile(r"id=[\"']([^\"']+)[\"']", re.I)
items = []
site = ROOT / "site"
if site.exists():
    for p in site.rglob("*.html"):
        s = p.read_text(encoding="utf-8", errors="ignore")
        for i, m in enumerate(STYLE_RE.finditer(s), 1):
            attrs, body = m.group(1), m.group(2)
            im = ID_RE.search(attrs)
            sid = im.group(1) if im else f"[no-id-{i}]"
            risky = bool(re.search(r"\bv\d+\b|final|fix|override|cleanup|patch", sid + " " + body[:300], re.I))
            items.append({"path": str(p.relative_to(ROOT)), "style_id": sid, "lines": body.count("\n") + 1, "important_count": body.count("!important"), "risky_patch_name": risky})
REPORT.parent.mkdir(parents=True, exist_ok=True)
REPORT.write_text(json.dumps({"status": "ok", "style_blocks": items, "count": len(items)}, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"OK: CSS patch block audit wrote {len(items)} style blocks to {REPORT}")
