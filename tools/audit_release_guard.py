import subprocess
import sys

CHECKS = [
    ["python3", "tools/audit_story_appendices_16.py"],
    ["python3", "tools/check_story_registry.py"],
    ["python3", "tools/audit_images_exist.py"],
    ["python3", "tools/audit_anchors.py"],
    ["python3", "tools/audit_visible_hebrew_in_english.py"],
    ["python3", "tools/check_files_language_labels.py"],
    ["python3", "tools/check_files_table_accessibility.py"],
]

def run(cmd):
    print("\n==>", " ".join(cmd))
    result = subprocess.run(cmd)
    if result.returncode != 0:
        raise SystemExit(result.returncode)

def main():
    for cmd in CHECKS:
        run(cmd)
    print("\nOK: release guard passed.")

if __name__ == "__main__":
    main()
