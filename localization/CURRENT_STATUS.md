# Localization Project — Current Status

Updated: 2026-06-13

## Overall status

**Translation, four-language site integration, and production verification: complete.**

The complete Klingon and Neo-Quenya Public Beta editions are merged into `main` and published in all 77 mapped sections and five formats per language.

Release merge:

`89827cfe127ace4c18c426fbb8eb338be2f94578`

The public site presents Hebrew, English, tlhIngan Hol, and Neo-Quenya through one globe language switcher in the header. The obsolete homepage Public Beta banner has been removed and is explicitly rejected by the build and production-verification gates.

A legacy navigation script was found replacing the four-language menu after page load with the previous Hebrew/English-only control. The conflict is repaired by `site/assets/bpi-four-language-runtime-guard.js`, loaded after the legacy script on every eligible page. It preserves the globe menu and all four language choices at runtime.

The live deployment is verified for both four-language menus, absence of the legacy banner, route availability, disclosure text on the localized editions, reviewer links, sitemap entries, file signatures, exact byte/SHA parity for stable formats, and normalized ZIP-content parity for DOCX packages. The authoritative result is recorded in `site/localization-public-beta-production-status.json` with `production_verified: true` for generated target commit `8b8ffb3d3488bcb445691ef8df63222768c75ded`.

## Completed after publication

- Obsolete PR #5 closed without merge.
- Issues #10 and #11 updated to reflect the live Public Beta state.
- Reviewer links added to both language gateway pages in the repository.
- One consistent globe language switcher added for all four languages.
- The Hebrew/English-only runtime replacement was repaired.
- Legacy Public Beta banner removed from the Hebrew and English homepages.
- Rebuild and exposure workflows prevent the banner from returning.
- Production verifier checks the four-language menus and rejects the legacy banner.
- README, outreach plan, reviewer handoff, and completion checklist added.
- Neo-Quenya routing request sent to the documented official scholarly contacts; no bounce or reply is currently recorded.
- Daily conditional monitoring enabled for email replies, GitHub review activity, and submitted response files.

## Open external dependencies

1. Independent Neo-Quenya response for issue #10.
2. Klingon request submission through an official KLI form, Discord, or subscribed discussion group. KLI publishes no direct email address on its official contact page, so no address was guessed.
3. Independent Klingon response for issue #11.

These are external dependencies, not unfinished site integration, translation, publication, or production-verification work.

## Current next action

The automated monitor will report new replies, review submissions, or relevant issue activity. The only manual action still required is submitting the prepared Klingon request through an official KLI web or community channel.

Accept only responses that pass `tools/preflight_external_specialist_review.py`. No speculative translation edits are authorized while no valid specialist response exists.
