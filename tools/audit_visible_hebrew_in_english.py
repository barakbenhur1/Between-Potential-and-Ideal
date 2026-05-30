from pathlib import Path
from html import unescape
import re
import json

SITE = Path("site")
REPORT = Path("reports/audit_visible_hebrew_in_english.json")
HE_RE = re.compile(r"[\u0590-\u05FF]")

ALLOWLIST_PHRASES = {
    "עברית",
}

def is_english_file(path):
    s = str(path)
    name = path.name.lower()

    if "/pages/en/" in s:
        return True

    if "/files/" in s and (
        name.endswith("-en.html")
        or "-en-" in name
        or "english" in name
        or name.endswith("-english.html")
    ):
        return True

    if path.name == "en.html":
        return True

    return False

def visible_text(html):
    html = re.sub(r"<style\b[^>]*>.*?</style>", " ", html, flags=re.I | re.S)
    html = re.sub(r"<script\b[^>]*>.*?</script>", " ", html, flags=re.I | re.S)
    html = re.sub(r"<code\b[^>]*>.*?</code>", " ", html, flags=re.I | re.S)
    html = re.sub(r"<pre\b[^>]*>.*?</pre>", " ", html, flags=re.I | re.S)
    html = re.sub(r"<[^>]+>", " ", html)
    return re.sub(r"\s+", " ", unescape(html)).strip()

def main():
    bad = []

    for path in sorted(SITE.rglob("*.html")):
        if not is_english_file(path):
            continue

        text = visible_text(path.read_text(encoding="utf-8", errors="ignore"))
        samples = sorted(set(x.strip() for x in re.findall(r"[\u0590-\u05FF][\u0590-\u05FF\s,.:;!?״׳־-]{0,120}", text)))
        samples = [x for x in samples if x and x not in ALLOWLIST_PHRASES]

        if samples:
            # potential-extensions-en intentionally contains Hebrew source titles / bilingual references.
            # Keep this audit strict elsewhere, but do not fail release on this known bilingual catalog page.
            if path.as_posix().endswith("site/pages/en/potential-extensions-en.html"):
                continue

            bad.append({
                "file": str(path),
                "samples": samples[:40],
            })

    result = {
        "files_with_visible_hebrew": len(bad),
        "issues": bad,
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    if bad:
        print("FAIL: visible Hebrew found in English files")
        for item in bad[:80]:
            print(item["file"])
            for s in item["samples"][:20]:
                print("  -", s)
        print("Report:", REPORT)
        raise SystemExit(1)

    print("OK: no visible Hebrew found in English HTML files.")
    print("Report:", REPORT)

if __name__ == "__main__":
    main()
