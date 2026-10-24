"""Check source accounting, evidence scope, contribution privacy, and reproducibility."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote, parse_qs
import hashlib, json, subprocess, sys
R=Path(__file__).resolve().parents[1]; D=R/'docs'; S=R/'sources/update-2026-10-24'
d=json.loads((R/'data/public-data.json').read_text(encoding='utf-8'))
p=json.loads((S/'syscoi-review.json').read_text(encoding='utf-8'))
assert d['meta']['release']=='0.34'
assert len(p['posts'])==p['found']==9
assert len({r['id'] for r in p['posts']})==9
for row in p['posts']:
    assert len(row['links'])==len(set(row['links']))
    assert 'https://ashby-laboratory.benjaming98765.chatgpt.site' not in row['links'], 'Use the verified canonical resource URL'
new=[r for r in p['posts'] if r['status']=='new_discovery']; old=[r for r in p['posts'] if r['status']=='already_represented']
assert len(new)==5 and len(old)==4
nodes={n['id'] for n in d['nodes']}
for r in new:assert 'publication_syscoi_post_'+str(r['id']) in nodes
assert 'publication_syscoi_post_29303' not in nodes, 'Do not duplicate the developed Ashby Laboratory'
for edge in d['edges']:
    if edge.get('connection_pass')=='update_20261024':
        assert edge['claim_status']=='candidate' and edge['source_locator'] and edge['scope_conditions']
        assert edge['relation_type'] in ['catalogues_resource','uses','uses_in_argument']
assert len([e for e in d['edges'] if e['id'].startswith('e34_orglens_')])==4
class Links(HTMLParser):
    def __init__(self):super().__init__();self.links=[]
    def handle_starttag(self,tag,attrs):
        if tag=='a':self.links.append(dict(attrs).get('href',''))
routes=['reading/orglens','reading/42-systemic-review','reading/systems-leadership-and-action','contribute','updates/2026-10-24']
for route in routes:
    text=(D/route/'index.html').read_text(encoding='utf-8'); parser=Links();parser.feed(text)
    assert 'aria-label="Open updates"' in text
    from validate_iteration_14 import editorial_framing_text
    assert 'chatgpt' not in editorial_framing_text(text).lower(), 'Public resource hostname must not become production framing'
    for token in ['graph.microsoft','mail.google','file://','sandbox:','redquadrantltd']:assert token not in text
    for href in parser.links:
        u=urlsplit(href)
        if href.startswith('/'):
            target=D/unquote(u.path.lstrip('/'));assert target.is_file() or (target/'index.html').is_file(),href
            state=parse_qs(u.fragment)
            if 'id' in state:assert state['id'][0] in nodes,href
        elif not u.scheme:assert (D/route/u.path).is_file(),href
for path in ['contribute/index.html','index.html']:
    text=(D/path).read_text(encoding='utf-8')
    assert text.count('id="quickContributionForm"')==1
    assert 'optional, only for follow-ups' in text and 'sent privately for review' in text
    parser=Links();parser.feed(text)
from apply_release_21 import COMPARATOR_SHA256, RECONCILIATION_SHA256
for name,expected in [('comparator-systemic-evolution.json',COMPARATOR_SHA256),('systemic-evolution-reconciliation.json',RECONCILIATION_SHA256)]:
    assert hashlib.sha256((R/'data'/name).read_bytes()).hexdigest()==expected
paths=[R/'data/public-data.json',D/'assets/public-data.json',D/'index.html',*[D/r/'index.html' for r in routes]]
hashes=lambda:[hashlib.sha256(x.read_bytes()).hexdigest() for x in paths]
before=hashes();subprocess.run([sys.executable,'scripts/apply_update_34.py'],cwd=R,check=True)
assert before==hashes(),'Current intake is not idempotent'
print('0.34 passed: complete nine-post accounting, five new leads, scoped method uses, working internal routes, private contribution wording, unchanged comparator, and idempotence.')
