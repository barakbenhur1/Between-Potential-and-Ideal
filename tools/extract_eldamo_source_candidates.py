#!/usr/bin/env python3
"""Extract compact records from a pinned Eldamo XML snapshot."""

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
FORM_KEYS = ("v", "value", "word", "form")
RECORD_KEYS = ("l", "v", "value", "word", "form", "gloss", "speech", "mark")
SOURCE_KEYS = ("source", "ref", "page", "locator", "work", "v", "l", "gloss", "mark")


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def normalized(value: str) -> str:
    return value.strip().casefold().rstrip("-")


def selected(attributes: dict[str, str], keys: tuple[str, ...]) -> dict[str, str]:
    return {key: attributes[key] for key in keys if key in attributes}


def compact_text(element: ET.Element, limit: int = 160) -> str:
    value = " ".join(part.strip() for part in element.itertext() if part.strip())
    return " ".join(value.split())[:limit]


def source_refs(record: ET.Element) -> list[dict[str, object]]:
    refs: list[dict[str, object]] = []
    seen: set[str] = set()
    for descendant in record.iter():
        name = local_name(descendant.tag)
        attributes = dict(descendant.attrib)
        if name not in {"ref", "source"} and "source" not in attributes and "ref" not in attributes:
            continue
        item: dict[str, object] = {"tag": name, "attributes": selected(attributes, SOURCE_KEYS)}
        text = compact_text(descendant)
        if text:
            item["text"] = text
        identity = json.dumps(item, ensure_ascii=False, sort_keys=True)
        if identity in seen:
            continue
        seen.add(identity)
        refs.append(item)
        if len(refs) >= 16:
            break
    return refs


def record_summary(record: ET.Element, matched: ET.Element | None = None) -> dict[str, object]:
    result: dict[str, object] = {
        "record_tag": local_name(record.tag),
        "record_attributes": selected(dict(record.attrib), RECORD_KEYS),
        "source_refs": source_refs(record),
    }
    if matched is not None:
        result["matched_element"] = {
            "tag": local_name(matched.tag),
            "attributes": selected(dict(matched.attrib), RECORD_KEYS),
        }
    return result


def enclosing_record(element: ET.Element, parents: dict[ET.Element, ET.Element]) -> ET.Element:
    current = element
    while True:
        if local_name(current.tag) in {"word", "entry"}:
            return current
        if "l" in current.attrib and "v" in current.attrib:
            return current
        parent = parents.get(current)
        if parent is None:
            return element
        current = parent


def exact_matches(
    root: ET.Element,
    parents: dict[ET.Element, ET.Element],
    term: str,
    max_records: int,
) -> list[dict[str, object]]:
    wanted = normalized(term)
    records: list[dict[str, object]] = []
    seen: set[str] = set()
    for element in root.iter():
        values = [element.attrib.get(key) for key in FORM_KEYS]
        if not any(value and normalized(value) == wanted for value in values):
            continue
        record = enclosing_record(element, parents)
        identity = ET.tostring(record, encoding="unicode")
        if identity in seen:
            continue
        seen.add(identity)
        records.append(record_summary(record, element))
        if len(records) >= max_records:
            break
    return records


def combined_gloss(record: ET.Element) -> str:
    values: list[str] = []
    for element in record.iter():
        gloss = element.attrib.get("gloss")
        if gloss:
            values.append(gloss)
    return " | ".join(values)


def gloss_matches(
    root: ET.Element,
    pattern: str,
    languages: set[str],
    max_records: int,
) -> list[dict[str, object]]:
    matcher = re.compile(pattern, re.IGNORECASE)
    records: list[dict[str, object]] = []
    for record in root.iter():
        if local_name(record.tag) != "word" or record.attrib.get("l") not in languages:
            continue
        glosses = combined_gloss(record)
        hit = matcher.search(glosses)
        if not hit:
            continue
        summary = record_summary(record)
        summary["matched_gloss"] = hit.group(0)
        summary["all_glosses"] = glosses[:500]
        records.append(summary)
        if len(records) >= max_records:
            break
    return records


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("terms", nargs="*")
    parser.add_argument("--gloss-regex")
    parser.add_argument("--languages", default="q,mq")
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--max-records", type=int, default=40)
    args = parser.parse_args()

    request = urllib.request.Request(
        args.url,
        headers={"User-Agent": "Between-Potential-and-Ideal-source-audit"},
    )
    with urllib.request.urlopen(request, timeout=90) as response:
        payload = response.read()
    root = ET.fromstring(payload)
    parents = {child: parent for parent in root.iter() for child in parent}
    limit = max(1, args.max_records)

    print("ELDAMO_META=" + json.dumps({"source_url": args.url, "byte_count": len(payload)}, separators=(",", ":")))

    if args.gloss_regex:
        languages = {item.strip() for item in args.languages.split(",") if item.strip()}
        records = gloss_matches(root, args.gloss_regex, languages, limit)
        print(
            "ELDAMO_GLOSS_TERM="
            + json.dumps(
                {
                    "pattern": args.gloss_regex,
                    "languages": sorted(languages),
                    "records_returned": len(records),
                },
                ensure_ascii=False,
                separators=(",", ":"),
            )
        )
        for index, record in enumerate(records, start=1):
            print("ELDAMO_GLOSS_RECORD=" + json.dumps({"index": index, **record}, ensure_ascii=False, separators=(",", ":")))
        return 0

    terms = args.terms or ["tamma", "pusta"]
    for term in terms:
        records = exact_matches(root, parents, term, limit)
        print("ELDAMO_TERM=" + json.dumps({"term": term, "records_returned": len(records)}, ensure_ascii=False, separators=(",", ":")))
        for index, record in enumerate(records, start=1):
            print("ELDAMO_RECORD=" + json.dumps({"term": term, "index": index, **record}, ensure_ascii=False, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
