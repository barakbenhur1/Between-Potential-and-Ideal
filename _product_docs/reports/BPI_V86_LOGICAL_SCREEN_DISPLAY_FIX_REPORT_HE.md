# BPI V86 - תיקון תצוגת HTML ושמירת תיקון PDF לגרסה הלוגית

Generated: 2026-05-25T22:32:21

V85 הכניס CSS גם ל־screen ולכן פגע בתצוגת HTML רגילה. V86 מסיר את השפעת screen ומשאיר רק CSS ל־print/PDF.

## Logical Hebrew
  - backup: `site/files/editorial-tightened/between-potential-and-ideal-tightened-he.html.v86.bak`
- removed V85 screen CSS and added V86 print-only CSS in `site/files/editorial-tightened/between-potential-and-ideal-tightened-he.html`
  - backup: `site/files/editorial-tightened/between-potential-and-ideal-tightened-he.pdf.v86.bak`
  - PDF rebuilt with weasyprint: `site/files/editorial-tightened/between-potential-and-ideal-tightened-he.pdf`
  - blank-page cleanup: no blank pages detected
  - backup: `site/files/editorial-tightened/between-potential-and-ideal-tightened-he.docx.v86.bak`
  - DOCX rebuilt with pandoc: `site/files/editorial-tightened/between-potential-and-ideal-tightened-he.docx`

## Logical English
  - backup: `site/files/editorial-tightened/between-potential-and-ideal-tightened-en.html.v86.bak`
- removed V85 screen CSS and added V86 print-only CSS in `site/files/editorial-tightened/between-potential-and-ideal-tightened-en.html`
  - backup: `site/files/editorial-tightened/between-potential-and-ideal-tightened-en.pdf.v86.bak`
  - PDF rebuilt with weasyprint: `site/files/editorial-tightened/between-potential-and-ideal-tightened-en.pdf`
  - blank-page cleanup: no blank pages detected
  - backup: `site/files/editorial-tightened/between-potential-and-ideal-tightened-en.docx.v86.bak`
  - DOCX rebuilt with pandoc: `site/files/editorial-tightened/between-potential-and-ideal-tightened-en.docx`

## בדיקות מומלצות
```bash
open site/files/editorial-tightened/between-potential-and-ideal-tightened-he.html
open site/files/editorial-tightened/between-potential-and-ideal-tightened-en.html
open site/files/editorial-tightened/between-potential-and-ideal-tightened-he.pdf
open site/files/editorial-tightened/between-potential-and-ideal-tightened-en.pdf
git status --short
git diff --stat
```
