# Production Next Phase Status

This document summarizes the post-release hardening and SEO/discoverability work performed after the initial `RELEASE_READY` gate.

## Scope

The work intentionally prioritized safe, additive, audit-first changes:

- deployment verification reliability
- repo-local release QA standardization
- CI release guard wiring
- download/document package audits
- SEO metadata audits
- sitemap/canonical audits
- search-index precision audits
- hreflang pair audits
- accessibility skip-link repair
- CSS integrity and consolidation candidate audits
- runtime JavaScript scope audits
- final document package sync audits
- AI disclosure and protected story detail audits

Protected content and approved visual/literary elements were not rewritten or removed.

## Completed phases

| Phase | Status | Notes |
|---|---:|---|
| Phase 0 | Done | Baseline/freeze rules established in the workflow. |
| Phase 1 | Done | Build-info tooling and deployment-verification guard added/updated. |
| Phase 2 | Done | `tools/final_release_qa.py --scan` became the standardized release command. |
| Phase 3 | Done | CI workflow was updated to call the standardized final release QA command. |
| Phase 4 | Done | File download and document package audit added. |
| Phase 5 | Done | Long-document SEO metadata audit added. |
| Phase 6 | Done | Sitemap/canonical parity audit added. |
| Phase 7 | Done | Search-index term precision audit added. |
| Phase 8 | Done | Bilingual hreflang pair audit added. |
| Phase 12 | Done | AI document skip-link accessibility was repaired. |
| Phase 12B | Done | CSS integrity repair and CSS integrity guard were added. |
| Phase 13 | Done as audit | Runtime JavaScript scope audit added; no risky JS split was applied. |
| Phase 14 | Done as audit | CSS consolidation candidates audit added; no risky CSS consolidation was applied. |
| Phase 15 | Done as audit/gate | Final document sync status audit was added to the release guard. |
| Phase 16 | Done as summary | This status document records what changed and what remains. |
| Phase 17 | Done as gate hardening | AI disclosure and protected story detail audits were added to the release guard. |
| Phase 18 | Done as gate hardening | CSS integrity and runtime JavaScript scope audits are now documented and release-guarded. |

## Release guard now covers

The final release QA command now wraps the detailed release guard. The guard includes baseline repo hygiene, CI/deploy docs, CSS integrity, SEO metadata, sitemap/canonical parity, search-index terms, hreflang, document SEO metadata, runtime JS scope, AI disclosures, protected story/story-registry checks, images, anchors, English-page Hebrew leakage, Files language/accessibility checks, file download packages, and document sync status.

## Important constraints preserved

Do not treat the following as problems without a real technical/accessibility/language/SEO blocker:

- blurbs
- arrows and symbolic markers
- story/document markers
- approved Author's Note styling
- `עברית` language-switch labels on English pages
- protected story endings and literary/philosophical wording
- approved images, fonts, colors, TOC styling, and document layout

## Known limits of this phase

Some changes are audit-first rather than automatic refactors. That is intentional.

The following should only be applied after visual QA and, where relevant, user approval:

- extracting/splitting inline JavaScript into external modules
- deeper CSS consolidation
- editing large/minified generated HTML documents by hand
- adding new gateway pages that affect public philosophical framing
- adding visible FAQ content
- adding FAQPage structured data
- adding broader hreflang tags into every generated document page
- changing `search-index.json` terms directly

`tools/audit_seo_social_preview.py` remains an informational/full SEO preview audit for now. Do not promote it to a release gate until long-document metadata work is complete, because it checks every HTML page under `site/` and can turn planned SEO work into a premature blocker.

## Deployment verification policy

A deployment gap should not be declared solely from a screenshot or browser-rendered DOM.

Before marking a deployment blocker, verify:

- latest Git commit
- Render deploy logs
- hard refresh
- incognito/private window
- page source
- cache/CDN behavior
- live `/build-info.json` if generated during deploy

If evidence is incomplete, use:

```text
Deployment verification inconclusive
```

## Recommended final local command

Run from repo root before push/release:

```bash
rm -rf reports tools/__pycache__
python3 tools/final_release_qa.py --scan
git diff --check
git status --short
```

## Recommended next work requiring content approval

The next high-value SEO/discoverability work is content-producing rather than purely technical:

1. Confirm which gateway pages are already approved and live.
2. Add remaining bilingual gateway pages such as Nihilism with Hope, How to Read, and Citation.
3. Add visible FAQ sections and then matching structured data.
4. Add related-reading links after the new pages exist.
5. Improve page-specific search-index terms from a single source-of-truth.
6. Complete long-document social preview metadata before promoting `audit_seo_social_preview.py` to the release gate.

These should not be auto-written without review because they affect public philosophical framing.
