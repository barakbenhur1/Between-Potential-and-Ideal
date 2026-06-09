#!/usr/bin/env python3
from __future__ import annotations

from argparse import ArgumentParser
from collections import Counter
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
LANGUAGES = ("tlh", "qya")
SEGMENT_RE = re.compile(r"^(\d+)-.+\.md$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
REVIEW_GATE_RE = re.compile(r"^##\s+(?:Segment|Placeholder) review gate\s*$", re.MULTILINE)
CONTROL_HEADINGS = {
    "tlh": "## mIw qawmoHghach — Translation control note",
    "qya": "## Enyalë Léo — Translation control note",
}
REQUIRED_FINAL_MARKERS = (
    "## Sources, Inspirations, Ideas, and Acknowledgements",
    "### Bibliography and Source Notes",
    "Back to table of contents",
)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_front_matter(path: Path) -> tuple[dict[str, str], str | None]:
    if not path.is_file():
        return {}, "missing file"
    text = path.read_text(encoding="utf-8", errors="strict")
    if not text.startswith("---\n"):
        return {}, "missing front matter"
    parts = text.split("---\n", 2)
    if len(parts) != 3:
        return {}, "malformed front matter"
    meta: dict[str, str] = {}
    for line in parts[1].splitlines():
        key, sep, value = line.partition(":")
        if sep:
            meta[key.strip()] = value.strip()
    return meta, None


def file_hash(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def heading_counts(text: str) -> dict[str, int]:
    counts = Counter(len(match.group(1)) for match in HEADING_RE.finditer(text))
    return {f"h{level}": counts.get(level, 0) for level in range(1, 7)}


def inspect_assembly(path: Path, language: str) -> tuple[dict[str, object], list[str]]:
    errors: list[str] = []
    metrics: dict[str, object] = {
        "path": rel(path),
        "exists": path.is_file(),
    }
    if not path.is_file():
        errors.append(f"missing assembled draft: {rel(path)}")
        return metrics, errors

    text = path.read_text(encoding="utf-8", errors="strict")
    control_heading = CONTROL_HEADINGS[language]
    review_gate_count = len(REVIEW_GATE_RE.findall(text))
    control_note_count = text.count(control_heading)
    marker_presence = {marker: marker in text for marker in REQUIRED_FINAL_MARKERS}
    metrics.update(
        {
            "bytes": path.stat().st_size,
            "lines": len(text.splitlines()),
            "sha256": file_hash(path),
            "headings": heading_counts(text),
            "review_gate_count": review_gate_count,
            "translation_control_note_count": control_note_count,
            "required_final_markers": marker_presence,
        }
    )

    if control_note_count != 1:
        errors.append(f"{rel(path)}: expected exactly one translation control note, found {control_note_count}")
    for marker, present in marker_presence.items():
        if not present:
            errors.append(f"{rel(path)}: missing final marker: {marker}")
    if marker_presence["Back to table of contents"] and control_note_count == 1:
        if text.rfind("Back to table of contents") > text.rfind(control_heading):
            errors.append(f"{rel(path)}: translation control note is not the final control section")
    return metrics, errors


def audit_language(contract: dict, language: str) -> dict:
    errors: list[str] = []
    blockers: list[str] = []
    segment_paths = [ROOT / item for item in contract.get("source_segments", {}).get(language, [])]
    segment_numbers: list[int] = []
    statuses: Counter[str] = Counter()
    publication_values: Counter[str] = Counter()

    for path in segment_paths:
        if not path.is_file():
            errors.append(f"missing canonical segment: {rel(path)}")
            continue
        match = SEGMENT_RE.match(path.name)
        if not match:
            errors.append(f"segment filename has no numeric prefix: {rel(path)}")
        else:
            segment_numbers.append(int(match.group(1)))
        meta, problem = read_front_matter(path)
        if problem:
            errors.append(f"{rel(path)}: {problem}")
            continue
        statuses[meta.get("status", "missing")] += 1
        publication_values[meta.get("publication", "missing")] += 1
        if meta.get("language") != language:
            errors.append(f"language mismatch: {rel(path)}")
        if meta.get("document_id") != contract.get("document_id"):
            errors.append(f"document_id mismatch: {rel(path)}")
        if meta.get("publication") != "forbidden":
            errors.append(f"publication lock missing: {rel(path)}")

    if len(segment_paths) != len(set(segment_paths)):
        errors.append("duplicate canonical segment paths")
    if segment_numbers != sorted(segment_numbers):
        errors.append("canonical segments are not numerically ordered")

    base_path = ROOT / contract["canonical_targets"][language]
    base_meta, base_problem = read_front_matter(base_path)
    if base_problem:
        errors.append(f"{rel(base_path)}: {base_problem}")
    elif base_meta.get("language") != language:
        errors.append(f"canonical base language mismatch: {rel(base_path)}")

    review_path = ROOT / contract["draft_assembly_outputs"][language]
    clean_path = (
        ROOT
        / "reports"
        / "localization"
        / "assembled-clean"
        / language
        / f"{contract['document_id']}-{language}.md"
    )
    review_metrics, review_errors = inspect_assembly(review_path, language)
    clean_metrics, clean_errors = inspect_assembly(clean_path, language)
    errors.extend(review_errors)
    errors.extend(clean_errors)

    review_gate_count = int(review_metrics.get("review_gate_count", -1))
    clean_gate_count = int(clean_metrics.get("review_gate_count", -1))
    if review_metrics.get("exists") and review_gate_count != len(segment_paths):
        errors.append(
            f"review assembly should contain one review-control section per segment: "
            f"expected {len(segment_paths)}, found {review_gate_count}"
        )
    if clean_metrics.get("exists") and clean_gate_count != 0:
        errors.append(f"clean assembly still contains {clean_gate_count} review-control sections")
    if review_metrics.get("exists") and clean_metrics.get("exists"):
        if int(clean_metrics.get("bytes", 0)) >= int(review_metrics.get("bytes", 0)):
            errors.append("clean assembly is not smaller than review assembly")

    nonapproved = sum(count for status, count in statuses.items() if status != "approved")
    placeholder_drafts = statuses.get("placeholder-draft", 0)
    if base_meta.get("status") != "approved":
        blockers.append(f"canonical base status={base_meta.get('status', 'missing')}")
    if nonapproved:
        blockers.append(f"{nonapproved} canonical segments are not approved")
    if placeholder_drafts:
        blockers.append(f"{placeholder_drafts} placeholder segments remain placeholder-draft")

    return {
        "language": language,
        "canonical_base": rel(base_path),
        "canonical_base_status": base_meta.get("status", "missing"),
        "segment_count": len(segment_paths),
        "segment_number_range": [min(segment_numbers), max(segment_numbers)] if segment_numbers else [],
        "segment_statuses": dict(sorted(statuses.items())),
        "publication_values": dict(sorted(publication_values.items())),
        "review_assembled_draft": review_metrics,
        "clean_assembled_preview": clean_metrics,
        "review_control_removal_verified": (
            review_metrics.get("exists")
            and clean_metrics.get("exists")
            and review_gate_count == len(segment_paths)
            and clean_gate_count == 0
        ),
        "structural_errors": errors,
        "publication_blockers": blockers,
    }


def render_assembly_metrics(lines: list[str], label: str, assembled: dict) -> None:
    lines.extend(
        [
            f"### {label}",
            "",
            f"- Output: `{assembled['path']}`",
            f"- Exists: `{assembled['exists']}`",
        ]
    )
    if assembled.get("exists"):
        lines.extend(
            [
                f"- Bytes: `{assembled.get('bytes')}`",
                f"- Lines: `{assembled.get('lines')}`",
                f"- SHA-256: `{assembled.get('sha256')}`",
                f"- Headings: `{json.dumps(assembled.get('headings'), sort_keys=True)}`",
                f"- Review-control sections: `{assembled.get('review_gate_count')}`",
                f"- Translation control notes: `{assembled.get('translation_control_note_count')}`",
            ]
        )
    lines.append("")


def render_markdown(result: dict) -> str:
    lines = [
        "# Localized Assembly and Parity Audit",
        "",
        f"- Document: `{result['document_id']}`",
        f"- Source commit: `{result['source_commit']}`",
        f"- Generated: `{result['generated_at']}`",
        f"- Assembly status: **{result['assembly_status']}**",
        f"- Clean preview status: **{result['clean_preview_status']}**",
        f"- Cross-language structural parity: **{result['cross_language_structural_parity']}**",
        f"- Publication readiness: **{result['publication_readiness']}**",
        "",
    ]
    for language in result["languages"]:
        lines.extend(
            [
                f"## {language['language']}",
                "",
                f"- Canonical segments: **{language['segment_count']}**",
                f"- Base status: `{language['canonical_base_status']}`",
                f"- Segment statuses: `{json.dumps(language['segment_statuses'], ensure_ascii=False, sort_keys=True)}`",
                f"- Review-control removal verified: `{language['review_control_removal_verified']}`",
                "",
            ]
        )
        render_assembly_metrics(lines, "Review assembly", language["review_assembled_draft"])
        render_assembly_metrics(lines, "Clean non-public preview", language["clean_assembled_preview"])
        if language["structural_errors"]:
            lines.append("### Structural errors")
            lines.extend(f"- {item}" for item in language["structural_errors"])
            lines.append("")
        if language["publication_blockers"]:
            lines.append("### Publication blockers")
            lines.extend(f"- {item}" for item in language["publication_blockers"])
            lines.append("")
    lines.extend(
        [
            "## Decision",
            "",
            result["decision"],
            "",
            "No public output was generated by this audit.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = ArgumentParser(description="Audit review and clean non-public localization assemblies.")
    parser.add_argument("document_id")
    parser.add_argument("--json-output", type=Path)
    parser.add_argument("--markdown-output", type=Path)
    parser.add_argument("--source-commit", default="unknown")
    args = parser.parse_args()

    contract_path = ROOT / "localization" / "documents" / f"{args.document_id}.json"
    if not contract_path.is_file():
        raise SystemExit(f"Missing localized document contract: {contract_path}")
    contract = json.loads(contract_path.read_text(encoding="utf-8"))

    languages = [audit_language(contract, language) for language in LANGUAGES]
    structural_errors = [
        f"{language['language']}: {item}"
        for language in languages
        for item in language["structural_errors"]
    ]
    publication_blockers = [
        f"{language['language']}: {item}"
        for language in languages
        for item in language["publication_blockers"]
    ]

    segment_counts = {language["segment_count"] for language in languages}
    if len(segment_counts) != 1:
        structural_errors.append("language segment counts do not match")

    review_heading_profiles = {
        json.dumps(language["review_assembled_draft"].get("headings", {}), sort_keys=True)
        for language in languages
    }
    clean_heading_profiles = {
        json.dumps(language["clean_assembled_preview"].get("headings", {}), sort_keys=True)
        for language in languages
    }
    if len(review_heading_profiles) != 1:
        structural_errors.append("review assembly heading profiles do not match across languages")
    if len(clean_heading_profiles) != 1:
        structural_errors.append("clean assembly heading profiles do not match across languages")

    control_removal_verified = all(language["review_control_removal_verified"] for language in languages)
    if not control_removal_verified:
        structural_errors.append("review-control removal was not verified for both languages")

    assembly_status = "FAIL" if structural_errors else "PASS"
    clean_preview_status = "FAIL" if structural_errors or not control_removal_verified else "PASS"
    cross_language_structural_parity = (
        "PASS"
        if not structural_errors and len(segment_counts) == 1 and len(review_heading_profiles) == 1 and len(clean_heading_profiles) == 1
        else "FAIL"
    )
    publication_readiness = "BLOCKED" if structural_errors or publication_blockers else "READY"

    if structural_errors:
        decision = "Assembly failed structural validation. Correct the listed errors before review continues."
    elif publication_blockers:
        decision = (
            "Review and clean non-public drafts assembled successfully, review-control removal is verified, "
            "and cross-language structural parity passed. Publication remains blocked only by source approval "
            "and unresolved placeholder chapters."
        )
    else:
        decision = "The assembled drafts passed structural and publication-readiness checks."

    result = {
        "schema_version": 2,
        "document_id": contract.get("document_id"),
        "source_commit": args.source_commit,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "assembly_status": assembly_status,
        "clean_preview_status": clean_preview_status,
        "cross_language_structural_parity": cross_language_structural_parity,
        "publication_readiness": publication_readiness,
        "segment_count_per_language": next(iter(segment_counts)) if len(segment_counts) == 1 else None,
        "review_control_removal_verified": control_removal_verified,
        "languages": languages,
        "structural_errors": structural_errors,
        "publication_blockers": publication_blockers,
        "decision": decision,
        "public_output_generated": False,
    }

    json_output = args.json_output or (
        ROOT / "localization" / "audits" / f"{args.document_id}-assembly-parity.json"
    )
    markdown_output = args.markdown_output or json_output.with_suffix(".md")
    json_output = json_output if json_output.is_absolute() else ROOT / json_output
    markdown_output = markdown_output if markdown_output.is_absolute() else ROOT / markdown_output
    json_output.parent.mkdir(parents=True, exist_ok=True)
    markdown_output.parent.mkdir(parents=True, exist_ok=True)
    json_output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    markdown_output.write_text(render_markdown(result), encoding="utf-8")

    print(f"assembly_status={assembly_status}")
    print(f"clean_preview_status={clean_preview_status}")
    print(f"cross_language_structural_parity={cross_language_structural_parity}")
    print(f"publication_readiness={publication_readiness}")
    print(f"segment_count_per_language={result['segment_count_per_language']}")
    print(f"review_control_removal_verified={control_removal_verified}")
    print(f"structural_errors={len(structural_errors)}")
    print(f"publication_blockers={len(publication_blockers)}")
    print(f"json={rel(json_output)}")
    print(f"markdown={rel(markdown_output)}")
    return 1 if structural_errors else 0


if __name__ == "__main__":
    sys.exit(main())
