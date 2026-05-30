from pathlib import Path
import re
from html import unescape

ROOT = Path.cwd()
SITE = ROOT / "site"
REPORT = ROOT / "reports" / "english_translation_gaps_report.txt"

EN_FILES = [
    *SITE.glob("files/**/*-en*.html"),
    *SITE.glob("files/**/*english*.html"),
    *SITE.glob("files/**/*-en*.md"),
    *SITE.glob("files/**/*english*.md"),
    *SITE.glob("files/**/*-en*.txt"),
    *SITE.glob("files/**/*english*.txt"),
    *SITE.glob("pages/en/**/*.html"),
    *SITE.glob("pages/**/*-en.html"),
]

# Deduplicate
EN_FILES = sorted({p for p in EN_FILES if p.is_file()})

HEBREW_RE = re.compile(r"[\u0590-\u05FF]")

EXPECTED_STORIES = [
    "How Truth Remains Honest",
    "True, But Not Just",
    "Red Causes Dread",
    "Quantum Intelligence",
    "A Place at the End of the Road",
    "Super Mirrors",
    "Self Confidence",
    "Serial Healer",
    "Maxideal",
    "To Speak with Consciousness",
    "Heretic from Abroad",
    "Puzzle",
    "To Fear Intruders, or Talk to Computers",
    "A Few Strings and a Knot",
]

