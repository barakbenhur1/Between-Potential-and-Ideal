(function () {
  'use strict';

  const GOLD_CLASS = 'bpi-final-html-gold';
  const FILL_CLASS = 'bpi-final-html-gold-fill';
  const LABEL_CLASS = 'bpi-final-html-gold-label';

  function normalizedHref(link) {
    return (link.getAttribute('href') || '').trim().toLowerCase();
  }

  function installFinalMobileTabbarCSS() {
    const id = 'bpi-final-mobile-tabbar-runtime-v4';
    const existing = document.getElementById(id);
    if (existing) existing.remove();

    const style = document.createElement('style');
    style.id = id;
    style.textContent = `
@media (max-width:860px){
  html,body{
    width:100%!important;
    max-width:100%!important;
    overflow-x:hidden!important;
  }

  html body.public-page header.site-header,
  html body.public-page .site-header,
  html body.public-page-he header.site-header,
  html body.public-page-en header.site-header{
    position:relative!important;
    inset:auto!important;
    width:100%!important;
    max-width:100vw!important;
    height:auto!important;
    min-height:0!important;
    max-height:none!important;
    display:flex!important;
    flex-direction:column!important;
    flex-wrap:nowrap!important;
    align-items:center!important;
    justify-content:center!important;
    gap:10px!important;
    margin:0!important;
    padding:12px 16px!important;
    box-sizing:border-box!important;
    overflow:visible!important;
    transform:none!important;
  }

  html body.public-page header.site-header .bpi-mobile-nav-toggle,
  html body.public-page .site-header .bpi-mobile-nav-toggle,
  html body.public-page-he header.site-header .bpi-mobile-nav-toggle,
  html body.public-page-en header.site-header .bpi-mobile-nav-toggle{
    display:none!important;
  }

  html body.public-page header.site-header .site-brand,
  html body.public-page .site-header .site-brand,
  html body.public-page-he header.site-header .site-brand,
  html body.public-page-en header.site-header .site-brand{
    order:1!important;
    grid-column:auto!important;
    justify-self:center!important;
    align-self:center!important;
    width:auto!important;
    min-width:0!important;
    max-width:100%!important;
    height:auto!important;
    margin:0!important;
    padding:0!important;
    text-align:center!important;
    overflow:visible!important;
  }

  html body.public-page header.site-header .site-brand>a,
  html body.public-page .site-header .site-brand>a,
  html body.public-page-he header.site-header .site-brand>a,
  html body.public-page-en header.site-header .site-brand>a{
    display:block!important;
    width:auto!important;
    max-width:calc(100vw - 32px)!important;
    font-size:15px!important;
    line-height:1.15!important;
    white-space:nowrap!important;
    overflow:hidden!important;
    text-overflow:ellipsis!important;
    text-align:center!important;
  }

  html body.public-page header.site-header nav.site-nav,
  html body.public-page header.site-header.bpi-mobile-nav-ready:not(.bpi-mobile-nav-open) nav.site-nav,
  html body.public-page header.site-header.bpi-mobile-nav-ready.bpi-mobile-nav-open nav.site-nav,
  html body.public-page .site-header nav.site-nav,
  html body.public-page-he header.site-header nav.site-nav,
  html body.public-page-en header.site-header nav.site-nav{
    order:2!important;
    grid-column:auto!important;
    justify-self:center!important;
    align-self:stretch!important;
    display:flex!important;
    flex-direction:row!important;
    flex-wrap:wrap!important;
    align-items:center!important;
    align-content:center!important;
    justify-content:center!important;
    gap:6px!important;
    width:100%!important;
    min-width:0!important;
    max-width:100%!important;
    height:auto!important;
    min-height:0!important;
    margin:0!important;
    padding:0!important;
    border:0!important;
    border-radius:0!important;
    background:transparent!important;
    box-shadow:none!important;
    overflow:visible!important;
    overflow-x:visible!important;
    overflow-y:visible!important;
    transform:none!important;
    scroll-snap-type:none!important;
  }

  html body.public-page header.site-header nav.site-nav>a,
  html body.public-page header.site-header nav.site-nav>a.active,
  html body.public-page header.site-header nav.site-nav>a[aria-current="page"],
  html body.public-page .site-header nav.site-nav>a,
  html body.public-page-he header.site-header nav.site-nav>a,
  html body.public-page-en header.site-header nav.site-nav>a{
    flex:0 1 auto!important;
    width:auto!important;
    min-width:0!important;
    max-width:100%!important;
    height:36px!important;
    min-height:36px!important;
    margin:0!important;
    padding:8px 10px!important;
    box-sizing:border-box!important;
    display:inline-flex!important;
    align-items:center!important;
    justify-content:center!important;
    font-size:12px!important;
    line-height:1.1!important;
    text-align:center!important;
    white-space:nowrap!important;
    overflow:visible!important;
    overflow-wrap:normal!important;
    word-break:normal!important;
    text-overflow:clip!important;
    transform:none!important;
    scroll-snap-align:none!important;
  }

  html body.public-page-he header.site-header nav.site-nav>a[href$="ai.html"],
  html body.public-page-he header.site-header nav.site-nav>a[href$="ai-as-witness.html"]{
    width:auto!important;
    min-width:0!important;
    max-width:100%!important;
    flex:0 1 auto!important;
    padding-inline:9px!important;
    font-size:11.5px!important;
  }

  html body.public-page header.site-header .language-switch,
  html body.public-page .site-header .language-switch,
  html body.public-page-he header.site-header .language-switch,
  html body.public-page-en header.site-header .language-switch{
    order:3!important;
    grid-column:auto!important;
    align-self:center!important;
    justify-self:center!important;
    width:auto!important;
    min-width:68px!important;
    max-width:none!important;
    height:36px!important;
    min-height:36px!important;
    margin:0!important;
    padding:7px 11px!important;
    box-sizing:border-box!important;
    white-space:nowrap!important;
  }
}

@media (max-width:390px){
  html body.public-page header.site-header,
  html body.public-page .site-header,
  html body.public-page-he header.site-header,
  html body.public-page-en header.site-header{
    gap:8px!important;
    padding:10px 9px!important;
  }

  html body.public-page header.site-header nav.site-nav,
  html body.public-page .site-header nav.site-nav,
  html body.public-page-he header.site-header nav.site-nav,
  html body.public-page-en header.site-header nav.site-nav{
    gap:5px!important;
  }

  html body.public-page header.site-header nav.site-nav>a,
  html body.public-page .site-header nav.site-nav>a,
  html body.public-page-he header.site-header nav.site-nav>a,
  html body.public-page-en header.site-header nav.site-nav>a{
    height:34px!important;
    min-height:34px!important;
    padding:7px 8px!important;
    font-size:11.5px!important;
  }
}
`;
    document.head.appendChild(style);
  }

  function removeDisclosureNavigation() {
    document.querySelectorAll('header.site-header').forEach((header) => {
      header.classList.remove('bpi-mobile-nav-ready', 'bpi-mobile-nav-open');
      header.querySelectorAll('.bpi-mobile-nav-toggle').forEach((toggle) => toggle.remove());
      const nav = header.querySelector('nav.site-nav');
      if (nav) nav.removeAttribute('aria-hidden');
    });
  }

  function isDocumentHtmlButton(link) {
    if (!(link instanceof HTMLAnchorElement)) return false;
    if (link.closest('.site-header, .site-nav, .site-brand, .language-switch, .breadcrumbs, table, .download-table')) return false;

    const href = normalizedHref(link);
    if (!href.includes('.html')) return false;

    const isButton = link.classList.contains('download-button') ||
      link.classList.contains('primary-format') ||
      link.classList.contains('html-format') ||
      link.classList.contains('is-html');

    if (!isButton) return false;

    return href.includes('/files/') ||
      href.startsWith('files/') ||
      href.startsWith('../files/') ||
      href.startsWith('../../files/') ||
      link.classList.contains('primary-format') ||
      link.classList.contains('html-format') ||
      link.classList.contains('is-html');
  }

  function ensureGoldStructure(link) {
    link.classList.add(GOLD_CLASS);

    let fill = link.querySelector(':scope > .' + FILL_CLASS);
    let label = link.querySelector(':scope > .' + LABEL_CLASS);

    if (!label) {
      label = document.createElement('span');
      label.className = LABEL_CLASS;
      const nodes = Array.from(link.childNodes).filter((node) => node !== fill);
      nodes.forEach((node) => label.appendChild(node));
      link.appendChild(label);
    }

    if (!fill) {
      fill = document.createElement('span');
      fill.className = FILL_CLASS;
      fill.setAttribute('aria-hidden', 'true');
      link.insertBefore(fill, label);
    }

    const gold = 'linear-gradient(135deg, #b98726 0%, #e6b84a 52%, #f5d06b 100%)';

    link.style.setProperty('position', 'relative', 'important');
    link.style.setProperty('isolation', 'isolate', 'important');
    link.style.setProperty('overflow', 'hidden', 'important');
    link.style.setProperty('display', 'inline-flex', 'important');
    link.style.setProperty('align-items', 'center', 'important');
    link.style.setProperty('justify-content', 'center', 'important');
    link.style.setProperty('background', gold, 'important');
    link.style.setProperty('background-color', '#e6b84a', 'important');
    link.style.setProperty('background-image', gold, 'important');
    link.style.setProperty('background-clip', 'border-box', 'important');
    link.style.setProperty('-webkit-background-clip', 'border-box', 'important');
    link.style.setProperty('-webkit-mask', 'none', 'important');
    link.style.setProperty('mask', 'none', 'important');
    link.style.setProperty('mix-blend-mode', 'normal', 'important');
    link.style.setProperty('color', '#07101d', 'important');
    link.style.setProperty('-webkit-text-fill-color', '#07101d', 'important');
    link.style.setProperty('border', '1.5px solid #d6a62a', 'important');
    link.style.setProperty('border-radius', '999px', 'important');
    link.style.setProperty('box-shadow', '0 8px 18px rgba(184,135,38,.22), inset 0 1px 0 rgba(255,255,255,.44)', 'important');
    link.style.setProperty('text-decoration', 'none', 'important');
    link.style.setProperty('text-shadow', 'none', 'important');
    link.style.setProperty('opacity', '1', 'important');
    link.style.setProperty('filter', 'none', 'important');

    fill.style.setProperty('position', 'absolute', 'important');
    fill.style.setProperty('inset', '0', 'important');
    fill.style.setProperty('z-index', '0', 'important');
    fill.style.setProperty('display', 'block', 'important');
    fill.style.setProperty('pointer-events', 'none', 'important');
    fill.style.setProperty('border-radius', 'inherit', 'important');
    fill.style.setProperty('background', gold, 'important');
    fill.style.setProperty('background-color', '#e6b84a', 'important');
    fill.style.setProperty('background-image', gold, 'important');
    fill.style.setProperty('opacity', '1', 'important');

    label.style.setProperty('position', 'relative', 'important');
    label.style.setProperty('z-index', '1', 'important');
    label.style.setProperty('background', 'transparent', 'important');
    label.style.setProperty('background-image', 'none', 'important');
    label.style.setProperty('color', '#07101d', 'important');
    label.style.setProperty('-webkit-text-fill-color', '#07101d', 'important');
    label.style.setProperty('text-shadow', 'none', 'important');
  }

  function styleDocumentHtmlButtons(root) {
    const scope = root && root.querySelectorAll ? root : document;
    scope.querySelectorAll('main#main a').forEach((link) => {
      if (isDocumentHtmlButton(link)) ensureGoldStructure(link);
    });
  }

  function findNavLink(nav, suffixes) {
    return Array.from(nav.querySelectorAll(':scope > a')).find((link) => {
      const href = normalizedHref(link);
      return suffixes.some((suffix) => href.endsWith(suffix));
    });
  }

  function putMethodologyBeforeCore() {
    document.querySelectorAll('header.site-header nav.site-nav').forEach((nav) => {
      const methodology = findNavLink(nav, ['methodology.html', 'methodology-en.html']);
      const core = findNavLink(nav, ['core.html', 'core-en.html']);
      if (methodology && core && methodology.nextElementSibling !== core) {
        nav.insertBefore(methodology, core);
      }
    });
  }

  function applyAll() {
    removeDisclosureNavigation();
    putMethodologyBeforeCore();
    styleDocumentHtmlButtons(document);
  }

  function observeChanges() {
    if (typeof MutationObserver === 'undefined') return;

    let scheduled = false;
    const observer = new MutationObserver((mutations) => {
      if (scheduled) return;
      const hasAddedNodes = mutations.some((mutation) => mutation.type === 'childList' && mutation.addedNodes.length);
      if (!hasAddedNodes) return;

      scheduled = true;
      window.requestAnimationFrame(() => {
        scheduled = false;
        applyAll();
      });
    });

    observer.observe(document.documentElement, { childList: true, subtree: true });
  }

  function init() {
    /* Loaded after the legacy navigation runtime. This style tag is appended last,
       so the approved homepage-style mobile tab bar wins over every older layer. */
    installFinalMobileTabbarCSS();
    applyAll();
    observeChanges();

    window.requestAnimationFrame(applyAll);
    window.setTimeout(applyAll, 120);
    window.setTimeout(applyAll, 500);
    window.setTimeout(applyAll, 1200);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init, { once: true });
  } else {
    init();
  }
})();
