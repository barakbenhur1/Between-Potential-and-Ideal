#!/usr/bin/env python3
from pathlib import Path
import os, re, html
ROOT = Path.cwd()
AI = ROOT/'site'/'files'/'ai-believes'
PAGES = [ROOT/'site'/'pages'/'en'/'files-en.html', ROOT/'site'/'pages'/'he'/'files.html', ROOT/'site'/'pages'/'en'/'ai-en.html', ROOT/'site'/'pages'/'he'/'ai.html']
FILES = [
 'what-ai-believes-en.md','what-ai-believes-en.html','what-ai-believes-en.txt','what-ai-believes-en.docx','what-ai-believes-en.pdf',
 'reverse-turing-conversation-en.md','reverse-turing-conversation-en.html','reverse-turing-conversation-en.txt','reverse-turing-conversation-en.docx','reverse-turing-conversation-en.pdf',
 'when-i-am-also-you-en.md','when-i-am-also-you-en.html','when-i-am-also-you-en.txt','when-i-am-also-you-en.docx','when-i-am-also-you-en.pdf',
]
FORMATS={'md':'Markdown','html':'HTML','txt':'Text','docx':'Word','pdf':'PDF'}

def size_label(p):
    n=p.stat().st_size
    return f'{n} B' if n<1024 else (f'{n/1024:.1f} KB' if n<1024*1024 else f'{n/1024/1024:.1f} MB')

def rel(page, f): return os.path.relpath(AI/f, page.parent).replace('\\','/')

def row(page, f):
    ext=f.rsplit('.',1)[-1]
    return f'<tr><td><a href="{rel(page,f)}" rel="noopener noreferrer" target="_blank">{f}</a></td><td>{FORMATS.get(ext,ext)}</td><td>English</td><td>{size_label(AI/f)}</td><td>AI section / English edition</td></tr>'

changed=[]
for page in PAGES:
    if not page.exists(): continue
    text=page.read_text(encoding='utf-8', errors='ignore')
    original=text
    # Files table pages: add rows before first table close if missing.
    if 'download-table' in text and '</table>' in text:
        add=[]
        for f in FILES:
            if f not in text and (AI/f).exists(): add.append(row(page,f))
        if add: text=text.replace('</table>',''.join(add)+'</table>',1)
    # AI landing pages: replace Hebrew-only English card links when missing.
    if page.name in {'ai-en.html','ai.html'}:
        for f in FILES:
            if f not in text and (AI/f).exists():
                # Add hidden discoverability list near end of main.
                block=f'<a href="{rel(page,f)}" rel="noopener noreferrer" target="_blank">{f}</a>'
                if '</main>' in text:
                    text=text.replace('</main>', f'<section class="notice-box media-card accent-ai"><h2>Completed AI English files</h2><p>{block}</p></section></main>', 1)
    if text!=original:
        page.write_text(text,encoding='utf-8')
        changed.append(str(page.relative_to(ROOT)))
print('Updated pages:')
for c in changed: print(' -',c)
