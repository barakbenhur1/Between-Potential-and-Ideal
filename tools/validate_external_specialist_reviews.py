#!/usr/bin/env python3
"""Validate immutable external specialist review intake for segment 020.

Missing review responses are a legitimate pending state. Once a response file is
added, however, it must be complete enough to audit and the authoritative status
file must agree with the validated intake state.
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEW_DIR = ROOT / "localization/reviews/between-potential-and-ideal"
STATUS_PATH = REVIEW_DIR / "020-specialist-status.json"
OUT = ROOT / "reports/localization/constructed-language-audit"
PACKET_COMMIT = "fc1867f8e94bf588d8e3f2d9954207444a5083f8"
ALLOWED_DECISIONS = {
    "PASS",
    "PASS WITH CORRECTION",
    "REJECT",
    "INSUFFICIENT EVIDENCE",
}


@dataclass(frozen=True)
class ReviewSpec:
    lang: str
    label: str
    response_name: str
    template_name: str
    status_flag: str
    item_ids: tuple[str, ...]
    expertise_key: str
    overall_heading: str


SPECS = (
    ReviewSpec(
        lang="qya",
        label="Neo-Quenya",
        response_name="020-external-qya-review-response-r2.md",
        template_name="020-external-qya-review-response-template-r2.md",
        status_flag="external_qya_review_complete",
        item_ids=tuple(f"QYA-{index:02d}" for index in range(1, 9)),
        expertise_key="Declared expertise and source access",
        overall_heading="Overall Neo-Quenya decision",
    ),
    ReviewSpec(
        lang="tlh",
        label="Klingon",
        response_name="020-external-tlh-review-response-r2.md",
        template_name="020-external-tlh-review-response-template-r2.md",
        status_flag="external_tlh_review_complete",
        item_ids=tuple(f"TLH-{index:02d}" for index in range(1, 8)),
        expertise_key="Declared expertise and canonical source access",
        overall_heading="Overall Klingon decision",
    ),
)


def field(text: str, key: str) -> str:
    match = re.search(rf"^{re.escape(key)}:\s*(.*?)\s*$", text, flags=re.M)
    return match.group(1).strip() if match else ""


def section(text: str, heading_prefix: str) -> str:
    match = re.search(
        rf"^##\s+{re.escape(heading_prefix)}\b.*?\n(.*?)(?=^##\s+|\Z)",
        text,
        flags=re.M | re.S,
    )
    return match.group(1) if match else ""


def selected_decision(text: str, key: str = "Decision") -> str:
    value = field(text, key).upper()
    if value in ALLOWED_DECISIONS:
        return value

    # Also permit a response that marks exactly one of the template options.
    block = re.search(
        rf"^{re.escape(key)}:\s*$\n(.*?)(?=^[A-Z][^\n:]*:\s*|^##\s+|\Z)",
        text,
        flags=re.M | re.S,
    )
    if not block:
        return ""
    selected = []
    for line in block.group(1).splitlines():
        match = re.match(r"^\s*-\s*\[(x|X)\]\s*(.+?)\s*$", line)
        if match and match.group(2).strip().upper() in ALLOWED_DECISIONS:
            selected.append(match.group(2).strip().upper())
    return selected[0] if len(selected) == 1 else ""


def nonempty_after_label(section_text: str, key: str) -> bool:
    return bool(field(section_text, key))


def validate_response(spec: ReviewSpec, text: str) -> tuple[list[str], dict]:
    errors: list[str] = []
    decisions: dict[str, str] = {}

    if "Status: blank response template" in text or "This file is not a review" in text:
        errors.append("response still declares itself to be the blank template")

    for key in ("Reviewer", "Review date", spec.expertise_key, "Reviewed packet commit"):
        value = field(text, key)
        if not value:
            errors.append(f"missing metadata field: {key}")
    reviewed_commit = field(text, "Reviewed packet commit")
    review_date = field(text, "Review date")
    if review_date and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", review_date):
        errors.append("Review date must use YYYY-MM-DD")
    if reviewed_commit and reviewed_commit.strip("`") != PACKET_COMMIT:
        errors.append(
            f"reviewed packet commit must be {PACKET_COMMIT}, found {reviewed_commit!r}"
        )

    for item_id in spec.item_ids:
        item = section(text, item_id)
        if not item:
            errors.append(f"missing section: {item_id}")
            continue
        if item_id == "TLH-07":
            decision = "SOURCE LEDGER"
        else:
            decision = selected_decision(item)
            if not decision:
                errors.append(f"{item_id}: choose exactly one allowed decision")
        decisions[item_id] = decision

        source_keys = (
            "Exact lexical sources",
            "Exact canonical lexical sources",
            "Exact Tolkien primary locator for `pusta-`",
            "Exact Tolkien primary locator",
            "Exact canonical sources",
        )
        grammar_keys = ("Exact grammar sources",)
        parse_keys = (
            "Morpheme-by-morpheme parse",
            "Word-by-word and suffix parse",
            "Clause-by-clause parse",
            "Full parse",
        )
        back_translation_keys = (
            "Literal back-translation",
            "Literal back-translations",
        )
        danger_keys = ("Alternative or dangerous readings",)

        if item_id == "TLH-07":
            ledger_rows = []
            for line in item.splitlines():
                if not line.lstrip().startswith("|") or line.count("|") < 6:
                    continue
                cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
                if not cells or cells[0] in {"Form", "---"} or set(cells[0]) == {"-"}:
                    continue
                ledger_rows.append(cells)
            if len(ledger_rows) < 14:
                errors.append("TLH-07: source-locator ledger is incomplete")
            else:
                for cells in ledger_rows:
                    form = cells[0]
                    if len(cells) < 5 or not cells[2] or not cells[3] or not cells[4]:
                        errors.append(
                            f"TLH-07: `{form}` lacks source work, precise locator, or canon status"
                        )
        elif decision in {"PASS", "PASS WITH CORRECTION"}:
            if item_id == "QYA-08":
                for key in (
                    "Exact Tolkien primary locator",
                    "Source date/period",
                    "Attested form and gloss",
                    "Sense boundary",
                    "Production recommendation",
                ):
                    if not nonempty_after_label(item, key):
                        errors.append(f"QYA-08: accepted lexical item lacks {key}")
            else:
                if not any(nonempty_after_label(item, key) for key in source_keys):
                    errors.append(f"{item_id}: accepted form lacks exact source locator(s)")
                if not any(nonempty_after_label(item, key) for key in parse_keys):
                    errors.append(f"{item_id}: accepted form lacks a complete parse")
                if not any(nonempty_after_label(item, key) for key in back_translation_keys):
                    errors.append(f"{item_id}: accepted form lacks literal back-translation")
                if not any(nonempty_after_label(item, key) for key in danger_keys):
                    errors.append(f"{item_id}: accepted form lacks alternate-reading analysis")
                if any(key in item for key in grammar_keys) and not any(
                    nonempty_after_label(item, key) for key in grammar_keys
                ):
                    errors.append(f"{item_id}: accepted form lacks exact grammar source(s)")

        if decision == "PASS WITH CORRECTION" and not (
            nonempty_after_label(item, "Corrected form, if any")
            or nonempty_after_label(item, "Corrected forms, if any")
            or nonempty_after_label(item, "Corrected stop clause, if defensible")
            or nonempty_after_label(
                item,
                "Direct “replace / instead of / take another's place” construction, if any",
            )
            or nonempty_after_label(
                item,
                "Direct “replace / take another's place / act instead of” construction, if any",
            )
        ):
            errors.append(f"{item_id}: PASS WITH CORRECTION lacks corrected wording")

    overall = section(text, spec.overall_heading)
    if not overall:
        errors.append(f"missing section: {spec.overall_heading}")
        overall_decisions = {}
    else:
        overall_decisions = {
            key: selected_decision(overall, key)
            for key in ("Complete title candidate", "Opening proposition architecture")
        }
        for key, decision in overall_decisions.items():
            if not decision:
                errors.append(f"overall decision missing or ambiguous: {key}")

    signature = field(text, "Reviewer signature/name")
    if not signature:
        errors.append("missing reviewer signature/name")
    if (
        "I reviewed the cited primary sources" not in text
        and "I checked the cited Okrand sources" not in text
    ):
        errors.append("required reviewer attestation is missing")

    return errors, {
        "decisions": decisions,
        "overall_decisions": overall_decisions,
        "reviewer": field(text, "Reviewer"),
        "review_date": field(text, "Review date"),
        "reviewed_packet_commit": reviewed_commit.strip("`"),
    }


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    status = json.loads(STATUS_PATH.read_text(encoding="utf-8"))
    acceptance = status.get("acceptance", {})
    rows = []
    all_errors: list[str] = []

    for spec in SPECS:
        response_path = REVIEW_DIR / spec.response_name
        template_path = REVIEW_DIR / spec.template_name
        response_exists = response_path.exists()
        status_complete = acceptance.get(spec.status_flag) is True
        row = {
            "language": spec.lang,
            "label": spec.label,
            "response_path": str(response_path.relative_to(ROOT)),
            "template_path": str(template_path.relative_to(ROOT)),
            "response_exists": response_exists,
            "status_complete": status_complete,
            "valid": False,
            "errors": [],
        }

        if not template_path.exists():
            row["errors"].append("required response template is missing")
        if not response_exists:
            if status_complete:
                row["errors"].append(
                    f"{spec.status_flag}=true but immutable response file is missing"
                )
            row["state"] = "pending"
        else:
            response_text = response_path.read_text(encoding="utf-8")
            errors, details = validate_response(spec, response_text)
            row.update(details)
            row["errors"].extend(errors)
            row["valid"] = not row["errors"]
            row["state"] = "valid" if row["valid"] else "invalid"
            if row["valid"] and not status_complete:
                row["errors"].append(
                    f"validated response exists but {spec.status_flag} is not true"
                )
                row["valid"] = False
                row["state"] = "status-mismatch"
            if not row["valid"] and status_complete:
                row["errors"].append(
                    f"{spec.status_flag}=true but response validation failed"
                )

        all_errors.extend(f"{spec.lang}: {error}" for error in row["errors"])
        rows.append(row)

    both_valid = all(row["valid"] for row in rows)
    if status.get("approved") is True and not both_valid:
        all_errors.append("segment approved=true before both external reviews validate")
    if status.get("publication") != "forbidden":
        all_errors.append("segment 020 publication must remain forbidden at review-intake stage")

    result = {
        "schema_version": 1,
        "segment": 20,
        "packet_commit": PACKET_COMMIT,
        "responses": rows,
        "both_external_reviews_valid": both_valid,
        "publication_approved": False,
        "errors": all_errors,
    }
    (OUT / "external-specialist-review-intake.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    md = [
        "# Segment 020 external specialist review intake",
        "",
        f"Packet commit: `{PACKET_COMMIT}`",
        f"Both external reviews valid: **{str(both_valid).lower()}**",
        "Publication approved: **false**",
        "",
        "| Language | Response | State | Status flag | Errors |",
        "|---|---|---|---|---|",
    ]
    for row in rows:
        errors = "; ".join(row["errors"]) or "none"
        escaped_errors = errors.replace("|", "\\|")
        md.append(
            f"| {row['label']} | `{row['response_path']}` | {row.get('state', 'invalid')} | "
            f"{str(row['status_complete']).lower()} | {escaped_errors} |"
        )
    (OUT / "external-specialist-review-intake.md").write_text(
        "\n".join(md) + "\n",
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "segment": 20,
                "qya": rows[0].get("state"),
                "tlh": rows[1].get("state"),
                "both_valid": both_valid,
                "errors": len(all_errors),
            }
        )
    )
    if all_errors:
        for error in all_errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
