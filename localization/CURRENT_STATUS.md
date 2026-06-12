# Localization Project — Current Status

Updated: 2026-06-12

## Overall status

**Translation and Public Beta publication: complete.**

The complete Klingon and Neo-Quenya Public Beta editions are merged into `main` and published in all 77 mapped sections and five formats per language.

Release merge:

`89827cfe127ace4c18c426fbb8eb338be2f94578`

The original release deployment was verified for route availability, disclosure text, file signatures, exact sizes, and exact SHA-256 parity against `localization/beta-release-manifest.json`.

## Completed after publication

- Obsolete PR #5 closed without merge.
- Issues #10 and #11 updated to reflect the live Public Beta state.
- Reviewer links added to the Klingon and Neo-Quenya gateway pages in the repository.
- Production verifier expanded to check reviewer links and accept a deployed descendant of the target revision.
- Repository README updated with live editions and review paths.
- Official outreach routes and ready-to-send messages documented in `localization/SPECIALIST_OUTREACH.md`.
- Single reviewer entry point created at `localization/reviews/between-potential-and-ideal/020-EXTERNAL-SPECIALIST-HANDOFF.md`.
- Final completion boundary recorded in `localization/REVIEW_COMPLETION_CHECKLIST.md`.

## Open external dependencies

1. Independent Neo-Quenya response for issue #10.
2. Independent Klingon response for issue #11.
3. Authoritative production-status refresh confirming that the public gateway pages include the reviewer links added after the original release verification.

The first two items require independent human specialists. Their absence is not unfinished translation work and must not be replaced by an invented approval.

## Current next action

Circulate the prepared outreach messages through the documented official routes and accept only responses that satisfy the response template and pass `tools/preflight_external_specialist_review.py`.

No speculative translation edits are authorized while no valid specialist response exists.
