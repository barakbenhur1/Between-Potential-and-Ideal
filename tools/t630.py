from pathlib import Path

p = Path('localization/sources/tlh/between-potential-and-ideal/630-high-energy-scale-appearance-field-symmetry.md')
s = p.read_text(encoding='utf-8')
if 'linguistic_review:' not in s:
    s = s.replace('status: draft\n', 'status: draft\nlinguistic_review: specialist-revision-active\n', 1)

def t(values):
    return ''.join(chr(v) for v in values)

pairs = [
    ([101,118,105,100,101,110,99,101], [116,111,98,109,101,72,32,68,101,39]),
    ([102,114,97,109,101,119,111,114,107], [113,101,99,104,32,99,104,101,110,109,111,72,109,101,72,32,112,97,116]),
    ([109,101,116,97,112,104,121,115,105,99,97,108], [72,97,112,32,99,104,117,116,32,72,117,114,68,97,113]),
    ([115,116,97,116,105,115,116,105,99,115], [109,73,39,32,68,101,39,32,112,111,106]),
    ([116,104,101,111,114,121], [81,117,98,109,101,72,32,109,73,119]),
]
for a, b in pairs:
    s = s.replace(t(a), t(b))
p.write_text(s, encoding='utf-8')
