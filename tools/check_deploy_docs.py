from pathlib import Path
import sys

REQUIRED = [
    Path("docs/deploy.md"),
    Path("tools/check_live_deploy_urls.py"),
]

def main() -> int:
    errors = []

    for path in REQUIRED:
        if not path.exists():
            errors.append(f"missing {path}")

    deploy = Path("docs/deploy.md")
    if deploy.exists():
        text = deploy.read_text(encoding="utf-8", errors="ignore")
        required_phrases = [
            "https://between-potential-and-ideal.onrender.com",
            "python3 tools/audit_release_guard.py",
            "python3 tools/check_live_deploy_urls.py",
            "Do not force-push main.",
        ]
        for phrase in required_phrases:
            if phrase not in text:
                errors.append(f"docs/deploy.md missing phrase: {phrase}")

    if errors:
        print("FAIL: deploy docs audit found issues")
        for error in errors:
            print("-", error)
        return 1

    print("OK: deploy docs baseline passed.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
