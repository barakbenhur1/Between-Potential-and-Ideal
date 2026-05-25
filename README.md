# Between Potential and Ideal

Static bilingual website and document archive for **Between Potential and Ideal** / **בין פוטנציאל לאידיאל**.

The project presents the theory, its logical and philosophical versions, appendices, AI dialogues, source material, and public reading pages. The repository should be treated as a public product, not as a scratch folder.

## Live site

The public site is deployed as a static website:

- Hebrew entry: `site/index.html`
- English entry: `site/en.html`

## Repository structure

```text
.
├── README.md
├── docs/
│   ├── PROJECT_STRUCTURE.md
│   └── QA_IMPLEMENTATION_2026_05_25.md
├── tools/
│   ├── fix_theory_cover_toc_gap.py
│   └── fix_logical_pdf_buttons.py
├── site/
│   ├── index.html
│   ├── en.html
│   ├── styles.css
│   ├── styles-base.css
│   ├── assets/
│   │   ├── bpi-global-document-buttons.css
│   │   └── bpi-ai-section-polish.css
│   ├── figures/
│   │   └── site and document images
│   ├── pages/
│   │   ├── he/
│   │   │   └── Hebrew public pages
│   │   └── en/
│   │       └── English public pages
│   └── files/
│       ├── main theory documents
│       ├── editorial-tightened/
│       ├── appendices/
│       └── ai-believes/
└── _product_docs/
    └── reports/
```

## Main public pages

The reader-facing site is under `site/pages`.

Hebrew pages:

```text
site/pages/he/summary.html
site/pages/he/core.html
site/pages/he/witness.html
site/pages/he/applied.html
site/pages/he/ai.html
site/pages/he/files.html
site/pages/he/methodology.html
site/pages/he/critique.html
site/pages/he/sources.html
```

English pages:

```text
site/pages/en/summary-en.html
site/pages/en/core-en.html
site/pages/en/witness-en.html
site/pages/en/applied-en.html
site/pages/en/ai-en.html
site/pages/en/files-en.html
site/pages/en/methodology-en.html
site/pages/en/critique-en.html
site/pages/en/sources-en.html
```

## Document archive

Long-form documents and export formats live under `site/files`.

Important areas:

```text
site/files/                              Main theory files
site/files/editorial-tightened/          Logical / tightened theory versions
site/files/appendices/                   Appendix and story files
site/files/ai-believes/                  AI dialogue files
```

Where a document is advertised publicly, keep related formats symmetric when they exist:

```text
HTML / PDF / DOCX / MD / TXT
```

The public Files page should not duplicate formats already shown in another adjacent card. For example, if `בתוך התאוריה` already exposes full/logical HTML/PDF, `קבצי מקור` should focus only on source/archive formats that are not already shown there.

## Design and content rules

These rules are important for future edits:

1. Do not remove or rewrite blurbs, poetic openings, intentional oddities, or deliberate phrases unless a task explicitly asks for that.
2. Do not “correct” intentional concepts such as `אין`, `יש`, and `יש מאין` just because they look unusual.
3. Any design change must be symmetric across related pages, languages, formats, and cards.
4. If one tab page receives a visual/design rule, apply the same rule to the matching tab pages where relevant.
5. Keep Hebrew RTL and English LTR correct.
6. Public pages should feel like product pages, not raw file dumps.
7. Long files belong in `site/files`; public tabs should guide reading rather than expose clutter.

## Styling

Global styling starts at:

```text
site/styles.css
```

`site/styles.css` imports:

```text
site/styles-base.css
site/assets/bpi-global-document-buttons.css
```

Focused styles:

```text
site/assets/bpi-global-document-buttons.css   Primary HTML button styling across document cards
site/assets/bpi-ai-section-polish.css         AI section card polish only
```

## Utility scripts

```bash
python3 tools/fix_theory_cover_toc_gap.py
python3 tools/fix_logical_pdf_buttons.py
```

Notes:

- `fix_theory_cover_toc_gap.py` patches HTML by default and does **not** rebuild PDF/DOCX unless `--rebuild-exports` is explicitly passed.
- Do not commit broken PDF/DOCX exports that were generated after image-fetch warnings.
- Do not commit `.bak` files.

## Recommended local checks

```bash
git status --short
git diff --stat
python3 tools/fix_logical_pdf_buttons.py
python3 tools/fix_theory_cover_toc_gap.py
git status --short
```

For visual checks:

```bash
open site/pages/he/files.html
open site/pages/en/files-en.html
open site/files/editorial-tightened/between-potential-and-ideal-tightened-he.html
open site/files/editorial-tightened/between-potential-and-ideal-tightened-en.html
```

## Deployment flow

```bash
git pull --ff-only
# make changes
git status --short
git diff --stat
git add <changed files only>
git commit -m "Describe the focused change"
git push origin main
```

Do not use force push unless explicitly planned.

## Do not commit

```text
.env*
node_modules/
.DS_Store
*.bak
*.tmp
*.v86.bak
local patch/extraction folders
private keys or API keys
```

## More documentation

See:

```text
docs/PROJECT_STRUCTURE.md
docs/QA_IMPLEMENTATION_2026_05_25.md
```
