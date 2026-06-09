#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
OUT = ROOT / "localization" / "audits" / "source-inventory.json"
TEXT_SUFFIXES = {".html", ".md", ".txt", ".json", ".xml"}
PACKAGE_TOKENS = (
    "between-potential-and-ideal",
    "editorial",
    "stories-before-thought",
    "nauseating",
    "what-ai-believes",
    "when-i-am-also-you",
    "reverse-turing",
)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def main() -> int:
    pages = {
        code: [rel(path) for path in sorted((SITE / "pages" / code).glob("*.html"))]
        if (SITE / "pages" / code).exists()
        else []
        for code in ("he", "en", "tlh", "qya")
    }
    files = []
    for path in sorted((SITE / "files").rglob("*")):
        if not path.is_file():
            continue
        lower = path.name.lower()
        if path.suffix.lower() in TEXT_SUFFIXES or any(token in lower for token in PACKAGE_TOKENS):
            files.append({
                "path": rel(path),
                "suffix": path.suffix.lower(),
                "bytes": path.stat().st_size,
            })
    payload = {
        "homes": [rel(path) for path in (SITE / "index.html", SITE / "en.html", SITE / "tlh.html", SITE / "qya.html") if path.exists()],
        "pages": pages,
        "page_counts": {code: len(items) for code, items in pages.items()},
        "candidate_files": files,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote={rel(OUT)}")
    print(f"candidate_files={len(files)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
