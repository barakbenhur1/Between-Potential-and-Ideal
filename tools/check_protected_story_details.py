from pathlib import Path
from html import unescape
import json
import re
import sys

REGISTRY = Path("site/data/protected_story_details.json")

FILES = {
    "he": Path("site/files/appendices/stories-before-thought-hebrew-rtl.html"),
    "en": Path("site/files/appendices/stories-before-thought-english.html"),
}

def strip_tags(html: str) -> str:
    html = re.sub(r"<style\b[^>]*>.*?</style>", " ", html, flags=re.I | re.S)
    html = re.sub(r"<script\b[^>]*>.*?</script>", " ", html, flags=re.I | re.S)
    html = re.sub(r"<[^>]+>", " ", html)
    return re.sub(r"\s+", " ", unescape(html)).strip()

def section_for_id(html: str, sid: str) -> str:
    m = re.search(
        r'<(?P<tag>section|article|div)\b[^>]*\bid=["\']' + re.escape(sid) + r'["\'][^>]*>.*?</(?P=tag)>',
        html,
        flags=re.I | re.S,
    )
    if m:
        return m.group(0)

    m = re.search(
        r'<h[1-6]\b[^>]*\bid=["\']' + re.escape(sid) + r'["\'][^>]*>.*?</h[1-6]>',
        html,
        flags=re.I | re.S,
    )
    if not m:
        return ""

    start = m.start()
    nxt = re.search(r"<h[1-6]\b", html[m.end():], flags=re.I)
    end = m.end() + nxt.start() if nxt else len(html)
    return html[start:end]

def normalize_text(html: str) -> str:
    return strip_tags(html)

def main() -> int:
    errors = []

    if not REGISTRY.exists():
        print("FAIL: missing protected details registry:", REGISTRY)
        return 1

    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    rules = data.get("protected_rules", [])

    if not rules:
        errors.append("protected_rules is empty")

    html_by_lang = {}

    for lang, path in FILES.items():
        if not path.exists():
            errors.append(f"{lang}: missing appendix file {path}")
            continue
        html_by_lang[lang] = path.read_text(encoding="utf-8", errors="ignore")

    for rule in rules:
        rid = rule.get("id", "<missing-id>")
        lang = rule.get("lang")
        story_id = rule.get("story_id")

        if lang not in html_by_lang:
            errors.append(f"{rid}: unknown or missing lang file: {lang}")
            continue

        html = html_by_lang[lang]
        visible_all = normalize_text(html)

        if rule.get("type") == "exact_required_text":
            text = rule.get("text", "")
            if text not in visible_all:
                errors.append(f"{rid}: exact protected text not found: {text}")
            continue

        if rule.get("type") == "story_rule":
            if not story_id:
                errors.append(f"{rid}: missing story_id")
                continue

            section = section_for_id(html, story_id)
            if not section:
                errors.append(f"{rid}: story section not found: {story_id}")
                continue

            visible = normalize_text(section)

            required_title = rule.get("required_title")
            if required_title and required_title not in visible:
                errors.append(f"{rid}: required title not found in section: {required_title}")

            required_subtitle = rule.get("required_subtitle")
            if required_subtitle and required_subtitle not in visible:
                errors.append(f"{rid}: required subtitle not found in section: {required_subtitle}")

            for term in rule.get("forbidden_terms", []):
                if term.lower() in visible.lower():
                    errors.append(f"{rid}: forbidden term found: {term}")

    if errors:
        print("FAIL: protected story details audit found issues")
        for e in errors:
            print("-", e)
        return 1

    print("OK: protected story details audit passed.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
