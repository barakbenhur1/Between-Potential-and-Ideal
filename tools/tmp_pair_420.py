from pathlib import Path

updates = {
    "localization/sources/tlh/between-potential-and-ideal/420-economy-money-value-inflation.md": [
        ("metaphysical absolutes bIHbe'", "ngoD Qav bIHbe'"),
        ("classical quantity identity 'oH", "classical quantity rapghach 'oH"),
        ("identity 'oH; causal law nap 'oHbe'", "rapghach 'oH; causal law nap 'oHbe'"),
        ("Loss of Precision", "lughchu'ghach chIlghach"),
    ],
    "localization/sources/qya/between-potential-and-ideal/420-economy-money-value-inflation.md": [
        ("i genius moneyo", "i curu moneyo"),
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
