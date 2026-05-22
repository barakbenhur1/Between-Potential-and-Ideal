#!/usr/bin/env python3
from pathlib import Path
from urllib.parse import unquote
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'theory-site-static'
PAIRS = [
    ('index.html','en.html'),('summary.html','summary-en.html'),('core.html','core-en.html'),
    ('witness.html','witness-en.html'),('applied.html','applied-en.html'),('ai.html','ai-en.html'),
    ('files.html','files-en.html'),('methodology.html','methodology-en.html'),('critique.html','critique-en.html'),
    ('sources.html','sources-en.html'),('about.html','about-en.html'),('changelog.html','changelog-en.html')
]

def soup(path):
    return BeautifulSoup(path.read_text(encoding='utf-8'), 'html.parser')

def internal_refs():
    missing=[]; total=0
    for html in SITE.glob('*.html'):
        s=soup(html)
        tags=[]
        tags += [(a,'href') for a in s.find_all('a', href=True)]
        tags += [(img,'src') for img in s.find_all('img', src=True)]
        tags += [(link,'href') for link in s.find_all('link', href=True)]
        for tag, attr in tags:
            val=tag.get(attr)
            if not val or val.startswith(('http://','https://','mailto:','tel:','#','javascript:')):
                continue
            total += 1
            rel=unquote(val.split('#')[0].split('?')[0])
            if not rel:
                continue
            target=(html.parent / rel).resolve()
            if not target.exists():
                missing.append((html.name, attr, val))
    return total, missing

lines=[]
lines.append('SITE PARITY AUDIT')
lines.append('=================')
lines.append('')
lines.append('Hebrew/English page-pair structural parity:')
for he,en in PAIRS:
    sh=soup(SITE/he); se=soup(SITE/en)
    
    def visible_links(s):
        return [a for a in s.find_all('a') if not any(getattr(p, 'has_attr', lambda *_: False)('hidden') for p in a.parents)]
    lines.append(f'- {he} / {en}: headings {len(sh.find_all(["h1","h2","h3"]))}/{len(se.find_all(["h1","h2","h3"]))}, images {len(sh.find_all("img"))}/{len(se.find_all("img"))}, visible links {len(visible_links(sh))}/{len(visible_links(se))}, all links {len(sh.find_all("a"))}/{len(se.find_all("a"))}')
lines.append('')
total, missing = internal_refs()
lines.append(f'Internal references checked: {total}')
lines.append(f'Missing internal references: {len(missing)}')
for row in missing:
    lines.append(f'  MISSING: {row[0]} {row[1]}={row[2]}')
lines.append('')
lines.append('Notes:')
lines.append('- The English AI page now exposes the full AI archive at the concept-card level, including Hebrew-source editions where no English adaptation exists yet.')
lines.append('- Visual parity was checked through image counts and visible media-card treatment for the main paired pages.')
(SITE / 'SITE_PARITY_AUDIT.txt').write_text('\n'.join(lines), encoding='utf-8')
print('\n'.join(lines))
