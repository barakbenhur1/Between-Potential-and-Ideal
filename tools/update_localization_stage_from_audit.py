#!/usr/bin/env python3
from __future__ import annotations

from argparse import ArgumentParser
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
LANGUAGES = ("tlh", "qya")
NEXT_STAGE = "linguistic review and placeholder publication decision"
CONTRACT_STATUS = "assembled-structural-parity-pass"
BATCH_TARGET_STATUS = "translation-assembled-review-pending"


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_compact_json(path: Path, data: dict) -> None:
    path.write_text(
        json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = ArgumentParser(description="Synchronize localization stage metadata from a verified assembly audit.")
    parser.add_argument("audit", type=Path)
    parser.add_argument("--contract", type=Path, default=Path("localization/documents/between-potential-and-ideal.json"))
    parser.add_argument("--batch", type=Path, default=Path("localization/batches/batch-1.json"))
    args = parser.parse_args()

    audit_path = args.audit if args.audit.is_absolute() else ROOT / args.audit
    contract_path = args.contract if args.contract.is_absolute() else ROOT / args.contract
    batch_path = args.batch if args.batch.is_absolute() else ROOT / args.batch

    audit = read_json(audit_path)
    required = {
        "assembly_status": "PASS",
        "clean_preview_status": "PASS",
        "cross_language_structural_parity": "PASS",
        "review_control_removal_verified": True,
        "public_output_generated": False,
    }
    failures = [
        f"{key}: expected {expected!r}, got {audit.get(key)!r}"
        for key, expected in required.items()
        if audit.get(key) != expected
    ]
    if failures:
        print("Refusing to advance localization stage because audit prerequisites failed:")
        for failure in failures:
            print("-", failure)
        return 1

    audit_rel = relative(audit_path)
    audit_summary = {
        "path": audit_rel,
        "source_commit": audit.get("source_commit"),
        "assembly_status": audit.get("assembly_status"),
        "clean_preview_status": audit.get("clean_preview_status"),
        "cross_language_structural_parity": audit.get("cross_language_structural_parity"),
        "publication_readiness": audit.get("publication_readiness"),
        "segment_count_per_language": audit.get("segment_count_per_language"),
        "review_control_removal_verified": audit.get("review_control_removal_verified"),
    }

    contract = read_json(contract_path)
    contract["latest_assembly_audit"] = audit_summary
    for language in LANGUAGES:
        progress = contract.setdefault("current_progress", {}).setdefault(language, {})
        progress["status"] = CONTRACT_STATUS
        progress["next"] = NEXT_STAGE
        progress["assembly_audit"] = audit_rel
        progress["publication_readiness"] = audit.get("publication_readiness", "BLOCKED").lower()
    write_compact_json(contract_path, contract)

    batch = read_json(batch_path)
    batch["latest_assembly_audit"] = audit_summary
    for language in LANGUAGES:
        target = batch.setdefault("targets", {}).setdefault(language, {})
        target["status"] = BATCH_TARGET_STATUS
        document = target.setdefault("documents", {}).setdefault("between-potential-and-ideal", {})
        document["status"] = CONTRACT_STATUS
        document["next"] = NEXT_STAGE
        document["assembly_audit"] = audit_rel
        document["public"] = False
    write_compact_json(batch_path, batch)

    print(f"contract={relative(contract_path)}")
    print(f"batch={relative(batch_path)}")
    print(f"status={CONTRACT_STATUS}")
    print(f"next={NEXT_STAGE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
