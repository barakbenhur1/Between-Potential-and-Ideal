from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urljoin, urlparse
from html import unescape
import xml.etree.ElementTree as ET
import re
import json

SITE = Path("site")
BASE_URL = "https://between-potential-and-ideal.onrender.com"
SITEMAP = SITE / "sitemap.xml"
REPORT = Path("reports/audit_sitemap_and_public_links.json")

HREF_RE = re.compile(r'\bhref=["\']([^"\']+)["\']', re.I)
SRC_RE = re.compile(r'\bsrc=["\']([^"\']+)["\']', re.I)

SKIP_PREFIXES = (
    "mailto:",
    "tel:",
    "javascript:",
    "#",
    "data:",
)

def fetch_status(url):
    req = Request(url, headers={"User-Agent": "BPI sitemap/link audit"})
    try:
        with urlopen(req, timeout=20) as r:
            return {
                "url": url,
                "status": getattr(r, "status", None),
                "final_url": r.geturl(),
                "ok": 200 <= getattr(r, "status", 0) < 400,
                "error": "",
            }
    except Exception as e:
        return {
            "url": url,
            "status": None,
            "final_url": "",
            "ok": False,
            "error": str(e),
        }

def sitemap_urls():
    if not SITEMAP.exists():
        return []

    raw = SITEMAP.read_text(encoding="utf-8", errors="ignore")
    root = ET.fromstring(raw)

    urls = []
    for elem in root.iter():
        if elem.tag.endswith("loc") and elem.text:
            urls.append(elem.text.strip())

    return urls

def local_path_for_url(url):
    parsed = urlparse(url)
    if parsed.netloc and parsed.netloc != "between-potential-and-ideal.onrender.com":
        return None

    path = parsed.path.lstrip("/")
    if not path:
        path = "index.html"

    return SITE / path

def collect_local_refs():
    refs = []

    for path in sorted(SITE.rglob("*.html")):
        html = path.read_text(encoding="utf-8", errors="ignore")

        for raw in HREF_RE.findall(html) + SRC_RE.findall(html):
            value = unescape(raw).strip()
            if not value or value.startswith(SKIP_PREFIXES):
                continue

            if value.startswith(("http://", "https://")):
                parsed = urlparse(value)
                if parsed.netloc != "between-potential-and-ideal.onrender.com":
                    continue
                target = local_path_for_url(value)
            elif value.startswith("/"):
                target = SITE / value.lstrip("/")
            else:
                target = path.parent / value.split("#", 1)[0].split("?", 1)[0]

            if target:
                refs.append({
                    "file": str(path),
                    "ref": value,
                    "resolved": str(target),
                    "exists": target.exists(),
                })

    return refs

def main():
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    urls = sitemap_urls()
    sitemap_results = [fetch_status(url) for url in urls]

    local_refs = collect_local_refs()
    missing_local = [x for x in local_refs if not x["exists"]]

    bad_sitemap = [x for x in sitemap_results if not x["ok"]]

    report = {
        "sitemap_url_count": len(urls),
        "bad_sitemap_url_count": len(bad_sitemap),
        "bad_sitemap_urls": bad_sitemap,
        "local_ref_count": len(local_refs),
        "missing_local_ref_count": len(missing_local),
        "missing_local_refs": missing_local,
    }

    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    if bad_sitemap or missing_local:
        print("FAIL: sitemap/public links audit found issues")
        print("bad sitemap URLs:", len(bad_sitemap))
        for item in bad_sitemap[:40]:
            print(" -", item)
        print("missing local refs:", len(missing_local))
        for item in missing_local[:80]:
            print(" -", item["file"], "=>", item["ref"], "=>", item["resolved"])
        print("Report:", REPORT)
        raise SystemExit(1)

    print("OK: sitemap URLs are reachable and local public references exist.")
    print("Report:", REPORT)

if __name__ == "__main__":
    main()
