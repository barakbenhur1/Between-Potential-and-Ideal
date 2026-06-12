#!/usr/bin/env python3
"""End-to-end contract tests for the external specialist response templates."""

from __future__ import annotations

import json
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate_external_specialist_reviews as intake  # noqa: E402
import validate_external_specialist_review_substance as substance  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
REVIEW_DIR = ROOT / "localization/reviews/between-potential-and-ideal"
GENERIC_EVIDENCE = (
    "Checked the named primary or canonical sources; exact support remains unavailable, "
    "so this item is not approved for production."
)


def set_blank_field(text: str, key: str, value: str) -> str:
    """Set one blank Markdown field, including a field at end-of-file."""

    pattern = rf"(?m)^{re.escape(key)}:[ \t]*$"
    updated, count = re.subn(pattern, f"{key}: {value}", text, count=1)
    if count != 1:
        raise AssertionError(f"expected exactly one blank field for {key!r}, found {count}")
    return updated


def fill_blank_labels(section_text: str) -> str:
    """Fill every blank field and numbered answer in one review section."""

    def replace(match: re.Match[str]) -> str:
        label = match.group(1)
        return f"{label}: {GENERIC_EVIDENCE}"

    return re.sub(
        r"(?m)^([^#|\n][^:\n]{0,180}):[ \t]*$",
        replace,
        section_text,
    )


def replace_section(text: str, heading: str, transform) -> str:
    pattern = re.compile(
        rf"(^##\s+{re.escape(heading)}\b.*?\n)(.*?)(?=^##\s+|\Z)",
        flags=re.M | re.S,
    )
    match = pattern.search(text)
    if not match:
        raise AssertionError(f"missing section {heading}")
    return text[: match.start()] + match.group(1) + transform(match.group(2)) + text[match.end() :]


def fill_ledger(section_text: str) -> str:
    rows = []
    for line in section_text.splitlines():
        if line.startswith("|") and line.count("|") >= 6:
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if cells and cells[0] not in {"Form", "---"} and set(cells[0]) != {"-"}:
                cells[2] = "Okrand primary source"
                cells[3] = "page or event locator"
                cells[4] = "canonical"
                cells[5] = "exact locator checked"
                line = "| " + " | ".join(cells) + " |"
        rows.append(line)
    return "\n".join(rows)


def completed_response(spec: intake.ReviewSpec) -> str:
    path = REVIEW_DIR / spec.template_name
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        "Status: blank response template. This file is not a review and grants no approval.",
        "Status: completed synthetic contract-test response.",
    )
    text = set_blank_field(text, "Reviewer", "Contract Test Reviewer")
    text = set_blank_field(text, "Review date", "2026-06-12")
    text = set_blank_field(
        text,
        spec.expertise_key,
        "Long-form specialist expertise with direct primary-source access.",
    )
    text = set_blank_field(text, "Reviewed packet commit", intake.PACKET_COMMIT)

    for item_id in spec.item_ids:
        if item_id == "TLH-07":
            text = replace_section(text, item_id, fill_ledger)
            continue

        def transform(section_text: str) -> str:
            section_text = set_blank_field(
                section_text,
                "Decision",
                "INSUFFICIENT EVIDENCE",
            )
            return fill_blank_labels(section_text)

        text = replace_section(text, item_id, transform)

    def fill_overall(section_text: str) -> str:
        section_text = set_blank_field(
            section_text,
            "Complete title candidate",
            "INSUFFICIENT EVIDENCE",
        )
        section_text = set_blank_field(
            section_text,
            "Opening proposition architecture",
            "INSUFFICIENT EVIDENCE",
        )
        section_text = set_blank_field(
            section_text,
            "Blocking findings",
            "Primary or canonical evidence remains insufficient for production approval.",
        )
        section_text = set_blank_field(
            section_text,
            "Reviewer signature/name",
            "Contract Test Reviewer",
        )
        return section_text

    text = replace_section(text, spec.overall_heading, fill_overall)
    return text


class ExternalSpecialistTemplateContractTests(unittest.TestCase):
    def test_every_template_item_has_a_parser_compatible_decision_field(self) -> None:
        for spec in intake.SPECS:
            template = (REVIEW_DIR / spec.template_name).read_text(encoding="utf-8")
            for item_id in spec.item_ids:
                if item_id == "TLH-07":
                    continue
                with self.subTest(language=spec.lang, item=item_id):
                    item = intake.section(template, item_id)
                    self.assertIn("Decision:", item)

    def test_completed_templates_pass_structure_and_substance_validation(self) -> None:
        for spec in intake.SPECS:
            with self.subTest(language=spec.lang):
                response = completed_response(spec)
                structure_errors, structure_details = intake.validate_response(spec, response)
                substance_errors, substance_details = substance.validate_response(spec, response)
                if structure_errors or substance_errors:
                    diagnostic = {
                        "language": spec.lang,
                        "structure_errors": structure_errors,
                        "structure_details": structure_details,
                        "substance_errors": substance_errors,
                        "substance_details": substance_details,
                    }
                    self.fail(json.dumps(diagnostic, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    unittest.main()
