"""Check reconciliation, attribution, navigation and reproducible current intake."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote, parse_qs
import hashlib, json, subprocess, sys, re
R=Path(__file__).resolve().parents[1]; D=R/'docs'; S=R/'sources/update-2026-10-18'
p=json.loads((S/'syscoi-review.json').read_text(encoding='utf-8'))
a=json.loads((S/'ashby-review.json').read_text(encoding='utf-8'))
d=json.loads((R/'data/public-data.json').read_text(encoding='utf-8'))
nodes={n['id'] for n in d['nodes']}
assert d['meta']['release']=='0.33'
assert len(p['posts'])==p['found']==27
assert len({r['id'] for r in p['posts']})==27
assert len({r['url'].rstrip('/') for r in p['posts']})==27
new=[r for r in p['posts'] if r['status']=='new_discovery']
old=[r for r in p['posts'] if r['status']=='already_represented']
assert len(new)==20 and len(old)==7
for r in new:assert 'publication_syscoi_post_'+str(r['id']) in nodes
for r in old:assert 'publication_syscoi_post_'+str(r['id']) not in nodes
assert sum(c['exercises'] for c in a['chapters'])==56
assert [c['chapter'] for c in a['chapters']]==[3,4,5,6]
assert len([e for e in d['edges'] if e['id'].startswith('e33_lab_')])==5
for e in d['edges']:
    if e.get('connection_pass')=='update_20261018':
        assert e['claim_status']=='candidate' and e['source_locator'] and e['scope_conditions']
        assert e['relation_type'] in ['catalogues_resource','presents_account_of']
class Links(HTMLParser):
    def __init__(self):super().__init__();self.links=[]
    def handle_starttag(self,tag,attrs):
        if tag=='a':self.links.append(dict(attrs).get('href',''))
routes=['reading/ashby-laboratory','updates/2026-10-18']
for route in routes:
    text=(D/route/'index.html').read_text(encoding='utf-8'); parser=Links();parser.feed(text)
    assert 'aria-label="Open updates"' in text
    for token in ['graph.microsoft','mail.google','file://','sandbox:','redquadrantltd']:assert token not in text
    for href in parser.links:
        u=urlsplit(href)
        if href.startswith('/'):
            target=D/unquote(u.path.lstrip('/')); assert target.is_file() or (target/'index.html').is_file(),href
            state=parse_qs(u.fragment)
            if 'id' in state:assert state['id'][0] in nodes,href
        elif not u.scheme:assert (D/route/u.path).is_file(),href
text=(D/'reading/ashby-laboratory/index.html').read_text(encoding='utf-8')
assert text.count('<article id="chapter-')==4
assert a['url'] in text and a['book_url'] in text and a['bibliography_url'] in text
assert a['url']+'#' not in text
assert 'unrestricted code licence' in text and 'full interactive correctness' in text
from validate_iteration_14 import editorial_framing_text
assert not re.search(r'\bChatGPT\b', editorial_framing_text(a['url']), re.I)
assert re.search(r'\bChatGPT\b', editorial_framing_text('Production notes mention ChatGPT.'), re.I)
assert re.search(r'\bChatGPT\b', editorial_framing_text('https://another.chatgpt.site/'), re.I)
from apply_release_21 import COMPARATOR_SHA256, RECONCILIATION_SHA256
for name,expected in [('comparator-systemic-evolution.json',COMPARATOR_SHA256),('systemic-evolution-reconciliation.json',RECONCILIATION_SHA256)]:
    assert hashlib.sha256((R/'data'/name).read_bytes()).hexdigest()==expected
paths=[R/'data/public-data.json',D/'assets/public-data.json',D/'index.html',*[D/r/'index.html' for r in routes]]
hashes=lambda:[hashlib.sha256(x.read_bytes()).hexdigest() for x in paths]
before=hashes();subprocess.run([sys.executable,'scripts/apply_update_33.py'],cwd=R,check=True)
assert before==hashes(),'Current intake is not idempotent'
print('0.33 passed: 27 posts, 20 additions, seven duplicate exclusions, four attributed chapter routes, stable links, comparator hashes and idempotence.')
