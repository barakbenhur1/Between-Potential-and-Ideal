from pathlib import Path
import sys

HTML_FILES = sorted(Path("site").rglob("*.html"))


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
            tag = opening_tag_around_marker(text, index)
            if not tag_is_hidden(tag):
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
