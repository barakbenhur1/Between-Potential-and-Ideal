(function () {
  'use strict';

  const heItems = [
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

  const enItems = [
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

  const heToEn = {
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

  const enToHe = {
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

  function currentPath() {
    return location.pathname || '';
  }

  function isHebrew() {
    return currentPath().includes('/pages/he/') ||
      currentPath().endsWith('/index.html') ||
      document.documentElement.dir === 'rtl';
  }

  function isInnerPage() {
    return currentPath().includes('/pages/he/') || currentPath().includes('/pages/en/');
  }

  function pageKey() {
    const fallback = isHebrew() ? 'index.html' : 'en.html';
    const filename = currentPath().split('/').pop() || fallback;
    return filename.replace('.html', '') || (isHebrew() ? 'index' : 'en');
  }

  function pageHref(file) {
    if (isInnerPage()) {
      if (file === 'index.html') return '../../index.html';
      if (file === 'en.html') return '../../en.html';
      return file;
    }

    if (isHebrew()) {
      return file === 'index.html' ? 'index.html' : 'pages/he/' + file;
    }

    return file === 'en.html' ? 'en.html' : 'pages/en/' + file;
  }

  function languageHref() {
    const current = pageKey();
    if (isHebrew()) {
      return isInnerPage()
        ? '../en/' + (heToEn[current] || 'en.html')
        : (heToEn[current] || 'en.html');
    }

    return isInnerPage()
      ? '../he/' + (enToHe[current] || 'index.html')
      : (enToHe[current] || 'index.html');
  }

  function replaceStyle(id, rules) {
    const existing = document.getElementById(id);
    if (existing) existing.remove();

    const style = document.createElement('style');
    style.id = id;
    style.textContent = rules.join('\n');
    document.head.appendChild(style);
  }

  function installFinalTabbarDimensions() {
    replaceStyle('bpi-final-tabbar-dimensions', [
      'html body.public-page .site-header{height:74px!important;min-height:74px!important;max-height:74px!important;display:grid!important;grid-template-columns:248px minmax(0,1080px) 104px!important;align-items:center!important;justify-content:center!important;column-gap:16px!important;padding:0 clamp(22px,2.4vw,36px)!important;box-sizing:border-box!important;overflow:visible!important;}',
      'html body.public-page-he .site-header{grid-template-columns:minmax(248px,1fr) minmax(0,1080px) minmax(248px,1fr)!important;justify-content:stretch!important;}',
      'html body.public-page-en .site-header{height:86px!important;min-height:86px!important;max-height:86px!important;grid-template-columns:300px minmax(0,1040px) 104px!important;}',
      'html body.public-page .site-header .site-brand{grid-column:1!important;justify-self:start!important;width:248px!important;min-width:248px!important;max-width:248px!important;white-space:nowrap!important;overflow:visible!important;}',
      'html body.public-page-en .site-header .site-brand{width:300px!important;min-width:300px!important;max-width:300px!important;}',
      'html body.public-page .site-header .site-brand a{font-family:ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif!important;font-size:16px!important;font-weight:800!important;line-height:1.05!important;letter-spacing:-.025em!important;white-space:nowrap!important;overflow:visible!important;text-overflow:clip!important;}',
      'html body.public-page .site-header .site-nav{grid-column:2!important;justify-self:center!important;width:100%!important;max-width:1080px!important;display:flex!important;flex-wrap:wrap!important;justify-content:center!important;align-items:center!important;align-content:center!important;text-align:center!important;margin-inline:auto!important;min-width:0!important;min-height:44px!important;gap:7px!important;overflow:visible!important;}',
      'html body.public-page-en .site-header .site-nav{max-width:1040px!important;gap:6px!important;}',
      'html body.public-page .site-header .site-nav a{min-height:36px!important;height:36px!important;padding:8px 13px!important;font-family:ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif!important;font-size:14px!important;font-weight:700!important;line-height:1.1!important;letter-spacing:0!important;box-sizing:border-box!important;white-space:nowrap!important;display:inline-flex!important;align-items:center!important;justify-content:center!important;}',
      'html body.public-page-he .site-header .site-nav a[href$="ai.html"],html body.public-page-he .site-header .site-nav a[href$="ai-as-witness.html"]{width:auto!important;min-width:0!important;max-width:none!important;flex:0 0 auto!important;padding-inline:9px!important;font-size:13px!important;line-height:1.1!important;white-space:nowrap!important;overflow:visible!important;text-overflow:clip!important;}',
      'html body.public-page-en .site-header .site-nav a{padding:8px 10px!important;font-size:13px!important;}',
      'html body.public-page .site-header .language-switch{grid-column:3!important;justify-self:end!important;width:104px!important;min-width:104px!important;max-width:104px!important;height:36px!important;min-height:36px!important;padding:8px 13px!important;font-family:ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif!important;font-size:14px!important;font-weight:700!important;line-height:1.1!important;box-sizing:border-box!important;white-space:nowrap!important;display:inline-flex!important;align-items:center!important;justify-content:center!important;}',
      '@media(max-width:1180px){html body.public-page-he .site-header{grid-template-columns:minmax(210px,1fr) minmax(0,1fr) minmax(210px,1fr)!important;}html body.public-page .site-header .site-brand{width:210px!important;min-width:210px!important;max-width:210px!important;}html body.public-page .site-header .language-switch{width:92px!important;min-width:92px!important;max-width:92px!important;}html body.public-page .site-header .site-nav a{font-size:13px!important;padding:8px 10px!important;}}',
      '@media(max-width:860px){html body.public-page .site-header,html body.public-page-en .site-header{height:auto!important;min-height:0!important;max-height:none!important;display:flex!important;flex-direction:column!important;gap:10px!important;padding:12px 16px!important;}html body.public-page .site-header .site-brand,html body.public-page-en .site-header .site-brand{width:auto!important;min-width:0!important;max-width:100%!important;}}'
    ]);
  }

  function installNavTextSafetyCSS() {
    replaceStyle('bpi-nav-text-safety-css', [
      'html body.public-page-he .site-header .site-nav a[href$="ai.html"],html body.public-page-he .site-header .site-nav a[href$="ai-as-witness.html"]{font-size:13px!important;line-height:1.1!important;color:inherit;}',
      'html body.public-page-he .site-header .site-nav a[href$="ai.html"]::before,html body.public-page-he .site-header .site-nav a[href$="ai.html"]::after,html body.public-page-he .site-header .site-nav a[href$="ai-as-witness.html"]::before,html body.public-page-he .site-header .site-nav a[href$="ai-as-witness.html"]::after{content:none!important;display:none!important;width:0!important;height:0!important;margin:0!important;padding:0!important;font-size:0!important;line-height:0!important;}'
    ]);
  }

  function installBreadcrumbSafetyCSS() {
    replaceStyle('bpi-breadcrumb-final-safety-css', [
      'html body.public-page nav.breadcrumbs,html body.public-page .breadcrumbs,html body.public-page nav[aria-label="Breadcrumb"]{color:#0A3A68!important;opacity:1!important;text-shadow:none!important;background:transparent!important;background-color:transparent!important;background-image:none!important;box-shadow:none!important;}',
      'html body.public-page nav.breadcrumbs *,html body.public-page .breadcrumbs *,html body.public-page nav[aria-label="Breadcrumb"] *{text-shadow:none!important;box-shadow:none!important;}',
      'html body.public-page nav.breadcrumbs a,html body.public-page .breadcrumbs a,html body.public-page nav[aria-label="Breadcrumb"] a,html body.public-page nav.breadcrumbs span,html body.public-page .breadcrumbs span,html body.public-page nav[aria-label="Breadcrumb"] span,html body.public-page nav.breadcrumbs [aria-current="page"],html body.public-page .breadcrumbs [aria-current="page"],html body.public-page nav[aria-label="Breadcrumb"] [aria-current="page"]{color:#0A3A68!important;-webkit-text-fill-color:#0A3A68!important;background:transparent!important;background-color:transparent!important;background-image:none!important;border:0!important;border-radius:0!important;box-shadow:none!important;outline:0!important;padding:0!important;margin:0!important;min-width:0!important;width:auto!important;max-width:none!important;min-height:0!important;height:auto!important;display:inline!important;line-height:1.35!important;font-weight:850!important;text-decoration:none!important;opacity:1!important;}',
      'html body.public-page nav.breadcrumbs a[href$="index.html"],html body.public-page .breadcrumbs a[href$="index.html"],html body.public-page nav[aria-label="Breadcrumb"] a[href$="index.html"],html body.public-page nav.breadcrumbs a:first-child,html body.public-page .breadcrumbs a:first-child,html body.public-page nav[aria-label="Breadcrumb"] a:first-child{color:#0A3A68!important;-webkit-text-fill-color:#0A3A68!important;background:transparent!important;background-color:transparent!important;background-image:none!important;border:0!important;border-radius:0!important;box-shadow:none!important;padding:0!important;}',
      'html body.public-page nav.breadcrumbs a.active,html body.public-page .breadcrumbs a.active,html body.public-page nav[aria-label="Breadcrumb"] a.active,html body.public-page nav.breadcrumbs .active,html body.public-page .breadcrumbs .active,html body.public-page nav[aria-label="Breadcrumb"] .active{color:#0A3A68!important;-webkit-text-fill-color:#0A3A68!important;background:transparent!important;background-color:transparent!important;background-image:none!important;border:0!important;border-radius:0!important;box-shadow:none!important;}',
      'html body.public-page nav.breadcrumbs a:hover,html body.public-page .breadcrumbs a:hover,html body.public-page nav[aria-label="Breadcrumb"] a:hover,html body.public-page nav.breadcrumbs a:focus-visible,html body.public-page .breadcrumbs a:focus-visible,html body.public-page nav[aria-label="Breadcrumb"] a:focus-visible{color:#062f56!important;-webkit-text-fill-color:#062f56!important;background:transparent!important;background-color:transparent!important;background-image:none!important;text-decoration:underline!important;box-shadow:none!important;}'
    ]);
  }

  function setActiveState(link, itemKey, activeKey) {
    const active = itemKey === activeKey;
    link.classList.toggle('active', active);
    if (active) link.setAttribute('aria-current', 'page');
    else link.removeAttribute('aria-current');
  }

  function normalizeExistingHebrewHeader(header, activeKey) {
    const brand = header.querySelector('.site-brand');
    const brandLink = brand && brand.querySelector('a');
    const nav = header.querySelector('.site-nav');
    const languageSwitch = header.querySelector('.language-switch');
    const links = nav ? Array.from(nav.querySelectorAll(':scope > a')) : [];

    if (!brand || !brandLink || !nav || !languageSwitch || links.length !== heItems.length) {
      return false;
    }

    header.dir = 'rtl';
    header.classList.add('bpi-shared-nav');
    header.classList.toggle('bpi-home-nav', activeKey === 'index');

    brandLink.href = isInnerPage() ? '../../index.html' : 'index.html';
    brandLink.textContent = 'Between Potential and Ideal';

    heItems.forEach(([label, file, itemKey], index) => {
      const link = links[index];
      link.href = pageHref(file);
      link.textContent = label;
      setActiveState(link, itemKey, activeKey);
    });

    languageSwitch.href = languageHref();
    languageSwitch.textContent = 'English';
    languageSwitch.setAttribute('aria-label', 'Switch to the English version');
    languageSwitch.title = 'English version';

    return true;
  }

  function buildHeader(header, he, activeKey) {
    const items = he ? heItems : enItems;
    header.dir = he ? 'rtl' : 'ltr';
    header.classList.add('bpi-shared-nav');
    header.classList.toggle('bpi-home-nav', activeKey === 'index' || activeKey === 'en');
    header.innerHTML = '';

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
      link.href = pageHref(file);
      link.textContent = label;
      setActiveState(link, itemKey, activeKey);
      nav.appendChild(link);
    });

    const languageSwitch = document.createElement('a');
    languageSwitch.className = 'language-switch';
    languageSwitch.href = languageHref();
    languageSwitch.textContent = he ? 'English' : 'עברית';
    languageSwitch.setAttribute(
      'aria-label',
      he ? 'Switch to the English version' : 'מעבר לגרסה העברית'
    );
    languageSwitch.title = he ? 'English version' : 'גרסה עברית';

    header.appendChild(brand);
    header.appendChild(nav);
    header.appendChild(languageSwitch);
  }

  function renderNav() {
    const header = document.querySelector('.site-header');
    if (!header) return;

    const he = isHebrew();
    const activeKey = pageKey();

    installFinalTabbarDimensions();
    installNavTextSafetyCSS();
    installBreadcrumbSafetyCSS();

    // Hebrew pages already contain the complete, correct navigation in the HTML.
    // Preserve those exact nodes instead of deleting/recreating the whole header.
    // This removes the final visible horizontal jump during DOMContentLoaded.
    if (he && normalizeExistingHebrewHeader(header, activeKey)) {
      return;
    }

    // English behaviour remains unchanged. Hebrew uses this only as a defensive
    // fallback if a future page is missing the expected shared navigation nodes.
    buildHeader(header, he, activeKey);
  }

  function sanitizeBreadcrumbs() {
    const crumbs = document.querySelectorAll(
      'main#main nav.breadcrumbs a, main#main .breadcrumbs a, main#main nav[aria-label="Breadcrumb"] a, nav.breadcrumbs a, .breadcrumbs a, nav[aria-label="Breadcrumb"] a'
    );

    crumbs.forEach((element) => {
      element.classList.remove('active');
      element.removeAttribute('aria-current');
      element.style.setProperty('color', '#0A3A68', 'important');
      element.style.setProperty('-webkit-text-fill-color', '#0A3A68', 'important');
      element.style.setProperty('background', 'transparent', 'important');
      element.style.setProperty('background-color', 'transparent', 'important');
      element.style.setProperty('background-image', 'none', 'important');
      element.style.setProperty('box-shadow', 'none', 'important');
      element.style.setProperty('border', '0', 'important');
      element.style.setProperty('border-radius', '0', 'important');
      element.style.setProperty('outline', '0', 'important');
      element.style.setProperty('padding', '0', 'important');
      element.style.setProperty('margin', '0', 'important');
      element.style.setProperty('min-width', '0', 'important');
      element.style.setProperty('width', 'auto', 'important');
      element.style.setProperty('max-width', 'none', 'important');
      element.style.setProperty('min-height', '0', 'important');
      element.style.setProperty('height', 'auto', 'important');
      element.style.setProperty('line-height', '1.35', 'important');
      element.style.setProperty('display', 'inline', 'important');
      element.style.setProperty('text-decoration', 'none', 'important');
      element.style.setProperty('text-shadow', 'none', 'important');
      element.style.setProperty('opacity', '1', 'important');
      element.style.setProperty('font-weight', '850', 'important');
    });

    document.querySelectorAll(
      'main#main nav.breadcrumbs, main#main .breadcrumbs, main#main nav[aria-label="Breadcrumb"], nav.breadcrumbs, .breadcrumbs, nav[aria-label="Breadcrumb"]'
    ).forEach((nav) => {
      nav.style.setProperty('color', '#0A3A68', 'important');
      nav.style.setProperty('background', 'transparent', 'important');
      nav.style.setProperty('background-color', 'transparent', 'important');
      nav.style.setProperty('background-image', 'none', 'important');
      nav.style.setProperty('box-shadow', 'none', 'important');
      nav.style.setProperty('text-shadow', 'none', 'important');
      nav.style.setProperty('opacity', '1', 'important');
    });
  }

  function init() {
    sanitizeBreadcrumbs();
    renderNav();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
