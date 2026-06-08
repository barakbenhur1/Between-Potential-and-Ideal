#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
OUT = ROOT / "reports" / "localization" / "inventory.json"
FORMATS = (".html", ".pdf", ".docx", ".md", ".txt")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def pages(code: str) -> list[str]:
    folder = SITE / "pages" / code
    return [rel(p) for p in sorted(folder.rglob("*.html"))] if folder.exists() else []


def document_groups() -> list[dict]:
    groups = {}
    base = SITE / "files"
    if not base.exists():
        return []
    for path in sorted(base.rglob("*")):
        if path.is_file() and path.suffix.lower() in FORMATS:
            stem = rel(path.with_suffix(""))
            groups.setdefault(stem, {})[path.suffix[1:].lower()] = rel(path)
    required = [ext[1:] for ext in FORMATS]
    return [
        {
            "stem": stem,
            "formats": found,
            "missing": [fmt for fmt in required if fmt not in found],
        }
        for stem, found in sorted(groups.items())
    ]


def main() -> int:
    payload = {
        "homes": {
            "he": rel(SITE / "index.html") if (SITE / "index.html").exists() else None,
            "en": rel(SITE / "en.html") if (SITE / "en.html").exists() else None,
            "tlh": rel(SITE / "tlh.html") if (SITE / "tlh.html").exists() else None,
            "qya": rel(SITE / "qya.html") if (SITE / "qya.html").exists() else None,
        },
        "pages": {code: pages(code) for code in ("he", "en", "tlh", "qya")},
        "required_formats": [ext[1:] for ext in FORMATS],
        "document_groups": document_groups(),
    }
    payload["page_counts"] = {code: len(items) for code, items in payload["pages"].items()}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("OK: wrote", rel(OUT))
    print("page_counts=", payload["page_counts"])
    print("document_groups=", len(payload["document_groups"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
