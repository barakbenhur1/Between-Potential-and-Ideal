#!/usr/bin/env python3
from pathlib import Path
import json
ROOT = Path.cwd()
REPORT = ROOT / "reports" / "audit_format_parity_matrix.json"
formats = [".html", ".pdf", ".docx", ".md", ".txt"]
groups = {}
base = ROOT / "site/files"
if base.exists():
    for p in base.rglob("*"):
        if not p.is_file() or p.suffix.lower() not in formats:
            continue
        stem = str(p.with_suffix("").relative_to(ROOT)).replace("\\", "/")
        groups.setdefault(stem, {})[p.suffix.lower()[1:]] = str(p.relative_to(ROOT)).replace("\\", "/")
items = []
for stem, found in sorted(groups.items()):
    items.append({"stem": stem, "formats": found, "missing": [f[1:] for f in formats if f[1:] not in found]})
REPORT.parent.mkdir(parents=True, exist_ok=True)
REPORT.write_text(json.dumps({"status": "ok", "groups": items}, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"OK: wrote format parity matrix for {len(items)} document groups to {REPORT}")
