#!/usr/bin/env python3
"""Preflight one external specialist response before opening a pull request.

This command runs the same structural and substantive validators used by CI, but
it does not read or modify the authoritative status file and grants no approval.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import validate_external_specialist_review_substance as substance
import validate_external_specialist_reviews as intake


def review_spec(language: str) -> intake.ReviewSpec:
    for spec in intake.SPECS:
        if spec.lang == language:
            return spec
    raise ValueError(f"unsupported language: {language}")


def validate_text(language: str, text: str, source: str = "<memory>") -> dict:
    spec = review_spec(language)
    structure_errors, structure_details = intake.validate_response(spec, text)
    substance_errors, substance_details = substance.validate_response(spec, text)

    errors: list[str] = []
    for category, values in (
        ("structure", structure_errors),
        ("substance", substance_errors),
    ):
        for value in values:
            rendered = f"{category}: {value}"
            if rendered not in errors:
                errors.append(rendered)

    return {
        "schema_version": 1,
        "language": spec.lang,
        "label": spec.label,
        "source": source,
        "expected_submission_name": spec.response_name,
        "packet_commit": intake.PACKET_COMMIT,
        "valid_for_submission": not errors,
        "approval_granted": False,
        "publication_allowed": False,
        "errors": errors,
        "structure": structure_details,
        "substance": substance_details,
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate one segment-020 specialist response before submission."
    )
    parser.add_argument("--language", required=True, choices=[spec.lang for spec in intake.SPECS])
    parser.add_argument("--response", required=True, type=Path)
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print a machine-readable JSON report instead of the human summary.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    path = args.response.expanduser()
    if not path.is_file():
        print(f"ERROR: response file not found: {path}", file=sys.stderr)
        return 2

    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeError as exc:
        print(f"ERROR: response must be UTF-8: {exc}", file=sys.stderr)
        return 2

    result = validate_text(args.language, text, str(path))
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif result["valid_for_submission"]:
        print(
            "PASS: response is structurally and substantively valid for submission as "
            f"{result['expected_submission_name']}."
        )
        print("NOTE: preflight validates intake only; it grants no linguistic or publication approval.")
    else:
        print(
            f"FAIL: {result['label']} response has {len(result['errors'])} blocking preflight error(s).",
            file=sys.stderr,
        )
        for error in result["errors"]:
            print(f"- {error}", file=sys.stderr)
        print(
            f"Expected final repository filename: {result['expected_submission_name']}",
            file=sys.stderr,
        )

    return 0 if result["valid_for_submission"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
