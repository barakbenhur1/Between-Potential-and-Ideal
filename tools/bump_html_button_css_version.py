#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "site/pages/he/ai.html",
    ROOT / "site/pages/en/ai-en.html",
    ROOT / "site/pages/he/files.html",
    ROOT / "site/pages/en/files-en.html",
]
OLD = "20260606-final-gold-html-v1"
NEW = "20260606-final-gold-html-ai-actions-v2"

changed = []
for path in TARGETS:
    text = path.read_text(encoding="utf-8")
    updated = text.replace(OLD, NEW)
    if updated != text:
        path.write_text(updated, encoding="utf-8")
        changed.append(str(path.relative_to(ROOT)))

print(f"Updated {len(changed)} files")
for item in changed:
    print(item)
