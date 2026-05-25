# BPI V78 — תיקון מדויק לתמונות במסמכים הראשיים

החבילה הזו מחליפה את V76/V77.

## מה היא מתקנת

- מטפלת רק במסמכים הראשיים:
  - `site/files/between-potential-and-ideal-en-editorial.html`
  - `site/files/between-potential-and-ideal-he-editorial.html`
  - `site/files/between-potential-and-ideal-en.md`
  - `site/files/between-potential-and-ideal-he.md`
  - `site/files/editorial-tightened/between-potential-and-ideal-tightened-en.html`
  - `site/files/editorial-tightened/between-potential-and-ideal-tightened-he.html`
  - `site/files/editorial-tightened/between-potential-and-ideal-tightened-en.md`
  - `site/files/editorial-tightened/between-potential-and-ideal-tightened-he.md`

## כלל התמונה

- אותו פרק בעברית/אנגלית ובכל פורמט = אותה תמונה.
- פרקים שונים = תמונות שונות.
- תמונת הלוקליות החלשה אסורה ומוחלפת.
- תמונת `I Have No Mouth` יכולה להישאר רק בפרק שלה ולא לחזור בפרקים אחרים.

## שימוש

להתחיל נקי:

```bash
cd ~/Downloads/theory-site
git reset --hard
git clean -fd
```

Audit בלבד:

```bash
unzip -o ~/Downloads/bpi_v78_precise_main_docs_image_fix.zip
python3 bpi_v78_precise_main_docs_image_fix/tools/apply_v78_precise_main_docs_image_fix.py
cat _product_docs/reports/BPI_V78_PRECISE_MAIN_DOCS_IMAGE_FIX_REPORT_HE.md
```

יישום HTML/MD בלבד:

```bash
python3 bpi_v78_precise_main_docs_image_fix/tools/apply_v78_precise_main_docs_image_fix.py --apply
git status --short
git diff --stat
```

אחרי שה־HTML/MD טובים, אפשר לעדכן גם DOCX/PDF:

```bash
brew install pandoc
python3 -m pip install weasyprint
python3 bpi_v78_precise_main_docs_image_fix/tools/apply_v78_precise_main_docs_image_fix.py --apply --rebuild-docx --rebuild-pdf
```

## מה החבילה לא עושה

- לא נוגעת ב־stories.
- לא נוגעת בקבצי AI.
- לא משנה עמודי אתר רגילים.
- לא יוצרת תמונות AI חדשות.
- לא מוחקת תמונות מקור.
