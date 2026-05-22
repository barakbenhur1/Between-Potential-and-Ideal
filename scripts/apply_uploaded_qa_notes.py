#!/usr/bin/env python3
from pathlib import Path
from bs4 import BeautifulSoup
import re
import os

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'theory-site-static'
BASE_URL = 'https://between-potential-and-ideal.onrender.com/'

PAGE_PAIRS = {
    'index.html': 'en.html',
    'summary.html': 'summary-en.html',
    'core.html': 'core-en.html',
    'witness.html': 'witness-en.html',
    'applied.html': 'applied-en.html',
    'ai.html': 'ai-en.html',
    'files.html': 'files-en.html',
    'methodology.html': 'methodology-en.html',
    'critique.html': 'critique-en.html',
    'sources.html': 'sources-en.html',
    'about.html': 'about-en.html',
    'changelog.html': 'changelog-en.html',
}

ALL_TOP_HTML = [p.name for p in SITE.glob('*.html')]


def read(p):
    return p.read_text(encoding='utf-8', errors='ignore')

def write(p, s):
    p.write_text(s, encoding='utf-8')


def format_size(n):
    if n < 1024:
        return f'{n} B'
    if n < 1024*1024:
        return f'{n/1024:.1f} KB'
    return f'{n/(1024*1024):.1f} MB'


def ensure_meta_link(soup, rel, href, attrs=None):
    head = soup.head
    if not head:
        return
    if soup.find('link', rel=rel, href=href):
        return
    tag = soup.new_tag('link', rel=rel, href=href)
    if attrs:
        for k,v in attrs.items():
            tag[k] = v
    # insert before stylesheet if possible
    css = head.find('link', href=re.compile(r'styles\.css'))
    if css:
        css.insert_before(tag)
    else:
        head.append(tag)


def add_seo_language_links():
    inverse = {v:k for k,v in PAGE_PAIRS.items()}
    for fname in ALL_TOP_HTML:
        path = SITE / fname
        if not path.exists():
            continue
        soup = BeautifulSoup(read(path), 'html.parser')
        html = soup.find('html')
        lang = html.get('lang','') if html else ''
        if fname in PAGE_PAIRS:
            he = fname
            en = PAGE_PAIRS[fname]
            canonical = he
        elif fname in inverse:
            he = inverse[fname]
            en = fname
            canonical = en
        else:
            # archive/unpaired pages get self canonical only
            ensure_meta_link(soup, 'canonical', BASE_URL + fname)
            write(path, str(soup))
            continue
        ensure_meta_link(soup, 'canonical', BASE_URL + canonical)
        ensure_meta_link(soup, 'alternate', BASE_URL + he, {'hreflang':'he'})
        ensure_meta_link(soup, 'alternate', BASE_URL + en, {'hreflang':'en'})
        # Hebrew is default for Hebrew pages, English default for English pages; index for neutral fallback
        ensure_meta_link(soup, 'alternate', BASE_URL + ('index.html' if lang == 'he' else 'en.html'), {'hreflang':'x-default'})
        # OG locale
        head = soup.head
        if head and not soup.find('meta', property='og:locale'):
            og = soup.new_tag('meta')
            og['property'] = 'og:locale'
            og['content'] = 'he_IL' if lang == 'he' else 'en_US'
            head.append(og)
        if head and not soup.find('meta', property='og:locale:alternate'):
            og2 = soup.new_tag('meta')
            og2['property'] = 'og:locale:alternate'
            og2['content'] = 'en_US' if lang == 'he' else 'he_IL'
            head.append(og2)
        write(path, str(soup))


