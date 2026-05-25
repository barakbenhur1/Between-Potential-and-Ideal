# BPI V79 — תיקון תמונות שבורות במסמכים הראשיים

מטרה:
- לתקן תמונות פרק שנראות שבורות/חתוכות/באנריות בתוך המסמכים הראשיים.
- לא להשתמש ב-tab/thumb/banner כתמונת פרק ראשית.
- לא להשתמש בתמונת הלוקליות החלשה.
- להשאיר את תמונת I Have No Mouth רק בפרק שלה.
- לא לגעת ב-stories / AI appendices / עמודי אתר רגילים.

שימוש:
```bash
cd ~/Downloads/theory-site
unzip -o ~/Downloads/bpi_v79_fix_broken_main_doc_images.zip
python3 bpi_v79_fix_broken_main_doc_images/tools/apply_v79_fix_broken_main_doc_images.py
```

יישום:
```bash
python3 bpi_v79_fix_broken_main_doc_images/tools/apply_v79_fix_broken_main_doc_images.py --apply
git status --short
git diff --stat
```
