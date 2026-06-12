#!/usr/bin/env python3
from pathlib import Path
import json, sys

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
CONFIG = ROOT / "localization/config.json"
BETA_MANIFEST = ROOT / "localization/beta-release-manifest.json"
DRAFT_MARKERS = ("linguistic-review", "publication: forbidden", "home-stage-", "summary-stage-")
BETA_DISCLOSURES = ("PUBLIC BETA", "Public Beta", "public beta")


def beta_manifest() -> dict | None:
    if not BETA_MANIFEST.is_file():
        return None
    try:
        data = json.loads(BETA_MANIFEST.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    if data.get("release_channel") != "public-beta":
        return None
    if data.get("linguistic_review_complete") is not False:
        return None
    return data


def has_beta_disclosure(path: Path) -> bool:
    if not path.is_file():
        return False
    text = path.read_text(encoding="utf-8", errors="ignore")
    return any(marker in text for marker in BETA_DISCLOSURES)


def main():
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    errors = []
    beta = beta_manifest()
    for code in ("tlh", "qya"):
        lang = cfg["languages"][code]
        if lang.get("publish"):
            continue
        home = ROOT / lang["home"]
        pages = ROOT / lang["pages_dir"]
        files = ROOT / lang["files_dir"]
        public_paths_exist = home.exists() or pages.exists() or files.exists()
        if not public_paths_exist:
            continue
        beta_files = [] if beta is None else [item.get("path") for item in beta.get("files", [])]
        expected_prefix = f"site/files/{code}/"
        listed = [item for item in beta_files if isinstance(item, str) and item.startswith(expected_prefix)]
        if beta is None or len(listed) < 5:
            errors.append(f"unpublished language exposes public paths without a complete beta manifest: {code}")
            continue
        if pages.exists():
            errors.append(f"public beta may expose the document gateway and packages, not untranslated mapped pages: {pages.relative_to(ROOT)}")
        if not has_beta_disclosure(home):
            errors.append(f"public beta gateway lacks a visible disclosure: {home.relative_to(ROOT)}")
        html_package = files / f"between-potential-and-ideal-{code}.html"
        if not has_beta_disclosure(html_package):
            errors.append(f"public beta document lacks a visible disclosure: {html_package.relative_to(ROOT)}")

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
    print("OK: incomplete editions remain hidden or are exposed only as disclosed public beta packages.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