def add_file_controls_and_notes():
    specs = {
        'files.html': {
            'title':'סינון וחיפוש בקבצים',
            'search':'חפש לפי שם, תיאור, שפה או פורמט',
            'all_type':'כל הפורמטים',
            'all_lang':'כל השפות',
            'note_h':'שימוש וזכויות',
            'note_p':'הקבצים זמינים לקריאה, שיתוף פרטי וביקורת. שימוש ציבורי, ציטוטים נרחבים, העתקה או פרסום מחדש דורשים ציון מקור והסכמה מפורשת אלא אם צוין רישיון אחר בתוך הקובץ עצמו.',
            'archives_h':'עמודי ארכיון ונספחים נוספים',
            'archives_p':'עמודים אלה קיימים כחומרי רקע וקריאה משלימה. הם אינם מחליפים את מסלול הקריאה הראשי, אך מאפשרים להגיע לסיפורים, דיונים ונספחי AI/טעות.',
            'links':[('stories.html','סיפורים ורקע'),('discussion.html','דיון פתוח'),('response.html','תגובה'),('mistake-repeats.html','טעות לעולם חוזרת'),('ai-believes.html','נספחי AI')]
        },
        'files-en.html': {
            'title':'Filter and search files',
            'search':'Search by name, description, language or format',
            'all_type':'All formats',
            'all_lang':'All languages',
            'note_h':'Use and rights',
            'note_p':'The files are provided for reading, private sharing and critique. Public use, extended quotation, republication or redistribution requires attribution and explicit permission unless a different license is stated inside the file itself.',
            'archives_h':'Archive pages and additional appendices',
            'archives_p':'These pages exist as background and supporting material. They do not replace the main reading path, but they make stories, discussions and AI/mistake appendices discoverable.',
            'links':[('stories.html','Stories and background'),('discussion.html','Open discussion'),('response.html','Response'),('mistake-repeats.html','Mistake Repeats'),('ai-believes.html','AI appendices')]
        }
    }
    for fname, spec in specs.items():
        path = SITE / fname
        soup = BeautifulSoup(read(path), 'html.parser')
        if soup.find(id='file-filter-panel'):
            continue
        wrap = soup.find('div', class_='table-wrap')
        if not wrap:
            continue
        section = soup.new_tag('section', **{'class':'file-tools media-card accent-files', 'id':'file-filter-panel'})
        h = soup.new_tag('h2'); h.string = spec['title']; section.append(h)
        p = soup.new_tag('p'); p.string = spec['search']; section.append(p)
        controls = soup.new_tag('div', **{'class':'file-filter-controls'})
        inp = soup.new_tag('input', **{'type':'search','id':'fileSearch','placeholder':spec['search'],'aria-label':spec['search']})
        sel_type = soup.new_tag('select', **{'id':'fileTypeFilter','aria-label':spec['all_type']})
        sel_lang = soup.new_tag('select', **{'id':'fileLangFilter','aria-label':spec['all_lang']})
        for sel,label,values in [(sel_type,spec['all_type'],['','HTML','PDF','Word','Markdown','Text']), (sel_lang,spec['all_lang'],['','עברית','English','Mixed/source'])]:
            opt=soup.new_tag('option', value=''); opt.string=label; sel.append(opt)
            for v in values[1:]:
                opt=soup.new_tag('option', value=v.lower()); opt.string=v; sel.append(opt)
        controls.append(inp); controls.append(sel_type); controls.append(sel_lang); section.append(controls)
        note=soup.new_tag('p', **{'class':'file-filter-count','id':'fileFilterCount'}); note.string=''; section.append(note)
        wrap.insert_before(section)
        # Rights note after format note
        main = soup.find('main')
        rights = soup.new_tag('section', **{'class':'notice-box media-card accent-methodology file-rights-note'})
        div=soup.new_tag('div', **{'class':'card-media-head'}); img=soup.new_tag('img', src='figures/thumb_sources.png', alt=spec['note_h'], **{'class':'card-thumb','loading':'lazy','decoding':'async','width':'480','height':'480'}); hh=soup.new_tag('h2'); hh.string=spec['note_h']; div.append(img); div.append(hh); rights.append(div)
        pp=soup.new_tag('p'); pp.string=spec['note_p']; rights.append(pp)
        if main and not soup.find(class_='file-rights-note'):
            # after existing language note if possible
            lang_note = soup.find('section', class_=lambda x: x and 'language-status-note' in x)
            if lang_note: lang_note.insert_after(rights)
            else: wrap.insert_before(rights)
        archives=soup.new_tag('section', **{'class':'notice-box media-card accent-files archive-links-note'})
        div=soup.new_tag('div', **{'class':'card-media-head'}); img=soup.new_tag('img', src='figures/thumb_files.png', alt=spec['archives_h'], **{'class':'card-thumb','loading':'lazy','decoding':'async','width':'480','height':'480'}); hh=soup.new_tag('h2'); hh.string=spec['archives_h']; div.append(img); div.append(hh); archives.append(div)
        pp=soup.new_tag('p'); pp.string=spec['archives_p']; archives.append(pp)
        row=soup.new_tag('div', **{'class':'archive-link-row'})
        for href,label in spec['links']:
            a=soup.new_tag('a', href=href, **{'class':'download-button'}); a.string=label; row.append(a)
        archives.append(row)
        if main and not soup.find(class_='archive-links-note'):
            wrap.insert_after(archives)
        # metadata fixes in table
        for tr in soup.select('table.download-table tr'):
            a = tr.find('a')
            tds = tr.find_all('td')
            if not a or len(tds) < 3:
                continue
            href = a.get('href','')
            name = Path(href).name
            if '-en.' in name or name.endswith('_en.txt') or 'english' in name.lower():
                tds[2].string = 'English'
            elif '-he.' in name or name.endswith('_he.txt') or 'hebrew' in name.lower() or 'rtl' in name.lower():
                tds[2].string = 'עברית'
            elif name.lower().endswith('readme.txt') or 'super_mirrors_when_its_not_you_final_micro' in name:
                tds[2].string = 'Mixed/source'
        write(path, str(soup))


