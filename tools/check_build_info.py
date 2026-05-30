from pathlib import Path
import json
import re
import sys

P = Path("site/build-info.json")

def main() -> int:
    errors = []

    if not P.exists():
        errors.append("missing site/build-info.json")
    else:
        try:
            data = json.loads(P.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"site/build-info.json is invalid JSON: {exc}")
            data = {}

        for key in ["project", "branch", "commit", "short_commit", "generated_at_utc", "source"]:
            if not data.get(key):
                errors.append(f"build-info missing key: {key}")

        commit = data.get("commit", "")
        if commit != "unknown" and not re.fullmatch(r"[0-9a-f]{40}", commit):
            errors.append("build-info commit is not a full git sha")

        short_commit = data.get("short_commit", "")
        if short_commit != "unknown" and not re.fullmatch(r"[0-9a-f]{7,12}", short_commit):
            errors.append("build-info short_commit is not a short git sha")

    if errors:
        print("FAIL: build-info audit found issues")
        for error in errors:
            print("-", error)
        return 1

    print("OK: build-info baseline passed.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
