# Segment 020 title remediation patch

Status: ready-to-apply patch instruction. This file does not approve the segment and does not change publication status.

The GitHub contents update tool could not safely rewrite the full source files because it requires complete-file replacement. The intended edit is limited to one heading line per target-language file.

## Klingon title line

File:

`localization/sources/tlh/between-potential-and-ideal/020-metamorphosis-code.md`

Replace the current heading line:

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

Replace the current heading line:

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

## Required verification after applying

1. Re-run the line-aware constructed-language audit.
2. Expected segment-020 result: `tlh_heading = 0`, `tlh_body = 0`, `qya_heading = 0`, `qya_body = 0`.
3. Keep `status: draft`, `publication: forbidden`, and `approved: false`.
4. Continue terminology validation and second review before any approval decision.

## PR status note

PR #6 must remain Draft while this patch is unapplied. The current source files still contain the three heading findings recorded in the remediation baseline.
