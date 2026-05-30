import ast
import sys
from pathlib import Path

GUARD = Path("tools/audit_release_guard.py")
DOC = Path("docs/tool-inventory.md")

def release_guard_scripts():
    tree = ast.parse(GUARD.read_text(encoding="utf-8", errors="ignore"))
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "CHECKS":
                    checks = ast.literal_eval(node.value)
                    return [item[1] for item in checks if isinstance(item, list) and len(item) == 2]
    return []

def main() -> int:
    errors = []

    if not GUARD.exists():
        errors.append("missing tools/audit_release_guard.py")

    if not DOC.exists():
        errors.append("missing docs/tool-inventory.md")
        doc_text = ""
    else:
        doc_text = DOC.read_text(encoding="utf-8", errors="ignore")

    if GUARD.exists():
        scripts = release_guard_scripts()
        if not scripts:
            errors.append("no scripts found in release guard CHECKS")
        for script in scripts:
            if script not in doc_text:
                errors.append(f"release guard script missing from docs/tool-inventory.md: {script}")

    required_phrases = [
        "Temporary `fix_*.py` scripts must not be listed here",
        "If a permanent tool is added to `tools/audit_release_guard.py`, it must also be listed in this file.",
        "tools/check_live_deploy_urls.py",
        "tools/update_build_info.py",
    ]

    for phrase in required_phrases:
        if phrase not in doc_text:
            errors.append(f"docs/tool-inventory.md missing phrase: {phrase}")

    if errors:
        print("FAIL: tool inventory audit found issues")
        for error in errors:
            print("-", error)
        return 1

    print("OK: tool inventory covers release guard checks.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
