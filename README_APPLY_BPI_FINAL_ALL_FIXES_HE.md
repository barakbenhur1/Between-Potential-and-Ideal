# BPI - חבילת תיקון מלאה סופית כולל פורמטים מיוצאים

החבילה הזו מחליפה את החבילות הקודמות. היא כוללת:

1. תיקוני האתר/HTML שכבר הוכנו.
2. יצירת עמודים מקבילים באנגלית במקום הסתרת קישורים.
3. תיקון workflow-ים ישנים כך שלא ירוצו אוטומטית ב-push ויחזירו regression.
4. תיקוני exported documents ל-MD/TXT/DOCX/PDF דרך סקריפט מקומי.
5. יצירת editorial-report-en בכל הפורמטים.
6. QA script שבודק glued Hebrew, alt ב-DOCX, metadata ב-PDF, workflow push triggers, וקבצי counterpart.

## הוראות שימוש

מתוך שורש הריפו:

```bash
unzip -o ~/Downloads/bpi_final_all_fixes_with_exported_docs.zip -d .
python3 -m pip install beautifulsoup4 python-docx PyMuPDF reportlab
python3 tools/bpi_apply_exported_documents_fixes.py
python3 tools/bpi_qa_exported_documents.py
```

אחרי זה:

```bash
git status --short
git diff --stat
```

בדיקה מקומית:

```bash
cd site
python3 -m http.server 8080
```

בדוק בעיניים:
- דף הבית עברית/אנגלית.
- דפי הקבצים עברית/אנגלית.
- ששת מסמכי התאוריה.
- עמודי witness/stories/AI/response/discussion באנגלית ובעברית.
- תמונות שער ותמונות פרקים.
- אין thumbnails בתתי כותרות.
- אין דאבל תמונות.
- אין workflows ישנים שרצים לבד על push.

## מגבלה יחידה שלא נפתרה אוטומטית

`site/files/appendices/mistake-repeats/infinity-pool-original-he.pdf` הוא PDF עברי שהוא תמונתי בלבד, ללא שכבת טקסט. לא נוצר לו תרגום אנגלי נאמן כי אין בקבצים שהועלו מקור טקסטואלי. כדי לייצר מקבילה איכותית צריך את מקור הטקסט או אישור לבצע OCR + בדיקה ידנית.
