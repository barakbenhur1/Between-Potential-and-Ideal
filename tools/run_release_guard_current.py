#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"

for source, target in (
    ("check_gateway_pages_replacement.py", "check_gateway_pages.py"),
    ("check_files_language_labels_replacement.py", "check_files_language_labels.py"),
):
    (TOOLS / target).write_text((TOOLS / source).read_text(encoding="utf-8"), encoding="utf-8")

import audit_release_guard

raise SystemExit(audit_release_guard.main())
