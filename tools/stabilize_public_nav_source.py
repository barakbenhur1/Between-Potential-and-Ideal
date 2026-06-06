#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site'
HEADER_RE = re.compile(r'<header class="site-header".*?</header>', re.S)
FINAL_CSS_RE = re.compile(r'<link\b[^>]*\bid="bpi-final-requested-fixes"[^>]*>\s*', re.I)
FINAL_JS_RE = re.compile(r'<script\b[^>]*\bid="bpi-final-requested-fixes-runtime"[^>]*>\s*</script>\s*', re.I)

FINAL_VERSION = '20260606-mobile-nav-gold-buttons-nav-order-v1'
SHARED_NAV_VERSION = '20260606-shared-nav-v146'

# Requested order: Methodology before Core in both languages.
HE = [
    ('בית','index.html','index'),('תקציר','summary.html','summary'),('מילון','glossary.html','glossary'),
    ('מושגים','potential-ideal-optimal.html','potential-ideal-optimal'),('בינה מלאכותית כעדות','ai-as-witness.html','ai-as-witness'),
    ('מתודולוגיה','methodology.html','methodology'),('ליבה','core.html','core'),('עדות','witness.html','witness'),
    ('יישום','applied.html','applied'),('בינה מלאכותית','ai.html','ai'),('קבצים','files.html','files'),
    ('ביקורת','critique.html','critique'),('מקורות','sources.html','sources')]
EN = [
    ('Home','en.html','en'),('Summary','summary-en.html','summary-en'),('Glossary','glossary-en.html','glossary-en'),
    ('Concepts','potential-ideal-optimal-en.html','potential-ideal-optimal-en'),('AI as Witness','ai-as-witness-en.html','ai-as-witness-en'),
    ('Methodology','methodology-en.html','methodology-en'),('Core','core-en.html','core-en'),('Witness','witness-en.html','witness-en'),
    ('Application','applied-en.html','applied-en'),('AI','ai-en.html','ai-en'),('Files','files-en.html','files-en'),
    ('Critique','critique-en.html','critique-en'),('Sources','sources-en.html','sources-en')]

HE_KEYS = {item[2] for item in HE}
EN_KEYS = {item[2] for item in EN}
HE_TO_EN = {
    'index':'en.html','summary':'summary-en.html','glossary':'glossary-en.html',
    'potential-ideal-optimal':'potential-ideal-optimal-en.html','ai-as-witness':'ai-as-witness-en.html',
    'methodology':'methodology-en.html','core':'core-en.html','witness':'witness-en.html',
    'applied':'applied-en.html','ai':'ai-en.html','files':'files-en.html',
    'critique':'critique-en.html','sources':'sources-en.html'
}
EN_TO_HE = {v[:-5] if v.endswith('.html') else v: k + '.html' for k, v in HE_TO_EN.items()}
EN_TO_HE['en'] = 'index.html'


def active(path: Path, he: bool, home: bool) -> str:
    if home:
        return 'index' if he else 'en'
    return path.stem


def nav_href(href: str, he: bool, home: bool) -> str:
    if home:
        if he:
            return href if href == 'index.html' else 'pages/he/' + href
        return href if href == 'en.html' else 'pages/en/' + href
    if he:
        return '../../index.html' if href == 'index.html' else href
    return '../../en.html' if href == 'en.html' else href


def lang_href(path: Path, he: bool, home: bool) -> str:
    key = active(path, he, home)
    if home:
        return 'en.html' if he else 'index.html'
    if he:
        return '../en/' + HE_TO_EN.get(key, key + '-en.html')
    base = key[:-3] if key.endswith('-en') else key
    return '../he/' + EN_TO_HE.get(key, base + '.html')


def build_nav(items, key, he, home):
    out = []
    valid_keys = HE_KEYS if he else EN_KEYS
    for label, href, item_key in items:
        attrs = ' aria-current="page" class="active"' if key in valid_keys and item_key == key else ''
        out.append(f'<a{attrs} href="{nav_href(href, he, home)}">{label}</a>')
    return ''.join(out)


