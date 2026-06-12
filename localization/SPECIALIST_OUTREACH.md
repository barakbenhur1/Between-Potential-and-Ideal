# Specialist Outreach Plan

Updated: 2026-06-12

## Purpose

Obtain independent, auditable reviews of the bounded segment 020 packets for the live Klingon and Neo-Quenya Public Beta editions.

This is a request for review, not a claim of endorsement. No organization or individual is listed as having accepted, approved, or reviewed the editions unless a response is actually received and recorded.

Current project state:

- Canonical project status: `localization/CURRENT_STATUS.md`
- Neo-Quenya review request: GitHub issue #10
- Klingon review request: GitHub issue #11
- Single reviewer handoff: `localization/reviews/between-potential-and-ideal/020-EXTERNAL-SPECIALIST-HANDOFF.md`
- Production proof: `site/localization-public-beta-production-status.json`

## Klingon outreach order

### 1. Klingon Language Institute contact form

Use the official KLI contact page to ask which staff member or experienced speaker is the appropriate recipient for a bounded grammatical review.

Official route:

`https://www.kli.org/about-klingon/contact-the-kli/`

The official page provides a JavaScript contact form plus Facebook and Discord routes. It does not publish a direct email address. Do not guess an address or imply that the KLI sponsors or endorses the project.

### 2. KLI email discussion group

The official KLI site describes the `tlhIngan-Hol` list as a long-running discussion forum with learners and advanced speakers. Subscription is required before normal posting.

Official route:

`https://www.kli.org/activities/email-discussion-group/`

Post only a concise request linking issue #11. Do not paste the complete translated work into the list.

### 3. KLI Discord community

The official KLI site describes its Discord as a place to ask grammatical questions and interact with advanced speakers.

Official route:

`https://www.kli.org/activities/discord/`

Ask a moderator where a structured segment-review request belongs before posting the packet.

## Neo-Quenya outreach order

### 1. Elvish Linguistic Fellowship

The E.L.F. identifies itself as an international organization devoted to scholarly study of Tolkien's invented languages and publishes `Vinyar Tengwar`, `Parma Eldalamberon`, and `Tengwestië`.

Official route:

`https://www.elvish.org/`

The request must preserve the project's explicit `Neo-Quenya` and `modern reconstruction` labels. It must not ask anyone to certify the text as Tolkien-authored or canonical.

### 2. Mythopoeic Society routing request

The E.L.F. is identified on its own site as a Special Interest Group of the Mythopoeic Society. The Society's contact page provides a general route when no listed category fits.

Official route:

`https://www.mythsoc.org/contact.htm`

Ask only for routing to a suitable Tolkienian linguistics reviewer or group. Do not imply that the Society has reviewed the project.

## Initial outreach message — Klingon

Subject: Bounded independent Klingon review request — segment 020

Hello,

I maintain a clearly disclosed Public Beta Klingon edition of *Between Potential and Ideal*. I am seeking an independent, evidence-based review of one bounded segment, not approval of the complete edition.

The review request, immutable packet references, response template, and preflight instructions are collected in GitHub issue #11:

`https://github.com/barakbenhur1/Between-Potential-and-Ideal/issues/11`

The requested review requires Okrand-canonical lexical and grammatical evidence, back-translations, and alternate-reading analysis. The live edition remains labelled Public Beta and is not presented as canonical Klingon.

Could you direct this request to an appropriate experienced reviewer or tell me the correct community channel for it?

Thank you.

## Initial outreach message — Neo-Quenya

Subject: Bounded independent Neo-Quenya review request — segment 020

Hello,

I maintain a clearly disclosed Neo-Quenya Public Beta edition of *Between Potential and Ideal*. It is explicitly labelled a modern reconstruction and is not represented as Tolkien-authored text. I am seeking an independent, evidence-based review of one bounded segment, not approval of the complete edition.

The review request, immutable packet references, response template, and preflight instructions are collected in GitHub issue #10:

`https://github.com/barakbenhur1/Between-Potential-and-Ideal/issues/10`

The requested review requires direct primary-source and grammatical evidence, back-translations, chronological compatibility analysis, and alternate readings.

Could you route this request to an appropriate Tolkienian linguistics reviewer or discussion group?

Thank you.

## Outreach log

Record actual contact attempts only after they occur.

| Date | Language | Channel | Recipient or group | Result | Follow-up |
|---|---|---|---|---|---|
| 2026-06-12 | Neo-Quenya | Email | Elvish Linguistic Fellowship (`Aelfwine@elvish.org`), CC Mythopoeic Society communications | Sent successfully from `barakbenhur@gmail.com`; no bounce or reply recorded at the time of this update | Monitor the existing Gmail thread; record any reply before treating it as review intake |
| 2026-06-12 | Klingon | KLI official contact routes | Klingon Language Institute | Not sent: the official page exposes a JavaScript form, Facebook, and Discord but no public direct email address; no address was guessed | Submit the prepared Klingon message through the official KLI form or Discord, then record the actual attempt here |

## Intake rule

An informal comment, chat response, routing reply, or expression of interest is not a completed specialist review. Only a response that follows the issue instructions and passes `tools/preflight_external_specialist_review.py` enters the formal intake workflow.
