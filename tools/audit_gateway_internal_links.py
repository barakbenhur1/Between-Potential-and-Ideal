from pathlib import Path
import json
import sys

SITE = Path("site")
REPORT_DIR = Path("reports/production_next")

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
    items = []

    for target in GATEWAYS:
        target_path = SITE / target
        if not target_path.exists():
            print(f"WARN: gateway file missing: {target}")
            warning_count += 1
            items.append({"target": target, "exists": False, "incoming": []})
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
        items.append({"target": target, "exists": True, "incoming": incoming})

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / "gateway_internal_links_audit.json").write_text(
        json.dumps({"warnings": warning_count, "items": items}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    lines = [
        "# Gateway Internal Links Audit",
        "",
        f"- Warnings: {warning_count}",
        "",
        "## Gateway incoming links",
    ]
    for item in items:
        lines.append(f"- `{item['target']}` — incoming files: {len(item['incoming'])}")
        for source in item["incoming"][:25]:
            lines.append(f"  - `{source}`")
    lines.append("")
    lines.append("Warnings are discoverability findings only and do not block release.")
    (REPORT_DIR / "gateway_internal_links_audit.md").write_text("\n".join(lines), encoding="utf-8")

    print(f"OK: gateway internal link audit completed. warnings={warning_count}")
    print("Report: reports/production_next/gateway_internal_links_audit.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
