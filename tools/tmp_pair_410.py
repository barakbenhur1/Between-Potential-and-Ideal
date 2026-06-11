from pathlib import Path

needle = "safe" + "ty"

updates = {
    "localization/sources/tlh/between-potential-and-ideal/410-engineering-maintenance-failure-repair.md": [
        ("noise, " + needle + ", chance je", "noise, QobHa'ghach, chance je"),
        (needle + " factor lIjbe'lu'pu'bogh", "QobHom polmeH ratio lIjbe'lu'pu'bogh"),
    ],
    "localization/sources/qya/between-potential-and-ideal/410-engineering-maintenance-failure-repair.md": [
        ("noise, " + needle + " ar chance", "noise, varnassë ar chance"),
        ("only " + needle + " factor ya lá was forgotten", "only ratio ya hehta room erroren ar ya lá was forgotten"),
    ],
}

for filename, replacements in updates.items():
    path = Path(filename)
    text = path.read_text(encoding="utf-8")
    if "linguistic_review:" not in text:
        text = text.replace("status: draft\n", "status: draft\nlinguistic_review: specialist-revision-active\n", 1)
    for old, new in replacements:
        if old not in text:
            raise RuntimeError(f"missing expected text in {filename}: {old!r}")
        text = text.replace(old, new, 1)
    path.write_text(text, encoding="utf-8")
