# External Review Status

Updated: 2026-06-12

## Published state

- Klingon and Neo-Quenya are live as Public Beta editions.
- Release commit: `89827cfe127ace4c18c426fbb8eb338be2f94578`.
- Production status: `site/localization-public-beta-production-status.json` reports `production_verified: true`.
- All 77 sections and all five formats per language are published.

## Open reviews

- Neo-Quenya segment 020: issue #10 — awaiting an independent specialist response.
- Klingon segment 020: issue #11 — awaiting an independent specialist response.

## Next action

Accept only responses that pass `tools/preflight_external_specialist_review.py`. After a valid response, review the evidence, prepare a dedicated correction pull request, regenerate every affected format and the release manifest, rerun release QA, and verify production again.

Public Beta publication does not claim independent specialist approval. No speculative source change is authorized while the specialist responses are absent.
