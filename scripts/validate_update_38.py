"""Validate Principia provenance, bounded changes and repeatable generation."""
from pathlib import Path
import hashlib, json, re, shutil, subprocess, sys, tempfile
from urllib.parse import urlsplit
R = Path(__file__).resolve().parents[1]
S = R/'documentation/research-2026-11-06-principia'
D = R/'docs'
M = 'principia_20261106'
d = json.loads((R/'data/public-data.json').read_text(encoding='utf-8'))
cohort = json.loads((S/'cohort.json').read_text(encoding='utf-8'))
register = json.loads((S/'register.json').read_text(encoding='utf-8'))
traces = json.loads((S/'primary-traces.json').read_text(encoding='utf-8'))
ids = {'organisation_principia_cybernetica_project','publication_principia_cybernetica_web','concept_semantic_network','comparator_corpus_principia_cybernetica_web_dictionary','tradition_evolutionary_cybernetics','concept_metasystem_transition','approach_family_metasystem_transition_theory'}
assert d['meta']['release'] == '0.38' and d[M]['originals']
assert len(d['nodes']) == 1422 and len(d['edges']) == 3158
assert len(cohort['pages']) == len(register['pages']) == 15
assert {p['url'] for p in cohort['pages']} == {p['url'] for p in register['pages']}
assert len({p['url'] for p in register['pages']}) == 15
assert len(traces['traces']) == 2
for row in register['pages']:
    assert urlsplit(row['url']).scheme in ('http', 'https')
    assert row.get('source_declared_status') and row.get('observed_text_status') and row.get('access') and row.get('checked_at')
    assert all(k in row for k in ('authors','creation_date','revision_date','locators'))
for row in traces['traces']:
    assert row.get('linked_pdf') and urlsplit(row['linked_pdf']).scheme in ('http', 'https') and row.get('pdf_status') and row.get('read_scope')
profiles = [p for p in d['profiles'] if p.get('connection_pass') == M]
nodes = [n for n in d['nodes'] if n.get('connection_pass') == M]
assert {p['node_id'] for p in profiles} == {n['id'] for n in nodes} == ids
assert len([j for j in d['journeys'] if j.get('connection_pass') == M]) == 1
assert not [x for key in ('edges','claims') for x in d[key] if x.get('connection_pass') == M]
def values(row, field):
    v = row.get(field, [])
    return json.loads(v) if isinstance(v, str) and v else v or []
source_ids = {s['id'] for s in d['sources']}
evidence_ids = {e['id'] for e in d['evidence']}
for row in nodes + profiles:
    assert row['review_status'] == 'research_pass_needs_editor' and not row.get('reviewed_by') and not row.get('reviewed_at')
    assert set(values(row, 'source_ids')) <= source_ids
for row in profiles:
    assert values(row, 'source_ids') and values(row, 'evidence_ids') and set(values(row, 'evidence_ids')) <= evidence_ids
for row in d['sources']:
    if row.get('connection_pass') == M:
        assert urlsplit(row['url']).scheme in ('http','https') and row.get('source_locator')
        assert not row.get('reviewed_by') and not row.get('reviewed_at')
for row in d['evidence']:
    if row.get('connection_pass') == M:
        assert row['source_id'] in source_ids and row.get('locator') and row.get('excerpt_or_summary')
        assert row['review_status'] == 'research_pass_needs_editor' and not row.get('reviewed_by') and not row.get('reviewed_at')
assert len(d[M]['originals']['nodes']) == 7
assert json.loads((D/'assets/public-data.json').read_text(encoding='utf-8')) == d
for name in ('register.json','primary-traces.json','cohort.json'):
    assert json.loads((D/'updates/2026-11-06-principia'/name).read_text(encoding='utf-8')) == json.loads((S/name).read_text(encoding='utf-8'))
for path in list(S.glob('*.json')) + [S/'reading.html']:
    content = path.read_text(encoding='utf-8')
    assert not re.search(r'(?i)(?:[a-z]:[\\\\/](?:users|d)[\\\\/]|sharepoint\.com|[\\w.+-]+@[\\w.-]+\.[a-z]{2,})', content), path
from apply_release_21 import COMPARATOR_SHA256, RECONCILIATION_SHA256
for name, expected in [('comparator-systemic-evolution.json', COMPARATOR_SHA256), ('systemic-evolution-reconciliation.json', RECONCILIATION_SHA256)]:
    assert hashlib.sha256((R/'data'/name).read_bytes()).hexdigest() == expected
with tempfile.TemporaryDirectory(prefix='tangle-38-') as temp:
    t = Path(temp)
    for folder in ['scripts','data','docs','documentation']:
        shutil.copytree(R/folder, t/folder)
    for name in ['README.md','CITATION.cff','CHANGELOG.md']:
        shutil.copy2(R/name, t/name)
    names = ['data/public-data.json','data/relationship-quality.json','documentation/TANGLE_STATE.md','documentation/NEXT_WORK.md','README.md','CITATION.cff','CHANGELOG.md','docs/assets/public-data.json','docs/assets/public-data.js','docs/assets/relationship-quality.json','docs/index.html','docs/library/index.html','docs/learning/index.html','docs/updates/index.html','docs/reading/knowledge-and-worldviews/index.html','docs/updates/2026-11-06-principia/index.html','docs/updates/2026-11-06-principia/register.json','docs/updates/2026-11-06-principia/primary-traces.json','docs/sitemap.xml','data/comparator-systemic-evolution.json','data/systemic-evolution-reconciliation.json']
    def hashes(): return {name: hashlib.sha256((t/name).read_bytes()).hexdigest() for name in names}
    before = hashes()
    subprocess.run([sys.executable,'scripts/apply_update_38.py'],cwd=t,check=True)
    assert before == hashes(), 'Release 0.38 application must be idempotent'
    subprocess.run([sys.executable,'scripts/prepare_update_38_baseline.py'],cwd=t,check=True)
    baseline = json.loads((t/'data/public-data.json').read_text(encoding='utf-8'))
    assert M not in baseline
    for key in ['nodes','profiles','sources','edges','evidence','claims','journeys']:
        identity = 'node_id' if key == 'profiles' else 'id'
        lookup = {row[identity]:row for row in baseline[key]}
        assert all(row.get('connection_pass') != M for row in baseline[key])
        assert all(lookup.get(row[identity]) == row for row in d[M]['originals'].get(key,[]))
print('0.38 passed: cohort, provenance, profiles, restoration, protected hashes, and idempotence.')
