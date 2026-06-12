#!/usr/bin/env python3
"""Contract tests for the segment-020 external-review handoff documents."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEW_DIR = ROOT / "localization/reviews/between-potential-and-ideal"
PACKET_COMMIT = "fc1867f8e94bf588d8e3f2d9954207444a5083f8"

FILES = {
    "request_index": "020-external-review-request-index.md",
    "submission_guide": "020-external-review-submission-guide.md",
    "supplemental_index": "020-external-review-supplemental-evidence-index-r3.md",
    "qya_request": "020-external-qya-review-request.md",
    "qya_template": "020-external-qya-review-response-template-r2.md",
    "qya_exact_trace": "020-tamma-pusta-source-trace-r3.md",
    "qya_nonreplacement_trace": "020-nonreplacement-source-trace-r3.md",
    "tlh_request": "020-external-tlh-review-request.md",
    "tlh_template": "020-external-tlh-review-response-template-r2.md",
    "tlh_trace": "020-tlh-source-ledger-trace-r3.md",
    "packet": "020-external-specialist-review-packet-r2.md",
    "status": "020-specialist-status.json",
}


def read(name: str) -> str:
    return (REVIEW_DIR / FILES[name]).read_text(encoding="utf-8")


class ExternalReviewHandoffTests(unittest.TestCase):
    def test_all_handoff_files_exist(self) -> None:
        missing = [filename for filename in FILES.values() if not (REVIEW_DIR / filename).is_file()]
        self.assertEqual([], missing)

    def test_request_index_exposes_supplemental_evidence(self) -> None:
        text = read("request_index")
        self.assertIn(FILES["supplemental_index"], text)
        self.assertIn(PACKET_COMMIT, text)
        self.assertIn("pre-answer specialist decisions", text)
        self.assertIn("amend the packet", text)

    def test_qya_request_exposes_both_current_traces(self) -> None:
        text = read("qya_request")
        for key in ("packet", "qya_template", "supplemental_index", "qya_exact_trace", "qya_nonreplacement_trace"):
            with self.subTest(file=FILES[key]):
                self.assertIn(FILES[key], text)
        self.assertIn(PACKET_COMMIT, text)
        self.assertIn("must not be presented as direct Tolkien primary-source verification", text)

    def test_tlh_request_exposes_current_ledger(self) -> None:
        text = read("tlh_request")
        for key in ("packet", "tlh_template", "supplemental_index", "tlh_trace"):
            with self.subTest(file=FILES[key]):
                self.assertIn(FILES[key], text)
        self.assertIn(PACKET_COMMIT, text)
        self.assertIn("must not be presented as direct Okrand canonical verification", text)

    def test_supplemental_index_preserves_evidentiary_boundary(self) -> None:
        text = read("supplemental_index")
        for key in ("qya_exact_trace", "qya_nonreplacement_trace", "tlh_trace"):
            with self.subTest(file=FILES[key]):
                self.assertIn(FILES[key], text)
        self.assertIn(PACKET_COMMIT, text)
        self.assertIn("does not modify", text)
        self.assertIn("cannot by themselves satisfy", text)
        self.assertIn("valid-awaiting-status-sync", text)

    def test_status_and_handoff_use_same_packet_contract(self) -> None:
        status = json.loads(read("status"))
        packet = status["review_packet"]
        self.assertEqual(PACKET_COMMIT, packet["commit"])
        self.assertEqual(
            f"localization/reviews/between-potential-and-ideal/{FILES['packet']}",
            packet["packet"],
        )
        self.assertEqual(
            f"localization/reviews/between-potential-and-ideal/{FILES['qya_template']}",
            packet["qya_template"],
        )
        self.assertEqual(
            f"localization/reviews/between-potential-and-ideal/{FILES['tlh_template']}",
            packet["tlh_template"],
        )
        self.assertEqual(10, packet["qya_issue"])
        self.assertEqual(11, packet["tlh_issue"])


if __name__ == "__main__":
    unittest.main()
