# BPI V72 — תיקון בטוח לתת־כותרת ומרכוז תמונות בנספחים

בוצע תיקון ממוקד בלבד:

- תת־הכותרת `סיפורים שסיפרתי לאימי` נשמרת/מועברת מיד מתחת לכותרת המסמך.
- התת־כותרת מקבלת עיצוב תת־כותרת אמיתי: קרובה לכותרת, ממורכזת, סמי־בולד, איטליק, גודל מובחן וצבע משני.
- כל התמונות ב־HTML ממורכזות: תמונת שער, figures, image-frame ותמונות סיפורים.
- קבצי DOCX תוקנו בצורה בטוחה בתוך ה־XML: ללא בנייה מחדש, ללא החלפת תמונות בתיאורים, וללא נגיעה בקבצי media.
- קבצי PDF לא נבנו מחדש בכוונה. כדי לעדכן PDF צריך להריץ את export/build הרשמי של הפרויקט אחרי בדיקת HTML/DOCX.

## קבצים ששונו

- `site/files/appendices/BPI_V72_APPENDIX_SUBTITLE_IMAGE_CENTER_FIX.css`
- `site/files/appendices/stories-before-thought-english.html`
- `site/files/appendices/stories-before-thought-hebrew-rtl.html`
- `site/pages/he/stories.html`
- `site/pages/en/witness-en.html`
- `site/_product_docs/reports/V23_FINAL_VERIFICATION_REPAIR_REPORT_HE.md`
- `site/files/appendices/stories-before-thought-english.md`
- `site/files/appendices/stories-before-thought-english.txt`
- `README_HE.md`
- `site/files/appendices/stories-before-thought-english.docx`
