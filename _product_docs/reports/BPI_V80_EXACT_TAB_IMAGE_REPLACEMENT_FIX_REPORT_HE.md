# BPI V80 — החלפת תמונות tab/banner מדויקות במסמכים הראשיים

Mode: APPLY

## מה תוקן
- מחליף רק תמונות בתוך `chapter-opening` של המסמכים הראשיים.
- מחליף `tab_*`, `tab_*_unique`, `thumb_*`, `banner`, `unique_reuse` ותמונת הלוקליות החלשה.
- לא נוגע בטקסט.
- לא נוגע ב־stories או ב־AI appendices.
- לא בונה DOCX/PDF בשלב הזה.

## החלפות
### `site/files/editorial-tightened/between-potential-and-ideal-tightened-he.html`
- from: `../../figures/tab_files_unique.png`
  - to: `../../figures/15_good_evil_responsibility.png`
  - asset: `15_good_evil_responsibility.png`
  - reason: replace tab_* banner in suffering/meaning chapter with full chapter-quality image
- from: `../../figures/tab_witness_unique.png`
  - to: `../../figures/cover_logical_recursion_whole_diagram.png`
  - asset: `cover_logical_recursion_whole_diagram.png`
  - reason: replace tab_* banner in recursive architecture with logical recursion full diagram
- from: `../../figures/tab_critique.png`
  - to: `../../figures/v25_chapter_recursive-edge.png`
  - asset: `v25_chapter_recursive-edge.png`
  - reason: replace tab_* banner with recursive-edge chapter image
- from: `../../figures/tab_files.png`
  - to: `../../figures/v25_chapter_science-physics-math-boundary-discipline.png`
  - asset: `v25_chapter_science-physics-math-boundary-discipline.png`
  - reason: replace tab_files banner with science/physics/mathematics chapter image
- from: `../../figures/tab_core.png`
  - to: `../../figures/v25_chapter_boundary-horizons.png`
  - asset: `v25_chapter_boundary-horizons.png`
  - reason: replace tab_core/low-quality locality image with stronger existing chapter-quality asset
- from: `../../figures/tab_ai_unique.png`
  - to: `../../figures/05_flow_toward_the_ideal.png`
  - asset: `05_flow_toward_the_ideal.png`
  - reason: replace tab_* banner in physical comparison map with full concept image
### `site/files/editorial-tightened/between-potential-and-ideal-tightened-en.html`
- from: `../../figures/tab_methodology_unique.png`
  - to: `../../figures/15_good_evil_responsibility.png`
  - asset: `15_good_evil_responsibility.png`
  - reason: replace tab_* banner in suffering/meaning chapter with full chapter-quality image
- from: `../../figures/tab_ai.png`
  - to: `../../figures/cover_logical_recursion_whole_diagram.png`
  - asset: `cover_logical_recursion_whole_diagram.png`
  - reason: replace tab_* banner in recursive architecture with logical recursion full diagram
- from: `../../figures/tab_critique.png`
  - to: `../../figures/v25_chapter_recursive-edge.png`
  - asset: `v25_chapter_recursive-edge.png`
  - reason: replace tab_* banner with recursive-edge chapter image
- from: `../../figures/tab_files.png`
  - to: `../../figures/v25_chapter_science-physics-math-boundary-discipline.png`
  - asset: `v25_chapter_science-physics-math-boundary-discipline.png`
  - reason: replace tab_files banner with science/physics/mathematics chapter image
- from: `../../figures/tab_core.png`
  - to: `../../figures/v25_chapter_boundary-horizons.png`
  - asset: `v25_chapter_boundary-horizons.png`
  - reason: replace tab_core/low-quality locality image with stronger existing chapter-quality asset
- from: `../../figures/tab_applied_unique.png`
  - to: `../../figures/05_flow_toward_the_ideal.png`
  - asset: `05_flow_toward_the_ideal.png`
  - reason: replace tab_* banner in physical comparison map with full concept image
### `site/files/between-potential-and-ideal-he-editorial.html`
- from: `../figures/tab_methodology.png`
  - to: `../figures/v25_chapter_shape-of-the-universe-and-potential.png`
  - asset: `v25_chapter_shape-of-the-universe-and-potential.png`
  - reason: replace tab image in opening philosophical chapter with full conceptual figure
- from: `../figures/tab_sources.png`
  - to: `../figures/cover_philosophical_recursion_whole_diagram.png`
  - asset: `cover_philosophical_recursion_whole_diagram.png`
  - reason: replace tab_sources banner with full self/ego/unity image
- from: `../figures/tab_witness.png`
  - to: `../figures/cover_logical_recursion_whole_diagram.png`
  - asset: `cover_logical_recursion_whole_diagram.png`
  - reason: replace tab_* banner in recursive architecture with logical recursion full diagram
- from: `../figures/tab_critique.png`
  - to: `../figures/v25_chapter_recursive-edge.png`
  - asset: `v25_chapter_recursive-edge.png`
  - reason: replace tab_* banner with recursive-edge chapter image
- from: `../figures/tab_files.png`
  - to: `../figures/v25_chapter_science-physics-math-boundary-discipline.png`
  - asset: `v25_chapter_science-physics-math-boundary-discipline.png`
  - reason: replace tab_files banner with science/physics/mathematics chapter image
- from: `../figures/tab_core.png`
  - to: `../figures/v25_chapter_boundary-horizons.png`
  - asset: `v25_chapter_boundary-horizons.png`
  - reason: replace tab_core/low-quality locality image with stronger existing chapter-quality asset
