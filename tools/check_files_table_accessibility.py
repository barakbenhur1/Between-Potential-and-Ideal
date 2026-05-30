from pathlib import Path
import re
import sys

FILES = [
    Path("site/pages/he/files.html"),
    Path("site/pages/en/files-en.html"),
]

TABLE_RE = re.compile(r"<table\b[^>]*class=[\"'][^\"']*download-table[^\"']*[\"'][^>]*>.*?</table>", re.I | re.S)

def main() -> int:
    errors = []

    for path in FILES:
        if not path.exists():
            errors.append(f"missing file: {path}")
            continue

        html = path.read_text(encoding="utf-8", errors="ignore")
        tables = list(TABLE_RE.finditer(html))

        if not tables:
            errors.append(f"{path}: no download-table found")
            continue

        for idx, m in enumerate(tables, start=1):
            table = m.group(0)

            if not re.search(r"<caption\b", table, re.I):
                errors.append(f"{path}: table {idx} missing caption")

            if not re.search(r"<thead\b", table, re.I):
                errors.append(f"{path}: table {idx} missing thead")

            if not re.search(r"<tbody\b", table, re.I):
                errors.append(f"{path}: table {idx} missing tbody")

            ths = re.findall(r"<th\b[^>]*>", table, re.I)
            if not ths:
                errors.append(f"{path}: table {idx} has no th cells")
            else:
                for th in ths:
                    if not re.search(r'\bscope=["\']col["\']', th, re.I):
                        errors.append(f"{path}: table {idx} has th without scope=col: {th[:120]}")

    if errors:
        print("FAIL: files table accessibility audit found issues")
        for e in errors:
            print("-", e)
        return 1

    print("OK: files tables have caption, thead, tbody, and scope=col.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
