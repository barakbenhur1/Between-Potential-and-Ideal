(function () {
  'use strict';

  const DEFAULT_EMAIL = 'barakbenhur@gmail.com';

  function pageLang() {
    const lang = (document.documentElement.getAttribute('lang') || '').toLowerCase();
    return lang.startsWith('he') || document.documentElement.getAttribute('dir') === 'rtl' ? 'he' : 'en';
  }

  function encodeMailSubject() {
    return pageLang() === 'he'
      ? 'ביקורת על בין פוטנציאל לאידיאל'
      : 'Feedback on Between Potential and Ideal';
  }

  function mailtoUrl(email, subject) {
    return 'mailto:' + encodeURIComponent(email) + '?subject=' + encodeURIComponent(subject);
  }

  function gmailUrl(email, subject) {
    return 'https://mail.google.com/mail/?view=cm&fs=1&to=' + encodeURIComponent(email) + '&su=' + encodeURIComponent(subject);
  }

  function extractEmailFromElement(el) {
    const href = el && el.closest ? (el.closest('a[href^="mailto:"]') || el).getAttribute?.('href') : '';
    if (href && href.startsWith('mailto:')) {
      const raw = href.slice('mailto:'.length).split('?')[0].trim();
      if (raw) return decodeURIComponent(raw);
    }
    return DEFAULT_EMAIL;
  }

  function isFeedbackTrigger(el) {
    if (!el || !el.closest) return false;
    const candidate = el.closest('a,button,[role="button"],.feedback-button,.feedback-link,.critique-button,.mail-button,[data-feedback],[data-mailto]');
    if (!candidate) return false;
    const text = (candidate.textContent || '').replace(/\s+/g, ' ').trim();
    const href = candidate.getAttribute && candidate.getAttribute('href');
    return Boolean(
      (href && href.startsWith('mailto:')) ||
      /שלח\s+ביקורת|פתח\s+תגובה\s+במייל|תגובה\s+במייל|ביקורת|send\s+feedback|send\s+critique|open\s+mail|email/i.test(text) ||
      candidate.hasAttribute('data-feedback') ||
      candidate.hasAttribute('data-mailto')
    ) ? candidate : false;
  }

  function ensureDialog() {
    let backdrop = document.querySelector('.bpi-feedback-dialog-backdrop');
    if (backdrop) return backdrop;

    const lang = pageLang();
    const rtl = lang === 'he';
    backdrop = document.createElement('div');
    backdrop.className = 'bpi-feedback-dialog-backdrop';
    backdrop.setAttribute('aria-hidden', 'true');
    backdrop.setAttribute('role', 'presentation');
    backdrop.innerHTML = `
      <div class="bpi-feedback-dialog" role="dialog" aria-modal="true" aria-labelledby="bpi-feedback-title" dir="${rtl ? 'rtl' : 'ltr'}">
        <h2 id="bpi-feedback-title">${rtl ? 'שליחת ביקורת' : 'Send feedback'}</h2>
        <p>${rtl ? 'בחר איך לפתוח את ההודעה. זה מיועד במיוחד למחשבים שבהם אין אפליקציית מייל מוגדרת.' : 'Choose how to open the message. This helps on desktop computers without a default mail app.'}</p>
        <div class="bpi-feedback-actions">
          <a class="bpi-feedback-gmail" target="_blank" rel="noopener">${rtl ? 'פתח ב־Gmail' : 'Open in Gmail'}</a>
          <a class="bpi-feedback-mailapp">${rtl ? 'פתח באפליקציית מייל' : 'Open mail app'}</a>
          <button type="button" class="bpi-feedback-copy">${rtl ? 'העתק כתובת מייל' : 'Copy email address'}</button>
        </div>
        <button type="button" class="bpi-feedback-close">${rtl ? 'סגור' : 'Close'}</button>
      </div>`;
    document.body.appendChild(backdrop);

    function close() {
      backdrop.setAttribute('aria-hidden', 'true');
    }
    backdrop.addEventListener('click', function (event) {
      if (event.target === backdrop || event.target.closest('.bpi-feedback-close')) close();
    });
    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape') close();
    });
    return backdrop;
  }

  function openFeedbackMenu(email, subject) {
    const backdrop = ensureDialog();
    const gmail = backdrop.querySelector('.bpi-feedback-gmail');
    const mailapp = backdrop.querySelector('.bpi-feedback-mailapp');
    const copy = backdrop.querySelector('.bpi-feedback-copy');
    gmail.href = gmailUrl(email, subject);
    mailapp.href = mailtoUrl(email, subject);
    copy.onclick = async function () {
      try {
        await navigator.clipboard.writeText(email);
        copy.textContent = pageLang() === 'he' ? 'הכתובת הועתקה' : 'Email copied';
      } catch (err) {
        window.prompt(pageLang() === 'he' ? 'העתק את הכתובת:' : 'Copy this address:', email);
      }
    };
    backdrop.setAttribute('aria-hidden', 'false');
    setTimeout(function () { gmail.focus(); }, 0);
  }

  function installFeedbackFallback() {
    document.addEventListener('click', function (event) {
      const candidate = isFeedbackTrigger(event.target);
      if (!candidate) return;
      const isDesktopLike = window.matchMedia && window.matchMedia('(hover: hover) and (pointer: fine)').matches;
      const href = candidate.getAttribute && candidate.getAttribute('href');

      // Keep mobile mailto behavior unless the trigger is not a real link/button target.
      if (!isDesktopLike && href && href.startsWith('mailto:')) return;

      event.preventDefault();
      event.stopPropagation();
      const email = extractEmailFromElement(candidate);
      const subject = encodeMailSubject();
      openFeedbackMenu(email, subject);
    }, true);
  }

  function fixMixedNistReferences() {
    const heTitle = 'ערכי CODATA ליחידות פלאנק וקבועי יסוד';
    const candidates = Array.from(document.querySelectorAll('li, p, div, span'))
      .filter(function (el) {
        const text = (el.textContent || '').replace(/\s+/g, ' ');
        return text.includes('CODATA') && text.includes('NIST');
      });

    candidates.forEach(function (el) {
      if (el.dataset && el.dataset.bpiNistFixed === '1') return;
      const text = (el.textContent || '').replace(/\s+/g, ' ').trim();
      if (!text.includes('CODATA') || !text.includes('NIST')) return;

      el.classList.add('bpi-rtl-mixed-reference-fix');
      el.setAttribute('dir', 'rtl');
      if (el.dataset) el.dataset.bpiNistFixed = '1';

      // If the DOM itself is reversed, repair the local HTML while preserving a simple existing link when possible.
      const anchor = Array.from(el.querySelectorAll('a')).find(function (a) {
        return (a.textContent || '').replace(/\s+/g, ' ').includes('CODATA');
      });
      if (anchor) {
        anchor.classList.add('bpi-ref-title-rtl');
        anchor.setAttribute('dir', 'rtl');
      }

      const hasExplicitFixedSource = el.querySelector('.bpi-ltr-source');
      if (!hasExplicitFixedSource) {
        // Wrap bare NIST text nodes in an LTR isolated span.
        const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT, {
          acceptNode: function (node) {
            return node.nodeValue && node.nodeValue.includes('NIST')
              ? NodeFilter.FILTER_ACCEPT
              : NodeFilter.FILTER_REJECT;
          }
        });
        const nodes = [];
        while (walker.nextNode()) nodes.push(walker.currentNode);
        nodes.forEach(function (node) {
          const frag = document.createDocumentFragment();
          node.nodeValue.split(/(NIST)/).forEach(function (part) {
            if (part === 'NIST') {
              const span = document.createElement('span');
              span.className = 'bpi-ltr-source';
              span.setAttribute('dir', 'ltr');
              span.textContent = 'NIST';
              frag.appendChild(span);
            } else if (part) {
              frag.appendChild(document.createTextNode(part));
            }
          });
          node.parentNode.replaceChild(frag, node);
        });
      }

      // If the visible order is caused by BiDi mixing, this isolation is enough. If the DOM order was literally
      // "NIST — Hebrew title", normalize simple text-only cases.
      if (!anchor && /^NIST\s*[–—-]\s*/.test(text) && text.includes(heTitle)) {
        el.innerHTML = '<span class="bpi-ref-title-rtl" dir="rtl">' + heTitle + '</span>' +
          '<span class="bpi-ref-separator" dir="ltr"> — </span>' +
          '<span class="bpi-ltr-source" dir="ltr">NIST</span>';
      }
    });
  }

  function run() {
    fixMixedNistReferences();
    installFeedbackFallback();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', run);
  } else {
    run();
  }
})();
