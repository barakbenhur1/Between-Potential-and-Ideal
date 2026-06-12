from pathlib import Path

MARKER = "\n## Segment review gate"


def update(path_string: str, replacements: list[tuple[str, str]]) -> None:
    path = Path(path_string)
    text = path.read_text(encoding="utf-8")
    if "linguistic_review:" not in text:
        text = text.replace(
            "status: draft\n",
            "status: draft\nlinguistic_review: specialist-revision-active\n",
            1,
        )
    body, gate = text.split(MARKER, 1)
    for old, new in replacements:
        if old not in body:
            raise RuntimeError(f"missing expected text in {path_string}: {old!r}")
        body = body.replace(old, new)
    path.write_text(body + MARKER + gate, encoding="utf-8")


update(
    "localization/sources/tlh/between-potential-and-ideal/430-economy-market-credit-labor-externality.md",
    [
        ("mirror", "mIllogh"),
        ("testimony", "yInDaj bopbogh QIch"),
    ],
)
update(
    "localization/sources/qya/between-potential-and-ideal/430-economy-market-credit-labor-externality.md",
    [],
)
update(
    "localization/sources/tlh/between-potential-and-ideal/440-economy-inequality-crisis-repair.md",
    [
        ("wealth time, safety, education", "wealth time, QobHa'ghach, education"),
        ("market mirror ratlhtaH'a'?", "market mIllogh ratlhtaH'a'?"),
        ("theory economic law nI'", "QubmeH mIw economic law nI'"),
    ],
)
update(
    "localization/sources/qya/between-potential-and-ideal/440-economy-inequality-crisis-repair.md",
    [("Wealth polë buy time, safety, education", "Wealth polë buy time, varnassë, education")],
)
update(
    "localization/sources/tlh/between-potential-and-ideal/450-governance-law-legitimacy-elections.md",
    [
        ("State of nature", "chut Hutlhbogh ghu'"),
        ("state of nature", "chut Hutlhbogh ghu'"),
        ("identities", "ghaH'egh pongmey"),
    ],
)
update(
    "localization/sources/qya/between-potential-and-ideal/450-governance-law-legitimacy-elections.md",
    [
        ("State of Nature", "I ghuo ú law"),
        ("State of nature", "I ghuo ú law"),
        ("state of nature", "i ghuo ú law"),
    ],
)
