from pathlib import Path
from html import unescape
import re
import sys

HTML_FILES = sorted(Path("site").rglob("*.html"))

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

    if errors:
        print("FAIL: external/new-tab link accessibility audit found issues")
        for e in errors[:200]:
            print("-", e)
        if len(errors) > 200:
            print(f"... and {len(errors) - 200} more")
        if warnings:
            print(f"WARNINGS: {len(warnings)} target=_blank links missing accessible new-tab label")
        return 1

    print(f"OK: external/new-tab links are accessible. checked={checked}")
    if warnings:
        print(f"WARNINGS: {len(warnings)} target=_blank links missing accessible new-tab label")
        for warning in warnings[:40]:
            print("-", warning)
        if len(warnings) > 40:
            print(f"... and {len(warnings) - 40} more")
    return 0


if __name__ == "__main__":
    sys.exit(main())
