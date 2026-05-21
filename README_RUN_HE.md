# הוראות הרצה ובדיקה

## הרצה מקומית

```bash
cd Between-Potential-and-Ideal-main/theory-site-static
python3 -m http.server 8000
```

פתח בדפדפן:

```text
http://localhost:8000/index.html
```

## בדיקות מומלצות

1. פתח את `index.html` ואת `en.html` ובדוק שהתמונות הקטנות בכרטיסים קיימות בשתי השפות.
2. פתח את `ai.html` ואת `ai-en.html` ובדוק שמדור AI מוצג ככרטיסים, לא כרשימת קבצים.
3. לחץ על כל כפתורי הקבצים במדור AI ובדוק שהם נפתחים.
4. פתח את `core/core-en`, `witness/witness-en`, `methodology/methodology-en`, `critique/critique-en` ובדוק שהתמונות הקטנות מופיעות גם באנגלית.
5. בדוק את `theory-site-static/SITE_PARITY_AUDIT.txt` לפירוט הבדיקות שבוצעו.

## פריסה

זהו אתר static. ניתן לפרוס את `theory-site-static` כפי שהוא לשרת סטטי או ל-Render static site, ללא `node_modules` וללא secrets.
