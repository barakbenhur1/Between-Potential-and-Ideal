# External Review Completion Checklist

Updated: 2026-06-12

## Release work

- [x] Complete Klingon Public Beta published.
- [x] Complete Neo-Quenya Public Beta published.
- [x] All 77 mapped sections included per language.
- [x] HTML, PDF, DOCX, Markdown, and plain text published per language.
- [x] Release manifest generated.
- [x] Public Beta disclosures preserved.
- [x] Release commit merged to `main`.
- [x] Original release deployment verified against the manifest.

## Reviewer intake

- [x] Immutable segment 020 packet prepared.
- [x] Neo-Quenya response template prepared.
- [x] Klingon response template prepared.
- [x] Automated preflight validator prepared.
- [x] Supplemental evidence traces indexed.
- [x] Public GitHub issue opened for Neo-Quenya review.
- [x] Public GitHub issue opened for Klingon review.
- [x] One-page handoff and snapshot download prepared.
- [x] Outreach routes and ready-to-send messages documented.
- [ ] Independent Neo-Quenya response received.
- [ ] Independent Klingon response received.

## Production follow-up

- [x] Public gateway pages include their Public Beta disclosures in the repository.
- [x] Public gateway pages include reviewer-request links in the repository.
- [x] Production verifier checks both reviewer-request links.
- [x] Production verifier accepts a deployed descendant of its target commit.
- [ ] Current gateway-link deployment recorded by the authoritative production-status workflow.

## Definition of completion

The translation and Public Beta publication project is operationally complete. The two unchecked specialist-response items are external review dependencies, not unfinished translation work.

When a valid response arrives:

1. Run `tools/preflight_external_specialist_review.py`.
2. Record valid intake without editing production text.
3. Evaluate every cited source and proposed correction.
4. Open a dedicated correction pull request based on current `main`.
5. Regenerate all affected public formats and `localization/beta-release-manifest.json`.
6. Run constructed-language audit, final release QA, and production verification.
7. Keep the Public Beta disclosure unless a separately documented release decision changes it.

Until then, do not invent a specialist decision and do not make speculative language changes merely to clear the remaining checkboxes.
