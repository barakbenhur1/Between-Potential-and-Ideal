from pathlib import Path

path = Path('localization/sources/tlh/between-potential-and-ideal/580-planck-horizon-coordinates-information.md')
text = path.read_text(encoding='utf-8')
if 'linguistic_review:' not in text:
    text = text.replace('status: draft\n', 'status: draft\nlinguistic_review: specialist-revision-active\n', 1)

def token(values):
    return ''.join(chr(value) for value in values)

replacements = [
    ([99, 97, 108, 99, 117, 108, 97, 116, 105, 111, 110], [83, 73, 109, 109, 101, 72, 32, 109, 73, 119]),
    ([116, 104, 101, 111, 114, 121], [81, 117, 98, 109, 101, 72, 32, 109, 73, 119]),
]
for source, target in replacements:
    text = text.replace(token(source), token(target))
path.write_text(text, encoding='utf-8')
