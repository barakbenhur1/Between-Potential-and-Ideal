#!/usr/bin/env python3
from pathlib import Path
import re
import json

ROOT = Path.cwd()
SITE = ROOT / "site"

TARGETS = [
    SITE / "index.html",
    SITE / "en.html",
]

REMOVE_PHRASES = {
    "index.html": [
        "מסלול קריאה קצר",
        "לפני הקריאה",
    ],
    "en.html": [
        "Short reading path",
        "Reading path",
        "Before reading",
        "Before you read",
    ],
}

# Matches a single section block. Homepage sections here are flat enough for this targeted cleanup.
SECTION_RE = re.compile(r"<section\b[^>]*>.*?</section>", re.I | re.S)

# Matches the blurbs block, whether implemented as section or div.
BLURBS_RE = re.compile(
    r"<(?P<tag>section|div)\b(?=[^>]*\b(?:signature-blurbs|refined-blurbs)\b)[^>]*>.*?</(?P=tag)>",
    re.I | re.S,
)

def remove_unwanted_cards(html: str, filename: str) -> tuple[str, list[str]]:
    removed = []

    def repl(match: re.Match) -> str:
        block = match.group(0)
        if any(phrase in block for phrase in REMOVE_PHRASES.get(filename, [])):
            # Do not remove the main Start Here card even if future copy contains similar wording.
            if 'id="bpi-start-here-note"' in block or "id='bpi-start-here-note'" in block:
                return block
            found = [phrase for phrase in REMOVE_PHRASES.get(filename, []) if phrase in block]
            removed.append(", ".join(found))
            return "\n"
        return block

    return SECTION_RE.sub(repl, html), removed

def move_blurbs_to_bottom(html: str) -> tuple[str, int]:
    blocks = [m.group(0) for m in BLURBS_RE.finditer(html)]
    if not blocks:
        return html, 0

    html_without = BLURBS_RE.sub("\n", html)
    blurbs_html = "\n".join(blocks).strip()

    # Put blurbs at the very bottom of the main content, before </main>.
    if "</main>" in html_without:
        html_without = html_without.replace("</main>", "\n" + blurbs_html + "\n</main>", 1)
    elif "</MAIN>" in html_without:
        html_without = html_without.replace("</MAIN>", "\n" + blurbs_html + "\n</MAIN>", 1)
    else:
        html_without = html_without.rstrip() + "\n" + blurbs_html + "\n"

    return html_without, len(blocks)

def cleanup_whitespace(html: str) -> str:
    html = re.sub(r"\n{3,}", "\n\n", html)
    return html

def patch_file(path: Path) -> dict:
    if not path.exists():
        return {"file": str(path), "missing": True}

    original = path.read_text(encoding="utf-8", errors="ignore")
    html = original

    html, removed_cards = remove_unwanted_cards(html, path.name)
    html, moved_blurbs = move_blurbs_to_bottom(html)
    html = cleanup_whitespace(html)

    path.write_text(html, encoding="utf-8")

    return {
        "file": str(path),
        "changed": html != original,
        "removed_cards": removed_cards,
        "moved_blurbs_blocks": moved_blurbs,
        "still_has_forbidden_phrases": [
            phrase for phrase in REMOVE_PHRASES.get(path.name, [])
            if phrase in html
        ],
        "blurbs_before_main_end": ("signature-blurbs" in html or "refined-blurbs" in html),
    }

def main():
    if not SITE.exists():
        raise SystemExit("ERROR: run from repo root — the directory that contains site/")

    results = [patch_file(path) for path in TARGETS]

    problems = []
    for r in results:
        if r.get("missing"):
            problems.append(f"missing target: {r['file']}")
            continue
        if r.get("still_has_forbidden_phrases"):
            problems.append(f"{r['file']}: still has {r['still_has_forbidden_phrases']}")
        if r.get("moved_blurbs_blocks", 0) == 0:
            problems.append(f"{r['file']}: no blurbs block found to move")

    report = [
        "BPI V418 remove extra homepage cards and move blurbs",
        "",
        "Changed:",
        "- Removed redundant cards: 'מסלול קריאה קצר' / 'לפני הקריאה' and English equivalents if present.",
        "- Moved blurbs block to the bottom of the homepage main content.",
        "- Did not touch Start Here, blue hero, opening image, theory documents, appendices, or content text except removing those cards.",
        "",
        "Results:",
        json.dumps(results, ensure_ascii=False, indent=2),
    ]

    if problems:
        report.append("")
        report.append("WARNINGS:")
        report.extend([f"- {p}" for p in problems])

    report.append("")
    report.append("OK" if not problems else "CHECK WARNINGS")
    (ROOT / "BPI_V418_REMOVE_EXTRA_CARDS_MOVE_BLURBS_REPORT.txt").write_text("\n".join(report) + "\n", encoding="utf-8")
    print("\n".join(report))

if __name__ == "__main__":
    main()
