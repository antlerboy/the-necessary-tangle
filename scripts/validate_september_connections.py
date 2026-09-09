from pathlib import Path
import json
from refresh_graph_snapshot import calculate
R=Path(__file__).resolve().parents[1]
d=json.loads((R/'data/public-data.json').read_text());public=json.loads((R/'docs/assets/public-data.json').read_text())
assert d==public,'Generated public data differs'
assert d['graph_snapshot']==calculate(d),'Graph snapshot does not match graph'
nodes={n['id'] for n in d['nodes']};sources={s['id'] for s in d['sources']};types={r['relation_type'] for r in d['relation_types']}
edges=[e for e in d['edges'] if e['id'].startswith('e24_')]
assert len(edges)>=32
for e in edges:
 assert e['source'] in nodes and e['target'] in nodes
 assert e['source']!=e['target'] and e['relation_type'] in types
 assert e['source_locator'] and e['scope_conditions']
 assert set(json.loads(e['source_ids']))<=sources
 assert not e['reviewed_by'] and not e['reviewed_at'],'Do not invent a named review'
assert len({(e['source'],e['target'],e['relation_type']) for e in edges})==len(edges)
assert all(e['relation_family']=='documentary' for e in edges if e['relation_type']=='offers_reading_route_to')
assert next(p for p in d['profiles'] if p['node_id']=='person_david_ing')['reviewed_by']==''
for route in ['corpora/ing-ocad','updates/2026-09-09']:
 text=(R/'docs'/route/'index.html').read_text();assert 'Open updates' in text and 'AI' in text
assert 'could not be retrieved' in (R/'docs/corpora/ing-ocad/index.html').read_text()
assert (R/'docs/events/resources/index.html').exists()
print('September sources, typed statements, public projections, provenance and queue gate passed:',len(edges),'statements')

assert all(len(d['versioned_curriculum'][v]['modules'])==24 for v in ['original','revised'])
assert 'Open updates' in (R/'docs/learning/leading-transformation/index.html').read_text()
