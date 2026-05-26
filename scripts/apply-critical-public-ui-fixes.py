#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
ASSETS = SITE / "assets"
ASSETS.mkdir(parents=True, exist_ok=True)

CSS_PATH = ASSETS / "bpi-critical-public-ui-fixes.css"
JS_PATH = ASSETS / "bpi-critical-public-ui-fixes.js"
STYLES = SITE / "styles.css"

CSS = r'''/* V108 — critical public UI fixes loaded after page inline styles.
   Fixes mobile nav overflow without changing the visual language. */
@media (max-width: 860px){
  html,body{width:100%!important;max-width:100%!important;overflow-x:hidden!important;}
  body.public-page .site-header,
  body.public-page header.site-header,
  .site-header{
    width:100%!important;
    max-width:100vw!important;
    box-sizing:border-box!important;
    overflow:hidden!important;
    padding-left:8px!important;
    padding-right:8px!important;
  }
  .site-header .site-brand,
  .site-header .language-switch{
    max-width:100%!important;
    min-width:0!important;
    box-sizing:border-box!important;
  }
  .site-header .site-nav,
  nav.site-nav{
    display:flex!important;
    flex-wrap:nowrap!important;
    width:100%!important;
    max-width:100%!important;
    min-width:0!important;
    box-sizing:border-box!important;
    overflow-x:auto!important;
    overflow-y:hidden!important;
    gap:.32rem!important;
    padding:.25rem .12rem .38rem!important;
    margin:0!important;
    -webkit-overflow-scrolling:touch!important;
    scrollbar-width:none!important;
    overscroll-behavior-x:contain!important;
    scroll-snap-type:x proximity!important;
  }
  .site-header .site-nav::-webkit-scrollbar,
  nav.site-nav::-webkit-scrollbar{display:none!important;}
  .site-header .site-nav a,
  nav.site-nav a,
  .site-header .site-nav a.active,
  nav.site-nav a.active,
  .site-header .site-nav a[aria-current="page"],
  nav.site-nav a[aria-current="page"]{
    flex:0 0 auto!important;
    min-width:0!important;
    max-width:78vw!important;
    box-sizing:border-box!important;
    white-space:nowrap!important;
    overflow:hidden!important;
    text-overflow:ellipsis!important;
    transform:none!important;
    margin:0!important;
    scroll-snap-align:center!important;
  }
  .site-header .site-nav a.active,
  nav.site-nav a.active,
  .site-header .site-nav a[aria-current="page"],
  nav.site-nav a[aria-current="page"]{
    position:relative!important;
    z-index:1!important;
  }
}
@media (max-width:480px){
  .site-header .site-nav a,
  nav.site-nav a,
  .site-header .site-nav a.active,
  nav.site-nav a.active,
  .site-header .site-nav a[aria-current="page"],
  nav.site-nav a[aria-current="page"]{
    max-width:72vw!important;
    padding-inline:.66rem!important;
    font-size:.94rem!important;
  }
}
'''

