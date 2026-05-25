(function(){
  'use strict';
  var EMAIL = 'barakbenhur@gmail.com';
  var HE_NIST_TITLE = 'ערכי CODATA ליחידות פלאנק וקבועי יסוד';
  var isHe = (document.documentElement.dir === 'rtl') || ((document.documentElement.lang || '').toLowerCase().indexOf('he') === 0);

  function enc(s){ return encodeURIComponent(s || ''); }
  function textOf(el){ return ((el && el.textContent) || '').replace(/\s+/g,' ').trim(); }
  function isFeedbackTrigger(el){
    if (!el) return false;
    var t = textOf(el).toLowerCase();
    var href = (el.getAttribute && (el.getAttribute('href') || '')) || '';
    return href.indexOf('mailto:') === 0 ||
      /שלח\s+ביקורת|שליחת\s+ביקורת|פתח\s+תגובה|תגובה\s+במייל|send\s+feedback|send\s+critique|open\s+feedback|email\s+feedback/i.test(t);
  }
  function subject(){ return isHe ? 'ביקורת על בין פוטנציאל לאידיאל' : 'Feedback on Between Potential and Ideal'; }
  function body(){ return isHe ? 'שלום,\n\nרציתי לשלוח ביקורת / הערה על האתר:\n' + location.href + '\n\n' : 'Hello,\n\nI wanted to send feedback about the site:\n' + location.href + '\n\n'; }
  function gmailUrl(){ return 'https://mail.google.com/mail/?view=cm&fs=1&to=' + enc(EMAIL) + '&su=' + enc(subject()) + '&body=' + enc(body()); }
  function mailtoUrl(){ return 'mailto:' + EMAIL + '?subject=' + enc(subject()) + '&body=' + enc(body()); }

  function removeOldBackdrops(){
    document.querySelectorAll('.bpi-v54-feedback-backdrop,.bpi-v55-feedback-backdrop,.bpi-v56-feedback-backdrop').forEach(function(x){ x.remove(); });
  }
  function ensureMenu(){
    removeOldBackdrops();
    var existing = document.querySelector('.bpi-v57-feedback-backdrop');
    if (existing) return existing;
    var wrap = document.createElement('div');
    wrap.className = 'bpi-v57-feedback-backdrop';
    wrap.hidden = true;
    wrap.setAttribute('aria-hidden','true');
    wrap.innerHTML = ''+
      '<div class="bpi-v57-feedback-dialog" role="dialog" aria-modal="true" aria-labelledby="bpi-v57-feedback-title">'+
        '<h2 id="bpi-v57-feedback-title">'+(isHe?'שליחת ביקורת':'Send feedback')+'</h2>'+ 
        '<p>'+(isHe?'בחר איך לפתוח את ההודעה. זה מיועד במיוחד למחשבים שבהם אין אפליקציית מייל מוגדרת.':'Choose how to open the message. This helps on computers without a default mail app.')+'</p>'+ 
        '<div class="bpi-v57-feedback-actions">'+
          '<a class="bpi-v57-open-gmail" target="_blank" rel="noopener">'+(isHe?'פתח ב־Gmail':'Open in Gmail')+'</a>'+ 
          '<a class="bpi-v57-open-mail">'+(isHe?'פתח באפליקציית מייל':'Open in mail app')+'</a>'+ 
          '<button type="button" class="bpi-v57-copy-email">'+(isHe?'העתק כתובת מייל':'Copy email address')+'</button>'+ 
        '</div>'+ 
        '<div class="bpi-v57-feedback-toast" aria-live="polite"></div>'+ 
        '<button type="button" class="bpi-v57-feedback-close">'+(isHe?'סגור':'Close')+'</button>'+ 
      '</div>';
    document.body.appendChild(wrap);
    wrap.querySelector('.bpi-v57-open-gmail').setAttribute('href', gmailUrl());
    wrap.querySelector('.bpi-v57-open-mail').setAttribute('href', mailtoUrl());
    wrap.querySelector('.bpi-v57-copy-email').addEventListener('click', function(){
      var toast = wrap.querySelector('.bpi-v57-feedback-toast');
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(EMAIL).then(function(){ toast.textContent = isHe ? 'כתובת המייל הועתקה.' : 'Email copied.'; }, function(){ toast.textContent = EMAIL; });
      } else { toast.textContent = EMAIL; }
    });
    wrap.querySelector('.bpi-v57-feedback-close').addEventListener('click', closeMenu);
    wrap.addEventListener('click', function(e){ if (e.target === wrap) closeMenu(); });
    document.addEventListener('keydown', function(e){ if(e.key === 'Escape') closeMenu(); });
    return wrap;
  }
  function openMenu(){
    var wrap = ensureMenu();
    wrap.hidden = false;
    wrap.setAttribute('data-open','true');
    wrap.setAttribute('aria-hidden','false');
    var first = wrap.querySelector('.bpi-v57-open-gmail');
    if (first) setTimeout(function(){ first.focus(); }, 0);
  }
  function closeMenu(){
    var wrap = document.querySelector('.bpi-v57-feedback-backdrop');
    if (!wrap) return;
    wrap.hidden = true;
    wrap.removeAttribute('data-open');
    wrap.setAttribute('aria-hidden','true');
  }
  function attachFeedback(){
    ensureMenu();
    Array.prototype.slice.call(document.querySelectorAll('a,button,[role="button"]')).forEach(function(el){
      if (!isFeedbackTrigger(el)) return;
      if (el.dataset.bpiV57FeedbackBound === '1') return;
      el.dataset.bpiV57FeedbackBound = '1';
      el.addEventListener('click', function(e){
        e.preventDefault();
        e.stopPropagation();
        openMenu();
      }, true);
    });
  }
  function fixNist(){
    if (!isHe) return;
    Array.prototype.slice.call(document.querySelectorAll('li,p,div')).forEach(function(el){
      var t = textOf(el);
      if (!(t.indexOf('NIST') >= 0 && t.indexOf('CODATA') >= 0 && t.length < 260)) return;
      var a = Array.prototype.slice.call(el.querySelectorAll('a')).filter(function(x){
        return textOf(x).indexOf('CODATA') >= 0 || ((x.getAttribute('href') || '').toLowerCase().indexOf('nist') >= 0);
      })[0];
      var href = a ? a.getAttribute('href') : '';
      el.classList.add('bpi-v57-nist-fixed-line');
      el.setAttribute('dir','rtl');
      el.innerHTML = (href ? '<a class="bpi-v57-nist-title" dir="rtl" href="'+href+'">'+HE_NIST_TITLE+'</a>' : '<span class="bpi-v57-nist-title" dir="rtl">'+HE_NIST_TITLE+'</span>') + '<span class="bpi-v57-nist-sep" dir="ltr"> — </span><span class="bpi-v57-nist-source" dir="ltr">NIST</span>';
    });
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function(){ fixNist(); attachFeedback(); });
  } else { fixNist(); attachFeedback(); }
})();
