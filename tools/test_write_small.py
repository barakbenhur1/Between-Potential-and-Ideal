from pathlib import Path
import html
import re

from bs4 import BeautifulSoup

import a as D

ROOT = D.ROOT
SITE = D.SITE
BASE = D.BASE_URL

NAMES = {
    "he": "עברית",
    "en": "English",
    "tlh": "tlhIngan Hol",
    "qya": "Neo-Quenya",
}

NAV = (
    "summary",
    "glossary",
    "potential-ideal-optimal",
    "ai-as-witness",
    "methodology",
    "core",
    "witness",
    "applied",
    "ai",
    "files",
    "critique",
    "sources",
)

COPY = {
    "tlh": {
        "warning": "mughghachvam beta 'oH; Hol po'wI' nuDghach taH.",
        "review": "Hol po'wI' nuDghach",
        "files": "ghItlh naQ laDlaHlu' HTML, PDF, DOCX, Markdown, TXT je lo'taHvIS.",
    },
    "qya": {
        "warning": "I quentalë quanta ná sí laitanwa ve public beta. I lambë ná Neo-Quenya, ar i metta parmaquetalië lemya carienna.",
        "review": "Lambë parmaquetalië",
        "files": "I quentalë quanta polë cenda mi HTML, PDF, DOCX, Markdown ar TXT.",
    },
}

THUMBNAILS = {
    "summary": "thumb_methodology.png",
    "glossary": "thumb_methodology.png",
    "potential-ideal-optimal": "thumb_core.png",
    "ai-as-witness": "thumb_witness.png",
    "methodology": "thumb_methodology.png",
    "core": "thumb_core.png",
    "witness": "thumb_witness.png",
    "stories": "thumb_witness.png",
    "applied": "thumb_applied.png",
    "law-of-potential": "thumb_applied.png",
    "medicine-of-potential": "thumb_applied.png",
    "education-of-potential": "thumb_applied.png",
    "art-of-potential": "thumb_applied.png",
    "music-of-potential": "thumb_applied.png",
    "ai": "thumb_ai.png",
    "ai-believes": "thumb_ai.png",
    "ai-open-problems": "thumb_ai.png",
    "files": "thumb_methodology.png",
    "sources": "thumb_methodology.png",
    "critique": "thumb_core.png",
}

EXCERPT_CONTROL_MARKERS = (
    "image description draft:",
    "image description:",
    "visual description draft:",
    "visual description:",
    "visual brief:",
    "alt text:",
    "translation control note",
    "editorial note:",
    "production note:",
    "source note:",
    "segment review gate",
    "placeholder review gate",
)


def route(lang, slug=None):
    if slug is None:
        return "/index.html" if lang == "he" else f"/{lang}.html"
    if lang == "he":
        return f"/pages/he/{slug}.html"
    if lang == "en":
        return f"/pages/en/{slug}-en.html"
    return f"/pages/{lang}/{slug}.html"


def warning(lang):
    return COPY[lang]["warning"]


def review_url(lang):
    return f'https://github.com/barakbenhur1/Between-Potential-and-Ideal/issues/{11 if lang == "tlh" else 10}'


def menu(lang, slug=None):
    links = "".join(
        f'<a href="{route(code, slug)}" hreflang="{code}"'
        + (' aria-current="page"' if code == lang else "")
        + f">{name}</a>"
        for code, name in NAMES.items()
    )
    return (
        f'<details class="bpi-language-menu"><summary aria-label="Language">{NAMES[lang]}</summary>'
        f'<div class="bpi-language-menu-panel">{links}</div></details>'
    )


def alternates(slug=None):
    return "".join(
        f'<link rel="alternate" hreflang="{code}" href="{BASE}{route(code, slug)}">'
        for code in NAMES
    ) + f'<link rel="alternate" hreflang="x-default" href="{BASE}/en.html">'


def nav(lang, current, prefix):
    links = [
        f'<a href="{prefix}{lang}.html"'
        + (' class="active" aria-current="page"' if current is None else "")
        + f">{NAMES[lang]}</a>"
    ]
    for slug in NAV:
        mark = ' class="active" aria-current="page"' if slug == current else ""
        links.append(
            f'<a href="{prefix}pages/{lang}/{slug}.html"{mark}>'
            f"{html.escape(D.title(lang, slug))}</a>"
        )
    return "".join(links)


def head(lang, title, slug, prefix, home=False):
    style = (
        f"{prefix}styles-home-original.css?v=20260527-v430-non-home-repair"
        if home
        else f"{prefix}styles.css?v=20260604-tabbar-dimensions-v2"
    )
    description = f"{title} — {NAMES[lang]}"
    return (
        '<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        f"<title>{html.escape(title)} - Between Potential and Ideal</title>"
        f'<meta name="description" content="{html.escape(description)}">'
        '<meta name="robots" content="index,follow">'
        f'<link rel="canonical" href="{BASE}{route(lang, slug)}">{alternates(slug)}'
        f'<link rel="stylesheet" href="{style}">'
        f'<link rel="stylesheet" href="{prefix}styles.css?v=20260604-tabbar-dimensions-v2">'
        f'<link rel="stylesheet" href="{prefix}assets/bpi-four-language-localization.css?v=20260612-full-site-v3">'
        "</head>"
    )


def header(lang, current, prefix):
    return (
        '<a class="skip-link" href="#main">Skip to main content</a>'
        '<header class="site-header">'
        f'<div class="site-brand"><a href="{prefix}{lang}.html">Between Potential and Ideal</a></div>'
        f'<nav class="site-nav" aria-label="Primary navigation">{nav(lang, current, prefix)}</nav>'
        f"{menu(lang, current)}</header>"
    )


