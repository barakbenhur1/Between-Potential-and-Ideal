# BPI V85 — תיקון דף שער ודפים ריקים בגרסה הלוגית

הבעיה:
- אחרי בנייה מחדש, דף השער של הגרסה הלוגית יצא מפורמט.
- הופיעו עמודים ריקים.

הפתרון:
- מוסיף CSS ייעודי לייצוא PDF/Print.
- מכריח את דף השער להיות קומפקטי, ממורכז, ולשבת בעמוד אחד.
- מבטל שבירת עמוד כפולה אחרי השער.
- בונה מחדש PDF/DOCX של הגרסה הלוגית בעברית ובאנגלית.
- מנקה עמודים ריקים מ-PDF אם מותקן PyMuPDF.

## הרצה

```bash
cd ~/Downloads/theory-site
unzip -o ~/Downloads/bpi_v85_fix_logical_cover_blank_pages.zip
python3 bpi_v85_fix_logical_cover_blank_pages/tools/apply_v85_fix_logical_cover_blank_pages.py
```

אם PDF או DOCX דולגו:

```bash
brew install pandoc
python3 -m pip install weasyprint pymupdf
python3 bpi_v85_fix_logical_cover_blank_pages/tools/apply_v85_fix_logical_cover_blank_pages.py
```

## בדיקה

```bash
open site/files/editorial-tightened/between-potential-and-ideal-tightened-he.pdf
open site/files/editorial-tightened/between-potential-and-ideal-tightened-en.pdf
git status --short
git diff --stat
cat _product_docs/reports/BPI_V85_LOGICAL_COVER_BLANK_PAGES_FIX_REPORT_HE.md
```

לפני commit:
```bash
rm -rf bpi_v85_fix_logical_cover_blank_pages
git add .
git commit -m "Fix logical cover export and remove blank pages"
git push origin main
```
