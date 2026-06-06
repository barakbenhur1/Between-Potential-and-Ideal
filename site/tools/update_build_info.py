#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import os
import runpy

# Compatibility wrapper for Render services configured with Root Directory = site.
# It executes the canonical repository-level build-info generator from repo root.
REPO_ROOT = Path(__file__).resolve().parents[2]
CANONICAL_SCRIPT = REPO_ROOT / "tools" / "update_build_info.py"

if not CANONICAL_SCRIPT.is_file():
    raise SystemExit(f"Missing canonical build script: {CANONICAL_SCRIPT}")

os.chdir(REPO_ROOT)
runpy.run_path(str(CANONICAL_SCRIPT), run_name="__main__")
