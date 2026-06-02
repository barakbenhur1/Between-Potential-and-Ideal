/* V124 — deterministic global nav order + lightweight file helpers.
   Fixes the gateway tab order by moving real DOM links instead of using CSS order hacks. */
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
    if (!link.hasAttribute('aria-current')) link.textContent = spec.label;
    link.style.setProperty('order', '0', 'important');
    link.style.setProperty('-webkit-order', '0', 'important');
    return link;
  }

  function installHeaderPolish(){
    if (document.getElementById('bpi-global-header-polish-v124')) return;
    var style = document.createElement('style');
    style.id = 'bpi-global-header-polish-v124';
    style.textContent = [
      '.site-header{display:grid!important;grid-template-columns:minmax(max-content,1fr) minmax(0,auto) minmax(90px,1fr)!important;align-items:center!important;column-gap:16px!important}',
      '.site-header .site-brand{justify-self:start!important;min-width:max-content!important;white-space:nowrap!important}',
      '.site-header .site-brand a{white-space:nowrap!important;display:inline-block!important}',
      '.site-header .language-switch{justify-self:end!important;white-space:nowrap!important}',
      '.site-header .site-nav{display:flex!important;flex-wrap:wrap!important;justify-content:center!important;align-items:center!important;text-align:center!important;justify-self:center!important;margin-left:auto!important;margin-right:auto!important;max-width:min(100%,1180px)!important}',
      '.site-header .site-nav a{text-align:center!important;order:0!important;-webkit-order:0!important}',
      '@media(max-width:860px){.site-header{display:flex!important;flex-direction:column!important}.site-header .site-brand,.site-header .language-switch,.site-header .site-nav{justify-self:center!important;min-width:0!important}.site-header .site-brand a{white-space:normal!important;text-align:center!important}}'
    ].join('');
    document.head.appendChild(style);
  }

  function normalizeNavOrder(){
    var nav = document.querySelector('.site-header .site-nav');
    if (!nav) return;

    var specs = isHe() ? [
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

    specs.forEach(function(spec){
      nav.appendChild(getOrCreate(nav, spec));
    });
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
    normalizeNavOrder();
    normalizeFileTargets();
    window.setTimeout(normalizeNavOrder, 60);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
