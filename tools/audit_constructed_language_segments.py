#!/usr/bin/env python3
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports/localization/constructed-language-audit"
PLACEHOLDER_POLICY = ROOT / "localization/policies/intentional-placeholders.json"
REVIEW_PROGRESS = ROOT / "localization/reviews/between-potential-and-ideal/review-progress.json"
TERMS = {
    "tlh": "frequency nature processor provisional domains theorem metaphysical nihilism fidelity theory testimony statistics optimization precision mirror logic safety protocol conditioning metamorphosis harmony framework representation calculation evidence context identity".split(),
    "qya": "capítulo saída salida metafísica usuario frequency nature genius optimization safety protocol conditioning metamorphosis harmony channel code synchronization framework representation evidence context".split(),
}


def translated_prose(text):
    if text.startswith("---"):
        parts = text.split("---", 2)
        text = parts[2] if len(parts) == 3 else text
    text = re.split(r"\n## (?:Segment|Placeholder) review gate\b", text, maxsplit=1)[0]
    text = re.sub(r"^!\[[^\n]*\]\([^\n]*\)\s*$", "", text, flags=re.M)
    text = re.sub(r"`[^`]*`", "", text)
    text = re.sub(r"\]\([^)]*\)", "]", text)
    return text.strip()


def metadata(text, key):
    match = re.search(rf"^{re.escape(key)}:\s*(.+?)\s*$", text, flags=re.M)
    return match.group(1) if match else ""


def scan(path, lang, placeholder):
    text = path.read_text(encoding="utf-8", errors="ignore")
    prose = translated_prose(text)
    low = prose.lower()
    expected_status = "placeholder-draft" if placeholder else "draft"
    expected_gate = "## Placeholder review gate" if placeholder else "## Segment review gate"
    return {
        "path": str(path.relative_to(ROOT)),
        "status": metadata(text, "status"),
        "status_ok": metadata(text, "status") == expected_status,
        "publication_forbidden": metadata(text, "publication") == "forbidden",
        "gate_ok": expected_gate in text,
        "blocks": len([x for x in re.split(r"\n\s*\n", prose) if x.strip()]),
        "suspicious_terms": [] if placeholder else [
            term for term in TERMS[lang]
            if re.search(rf"(?<![\w'-]){re.escape(term)}(?![\w'-])", low)
        ],
        "intentional_placeholder": placeholder,
    }


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    policy = json.loads(PLACEHOLDER_POLICY.read_text(encoding="utf-8"))
    placeholders = {f"{int(item['segment']):03d}" for item in policy["segments"]}
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
            item = scan(path, lang, segment in placeholders)
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
    result = {
        "schema_version": 2,
        "pairs": len(rows),
        "automated_blocked": blocked,
        "automated_clear": len(rows) - blocked,
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
        f"Specialist approved: {result['specialist_approved']}",
        "",
        "| Segment | Automated status | Blockers |",
        "|---:|---|---|",
    ]
    lines += [
        f"| {row['segment']} | {row['automated_status']} | {', '.join(row['automated_blockers']) or 'none'} |"
        for row in rows
    ]
    (OUT / "audit.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({key: result[key] for key in ("pairs", "automated_blocked", "automated_clear", "specialist_approved")}))


if __name__ == "__main__":
    main()
