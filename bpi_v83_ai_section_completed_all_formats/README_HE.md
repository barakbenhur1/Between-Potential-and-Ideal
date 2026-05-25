# BPI V83 - השלמת קבצי AI באנגלית ובכל הפורמטים

החבילה מוסיפה קבצים מוכנים להעתקה לתוך הריפו:

- `what-ai-believes-en` - MD / TXT / HTML / DOCX / PDF
- `reverse-turing-conversation-en` - MD / TXT / HTML / DOCX / PDF
- `when-i-am-also-you-en` - MD / TXT / HTML / DOCX / PDF

היא נועדה להשלים את חוסר התרגומים/פורמטים באנגלית בחלק AI בלי להפעיל OpenAI API אצלך.

## שימוש

מתוך שורש הפרויקט:

```bash
cd ~/Downloads/theory-site
unzip -o ~/Downloads/bpi_v83_ai_section_completed_all_formats.zip
python3 tools/apply_v83_ai_completed_files.py
```

בדיקה:

```bash
git status --short
git diff --stat
open site/files/ai-believes/what-ai-believes-en.html
open site/files/ai-believes/reverse-turing-conversation-en.html
open site/files/ai-believes/when-i-am-also-you-en.html
```

## הערה

הקבצים האנגליים כאן הם גרסאות קריאה ערוכות ושלמות באנגלית, שנבנו כדי להשלים את המטריצה של AI בכל הפורמטים. הם לא דורשים מפתח API ולא יוצרים תלות חיצונית.
