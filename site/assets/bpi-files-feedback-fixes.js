/* V114 — Scoped fixes only.
   1) Home mobile top bar: match the other tabs more closely, no horizontal scroll.
   2) Files page: lightweight filtering only; no MutationObserver, no global click loop, no freeze.
   Feedback links are handled only by assets/bpi-fixes/bpi-feedback-desktop.js. */
(function(){
  'use strict';

  var KNOWN_FORMATS = ['html','pdf','docx','md','txt'];

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

  function installHomeMobileTopBarFix(){
    if (!isHomePage() || document.getElementById('bpi-home-mobile-topbar-match-v114')) return;
    var style = document.createElement('style');
    style.id = 'bpi-home-mobile-topbar-match-v114';
    style.textContent = '' +
      '@media (max-width:860px){' +
      'html,body{width:100%!important;max-width:100%!important;overflow-x:hidden!important;}' +
      'body.public-page{max-width:100vw!important;overflow-x:hidden!important;background:#f3eadb!important;}' +

      /* Header: same full-width visual language as the other tabs, but less tall than the previous Home patch. */
      'body.public-page .site-header,body.public-page header.site-header,.site-header{' +
      'width:100%!important;max-width:100vw!important;margin:0!important;padding:22px 18px 18px!important;box-sizing:border-box!important;' +
      'display:flex!important;flex-direction:column!important;align-items:center!important;justify-content:center!important;gap:14px!important;' +
      'border:0!important;border-radius:0!important;overflow:hidden!important;overflow-x:hidden!important;' +
      'background:radial-gradient(circle at 96% 86%,rgba(245,154,57,.86),rgba(245,154,57,0) 32%),linear-gradient(135deg,#06446a 0%,#075777 48%,#0a5269 73%,#e69a3c 116%)!important;' +
      'box-shadow:none!important;color:#fffaf0!important;text-align:center!important;' +
      '}' +

      'body.public-page .site-brand,.site-header .site-brand{width:100%!important;display:flex!important;justify-content:center!important;align-items:center!important;margin:0!important;min-width:0!important;max-width:100%!important;text-align:center!important;}' +
      'body.public-page .site-brand a,.site-header .site-brand a{' +
      'display:block!important;width:100%!important;text-align:center!important;color:#fffaf0!important;text-decoration:none!important;font-family:Georgia,"Times New Roman",serif!important;font-weight:800!important;font-size:clamp(1.28rem,4.75vw,1.78rem)!important;line-height:1.12!important;letter-spacing:.01em!important;white-space:normal!important;' +
      '}' +

      'body.public-page .site-header .site-nav,.site-header .site-nav,nav.site-nav{' +
      'display:flex!important;flex-direction:row!important;flex-wrap:wrap!important;justify-content:center!important;align-items:center!important;align-content:center!important;' +
      'width:100%!important;max-width:680px!important;min-width:0!important;height:auto!important;max-height:none!important;box-sizing:border-box!important;' +
      'overflow:visible!important;overflow-x:visible!important;overflow-y:visible!important;white-space:normal!important;gap:8px 7px!important;margin:0 auto!important;padding:0!important;' +
      'scrollbar-width:none!important;scroll-snap-type:none!important;text-align:center!important;' +
      '}' +
      'body.public-page .site-header .site-nav::-webkit-scrollbar,.site-header .site-nav::-webkit-scrollbar,nav.site-nav::-webkit-scrollbar{display:none!important;}' +
      'body.public-page .site-header .site-nav a,.site-header .site-nav a,nav.site-nav a{' +
      'display:inline-flex!important;align-items:center!important;justify-content:center!important;flex:0 0 auto!important;min-width:0!important;max-width:none!important;box-sizing:border-box!important;' +
      'min-height:38px!important;padding:.45rem .74rem!important;border-radius:999px!important;border:1px solid rgba(255,255,255,.28)!important;background:rgba(255,255,255,.10)!important;' +
      'color:#fffaf0!important;text-decoration:none!important;font-family:Georgia,"Times New Roman","Noto Serif Hebrew",serif!important;font-size:clamp(.94rem,3.85vw,1.08rem)!important;font-weight:700!important;line-height:1!important;letter-spacing:.01em!important;' +
      'white-space:nowrap!important;overflow:hidden!important;text-overflow:ellipsis!important;transform:none!important;scroll-snap-align:none!important;box-shadow:none!important;' +
      '}' +
      'body.public-page .site-header .site-nav a.active,body.public-page .site-header .site-nav a[aria-current="page"],.site-header .site-nav a.active,.site-header .site-nav a[aria-current="page"]{' +
      'background:rgba(255,255,255,.22)!important;border-color:rgba(255,255,255,.46)!important;box-shadow:0 8px 20px rgba(255,255,255,.08) inset,0 6px 18px rgba(0,0,0,.05)!important;color:#fffaf0!important;' +
      '}' +

      'body.public-page .language-switch,.site-header .language-switch{' +
      'display:flex!important;align-items:center!important;justify-content:center!important;width:100%!important;max-width:680px!important;min-height:50px!important;margin:3px auto 0!important;padding:.56rem 1rem!important;box-sizing:border-box!important;' +
      'border-radius:999px!important;border:1px solid rgba(255,255,255,.30)!important;background:rgba(255,255,255,.08)!important;color:#fffaf0!important;text-decoration:none!important;font-family:Georgia,"Times New Roman",serif!important;font-size:clamp(1.05rem,4.05vw,1.35rem)!important;font-weight:600!important;line-height:1!important;box-shadow:none!important;' +
      '}' +

      /* Keep Home content inside the viewport, but do not redesign it. */
      'body.public-page .site-main{width:100%!important;max-width:100vw!important;overflow-x:hidden!important;box-sizing:border-box!important;padding-left:0!important;padding-right:0!important;}' +
      'body.public-page .breadcrumbs,body.public-page .concise-hero,body.public-page .hero,body.public-page .opening-visual,body.public-page .signature-blurbs,body.public-page .notice-box,body.public-page .hub-grid,body.public-page .reading-path-cta{' +
      'width:min(100% - 36px,1120px)!important;max-width:calc(100vw - 36px)!important;margin-left:auto!important;margin-right:auto!important;box-sizing:border-box!important;' +
      '}' +
      'body.public-page .concise-hero,body.public-page .hero{padding-left:clamp(16px,4vw,28px)!important;padding-right:clamp(16px,4vw,28px)!important;}' +
      '}' +

      '@media (max-width:390px){' +
      'body.public-page .site-header,body.public-page header.site-header,.site-header{padding:20px 14px 16px!important;gap:12px!important;}' +
      'body.public-page .site-header .site-nav,.site-header .site-nav,nav.site-nav{gap:7px 6px!important;}' +
      'body.public-page .site-header .site-nav a,.site-header .site-nav a,nav.site-nav a{padding:.42rem .66rem!important;font-size:clamp(.9rem,3.75vw,1rem)!important;min-height:36px!important;}' +
      'body.public-page .language-switch,.site-header .language-switch{min-height:48px!important;}' +
      'body.public-page .breadcrumbs,body.public-page .concise-hero,body.public-page .hero,body.public-page .opening-visual,body.public-page .signature-blurbs,body.public-page .notice-box,body.public-page .hub-grid,body.public-page .reading-path-cta{width:min(100% - 30px,1120px)!important;max-width:calc(100vw - 30px)!important;}' +
      '}';
    document.head.appendChild(style);
  }

  function isFilesPage(){
    var p = location.pathname.toLowerCase();
    return p.endsWith('/files.html') || p.endsWith('/files-en.html') ||
      document.body.classList.contains('files-page') ||
      !!document.querySelector('#fileSearch,#fileTypeFilter,#fileLangFilter,.download-table');
  }

  function normalizeFormat(value){
    value = (value || '').toLowerCase().trim();
    if (value === 'word' || value === 'doc') return 'docx';
    if (value === 'markdown') return 'md';
    if (value === 'text') return 'txt';
    return value;
  }

  function formatFromHref(href){
    var clean = (href || '').split('?')[0].split('#')[0].toLowerCase();
    var match = clean.match(/\.([a-z0-9]+)$/);
    if (!match) return '';
    var ext = normalizeFormat(match[1]);
    return KNOWN_FORMATS.indexOf(ext) !== -1 ? ext : '';
  }

  function rowText(row){
    var hrefs = Array.from(row.querySelectorAll('a[href]')).map(function(a){ return a.getAttribute('href') || ''; }).join(' ');
    return ((row.textContent || '') + ' ' + hrefs).toLowerCase();
  }

  function rowFormats(row){
    var formats = new Set();
    Array.from(row.querySelectorAll('a[href]')).forEach(function(a){
      var f = formatFromHref(a.getAttribute('href'));
      if (f) formats.add(f);
    });

    var existing = [
      row.getAttribute('data-format'),
      row.getAttribute('data-formats'),
      row.getAttribute('data-file-format'),
      row.getAttribute('data-file-formats')
    ].filter(Boolean).join(' ');
    existing.split(/[\s,|/]+/).forEach(function(f){
      f = normalizeFormat(f);
      if (KNOWN_FORMATS.indexOf(f) !== -1) formats.add(f);
    });

    var text = rowText(row);
    if (text.indexOf('html') !== -1) formats.add('html');
    if (text.indexOf('pdf') !== -1) formats.add('pdf');
    if (text.indexOf('docx') !== -1 || text.indexOf('word') !== -1) formats.add('docx');
    if (text.indexOf('markdown') !== -1 || text.indexOf('.md') !== -1) formats.add('md');
    if (text.indexOf('text') !== -1 || text.indexOf('.txt') !== -1) formats.add('txt');

    if (text.indexOf('התאוריה הפילוסופית') !== -1 ||
        text.indexOf('התיאוריה הפילוסופית') !== -1 ||
        text.indexOf('philosophical theory') !== -1 ||
        text.indexOf('between-potential-and-ideal-he') !== -1 ||
        text.indexOf('between-potential-and-ideal-en') !== -1) {
      ['html','pdf','docx','md'].forEach(function(f){ formats.add(f); });
    }
    return formats;
  }

  function applyFilesFilter(){
    if (!isFilesPage()) return;
    var rows = Array.from(document.querySelectorAll('.download-table tr')).slice(1);
    if (!rows.length) return;

    var qEl = document.querySelector('#fileSearch');
    var typeEl = document.querySelector('#fileTypeFilter');
    var langEl = document.querySelector('#fileLangFilter');
    var query = (qEl && qEl.value || '').toLowerCase().trim();
    var type = normalizeFormat(typeEl && typeEl.value || '');
    var lang = (langEl && langEl.value || '').toLowerCase().trim();
    var visible = 0;

    rows.forEach(function(row){
      var text = rowText(row);
      var formats = rowFormats(row);
      var formatValue = Array.from(formats).sort().join(' ');
      row.setAttribute('data-format', formatValue);
      row.setAttribute('data-formats', formatValue);
      row.setAttribute('data-file-format', formatValue);
      row.setAttribute('data-file-formats', formatValue);

      var okQuery = !query || text.indexOf(query) !== -1;
      var okType = !type || formats.has(type);
      var okLang = !lang || text.indexOf(lang) !== -1;
      var ok = okQuery && okType && okLang;
      row.style.display = ok ? '' : 'none';
      if (ok) visible += 1;
    });

    var count = document.querySelector('#fileFilterCount');
    if (count) count.textContent = isHe() ? ('מוצגים ' + visible + ' קבצים') : (visible + ' files shown');
  }

  function installFilesFilters(){
    if (!isFilesPage()) return;
    var search = document.querySelector('#fileSearch');
    var type = document.querySelector('#fileTypeFilter');
    var lang = document.querySelector('#fileLangFilter');
    if (search) search.addEventListener('input', applyFilesFilter, false);
    if (type) type.addEventListener('change', applyFilesFilter, false);
    if (lang) lang.addEventListener('change', applyFilesFilter, false);
    applyFilesFilter();
  }

  function init(){
    installHomeMobileTopBarFix();
    installFilesFilters();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
