#!/usr/bin/env python3
from pathlib import Path
import json, re

ROOT = Path(__file__).resolve().parents[1]
JOBS = ROOT / "reports/localization/ai-jobs"
RESULTS = ROOT / "reports/localization/ai-results"


def clean(text):
    text = text.strip()
    text = re.sub(r"^```(?:markdown)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return text.rstrip() + "\n"


def main():
    plan = json.loads((JOBS / "release-plan.json").read_text(encoding="utf-8"))
    jobs = {item["id"]: item["paths"][0] for item in plan["jobs"]}
    seen = set()
    for result_path in sorted(RESULTS.glob("*.json")):
        job_id = result_path.stem
        if job_id not in jobs:
            raise SystemExit(f"Unexpected job: {job_id}")
        target = ROOT / jobs[job_id]
        target.write_text(clean(result_path.read_text(encoding="utf-8")), encoding="utf-8")
        seen.add(job_id)
    missing = sorted(set(jobs) - seen)
    if missing:
        raise SystemExit(f"Missing jobs: {missing}")
    print(f"written={len(seen)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
