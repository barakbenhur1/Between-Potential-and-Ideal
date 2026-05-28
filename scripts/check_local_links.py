#!/usr/bin/env python3
"""Check local links and assets in the static site.

This script is intentionally dependency-free so it can run in GitHub Actions and
locally without installing packages. It checks local href/src/action/poster-style
references in HTML and local url(...) references in CSS.

It ignores external URLs, mailto/tel links, data/blob/javascript URLs, and pure
same-page hash references. It also validates local fragment anchors when the
referenced HTML file exists.
"""

from __future__ import annotations

import argparse
import html.parser
import pathlib
import re
import sys
import urllib.parse
from dataclasses import dataclass
from typing import Iterable

LOCAL_ATTRS = {
    "a": ("href",),
    "area": ("href",),
    "link": ("href",),
    "script": ("src",),
    "img": ("src", "srcset"),
    "source": ("src", "srcset"),
    "iframe": ("src",),
    "embed": ("src",),
    "object": ("data",),
    "video": ("src", "poster"),
    "audio": ("src",),
    "form": ("action",),
}

SKIP_SCHEMES = {
    "http",
    "https",
    "mailto",
    "tel",
    "sms",
    "data",
    "blob",
    "javascript",
    "about",
}

CSS_URL_RE = re.compile(r"url\((?P<q>['\"]?)(?P<url>.*?)(?P=q)\)", re.IGNORECASE)
IMPORT_RE = re.compile(r"@import\s+(?:url\()?['\"](?P<url>[^'\"]+)['\"]\)?", re.IGNORECASE)
ID_RE = re.compile(r"\bid\s*=\s*(['\"])(.*?)\1", re.IGNORECASE | re.DOTALL)
NAME_RE = re.compile(r"\bname\s*=\s*(['\"])(.*?)\1", re.IGNORECASE | re.DOTALL)


@dataclass(frozen=True)
class Problem:
    source: pathlib.Path
    target: str
    reason: str


class LinkParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.refs: list[tuple[str, str]] = []
        self.ids: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = {name.lower(): value for name, value in attrs if name and value is not None}
        for attr in LOCAL_ATTRS.get(tag.lower(), ()):
            value = attr_map.get(attr)
            if not value:
                continue
            if attr == "srcset":
                for candidate in parse_srcset(value):
                    self.refs.append((attr, candidate))
            else:
                self.refs.append((attr, value))
        if "id" in attr_map and attr_map["id"]:
            self.ids.add(attr_map["id"] or "")
        if tag.lower() == "a" and attr_map.get("name"):
            self.ids.add(attr_map["name"] or "")


def parse_srcset(value: str) -> Iterable[str]:
    for part in value.split(","):
        part = part.strip()
        if not part:
            continue
        yield part.split()[0]


def is_skipped_ref(ref: str) -> bool:
    ref = ref.strip()
    if not ref or ref.startswith("#"):
        return True
    parsed = urllib.parse.urlsplit(ref)
    if parsed.scheme.lower() in SKIP_SCHEMES:
        return True
    if ref.startswith("//"):
        return True
    return False


def clean_local_ref(ref: str) -> tuple[str, str]:
    parsed = urllib.parse.urlsplit(ref.strip())
    return urllib.parse.unquote(parsed.path), urllib.parse.unquote(parsed.fragment)


def resolve_path(site_root: pathlib.Path, source_file: pathlib.Path, ref_path: str) -> pathlib.Path:
    if ref_path.startswith("/"):
        return (site_root / ref_path.lstrip("/")).resolve()
    return (source_file.parent / ref_path).resolve()


def collect_html_ids(path: pathlib.Path) -> set[str]:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return set()
    ids = set(match.group(2) for match in ID_RE.finditer(text))
    ids.update(match.group(2) for match in NAME_RE.finditer(text))
    return ids


def check_ref(site_root: pathlib.Path, source_file: pathlib.Path, raw_ref: str) -> Problem | None:
    if is_skipped_ref(raw_ref):
        return None

    ref_path, fragment = clean_local_ref(raw_ref)
    if not ref_path and fragment:
        # Same-page hash was already ignored above, but keep this safe for odd URLs.
        return None

    target = resolve_path(site_root, source_file, ref_path)

    try:
        target.relative_to(site_root.resolve())
    except ValueError:
        return Problem(source_file, raw_ref, "local reference escapes site root")

    if not target.exists():
        return Problem(source_file, raw_ref, "missing local file or asset")

    if fragment and target.suffix.lower() in {".html", ".htm"}:
        ids = collect_html_ids(target)
        if fragment not in ids:
            return Problem(source_file, raw_ref, "missing target anchor")

    return None


def check_html(site_root: pathlib.Path, path: pathlib.Path) -> list[Problem]:
    parser = LinkParser()
    text = path.read_text(encoding="utf-8", errors="ignore")
    parser.feed(text)
    problems = []
    for _, ref in parser.refs:
        problem = check_ref(site_root, path, ref)
        if problem:
            problems.append(problem)
    return problems


def check_css(site_root: pathlib.Path, path: pathlib.Path) -> list[Problem]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    refs = [match.group("url").strip() for match in CSS_URL_RE.finditer(text)]
    refs.extend(match.group("url").strip() for match in IMPORT_RE.finditer(text))
    problems = []
    for ref in refs:
        problem = check_ref(site_root, path, ref)
        if problem:
            problems.append(problem)
    return problems


def iter_site_files(site_root: pathlib.Path) -> Iterable[pathlib.Path]:
    for suffix in ("*.html", "*.htm", "*.css"):
        yield from site_root.rglob(suffix)


def main() -> int:
    parser = argparse.ArgumentParser(description="Check local links/assets in the static site.")
    parser.add_argument("--site-root", default="site", help="Static site root directory. Default: site")
    parser.add_argument("--max-problems", type=int, default=200, help="Maximum problems to print before truncating output.")
    args = parser.parse_args()

    site_root = pathlib.Path(args.site_root).resolve()
    if not site_root.exists():
        print(f"ERROR: site root does not exist: {site_root}", file=sys.stderr)
        return 2

    problems: list[Problem] = []
    checked = 0
    for path in sorted(iter_site_files(site_root)):
        checked += 1
        if path.suffix.lower() in {".html", ".htm"}:
            problems.extend(check_html(site_root, path))
        elif path.suffix.lower() == ".css":
            problems.extend(check_css(site_root, path))

    if problems:
        print(f"Checked {checked} files. Found {len(problems)} broken local references.\n")
        for problem in problems[: args.max_problems]:
            rel_source = problem.source.relative_to(site_root.parent)
            print(f"- {rel_source}: {problem.target} -> {problem.reason}")
        if len(problems) > args.max_problems:
            print(f"\nOutput truncated. {len(problems) - args.max_problems} more problems not shown.")
        return 1

    print(f"Checked {checked} files. No broken local links/assets found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
