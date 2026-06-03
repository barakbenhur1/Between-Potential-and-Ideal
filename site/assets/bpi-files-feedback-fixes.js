/* V126 — nav, language switch, file targets, and final polish loader. */
(function(){
  'use strict';

  function isHe(){
    return document.documentElement.lang === 'he' || document.documentElement.dir === 'rtl' || document.body.classList.contains('public-page-he');
  }

  function inPageFolder(){
    var p = location.pathname.toLowerCase();
    return p.indexOf('/pages/he/') !== -1 || p.indexOf('/pages/en/') !== -1 || p.indexOf('/site/pages/he/') !== -1 || p.indexOf('/site/pages/en/') !== -1;
  }

  function pageHref(file){
    if (inPageFolder()) return './' + file;
    return isHe() ? 'pages/he/' + file : 'pages/en/' + file;
  }

  function homeHref(){
    if (inPageFolder()) return isHe() ? '../../index.html' : '../../en.html';
    return isHe() ? 'index.html' : 'en.html';
  }

  function assetHref(file){
    return inPageFolder() ? '../../assets/' + file : 'assets/' + file;
  }

  function cleanHref(a){
    return (a && a.getAttribute('href') || '').split('?')[0].split('#')[0].toLowerCase();
  }

  function currentFile(){
    var p = location.pathname.split('?')[0].split('#')[0].toLowerCase();
    var f = p.substring(p.lastIndexOf('/') + 1);
    return f || (isHe() ? 'index.html' : 'en.html');
  }

  function findLink(nav, endings){
    endings = Array.isArray(endings) ? endings : [endings];
    return Array.from(nav.querySelectorAll('a[href]')).find(function(a){
      var h = cleanHref(a);
      return endings.some(function(e){ return h === e || h.endsWith('/' + e) || h.endsWith(e); });
    });
  }

  function ensureLink(nav, spec){
    var a = findLink(nav, spec.endings);
    if (!a) {
      a = document.createElement('a');
      a.href = spec.href;
    }
    a.textContent = spec.label;
    a.style.setProperty('order', '0', 'important');
    a.style.setProperty('-webkit-order', '0', 'important');
    nav.appendChild(a);
  }

  function specs(){
    return isHe() ? [
      ['בית', homeHref(), ['index.html']],
      ['תקציר', pageHref('summary.html'), ['summary.html']],
      ['מילון', pageHref('glossary.html'), ['glossary.html']],
      ['מושגים', pageHref('potential-ideal-optimal.html'), ['potential-ideal-optimal.html']],
      ['בינה מלאכותית כעדות', pageHref('ai-as-witness.html'), ['ai-as-witness.html']],
      ['מתודולוגיה', pageHref('methodology.html'), ['methodology.html']],
      ['ליבה', pageHref('core.html'), ['core.html']],
      ['עדות', pageHref('witness.html'), ['witness.html']],
      ['יישום', pageHref('applied.html'), ['applied.html']],
      ['בינה מלאכותית', pageHref('ai.html'), ['ai.html']],
      ['קבצים', pageHref('files.html'), ['files.html']],
      ['ביקורת', pageHref('critique.html'), ['critique.html']],
      ['מקורות', pageHref('sources.html'), ['sources.html']]
    ] : [
      ['Home', homeHref(), ['en.html']],
      ['Summary', pageHref('summary-en.html'), ['summary-en.html']],
      ['Glossary', pageHref('glossary-en.html'), ['glossary-en.html']],
      ['Concepts', pageHref('potential-ideal-optimal-en.html'), ['potential-ideal-optimal-en.html']],
      ['AI as Witness', pageHref('ai-as-witness-en.html'), ['ai-as-witness-en.html']],
      ['Methodology', pageHref('methodology-en.html'), ['methodology-en.html']],
      ['Core', pageHref('core-en.html'), ['core-en.html']],
      ['Witness', pageHref('witness-en.html'), ['witness-en.html']],
      ['Application', pageHref('applied-en.html'), ['applied-en.html']],
      ['AI', pageHref('ai-en.html'), ['ai-en.html']],
      ['Files', pageHref('files-en.html'), ['files-en.html']],
      ['Critique', pageHref('critique-en.html'), ['critique-en.html']],
      ['Sources', pageHref('sources-en.html'), ['sources-en.html']]
    ];
  }

  function loadPolish(){
    if (!document.getElementById('bpi-final-runtime-polish-v126')) {
      var l = document.createElement('link');
      l.id = 'bpi-final-runtime-polish-v126';
      l.rel = 'stylesheet';
      l.href = assetHref('bpi-final-runtime-polish.css?v=20260603-final-runtime-v126');
      document.head.appendChild(l);
    }
    if (!document.getElementById('bpi-global-header-polish-v126')) {
      var s = document.createElement('style');
      s.id = 'bpi-global-header-polish-v126';
      s.textContent = '.site-header{display:grid!important;grid-template-columns:minmax(max-content,1fr) minmax(0,auto) minmax(90px,1fr)!important;align-items:center!important;column-gap:16px!important;background:linear-gradient(90deg,#0A3A68 0%,#0b5b72 46%,#77795f 76%,#f29a38 100%)!important;border-bottom:1px solid rgba(255,255,255,.14)!important;box-shadow:0 10px 28px rgba(7,16,29,.18)!important}.site-header .site-brand{justify-self:start!important;min-width:max-content!important;white-space:nowrap!important}.site-header .site-brand a{white-space:nowrap!important;display:inline-block!important}.site-header .language-switch{justify-self:end!important;white-space:nowrap!important}.site-header .site-nav{display:flex!important;flex-wrap:wrap!important;justify-content:center!important;align-items:center!important;text-align:center!important;justify-self:center!important;margin-left:auto!important;margin-right:auto!important;max-width:min(100%,1180px)!important}.site-header .site-nav a{text-align:center!important;order:0!important;-webkit-order:0!important}.site-header .site-nav a.active,.site-header .site-nav a[aria-current="page"]{color:#07101d!important;background:linear-gradient(135deg,#b98726,#e6b84a,#f5d06b)!important;border-color:rgba(255,255,255,.28)!important;box-shadow:0 0 30px rgba(230,184,74,.20),0 0 86px rgba(124,58,237,.13)!important}@media(max-width:860px){.site-header{display:flex!important;flex-direction:column!important}.site-header .site-brand,.site-header .language-switch,.site-header .site-nav{justify-self:center!important;min-width:0!important}.site-header .site-brand a{white-space:normal!important;text-align:center!important}}';
      document.head.appendChild(s);
    }
  }

  function normalizeNav(){
    var nav = document.querySelector('.site-header .site-nav');
    if (!nav) return;
    specs().forEach(function(x){ ensureLink(nav, {label:x[0], href:x[1], endings:x[2]}); });
    var cur = currentFile();
    var links = Array.from(nav.querySelectorAll('a[href]'));
    links.forEach(function(a){ a.classList.remove('active'); a.removeAttribute('aria-current'); });
    var active = links.find(function(a){ var h = cleanHref(a); return h === cur || h.endsWith('/' + cur) || h.endsWith(cur); });
    if (active) { active.classList.add('active'); active.setAttribute('aria-current','page'); }
  }

  function normalizeLanguage(){
    var a = document.querySelector('.site-header .language-switch');
    if (!a) return;
    if (isHe()) { a.textContent = 'English'; a.setAttribute('title','English version of this page'); a.setAttribute('aria-label','Switch to the English version'); }
    else { a.textContent = 'עברית'; a.setAttribute('title','גרסה עברית של העמוד'); a.setAttribute('aria-label','מעבר לגרסה העברית'); }
  }

  function normalizeTargets(){
    Array.from(document.querySelectorAll('a[href]')).forEach(function(a){
      var h = cleanHref(a);
      if (h.indexOf('/files/') === -1 && h.indexOf('../../files/') !== 0 && h.indexOf('../files/') !== 0 && h.indexOf('files/') !== 0) return;
      if (!/\.(html|pdf|docx|md|txt)$/.test(h)) return;
      a.setAttribute('target','_blank');
      var rel = (a.getAttribute('rel') || '').split(/\s+/).filter(Boolean);
      ['noopener','noreferrer'].forEach(function(t){ if (rel.indexOf(t) === -1) rel.push(t); });
      a.setAttribute('rel', rel.join(' '));
    });
  }

  function init(){
    loadPolish();
    normalizeLanguage();
    normalizeNav();
    normalizeTargets();
    window.setTimeout(function(){ loadPolish(); normalizeLanguage(); normalizeNav(); }, 60);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
