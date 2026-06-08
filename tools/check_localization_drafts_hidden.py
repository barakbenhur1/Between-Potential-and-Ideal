#!/usr/bin/env python3
from pathlib import Path
import json, sys

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
CONFIG = ROOT / "localization/config.json"
DRAFT_MARKERS = ("linguistic-review", "publication: forbidden", "home-stage-", "summary-stage-")


def main():
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    errors = []
    for code in ("tlh", "qya"):
        lang = cfg["languages"][code]
        if not lang.get("publish"):
            forbidden = [ROOT / lang["home"], ROOT / lang["pages_dir"], ROOT / lang["files_dir"]]
            for path in forbidden:
                if path.exists():
                    errors.append(f"draft language is not publishable but public path exists: {path.relative_to(ROOT)}")
    for path in SITE.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".html", ".js", ".css", ".json", ".xml"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for marker in DRAFT_MARKERS:
            if marker in text:
                errors.append(f"public file references localization draft marker {marker!r}: {path.relative_to(ROOT)}")
    if errors:
        print("FAIL: localization draft exposure detected")
        for error in errors:
            print("-", error)
        return 1
    print("OK: incomplete localization editions remain outside public site paths.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
