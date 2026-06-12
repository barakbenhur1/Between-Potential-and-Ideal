#!/usr/bin/env python3
"""Regression tests for the standalone external-review preflight command."""

from __future__ import annotations

import io
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import preflight_external_specialist_review as preflight  # noqa: E402
import validate_external_specialist_reviews as intake  # noqa: E402
from test_external_specialist_review_templates import completed_response  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
REVIEW_DIR = ROOT / "localization/reviews/between-potential-and-ideal"


class ExternalSpecialistPreflightTests(unittest.TestCase):
    def test_complete_synthetic_responses_pass_for_both_languages(self) -> None:
        for spec in intake.SPECS:
            with self.subTest(language=spec.lang):
                result = preflight.validate_text(spec.lang, completed_response(spec))
                self.assertTrue(result["valid_for_submission"], result["errors"])
                self.assertFalse(result["approval_granted"])
                self.assertFalse(result["publication_allowed"])
                self.assertEqual(spec.response_name, result["expected_submission_name"])

    def test_blank_templates_fail_for_both_languages(self) -> None:
        for spec in intake.SPECS:
            with self.subTest(language=spec.lang):
                text = (REVIEW_DIR / spec.template_name).read_text(encoding="utf-8")
                result = preflight.validate_text(spec.lang, text)
                self.assertFalse(result["valid_for_submission"])
                self.assertTrue(any("blank template" in error for error in result["errors"]))

    def test_cli_json_report_matches_validation_result(self) -> None:
        spec = preflight.review_spec("qya")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "review.md"
            path.write_text(completed_response(spec), encoding="utf-8")
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = preflight.main(
                    ["--language", "qya", "--response", str(path), "--json"]
                )
        self.assertEqual(0, exit_code)
        self.assertIn('"valid_for_submission": true', stdout.getvalue())
        self.assertIn(intake.PACKET_COMMIT, stdout.getvalue())

    def test_cli_missing_file_returns_usage_error_code(self) -> None:
        stderr = io.StringIO()
        with redirect_stderr(stderr):
            exit_code = preflight.main(
                ["--language", "tlh", "--response", "/definitely/missing/review.md"]
            )
        self.assertEqual(2, exit_code)
        self.assertIn("response file not found", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
