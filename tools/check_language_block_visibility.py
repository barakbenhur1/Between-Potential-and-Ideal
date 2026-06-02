from pathlib import Path
import sys

HTML_FILES = sorted(Path("site").rglob("*.html"))


def get_page_lang(text):
    head = text[:2000].lower()
    if 'lang="he"' in head or "lang='he'" in head:
        return "he"
    if 'lang="en"' in head or "lang='en'" in head:
        return "en"
    return ""


def tag_is_hidden(fragment):
    tag_end = fragment.find(">")
    tag = fragment[:tag_end if tag_end != -1 else 300].lower()
    return " hidden" in tag or "display:none" in tag.replace(" ", "")


def main():
    errors = []
    checked = 0

    for path in HTML_FILES:
        text = path.read_text(encoding="utf-8", errors="ignore")
        lang = get_page_lang(text)
        if lang == "he":
            marker = 'data-lang-block="en"'
        elif lang == "en":
            marker = 'data-lang-block="he"'
        else:
            continue

        start = 0
        while True:
            index = text.find(marker, start)
            if index == -1:
                break
            checked += 1
            fragment_start = max(0, index - 120)
            fragment = text[fragment_start:index + 300]
            if not tag_is_hidden(fragment):
                errors.append(f"{path}: opposite-language block is not hidden: {marker}")
            start = index + len(marker)

    if errors:
        print("FAIL: visible opposite-language blocks found")
        for error in errors:
            print("-", error)
        return 1

    print(f"OK: language-block visibility baseline passed. opposite_blocks_checked={checked}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
