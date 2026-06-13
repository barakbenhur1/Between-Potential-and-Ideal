#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import html
import importlib.util
import json
import re
import sys
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
CORE_PATH = ROOT / "tools" / "build_localized_public_release_core.py"


def load_core():
    spec = importlib.util.spec_from_file_location("bpi_localization_release_core", CORE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {CORE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


B = load_core()
SITE = B.SITE
BASE_URL = B.BASE_URL
LANGUAGES = B.LANGUAGES
PACKAGES = B.PACKAGES
PAGE_SLUGS = B.PAGE_SLUGS


def source_route(language: str, slug: str | None = None) -> str:
    return B.source_route(language, slug)


def menu_block(current: str, slug: str | None, asset_prefix: str) -> str:
    names = {"he": "עברית", "en": "English", "tlh": "tlhIngan Hol", "qya": "Neo-Quenya"}
    links = []
    for code, name in names.items():
        current_attr = ' aria-current="page"' if code == current else ""
        links.append(
            f'<a class="bpi-language-option" href="{html.escape(source_route(code, slug))}" '
            f'hreflang="{code}"{current_attr}>{html.escape(name)}</a>'
        )
    return (
        f'<link id="bpi-four-language-localization" rel="stylesheet" '
        f'href="{asset_prefix}assets/bpi-four-language-localization.css?v=20260613-v2">'
        '<details class="bpi-language-menu">'
        '<summary aria-label="Choose language">'
        '<span class="bpi-language-menu-icon" aria-hidden="true">🌐</span>'
        f'<span class="bpi-language-menu-current">{html.escape(names[current])}</span>'
        '</summary>'
        f'<div class="bpi-language-menu-panel">{"".join(links)}</div>'
        '</details>'
    )


def patch_existing_page(path: Path, language: str, slug: str | None, asset_prefix: str) -> None:
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    for tag in soup.head.find_all("link", rel=lambda value: value and ("alternate" in value or "canonical" in value)):
        tag.decompose()
    canonical = soup.new_tag("link", rel="canonical", href=f"{BASE_URL}{source_route(language, slug)}")
    soup.head.append(canonical)
    for code in ("he", "en", "tlh", "qya"):
        alternate = soup.new_tag("link", rel="alternate", hreflang=code, href=f"{BASE_URL}{source_route(code, slug)}")
        soup.head.append(alternate)
    default = soup.new_tag("link", rel="alternate", hreflang="x-default", href=f"{BASE_URL}/en.html")
    soup.head.append(default)
    old_stylesheet = soup.find("link", id="bpi-four-language-localization")
    if old_stylesheet:
        old_stylesheet["href"] = f"{asset_prefix}assets/bpi-four-language-localization.css?v=20260613-v2"
    else:
        stylesheet = soup.new_tag(
            "link",
            id="bpi-four-language-localization",
            rel="stylesheet",
            href=f"{asset_prefix}assets/bpi-four-language-localization.css?v=20260613-v2",
        )
        soup.head.append(stylesheet)
    header = soup.find("header", class_="site-header")
    if header:
        for node in header.select(".language-switch, .bpi-language-menu"):
            node.decompose()
        fragment = BeautifulSoup(menu_block(language, slug, asset_prefix), "html.parser")
        detail = fragment.find("details")
        if detail:
            header.append(detail)
    path.write_text(str(soup), encoding="utf-8")


def patch_existing_languages() -> None:
    patch_existing_page(SITE / "index.html", "he", None, "")
    patch_existing_page(SITE / "en.html", "en", None, "")
    for slug in PAGE_SLUGS:
        patch_existing_page(SITE / "pages" / "he" / f"{slug}.html", "he", slug, "../../")
        patch_existing_page(SITE / "pages" / "en" / f"{slug}-en.html", "en", slug, "../../")


def write_shared_css() -> None:
    path = SITE / "assets" / "bpi-four-language-localization.css"
    path.write_text(
        """
.bpi-language-menu{position:relative;justify-self:end;z-index:2000;font-family:inherit}
.bpi-language-menu>summary{list-style:none;cursor:pointer;display:inline-flex;align-items:center;justify-content:center;gap:.5rem;min-height:42px;padding:.62rem .9rem;border:1px solid rgba(242,196,94,.52);border-radius:999px;background:rgba(5,8,13,.9);color:#f2c45e;font-weight:800;white-space:nowrap;box-shadow:0 8px 28px rgba(0,0,0,.3)}
.bpi-language-menu>summary::-webkit-details-marker{display:none}.bpi-language-menu>summary::after{content:'▾';font-size:.74em;opacity:.82}.bpi-language-menu[open]>summary::after{content:'▴'}
.bpi-language-menu-icon{font-size:1.08rem;line-height:1;transform:translateY(-.02em)}.bpi-language-menu-current{unicode-bidi:isolate}
.bpi-language-menu-panel{position:absolute;inset-inline-end:0;top:calc(100% + .55rem);display:grid;min-width:190px;padding:.5rem;border:1px solid rgba(255,255,255,.18);border-radius:16px;background:#080c13;box-shadow:0 18px 60px rgba(0,0,0,.58)}
.bpi-language-menu-panel a{display:block;padding:.72rem .82rem;border-radius:11px;color:#e9edf5;text-decoration:none;font-weight:700;text-align:start}.bpi-language-menu-panel a:hover,.bpi-language-menu-panel a:focus-visible,.bpi-language-menu-panel a[aria-current='page']{background:rgba(242,196,94,.13);color:#f2c45e}
.bpi-localized-content{max-width:980px;margin:clamp(1rem,3vw,2rem) auto;padding:clamp(1.1rem,4vw,2.3rem);overflow-wrap:anywhere}.bpi-localized-content .language-status-note{margin:0 0 1.35rem;padding:1rem 1.1rem;color:#d9e1ed}.bpi-localized-content h2,.bpi-localized-content h3,.bpi-localized-content h4{scroll-margin-top:8rem}.bpi-localized-content img{max-width:100%;height:auto;border-radius:18px}.bpi-localized-download-grid{margin-top:clamp(1rem,3vw,2rem)}.bpi-document-main{max-width:1100px;margin-inline:auto;padding:clamp(1rem,4vw,3rem)}.bpi-localized-opening{margin-top:clamp(1rem,4vw,3rem)}
@media(max-width:860px){.site-header .bpi-language-menu{order:2;align-self:center;justify-self:center}.bpi-language-menu-panel{position:fixed;left:1rem;right:1rem;top:auto;bottom:1rem;min-width:0;grid-template-columns:repeat(2,minmax(0,1fr));z-index:10000}.bpi-language-menu-panel a{text-align:center}.bpi-localized-content{padding:1rem}}
""".strip() + "\n",
        encoding="utf-8",
    )


def update_sitemap() -> None:
    path = SITE / "sitemap.xml"
    namespace = "http://www.sitemaps.org/schemas/sitemap/0.9"
    ET.register_namespace("", namespace)
    try:
        tree = ET.parse(path)
        root = tree.getroot()
    except (FileNotFoundError, ET.ParseError):
        root = ET.Element(f"{{{namespace}}}urlset")
        tree = ET.ElementTree(root)
    existing = {node.text for node in root.findall(f"{{{namespace}}}url/{{{namespace}}}loc") if node.text}
    urls = []
    for language in LANGUAGES:
        urls.append(f"{BASE_URL}/{language}.html")
        urls.extend(f"{BASE_URL}/pages/{language}/{slug}.html" for slug in PAGE_SLUGS)
        urls.extend(f"{BASE_URL}/files/{language}/{package}-{language}.html" for package in PACKAGES)
    for url in urls:
        if url in existing:
            continue
        item = ET.SubElement(root, f"{{{namespace}}}url")
        ET.SubElement(item, f"{{{namespace}}}loc").text = url
    ET.indent(tree, space="  ")
    tree.write(path, encoding="utf-8", xml_declaration=True)


def update_search_index() -> None:
    from bs4 import BeautifulSoup

    entries = []
    for language in LANGUAGES:
        paths = [(SITE / f"{language}.html", f"/{language}.html")]
        paths.extend((SITE / "pages" / language / f"{slug}.html", f"/pages/{language}/{slug}.html") for slug in PAGE_SLUGS)
        for path, url in paths:
            soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
            title = soup.title.get_text(" ", strip=True) if soup.title else path.stem
            main = soup.find("main")
            text = (main or soup).get_text(" ", strip=True)
            entries.append({"language": language, "url": url, "title": title, "text": re.sub(r"\s+", " ", text)[:4000]})
    output = SITE / "data" / "localization-search-index.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(entries, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_metadata() -> None:
    config_path = ROOT / "localization" / "config.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    for language in LANGUAGES:
        config["languages"][language]["publish"] = True
        config["languages"][language]["publication_note"] = "machine-assisted experimental edition; automated structural QA complete"
    config_path.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    manifest_path = ROOT / "localization" / "translation-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["status"] = "public-release-built"
    manifest["completed_languages"] = list(LANGUAGES)
    manifest["review_disclosure"] = "Machine-assisted experimental editions; not represented as expert linguistic certification."
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    write_shared_css()
    for language in LANGUAGES:
        bodies = B.package_bodies(language)
        for package in PACKAGES:
            B.write_package(language, package, bodies[package])
        B.write_pages(language)
    patch_existing_languages()
    update_sitemap()
    update_search_index()
    update_metadata()
    B.write_release_manifest()
    print("LOCALIZED PUBLIC RELEASE BUILT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
