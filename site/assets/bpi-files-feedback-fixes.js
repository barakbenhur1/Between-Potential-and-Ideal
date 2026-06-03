/* V132 — deterministic stable nav + language switch + file targets + final CSS loader.
   Single source of truth for public nav. Does not change page content. */
(function(){
  'use strict';

  function isHe(){
    return document.documentElement.lang === 'he' || document.documentElement.dir === 'rtl' || document.body.classList.contains('public-page-he');
  }

  function inPages(){
    var p = location.pathname.toLowerCase();
    return p.indexOf('/pages/he/') !== -1 || p.indexOf('/pages/en/') !== -1 || p.indexOf('/site/pages/he/') !== -1 || p.indexOf('/site/pages/en/') !== -1;
  }

  function page(file){ return inPages() ? './' + file : (isHe() ? 'pages/he/' + file : 'pages/en/' + file); }
  function home(){ return inPages() ? (isHe() ? '../../index.html' : '../../en.html') : (isHe() ? 'index.html' : 'en.html'); }
  function asset(file){ return inPages() ? '../../assets/' + file : 'assets/' + file; }

  function currentFile(){
    var p = location.pathname.split('?')[0].split('#')[0].toLowerCase();
    var f = p.substring(p.lastIndexOf('/') + 1);
    return f || (isHe() ? 'index.html' : 'en.html');
  }

  function navItems(){
    return isHe() ? [
      ['בית', home(), 'index.html'],
      ['תקציר', page('summary.html'), 'summary.html'],
      ['מילון', page('glossary.html'), 'glossary.html'],
      ['מושגים', page('potential-ideal-optimal.html'), 'potential-ideal-optimal.html'],
      ['בינה מלאכותית כעדות', page('ai-as-witness.html'), 'ai-as-witness.html'],
      ['ליבה', page('core.html'), 'core.html'],
      ['מתודולוגיה', page('methodology.html'), 'methodology.html'],
      ['עדות', page('witness.html'), 'witness.html'],
      ['יישום', page('applied.html'), 'applied.html'],
      ['בינה מלאכותית', page('ai.html'), 'ai.html'],
      ['קבצים', page('files.html'), 'files.html'],
      ['ביקורת', page('critique.html'), 'critique.html'],
      ['מקורות', page('sources.html'), 'sources.html']
    ] : [
      ['Home', home(), 'en.html'],
      ['Summary', page('summary-en.html'), 'summary-en.html'],
      ['Glossary', page('glossary-en.html'), 'glossary-en.html'],
      ['Concepts', page('potential-ideal-optimal-en.html'), 'potential-ideal-optimal-en.html'],
      ['AI as Witness', page('ai-as-witness-en.html'), 'ai-as-witness-en.html'],
      ['Core', page('core-en.html'), 'core-en.html'],
      ['Methodology', page('methodology-en.html'), 'methodology-en.html'],
      ['Witness', page('witness-en.html'), 'witness-en.html'],
      ['Application', page('applied-en.html'), 'applied-en.html'],
      ['AI', page('ai-en.html'), 'ai-en.html'],
      ['Files', page('files-en.html'), 'files-en.html'],
      ['Critique', page('critique-en.html'), 'critique-en.html'],
      ['Sources', page('sources-en.html'), 'sources-en.html']
    ];
  }

  function normalizeNav(){
    var nav = document.querySelector('.site-header .site-nav');
    if (!nav) return;
    var cur = currentFile();
    nav.textContent = '';
    navItems().forEach(function(item){
      var a = document.createElement('a');
      a.href = item[1];
      a.textContent = item[0];
      if (cur === item[2] || (cur === 'index.html' && item[2] === 'index.html') || (cur === 'en.html' && item[2] === 'en.html')) {
        a.className = 'active';
        a.setAttribute('aria-current', 'page');
      }
      nav.appendChild(a);
    });
    document.body.classList.add('bpi-nav-ready');
  }

  function counterpartFile(file){
    var heToEn = {
      'index.html':'en.html',
      'summary.html':'summary-en.html',
      'glossary.html':'glossary-en.html',
      'potential-ideal-optimal.html':'potential-ideal-optimal-en.html',
      'ai-as-witness.html':'ai-as-witness-en.html',
      'methodology.html':'methodology-en.html',
      'core.html':'core-en.html',
      'witness.html':'witness-en.html',
      'applied.html':'applied-en.html',
      'ai.html':'ai-en.html',
      'files.html':'files-en.html',
      'critique.html':'critique-en.html',
      'sources.html':'sources-en.html'
    };
    var enToHe = {};
    Object.keys(heToEn).forEach(function(k){ enToHe[heToEn[k]] = k; });
    return isHe() ? (heToEn[file] || 'en.html') : (enToHe[file] || 'index.html');
  }

  function counterpartHref(){
    var target = counterpartFile(currentFile());
    if (inPages()) return isHe() ? '../en/' + target : '../he/' + target;
    return target;
  }

  function normalizeLanguageSwitch(){
    var sw = document.querySelector('.site-header .language-switch');
    if (!sw) return;
    sw.textContent = isHe() ? 'English' : 'עברית';
    sw.setAttribute('href', counterpartHref());
    sw.setAttribute('aria-label', isHe() ? 'Switch to the English version' : 'מעבר לגרסה העברית');
    sw.setAttribute('title', isHe() ? 'English version' : 'גרסה עברית');
  }

  function cleanHref(a){ return (a && a.getAttribute('href') || '').split('?')[0].split('#')[0].toLowerCase(); }

  function normalizeFileTargets(){
    Array.from(document.querySelectorAll('a[href]')).forEach(function(a){
      var h = cleanHref(a);
      var isArchive = h.indexOf('/files/') !== -1 || h.indexOf('../../files/') === 0 || h.indexOf('../files/') === 0 || h.indexOf('files/') === 0;
      if (!isArchive || !/\.(html|pdf|docx|md|txt)$/.test(h)) return;
      a.setAttribute('target', '_blank');
      var rel = (a.getAttribute('rel') || '').split(/\s+/).filter(Boolean);
      ['noopener','noreferrer'].forEach(function(token){ if (rel.indexOf(token) === -1) rel.push(token); });
      a.setAttribute('rel', rel.join(' '));
    });
  }

  function loadFinalCss(){
    if (!document.getElementById('bpi-final-ai-buttons-fix-v132')) {
      var oldLink = document.createElement('link');
      oldLink.id = 'bpi-final-ai-buttons-fix-v132';
      oldLink.rel = 'stylesheet';
      oldLink.href = asset('bpi-final-ai-buttons-fix.css?v=20260603-v132');
      document.head.appendChild(oldLink);
    }
    if (!document.getElementById('bpi-nav-and-primary-final-v132')) {
      var link = document.createElement('link');
      link.id = 'bpi-nav-and-primary-final-v132';
      link.rel = 'stylesheet';
      link.href = asset('bpi-nav-and-primary-final-v131.css?v=20260603-v132-home-en');
      document.head.appendChild(link);
    }
  }

  function init(){
    normalizeNav();
    normalizeLanguageSwitch();
    normalizeFileTargets();
    loadFinalCss();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
