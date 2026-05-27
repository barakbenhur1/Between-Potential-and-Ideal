#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import json, re, zipfile

ROOT=Path.cwd()
issues=[]
summary={}

def add(kind,path,msg): issues.append({"kind":kind,"path":str(path),"message":msg})

def check_text():
    glued=["ואידיאליכולים","אידיאליכולים","תהיהאידיאלית","ביצירהאידיאלי","אידיאליש","האידיאליכול","אידיאליכול","שהיהאידיאלי","שנעשהאידיאלי","נעשהאידיאלי"]
    count=0
    for p in list((ROOT/'site').rglob('*.md'))+list((ROOT/'site').rglob('*.txt')):
        try: t=p.read_text(encoding='utf-8')
        except Exception: continue
        count+=1
        for bad in glued:
            if bad in t: add('glued_hebrew',p,bad)
    summary['text_files_checked']=count

def check_editorial_en():
    base=ROOT/'site/files/editorial-tightened'
    for ext in ['html','md','txt','docx','pdf']:
        p=base/f'editorial-report-en.{ext}'
        if not p.exists(): add('missing_counterpart',p,'Missing English editorial report counterpart')

def check_docx():
    total=0; bad=0
    for p in (ROOT/'site').rglob('*.docx'):
        total+=1
        try:
            with zipfile.ZipFile(p) as z:
                if 'word/document.xml' not in z.namelist(): continue
                xml=z.read('word/document.xml').decode('utf-8',errors='ignore')
                for m in re.finditer(r'<wp:docPr\b([^>]*)/>',xml):
                    attrs=m.group(1)
                    if 'descr=' not in attrs:
                        bad+=1; add('docx_missing_alt',p,'wp:docPr without descr')
                        break
                if any(x in p.as_posix().lower() for x in ['between-potential','editorial-tightened','potential-extensions']):
                    if 'Short methodological clarification' not in xml and 'הבהרת מתודולוגיה קצרה' not in xml:
                        add('docx_missing_method_note',p,'Relevant DOCX missing methodological clarification')
        except Exception as e: add('docx_read_error',p,str(e))
    summary['docx_checked']=total; summary['docx_missing_alt_files']=bad

def check_pdf():
    try: import fitz
    except Exception as e:
        add('pdf_check_skipped','site',f'PyMuPDF unavailable: {e}'); return
    total=0
    for p in (ROOT/'site').rglob('*.pdf'):
        total+=1
        try:
            doc=fitz.open(p); meta=doc.metadata or {}; doc.close()
            if not meta.get('title'): add('pdf_missing_title',p,'PDF metadata title missing')
            if not meta.get('author'): add('pdf_missing_author',p,'PDF metadata author missing')
        except Exception as e: add('pdf_read_error',p,str(e))
    summary['pdf_checked']=total

def check_workflows():
    wf=ROOT/'.github/workflows'
    total=0
    if wf.exists():
        for p in wf.glob('*.yml'):
            total+=1
            t=p.read_text(encoding='utf-8',errors='ignore')
            if any(k in p.name for k in ['one-time','fix-','bpi-v86','bpi-v87','bpi-v88']) and re.search(r'\n  push:',t):
                add('workflow_push_still_enabled',p,'Regression-prone workflow still has push trigger')
    summary['workflows_checked']=total

def main():
    check_text(); check_editorial_en(); check_docx(); check_pdf(); check_workflows()
    result={'summary':summary,'issues':issues,'ok':not issues}
    print(json.dumps(result,ensure_ascii=False,indent=2))
    Path('BPI_EXPORTED_DOCUMENTS_QA_REPORT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    if issues: raise SystemExit(1)
if __name__=='__main__': main()
