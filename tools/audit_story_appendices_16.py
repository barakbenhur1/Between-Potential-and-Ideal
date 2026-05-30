from pathlib import Path
from html import unescape
import re
import json

APP = Path("site/files/appendices")
HE = APP / "stories-before-thought-hebrew-rtl.html"
EN = APP / "stories-before-thought-english.html"
REPORT = Path("reports/audit_story_appendices_16.json")

EXPECTED = [
    "story-1",
    "story-2",
    "story-3",
    "story-4",
    "story-5",
    "story-6",
    "story-7",
    "shalosh-sheelot-iska-bankait",
    "story-8",
    "story-9",
    "story-10",
    "story-11",
    "story-12",
    "haemet-hamavchila-eifo-hatzlalim",
    "story-13",
    "story-14",
]

EN_TITLES = {
    "story-1": "How Truth Remains Honest",
    "story-2": "True, But Not Just",
    "story-3": "Red Causes Dread",
    "story-4": "Quantum Intelligence",
    "story-5": "A Place at the End of the Road",
    "story-6": "Super Mirrors",
    "story-7": "Self-Confidence",
    "shalosh-sheelot-iska-bankait": "Three Queries",
    "story-8": "Serial Healer",
    "story-9": "Maxideal",
    "story-10": "To Speak with Consciousness",
    "story-11": "Heretic from Abroad",
    "story-12": "Puzzle",
    "haemet-hamavchila-eifo-hatzlalim": "The Nauseating Truth",
    "story-13": "To Fear Intruders, or Talk to Computers",
    "story-14": "A Few Strings and a Knot",
}

def read(path):
    if not path.exists():
        raise SystemExit(f"missing file: {path}")
    return path.read_text(encoding="utf-8", errors="ignore")

def toc_section(html):
    m = re.search(
        r'<section\b(?=[^>]*(?:id=["\']table-of-contents["\']|class=["\'][^"\']*story-toc-page[^"\']*["\']))[^>]*>.*?</section>',
        html,
        flags=re.I | re.S,
    )
    return m.group(0) if m else html

def body_order(html):
    order = []
    for m in re.finditer(r'<section\b[^>]*\bid=["\']([^"\']+)["\']', html, flags=re.I):
        sid = m.group(1)
        if sid in EXPECTED and sid not in order:
            order.append(sid)
    return order

def toc_order(html):
    toc = toc_section(html)
    order = []
    for sid in re.findall(r'href=["\']#([^"\']+)["\']', toc, flags=re.I):
        if sid in EXPECTED and sid not in order:
            order.append(sid)
    return order

def section(html, sid):
    m = re.search(
        r'<section\b(?=[^>]*\bid=["\']' + re.escape(sid) + r'["\'])[^>]*>.*?</section>',
        html,
        flags=re.I | re.S,
    )
    return m.group(0) if m else ""

def audit_file(path, is_english=False):
    html = read(path)
    errors = []
    body = body_order(html)
    toc = toc_order(html)

    if body != EXPECTED:
        errors.append({
            "type": "body_order_mismatch",
            "expected": EXPECTED,
            "actual": body,
        })

    if toc[:16] != EXPECTED:
        errors.append({
            "type": "toc_order_mismatch",
            "expected": EXPECTED,
            "actual": toc[:16],
        })

    for sid in EXPECTED:
        sec = section(html, sid)
        if not sec:
            errors.append({"type": "missing_story_section", "id": sid})
            continue

        if f'href="#{sid}"' not in html:
            errors.append({"type": "missing_toc_link", "id": sid})

        toc_row = ""
        for m in re.finditer(r'<(?:p|li)\b[^>]*(?:story-toc-row|toc)[^>]*>.*?</(?:p|li)>', html, flags=re.I | re.S):
            row = m.group(0)
            if f'href="#{sid}"' in row or f"href='#{sid}'" in row:
                toc_row = row
                break

        if not toc_row:
            m = re.search(r'<a\b[^>]*href=["\']#' + re.escape(sid) + r'["\'][^>]*>.*?</a>', html, flags=re.I | re.S)
            toc_row = m.group(0) if m else ""

        if not toc_row:
            errors.append({"type": "missing_toc_row", "id": sid})
        elif "<img" not in toc_row:
            errors.append({"type": "toc_row_missing_image", "id": sid})

        if "<figure" not in sec or "<img" not in sec:
            errors.append({"type": "story_section_missing_image", "id": sid})

        if is_english:
            title = EN_TITLES[sid]
            if title not in sec and title not in toc_row:
                errors.append({"type": "english_title_missing", "id": sid, "title": title})

    return {
        "path": str(path),
        "body_order": body,
        "toc_order": toc[:16],
        "errors": errors,
    }

def main():
    results = [
        audit_file(HE, is_english=False),
        audit_file(EN, is_english=True),
    ]
    REPORT.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")

    errors = []
    for r in results:
        errors.extend((r["path"], e) for e in r["errors"])

    if errors:
        print("FAIL: story appendix 16 audit")
        for path, err in errors[:80]:
            print(path, "=>", err)
        print("Report:", REPORT)
        raise SystemExit(1)

    print("OK: 16 stories exist in Hebrew and English, same order, TOC rows, story images, and English titles.")
    print("Report:", REPORT)

if __name__ == "__main__":
    main()
