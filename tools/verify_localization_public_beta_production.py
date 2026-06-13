#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import html
import json
import subprocess
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIVE = "https://between-potential-and-ideal.onrender.com"
RELEASE_COMMIT = "89827cfe127ace4c18c426fbb8eb338be2f94578"
STATUS_PATH = ROOT / "site/localization-public-beta-production-status.json"
MANIFEST_PATH = ROOT / "localization/beta-release-manifest.json"
TLH_REVIEW_URL = "https://github.com/barakbenhur1/Between-Potential-and-Ideal/issues/11"
QYA_REVIEW_URL = "https://github.com/barakbenhur1/Between-Potential-and-Ideal/issues/10"
LEGACY_BANNER_MARKER = "localization-public-beta-links:start"


def fetch(path: str) -> dict:
    last_error = ""
    for attempt in range(5):
        try:
            request = urllib.request.Request(
                LIVE + path,
                headers={"User-Agent": "bpi-production-verifier/1.4"},
            )
            with urllib.request.urlopen(request, timeout=180) as response:
                body = response.read()
                return {
                    "http_code": response.status,
                    "content_type": response.headers.get_content_type(),
                    "downloaded_bytes": len(body),
                    "sha256": hashlib.sha256(body).hexdigest(),
                    "effective_url": response.geturl(),
                    "body": body,
                }
        except Exception as exc:
            last_error = str(exc)
            if attempt < 4:
                time.sleep(3)
    return {
        "http_code": 0,
        "content_type": "",
        "downloaded_bytes": 0,
        "sha256": "",
        "effective_url": LIVE + path,
        "error": last_error,
        "body": b"",
    }


def as_text(record: dict) -> str:
    return record["body"].decode("utf-8", errors="replace")


def normalized_text(record: dict) -> str:
    return html.unescape(as_text(record)).casefold()


def parse_json(record: dict) -> dict:
    try:
        return json.loads(as_text(record))
    except Exception:
        return {}


def commit_contains(required_commit: str, deployed_commit: str, *, refresh: bool = False) -> bool:
    if len(required_commit) != 40 or len(deployed_commit) != 40:
        return False
    if required_commit == deployed_commit:
        return True
    if refresh:
        subprocess.run(
            ["git", "fetch", "--quiet", "origin", "main"],
            cwd=ROOT,
            check=False,
        )
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", required_commit, deployed_commit],
        cwd=ROOT,
        check=False,
    ).returncode == 0


def exact_match(record: dict, entry: dict) -> bool:
    return (
        record["http_code"] == 200
        and record["downloaded_bytes"] == entry["bytes"]
        and record["sha256"] == entry["sha256"]
    )


def has_four_language_menu(record: dict) -> bool:
    text = as_text(record)
    return all(
        marker in text
        for marker in (
            'class="bpi-language-menu"',
            'class="bpi-language-menu-icon"',
            'href="/index.html"',
            'href="/en.html"',
            'href="/tlh.html"',
            'href="/qya.html"',
        )
    )


def has_no_legacy_beta_banner(record: dict) -> bool:
    return LEGACY_BANNER_MARKER not in as_text(record)


def wait_for_current_deployment(
    target_commit: str,
    expected: dict[str, dict],
) -> tuple[dict, dict, dict, dict, dict]:
    build = fetch("/build-info.json")
    home = fetch("/")
    home_en = fetch("/en.html")
    tlh_gateway = fetch("/tlh.html")
    qya_gateway = fetch("/qya.html")

    for attempt in range(30):
        build_data = parse_json(build)
        deployed_commit = str(build_data.get("commit", ""))
        metadata_current = commit_contains(
            target_commit,
            deployed_commit,
            refresh=attempt % 6 == 0,
        )
        content_current = (
            has_four_language_menu(home)
            and has_four_language_menu(home_en)
            and has_no_legacy_beta_banner(home)
            and has_no_legacy_beta_banner(home_en)
            and exact_match(tlh_gateway, expected["site/tlh.html"])
            and exact_match(qya_gateway, expected["site/qya.html"])
            and TLH_REVIEW_URL in as_text(tlh_gateway)
            and QYA_REVIEW_URL in as_text(qya_gateway)
        )
        if metadata_current or content_current:
            break
        if attempt < 29:
            time.sleep(10)
            build = fetch("/build-info.json")
            home = fetch("/")
            home_en = fetch("/en.html")
            tlh_gateway = fetch("/tlh.html")
            qya_gateway = fetch("/qya.html")

    return build, home, home_en, tlh_gateway, qya_gateway


