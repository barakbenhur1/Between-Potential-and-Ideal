import ast
import subprocess
import sys
from pathlib import Path

P = Path("tools/audit_release_guard.py")

BOOTSTRAP_PREFIX = [
    ["python3", "tools/check_no_root_junk_files.py"],
    ["python3", "tools/check_tool_inventory.py"],
    ["python3", "tools/check_release_guard_integrity.py"],
]

def main() -> int:
    errors = []

    if not P.exists():
        print("FAIL: missing tools/audit_release_guard.py")
        return 1

    text = P.read_text(encoding="utf-8", errors="ignore")
    tree = ast.parse(text)

    checks = None
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "CHECKS":
                    checks = ast.literal_eval(node.value)

    if checks is None:
        errors.append("CHECKS list not found")
    elif not isinstance(checks, list):
        errors.append("CHECKS is not a list")
    else:
        if checks[:len(BOOTSTRAP_PREFIX)] != BOOTSTRAP_PREFIX:
            errors.append(f"CHECKS must start with bootstrap prefix: {BOOTSTRAP_PREFIX}")

        seen = set()
        for item in checks:
            if not isinstance(item, list) or len(item) != 2:
                errors.append(f"bad CHECKS item shape: {item}")
                continue

            exe, script = item
            if exe != "python3":
                errors.append(f"CHECKS item must use python3: {item}")

            if not isinstance(script, str) or not script.startswith("tools/") or not script.endswith(".py"):
                errors.append(f"CHECKS script must be tools/*.py: {item}")
                continue

            if script in seen:
                errors.append(f"duplicate CHECKS script: {script}")
            seen.add(script)

            if "/fix_" in script or script.startswith("tools/fix_"):
                errors.append(f"fix script must not be in release guard: {script}")

            path = Path(script)
            if not path.exists():
                errors.append(f"CHECKS script missing on disk: {script}")
                continue

            result = subprocess.run(["python3", "-m", "py_compile", script], capture_output=True, text=True)
            if result.returncode != 0:
                errors.append(f"CHECKS script does not compile: {script}\n{result.stderr}")

    if errors:
        print("FAIL: release guard integrity audit found issues")
        for error in errors:
            print("-", error)
        return 1

    print("OK: release guard integrity passed.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
