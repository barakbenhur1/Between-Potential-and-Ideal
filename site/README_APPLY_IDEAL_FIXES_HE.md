# חבילת תיקון 10/10 — Between Potential and Ideal

החבילה הזו לא דורסת לך את הריפו עם קבצים ישנים. היא מריצה תיקון על **המצב המקומי הנוכחי שלך**, ולכן היא מתאימה גם אם יש לך שינויים שלא קיימים עדיין ב-GitHub.

## מה היא מתקנת

- מוסיפה alt משמעותי לתמונות חסרות alt.
- מוסיפה loading="lazy" ו-decoding="async" לתמונות.
- מסירה transform: scale(...) ממסמכי התאוריה, כדי למנוע crop מוגזם ורווחים/חיתוכים לא רצויים.
- מייצבת קופסאות תמונות שער/פרקים ותמונות תוכן עניינים במסמכי התאוריה.
- משאירה thumbnails רק בפרקים ראשיים, לא ב-toc-sub.
- מסירה כפילויות figure סמוכות ברורות.
- שומרת על הכותרות/שורות שאמרת לא לגעת בהן: Chapter ?: ↓ / פרק ?: ↓ / Chapter *: Understanding / פרק *: הבנה.
- מוסיפה הערת מתודולוגיה קצרה למסמכי התאוריה על מדע/מתמטיקה כמטאפורה לעומת טענה פורמלית.
- מוסיפה התחלה מומלצת לדף הבית ולדפי הקבצים אם חסרה.
- מוסיפה focus-visible ו-skip-link CSS.
- מייצרת sitemap.xml ו-robots.txt.
- לא מוחקת תוכן רעיוני.

## איך להריץ

מתוך שורש הריפו או מתוך תיקיית site:

```bash
python3 -m pip install beautifulsoup4
python3 tools/bpi_apply_ideal_fixes.py
python3 tools/bpi_qa_ideal_check.py
```

אחר כך:

```bash
git status --short
git diff --stat
```

בדוק בעיניים את האתר המקומי:

```bash
cd site
python3 -m http.server 8080
```

פתח:

- http://localhost:8080/index.html
- http://localhost:8080/en.html
- http://localhost:8080/pages/he/files.html
- http://localhost:8080/pages/en/files-en.html
- http://localhost:8080/files/between-potential-and-ideal-he-editorial.html
- http://localhost:8080/files/between-potential-and-ideal-en-editorial.html
- http://localhost:8080/files/between-potential-and-ideal-he.html
- http://localhost:8080/files/between-potential-and-ideal-en.html
- http://localhost:8080/files/editorial-tightened/between-potential-and-ideal-tightened-he.html
- http://localhost:8080/files/editorial-tightened/between-potential-and-ideal-tightened-en.html

## קומיט

אם הכל נראה טוב:

```bash
git add site tools docs
git commit -m "Apply ideal product and document fixes"
git push origin main
```

## הערה חשובה

PDF/DOCX לא מתעדכנים אוטומטית על ידי הסקריפט הזה. אחרי תיקוני HTML, צריך להריץ את pipeline הייצוא הקיים שלך אם אתה מציג PDF/DOCX כפורמטים מקבילים.
