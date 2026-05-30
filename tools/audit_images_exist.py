from pathlib import Path
from urllib.parse import urlparse
import re
import json

SITE = Path("site")
REPORT = Path("reports/audit_images_exist.json")

IMG_RE = re.compile(r'<img\b[^>]*\bsrc=["\']([^"\']+)["\']', re.I | re.S)

def is_external(src):
    return src.startswith(("http://", "https://", "data:", "mailto:", "tel:"))

def main():
    missing = []
    checked = 0

    for path in sorted(SITE.rglob("*.html")):
        html = path.read_text(encoding="utf-8", errors="ignore")
        for src in IMG_RE.findall(html):
            if is_external(src):
                continue

            clean_src = src.split("#", 1)[0].split("?", 1)[0]
            if not clean_src:
                continue

            if clean_src.startswith("/"):
                target = SITE / clean_src.lstrip("/")
            else:
                target = path.parent / clean_src

            checked += 1

            if not target.exists():
                missing.append({
                    "file": str(path),
                    "src": src,
                    "resolved": str(target),
                })

    result = {
        "checked": checked,
        "missing_count": len(missing),
        "missing": missing,
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    if missing:
        print("FAIL: missing images")
        for m in missing[:80]:
            print(m["file"], "=>", m["src"], "=>", m["resolved"])
        print("Report:", REPORT)
        raise SystemExit(1)

    print(f"OK: all local images exist. checked={checked}")
    print("Report:", REPORT)

if __name__ == "__main__":
    main()
