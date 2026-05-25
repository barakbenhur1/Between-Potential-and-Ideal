# BPI V82 — השלמת קבצי AI בכל הפורמטים והשפות

מטרה:
- להשלים את החלק של הבינה המלאכותית תחת `site/files/ai-believes`.
- להשלים קבצים חסרים באנגלית ובעברית.
- להפיק MD / HTML / TXT / DOCX / PDF לכל מסמך.
- לעדכן את עמודי הקבצים כך שהקבצים החדשים יהיו נגישים.

הסקריפט לא מזייף תרגומים:
- אם חסרה גרסה באנגלית, הוא יתרגם רק עם `--translate` ורק אם מוגדר `OPENAI_API_KEY`.
- בלי מפתח API הוא יעשה audit וידווח מה חסר.

## שימוש מומלץ

```bash
cd ~/Downloads/theory-site
unzip -o ~/Downloads/bpi_v82_complete_ai_section_files.zip

# בדיקה בלבד
python3 bpi_v82_complete_ai_section_files/tools/apply_v82_complete_ai_section_files.py

# התקנות להפקת פורמטים
brew install pandoc
python3 -m pip install weasyprint

# הפקה בלי תרגום — משלים רק פורמטים מתוך שפות שכבר קיימות
python3 bpi_v82_complete_ai_section_files/tools/apply_v82_complete_ai_section_files.py --apply --update-file-pages

# הפקה מלאה כולל תרגומי אנגלית חסרים
export OPENAI_API_KEY="YOUR_KEY_HERE"
python3 bpi_v82_complete_ai_section_files/tools/apply_v82_complete_ai_section_files.py --apply --translate --update-file-pages
```

בדיקה:

```bash
git status --short
git diff --stat
cat _product_docs/reports/BPI_V82_COMPLETE_AI_SECTION_FILES_REPORT_HE.md
```
