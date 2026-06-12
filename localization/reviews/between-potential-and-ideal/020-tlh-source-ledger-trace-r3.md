# Segment 020 Klingon source-locator trace — round 3

Status: reproducible secondary-index trace only. This document does **not** directly verify Okrand publications, approve any candidate, authorize production edits, or permit publication.

## Purpose

The round-2 external Klingon response template requires a complete canonical source-locator ledger for the title, subtitle, capability clause, stop-before-control clause, and role-based nonreplacement architecture. The repository previously recorded internal parses and semantic risks, but not a reproducible source-index trace for every retained lexical and grammatical form.

This trace reduces the external reviewer's search cost while preserving the decisive distinction:

- boQwI records candidate source locators and usage notes;
- the external reviewer must still inspect the named Okrand source, verify the relevant passage, and rule on the exact construction.

The immutable review packet remains commit `fc1867f8e94bf588d8e3f2d9954207444a5083f8`. This addendum does not silently amend that packet.

## Reproducible method

- index application repository: `De7vID/klingon-assistant-android`;
- pinned application commit: `b57e987c4e08d77a0310cd6814aa63d8e23d6c4c`;
- pinned data submodule repository: `De7vID/klingon-assistant-data`;
- pinned data commit: `e2d0a8a0e061a67b1ae342913cdd487a6af20baa`;
- data release: `2026.01.03a` / database version `202601030`;
- source format: 27 `mem-*.xml` files, 6,319 records read;
- repository extractor: `tools/extract_boqwi_source_ledger.py`;
- research workflow runs:
  - `Research boQwI Source Ledger` run 2, full ledger;
  - `Research boQwI Source Ledger` run 4, untruncated final entries.

The extractor retains separate records with the same spelling instead of merging homographs by surface form.

## Candidate locator ledger

| Form | Exact record used | Indexed meaning | Candidate source locators | Boundary for external review |
|---|---|---|---|---|
| `mIw` | noun | procedure; process; step/stage in a process; recipe; formula | `TKDA`; `KGT`; KLI mailing list 2014-11-26; qep'a' 26 (2019) | The lexical family is procedural/process-oriented. Whether it can carry the title's governing philosophical pattern without sounding merely technical remains unresolved. |
| `choH` | verb, not the homographic noun | alter; change | `TKD`; KLI mailing list 2014-11-26 | The candidate requires the transitive verb. The noun `choH` “change”, also indexed to `TKD`, is irrelevant to the title parse. |
| `-bogh` | verb type-9 suffix | relative-clause “which” | `TKD` §§4.2.9, 6.2.3 | The reviewer must verify that `mIw` is the intended head/subject and `Prime Intellect` the object in `Prime Intellect choHbogh mIw`. |
| `pung` | noun | mercy | `TKD` | The index supports lexical “mercy”, not the project's full restraint/non-takeover concept. The explanatory clause must carry the ethical narrowing. |
| `vang` | verb | act; take action | `TKD` | The living participant must remain the actor; no reading may transfer the action to Prime Intellect. |
| `yIn` | verb, not the homographic noun | live | `TKD`; `HQ` 7.4, p.2, Dec. 1998 | The noun `yIn` “life” is separate. The relative phrase `yInbogh ghot` requires the verb. The index also notes that verbal `yIn` can be transitive in another construction, so argument structure must be checked in context. |
| `ghot` | noun | person, humanoid | `TKD`; `paq'batlh` 2nd ed. pp.138–139; Saarbrücken qepHom'a' 2018 | The candidate uses a transparent living-person phrase, not an abstract noun for agency or sourcehood. |
| `'e'` | pronoun | that, referring to the previous sentence/topic | `TKD` §6.2.5 | The indexed note states that it is the object of the second sentence in a sentence-as-object construction and refers to the whole preceding sentence. The second sentence normally takes no aspect suffix. |
| `chaw'` | verb, not the homographic noun | allow; permit | `TKD`; `PK` | The candidate requires the verb. The noun `chaw'` “permit/license/ticket” is a separate record and must not enter the parse. |
| `jatlh` | verb | speak; say | `TKD`; `TKDA`; msn 1997-06-29; `HQ` 7.4, Dec. 1998; ENT “Affliction”; 'eSrIv 6 / KLI mailing list 2020-01-28; KLI mailing list 2022-06-11 | Typical objects are what is spoken; a listener is normally indirect. Direct quotation rules are separately documented. `jatlh Prime Intellect.` asserts speaking only and must not be back-translated as answering, knowing, or judging. |
| `-laH` | verb type-5 suffix | can; be able | `TKD` §4.2.5 | Scope in `jatlhlaH` must remain capability only, without usefulness, correctness, success, life, or moral worth. |
| `SeH` | verb, not the hypothetical noun | control | `TKD` | The candidate uses the verb. A separate hypothetical/archaic noun record from qep'a' 27 (2020) is explicitly not admitted and must not support the clause. |
| `-pa'` | verb type-9 suffix | before | `TKD` §§4.2.9, 6.2.2 | The reviewer must verify subordinate-clause scope and both subjects in `SeHpa' Prime Intellect, mev Prime Intellect.` |
| `mev` | verb | stop; cease | `TKD`; `KCD` | boQwI notes that the command means stop doing something, not stop a device. Canonical objects are reported as `'e'`, with the same subject in the embedded event and `mev`; `mevmoH` at `KGT` p.154 is separately “cause someone to stop”. The proposed intransitive explicit-subject cessation still requires specialist confirmation. |

