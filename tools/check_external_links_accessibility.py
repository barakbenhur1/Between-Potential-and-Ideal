from pathlib import Path
from html import unescape
import json
import re
import sys

HTML_FILES = sorted(Path("site").rglob("*.html"))
REPORT_DIR = Path("reports/production_next")
EXPECTED_MIN_BLANK_LINKS = 1

LINK_RE = re.compile(r"<a\b[^>]*>", re.I | re.S)


def attr(tag, name):
    m = re.search(r"\b" + re.escape(name) + r"\s*=\s*([\"\x27])([^\"\x27]*)\1", tag, re.I | re.S)
    return unescape(m.group(2)).strip() if m else ""


def is_blank(tag):
    return attr(tag, "target").lower() == "_blank"


def has_safe_rel(tag):
    rel = attr(tag, "rel").lower().split()
    return "noopener" in rel and "noreferrer" in rel


def has_new_tab_label(tag):
    aria = attr(tag, "aria-label").lower()
    title = attr(tag, "title").lower()
    combined = aria + " " + title
    phrases = [
        "opens in a new tab",
        "opens in new tab",
        "new tab",
        "נפתח בכרטיסייה חדשה",
        "כרטיסייה חדשה",
    ]
    return any(p in combined for p in phrases)


def write_report(checked, errors, warnings):
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "checked": checked,
        "errors": errors,
        "warnings": warnings,
    }
    (REPORT_DIR / "external_links_accessibility_audit.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    lines = [
        "# External/New-Tab Links Accessibility Audit",
        "",
        f"- Checked: {checked}",
        f"- Errors: {len(errors)}",
        f"- Warnings: {len(warnings)}",
        "",
    ]
    if errors:
        lines.append("## Errors")
        for error in errors[:200]:
            lines.append(f"- {error}")
        lines.append("")
    if warnings:
        lines.append("## Warnings")
        for warning in warnings[:200]:
            lines.append(f"- {warning}")
        lines.append("")
    lines.append("Missing `rel=\"noopener noreferrer\"` is a release blocker. Missing new-tab label is currently reported as a warning.")
    (REPORT_DIR / "external_links_accessibility_audit.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    errors = []
    warnings = []
    checked = 0

    for path in HTML_FILES:
        html = path.read_text(encoding="utf-8", errors="ignore")
        for m in LINK_RE.finditer(html):
            tag = m.group(0)
            if not is_blank(tag):
                continue
            checked += 1
            href = attr(tag, "href")
            if not has_safe_rel(tag):
                errors.append(f"{path}: target=_blank missing rel noopener noreferrer: {href}")
            if not has_new_tab_label(tag):
                warnings.append(f"{path}: target=_blank missing accessible new-tab label: {href}")

    if checked < EXPECTED_MIN_BLANK_LINKS:
        errors.append(f"expected at least {EXPECTED_MIN_BLANK_LINKS} target=_blank link, found {checked}")

    write_report(checked, errors, warnings)

    if errors:
        print("FAIL: external/new-tab link accessibility audit found issues")
        for e in errors[:200]:
            print("-", e)
        if len(errors) > 200:
            print(f"... and {len(errors) - 200} more")
        if warnings:
            print(f"WARNINGS: {len(warnings)} target=_blank links missing accessible new-tab label")
        print("Report: reports/production_next/external_links_accessibility_audit.md")
        return 1

    print(f"OK: external/new-tab links are accessible. checked={checked}")
    if warnings:
        print(f"WARNINGS: {len(warnings)} target=_blank links missing accessible new-tab label")
        for warning in warnings[:40]:
            print("-", warning)
        if len(warnings) > 40:
            print(f"... and {len(warnings) - 40} more")
    print("Report: reports/production_next/external_links_accessibility_audit.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
