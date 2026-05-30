from pathlib import Path
import sys

P = Path("docs/visual-qa.md")

def main() -> int:
    errors = []
    if not P.exists():
        errors.append("missing docs/visual-qa.md")
    else:
        text = P.read_text(encoding="utf-8", errors="ignore")
        required = [
            "Do not perform CSS cleanup",
            "390px wide",
            "768px wide",
            "1440px wide",
            "/files/appendices/stories-before-thought-hebrew-rtl.html",
            "/files/appendices/stories-before-thought-english.html",
            "AI disclosure blocks",
            "Do not commit screenshots by default.",
            "Only after this baseline may CSS consolidation be considered.",
        ]
        for phrase in required:
            if phrase not in text:
                errors.append(f"docs/visual-qa.md missing phrase: {phrase}")

    if errors:
        print("FAIL: visual QA docs audit found issues")
        for error in errors:
            print("-", error)
        return 1

    print("OK: visual QA baseline docs passed.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
