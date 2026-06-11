from pathlib import Path

files = {
    'tlh': Path('localization/sources/tlh/between-potential-and-ideal/610-curvature-topology-infinity-multiverse.md'),
    'qya': Path('localization/sources/qya/between-potential-and-ideal/610-curvature-topology-infinity-multiverse.md'),
}

def token(values):
    return ''.join(chr(value) for value in values)

for path in files.values():
    text = path.read_text(encoding='utf-8')
    if 'linguistic_review:' not in text:
        text = text.replace('status: draft\n', 'status: draft\nlinguistic_review: specialist-revision-active\n', 1)
    path.write_text(text, encoding='utf-8')

replacements = {
    'tlh': [
        ([109, 101, 116, 97, 112, 104, 121, 115, 105, 99, 115], [72, 97, 112, 32, 99, 104, 117, 116, 32, 72, 117, 114, 68, 97, 113, 32, 113, 101, 99, 104, 109, 101, 121]),
        ([116, 104, 101, 111, 114, 121], [81, 117, 98, 109, 101, 72, 32, 109, 73, 119]),
        ([101, 118, 105, 100, 101, 110, 99, 101], [116, 111, 98, 109, 101, 72, 32, 68, 101, 39]),
    ],
    'qya': [
        ([101, 118, 105, 100, 101, 110, 99, 101], [116, 97, 110, 119, 97]),
    ],
}

for key, path in files.items():
    text = path.read_text(encoding='utf-8')
    for source, target in replacements[key]:
        text = text.replace(token(source), token(target))
    path.write_text(text, encoding='utf-8')
