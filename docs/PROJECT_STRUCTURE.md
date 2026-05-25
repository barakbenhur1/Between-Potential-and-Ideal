# Between Potential and Ideal — Project Structure

This document describes the public website/repository structure and the rules for future edits.

## Purpose

**Between Potential and Ideal** is a static bilingual reading site for the theory, documents, appendices, AI dialogues, sources, and self-critique around the relation between potential, ideal, and the local optimum under real constraints.

The repository should be treated as a public product, not as a scratch archive. Build artifacts, QA reports, source documents, and public reader pages should be kept clearly separated.

## Core editing rule

Do **not** remove or rewrite the public blurbs, poetic openings, intentional oddities, or philosophical phrasing unless the requested task explicitly asks for that. Future cleanup should improve structure, hierarchy, linking, formatting, exports, and documentation without flattening the voice of the project.

## Repository map

```text
.
├── README.md
├── docs/
│   └── PROJECT_STRUCTURE.md
├── site/
│   ├── index.html
│   ├── en.html
│   ├── styles.css
│   ├── favicon.ico
│   ├── apple-touch-icon.png
│   ├── figures/
│   │   ├── tab_*.png
│   │   ├── thumb_*.png
│   │   ├── v25_chapter_*.png
│   │   └── document/cover/appendix images
│   ├── pages/
│   │   ├── he/
│   │   │   ├── summary.html
│   │   │   ├── core.html
│   │   │   ├── witness.html
│   │   │   ├── applied.html
│   │   │   ├── ai.html
│   │   │   ├── files.html
│   │   │   ├── methodology.html
│   │   │   ├── critique.html
│   │   │   └── sources.html
│   │   └── en/
│   │       ├── summary-en.html
│   │       ├── core-en.html
│   │       ├── witness-en.html
│   │       ├── applied-en.html
│   │       ├── ai-en.html
│   │       ├── files-en.html
│   │       ├── methodology-en.html
│   │       ├── critique-en.html
│   │       └── sources-en.html
│   └── files/
│       ├── between-potential-and-ideal-*.html/md/pdf/docx
│       ├── editorial-tightened/
│       │   └── between-potential-and-ideal-tightened-*.html/md/pdf/docx
│       ├── appendices/
│       │   └── stories-before-thought-* and appendix assets
│       └── ai-believes/
│           ├── what-ai-believes-*.html/md/txt/pdf/docx
│           ├── reverse-turing-conversation-*.html/md/txt/pdf/docx
│           └── when-i-am-also-you-*.html/md/txt/pdf/docx
└── _product_docs/ or reports/ if present
    └── internal QA/build notes, not public reader flow
```

## Public pages vs document files

### Public pages

`site/pages/he/*.html` and `site/pages/en/*.html` are the reader-facing product pages. They should be short, navigable, and product-like.

The most important public page groups are:

- **Home / Summary** — first orientation.
- **Core** — the conceptual core.
- **Witness** — source, witness, critique, and files as reader pathways.
- **Applied** — applied domains.
- **AI** — AI as mirror/witness/tool, not as machine personhood.
- **Files** — archive/download layer.
- **Methodology / Critique / Sources** — trust, limits, and source discipline.

### Document files

`site/files/**` contains the long reading artifacts in multiple formats. These files are allowed to be deep and document-like. Public pages should link to them, not dump them.

## AI section rules

The AI section is sensitive because it can easily look like raw file output or accidental machine-personification. Maintain these rules:

1. The public AI pages must be **cards only**, not raw file dumps.
2. Do not show build labels such as `Completed AI English files` on public reader pages.
3. Each AI document card should clearly state language/version status, such as:
   - Hebrew original
   - Full English version
   - English adaptation
4. Keep the central caution visible: information is not experience; simulation is not living witness; linguistic response is not belief.
5. Raw format lists belong in `files.html` / `files-en.html`, not in the AI landing pages.

## Image rules

1. Chapter images should be full chapter/cover images, not tab banners or thumbnails.
2. `tab_*` and `thumb_*` images are for cards/navigation only.
3. A chapter image should not be reused across many adjacent chapters unless intentionally documented.
4. If a visual is marked low quality, do not reintroduce it as a fallback.
5. Keep Hebrew/English versions of the same chapter visually consistent.

## Export rules

When rebuilding HTML/PDF/DOCX:

1. Build DOCX/PDF from the corrected local HTML/MD source.
2. Verify cover pages visually after export.
3. Verify there are no blank pages after cover pages.
4. Do not commit `*.bak`, local package folders, or temporary scripts.
5. Keep PDF/DOCX/HTML/MD/TXT parity for public downloads where the site advertises those formats.

Recommended local tools:

```bash
brew install pandoc
python3 -m pip install weasyprint pymupdf
```

Useful checks:

```bash
git status --short
git diff --stat
find site -name "*.bak" -o -name "*.tmp"
```

## Source and science discipline

The theory uses science, logic, AI, literature, and philosophy as structural language. Source pages and document sections should distinguish:

- formal claim
- metaphor
- heuristic
- background source
- level of confidence

Scientific and mathematical terms should not be used as proof of metaphysical claims. Near high-risk language, keep a local caution close to the term.

## Accessibility and SEO checklist

For public pages:

- one clear `<main>` region
- meaningful `<title>` and meta description
- canonical and hreflang links for Hebrew/English pairs
- `alt` text for images
- keyboard-accessible links/buttons
- visible focus states
- no hidden file dumps in reader flow

## Deployment notes

The site is static. After changes:

```bash
git status --short
git add .
git commit -m "Describe the public-site fix"
git push origin main
```

Then wait for the hosting provider to deploy and test the live site.

## Do not commit

Do not commit:

```text
node_modules/
.env*
*.bak
*.tmp
.DS_Store
local package extraction folders
one-off patch folders
private keys or API keys
```

## Current cleanup direction

The latest audit direction is:

- preserve the blurbs and voice;
- clean the public AI section into product cards;
- keep raw archives in Files only;
- avoid exposing build/report language in reader pages;
- keep document exports consistent and visually checked;
- document intentional poetic choices rather than automatically “fixing” them.