JS = r'''/* V108 — critical public UI runtime fixes.
   1. Keeps selected mobile nav visible instead of resetting the rail.
   2. Makes Files filtering include all files, including the philosophical theory.
   3. Converts feedback/Gmail links/buttons into native mailto links with subject/body.
*/
(function(){
  'use strict';
  var KNOWN_FORMATS = ['html','pdf','docx','md','markdown','word','doc','txt','text'];
  var lastFormat = '';
  var navKey = 'bpi:last-nav-href';

  function he(){return document.documentElement.lang==='he'||document.documentElement.dir==='rtl'||document.body.classList.contains('public-page-he');}
  function enc(v){return encodeURIComponent(v).replace(/%20/g,'%20');}
  function feedbackHref(){
    var subject = he() ? 'ביקורת על Between Potential and Ideal' : 'Feedback on Between Potential and Ideal';
    var body = he()
      ? ['שלום ברק,','','קראתי את הפרויקט Between Potential and Ideal ויש לי ביקורת / הערה:','','','העמוד שבו הייתי:',location.href,'','הערה:'].join('\n')
      : ['Hi Barak,','','I read Between Potential and Ideal and have feedback / a note:','','','Page I was on:',location.href,'','Feedback:'].join('\n');
    return 'mailto:barakbenhur@gmail.com?subject='+enc(subject)+'&body='+enc(body);
  }

  function isFeedbackElement(el){
    if(!el) return false;
    var href = ((el.getAttribute && el.getAttribute('href')) || '').toLowerCase();
    var text = (el.textContent || '').trim().toLowerCase();
    var aria = ((el.getAttribute && el.getAttribute('aria-label')) || '').toLowerCase();
    var title = ((el.getAttribute && el.getAttribute('title')) || '').toLowerCase();
    return href.includes('mail.google.com') || href.includes('gmail.com/mail') ||
      text.includes('שלח ביקורת') || aria.includes('שלח ביקורת') || title.includes('שלח ביקורת') ||
      text.includes('send feedback') || aria.includes('send feedback') || title.includes('send feedback') ||
      text.includes('feedback') && (href.includes('gmail') || href.startsWith('mailto:'));
  }

  function patchFeedback(){
    document.querySelectorAll('a[href],button,[role="button"]').forEach(function(el){
      if(!isFeedbackElement(el)) return;
      if(el.tagName && el.tagName.toLowerCase()==='a'){
        el.href = feedbackHref();
        el.removeAttribute('target');
        el.removeAttribute('rel');
      }
      el.setAttribute('data-bpi-feedback-fixed','true');
    });
  }

  document.addEventListener('click',function(e){
    var el = e.target && e.target.closest ? e.target.closest('a[href],button,[role="button"]') : null;
    if(!isFeedbackElement(el)) return;
    e.preventDefault();
    e.stopPropagation();
    window.location.href = feedbackHref();
  },true);

  function navAbs(a){try{return new URL(a.getAttribute('href'),location.href).pathname.replace(/\/+$/,'');}catch(e){return '';}}
  function centerNav(){
    document.querySelectorAll('.site-nav').forEach(function(nav){
      var active = nav.querySelector('a[aria-current="page"],a.active');
      var saved = ''; try{saved=sessionStorage.getItem(navKey)||'';}catch(e){}
      if(!active && saved){active = Array.from(nav.querySelectorAll('a[href]')).find(function(a){return navAbs(a)===saved;});}
      if(!active) active = Array.from(nav.querySelectorAll('a[href]')).find(function(a){return navAbs(a)===location.pathname.replace(/\/+$/,'');});
      if(!active || nav.scrollWidth <= nav.clientWidth+2) return;
      try{active.scrollIntoView({block:'nearest',inline:'center',behavior:'auto'});}catch(e){
        nav.scrollLeft = Math.max(0,active.offsetLeft-(nav.clientWidth-active.offsetWidth)/2);
      }
    });
  }

  document.addEventListener('click',function(e){
    var a = e.target && e.target.closest ? e.target.closest('.site-nav a[href]') : null;
    if(!a) return;
    try{sessionStorage.setItem(navKey,navAbs(a)||a.getAttribute('href')||'');}catch(err){}
    setTimeout(centerNav,0);
  },true);
  window.addEventListener('pageshow',function(){setTimeout(centerNav,0);setTimeout(centerNav,120);});
  window.addEventListener('load',function(){setTimeout(centerNav,80);setTimeout(centerNav,260);});
  window.addEventListener('resize',function(){setTimeout(centerNav,120);});

  function filesPage(){var p=location.pathname.toLowerCase();return p.endsWith('/files.html')||p.endsWith('/files-en.html')||!!document.querySelector('#fileSearch,#fileTypeFilter,.download-table');}
  function normFormat(v){v=(v||'').toLowerCase().trim(); if(v==='word')return 'docx'; if(v==='markdown')return 'md'; if(v==='text')return 'txt'; return v;}
  function fmtFromHref(h){var m=(h||'').split('?')[0].split('#')[0].toLowerCase().match(/\.([a-z0-9]+)$/);return m?normFormat(m[1]):'';}
  function rowText(row){return (row.textContent||'').toLowerCase()+' '+Array.from(row.querySelectorAll('a[href]')).map(function(a){return a.getAttribute('href')||'';}).join(' ').toLowerCase();}
  function rowFormats(row){
    var set = new Set();
    Array.from(row.querySelectorAll('a[href]')).forEach(function(a){var f=fmtFromHref(a.getAttribute('href')); if(f)set.add(f);});
    (row.getAttribute('data-format')||'').split(/[\s,|/]+/).forEach(function(f){f=normFormat(f);if(f)set.add(f);});
    var t=rowText(row);
    if(t.includes('pdf'))set.add('pdf'); if(t.includes('html'))set.add('html'); if(t.includes('docx')||t.includes('word'))set.add('docx'); if(t.includes('markdown')||t.includes('.md'))set.add('md'); if(t.includes('text')||t.includes('.txt'))set.add('txt');
    if(t.includes('התאוריה הפילוסופית')||t.includes('התיאוריה הפילוסופית')||t.includes('philosophical theory')||t.includes('between-potential-and-ideal-he')||t.includes('between-potential-and-ideal-en')) ['html','pdf','docx','md'].forEach(function(f){set.add(f);});
    return set;
  }
  function normalizeFiles(){
    if(!filesPage())return;
    var rows=Array.from(document.querySelectorAll('.download-table tr')).slice(1);
    rows.forEach(function(row){
      var formats=Array.from(rowFormats(row));
      if(formats.length){row.setAttribute('data-format',formats.join(' ')); row.setAttribute('data-formats',formats.join(' '));}
    });
    applyFilter();
  }
  function applyFilter(){
    if(!filesPage())return;
    var qEl=document.querySelector('#fileSearch');
    var typeEl=document.querySelector('#fileTypeFilter');
    var langEl=document.querySelector('#fileLangFilter');
    var q=(qEl&&qEl.value||'').toLowerCase().trim();
    var type=normFormat(typeEl&&typeEl.value||lastFormat||'');
    var lang=(langEl&&langEl.value||'').toLowerCase().trim();
    var visible=0;
    Array.from(document.querySelectorAll('.download-table tr')).forEach(function(row,i){
      if(i===0)return;
      var t=rowText(row);
      var formats=rowFormats(row);
      var okQ=!q||t.includes(q);
      var okType=!type||formats.has(type);
      var okLang=!lang||t.includes(lang);
      var ok=okQ&&okType&&okLang;
      row.style.display=ok?'':'none';
      if(ok)visible++;
    });
    var count=document.querySelector('#fileFilterCount');
    if(count) count.textContent = he() ? ('מוצגים '+visible+' קבצים') : (visible+' files shown');
  }
  document.addEventListener('input',function(e){if(e.target&&e.target.id==='fileSearch')applyFilter();},true);
  document.addEventListener('change',function(e){if(e.target&&e.target.id==='fileTypeFilter'){lastFormat=normFormat(e.target.value||'');applyFilter();} if(e.target&&e.target.id==='fileLangFilter')applyFilter();},true);

  function init(){patchFeedback();centerNav();normalizeFiles();setTimeout(function(){patchFeedback();centerNav();normalizeFiles();},120);}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();
'''

