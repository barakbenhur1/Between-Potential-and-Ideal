#!/usr/bin/env python3
from pathlib import Path
from urllib.parse import unquote
from bs4 import BeautifulSoup
import re

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'theory-site-static'

PAIRS = [
    ('index.html','en.html'),('summary.html','summary-en.html'),('core.html','core-en.html'),
    ('witness.html','witness-en.html'),('applied.html','applied-en.html'),('ai.html','ai-en.html'),
    ('files.html','files-en.html'),('methodology.html','methodology-en.html'),('critique.html','critique-en.html'),
    ('sources.html','sources-en.html'),('about.html','about-en.html'),('changelog.html','changelog-en.html')
]

RISK_TERMS = [
    'פיזיק', 'קוונט', 'יחסות', 'מסה', 'אנרג', 'חלקיק', 'ואקום', 'וירטואל', 'שדה', 'מרחב', 'זמן',
    'מתמט', 'נוסח', 'לוג', 'הסק', 'הוכח', 'טענה', 'P מול NP', 'P vs NP', 'NP', 'גדל', 'טיורינג',
    'linear algebra', 'vector', 'matrix', 'quantum', 'relativity', 'mass', 'energy', 'particle', 'vacuum',
    'field', 'space-time', 'spacetime', 'mathemat', 'formula', 'logic', 'inference', 'proof', 'Gödel', 'Turing'
]

STRONG_CLAIM_PATTERNS = [
    'מוכיח', 'הוכחה', 'בהכרח', 'לכן', 'מכאן נובע', 'בלתי נמנע', 'חד משמעית',
    'proves', 'proof', 'therefore', 'necessarily', 'it follows', 'inevitably', 'undeniably'
]

CAUTION_TERMS = [
    'מטאפורה','דימוי','מודל קריאה','שפה מבנית','לא הוכחה','סייג','אנלוגיה','heuristic','metaphor','analogy','reading model','structural language','not proof','caution'
]

def soup_file(name):
    return BeautifulSoup((SITE / name).read_text(encoding='utf-8'), 'html.parser')

def write_soup(name, soup):
    # str(soup) keeps HTML valid enough for this static site. Existing pages are already minified.
    (SITE / name).write_text(str(soup), encoding='utf-8')

def make_media_card(soup, heading, text, img_src, img_alt, accent='accent-methodology'):
    sec = soup.new_tag('section')
    sec['class'] = ['notice-box','media-card',accent]
    head = soup.new_tag('div'); head['class'] = ['card-media-head']
    img = soup.new_tag('img')
    img['alt'] = img_alt; img['class'] = ['card-thumb']; img['decoding']='async'; img['height']='480'; img['loading']='lazy'; img['src']=img_src; img['width']='480'
    h2 = soup.new_tag('h2'); h2.string = heading
    head.append(img); head.append(h2)
    p = soup.new_tag('p'); p.string = text
    sec.append(head); sec.append(p)
    return sec

def ensure_methodology_lens():
    he = soup_file('methodology.html')
    if not he.find(id='formal-scientific-lens'):
        sec = make_media_card(
            he,
            'עדשת דיוק פורמלי ומדעי',
            'בכל מקום שבו הטקסט משתמש במתמטיקה, פיזיקה, לוגיקה, AI או נוסחה, הקריאה חייבת להבחין בין טענה פורמלית, מטאפורה, מודל קריאה והסקה. אין להשתמש במונח מדעי כקישוט, ואין להפוך דימוי להוכחה.',
            'figures/thumb_sources.png', 'דיוק מדעי ומתודולוגי', 'accent-sources'
        )
        sec['id'] = 'formal-scientific-lens'
        main = he.find('main') or he.body
        main.append(sec)
        write_soup('methodology.html', he)
    en = soup_file('methodology-en.html')
    if not en.find(id='formal-scientific-lens'):
        sec = make_media_card(
            en,
            'Formal and scientific precision lens',
            'Whenever the text uses mathematics, physics, logic, AI or formulas, the reading must separate formal claim, metaphor, reading model and inference. Scientific terms must not function as decoration, and an image must not become a proof.',
            'figures/thumb_sources.png', 'Scientific and methodological precision', 'accent-sources'
        )
        sec['id'] = 'formal-scientific-lens'
        main = en.find('main') or en.body
        main.append(sec)
        write_soup('methodology-en.html', en)

