#!/usr/bin/env python3
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "localization" / "config.json"
MANIFEST = ROOT / "localization" / "translation-manifest.json"
REPORT = ROOT / "reports" / "localization" / "parity.json"
TARGETS = ("tlh", "qya")


def inspect_file(path: Path) -> dict:
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "exists": path.is_file(),
        "bytes": path.stat().st_size if path.is_file() else 0,
    }


def audit_language(code: str, cfg: dict, manifest: dict) -> dict:
    language = cfg["languages"][code]
    required = cfg["required_download_formats"]
    missing = []

    home = inspect_file(ROOT / language["home"])
    if not home["exists"]:
        missing.append(home["path"])

    pages_dir = ROOT / language["pages_dir"]
    pages = []
    for slug in manifest["public_pages"]:
        if slug == "home":
            continue
        item = inspect_file(pages_dir / f"{slug}.html")
        pages.append(item)
        if not item["exists"]:
            missing.append(item["path"])

    files_dir = ROOT / language["files_dir"]
    packages = []
    for package in manifest["document_packages"]:
        formats = []
        for fmt in required:
            item = inspect_file(files_dir / f"{package}-{code}.{fmt}")
            formats.append(item)
            if not item["exists"]:
                missing.append(item["path"])
        packages.append({"package": package, "formats": formats})

    blockers = missing if language.get("publish") else []
    warnings = [] if language.get("publish") else missing
    return {
        "code": code,
        "label": language["label"],
        "publish": bool(language.get("publish")),
        "home": home,
        "pages": pages,
        "packages": packages,
        "missing_count": len(missing),
        "blockers": blockers,
        "warnings": warnings,
    }


def main() -> int:
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    languages = [audit_language(code, cfg, manifest) for code in TARGETS]
    blockers = [item for lang in languages for item in lang["blockers"]]
    result = {
        "status": "FAIL" if blockers else "OK",
        "policy": "Draft languages may be incomplete; published languages may not.",
        "languages": languages,
        "blockers": blockers,
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for lang in languages:
        state = "published" if lang["publish"] else "draft"
        print(f"{lang['code']}: {state}; missing={lang['missing_count']}")
    print("Report:", REPORT.relative_to(ROOT).as_posix())
    return 1 if blockers else 0


if __name__ == "__main__":
    sys.exit(main())
