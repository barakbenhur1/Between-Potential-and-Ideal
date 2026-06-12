#!/usr/bin/env python3
"""Extract compact source-candidate records from a pinned Eldamo XML snapshot."""

from __future__ import annotations

import argparse
import json
import urllib.request
import xml.etree.ElementTree as ET

DEFAULT_URL = (
    "https://raw.githubusercontent.com/pfstrack/eldamo/"
    "4071c9caa95caca905c96af2505d5252045e2aaa/src/data/eldamo-data.xml"
)
FORM_KEYS = ("v", "value", "word", "form")
RECORD_KEYS = (
    "l",
    "v",
    "value",
    "word",
    "form",
    "gloss",
    "speech",
    "mark",
    "source",
    "ref",
    "rule",
    "from",
    "to",
)
SOURCE_KEYS = ("source", "ref", "page", "locator", "work", "v", "l", "gloss", "mark")


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def normalized(value: str) -> str:
    return value.strip().casefold().rstrip("-")


def selected(attributes: dict[str, str], keys: tuple[str, ...]) -> dict[str, str]:
    return {key: attributes[key] for key in keys if key in attributes}


def compact_text(element: ET.Element, limit: int = 180) -> str:
    value = " ".join(part.strip() for part in element.itertext() if part.strip())
    return " ".join(value.split())[:limit]


def is_exact_form(element: ET.Element, term: str) -> bool:
    wanted = normalized(term)
    return any(
        value and normalized(value) == wanted
        for key in FORM_KEYS
        if (value := element.attrib.get(key)) is not None
    )


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


def language_path(
    record: ET.Element,
    parents: dict[ET.Element, ET.Element],
) -> list[dict[str, object]]:
    path: list[dict[str, object]] = []
    current = parents.get(record)
    while current is not None:
        name = local_name(current.tag)
        if name in {"language", "language-cat"}:
            path.append({"tag": name, "attributes": dict(current.attrib)})
        current = parents.get(current)
    path.reverse()
    return path


def source_refs(record: ET.Element) -> list[dict[str, object]]:
    refs: list[dict[str, object]] = []
    seen: set[str] = set()
    for descendant in record.iter():
        name = local_name(descendant.tag)
        attributes = dict(descendant.attrib)
        relevant = (
            name in {"ref", "source"}
            or "source" in attributes
            or "ref" in attributes
        )
        if not relevant:
            continue
        item: dict[str, object] = {
            "tag": name,
            "attributes": selected(attributes, SOURCE_KEYS),
        }
        text = compact_text(descendant)
        if text:
            item["text"] = text
        identity = json.dumps(item, ensure_ascii=False, sort_keys=True)
        if identity in seen:
            continue
        seen.add(identity)
        refs.append(item)
        if len(refs) >= 25:
            break
    return refs


def extract(url: str, terms: list[str], max_records: int) -> list[dict[str, object]]:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Between-Potential-and-Ideal-source-audit"},
    )
    with urllib.request.urlopen(request, timeout=90) as response:
        payload = response.read()

    root = ET.fromstring(payload)
    parents = {child: parent for parent in root.iter() for child in parent}
    output: list[dict[str, object]] = []

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
            records.append(
                {
                    "record_tag": local_name(record.tag),
                    "record_attributes": selected(dict(record.attrib), RECORD_KEYS),
                    "matched_element": {
                        "tag": local_name(element.tag),
                        "attributes": selected(dict(element.attrib), RECORD_KEYS),
                    },
                    "language_path": language_path(record, parents),
                    "source_refs": source_refs(record),
                }
            )
            if len(records) >= max_records:
                break
        output.append(
            {
                "term": term,
                "exact_element_count": len(exact_elements),
                "record_count": len(seen),
                "records_returned": len(records),
                "records": records,
            }
        )

    print(
        "ELDAMO_META="
        + json.dumps(
            {"source_url": url, "byte_count": len(payload)},
            ensure_ascii=False,
            separators=(",", ":"),
        )
    )
    for result in output:
        summary = {key: value for key, value in result.items() if key != "records"}
        print("ELDAMO_TERM=" + json.dumps(summary, ensure_ascii=False, separators=(",", ":")))
        for index, record in enumerate(result["records"], start=1):
            print(
                "ELDAMO_RECORD="
                + json.dumps(
                    {"term": result["term"], "index": index, **record},
                    ensure_ascii=False,
                    separators=(",", ":"),
                )
            )
    return output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("terms", nargs="*", default=["tamma", "pusta"])
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--max-records", type=int, default=12)
    args = parser.parse_args()

    extract(args.url, args.terms, max(1, args.max_records))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
