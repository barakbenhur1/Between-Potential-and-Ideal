#!/usr/bin/env python3
from pathlib import Path
import json, shutil

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports/localization/ai-jobs"
CONTRACT = ROOT / "localization/documents/between-potential-and-ideal.json"
LANGUAGES = ("tlh", "qya")
GROUP_SIZE = 1


def read(path):
    return path.read_text(encoding="utf-8")


def rel(path):
    return path.relative_to(ROOT).as_posix()


def glossary(language):
    folder = ROOT / "localization/pages" / language
    names = ("glossary-stage-1.md", "glossary-stage-2.md", "potential-ideal-optimal-draft.md")
    return "\n\n".join(read(folder / name) for name in names if (folder / name).is_file())


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    contract = json.loads(read(CONTRACT))
    matrix, plan = [], {"jobs": []}
    for language in LANGUAGES:
        paths = [ROOT / contract["canonical_targets"][language]]
        paths += [ROOT / p for p in contract["source_segments"][language]]
        for start in range(0, len(paths), GROUP_SIZE):
            group = paths[start:start + GROUP_SIZE]
            job_id = f"repair-{language}-{start // GROUP_SIZE + 1:03d}"
            data = {
                "job_id": job_id,
                "language": language,
                "profile": "standard Klingon" if language == "tlh" else "consistent Neo-Quenya",
                "glossary": glossary(language),
                "items": [{"path": rel(p), "content": read(p)} for p in group],
            }
            name = f"{job_id}.json"
            (OUT / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            matrix.append({"id": job_id, "input": name, "language_mode": language})
            plan["jobs"].append({"id": job_id, "paths": [rel(p) for p in group]})
    (OUT / "matrix.json").write_text(json.dumps({"include": matrix}) + "\n", encoding="utf-8")
    (OUT / "release-plan.json").write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
    print(f"jobs={len(matrix)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
