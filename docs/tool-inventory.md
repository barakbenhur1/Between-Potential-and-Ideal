# Tool Inventory

This document lists the permanent QA and release tools used by the project.

Temporary `fix_*.py` scripts must not be listed here and must not be committed unless explicitly promoted into a permanent audit/check tool.

## Main command

- `tools/final_release_qa.py` — runs the repo-local final release QA gate before push/release.
- `tools/audit_release_guard.py` — runs the detailed local release guard used by the final QA command.

## Permanent checks

- `tools/check_no_root_junk_files.py` — prevents temporary repair/debug/archive artifacts at repository root.
- `tools/check_release_guard_integrity.py` — validates the release guard itself.
- `tools/check_no_public_junk_files.py` — prevents public junk/debug/temp files under `site/`.
- `tools/check_localization_drafts_hidden.py` — blocks public Klingon or Neo-Quenya paths and draft markers while those languages remain unpublished.
- `tools/check_localized_document_contracts.py` — verifies canonical localized bases, ordered source segments, front matter, language identity, publication locks, and approval requirements.
- `tools/check_gitignore.py` — verifies local generated artifacts are ignored.
- `tools/check_files_filter_live_region.py` — verifies Files page filter status is announced accessibly.
- `tools/check_external_links_accessibility.py` — verifies new-tab links are accessible.
- `tools/check_qa_docs_index.py` — verifies the QA docs index.
- `tools/check_readme_docs.py` — verifies README structure and current QA workflow instructions.
- `tools/check_contributor_guardrails.py` — verifies contributor guardrails.
- `tools/check_performance_budget_docs.py` — verifies performance/asset policy.
- `tools/check_visual_qa_docs.py` — verifies visual QA baseline docs.
- `tools/check_build_info.py` — verifies build metadata.
- `tools/check_build_info_matches_head.py` — verifies build-info metadata without creating false deployment blockers.
- `tools/check_ci_workflow.py` — verifies GitHub Actions release guard workflow.
- `tools/check_deploy_docs.py` — verifies deploy documentation.
- `tools/check_css_integrity.py` — verifies CSS files have basic structural integrity and protected patch markers remain paired.
- `tools/check_seo_metadata.py` — verifies robots and sitemap SEO baseline.
- `tools/check_gateway_pages.py` — verifies existing gateway pages have baseline metadata, canonical links, hreflang links, language switch, and main target.
- `tools/audit_sitemap_canonical_parity.py` — verifies sitemap URLs, canonical base, duplicate URL safety, local target existence, and lastmod coverage.
- `tools/audit_search_index_terms.py` — audits search-index URL integrity and term precision warnings.
- `tools/audit_hreflang_links.py` — audits bilingual hreflang pair coverage and reports missing alternates as warnings.
- `tools/audit_document_seo_metadata.py` — audits long public document HTML SEO and social metadata readiness.
- `tools/audit_runtime_js_scope.py` — audits runtime JavaScript scope before any future script split.
- `tools/audit_css_consolidation_candidates.py` — reports CSS consolidation candidates without rewriting protected design.
- `tools/check_ai_disclosures.py` — verifies AI dialogue disclosure blocks.
- `tools/check_files_table_accessibility.py` — verifies Files table semantics.
- `tools/check_files_language_labels.py` — verifies Files page labels match page language.
- `tools/check_story_registry.py` — verifies protected 16-story appendix registry.
- `tools/check_protected_story_details.py` — verifies protected story details.
- `tools/check_tool_inventory.py` — verifies this inventory covers release guard checks.
- `tools/audit_file_download_links.py` — verifies Files page download links and document sibling packages.
- `tools/audit_document_sync_status.py` — verifies expected public document sibling formats exist and are non-empty.
- `tools/audit_extended_localization_parity.py` — allows incomplete draft editions but blocks publication of Klingon or Neo-Quenya when any mapped page or required format is missing.

## Existing audit tools

- `tools/audit_story_appendices_16.py`
- `tools/audit_images_exist.py`
- `tools/audit_anchors.py`
- `tools/audit_visible_hebrew_in_english.py`
- `tools/audit_seo_social_preview.py` — informational/full SEO preview audit; do not promote to release gate until long document metadata work is complete.
- `tools/audit_sitemap_and_public_links.py` — manual post-deploy live audit; do not promote to release gate.
- `tools/audit_sitemap_canonical_parity.py`
- `tools/audit_search_index_terms.py`
- `tools/audit_hreflang_links.py`
- `tools/audit_gateway_internal_links.py` — informational audit for gateway-page internal-link discoverability; warnings only.
- `tools/audit_document_seo_metadata.py`
- `tools/audit_runtime_js_scope.py`
- `tools/audit_css_consolidation_candidates.py`
- `tools/audit_file_download_links.py`
- `tools/audit_document_sync_status.py`
- `tools/audit_extended_localization_parity.py`

## Operational tools

- `tools/check_live_deploy_urls.py` — checks important live URLs after Render deploy.
- `tools/update_build_info.py` — updates `site/build-info.json` before important releases or during deploy builds.
- `tools/build_localization_inventory.py` — inventories public pages and all HTML/PDF/DOCX/MD/TXT document groups for the four-language project.
- `tools/assemble_localized_document.py` — assembles a canonical localized base and its ordered review segments into one non-public Markdown preview.
- `tools/audit_localized_assembly.py` — audits review and clean non-public localization assemblies for structural completeness, control-section removal, hashes, parity, and publication readiness.
- `tools/update_localization_stage_from_audit.py` — advances contract and batch metadata only after a verified assembly audit passes all structural prerequisites.

## Rule

If a permanent tool is added to `tools/audit_release_guard.py`, it must also be listed in this file.
