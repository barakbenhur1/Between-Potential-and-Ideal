# Segment 020 `tamma` and `pusta-` source trace — round 3

Status: reproducible secondary-index source trace. This is **not** primary-source verification, specialist approval, or production authorization. Production source remains unchanged. Publication remains forbidden.

## Purpose

The round-2 boundary record knew that the pinned Eldamo course listed unmarked `tamma` “tool” and `pusta-` “to stop”, but it did not contain exact source locators or period classification. This trace narrows those questions using Eldamo's pinned XML data rather than the abbreviated course glossary.

The immutable external packet remains commit `fc1867f8e94bf588d8e3f2d9954207444a5083f8`. This document is a supplemental locator trace only; it does not silently amend the packet or pre-answer the external specialist.

## Reproducible method

- Upstream repository: `pfstrack/eldamo`
- Pinned upstream commit: `4071c9caa95caca905c96af2505d5252045e2aaa`
- Pinned data file: `src/data/eldamo-data.xml`
- Downloaded byte count: `30,325,949`
- Repository extractor: `tools/extract_eldamo_source_candidates.py`
- Verified research workflow run: `Research Eldamo Source Candidates` run `5`
- Exact-form matching normalizes only a trailing hyphen, then records language code, form, gloss, part of speech, and source references.

The extractor returned three distinct records for `tamma` and seven for `pusta`; homographs and grammatical elements were kept separate rather than merged by spelling.

## `tamma` — traced candidate

Relevant exact record:

- language code: `q` — the Eldamo data's Late Quenya category;
- form: `tamma`;
- gloss: `tool`;
- part of speech: noun;
- indexed source locator: `PE17/108.0404`;
- indexed derivational record: `TAM`, `PE17/107.4010`.

Excluded homograph:

- Noldorin `tamma-` “to knock” is a different language, verb, and sense; it provides no evidence for Quenya `tamma` “tool”.

### Bounded decision

The exact **candidate locator and period direction are now traced**. This is stronger than the course-glossary entry, but it is still a secondary-index result. The project has not directly inspected and transcribed the relevant `PE17/108` primary passage.

Therefore:

- exact index locator traced: **yes**;
- Late-Quenya category in pinned index: **yes**;
- direct primary-page verification: **no**;
- generic ethical-tool sense approved: **no**;
- substitution for protected `Prime Intellect`: **forbidden**;
- production use: **forbidden**.

The external reviewer must verify the primary passage, confirm the noun's actual sense boundary, and decide whether “tool” is broad enough for a generic ethical discussion without reducing an intelligence or model to a physical implement.

## `pusta-` — traced period mismatch

Relevant exact verb record:

- language code: `mq` — Middle Quenya, not Late Quenya;
- form: `pusta-`;
- gloss: `to stop, put a stop to, cease`;
- part of speech: verb;
- indexed source locators:
  - `Ety/PUS.006`, including “to stop, put a stop to, cease (intr.), stop (intr.)”;
  - `Ety/PUS.042`, “to stop”;
- indexed derivational roots:
  - `PUS`, `Ety/PUS.001`;
  - `PUT`, `Ety/PUS.035`.

Separate exact records that must not be conflated with the verb:

- Middle Quenya noun `pusta` “stop, in punctuation full stop”, including `Ety/PUS.017`;
- Early Qenya `pusta-` “to blow”, reconstructed from an inflected form and unrelated to the intended cessation sense;
- grammatical/compound element records that do not independently establish a Late Quenya verb.

No exact `q` / Late Quenya verb record for cessation was returned by the pinned-data extraction.

### Bounded decision

The previous statement “exact Tolkien primary locator and period are not recorded” is now narrowed:

- candidate primary locators traced: **yes**;
- indexed period: **Middle Quenya**;
- Late-Quenya-first compatibility established: **no**;
- direct primary-page verification: **no**;
- voluntary explicit-subject clause approved: **no**;
- “before control” construction approved: **no**;
- production use: **forbidden**.

Under the project's Late-Quenya-first profile, `Prime Intellect pusta.` cannot be promoted merely because the Neo-Quenya course glossary lists `pusta-` without a warning marker. The exact source trace instead exposes a period mismatch. A specialist may still discuss a transparent Middle-to-Late adaptation, but must label and justify it explicitly; absent that justification, the safe decision is `REJECT` or `INSUFFICIENT EVIDENCE`, not `PASS`.

## External-review handoff

For QYA-06, the reviewer should verify `Ety/PUS.006` and `Ety/PUS.042`, distinguish transitive and intransitive readings, and state whether any Late-compatible adaptation is defensible. If not, they should propose a separately sourced Late construction or prohibit the form.

For QYA-08, the reviewer should verify `PE17/108.0404` and the related `TAM` material at `PE17/107.4010`, then rule on the semantic breadth and philosophical risk of `tamma`.

These locator candidates reduce search cost; they do not replace direct source access, grammatical analysis, or independent specialist judgment.
