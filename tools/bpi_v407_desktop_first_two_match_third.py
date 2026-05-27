#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path.cwd()
SITE = ROOT / "site"
CSS_FILE = SITE / "styles.css"

CSS_BLOCK = """
/* BPI V407 - desktop: make first two homepage cards match the third visual card width.
   Scope: homepage only. Mobile is intentionally untouched; V406 keeps 12px side margins.
   This only changes desktop width alignment for:
   1) Start Here white card
   2) Blue thought/hero card
   3) Opening image/visual card
*/
@media (min-width: 769px){
  body.bpi-home-width-clean{
    --bpi-home-card-width: min(1680px, calc(100vw - 96px));
  }

  body.bpi-home-width-clean .site-main > :is(
    .bpi-start-here-note,
    .hero.concise-hero,
    .opening-visual
  ){
    width: var(--bpi-home-card-width) !important;
    max-width: var(--bpi-home-card-width) !important;
    margin-left: auto !important;
    margin-right: auto !important;
    box-sizing: border-box !important;
  }
}
""".strip()

def main():
    if not SITE.exists():
        raise SystemExit("ERROR: run from repository root — the directory that contains site/")
    if not CSS_FILE.exists():
        raise SystemExit("ERROR: site/styles.css not found")

    original = CSS_FILE.read_text(encoding="utf-8", errors="ignore")
    css = original

    # Remove prior V407 if rerun, then append clean block.
    css = re.sub(
        r'\n/\* BPI V407 - desktop: make first two homepage cards match the third visual card width\..*?(?=\n/\*|\Z)',
        '\n',
        css,
        flags=re.S
    ).rstrip() + "\n" + CSS_BLOCK + "\n"

    CSS_FILE.write_text(css, encoding="utf-8")

    report = [
        "BPI V407 desktop card width alignment",
        "",
        "Changed:",
        "- Desktop only: first two homepage cards now use the same width as the third visual/image card.",
        "- Mobile untouched: keeps the previous 12px side margin behavior.",
        "- No content changes.",
        "- No theory/appendix/document changes.",
        "",
        "Files changed:",
        "- site/styles.css",
        "",
        "Manual QA:",
        "- Desktop: Start Here white card, blue thought/hero card, and image card below are same width.",
        "- Mobile: still centered with about 12px side margins.",
        "- Start Here still appears once and has 3 buttons.",
    ]

    problems = []
    new_css = CSS_FILE.read_text(encoding="utf-8", errors="ignore")
    if "BPI V407" not in new_css:
        problems.append("V407 block missing after write")
    if "calc(100vw - 96px)" not in new_css:
        problems.append("desktop 96px width rule missing")
    if "padding-left:12px!important" not in new_css and "padding-left: 12px" not in new_css:
        problems.append("warning: could not detect V406 12px mobile padding; verify mobile manually")

    if problems:
        report.append("")
        report.append("WARNINGS/FAILED CHECKS:")
        report.extend([f"- {p}" for p in problems])

    report.append("")
    report.append("OK" if not any("missing" in p for p in problems) else "CHECK MANUALLY")
    (ROOT / "BPI_V407_DESKTOP_CARD_WIDTH_REPORT.txt").write_text("\n".join(report) + "\n", encoding="utf-8")
    print("\n".join(report))

if __name__ == "__main__":
    main()
