#!/usr/bin/env python3
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports/localization/constructed-language-audit"
PLACEHOLDER_POLICY = ROOT / "localization/policies/intentional-placeholders.json"
REMEDIATION_POLICY = ROOT / "localization/terminology/constructed-language-remediation-policy.json"
REVIEW_PROGRESS = ROOT / "localization/reviews/between-potential-and-ideal/review-progress.json"
TERMS = {
    "tlh": "frequency nature processor provisional domains theorem metaphysical nihilism fidelity theory testimony statistics optimization precision mirror logic safety protocol conditioning metamorphosis harmony framework representation calculation evidence context identity".split(),
    "qya": "capítulo saída salida metafísica usuario frequency nature genius optimization safety protocol conditioning metamorphosis harmony channel code synchronization framework representation evidence context".split(),
}


def metadata(text, key):
    match = re.search(rf"^{re.escape(key)}:\s*(.+?)\s*$", text, flags=re.M)
    return match.group(1) if match else ""


def translated_lines(text):
    """Return translated-prose lines while preserving original line numbers."""
    lines = text.splitlines()
    start = 0
    if lines and lines[0].strip() == "---":
        for index in range(1, len(lines)):
            if lines[index].strip() == "---":
                start = index + 1
                break

    result = []
    gate_pattern = re.compile(r"^## (?:Segment|Placeholder) review gate\b")
    image_only = re.compile(r"^!\[[^\n]*\]\([^\n]*\)\s*$")
    for index in range(start, len(lines)):
        raw = lines[index]
        if gate_pattern.match(raw):
            break
        if image_only.match(raw.strip()):
            continue
        cleaned = re.sub(r"`[^`]*`", "", raw)
        cleaned = re.sub(r"\]\([^)]*\)", "]", cleaned)
        result.append((index + 1, raw, cleaned))
    return result


def occurrence_section(raw_line):
    return "heading" if raw_line.lstrip().startswith("#") else "body"


def term_occurrences(lines, terms):
    occurrences = []
    for term in terms:
        pattern = re.compile(rf"(?<![\w'-]){re.escape(term)}(?![\w'-])", flags=re.I)
        for line_number, raw, cleaned in lines:
            if pattern.search(cleaned):
                occurrences.append({
                    "term": term,
                    "line": line_number,
                    "section": occurrence_section(raw),
                    "excerpt": raw.strip()[:240],
                })
    return sorted(occurrences, key=lambda item: (item["line"], item["term"]))


def prose_block_count(lines):
    text = "\n".join(cleaned for _, _, cleaned in lines).strip()
    return len([block for block in re.split(r"\n\s*\n", text) if block.strip()])


def scan(path, lang, placeholder, protected_terms):
    text = path.read_text(encoding="utf-8", errors="ignore")
    lines = translated_lines(text)
    expected_status = "placeholder-draft" if placeholder else "draft"
    expected_gate = "## Placeholder review gate" if placeholder else "## Segment review gate"

    occurrences = [] if placeholder else term_occurrences(lines, TERMS[lang])
    protected_occurrences = [] if placeholder else term_occurrences(lines, protected_terms)
    suspicious_terms = sorted({item["term"] for item in occurrences})
    body_terms = sorted({item["term"] for item in occurrences if item["section"] == "body"})
    heading_terms = sorted({item["term"] for item in occurrences if item["section"] == "heading"})

    return {
        "path": str(path.relative_to(ROOT)),
        "status": metadata(text, "status"),
        "status_ok": metadata(text, "status") == expected_status,
        "publication_forbidden": metadata(text, "publication") == "forbidden",
        "gate_ok": expected_gate in text,
        "blocks": prose_block_count(lines),
        "suspicious_terms": suspicious_terms,
        "suspicious_body_terms": body_terms,
        "suspicious_heading_terms": heading_terms,
        "suspicious_occurrences": occurrences,
        "protected_term_occurrences": protected_occurrences,
        "intentional_placeholder": placeholder,
    }


