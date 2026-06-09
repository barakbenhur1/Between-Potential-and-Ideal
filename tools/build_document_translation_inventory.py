#!/usr/bin/env python3
from pathlib import Path
import json
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
EN = ROOT / "site/files/between-potential-and-ideal-en.html"
HE = ROOT / "site/files/between-potential-and-ideal-he.html"
OUT = ROOT / "reports/localization/between-potential-and-ideal-inventory.json"


def clean(value):
    return " ".join((value or "").split())


def extract(path):
    soup = BeautifulSoup(path.read_text(encoding="utf-8", errors="ignore"), "html.parser")
    main = soup.find(id="main") or soup.body or soup
    headings = []
    for node in main.find_all(["h1", "h2", "h3", "h4"]):
        headings.append({
            "level": int(node.name[1]),
            "id": node.get("id"),
            "text": clean(node.get_text(" ", strip=True)),
        })
    figures = []
    for index, figure in enumerate(main.find_all("figure"), start=1):
        image = figure.find("img")
        caption = figure.find("figcaption")
        figures.append({
            "index": index,
            "src": image.get("src") if image else None,
            "alt": clean(image.get("alt")) if image else "",
            "caption": clean(caption.get_text(" ", strip=True)) if caption else "",
            "nearest_heading_id": nearest_heading_id(figure),
        })
    return {"headings": headings, "figures": figures}


def nearest_heading_id(node):
    previous = node.find_previous(["h1", "h2", "h3", "h4"])
    return previous.get("id") if previous else None


def main():
    if not EN.is_file() or not HE.is_file():
        raise SystemExit("English and Hebrew central documents must exist")
    payload = {
        "schema_version": 1,
        "document_id": "between-potential-and-ideal",
        "english_source": EN.relative_to(ROOT).as_posix(),
        "hebrew_cross_check": HE.relative_to(ROOT).as_posix(),
        "english": extract(EN),
        "hebrew": extract(HE),
    }
    payload["counts"] = {
        "english_headings": len(payload["english"]["headings"]),
        "hebrew_headings": len(payload["hebrew"]["headings"]),
        "english_figures": len(payload["english"]["figures"]),
        "hebrew_figures": len(payload["hebrew"]["figures"]),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload["counts"], ensure_ascii=False))
    print(OUT.relative_to(ROOT).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