def add_sources_depth():
    data = {
        'sources.html': {
            'h':'מקורות מורחבים לפי תחומים',
            'p':'העמוד הציבורי נשאר קצר כדי לא להכביד על קורא חדש, אך המסות המלאות כוללות שכבת מקורות רחבה יותר. כדי לצמצם פער בין שאפתנות התאוריה לבין הראות הציבורית של מקורותיה, מומלץ לקרוא את המקורות דרך המעגלים הבאים:',
            'items':['פילוסופיה: פוטנציאל, אידיאל, אפשרות, גבול, אמת ותנועה.','לוגיקה ומתמטיקה: גדל, טיורינג, P מול NP, QBF וסוגי טענה פורמלית.','פיזיקה וקוסמולוגיה: ואקום, אנטרופיה, יחסות, קוונטים, אופקי אירועים וחורים שחורים כמטאפורות מבניות בלבד.','AI ואלגברה ליניארית: מודלים, embeddings, הסתברות, חיזוי, אנתרופומורפיזם וזהירות מפני האנשת מכונה.','דתות ומסורות: שימוש במונחים וסמלים מתוך כבוד, השוואה וזהירות, לא כהחלפת מסורת קיימת.'],
            'link':'files/between-potential-and-ideal-he-editorial.html',
            'label':'לקריאת המסה המלאה והביבליוגרפיה המורחבת'
        },
        'sources-en.html': {
            'h':'Extended sources by domain',
            'p':'The public sources page stays short so a new reader is not overloaded, but the full essays contain a broader source layer. To reduce the gap between the theory’s ambition and the public visibility of its grounding, read the sources through these circles:',
            'items':['Philosophy: potential, ideal, possibility, boundary, truth and movement.','Logic and mathematics: Gödel, Turing, P vs NP, QBF and formal claim types.','Physics and cosmology: vacuum, entropy, relativity, quantum language, event horizons and black holes as structural metaphors only.','AI and linear algebra: models, embeddings, probability, prediction, anthropomorphism and caution against machine personhood.','Religions and traditions: terms and symbols used with respect, comparison and caution, not as a replacement for any tradition.'],
            'link':'files/between-potential-and-ideal-en-editorial.html',
            'label':'Read the full essay and expanded bibliography'
        }
    }
    for fname,spec in data.items():
        p=SITE/fname
        soup=BeautifulSoup(read(p),'html.parser')
        if soup.find(id='extended-sources'):
            continue
        main=soup.find('main')
        sec=soup.new_tag('section', id='extended-sources', **{'class':'notice-box media-card accent-sources'})
        div=soup.new_tag('div', **{'class':'card-media-head'}); img=soup.new_tag('img',src='figures/thumb_sources.png',alt=spec['h'], **{'class':'card-thumb','loading':'lazy','decoding':'async','width':'480','height':'480'}); h=soup.new_tag('h2'); h.string=spec['h']; div.append(img); div.append(h); sec.append(div)
        pp=soup.new_tag('p'); pp.string=spec['p']; sec.append(pp)
        ul=soup.new_tag('ul')
        for it in spec['items']:
            li=soup.new_tag('li'); li.string=it; ul.append(li)
        sec.append(ul)
        a=soup.new_tag('a', href=spec['link'], **{'class':'card-link','target':'_blank','rel':'noopener noreferrer'}); a.string=spec['label']; sec.append(a)
        if main:
            main.append(sec)
        write(p,str(soup))


