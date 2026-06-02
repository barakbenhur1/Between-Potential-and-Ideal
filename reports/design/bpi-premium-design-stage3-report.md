# BPI Premium Design Stage 3 — Side Branch Report

Branch: `bpi-premium-design-stage3`
Base branch: `main`

## Goal

Apply a v0-inspired premium visual layer to the existing static site without replacing the original content, page structure, links, blurbs, or bilingual text.

## What changed

Added:

- `site/assets/bpi-premium-design.css`

Updated:

- `site/assets/bpi-skip-link-fix.css`

The update to `bpi-skip-link-fix.css` only imports the new premium design stylesheet:

```css
@import url("./bpi-premium-design.css?v=20260602-stage3-side-branch");
```

## Preservation status

No HTML files were edited in this stage.

Therefore this stage does not delete, shorten, rewrite, merge, summarize, or replace:

- homepage hero text
- blurbs
- card descriptions
- CTA labels
- navigation labels
- Hebrew text
- English text
- document descriptions
- story descriptions
- internal links
- language switch links
- SEO metadata in HTML

The site content remains the existing content from the original static pages.

## Design scope

The new CSS layer targets existing classes only and improves:

- cinematic dark background atmosphere
- sticky glass navigation
- active tab styling
- hero visual hierarchy
- premium gradient buttons
- gateway cards
- reading surfaces
- story/signature blurb presentation
- image framing
- footer styling
- RTL/LTR alignment polish
- keyboard focus visibility
- reduced-motion behavior

## Safety notes

This is a side-branch prototype, not a release-ready merge.

The branch is currently intended for visual review. Before merging into `main`, run local QA:

```bash
python3 tools/final_release_qa.py --scan
git diff --check
```

Also manually check:

- Hebrew homepage
- English homepage
- Hebrew witness page
- English witness page
- files pages
- mobile navigation
- active tabs
- Hebrew pages do not show the term `AI` where Hebrew UI should say `בינה מלאכותית`

## Merge caution

At creation time, this branch was made from `main`, but `main` later advanced. Before merge, sync/rebase this branch against the latest `main` and re-run QA.
