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
            "python3 tools/final_release_qa.py --scan",
            "git diff --check",
        ]
        for phrase in required:
            if phrase not in text:
                errors.append(f"workflow missing phrase: {phrase}")

        # The detailed guard is now called by tools/final_release_qa.py, not directly
        # from the workflow. This avoids duplicating release-gate behavior while keeping
        # a single canonical CI entry point.
        final_qa = Path("tools/final_release_qa.py")
        if not final_qa.exists():
            errors.append("missing tools/final_release_qa.py")
        else:
            final_qa_text = final_qa.read_text(encoding="utf-8", errors="ignore")
            if "tools/audit_release_guard.py" not in final_qa_text:
                errors.append("tools/final_release_qa.py does not wrap tools/audit_release_guard.py")

    if errors:
        print("FAIL: CI workflow audit found issues")
        for error in errors:
            print("-", error)
        return 1

    print("OK: CI workflow baseline passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
