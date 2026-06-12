#!/usr/bin/env python3
"""Extract a compact Klingon source ledger from a pinned boQwI data snapshot."""

from __future__ import annotations

import argparse
import html
import json
import re
import urllib.request

DEFAULT_REPOSITORY = "De7vID/klingon-assistant-data"
DEFAULT_COMMIT = "e2d0a8a0e061a67b1ae342913cdd487a6af20baa"
DEFAULT_TERMS = [
    "mIw",
    "choH",
    "-bogh",
    "pung",
    "vang",
    "yIn",
    "ghot",
    "'e'",
    "chaw'",
    "jatlh",
    "-laH",
    "SeH",
    "-pa'",
    "mev",
]
FILES = [
    "mem-01-b.xml",
    "mem-02-ch.xml",
    "mem-03-D.xml",
    "mem-04-gh.xml",
    "mem-05-H.xml",
    "mem-06-j.xml",
    "mem-07-l.xml",
    "mem-08-m.xml",
    "mem-09-n.xml",
    "mem-10-ng.xml",
    "mem-11-p.xml",
    "mem-12-q.xml",
    "mem-13-Q.xml",
    "mem-14-r.xml",
    "mem-15-S.xml",
    "mem-16-t.xml",
    "mem-17-tlh.xml",
    "mem-18-v.xml",
    "mem-19-w.xml",
    "mem-20-y.xml",
    "mem-21-a.xml",
    "mem-22-e.xml",
    "mem-23-I.xml",
    "mem-24-o.xml",
    "mem-25-u.xml",
    "mem-26-suffixes.xml",
    "mem-27-extra.xml",
]
TABLE_RE = re.compile(r'<table\s+name="mem">(.*?)</table>', re.DOTALL)
COLUMN_RE = re.compile(r'<column\s+name="([^"]+)">(.*?)</column>', re.DOTALL)


def clean(value: str) -> str:
    value = re.sub(r"<[^>]+>", "", value)
    return html.unescape(value).strip()


def download(repository: str, commit: str, filename: str) -> str:
    url = f"https://raw.githubusercontent.com/{repository}/{commit}/{filename}"
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Between-Potential-and-Ideal-source-audit"},
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read().decode("utf-8")


def records_from_fragment(fragment: str, filename: str) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    for table in TABLE_RE.findall(fragment):
        columns = {name: clean(value) for name, value in COLUMN_RE.findall(table)}
        if not columns.get("entry_name"):
            continue
        columns["data_file"] = filename
        records.append(columns)
    return records


def normalized_entry_name(value: str) -> str:
    return value.strip()


def extract(repository: str, commit: str, terms: list[str]) -> dict[str, object]:
    wanted = {normalized_entry_name(term) for term in terms}
    matches: dict[str, list[dict[str, str]]] = {term: [] for term in terms}
    files_read = 0
    records_read = 0

    for filename in FILES:
        fragment = download(repository, commit, filename)
        files_read += 1
        records = records_from_fragment(fragment, filename)
        records_read += len(records)
        for record in records:
            name = normalized_entry_name(record["entry_name"])
            if name not in wanted:
                continue
            compact = {
                key: record.get(key, "")
                for key in (
                    "entry_name",
                    "part_of_speech",
                    "definition",
                    "notes",
                    "hidden_notes",
                    "components",
                    "examples",
                    "source",
                    "data_file",
                )
            }
            matches[name].append(compact)

    return {
        "repository": repository,
        "commit": commit,
        "files_read": files_read,
        "records_read": records_read,
        "terms": [
            {
                "term": term,
                "match_count": len(matches[term]),
                "matches": matches[term],
            }
            for term in terms
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("terms", nargs="*", default=DEFAULT_TERMS)
    parser.add_argument("--repository", default=DEFAULT_REPOSITORY)
    parser.add_argument("--commit", default=DEFAULT_COMMIT)
    args = parser.parse_args()

    report = extract(args.repository, args.commit, args.terms or DEFAULT_TERMS)
    meta = {key: report[key] for key in ("repository", "commit", "files_read", "records_read")}
    print("BOQWI_META=" + json.dumps(meta, ensure_ascii=False, separators=(",", ":")))
    for term in report["terms"]:
        print("BOQWI_TERM=" + json.dumps(term, ensure_ascii=False, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
