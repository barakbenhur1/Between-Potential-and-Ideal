#!/usr/bin/env python3
from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import hashlib
import json
import os
import re

ROOT = Path(__file__).resolve().parents[1]
JOBS_FILE = ROOT / "reports" / "localization" / "ai-jobs" / "all-jobs.json"
RESULTS_DIR = ROOT / "reports" / "localization" / "ai-results"
CACHE_DIR = ROOT / "localization" / "translation-cache"
STATE_FILE = ROOT / "localization" / "release-state.json"


def clean(text: str) -> str:
    text = text.replace("\r\n", "\n").strip()
    text = re.sub(r"^```(?:markdown|md|text)?\s*", "", text, flags=re.I)
    return re.sub(r"\s*```$", "", text).strip()


def valid(source: str, translated: str) -> bool:
    lowered = translated.lower()
    refusal_markers = (
        "i can't assist",
        "i cannot assist",
        "as an ai language model",
        "cannot translate",
    )
    return (
        len(translated) >= max(60, int(len(source) * 0.10))
        and translated != source
        and not any(marker in lowered for marker in refusal_markers)
    )


def cache_result(job_id: str, data: dict, translated: str, origin: str) -> None:
    source_hash = hashlib.sha256(data["source"].encode()).hexdigest()
    (CACHE_DIR / f"{job_id}.md").write_text(translated + "\n", encoding="utf-8")
    (CACHE_DIR / f"{job_id}.json").write_text(
        json.dumps(
            {
                "job_id": job_id,
                "package": data["package"],
                "language": data["language"],
                "chunk_index": data["chunk_index"],
                "chunk_count": data["chunk_count"],
                "source_sha256": source_hash,
                "origin": origin,
                "review_status": "machine-assisted-experimental",
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> int:
    jobs = {
        data["job_id"]: data
        for data in json.loads(JOBS_FILE.read_text(encoding="utf-8"))
    }
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    if RESULTS_DIR.exists():
        for path in RESULTS_DIR.glob("*.json"):
            data = jobs.get(path.stem)
            if not data:
                continue
            translated = clean(path.read_text(encoding="utf-8", errors="ignore"))
            if valid(data["source"], translated):
                cache_result(path.stem, data, translated, "current-batch")

    groups: dict[tuple[str, str], dict[int, str]] = defaultdict(dict)
    complete = 0

    for job_id, data in jobs.items():
        body = CACHE_DIR / f"{job_id}.md"
        meta = CACHE_DIR / f"{job_id}.json"
        if not body.is_file() or not meta.is_file():
            continue
        try:
            info = json.loads(meta.read_text(encoding="utf-8"))
            translated = clean(body.read_text(encoding="utf-8"))
        except Exception:
            continue
        source_hash = hashlib.sha256(data["source"].encode()).hexdigest()
        if info.get("source_sha256") != source_hash or not valid(
            data["source"], translated
        ):
            continue
        groups[(data["package"], data["language"])][data["chunk_index"]] = translated
        complete += 1

    for (package, language), chunks in groups.items():
        expected = next(
            data["chunk_count"]
            for data in jobs.values()
            if data["package"] == package and data["language"] == language
        )
        if sorted(chunks) != list(range(1, expected + 1)):
            continue
        body = "\n\n".join(chunks[index] for index in range(1, expected + 1)).strip()
        target = ROOT / "localization" / "sources" / language / f"{package}-{language}.md"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(
            "---\n"
            f"document_id: {package}\n"
            f"language: {language}\n"
            "status: release-candidate\n"
            "linguistic_review: machine-assisted-experimental\n"
            "publication: forbidden\n"
            "---\n\n"
            + body
            + "\n",
            encoding="utf-8",
        )

    pending = len(jobs) - complete
    state = {
        "total": len(jobs),
        "cached": complete,
        "pending": pending,
        "status": "translation-complete" if pending == 0 else "translation-in-progress",
    }
    STATE_FILE.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")

    output_path = os.environ.get("GITHUB_OUTPUT")
    if output_path:
        with open(output_path, "a", encoding="utf-8") as output:
            output.write(f"pending={pending}\n")
            output.write(f"cached={complete}\n")

    print(json.dumps(state))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
