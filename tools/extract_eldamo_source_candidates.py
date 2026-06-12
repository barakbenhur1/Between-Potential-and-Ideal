#!/usr/bin/env python3
"""Extract concise source-candidate records from a pinned Eldamo XML snapshot."""

from __future__ import annotations

import argparse
import json
import re
import urllib.request
import xml.etree.ElementTree as ET

DEFAULT_URL = (
    "https://raw.githubusercontent.com/pfstrack/eldamo/"
    "4071c9caa95caca905c96af2505d5252045e2aaa/src/data/eldamo-data.xml"
)


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def normalized(value: str) -> str:
    return value.strip().casefold().rstrip("-")


def compact_text(element: ET.Element, limit: int = 500) -> str:
    text = " ".join(part.strip() for part in element.itertext() if part.strip())
    return re.sub(r"\s+", " ", text)[:limit]


def is_exact_form(element: ET.Element, term: str) -> bool:
    wanted = normalized(term)
    for key in ("v", "value", "word", "form"):
        value = element.attrib.get(key)
        if value and normalized(value) == wanted:
            return True
    return False


def enclosing_record(
    element: ET.Element,
    parents: dict[ET.Element, ET.Element],
) -> ET.Element:
    current = element
    while True:
        name = local_name(current.tag)
        if name in {"word", "entry"}:
            return current
        if "l" in current.attrib and "v" in current.attrib:
            return current
        parent = parents.get(current)
        if parent is None:
            return element
        current = parent


def summarize_record(
    record: ET.Element,
    parents: dict[ET.Element, ET.Element],
) -> dict[str, object]:
    ancestors: list[dict[str, object]] = []
    current: ET.Element | None = record
    while current is not None and len(ancestors) < 8:
        ancestors.append(
            {
                "tag": local_name(current.tag),
                "attributes": dict(current.attrib),
            }
        )
        current = parents.get(current)

    evidence: list[dict[str, object]] = []
    interesting_tags = {
        "ref",
        "source",
        "gloss",
        "notes",
        "note",
        "deriv",
        "cognate",
        "inflect",
        "rule",
        "element",
        "combine",
    }
    interesting_attributes = {
        "source",
        "ref",
        "gloss",
        "speech",
        "mark",
        "v",
        "value",
        "l",
        "from",
        "to",
        "rule",
    }

    for descendant in record.iter():
        name = local_name(descendant.tag)
        attributes = dict(descendant.attrib)
        if name not in interesting_tags and not (
            set(attributes) & interesting_attributes
        ):
            continue
        evidence.append(
            {
                "tag": name,
                "attributes": attributes,
                "text": compact_text(descendant),
            }
        )

    return {
        "record_tag": local_name(record.tag),
        "record_attributes": dict(record.attrib),
        "record_text": compact_text(record, 1000),
        "ancestor_chain": ancestors,
        "evidence": evidence,
    }


def extract(url: str, terms: list[str]) -> dict[str, object]:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Between-Potential-and-Ideal-source-audit"},
    )
    with urllib.request.urlopen(request, timeout=90) as response:
        payload = response.read()

    root = ET.fromstring(payload)
    parents = {child: parent for parent in root.iter() for child in parent}
    result: dict[str, object] = {
        "source_url": url,
        "byte_count": len(payload),
        "terms": {},
    }

    for term in terms:
        exact_elements = [element for element in root.iter() if is_exact_form(element, term)]
        records: list[dict[str, object]] = []
        seen: set[str] = set()
        for element in exact_elements:
            record = enclosing_record(element, parents)
            identity = ET.tostring(record, encoding="unicode")
            if identity in seen:
                continue
            seen.add(identity)
            records.append(summarize_record(record, parents))
        result["terms"][term] = {
            "exact_element_count": len(exact_elements),
            "record_count": len(records),
            "records": records,
        }

    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("terms", nargs="*", default=["tamma", "pusta"])
    parser.add_argument("--url", default=DEFAULT_URL)
    args = parser.parse_args()

    report = extract(args.url, args.terms)
    print("ELDAMO_REPORT=" + json.dumps(report, ensure_ascii=False, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
