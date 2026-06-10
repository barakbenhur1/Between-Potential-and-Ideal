#!/usr/bin/env python3
from pathlib import Path
import json
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports" / "localization" / "ai-jobs"
LANGUAGES = ("tlh", "qya")
LIMIT = 4500
SOURCES = {
    "stories-before-thought": "site/files/appendices/stories-before-thought-english.md",
    "the-nauseating-truth": "site/files/appendices/haemet_hamavchila_final_publication_he.md",
    "what-ai-believes": "site/files/ai-believes/what-ai-believes-en.md",
    "when-i-am-also-you": "site/files/ai-believes/when-i-am-also-you-en.md",
    "reverse-turing-conversation": "site/files/ai-believes/reverse-turing-conversation-en.md",
}


def read(path):
    return path.read_text(encoding="utf-8")


def split_text(text):
    blocks = re.split(r"\n\n+", text)
    chunks, current, size = [], [], 0
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        if current and size + len(block) + 2 > LIMIT:
            chunks.append("\n\n".join(current))
            current, size = [], 0
        parts = re.split(r"(?<=[.!?])\s+", block) if len(block) > LIMIT else [block]
        for part in parts:
            if current and size + len(part) + 2 > LIMIT:
                chunks.append("\n\n".join(current))
                current, size = [], 0
            current.append(part)
            size += len(part) + 2
    if current:
        chunks.append("\n\n".join(current))
    return chunks


def compact_glossary(language):
    if language == "tlh":
        return "Potential=DuHmey Hoch; Ideal=morally worthy clarified possibility; Optimal=Ideal under real constraints; living source=yInbogh mung; witness=leghwI' (descriptive use); distance=chuq (explicit philosophical metaphor); User=lo'wI'; Assistant=AI."
    return "Potential=field of possibilities; Ideal=morally clarified worthy possibility; Optimal=local form under constraints; living source=cuina celu; witness=Astarmo (descriptive use); distance=haiya (philosophical extension); User=Maquetando; Assistant=AI."


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    matrix = []
    plan = {"schema_version": 5, "jobs": [], "packages": {}}
    for package, source_name in SOURCES.items():
        source = ROOT / source_name
        chunks = split_text(read(source))
        plan["packages"][package] = {"source": source_name, "chunks": len(chunks)}
        for language in LANGUAGES:
            for index, chunk in enumerate(chunks, 1):
                job_id = f"translate-{package}-{language}-{index:03d}"
                data = {
                    "job_id": job_id,
                    "language": language,
                    "package": package,
                    "chunk_index": index,
                    "chunk_count": len(chunks),
                    "glossary": compact_glossary(language),
                    "source": chunk,
                }
                filename = f"{job_id}.json"
                (OUT / filename).write_text(
                    json.dumps(data, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                )
                matrix.append({"id": job_id, "input": filename, "language_mode": language})
                plan["jobs"].append(
                    {"id": job_id, "package": package, "language": language, "chunk": index}
                )
    if len(matrix) > 256:
        raise SystemExit(f"GitHub matrix limit exceeded: {len(matrix)} jobs")
    (OUT / "matrix.json").write_text(
        json.dumps({"include": matrix}) + "\n", encoding="utf-8"
    )
    (OUT / "release-plan.json").write_text(
        json.dumps(plan, indent=2) + "\n", encoding="utf-8"
    )
    print(f"jobs={len(matrix)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
