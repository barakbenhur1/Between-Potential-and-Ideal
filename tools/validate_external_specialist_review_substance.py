#!/usr/bin/env python3
"""Reject placeholder-filled or unsupported specialist review responses."""

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

PLACEHOLDERS = {
    "-", "--", "...", "n/a", "na", "none", "not applicable",
    "not provided", "placeholder", "same as above", "tbd", "todo", "unknown",
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
BACK_KEYS = ("Literal back-translation", "Literal back-translations")
DANGER_KEYS = ("Alternative or dangerous readings",)


def clean(value: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[`*_>#]", "", value).strip())


def substantive(value: str) -> bool:
    value = clean(value)
    return bool(value) and value.casefold() not in PLACEHOLDERS and len(re.findall(r"[\w\d]", value)) >= 3


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
    return " ".join(line.strip() for line in match.group(1).splitlines() if line.strip())


def has_field(text: str, keys: tuple[str, ...]) -> bool:
    return any(substantive(field_or_block(text, key)) for key in keys)


def normalize_name(value: str) -> str:
    tokens = re.findall(r"[\w'-]+", clean(value).casefold())
    while tokens and tokens[0].rstrip(".") in {"dr", "prof", "mr", "mrs", "ms"}:
        tokens.pop(0)
    return " ".join(tokens)


def names_match(reviewer: str, signature: str) -> bool:
    left, right = normalize_name(reviewer), normalize_name(signature)
    return bool(left and right) and (
        left == right
        or (len(left) >= 5 and left in right)
        or (len(right) >= 5 and right in left)
    )


def validate_review_date(value: str) -> str | None:
    try:
        parsed = date.fromisoformat(value)
    except ValueError:
        return "Review date must be a real calendar date in YYYY-MM-DD format"
    return "Review date cannot be in the future" if parsed > date.today() else None


def specific_answers(item: str) -> list[str]:
    return [
        match.group(1).strip()
        for match in re.finditer(r"^\s*\d+\.\s+[^:\n]+:\s*(.*?)\s*$", item, flags=re.M)
    ]


def validate_ledger(item: str) -> list[str]:
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
    errors: list[str] = []
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
    if item_id == "TLH-07":
        return validate_ledger(item)

    errors: list[str] = []
    answers = specific_answers(item)
    if answers and any(not substantive(answer) for answer in answers):
        errors.append(f"{item_id}: every numbered specific answer must be completed substantively")

    if item_id == "QYA-08":
        required = (
            "Exact Tolkien primary locator",
            "Source date/period",
            "Attested form and gloss",
            "Sense boundary",
            "Production recommendation",
        )
        keys = required if decision != "INSUFFICIENT EVIDENCE" else (
            "Exact Tolkien primary locator",
            "Production recommendation",
        )
        for key in keys:
            if not substantive(field_or_block(item, key)):
                errors.append(f"QYA-08: {decision} lacks substantive {key}")
        return errors

    if decision in {"PASS", "PASS WITH CORRECTION", "REJECT"}:
        checks = (
            (SOURCE_KEYS, "exact source locator(s)"),
            (PARSE_KEYS, "complete parse"),
            (BACK_KEYS, "literal back-translation"),
            (DANGER_KEYS, "alternate-reading analysis"),
        )
        for keys, label in checks:
            if not has_field(item, keys):
                errors.append(f"{item_id}: {decision} lacks substantive {label}")
        if any(key in item for key in GRAMMAR_KEYS) and not has_field(item, GRAMMAR_KEYS):
            errors.append(f"{item_id}: {decision} lacks substantive exact grammar source(s)")
    elif decision == "INSUFFICIENT EVIDENCE":
        if not has_field(item, SOURCE_KEYS):
            errors.append(
                f"{item_id}: INSUFFICIENT EVIDENCE must state which exact source check failed or was unavailable"
            )
        if not has_field(item, DANGER_KEYS):
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
    if not substantive(expertise) or len(clean(expertise)) < 20:
        errors.append(f"{spec.expertise_key} must describe relevant expertise and source access")
    if review_date:
        date_error = validate_review_date(clean(review_date))
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
    all_decisions = set(decisions.values()) | set(overall_decisions.values())
    blocking = field_or_block(overall, "Blocking findings") if overall else ""
    corrections = field_or_block(overall, "Required corrections") if overall else ""
    if {"REJECT", "INSUFFICIENT EVIDENCE"} & all_decisions and not substantive(blocking):
        errors.append("rejected or insufficient decisions require substantive Blocking findings")
    if "PASS WITH CORRECTION" in all_decisions and not substantive(corrections):
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
        path = REVIEW_DIR / spec.response_name
        row = {
            "language": spec.lang,
            "label": spec.label,
            "response_path": str(path.relative_to(ROOT)),
            "response_exists": path.exists(),
            "state": "pending",
            "errors": [],
        }
        if path.exists():
            errors, details = validate_response(spec, path.read_text(encoding="utf-8"))
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
        escaped_errors = errors.replace("|", "\\|")
        md.append(
            f"| {row['label']} | `{row['response_path']}` | {row['state']} | {escaped_errors} |"
        )
    (OUT / "external-specialist-review-substance.md").write_text(
        "\n".join(md) + "\n",
        encoding="utf-8",
    )

    print(json.dumps({
        "segment": 20,
        "states": [row["state"] for row in rows],
        "errors": len(all_errors),
    }))
    if all_errors:
        for error in all_errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
