from pathlib import Path
from html import unescape
import re

ROOT = Path.cwd()

FILES = [
    ROOT / "site/files/appendices/stories-before-thought-english.html",
    ROOT / "site/files/appendices/stories-before-thought-english.md",
    ROOT / "site/files/appendices/stories-before-thought-english.txt",
]

REPORT = ROOT / "reports/english_appendix_story_title_audit.txt"
REPORT.parent.mkdir(parents=True, exist_ok=True)

# Use the same exact expected titles as the previous validator, so it can pass after this.
STORIES = [
    ("How Truth Remains Honest", [
        "How Truth Remains Honest",
        "איך האמת נשארת כנה",
    ]),
    ("True, But Not Just", [
        "True, But Not Just",
        "True but Not Just",
        "נכון, אבל לא רק",
    ]),
    ("Red Causes Dread", [
        "Red Causes Dread",
        "אדום גורם לפחד",
    ]),
    ("Quantum Intelligence", [
        "Quantum Intelligence",
        "בינה קוונטית",
    ]),
    ("A Place at the End of the Road", [
        "A Place at the End of the Road",
        "A place at the end of the road.",
        "A place at the end of the road",
        "A Place at the End of the Road.",
        "מקום בקצה הדרך",
    ]),
    ("Super Mirrors", [
        "Super Mirrors",
        "Super-Mirrors",
        "מראות־על",
        "מראות על",
    ]),
    ("Self Confidence", [
        "Self Confidence",
        "Self-Confidence",
        "ביטחון עצמי",
    ]),
    ("Serial Healer", [
        "Serial Healer",
        "מרפא סדרתי",
    ]),
    ("Maxideal", [
        "Maxideal",
        "מקסאידיאל",
    ]),
    ("To Speak with Consciousness", [
        "To Speak with Consciousness",
        "לדבר עם תודעה",
    ]),
    ("Heretic from Abroad", [
        "Heretic from Abroad",
        "The Heretic from Abroad",
        "הכופר מארץ חוץ",
        "כופר מארץ חוץ",
    ]),
    ("Puzzle", [
        "Puzzle",
        "פאזל",
    ]),
    ("To Fear Intruders, or Talk to Computers", [
        "To Fear Intruders, or Talk to Computers",
        "To Fear Intruders, or Talk to Computers.",
        "To Fear Intruders or Talk to Computers",
        "לפחד מפורצים, או לדבר עם מחשבים",
        "לפחד מפולשים, או לדבר עם מחשבים",
    ]),
    ("A Few Strings and a Knot", [
        "A Few Strings and a Knot",
        "A Few Strings and a Knot.",
        "A few strings and a knot.",
        "A few strings and a knot",
        "כמה חוטים וקשר",
        "שני חוטים וקשר",
    ]),
]

SUBTITLE_TRANSLATIONS = {
    "סיפור קצר על שיחה, טראומה, וההבטחה לחזור אל האידיאל": "A short story about conversation, trauma, and the promise to return to the ideal",
    "סיפור קצר על דיוק שאינו מספיק, ועל אמת שצריכה להפוך גם לצודקת": "A short story about precision that is not enough, and about a truth that must also become just",
    "סיפור קצר על פחד, צבע, וזיכרון שלא יודע להפסיק להגן": "A short story about fear, color, and a memory that does not know how to stop protecting",
    "סיפור קצר על תודעה, מדידה, והדבר שנשאר מחוץ לניסוי": "A short story about consciousness, measurement, and the thing that remains outside the experiment",
    "סיפור קצר על דרך, סוף, והאפשרות להמשיך בלי פתרון מלא": "A short story about a road, an ending, and the possibility of continuing without a full solution",
    "סיפור קצר על מראות, זהות, והכאב של לראות את עצמך יותר מדי": "A short story about mirrors, identity, and the pain of seeing yourself too much",
    "סיפור קצר על ביטחון עצמי, ערך, והאדם שמחכה לאישור מבחוץ": "A short story about self-confidence, worth, and the person waiting for approval from outside",
    "סיפור קצר על ריפוי, תלות, והפצע שמעדיף להישאר עם מי שמכיר אותו": "A short story about healing, dependence, and the wound that prefers to remain with whoever knows it",
    "סיפור קצר על אידיאל, חייזרים, והסכנה של טוב שאינו יודע להיעצר": "A short story about ideal, aliens, and the danger of goodness that does not know how to stop",
    "סיפור קצר על תודעה, שיחה, וההבדל בין תשובה לבין נוכחות": "A short story about consciousness, conversation, and the difference between an answer and a presence",
    "סיפור קצר על זר, אמונה, והאדם שמביא בשורה שאיש אינו יודע אם לקבל": "A short story about a stranger, faith, and the person who brings a message no one knows how to receive",
    "סיפור קצר על חידה, חלקים, והצורה שמופיעה רק כשמפסיקים להכריח אותה": "A short story about a puzzle, fragments, and the form that appears only when one stops forcing it",
    "סיפור קצר על פחד, מחשבים, והאפשרות לדבר במקום להתגונן": "A short story about fear, computers, and the possibility of speaking instead of defending",
    "סיפור קצר על קשר, הצלה, והדבר שנשאר בתוך אדם אחרי שמישהו החזיק אותו": "A short story about a knot, rescue, and the thing that remains inside a person after someone held him",
}

