# Between Potential and Ideal

A static publication site for **Between Potential and Ideal / בין פוטנציאל לאידיאל**, with Hebrew and English core editions and clearly disclosed constructed-language Public Beta editions.

Live site:

- https://between-potential-and-ideal.onrender.com

## Constructed-language Public Beta editions

Complete Public Beta editions are live in all 77 mapped sections and in HTML, PDF, DOCX, Markdown, and plain text:

- Klingon (`tlhIngan Hol`): https://between-potential-and-ideal.onrender.com/tlh.html
- Neo-Quenya: https://between-potential-and-ideal.onrender.com/qya.html

These editions do not claim independent specialist approval. Current review status and the correction workflow are recorded in `localization/EXTERNAL_REVIEW_STATUS.md`.

Independent bounded reviews of segment 020 are open:

- Neo-Quenya: https://github.com/barakbenhur1/Between-Potential-and-Ideal/issues/10
- Klingon: https://github.com/barakbenhur1/Between-Potential-and-Ideal/issues/11

Production verification is recorded in `site/localization-public-beta-production-status.json`. The verifier checks the deployed revision, both review links, sitemap coverage, disclosure text, image availability, and exact manifest size and SHA-256 parity for all five formats in both languages.

## Current repository structure

The repository is intentionally kept conservative and production-focused.

```text
.
├── .github/workflows/          # Release Guard CI workflow
├── docs/                       # QA, deploy, guardrails, and operational docs
├── tools/                      # Permanent QA/audit/release tools
├── README.md
└── site/
    ├── assets / styles / shared site resources
    ├── figures / document and chapter images
    ├── files / public theory documents and appendices
    └── pages / site pages by language
```

The root should stay clean. Do not commit temporary ZIPs, local backups, generated test folders, cache folders, or one-off working scripts unless they are intentionally part of the production site workflow.

## Main public theory documents

Core document files are under `site/files/`:

- `between-potential-and-ideal-he.html`
- `between-potential-and-ideal-en.html`
- `between-potential-and-ideal-he-editorial.html`
- `between-potential-and-ideal-en-editorial.html`
- `editorial-tightened/between-potential-and-ideal-tightened-he.html`
- `editorial-tightened/between-potential-and-ideal-tightened-en.html`

These documents should stay visually aligned across Hebrew and English versions as much as possible.

## Current document conventions

- Hebrew documents use RTL alignment.
- English documents use LTR alignment.
- Real document body headings and subheadings should be side-aligned by language, not centered.
- The cover, author note, table of contents, figures, captions, and math blocks may keep their intentional centered styling.
- Chapter images must match the actual chapter in both the chapter body and the table of contents thumbnail.
- The chapter **“This Is a Model, Not a Final Declaration” / “זהו מודל, לא הכרזה סופית”** uses:

```text
site/figures/chapter_model_not_final_declaration_v1.png
```

- The summary / abstract chapter should use its own summary/overview image and must not accidentally reuse the model-not-final image.
- The special decorative `key-term` font styling for the words Potential / Ideal / פוטנציאל / אידיאל should not appear inside the public document files unless intentionally restored.

## Working rules

Before committing visual or document changes, run the full local gate:

```bash
rm -rf reports tools/__pycache__
python3 tools/final_release_qa.py --scan
git diff --check
git status --short
```

For document/image mapping changes, verify at least:

```bash
grep -RIn 'chapter_model_not_final_declaration_v1.png\|summary-theory-overview-v2.png' site/files | head -80
```

When updating images in the theory documents, update both:

1. The image inside the relevant chapter body.
2. The thumbnail inside the interactive table of contents.

## Cleanup policy

Keep production files only. Safe to remove from the repo:

- local backup folders
- temporary ZIPs
- `_local_tmp`, `tmp`, `backup`, `backups`
- generated test outputs
- unused scripts created only for one-time repair work
- unused images that are not referenced by any file under `site/`

Do not remove:

- `site/`
- `README.md`
- images referenced by documents, pages, CSS, JS, Open Graph tags, or table-of-contents thumbnails
- files needed for the deployed site

## Deployment

The site is deployed from the repository to Render. After pushing to `main`, wait for Render to finish deploying, then hard-refresh the live page before judging visual changes.

Before pushing or releasing, run the repo-local final release QA command:

```bash
rm -rf reports tools/__pycache__
python3 tools/final_release_qa.py --scan
git diff --check
git status --short
```

This command wraps `tools/audit_release_guard.py`, `git diff --check`, and build-info verification. Generated reports under `reports/` are local review artifacts and should not be committed unless explicitly requested.

---

## Contributor Guardrails

Before editing this project, read:

- `docs/contributor-guardrails.md`
- `docs/deploy.md`
- `docs/qa-index.md`
- `docs/tool-inventory.md`
- `docs/production-next-phase-status.md`
- `docs/visual-qa.md`
- `docs/performance-budget.md`

Always run `python3 tools/final_release_qa.py --scan` before pushing to `main`.
