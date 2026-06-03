(function(){
  'use strict';

  var AI_WITNESS_HE = 'בינה מלאכותית כעדות';
  var AI_WITNESS_EN = 'AI as Witness';

  var HE_ITEMS = [
    ['בית','index.html','index'],
    ['תקציר','summary.html','summary'],
    ['מילון','glossary.html','glossary'],
    ['מושגים','potential-ideal-optimal.html','potential-ideal-optimal'],
    [AI_WITNESS_HE,'ai-as-witness.html','ai-as-witness'],
    ['ליבה','core.html','core'],
    ['מתודולוגיה','methodology.html','methodology'],
    ['עדות','witness.html','witness'],
    ['יישום','applied.html','applied'],
    ['בינה מלאכותית','ai.html','ai'],
    ['קבצים','files.html','files'],
    ['ביקורת','critique.html','critique'],
    ['מקורות','sources.html','sources']
  ];

  var EN_ITEMS = [
    ['Home','en.html','en'],
    ['Summary','summary-en.html','summary-en'],
    ['Glossary','glossary-en.html','glossary-en'],
    ['Concepts','potential-ideal-optimal-en.html','potential-ideal-optimal-en'],
    [AI_WITNESS_EN,'ai-as-witness-en.html','ai-as-witness-en'],
    ['Core','core-en.html','core-en'],
    ['Methodology','methodology-en.html','methodology-en'],
    ['Witness','witness-en.html','witness-en'],
    ['Application','applied-en.html','applied-en'],
    ['AI','ai-en.html','ai-en'],
    ['Files','files-en.html','files-en'],
    ['Critique','critique-en.html','critique-en'],
    ['Sources','sources-en.html','sources-en']
  ];

  var HE_TO_EN = {
    'index':'en.html','summary':'summary-en.html','glossary':'glossary-en.html',
    'potential-ideal-optimal':'potential-ideal-optimal-en.html','ai-as-witness':'ai-as-witness-en.html',
    'core':'core-en.html','methodology':'methodology-en.html','witness':'witness-en.html',
    'applied':'applied-en.html','ai':'ai-en.html','files':'files-en.html',
    'critique':'critique-en.html','sources':'sources-en.html'
  };
  var EN_TO_HE = {
    'en':'index.html','summary-en':'summary.html','glossary-en':'glossary.html',
    'potential-ideal-optimal-en':'potential-ideal-optimal.html','ai-as-witness-en':'ai-as-witness.html',
    'core-en':'core.html','methodology-en':'methodology.html','witness-en':'witness.html',
    'applied-en':'applied.html','ai-en':'ai.html','files-en':'files.html',
    'critique-en':'critique.html','sources-en':'sources.html'
  };

  function pathName(){ return window.location.pathname || ''; }
  function fileName(){
    var clean = pathName().split('?')[0].split('#')[0];
    var name = clean.substring(clean.lastIndexOf('/') + 1);
    if (!name) return isHebrew() ? 'index.html' : 'en.html';
    return name;
  }
  function isInner(){ return /\/pages\/(he|en)\//.test(pathName()); }
  function isHebrew(){
    var p = pathName().toLowerCase();
    if (p.indexOf('/pages/en/') !== -1 || /\/en\.html$/.test(p)) return false;
    if (p.indexOf('/pages/he/') !== -1 || /\/index\.html$/.test(p) || p === '/' || p.endsWith('/site/')) return true;
    return document.documentElement.lang === 'he' || document.documentElement.dir === 'rtl' || document.body.classList.contains('public-page-he');
  }
  function key(){
    var f = fileName().replace(/\.html$/,'');
    if (!f) return isHebrew() ? 'index' : 'en';
    if (f === 'index') return 'index';
    return f;
  }
  function homeHref(){ return isInner() ? (isHebrew() ? '../../index.html' : '../../en.html') : (isHebrew() ? 'index.html' : 'en.html'); }
  function pageHref(file){
    if (isInner()) return file === 'index.html' ? '../../index.html' : file === 'en.html' ? '../../en.html' : file;
    return isHebrew() ? (file === 'index.html' ? 'index.html' : 'pages/he/' + file) : (file === 'en.html' ? 'en.html' : 'pages/en/' + file);
  }
  function langHref(){
    var k = key();
    if (isHebrew()) {
      var en = HE_TO_EN[k] || 'en.html';
      return isInner() ? '../en/' + en : en;
    }
    var he = EN_TO_HE[k] || 'index.html';
    return isInner() ? '../he/' + he : he;
  }
  function escapeText(s){
    return String(s).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];});
  }
  function navHtml(items, activeKey){
    return items.map(function(item){
      var active = item[2] === activeKey;
      return '<a' + (active ? ' aria-current="page" class="active"' : '') + ' href="' + pageHref(item[1]) + '">' + escapeText(item[0]) + '</a>';
    }).join('');
  }

  function normalizeDuplicatedLabels(){
    Array.from(document.querySelectorAll('.site-header .site-nav a')).forEach(function(a){
      var href = (a.getAttribute('href') || '').toLowerCase();
      var text = (a.textContent || '').replace(/\s+/g, ' ').trim();
      if (href.indexOf('ai-as-witness') !== -1) {
        a.textContent = isHebrew() ? AI_WITNESS_HE : AI_WITNESS_EN;
      } else if (text.indexOf(AI_WITNESS_HE + AI_WITNESS_HE) !== -1) {
        a.textContent = text.replace(AI_WITNESS_HE + AI_WITNESS_HE, AI_WITNESS_HE);
      } else if (text.indexOf(AI_WITNESS_EN + AI_WITNESS_EN) !== -1) {
        a.textContent = text.replace(AI_WITNESS_EN + AI_WITNESS_EN, AI_WITNESS_EN);
      }
    });
  }

  function installNoPseudoNavRule(){
    if (document.getElementById('bpi-no-duplicated-nav-pseudo')) return;
    var style = document.createElement('style');
    style.id = 'bpi-no-duplicated-nav-pseudo';
    style.textContent = '.site-header .site-nav a::before,.site-header .site-nav a::after{content:none!important;display:none!important;}';
    document.head.appendChild(style);
  }

  function renderSharedHeader(){
    var header = document.querySelector('.site-header');
    if (!header) return;
    var he = isHebrew();
    var items = he ? HE_ITEMS : EN_ITEMS;
    var activeKey = key();
    header.setAttribute('dir', he ? 'rtl' : 'ltr');
    header.setAttribute('role', 'banner');
    header.classList.toggle('bpi-home-nav', activeKey === 'index' || activeKey === 'en');
    header.classList.add('bpi-shared-nav');
    header.innerHTML = '<div class="site-brand"><a href="' + homeHref() + '">Between Potential and Ideal</a></div>' +
      '<nav aria-label="Primary navigation" class="site-nav" role="navigation">' + navHtml(items, activeKey) + '</nav>' +
      '<a class="language-switch" href="' + langHref() + '" title="' + (he ? 'English version' : 'גרסה עברית') + '">' + (he ? 'English' : 'עברית') + '</a>';
    normalizeDuplicatedLabels();
    document.body.classList.add('bpi-shared-nav-ready');
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
  function init(){ installNoPseudoNavRule(); renderSharedHeader(); normalizeDuplicatedLabels(); normalizeFileTargets(); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
