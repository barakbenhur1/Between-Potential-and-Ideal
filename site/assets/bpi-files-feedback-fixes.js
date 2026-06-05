(function () {
  'use strict';

  const HE_ITEMS = [
    ['בית', 'index.html', 'index'],
    ['תקציר', 'summary.html', 'summary'],
    ['מילון', 'glossary.html', 'glossary'],
    ['מושגים', 'potential-ideal-optimal.html', 'potential-ideal-optimal'],
    ['בינה מלאכותית כעדות', 'ai-as-witness.html', 'ai-as-witness'],
    ['ליבה', 'core.html', 'core'],
    ['מתודולוגיה', 'methodology.html', 'methodology'],
    ['עדות', 'witness.html', 'witness'],
    ['יישום', 'applied.html', 'applied'],
    ['בינה מלאכותית', 'ai.html', 'ai'],
    ['קבצים', 'files.html', 'files'],
    ['ביקורת', 'critique.html', 'critique'],
    ['מקורות', 'sources.html', 'sources']
  ];

  const EN_ITEMS = [
    ['Home', 'en.html', 'en'],
    ['Summary', 'summary-en.html', 'summary-en'],
    ['Glossary', 'glossary-en.html', 'glossary-en'],
    ['Concepts', 'potential-ideal-optimal-en.html', 'potential-ideal-optimal-en'],
    ['AI as Witness', 'ai-as-witness-en.html', 'ai-as-witness-en'],
    ['Core', 'core-en.html', 'core-en'],
    ['Methodology', 'methodology-en.html', 'methodology-en'],
    ['Witness', 'witness-en.html', 'witness-en'],
    ['Application', 'applied-en.html', 'applied-en'],
    ['AI', 'ai-en.html', 'ai-en'],
    ['Files', 'files-en.html', 'files-en'],
    ['Critique', 'critique-en.html', 'critique-en'],
    ['Sources', 'sources-en.html', 'sources-en']
  ];

  const HE_TO_EN = {
    index: 'en.html',
    summary: 'summary-en.html',
    glossary: 'glossary-en.html',
    'potential-ideal-optimal': 'potential-ideal-optimal-en.html',
    'ai-as-witness': 'ai-as-witness-en.html',
    core: 'core-en.html',
    methodology: 'methodology-en.html',
    witness: 'witness-en.html',
    applied: 'applied-en.html',
    ai: 'ai-en.html',
    files: 'files-en.html',
    critique: 'critique-en.html',
    sources: 'sources-en.html'
  };

  const EN_TO_HE = {
    en: 'index.html',
    'summary-en': 'summary.html',
    'glossary-en': 'glossary.html',
    'potential-ideal-optimal-en': 'potential-ideal-optimal.html',
    'ai-as-witness-en': 'ai-as-witness.html',
    'core-en': 'core.html',
    'methodology-en': 'methodology.html',
    'witness-en': 'witness.html',
    'applied-en': 'applied.html',
    'ai-en': 'ai.html',
    'files-en': 'files.html',
    'critique-en': 'critique.html',
    'sources-en': 'sources.html'
  };

  function pathname() {
    return location.pathname || '';
  }

  function isHebrew() {
    return document.documentElement.lang === 'he' || document.documentElement.dir === 'rtl';
  }

  function isInnerPage() {
    return pathname().includes('/pages/he/') || pathname().includes('/pages/en/');
  }

  function pageKey() {
    const fallback = isHebrew() ? 'index.html' : 'en.html';
    const filename = pathname().split('/').pop() || fallback;
    return filename.replace(/\.html$/, '') || (isHebrew() ? 'index' : 'en');
  }

  function navHref(file, he) {
    if (isInnerPage()) {
      if (file === 'index.html') return '../../index.html';
      if (file === 'en.html') return '../../en.html';
      return file;
    }

    if (he) return file === 'index.html' ? 'index.html' : 'pages/he/' + file;
    return file === 'en.html' ? 'en.html' : 'pages/en/' + file;
  }

  function languageHref(he, key) {
    if (he) {
      const target = HE_TO_EN[key] || (key === 'index' ? 'en.html' : key + '-en.html');
      return isInnerPage() ? '../en/' + target : target;
    }

    const fallbackKey = key.endsWith('-en') ? key.slice(0, -3) : key;
    const target = EN_TO_HE[key] || fallbackKey + '.html';
    return isInnerPage() ? '../he/' + target : target;
  }

  function setActiveState(link, itemKey, activeKey) {
    const active = itemKey === activeKey;
    link.classList.toggle('active', active);
    if (active) link.setAttribute('aria-current', 'page');
    else link.removeAttribute('aria-current');
  }

  function normalizeExistingHeader(header, he, activeKey) {
    const brand = header.querySelector(':scope > .site-brand');
    const brandLink = brand && brand.querySelector(':scope > a');
    const nav = header.querySelector(':scope > nav.site-nav');
    const languageSwitch = header.querySelector(':scope > .language-switch');
    const items = he ? HE_ITEMS : EN_ITEMS;
    const links = nav ? Array.from(nav.querySelectorAll(':scope > a')) : [];

    if (!brand || !brandLink || !nav || !languageSwitch || links.length !== items.length) {
      return false;
    }

    header.dir = he ? 'rtl' : 'ltr';
    header.classList.add('bpi-shared-nav');
    header.classList.toggle('bpi-home-nav', activeKey === 'index' || activeKey === 'en');

    brandLink.href = isInnerPage()
      ? (he ? '../../index.html' : '../../en.html')
      : (he ? 'index.html' : 'en.html');
    brandLink.textContent = 'Between Potential and Ideal';

    nav.setAttribute('aria-label', 'Primary navigation');
    nav.setAttribute('role', 'navigation');

    items.forEach(([label, file, itemKey], index) => {
      const link = links[index];
      link.href = navHref(file, he);
      link.textContent = label;
      setActiveState(link, itemKey, activeKey);
    });

    languageSwitch.href = languageHref(he, activeKey);
    languageSwitch.textContent = he ? 'English' : 'עברית';
    languageSwitch.setAttribute(
      'aria-label',
      he ? 'Switch to the English version' : 'מעבר לגרסה העברית'
    );
    languageSwitch.title = he ? 'English version' : 'גרסה עברית';

    return true;
  }

  function buildHeader(header, he, activeKey) {
    const items = he ? HE_ITEMS : EN_ITEMS;
    header.dir = he ? 'rtl' : 'ltr';
    header.classList.add('bpi-shared-nav');
    header.classList.toggle('bpi-home-nav', activeKey === 'index' || activeKey === 'en');
    header.replaceChildren();

    const brand = document.createElement('div');
    brand.className = 'site-brand';

    const brandLink = document.createElement('a');
    brandLink.href = isInnerPage()
      ? (he ? '../../index.html' : '../../en.html')
      : (he ? 'index.html' : 'en.html');
    brandLink.textContent = 'Between Potential and Ideal';
    brand.appendChild(brandLink);

    const nav = document.createElement('nav');
    nav.className = 'site-nav';
    nav.setAttribute('aria-label', 'Primary navigation');
    nav.setAttribute('role', 'navigation');

    items.forEach(([label, file, itemKey]) => {
      const link = document.createElement('a');
      link.href = navHref(file, he);
      link.textContent = label;
      setActiveState(link, itemKey, activeKey);
      nav.appendChild(link);
    });

    const languageSwitch = document.createElement('a');
    languageSwitch.className = 'language-switch';
    languageSwitch.href = languageHref(he, activeKey);
    languageSwitch.textContent = he ? 'English' : 'עברית';
    languageSwitch.setAttribute(
      'aria-label',
      he ? 'Switch to the English version' : 'מעבר לגרסה העברית'
    );
    languageSwitch.title = he ? 'English version' : 'גרסה עברית';

    header.append(brand, nav, languageSwitch);
  }

  function renderNav() {
    const header = document.querySelector('header.site-header');
    if (!header) return;

    const he = isHebrew();
    const activeKey = pageKey();

    // Standard pages already contain the full navigation in their HTML.
    // Preserve those nodes so JavaScript never changes layout after first paint.
    if (!normalizeExistingHeader(header, he, activeKey)) {
      buildHeader(header, he, activeKey);
    }
  }

  function sanitizeBreadcrumbs() {
    const breadcrumbs = document.querySelectorAll(
      'main#main nav.breadcrumbs, main#main .breadcrumbs, main#main nav[aria-label="Breadcrumb"], nav.breadcrumbs, .breadcrumbs, nav[aria-label="Breadcrumb"]'
    );

    breadcrumbs.forEach((nav) => {
      nav.style.setProperty('color', '#0A3A68', 'important');
      nav.style.setProperty('background', 'transparent', 'important');
      nav.style.setProperty('background-image', 'none', 'important');
      nav.style.setProperty('box-shadow', 'none', 'important');
      nav.style.setProperty('text-shadow', 'none', 'important');
      nav.style.setProperty('opacity', '1', 'important');

      nav.querySelectorAll('a').forEach((link) => {
        link.classList.remove('active');
        link.removeAttribute('aria-current');
        link.style.setProperty('color', '#0A3A68', 'important');
        link.style.setProperty('-webkit-text-fill-color', '#0A3A68', 'important');
        link.style.setProperty('background', 'transparent', 'important');
        link.style.setProperty('background-image', 'none', 'important');
        link.style.setProperty('border', '0', 'important');
        link.style.setProperty('border-radius', '0', 'important');
        link.style.setProperty('box-shadow', 'none', 'important');
        link.style.setProperty('padding', '0', 'important');
        link.style.setProperty('margin', '0', 'important');
        link.style.setProperty('width', 'auto', 'important');
        link.style.setProperty('height', 'auto', 'important');
        link.style.setProperty('display', 'inline', 'important');
        link.style.setProperty('line-height', '1.35', 'important');
        link.style.setProperty('font-weight', '850', 'important');
        link.style.setProperty('transform', 'none', 'important');
      });
    });
  }

  function init() {
    sanitizeBreadcrumbs();
    renderNav();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init, { once: true });
  } else {
    init();
  }
})();
