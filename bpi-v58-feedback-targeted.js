(function(){
  'use strict';
  if (window.__bpiV58FeedbackLoaded) return;
  window.__bpiV58FeedbackLoaded = true;
  function norm(s){ return (s || '').replace(/\s+/g,' ').trim(); }
  function txt(el){ return norm(el && (el.innerText || el.textContent || '')); }
  function insideNav(el){ return !!(el && el.closest('nav,[role="navigation"],header,.site-nav,.top-nav,.main-nav,.nav,.tabs,.tabbar,.pill-nav,.nav-pills,.page-tabs')); }
  function isCritiqueNav(el){
    var t = txt(el).toLowerCase();
    if (!insideNav(el)) return false;
    return t === 'ביקורת' || t === 'critique' || t === 'criticism' || t === 'review';
  }
  function looksLikeFeedbackAction(el){
    if (!el) return false;
    if (el.hasAttribute('data-bpi-feedback-trigger') || el.getAttribute('data-feedback') === 'email') return true;
    if (insideNav(el)) return false;
    var t = txt(el);
    var href = (el.getAttribute && (el.getAttribute('href') || '') || '').toLowerCase();
    if (href.indexOf('mailto:') === 0) return true;
    return /(שלח\s*ביקורת|שליחת\s*ביקורת|פתח\s*תגובה\s*במייל|פתח\s*מייל|תגובה\s*במייל|send\s*feedback|submit\s*feedback|email\s*feedback|open\s*feedback)/i.test(t);
  }
  function pageEmail(){
    var direct = document.querySelector('[data-feedback-email],[data-bpi-feedback-email]');
    if (direct) return direct.getAttribute('data-feedback-email') || direct.getAttribute('data-bpi-feedback-email');
    var mail = document.querySelector('a[href^="mailto:"]');
    if (mail) return (mail.getAttribute('href') || '').replace(/^mailto:/i,'').split('?')[0];
    return 'barakbenhur@gmail.com';
  }
  function subject(){
    var lang = (document.documentElement.lang || '').toLowerCase();
    return lang.indexOf('he') === 0 ? 'ביקורת על Between Potential and Ideal' : 'Feedback on Between Potential and Ideal';
  }
  function gmailUrl(email, subj){ return 'https://mail.google.com/mail/?view=cm&fs=1&to=' + encodeURIComponent(email) + '&su=' + encodeURIComponent(subj); }
  function mailtoUrl(email, subj){ return 'mailto:' + encodeURIComponent(email) + '?subject=' + encodeURIComponent(subj); }
  function ensureModal(){
    var overlay = document.getElementById('bpi-v58-feedback-overlay');
    var modal = document.getElementById('bpi-v58-feedback-modal');
    if (overlay && modal) return {overlay:overlay, modal:modal};
    overlay = document.createElement('div'); overlay.id = 'bpi-v58-feedback-overlay'; overlay.hidden = true;
    modal = document.createElement('section'); modal.id = 'bpi-v58-feedback-modal'; modal.hidden = true;
    modal.setAttribute('role','dialog'); modal.setAttribute('aria-modal','true');
    var isHe = (document.documentElement.lang || '').toLowerCase().indexOf('he') === 0 || document.documentElement.dir === 'rtl';
    modal.dir = isHe ? 'rtl' : 'ltr';
    modal.innerHTML = isHe ?
      '<h2>שליחת ביקורת</h2><p>בחר איך לפתוח את ההודעה. זה מיועד במיוחד למחשבים שבהם אין אפליקציית מייל מוגדרת.</p><div class="bpi-v58-feedback-actions"><a class="bpi-v58-feedback-action" id="bpi-v58-gmail" target="_blank" rel="noopener">פתח ב-Gmail</a><a class="bpi-v58-feedback-action" id="bpi-v58-mailapp">פתח באפליקציית מייל</a><button type="button" id="bpi-v58-copy">העתק כתובת מייל</button></div><button type="button" id="bpi-v58-feedback-close">סגור</button>' :
      '<h2>Send feedback</h2><p>Choose how to open the message. This helps on desktop when no mail app is configured.</p><div class="bpi-v58-feedback-actions"><a class="bpi-v58-feedback-action" id="bpi-v58-gmail" target="_blank" rel="noopener">Open in Gmail</a><a class="bpi-v58-feedback-action" id="bpi-v58-mailapp">Open mail app</a><button type="button" id="bpi-v58-copy">Copy email address</button></div><button type="button" id="bpi-v58-feedback-close">Close</button>';
    document.body.appendChild(overlay); document.body.appendChild(modal);
    function close(){ overlay.hidden = true; modal.hidden = true; }
    overlay.addEventListener('click', close);
    modal.querySelector('#bpi-v58-feedback-close').addEventListener('click', close);
    document.addEventListener('keydown', function(e){ if(e.key === 'Escape') close(); });
    return {overlay:overlay, modal:modal};
  }
  function showMenu(){
    var email = pageEmail(); var subj = subject(); var m = ensureModal();
    var gmail = m.modal.querySelector('#bpi-v58-gmail');
    var mailapp = m.modal.querySelector('#bpi-v58-mailapp');
    var copy = m.modal.querySelector('#bpi-v58-copy');
    gmail.href = gmailUrl(email, subj);
    mailapp.href = mailtoUrl(email, subj);
    copy.onclick = function(){
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(email);
      copy.textContent = (m.modal.dir === 'rtl') ? 'הכתובת הועתקה' : 'Email copied';
      setTimeout(function(){ copy.textContent = (m.modal.dir === 'rtl') ? 'העתק כתובת מייל' : 'Copy email address'; }, 1500);
    };
    m.overlay.hidden = false; m.modal.hidden = false;
  }
  document.addEventListener('click', function(e){
    var el = e.target && e.target.closest && e.target.closest('a,button,[role="button"]');
    if (!el) return;
    if (isCritiqueNav(el)) {
      e.stopImmediatePropagation();
      return;
    }
    if (looksLikeFeedbackAction(el)) {
      e.preventDefault();
      e.stopImmediatePropagation();
      showMenu();
    }
  }, true);
})();
