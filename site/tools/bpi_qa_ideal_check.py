#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
import re, json
try:
    from bs4 import BeautifulSoup
except Exception:
    print('Missing dependency: python3 -m pip install beautifulsoup4')
    raise

def root_from_cwd():
    cwd=Path.cwd().resolve()
    if (cwd/'site').exists(): return cwd
    if cwd.name=='site': return cwd.parent
    raise SystemExit('Run from repo root or site/')

def clean(s): return re.sub(r'\s+',' ',s or '').strip()
root=root_from_cwd(); site=root/'site'
res={'empty_alt':[], 'missing_local_images':[], 'bad_hash_targets':[], 'toc_sub_thumbs':[], 'scale_in_theory_docs':[], 'redirect_links':[], 'html_files':0}
for p in site.rglob('*.html'):
    res['html_files']+=1
    text=p.read_text(encoding='utf-8',errors='replace')
    soup=BeautifulSoup(text,'html.parser')
    ids={t.get('id') for t in soup.find_all(attrs={'id':True})}
    for a in soup.find_all('a',href=True):
        href=a['href']
        if href.startswith('#') and href[1:] not in ids:
            res['bad_hash_targets'].append([str(p.relative_to(root)),href,clean(a.get_text(' ',strip=True))])
        if 'redirect.html' in href:
            res['redirect_links'].append([str(p.relative_to(root)),href,clean(a.get_text(' ',strip=True))])
    for img in soup.find_all('img'):
        if not img.get('alt','').strip():
            res['empty_alt'].append([str(p.relative_to(root)),img.get('src','')])
        src=img.get('src','')
        if src and not src.startswith(('http:','https:','data:','mailto:','#')):
            src2=src.split('#')[0].split('?')[0]
            target=(p.parent/src2).resolve() if not src2.startswith('/') else (site/src2.lstrip('/')).resolve()
            if not target.exists():
                res['missing_local_images'].append([str(p.relative_to(root)),src])
    if p.name.startswith('between-potential-and-ideal') or 'editorial-tightened' in str(p):
        if 'scale(' in text:
            res['scale_in_theory_docs'].append(str(p.relative_to(root)))
        toc=soup.find(id='interactive-toc') or soup.find(class_='document-screen-toc')
        if toc and toc.select('li.toc-sub img.theory-toc-thumb, li.toc-sub .theory-toc-thumb-box'):
            res['toc_sub_thumbs'].append(str(p.relative_to(root)))
print(json.dumps(res, ensure_ascii=False, indent=2))
fail_keys=['empty_alt','missing_local_images','toc_sub_thumbs','scale_in_theory_docs']
if any(res[k] for k in fail_keys):
    raise SystemExit('QA FAILED: see JSON above')
print('QA OK for required image/accessibility checks. Review bad_hash_targets/redirect_links manually if listed.')
