# External Klingon specialist review request — segment 020

An independent specialist review is required for the Klingon candidate work in segment 020.

This is a bounded language review, not a request to approve PR #6 or any publication.

## Start here

- Review packet: `020-external-specialist-review-packet-r2.md`
- Response template: `020-external-tlh-review-response-template-r2.md`
- Submission guide: `020-external-review-submission-guide.md`
- Supplemental evidence index: `020-external-review-supplemental-evidence-index-r3.md`
- Klingon source-locator trace: `020-tlh-source-ledger-trace-r3.md`
- Packet commit: `fc1867f8e94bf588d8e3f2d9954207444a5083f8`

All files are in:

`localization/reviews/between-potential-and-ideal/`

The packet at the pinned commit remains the immutable review target. The round-3 ledger is a later secondary-index trace only: it does not amend the packet, replace direct Okrand-source inspection, or pre-answer a construction-level decision.

## Required output

Add one completed immutable response file:

`020-external-tlh-review-response-r2.md`

Before opening a pull request, run:

```bash
python3 tools/preflight_external_specialist_review.py \
  --language tlh \
  --response /path/to/020-external-tlh-review-response-r2.md
```

The preflight uses the same structural and substantive validators as CI. A `PASS` confirms intake validity only; it grants no linguistic approval and permits no production change or publication.

Do not edit the authoritative status file or production translation sources.
A valid contribution will enter `valid-awaiting-status-sync`; that means the
review was received and validated, not that it was approved for production.

## Core questions

The response must address all template items, including:

- `Prime Intellect choHbogh mIw`;
- `pung: vang yInbogh ghot 'e' chaw' Prime Intellect`;
- relative-clause head and subject/object scope;
- sentence-as-object scope with `'e'`;
- direct verification of the traced Okrand locators for `mIw`, `choH`, `-bogh`, `pung`, `vang`, `yIn`, `ghot`, `'e'`, `chaw'`, `jatlh`, `-laH`, `SeH`, `-pa'`, and `mev`;
- `mIw` semantic breadth, bare voluntary `mev`, and the stop-before-control idiom;
- role-sequence sufficiency versus a direct nonreplacement construction;
- a complete canonical source-locator ledger;
- literal and idiomatic back-translations and dangerous alternate readings.

Use only the required decision vocabulary:

- `PASS`
- `PASS WITH CORRECTION`
- `REJECT`
- `INSUFFICIENT EVIDENCE`

Every decision must include enough evidence to audit independently. A pinned boQwI trace may reduce search cost, but it must not be presented as direct Okrand canonical verification.
