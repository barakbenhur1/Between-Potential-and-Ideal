# Git LFS

נוסף קובץ `.gitattributes` שמגדיר DOCXים תחת `files/` כקבצי Git LFS:

```bash
files/**/*.docx filter=lfs diff=lfs merge=lfs -text
```

זה לא משנה את המסמכים עצמם.
כדי להשתמש בזה בפועל:

```bash
brew install git-lfs
git lfs install
git add .gitattributes
git rm --cached files/**/*.docx
git add files/**/*.docx
git commit -m "Track DOCX files with Git LFS"
git push
```

אם Render לא מושך LFS אוטומטית, צריך להוסיף `git lfs pull` לתהליך.