### `site/files/between-potential-and-ideal-en-editorial.html`
- from: `../figures/tab_sources_unique.png`
  - to: `../figures/cover_philosophical_recursion_whole_diagram.png`
  - asset: `cover_philosophical_recursion_whole_diagram.png`
  - reason: replace tab_sources banner with full self/ego/unity image
- from: `../figures/tab_applied.png`
  - to: `../figures/cover_logical_recursion_whole_diagram.png`
  - asset: `cover_logical_recursion_whole_diagram.png`
  - reason: replace tab_* banner in recursive architecture with logical recursion full diagram
- from: `../figures/tab_critique.png`
  - to: `../figures/v25_chapter_recursive-edge.png`
  - asset: `v25_chapter_recursive-edge.png`
  - reason: replace tab_* banner with recursive-edge chapter image
- from: `../figures/tab_files.png`
  - to: `../figures/v25_chapter_science-physics-math-boundary-discipline.png`
  - asset: `v25_chapter_science-physics-math-boundary-discipline.png`
  - reason: replace tab_files banner with science/physics/mathematics chapter image
- from: `../figures/tab_core.png`
  - to: `../figures/v25_chapter_boundary-horizons.png`
  - asset: `v25_chapter_boundary-horizons.png`
  - reason: replace tab_core/low-quality locality image with stronger existing chapter-quality asset
- from: `../figures/tab_core_unique.png`
  - to: `../figures/02_navigation_between_banks.png`
  - asset: `02_navigation_between_banks.png`
  - reason: replace tab/incorrect image in imaginary/virtual/horizon chapter with full image already used for that concept
- from: `../figures/tab_critique_unique.png`
  - to: `../figures/05_flow_toward_the_ideal.png`
  - asset: `05_flow_toward_the_ideal.png`
  - reason: replace tab_* banner in physical comparison map with full concept image
### `site/files/between-potential-and-ideal-he.md`
- from: `../figures/tab_sources.png`
  - to: `../figures/cover_philosophical_recursion_whole_diagram.png`
  - asset: `cover_philosophical_recursion_whole_diagram.png`
  - reason: replace tab_sources banner with full self/ego/unity image
- from: `../figures/tab_witness.png`
  - to: `../figures/cover_logical_recursion_whole_diagram.png`
  - asset: `cover_logical_recursion_whole_diagram.png`
  - reason: replace tab_* banner in recursive architecture with logical recursion full diagram
- from: `../figures/tab_critique.png`
  - to: `../figures/v25_chapter_recursive-edge.png`
  - asset: `v25_chapter_recursive-edge.png`
  - reason: replace tab_* banner with recursive-edge chapter image
- from: `../figures/tab_files.png`
  - to: `../figures/v25_chapter_science-physics-math-boundary-discipline.png`
  - asset: `v25_chapter_science-physics-math-boundary-discipline.png`
  - reason: replace tab_files banner with science/physics/mathematics chapter image
- from: `../figures/tab_core.png`
  - to: `../figures/v25_chapter_boundary-horizons.png`
  - asset: `v25_chapter_boundary-horizons.png`
  - reason: replace tab_core/low-quality locality image with stronger existing chapter-quality asset
### `site/files/between-potential-and-ideal-en.md`
- from: `../figures/tab_sources_unique.png`
  - to: `../figures/cover_philosophical_recursion_whole_diagram.png`
  - asset: `cover_philosophical_recursion_whole_diagram.png`
  - reason: replace tab_sources banner with full self/ego/unity image
- from: `../figures/tab_applied.png`
  - to: `../figures/cover_logical_recursion_whole_diagram.png`
  - asset: `cover_logical_recursion_whole_diagram.png`
  - reason: replace tab_* banner in recursive architecture with logical recursion full diagram
- from: `../figures/tab_critique.png`
  - to: `../figures/v25_chapter_recursive-edge.png`
  - asset: `v25_chapter_recursive-edge.png`
  - reason: replace tab_* banner with recursive-edge chapter image
- from: `../figures/tab_files.png`
  - to: `../figures/v25_chapter_science-physics-math-boundary-discipline.png`
  - asset: `v25_chapter_science-physics-math-boundary-discipline.png`
  - reason: replace tab_files banner with science/physics/mathematics chapter image
- from: `../figures/tab_core.png`
  - to: `../figures/v25_chapter_boundary-horizons.png`
  - asset: `v25_chapter_boundary-horizons.png`
  - reason: replace tab_core/low-quality locality image with stronger existing chapter-quality asset
- from: `../figures/tab_core_unique.png`
  - to: `../figures/02_navigation_between_banks.png`
  - asset: `02_navigation_between_banks.png`
  - reason: replace tab/incorrect image in imaginary/virtual/horizon chapter with full image already used for that concept
- from: `../figures/tab_critique_unique.png`
  - to: `../figures/05_flow_toward_the_ideal.png`
  - asset: `05_flow_toward_the_ideal.png`
  - reason: replace tab_* banner in physical comparison map with full concept image

## קבצים ששונו בפועל
- `site/files/editorial-tightened/between-potential-and-ideal-tightened-he.html`
- `site/files/editorial-tightened/between-potential-and-ideal-tightened-en.html`
- `site/files/between-potential-and-ideal-he-editorial.html`
- `site/files/between-potential-and-ideal-en-editorial.html`
- `site/files/between-potential-and-ideal-he.md`
- `site/files/between-potential-and-ideal-en.md`

## שאריות בעייתיות שעדיין נמצאו
לא נמצאו `tab/thumb/banner/unique_reuse` בתוך `chapter-opening` במסמכים הראשיים.
