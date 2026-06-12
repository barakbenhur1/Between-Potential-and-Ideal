#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE_MANIFEST = ROOT / "localization/site-language-parity-manifest.json"
BETA_MANIFEST = ROOT / "localization/beta-release-manifest.json"
REPORT = ROOT / "reports/localization/parity.json"
LANGUAGES = ("tlh", "qya")
REQUIRED_FORMATS = {"html", "pdf", "docx", "md", "txt"}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def check_entry(entry: dict) -> dict:
    path = ROOT / entry["path"]
    exists = path.is_file()
    actual_bytes = path.stat().st_size if exists else 0
    actual_sha256 = sha256(path) if exists else ""
    return {
        "path": entry["path"],
        "exists": exists,
        "expected_bytes": int(entry["bytes"]),
        "actual_bytes": actual_bytes,
        "expected_sha256": entry["sha256"],
        "actual_sha256": actual_sha256,
        "bytes_match": exists and actual_bytes == int(entry["bytes"]),
        "sha256_match": exists and actual_sha256 == entry["sha256"],
    }


def source_status(path: Path) -> str:
    if not path.is_file():
        return "missing"
    text = path.read_text(encoding="utf-8", errors="ignore")
    if not text.startswith("---\n"):
        return "invalid"
    parts = text.split("---\n", 2)
    if len(parts) != 3:
        return "invalid"
    for line in parts[1].splitlines():
        key, sep, value = line.partition(":")
        if sep and key.strip() == "status":
            return value.strip() or "missing-status"
    return "missing-status"


def main() -> int:
    site_manifest = json.loads(SITE_MANIFEST.read_text(encoding="utf-8"))
    beta_manifest = json.loads(BETA_MANIFEST.read_text(encoding="utf-8"))
    blockers: list[str] = []
    warnings: list[str] = []

    if site_manifest.get("release_channel") != "public-beta-full-site":
        blockers.append("site parity manifest release channel is not public-beta-full-site")
    if beta_manifest.get("release_channel") != "public-beta":
        blockers.append("beta release manifest release channel is not public-beta")
    if set(site_manifest.get("languages", [])) != set(LANGUAGES):
        blockers.append("site parity manifest language set is incomplete")
    if set(beta_manifest.get("languages", [])) != set(LANGUAGES):
        blockers.append("beta release manifest language set is incomplete")

    site_results = [check_entry(entry) for entry in site_manifest.get("files", [])]
    beta_results = [check_entry(entry) for entry in beta_manifest.get("files", [])]
    for result in site_results + beta_results:
        if not result["exists"]:
            blockers.append(f"missing manifest file: {result['path']}")
        elif not result["bytes_match"]:
            blockers.append(f"byte mismatch: {result['path']}")
        elif not result["sha256_match"]:
            blockers.append(f"SHA-256 mismatch: {result['path']}")

    expected_pages = int(site_manifest.get("pages_per_language", 0))
    expected_segments = int(beta_manifest.get("segments_per_language", 0))
    language_results = []

    for language in LANGUAGES:
        page_prefix = f"site/pages/{language}/"
        page_paths = [
            entry["path"]
            for entry in site_manifest.get("files", [])
            if entry["path"] == f"site/{language}.html" or entry["path"].startswith(page_prefix)
        ]
        if len(page_paths) != expected_pages:
            blockers.append(
                f"{language}: expected {expected_pages} public pages in manifest, found {len(page_paths)}"
            )

        file_prefix = f"site/files/{language}/"
        package_entries = [
            entry
            for entry in beta_manifest.get("files", [])
            if entry["path"].startswith(file_prefix)
        ]
        formats = {Path(entry["path"]).suffix.lstrip(".") for entry in package_entries}
        if formats != REQUIRED_FORMATS:
            blockers.append(
                f"{language}: required download formats {sorted(REQUIRED_FORMATS)}, found {sorted(formats)}"
            )

        source_dir = ROOT / "localization" / "sources" / language / "between-potential-and-ideal"
        source_files = sorted(source_dir.glob("*.md")) if source_dir.is_dir() else []
        if len(source_files) != expected_segments:
            blockers.append(
                f"{language}: expected {expected_segments} source segments, found {len(source_files)}"
            )

        statuses: dict[str, int] = {}
        for source in source_files:
            status = source_status(source)
            statuses[status] = statuses.get(status, 0) + 1
            if status in {"missing", "invalid", "missing-status"}:
                blockers.append(f"{rel(source)} has invalid source status metadata: {status}")

        non_approved = sum(count for status, count in statuses.items() if status != "approved")
        if non_approved:
            if beta_manifest.get("linguistic_review_complete") is False:
                warnings.append(
                    f"{language}: {non_approved} source segments remain non-final under the disclosed Public Beta"
                )
            else:
                blockers.append(
                    f"{language}: manifest claims linguistic review complete but {non_approved} segments are non-approved"
                )

        language_results.append(
            {
                "code": language,
                "public_pages": len(page_paths),
                "download_formats": sorted(formats),
                "source_segments": len(source_files),
                "source_statuses": statuses,
            }
        )

    result = {
        "status": "FAIL" if blockers else "OK",
        "release_channel": beta_manifest.get("release_channel"),
        "linguistic_review_complete": beta_manifest.get("linguistic_review_complete"),
        "site_manifest_files": len(site_results),
        "beta_manifest_files": len(beta_results),
        "languages": language_results,
        "warnings": warnings,
        "blockers": blockers,
        "site_files": site_results,
        "beta_files": beta_results,
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for language in language_results:
        print(
            f"{language['code']}: pages={language['public_pages']} "
            f"formats={len(language['download_formats'])} segments={language['source_segments']}"
        )
    for warning in warnings:
        print("WARNING:", warning)
    print("Report:", rel(REPORT))

    if blockers:
        print("FAIL: localized public-beta parity blockers")
        for blocker in blockers:
            print("-", blocker)
        return 1

    print("OK: localized public-beta files match authoritative manifests; linguistic review remains explicitly incomplete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
