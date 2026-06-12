# External Specialist Review Handoff — Segment 020

This is the single entry point for independent review of segment 020 in the live Public Beta Klingon and Neo-Quenya editions of **Between Potential and Ideal**.

Publication as Public Beta does not claim specialist approval. This handoff requests a bounded, auditable linguistic assessment only.

## Immutable review snapshot

Review packet commit:

`fc1867f8e94bf588d8e3f2d9954207444a5083f8`

Download the complete immutable repository snapshot:

`https://github.com/barakbenhur1/Between-Potential-and-Ideal/archive/fc1867f8e94bf588d8e3f2d9954207444a5083f8.zip`

Or check it out with Git:

```bash
git clone https://github.com/barakbenhur1/Between-Potential-and-Ideal.git
cd Between-Potential-and-Ideal
git checkout fc1867f8e94bf588d8e3f2d9954207444a5083f8
```

The immutable packet is the decision basis. Files added later as supplemental traces are search aids only and do not replace direct primary-source verification.

## Shared files

Under `localization/reviews/between-potential-and-ideal/`:

- `020-external-specialist-review-packet-r2.md`
- `020-external-review-submission-guide.md`
- `020-external-review-supplemental-evidence-index-r3.md`

## Neo-Quenya review

Tracking issue:

`https://github.com/barakbenhur1/Between-Potential-and-Ideal/issues/10`

Required packet files:

- `020-external-qya-review-request.md`
- `020-external-qya-review-response-template-r2.md`
- `020-tamma-pusta-source-trace-r3.md`
- `020-nonreplacement-source-trace-r3.md`

Submit exactly:

`localization/reviews/between-potential-and-ideal/020-external-qya-review-response-r2.md`

Validate before opening the pull request:

```bash
python3 tools/preflight_external_specialist_review.py \
  --language qya \
  --response localization/reviews/between-potential-and-ideal/020-external-qya-review-response-r2.md
```

## Klingon review

Tracking issue:

`https://github.com/barakbenhur1/Between-Potential-and-Ideal/issues/11`

Required packet files:

- `020-external-tlh-review-request.md`
- `020-external-tlh-review-response-template-r2.md`
- `020-tlh-source-ledger-trace-r3.md`

Submit exactly:

`localization/reviews/between-potential-and-ideal/020-external-tlh-review-response-r2.md`

Validate before opening the pull request:

```bash
python3 tools/preflight_external_specialist_review.py \
  --language tlh \
  --response localization/reviews/between-potential-and-ideal/020-external-tlh-review-response-r2.md
```

## Required decision form

Every requested item must use exactly one decision:

- `PASS`
- `PASS WITH CORRECTION`
- `REJECT`
- `INSUFFICIENT EVIDENCE`

Every decision must include:

1. Auditable lexical and grammatical evidence from the relevant primary sources.
2. A back-translation.
3. Analysis of plausible alternate readings.
4. A concrete correction when the decision is `PASS WITH CORRECTION` or `REJECT`.

## Scope boundary

A valid response records an independent assessment of the bounded segment only. It does not:

- approve the complete edition;
- certify the edition as canonical;
- remove the Public Beta disclosure;
- directly modify production text;
- authorize publication retroactively.

Accepted evidence is evaluated in a separate correction pull request. All affected public formats, the release manifest, release QA, and production verification must then be regenerated before a correction becomes live.
