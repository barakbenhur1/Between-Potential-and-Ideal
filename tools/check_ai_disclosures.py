from pathlib import Path
import re
import sys

AI_DIR = Path("site/files/ai-believes")

def is_ai_dialogue(path: Path) -> bool:
    if not path.exists() or path.suffix.lower() != ".html":
        return False
    if path.name.startswith("."):
        return False
    return True

def main() -> int:
    errors = []

    if not AI_DIR.exists():
        print("SKIP: no AI dialogue directory found:", AI_DIR)
        return 0

    files = sorted(p for p in AI_DIR.rglob("*.html") if is_ai_dialogue(p))

    if not files:
        print("SKIP: no AI dialogue HTML files found")
        return 0

    for path in files:
        html = path.read_text(encoding="utf-8", errors="ignore")

        if 'class="ai-disclosure"' not in html and "class='ai-disclosure'" not in html:
            errors.append(f"{path}: missing ai-disclosure block")
            continue

        text = re.sub(r"<[^>]+>", " ", html)
        text = re.sub(r"\s+", " ", text).strip().lower()

        required_any = [
            "not evidence that ai is conscious",
            "not evidence of consciousness",
            "אינה הוכחה לכך שבינה מלאכותית מודעת",
            "אינו הוכחה לכך שבינה מלאכותית מודעת",
            "לא הוכחה לתודעה",
        ]

        if not any(x.lower() in text for x in required_any):
            errors.append(f"{path}: ai-disclosure exists but missing consciousness/evidence disclaimer")

    if errors:
        print("FAIL: AI disclosure audit found issues")
        for e in errors:
            print("-", e)
        return 1

    print(f"OK: AI disclosure audit passed. checked={len(files)}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
