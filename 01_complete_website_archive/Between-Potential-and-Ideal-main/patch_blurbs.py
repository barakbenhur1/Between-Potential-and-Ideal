from bs4 import BeautifulSoup
from pathlib import Path

base = Path('/mnt/data/blurbs_box_work/theory-site-static')
index_path = base/'index.html'
html = index_path.read_text(encoding='utf-8')
soup = BeautifulSoup(html, 'html.parser')

# Remove opening quote / blurb blocks from the hero and gather them in their current order.
selectors = ['cosmic-blurb', 'choice-blurb', 'pig-question-blurb', 'red-what-blurb']
blocks = []
hero = soup.select_one('section.hero')
for cls in selectors:
    # find all matching sections that still live at the top of the page
    for tag in list(soup.select(f'section.{cls}')):
        blocks.append(tag.extract())

# Build one large inner box for the preserved quote blocks.
wrapper = soup.new_tag('div')
wrapper['class'] = ['theory-blurbs-box']
wrapper['aria-label'] = 'ציטוטים ופתיחות לתאוריה'
wrapper['dir'] = 'rtl'

for tag in blocks:
    # Keep each block identity, text, direction and language visibility as-is.
    wrapper.append(tag)

# Insert under the response button, still inside the large theory / approach frame.
response_row = soup.select_one('.approach-frame .response-button-row')
if not response_row:
    raise SystemExit('Could not find response button row')
response_row.insert_after(wrapper)

# Update cache-busting query only for CSS/JS references.
for link in soup.find_all('link', href=True):
    if link['href'].startswith('styles.css'):
        link['href'] = 'styles.css?v=20260518-blurbs-in-theory-box'
for script in soup.find_all('script', src=True):
    if script['src'].startswith('script.js'):
        script['src'] = 'script.js?v=20260518-blurbs-in-theory-box'

index_path.write_text(str(soup), encoding='utf-8')

css_path = base/'styles.css'
css = css_path.read_text(encoding='utf-8')
append_css = r'''

/* Move opening blurbs into one designed theory box under the reply button */
.theory-blurbs-box{
  width:min(920px,100%);
  margin:58px auto 10px;
  padding:30px 28px 32px;
  border:1px solid rgba(86,97,115,.24);
  background:rgba(255,249,236,.54);
  box-shadow:0 18px 52px rgba(23,32,45,.055);
  position:relative;
}
.theory-blurbs-box:before{
  content:"";
  display:block;
  width:86px;
  height:1px;
  background:rgba(166,112,45,.66);
  margin:0 auto 24px;
}
.theory-blurbs-box .cosmic-blurb,
.theory-blurbs-box .choice-blurb,
.theory-blurbs-box .pig-question-blurb,
.theory-blurbs-box .red-what-blurb{
  grid-column:auto;
  width:100%;
  margin-left:auto;
  margin-right:auto;
}
.theory-blurbs-box .cosmic-blurb{
  margin-top:0;
  margin-bottom:26px;
}
.theory-blurbs-box .choice-blurb{
  margin-top:0;
  margin-bottom:24px;
}
.theory-blurbs-box .pig-question-blurb{
  margin-top:0;
  margin-bottom:22px;
}
.theory-blurbs-box .red-what-blurb{
  margin-top:0;
  margin-bottom:0;
}
.theory-blurbs-box .cosmic-blurb:last-child,
.theory-blurbs-box .choice-blurb:last-child,
.theory-blurbs-box .pig-question-blurb:last-child,
.theory-blurbs-box .red-what-blurb:last-child{
  margin-bottom:0;
}
@media(max-width:720px){
  .theory-blurbs-box{padding:22px 14px 24px;margin-top:46px;}
}
'''
# Avoid duplicate if re-run
if 'Move opening blurbs into one designed theory box under the reply button' not in css:
    css += append_css
else:
    import re
    css = re.sub(r'\n/\* Move opening blurbs into one designed theory box under the reply button \*/[\s\S]*$', append_css, css)
css_path.write_text(css, encoding='utf-8')