def remove_placeholder_chapters():
    html_files = [
        SITE/'files/between-potential-and-ideal-he-editorial.html',
        SITE/'files/between-potential-and-ideal-en-editorial.html',
        SITE/'files/editorial-tightened/between-potential-and-ideal-tightened-he.html',
        SITE/'files/editorial-tightened/between-potential-and-ideal-tightened-en.html',
    ]
    for p in html_files:
        if not p.exists(): continue
        soup=BeautifulSoup(read(p),'html.parser')
        changed=False
        # remove TOC entries pointing to placeholder headings
        for a in list(soup.find_all('a', href=True)):
            href=a['href']
            if href.startswith('#פרק-?') or href.startswith('#Chapter-?'):
                li=a.find_parent('li')
                if li:
                    li.decompose(); changed=True
        # remove placeholder h2 entries
        for h in list(soup.find_all(['h1','h2','h3'])):
            hid=h.get('id','')
            text=h.get_text(' ',strip=True)
            if hid.startswith('פרק-?') or hid.startswith('Chapter-?') or re.fullmatch(r'(פרק|Chapter) \?:\s*[↓.]?', text):
                h.decompose(); changed=True
        if changed:
            write(p,str(soup))
    md_files = [
        SITE/'files/between-potential-and-ideal-he.md',
        SITE/'files/between-potential-and-ideal-en.md',
        SITE/'files/editorial-tightened/between-potential-and-ideal-tightened-he.md',
        SITE/'files/editorial-tightened/between-potential-and-ideal-tightened-en.md',
    ]
    pat = re.compile(r'^##\s+<span class="(?:chapter-prefix|mystery-spacer)">(פרק|Chapter) \?:</span><span class="(?:mystery-arrow|mystery-dotmark)">[↓.]</span>\s*$', re.M)
    for p in md_files:
        if not p.exists(): continue
        s=read(p)
        ns=pat.sub('',s)
        ns=re.sub(r'\n{3,}', '\n\n', ns)
        if ns != s:
            write(p,ns)


def update_css_and_js():
    css = SITE/'styles.css'
    s = read(css)
    append = r'''

/* QA notes pass: accessibility, file filtering and softer card side light */
.file-tools{margin:22px 0;padding:clamp(18px,3vw,28px)}
.file-filter-controls{display:flex;gap:12px;flex-wrap:wrap;align-items:center;margin-top:12px}
.file-filter-controls input,.file-filter-controls select{font:inherit;min-height:44px;border:1px solid var(--line);background:rgba(255,249,236,.88);color:var(--ink);border-radius:999px;padding:10px 14px;box-shadow:0 8px 22px rgba(23,32,45,.04)}
.file-filter-controls input{flex:1 1 280px}.file-filter-controls select{flex:0 1 180px}.file-filter-count{font-family:ui-sans-serif,system-ui;color:var(--muted);font-size:.9rem;margin-top:10px}.archive-link-row{display:flex;flex-wrap:wrap;gap:10px;margin-top:16px}
.download-table tr[hidden]{display:none!important}
.media-card::after,.reader-card::after,.notice-box::after{filter:saturate(1.06) brightness(1.18);opacity:.82}
@media (prefers-reduced-motion: reduce){html{scroll-behavior:auto!important}*,*::before,*::after{animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important;scroll-behavior:auto!important}}
@media (max-width:720px){.table-wrap{overflow-x:auto}.download-table{min-width:760px}.file-filter-controls{display:grid;grid-template-columns:1fr}.file-filter-controls input,.file-filter-controls select{width:100%}}
'''
    if 'QA notes pass: accessibility' not in s:
        write(css, s+append)
    js = SITE/'script.js'
    j = read(js)
    add = r'''

function setupFileFiltering(){
  const table=document.querySelector('.download-table');
  const search=document.getElementById('fileSearch');
  const type=document.getElementById('fileTypeFilter');
  const lang=document.getElementById('fileLangFilter');
  const count=document.getElementById('fileFilterCount');
  if(!table||!search||!type||!lang) return;
  const rows=Array.from(table.querySelectorAll('tr')).slice(1);
  function apply(){
    const q=(search.value||'').trim().toLowerCase();
    const ft=(type.value||'').toLowerCase();
    const fl=(lang.value||'').toLowerCase();
    let visible=0;
    rows.forEach(row=>{
      const cells=Array.from(row.children).map(td=>(td.textContent||'').toLowerCase());
      const text=cells.join(' ');
      const matchesQ=!q||text.includes(q);
      const matchesT=!ft||(cells[1]||'').includes(ft);
      const matchesL=!fl||(cells[2]||'').includes(fl);
      const show=matchesQ&&matchesT&&matchesL;
      row.hidden=!show;
      if(show) visible++;
    });
    if(count) count.textContent = document.documentElement.lang==='he' ? `${visible} קבצים מוצגים` : `${visible} files shown`;
  }
  [search,type,lang].forEach(el=>el.addEventListener('input',apply));
  apply();
}
document.addEventListener('DOMContentLoaded',setupFileFiltering);
'''
    if 'setupFileFiltering' not in j:
        write(js,j+add)
    # Ensure pages include script.js
    for fname in ['files.html','files-en.html']:
        p=SITE/fname
        soup=BeautifulSoup(read(p),'html.parser')
        if not soup.find('script', src='script.js'):
            script=soup.new_tag('script', src='script.js', defer=True)
            soup.body.append(script)
            write(p,str(soup))


