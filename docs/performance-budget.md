# Performance Budget and Asset Policy

This document defines the performance and asset rules for the static site.

Do not delete, compress, replace, rename, or move images, documents, CSS, fonts, or public files without explicit approval.

Do not perform CSS cleanup before the visual QA baseline has been completed.

## Goals

- Keep the site static and easy to deploy.
- Prevent accidental removal of public files.
- Prevent image/path regressions.
- Make future optimization measurable instead of destructive.

## Performance budget targets

These are target budgets for future measurement, not automatic deletion rules.

- Home pages should remain lightweight and fast on mobile.
- Critical CSS should not grow without reason.
- New images should include width/height or stable layout behavior where practical.
- Large images should be justified by document/story value.
- PDF/DOCX/HTML/MD/TXT variants should remain available unless explicitly removed.

## Image policy

- Do not replace existing story or chapter images unless explicitly requested.
- Do not delete unused-looking images without an asset reference audit.
- Do not change image crops globally.
- Do not change chapter image style without screenshot comparison.
- Every public image reference must point to an existing file.

## CSS policy

- Do not remove CSS only because it looks duplicated.
- Do not remove inline styles before screenshot comparison.
- Do not change global typography, palette, spacing, or direction rules without explicit approval.
- CSS consolidation is allowed only after visual QA baseline and final release QA pass.

## Document/file policy

- Preserve HTML, PDF, DOCX, MD, and TXT variants unless explicitly told otherwise.
- Do not remove editorial, tightened, full, appendix, or AI dialogue files.
- Do not rename public files without redirect/cross-link review.

## Future measurement checklist

Before any real performance cleanup:

- Run final release QA.
- Run live deploy URL check.
- Complete visual QA baseline.
- Record before/after screenshots.
- Measure Lighthouse or equivalent on mobile and desktop.
- Review changed files with `git diff --stat` and `git diff --check`.

## Acceptance criteria

- No optimization commit may remove files unless explicitly approved.
- No CSS cleanup may happen before visual QA.
- No image compression/replacement may happen without checking visual output.
- Performance work must be measurable and reversible.
