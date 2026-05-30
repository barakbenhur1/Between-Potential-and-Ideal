from pathlib import Path
from html import unescape
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

def main() -> int:
    errors = []

    for path, patterns in CHECKS.items():
        if not path.exists():
            errors.append(f"missing file: {path}")
            continue

        html = path.read_text(encoding="utf-8", errors="ignore")

        for pattern, message in patterns:
            if re.search(pattern, html, flags=re.I):
                errors.append(f"{path}: {message}")

    if errors:
        print("FAIL: files language label audit found issues")
        for e in errors:
            print("-", e)
        return 1

    print("OK: files language labels match page language.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