def render_occurrence_details(rows):
    lines = [
        "",
        "## Foreign-term occurrences",
        "",
        "Heading-only findings still require an explicit title or proper-name policy; they are not silently cleared.",
        "",
        "| Segment | Language | Term | Line | Section | Excerpt |",
        "|---:|---|---|---:|---|---|",
    ]
    found = False
    for row in rows:
        for lang in ("tlh", "qya"):
            item = row.get(lang)
            if not item:
                continue
            for occurrence in item["suspicious_occurrences"]:
                found = True
                excerpt = occurrence["excerpt"].replace("|", "\\|")
                lines.append(
                    f"| {row['segment']} | {lang} | `{occurrence['term']}` | "
                    f"{occurrence['line']} | {occurrence['section']} | {excerpt} |"
                )
    if not found:
        lines.append("| — | — | — | — | — | No suspicious terms found |")
    return lines


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    placeholder_policy = json.loads(PLACEHOLDER_POLICY.read_text(encoding="utf-8"))
    remediation_policy = json.loads(REMEDIATION_POLICY.read_text(encoding="utf-8")) if REMEDIATION_POLICY.exists() else {}
    placeholders = {f"{int(item['segment']):03d}" for item in placeholder_policy["segments"]}
    protected_terms = remediation_policy.get("protected_project_terms", [])
    roots = {lang: ROOT / "localization/sources" / lang / "between-potential-and-ideal" for lang in ("tlh", "qya")}
    files = {lang: {path.name[:3]: path for path in root.glob("*.md")} for lang, root in roots.items()}
    rows = []
    for segment in sorted(set(files["tlh"]) | set(files["qya"])):
        blockers = []
        pair = {"segment": segment, "intentional_placeholder": segment in placeholders}
        for lang in ("tlh", "qya"):
            path = files[lang].get(segment)
            if not path:
                blockers.append(f"{lang}:missing")
                continue
            item = scan(path, lang, segment in placeholders, protected_terms)
            pair[lang] = item
            if not item["status_ok"]:
                blockers.append(f"{lang}:status")
            if not item["publication_forbidden"]:
                blockers.append(f"{lang}:publication")
            if not item["gate_ok"]:
                blockers.append(f"{lang}:gate")
            if item["suspicious_terms"]:
                blockers.append(f"{lang}:foreign-terms")
        if "tlh" in pair and "qya" in pair and not pair["intentional_placeholder"]:
            if abs(pair["tlh"]["blocks"] - pair["qya"]["blocks"]) > 4:
                blockers.append("structure")
        pair["automated_blockers"] = blockers
        pair["automated_status"] = "blocked" if blockers else "clear"
        rows.append(pair)

    progress = json.loads(REVIEW_PROGRESS.read_text(encoding="utf-8")) if REVIEW_PROGRESS.exists() else {}
    blocked = sum(bool(row["automated_blockers"]) for row in rows)
    occurrence_count = sum(
        len(row.get(lang, {}).get("suspicious_occurrences", []))
        for row in rows
        for lang in ("tlh", "qya")
    )
    body_occurrence_count = sum(
        1
        for row in rows
        for lang in ("tlh", "qya")
        for item in row.get(lang, {}).get("suspicious_occurrences", [])
        if item["section"] == "body"
    )
    heading_occurrence_count = occurrence_count - body_occurrence_count
    result = {
        "schema_version": 3,
        "pairs": len(rows),
        "automated_blocked": blocked,
        "automated_clear": len(rows) - blocked,
        "foreign_term_occurrences": occurrence_count,
        "foreign_term_body_occurrences": body_occurrence_count,
        "foreign_term_heading_occurrences": heading_occurrence_count,
        "specialist_first_pass_complete": int(progress.get("first_pass_complete_pairs", 0)),
        "specialist_approved": int(progress.get("approved_pairs", 0)),
        "publication_approved": False,
        "note": "Automated clearance never replaces specialist linguistic approval.",
        "items": rows,
    }
    (OUT / "audit.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Paired constructed-language audit",
        "",
        f"Pairs: {result['pairs']}",
        f"Automated blocked: {result['automated_blocked']}",
        f"Automated clear: {result['automated_clear']}",
        f"Foreign-term occurrences: {result['foreign_term_occurrences']}",
        f"Body occurrences: {result['foreign_term_body_occurrences']}",
        f"Heading occurrences: {result['foreign_term_heading_occurrences']}",
        f"First-pass complete: {result['specialist_first_pass_complete']}",
        f"Specialist approved: {result['specialist_approved']}",
        "",
        "| Segment | Automated status | Blockers |",
        "|---:|---|---|",
    ]
    lines += [
        f"| {row['segment']} | {row['automated_status']} | {', '.join(row['automated_blockers']) or 'none'} |"
        for row in rows
    ]
    lines += render_occurrence_details(rows)
    (OUT / "audit.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({key: result[key] for key in (
        "pairs",
        "automated_blocked",
        "automated_clear",
        "foreign_term_occurrences",
        "specialist_first_pass_complete",
        "specialist_approved",
    )}))


if __name__ == "__main__":
    main()
