const text={he:{dir:"rtl",langButton:"English",navIntro:"מבוא",navRead:"קריאה",navFigures:"איורים",navAI:"במה בינה מלאכותית מאמינה?",navTheory:"התאוריה",navDownloads:"קבצים",navAppendices:"נספחים",navContact:"תגובה"},en:{dir:"ltr",langButton:"עברית",navIntro:"Intro",navRead:"Read",navFigures:"Figures",navAI:"What AI Believes",navTheory:"The Theory",navDownloads:"Files",navAppendices:"Appendices",navContact:"Respond"}};
function pageLang(){return (document.documentElement.lang||"he").toLowerCase().startsWith("en")?"en":"he"}
let currentLang=pageLang();
const $$=s=>Array.from(document.querySelectorAll(s));
function applyLanguage(lang){currentLang=lang;document.documentElement.lang=lang;document.documentElement.dir=text[lang].dir;$$('[data-lang-block]').forEach(b=>{b.hidden=b.getAttribute('data-lang-block')!==lang;b.style.display=b.hidden?'none':''});$$('[data-i18n]').forEach(el=>{const k=el.getAttribute('data-i18n');if(text[lang][k])el.textContent=text[lang][k]});const btn=document.getElementById('langButton');if(btn)btn.textContent=text[lang].langButton}
document.addEventListener('DOMContentLoaded',()=>{applyLanguage(pageLang());const btn=document.getElementById('langButton');if(btn)btn.addEventListener('click',()=>applyLanguage(currentLang==='he'?'en':'he'))});

function setupFileFiltering(){
  const table=document.querySelector('.download-table');
  const search=document.getElementById('fileSearch');
  const type=document.getElementById('fileTypeFilter');
  const lang=document.getElementById('fileLangFilter');
  const count=document.getElementById('fileFilterCount');
  if(!table||!search||!type||!lang) return;
  const rows=Array.from(table.querySelectorAll('tr')).slice(1);
  function apply(){
    const q=(search.value||'').trim().toLowerCase();
    const ft=(type.value||'').toLowerCase();
    const fl=(lang.value||'').toLowerCase();
    let visible=0;
    rows.forEach(row=>{
      const cells=Array.from(row.children).map(td=>(td.textContent||'').toLowerCase());
      const text=cells.join(' ');
      const matchesQ=!q||text.includes(q);
      const matchesT=!ft||(cells[1]||'').includes(ft);
      const matchesL=!fl||(cells[2]||'').includes(fl);
      const show=matchesQ&&matchesT&&matchesL;
      row.hidden=!show;
      if(show) visible++;
    });
    if(count) count.textContent = document.documentElement.lang==='he' ? `${visible} קבצים מוצגים` : `${visible} files shown`;
  }
  [search,type,lang].forEach(el=>el.addEventListener('input',apply));
  apply();
}
document.addEventListener('DOMContentLoaded',setupFileFiltering);
