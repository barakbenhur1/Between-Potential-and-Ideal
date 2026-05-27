#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path.cwd()
HTML_FILES = [ROOT / "site/index.html", ROOT / "site/en.html"]
CSS_FILE = ROOT / "site/styles.css"

HE_TEXT = "זהו ניסוי מחשבתי דו־לשוני שמחבר מסה פילוסופית, מבנה לוגי, סיפורים ויישומים. הדרך המומלצת היא להתחיל בתקציר, לעבור לגרסה המהודקת, ואז לפתוח את המסמך המלא או הנספחים."
EN_TEXT = "This is a bilingual thought experiment combining a philosophical essay, a logical structure, stories, and applications. The recommended path is to start with the summary, continue to the tightened version, and then open the full document or appendices."

START_CLARITY_RE = re.compile(r'<section\b[^>]*\bid=["\']bpi-start-here-clarity["\'][^>]*>.*?</section>', re.S | re.I)
START_NOTE_RE = re.compile(r'<section\b[^>]*\bid=["\']bpi-start-here-note["\'][^>]*>.*?</section>', re.S | re.I)

HE_NOTE = f'<section class="notice-box bpi-start-here-note media-card accent-core" id="bpi-start-here-note"><h2>התחל כאן</h2><p>{HE_TEXT}</p><div class="download-row bpi-start-here-buttons"><a class="download-button primary" href="pages/he/summary.html">תקציר</a><a class="download-button" href="files/editorial-tightened/between-potential-and-ideal-tightened-he.html">גרסה מהודקת</a><a class="download-button" href="files/between-potential-and-ideal-he-editorial.html">המסמך המלא</a></div></section>'

EN_NOTE = f'<section class="notice-box bpi-start-here-note media-card accent-core" id="bpi-start-here-note"><h2>Start here</h2><p>{EN_TEXT}</p><div class="download-row bpi-start-here-buttons"><a class="download-button primary" href="pages/en/summary-en.html">Summary</a><a class="download-button" href="files/editorial-tightened/between-potential-and-ideal-tightened-en.html">Tightened version</a><a class="download-button" href="files/between-potential-and-ideal-en-editorial.html">Full document</a></div></section>'

CSS_BLOCK = r'''

/* BPI V402 - single Start Here card + matching hero width.
   Keeps the SECOND Start Here card design, removes the duplicate first card in HTML,
   gives the card the full first-card content, adds 3 buttons, and makes the blue hero
   card match the Start Here card width on desktop and mobile. */
body.public-page .site-main > .bpi-start-here-clarity{
  display:none!important;
}
body.public-page .site-main > .bpi-start-here-note,
body.public-page .site-main > .hero.concise-hero{
  width:min(1680px, calc(100vw - 144px))!important;
  max-width:min(1680px, calc(100vw - 144px))!important;
  margin-inline:auto!important;
  box-sizing:border-box!important;
}
body.public-page .site-main > .bpi-start-here-note{
  margin-block:28px 34px!important;
  padding:clamp(30px,3.2vw,54px) clamp(28px,5vw,78px)!important;
  border-radius:24px!important;
  text-align:center!important;
  overflow:hidden!important;
}
body.public-page .site-main > .bpi-start-here-note h2{
  margin:0 0 18px!important;
  line-height:1.15!important;
}
body.public-page .site-main > .bpi-start-here-note p{
  max-width:1160px!important;
  margin:0 auto!important;
  line-height:1.75!important;
  text-align:center!important;
}
body.public-page .site-main > .bpi-start-here-note .download-row,
body.public-page .site-main > .bpi-start-here-note .bpi-start-here-buttons{
  display:grid!important;
  grid-template-columns:repeat(3,minmax(160px,1fr))!important;
  gap:18px!important;
  width:100%!important;
  max-width:1180px!important;
  margin:30px auto 0!important;
  align-items:center!important;
}
body.public-page .site-main > .bpi-start-here-note .download-button{
  width:100%!important;
  min-width:0!important;
  justify-content:center!important;
  text-align:center!important;
  box-sizing:border-box!important;
  white-space:normal!important;
}
body.public-page .site-main > .hero.concise-hero{
  margin-block:34px 28px!important;
}
@media (max-width: 900px){
  body.public-page .site-main > .bpi-start-here-note,
  body.public-page .site-main > .hero.concise-hero{
    width:calc(100vw - 32px)!important;
    max-width:calc(100vw - 32px)!important;
  }
  body.public-page .site-main > .bpi-start-here-note{
    padding:32px 22px!important;
  }
  body.public-page .site-main > .bpi-start-here-note .download-row,
  body.public-page .site-main > .bpi-start-here-note .bpi-start-here-buttons{
    grid-template-columns:repeat(2,minmax(0,1fr))!important;
    gap:12px!important;
    margin-top:26px!important;
  }
  body.public-page .site-main > .bpi-start-here-note .download-button:last-child{
    grid-column:1 / -1!important;
    justify-self:center!important;
    width:min(100%, 320px)!important;
  }
}
@media (max-width: 520px){
  body.public-page .site-main > .bpi-start-here-note .download-row,
  body.public-page .site-main > .bpi-start-here-note .bpi-start-here-buttons{
    grid-template-columns:1fr!important;
  }
  body.public-page .site-main > .bpi-start-here-note .download-button:last-child{
    grid-column:auto!important;
    width:100%!important;
  }
}
'''

