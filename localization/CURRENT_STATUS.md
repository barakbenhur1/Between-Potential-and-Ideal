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
- Reviewer links added to both language gateway pages in the repository.
- Production verifier expanded to check reviewer links and deployed descendants.
- README, outreach plan, reviewer handoff, and completion checklist added.
- Neo-Quenya routing request sent to the documented official scholarly contacts; no bounce or reply is currently recorded.
- Daily conditional monitoring enabled for email replies, GitHub review activity, submitted response files, and production-verification changes.

## Open external dependencies

1. Independent Neo-Quenya response for issue #10.
2. Klingon request submission through an official KLI form, Discord, or subscribed discussion group. KLI publishes no direct email address on its official contact page, so no address was guessed.
3. Independent Klingon response for issue #11.
4. Production-status refresh for the post-release reviewer links.

These are external dependencies, not unfinished translation work.

## Current next action

The automated monitor will report new replies, review submissions, relevant issue activity, or a production-status update. The only manual action still required is submitting the prepared Klingon request through an official KLI web or community channel.

Accept only responses that pass `tools/preflight_external_specialist_review.py`. No speculative translation edits are authorized while no valid specialist response exists.
