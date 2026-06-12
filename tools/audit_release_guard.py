#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

CHECKS = [
    ["python3", "tools/check_no_root_junk_files.py"],
    ["python3", "tools/check_tool_inventory.py"],
    ["python3", "tools/check_release_guard_integrity.py"],
    ["python3", "tools/check_gitignore.py"],
    ["python3", "tools/check_no_public_junk_files.py"],
    ["python3", "tools/check_localization_drafts_hidden.py"],
    ["python3", "tools/check_localized_document_contracts.py"],
    ["python3", "tools/check_files_filter_live_region.py"],
    ["python3", "tools/check_external_links_accessibility.py"],
    ["python3", "tools/check_qa_docs_index.py"],
    ["python3", "tools/check_readme_docs.py"],
    ["python3", "tools/check_contributor_guardrails.py"],
    ["python3", "tools/check_performance_budget_docs.py"],
    ["python3", "tools/check_visual_qa_docs.py"],
    ["python3", "tools/check_build_info.py"],
    ["python3", "tools/check_ci_workflow.py"],
    ["python3", "tools/check_deploy_docs.py"],
    ["python3", "tools/check_css_integrity.py"],
    ["python3", "tools/check_seo_metadata.py"],
    ["python3", "tools/check_gateway_pages.py"],
    ["python3", "tools/audit_sitemap_canonical_parity.py"],
    ["python3", "tools/audit_search_index_terms.py"],
    ["python3", "tools/audit_hreflang_links.py"],
    ["python3", "tools/audit_gateway_internal_links.py"],
    ["python3", "tools/audit_document_seo_metadata.py"],
    ["python3", "tools/audit_runtime_js_scope.py"],
    ["python3", "tools/audit_css_consolidation_candidates.py"],
    ["python3", "tools/check_ai_disclosures.py"],
    ["python3", "tools/audit_story_appendices_16.py"],
    ["python3", "tools/check_story_registry.py"],
    ["python3", "tools/check_protected_story_details.py"],
    ["python3", "tools/audit_images_exist.py"],
    ["python3", "tools/audit_anchors.py"],
    ["python3", "tools/audit_visible_hebrew_in_english.py"],
    ["python3", "tools/check_files_language_labels.py"],
    ["python3", "tools/check_files_table_accessibility.py"],
    ["python3", "tools/audit_file_download_links.py"],
    ["python3", "tools/audit_document_sync_status.py"],
    ["python3", "tools/audit_extended_localization_parity.py"],
]

ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "reports" / "production_next" / "release_guard_results.json"


def run(cmd: list[str]) -> dict:
    print("\n==>", " ".join(cmd), flush=True)
    result = subprocess.run(
        cmd,
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.stdout:
        print(result.stdout, end="" if result.stdout.endswith("\n") else "\n")
    if result.stderr:
        print(result.stderr, end="" if result.stderr.endswith("\n") else "\n", file=sys.stderr)
    return {
        "command": cmd,
        "returncode": result.returncode,
        "ok": result.returncode == 0,
        "stdout_tail": "\n".join(result.stdout.splitlines()[-80:]),
        "stderr_tail": "\n".join(result.stderr.splitlines()[-80:]),
    }


def main() -> int:
    results = [run(cmd) for cmd in CHECKS]
    failures = [result for result in results if not result["ok"]]

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "status": "passed" if not failures else "failed",
        "checks_total": len(results),
        "checks_passed": len(results) - len(failures),
        "checks_failed": len(failures),
        "failed_commands": [" ".join(result["command"]) for result in failures],
        "results": results,
    }
    REPORT_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    if failures:
        print("\nFAIL: release guard failed checks:")
        for result in failures:
            print(f"- {' '.join(result['command'])} (exit {result['returncode']})")
        print(f"Detailed report: {REPORT_PATH.relative_to(ROOT)}")
        return 1

    print("\nOK: release guard passed.")
    print(f"Detailed report: {REPORT_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
