#!/usr/bin/env python3
from pathlib import Path
import json, re, sys

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "localization/documents"
CONFIG = ROOT / "localization/config.json"
SEGMENT_RE = re.compile(r"^(\d+)-.+\.md$")


def front_matter(path):
    text = path.read_text(encoding="utf-8", errors="ignore")
    if not text.startswith("---\n"):
        return {}, "missing front matter"
    parts = text.split("---\n", 2)
    if len(parts) != 3:
        return {}, "malformed front matter"
    meta = {}
    for line in parts[1].splitlines():
        key, sep, value = line.partition(":")
        if sep:
            meta[key.strip()] = value.strip()
    return meta, None


def main():
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    errors, warnings = [], []
    contracts = sorted(DOCS.glob("*.json"))
    if not contracts:
        errors.append("no localized document contracts found")

    for contract_path in contracts:
        data = json.loads(contract_path.read_text(encoding="utf-8"))
        document_id = data.get("document_id")
        assembler = ROOT / data.get("assembly_tool", "")
        if not assembler.is_file():
            errors.append(f"{contract_path.name}: missing assembly tool {data.get('assembly_tool')}")

        for language in ("tlh", "qya"):
            lang_cfg = config["languages"][language]
            base_rel = data.get("canonical_targets", {}).get(language)
            if not base_rel:
                errors.append(f"{contract_path.name}: missing canonical target for {language}")
                continue
            base = ROOT / base_rel
            if not base.is_file():
                errors.append(f"{contract_path.name}: missing canonical base {base_rel}")
                continue
            base_meta, problem = front_matter(base)
            if problem:
                errors.append(f"{base_rel}: {problem}")
            elif base_meta.get("language") != language:
                errors.append(f"{base_rel}: language mismatch")

            segments = data.get("source_segments", {}).get(language, [])
            if len(segments) != len(set(segments)):
                errors.append(f"{contract_path.name}: duplicate {language} segment path")
            numbers = []
            for segment_rel in segments:
                segment = ROOT / segment_rel
                if not segment.is_file():
                    errors.append(f"{contract_path.name}: missing segment {segment_rel}")
                    continue
                match = SEGMENT_RE.match(segment.name)
                if not match:
                    errors.append(f"{segment_rel}: segment filename needs numeric prefix")
                else:
                    numbers.append(int(match.group(1)))
                meta, problem = front_matter(segment)
                if problem:
                    errors.append(f"{segment_rel}: {problem}")
                    continue
                if meta.get("document_id") != document_id:
                    errors.append(f"{segment_rel}: document_id mismatch")
                if meta.get("language") != language:
                    errors.append(f"{segment_rel}: language mismatch")
                if meta.get("publication") != "forbidden" and not lang_cfg.get("publish"):
                    errors.append(f"{segment_rel}: draft segment must declare publication: forbidden")
                if lang_cfg.get("publish") and meta.get("status") != "approved":
                    errors.append(f"{segment_rel}: published language requires approved segment")
                elif meta.get("status") != "approved":
                    warnings.append(f"{segment_rel}: status={meta.get('status', 'missing')}")
            if numbers != sorted(numbers):
                errors.append(f"{contract_path.name}: {language} segments are not numerically ordered")

    if warnings:
        print(f"WARNINGS: {len(warnings)} draft segment statuses")
        for item in warnings:
            print("-", item)
    if errors:
        print("FAIL: localized document contract errors")
        for item in errors:
            print("-", item)
        return 1
    print(f"OK: localized document contracts valid ({len(contracts)} contract(s)).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
