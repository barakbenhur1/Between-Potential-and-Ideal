from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urlparse, unquote

ROOT = Path("site")
REPORT = Path("BPI_A11Y_LINK_AUDIT_REPORT.md")

HTML_FILES = []
for p in [ROOT / "index.html", ROOT / "en.html"]:
    if p.exists():
        HTML_FILES.append(p)

for folder in [ROOT / "pages", ROOT / "files"]:
    if folder.exists():
        HTML_FILES.extend(folder.rglob("*.html"))

missing_alt = []
broken_links = []
broken_anchors = []
empty_interactive = []

EXTERNAL_SCHEMES = {"http", "https", "mailto", "tel", "data", "javascript"}

def is_external(ref: str) -> bool:
    parsed = urlparse(ref)
    return bool(parsed.scheme and parsed.scheme in EXTERNAL_SCHEMES)

def clean_ref(ref: str) -> str:
    ref = ref.split("#", 1)[0]
    ref = ref.split("?", 1)[0]
    return unquote(ref.strip())

def resolve_local(base_file: Path, ref: str):
    if not ref or ref.startswith("#") or is_external(ref):
        return None

    clean = clean_ref(ref)
    if not clean:
        return None

    if clean.startswith("/"):
        clean = clean.lstrip("/")
        if clean.startswith("site/"):
            return Path(clean)
        return ROOT / clean

    return (base_file.parent / clean).resolve()

def anchors_in(soup):
    out = set()
    for tag in soup.find_all(True):
        if tag.get("id"):
            out.add(tag["id"])
        if tag.name == "a" and tag.get("name"):
            out.add(tag["name"])
    return out

for html_path in HTML_FILES:
    raw = html_path.read_text(encoding="utf-8", errors="ignore")
    soup = BeautifulSoup(raw, "html.parser")
    local_anchors = anchors_in(soup)

    for img in soup.find_all("img"):
        alt = img.get("alt")
        if alt is None or not alt.strip():
            missing_alt.append((str(html_path), img.get("src", "")))

    for tag in soup.find_all(["a", "button"]):
        label = tag.get_text(" ", strip=True)
        aria = (tag.get("aria-label") or "").strip()
        title = (tag.get("title") or "").strip()
        if not label and not aria and not title:
            empty_interactive.append((str(html_path), tag.name, str(tag)[:180]))

    for tag in soup.find_all(True):
        for attr in ["href", "src"]:
            ref = tag.get(attr)
            if not ref:
                continue

            if ref.startswith("#"):
                anchor = ref[1:]
                if anchor and anchor not in local_anchors:
                    broken_anchors.append((str(html_path), ref))
                continue

            if is_external(ref):
                continue

            anchor = None
            if "#" in ref:
                anchor = ref.split("#", 1)[1].split("?", 1)[0]

            target = resolve_local(html_path, ref)
            if target is None:
                continue

            if not target.exists():
                broken_links.append((str(html_path), tag.name, attr, ref))
                continue

            if anchor and target.suffix.lower() in {".html", ".htm"}:
                try:
                    target_soup = BeautifulSoup(target.read_text(encoding="utf-8", errors="ignore"), "html.parser")
                    if anchor not in anchors_in(target_soup):
                        broken_anchors.append((str(html_path), ref))
                except Exception:
                    pass

lines = []
lines.append("# BPI accessibility/link audit report")
lines.append("")
lines.append("Audit-only report. No site files were changed.")
lines.append("")
lines.append("## Summary")
lines.append("")
lines.append(f"- HTML files scanned: {len(HTML_FILES)}")
lines.append(f"- Images missing alt: {len(missing_alt)}")
lines.append(f"- Broken local links/assets: {len(broken_links)}")
lines.append(f"- Broken anchors: {len(broken_anchors)}")
lines.append(f"- Empty interactive elements: {len(empty_interactive)}")
lines.append("")

def section(title, rows, headers):
    lines.append(f"## {title}")
    lines.append("")
    if not rows:
        lines.append("None found.")
        lines.append("")
        return

    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join(["---"] * len(headers)) + " |")

    for row in rows[:300]:
        safe = [str(x).replace("|", "\\|").replace("\n", " ") for x in row]
        lines.append("| " + " | ".join(safe) + " |")

    if len(rows) > 300:
        lines.append("")
        lines.append(f"Showing first 300 of {len(rows)}.")
    lines.append("")

section("Images missing alt", missing_alt, ["File", "Image src"])
section("Broken local links/assets", broken_links, ["File", "Tag", "Attribute", "Reference"])
section("Broken anchors", broken_anchors, ["File", "Anchor reference"])
section("Empty interactive elements", empty_interactive, ["File", "Tag", "Snippet"])

REPORT.write_text("\n".join(lines), encoding="utf-8")

print("WROTE", REPORT)
print("missing_alt:", len(missing_alt))
print("broken_links:", len(broken_links))
print("broken_anchors:", len(broken_anchors))
print("empty_interactive:", len(empty_interactive))
