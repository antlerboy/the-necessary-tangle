"""Check source-access boundaries, canonical graph preservation, and reader routes."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib
import json
from apply_release_21 import COMPARATOR_SHA256, RECONCILIATION_SHA256
from refresh_graph_snapshot import calculate

root=Path(__file__).resolve().parents[1]
data=json.loads((root/'data/public-data.json').read_text(encoding='utf-8'))
packet=json.loads((root/'sources/maps-2026-09-19/review.json').read_text(encoding='utf-8'))
assert data['meta']['release']=='0.25'
assert data==json.loads((root/'docs/assets/public-data.json').read_text(encoding='utf-8'))
assert data['graph_snapshot']==calculate(data)
assert data['map_source_review']==packet
assert packet==json.loads((root/'docs/prior-maps/coexplorer/source-review.json').read_text(encoding='utf-8'))
expected=json.loads((root/'validation/maps-input.json').read_text(encoding='utf-8'))
identities=json.loads((root/'sources/maps-2026-09-19/canonical-identities.json').read_text(encoding='utf-8'))
for key,sha in expected.items():
    records=sorted(data[key],key=lambda x:x.get('id',x.get('node_id','')))
    assert [x.get('id',x.get('node_id','')) for x in records]==identities[key], 'Canonical identities changed: '+key
    assert hashlib.sha256(json.dumps(records,sort_keys=True,ensure_ascii=False).encode()).hexdigest()==sha, 'Canonical content changed: '+key
for name,sha in [('comparator-systemic-evolution.json',COMPARATOR_SHA256),('systemic-evolution-reconciliation.json',RECONCILIATION_SHA256)]:
    original=(root/'data'/name).read_bytes()
    assert hashlib.sha256(original).hexdigest()==sha
    assert original==(root/'docs/assets'/name).read_bytes()
assert len(packet['sources'])==9
assert len([s for s in packet['sources'] if 'unread (HTTP 403)' in s['access']])==2
class Links(HTMLParser):
    def __init__(self):super().__init__();self.links=[]
    def handle_starttag(self,tag,attrs):
        if tag=='a':self.links.append(dict(attrs).get('href',''))
page=(root/'docs/prior-maps/coexplorer/index.html').read_text(encoding='utf-8')
assert 'Independent specialist review is not recorded' in page
assert 'Open updates' in page and 'Peter Tuddenham' in page
assert 'Curt McNamara' in page and 'full chapter remains unread' in page
parser=Links();parser.feed(page)
for href in parser.links:
    if href.startswith('/'):
        path=href.split('#')[0].split('?')[0]
        target=root/'docs'/path.lstrip('/')
        assert target.exists(),href
for source in packet['sources']:assert source['url'] in parser.links
for name in ['prior-maps/index.html','reading-list.html','updates/index.html']:
    assert '/prior-maps/coexplorer/' in (root/'docs'/name).read_text(encoding='utf-8')
assert 'https://transduction.systems/prior-maps/coexplorer/' in (root/'docs/sitemap.xml').read_text(encoding='utf-8')
assert json.loads((root/'data/relationship-quality.json').read_text(encoding='utf-8'))['release']=='0.25'
print('Map review passed: access labels, all nine source links, reader routes, exact canonical graph, and approved comparator bytes')
