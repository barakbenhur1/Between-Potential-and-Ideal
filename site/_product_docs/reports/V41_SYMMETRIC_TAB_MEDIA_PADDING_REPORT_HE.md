# V41 — תיקון padding סימטרי לתמונות הטאבים

בוצע תיקון ממוקד באתר בלבד, בלי לייצר תמונות ובלי לשנות מסמכים.

מה תוקן:
- נוספה שכבת CSS מאוחרת שמכריחה padding לבן סימטרי סביב תמונות הטאבים/עמודי התוכן.
- התיקון חל על:
  - `compact-section-visual`
  - `section-visual`
  - `opening-visual`
  - `hero-art`
  - `image-frame`
  - `content-card-image`
- התמונה נשארת במרכז, בלי שינוי קובצי תמונה.
- עודכנו `styles.css` ו־`styles-home-original.css`.
- נוסף override inline מאוחר בעמודי HTML הרלוונטיים כדי לנצח overrides קיימים מתוך העמודים.

לא בוצע:
- לא שונו PDF/DOCX/MD.
- לא שונו תמונות מקור.
- לא שונה מבנה תיקיות.