def replace_start_sections(path: Path) -> dict:
    if not path.exists():
        return {"path": str(path), "status": "missing"}
    text = path.read_text(encoding="utf-8")
    before = text

    text, removed = START_CLARITY_RE.subn("", text)

    is_he = path.name == "index.html"
    new_note = HE_NOTE if is_he else EN_NOTE

    if START_NOTE_RE.search(text):
        text, replaced = START_NOTE_RE.subn(new_note, text, count=1)
    else:
        marker = '</nav>'
        idx = text.find(marker, text.find('<main'))
        if idx != -1:
            text = text[:idx+len(marker)] + new_note + text[idx+len(marker):]
            replaced = 1
        else:
            replaced = 0

    path.write_text(text, encoding="utf-8")
    return {
        "path": str(path),
        "removed_bpi_start_here_clarity": removed,
        "replaced_bpi_start_here_note": replaced,
        "changed": text != before,
    }

def patch_css(path: Path) -> dict:
    if not path.exists():
        return {"path": str(path), "status": "missing"}
    text = path.read_text(encoding="utf-8")
    before = text
    text = re.sub(r'\n/\* BPI V402 - single Start Here card \+ matching hero width\..*?\n}\n(?=\n|$)', '\n', text, flags=re.S)
    if "BPI V402 - single Start Here card" not in text:
        text = text.rstrip() + CSS_BLOCK + "\n"
    path.write_text(text, encoding="utf-8")
    return {"path": str(path), "changed": text != before}

def quick_check() -> list[str]:
    problems = []
    for p in HTML_FILES:
        if not p.exists():
            problems.append(f"missing html: {p}")
            continue
        text = p.read_text(encoding="utf-8")
        if 'id="bpi-start-here-clarity"' in text:
            problems.append(f"old duplicate block still exists: {p}")
        count = text.count('id="bpi-start-here-note"')
        if count != 1:
            problems.append(f"expected exactly one bpi-start-here-note in {p}, got {count}")
        if 'bpi-start-here-buttons' not in text:
            problems.append(f"missing bpi-start-here-buttons: {p}")
        if p.name == 'index.html' and 'המסמך המלא' not in text:
            problems.append(f"missing Hebrew third button: {p}")
        if p.name == 'en.html' and 'Full document' not in text:
            problems.append(f"missing English third button: {p}")
    if CSS_FILE.exists():
        css = CSS_FILE.read_text(encoding="utf-8")
        if "BPI V402 - single Start Here card" not in css:
            problems.append("missing V402 css block")
    else:
        problems.append("missing site/styles.css")
    return problems

if __name__ == "__main__":
    results = [replace_start_sections(p) for p in HTML_FILES]
    results.append(patch_css(CSS_FILE))
    problems = quick_check()

    print("BPI Start Here single-card layout fix")
    for r in results:
        print(r)
    if problems:
        print("\nFAILED:")
        for p in problems:
            print("-", p)
        raise SystemExit(1)
    print("\nOK: duplicate Start Here block removed, second-card design kept, 3 buttons added, hero width matched.")
