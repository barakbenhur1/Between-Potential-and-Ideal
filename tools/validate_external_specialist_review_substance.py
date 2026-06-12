#!/usr/bin/env python3
"""Require substantive evidence in external specialist review responses.

The primary intake validator checks structure and status synchronization. This
second gate rejects placeholder-filled responses and requires every decision,
including REJECT and INSUFFICIENT EVIDENCE, to carry auditable reasoning.
Missing responses remain a valid pending state.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path

import validate_external_specialist_reviews as intake

ROOT = Path(__file__).resolve().parents[1]
REVIEW_DIR = ROOT / "localization/reviews/between-potential-and-ideal"
OUT = ROOT / "reports/localization/constructed-language-audit"

PLACEHOLDER_VALUES = {
    "-",
    "--",
    "...",
    "n/a",
    "na",
    "none",
    "not applicable",
    "not provided",
    "placeholder",
    "same as above",
    "tbd",
    "todo",
    "unknown",
}

SOURCE_KEYS = (
    "Exact lexical sources",
    "Exact canonical lexical sources",
    "Exact Tolkien primary locator for `pusta-`",
    "Exact Tolkien primary locator",
    "Exact canonical sources",
)
GRAMMAR_KEYS = ("Exact grammar sources",)
PARSE_KEYS = (
    "Morpheme-by-morpheme parse",
    "Word-by-word and suffix parse",
    "Clause-by-clause parse",
    "Full parse",
)
BACK_TRANSLATION_KEYS = (
    "Literal back-translation",
    "Literal back-translations",
)
DANGER_KEYS = ("Alternative or dangerous readings",)


def cleaned(value: str) -> str:
    value = re.sub(r"[`*_>#]", "", value).strip()
    value = re.sub(r"\s+", " ", value)
    return value


def substantive(value: str) -> bool:
    value = cleaned(value)
    if not value or value.casefold() in PLACEHOLDER_VALUES:
        return False
    return len(re.findall(r"[\w\d]", value, flags=re.UNICODE)) >= 3


def field_or_block(text: str, key: str) -> str:
    inline = intake.field(text, key)
    if substantive(inline):
        return inline
    match = re.search(
        rf"^{re.escape(key)}:\s*$\n(.*?)(?=^[A-Z][^\n:]{{1,100}}:\s*|^##\s+|\Z)",
        text,
        flags=re.M | re.S,
    )
    if not match:
        return ""
    lines = [line.strip() for line in match.group(1).splitlines() if line.strip()]
    return " ".join(lines)


def has_substantive_field(text: str, keys: tuple[str, ...]) -> bool:
    return any(substantive(field_or_block(text, key)) for key in keys)


def normalized_name(value: str) -> str:
    tokens = re.findall(r"[\w'-]+", cleaned(value).casefold(), flags=re.UNICODE)
    while tokens and tokens[0].rstrip(".") in {"dr", "prof", "mr", "mrs", "ms"}:
        tokens.pop(0)
    return " ".join(tokens)


def names_match(reviewer: str, signature: str) -> bool:
    left = normalized_name(reviewer)
    right = normalized_name(signature)
    if not left or not right:
        return False
    return left == right or (len(left) >= 5 and left in right) or (len(right) >= 5 and right in left)


def validate_review_date(value: str) -> str | None:
    try:
        parsed = date.fromisoformat(value)
    except ValueError:
        return "Review date must be a real calendar date in YYYY-MM-DD format"
    if parsed > date.today():
        return "Review date cannot be in the future"
    return None


def specific_answer_values(item: str) -> list[str]:
    return [
        match.group(1).strip()
        for match in re.finditer(r"^\s*\d+\.\s+[^:\n]+:\s*(.*?)\s*$", item, flags=re.M)
    ]


def validate_source_ledger(item: str) -> list[str]:
    errors: list[str] = []
    rows: list[list[str]] = []
    for line in item.splitlines():
        if not line.lstrip().startswith("|") or line.count("|") < 6:
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if not cells or cells[0] in {"Form", "---"} or set(cells[0]) == {"-"}:
            continue
        rows.append(cells)
    if len(rows) < 14:
        return ["TLH-07: source-locator ledger is incomplete"]
    for cells in rows:
        form = cells[0]
        if len(cells) < 5:
            errors.append(f"TLH-07: `{form}` has too few ledger columns")
            continue
        for label, index in (("source work", 2), ("precise locator", 3), ("canon status", 4)):
            if not substantive(cells[index]):
                errors.append(f"TLH-07: `{form}` has a blank or placeholder {label}")
    return errors


def validate_item(item_id: str, item: str, decision: str) -> list[str]:
    errors: list[str] = []
    if item_id == "TLH-07":
        return validate_source_ledger(item)

    specific = specific_answer_values(item)
    if specific and any(not substantive(value) for value in specific):
        errors.append(f"{item_id}: every numbered specific answer must be completed substantively")

    if item_id == "QYA-08":
        required = (
            "Exact Tolkien primary locator",
            "Source date/period",
            "Attested form and gloss",
            "Sense boundary",
            "Production recommendation",
        )
        if decision in {"PASS", "PASS WITH CORRECTION", "REJECT"}:
            for key in required:
                if not substantive(field_or_block(item, key)):
                    errors.append(f"QYA-08: {decision} lacks substantive {key}")
        elif decision == "INSUFFICIENT EVIDENCE":
            for key in ("Exact Tolkien primary locator", "Production recommendation"):
                if not substantive(field_or_block(item, key)):
                    errors.append(f"QYA-08: INSUFFICIENT EVIDENCE lacks {key}")
        return errors

    if decision in {"PASS", "PASS WITH CORRECTION", "REJECT"}:
        checks = (
            (SOURCE_KEYS, "exact source locator(s)"),
            (PARSE_KEYS, "complete parse"),
            (BACK_TRANSLATION_KEYS, "literal back-translation"),
            (DANGER_KEYS, "alternate-reading analysis"),
        )
        for keys, label in checks:
            if not has_substantive_field(item, keys):
                errors.append(f"{item_id}: {decision} lacks substantive {label}")
        if any(key in item for key in GRAMMAR_KEYS) and not has_substantive_field(item, GRAMMAR_KEYS):
            errors.append(f"{item_id}: {decision} lacks substantive exact grammar source(s)")
    elif decision == "INSUFFICIENT EVIDENCE":
        if not has_substantive_field(item, SOURCE_KEYS):
            errors.append(
                f"{item_id}: INSUFFICIENT EVIDENCE must state which exact source check failed or was unavailable"
            )
        if not has_substantive_field(item, DANGER_KEYS):
            errors.append(
                f"{item_id}: INSUFFICIENT EVIDENCE must explain the unresolved semantic or grammatical risk"
            )
    return errors


def validate_response(spec: intake.ReviewSpec, text: str) -> tuple[list[str], dict]:
    errors: list[str] = []
    reviewer = field_or_block(text, "Reviewer")
    expertise = field_or_block(text, spec.expertise_key)
    review_date = field_or_block(text, "Review date")
    signature = field_or_block(text, "Reviewer signature/name")

    if not substantive(reviewer):
        errors.append("Reviewer must contain a substantive name")
    if not substantive(expertise) or len(cleaned(expertise)) < 20:
        errors.append(f"{spec.expertise_key} must describe relevant expertise and source access")
    if review_date:
        date_error = validate_review_date(cleaned(review_date))
        if date_error:
            errors.append(date_error)
    if not substantive(signature):
        errors.append("Reviewer signature/name must be substantive")
    elif substantive(reviewer) and not names_match(reviewer, signature):
        errors.append("Reviewer signature/name must match the declared reviewer")

    decisions: dict[str, str] = {}
    for item_id in spec.item_ids:
        item = intake.section(text, item_id)
        if not item:
            continue
        decision = "SOURCE LEDGER" if item_id == "TLH-07" else intake.selected_decision(item)
        decisions[item_id] = decision
        if decision:
            errors.extend(validate_item(item_id, item, decision))

    overall = intake.section(text, spec.overall_heading)
    overall_decisions = {
        key: intake.selected_decision(overall, key)
        for key in ("Complete title candidate", "Opening proposition architecture")
    } if overall else {}

    item_values = set(decisions.values())
    overall_values = set(overall_decisions.values())
    blocking = field_or_block(overall, "Blocking findings") if overall else ""
    corrections = field_or_block(overall, "Required corrections") if overall else ""
    if ({"REJECT", "INSUFFICIENT EVIDENCE"} & (item_values | overall_values)) and not substantive(blocking):
        errors.append("rejected or insufficient decisions require substantive Blocking findings")
    if "PASS WITH CORRECTION" in (item_values | overall_values) and not substantive(corrections):
        errors.append("PASS WITH CORRECTION requires substantive Required corrections")

    return errors, {
        "reviewer": reviewer,
        "signature": signature,
        "review_date": review_date,
        "decisions": decisions,
        "overall_decisions": overall_decisions,
    }


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    all_errors: list[str] = []

    for spec in intake.SPECS:
        response_path = REVIEW_DIR / spec.response_name
        row = {
            "language": spec.lang,
            "label": spec.label,
            "response_path": str(response_path.relative_to(ROOT)),
            "response_exists": response_path.exists(),
            "state": "pending",
            "errors": [],
        }
        if response_path.exists():
            errors, details = validate_response(spec, response_path.read_text(encoding="utf-8"))
            row.update(details)
            row["errors"] = errors
            row["state"] = "valid" if not errors else "invalid"
            all_errors.extend(f"{spec.lang}: {error}" for error in errors)
        rows.append(row)

    result = {
        "schema_version": 1,
        "segment": 20,
        "responses": rows,
        "all_present_responses_substantive": not all_errors,
        "errors": all_errors,
    }
    (OUT / "external-specialist-review-substance.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    md = [
        "# Segment 020 external specialist review substance",
        "",
        f"All present responses substantive: **{str(not all_errors).lower()}**",
        "",
        "| Language | Response | State | Errors |",
        "|---|---|---|---|",
    ]
    for row in rows:
        errors = "; ".join(row["errors"]) or "none"
        md.append(
            f"| {row['label']} | `{row['response_path']}` | {row['state']} | {errors.replace('|', '\\|')} |"
        )
    (OUT / "external-specialist-review-substance.md").write_text(
        "\n".join(md) + "\n",
        encoding="utf-8",
    )

    print(json.dumps({"segment": 20, "states": [row["state"] for row in rows], "errors": len(all_errors)}))
    if all_errors:
        for error in all_errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
