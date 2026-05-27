#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BPI ideal all-fixes patcher.
Run from repository root OR from the site/ directory.
It applies safe, additive/minimal fixes only. It preserves existing content and does not remove conceptual material.
It deliberately DOES NOT rename or remove requested-preserved TOC/title rows such as:
  Chapter ?: ↓ / פרק ?: ↓ / Chapter *: Understanding / פרק *: הבנה
"""
from pathlib import Path
from datetime import datetime
import re, html, json, shutil

try:
    from bs4 import BeautifulSoup, Tag
except Exception:
    print("Missing dependency: beautifulsoup4")
    print("Run: python3 -m pip install beautifulsoup4")
    raise

BASE_URL = "https://between-potential-and-ideal.onrender.com"
RUN_ID = datetime.now().strftime("%Y%m%d_%H%M%S")
STYLE_ID_DOC = "v300-bpi-ideal-document-image-accessibility-fixes"
STYLE_ID_SITE = "bpi-v300-site-accessibility-product-fixes"
SCIENCE_NOTE_ID = "bpi-method-scope-note"
START_HERE_ID = "bpi-start-here-clarity"
RECOMMENDED_ID = "bpi-recommended-start"

GLUED_FIXES = {
    'ואידיאליכולים': 'ואידיאל יכולים',
    'תהיהאידיאלית': 'תהיה אידיאלית',
    'ביצירהאידיאלי': 'ביצירה אידיאלי',
    'אידיאליש': 'אידיאל יש',
    'האידיאליכול': 'האידיאל יכול',
    'שהיהאידיאלי': 'שהיה אידיאלי',
    'שנעשהאידיאלי': 'שנעשה אידיאלי',
    'נעשהאידיאלי': 'נעשה אידיאלי',
}

DOC_STYLE = """
/* V300 - ideal document image/accessibility fix. Minimal, additive, preserves TOC/title structure. */
a:focus-visible, button:focus-visible, .document-screen-toc a:focus-visible, .document-backbar a:focus-visible{
  outline:3px solid #b87926!important;
  outline-offset:3px!important;
  border-radius:6px!important;
}
h1,h2,h3,h4,[id]{scroll-margin-top:76px;}
figure.cover-figure.image-frame{
  width:min(760px,100%)!important;
  max-width:100%!important;
  margin:18px auto 0!important;
  padding:0!important;
  overflow:hidden!important;
  box-sizing:border-box!important;
  text-align:center!important;
}
figure.cover-figure.image-frame > img{
  display:block!important;
  width:100%!important;
  min-width:100%!important;
  max-width:100%!important;
  height:auto!important;
  max-height:none!important;
  object-fit:cover!important;
  object-position:center center!important;
  transform:none!important;
  margin:0!important;
  border-radius:18px!important;
  box-sizing:border-box!important;
}
main figure.image-frame:not(.cover-figure),
figure.image-frame:not(.cover-figure),
.chapter-opening figure.image-frame:not(.cover-figure),
figure.chapter-figure.image-frame:not(.cover-figure){
  width:min(760px,100%)!important;
  max-width:100%!important;
  margin:24px auto 30px!important;
  padding:12px!important;
  overflow:hidden!important;
  box-sizing:border-box!important;
  text-align:center!important;
}
main figure.image-frame:not(.cover-figure) > img,
figure.image-frame:not(.cover-figure) > img,
.chapter-opening figure.image-frame:not(.cover-figure) > img,
figure.chapter-figure.image-frame:not(.cover-figure) > img{
  display:block!important;
  width:100%!important;
  min-width:100%!important;
  max-width:100%!important;
  height:auto!important;
  max-height:none!important;
  object-fit:cover!important;
  object-position:center center!important;
  transform:none!important;
  margin:0!important;
  border-radius:16px!important;
  box-sizing:border-box!important;
}
.document-screen-toc .theory-toc-entry{
  display:inline-flex!important;
  align-items:center!important;
  gap:10px!important;
}
.document-screen-toc .theory-toc-thumb-box{
  display:block!important;
  flex:0 0 58px!important;
  width:58px!important;
  min-width:58px!important;
  height:40px!important;
  overflow:hidden!important;
  border-radius:8px!important;
  border:1px solid rgba(10,58,104,.13)!important;
  background:#fffaf0!important;
  box-shadow:0 3px 9px rgba(20,40,60,.07)!important;
  margin:0!important;
  box-sizing:border-box!important;
}
.document-screen-toc .theory-toc-thumb-box .theory-toc-thumb,
.document-screen-toc img.theory-toc-thumb{
  display:block!important;
  width:100%!important;
  min-width:0!important;
  height:100%!important;
  max-width:none!important;
  max-height:none!important;
  object-fit:cover!important;
  object-position:center center!important;
  transform:none!important;
  border:0!important;
  border-radius:0!important;
  box-shadow:none!important;
  background:transparent!important;
  margin:0!important;
}
.document-screen-toc .toc-sub img.theory-toc-thumb,
.document-screen-toc .toc-sub .theory-toc-thumb-box{
  display:none!important;
}
.bpi-method-scope-note{
  margin:16px auto 22px!important;
  padding:13px 16px!important;
  border:1px solid rgba(184,121,38,.28)!important;
  border-inline-start:4px solid #b87926!important;
  border-radius:12px!important;
  background:#fff7e8!important;
  color:#4b3d2e!important;
  font-size:14px!important;
  line-height:1.58!important;
  box-sizing:border-box!important;
}
@media print{
  figure.cover-figure.image-frame{width:150mm!important;max-width:150mm!important;}
  main figure.image-frame:not(.cover-figure),figure.image-frame:not(.cover-figure){width:160mm!important;max-width:160mm!important;padding:2.5mm!important;}
  .document-screen-toc .theory-toc-thumb-box{flex-basis:18mm!important;width:18mm!important;min-width:18mm!important;height:12mm!important;box-shadow:none!important;}
}
""".strip()

SITE_STYLE = """
/* BPI V300 - product-level accessibility and navigation safety fixes. */
.skip-link{
  position:absolute!important;
  inset-inline-start:12px!important;
  top:10px!important;
  transform:translateY(-160%)!important;
  background:#1d2938!important;
  color:#fff!important;
  padding:8px 12px!important;
  border-radius:8px!important;
  z-index:9999!important;
}
.skip-link:focus{transform:translateY(0)!important;}
a:focus-visible,button:focus-visible,[role="button"]:focus-visible,input:focus-visible,select:focus-visible,textarea:focus-visible{
  outline:3px solid #b87926!important;
  outline-offset:3px!important;
  border-radius:6px!important;
}
[id]{scroll-margin-top:78px;}
.bpi-start-here-clarity,.bpi-recommended-start{
  margin:22px auto!important;
  padding:18px 20px!important;
  max-width:980px!important;
  border:1px solid rgba(184,121,38,.28)!important;
  border-radius:18px!important;
  background:#fff7e8!important;
  box-shadow:0 8px 22px rgba(23,32,45,.05)!important;
  box-sizing:border-box!important;
}
.bpi-start-here-clarity h2,.bpi-recommended-start h2{margin-top:0!important;color:#b87926!important;}
.bpi-start-actions,.bpi-recommended-grid{display:flex!important;flex-wrap:wrap!important;gap:10px!important;margin-top:12px!important;}
.bpi-start-actions a,.bpi-recommended-grid a{
  display:inline-block!important;
  padding:9px 13px!important;
  border:1px solid rgba(184,121,38,.35)!important;
  border-radius:999px!important;
  background:#fffaf0!important;
  color:#08737a!important;
  text-decoration:none!important;
  font-weight:700!important;
}
.bpi-status-note,.bpi-ai-transparency-note{
  margin:16px auto!important;
  padding:12px 15px!important;
  border:1px solid rgba(184,121,38,.22)!important;
  border-radius:12px!important;
  background:#fffaf0!important;
  color:#4b3d2e!important;
  font-size:14px!important;
  line-height:1.55!important;
}
""".strip()

def repo_root_from_cwd() -> Path:
    cwd = Path.cwd().resolve()
    if (cwd/'site').is_dir():
        return cwd
    if cwd.name == 'site' and (cwd/'files').is_dir():
        return cwd.parent
    p = cwd
    while p != p.parent:
        if (p/'site').is_dir():
            return p
        p = p.parent
    print('ERROR: Run this script from repository root or from the site/ directory.')
    raise SystemExit(2)

def read_text(p: Path) -> str:
    return p.read_text(encoding='utf-8', errors='replace')

def write_text_if_changed(p: Path, text: str, changes: list, label: str):
    old = read_text(p) if p.exists() else None
    if old != text:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding='utf-8')
        changes.append(f'{label}: {p}')

def clean_text(s: str) -> str:
    return re.sub(r'\s+', ' ', s or '').strip()

def is_hebrew_soup(soup, path: Path) -> bool:
    html_tag = soup.find('html')
    lang = (html_tag.get('lang','') if html_tag else '').lower()
    if lang.startswith('he'):
        return True
    return '-he' in path.name or '/he/' in str(path).replace('\\','/') or path.name in {'index.html'}

def remove_transform_scale(style: str) -> str:
    if not style:
        return style
    style = re.sub(r'transform\s*:\s*scale\([^)]*\)\s*!important\s*;?', '', style, flags=re.I)
    style = re.sub(r'transform\s*:\s*scale\([^)]*\)\s*;?', '', style, flags=re.I)
    style = re.sub(r'transform-origin\s*:[^;]+;?', '', style, flags=re.I)
    return style

def normalize_fig_src(src: str, expected_prefix: str) -> str:
    if not src:
        return src
    src = html.unescape(src)
    if src.startswith(('http:', 'https:', 'data:', '#', 'mailto:')):
        return src
    m = re.search(r'(?:^|/)(figures/[^?#]+)([?#].*)?$', src)
    if m:
        filename = m.group(1).split('/',1)[1]
        suffix = m.group(2) or ''
        return expected_prefix + filename + suffix
    return src

def nearest_heading_text(tag: Tag) -> str:
    for prev in tag.find_all_previous(['h1','h2','h3','h4']):
        txt = clean_text(prev.get_text(' ', strip=True))
        if txt:
            return txt
    return ''

def set_alt(img: Tag, lang_he: bool) -> bool:
    old = img.get('alt')
    if old and old.strip() and old.strip().lower() not in {'image','cover image','תמונה'}:
        return False
    title = ''
    if 'theory-toc-thumb' in (img.get('class') or []):
        a = img.find_parent('a')
        if a:
            span = a.find(class_='theory-toc-title')
            title = clean_text(span.get_text(' ', strip=True) if span else a.get_text(' ', strip=True))
        img['alt'] = (f'תמונת תוכן עניינים: {title}' if lang_he else f'TOC thumbnail: {title}') if title else ('תמונת תוכן עניינים' if lang_he else 'TOC thumbnail')
        return True
    fig = img.find_parent('figure')
    if fig:
        cap = fig.find('figcaption')
        cap_text = clean_text(cap.get_text(' ', strip=True)) if cap else ''
        if cap_text:
            img['alt'] = cap_text
        elif 'cover-figure' in (fig.get('class') or []):
            img['alt'] = 'תמונת שער: בין פוטנציאל לאידיאל' if lang_he else 'Cover image: Between Potential and Ideal'
        else:
            h = nearest_heading_text(fig)
            img['alt'] = (f'איור עבור הפרק: {h}' if lang_he else f'Illustration for chapter: {h}') if h else ('איור במסמך' if lang_he else 'Document illustration')
        return True
    h = nearest_heading_text(img)
    img['alt'] = (f'תמונה במסמך: {h}' if lang_he else f'Document image: {h}') if h else ('תמונה במסמך' if lang_he else 'Document image')
    return True

def ensure_style(head: Tag, soup: BeautifulSoup, style_id: str, css: str):
    for st in list(head.find_all('style', id=style_id)):
        st.decompose()
    st = soup.new_tag('style', id=style_id)
    st.string = css
    head.append(st)

def ensure_meta(soup: BeautifulSoup, path: Path, rel_url: str):
    head = soup.head
    if not head:
        return
    title = clean_text(soup.title.get_text(' ', strip=True)) if soup.title else 'Between Potential and Ideal'
    if not head.find('meta', attrs={'name':'description'}):
        m = soup.new_tag('meta')
        m['name'] = 'description'
        if is_hebrew_soup(soup, path):
            m['content'] = 'בין פוטנציאל לאידיאל — ניסוי מחשבתי דו־לשוני על פוטנציאל, אידיאל, משמעות ואחריות תחת אילוצים.'
        else:
            m['content'] = 'Between Potential and Ideal — a bilingual thought experiment on potential, ideal, meaning, and responsibility under constraints.'
        head.append(m)
    if not head.find('link', rel='canonical'):
        c = soup.new_tag('link')
        c['rel'] = 'canonical'
        c['href'] = f'{BASE_URL}/{rel_url}'
        head.append(c)
    if not head.find('meta', property='og:title'):
        og = soup.new_tag('meta'); og['property']='og:title'; og['content']=title; head.append(og)
    if not head.find('meta', property='og:type'):
        og = soup.new_tag('meta'); og['property']='og:type'; og['content']='website'; head.append(og)

def wrap_toc_thumbs(soup: BeautifulSoup):
    toc = soup.find(id='interactive-toc') or soup.find(class_='document-screen-toc')
    removed = 0; wrapped = 0
    if not toc:
        return removed, wrapped
    for li in toc.select('li.toc-sub'):
        for box in list(li.select('.theory-toc-thumb-box')):
            box.decompose(); removed += 1
        for im in list(li.select('img.theory-toc-thumb')):
            im.decompose(); removed += 1
    for img in list(toc.select('li.toc-main img.theory-toc-thumb')):
        if img.find_parent(class_='theory-toc-thumb-box'):
            continue
        box = soup.new_tag('span')
        box['class'] = 'theory-toc-thumb-box'
        img.wrap(box)
        wrapped += 1
    return removed, wrapped

def remove_adjacent_duplicate_figures(soup: BeautifulSoup) -> int:
    removed = 0
    for parent in soup.find_all(True):
        prev_src = None; prev_was_fig = False
        for child in list(parent.children):
            if not isinstance(child, Tag):
                continue
            if child.name == 'figure':
                img = child.find('img')
                src = img.get('src') if img else None
                if prev_was_fig and src and src == prev_src:
                    child.decompose(); removed += 1
                    continue
                prev_src = src; prev_was_fig = True
            elif child.name in ['p','div'] and not clean_text(child.get_text(' ', strip=True)):
                continue
            else:
                prev_src = None; prev_was_fig = False
    return removed

def add_method_note(soup: BeautifulSoup, lang_he: bool) -> bool:
    if soup.find(id=SCIENCE_NOTE_ID):
        return False
    target = soup.find(id='interactive-toc') or soup.find('main') or soup.find(id='main') or soup.body
    if not target:
        return False
    note = soup.new_tag('aside', id=SCIENCE_NOTE_ID)
    note['class'] = 'bpi-method-scope-note'
    if lang_he:
        note.string = 'הבהרת מתודולוגיה: כאשר מופיעים כאן מושגים ממדע, מתמטיקה, פיזיקה, מדעי המחשב או לוגיקה, יש לקרוא אותם כמודלים ומטאפורות מבניות אלא אם נאמר במפורש שמדובר בטענה פורמלית או מדעית. המסמך הוא ניסוי מחשבתי פתוח, לא הוכחה מדעית סגורה.'
    else:
        note.string = 'Method note: when concepts from science, mathematics, physics, computer science, or logic appear here, they should be read as structural models and metaphors unless explicitly marked as formal or scientific claims. This document is an open thought experiment, not a closed scientific proof.'
    target.insert_before(note)
    return True

def add_tightened_note(soup: BeautifulSoup, lang_he: bool) -> bool:
    if soup.find(id='bpi-tightened-version-note'):
        return False
    if 'tightened' not in clean_text(soup.get_text(' ', strip=True)).lower() and not soup.find(string=re.compile('מהודק|מהודקת|tightened', re.I)):
        return False
    toc = soup.find(id='interactive-toc') or soup.find(class_='document-screen-toc')
    if not toc:
        return False
    note = soup.new_tag('p', id='bpi-tightened-version-note')
    note['class'] = 'bpi-status-note'
    note.string = 'הערה: זוהי גרסה מהודקת/לוגית. היא מיועדת לקריאה מרוכזת ולכן עשויה לקצר חלק מההרחבות שקיימות במסמך המלא, בלי לשנות את משמעות הליבה.' if lang_he else 'Note: this is a tightened/logical version. It is meant for focused reading and may condense some expansions from the full document without changing the core meaning.'
    toc.insert_before(note)
    return True

def fix_html_file(path: Path, root: Path, is_theory_doc: bool, changes: dict):
    raw = read_text(path)
    original = raw
    for a,b in GLUED_FIXES.items():
        raw = raw.replace(a,b)
    soup = BeautifulSoup(raw, 'html.parser')
    if not soup.find('html'):
        return
    lang_he = is_hebrew_soup(soup, path)
    if soup.html:
        soup.html['dir'] = 'rtl' if lang_he else 'ltr'
        soup.html['lang'] = 'he' if lang_he else 'en'
    rel_url = str(path.relative_to(root/'site')).replace('\\','/') if str(path).startswith(str(root/'site')) else path.name
    if rel_url.startswith('/'):
        rel_url = rel_url[1:]
    if soup.head:
        ensure_meta(soup, path, rel_url)
    if is_theory_doc:
        for st in list(soup.find_all('style')):
            sid = st.get('id','')
            if sid == STYLE_ID_DOC or re.match(r'v13[1-9]-.*(?:image|gap|fill|duplicate|cover)', sid, re.I):
                st.decompose()
        for st in soup.find_all('style'):
            old = st.string or st.get_text()
            new = remove_transform_scale(old)
            if new != old:
                st.string = new
                changes['scale_removed'] = changes.get('scale_removed',0) + old.count('scale(')
        for tag in soup.find_all(True):
            if tag.has_attr('style'):
                old = tag['style']; new = remove_transform_scale(old)
                if new != old:
                    tag['style'] = new
                    changes['scale_removed'] = changes.get('scale_removed',0) + old.count('scale(')
        if soup.head:
            ensure_style(soup.head, soup, STYLE_ID_DOC, DOC_STYLE)
        add_method_note(soup, lang_he)
        add_tightened_note(soup, lang_he)
        expected = '../../figures/' if 'editorial-tightened' in str(path).replace('\\','/') else '../figures/'
        for img in soup.find_all('img'):
            old_src = img.get('src')
            new_src = normalize_fig_src(old_src, expected)
            if new_src != old_src:
                img['src'] = new_src
                changes['paths_normalized'] = changes.get('paths_normalized',0)+1
        removed, wrapped = wrap_toc_thumbs(soup)
        changes['toc_sub_thumbs_removed'] = changes.get('toc_sub_thumbs_removed',0)+removed
        changes['toc_thumbs_wrapped'] = changes.get('toc_thumbs_wrapped',0)+wrapped
        dup = remove_adjacent_duplicate_figures(soup)
        changes['duplicate_figures_removed'] = changes.get('duplicate_figures_removed',0)+dup
    for img in soup.find_all('img'):
        if set_alt(img, lang_he):
            changes['alt_added'] = changes.get('alt_added',0)+1
        if not img.has_attr('loading'):
            img['loading'] = 'lazy'; changes['lazy_added'] = changes.get('lazy_added',0)+1
        if not img.has_attr('decoding'):
            img['decoding'] = 'async'; changes['decoding_added'] = changes.get('decoding_added',0)+1
    if soup.body and not soup.find('a', class_='skip-link'):
        main_target = soup.find(id='main') or soup.find('main')
        if main_target:
            if not main_target.get('id'):
                main_target['id'] = 'main'
            skip = soup.new_tag('a', href='#main'); skip['class'] = 'skip-link'
            skip.string = 'דלג לתוכן המרכזי' if lang_he else 'Skip to main content'
            soup.body.insert(0, skip); changes['skip_links_added'] = changes.get('skip_links_added',0)+1
    for a in soup.find_all('a'):
        txt = clean_text(a.get_text(' ', strip=True)); href = (a.get('href') or '').lower()
        if txt in {'דיון פתוח','Open Discussion'} and any(x in href for x in ['response','contact','mailto','feedback','reply','comment']):
            a.string = 'שליחת תגובה' if lang_he else 'Send feedback'
            changes['discussion_labels_fixed'] = changes.get('discussion_labels_fixed',0)+1
    out = str(soup)
    if original.lstrip().lower().startswith('<!doctype') and not out.lstrip().lower().startswith('<!doctype'):
        out = '<!DOCTYPE html>\n' + out
    if out != original:
        path.write_text(out, encoding='utf-8')
        changes['html_files_changed'] = changes.get('html_files_changed',0)+1

def add_site_style(root: Path, changes: dict):
    css = root/'site/styles.css'
    if not css.exists():
        return
    text = read_text(css)
    block = f'\n\n/* {STYLE_ID_SITE} */\n{SITE_STYLE}\n'
    if STYLE_ID_SITE not in text:
        css.write_text(text.rstrip()+block, encoding='utf-8')
        changes['styles_css_updated'] = True

def add_start_here_to_home(path: Path, lang_he: bool, changes: dict):
    if not path.exists(): return
    raw = read_text(path)
    if START_HERE_ID in raw: return
    soup = BeautifulSoup(raw, 'html.parser')
    target = soup.find('main') or soup.find(id='main') or soup.body
    if not target: return
    sec = soup.new_tag('section', id=START_HERE_ID); sec['class'] = 'bpi-start-here-clarity'
    if lang_he:
        html_block = '<h2>התחל כאן</h2><p>זהו ניסוי מחשבתי דו־לשוני שמחבר מסה פילוסופית, מבנה לוגי, סיפורים ויישומים. הדרך המומלצת היא להתחיל בתקציר, לעבור לגרסה המהודקת, ואז לפתוח את המסמך המלא או הנספחים.</p><div class="bpi-start-actions"><a href="pages/he/summary.html">תקציר</a><a href="files/editorial-tightened/between-potential-and-ideal-tightened-he.html">גרסה מהודקת</a><a href="files/between-potential-and-ideal-he-editorial.html">המסמך המלא</a></div>'
    else:
        html_block = '<h2>Start here</h2><p>This is a bilingual thought experiment combining a philosophical essay, a logical structure, stories, and applications. The recommended path is to start with the summary, continue to the tightened version, and then open the full document or appendices.</p><div class="bpi-start-actions"><a href="pages/en/summary-en.html">Summary</a><a href="files/editorial-tightened/between-potential-and-ideal-tightened-en.html">Tightened version</a><a href="files/between-potential-and-ideal-en-editorial.html">Full document</a></div>'
    sec.append(BeautifulSoup(html_block, 'html.parser'))
    children = [c for c in target.children if isinstance(c, Tag)]
    if children: children[0].insert_after(sec)
    else: target.append(sec)
    path.write_text(str(soup), encoding='utf-8'); changes['home_start_here_added'] = changes.get('home_start_here_added',0)+1

def add_recommended_to_files(path: Path, lang_he: bool, changes: dict):
    if not path.exists(): return
    raw = read_text(path)
    if RECOMMENDED_ID in raw: return
    soup = BeautifulSoup(raw, 'html.parser')
    target = soup.find('main') or soup.find(id='main') or soup.body
    if not target: return
    sec = soup.new_tag('section', id=RECOMMENDED_ID); sec['class'] = 'bpi-recommended-start'
    if lang_he:
        html_block = '<h2>התחלה מומלצת</h2><p>כדי לא להיכנס ישר לארכיון, מומלץ לקרוא לפי הסדר הזה.</p><div class="bpi-recommended-grid"><a href="summary.html">1. תקציר</a><a href="../../files/editorial-tightened/between-potential-and-ideal-tightened-he.html">2. גרסה מהודקת / לוגית</a><a href="../../files/between-potential-and-ideal-he-editorial.html">3. מסמך מלא</a></div>'
    else:
        html_block = '<h2>Recommended start</h2><p>To avoid entering directly through the archive, start with this reading path.</p><div class="bpi-recommended-grid"><a href="summary-en.html">1. Summary</a><a href="../../files/editorial-tightened/between-potential-and-ideal-tightened-en.html">2. Tightened / logical version</a><a href="../../files/between-potential-and-ideal-en-editorial.html">3. Full document</a></div>'
    sec.append(BeautifulSoup(html_block, 'html.parser'))
    h = target.find(['h1','h2']) if isinstance(target, Tag) else None
    if h: h.insert_after(sec)
    else: target.insert(0, sec)
    path.write_text(str(soup), encoding='utf-8'); changes['files_recommended_added'] = changes.get('files_recommended_added',0)+1

def write_text_if_changed_file(p: Path, text: str, changes: dict, label: str):
    old = read_text(p) if p.exists() else None
    if old != text:
        p.write_text(text, encoding='utf-8')
        changes.setdefault('file_changes',[]).append(f'{label}: {p}')

def create_sitemap_and_robots(root: Path, changes: dict):
    site = root/'site'
    htmls = sorted(p for p in site.rglob('*.html') if '.git' not in p.parts)
    urls = []
    for p in htmls:
        rel = p.relative_to(site).as_posix()
        if rel.endswith('redirect.html'): continue
        urls.append(f'  <url><loc>{BASE_URL}/{rel}</loc></url>')
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + '\n'.join(urls) + '\n</urlset>\n'
    write_text_if_changed_file(site/'sitemap.xml', sitemap, changes, 'sitemap')
    robots = f'User-agent: *\nAllow: /\n\nSitemap: {BASE_URL}/sitemap.xml\n'
    write_text_if_changed_file(site/'robots.txt', robots, changes, 'robots')

def qa(root: Path):
    site = root/'site'
    out = {'html_files':0,'empty_alt':[],'scale_in_theory_docs':[],'toc_sub_thumbs':[],'bad_hash_targets':[],'missing_local_images':[],'redirect_links':[]}
    for p in site.rglob('*.html'):
        out['html_files'] += 1
        s = read_text(p); soup = BeautifulSoup(s,'html.parser')
        ids = {t.get('id') for t in soup.find_all(attrs={'id': True})}
        for a in soup.find_all('a', href=True):
            href = a['href']
            if href.startswith('#') and href[1:] not in ids: out['bad_hash_targets'].append([str(p.relative_to(root)), href, clean_text(a.get_text(' ',strip=True))])
            if 'redirect.html' in href: out['redirect_links'].append([str(p.relative_to(root)), href, clean_text(a.get_text(' ',strip=True))])
        for img in soup.find_all('img'):
            if not img.get('alt','').strip(): out['empty_alt'].append([str(p.relative_to(root)), img.get('src','')])
            src = img.get('src','')
            if src and not src.startswith(('http:','https:','data:','mailto:','#')):
                src_noq = src.split('#')[0].split('?')[0]
                target = (p.parent / src_noq).resolve() if not src_noq.startswith('/') else (site / src_noq.lstrip('/')).resolve()
                if not target.exists(): out['missing_local_images'].append([str(p.relative_to(root)), src])
        if p.name.startswith('between-potential-and-ideal') or 'editorial-tightened' in str(p):
            if 'scale(' in s: out['scale_in_theory_docs'].append(str(p.relative_to(root)))
            toc=soup.find(id='interactive-toc') or soup.find(class_='document-screen-toc')
            if toc and toc.select('li.toc-sub img.theory-toc-thumb, li.toc-sub .theory-toc-thumb-box'): out['toc_sub_thumbs'].append(str(p.relative_to(root)))
    return out

def main():
    root = repo_root_from_cwd(); site = root/'site'
    if not site.exists(): raise SystemExit('site/ not found')
    changes = {}; backup_root = root / f'.bpi_fix_backup_{RUN_ID}'
    candidates = [site/'styles.css', site/'index.html', site/'en.html', site/'pages/he/files.html', site/'pages/en/files-en.html'] + list(site.rglob('*.html'))
    seen=set()
    for p in candidates:
        if p.exists() and p not in seen:
            seen.add(p); b = backup_root / p.relative_to(root); b.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(p,b)
    add_site_style(root, changes)
    add_start_here_to_home(site/'index.html', True, changes)
    add_start_here_to_home(site/'en.html', False, changes)
    add_recommended_to_files(site/'pages/he/files.html', True, changes)
    add_recommended_to_files(site/'pages/en/files-en.html', False, changes)
    theory_names = {'between-potential-and-ideal-he-editorial.html','between-potential-and-ideal-en-editorial.html','between-potential-and-ideal-he.html','between-potential-and-ideal-en.html','between-potential-and-ideal-tightened-he.html','between-potential-and-ideal-tightened-en.html'}
    for p in sorted(site.rglob('*.html')):
        fix_html_file(p, root, p.name in theory_names, changes)
    create_sitemap_and_robots(root, changes)
    q = qa(root)
    report = {'run_id': RUN_ID, 'repo_root': str(root), 'backup_root': str(backup_root), 'changes': changes, 'qa': q, 'notes': ['Preserved requested TOC/title artifacts.', 'No conceptual body text was removed.', 'PDF/DOCX regeneration still depends on the existing build/export pipeline.']}
    out = root / f'BPI_IDEAL_FIX_REPORT_{RUN_ID}.json'
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print('\nBPI ideal fixes applied.')
    print('Backup:', backup_root)
    print('Report:', out)
    print('\nChanged summary:')
    for k,v in changes.items(): print(f'- {k}: {v}')
    print('\nQA summary:')
    for k,v in q.items(): print(f'- {k}: {len(v) if isinstance(v, list) else v}')
    print('\nNext: run git diff --stat, inspect visually, then commit.')

if __name__ == '__main__':
    main()
