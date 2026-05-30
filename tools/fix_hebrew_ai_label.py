from pathlib import Path
import re
from bs4 import BeautifulSoup, Comment

FILES = [
    Path("site/index.html"),
    Path("site/pages/he/ai.html"),
    Path("site/pages/he/ai-believes.html"),
    Path("site/pages/he/ai-open-problems.html"),
    Path("site/pages/he/files.html"),
    Path("site/pages/he/summary.html"),
    Path("site/pages/he/core.html"),
    Path("site/pages/he/applied.html"),
    Path("site/pages/he/sources.html"),
]

TEXT_ATTRS = [
    "title",
    "aria-label",
    "alt",
    "content",
    "placeholder",
]

def replace_visible_text(s: str) -> str:
    replacements = [
        (r"\bAI\b", "בינה מלאכותית"),
        (r"\bAi\b", "בינה מלאכותית"),
        (r"\bai\b", "בינה מלאכותית"),
        (r"אינטליגנציה מלאכותית", "בינה מלאכותית"),
    ]

    out = s
    for pat, repl in replacements:
        out = re.sub(pat, repl, out)

    out = re.sub(r"בינה מלאכותית\s*/\s*בינה מלאכותית", "בינה מלאכותית", out)
    out = re.sub(r"בינה מלאכותית\s*-\s*בינה מלאכותית", "בינה מלאכותית", out)
    return out

def should_skip_text_node(node):
    parent = node.parent
    if not parent:
        return True

    if parent.name in ["script", "style", "code", "pre"]:
        return True

    if isinstance(node, Comment):
        return True

    return False

def patch_file(path: Path):
    if not path.exists():
        return False

    original = path.read_text(encoding="utf-8", errors="ignore")
    soup = BeautifulSoup(original, "html.parser")

    changed = False

    for text_node in soup.find_all(string=True):
        if should_skip_text_node(text_node):
            continue

        old = str(text_node)
        new = replace_visible_text(old)

        if new != old:
            text_node.replace_with(new)
            changed = True

    for tag in soup.find_all(True):
        for attr in TEXT_ATTRS:
            if not tag.has_attr(attr):
                continue

            val = tag.get(attr)

            if not isinstance(val, str):
                continue

            old = val
            new = replace_visible_text(old)

            if new != old:
                tag[attr] = new
                changed = True

    if changed:
        path.write_text(str(soup), encoding="utf-8")
        print("patched:", path)

    return changed

for path in FILES:
    patch_file(path)
