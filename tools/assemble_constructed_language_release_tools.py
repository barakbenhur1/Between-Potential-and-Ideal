#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PARTS=ROOT/'tools'/'release_parts'
TOOLS=ROOT/'tools'
for first in sorted(PARTS.glob('*.py.part01')):
    name=first.name.split('.part',1)[0]
    pieces=sorted(PARTS.glob(name+'.part*'))
    (TOOLS/name).write_text(''.join(p.read_text(encoding='utf-8') for p in pieces),encoding='utf-8')
print('assembled',len(list(PARTS.glob('*.py.part01'))),'release tools')
