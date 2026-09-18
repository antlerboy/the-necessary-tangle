"""Check attribution, graph integrity, scoped evidence, and approved source bytes."""
from pathlib import Path
import hashlib
import json
from refresh_graph_snapshot import calculate
from apply_release_21 import COMPARATOR_SHA256, RECONCILIATION_SHA256

root = Path(__file__).resolve().parents[1]
data = json.loads((root / 'data/public-data.json').read_text(encoding='utf-8'))
packet = json.loads((root / 'sources/intake-2026-09-18/entries.json').read_text(encoding='utf-8'))
assert data == json.loads((root / 'docs/assets/public-data.json').read_text(encoding='utf-8'))
assert data['meta']['release'] == packet['release']
assert data['graph_snapshot'] == calculate(data)
assert data['meta']['public_link_source_count'] == sum(s.get('public_link_status') == 'public_link' for s in data['sources'])
assert data['meta']['unconnected_entry_count'] == data['relational_depth']['aggregate']['connection_bands'].get('unconnected', 0)
assert json.loads((root/'data/relationship-quality.json').read_text(encoding='utf-8'))['release'] == packet['release']
nodes = {n['id']: n for n in data['nodes']}
sources = {s['id'] for s in data['sources']}
edges = [e for e in data['edges'] if e['id'].startswith('e25_')]
assert len(edges) == len(packet['relations']) == 12
for edge in edges:
    assert edge['source'] in nodes and edge['target'] in nodes
    assert edge['source'] != edge['target']
    assert set(json.loads(edge['source_ids'])) <= sources
    assert edge['source_locator'] and edge['scope_conditions']
    assert not edge['reviewed_by'] and not edge['reviewed_at']
    assert edge['claim_status'] == 'candidate'
assert len({(e['source'], e['target'], e['relation_type']) for e in edges}) == len(edges)
for item in packet['entries']:
    node = nodes[item['id']]
    profile = next(p for p in data['profiles'] if p['node_id'] == item['id'])
    assert node['publication_level'] == 'profile' and node['status'] == 'candidate'
    assert not node['reviewed_by'] and not profile['reviewed_by']
    assert json.loads(profile['open_checks']) and 'AI assistance' in profile['editorial_note']
assert not any(e['source'] == 'person_judith_rosen' and e['relation_type'] in {'authored', 'edited'} for e in edges)
assert not any(e['source'] == 'person_david_l_hawk' and e['relation_type'] in {'studied_under', 'influenced_by'} for e in edges)
for name, expected in [('comparator-systemic-evolution.json', COMPARATOR_SHA256), ('systemic-evolution-reconciliation.json', RECONCILIATION_SHA256)]:
    original = (root / 'data' / name).read_bytes()
    assert hashlib.sha256(original).hexdigest() == expected, 'Reviewed file changed: ' + name
    assert original == (root / 'docs/assets' / name).read_bytes()
page = (root / 'docs/updates/2026-09-18/index.html').read_text(encoding='utf-8')
assert 'Open updates' in page and 'Independent specialist review is not recorded' in page
assert 'Valerie Ahl' in page
assert 'entry-editorial-note' in (root/'docs/assets/app.js').read_text(encoding='utf-8')
assert 'https://transduction.systems/updates/2026-09-18/' in (root / 'docs/sitemap.xml').read_text(encoding='utf-8')
print('Intake gate passed: source scope, credits, review status, graph consistency, feedback control, and approved bytes')
