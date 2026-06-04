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

  function installFinalTabbarDimensions(){
    const old = document.getElementById('bpi-final-tabbar-dimensions');
    if (old) old.remove();
    const style = document.createElement('style');
    style.id = 'bpi-final-tabbar-dimensions';
    style.textContent = [
      'html body.public-page .site-header{height:74px!important;min-height:74px!important;max-height:74px!important;display:grid!important;grid-template-columns:248px minmax(0,1080px) 104px!important;align-items:center!important;justify-content:center!important;column-gap:16px!important;padding:0 clamp(22px,2.4vw,36px)!important;box-sizing:border-box!important;overflow:visible!important;}',
      'html body.public-page-en .site-header{height:86px!important;min-height:86px!important;max-height:86px!important;grid-template-columns:300px minmax(0,1040px) 104px!important;}',
      'html body.public-page .site-header .site-brand{grid-column:1!important;justify-self:start!important;width:248px!important;min-width:248px!important;max-width:248px!important;white-space:nowrap!important;overflow:visible!important;}',
      'html body.public-page-en .site-header .site-brand{width:300px!important;min-width:300px!important;max-width:300px!important;}',
      'html body.public-page .site-header .site-brand a{font-family:ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif!important;font-size:16px!important;font-weight:800!important;line-height:1.05!important;letter-spacing:-.025em!important;white-space:nowrap!important;overflow:visible!important;text-overflow:clip!important;}',
      'html body.public-page .site-header .site-nav{grid-column:2!important;justify-self:center!important;width:100%!important;max-width:1080px!important;display:flex!important;flex-wrap:wrap!important;justify-content:center!important;align-items:center!important;align-content:center!important;text-align:center!important;margin-left:auto!important;margin-right:auto!important;min-width:0!important;min-height:44px!important;gap:7px!important;overflow:visible!important;}',
      'html body.public-page-en .site-header .site-nav{max-width:1040px!important;gap:6px!important;}',
      'html body.public-page .site-header .site-nav a{min-height:36px!important;height:36px!important;padding:8px 13px!important;font-family:ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif!important;font-size:14px!important;font-weight:700!important;line-height:1.1!important;letter-spacing:0!important;box-sizing:border-box!important;white-space:nowrap!important;display:inline-flex!important;align-items:center!important;justify-content:center!important;}',
      'html body.public-page-en .site-header .site-nav a{padding:8px 10px!important;font-size:13px!important;}',
      'html body.public-page .site-header .language-switch{grid-column:3!important;justify-self:end!important;width:104px!important;min-width:104px!important;max-width:104px!important;height:36px!important;min-height:36px!important;padding:8px 13px!important;font-family:ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif!important;font-size:14px!important;font-weight:700!important;line-height:1.1!important;box-sizing:border-box!important;white-space:nowrap!important;display:inline-flex!important;align-items:center!important;justify-content:center!important;}',
      '@media(max-width:1180px){html body.public-page .site-header{grid-template-columns:210px minmax(0,1fr) 92px!important;}html body.public-page .site-header .site-brand{width:210px!important;min-width:210px!important;max-width:210px!important;}html body.public-page .site-header .language-switch{width:92px!important;min-width:92px!important;max-width:92px!important;}html body.public-page .site-header .site-nav a{font-size:13px!important;padding:8px 10px!important;}}',
      '@media(max-width:860px){html body.public-page .site-header,html body.public-page-en .site-header{height:auto!important;min-height:0!important;max-height:none!important;display:flex!important;flex-direction:column!important;gap:10px!important;padding:12px 16px!important;}html body.public-page .site-header .site-brand,html body.public-page-en .site-header .site-brand{width:auto!important;min-width:0!important;max-width:100%!important;}}'
    ].join('\n');
    document.head.appendChild(style);
  }

  function installNavTextSafetyCSS(){
    if (document.getElementById('bpi-nav-text-safety-css')) return;
    const style = document.createElement('style');
    style.id = 'bpi-nav-text-safety-css';
    style.textContent = [
      'body.public-page-he .site-nav a[href="ai.html"]{font-size:14px!important;line-height:1.1!important;color:inherit;}',
      'body.public-page-he .site-nav a[href="ai.html"]::before,body.public-page-he .site-nav a[href="ai.html"]::after{content:none!important;display:none!important;font-size:0!important;line-height:0!important;}',
      'body.public-page-he .site-nav a[href="ai-as-witness.html"]::before,body.public-page-he .site-nav a[href="ai-as-witness.html"]::after{content:none!important;display:none!important;font-size:0!important;line-height:0!important;}'
    ].join('\n');
    document.head.appendChild(style);
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
    installNavTextSafetyCSS();
    installFinalTabbarDimensions();
    enforceExactLabels(nav, he);
  }

  function init(){ installNavTextSafetyCSS(); installFinalTabbarDimensions(); renderNav(); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