def update_sitemap():
    p=SITE/'sitemap.xml'
    if not p.exists(): return
    s=read(p)
    extras=['stories.html','discussion.html','response.html','mistake-repeats.html','ai-believes.html']
    insert=''
    for e in extras:
        if e not in s:
            insert += f'  <url><loc>{BASE_URL}{e}</loc><lastmod>2026-05-21</lastmod></url>\n'
    if insert and '</urlset>' in s:
        s=s.replace('</urlset>',insert+'</urlset>')
        write(p,s)


def update_readme_and_changelog():
    root_readme=ROOT/'README.md'
    if not root_readme.exists():
        root_readme.write_text('# Between Potential and Ideal\n',encoding='utf-8')
    r=read(root_readme)
    add='''

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
- Preserved “פרק ?:” / “Chapter ?:” as intentional open/infinite chapter markers, not placeholders.
- Preserved intentional poetic differences between Hebrew and English blurbs, including the water/vessel line.
- Added reduced-motion CSS handling.
- Expanded public source-context pages with domain-based source guidance.
'''
    if 'QA notes integrated in this package' not in r:
        write(root_readme,r+add)
    site_readme=SITE/'README.md'
    sr=read(site_readme) if site_readme.exists() else '# theory-site-static\n'
    if 'QA notes integrated in this package' not in sr:
        write(site_readme,sr+add)
    changelog=SITE/'CHANGELOG_QA_NOTES_FIX_HE.md'
    changelog.write_text('''# תיקוני QA לפי ההערות שהועלו\n\nבוצע סבב תיקונים ממוקד לפי דוחות הביקורת המצורפים, תוך שמירה על הבדלים מכוונים בין עברית לאנגלית.\n\n## תוקן\n- נוספו canonical/hreflang לדפים דו-לשוניים מרכזיים.\n- נוסף סינון וחיפוש לעמודי הקבצים בעברית ובאנגלית.\n- נוסף הסבר שימוש וזכויות בעמודי הקבצים.\n- נוספו קישורים לעמודי ארכיון/נספחים קיימים כדי שלא יישארו מיותמים.\n- נשמרו סימוני “פרק ?:” / “Chapter ?:” כסימון רעיוני מכוון לפתיחות ולא כ-placeholder.\n- תוקנה מטא-דאטת שפה בטבלת הקבצים לפי שמות קבצים מובהקים.\n- נוספה תמיכה ב-prefers-reduced-motion.\n- הורחבו עמודי המקורות בשכבת מקורות לפי תחומים.\n\n## נשמר במכוון\n- לא שונה משפט המים/כלי בין עברית לאנגלית, משום שהפער שם יכול להיות בחירה פואטית מכוונת ולא בהכרח טעות תרגום.\n- לא שוטחו טקסטים פילוסופיים ולא הוחלפו ניסוחים עמוקים בניסוח טכני.\n- לא נמחקו קבצי דוחות/אימות, אלא רק הובהרה ההבחנה בין ארכיון/עבודה לבין מסלול קריאה.\n''',encoding='utf-8')


def main():
    add_seo_language_links()
    add_file_controls_and_notes()
    add_sources_depth()
    remove_placeholder_chapters()
    update_css_and_js()
    update_sitemap()
    update_readme_and_changelog()

if __name__ == '__main__':
    main()
