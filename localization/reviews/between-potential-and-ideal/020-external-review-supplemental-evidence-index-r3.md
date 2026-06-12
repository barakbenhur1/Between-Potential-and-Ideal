# Segment 020 external-review supplemental evidence index — round 3

Status: current reviewer handoff index. This document supplements, but does not modify, the immutable round-2 packet. It grants no linguistic approval, authorizes no production edit, and permits no publication.

## Immutable review target

Review the packet exactly as it existed at commit:

`fc1867f8e94bf588d8e3f2d9954207444a5083f8`

Packet:

`020-external-specialist-review-packet-r2.md`

The response templates remain:

- Neo-Quenya: `020-external-qya-review-response-template-r2.md`
- Klingon: `020-external-tlh-review-response-template-r2.md`

## Supplemental evidence produced after the packet

These documents reduce source-search ambiguity. They do not pre-answer any required reviewer decision.

### Neo-Quenya

1. `020-tamma-pusta-source-trace-r3.md`
   - traces `tamma` “tool” to candidate locator `PE17/108.0404` and related `TAM` material at `PE17/107.4010`;
   - traces cessation `pusta-` only to Middle Quenya candidates `Ety/PUS.006` and `Ety/PUS.042`;
   - records that direct primary-page verification, Late-profile compatibility, semantic breadth, transitivity, and construction-level approval remain unresolved.

2. `020-nonreplacement-source-trace-r3.md`
   - records a reproducible negative search for a safe Late Quenya replacement/nonreplacement lexeme;
   - rejects Middle Quenya `neuro` “follower, successor” as semantically non-equivalent and period-mismatched;
   - leaves role-separation sufficiency and any explicit negative construction for independent specialist decision.

### Klingon

1. `020-tlh-source-ledger-trace-r3.md`
   - traces candidate source locators for all 14 TLH-07 forms from pinned boQwI data release `2026.01.03a`;
   - separates verb/noun homographs for `choH`, `yIn`, `chaw'`, and `SeH`;
   - identifies grammar locators for `-bogh`, `'e'`, `-laH`, and `-pa'`;
   - leaves direct Okrand-source inspection, complete-construction naturalness, `mIw` breadth, voluntary bare `mev`, stop-before-control, and nonreplacement rulings unresolved.

## Reviewer-use rule

A reviewer must:

1. review the immutable packet at the pinned commit;
2. use the appropriate current response template;
3. consult the language-specific supplemental traces above;
4. independently inspect the named Tolkien or Okrand source wherever available;
5. mark unavailable or inconclusive evidence as `INSUFFICIENT EVIDENCE` rather than promoting a secondary index to primary/canonical proof.

The supplemental traces may be cited as reproducible search aids, but they cannot by themselves satisfy a template field that requires direct primary or canonical verification.

## Local preflight

Before opening a pull request, run the completed response through:

`tools/preflight_external_specialist_review.py`

Use `--language qya` for Neo-Quenya or `--language tlh` for Klingon. The command runs the same structural and substantive validators used by CI. A successful result confirms intake validity only and grants no linguistic approval or publication permission.

## Submission boundary

Submit only one completed language-specific response file under `localization/reviews/between-potential-and-ideal/`:

- `020-external-qya-review-response-r2.md`, or
- `020-external-tlh-review-response-r2.md`.

Do not edit `020-specialist-status.json`, production translation sources, publication files, the immutable packet, blank templates, or supplemental traces.

A valid response enters `valid-awaiting-status-sync`. That state records successful intake only; it does not approve a language, the segment, PR #6, or publication.
