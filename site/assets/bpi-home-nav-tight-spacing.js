(function(){
  'use strict';

  function install(){
    if (!document.body || !document.body.classList.contains('public-page-he') || !document.body.classList.contains('bpi-home-page')) return;
    var old = document.getElementById('bpi-home-nav-tight-spacing-final');
    if (old) old.remove();
    var style = document.createElement('style');
    style.id = 'bpi-home-nav-tight-spacing-final';
    style.textContent = [
      'html body.public-page-he.bpi-home-page .site-header .site-nav{gap:2px!important;column-gap:2px!important;row-gap:2px!important;}',
      'html body.public-page-he.bpi-home-page .site-header .site-nav a{padding-left:7px!important;padding-right:7px!important;padding-inline:7px!important;}',
      '@media(max-width:1180px){html body.public-page-he.bpi-home-page .site-header .site-nav{gap:2px!important;column-gap:2px!important;row-gap:2px!important;}html body.public-page-he.bpi-home-page .site-header .site-nav a{padding-left:6px!important;padding-right:6px!important;padding-inline:6px!important;}}'
    ].join('\n');
    document.head.appendChild(style);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', install);
  else install();
  window.addEventListener('load', install);
  setTimeout(install, 50);
  setTimeout(install, 250);
})();