def note(lang):
    return (
        '<aside class="language-status-note"><strong>Public Beta</strong>'
        f"<p>{html.escape(warning(lang))}</p>"
        f'<a href="{review_url(lang)}">{html.escape(COPY[lang]["review"])}</a></aside>'
    )


def downloads(lang, prefix):
    stem = f"between-potential-and-ideal-{lang}"
    return '<div class="download-row bpi-localized-download-grid">' + "".join(
        f'<a class="download-button" href="{prefix}files/{lang}/{stem}.{ext}">{ext.upper()}</a>'
        for ext in ("html", "pdf", "docx", "md", "txt")
    ) + "</div>"


def thumbnail(slug):
    return THUMBNAILS.get(slug, "thumb_core.png")


def excerpt(lang, slug, limit=360):
    if slug == "files":
        return COPY[lang]["files"]
    text = D.body(lang, slug)
    for block in re.split(r"\n\s*\n", text):
        candidate = block.strip()
        if not candidate or candidate.startswith(("#", "![", "```", ">")):
            continue
        candidate = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", candidate)
        candidate = re.sub(r"[*_`]+", "", candidate)
        candidate = re.sub(r"^\s*(?:[-+*]|\d+\.)\s+", "", candidate)
        candidate = BeautifulSoup(candidate, "html.parser").get_text(" ", strip=True)
        candidate = re.sub(r"\s+", " ", candidate).strip()
        lowered = candidate.casefold()
        if any(marker in lowered for marker in EXCERPT_CONTROL_MARKERS):
            continue
        if len(candidate) < 70:
            continue
        if len(candidate) <= limit:
            return candidate
        shortened = candidate[: limit + 1].rsplit(" ", 1)[0].rstrip(" ,;:-")
        return shortened + "…"
    return D.title(lang, slug)


def card(lang, slug, accent):
    title = D.title(lang, slug)
    image = thumbnail(slug)
    return (
        f'<article class="hub-card media-card accent-{accent}">'
        '<div class="card-media-head">'
        f'<img alt="{html.escape(title)}" class="card-thumb" decoding="async" loading="lazy" '
        f'src="figures/{image}"><h2>{html.escape(title)}</h2></div>'
        f"<p>{html.escape(excerpt(lang, slug))}</p>"
        f'<a class="card-link" href="pages/{lang}/{slug}.html">{html.escape(title)} →</a>'
        "</article>"
    )


def write_home(lang):
    title = D.title(lang, "summary")
    hero_lead = excerpt(lang, "summary", 430)
    method_note = excerpt(lang, "methodology", 430)

    primary = "".join(
        card(lang, slug, accent)
        for slug, accent in (
            ("core", "core"),
            ("witness", "witness"),
            ("applied", "applied"),
        )
    )
    gateways = "".join(
        card(lang, slug, accent)
        for slug, accent in (
            ("summary", "core"),
            ("glossary", "core"),
            ("ai-as-witness", "witness"),
            ("methodology", "applied"),
            ("ai", "witness"),
            ("files", "applied"),
        )
    )
    featured = {
        "core",
        "witness",
        "applied",
        "summary",
        "glossary",
        "ai-as-witness",
        "methodology",
        "ai",
        "files",
    }
    remaining = "".join(
        f'<a href="pages/{lang}/{slug}.html">{html.escape(D.title(lang, slug))}</a>'
        for slug in D.PAGES
        if slug not in featured
    )

    doc = (
        f'<!doctype html><html lang="{lang}" dir="ltr">'
        f'{head(lang, NAMES[lang], None, "", True)}'
        '<body class="public-page design-prompt-theme bpi-home-page">'
        f'{header(lang, None, "")}<main class="site-main" id="main">'
        f"{note(lang)}"
        '<section class="hero concise-hero">'
        '<p class="kicker">Between Potential and Ideal</p>'
        f"<h1>{html.escape(title)}</h1>"
        f'<p class="lead">{html.escape(hero_lead)}</p>'
        f'<p class="method-note">{html.escape(method_note)}</p>'
        '<div class="hero-cta-row">'
        f'<a class="download-button primary" href="pages/{lang}/summary.html">{html.escape(D.title(lang, "summary"))}</a>'
        f'<a class="download-button" href="pages/{lang}/core.html">{html.escape(D.title(lang, "core"))}</a>'
        "</div></section>"
        '<figure class="opening-visual">'
        '<img src="figures/homepage_hero_replacement_v43.png" alt="Between Potential and Ideal" '
        'decoding="async" loading="eager">'
        f"<figcaption>{html.escape(title)}</figcaption></figure>"
        '<section class="notice-box bpi-start-here-note media-card accent-core homepage-start-card">'
        '<div class="card-media-head">'
        f'<img alt="{html.escape(title)}" class="card-thumb" decoding="async" loading="lazy" '
        'src="figures/thumb_methodology.png">'
        f"<h2>{html.escape(title)}</h2></div>"
        f"<p>{html.escape(warning(lang))}</p>"
        f"{downloads(lang, '')}</section>"
        f'<section class="hub-grid three">{primary}</section>'
        f'<section class="hub-grid three bpi-gateway-cards">{gateways}</section>'
        '<section class="reader-card">'
        f"<h2>{html.escape(NAMES[lang])}</h2>"
        f'<div class="bpi-localized-link-grid">{remaining}</div></section>'
        "</main>"
        f"<footer class=\"site-footer\"><p>Between Potential and Ideal — {NAMES[lang]} Public Beta</p></footer>"
        "</body></html>"
    )
    (SITE / f"{lang}.html").write_text(doc, encoding="utf-8")
