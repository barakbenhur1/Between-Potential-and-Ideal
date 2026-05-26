/* V112 — Files filtering fixes + scoped Home mobile tab-bar fix.
   Feedback links are handled only by assets/bpi-fixes/bpi-feedback-desktop.js.
   This file is already loaded by the Home page, so it injects a mobile-only Home nav fix
   without changing the restored Home design/content. */
(function(){
  'use strict';

  var KNOWN_FORMATS = ['html','pdf','docx','md','txt'];
  var lastFormat = null;

  function isHe(){
    return document.documentElement.lang === 'he' ||
      document.documentElement.dir === 'rtl' ||
      document.body.classList.contains('public-page-he');
  }

  function isHomePage(){
    var path = (location.pathname || '').toLowerCase();
    return path === '/' || path.endsWith('/index.html') || path.endsWith('/en.html') ||
      path.endsWith('/site/index.html') || path.endsWith('/site/en.html');
  }

  function installHomeMobileTabBarFix(){
    if (!isHomePage() || document.getElementById('bpi-home-mobile-all-tabs-v112')) return;
    var style = document.createElement('style');
    style.id = 'bpi-home-mobile-all-tabs-v112';
    style.textContent = '' +
      '@media (max-width:860px){' +
      'body.public-page .site-header,body.public-page header.site-header,.site-header{' +
      'width:calc(100% - 16px)!important;max-width:100vw!important;min-width:0!important;height:auto!important;max-height:none!important;box-sizing:border-box!important;overflow:visible!important;overflow-x:visible!important;overflow-y:visible!important;' +
      '}' +
      'body.public-page .site-header .site-nav,.site-header .site-nav,nav.site-nav{' +
      'display:flex!important;flex-wrap:wrap!important;justify-content:center!important;align-items:center!important;width:100%!important;max-width:100%!important;min-width:0!important;height:auto!important;max-height:none!important;box-sizing:border-box!important;overflow:visible!important;overflow-x:visible!important;overflow-y:visible!important;white-space:normal!important;gap:.32rem!important;scrollbar-width:none!important;scroll-snap-type:none!important;' +
      '}' +
      'body.public-page .site-header .site-nav::-webkit-scrollbar,.site-header .site-nav::-webkit-scrollbar,nav.site-nav::-webkit-scrollbar{display:none!important;}' +
      'body.public-page .site-header .site-nav a,.site-header .site-nav a,nav.site-nav a{' +
      'display:inline-flex!important;flex:0 1 auto!important;min-width:0!important;max-width:calc(50vw - .7rem)!important;box-sizing:border-box!important;white-space:nowrap!important;overflow:hidden!important;text-overflow:ellipsis!important;transform:none!important;scroll-snap-align:none!important;' +
      '}' +
      '}' +
      '@media (max-width:480px){body.public-page .site-header .site-nav,.site-header .site-nav,nav.site-nav{gap:.24rem!important;}body.public-page .site-header .site-nav a,.site-header .site-nav a,nav.site-nav a{max-width:calc(50vw - .55rem)!important;}}' +
      '@media (max-width:360px){body.public-page .site-header .site-nav a,.site-header .site-nav a,nav.site-nav a{max-width:calc(100vw - 1rem)!important;}}';
    document.head.appendChild(style);
  }

  function isFilesPage(){
    var p = location.pathname.toLowerCase();
    return p.endsWith('/files.html') || p.endsWith('/files-en.html') ||
      document.body.classList.contains('files-page') ||
      !!document.querySelector('#fileSearch,#fileTypeFilter,#fileLangFilter,.download-table,.file-card,.download-card,.resource-card,[data-format],[data-formats]');
  }

  function normalizeFormat(value){
    value = (value || '').toLowerCase().trim();
    if (value === 'word' || value === 'doc') return 'docx';
    if (value === 'markdown') return 'md';
    if (value === 'text') return 'txt';
    return value;
  }

  function fmtFromHref(h){
    var clean = (h || '').split('?')[0].split('#')[0].toLowerCase();
    var m = clean.match(/\.([a-z0-9]+)$/);
    if (!m) return null;
    var e = normalizeFormat(m[1]);
    return KNOWN_FORMATS.indexOf(e) >= 0 ? e : null;
  }

  function cards(){
    return Array.from(document.querySelectorAll([
      '[data-format]','[data-formats]','[data-file-format]','[data-file-formats]',
      '.file-card','.file-item','.download-card','.download-item','.resource-card','.reader-card','.appendix-card',
      'article','li'
    ].join(','))).filter(function(el){
      return el && el.querySelector && el.querySelector('a[href]');
    });
  }

  function rows(){
    return Array.from(document.querySelectorAll('.download-table tr')).slice(1);
  }

  function formatsOf(el){
    var formats = new Set();
    [
      el.getAttribute('data-format'),
      el.getAttribute('data-formats'),
      el.getAttribute('data-file-format'),
      el.getAttribute('data-file-formats'),
      el.dataset && el.dataset.format,
      el.dataset && el.dataset.formats,
      el.dataset && el.dataset.fileFormat,
      el.dataset && el.dataset.fileFormats
    ].filter(Boolean).join(' ').split(/[\s,|/]+/).forEach(function(f){
      f = normalizeFormat(f);
      if (KNOWN_FORMATS.indexOf(f) >= 0) formats.add(f);
    });
    el.querySelectorAll('a[href]').forEach(function(a){
      var f = fmtFromHref(a.getAttribute('href'));
      if (f) formats.add(f);
    });
    var text = (el.textContent || '').toLowerCase();
    if (text.includes('pdf')) formats.add('pdf');
    if (text.includes('html')) formats.add('html');
    if (text.includes('word') || text.includes('docx')) formats.add('docx');
    if (text.includes('markdown')) formats.add('md');
    if (text.includes('text')) formats.add('txt');
    return formats;
  }

  function isPhilosophicalBlock(el){
    var text = (el.textContent || '').toLowerCase();
    var hrefs = Array.from(el.querySelectorAll('a[href]')).map(function(a){return a.getAttribute('href') || '';}).join(' ').toLowerCase();
    return text.includes('התאוריה הפילוסופית') || text.includes('התיאוריה הפילוסופית') ||
      text.includes('philosophical theory') || text.includes('between potential and ideal') ||
      hrefs.includes('between-potential-and-ideal-he') ||
      hrefs.includes('between-potential-and-ideal-en');
  }

  function setFormats(el){
    var formats = formatsOf(el);
    if (isPhilosophicalBlock(el)) {
      ['html','pdf','docx','md'].forEach(function(f){ formats.add(f); });
      if (el.dataset) {
        el.dataset.search = [
          el.dataset.search || '',
          'התאוריה הפילוסופית','התיאוריה הפילוסופית','בין פוטנציאל לאידיאל',
          'philosophical theory','between potential and ideal','html pdf docx md'
        ].join(' ');
      }
    }
    if (!formats.size) return formats;
    var value = Array.from(formats).sort().join(' ');
    el.setAttribute('data-format', value);
    el.setAttribute('data-formats', value);
    el.setAttribute('data-file-format', value);
    el.setAttribute('data-file-formats', value);
    el.setAttribute('data-filter-formats', value);
    KNOWN_FORMATS.forEach(function(f){ el.classList.toggle('format-' + f, formats.has(f)); });
    return formats;
  }

  function hasPhilosophical(){
    return cards().some(isPhilosophicalBlock) || rows().some(isPhilosophicalBlock);
  }

  function filesContainer(){
    return document.querySelector('.files-grid,.file-grid,.download-grid,.downloads-grid,[data-files-list]') || document.querySelector('main');
  }

  function basePrefix(){
    return location.pathname.includes('/site/pages/') || location.pathname.includes('/pages/') ? '../../files/' : 'files/';
  }

  function createPhilosophical(){
    var he = isHe();
    var base = basePrefix();
    var stem = he ? 'between-potential-and-ideal-he-editorial' : 'between-potential-and-ideal-en-editorial';
    var a = document.createElement('article');
    a.className = 'file-card download-card resource-card bpi-added-philosophical-theory-card format-html format-pdf format-docx format-md';
    a.setAttribute('data-format','docx html md pdf');
    a.setAttribute('data-formats','docx html md pdf');
    a.setAttribute('data-file-format','docx html md pdf');
    a.setAttribute('data-file-formats','docx html md pdf');
    a.setAttribute('data-search', he ?
      'התאוריה הפילוסופית התיאוריה הפילוסופית בין פוטנציאל לאידיאל html pdf docx md' :
      'philosophical theory between potential and ideal html pdf docx md'
    );
    a.innerHTML = he ?
      '<h3>התאוריה הפילוסופית</h3><p>המסמך המרכזי של Between Potential and Ideal בפורמטים מלאים.</p><div class="appendix-actions file-actions"><a class="primary-format" href="'+base+stem+'.html">HTML</a><a href="'+base+stem+'.pdf">PDF</a><a href="'+base+stem+'.docx">DOCX</a><a href="'+base+stem+'.md">MD</a></div>' :
      '<h3>Philosophical Theory</h3><p>The main Between Potential and Ideal document in full formats.</p><div class="appendix-actions file-actions"><a class="primary-format" href="'+base+stem+'.html">HTML</a><a href="'+base+stem+'.pdf">PDF</a><a href="'+base+stem+'.docx">DOCX</a><a href="'+base+stem+'.md">MD</a></div>';
    return a;
  }

  function currentFormatFromControl(el){
    if (!el) return null;
    var raw = [
      el.getAttribute && el.getAttribute('data-format'),
      el.getAttribute && el.getAttribute('data-filter'),
      el.getAttribute && el.getAttribute('data-value'),
      el.value,
      el.textContent
    ].filter(Boolean).join(' ').toLowerCase();
    for (var i=0;i<KNOWN_FORMATS.length;i++) if (normalizeFormat(raw).includes(KNOWN_FORMATS[i])) return KNOWN_FORMATS[i];
    if (raw.includes('all') || raw.includes('הכל') || raw.includes('כולם')) return null;
    return lastFormat;
  }

  function rememberFormatFromEvent(ev){
    var el = ev && ev.target && ev.target.closest ? ev.target.closest('button,a,input,select,[data-format],[data-filter],[data-value]') : null;
    var f = currentFormatFromControl(el);
    lastFormat = f;
  }

  function applyTableFilter(){
    var tableRows = rows();
    if (!tableRows.length) return;
    var qEl = document.querySelector('#fileSearch');
    var typeEl = document.querySelector('#fileTypeFilter');
    var langEl = document.querySelector('#fileLangFilter');
    var q = (qEl && qEl.value || '').toLowerCase().trim();
    var type = normalizeFormat(typeEl && typeEl.value || lastFormat || '');
    var lang = (langEl && langEl.value || '').toLowerCase().trim();
    var visible = 0;
    tableRows.forEach(function(row){
      var formats = setFormats(row);
      if (isPhilosophicalBlock(row)) ['html','pdf','docx','md'].forEach(function(f){ formats.add(f); });
      var text = (row.textContent || '').toLowerCase() + ' ' + Array.from(row.querySelectorAll('a[href]')).map(function(a){ return a.getAttribute('href') || ''; }).join(' ').toLowerCase();
      var okQ = !q || text.includes(q);
      var okType = !type || formats.has(type);
      var okLang = !lang || text.includes(lang);
      var ok = okQ && okType && okLang;
      row.style.display = ok ? '' : 'none';
      if (ok) visible += 1;
    });
    var count = document.querySelector('#fileFilterCount');
    if (count) count.textContent = isHe() ? ('מוצגים ' + visible + ' קבצים') : (visible + ' files shown');
  }

  function forceVisibleForFormat(){
    if (!isFilesPage() || !lastFormat) return;
    cards().forEach(function(card){
      var formats = setFormats(card);
      if (!formats.has(lastFormat)) return;
      card.hidden = false;
      card.removeAttribute('hidden');
      if (card.style && (card.style.display === 'none' || card.style.visibility === 'hidden')) {
        card.style.display = '';
        card.style.visibility = '';
      }
      card.classList.remove('is-hidden','hidden','filtered-out');
    });
  }

  function normalizeFiles(){
    if (!isFilesPage()) return;
    if (!hasPhilosophical()) {
      var c = filesContainer();
      if (c) c.appendChild(createPhilosophical());
    }
    cards().forEach(setFormats);
    applyTableFilter();
    forceVisibleForFormat();
  }

  function init(){
    installHomeMobileTabBarFix();
    normalizeFiles();
    document.addEventListener('click', function(ev){ rememberFormatFromEvent(ev); setTimeout(normalizeFiles, 0); }, true);
    document.addEventListener('change', function(ev){ rememberFormatFromEvent(ev); setTimeout(normalizeFiles, 0); }, true);
    document.addEventListener('input', function(ev){ rememberFormatFromEvent(ev); setTimeout(normalizeFiles, 0); }, true);
    if (isFilesPage()) {
      new MutationObserver(function(){ normalizeFiles(); }).observe(document.documentElement, {
        childList:true, subtree:true, attributes:true,
        attributeFilter:['data-format','data-formats','data-file-format','data-file-formats','class','hidden','style']
      });
    }
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
