# Visual QA Baseline

This document defines the manual screenshot and visual QA baseline before any CSS, image sizing, typography, or layout cleanup.

Do not perform CSS cleanup, redesign, image replacement, font changes, spacing changes, or layout refactors before this checklist has been completed.

## Required breakpoints

- Mobile narrow: 390px wide
- Tablet: 768px wide
- Desktop: 1440px wide
- Print/PDF preview for long theory documents

## Core pages to capture

- `/`
- `/en.html`
- `/pages/he/files.html`
- `/pages/en/files-en.html`
- `/pages/he/stories.html`
- `/pages/en/stories-en.html`
- `/pages/he/ai.html`
- `/pages/en/ai-en.html`

## Long documents to capture

- `/files/between-potential-and-ideal-he.html`
- `/files/between-potential-and-ideal-en.html`
- `/files/editorial-tightened/between-potential-and-ideal-tightened-he.html`
- `/files/editorial-tightened/between-potential-and-ideal-tightened-en.html`
- `/files/appendices/stories-before-thought-hebrew-rtl.html`
- `/files/appendices/stories-before-thought-english.html`

## AI dialogue pages to capture

- `/files/ai-believes/what-ai-believes-he.html`
- `/files/ai-believes/what-ai-believes-en.html`
- `/files/ai-believes/reverse-turing-conversation-he.html`
- `/files/ai-believes/reverse-turing-conversation-en.html`
- `/files/ai-believes/when-i-am-also-you-he.html`
- `/files/ai-believes/when-i-am-also-you-en.html`

## What to verify visually

- Hebrew pages are RTL and right-aligned.
- English pages are LTR and left-aligned.
- Header navigation wraps cleanly on mobile.
- File tables remain visually unchanged after accessibility improvements.
- Story appendices still show 16 stories in the protected order.
- Story TOC thumbnails are visible and not cropped badly.
- AI disclosure blocks appear near the top and do not break page layout.
- Theory document cover titles are centered.
- Chapter headings are aligned according to language.
- Chapter images have captions where expected.
- No temporary repair files, reports, or debug text appear on public pages.

## Screenshot storage rule

Do not commit screenshots by default.

If screenshots are needed for review, place them outside the repository or in a temporary folder that is not committed unless explicitly requested.

## Acceptance criteria before CSS cleanup

- Release guard passes.
- Live deploy URLs are reachable.
- Screenshot matrix has been manually reviewed.
- Any visual regressions are fixed before CSS cleanup begins.
- Only after this baseline may CSS consolidation be considered.
