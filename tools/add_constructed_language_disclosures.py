#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
NOTES = {
    "tlh": "tlhIngan Hol mughghach ghantoH 'oH. De'wI' jan boQ lo'lu'pu'; mughwI' po' DIchmoHghach pagh Star Trek mughghach chut 'oHbe'.",
    "qya": "Neo-Quenya quentalë tyaliëo ná. Mahtalë masina-yanwëo carna sa; lá ná quentalë Tolkienwa hya lambengolmo tulcaina quentalë.",
}
STYLE = "<style>.edition-disclosure{max-width:900px;margin:0 auto 22px;padding:12px 16px;border:1px solid #72d8d055;border-radius:14px;background:#0b2022;color:#c8f3ef;font-size:.88rem;line-height:1.5}</style>"


def patch(path: Path, language: str) -> None:
    text = path.read_text(encoding="utf-8")
    if 'name="translation-profile"' not in text:
        text = text.replace("</head>", '<meta name="translation-profile" content="experimental-machine-assisted-constructed-language-edition">' + STYLE + "</head>")
    if "edition-disclosure" not in text.split("<body", 1)[-1]:
        note = f'<aside class="edition-disclosure" role="note">{NOTES[language]}</aside>'
        if "<main" in text:
            start = text.find(">", text.find("<main")) + 1
            text = text[:start] + note + text[start:]
        else:
            start = text.find(">", text.find("<body")) + 1
            text = text[:start] + note + text[start:]
    path.write_text(text, encoding="utf-8")


def main() -> int:
    for language in NOTES:
        candidates = [SITE / f"{language}.html"]
        candidates.extend((SITE / "pages" / language).glob("*.html"))
        candidates.extend((SITE / "files" / language).glob("*.html"))
        for path in candidates:
            if path.is_file():
                patch(path, language)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
