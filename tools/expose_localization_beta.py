#!/usr/bin/env python3
"""Expose completed localization beta packages without claiming final approval."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
START = "<!-- localization-public-beta-links:start -->"
END = "<!-- localization-public-beta-links:end -->"


def beta_bar(language: str) -> str:
    if language == "he":
        label = "תרגומי בטא ציבוריים"
        detail = "התרגומים המלאים עדיין בביקורת לשונית"
    else:
        label = "Public beta translations"
        detail = "Complete editions; linguistic review is still ongoing"
    return (
        f'{START}<aside aria-label="{label}" style="padding:.75rem 1rem;text-align:center;'
        'background:#211b0e;color:#fff7db;border-bottom:2px solid #f2c45e">'
        f'<strong>{label}:</strong> <a href="tlh.html" style="color:#8edcff">tlhIngan Hol</a> · '
        f'<a href="qya.html" style="color:#8edcff">Neo-Quenya</a> '
        f'<small>— {detail}</small></aside>{END}'
    )


def patch_home(path: Path, language: str) -> None:
    text = path.read_text(encoding="utf-8")
    if START in text and END in text:
        before, rest = text.split(START, 1)
        _, after = rest.split(END, 1)
        text = before + after
    bar = beta_bar(language)
    if "</header>" not in text:
        raise RuntimeError(f"Missing header close in {path.relative_to(ROOT)}")
    text = text.replace("</header>", "</header>" + bar, 1)
    alternates = (
        '<link href="https://between-potential-and-ideal.onrender.com/tlh.html" hreflang="tlh" rel="alternate"/>'
        '<link href="https://between-potential-and-ideal.onrender.com/qya.html" hreflang="qya" rel="alternate"/>'
    )
    if 'hreflang="tlh"' not in text:
        text = text.replace("</head>", alternates + "</head>", 1)
    path.write_text(text, encoding="utf-8")


def patch_sitemap() -> None:
    path = SITE / "sitemap.xml"
    text = path.read_text(encoding="utf-8")
    urls = (
        "https://between-potential-and-ideal.onrender.com/tlh.html",
        "https://between-potential-and-ideal.onrender.com/qya.html",
        "https://between-potential-and-ideal.onrender.com/files/tlh/between-potential-and-ideal-tlh.html",
        "https://between-potential-and-ideal.onrender.com/files/qya/between-potential-and-ideal-qya.html",
    )
    additions = ""
    for url in urls:
        if f"<loc>{url}</loc>" not in text:
            additions += f"  <url><loc>{url}</loc></url>\n"
    if additions:
        text = text.replace("</urlset>", additions + "</urlset>")
        path.write_text(text, encoding="utf-8")


def main() -> int:
    required = [
        SITE / "tlh.html",
        SITE / "qya.html",
        SITE / "files/tlh/between-potential-and-ideal-tlh.html",
        SITE / "files/qya/between-potential-and-ideal-qya.html",
    ]
    missing = [path.relative_to(ROOT).as_posix() for path in required if not path.is_file()]
    if missing:
        raise RuntimeError("Missing beta outputs: " + ", ".join(missing))
    patch_home(SITE / "index.html", "he")
    patch_home(SITE / "en.html", "en")
    patch_sitemap()
    print("Exposed public beta editions in Hebrew/English homepages and sitemap.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
