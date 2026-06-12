# Segment 020 external specialist review submission guide

This guide defines the contribution path for independent Neo-Quenya and Klingon specialist reviews.

## Review target

Review the immutable packet at commit:

`fc1867f8e94bf588d8e3f2d9954207444a5083f8`

Packet:

`localization/reviews/between-potential-and-ideal/020-external-specialist-review-packet-r2.md`

## Submission paths

### Neo-Quenya

1. Copy `020-external-qya-review-response-template-r2.md`.
2. Complete every item and preserve every section.
3. Add the completed response as:
   `020-external-qya-review-response-r2.md`.

### Klingon

1. Copy `020-external-tlh-review-response-template-r2.md`.
2. Complete every item and preserve every section.
3. Add the completed response as:
   `020-external-tlh-review-response-r2.md`.

All paths are under:

`localization/reviews/between-potential-and-ideal/`

## Contributor boundary

External reviewers must not edit:

- `020-specialist-status.json`;
- production translation sources;
- title or body publication files;
- the review packet or blank templates.

A structurally and substantively valid response is accepted by CI as
`valid-awaiting-status-sync`. That state means only that the immutable review
was received and validated. It does not approve the segment, alter production,
or permit publication.

The maintainer separately synchronizes the authoritative status after reviewing
the submitted evidence.

## Required evidence

For every item, choose exactly one:

- `PASS`
- `PASS WITH CORRECTION`
- `REJECT`
- `INSUFFICIENT EVIDENCE`

Every decision must be auditable. Depending on the item, include exact primary
or canonical source locators, full grammatical analysis, literal and idiomatic
back-translations, alternate readings, period/profile compatibility, and a
specific explanation of unavailable evidence or rejection.

Placeholder values, unexplained decisions, invalid dates, mismatched signatures,
incomplete numbered answers, or non-auditable source ledgers are rejected by CI.

## Scope

A submitted specialist response reviews segment 020 only. It does not approve
PR #6 as a whole and does not authorize merging or publication.
