# Canonical localized sources

Every downloadable translation is authored once as Markdown and generated into HTML, PDF, DOCX, Markdown and TXT.

Directory layout:

```text
localization/sources/tlh/<package>-tlh.md
localization/sources/qya/<package>-qya.md
```

Required front matter:

```text
---
title: Localized title
language: tlh
language_label: tlhIngan Hol
direction: ltr
status: draft
source_document: site/files/between-potential-and-ideal-en.html
semantic_cross_check: site/files/between-potential-and-ideal-he.html
translator_note: Short note about terminology choices
---
```

Allowed status values:

- `draft` - active translation work; never publish.
- `linguistic-review` - complete draft awaiting language review.
- `content-review` - language reviewed; awaiting comparison with English and Hebrew meaning.
- `approved` - eligible for five-format generation and publication QA.

Do not mark a source `approved` until every section, caption, note, quotation, link label and protected literary detail has been reviewed. Generated files are outputs, not editing sources.
