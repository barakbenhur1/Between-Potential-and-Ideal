(function () {
  'use strict';

  const STYLE_ID = 'bpi-he-header-match-en-runtime-v2';

  function installHebrewHeaderParity() {
    document.getElementById(STYLE_ID)?.remove();

    const style = document.createElement('style');
    style.id = STYLE_ID;
    style.textContent = `
/* Keep the approved English header as the physical layout reference.
   Hebrew changes only the reading order inside the navigation. */
@media (min-width:861px){
  html[lang="he"] body.public-page-he header.site-header,
  html[lang="he"] body.public-page-he .site-header{
    direction:ltr!important;
    width:100%!important;
    max-width:100%!important;
    height:86px!important;
    min-height:86px!important;
    max-height:86px!important;
    display:grid!important;
    grid-template-columns:300px minmax(0,1040px) 104px!important;
    align-items:center!important;
    justify-content:center!important;
    column-gap:16px!important;
    padding:0 clamp(22px,2.4vw,36px)!important;
    margin:0!important;
    box-sizing:border-box!important;
    overflow:visible!important;
    transform:none!important;
    translate:none!important;
    inset:auto!important;
  }

  html[lang="he"] body.public-page-he header.site-header .site-brand,
  html[lang="he"] body.public-page-he .site-header .site-brand{
    grid-column:1!important;
    justify-self:start!important;
    align-self:center!important;
    width:300px!important;
    min-width:300px!important;
    max-width:300px!important;
    height:auto!important;
    margin:0!important;
    padding:0!important;
    direction:ltr!important;
    text-align:start!important;
    white-space:nowrap!important;
    overflow:visible!important;
    transform:none!important;
  }

  html[lang="he"] body.public-page-he header.site-header .site-brand>a,
  html[lang="he"] body.public-page-he .site-header .site-brand>a{
    display:block!important;
    width:auto!important;
    max-width:none!important;
    margin:0!important;
    padding:0!important;
    direction:ltr!important;
    unicode-bidi:isolate!important;
    font-family:ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif!important;
    font-size:16px!important;
    font-weight:800!important;
    line-height:1.05!important;
    letter-spacing:-.025em!important;
    text-align:start!important;
    white-space:nowrap!important;
    overflow:visible!important;
    text-overflow:clip!important;
    transform:none!important;
  }

  html[lang="he"] body.public-page-he header.site-header nav.site-nav,
  html[lang="he"] body.public-page-he .site-header nav.site-nav{
    direction:rtl!important;
    grid-column:2!important;
    justify-self:center!important;
    align-self:center!important;
    width:100%!important;
    min-width:0!important;
    max-width:1040px!important;
    min-height:44px!important;
    margin:0 auto!important;
    padding:0!important;
    display:flex!important;
    flex-direction:row!important;
    flex-wrap:wrap!important;
    align-items:center!important;
    align-content:center!important;
    justify-content:center!important;
    gap:6px!important;
    text-align:center!important;
    overflow:visible!important;
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
    font-family:ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif!important;
    font-size:13px!important;
    font-weight:700!important;
    line-height:1.1!important;
    letter-spacing:0!important;
    text-align:center!important;
    white-space:nowrap!important;
    overflow:visible!important;
    text-overflow:clip!important;
    transform:none!important;
  }

  html[lang="he"] body.public-page-he header.site-header .language-switch,
  html[lang="he"] body.public-page-he .site-header .language-switch{
    direction:ltr!important;
    grid-column:3!important;
    justify-self:end!important;
    align-self:center!important;
    width:104px!important;
    min-width:104px!important;
    max-width:104px!important;
    height:36px!important;
    min-height:36px!important;
    margin:0!important;
    padding:8px 13px!important;
    box-sizing:border-box!important;
    display:inline-flex!important;
    align-items:center!important;
    justify-content:center!important;
    font-family:ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif!important;
    font-size:14px!important;
    font-weight:700!important;
    line-height:1.1!important;
    white-space:nowrap!important;
    transform:none!important;
  }
}

@media (max-width:1180px) and (min-width:861px){
  html[lang="he"] body.public-page-he header.site-header .site-brand,
  html[lang="he"] body.public-page-he .site-header .site-brand{
    width:210px!important;
    min-width:210px!important;
    max-width:210px!important;
  }

  html[lang="he"] body.public-page-he header.site-header .language-switch,
  html[lang="he"] body.public-page-he .site-header .language-switch{
    width:92px!important;
    min-width:92px!important;
    max-width:92px!important;
  }
}

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
    installHebrewHeaderParity();
    requestAnimationFrame(installHebrewHeaderParity);
    setTimeout(installHebrewHeaderParity, 120);
    setTimeout(installHebrewHeaderParity, 500);
    setTimeout(installHebrewHeaderParity, 1200);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init, { once: true });
  } else {
    init();
  }
})();
