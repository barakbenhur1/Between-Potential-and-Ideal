#!/usr/bin/env python3
from pathlib import Path
from collections import defaultdict
import json, re

ROOT = Path(__file__).resolve().parents[1]
JOBS = ROOT / "reports/localization/ai-jobs"
RESULTS = ROOT / "reports/localization/ai-results"
LANGUAGES = {"tlh", "qya"}


def clean(text):
    text = text.strip()
    text = re.sub(r"^```(?:markdown)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def main():
    plan = json.loads((JOBS / "release-plan.json").read_text(encoding="utf-8"))
    jobs = {item["id"]: item for item in plan["jobs"]}
    chunks = defaultdict(dict)
    seen = set()
    for result_path in sorted(RESULTS.glob("*.json")):
        job_id = result_path.stem
        if job_id not in jobs:
            raise SystemExit(f"Unexpected job: {job_id}")
        item = jobs[job_id]
        language = item["language"]
        if language not in LANGUAGES:
            raise SystemExit(f"Unexpected language: {language}")
        key = (item["package"], language)
        chunks[key][int(item["chunk"])] = clean(result_path.read_text(encoding="utf-8"))
        seen.add(job_id)
    missing = sorted(set(jobs) - seen)
    if missing:
        raise SystemExit(f"Missing jobs: {missing}")
    written = 0
    for (package, language), values in sorted(chunks.items()):
        expected = int(plan["packages"][package]["chunks"])
        if sorted(values) != list(range(1, expected + 1)):
            raise SystemExit(f"Incomplete chunks: {package} {language}")
        body = "\n\n".join(values[index] for index in range(1, expected + 1)).strip()
        header = (
            "---\n"
            f"document_id: {package}\n"
            f"language: {language}\n"
            "status: release-candidate\n"
            "linguistic_review: machine-assisted-structured-translation\n"
            "publication: forbidden\n"
            "---\n\n"
        )
        target = ROOT / "localization" / "sources" / language / f"{package}-{language}.md"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(header + body + "\n", encoding="utf-8")
        written += 1
    print(f"written={written}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
