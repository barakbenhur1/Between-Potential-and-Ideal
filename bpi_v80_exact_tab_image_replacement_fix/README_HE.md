# BPI V80 — החלפת תמונות tab/banner מדויקות במסמכים הראשיים

החבילה הזו נבנתה לפי הפלט המדויק שהודפס מהקבצים המקומיים:
- `tab_files.png`
- `tab_core.png`
- `tab_critique.png`
- `tab_ai.png`
- `tab_*_unique`
- ותמונת הלוקליות החלשה

היא מחליפה רק תמונות בתוך `chapter-opening` במסמכים הראשיים.

שימוש:

```bash
cd ~/Downloads/theory-site
unzip -o ~/Downloads/bpi_v80_exact_tab_image_replacement_fix.zip
python3 bpi_v80_exact_tab_image_replacement_fix/tools/apply_v80_exact_tab_image_replacement_fix.py
```

יישום:

```bash
python3 bpi_v80_exact_tab_image_replacement_fix/tools/apply_v80_exact_tab_image_replacement_fix.py --apply
git status --short
git diff --stat
```
