(function () {
  'use strict';

  const LANGUAGE_NAMES = {
    he: 'עברית',
    en: 'English',
    tlh: 'tlhIngan Hol',
    qya: 'Neo-Quenya'
  };

  const LANGUAGE_ORDER = ['he', 'en', 'tlh', 'qya'];
  const STYLE_ID = 'bpi-four-language-runtime-guard-style';

  function installLayoutSafety() {
    if (document.getElementById(STYLE_ID)) return;

    const style = document.createElement('style');
    style.id = STYLE_ID;
    style.textContent = `
      .site-header .bpi-language-menu{
        grid-column:3!important;
        justify-self:end!important;
        align-self:center!important;
      }
      @media(max-width:860px){
        .site-header .bpi-language-menu{
          order:3!important;
          grid-column:auto!important;
          justify-self:center!important;
          align-self:center!important;
        }
      }
    `;
    document.head.appendChild(style);
  }

  function alternateHref(code) {
    const alternate = document.querySelector(`link[rel="alternate"][hreflang="${code}"]`);
    return alternate ? alternate.href : '';
  }

  function currentLanguage() {
    const code = (document.documentElement.lang || '').toLowerCase();
    return LANGUAGE_NAMES[code] ? code : 'en';
  }

  function buildMenu() {
    const current = currentLanguage();
    const details = document.createElement('details');
    details.className = 'bpi-language-menu';

    const summary = document.createElement('summary');
    summary.setAttribute('aria-label', 'Choose language');

    const icon = document.createElement('span');
    icon.className = 'bpi-language-menu-icon';
    icon.setAttribute('aria-hidden', 'true');
    icon.textContent = '🌐';

    const label = document.createElement('span');
    label.className = 'bpi-language-menu-current';
    label.textContent = LANGUAGE_NAMES[current];

    summary.append(icon, label);

    const panel = document.createElement('div');
    panel.className = 'bpi-language-menu-panel';

    LANGUAGE_ORDER.forEach((code) => {
      const href = alternateHref(code);
      if (!href) return;

      const link = document.createElement('a');
      link.className = 'bpi-language-option';
      link.href = href;
      link.hreflang = code;
      link.textContent = LANGUAGE_NAMES[code];
      if (code === current) link.setAttribute('aria-current', 'page');
      panel.appendChild(link);
    });

    details.append(summary, panel);
    return details;
  }

  function restoreMenu() {
    const header = document.querySelector('header.site-header');
    if (!header) return;

    const existing = header.querySelector('.bpi-language-menu');
    if (existing && existing.querySelectorAll('.bpi-language-option').length === 4) {
      header.querySelectorAll('.language-switch').forEach((node) => node.remove());
      return;
    }

    const menu = buildMenu();
    const oldSwitch = header.querySelector('.language-switch');
    const oldMenu = header.querySelector('.bpi-language-menu');

    if (oldSwitch) oldSwitch.replaceWith(menu);
    else if (oldMenu) oldMenu.replaceWith(menu);
    else header.appendChild(menu);
  }

  function init() {
    installLayoutSafety();
    restoreMenu();
    requestAnimationFrame(restoreMenu);
    setTimeout(restoreMenu, 120);
    setTimeout(restoreMenu, 600);

    const header = document.querySelector('header.site-header');
    if (!header || typeof MutationObserver === 'undefined') return;

    const observer = new MutationObserver(() => restoreMenu());
    observer.observe(header, { childList: true, subtree: false });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init, { once: true });
  } else {
    init();
  }
})();
