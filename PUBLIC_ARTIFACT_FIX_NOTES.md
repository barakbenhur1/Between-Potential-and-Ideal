# Public artifact cleanup notes

This repository is a public product archive. The public artifact layer should stay clean and symmetric across Hebrew and English.

## Fixed in repository

- Added `.gitignore` rules for local backup files, temporary files, editor leftovers, caches, and generated local audit reports.

## Required cleanup checks before publishing

Run these commands from the repository root:

```bash
find site docs -type f \\( -name '*.bak' -o -name '*.tmp' -o -name '*.temp' -o -name '*.orig' -o -name '*.rej' -o -name '*.old' -o -name '*.backup' -o -name '*~' \\) 2>/dev/null
```

If any files are printed, remove them from the public artifact layer before publishing.

## Text export glitches to check

Search in text-based public artifacts:

```bash
grep -RIn "N P\|N-P\|c o NP\|c-o-NP\|Q B F\|P S P A C E" site docs 2>/dev/null
```

Expected visible forms:

- `NP`
- `coNP`
- `QBF`
- `PSPACE`

## Hebrew TOC check

Search:

```bash
grep -RIn "## זהו מודל, לא הכרזה סופית" site/files 2>/dev/null
```

If it appears inside a table of contents block, it should not be a Markdown heading there. It should be either a normal TOC link or moved to the body as a real section heading.

## Symmetry rule

For the main public theory document, keep Hebrew and English aligned across the same exposed formats when possible:

- HTML
- PDF
- DOCX
- MD
- TXT

If one format is intentionally absent, mark that intentionally in the files page rather than leaving the public set ambiguous.
