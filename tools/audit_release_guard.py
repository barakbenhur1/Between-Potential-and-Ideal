import subprocess
import sys

CHECKS = [
    ["python3", "tools/check_no_root_junk_files.py"],
    ["python3", "tools/check_tool_inventory.py"],
    ["python3", "tools/check_release_guard_integrity.py"],
    ["python3", "tools/check_gitignore.py"],
    ["python3", "tools/check_no_public_junk_files.py"],
    ["python3", "tools/check_files_filter_live_region.py"],
    ["python3", "tools/check_external_links_accessibility.py"],
    ["python3", "tools/check_qa_docs_index.py"],
    ["python3", "tools/check_contributor_guardrails.py"],
    ["python3", "tools/check_performance_budget_docs.py"],
    ["python3", "tools/check_visual_qa_docs.py"],
    ["python3", "tools/check_build_info.py"],
    ["python3", "tools/check_ci_workflow.py"],
    ["python3", "tools/check_deploy_docs.py"],
    ["python3", "tools/check_css_integrity.py"],
    ["python3", "tools/check_seo_metadata.py"],
    ["python3", "tools/audit_sitemap_canonical_parity.py"],
    ["python3", "tools/audit_search_index_terms.py"],
    ["python3", "tools/audit_hreflang_links.py"],
    ["python3", "tools/audit_document_seo_metadata.py"],
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
]

def run(cmd):
    print("\n==>", " ".join(cmd))
    result = subprocess.run(cmd)
    if result.returncode != 0:
        raise SystemExit(result.returncode)

def main():
    for cmd in CHECKS:
        run(cmd)
    print("\nOK: release guard passed.")

if __name__ == "__main__":
    main()
