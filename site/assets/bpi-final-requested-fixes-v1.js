(function () {
  'use strict';

  const GOLD_CLASS = 'bpi-final-html-gold';
  const FILL_CLASS = 'bpi-final-html-gold-fill';
  const LABEL_CLASS = 'bpi-final-html-gold-label';

  function normalizedHref(link) {
    return (link.getAttribute('href') || '').trim().toLowerCase();
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
    putMethodologyBeforeCore();
    styleDocumentHtmlButtons(document);
  }

  function observeChanges() {
    if (typeof MutationObserver === 'undefined') return;

    const observer = new MutationObserver((mutations) => {
      let shouldReapply = false;
      for (const mutation of mutations) {
        if (mutation.type === 'childList' && mutation.addedNodes.length) {
          shouldReapply = true;
          break;
        }
      }
      if (shouldReapply) window.requestAnimationFrame(applyAll);
    });

    observer.observe(document.documentElement, { childList: true, subtree: true });
  }

  function init() {
    applyAll();
    observeChanges();

    window.requestAnimationFrame(applyAll);
    window.setTimeout(applyAll, 80);
    window.setTimeout(applyAll, 180);
    window.setTimeout(applyAll, 700);
    window.setTimeout(applyAll, 1500);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init, { once: true });
  } else {
    init();
  }
})();
