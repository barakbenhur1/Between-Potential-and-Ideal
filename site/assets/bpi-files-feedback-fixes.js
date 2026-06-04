(function(){
  'use strict';

  const heItems = [
    ['בית','index.html','index'],
    ['תקציר','summary.html','summary'],
    ['מילון','glossary.html','glossary'],
    ['מושגים','potential-ideal-optimal.html','potential-ideal-optimal'],
    ['בינה מלאכותית כעדות','ai-as-witness.html','ai-as-witness'],
    ['ליבה','core.html','core'],
    ['מתודולוגיה','methodology.html','methodology'],
    ['עדות','witness.html','witness'],
    ['יישום','applied.html','applied'],
    ['בינה מלאכותית','ai.html','ai'],
    ['קבצים','files.html','files'],
    ['ביקורת','critique.html','critique'],
    ['מקורות','sources.html','sources']
  ];

  const enItems = [
    ['Home','en.html','en'],
    ['Summary','summary-en.html','summary-en'],
    ['Glossary','glossary-en.html','glossary-en'],
    ['Concepts','potential-ideal-optimal-en.html','potential-ideal-optimal-en'],
    ['AI as Witness','ai-as-witness-en.html','ai-as-witness-en'],
    ['Core','core-en.html','core-en'],
    ['Methodology','methodology-en.html','methodology-en'],
    ['Witness','witness-en.html','witness-en'],
    ['Application','applied-en.html','applied-en'],
    ['AI','ai-en.html','ai-en'],
    ['Files','files-en.html','files-en'],
    ['Critique','critique-en.html','critique-en'],
    ['Sources','sources-en.html','sources-en']
  ];

  const heToEn = {
    index:'en.html', summary:'summary-en.html', glossary:'glossary-en.html',
    'potential-ideal-optimal':'potential-ideal-optimal-en.html', 'ai-as-witness':'ai-as-witness-en.html',
    core:'core-en.html', methodology:'methodology-en.html', witness:'witness-en.html',
    applied:'applied-en.html', ai:'ai-en.html', files:'files-en.html', critique:'critique-en.html', sources:'sources-en.html'
  };
  const enToHe = {
    en:'index.html', 'summary-en':'summary.html', 'glossary-en':'glossary.html',
    'potential-ideal-optimal-en':'potential-ideal-optimal.html', 'ai-as-witness-en':'ai-as-witness.html',
    'core-en':'core.html', 'methodology-en':'methodology.html', 'witness-en':'witness.html',
    'applied-en':'applied.html', 'ai-en':'ai.html', 'files-en':'files.html', 'critique-en':'critique.html', 'sources-en':'sources.html'
  };

  function path(){ return location.pathname || ''; }
  function isHe(){ return path().includes('/pages/he/') || path().endsWith('/index.html') || document.documentElement.dir === 'rtl'; }
  function isInner(){ return path().includes('/pages/he/') || path().includes('/pages/en/'); }
  function key(){
    const name = (path().split('/').pop() || (isHe() ? 'index.html' : 'en.html')).replace('.html','');
    return name || (isHe() ? 'index' : 'en');
  }
  function href(file){
    if (isInner()) return file === 'index.html' ? '../../index.html' : file === 'en.html' ? '../../en.html' : file;
    return isHe() ? (file === 'index.html' ? 'index.html' : 'pages/he/' + file) : (file === 'en.html' ? 'en.html' : 'pages/en/' + file);
  }
  function langHref(){
    const k = key();
    if (isHe()) return isInner() ? '../en/' + (heToEn[k] || 'en.html') : (heToEn[k] || 'en.html');
    return isInner() ? '../he/' + (enToHe[k] || 'index.html') : (enToHe[k] || 'index.html');
  }

  function enforceExactLabels(nav, he){
    nav.querySelectorAll('a').forEach(a => {
      const rawHref = (a.getAttribute('href') || '').split('?')[0].split('#')[0];
      if (he && rawHref.endsWith('ai.html')) a.textContent = 'בינה מלאכותית';
      if (he && rawHref.endsWith('ai-as-witness.html')) a.textContent = 'בינה מלאכותית כעדות';
      if (!he && rawHref.endsWith('ai-en.html')) a.textContent = 'AI';
      if (!he && rawHref.endsWith('ai-as-witness-en.html')) a.textContent = 'AI as Witness';
    });
  }

  function renderNav(){
    const header = document.querySelector('.site-header');
    if (!header) return;
    const he = isHe();
    const active = key();
    const items = he ? heItems : enItems;
    header.dir = he ? 'rtl' : 'ltr';
    header.classList.add('bpi-shared-nav');
    header.classList.toggle('bpi-home-nav', active === 'index' || active === 'en');
    header.innerHTML = '';

    const brand = document.createElement('div');
    brand.className = 'site-brand';
    const brandLink = document.createElement('a');
    brandLink.href = isInner() ? (he ? '../../index.html' : '../../en.html') : (he ? 'index.html' : 'en.html');
    brandLink.textContent = 'Between Potential and Ideal';
    brand.appendChild(brandLink);

    const nav = document.createElement('nav');
    nav.className = 'site-nav';
    nav.setAttribute('aria-label', 'Primary navigation');
    items.forEach(([label,file,itemKey]) => {
      const a = document.createElement('a');
      a.href = href(file);
      a.textContent = label;
      if (itemKey === active) {
        a.className = 'active';
        a.setAttribute('aria-current','page');
      }
      nav.appendChild(a);
    });
    enforceExactLabels(nav, he);

    const lang = document.createElement('a');
    lang.className = 'language-switch';
    lang.href = langHref();
    lang.textContent = he ? 'English' : 'עברית';

    header.appendChild(brand);
    header.appendChild(nav);
    header.appendChild(lang);
  }

  function init(){ renderNav(); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
