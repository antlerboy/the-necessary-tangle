"""Validate the bounded 0.37 source accounts and reversible generation."""
from pathlib import Path
import hashlib, json, shutil, subprocess, sys, tempfile
from urllib.parse import urlsplit
R = Path(__file__).resolve().parents[1]
D = R/'docs'
M = 'foundational_20261106'
d = json.loads((R/'data/public-data.json').read_text(encoding='utf-8'))
packet = json.loads((R/'documentation/research-2026-11-06-foundational/packet.json').read_text(encoding='utf-8'))
assert d['meta']['release'] == '0.37' and d[M]['originals']
ids = {'publication_fpcs_013','publication_fpcs_023','publication_fpcs_037','publication_fpcs_055'}
def values(row, field):
    value = row.get(field, [])
    return json.loads(value) if isinstance(value, str) and value else value or []
profiles = [p for p in d['profiles'] if p.get('connection_pass') == M]
nodes = [n for n in d['nodes'] if n.get('connection_pass') == M]
assert {p['node_id'] for p in profiles} == {n['id'] for n in nodes} == ids
assert len([j for j in d['journeys'] if j.get('connection_pass') == M]) == 1
assert not [e for e in d['edges'] if e.get('connection_pass') == M]
source_ids = {s['id'] for s in d['sources']}
evidence_ids = {e['id'] for e in d['evidence']}
for row in nodes+profiles:
    assert row['review_status'] == 'research_pass_needs_editor' and not row.get('reviewed_by') and not row.get('reviewed_at')
    assert set(values(row, 'source_ids')) <= source_ids
for row in profiles:
    assert values(row, 'source_ids') and values(row, 'evidence_ids') and set(values(row, 'evidence_ids')) <= evidence_ids
for row in d['sources']:
    if row.get('connection_pass') == M:
        assert urlsplit(row['url']).scheme in ('http','https') and row.get('source_locator')
for row in d['evidence']:
    if row.get('connection_pass') == M:
        assert row['source_id'] in source_ids and row.get('locator') and row.get('excerpt_or_summary')
        assert row['review_status'] == 'research_pass_needs_editor'
assert len(d[M]['originals']['nodes']) == 4
assert d['depth_20261106'] and (D/'updates/2026-11-06/index.html').is_file()
assert json.loads((D/'assets/public-data.json').read_text(encoding='utf-8')) == d
from apply_release_21 import COMPARATOR_SHA256, RECONCILIATION_SHA256
for name, expected in [('comparator-systemic-evolution.json', COMPARATOR_SHA256), ('systemic-evolution-reconciliation.json', RECONCILIATION_SHA256)]:
    assert hashlib.sha256((R/'data'/name).read_bytes()).hexdigest() == expected
with tempfile.TemporaryDirectory(prefix='tangle-37-') as temp:
    t = Path(temp)
    for folder in ['scripts','data','docs']:
        (t/folder).mkdir()
    for name in ['scripts/prepare_update_37_baseline.py','data/public-data.json','docs/index.html']:
        shutil.copy2(R/name,t/name)
    subprocess.run([sys.executable,str(t/'scripts/prepare_update_37_baseline.py')],check=True)
    baseline = json.loads((t/'data/public-data.json').read_text(encoding='utf-8'))
    assert M not in baseline
    for key in ['nodes','profiles','sources','edges','evidence','claims','journeys']:
        identity = 'node_id' if key == 'profiles' else 'id'
        lookup = {row[identity]:row for row in baseline[key]}
        assert all(row.get('connection_pass') != M for row in baseline[key])
        assert all(lookup.get(row[identity]) == row for row in d[M]['originals'].get(key,[]))
    assert 'Release 0.36' in (t/'docs/index.html').read_text(encoding='utf-8')
# Exercise application and protected hashes in a disposable repository copy.
with tempfile.TemporaryDirectory(prefix='tangle-37-idempotence-') as temp:
    t = Path(temp)
    for folder in ['scripts', 'data', 'docs', 'documentation']:
        shutil.copytree(R/folder, t/folder)
    for name in ['README.md', 'CITATION.cff', 'CHANGELOG.md']:
        shutil.copy2(R/name, t/name)
    names = ['data/public-data.json','data/relationship-quality.json','documentation/TANGLE_STATE.md','documentation/NEXT_WORK.md','README.md','CITATION.cff','CHANGELOG.md','docs/assets/public-data.json','docs/assets/public-data.js','docs/assets/relationship-quality.json','docs/index.html','docs/library/index.html','docs/learning/index.html','docs/updates/index.html','docs/reading/models-and-patterns/index.html','docs/updates/2026-11-06-foundational/index.html','docs/updates/2026-11-06-foundational/evidence.json','docs/updates/2026-11-06/index.html','docs/sitemap.xml']
    names += ['data/comparator-systemic-evolution.json', 'data/systemic-evolution-reconciliation.json']
    def hashes(): return {name: hashlib.sha256((t/name).read_bytes()).hexdigest() for name in names}
    before = hashes()
    subprocess.run([sys.executable, 'scripts/apply_update_37.py'], cwd=t, check=True)
    assert before == hashes(), 'Release 0.37 application and protected sources must be unchanged in the disposable copy'
assert (R/'documentation/NEXT_WORK.md').read_text(encoding='utf-8') == (R/'documentation/research-2026-11-06-foundational/work-packet.md').read_text(encoding='utf-8')
print('0.37 passed: four profiles, source and evidence references, original-record restoration, protected hashes, and idempotence.')