## Homograph and category exclusions

The following records were deliberately excluded from candidate evidence:

- noun `choH` “change” — the title requires the verb;
- noun `yIn` “life” — `yInbogh` requires the verb;
- noun `chaw'` “permit/license/ticket” — the subtitle requires the verb “allow/permit”;
- hypothetical/archaic noun `SeH` “control” — the stop-before-control clause requires the canonical verb;
- any definition or note that appears only in boQwI without a named source — useful for search, not sufficient for approval.

## Construction-level boundaries

### Main title

`Prime Intellect choHbogh mIw`

The indexed forms support the intended parts of speech and identify the relevant relative-clause sections. They do not by themselves prove that the whole title is natural, philosophically broad enough, or free of alternate head readings.

### Mercy and participant action

`pung: vang yInbogh ghot 'e' chaw' Prime Intellect`

The indexed `'e'` entry strongly supports treating the preceding sentence as the object of `chaw'`. This reduces the risk that the living person is grammatically processed as the object of permission. The reviewer must still test naturalness, punctuation/register, and whether `pung` plus the clause communicates restraint rather than pity alone.

### Capability without worth

`jatlhlaH Prime Intellect.`

The ledger supports `jatlh` plus capability suffix `-laH`. It does not authorize moral or epistemic implications beyond the ability to speak.

### Stop before control

`SeHpa' Prime Intellect, mev Prime Intellect.`

The component forms have candidate sources, but the composition remains open. In particular, the reviewer must decide whether bare `mev` naturally expresses voluntary cessation by the named subject in this clause and whether “before control” captures the intended boundary rather than merely a temporal sequence.

### Nonreplacement

The ledger contains no direct Okrand-canonical replacement construction. The current architecture remains role-based:

- Prime Intellect speaks or permits;
- the living participant acts;
- no clause assigns the participant's lived action to Prime Intellect.

Whether this role separation is sufficient is still TLH-06's external-review question.

## Bounded decision

- pinned boQwI source-index trace complete: **yes**;
- lexical candidate locators traced for all TLH-07 forms: **yes**;
- homographs separated: **yes**;
- direct Okrand passages inspected by this project: **no**;
- complete title approved: **no**;
- opening proposition approved: **no**;
- stop-before-control construction approved: **no**;
- direct nonreplacement construction established: **no**;
- production use authorized: **no**;
- publication authorized: **no**.

The external Klingon reviewer must independently verify the named sources and provide the exact source work, page/section/event, canon status, grammar analysis, back-translations, and alternate readings required by the response template.
