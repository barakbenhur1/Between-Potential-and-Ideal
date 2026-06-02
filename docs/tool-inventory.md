# Tool Inventory

This document lists the permanent QA and release tools used by the project.

Temporary `fix_*.py` scripts must not be listed here and must not be committed unless explicitly promoted into a permanent audit/check tool.

## Main command

- `tools/final_release_qa.py` — runs the repo-local final release QA gate before push/release.
- `tools/audit_release_guard.py` — runs the detailed local release guard used by the final QA command.

## Permanent checks

- `tools/check_release_guard_integrity.py` — validates the release guard itself.
- `tools/check_no_public_junk_files.py` — prevents public junk/debug/temp files under `site/`.
- `tools/check_gitignore.py` — verifies local generated artifacts are ignored.
- `tools/check_files_filter_live_region.py` — verifies Files page filter status is announced accessibly.
- `tools/check_external_links_accessibility.py` — verifies new-tab links are accessible.
- `tools/check_qa_docs_index.py` — verifies the QA docs index.
- `tools/check_contributor_guardrails.py` — verifies contributor guardrails.
- `tools/check_performance_budget_docs.py` — verifies performance/asset policy.
- `tools/check_visual_qa_docs.py` — verifies visual QA baseline docs.
- `tools/check_build_info.py` — verifies build metadata.
- `tools/check_build_info_matches_head.py` — verifies build-info metadata without creating false deployment blockers.
- `tools/check_ci_workflow.py` — verifies GitHub Actions release guard workflow.
- `tools/check_deploy_docs.py` — verifies deploy documentation.
- `tools/check_seo_metadata.py` — verifies robots and sitemap SEO baseline.
- `tools/audit_sitemap_canonical_parity.py` — verifies sitemap URLs, canonical base, duplicate URL safety, local target existence, and lastmod coverage.
- `tools/audit_search_index_terms.py` — audits search-index URL integrity and term precision warnings.
- `tools/audit_hreflang_links.py` — audits bilingual hreflang pair coverage and reports missing alternates as warnings.
- `tools/audit_document_seo_metadata.py` — audits long public document HTML SEO and social metadata readiness.
- `tools/check_ai_disclosures.py` — verifies AI dialogue disclosure blocks.
- `tools/check_files_table_accessibility.py` — verifies Files table semantics.
- `tools/check_files_language_labels.py` — verifies Files page labels match page language.
- `tools/check_story_registry.py` — verifies protected 16-story appendix registry.
- `tools/check_protected_story_details.py` — verifies protected story details.
- `tools/check_tool_inventory.py` — verifies this inventory covers release guard checks.
- `tools/audit_file_download_links.py` — verifies Files page download links and document sibling packages.
- `tools/audit_document_sync_status.py` — verifies expected public document sibling formats exist and are non-empty.

## Existing audit tools

- `tools/audit_story_appendices_16.py`
- `tools/audit_images_exist.py`
- `tools/audit_anchors.py`
- `tools/audit_visible_hebrew_in_english.py`
- `tools/audit_seo_social_preview.py`
- `tools/audit_sitemap_and_public_links.py`
- `tools/audit_sitemap_canonical_parity.py`
- `tools/audit_search_index_terms.py`
- `tools/audit_hreflang_links.py`
- `tools/audit_document_seo_metadata.py`
- `tools/audit_file_download_links.py`
- `tools/audit_document_sync_status.py`

## Operational tools

- `tools/check_live_deploy_urls.py` — checks important live URLs after Render deploy.
- `tools/update_build_info.py` — updates `site/build-info.json` before important releases or during deploy builds.

## Rule

If a permanent tool is added to `tools/audit_release_guard.py`, it must also be listed in this file.

- `tools/check_no_root_junk_files.py` — prevents temporary repair/debug/archive artifacts at repository root.
