# Between Potential and Ideal - static site

This package contains the static website and downloadable theory files.

Updates in this build:
- Added the new recursion / inner rapture chapter inside the theory documents.
- Original theory: chapter 15 / פרק ט״ו.
- Logical updated theory: chapter 13.
- Removed the standalone supporting-material page and its public files from the site.
- Rebuilt DOCX/PDF/HTML/MD theory files for Hebrew and English.


Stories/background page restored as `stories.html`; story files are under `files/appendices/`.

- Added Mass-Energy and Medium as the final Hebrew theory chapter above the arrow section.
- Added chapter subtitles to the Hebrew theory structure.


This build integrates the chapter "יצירה, קאנון ואופטימום: מה אסור לאבד" / "Creation, Canon, and Optimum: What Must Not Be Lost" after the computation chapter, with numbering updated in Hebrew and English full and tightened theory files.


## Run locally

```bash
cd theory-site-static
python3 -m http.server 8000
```

Open `http://localhost:8000/index.html` for Hebrew or `http://localhost:8000/en.html` for English.

## QA notes integrated in this package

- Added multilingual canonical / hreflang hints for paired Hebrew and English pages.
- Added searchable/filterable file index controls without removing the full archive table.
- Added public use/rights notice on the files pages.
- Added discoverability links for archive/supporting pages.
- Preserved and restored “פרק ?:” / “Chapter ?:” markers as intentional open/infinite chapter markers, not unresolved placeholders.
- Preserved intentional poetic differences between Hebrew and English blurbs, including the water/vessel line.
- Added reduced-motion CSS handling.
- Expanded public source-context pages with domain-based source guidance.
