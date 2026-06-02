# BPI Stage 3 — Inner Pages Premium Redesign Report

Branch: `bpi-premium-design-stage3`

## Purpose

Continue the visual redesign beyond the homepage and apply a unified premium visual layer to the rest of the site.

## Files added

- `site/assets/bpi-inner-pages-premium-redesign.css`

## Files updated

- `site/styles.css`

## Scope

The new CSS layer targets inner pages that already use the existing static site structure, including:

- Summary / תקציר
- Core / ליבה
- Witness / עדות
- Application / יישום
- Files / קבצים
- Methodology / מתודולוגיה
- Critique / ביקורת
- Sources / מקורות
- Glossary / מילון
- Concepts / מושגים
- AI / בינה מלאכותית
- AI as Witness / בינה מלאכותית כעדות

## Preservation rule

This stage is CSS-only for the inner page redesign layer. It does not delete, shorten, rewrite, summarize, merge, or replace page text.

Protected content remains protected:

- headings
- blurbs
- page intros
- story descriptions
- document descriptions
- CTAs
- Hebrew text
- English text
- links
- metadata

## Visual changes

The layer improves:

- inner-page background atmosphere
- sticky gradient header
- active nav state
- page-title hero cards
- page hero imagery
- reading layout
- side table of contents
- long-form reader cards
- archive/download cards
- story/document cards
- tables
- footer
- RTL/LTR layout polish
- mobile inner-page stacking

## Manual QA checklist

Check these pages locally after pulling the branch:

- `/pages/he/summary.html`
- `/pages/en/summary-en.html`
- `/pages/he/core.html`
- `/pages/en/core-en.html`
- `/pages/he/witness.html`
- `/pages/en/witness-en.html`
- `/pages/he/applied.html`
- `/pages/en/applied-en.html`
- `/pages/he/files.html`
- `/pages/en/files-en.html`
- `/pages/he/methodology.html`
- `/pages/en/methodology-en.html`
- `/pages/he/critique.html`
- `/pages/en/critique-en.html`
- `/pages/he/sources.html`
- `/pages/en/sources-en.html`
- `/pages/he/glossary.html`
- `/pages/en/glossary-en.html`
- `/pages/he/potential-ideal-optimal.html`
- `/pages/en/potential-ideal-optimal-en.html`
- `/pages/he/ai-as-witness.html`
- `/pages/en/ai-as-witness-en.html`

Check specifically:

- text remains readable
- no blurbs disappeared
- nav order is correct
- Hebrew remains RTL
- English remains LTR
- AI page images are not stretched
- long text is comfortable to read
- mobile has no horizontal scroll
- table/download pages remain usable
