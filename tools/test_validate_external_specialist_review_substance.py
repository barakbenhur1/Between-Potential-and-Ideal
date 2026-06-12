#!/usr/bin/env python3
"""Focused regression tests for specialist-review substance validation."""

from __future__ import annotations

import sys
import unittest
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate_external_specialist_review_substance as substance  # noqa: E402


class SpecialistReviewSubstanceTests(unittest.TestCase):
    def test_placeholders_are_not_substantive(self) -> None:
        for value in ("", "TBD", "todo", "N/A", "...", "placeholder"):
            with self.subTest(value=value):
                self.assertFalse(substance.substantive(value))
        self.assertTrue(substance.substantive("PE17/77, lines 3-5"))

    def test_field_or_block_accepts_multiline_evidence(self) -> None:
        text = "Exact lexical sources:\n\nPE17/77, lines 3-5\n\nFull parse: next"
        self.assertEqual(
            "PE17/77, lines 3-5",
            substance.field_or_block(text, "Exact lexical sources"),
        )

    def test_signature_must_match_reviewer(self) -> None:
        self.assertTrue(substance.names_match("Dr. Jane Smith", "Jane Smith"))
        self.assertFalse(substance.names_match("Jane Smith", "John Smith"))

    def test_review_date_rejects_invalid_and_future_values(self) -> None:
        self.assertIsNotNone(substance.validate_review_date("2026-02-31"))
        future = (date.today() + timedelta(days=1)).isoformat()
        self.assertIsNotNone(substance.validate_review_date(future))
        self.assertIsNone(substance.validate_review_date(date.today().isoformat()))

    def test_insufficient_evidence_requires_documented_search_and_risk(self) -> None:
        empty_errors = substance.validate_item(
            "QYA-01",
            "Exact lexical sources: TBD\nAlternative or dangerous readings: TBD\n",
            "INSUFFICIENT EVIDENCE",
        )
        self.assertGreaterEqual(len(empty_errors), 2)

        documented_errors = substance.validate_item(
            "QYA-01",
            "Exact lexical sources: Checked PE17 and VT49; no primary attestation found.\n"
            "Alternative or dangerous readings: The unverified form could imply location rather than relation.\n",
            "INSUFFICIENT EVIDENCE",
        )
        self.assertEqual([], documented_errors)

    def test_reject_requires_full_auditable_analysis(self) -> None:
        incomplete = substance.validate_item(
            "TLH-01",
            "Exact canonical lexical sources: TKD p. 1\nAlternative or dangerous readings: ambiguous head\n",
            "REJECT",
        )
        self.assertTrue(any("complete parse" in error for error in incomplete))
        self.assertTrue(any("literal back-translation" in error for error in incomplete))

        complete = substance.validate_item(
            "TLH-01",
            "Exact canonical lexical sources: TKD p. 1\n"
            "Exact grammar sources: TKD section 6.2.3\n"
            "Word-by-word and suffix parse: choH-bogh modifies mIw; Prime Intellect is object.\n"
            "Literal back-translation: process which changes Prime Intellect\n"
            "Alternative or dangerous readings: noun-head scope remains ambiguous in isolation.\n",
            "REJECT",
        )
        self.assertEqual([], complete)

    def test_source_ledger_rejects_placeholder_locators(self) -> None:
        rows = [
            f"| form{i} | meaning | TBD | ... | unknown | note |"
            for i in range(14)
        ]
        errors = substance.validate_source_ledger("\n".join(rows))
        self.assertGreaterEqual(len(errors), 14)


if __name__ == "__main__":
    unittest.main()
