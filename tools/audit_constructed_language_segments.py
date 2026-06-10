#!/usr/bin/env python3
from pathlib import Path
import json, re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports/localization/constructed-language-audit"
TERMS = {
    "tlh": "frequency nature processor provisional domains theorem metaphysical nihilism fidelity theory testimony statistics optimization precision mirror logic safety protocol conditioning metamorphosis harmony framework representation calculation evidence context identity".split(),
    "qya": "capítulo saída salida metafísica usuario frequency nature genius potential optimization safety protocol conditioning metamorphosis harmony channel code synchronization framework representation evidence context".split(),
}


def scan(path, lang):
    text = path.read_text(encoding="utf-8", errors="ignore")
    low = text.lower()
    return {
        "path": str(path.relative_to(ROOT)),
        "draft": "status: draft" in text,
        "forbidden": "publication: forbidden" in text,
        "gate": "## Segment review gate" in text,
        "blocks": len([x for x in re.split(r"\n\s*\n", text) if x.strip()]),
        "terms": [x for x in TERMS[lang] if re.search(rf"(?<![\w'-]){re.escape(x)}(?![\w'-])", low)],
    }


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    roots = {x: ROOT / "localization/sources" / x / "between-potential-and-ideal" for x in ("tlh", "qya")}
    tlh = {p.name[:3]: p for p in roots["tlh"].glob("*.md")}
    qya = {p.name[:3]: p for p in roots["qya"].glob("*.md")}
    rows = []
    for seg in sorted(set(tlh) | set(qya)):
        blockers = []
        pair = {"segment": seg}
        for lang, files in (("tlh", tlh), ("qya", qya)):
            if seg not in files:
                blockers.append(f"{lang}:missing")
                continue
            item = scan(files[seg], lang)
            pair[lang] = item
            if not item["draft"]: blockers.append(f"{lang}:status")
            if not item["forbidden"]: blockers.append(f"{lang}:publication")
            if not item["gate"]: blockers.append(f"{lang}:gate")
            if item["terms"]: blockers.append(f"{lang}:foreign-terms")
        if "tlh" in pair and "qya" in pair and abs(pair["tlh"]["blocks"] - pair["qya"]["blocks"]) > 4:
            blockers.append("structure")
        pair["blockers"] = blockers
        pair["status"] = "review-required" if blockers else "automated-clear"
        rows.append(pair)
    result = {"pairs": len(rows), "review_required": sum(bool(x["blockers"]) for x in rows), "approval": False, "items": rows}
    (OUT / "audit.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["# Paired constructed-language audit", "", f"Pairs: {result['pairs']}", f"Review required: {result['review_required']}", "", "| Segment | Status | Blockers |", "|---:|---|---|"]
    lines += [f"| {x['segment']} | {x['status']} | {', '.join(x['blockers']) or 'none'} |" for x in rows]
    (OUT / "audit.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"pairs": result["pairs"], "review_required": result["review_required"]}))


if __name__ == "__main__":
    main()
