# Render — הגדרת הפריסה הנוכחית

מבנה הריפו הנוכחי כולל תיקיית `site/`, והיא תיקיית הפרסום היחידה של האתר.

הגדרות החובה ב־Render:

- Repository: `barakbenhur1/Between-Potential-and-Ideal`
- Branch: `main`
- Runtime / Service type: Static Site
- Build Command: `python3 tools/update_build_info.py`
- Publish Directory / Static Publish Path: `site` או `./site`
- Auto Deploy: מופעל על כל commit

המבנה שמתפרסם מתוך `site/`:

- `site/index.html`
- `site/en.html`
- `site/pages/`
- `site/files/`
- `site/figures/`
- `site/assets/`

אסור להגדיר את שורש הריפו כתיקיית הפרסום, משום שאין בו `index.html` ציבורי. קובץ `render.yaml` בשורש הריפו הוא מקור האמת להגדרת הפריסה.
