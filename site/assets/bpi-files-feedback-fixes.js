/* V121 — scoped Home mobile shell + lightweight Files filtering + file-link target normalization + Witness hero enforcement + Home gateway links.
   Home mobile loads the same main stylesheet used by the Summary tab, then keeps
   only the Home opening hero blue/turquoise. Mobile Home content is slightly wider.
   Files pages normalize real file/download links so they open in a new tab.
   Existing gateway pages are exposed from the Home page without changing their contents.
   English Witness hero is normalized after CSS loads to match Core geometry.
   No unrelated desktop design changes. */
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

  function setImportant(el, prop, value){
    if (!el) return;
    el.style.setProperty(prop, value, 'important');
  }

  function installEnglishWitnessHeroLayout(){ return; }

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

  function installHomeGatewayLinks(){
    if (!isHomePage() || document.getElementById('bpi-home-gateway-links')) return;

    var main = document.getElementById('main') || document.querySelector('main');
    if (!main) return;

    var he = isHe();
    var section = document.createElement('section');
    section.id = 'bpi-home-gateway-links';
    section.className = 'hub-grid three';
    section.setAttribute('aria-label', he ? 'מדריכי כניסה מהירים' : 'Quick entry guides');
    section.innerHTML = he ? [
      '<article class="hub-card media-card accent-core"><div class="card-media-head"><img alt="מילון מושגים" class="card-thumb" decoding="async" height="480" loading="lazy" src="figures/thumb_methodology.png" width="480"/><h2>מילון מושגים</h2></div><p>כניסה קצרה למונחי היסוד של הפרויקט ולדרך שבה הם נבדלים זה מזה.</p><a class="card-link" href="pages/he/glossary.html">פתח מילון מושגים</a></article>',
      '<article class="hub-card media-card accent-core"><div class="card-media-head"><img alt="פוטנציאל, אידיאל ואופטימלי" class="card-thumb" decoding="async" height="480" loading="lazy" src="figures/thumb_core.png" width="480"/><h2>פוטנציאל, אידיאל, אופטימלי</h2></div><p>דף שער שמפריד בין שדה האפשרויות, הצורה הראויה, והתרגום המקומי תחת מגבלות.</p><a class="card-link" href="pages/he/potential-ideal-optimal.html">קרא את דף המושגים</a></article>',
      '<article class="hub-card media-card accent-ai"><div class="card-media-head"><img alt="בינה מלאכותית כעדות" class="card-thumb" decoding="async" height="480" loading="lazy" src="figures/thumb_ai.png" width="480"/><h2>בינה מלאכותית כעדות</h2></div><p>שער קצר לקריאת AI כמראה, עדשה וכלי בדיקה — לא כמקור חי ולא כסמכות.</p><a class="card-link" href="pages/he/ai-as-witness.html">פתח את שער ה־AI</a></article>'
    ].join('') : [
      '<article class="hub-card media-card accent-core"><div class="card-media-head"><img alt="Glossary" class="card-thumb" decoding="async" height="480" loading="lazy" src="figures/thumb_methodology.png" width="480"/><h2>Glossary</h2></div><p>A short entry point into the project’s key terms and the distinctions between them.</p><a class="card-link" href="pages/en/glossary-en.html">Open the glossary</a></article>',
      '<article class="hub-card media-card accent-core"><div class="card-media-head"><img alt="Potential, Ideal, Optimal" class="card-thumb" decoding="async" height="480" loading="lazy" src="figures/thumb_core.png" width="480"/><h2>Potential, Ideal, Optimal</h2></div><p>A gateway page separating the field of possibility, the worthy form, and the local translation under constraints.</p><a class="card-link" href="pages/en/potential-ideal-optimal-en.html">Read the concepts page</a></article>',
      '<article class="hub-card media-card accent-ai"><div class="card-media-head"><img alt="AI as Witness" class="card-thumb" decoding="async" height="480" loading="lazy" src="figures/thumb_ai.png" width="480"/><h2>AI as Witness</h2></div><p>A short gateway for reading AI as mirror, lens, and stress test — not as a living source or authority.</p><a class="card-link" href="pages/en/ai-as-witness-en.html">Open the AI gateway</a></article>'
    ].join('');

    var firstHubGrid = main.querySelector('.hub-grid.three');
    if (firstHubGrid && firstHubGrid.parentNode) {
      firstHubGrid.parentNode.insertBefore(section, firstHubGrid.nextSibling);
    } else {
      main.appendChild(section);
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
    installEnglishWitnessHeroLayout();
    if (window.requestAnimationFrame) window.requestAnimationFrame(installEnglishWitnessHeroLayout);
    window.setTimeout(installEnglishWitnessHeroLayout, 120);
    installHomeMobileSummaryShell();
    installHomeGatewayLinks();
    installFilesFilters();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
