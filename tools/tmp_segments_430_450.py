import html,re
import markdown
from bs4 import BeautifulSoup
import a as D
import test_write_small as S
SITE=D.SITE

def body_html(lang,slug):
 if slug=='files':return S.downloads(lang,'../../')
 if slug=='changelog':return '<h2>2026-06-12</h2><p>77 mapped sections, 34 public pages and five document formats.</p>'
 rendered=markdown.markdown(D.body(lang,slug),extensions=['extra','tables','fenced_code','sane_lists'],output_format='html5')
 rendered=re.sub(r'(?:\.\./)+figures/','../../figures/',rendered)
 rendered=re.sub(r'(?<![./])figures/','../../figures/',rendered)
 soup=BeautifulSoup(rendered,'html.parser')
 page_dir=SITE/'pages'/lang
 for image in soup.find_all('img'):
  src=(image.get('src') or '').split('#',1)[0].split('?',1)[0]
  if not src or src.startswith(('http://','https://','data:')):continue
  target=(SITE/src.lstrip('/')) if src.startswith('/') else (page_dir/src)
  if not target.exists():image['src']='../../figures/thumb_core.png'
 return str(soup)

def write_page(lang,slug):
 title=D.title(lang,slug)
 siblings=''.join(f'<a href="{other}.html">{html.escape(D.title(lang,other))}</a>' for other in D.PAGES if other!=slug)
 doc=f'<!doctype html><html lang="{lang}" dir="ltr">{S.head(lang,title,slug,"../../")}<body class="public-page design-prompt-theme section-{slug}">{S.header(lang,slug,"../../")}<main class="site-main" id="main"><nav class="breadcrumbs"><a href="../../{lang}.html">{S.NAMES[lang]}</a><span>›</span><span>{html.escape(title)}</span></nav>{S.note(lang)}<section class="page-title media-page-title"><div class="page-title-head"><img class="page-title-mark" src="../../figures/thumb_core.png" alt="{html.escape(title)}"><h1>{html.escape(title)}</h1></div></section><section class="reader-layout"><article class="reader-card long-read tone-card bpi-localized-content">{body_html(lang,slug)}</article></section><section class="reader-card"><div class="bpi-localized-link-grid">{siblings}</div></section></main><footer class="site-footer"><p>Between Potential and Ideal — {S.NAMES[lang]} Public Beta</p></footer></body></html>'
 path=SITE/'pages'/lang/f'{slug}.html';path.parent.mkdir(parents=True,exist_ok=True);path.write_text(doc,encoding='utf-8')

def write_pages(lang):
 S.write_home(lang)
 for slug in D.PAGES:write_page(lang,slug)
