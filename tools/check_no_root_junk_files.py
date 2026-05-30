from pathlib import Path
import sys

ROOT = Path(".")

SKIP_DIRS = {
    ".git",
    "site",
    "docs",
    "tools",
    ".github",
}

BAD_EXACT_NAMES = {
    "README_RESTORE_EN_EDITORIAL.txt",
    "README_SELF_EGO_UNITY_FIX.txt",
    "QA_BUNDLE_MANIFEST_HE.txt",
    "QA_PRODUCT_AUDIT_FULL_HE.md",
    "manifest.json",
    ".DS_Store",
    "Thumbs.db",
}

BAD_PREFIXES = (
    "bpi_missing_english_stories_package",
    "bpi_translation_files_only",
)

BAD_PARTS = (
    "ultimate_repair_prompt",
    "repair_prompt",
    "restore_en_editorial",
    "self_ego_unity_fix",
)

BAD_SUFFIXES = (
    ".zip",
    ".pyc",
    ".pyo",
    ".log",
)

def should_skip(path: Path) -> bool:
    parts = set(path.parts)
    return bool(parts & SKIP_DIRS)

def main() -> int:
    errors = []

    for path in ROOT.iterdir():
        if path.name in SKIP_DIRS:
            continue

        name = path.name
        lower = name.lower()

        if name in BAD_EXACT_NAMES:
            errors.append(f"bad root artifact: {path}")
            continue

        if any(name.startswith(prefix) for prefix in BAD_PREFIXES):
            errors.append(f"bad root extraction/package artifact: {path}")
            continue

        if any(part in lower for part in BAD_PARTS):
            errors.append(f"bad root repair/debug artifact: {path}")
            continue

        if path.is_file() and lower.endswith(BAD_SUFFIXES):
            errors.append(f"bad root generated/archive file: {path}")
            continue

    if errors:
        print("FAIL: root junk audit found issues")
        for error in errors:
            print("-", error)
        return 1

    print("OK: no root junk/temp repair artifacts found.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
