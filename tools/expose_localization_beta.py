#!/usr/bin/env python3
"""Expose completed localization packages without adding a homepage beta banner."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
BETA_MANIFEST = ROOT / "localization/beta-release-manifest.json"
START = "<!-- localization-public-beta-links:start -->"
END = "<!-- localization-public-beta-links:end -->"


def remove_legacy_beta_banner(text: str) -> str:
    while START in text and END in text:
        before, rest = text.split(START, 1)
        _, after = rest.split(END, 1)
        text = before + after
    return text


def patch_home(path: Path) -> None:
    text = remove_legacy_beta_banner(path.read_text(encoding="utf-8"))
    alternates = (
        '<link href="https://between-potential-and-ideal.onrender.com/tlh.html" hreflang="tlh" rel="alternate"/>'
        '<link href="https://between-potential-and-ideal.onrender.com/qya.html" hreflang="qya" rel="alternate"/>'
    )
    if 'hreflang="tlh"' not in text:
        text = text.replace("</head>", alternates + "</head>", 1)
    required = (
        'class="bpi-language-menu"',
        'href="/index.html"',
        'href="/en.html"',
        'href="/tlh.html"',
        'href="/qya.html"',
        'class="bpi-language-menu-icon"',
    )
    missing = [marker for marker in required if marker not in text]
    if missing:
        raise RuntimeError(
            f"Four-language menu is incomplete in {path.relative_to(ROOT)}: " + ", ".join(missing)
        )
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


def normalize_beta_assets() -> list[Path]:
    changed = []
    for language in ("tlh", "qya"):
        stem = f"between-potential-and-ideal-{language}"
        for extension in ("html", "md"):
            path = SITE / "files" / language / f"{stem}.{extension}"
            text = path.read_text(encoding="utf-8")
            normalized = re.sub(r"(?:\.\./)+figures/", "../../figures/", text)
            normalized = normalized.replace(
                "v25_chapter-boundary-horizons.png",
                "v25_chapter_boundary-horizons.png",
            )
            if normalized != text:
                path.write_text(normalized, encoding="utf-8")
                changed.append(path)
    return changed


def refresh_beta_manifest() -> None:
    data = json.loads(BETA_MANIFEST.read_text(encoding="utf-8"))
    for entry in data.get("files", []):
        path = ROOT / entry["path"]
        if not path.is_file():
            raise RuntimeError(f"Beta manifest target missing: {entry['path']}")
        payload = path.read_bytes()
        entry["bytes"] = len(payload)
        entry["sha256"] = hashlib.sha256(payload).hexdigest()
    BETA_MANIFEST.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    required = [
        SITE / "tlh.html",
        SITE / "qya.html",
        SITE / "files/tlh/between-potential-and-ideal-tlh.html",
        SITE / "files/qya/between-potential-and-ideal-qya.html",
        SITE / "files/tlh/between-potential-and-ideal-tlh.md",
        SITE / "files/qya/between-potential-and-ideal-qya.md",
        BETA_MANIFEST,
    ]
    missing = [path.relative_to(ROOT).as_posix() for path in required if not path.is_file()]
    if missing:
        raise RuntimeError("Missing beta outputs: " + ", ".join(missing))
    changed = normalize_beta_assets()
    refresh_beta_manifest()
    patch_home(SITE / "index.html")
    patch_home(SITE / "en.html")
    patch_sitemap()
    print(
        f"Exposed localized editions without a homepage beta banner and normalized {len(changed)} package files."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
