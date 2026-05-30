from pathlib import Path
import datetime
import json
import subprocess

OUT = Path("site/build-info.json")

def run(cmd):
    try:
        return subprocess.check_output(cmd, text=True).strip()
    except Exception:
        return "unknown"

def main():
    data = {
        "project": "Between Potential and Ideal",
        "branch": run(["git", "rev-parse", "--abbrev-ref", "HEAD"]),
        "commit": run(["git", "rev-parse", "HEAD"]),
        "short_commit": run(["git", "rev-parse", "--short", "HEAD"]),
        "generated_at_utc": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
        "source": "tools/update_build_info.py"
    }
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote", OUT)

if __name__ == "__main__":
    main()
