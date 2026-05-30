from pathlib import Path
import sys

WORKFLOW = Path(".github/workflows/release-guard.yml")

def main() -> int:
    errors = []

    if not WORKFLOW.exists():
        errors.append("missing .github/workflows/release-guard.yml")
    else:
        text = WORKFLOW.read_text(encoding="utf-8", errors="ignore")
        required = [
            "Release Guard",
            "actions/checkout@v4",
            "actions/setup-python@v5",
            "python3 tools/audit_release_guard.py",
            "git diff --check",
        ]
        for phrase in required:
            if phrase not in text:
                errors.append(f"workflow missing phrase: {phrase}")

    if errors:
        print("FAIL: CI workflow audit found issues")
        for error in errors:
            print("-", error)
        return 1

    print("OK: CI workflow baseline passed.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
