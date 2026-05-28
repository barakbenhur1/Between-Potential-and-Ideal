/* V120 — scoped Home mobile shell + lightweight Files filtering + file-link target normalization + Home reflection fold.
   Home mobile loads the same main stylesheet used by the Summary tab, then keeps
   only the Home opening hero blue/turquoise. Mobile Home content is slightly wider.
   Files pages normalize real file/download links so they open in a new tab.
   Home keeps the long poetic/reflection block, but folds it behind a reader-controlled summary.
   No desktop design changes outside the targeted Home/Files behaviors. */
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

  function installHomeMobileSummaryShell(){
    if (!isHomePage() || !window.matchMedia || !window.matchMedia('(max-width: 860px)').matches) return;

    if (!document.getElementById('bpi-home-mobile-summary-stylesheet-v117')) {
      var link = document.createElement('link');
      link.id = 'bpi-home-mobile-summary-stylesheet-v117';
      link.rel = 'stylesheet';
      link.href = 'styles.css?v=20260526-home-mobile-summary-shell-v117';
      document.head.appendChild(link);
    }

    if (document.getElementById('bpi-home-mobile-blue-hero-v117')) return;
    var style = document.createElement('style');
    style.id = 'bpi-home-mobile-blue-hero-v117';
    style.textContent = [
      '@media (max-width:860px){',
      'html,body{width:100%!important;max-width:100%!important;overflow-x:hidden!important;}',
      'body.public-page{background:radial-gradient(circle at 0% 12%,rgba(0,167,183,.10),transparent 34rem),radial-gradient(circle at 100% 0%,rgba(242,142,43,.12),transparent 32rem),#f7efe1!important;color:#102033!important;}',
      'body.public-page .site-main{background:transparent!important;color:#102033!important;max-width:100vw!important;overflow-x:hidden!important;}',

      /* Use Summary shell, only guarantee no horizontal mobile rail on Home. */
      'body.public-page .site-header{background:linear-gradient(135deg,#0A3A68,#0C526D 58%,rgba(242,142,43,.92))!important;color:#fff!important;}',
      'body.public-page .site-header a{color:#fff!important;}',
      'body.public-page .site-header .site-nav{display:flex!important;flex-wrap:wrap!important;justify-content:center!important;align-items:center!important;overflow:visible!important;overflow-x:visible!important;scroll-snap-type:none!important;}',
      'body.public-page .site-header .site-nav a{transform:none!important;scroll-snap-align:none!important;}',

      /* Summary-like page spacing. */
      'body.public-page .breadcrumbs{width:min(100% - 24px,1120px)!important;max-width:calc(100vw - 24px)!important;margin:52px auto 14px!important;box-sizing:border-box!important;}',
      'body.public-page .opening-visual,body.public-page .signature-blurbs,body.public-page .notice-box,body.public-page .hub-grid,body.public-page .reading-path-cta{width:min(100% - 24px,1120px)!important;max-width:calc(100vw - 24px)!important;margin-left:auto!important;margin-right:auto!important;box-sizing:border-box!important;}',

      /* Restore the Home-specific opening block: blue/turquoise card with white text. */
      'body.public-page .concise-hero,body.public-page .hero.concise-hero{display:block!important;width:min(100% - 24px,1120px)!important;max-width:calc(100vw - 24px)!important;margin:0 auto 26px!important;box-sizing:border-box!important;padding:clamp(34px,8vw,56px) clamp(24px,6vw,42px)!important;border-radius:30px!important;border:1px solid rgba(255,255,255,.22)!important;background:linear-gradient(145deg,#06466d 0%,#007b91 58%,#008fa2 100%)!important;color:#fffaf0!important;box-shadow:0 18px 48px rgba(10,58,104,.18)!important;text-align:center!important;overflow:hidden!important;}',
      'body.public-page .concise-hero::before,body.public-page .hero.concise-hero::before{display:none!important;content:none!important;}',
      'body.public-page .concise-hero .kicker,body.public-page .hero.concise-hero .kicker{color:#fffaf0!important;background:transparent!important;border:0!important;margin:0 auto clamp(30px,8vw,58px)!important;padding:0!important;text-align:center!important;font-weight:800!important;}',
      'body.public-page .concise-hero h1,body.public-page .hero.concise-hero h1{color:#fffaf0!important;text-align:center!important;margin:0 auto!important;max-width:760px!important;font-family:"Gveret Levin","Noto Sans Hebrew",Georgia,"Times New Roman",serif!important;font-size:clamp(2.7rem,11.5vw,4.8rem)!important;line-height:1.04!important;letter-spacing:-.025em!important;}',
      'body.public-page .concise-hero .lead,body.public-page .hero.concise-hero .lead,body.public-page .concise-hero .method-note,body.public-page .hero.concise-hero .method-note{color:rgba(255,250,240,.92)!important;text-align:center!important;margin-left:auto!important;margin-right:auto!important;max-width:72ch!important;background:transparent!important;border:0!important;box-shadow:none!important;padding:0!important;font-size:clamp(1rem,4.5vw,1.18rem)!important;line-height:1.7!important;}',
      '}',
      '@media (max-width:390px){',
      'body.public-page .breadcrumbs{width:min(100% - 20px,1120px)!important;max-width:calc(100vw - 20px)!important;margin-top:48px!important;}',
      'body.public-page .concise-hero,body.public-page .hero.concise-hero{width:min(100% - 20px,1120px)!important;max-width:calc(100vw - 20px)!important;padding:44px 22px!important;border-radius:28px!important;}',
      '}'
    ].join('');
    document.head.appendChild(style);
  }

  function installHomeReflectionFold(){
    if (!isHomePage()) return;
    if (document.querySelector('.bpi-home-reflection-fold')) return;

    var section = document.querySelector('.signature-blurbs');
    if (!section || !section.parentNode) return;

    var fold = document.createElement('details');
    fold.className = 'bpi-home-reflection-fold media-card accent-witness';

    var summary = document.createElement('summary');
    summary.textContent = isHe() ? 'פתיחה פואטית / אישית' : 'Poetic opening / personal reflection';
    fold.appendChild(summary);

    section.parentNode.insertBefore(fold, section);
    fold.appendChild(section);

    if (!document.getElementById('bpi-home-reflection-fold-style-v120')) {
      var style = document.createElement('style');
      style.id = 'bpi-home-reflection-fold-style-v120';
      style.textContent = [
        'body.bpi-home-page .bpi-home-reflection-fold{width:min(1680px,calc(100vw - 96px))!important;max-width:min(1680px,calc(100vw - 96px))!important;margin:28px auto!important;padding:0!important;box-sizing:border-box!important;border:1px solid rgba(18,63,115,.14)!important;border-radius:24px!important;background:linear-gradient(135deg,rgba(255,255,255,.98),rgba(255,250,240,.96))!important;box-shadow:0 14px 38px rgba(10,58,104,.08)!important;overflow:hidden!important;}',
        'body.bpi-home-page .bpi-home-reflection-fold summary{cursor:pointer;list-style:none;padding:20px 24px!important;color:#123f73!important;font-weight:900!important;font-size:clamp(1.15rem,1.5vw,1.45rem)!important;line-height:1.35!important;}',
        'body.bpi-home-page .bpi-home-reflection-fold summary::-webkit-details-marker{display:none!important;}',
        'body.bpi-home-page .bpi-home-reflection-fold summary::after{content:"＋";float:inline-end;font-weight:900;color:#b87926;}',
        'body.bpi-home-page .bpi-home-reflection-fold[open] summary::after{content:"−";}',
        'body.bpi-home-page .bpi-home-reflection-fold .signature-blurbs{width:100%!important;max-width:none!important;margin:0!important;padding:0 24px 24px!important;box-sizing:border-box!important;}',
        'body.bpi-home-page .bpi-home-reflection-fold:not([open]){margin-bottom:24px!important;}',
        '@media(max-width:860px){body.bpi-home-page .bpi-home-reflection-fold{width:calc(100vw - 24px)!important;max-width:calc(100vw - 24px)!important;margin:22px auto!important;}body.bpi-home-page .bpi-home-reflection-fold summary{padding:18px 18px!important;}body.bpi-home-page .bpi-home-reflection-fold .signature-blurbs{padding:0 18px 20px!important;}}'
      ].join('');
      document.head.appendChild(style);
    }
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

  function normalizeFileDownloadTargets(){
    if (!isFilesPage()) return;

    Array.from(document.querySelectorAll('a[href]')).forEach(function(a){
      var href = a.getAttribute('href') || '';
      var clean = href.split('?')[0].split('#')[0].toLowerCase();
      var pointsToFileArchive = clean.indexOf('/files/') !== -1 ||
        clean.indexOf('../../files/') === 0 || clean.indexOf('../files/') === 0 ||
        clean.indexOf('files/') === 0;

      if (!pointsToFileArchive || !formatFromHref(href)) return;

      a.setAttribute('target', '_blank');

      var rel = (a.getAttribute('rel') || '').split(/\s+/).filter(Boolean);
      ['noopener','noreferrer'].forEach(function(token){
        if (rel.indexOf(token) === -1) rel.push(token);
      });
      a.setAttribute('rel', rel.join(' '));
    });
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

    [row.getAttribute('data-format'), row.getAttribute('data-formats'), row.getAttribute('data-file-format'), row.getAttribute('data-file-formats')]
      .filter(Boolean).join(' ').split(/[\s,|/]+/).forEach(function(f){
        f = normalizeFormat(f);
        if (KNOWN_FORMATS.indexOf(f) !== -1) formats.add(f);
      });

    var text = rowText(row);
    if (text.indexOf('html') !== -1) formats.add('html');
    if (text.indexOf('pdf') !== -1) formats.add('pdf');
    if (text.indexOf('docx') !== -1 || text.indexOf('word') !== -1) formats.add('docx');
    if (text.indexOf('markdown') !== -1 || text.indexOf('.md') !== -1) formats.add('md');
    if (text.indexOf('text') !== -1 || text.indexOf('.txt') !== -1) formats.add('txt');
    if (text.indexOf('התאוריה הפילוסופית') !== -1 || text.indexOf('התיאוריה הפילוסופית') !== -1 || text.indexOf('philosophical theory') !== -1 || text.indexOf('between-potential-and-ideal-he') !== -1 || text.indexOf('between-potential-and-ideal-en') !== -1) {
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

      var ok = (!query || text.indexOf(query) !== -1) && (!type || formats.has(type)) && (!lang || text.indexOf(lang) !== -1);
      row.style.display = ok ? '' : 'none';
      if (ok) visible += 1;
    });

    var count = document.querySelector('#fileFilterCount');
    if (count) count.textContent = isHe() ? ('מוצגים ' + visible + ' קבצים') : (visible + ' files shown');
  }

  function installFilesFilters(){
    if (!isFilesPage()) return;
    normalizeFileDownloadTargets();
    var search = document.querySelector('#fileSearch');
    var type = document.querySelector('#fileTypeFilter');
    var lang = document.querySelector('#fileLangFilter');
    if (search) search.addEventListener('input', applyFilesFilter, false);
    if (type) type.addEventListener('change', applyFilesFilter, false);
    if (lang) lang.addEventListener('change', applyFilesFilter, false);
    applyFilesFilter();
  }

  function init(){
    installHomeMobileSummaryShell();
    installHomeReflectionFold();
    installFilesFilters();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
