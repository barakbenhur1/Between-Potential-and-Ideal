/* V107 — Files filtering + feedback mail + mobile nav position fixes.
   Additive runtime patch:
   - keeps all file cards discoverable by real link formats
   - restores philosophical theory under format/search filtering
   - converts feedback/Gmail links to native mail links and intercepts clicks to avoid blank tabs
   - keeps the selected mobile nav tab visible instead of letting the nav rail reset to the start
*/
(function(){
  'use strict';

  var FEEDBACK_TO = 'barakbenhur@gmail.com';
  var KNOWN_FORMATS = ['html','pdf','docx','md','txt'];
  var NAV_SCROLL_KEY = 'bpi:last-selected-nav-href';
  var lastFormat = null;
  var navScrollInstalled = false;

  function isHe(){
    return document.documentElement.lang === 'he' ||
      document.documentElement.dir === 'rtl' ||
      document.body.classList.contains('public-page-he');
  }

  function isFilesPage(){
    var p = location.pathname.toLowerCase();
    return p.endsWith('/files.html') || p.endsWith('/files-en.html') ||
      document.body.classList.contains('files-page') ||
      !!document.querySelector('.file-card,.download-card,.resource-card,[data-format],[data-formats]');
  }

  function enc(v){ return encodeURIComponent(v).replace(/%20/g,'%20'); }

  function feedbackMailto(){
    var he = isHe();
    var subject = he ? 'ביקורת על Between Potential and Ideal' : 'Feedback on Between Potential and Ideal';
    var body = he ? [
      'שלום ברק,',
      '',
      'קראתי את הפרויקט Between Potential and Ideal ויש לי ביקורת / הערה:',
      '',
      '',
      'העמוד שבו הייתי:',
      location.href,
      '',
      'הערה:'
    ].join('\n') : [
      'Hi Barak,',
      '',
      'I read Between Potential and Ideal and have feedback / a note:',
      '',
      '',
      'Page I was on:',
      location.href,
      '',
      'Feedback:'
    ].join('\n');
    return 'mailto:' + FEEDBACK_TO + '?subject=' + enc(subject) + '&body=' + enc(body);
  }

  function isFeedbackAnchor(a){
    if (!a || !a.getAttribute) return false;
    var href = (a.getAttribute('href') || '').toLowerCase();
    var text = (a.textContent || '').trim().toLowerCase();
    var aria = (a.getAttribute('aria-label') || '').toLowerCase();
    var title = (a.getAttribute('title') || '').toLowerCase();
    return href.includes('mail.google.com') || href.includes('gmail.com/mail') ||
      href.startsWith('mailto:') && (text.includes('ביקורת') || text.includes('feedback')) ||
      text.includes('שלח ביקורת') || aria.includes('שלח ביקורת') || title.includes('שלח ביקורת') ||
      text.includes('send feedback') || aria.includes('send feedback') || title.includes('send feedback') ||
      text === 'feedback' || aria === 'feedback' || title === 'feedback';
  }

  function patchFeedbackLinks(){
    var mail = feedbackMailto();
    document.querySelectorAll('a[href]').forEach(function(a){
      if (!isFeedbackAnchor(a)) return;
      a.setAttribute('href', mail);
      a.removeAttribute('target');
      a.removeAttribute('rel');
      a.setAttribute('data-bpi-feedback-mail','true');
    });
  }

  function installFeedbackClickGuard(){
    document.addEventListener('click', function(ev){
      var a = ev.target && ev.target.closest ? ev.target.closest('a[href]') : null;
      if (!isFeedbackAnchor(a)) return;
      ev.preventDefault();
      ev.stopPropagation();
      a.removeAttribute('target');
      a.removeAttribute('rel');
      a.setAttribute('href', feedbackMailto());
      window.location.href = feedbackMailto();
    }, true);
  }

  function fmtFromHref(h){
    var clean = (h || '').split('?')[0].split('#')[0].toLowerCase();
    var m = clean.match(/\.([a-z0-9]+)$/);
    if (!m) return null;
    var e = m[1] === 'htm' ? 'html' : m[1];
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

  function formatsOf(card){
    var formats = new Set();
    [
      card.getAttribute('data-format'),
      card.getAttribute('data-formats'),
      card.getAttribute('data-file-format'),
      card.getAttribute('data-file-formats'),
      card.dataset && card.dataset.format,
      card.dataset && card.dataset.formats,
      card.dataset && card.dataset.fileFormat,
      card.dataset && card.dataset.fileFormats
    ].filter(Boolean).join(' ').split(/[\s,|/]+/).forEach(function(f){
      f = (f || '').trim().toLowerCase();
      if (KNOWN_FORMATS.indexOf(f) >= 0) formats.add(f);
    });
    card.querySelectorAll('a[href]').forEach(function(a){
      var f = fmtFromHref(a.getAttribute('href'));
      if (f) formats.add(f);
    });
    return formats;
  }

  function isPhilosophicalCard(card){
    var text = (card.textContent || '').toLowerCase();
    var hrefs = Array.from(card.querySelectorAll('a[href]')).map(function(a){return a.getAttribute('href') || '';}).join(' ').toLowerCase();
    return text.includes('התאוריה הפילוסופית') || text.includes('התיאוריה הפילוסופית') ||
      text.includes('philosophical theory') || text.includes('between potential and ideal') ||
      hrefs.includes('between-potential-and-ideal-he-editorial') ||
      hrefs.includes('between-potential-and-ideal-en-editorial');
  }

  function setCardFormats(card){
    var formats = formatsOf(card);
    if (isPhilosophicalCard(card)) {
      ['html','pdf','docx','md'].forEach(function(f){ formats.add(f); });
      card.dataset.search = [
        card.dataset.search || '',
        'התאוריה הפילוסופית','התיאוריה הפילוסופית','בין פוטנציאל לאידיאל',
        'philosophical theory','between potential and ideal','html pdf docx md'
      ].join(' ');
    }
    if (!formats.size) return;
    var value = Array.from(formats).sort().join(' ');
    card.setAttribute('data-format', value);
    card.setAttribute('data-formats', value);
    card.setAttribute('data-file-format', value);
    card.setAttribute('data-file-formats', value);
    card.setAttribute('data-filter-formats', value);
    KNOWN_FORMATS.forEach(function(f){ card.classList.toggle('format-' + f, formats.has(f)); });
  }

  function hasPhilosophical(){ return cards().some(isPhilosophicalCard); }

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
    for (var i=0;i<KNOWN_FORMATS.length;i++) if (raw.includes(KNOWN_FORMATS[i])) return KNOWN_FORMATS[i];
    if (raw.includes('all') || raw.includes('הכל') || raw.includes('כולם')) return null;
    return lastFormat;
  }

  function rememberFormatFromEvent(ev){
    var el = ev && ev.target && ev.target.closest ? ev.target.closest('button,a,input,select,[data-format],[data-filter],[data-value]') : null;
    var f = currentFormatFromControl(el);
    lastFormat = f;
  }

  function forceVisibleForFormat(){
    if (!isFilesPage() || !lastFormat) return;
    cards().forEach(function(card){
      var formats = formatsOf(card);
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
    cards().forEach(setCardFormats);
    forceVisibleForFormat();
  }

  function absPath(a){
    try { return new URL(a.getAttribute('href'), location.href).pathname.replace(/\/+$/,''); }
    catch(e) { return ''; }
  }

  function currentPath(){ return location.pathname.replace(/\/+$/,''); }

  function findNavTarget(nav){
    if (!nav) return null;
    var active = nav.querySelector('a[aria-current="page"],a.active');
    if (active) return active;

    var saved = null;
    try { saved = sessionStorage.getItem(NAV_SCROLL_KEY); } catch(e) {}
    var links = Array.from(nav.querySelectorAll('a[href]'));
    if (saved) {
      var bySaved = links.find(function(a){ return absPath(a) === saved || a.getAttribute('href') === saved; });
      if (bySaved) return bySaved;
    }
    var now = currentPath();
    return links.find(function(a){ return absPath(a) === now; }) || null;
  }

  function centerNavTarget(nav, target){
    if (!nav || !target) return;
    if (nav.scrollWidth <= nav.clientWidth + 2) return;

    var reduceMotion = false;
    try { reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches; } catch(e) {}
    var behavior = reduceMotion ? 'auto' : 'smooth';

    try {
      target.scrollIntoView({block:'nearest', inline:'center', behavior:behavior});
    } catch(e) {
      var desired = target.offsetLeft - ((nav.clientWidth - target.offsetWidth) / 2);
      nav.scrollLeft = Math.max(0, desired);
    }
  }

  function keepSelectedNavVisible(){
    var navs = Array.from(document.querySelectorAll('.site-nav'));
    navs.forEach(function(nav){
      var target = findNavTarget(nav);
      if (!target) return;
      centerNavTarget(nav, target);
    });
  }

  function installMobileNavScrollFix(){
    if (navScrollInstalled) return;
    navScrollInstalled = true;

    document.addEventListener('click', function(ev){
      var a = ev.target && ev.target.closest ? ev.target.closest('.site-nav a[href]') : null;
      if (!a) return;
      try { sessionStorage.setItem(NAV_SCROLL_KEY, absPath(a) || a.getAttribute('href') || ''); } catch(e) {}
      setTimeout(keepSelectedNavVisible, 0);
    }, true);

    window.addEventListener('pageshow', function(){ setTimeout(keepSelectedNavVisible, 0); setTimeout(keepSelectedNavVisible, 120); });
    window.addEventListener('load', function(){ setTimeout(keepSelectedNavVisible, 80); });
    window.addEventListener('resize', function(){ setTimeout(keepSelectedNavVisible, 120); });
  }

  function init(){
    patchFeedbackLinks();
    installFeedbackClickGuard();
    installMobileNavScrollFix();
    normalizeFiles();
    keepSelectedNavVisible();
    setTimeout(keepSelectedNavVisible, 80);
    setTimeout(keepSelectedNavVisible, 240);
    document.addEventListener('click', function(ev){ rememberFormatFromEvent(ev); setTimeout(function(){ patchFeedbackLinks(); normalizeFiles(); keepSelectedNavVisible(); }, 0); }, true);
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
