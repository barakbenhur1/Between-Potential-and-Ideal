from pathlib import Path
import sys

P = Path(".gitignore")

REQUIRED = [
    "reports/",
    "tools/__pycache__/",
    "__pycache__/",
    "*.pyc",
    ".DS_Store",
    "bpi_missing_english_stories_package/",
    "README_RESTORE_EN_EDITORIAL.txt",
    "README_SELF_EGO_UNITY_FIX.txt",
    "*ultimate_repair_prompt*.txt",
]

def main() -> int:
    errors = []
    if not P.exists():
        errors.append("missing .gitignore")
        text = ""
    else:
        text = P.read_text(encoding="utf-8", errors="ignore")

    lines = set(text.splitlines())
    for item in REQUIRED:
        if item not in lines:
            errors.append(f".gitignore missing: {item}")

    if errors:
        print("FAIL: gitignore audit found issues")
        for error in errors:
            print("-", error)
        return 1

    print("OK: gitignore protects local QA/temp artifacts.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
