# External Neo-Quenya specialist review request — segment 020

An independent specialist review is required for the Neo-Quenya candidate work in segment 020.

This is a bounded language review, not a request to approve PR #6 or any publication.

## Start here

- Review packet: `020-external-specialist-review-packet-r2.md`
- Response template: `020-external-qya-review-response-template-r2.md`
- Submission guide: `020-external-review-submission-guide.md`
- Supplemental evidence index: `020-external-review-supplemental-evidence-index-r3.md`
- Neo-Quenya exact-form trace: `020-tamma-pusta-source-trace-r3.md`
- Neo-Quenya nonreplacement trace: `020-nonreplacement-source-trace-r3.md`
- Packet commit: `fc1867f8e94bf588d8e3f2d9954207444a5083f8`

All files are in:

`localization/reviews/between-potential-and-ideal/`

The packet at the pinned commit remains the immutable review target. The round-3 traces are later search aids only: they do not amend the packet, establish primary-source verification, or pre-answer a decision.

## Required output

Add one completed immutable response file:

`020-external-qya-review-response-r2.md`

Before opening a pull request, run:

```bash
python3 tools/preflight_external_specialist_review.py \
  --language qya \
  --response /path/to/020-external-qya-review-response-r2.md
```

The preflight uses the same structural and substantive validators as CI. A `PASS` confirms intake validity only; it grants no linguistic approval and permits no production change or publication.

Do not edit the authoritative status file or production translation sources.
A valid contribution will enter `valid-awaiting-status-sync`; that means the
review was received and validated, not that it was approved for production.

## Core questions

The response must address all template items, including:

- `I Cantië yassë Prime Intellect ahya`;
- `Lissë: I Coirëa Quén Lelya Tierya`;
- directed-dialogue case constructions;
- capability and participant-agency constructions;
- direct verification and Late-profile compatibility of `pusta-` at the traced `Ety/PUS.006` and `Ety/PUS.042` candidates;
- role-sequence sufficiency versus a direct nonreplacement construction;
- direct verification and semantic breadth of `tamma` at the traced `PE17/108.0404` candidate;
- title styling, profile compatibility, literal and idiomatic back-translations,
  and dangerous alternate readings.

Use only the required decision vocabulary:

- `PASS`
- `PASS WITH CORRECTION`
- `REJECT`
- `INSUFFICIENT EVIDENCE`

Every decision must include enough evidence to audit independently. A pinned secondary-index trace may reduce search cost, but it must not be presented as direct Tolkien primary-source verification.