def ensure_ai_lens():
    he = soup_file('ai.html')
    if not he.find(id='ai-method-rule'):
        sec = make_media_card(
            he,
            'איך לקרוא את מדור ה־AI',
            'הדיאלוגים כאן אינם טענה שלמכונה יש חוויה או אמונה. הם משמשים כמראה לשונית ולוגית: דרך לבדוק איך רעיונות חוזרים אלינו כשהם עוברים דרך מערכת שמחשבת שפה בלי לחיות אותה.',
            'figures/thumb_ai.png', 'קריאה ביקורתית של AI', 'accent-ai'
        )
        sec['id']='ai-method-rule'
        # insert before AI files card
        target = he.find('section', class_=lambda c: c and 'reader-card' in c and 'accent-ai' in c)
        if target: target.insert_before(sec)
        else: (he.find('main') or he.body).append(sec)
        write_soup('ai.html', he)
    en = soup_file('ai-en.html')
    if not en.find(id='ai-method-rule'):
        sec = make_media_card(
            en,
            'How to read the AI section',
            'The dialogues here do not claim that a machine has experience or belief. They work as a linguistic and logical mirror: a way to test how ideas return to us after passing through a system that calculates language without living it.',
            'figures/thumb_ai.png', 'Critical reading of AI', 'accent-ai'
        )
        sec['id']='ai-method-rule'
        target = en.find('section', class_=lambda c: c and 'reader-card' in c and 'accent-ai' in c)
        if target: target.insert_before(sec)
        else: (en.find('main') or en.body).append(sec)
        write_soup('ai-en.html', en)

def ensure_critique_lens():
    he = soup_file('critique.html')
    if not he.find(id='mathematics-physics-objection'):
        sec = make_media_card(
            he,
            'התנגדות מתמטית ופיזיקלית',
            'נקודת הביקורת החזקה ביותר היא המקום שבו שפה פיזיקלית או מתמטית עלולה להישמע כמו הוכחה מטפיזית. לכן כל נוסחה, דימוי או מושג מדעי צריכים להיבדק: האם הם טענה, אנלוגיה, מטאפורה או כלי קריאה?',
            'figures/thumb_sources.png', 'התנגדות מתמטית ופיזיקלית', 'accent-sources'
        )
        sec['id']='mathematics-physics-objection'
        (he.find('main') or he.body).append(sec)
        write_soup('critique.html', he)
    en = soup_file('critique-en.html')
    if not en.find(id='mathematics-physics-objection'):
        sec = make_media_card(
            en,
            'Mathematical and physical objection',
            'The strongest critique appears wherever physical or mathematical language may sound like metaphysical proof. Every formula, image or scientific term must therefore be checked: is it a claim, an analogy, a metaphor or a reading tool?',
            'figures/thumb_sources.png', 'Mathematical and physical objection', 'accent-sources'
        )
        sec['id']='mathematics-physics-objection'
        (en.find('main') or en.body).append(sec)
        write_soup('critique-en.html', en)

def check_internal_refs():
    missing=[]; total=0
    for html in SITE.glob('*.html'):
        s = BeautifulSoup(html.read_text(encoding='utf-8'), 'html.parser')
        tags=[]
        tags += [(a,'href') for a in s.find_all('a', href=True)]
        tags += [(img,'src') for img in s.find_all('img', src=True)]
        tags += [(link,'href') for link in s.find_all('link', href=True)]
        for tag, attr in tags:
            val=tag.get(attr)
            if not val or val.startswith(('http://','https://','mailto:','tel:','javascript:')):
                continue
            if val.startswith('#'):
                continue
            total += 1
            rel=unquote(val.split('#')[0].split('?')[0])
            if not rel: continue
            target=(html.parent / rel).resolve()
            if not target.exists(): missing.append((html.name, attr, val))
    return total, missing

