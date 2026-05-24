# V39 — תיקון בעיות קבצים, מייל ונספחים

בוצע כ־patch ממוקד על בסיס V36/V37/V38, בלי שינוי מבנה תיקיות ובלי שינוי תוכן הפרקים.

## תוקן

1. `קבצי מקור` בעמוד היישום
- הכרטיס כבר לא ריק.
- נוספו קישורי DOCX/MD למסמך המלא ולגרסה הלוגית.

2. `בתוך התאוריה`
- הוסר מצב של PDF כפול.
- הכרטיס מציג עכשיו: HTML מלא, PDF מלא, HTML לוגי, MD לוגי.

3. כפתור `פתח מייל תגובה`
- הוחלף מ־mailto שעלול לא לעבוד בדפדפנים בלי תוכנת מייל מקומית לקישור Gmail compose בדפדפן.
- הקישור נפתח בטאב חדש.

4. שער הנספחים
- הוסר הטקסט/כיתוב השבור שהיה ליד התמונה.
- התמונה נשארת נקייה וממורכזת.

5. תוכן עניינים של הנספחים
- הוסר המספור הבעייתי שיצר שבירת דו־ספרתי כמו `1 0`.
- נשארה רשימת קישורים נקייה ללא מספור.

6. תמונות בנספחים
- הוסרו אילוצי stretch/squash.
- התמונות מוגדרות עכשיו לפי יחס התמונה המקורי: `width:auto`, `height:auto`, `object-fit:contain`.
- התמונות ממורכזות.

7. כותרות סיפורים מאוחרים
- כל כותרות הסיפורים ותתי־הכותרות בנספחים מיושרות למרכז באותה צורה.
- הוסרו סגנונות inline שסתרו זה את זה וגרמו פעם לימין, פעם לשמאל ופעם למרכז.

8. כותרת ותמונה באותו רצף
- נוספו כללי page-break כדי שלא ייווצר מצב שבו הכותרת נשארת לבד והתמונה עוברת לדף הבא ללא צורך.
- ה־PDF של הנספחים נבנה מחדש בעברית ובאנגלית.

## קבצים שעודכנו בפועל

- `styles.css`
- `pages/he/applied.html`
- `pages/en/applied-en.html`
- `pages/he/critique.html`
- `pages/he/discussion.html`
- `pages/he/response.html`
- `pages/he/ai-believes.html`
- `pages/en/critique-en.html`
- `pages/he/stories.html`
- `files/appendices/stories-before-thought-hebrew-rtl.html`
- `files/appendices/stories-before-thought-hebrew-rtl.pdf`
- `files/appendices/stories-before-thought-hebrew-rtl.docx`
- `files/appendices/stories-before-thought-english.html`
- `files/appendices/stories-before-thought-english.pdf`
- `files/appendices/stories-before-thought-english.docx`

## בדיקות

- נבדקו 2,067 קישורים מקומיים: 0 שבורים.
- כפתורי מייל הפכו לקישורי Gmail compose.
- אין PDF כפול ב־`בתוך התאוריה`.
- אין כיתוב שבור בשער הנספחים.
- אין מספור דו־ספרתי שבור בתוכן העניינים.
- בדיקת verify הסתיימה עם `failures: []`.
