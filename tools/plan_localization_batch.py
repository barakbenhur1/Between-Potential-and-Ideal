#!/usr/bin/env python3
from __future__ import annotations

from difflib import SequenceMatcher
from pathlib import Path
import hashlib
import json
import os
import re

ROOT = Path(__file__).resolve().parents[1]
JOBS_DIR = ROOT / "reports" / "localization" / "ai-jobs"
CACHE_DIR = ROOT / "localization" / "translation-cache"
RECOVERED_DIR = ROOT / "reports" / "localization" / "recovered"
BATCH_SIZE = 32
MODEL = "openai/gpt-4.1"
TARGETS = {
    "tlh": (
        "Klingon (tlhIngan Hol), using canonical Marc Okrand grammar and attested vocabulary. "
        "Use transparent Klingon descriptive phrases when no attested one-word term exists. "
        "Do not leave English prose except protected names, titles, citations, URLs, and the term AI."
    ),
    "qya": (
        "Neo-Quenya, using one internally consistent Tolkienian Neo-Quenya grammar and morphology profile. "
        "Use transparent descriptive phrases for modern concepts. Do not leave English, Spanish, or Portuguese "
        "prose except protected names, titles, citations, URLs, and the term AI."
    ),
}


def clean(text: str) -> str:
    text = text.replace("\r\n", "\n").strip()
    text = re.sub(r"^```(?:markdown|md|text)?\s*", "", text, flags=re.I)
    return re.sub(r"\s*```$", "", text).strip()


def valid(source: str, translated: str) -> bool:
    lowered = translated.lower()
    refused = any(
        marker in lowered
        for marker in (
            "i can't assist",
            "i cannot assist",
            "as an ai language model",
            "cannot translate",
        )
    )
    similarity = SequenceMatcher(None, source[:6000], translated[:6000]).ratio()
    return (
        len(translated) >= max(200, int(len(source) * 0.45))
        and translated != source
        and similarity < 0.65
        and not refused
    )


def cache_recovered(job_id: str, data: dict, source_hash: str) -> bool:
    if not RECOVERED_DIR.exists():
        return False
    candidates = list(RECOVERED_DIR.rglob(f"{job_id}.json")) + list(
        RECOVERED_DIR.rglob(f"{job_id}.txt")
    )
    for candidate in candidates:
        translated = clean(candidate.read_text(encoding="utf-8", errors="ignore"))
        if not valid(data["source"], translated):
            continue
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
                    "origin": "recovered",
                    "review_status": "machine-assisted-experimental",
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        return True
    return False


def main() -> int:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    jobs: list[tuple[Path, dict, bool]] = []
    for path in sorted(JOBS_DIR.glob("translate-*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        job_id = data["job_id"]
        source_hash = hashlib.sha256(data["source"].encode()).hexdigest()
        body = CACHE_DIR / f"{job_id}.md"
        meta = CACHE_DIR / f"{job_id}.json"
        cached = False
        if body.is_file() and meta.is_file():
            try:
                info = json.loads(meta.read_text(encoding="utf-8"))
                cached = info.get("source_sha256") == source_hash and valid(
                    data["source"], clean(body.read_text(encoding="utf-8"))
                )
            except Exception:
                cached = False
        if not cached:
            cached = cache_recovered(job_id, data, source_hash)
        jobs.append((path, data, cached))

    pending = [(path, data) for path, data, cached in jobs if not cached]
    batch = pending[:BATCH_SIZE]
    include = [
        {
            "id": data["job_id"],
            "input": path.name,
            "language_mode": TARGETS[data["language"]],
            "model": MODEL,
        }
        for path, data in batch
    ]
    (JOBS_DIR / "matrix.json").write_text(
        json.dumps({"include": include}) + "\n", encoding="utf-8"
    )
    (JOBS_DIR / "all-jobs.json").write_text(
        json.dumps([data for _, data, _ in jobs], ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    status = {
        "total": len(jobs),
        "cached": len(jobs) - len(pending),
        "pending": len(pending),
        "batch": len(batch),
        "model": MODEL,
    }
    (JOBS_DIR / "status.json").write_text(
        json.dumps(status, indent=2) + "\n", encoding="utf-8"
    )
    if output_path := os.environ.get("GITHUB_OUTPUT"):
        with open(output_path, "a", encoding="utf-8") as output:
            output.write(
                "matrix="
                + json.dumps({"include": include}, separators=(",", ":"))
                + "\n"
            )
            output.write(f"batch={len(batch)}\n")
            output.write(f"pending={len(pending)}\n")
    print(json.dumps(status))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
