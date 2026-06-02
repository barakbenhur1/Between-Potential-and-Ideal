from pathlib import Path
import sys

DOC = Path("docs/contributor-guardrails.md")
README = Path("README.md")


def main() -> int:
    errors = []

    if not DOC.exists():
        errors.append("missing docs/contributor-guardrails.md")
        text = ""
    else:
        text = DOC.read_text(encoding="utf-8", errors="ignore")

    required = [
        "Make the smallest measurable change.",
        "python3 tools/final_release_qa.py --scan",
        "git diff --check",
        "git status --short",
        "tools/audit_release_guard.py",
        "Do not return the appendix to 14 stories.",
        "ואז... הוא 🥱",
        "Do not present AI as conscious.",
        "Do not force-push `main`.",
        "Do not perform CSS cleanup before the visual QA baseline is reviewed.",
        "Final release QA passes.",
    ]

    for phrase in required:
        if phrase not in text:
            errors.append(f"guardrails missing phrase: {phrase}")

    if not README.exists():
        errors.append("missing README.md")
    else:
        readme = README.read_text(encoding="utf-8", errors="ignore")
        if "docs/contributor-guardrails.md" not in readme:
            errors.append("README missing contributor guardrails link")

    if errors:
        print("FAIL: contributor guardrails audit found issues")
        for error in errors:
            print("-", error)
        return 1

    print("OK: contributor guardrails docs passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
