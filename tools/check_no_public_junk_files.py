from pathlib import Path
import sys

ROOT = Path("site")

BAD_DIR_NAMES = {
    "__pycache__",
    "reports",
    "bpi_missing_english_stories_package",
}

BAD_FILE_NAMES = {
    ".DS_Store",
    "Thumbs.db",
}

BAD_NAME_PARTS = [
    "debug",
    "tmp",
    "temp",
    "repair_prompt",
    "ultimate_repair_prompt",
    "restore",
    "missing_english_stories_package",
    "README_RESTORE",
    "README_SELF_EGO_UNITY_FIX",
]

BAD_SUFFIXES = {
    ".pyc",
    ".pyo",
    ".log",
}

def main() -> int:
    errors = []

    if not ROOT.exists():
        print("SKIP: no site directory")
        return 0

    for path in ROOT.rglob("*"):
        rel = path.as_posix()
        name = path.name
        lower = name.lower()

        if any(part in BAD_DIR_NAMES for part in path.parts):
            errors.append(f"bad public directory/file under forbidden dir: {rel}")
            continue

        if name in BAD_FILE_NAMES:
            errors.append(f"bad public system file: {rel}")
            continue

        if path.is_file() and path.suffix.lower() in BAD_SUFFIXES:
            errors.append(f"bad public generated file: {rel}")
            continue

        if path.is_file():
            for bad in BAD_NAME_PARTS:
                if bad.lower() in lower:
                    errors.append(f"possible temporary/debug public file: {rel}")
                    break

    if errors:
        print("FAIL: public junk audit found issues")
        for error in errors[:200]:
            print("-", error)
        if len(errors) > 200:
            print(f"... and {len(errors) - 200} more")
        return 1

    print("OK: no public junk/debug/temp files found under site/.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
