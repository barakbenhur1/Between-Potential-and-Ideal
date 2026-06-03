/* V125 — deterministic global nav order + header/language normalization + lightweight file helpers.
   Fixes: language switch labels, active nav state for generated links, and consistent premium header color. */
(function(){
  'use strict';

  var KNOWN_FORMATS = ['html','pdf','docx','md','txt'];

  function isHe(){
    return document.documentElement.lang === 'he' ||
      document.documentElement.dir === 'rtl' ||
      document.body.classList.contains('public-page-he');
  }

  function inPageFolder(){
    var path = (location.pathname || '').toLowerCase();
    return path.indexOf('/pages/he/') !== -1 || path.indexOf('/pages/en/') !== -1 ||
      path.indexOf('/site/pages/he/') !== -1 || path.indexOf('/site/pages/en/') !== -1;
  }

  function pageHref(fileName){
    if (inPageFolder()) return './' + fileName;
    return isHe() ? 'pages/he/' + fileName : 'pages/en/' + fileName;
  }

  function homeHref(){
    if (inPageFolder()) return isHe() ? '../../index.html' : '../../en.html';
    return isHe() ? 'index.html' : 'en.html';
  }

  function cleanHref(a){
    return (a && a.getAttribute('href') || '').split('?')[0].split('#')[0].toLowerCase();
  }

  function currentFileName(){
    var path = (location.pathname || '').split('?')[0].split('#')[0].toLowerCase();
    var last = path.substring(path.lastIndexOf('/') + 1);
    if (!last) return isHe() ? 'index.html' : 'en.html';
    return last;
  }

  function hrefMatchesFile(a, fileName){
    var href = cleanHref(a);
    if (!href || !fileName) return false;
    return href === fileName || href.endsWith('/' + fileName) || href.endsWith('./' + fileName) || href.endsWith(fileName);
  }

  function findLink(nav, endings){
    endings = Array.isArray(endings) ? endings : [endings];
    return Array.from(nav.querySelectorAll('a[href]')).find(function(a){
      var href = cleanHref(a);
      return endings.some(function(ending){
        return href === ending || href.endsWith('/' + ending) || href.endsWith(ending);
      });
    }) || null;
  }

  function getOrCreate(nav, spec){
    var link = findLink(nav, spec.endings);
    if (!link) {
      link = document.createElement('a');
      link.href = spec.href;
    }
    link.textContent = spec.label;
    link.style.setProperty('order', '0', 'important');
    link.style.setProperty('-webkit-order', '0', 'important');
    return link;
  }

  function installHeaderPolish(){
    if (document.getElementById('bpi-global-header-polish-v125')) return;
    var style = document.createElement('style');
    style.id = 'bpi-global-header-polish-v125';
    style.textContent = [
      '.site-header{display:grid!important;grid-template-columns:minmax(max-content,1fr) minmax(0,auto) minmax(90px,1fr)!important;align-items:center!important;column-gap:16px!important;background:linear-gradient(90deg,#0A3A68 0%,#0b5b72 46%,#77795f 76%,#f29a38 100%)!important;border-bottom:1px solid rgba(255,255,255,.14)!important;box-shadow:0 10px 28px rgba(7,16,29,.18)!important}',
      '.site-header .site-brand{justify-self:start!important;min-width:max-content!important;white-space:nowrap!important}',
      '.site-header .site-brand a{white-space:nowrap!important;display:inline-block!important}',
      '.site-header .language-switch{justify-self:end!important;white-space:nowrap!important}',
      '.site-header .site-nav{display:flex!important;flex-wrap:wrap!important;justify-content:center!important;align-items:center!important;text-align:center!important;justify-self:center!important;margin-left:auto!important;margin-right:auto!important;max-width:min(100%,1180px)!important}',
      '.site-header .site-nav a{text-align:center!important;order:0!important;-webkit-order:0!important}',
      '.site-header .site-nav a.active,.site-header .site-nav a[aria-current="page"]{color:#07101d!important;background:linear-gradient(135deg,#b98726,#e6b84a,#f5d06b)!important;border-color:rgba(255,255,255,.28)!important;box-shadow:0 0 30px rgba(230,184,74,.20),0 0 86px rgba(124,58,237,.13)!important}',
      '@media(max-width:860px){.site-header{display:flex!important;flex-direction:column!important}.site-header .site-brand,.site-header .language-switch,.site-header .site-nav{justify-self:center!important;min-width:0!important}.site-header .site-brand a{white-space:normal!important;text-align:center!important}}'
    ].join('');
    document.head.appendChild(style);
  }

  function navSpecs(){
    return isHe() ? [
      { label:'בית', href:homeHref(), endings:['index.html'] },
      { label:'תקציר', href:pageHref('summary.html'), endings:['summary.html'] },
      { label:'מילון', href:pageHref('glossary.html'), endings:['glossary.html'] },
      { label:'מושגים', href:pageHref('potential-ideal-optimal.html'), endings:['potential-ideal-optimal.html'] },
      { label:'בינה מלאכותית כעדות', href:pageHref('ai-as-witness.html'), endings:['ai-as-witness.html'] },
      { label:'מתודולוגיה', href:pageHref('methodology.html'), endings:['methodology.html'] },
      { label:'ליבה', href:pageHref('core.html'), endings:['core.html'] },
      { label:'עדות', href:pageHref('witness.html'), endings:['witness.html'] },
      { label:'יישום', href:pageHref('applied.html'), endings:['applied.html'] },
      { label:'בינה מלאכותית', href:pageHref('ai.html'), endings:['ai.html'] },
      { label:'קבצים', href:pageHref('files.html'), endings:['files.html'] },
      { label:'ביקורת', href:pageHref('critique.html'), endings:['critique.html'] },
      { label:'מקורות', href:pageHref('sources.html'), endings:['sources.html'] }
    ] : [
      { label:'Home', href:homeHref(), endings:['en.html'] },
      { label:'Summary', href:pageHref('summary-en.html'), endings:['summary-en.html'] },
      { label:'Glossary', href:pageHref('glossary-en.html'), endings:['glossary-en.html'] },
      { label:'Concepts', href:pageHref('potential-ideal-optimal-en.html'), endings:['potential-ideal-optimal-en.html'] },
      { label:'AI as Witness', href:pageHref('ai-as-witness-en.html'), endings:['ai-as-witness-en.html'] },
      { label:'Methodology', href:pageHref('methodology-en.html'), endings:['methodology-en.html'] },
      { label:'Core', href:pageHref('core-en.html'), endings:['core-en.html'] },
      { label:'Witness', href:pageHref('witness-en.html'), endings:['witness-en.html'] },
      { label:'Application', href:pageHref('applied-en.html'), endings:['applied-en.html'] },
      { label:'AI', href:pageHref('ai-en.html'), endings:['ai-en.html'] },
      { label:'Files', href:pageHref('files-en.html'), endings:['files-en.html'] },
      { label:'Critique', href:pageHref('critique-en.html'), endings:['critique-en.html'] },
      { label:'Sources', href:pageHref('sources-en.html'), endings:['sources-en.html'] }
    ];
  }

  function setActiveNav(nav){
    var fileName = currentFileName();
    var links = Array.from(nav.querySelectorAll('a[href]'));
    links.forEach(function(a){
      a.classList.remove('active');
      a.removeAttribute('aria-current');
    });
    var active = links.find(function(a){ return hrefMatchesFile(a, fileName); });
    if (!active && fileName === 'index.html') active = findLink(nav, 'index.html');
    if (!active && fileName === 'en.html') active = findLink(nav, 'en.html');
    if (active) {
      active.classList.add('active');
      active.setAttribute('aria-current', 'page');
    }
  }

  function normalizeNavOrder(){
    var nav = document.querySelector('.site-header .site-nav');
    if (!nav) return;

    navSpecs().forEach(function(spec){
      nav.appendChild(getOrCreate(nav, spec));
    });
    setActiveNav(nav);
  }

  function normalizeLanguageSwitch(){
    var switcher = document.querySelector('.site-header .language-switch');
    if (!switcher) return;
    if (isHe()) {
      switcher.textContent = 'English';
      switcher.setAttribute('title', 'English version of this page');
      switcher.setAttribute('aria-label', 'Switch to the English version');
    } else {
      switcher.textContent = 'עברית';
      switcher.setAttribute('title', 'גרסה עברית של העמוד');
      switcher.setAttribute('aria-label', 'מעבר לגרסה העברית');
    }
  }

  function normalizeFormat(value){
    value = (value || '').toLowerCase().trim();
    if (value === 'word' || value === 'doc') return 'docx';
    if (value === 'markdown') return 'md';
    if (value === 'text') return 'txt';
    return value;
  }

  function fileFormatFromHref(href){
    var clean = (href || '').split('?')[0].split('#')[0].toLowerCase();
    var match = clean.match(/\.([a-z0-9]+)$/);
    if (!match) return '';
    var ext = normalizeFormat(match[1]);
    return KNOWN_FORMATS.indexOf(ext) !== -1 ? ext : '';
  }

  function normalizeFileTargets(){
    Array.from(document.querySelectorAll('a[href]')).forEach(function(a){
      var href = a.getAttribute('href') || '';
      var clean = href.split('?')[0].split('#')[0].toLowerCase();
      var archive = clean.indexOf('/files/') !== -1 || clean.indexOf('../../files/') === 0 || clean.indexOf('../files/') === 0 || clean.indexOf('files/') === 0;
      if (!archive || !fileFormatFromHref(href)) return;
      a.setAttribute('target', '_blank');
      var rel = (a.getAttribute('rel') || '').split(/\s+/).filter(Boolean);
      ['noopener','noreferrer'].forEach(function(token){ if (rel.indexOf(token) === -1) rel.push(token); });
      a.setAttribute('rel', rel.join(' '));
    });
  }

  function init(){
    installHeaderPolish();
    normalizeLanguageSwitch();
    normalizeNavOrder();
    normalizeFileTargets();
    window.setTimeout(function(){
      normalizeLanguageSwitch();
      normalizeNavOrder();
    }, 60);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
