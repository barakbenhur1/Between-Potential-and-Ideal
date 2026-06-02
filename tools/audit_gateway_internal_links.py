from pathlib import Path
import sys

SITE = Path("site")

GATEWAYS = [
    "pages/he/glossary.html",
    "pages/en/glossary-en.html",
    "pages/he/potential-ideal-optimal.html",
    "pages/en/potential-ideal-optimal-en.html",
    "pages/he/ai-as-witness.html",
    "pages/en/ai-as-witness-en.html",
]


def main() -> int:
    warning_count = 0
    html_files = list(SITE.rglob("*.html"))

    for target in GATEWAYS:
        target_path = SITE / target
        if not target_path.exists():
            print(f"WARN: gateway file missing: {target}")
            warning_count += 1
            continue

        incoming = []
        for html in html_files:
            if html == target_path:
                continue
            text = html.read_text(encoding="utf-8", errors="ignore")
            if target in text or target_path.name in text:
                incoming.append(str(html.relative_to(SITE)).replace("\\", "/"))

        print(f"gateway={target} incoming={len(incoming)}")
        if not incoming:
            print(f"WARN: no internal incoming link found for {target}")
            warning_count += 1

    print(f"OK: gateway internal link audit completed. warnings={warning_count}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
