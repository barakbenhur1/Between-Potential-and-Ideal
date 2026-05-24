(function () {
  const DEFAULT_TO = 'barakbenhur@gmail.com';
  const DEFAULT_SUBJECT = 'תגובה על Between Potential and Ideal';

  function enc(value) { return encodeURIComponent(value || ''); }
  function findMailTarget(el) {
    const explicit = el.getAttribute('data-email') || el.getAttribute('data-to');
    if (explicit) return explicit;
    const href = el.getAttribute('href') || '';
    const mailto = href.match(/^mailto:([^?]+)/i);
    if (mailto) return decodeURIComponent(mailto[1]);
    return DEFAULT_TO;
  }
  function findSubject(el) {
    const explicit = el.getAttribute('data-subject');
    if (explicit) return explicit;
    const href = el.getAttribute('href') || '';
    const subject = href.match(/[?&]subject=([^&]+)/i);
    if (subject) return decodeURIComponent(subject[1].replace(/\+/g, ' '));
    const title = document.title || 'Between Potential and Ideal';
    return DEFAULT_SUBJECT + ' — ' + title;
  }
  function removePanel() {
    const old = document.querySelector('.bpi-mail-choice-panel');
    if (old) old.remove();
  }
  function showPanel(trigger) {
    removePanel();
    const to = findMailTarget(trigger);
    const subject = findSubject(trigger);
    const body = 'שלום,\n\nרציתי להגיב על: ' + (document.title || location.href) + '\n' + location.href + '\n\n';
    const mailto = 'mailto:' + enc(to) + '?subject=' + enc(subject) + '&body=' + enc(body);
    const gmail = 'https://mail.google.com/mail/?view=cm&fs=1&to=' + enc(to) + '&su=' + enc(subject) + '&body=' + enc(body);

    const panel = document.createElement('aside');
    panel.className = 'bpi-mail-choice-panel';
    panel.setAttribute('role', 'dialog');
    panel.setAttribute('aria-modal', 'false');
    panel.innerHTML = [
      '<h2>איך לפתוח תגובה?</h2>',
      '<p>בחר פתיחה דרך Gmail בדפדפן או דרך אפליקציית המייל של המחשב.</p>',
      '<div class="bpi-mail-choice-actions">',
      '<a class="primary" target="_blank" rel="noopener noreferrer" href="' + gmail + '">פתח ב-Gmail</a>',
      '<a href="' + mailto + '">פתח באפליקציית מייל</a>',
      '<button type="button" data-bpi-copy-mail>העתק כתובת</button>',
      '<button type="button" data-bpi-close>סגור</button>',
      '</div>'
    ].join('');
    document.body.appendChild(panel);
    const copy = panel.querySelector('[data-bpi-copy-mail]');
    copy.addEventListener('click', async function () {
      try { await navigator.clipboard.writeText(to); copy.textContent = 'הועתק'; }
      catch (e) { copy.textContent = to; }
    });
    panel.querySelector('[data-bpi-close]').addEventListener('click', removePanel);
  }

  document.addEventListener('click', function (event) {
    const target = event.target.closest('a,button');
    if (!target) return;
    const text = (target.textContent || '').trim();
    const href = target.getAttribute('href') || '';
    const cls = target.className || '';
    const isMail = /^mailto:/i.test(href) || /mail|email|gmail|תגובה|respond|response/i.test(text + ' ' + cls);
    if (!isMail) return;
    if (target.hasAttribute('data-bpi-direct-mail')) return;
    event.preventDefault();
    showPanel(target);
  });
})();