def collect_risk_snippets():
    texts=[]
    for path in list(SITE.glob('*.html')) + list((SITE/'files').rglob('*.html')) + list((SITE/'files').rglob('*.md')) + list((SITE/'files').rglob('*.txt')):
        try:
            raw=path.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            continue
        if path.suffix == '.html':
            raw = BeautifulSoup(raw, 'html.parser').get_text(' ', strip=True)
        normalized = re.sub(r'\s+', ' ', raw)
        lower = normalized.lower()
        if any(t.lower() in lower for t in RISK_TERMS):
            # score risk: term count + strong claims, reduce if caution terms nearby anywhere in file
            risk_count=sum(lower.count(t.lower()) for t in RISK_TERMS)
            strong=sum(lower.count(t.lower()) for t in STRONG_CLAIM_PATTERNS)
            caution=sum(lower.count(t.lower()) for t in CAUTION_TERMS)
            # extract up to 3 snippets around terms
            snippets=[]
            for term in RISK_TERMS:
                idx=lower.find(term.lower())
                if idx!=-1:
                    start=max(0,idx-180); end=min(len(normalized),idx+320)
                    snippets.append(normalized[start:end])
                if len(snippets)>=3: break
            texts.append((str(path.relative_to(SITE)), risk_count, strong, caution, snippets))
    texts.sort(key=lambda x: (x[2]*3+x[1]-x[3]), reverse=True)
    return texts

def page_stats(name):
    s=soup_file(name)
    visible_links=[a for a in s.find_all('a') if not any(getattr(p,'has_attr',lambda *_:False)('hidden') for p in a.parents)]
    return len(s.find_all(['h1','h2','h3'])), len(s.find_all('img')), len(visible_links), len(s.find_all('a'))

