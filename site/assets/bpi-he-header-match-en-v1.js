(function () {
  'use strict';

  const STYLE_ID = 'bpi-he-mobile-header-runtime-v3';

  function installHebrewMobileHeaderFix() {
    document.getElementById(STYLE_ID)?.remove();

    const style = document.createElement('style');
    style.id = STYLE_ID;
    style.textContent = `
/* Hebrew mobile only. No English selectors and no desktop/tablet rules. */
@media (max-width:860px){
  html[lang="he"] body.public-page-he header.site-header,
  html[lang="he"] body.public-page-he .site-header{
    direction:ltr!important;
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
    overflow-x:hidden!important;
    overflow-y:visible!important;
    transform:none!important;
    translate:none!important;
  }

  html[lang="he"] body.public-page-he header.site-header .site-brand,
  html[lang="he"] body.public-page-he .site-header .site-brand{
    order:1!important;
    align-self:center!important;
    justify-self:center!important;
    width:auto!important;
    min-width:0!important;
    max-width:100%!important;
    height:auto!important;
    margin:0!important;
    padding:0!important;
    direction:ltr!important;
    text-align:center!important;
    overflow:visible!important;
    transform:none!important;
  }

  html[lang="he"] body.public-page-he header.site-header .site-brand>a,
  html[lang="he"] body.public-page-he .site-header .site-brand>a{
    display:block!important;
    width:auto!important;
    max-width:calc(100vw - 32px)!important;
    margin:0!important;
    padding:0!important;
    direction:ltr!important;
    unicode-bidi:isolate!important;
    font-size:15px!important;
    line-height:1.15!important;
    text-align:center!important;
    white-space:nowrap!important;
    overflow:hidden!important;
    text-overflow:ellipsis!important;
    transform:none!important;
  }

  html[lang="he"] body.public-page-he header.site-header nav.site-nav,
  html[lang="he"] body.public-page-he .site-header nav.site-nav{
    direction:rtl!important;
    order:2!important;
    align-self:center!important;
    justify-self:center!important;
    width:100%!important;
    min-width:0!important;
    max-width:100%!important;
    height:auto!important;
    min-height:0!important;
    max-height:none!important;
    margin:0!important;
    padding:0!important;
    display:flex!important;
    flex-direction:row!important;
    flex-wrap:wrap!important;
    align-items:center!important;
    align-content:center!important;
    justify-content:center!important;
    gap:6px!important;
    overflow-x:hidden!important;
    overflow-y:visible!important;
    overscroll-behavior-x:none!important;
    touch-action:pan-y!important;
    transform:none!important;
  }

  html[lang="he"] body.public-page-he header.site-header nav.site-nav>a,
  html[lang="he"] body.public-page-he .site-header nav.site-nav>a,
  html[lang="he"] body.public-page-he header.site-header nav.site-nav>a[href$="ai.html"],
  html[lang="he"] body.public-page-he header.site-header nav.site-nav>a[href$="ai-as-witness.html"]{
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
    overflow:hidden!important;
    text-overflow:clip!important;
    transform:none!important;
  }

  html[lang="he"] body.public-page-he header.site-header .language-switch,
  html[lang="he"] body.public-page-he .site-header .language-switch{
    direction:ltr!important;
    order:3!important;
    align-self:center!important;
    justify-self:center!important;
    width:auto!important;
    min-width:68px!important;
    max-width:100%!important;
    height:36px!important;
    min-height:36px!important;
    margin:0!important;
    padding:7px 11px!important;
    box-sizing:border-box!important;
    white-space:nowrap!important;
    transform:none!important;
  }
}

@media (max-width:390px){
  html[lang="he"] body.public-page-he header.site-header,
  html[lang="he"] body.public-page-he .site-header{
    gap:8px!important;
    padding:10px 9px!important;
  }

  html[lang="he"] body.public-page-he header.site-header nav.site-nav,
  html[lang="he"] body.public-page-he .site-header nav.site-nav{
    gap:5px!important;
  }

  html[lang="he"] body.public-page-he header.site-header nav.site-nav>a,
  html[lang="he"] body.public-page-he .site-header nav.site-nav>a{
    height:34px!important;
    min-height:34px!important;
    padding:7px 8px!important;
    font-size:11.5px!important;
  }
}
`;

    document.head.appendChild(style);
  }

  function init() {
    installHebrewMobileHeaderFix();
    requestAnimationFrame(installHebrewMobileHeaderFix);
    setTimeout(installHebrewMobileHeaderFix, 120);
    setTimeout(installHebrewMobileHeaderFix, 500);
    setTimeout(installHebrewMobileHeaderFix, 1200);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init, { once: true });
  } else {
    init();
  }
})();
