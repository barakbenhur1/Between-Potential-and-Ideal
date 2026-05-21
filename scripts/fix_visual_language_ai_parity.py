#!/usr/bin/env python3
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'theory-site-static'


def read(name):
    return BeautifulSoup((SITE / name).read_text(encoding='utf-8'), 'html.parser')


def write(name, soup):
    (SITE / name).write_text(str(soup), encoding='utf-8')


def ensure_classes(tag, classes):
    existing = tag.get('class', [])
    for c in classes:
        if c not in existing:
            existing.append(c)
    tag['class'] = existing


def remove_class(tag, cls):
    existing = tag.get('class', [])
    if cls in existing:
        existing = [c for c in existing if c != cls]
    tag['class'] = existing


def wrap_heading_with_image(soup, card, img_src, img_alt, heading_tag='h2'):
    h = card.find(['h1','h2','h3'])
    if not h:
        return
    if card.find('img'):
        return
    # Create card-media-head div and insert image + existing heading.
    head = soup.new_tag('div')
    head['class'] = ['card-media-head']
    img = soup.new_tag('img')
    img['alt'] = img_alt
    img['class'] = ['card-thumb']
    img['decoding'] = 'async'
    img['height'] = '480'
    img['loading'] = 'lazy'
    img['src'] = img_src
    img['width'] = '480'
    h.extract()
    head.append(img)
    head.append(h)
    card.insert(0, head)
    ensure_classes(card, ['media-card'])


def find_by_heading(soup, text):
    for tag in soup.find_all(['section','article']):
        h = tag.find(['h1','h2','h3'])
        if h and h.get_text(' ', strip=True) == text:
            return tag
    return None


def fix_en_home():
    soup = read('en.html')
    card = find_by_heading(soup, '2. Witness')
    if card:
        ensure_classes(card, ['media-card', 'accent-witness'])
        wrap_heading_with_image(soup, card, 'figures/thumb_witness.png', 'Witness')
    write('en.html', soup)


def fix_core_en():
    soup = read('core-en.html')
    card = find_by_heading(soup, 'Recommended path')
    if card:
        remove_class(card, 'tone-card')
        ensure_classes(card, ['media-card', 'accent-core'])
        wrap_heading_with_image(soup, card, 'figures/thumb_methodology.png', 'Reading path')
    card = find_by_heading(soup, 'Method note')
    if card:
        remove_class(card, 'tone-card')
        ensure_classes(card, ['media-card', 'accent-methodology'])
        wrap_heading_with_image(soup, card, 'figures/thumb_methodology.png', 'Methodology')
    write('core-en.html', soup)


def fix_witness_en():
    soup = read('witness-en.html')
    card = find_by_heading(soup, 'A Mistake Always Returns')
    if card:
        remove_class(card, 'tone-card')
        ensure_classes(card, ['media-card', 'accent-critique'])
        wrap_heading_with_image(soup, card, 'figures/thumb_critique.png', 'A mistake always returns')
    card = find_by_heading(soup, 'AI as witness')
    if card:
        remove_class(card, 'tone-card')
        ensure_classes(card, ['media-card', 'accent-ai'])
        wrap_heading_with_image(soup, card, 'figures/thumb_ai.png', 'AI as witness')
    write('witness-en.html', soup)


def fix_methodology_en():
    soup = read('methodology-en.html')
    card = find_by_heading(soup, 'Domain markers')
    if card:
        remove_class(card, 'tone-card')
        ensure_classes(card, ['media-card', 'accent-methodology'])
        wrap_heading_with_image(soup, card, 'figures/thumb_sources.png', 'Domain markers')
    write('methodology-en.html', soup)


def fix_applied_en():
    soup = read('applied-en.html')
    card = find_by_heading(soup, 'Scientific caution')
    if card:
        img = card.find('img')
        if img:
            img['src'] = 'figures/thumb_sources.png'
            img['alt'] = 'Scientific caution and sources'
    write('applied-en.html', soup)


def fix_critique_en():
    soup = read('critique-en.html')
    items = [
        ('Questions for readers', 'figures/thumb_ai.png', 'Questions for readers', ['media-card','accent-critique']),
        ('The scientific reader', 'figures/thumb_sources.png', 'Scientific reader', ['media-card','accent-sources']),
        ('The philosophical reader', 'figures/thumb_core.png', 'Philosophical reader', ['media-card','accent-core']),
        ('The religious reader', 'figures/thumb_witness.png', 'Religious reader', ['media-card','accent-witness']),
        ('The literary reader', 'files/appendices/assets/story_image_9.png', 'Literary reader', ['media-card','accent-witness']),
    ]
    for title, src, alt, classes in items:
        card = find_by_heading(soup, title)
        if card:
            remove_class(card, 'tone-card')
            ensure_classes(card, classes)
            wrap_heading_with_image(soup, card, src, alt)
    write('critique-en.html', soup)


def make_action_link(soup, href, label, size):
    a = soup.new_tag('a')
    a['href'] = href
    a['rel'] = 'noopener noreferrer'
    a['target'] = '_blank'
    a.append(label + ' ')
    span = soup.new_tag('span')
    span['class'] = ['file-size']
    span.string = size
    a.append(span)
    return a