STYLE_IMPORT = '@import url("./assets/bpi-critical-public-ui-fixes.css?v=20260526-critical-v108");'
SCRIPT_TAG_ROOT = '<script src="assets/bpi-critical-public-ui-fixes.js?v=20260526-critical-v108" defer></script>'
SCRIPT_TAG_PAGES = '<script src="../../assets/bpi-critical-public-ui-fixes.js?v=20260526-critical-v108" defer></script>'

CSS_PATH.write_text(CSS, encoding='utf-8')
JS_PATH.write_text(JS, encoding='utf-8')

if STYLES.exists():
    text = STYLES.read_text(encoding='utf-8')
    if 'bpi-critical-public-ui-fixes.css' not in text:
        if not text.endswith('\n'):
            text += '\n'
        text += STYLE_IMPORT + '\n'
        STYLES.write_text(text, encoding='utf-8')

pages = [SITE / 'index.html', SITE / 'en.html'] + sorted((SITE / 'pages').glob('**/*.html'))
changed = []
for path in pages:
    if not path.exists():
        continue
    html = path.read_text(encoding='utf-8', errors='ignore')
    if 'bpi-critical-public-ui-fixes.js' in html:
        continue
    tag = SCRIPT_TAG_ROOT if path.parent == SITE else SCRIPT_TAG_PAGES
    if '</body>' in html:
        html = html.replace('</body>', tag + '\n</body>', 1)
    else:
        html += '\n' + tag + '\n'
    path.write_text(html, encoding='utf-8')
    changed.append(str(path.relative_to(ROOT)))

print('Wrote:', CSS_PATH.relative_to(ROOT), JS_PATH.relative_to(ROOT))
print('Injected script into', len(changed), 'HTML files')
for item in changed:
    print('-', item)
