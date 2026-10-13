"""Check reader routes, references, privacy and reproducible release 0.32 output."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote, parse_qs
import hashlib, json, subprocess, sys
R=Path(__file__).resolve().parents[1];D=R/'docs'
p=json.loads((R/'sources/update-2026-10-13/review.json').read_text())
d=json.loads((R/'data/public-data.json').read_text())
assert d['meta']['release']=='0.32'
assert len(p['design_horizon']['resources'])==8
assert len(p['maps'])==11
nodes={n['id'] for n in d['nodes']}
for r in p['design_horizon']['resources']:
    assert r['atlas_id'] in nodes, r
    assert r['author'] and r['locator'] and r['status'] and r['url'].startswith('https://')
routes=['about/how-to-use','about/evidence','reading/design-horizon','prior-maps/sources','updates/2026-10-13']
class Links(HTMLParser):
    def __init__(self):super().__init__();self.links=[]
    def handle_starttag(self,tag,attrs):
        if tag=='a':self.links.append(dict(attrs).get('href',''))
for route in routes:
    text=(D/route/'index.html').read_text(); parser=Links();parser.feed(text)
    assert 'aria-label="Open updates"' in text
    for token in ['graph.microsoft','mail.google','redquadrantltd','file://','sandbox:']:
        assert token not in text
    for href in parser.links:
        if href.startswith('/'):
            path=D/unquote(urlsplit(href).path.lstrip('/'))
            assert path.is_file() or (path/'index.html').is_file(), (route,href)
            state=parse_qs(urlsplit(href).fragment)
            if 'id' in state:assert state['id'][0] in nodes, href
text=(D/'index.html').read_text()
about=text.split('<section id="view-about"')[1].split('<section id="view-ai-observations"')[0]
for heading in ['Choose a starting point','What a connection means','Why the name?','Who is responsible?']:
    assert heading in about
assert 'relationalDepthMetrics' in about
assert 'summary>More about the map' in about
from apply_release_21 import COMPARATOR_SHA256, RECONCILIATION_SHA256
for name,expected in [('comparator-systemic-evolution.json',COMPARATOR_SHA256),('systemic-evolution-reconciliation.json',RECONCILIATION_SHA256)]:
    assert hashlib.sha256((R/'data'/name).read_bytes()).hexdigest()==expected
paths=[D/'index.html',R/'data/public-data.json',D/'assets/public-data.json',*[D/r/'index.html' for r in routes]]
hashes=lambda:[hashlib.sha256(x.read_bytes()).hexdigest() for x in paths]
before=hashes();subprocess.run([sys.executable,'scripts/apply_update_32.py'],cwd=R,check=True)
assert before==hashes(),'Release 0.32 rebuild is not idempotent'
print('Release 0.32 passed: guides, eight source routes, eleven map references, atlas targets, privacy, comparator hashes and idempotence.')
