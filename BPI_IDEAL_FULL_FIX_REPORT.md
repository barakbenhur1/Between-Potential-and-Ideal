# BPI ideal full fixes report

This package applies all safe approved fixes to the uploaded repository subset, without changing preserved TOC/title rows and without deleting conceptual content.

## Created files
- `site/pages/en/response-en.html`
- `site/pages/en/discussion-en.html`
- `site/pages/en/stories-en.html`
- `site/pages/en/mistake-repeats-en.html`
- `site/pages/en/ai-believes-en.html`
- `site/sitemap.xml`
- `site/robots.txt`
- `BPI_IDEAL_FULL_FIX_REPORT.json`

## Changed files
- `site/en.html`
- `site/files/ai-believes/reverse-turing-conversation-en.html`
- `site/files/ai-believes/what-ai-believes-en.html`
- `site/files/ai-believes/when-i-am-also-you-en.html`
- `site/files/between-potential-and-ideal-en-editorial.html`
- `site/files/between-potential-and-ideal-en.html`
- `site/files/between-potential-and-ideal-he-editorial.html`
- `site/files/between-potential-and-ideal-he.html`
- `site/files/editorial-tightened/between-potential-and-ideal-tightened-en.html`
- `site/files/editorial-tightened/between-potential-and-ideal-tightened-he.html`
- `site/index.html`
- `site/pages/en/files-en.html`
- `site/pages/en/witness-en.html`
- `site/pages/he/ai-believes.html`
- `site/pages/he/discussion.html`
- `site/pages/he/files.html`
- `site/pages/he/mistake-repeats.html`
- `site/pages/he/response.html`
- `site/pages/he/stories.html`
- `site/styles.css`

## Key fix categories
- Added/normalized image alt text and lazy/async loading.
- Removed transform scale rules to avoid over-cropping.
- Added safe image-frame CSS so cover/chapter images fill their boxes through width/object-fit rather than destructive scaling.
- Preserved existing TOC hierarchy and the specific title rows previously marked as not to touch.
- Ensured toc-sub entries do not carry theory thumbnails.
- Added English parallel gateway pages for he-only pages instead of hiding links.
- Updated English archive links to point to English pages instead of Hebrew pages.
- Added product-level focus accessibility, scroll-margin, sitemap.xml, and robots.txt.
- Added method-scope notes in theory documents where relevant, without rewriting the theory.
- Fixed known internal HTML links from theory documents back to Files pages.

## QA summary
- `bad_internal_html_hrefs`: 0 listed
- `bad_internal_html_hrefs_count`: 0
- `bad_image_paths_excluding_unuploaded_nested_assets`: 0 listed
- `bad_image_paths_count`: 0
- `empty_alt_count`: 0
- `empty_alt_sample`: 0 listed
- `transform_scale_files`: 0 listed
- `toc_sub_thumb_files`: 0 listed
- `duplicate_id_files_count`: 0
- `duplicate_id_files_sample`: 0 listed
