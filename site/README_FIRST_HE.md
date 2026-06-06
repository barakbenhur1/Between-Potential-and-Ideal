# Between Potential and Ideal — מבנה הפרויקט הנוכחי

האתר הציבורי נמצא תחת תיקיית `site/` בריפו.

## מבנה האתר

- `site/index.html` — דף הבית בעברית.
- `site/en.html` — דף הבית באנגלית.
- `site/404.html` — דף שגיאה.
- `site/pages/he/` — עמודי התוכן בעברית.
- `site/pages/en/` — עמודי התוכן באנגלית.
- `site/files/` — מסמכים וקבצים להורדה.
- `site/figures/` — תמונות ואיורים.
- `site/assets/` — CSS, JavaScript ונכסים משותפים.

## Render

האתר חייב להיפרס מהענף `main` עם:

- Static Publish Path: `./site`
- Build Command: `python3 tools/update_build_info.py`
- Auto Deploy Trigger: `commit`

קובץ `render.yaml` בשורש הריפו מגדיר את ההגדרות האלה. אין לפרסם את שורש הריפו עצמו, משום שקובצי האתר הציבוריים נמצאים בתוך `site/`.