def main() -> int:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    expected = {entry["path"]: entry for entry in manifest["files"]}
    target_commit = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()
    build, home, home_en, tlh_gateway, qya_gateway = wait_for_current_deployment(
        target_commit,
        expected,
    )

    paths = {
        "sitemap": "/sitemap.xml",
        "cover_image": "/figures/cover_philosophical_recursion_whole_diagram.png",
    }
    for language in ("tlh", "qya"):
        for extension in ("html", "pdf", "docx", "md", "txt"):
            paths[f"{language}_{extension}"] = (
                f"/files/{language}/between-potential-and-ideal-{language}.{extension}"
            )

    records = {name: fetch(path) for name, path in paths.items()}
    records["build"] = build
    records["home"] = home
    records["home_en"] = home_en
    records["tlh_gateway"] = tlh_gateway
    records["qya_gateway"] = qya_gateway

    build_data = parse_json(records["build"])
    deployed_commit = str(build_data.get("commit", ""))
    metadata_contains_target = commit_contains(
        target_commit,
        deployed_commit,
        refresh=True,
    )
    metadata_contains_release = commit_contains(RELEASE_COMMIT, deployed_commit)

    tlh_gateway_text = normalized_text(records["tlh_gateway"])
    qya_gateway_text = normalized_text(records["qya_gateway"])

    assertions = {
        "home_http_200": records["home"]["http_code"] == 200,
        "home_en_http_200": records["home_en"]["http_code"] == 200,
        "home_has_four_language_menu": has_four_language_menu(records["home"]),
        "home_en_has_four_language_menu": has_four_language_menu(records["home_en"]),
        "home_has_no_beta_banner": has_no_legacy_beta_banner(records["home"]),
        "home_en_has_no_beta_banner": has_no_legacy_beta_banner(records["home_en"]),
        "build_http_200": records["build"]["http_code"] == 200,
        "sitemap_http_200": records["sitemap"]["http_code"] == 200,
        "sitemap_has_localized_routes": all(
            route in as_text(records["sitemap"])
            for route in (
                "/tlh.html",
                "/qya.html",
                "/files/tlh/between-potential-and-ideal-tlh.html",
                "/files/qya/between-potential-and-ideal-qya.html",
            )
        ),
        "tlh_gateway_http_200": records["tlh_gateway"]["http_code"] == 200,
        "tlh_gateway_disclosure": all(
            marker in tlh_gateway_text
            for marker in ("public beta", "mughghachvam beta", "hol po'wi' nudghach")
        ),
        "tlh_gateway_has_review_link": TLH_REVIEW_URL in as_text(records["tlh_gateway"]),
        "qya_gateway_http_200": records["qya_gateway"]["http_code"] == 200,
        "qya_gateway_disclosure": all(
            marker in qya_gateway_text
            for marker in ("public beta", "neo-quenya", "parmaquetalië")
        ),
        "qya_gateway_has_review_link": QYA_REVIEW_URL in as_text(records["qya_gateway"]),
        "cover_image_http_200": records["cover_image"]["http_code"] == 200,
    }

    route_manifest: dict[str, str] = {}
    for language in ("tlh", "qya"):
        stem = f"between-potential-and-ideal-{language}"
        for extension in ("html", "pdf", "docx", "md", "txt"):
            name = f"{language}_{extension}"
            repo_path = f"site/files/{language}/{stem}.{extension}"
            route_manifest[name] = repo_path
            entry = expected[repo_path]
            assertions[f"{name}_http_200"] = records[name]["http_code"] == 200
            assertions[f"{name}_exact_size"] = records[name]["downloaded_bytes"] == entry["bytes"]
            assertions[f"{name}_exact_sha256"] = records[name]["sha256"] == entry["sha256"]

    for language in ("tlh", "qya"):
        name = f"{language}_gateway"
        repo_path = f"site/{language}.html"
        route_manifest[name] = repo_path
        entry = expected[repo_path]
        assertions[f"{name}_exact_size"] = records[name]["downloaded_bytes"] == entry["bytes"]
        assertions[f"{name}_exact_sha256"] = records[name]["sha256"] == entry["sha256"]

    assertions.update(
        {
            "tlh_html_disclosure": "not presented as canonical Klingon" in as_text(records["tlh_html"]),
            "qya_html_disclosure": "modern reconstruction" in as_text(records["qya_html"]),
            "tlh_pdf_magic": records["tlh_pdf"]["body"].startswith(b"%PDF"),
            "qya_pdf_magic": records["qya_pdf"]["body"].startswith(b"%PDF"),
            "tlh_docx_magic": records["tlh_docx"]["body"].startswith(b"PK"),
            "qya_docx_magic": records["qya_docx"]["body"].startswith(b"PK"),
            "tlh_md_disclosure": "Public Beta" in as_text(records["tlh_md"]),
            "qya_md_disclosure": "Public Beta" in as_text(records["qya_md"]),
        }
    )

    content_evidence_keys = [key for key in assertions if key != "build_http_200"]
    deployed_content_matches_repository = all(
        assertions[key] for key in content_evidence_keys
    )
    deployed_target_evidenced = metadata_contains_target or deployed_content_matches_repository
    assertions["deployed_target_evidenced"] = deployed_target_evidenced
    assertions["release_lineage_evidenced"] = (
        metadata_contains_release or deployed_content_matches_repository
    )

    routes = {}
    for name, record in records.items():
        routes[name] = {key: value for key, value in record.items() if key != "body"}
        if name in route_manifest:
            routes[name]["manifest_path"] = route_manifest[name]

    verified = all(assertions.values())
    payload = {
        "status": "verified" if verified else "failed",
        "production_verified": verified,
        "verification_scope": "four-language globe menus without a homepage beta banner, localized gateway disclosures and review links, sitemap, image, and exact repository manifest parity for both gateways and all five formats in both localized editions",
        "target_commit": target_commit,
        "required_release_commit": RELEASE_COMMIT,
        "deployment_evidence": {
            "metadata_contains_target": metadata_contains_target,
            "metadata_contains_release": metadata_contains_release,
            "content_matches_repository": deployed_content_matches_repository,
            "target_evidenced_by_metadata_or_content": deployed_target_evidenced,
            "note": "Exact live content checks are authoritative when Render build-info metadata is stale or cached.",
        },
        "deployed_build": build_data,
        "recorded_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "assertions": assertions,
        "routes": routes,
    }
    STATUS_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if verified else 1


if __name__ == "__main__":
    raise SystemExit(main())
