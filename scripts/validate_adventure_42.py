"""Verify projection completeness, provenance, reproducibility, and release wiring."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

R = Path(__file__).resolve().parents[1]
D = R / 'docs/42'
data = json.loads((R / 'data/public-data.json').read_text())
atlas = json.loads((D / 'atlas.json').read_text())
manifest = json.loads((D / 'manifest.json').read_text())
worlds = json.loads((D / 'worlds.json').read_text())
expected = {n['id'] for n in data['nodes'] if n.get('public_visibility') == 'public' and n.get('canonical_id', n['id']) == n['id']}
assert {n['id'] for n in atlas['nodes']} == expected, 'Serendipity must cover the full canonical public set'
assert len(atlas['nodes']) == len(expected)
original_edges = {e['id']: e for e in data['edges'] if e['source'] in expected and e['target'] in expected}
assert {e['id'] for e in atlas['edges']} == set(original_edges)
for e in atlas['edges']:
    source = original_edges[e['id']]
    assert e['source'] == source['source'] and e['target'] == source['target']
    assert e['relation_type'] == source['relation_type'] and e['scope'] == source.get('scope_conditions', '')
    assert e['directed'] == (source.get('directed') in [True, 'true', 'True'])
assert manifest['graph_sha256'] == hashlib.sha256((R / 'data/public-data.json').read_bytes()).hexdigest()
assert manifest['reader_release'] == '0.42' and manifest['graph_release'] == data['meta']['release']
for name in ['worlds.json', 'engine.js', 'app.js', 'adventure.css', 'index.html']:
    assert (D / name).read_bytes() == (R / 'sources/adventure-42' / name).read_bytes(), name
for n in atlas['nodes']:
    assert n['url'].startswith(('/entries/', '/#view=item&id='))
    for s in n['sources']:
        assert not s['url'] or s['url'].startswith(('https://', 'http://'))
        assert 'excerpt' not in s
assert len(worlds['rooms']) >= 10
assert all(r['anchor'] in expected for r in worlds['rooms'])
for name in ['docs/index.html', 'docs/updates/index.html', 'documentation/NEXT_WORK.md', 'README.md']:
    assert 'adventure-42' in (R / name).read_text(), name
assert 'href="/42/"' in (R / 'docs/index.html').read_text()
before = {str(p.relative_to(D)): hashlib.sha256(p.read_bytes()).hexdigest() for p in D.iterdir() if p.is_file()}
subprocess.run([sys.executable, 'scripts/build_adventure_42.py'], cwd=R, check=True)
after = {str(p.relative_to(D)): hashlib.sha256(p.read_bytes()).hexdigest() for p in D.iterdir() if p.is_file()}
assert before == after, 'Rebuilding the adventure must be deterministic'
assert manifest['graph_sha256'] == hashlib.sha256((R / 'data/public-data.json').read_bytes()).hexdigest()
print('Adventure structure passed: complete public projection, unchanged graph, exact connection semantics, source links, deterministic generation, and reader release.')
