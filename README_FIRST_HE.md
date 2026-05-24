# Between Potential and Ideal — מוצר מאורגן V33

זהו ZIP מלא ומאורגן של המוצר.

## מבנה ראשי

- `site/` — האתר המלא והנקי לפריסה. זה החלק שאמור לעלות ל־Render / Static hosting.
- `product_docs/` — דוחות, אימותים, אינדקסים והסברים. לא חייבים להעלות לפרודקשן.
- `README_FIRST_HE.md` — הקובץ הזה.
- `RENDER_DEPLOY_NOTES_HE.md` — איך לפרוס בלי לשבור נתיבים.

## מה חשוב

הנתיבים בתוך `site/` נשמרו כדי לא לשבור קישורים:
- `site/index.html`
- `site/en.html`
- `site/files/...`
- `site/files/appendices/...`
- `site/files/editorial-tightened/...`
- `site/figures/...`

אם אתה מעלה ל־Render, בדרך כלל צריך להגדיר את תיקיית הפרסום ל־`site`.

אם אתה מחליף קבצים בריפו קיים שבו `index.html` נמצא בשורש, העלה את **התוכן של `site/`** לשורש הריפו, לא את התיקייה `site` עצמה.
