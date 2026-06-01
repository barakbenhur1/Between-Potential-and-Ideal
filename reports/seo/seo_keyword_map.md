# BPI SEO Keyword Map

Implementation date: 2026-06-01
Scope: additive discoverability layer for Between Potential and Ideal.

## Guardrails applied

- Protected blurbs, arrows, symbolic separators, approved TOC items, approved Author's Note content, and language-switch text were not changed.
- No keyword stuffing was added.
- Structured data is limited to visible page content.
- Deployment verification is not treated as a blocker without commit hash, deploy log, hard refresh, incognito, page source, cache/CDN, and exact checked path evidence.

## Core page map

| Path | Language | Page type | Primary keyword | Search intent | Related pages | Paired language page |
|---|---|---|---|---|---|---|
| `/` | he | Home | בין פוטנציאל לאידיאל | Brand / concept entry | summary, core, glossary | `/en.html` |
| `/en.html` | en | Home | Between Potential and Ideal | Brand / concept entry | summary, core, glossary | `/` |
| `/pages/he/summary.html` | he | Summary | תקציר בין פוטנציאל לאידיאל | Understand theory quickly | core, glossary, how-to-read | `/pages/en/summary-en.html` |
| `/pages/en/summary-en.html` | en | Summary | Between Potential and Ideal summary | Understand theory quickly | core, glossary, how-to-read | `/pages/he/summary.html` |
| `/pages/he/core.html` | he | Core theory | פוטנציאל אידיאל אופטימלי | Deep conceptual reading | glossary, potential terms | `/pages/en/core-en.html` |
| `/pages/en/core-en.html` | en | Core theory | Potential Ideal Optimal | Deep conceptual reading | glossary, potential terms | `/pages/he/core.html` |
| `/pages/he/ai.html` | he | AI application | בינה מלאכותית כעד | AI / AI ethics readers | ai-as-witness, reverse turing | `/pages/en/ai-en.html` |
| `/pages/en/ai-en.html` | en | AI application | AI as witness | AI / AI ethics readers | ai-as-witness, reverse turing | `/pages/he/ai.html` |
| `/pages/he/files.html` | he | Collection page | קבצים בין פוטנציאל לאידיאל | Find downloadable files | citation, sources | `/pages/en/files-en.html` |
| `/pages/en/files-en.html` | en | Collection page | Between Potential and Ideal files | Find downloadable files | citation, sources | `/pages/he/files.html` |

## New additive gateway pages

| Path | Language | Page type | Primary keyword | Related pages |
|---|---|---|---|---|
| `/pages/en/glossary-en.html` | en | Glossary | Between Potential and Ideal glossary | summary, core, potential terms |
| `/pages/he/glossary.html` | he | Glossary | מילון מונחים בין פוטנציאל לאידיאל | summary, core, potential terms |
| `/pages/en/potential-ideal-optimal-en.html` | en | Concept gateway | Potential Ideal Optimal | core, glossary, applied |
| `/pages/he/potential-ideal-optimal.html` | he | Concept gateway | פוטנציאל אידיאל אופטימלי | core, glossary, applied |
| `/pages/en/ai-as-witness-en.html` | en | AI gateway | AI as witness | ai, reverse turing, files |
| `/pages/he/ai-as-witness.html` | he | AI gateway | בינה מלאכותית כעד | ai, reverse turing, files |
| `/pages/en/nihilism-with-hope-en.html` | en | Philosophy gateway | nihilism with hope | core, methodology, critique |
| `/pages/he/nihilism-with-hope.html` | he | Philosophy gateway | ניהיליזם עם תקווה | core, methodology, critique |
| `/pages/en/how-to-read-the-theory-en.html` | en | Reader guide | how to read Between Potential and Ideal | summary, files, stories |
| `/pages/he/how-to-read-the-theory.html` | he | Reader guide | איך לקרוא את בין פוטנציאל לאידיאל | summary, files, stories |
| `/pages/en/citation-en.html` | en | Citation guide | cite Between Potential and Ideal | files, sources, about |
| `/pages/he/citation.html` | he | Citation guide | איך לצטט את בין פוטנציאל לאידיאל | files, sources, about |

## Remaining safe next steps

1. Add visible Related reading links from existing home, summary, core, AI, and files pages to the new gateway pages through the existing generation pipeline.
2. Add reciprocal `x-default` hreflang to the two home pages when the pipeline can safely rewrite their head sections.
3. Run `git diff --check`, the SEO/accessibility audit, and final release QA after checkout.
4. If HTML content is regenerated, sync TXT/MD/DOCX/PDF through the existing pipeline.