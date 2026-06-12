# Segment 020 title remediation patch

Status: applied and mechanically verified. This file does not approve the segment and does not change publication status.

The edit was intentionally limited to one heading line per target-language file. No body content was changed.

## Klingon title line

File:

`localization/sources/tlh/between-potential-and-ideal/020-metamorphosis-code.md`

Replaced:

```md
## pung chuq je Metamorphosis Code
```

with this provisional localized heading:

```md
## pung chuq je choHmeH chut
```

Rationale:

- removes the unresolved English heading token `Metamorphosis`;
- uses existing provisional body direction around `choH` for transformation/change;
- uses `chut` only as a provisional governing-rule direction, not as final approval;
- preserves grace and distance as visible coordinated concepts;
- remains subject to Okrand-canonical specialist verification.

## Neo-Quenya title line

File:

`localization/sources/qya/between-potential-and-ideal/020-metamorphosis-code.md`

Replaced:

```md
## I Metamorphosis Code Lissëo ar Haiyava
```

with this provisional localized heading:

```md
## I Cantië Ahyaliëo Lissëo ar Haiyava
```

Rationale:

- removes unresolved English heading tokens `Metamorphosis` and `Code`;
- uses `cantië` only as the documented provisional candidate for governing pattern, not software code;
- uses the existing `ahyalië` direction for transformation/change and keeps it subject to morphological review;
- preserves grace and distance as visible coordinated concepts;
- remains subject to Late-Quenya-first specialist verification.

## Verification result

The line-aware constructed-language audit completed successfully on workflow run `27294229090`, head `e410db1308fa1265619cf400d70c439903db6bfa`.

Verified segment-020 result:

- `tlh_heading = 0`
- `tlh_body = 0`
- `qya_heading = 0`
- `qya_body = 0`

The source metadata remains `status: draft` and `publication: forbidden`. Mechanical clearance does not replace terminology validation, full specialist revision, or independent second review.

## PR status note

PR #6 must remain Draft. Segment 020 is now mechanically clear but is still linguistically unapproved, and the four-language release remains forbidden until all 77 paired segments are approved and every release gate passes.
