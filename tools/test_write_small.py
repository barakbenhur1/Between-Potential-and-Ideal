from pathlib import Path
import html,re
from bs4 import BeautifulSoup
import a as D
ROOT=D.ROOT;SITE=D.SITE;BASE=D.BASE_URL
NAMES={'he':'עברית','en':'English','tlh':'tlhIngan Hol','qya':'Neo-Quenya'}
NAV=('summary','glossary','potential-ideal-optimal','ai-as-witness','methodology','core','witness','applied','ai','files','critique','sources')
def route(lang,slug=None):
 if slug is None:return '/index.html' if lang=='he' else f'/{lang}.html'
 if lang=='he':return f'/pages/he/{slug}.html'
 if lang=='en':return f'/pages/en/{slug}-en.html'
 return f'/pages/{lang}/{slug}.html'
def warning(lang):
 text=(SITE/f'{lang}.html').read_text(encoding='utf-8');m=re.search(r'<p class="warning">(.*?)</p>',text,re.S)
 return BeautifulSoup(m.group(1),'html.parser').get_text(' ',strip=True) if m else 'Public Beta — linguistic review ongoing.'
def review_url(lang):return f'https://github.com/barakbenhur1/Between-Potential-and-Ideal/issues/{11 if lang=="tlh" else 10}'
def menu(lang,slug=None):
 links=''.join(f'<a href="{route(code,slug)}" hreflang="{code}"'+(' aria-current="page"' if code==lang else '')+f'>{name}</a>' for code,name in NAMES.items())
 return f'<details class="bpi-language-menu"><summary aria-label="Language">{NAMES[lang]}</summary><div class="bpi-language-menu-panel">{links}</div></details>'
def alternates(slug=None):return ''.join(f'<link rel="alternate" hreflang="{code}" href="{BASE}{route(code,slug)}">' for code in NAMES)+f'<link rel="alternate" hreflang="x-default" href="{BASE}/en.html">'
def nav(lang,current,prefix):
 links=[f'<a href="{prefix}{lang}.html"'+(' class="active" aria-current="page"' if current is None else '')+f'>{NAMES[lang]}</a>']
 for slug in NAV:
  mark=' class="active" aria-current="page"' if slug==current else ''
  links.append(f'<a href="{prefix}pages/{lang}/{slug}.html"{mark}>{html.escape(D.title(lang,slug))}</a>')
 return ''.join(links)
def head(lang,title,slug,prefix,home=False):
 style=f'{prefix}styles-home-original.css?v=20260527-v430-non-home-repair' if home else f'{prefix}styles.css?v=20260604-tabbar-dimensions-v2'
 return f'<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)} - Between Potential and Ideal</title><meta name="description" content="{html.escape(title)} — {NAMES[lang]} Public Beta"><meta name="robots" content="index,follow"><link rel="canonical" href="{BASE}{route(lang,slug)}">{alternates(slug)}<link rel="stylesheet" href="{style}"><link rel="stylesheet" href="{prefix}styles.css?v=20260604-tabbar-dimensions-v2"><link rel="stylesheet" href="{prefix}assets/bpi-four-language-localization.css?v=20260612-full-site-v1"></head>'
def header(lang,current,prefix):return f'<a class="skip-link" href="#main">Skip to main content</a><header class="site-header"><div class="site-brand"><a href="{prefix}{lang}.html">Between Potential and Ideal</a></div><nav class="site-nav" aria-label="Primary navigation">{nav(lang,current,prefix)}</nav>{menu(lang,current)}</header>'
def note(lang):return f'<aside class="language-status-note"><strong>Public Beta</strong><p>{html.escape(warning(lang))}</p><a href="{review_url(lang)}">Independent linguistic review</a></aside>'
def downloads(lang,prefix):
 stem=f'between-potential-and-ideal-{lang}'
 return '<div class="download-row bpi-localized-download-grid">'+''.join(f'<a class="download-button" href="{prefix}files/{lang}/{stem}.{ext}">{ext.upper()}</a>' for ext in ('html','pdf','docx','md','txt'))+'</div>'
def write_home(lang):
 cards=''.join(f'<article class="hub-card media-card"><h2>{html.escape(D.title(lang,slug))}</h2><a class="card-link" href="pages/{lang}/{slug}.html">Open</a></article>' for slug in D.PAGES)
 title=D.title(lang,'summary')
 doc=f'<!doctype html><html lang="{lang}" dir="ltr">{head(lang,NAMES[lang],None,"",True)}<body class="public-page design-prompt-theme bpi-home-page">{header(lang,None,"")}<main class="site-main" id="main">{note(lang)}<section class="hero concise-hero"><p class="kicker">Between Potential and Ideal</p><h1>{html.escape(title)}</h1><p class="lead">{html.escape(warning(lang))}</p><img src="figures/homepage_hero_replacement_v43.png" alt="Between Potential and Ideal"></section><section class="notice-box media-card">{downloads(lang,"")}</section><section class="hub-grid three">{cards}</section></main><footer class="site-footer"><p>Between Potential and Ideal — {NAMES[lang]} Public Beta</p></footer></body></html>'
 (SITE/f'{lang}.html').write_text(doc,encoding='utf-8')