def make_ai_doc_card(soup, img_src, img_alt, title, desc, links):
    card = soup.new_tag('article')
    card['class'] = ['appendix-card','media-card','accent-ai','ai-reading-card']
    head = soup.new_tag('div')
    head['class'] = ['card-media-head']
    img = soup.new_tag('img')
    img['alt'] = img_alt
    img['class'] = ['card-thumb']
    img['decoding'] = 'async'
    img['height'] = '480'
    img['loading'] = 'lazy'
    img['src'] = img_src
    img['width'] = '480'
    h3 = soup.new_tag('h3')
    h3.string = title
    head.append(img)
    head.append(h3)
    p = soup.new_tag('p')
    p.string = desc
    actions = soup.new_tag('div')
    actions['class'] = ['appendix-actions']
    for label, href, size in links:
        actions.append(make_action_link(soup, href, label, size))
    card.append(head)
    card.append(p)
    card.append(actions)
    return card


def replace_ai_grid(page, cards):
    soup = read(page)
    # Hide source list but keep it in the DOM as an archive of every linked file.
    ul = soup.find('ul', class_='file-list')
    if ul:
        ul['hidden'] = ''
        ul['aria-hidden'] = 'true'
    old = soup.find('div', class_='ai-card-grid')
    if old:
        old.decompose()
    grid = soup.new_tag('div')
    grid['class'] = ['ai-card-grid','ai-page-card-grid']
    for c in cards:
        grid.append(make_ai_doc_card(soup, **c))
    if ul:
        ul.insert_after(grid)
    write(page, soup)


def fix_ai_pages():
    he_cards = [
        dict(
            img_src='figures/thumb_ai.png', img_alt='טיורינג הפוך', title='טיורינג הפוך',
            desc='שיחה שמחליפה את כיוון מבחן טיורינג: לא רק האם מכונה נראית אנושית, אלא מה האדם מגלה על עצמו כשהוא עומד מול מראה לשונית.',
            links=[
                ('HTML','files/ai-believes/reverse-turing-conversation-he.html','99.2 KB'),
                ('PDF','files/ai-believes/reverse-turing-conversation-he.pdf','72.0 KB'),
                ('DOCX','files/ai-believes/reverse-turing-conversation-he.docx','67.6 KB'),
                ('MD','files/ai-believes/reverse-turing-conversation-he.md','58.4 KB'),
            ]),
        dict(
            img_src='figures/thumb_sources.png', img_alt='מה בינה מלאכותית מאמינה', title='מה בינה מלאכותית מאמינה',
            desc='בדיקה זהירה של השאלה מה ניתן, ומה אסור, לייחס למענה של מודל: אמונה, סימולציה, עדות, דפוס או רק שפה מחושבת.',
            links=[
                ('HTML','files/ai-believes/what-ai-believes-he.html','527.0 KB'),
                ('PDF','files/ai-believes/what-ai-believes-he.pdf','296.1 KB'),
                ('DOCX','files/ai-believes/what-ai-believes-he.docx','174.8 KB'),
                ('MD','files/ai-believes/what-ai-believes-he.md','373.4 KB'),
            ]),
        dict(
            img_src='figures/thumb_witness.png', img_alt='כשאני גם אתה', title='כשאני גם אתה',
            desc='דיאלוג על גבול הזהות: מה קורה כשאדם, קול ומראה מלאכותית מתחילים להחזיר זה לזה את השאלה מי מדבר כאן.',
            links=[
                ('HTML','files/ai-believes/when-i-am-also-you-he.html','221.3 KB'),
                ('PDF','files/ai-believes/when-i-am-also-you-he.pdf','140.7 KB'),
                ('DOCX','files/ai-believes/when-i-am-also-you-he.docx','97.1 KB'),
                ('MD','files/ai-believes/when-i-am-also-you-he.md','144.8 KB'),
            ]),
    ]
    en_cards = [
        dict(
            img_src='figures/thumb_witness.png', img_alt='When I Am Also You', title='When I Am Also You',
            desc='A dialogue about identity, reflection and meaning between a human voice and an artificial mirror.',
            links=[
                ('HTML','files/ai-believes/when-i-am-also-you-en.html','144.2 KB'),
                ('PDF','files/ai-believes/when-i-am-also-you-en.pdf','128.7 KB'),
                ('DOCX','files/ai-believes/when-i-am-also-you-en.docx','92.5 KB'),
                ('MD','files/ai-believes/when-i-am-also-you-en.md','98.2 KB'),
            ]),
        dict(
            img_src='figures/thumb_ai.png', img_alt='Reverse Turing conversation', title='Reverse Turing Conversation',
            desc='Hebrew source edition. It belongs in the English AI section so the reader sees the full archive, even before a complete English adaptation exists.',
            links=[
                ('HTML','files/ai-believes/reverse-turing-conversation-he.html','99.2 KB'),
                ('PDF','files/ai-believes/reverse-turing-conversation-he.pdf','72.0 KB'),
                ('DOCX','files/ai-believes/reverse-turing-conversation-he.docx','67.6 KB'),
                ('MD','files/ai-believes/reverse-turing-conversation-he.md','58.4 KB'),
            ]),
        dict(
            img_src='figures/thumb_sources.png', img_alt='What AI Believes', title='What AI Believes',
            desc='Hebrew source edition. A cautious test of what can and cannot be inferred from an AI system’s linguistic responses.',
            links=[
                ('HTML','files/ai-believes/what-ai-believes-he.html','527.0 KB'),
                ('PDF','files/ai-believes/what-ai-believes-he.pdf','296.1 KB'),
                ('DOCX','files/ai-believes/what-ai-believes-he.docx','174.8 KB'),
                ('MD','files/ai-believes/what-ai-believes-he.md','373.4 KB'),
            ]),
    ]
    replace_ai_grid('ai.html', he_cards)
    replace_ai_grid('ai-en.html', en_cards)


def main():
    fix_en_home()
    fix_core_en()
    fix_witness_en()
    fix_methodology_en()
    fix_applied_en()
    fix_critique_en()
    fix_ai_pages()

if __name__ == '__main__':
    main()
