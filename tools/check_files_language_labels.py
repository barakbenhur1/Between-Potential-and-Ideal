from pathlib import Path
import re
import sys

CHECKS = {
    Path("site/pages/en/files-en.html"): [
        (r">\s*עברית\s*<", "English files page has visible Hebrew language label: עברית"),
        (r">\s*אנגלית\s*<", "English files page has visible Hebrew language label: אנגלית"),
        (r">\s*מעורב\s*/\s*מקור\s*<", "English files page has visible Hebrew label: מעורב / מקור"),
    ],
    Path("site/pages/he/files.html"): [
        (r">\s*English\s*<", "Hebrew files page has visible English language label: English"),
        (r">\s*Mixed\s*/\s*source\s*<", "Hebrew files page has visible English label: Mixed/source"),
        (r">\s*All languages\s*<", "Hebrew files page has visible English label: All languages"),
        (r">\s*All formats\s*<", "Hebrew files page has visible English label: All formats"),
    ],
}

# A language switch intentionally names the destination language and may therefore
# contain text from the opposite language. Exclude only that navigation control;
# file filters, table labels, cards, and all other visible page content remain audited.
LANGUAGE_SWITCH_RE = re.compile(
    r'<a\b(?=[^>]*\bclass\s*=\s*["\'][^"\']*\blanguage-switch\b[^"\']*["\'])[^>]*>.*?</a>',
    flags=re.I | re.S,
)


def main() -> int:
    errors = []

    for path, patterns in CHECKS.items():
        if not path.exists():
            errors.append(f"missing file: {path}")
            continue

        html = path.read_text(encoding="utf-8", errors="ignore")
        audited_html = LANGUAGE_SWITCH_RE.sub("", html)

        for pattern, message in patterns:
            if re.search(pattern, audited_html, flags=re.I):
                errors.append(f"{path}: {message}")

    if errors:
        print("FAIL: files language label audit found issues")
        for error in errors:
            print("-", error)
        return 1

    print("OK: files language labels match page language.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
