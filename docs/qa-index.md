# QA and Repair Index

This document is the starting point for future repair, QA, deploy, and release work.

## Read first

1. `docs/contributor-guardrails.md`
2. `docs/deploy.md`
3. `docs/visual-qa.md`
4. `docs/performance-budget.md`

## Required command before push

Run from repository root:

```bash
rm -rf reports tools/__pycache__
python3 tools/audit_release_guard.py
git diff --check
git status --short
```

## Core release checks

The release guard includes checks for:

- 16-story appendix registry and protected order
- protected story details
- local images
- anchors and duplicate IDs
- visible Hebrew leakage in English files
- files page language labels
- files table accessibility
- SEO metadata and robots baseline
- AI dialogue disclosures
- deploy documentation
- CI workflow
- build info
- visual QA docs
- performance budget docs
- contributor guardrails

## Manual checks after deploy

After Render deploy finishes:

```bash
python3 tools/check_live_deploy_urls.py
```

Then manually open key Hebrew, English, files, stories, theory, and AI pages.

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
