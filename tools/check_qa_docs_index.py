from pathlib import Path
import sys

P = Path("docs/qa-index.md")

def main() -> int:
    errors = []
    if not P.exists():
        errors.append("missing docs/qa-index.md")
        text = ""
    else:
        text = P.read_text(encoding="utf-8", errors="ignore")

    required = [
        "python3 tools/audit_release_guard.py",
        "python3 tools/check_live_deploy_urls.py",
        "docs/contributor-guardrails.md",
        "docs/deploy.md",
        "docs/visual-qa.md",
        "docs/performance-budget.md",
        "Do not return the appendix to 14 stories.",
        "Do not force-push `main`.",
    ]

    for phrase in required:
        if phrase not in text:
            errors.append(f"docs/qa-index.md missing phrase: {phrase}")

    if errors:
        print("FAIL: QA docs index audit found issues")
        for error in errors:
            print("-", error)
        return 1

    print("OK: QA docs index passed.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