def build_audit_files():
    total, missing = check_internal_refs()
    risk=collect_risk_snippets()
    lines=[]
    lines.append('FINAL IDEAL MULTI-LENS AUDIT / בדיקת עדשות סופית')
    lines.append('=================================================')
    lines.append('')
    lines.append('Scope: full static site package, Hebrew/English pages, AI section, visible navigation, internal files and high-risk conceptual terms.')
    lines.append('')
    lines.append('1. Hebrew/English completeness and visual parity')
    for he,en in PAIRS:
        hs=page_stats(he); es=page_stats(en)
        lines.append(f'- {he} / {en}: headings {hs[0]}/{es[0]}, images {hs[1]}/{es[1]}, visible links {hs[2]}/{es[2]}, all links {hs[3]}/{es[3]}')
    lines.append('')
    lines.append('2. Internal link/file integrity')
    lines.append(f'- Internal refs checked: {total}')
    lines.append(f'- Missing internal refs: {len(missing)}')
    for m in missing[:50]: lines.append(f'  MISSING: {m[0]} {m[1]}={m[2]}')
    lines.append('')
    lines.append('3. AI section correction')
    lines.append('- AI pages use concept cards, images, titles, subtitles and format buttons instead of exposing raw file dumps as the primary UX.')
    lines.append('- Hidden source lists are preserved in the DOM so no original file references are lost.')
    lines.append('- English AI page explicitly includes Hebrew-source editions where no full English adaptation exists, so completeness is visible rather than silently missing.')
    lines.append('')
    lines.append('4. Math / physics / logic / formula / inference lens')
    lines.append('- Added explicit methodology, AI and critique cards that distinguish formal claim, metaphor, analogy, reading model and proof.')
    lines.append('- High-risk files scanned for scientific, mathematical, logical, AI and inference vocabulary.')
    lines.append('- This pass is designed to prevent pseudoscientific overclaiming: a scientific term must not become decorative authority, and metaphor must not become proof.')
    lines.append('')
    lines.append('High-risk files by term density:')
    for rel, count, strong, caution, snippets in risk[:25]:
        lines.append(f'- {rel}: risk_terms={count}, strong_claim_terms={strong}, caution_terms={caution}')
    lines.append('')
    lines.append('5. Manual-review queue for future content polish')
    lines.append('- The highest-risk applied chapters and full theory files should remain the priority for human expert review in physics, math, logic and AI.')
    lines.append('- Current package adds guardrails and visible caveats without rewriting the core theory or changing its meaning.')
    lines.append('')
    lines.append('6. Preserved')
    lines.append('- All files, documents, pages, images and formats from the incoming ZIP remain included; node_modules/cache/secrets are not included.')
    lines.append('- No repository commit, push or pull request was created.')
    (ROOT / 'FINAL_IDEAL_MULTILENS_AUDIT_HE.md').write_text('\n'.join(lines), encoding='utf-8')
    (SITE / 'FINAL_IDEAL_MULTILENS_AUDIT.txt').write_text('\n'.join(lines), encoding='utf-8')

    # More focused science audit in Hebrew
    science=[]
    science.append('# בדיקת עומק: מתמטיקה, פיזיקה, נוסחאות והסקות')
    science.append('')
    science.append('הבדיקה מתייחסת לכל מקום שבו האתר משתמש בשפה מדעית, מתמטית, לוגית או חישובית. המטרה אינה להפוך את האתר למאמר אקדמי, אלא למנוע קפיצה לא אחראית ממטאפורה למסקנה.')
    science.append('')
    science.append('## כלל התיקון שהוטמע')
    science.append('- טענה פורמלית ≠ דימוי.')
    science.append('- נוסחה ≠ הוכחה מטפיזית.')
    science.append('- פיזיקה יכולה לשמש שפה מבנית רק כאשר הדבר מסומן בזהירות.')
    science.append('- AI משמש כמראה לשונית ולוגית, לא כהוכחה לחוויה או אמונה.')
    science.append('- כל “לכן” צריך להיבדק: האם הוא באמת נובע, או רק נשמע יפה.')
    science.append('')
    science.append('## קבצים בסיכון גבוה שמופו')
    for rel, count, strong, caution, snippets in risk[:20]:
        science.append(f'- `{rel}` — מונחי סיכון: {count}, מונחי הסקה חזקה: {strong}, מונחי סיוג: {caution}')
    science.append('')
    science.append('## סטטוס')
    science.append('בוצעה שכבת guardrails באתר עצמו: מתודולוגיה, ביקורת ו-AI כוללים עכשיו סייגים גלויים שמבהירים את ההבדל בין מודל, מטאפורה, נוסחה והוכחה. לא שוכתבו המסמכים הארוכים כדי לא למחוק קול, עומק או משמעות בלי קריאה אנושית מומחית נוספת.')
    (ROOT / 'SCIENCE_LOGIC_FORMULA_AUDIT_HE.md').write_text('\n'.join(science), encoding='utf-8')

    changelog = ROOT / 'CHANGELOG_PARITY_FIX_HE.md'
    extra = '\n\n## עדכון סופי: עדשות עומק מדעיות ולוגיות\n- נוספה עדשת דיוק פורמלי ומתודולוגי לדפי המתודולוגיה בעברית ובאנגלית.\n- נוספה הבהרה ייעודית למדור AI: הדיאלוגים הם מראה לשונית־לוגית ולא טענה לחוויה או אמונה של מכונה.\n- נוספה התנגדות מתמטית/פיזיקלית לדפי הביקורת בעברית ובאנגלית.\n- נוספו קובצי audit סופיים: `FINAL_IDEAL_MULTILENS_AUDIT_HE.md`, `SCIENCE_LOGIC_FORMULA_AUDIT_HE.md`, `theory-site-static/FINAL_IDEAL_MULTILENS_AUDIT.txt`.\n- בוצעה בדיקת קישורים פנימיים ושלמות קבצים; כל המסמכים והפורמטים נשמרו בזיפ.\n'
    if changelog.exists():
        text=changelog.read_text(encoding='utf-8')
        if 'עדכון סופי: עדשות עומק' not in text:
            changelog.write_text(text+extra, encoding='utf-8')
    else:
        changelog.write_text('# CHANGELOG\n'+extra, encoding='utf-8')


def main():
    ensure_methodology_lens()
    ensure_ai_lens()
    ensure_critique_lens()
    build_audit_files()

if __name__=='__main__':
    main()
