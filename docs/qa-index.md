# QA and Repair Index

This document is the starting point for future repair, QA, deploy, and release work.

## Read first

1. `docs/contributor-guardrails.md`
2. `docs/deploy.md`
3. `docs/visual-qa.md`
4. `docs/performance-budget.md`
5. `docs/tool-inventory.md`
6. `docs/production-next-phase-status.md`

## Required command before push

Run from repository root:

```bash
rm -rf reports tools/__pycache__
python3 tools/final_release_qa.py --scan
git diff --check
git status --short
```

For detailed local release-guard diagnostics, run:

```bash
python3 tools/audit_release_guard.py
```

## Core release checks

The final release QA and release guard include checks for:

- root junk/temp repair artifacts
- tool inventory coverage
- release guard integrity
- gitignore protection for local QA/temp artifacts
- public junk/debug/temp files under `site/`
- files filter live-region accessibility
- external/new-tab link accessibility
- QA docs index
- contributor guardrails
- performance budget docs
- visual QA baseline docs
- build info
- CI workflow
- deploy documentation
- CSS integrity
- SEO metadata and robots baseline
- sitemap/canonical parity
- search-index term precision
- bilingual hreflang pair coverage
- long-document SEO metadata readiness
- runtime JavaScript scope
- CSS consolidation candidate reporting
- AI dialogue disclosures
- 16-story appendix registry and protected order
- protected story details
- local images
- anchors and duplicate IDs
- visible Hebrew leakage in English files
- files page language labels
- files table accessibility
- files page download links and document sibling packages
- public document sibling format sync

## Manual checks after deploy

After Render deploy finishes:

```bash
python3 tools/check_live_deploy_urls.py
```

Then manually open key Hebrew, English, files, stories, theory, and AI pages.

For live sitemap/public links, `tools/audit_sitemap_and_public_links.py` is a manual post-deploy audit, not a required push gate.

## Safety rules

- Do not redesign.
- Do not delete files.
- Do not remove images.
- Do not change story order or story IDs.
- Do not return the appendix to 14 stories.
- Do not change protected story details.
- Do not present AI as conscious or authoritative.
- Do not perform CSS cleanup before visual QA.
- Do not force-push `main`.

## Cleanup rule

Before every commit, remove temporary outputs:

```bash
rm -rf reports tools/__pycache__
```

Do not commit temporary repair scripts unless they are permanent audit/check tools.
