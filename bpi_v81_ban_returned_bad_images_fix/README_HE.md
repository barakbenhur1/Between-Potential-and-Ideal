# BPI V81 — איסור שתי התמונות שחזרו

מתקן את שתי התמונות שהמשתמש סימן בצילומי המסך:
- `v25_chapter_science-physics-math-boundary-discipline.png`
- `cover_logical_recursion_whole_diagram.png`

בנוסף עדיין אוסר:
- `v25_chapter_locality-nonlocality-contextuality.png`
- `tab_*`
- `thumb_*`
- `banner`
- `unique_reuse`

השינוי מוגבל למסמכים הראשיים בלבד.

שימוש:

```bash
cd ~/Downloads/theory-site
unzip -o ~/Downloads/bpi_v81_ban_returned_bad_images_fix.zip
python3 bpi_v81_ban_returned_bad_images_fix/tools/apply_v81_ban_returned_bad_images_fix.py
```

יישום:

```bash
python3 bpi_v81_ban_returned_bad_images_fix/tools/apply_v81_ban_returned_bad_images_fix.py --apply
git status --short
git diff --stat
```
