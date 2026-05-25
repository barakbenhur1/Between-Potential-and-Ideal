# QA implementation note — 2026-05-25

This note records the repository-side implementation of the latest critic reports.

## Sources used

The patch follows the uploaded critic/QA reports from 2026-05-25. The main actionable findings were:

- AI section must become a product screen: cards only, no file dump, no `Completed AI English files`, clear labels for Hebrew original / English full / English adaptation.
- Preserve the poetic voice, blurbs, intentional oddities, and self-critique.
- Do not flatten the site into dry academic prose.
- Separate public reader pages from archive/build/report material.
- Add repository documentation describing the project and file structure.
- Keep AI framing strict: AI is mirror/witness/tool, not machine personhood.

## Implemented changes

### Public AI pages

Rebuilt these pages as clean public product pages:

- `site/pages/he/ai.html`
- `site/pages/en/ai-en.html`

The new pages include:

- a concise hero;
- a visible caution about AI and living witness;
- three document cards only;
- no raw file dump;
- no build/completion headings;
- format buttons for HTML/PDF/DOCX/MD;
- language labels and links between Hebrew and English.

### Repository documentation

Added:

- `docs/PROJECT_STRUCTURE.md`

This file explains:

- the purpose of the project;
- repository structure;
- public pages versus long document files;
- AI section rules;
- image rules;
- export rules;
- accessibility/SEO checklist;
- deployment and do-not-commit rules.

## Explicitly preserved

The implementation did **not** rewrite or remove the public blurbs. It did not remove poetic material, intentional language, theory content, source discipline, or self-critique.

## Still recommended later

The critic reports include additional possible work that was not fully automated in this commit:

1. Deeper source-map table for scientific/philosophical claims.
2. Full audit of mathematical typography in every generated PDF/DOCX.
3. Further separation of internal QA/build reports from public-facing archives.
4. Mobile screenshot parity pass.
5. Lighthouse/axe/keyboard accessibility pass.

## Verification checklist

After deploy, verify:

```bash
open site/pages/he/ai.html
open site/pages/en/ai-en.html
open docs/PROJECT_STRUCTURE.md
```

Live checks:

- Hebrew AI page shows only product cards.
- English AI page shows only product cards.
- No `Completed AI English files` text appears on public AI pages.
- AI document buttons resolve to existing files.
- BlurBs and poetic homepage material remain untouched.
