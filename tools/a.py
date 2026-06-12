from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/'site'
BASE_URL='https://between-potential-and-ideal.onrender.com'
LANGUAGES=('tlh','qya')
PACKAGES=('between-potential-and-ideal',)
PAGES=('about','ai-as-witness','ai-believes','ai-open-problems','ai','applied','art-of-potential','black-holes-horizons-holography','boundary-horizons','changelog','core','critique','discussion','education-of-potential','files','glossary','high-energy-physics','i-have-no-'+ 'mouth','law-of-potential','locality-nonlocality-contextuality','medicine-of-potential','methodology','mistake-repeats','music-of-potential','potential-extensions','potential-ideal-optimal','recursive-edge','response','science-physics-math-boundary-discipline','shape-of-the-universe-and-potential','sources','stories','summary','witness')
SEG={'about':(750,760,770),'ai-as-witness':(170,),'ai-believes':(70,170),'ai-open-problems':(180,),'ai':(170,180,190,200,210,220,290),'applied':tuple(range(390,520,10)),'art-of-potential':(370,),'black-holes-horizons-holography':(530,660),'boundary-horizons':(550,),'core':(20,30,40,50,60,80,90,100,110,120,130,140,150,160),'critique':(40,50,330,540,590,650),'discussion':(30,230,250),'education-of-potential':(120,),'glossary':(20,30,90,100,110),'high-energy-physics':(630,640,650),'i-have-no-'+ 'mouth':(190,),'law-of-potential':(480,490,500),'locality-nonlocality-contextuality':(310,320,330),'medicine-of-potential':(510,),'methodology':(40,50,300,540,590),'mistake-repeats':(200,210,220),'music-of-potential':(380,),'potential-extensions':tuple(range(520,630,10)),'potential-ideal-optimal':(30,90,100,110),'recursive-edge':(250,),'response':(40,50,540,590,650),'science-physics-math-boundary-discipline':(300,),'shape-of-the-universe-and-potential':(600,610,620),'sources':(750,760,770,780),'stories':(70,190,230),'summary':(20,30,60,90,100,110),'witness':(70,170,190,230)}
TITLES={
'tlh':{'about':'jInmol Delghach','ai-as-witness':'AI leghwI\'','ai-believes':'AI Harghach','ai-open-problems':'AI yu\'mey poS','ai':'AI','applied':'lo\'meH qechmey','art-of-potential':'Potential mIw "IH','black-holes-horizons-holography':'qIjbogh QemjIqmey, veHmey, holography','boundary-horizons':'veHmey','changelog':'choHmey QonoS','core':'botlh','critique':'poj','discussion':'ja\'chuqghach','education-of-potential':'Potential ghojmoHghach','files':'ghItlhmey','glossary':'qechmey mu\'ghom','high-energy-physics':'HoS jen HapQeD','i-have-no-mouth':'I Have No Mouth','law-of-potential':'Potential chut','locality-nonlocality-contextuality':'Daq, Daqbe\'ghach, ghu\' je','medicine-of-potential':'Potential Qelghach','methodology':'mIw','mistake-repeats':'Qagh qa\'','music-of-potential':'Potential QoQ','potential-extensions':'Potential Sachghachmey','potential-ideal-optimal':'Potential, Ideal, Optimal','recursive-edge':'chelqa\'bogh veH','response':'jangghach','science-physics-math-boundary-discipline':'QeD, HapQeD, mI\'QeD je veH','shape-of-the-universe-and-potential':'qo\' Hoch chen','sources':'mungmey','stories':'lutmey','summary':'qIjmeH ghItlh','witness':'leghwI\''},
'qya':{'about':'I Quenta','ai-as-witness':'AI ve Astarmo','ai-believes':'I ya AI Savë','ai-open-problems':'AI Mahtali Pantë','ai':'AI','applied':'Natyalië','art-of-potential':'Carmë Potentialo','black-holes-horizons-holography':'Mornë Hyarmar, Réni ar Holography','boundary-horizons':'Réni','changelog':'Quentalë Ahyaron','core':'Enda','critique':'Cesta','discussion':'Quetalië','education-of-potential':'Parma Potentialo','files':'Parmar','glossary':'Quettaparma','high-energy-physics':'Túrë Arda','i-have-no-mouth':'I Have No Mouth','law-of-potential':'Sanya Potentialo','locality-nonlocality-contextuality':'Nómë, Únómë ar Canta','medicine-of-potential':'Nestë Potentialo','methodology':'Cantië','mistake-repeats':'Loica Entulë','music-of-potential':'Lindalë Potentialo','potential-extensions':'Lantier Potentialo','potential-ideal-optimal':'Potential, Ideal, Optimal','recursive-edge':'Réna Envinyanta','response':'Hanquenta','science-physics-math-boundary-discipline':'Nolmë, Corma ar Nótë','shape-of-the-universe-and-potential':'Cantië Eäo','sources':'Celur','stories':'Nyári','summary':'Quenta Sinta','witness':'Astarmo'}}
PUBLIC_CONTROL_MARKERS=('image description draft:','image description:','visual description draft:','visual description:','visual brief:','alt text draft:','alt text:','image prompt draft:')
def clean(text):
 if text.startswith('---\n'):
  parts=text.split('---\n',2);text=parts[2] if len(parts)==3 else text
 lines=text.splitlines()
 for i,line in enumerate(lines):
  if line.strip() in ('## Segment review gate','## Placeholder review gate'):lines=lines[:i];break
 text='\n'.join(lines).strip()
 blocks=[]
 for block in re.split(r'\n\s*\n',text):
  normalized=re.sub(r'<[^>]+>',' ',block)
  normalized=re.sub(r'!\[[^\]]*\]\([^)]*\)',' ',normalized)
  normalized=re.sub(r'[>_*`\[\]()#\s-]+',' ',normalized).casefold()
  if any(marker in normalized for marker in PUBLIC_CONTROL_MARKERS):continue
  blocks.append(block.strip())
 return '\n\n'.join(blocks).strip()
def contract():return json.loads((ROOT/'localization/documents/between-potential-and-ideal.json').read_text())
def segments(lang):
 out={}
 for rel in contract()['source_segments'][lang]:
  m=re.search(r'/(\d{3})-',rel)
  if m:out[int(m.group(1))]=ROOT/rel
 return out
def body(lang,slug):
 m=segments(lang);return '\n\n'.join(clean(m[n].read_text()) for n in SEG.get(slug,SEG['summary']) if n in m)
def title(lang,slug):return TITLES.get(lang,{}).get(slug,slug.replace('-',' ').title())