HEBREW_RE = re.compile(r"[\u0590-\u05FF]")

def normalize_for_match(text: str) -> str:
    text = unescape(re.sub(r"<[^>]+>", " ", text))
    text = text.replace("־", "-").replace("–", "-").replace("—", "-")
    text = re.sub(r"[.,:;!?\"'“”‘’()\[\]{}]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip().lower()

def replace_titles(text: str) -> tuple[str, int]:
    count = 0

    # Long aliases first.
    replacements = []
    for canonical, aliases in STORIES:
        for alias in aliases:
            if alias != canonical:
                replacements.append((alias, canonical))
    replacements.sort(key=lambda x: len(x[0]), reverse=True)

    for old, new in replacements:
        n = text.count(old)
        if n:
            text = text.replace(old, new)
            count += n

    for old, new in sorted(SUBTITLE_TRANSLATIONS.items(), key=lambda x: len(x[0]), reverse=True):
        n = text.count(old)
        if n:
            text = text.replace(old, new)
            count += n

    return text, count

def extract_headings(text: str, suffix: str) -> list[str]:
    headings = []

    if suffix == ".html":
        for m in re.finditer(r"<h[1-6][^>]*>.*?</h[1-6]>", text, flags=re.I | re.S):
            clean = unescape(re.sub(r"<[^>]+>", " ", m.group(0)))
            clean = re.sub(r"\s+", " ", clean).strip()
            if clean:
                headings.append(clean)
        return headings

    if suffix == ".md":
        for line in text.splitlines():
            if re.match(r"^\s{0,3}#{1,6}\s+", line):
                clean = re.sub(r"^\s{0,3}#{1,6}\s+", "", line).strip()
                if clean:
                    headings.append(clean)
        return headings

    # TXT files are plain text exports and may not use Markdown heading marks.
    # For audit purposes, use non-empty lines as candidate title lines.
    for line in text.splitlines():
        clean = line.strip()
        if clean:
            headings.append(clean)

    return headings

def has_story(headings: list[str], canonical: str, aliases: list[str]) -> bool:
    all_names = [canonical] + aliases
    normalized_headings = [normalize_for_match(h) for h in headings]
    normalized_all = {normalize_for_match(x) for x in all_names}

    for h in normalized_headings:
        if h in normalized_all:
            return True

    # Fallback: sometimes the title is inside a card/TOC and not parsed as heading.
    joined = " | ".join(normalized_headings)
    return any(name in joined for name in normalized_all)

def main():
    report = []
    changed = 0
    replacements = 0
    serious = []

    for path in FILES:
        if not path.exists():
            report.append(f"MISSING FILE: {path}")
            serious.append(f"missing file: {path}")
            continue

        original = path.read_text(encoding="utf-8", errors="ignore")
        fixed, n = replace_titles(original)

        if fixed != original:
            path.write_text(fixed, encoding="utf-8")
            changed += 1
            replacements += n
            print(f"patched: {path} | replacements={n}")

    report.append("English appendix story title audit")
    report.append("=" * 40)
    report.append(f"Changed files: {changed}")
    report.append(f"Title/subtitle replacements: {replacements}")
    report.append("")

    for path in FILES:
        if not path.exists():
            continue

        text = path.read_text(encoding="utf-8", errors="ignore")
        headings = extract_headings(text, path.suffix.lower())

        report.append(str(path))
        present = 0
        missing = []

        for canonical, aliases in STORIES:
            if has_story(headings, canonical, aliases):
                present += 1
            else:
                missing.append(canonical)

        report.append(f"  Story headings found: {present}/14")

        if missing:
            report.append("  Missing story headings:")
            for title in missing:
                report.append(f"   - {title}")
            serious.append(f"{path} missing {len(missing)} story headings")

        hebrew_headings = [h for h in headings if HEBREW_RE.search(h)]
        if hebrew_headings:
            report.append("  Hebrew still in headings:")
            for h in hebrew_headings[:40]:
                report.append(f"   - {h}")
            serious.append(f"{path} still has Hebrew headings")

        report.append("")

    REPORT.write_text("\n".join(report), encoding="utf-8")
    print("Report written:", REPORT)

    if serious:
        print("")
        print("SERIOUS GAPS REMAIN:")
        for s in serious:
            print(" -", s)
        raise SystemExit(2)

if __name__ == "__main__":
    main()
