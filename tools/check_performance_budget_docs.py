from pathlib import Path
import sys

P = Path("docs/performance-budget.md")


def main() -> int:
    errors = []
    if not P.exists():
        errors.append("missing docs/performance-budget.md")
    else:
        text = P.read_text(encoding="utf-8", errors="ignore")
        required = [
            "Do not delete, compress, replace, rename, or move images",
            "Do not perform CSS cleanup before the visual QA baseline",
            "Do not replace existing story or chapter images unless explicitly requested.",
            "Do not remove CSS only because it looks duplicated.",
            "CSS consolidation is allowed only after visual QA baseline and final release QA pass.",
            "Run final release QA.",
            "Preserve HTML, PDF, DOCX, MD, and TXT variants unless explicitly told otherwise.",
            "No optimization commit may remove files unless explicitly approved.",
            "Performance work must be measurable and reversible.",
        ]
        for phrase in required:
            if phrase not in text:
                errors.append(f"docs/performance-budget.md missing phrase: {phrase}")

    if errors:
        print("FAIL: performance budget docs audit found issues")
        for error in errors:
            print("-", error)
        return 1

    print("OK: performance budget docs passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