def build_header(path: Path, he: bool, home: bool) -> str:
    key = active(path, he, home)
    if he:
        brand = 'index.html' if home else '../../index.html'
        return (
            f'<header class="site-header" dir="rtl" role="banner">'
            f'<div class="site-brand"><a href="{brand}">Between Potential and Ideal</a></div>'
            f'<nav aria-label="Primary navigation" class="site-nav" role="navigation">'
            f'{build_nav(HE, key, True, home)}</nav>'
            f'<a aria-label="Switch to the English version" class="language-switch" '
            f'href="{lang_href(path, True, home)}" title="English version">English</a></header>'
        )

    brand = 'en.html' if home else '../../en.html'
    return (
        f'<header class="site-header" dir="ltr" role="banner">'
        f'<div class="site-brand"><a href="{brand}">Between Potential and Ideal</a></div>'
        f'<nav aria-label="Primary navigation" class="site-nav" role="navigation">'
        f'{build_nav(EN, key, False, home)}</nav>'
        f'<a aria-label="מעבר לגרסה העברית" class="language-switch" '
        f'href="{lang_href(path, False, home)}" title="גרסה עברית">עברית</a></header>'
    )


def asset_prefix(home: bool) -> str:
    return '' if home else '../../'


def install_final_assets(text: str, home: bool) -> str:
    prefix = asset_prefix(home)
    css = (
        f'<link id="bpi-final-requested-fixes" '
        f'href="{prefix}assets/bpi-final-requested-fixes-v1.css?v={FINAL_VERSION}" '
        f'rel="stylesheet"/>'
    )
    js = (
        f'<script defer id="bpi-final-requested-fixes-runtime" '
        f'src="{prefix}assets/bpi-final-requested-fixes-v1.js?v={FINAL_VERSION}"></script>'
    )

    text = FINAL_CSS_RE.sub('', text)
    text = FINAL_JS_RE.sub('', text)

    if '</head>' not in text or '</body>' not in text:
        raise RuntimeError('missing head/body closing tag')

    text = text.replace('</head>', css + '</head>', 1)
    text = text.replace('</body>', js + '</body>', 1)
    return text


def fix(path: Path, he: bool, home: bool = False) -> bool:
    text = path.read_text(encoding='utf-8')
    old = text

    text, n = HEADER_RE.subn(build_header(path, he, home), text, count=1)
    if n != 1:
        raise RuntimeError(f'header count failed: {path}')

    text = re.sub(
        r'bpi-files-feedback-fixes\.js\?v=[^"\']+',
        f'bpi-files-feedback-fixes.js?v={SHARED_NAV_VERSION}',
        text,
    )
    text = install_final_assets(text, home)

    if text != old:
        path.write_text(text, encoding='utf-8')
        return True
    return False


def verify(path: Path, he: bool, home: bool = False):
    text = path.read_text(encoding='utf-8')
    header_match = HEADER_RE.search(text)
    if not header_match:
        raise RuntimeError(f'missing header: {path}')

    header = header_match.group(0)
    nav_match = re.search(r'<nav[^>]*class="site-nav"[^>]*>(.*?)</nav>', header, re.S)
    if not nav_match:
        raise RuntimeError(f'missing site nav: {path}')

    labels = re.findall(r'<a(?:\s[^>]*)?>(.*?)</a>', nav_match.group(1), re.S)
    labels = [re.sub(r'<.*?>', '', x).strip() for x in labels]
    expected = [x[0] for x in (HE if he else EN)]

    if labels != expected:
        raise RuntimeError(f'bad nav {path}: {labels}')
    if len(labels) != len(set(labels)):
        raise RuntimeError(f'duplicate labels {path}: {labels}')

    key = active(path, he, home)
    valid_keys = HE_KEYS if he else EN_KEYS
    expected_active = 1 if key in valid_keys else 0
    if header.count('aria-current="page"') != expected_active:
        raise RuntimeError(f'bad active count {path}')

    if text.count('id="bpi-final-requested-fixes"') != 1:
        raise RuntimeError(f'bad final stylesheet count: {path}')
    if text.count('id="bpi-final-requested-fixes-runtime"') != 1:
        raise RuntimeError(f'bad final runtime count: {path}')


def main():
    changed = []
    targets = [(SITE / 'index.html', True, True), (SITE / 'en.html', False, True)]
    targets += [(p, True, False) for p in sorted((SITE / 'pages' / 'he').glob('*.html'))]
    targets += [(p, False, False) for p in sorted((SITE / 'pages' / 'en').glob('*.html'))]

    for path, he, home in targets:
        if path.exists() and '<header class="site-header"' in path.read_text(encoding='utf-8'):
            if fix(path, he, home):
                changed.append(str(path.relative_to(ROOT)))
            verify(path, he, home)

    print('\n'.join(changed) if changed else 'No changes')


if __name__ == '__main__':
    main()
