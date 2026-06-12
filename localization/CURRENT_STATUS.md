# Localization Project — Current Status

Updated: 2026-06-12

## Overall status

**Translation and Public Beta publication: complete.**

The complete Klingon and Neo-Quenya Public Beta editions are merged into `main` and published in all 77 mapped sections and five formats per language.

Release merge:

`89827cfe127ace4c18c426fbb8eb338be2f94578`

The live deployment is verified for route availability, disclosure text, reviewer links, file signatures, exact sizes, and exact SHA-256 parity against the current localization manifests. The authoritative result is recorded in `site/localization-public-beta-production-status.json` with `production_verified: true`.

## Completed after publication

- Obsolete PR #5 closed without merge.
- Issues #10 and #11 updated to reflect the live Public Beta state.
- Reviewer links added to both language gateway pages in the repository.
- Production verifier expanded to check reviewer links and exact deployed content parity.
- README, outreach plan, reviewer handoff, and completion checklist added.
- Neo-Quenya routing request sent to the documented official scholarly contacts; no bounce or reply is currently recorded.
- Daily conditional monitoring enabled for email replies, GitHub review activity, and submitted response files.

## Open external dependencies

1. Independent Neo-Quenya response for issue #10.
2. Klingon request submission through an official KLI form, Discord, or subscribed discussion group. KLI publishes no direct email address on its official contact page, so no address was guessed.
3. Independent Klingon response for issue #11.

These are external dependencies, not unfinished translation, publication, or production-verification work.

## Current next action

The automated monitor will report new replies, review submissions, or relevant issue activity. The only manual action still required is submitting the prepared Klingon request through an official KLI web or community channel.

Accept only responses that pass `tools/preflight_external_specialist_review.py`. No speculative translation edits are authorized while no valid specialist response exists.
