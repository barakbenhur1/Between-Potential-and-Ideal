#!/usr/bin/env python3
from __future__ import annotations

from argparse import ArgumentParser
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_LANGUAGES = {"tlh", "qya"}


def strip_front_matter(text: str, path: Path) -> str:
    if not text.startswith("---\n"):
        raise SystemExit(f"Missing front matter: {path}")
    parts = text.split("---\n", 2)
    if len(parts) != 3:
        raise SystemExit(f"Malformed front matter: {path}")
    return parts[2].strip()


def main() -> int:
    parser = ArgumentParser(description="Assemble one localized document from its canonical base and ordered continuation segments.")
    parser.add_argument("document_id")
    parser.add_argument("language", choices=sorted(ALLOWED_LANGUAGES))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    contract_path = ROOT / "localization" / "documents" / f"{args.document_id}.json"
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    language = args.language

    base = ROOT / contract["canonical_targets"][language]
    segments = [ROOT / item for item in contract.get("source_segments", {}).get(language, [])]
    inputs = [base, *segments]
    for path in inputs:
        if not path.is_file():
            raise SystemExit(f"Missing canonical source segment: {path.relative_to(ROOT)}")

    base_text = base.read_text(encoding="utf-8").rstrip()
    marker = "\n---\n\n## "
    control_markers = ("Translation control note", "mIw qawmoHghach", "Enyalë Léo")
    cut_at = None
    for control in control_markers:
        needle = f"\n## {control}"
        index = base_text.find(needle)
        if index >= 0:
            cut_at = index
            break
    if cut_at is None:
        raise SystemExit("Canonical base is missing its translation control note")

    body = base_text[:cut_at].rstrip()
    control = base_text[cut_at:].lstrip()
    assembled_parts = [body]
    for segment in segments:
        assembled_parts.append(strip_front_matter(segment.read_text(encoding="utf-8"), segment))
    assembled_parts.append(control)
    assembled = "\n\n".join(part.strip() for part in assembled_parts if part.strip()) + "\n"

    output = args.output or (
        ROOT / "reports" / "localization" / "assembled" / language / f"{args.document_id}-{language}.md"
    )
    output = output.resolve()
    public_root = (ROOT / "site").resolve()
    if output == public_root or public_root in output.parents:
        raise SystemExit("Assembler may not write draft output under site/")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(assembled, encoding="utf-8")

    print(f"base={base.relative_to(ROOT)}")
    print(f"segments={len(segments)}")
    for segment in segments:
        print(f"- {segment.relative_to(ROOT)}")
    print(f"output={output.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
