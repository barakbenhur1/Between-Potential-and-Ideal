from pathlib import Path
from html import unescape
import json
import re
import sys

REGISTRY = Path("site/data/stories.json")

FILES = {
    "he": Path("site/files/appendices/stories-before-thought-hebrew-rtl.html"),
    "en": Path("site/files/appendices/stories-before-thought-english.html"),
}

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

def ordered_body_ids(html: str, expected_ids: list[str]) -> list[str]:
    found = []

    for sid in expected_ids:
        m = re.search(r'\bid=["\']' + re.escape(sid) + r'["\']', html, flags=re.I)
        if m:
            found.append((m.start(), sid))

    return [sid for _, sid in sorted(found)]

def ordered_toc_ids(html: str, expected_ids: list[str]) -> list[str]:
    found = []

    for m in re.finditer(r'href=["\']#([^"\']+)["\']', html, flags=re.I):
        sid = unescape(m.group(1)).strip()
        if sid in expected_ids and sid not in found:
            found.append(sid)

    return found

def has_image(html: str) -> bool:
    return bool(re.search(r"<img\b[^>]*\bsrc=", html, flags=re.I | re.S))

def main() -> int:
    errors = []

    if not REGISTRY.exists():
        print("FAIL: missing registry:", REGISTRY)
        return 1

    stories = json.loads(REGISTRY.read_text(encoding="utf-8"))
    expected_ids = [item["id"] for item in stories]

    if len(expected_ids) != 16:
        errors.append(f"registry has {len(expected_ids)} stories, expected 16")

    if len(expected_ids) != len(set(expected_ids)):
        errors.append("registry has duplicate ids")

    if expected_ids[7] != "shalosh-sheelot-iska-bankait":
        errors.append("Three Queries must be story position 8")

    if expected_ids[13] != "haemet-hamavchila-eifo-hatzlalim":
        errors.append("The Nauseating Truth must be story position 14")

    for lang, path in FILES.items():
        if not path.exists():
            errors.append(f"{lang}: missing appendix file: {path}")
            continue

        html = path.read_text(encoding="utf-8", errors="ignore")

        body_ids = ordered_body_ids(html, expected_ids)
        toc_ids = ordered_toc_ids(html, expected_ids)

        if body_ids != expected_ids:
            errors.append(f"{lang}: body order mismatch\n  expected={expected_ids}\n  actual={body_ids}")

        if toc_ids != expected_ids:
            errors.append(f"{lang}: TOC order mismatch\n  expected={expected_ids}\n  actual={toc_ids}")

        for sid in expected_ids:
            id_count = len(re.findall(r'\bid=["\']' + re.escape(sid) + r'["\']', html, flags=re.I))
            if id_count != 1:
                errors.append(f"{lang}: id {sid} appears {id_count} times, expected 1")

            href_count = len(re.findall(r'href=["\']#' + re.escape(sid) + r'["\']', html, flags=re.I))
            if href_count < 1:
                errors.append(f"{lang}: missing TOC href for {sid}")

            section = section_for_id(html, sid)
            if not section:
                errors.append(f"{lang}: missing body section for {sid}")
                continue

            if not has_image(section):
                errors.append(f"{lang}: story {sid} has no body image")

    if errors:
        print("FAIL: story registry audit found issues")
        for error in errors:
            print("-", error)
        return 1

    print("OK: story registry audit passed — 16 stories, protected order, TOC links, unique ids, and body images.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
