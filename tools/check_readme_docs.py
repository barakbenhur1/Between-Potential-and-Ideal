from pathlib import Path
import sys

P = Path("README.md")


def main() -> int:
    errors = []
    if not P.exists():
        errors.append("missing README.md")
        text = ""
    else:
        text = P.read_text(encoding="utf-8", errors="ignore")

    required_phrases = [
        "https://between-potential-and-ideal.onrender.com",
        ".github/workflows/",
        "docs/",
        "tools/",
        "site/",
        "python3 tools/final_release_qa.py --scan",
        "git diff --check",
        "git status --short",
        "docs/contributor-guardrails.md",
        "docs/deploy.md",
        "docs/qa-index.md",
        "docs/tool-inventory.md",
        "docs/production-next-phase-status.md",
        "docs/visual-qa.md",
        "docs/performance-budget.md",
    ]

    for phrase in required_phrases:
        if phrase not in text:
            errors.append(f"README.md missing phrase: {phrase}")

    if errors:
        print("FAIL: README docs audit found issues")
        for error in errors:
            print("-", error)
        return 1

    print("OK: README docs baseline passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
