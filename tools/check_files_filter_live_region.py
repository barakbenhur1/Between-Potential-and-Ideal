from pathlib import Path
import re
import sys

FILES = [
    Path("site/pages/he/files.html"),
    Path("site/pages/en/files-en.html"),
]

def main() -> int:
    errors = []

    for path in FILES:
        if not path.exists():
            errors.append(f"missing {path}")
            continue

        s = path.read_text(encoding="utf-8", errors="ignore")
        low = s.lower()

        if "<select" in low or "<input" in low:
            if "aria-live=" not in low and "role=\"status\"" not in low and "role='status'" not in low:
                errors.append(f"{path}: filters exist but no aria-live/status region found")

    if errors:
        print("FAIL: files filter live-region audit found issues")
        for error in errors:
            print("-", error)
        return 1

    print("OK: files filter live-region baseline passed.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
