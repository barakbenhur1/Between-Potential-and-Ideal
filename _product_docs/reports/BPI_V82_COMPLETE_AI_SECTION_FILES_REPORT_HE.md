# BPI V82 — השלמת קבצי AI בכל הפורמטים והשפות

Mode: APPLY
Translate missing language counterparts: no

## Current AI file matrix
### reverse-turing-conversation
- reverse-turing-conversation-he: md:yes, html:yes, txt:NO, docx:yes, pdf:yes
- reverse-turing-conversation-en: md:NO, html:NO, txt:NO, docx:NO, pdf:NO
### what-ai-believes
- what-ai-believes-he: md:yes, html:yes, txt:NO, docx:yes, pdf:yes
- what-ai-believes-en: md:NO, html:NO, txt:NO, docx:NO, pdf:NO
### when-i-am-also-you
- when-i-am-also-you-he: md:yes, html:yes, txt:NO, docx:yes, pdf:yes
- when-i-am-also-you-en: md:yes, html:yes, txt:NO, docx:yes, pdf:yes

## Actions
- created `site/files/ai-believes/reverse-turing-conversation-he.txt` from Markdown
- missing `site/files/ai-believes/reverse-turing-conversation-en.md` — translation required, skipped in audit/no-translate mode
- missing `site/files/ai-believes/reverse-turing-conversation-en.txt` — no source found
- missing `site/files/ai-believes/reverse-turing-conversation-en.html` — no Markdown source found
- missing `site/files/ai-believes/reverse-turing-conversation-en.docx` — no Markdown source found
- missing `site/files/ai-believes/reverse-turing-conversation-en.pdf` — need weasyprint or pandoc
- created `site/files/ai-believes/what-ai-believes-he.txt` from Markdown
- missing `site/files/ai-believes/what-ai-believes-en.md` — translation required, skipped in audit/no-translate mode
- missing `site/files/ai-believes/what-ai-believes-en.txt` — no source found
- missing `site/files/ai-believes/what-ai-believes-en.html` — no Markdown source found
- missing `site/files/ai-believes/what-ai-believes-en.docx` — no Markdown source found
- missing `site/files/ai-believes/what-ai-believes-en.pdf` — need weasyprint or pandoc
- created `site/files/ai-believes/when-i-am-also-you-he.txt` from Markdown
- created `site/files/ai-believes/when-i-am-also-you-en.txt` from Markdown
- updated `site/pages/en/files-en.html` with 4 AI file rows
- updated `site/pages/he/files.html` with 4 AI file rows

## Notes
- The script does not create fake English translations. Missing language counterparts are translated only when `--translate` is passed and `OPENAI_API_KEY` exists.
- DOCX generation requires `pandoc`.
- PDF generation requires `weasyprint` or `pandoc` PDF support.
- Existing files are preserved; the script fills missing files only.
