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


def get_page_lang(text):
    head = text[:2000].lower()
    html_start = head.find("<html")
    if html_start == -1:
        return ""
    html_end = head.find(">", html_start)
    html_tag = head[html_start:html_end if html_end != -1 else len(head)]
    if ' lang="he"' in html_tag or " lang='he'" in html_tag:
        return "he"
    if ' lang="en"' in html_tag or " lang='en'" in html_tag:
        return "en"
    return ""


def opening_tag_around_marker(text, index):
    tag_start = text.rfind("<", 0, index)
    tag_end = text.find(">", index)
    if tag_start == -1 or tag_end == -1:
        return ""
    return text[tag_start:tag_end + 1].lower()


def tag_is_hidden(tag):
    compact = tag.replace(" ", "")
    return " hidden" in tag or "hidden=" in tag or "display:none" in compact


def check_language_blocks(path, text, errors):
    lang = get_page_lang(text)
    if lang == "he":
        marker = 'data-lang-block="en"'
    elif lang == "en":
        marker = 'data-lang-block="he"'
    else:
        return

    start = 0
    while True:
        index = text.find(marker, start)
        if index == -1:
            break
        tag = opening_tag_around_marker(text, index)
        if not tag_is_hidden(tag):
            errors.append(f"opposite-language block is not hidden: {path.as_posix()} {marker}")
        start = index + len(marker)


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

            if path.suffix.lower() == ".html":
                text = path.read_text(encoding="utf-8", errors="ignore")
                check_language_blocks(path, text, errors)

    if errors:
        print("FAIL: public junk/language-block audit found issues")
        for error in errors[:200]:
            print("-", error)
        if len(errors) > 200:
            print(f"... and {len(errors) - 200} more")
        return 1

    print("OK: no public junk/debug/temp files or visible opposite-language blocks found under site/.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
