# Klingon and Neo-Quenya localization

This directory defines the production workflow for adding two complete public language editions to **Between Potential and Ideal**:

- Klingon: `tlhIngan Hol`, language code `tlh`
- Neo-Quenya: language code `qya`

## Approved scope

Both editions must include:

1. Every public website page.
2. Every public long-form document and appendix.
3. Every public story and AI dialogue.
4. Navigation, breadcrumbs, accessibility labels, metadata, alt text, Open Graph, canonical and hreflang data.
5. Download packages in all formats already used by the project:
   - HTML
   - PDF
   - DOCX
   - Markdown
   - TXT

The brand name **Between Potential and Ideal** remains in English.

## Translation policy

- English is the primary structural source.
- Hebrew is the semantic cross-check source.
- Klingon uses the standard Latin transcription of `tlhIngan Hol`.
- Quenya content is explicitly identified as **Neo-Quenya**.
- Existing vocabulary and attested grammar are preferred.
- Descriptive compounds are preferred over undocumented invented words.
- Project terminology must be recorded in the shared glossary before broad reuse.
- Literary endings, humor, paradoxes, protected story details, image order, and document structure must not be simplified or silently rewritten.

## Public-release rule

The new languages stay hidden from the public language menu until a language passes all of the following:

- homepage exists;
- every mapped public page exists;
- every mapped download package exists in all five formats;
- local links and assets pass;
- no source-language residue remains outside approved names, quotations, URLs, citations, or bibliography entries;
- canonical, hreflang, sitemap and search-index entries are complete;
- desktop and mobile visual QA pass;
- the final release guard passes.

Publication is controlled by `localization/config.json`. Do not set `publish` to `true` until parity QA reports no blockers.

## Planned paths

```text
site/tlh.html
site/qya.html
site/pages/tlh/...
site/pages/qya/...
site/files/tlh/...
site/files/qya/...
```

## Required workflow

1. Run the inventory generator.
2. Review the complete source page and download-package inventory.
3. Approve the glossary entries for the current translation batch.
4. Translate one canonical source into the language source file.
5. Generate HTML, PDF, DOCX, Markdown and TXT from that canonical source.
6. Run localization parity QA.
7. Review visual and linguistic QA.
8. Publish the language only after all batches are complete.

Commands:

```bash
python3 tools/build_localization_inventory.py
python3 tools/audit_extended_localization_parity.py
python3 tools/final_release_qa.py --scan
```

Generated inventory and QA reports are written under `reports/localization/` and are not committed by default.
