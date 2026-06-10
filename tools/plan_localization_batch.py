#!/usr/bin/env python3
from __future__ import annotations

from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path
import hashlib
import json
import os
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
JOBS_DIR = ROOT / "reports" / "localization" / "ai-jobs"
CACHE_DIR = ROOT / "localization" / "translation-cache"
CACHE_SCHEMA = "constructed-languages-1500-v3"
BATCH_SIZE = 4
MODELS = ("openai/gpt-4.1", "openai/gpt-4.1-mini")
TARGETS = {
    "tlh": (
        "Klingon (tlhIngan Hol), using canonical Marc Okrand grammar and attested vocabulary. "
        "Use transparent Klingon descriptive phrases when no attested one-word term exists. "
        "Do not leave English prose except protected names, titles, citations, URLs, and AI."
    ),
    "qya": (
        "Neo-Quenya, using one internally consistent Tolkienian Neo-Quenya grammar and morphology profile. "
        "Use transparent descriptive phrases for modern concepts. Do not leave English, Spanish, or Portuguese "
        "prose except protected names, titles, citations, URLs, and AI."
    ),
}


def clean(text: str) -> str:
    text = text.replace("\r\n", "\n").strip()
    text = re.sub(r"^```(?:markdown|md|text)?\s*", "", text, flags=re.I)
    return re.sub(r"\s*```$", "", text).strip()


def valid(source: str, translated: str) -> bool:
    lowered = translated.lower()
    if any(
        marker in lowered
        for marker in (
            "i can't assist",
            "i cannot assist",
            "as an ai language model",
            "cannot translate",
            "capítulo",
            "usuario:",
            "saída",
        )
    ):
        return False
    if translated == source or not (0.45 <= len(translated) / max(1, len(source)) <= 3.0):
        return False
    if SequenceMatcher(None, source[:4000], translated[:4000]).ratio() >= 0.65:
        return False
    words = re.findall(r"[\w'’-]+", lowered, flags=re.UNICODE)
    if len(words) < 25:
        return False
    counts = Counter(words)
    if counts.most_common(1)[0][1] / len(words) > 0.18:
        return False
    if re.search(r"\b([\w'’-]+)(?:\s+\1){7,}\b", lowered, flags=re.UNICODE):
        return False
    if len(set(words)) / len(words) < 0.08:
        return False
    source_blocks = len([part for part in re.split(r"\n\s*\n", source) if part.strip()])
    target_blocks = len([part for part in re.split(r"\n\s*\n", translated) if part.strip()])
    return target_blocks >= max(1, source_blocks // 2)


def ensure_cache_schema() -> None:
    marker = CACHE_DIR / ".schema"
    current = marker.read_text(encoding="utf-8").strip() if marker.is_file() else ""
    if current != CACHE_SCHEMA:
        shutil.rmtree(CACHE_DIR, ignore_errors=True)
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        marker.write_text(CACHE_SCHEMA + "\n", encoding="utf-8")


def main() -> int:
    ensure_cache_schema()
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
        jobs.append((path, data, cached))

    pending = [(path, data) for path, data, cached in jobs if not cached]
    batch = pending[:BATCH_SIZE]
    include = []
    for index, (path, data) in enumerate(batch):
        include.append(
            {
                "id": data["job_id"],
                "input": path.name,
                "language_mode": TARGETS[data["language"]],
                "model": MODELS[index % len(MODELS)],
            }
        )
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
        "models": list(MODELS),
        "cache_schema": CACHE_SCHEMA,
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