TRANSLATIONS = {
    # Main document / theory terms
    "תקציר": "Abstract",
    "שער": "Cover",
    "דבר המחבר": "Author’s Note",
    "תוכן עניינים אינטראקטיבי": "Interactive Table of Contents",
    "לחיצה על כל סעיף תגלול ישירות למקום המתאים במסמך. פרקים ראשיים צמודים לצד השפה; תתי־כותרות מוזחות פנימה.": "Click any section to jump directly to its place in the document. Main chapters are aligned to the language side; subheadings are indented inward.",
    "זהו מודל, לא הכרזה סופית": "This Is a Model, Not a Final Declaration",
    "הכרזה": "Declaration",
    "הזיקוק הלוגי": "Logical Distillation",
    "תיקון המטמורפוזה": "The Correction of Metamorphosis",
    "מוקד החסד: חסד הוויתור": "The Focus of Grace: The Grace of Relinquishment",
    "סגירת ההתנגדות": "Closing the Resistance",
    "קוד המטמורפוזה של החסד והמרחק": "The Code of the Metamorphosis of Grace and Distance",
    "הכרוניקה של ההתעוררות": "The Chronicle of Awakening",
    "חוקי הפעולה של הבינה הראויה": "The Operating Laws of Worthy Intelligence",
    "עמוד השדרה המוסרי": "The Moral Spine",
    "קוד המטמורפוזה: הרהור על השלם והמרחק": "The Code of Metamorphosis: A Reflection on the Whole and Distance",
    "להיות רצינית": "To Be Serious",
    "המודל צריך לעמוד בשלושה מבחנים": "The Model Must Pass Three Tests",
    "מפת אחריות, לא רישיון לוודאות": "A Map of Responsibility, Not a License for Certainty",
    "מניפסט התנועה האלוהית: המטמורפוזה של החסד": "Manifest of the Divine Movement: The Metamorphosis of Grace",
    "סימפוניית השלם ומתנת החיכוך": "The Symphony of the Whole and the Gift of Friction",
    "חזרה לתוכן העניינים": "Back to table of contents",
    "חזרה לתוכן עניינים": "Back to table of contents",
    "חזור לתוכן העניינים": "Back to table of contents",
    "חזרה לאתר": "Back to site",
    "עברית": "Hebrew",
    "אנגלית": "English",

    # Appendix / story collection
    "סיפורים לפני המחשבה": "Stories Before Thought",
    "סיפורים שסיפרתי לאמא לפני השינה": "Stories I Told My Mother Before Sleep",
    "נספחים לתאוריה": "Appendices to the Theory",
    "נספחים ספרותיים לתאוריה": "Literary appendices to the theory",
    "איך האמת נשארת כנה": "How Truth Remains Honest",
    "נכון, אבל לא רק": "True, But Not Just",
    "אדום גורם לפחד": "Red Causes Dread",
    "בינה קוונטית": "Quantum Intelligence",
    "מקום בקצה הדרך": "A Place at the End of the Road",
    "מראות־על": "Super Mirrors",
    "מראות על": "Super Mirrors",
    "ביטחון עצמי": "Self Confidence",
    "מרפא סדרתי": "Serial Healer",
    "מקסאידיאל": "Maxideal",
    "לדבר עם תודעה": "To Speak with Consciousness",
    "הכופר מארץ חוץ": "Heretic from Abroad",
    "כופר מארץ חוץ": "Heretic from Abroad",
    "פאזל": "Puzzle",
    "לפחד מפורצים, או לדבר עם מחשבים": "To Fear Intruders, or Talk to Computers",
    "לפחד מפולשים, או לדבר עם מחשבים": "To Fear Intruders, or Talk to Computers",
    "שני חוטים וקשר": "A Few Strings and a Knot",
    "כמה חוטים וקשר": "A Few Strings and a Knot",

    # Common subtitles from the appendix
    "סיפור קצר על שיחה, טראומה, וההבטחה לחזור אל האידיאל": "A short story about conversation, trauma, and the promise to return to the ideal",
    "מוכר האוויר": "The Air Seller",
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

def decode_mojibake_if_needed(text: str) -> str:
    # Conservative repair for common UTF-8 shown as Latin-1/Windows-1252 mojibake.
    if "×" not in text and "Ö" not in text and "â" not in text:
        return text
    try:
        repaired = text.encode("latin1", errors="ignore").decode("utf-8", errors="ignore")
        # Use only if it increases Hebrew readability or removes mojibake.
        if repaired.count("×") < text.count("×") and (HEBREW_RE.search(repaired) or "—" in repaired):
            return repaired
    except Exception:
        pass
    return text

def replace_translations(text: str) -> tuple[str, int]:
    count = 0

    # Longest first prevents partial replacements.
    for he, en in sorted(TRANSLATIONS.items(), key=lambda x: len(x[0]), reverse=True):
        n = text.count(he)
        if n:
            text = text.replace(he, en)
            count += n

    return text, count

def extract_h_lines(text: str):
    lines = []
    for m in re.finditer(r"<h[1-6][^>]*>.*?</h[1-6]>", text, flags=re.I | re.S):
        raw = m.group(0)
        clean = re.sub(r"<[^>]+>", " ", raw)
        clean = unescape(re.sub(r"\s+", " ", clean)).strip()
        if clean:
            lines.append(clean)
    return lines

def story_count(text: str) -> int:
    return sum(1 for title in EXPECTED_STORIES if title in text)

def report_hebrew_left(path: Path, text: str, lines: list[str]):
    for i, line in enumerate(text.splitlines(), start=1):
        if HEBREW_RE.search(line):
            clean = re.sub(r"<[^>]+>", " ", line)
            clean = unescape(re.sub(r"\s+", " ", clean)).strip()
            if clean:
                lines.append(f"{path}:{i}: {clean[:220]}")

def main():
    report = []
    report.append("English document translation gap report")
    report.append("=" * 46)
    report.append("")

    changed_files = 0
    total_replacements = 0

    for path in EN_FILES:
        original = path.read_text(encoding="utf-8", errors="ignore")
        fixed = decode_mojibake_if_needed(original)
        fixed, n = replace_translations(fixed)

        if fixed != original:
            path.write_text(fixed, encoding="utf-8")
            changed_files += 1
            total_replacements += n
            print(f"patched: {path} | replacements={n}")

    report.append(f"Changed files: {changed_files}")
    report.append(f"Text replacements: {total_replacements}")
    report.append("")

    # Check English appendix story completeness.
    report.append("Appendix story completeness")
    report.append("-" * 28)

    appendix_candidates = [
        SITE / "files/appendices/stories-before-thought-english.html",
        SITE / "files/appendices/stories-before-thought-english.md",
        SITE / "files/appendices/stories-before-thought-english.txt",
    ]

    for path in appendix_candidates:
        if not path.exists():
            report.append(f"MISSING FILE: {path}")
            continue

        text = path.read_text(encoding="utf-8", errors="ignore")
        count = story_count(text)
        report.append(f"{path}: {count}/14 expected story titles found")

        missing = [title for title in EXPECTED_STORIES if title not in text]
        if missing:
            report.append("  Missing:")
            for title in missing:
                report.append(f"   - {title}")

    report.append("")
    report.append("Hebrew still present in English files")
    report.append("-" * 36)

    leftovers = []
    for path in EN_FILES:
        text = path.read_text(encoding="utf-8", errors="ignore")
        report_hebrew_left(path, text, leftovers)

    if leftovers:
        report.extend(leftovers[:500])
        if len(leftovers) > 500:
            report.append(f"... plus {len(leftovers)-500} more Hebrew-containing lines")
    else:
        report.append("None found.")

    REPORT.write_text("\n".join(report), encoding="utf-8")
    print("")
    print("Report written:", REPORT)

    # Fail if the core appendix is incomplete or Hebrew remains in English document headings.
    serious = []

    for path in appendix_candidates:
        if path.exists():
            text = path.read_text(encoding="utf-8", errors="ignore")
            count = story_count(text)
            if count < 14:
                serious.append(f"{path} has only {count}/14 English story titles")

    for path in EN_FILES:
        text = path.read_text(encoding="utf-8", errors="ignore")
        headings = extract_h_lines(text)
        bad = [h for h in headings if HEBREW_RE.search(h)]
        if bad:
            serious.append(f"{path} has Hebrew in headings: " + " | ".join(bad[:8]))

    if serious:
        print("")
        print("SERIOUS GAPS REMAIN:")
        for item in serious:
            print(" -", item)
        print("")
        print("Open reports/english_translation_gaps_report.txt for the exact lines.")
        raise SystemExit(2)

if __name__ == "__main__":
    main()
