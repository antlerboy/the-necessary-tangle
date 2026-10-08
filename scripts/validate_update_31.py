"""Validate the research boundary, full disposition, reader routes, and repeatability."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,hashlib,subprocess,sys
R=Path(__file__).resolve().parents[1];S=R/'sources/update-2026-10-08';D=R/'docs';M='update_20261008'
p=json.loads((S/'review.json').read_text());d=json.loads((R/'data/public-data.json').read_text())
assert d['meta']['release']=='0.31'
assert len(p['comments'])==len({x['id'] for x in p['comments']})==85
assert len(p['issues'])==len({x['number'] for x in p['issues']})==14
actions={x['id'] for x in p['actions']}
assert all(c['actions'] and set(c['actions'])<=actions for c in p['comments'])
assert len(p['modules'])==5 and sum(m['pages'] for m in p['modules'])==32
assert len(p['ocad']['modules'])==12 and len(p['isss']['readings'])==57
assert len(json.loads((S/'castellani-link-audit.json').read_text())['links'])==307
nodes={n['id']:n for n in d['nodes']};sources={s['id']:s for s in d['sources']}
edges=[e for e in d['edges'] if e.get('connection_pass')==M]
assert len(edges)==41
assert nodes['concept_physical_exchange']['id'] != nodes['concept_material_open_system']['id']
assert next(e for e in edges if e['id']=='e31_module_prigogine_1')['target']=='concept_physical_exchange'
assert next(e for e in edges if e['target']=='concept_dissipative_structure' and e['relation_type']=='explanatory_prerequisite')['source']=='concept_physical_exchange'
for e in edges:
 assert e['source'] in nodes and e['target'] in nodes
 assert e['source_locator'] and e['scope_conditions'] and e['claim_status']=='candidate' and not e['reviewed_by']
 assert e['relation_type'] not in ['conceptually_related_to','legacy_association_unspecified']
 assert json.loads(e['evidence_ids']) and e['claim_id']
 assert all(sid in sources for sid in json.loads(e['source_ids']))
for m in p['modules']:
 assert sources['src_u31_'+m['id']]['content_hash']==m['sha256']
 assert 'publication_u31_'+m['id'] in nodes
assert not any(e['id']=='e31_isss_ocad' for e in d['edges'])
routes=['learning','learning/isss','corpora/ing-ocad','reading/researcher-modules','reading/orglens','prior-maps/principles','prior-maps/review-2026-10','updates/2026-10-08']
class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[]
 def handle_starttag(self,tag,attrs):
  if tag=='a':self.links.append(dict(attrs).get('href',''))
for route in routes:
 page=D/route/'index.html';text=page.read_text();parser=Links();parser.feed(text)
 assert 'aria-label="Open updates"' in text
 assert 'Curator: Benjamin P Taylor' in text
 for href in parser.links:
  if href.startswith('/') and not href.startswith('//'):
   target=D/unquote(urlsplit(href).path.lstrip('/'))
   assert target.is_file() or (target/'index.html').is_file(),(page,href)
assert '<span id="releaseBadge">Release 0.31</span>' in (D/'index.html').read_text()
ocad=(D/'corpora/ing-ocad/index.html').read_text()
assert 'not evidence that every suggestion entered the launched syllabus' in ocad
assert 'could not be retrieved' not in ocad and 'unavailable' not in ocad
from apply_release_21 import COMPARATOR_SHA256,RECONCILIATION_SHA256
for name,expected in [('comparator-systemic-evolution.json',COMPARATOR_SHA256),('systemic-evolution-reconciliation.json',RECONCILIATION_SHA256)]:
 for folder in ['data','docs/assets']:
  path=R/folder/name;assert hashlib.sha256(path.read_bytes()).hexdigest()==expected,path
for name in ['systemic-evolution-map.js','prior-maps.css']:
 assert (D/'assets'/name).read_bytes()==(R/'sources/systemic-evolution/review-1/site/assets'/name).read_bytes(),name
paths=[R/'README.md',R/'data/public-data.json',D/'assets/public-data.json',D/'index.html',D/'assets/app.js',D/'assets/site-enhancements.js',D/'sitemap.xml',*[D/r/'index.html' for r in routes]]
hashes=lambda:{str(x):hashlib.sha256(x.read_bytes()).hexdigest() for x in paths}
before=hashes()
for name in ['apply_update_31.py','patch_reader_31.py']:subprocess.run([sys.executable,str(R/'scripts'/name)],check=True,cwd=R)
after=hashes()
assert before==after,'Release 0.31 rebuild is not idempotent: '+', '.join(k for k in before if before[k]!=after[k])
print('Release 0.31 passed: 85 comments, 14 issues, 32 PDF pages, 12 modules, 57 citations, 41 located candidate claims, routes, comparator hashes, and idempotence.')
