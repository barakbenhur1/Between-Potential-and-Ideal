(function () {
  'use strict';
  const DEFAULT_EMAIL = 'barakbenhur@gmail.com';
  const HE_TITLE = 'ערכי CODATA ליחידות פלאנק וקבועי יסוד';

  function isHebrewPage() {
    const html = document.documentElement;
    const lang = (html.getAttribute('lang') || '').toLowerCase();
    return lang.startsWith('he') || html.getAttribute('dir') === 'rtl';
  }
  function subject() {
    return isHebrewPage() ? 'ביקורת על בין פוטנציאל לאידיאל' : 'Feedback on Between Potential and Ideal';
  }
  function mailto(email) {
    return 'mailto:' + encodeURIComponent(email) + '?subject=' + encodeURIComponent(subject());
  }
  function gmail(email) {
    return 'https://mail.google.com/mail/?view=cm&fs=1&to=' + encodeURIComponent(email) + '&su=' + encodeURIComponent(subject());
  }
  function triggerFrom(target) {
    const el = target && target.closest && target.closest('a,button,[role="button"],[data-feedback],[data-mailto],.feedback-button,.feedback-link,.mail-button,.critique-button');
    if (!el) return null;
    const text = (el.textContent || '').replace(/\s+/g, ' ').trim();
    const href = el.getAttribute && (el.getAttribute('href') || '');
    const explicit = el.hasAttribute('data-feedback') || el.hasAttribute('data-mailto') || (href && href.startsWith('mailto:'));
    const byText = /שלח\s+ביקורת|שליחת\s+ביקורת|פתח\s+תגובה\s+במייל|תגובה\s+במייל|send\s+feedback|send\s+critique|open\s+mail|email\s+feedback/i.test(text);
    return explicit || byText ? el : null;
  }
  function emailFrom(el) {
    const data = el.getAttribute && (el.getAttribute('data-mailto') || el.getAttribute('data-email'));
    if (data && data.includes('@')) return data.trim();
    const href = el.getAttribute && (el.getAttribute('href') || '');
    if (href.startsWith('mailto:')) {
      const raw = href.slice(7).split('?')[0].trim();
      if (raw) return decodeURIComponent(raw);
    }
    return DEFAULT_EMAIL;
  }
  function ensureDialog() {
    let backdrop = document.querySelector('.bpi-v55-feedback-backdrop');
    if (backdrop) return backdrop;
    const he = isHebrewPage();
    backdrop = document.createElement('div');
    backdrop.className = 'bpi-v55-feedback-backdrop';
    backdrop.setAttribute('data-open', '0');
    backdrop.innerHTML = `
      <div class="bpi-v55-feedback-dialog" role="dialog" aria-modal="true" dir="${he ? 'rtl' : 'ltr'}" aria-labelledby="bpi-v55-feedback-title">
        <h2 id="bpi-v55-feedback-title">${he ? 'שליחת ביקורת' : 'Send feedback'}</h2>
        <p>${he ? 'בחר איך לפתוח את ההודעה. זה מיועד במיוחד למחשבים שבהם אין אפליקציית מייל מוגדרת.' : 'Choose how to open the message. This helps on desktop computers without a configured default mail app.'}</p>
        <div class="bpi-v55-feedback-actions">
          <a class="bpi-v55-gmail" target="_blank" rel="noopener">${he ? 'פתח ב־Gmail' : 'Open in Gmail'}</a>
          <a class="bpi-v55-mailapp">${he ? 'פתח באפליקציית מייל' : 'Open mail app'}</a>
          <button type="button" class="bpi-v55-copy">${he ? 'העתק כתובת מייל' : 'Copy email address'}</button>
        </div>
        <button type="button" class="bpi-v55-feedback-close">${he ? 'סגור' : 'Close'}</button>
      </div>`;
    document.body.appendChild(backdrop);
    function close() { backdrop.setAttribute('data-open', '0'); }
    backdrop.addEventListener('click', function (event) {
      if (event.target === backdrop || event.target.closest('.bpi-v55-feedback-close')) close();
    });
    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape') close();
    });
    return backdrop;
  }
  function openDialog(email) {
    const backdrop = ensureDialog();
    const gm = backdrop.querySelector('.bpi-v55-gmail');
    const ma = backdrop.querySelector('.bpi-v55-mailapp');
    const cp = backdrop.querySelector('.bpi-v55-copy');
    gm.href = gmail(email);
    ma.href = mailto(email);
    cp.onclick = async function () {
      try {
        await navigator.clipboard.writeText(email);
        cp.textContent = isHebrewPage() ? 'הכתובת הועתקה' : 'Email copied';
      } catch (e) {
        window.prompt(isHebrewPage() ? 'העתק את הכתובת:' : 'Copy this address:', email);
      }
    };
    backdrop.setAttribute('data-open', '1');
    setTimeout(function () { gm.focus(); }, 0);
  }
  function installFeedback() {
    document.addEventListener('click', function (event) {
      const el = triggerFrom(event.target);
      if (!el) return;
      const href = el.getAttribute && (el.getAttribute('href') || '');
      const desktop = window.matchMedia && window.matchMedia('(hover: hover) and (pointer: fine)').matches;
      if (!desktop && href.startsWith('mailto:')) return; // mobile already works.
      event.preventDefault();
      event.stopPropagation();
      openDialog(emailFrom(el));
    }, true);
  }
  function fixNist() {
    if (!isHebrewPage()) return;
    const candidates = Array.from(document.querySelectorAll('li,p,div'))
      .filter(el => {
        const t = (el.textContent || '').replace(/\s+/g, ' ').trim();
        return t.includes('NIST') && t.includes('CODATA') && t.length < 260;
      });
    candidates.forEach(function (el) {
      if (el.dataset.bpiV55Nist === '1') return;
      const anchor = Array.from(el.querySelectorAll('a')).find(a => (a.textContent || '').includes('CODATA') || (a.href || '').toLowerCase().includes('nist'));
      const href = anchor ? anchor.getAttribute('href') : '';
      el.dataset.bpiV55Nist = '1';
      el.classList.add('bpi-v55-nist-fixed-line');
      el.setAttribute('dir', 'rtl');
      const titleHtml = href
        ? `<a class="bpi-v55-nist-title" dir="rtl" href="${href}">${HE_TITLE}</a>`
        : `<span class="bpi-v55-nist-title" dir="rtl">${HE_TITLE}</span>`;
      el.innerHTML = `${titleHtml}<span class="bpi-v55-nist-sep" dir="ltr"> — </span><span class="bpi-v55-nist-source" dir="ltr">NIST</span>`;
    });
  }
  function run() { fixNist(); installFeedback(); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run);
  else run();
})();
