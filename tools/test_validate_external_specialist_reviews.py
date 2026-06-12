#!/usr/bin/env python3
"""Regression tests for external specialist review intake state handling."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate_external_specialist_reviews as intake  # noqa: E402


class ExternalSpecialistReviewIntakeTests(unittest.TestCase):
    def test_valid_response_can_await_maintainer_status_sync(self) -> None:
        state, valid, errors = intake.reconcile_status(True, False)
        self.assertEqual("valid-awaiting-status-sync", state)
        self.assertTrue(valid)
        self.assertEqual([], errors)

    def test_valid_response_with_synced_status_is_complete(self) -> None:
        state, valid, errors = intake.reconcile_status(True, True)
        self.assertEqual("valid", state)
        self.assertTrue(valid)
        self.assertEqual([], errors)

    def test_status_cannot_claim_completion_for_invalid_response(self) -> None:
        state, valid, errors = intake.reconcile_status(False, True)
        self.assertEqual("invalid", state)
        self.assertFalse(valid)
        self.assertTrue(errors)

    def test_invalid_response_without_status_is_invalid(self) -> None:
        state, valid, errors = intake.reconcile_status(False, False)
        self.assertEqual("invalid", state)
        self.assertFalse(valid)
        self.assertEqual([], errors)


if __name__ == "__main__":
    unittest.main()
