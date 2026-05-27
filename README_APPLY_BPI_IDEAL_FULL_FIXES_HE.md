# הוראות החלת תיקון BPI מלא

החבילה הזו כוללת רק קבצים ששונו או נוצרו מתוך ה־ZIPים שהועלו לשיחה.
היא אינה כוללת את PDF/DOCX/MD/TXT שלא הועלו בחלק 04.

## איך להחיל

מתוך שורש הריפו המקומי:

```bash
unzip -o ~/Downloads/bpi_ideal_full_fixes_completed_package.zip -d .
```

ואז לבדוק:

```bash
git status --short
git diff --stat
```

## בדיקות חובה לפני קומיט

```bash
grep -R "transform:scale\|transform: scale" site/files/*.html site/files/editorial-tightened/*.html
grep -R 'alt=""' site | head
grep -R "toc-sub.*theory-toc-thumb\|theory-toc-thumb.*toc-sub" site/files/*.html site/files/editorial-tightened/*.html
```

אם אין פלט בשלוש הבדיקות האלה — זה תקין.

בדיקה מקומית:

```bash
cd site
python3 -m http.server 8080
```

פתח בדפדפן:

- http://localhost:8080/
- http://localhost:8080/en.html
- http://localhost:8080/pages/he/files.html
- http://localhost:8080/pages/en/files-en.html
- http://localhost:8080/files/between-potential-and-ideal-he-editorial.html
- http://localhost:8080/files/between-potential-and-ideal-en-editorial.html
- http://localhost:8080/files/editorial-tightened/between-potential-and-ideal-tightened-he.html
- http://localhost:8080/files/editorial-tightened/between-potential-and-ideal-tightened-en.html
- http://localhost:8080/pages/en/stories-en.html
- http://localhost:8080/pages/en/discussion-en.html
- http://localhost:8080/pages/en/response-en.html
- http://localhost:8080/pages/en/mistake-repeats-en.html
- http://localhost:8080/pages/en/ai-believes-en.html

## קומיט

```bash
git add site BPI_IDEAL_FULL_FIX_REPORT.json BPI_IDEAL_FULL_FIX_REPORT.md README_APPLY_BPI_IDEAL_FULL_FIXES_HE.md
git commit -m "Apply ideal product and document fixes"
git push origin main
```

## הערה

אם רוצים לסנכרן גם PDF/DOCX/MD/TXT, צריך להעלות או להריץ בנפרד את חלק 04 של המסמכים המיוצאים. החבילה הזו לא משנה אותם.
