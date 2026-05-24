# הנחיות Render / פריסה

## מצב מומלץ

אם Render מאפשר Publish Directory:

- Build Command: ריק / לא נדרש לאתר סטטי
- Publish Directory: `site`

## אם הריפו הקיים מצפה ל־index.html בשורש

במקום להעלות את התיקייה `site` עצמה, העתק את **כל התוכן שבתוך `site/`** לשורש הריפו.

כלומר:
- נכון: `index.html`, `styles.css`, `files/`, `figures/` נמצאים בשורש הפריסה.
- לא נכון אם אין Publish Directory: `site/index.html` כשהשרת מחפש `index.html` בשורש.

## שינויי Render

לא אמור להידרש שינוי ב־Render אם אתה מחליף את תוכן האתר הקיים באותו מבנה.
אם אתה מעלה את המבנה המאורגן החדש כמו שהוא, צריך להגדיר Publish Directory ל־`site`.
