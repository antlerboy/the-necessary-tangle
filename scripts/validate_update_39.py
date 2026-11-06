"""Check the bounded SysPrac six source and reader release."""
from pathlib import Path
from urllib.parse import urlsplit
import hashlib, json, re, shutil, subprocess, sys, tempfile
R=Path(__file__).resolve().parents[1]; S=R/'documentation/research-2026-11-06-sysprac-six'; D=R/'docs'; M='sysprac_six_20261106'
d=json.loads((R/'data/public-data.json').read_text(encoding='utf-8')); p=json.loads((S/'evidence.json').read_text(encoding='utf-8'))
assert d['meta']['release']=='0.39'
assert len(p['sources'])==8 and len(p['evidence_proposals'])==7
assert {x['id'] for x in p['sources'] if x['id'].startswith('src_u39_s')}=={'src_u39_'+x for x in ('s30','s33','s34','s35','s38','s41')}
assert {x['id'] for x in d['nodes'] if x.get('connection_pass')==M}=={'publication_syscoi_post_28881'}
assert len([x for x in d['profiles'] if x.get('connection_pass')==M])==1
assert not [x for k in ('edges','claims') for x in d[k] if x.get('connection_pass')==M]
for row in p['sources']:
 assert urlsplit(row['url']).scheme in ('http','https') and row['locator']
for row in p['evidence_proposals']:
 assert row['locator'] and row['excerpt_or_summary'] and row['review_status']=='research_pass_needs_editor'
for f in S.glob('*'):
 if f.suffix in ('.json','.md','.html'):
  assert not re.search(r'(?i)(?:[a-z]:[\\\\/](?:users|d)[\\\\/]|sharepoint\.com|[\w.+-]+@[\w.-]+\.[a-z]{2,})',f.read_text(encoding='utf-8-sig')),f
for path in ['reading/conditions-for-action/index.html','updates/2026-11-06-sysprac-six/index.html']:
 text=(D/path).read_text(encoding='utf-8'); assert 'aria-label="Open updates"' in text and '<a href=' in text
from apply_release_21 import COMPARATOR_SHA256, RECONCILIATION_SHA256
for name, expected in [('comparator-systemic-evolution.json',COMPARATOR_SHA256),('systemic-evolution-reconciliation.json',RECONCILIATION_SHA256)]:
 assert hashlib.sha256((R/'data'/name).read_bytes()).hexdigest()==expected
with tempfile.TemporaryDirectory(prefix='tangle-39-') as temp:
 t=Path(temp)
 for folder in ('scripts','data','docs','documentation'): shutil.copytree(R/folder,t/folder)
 for name in ('README.md','CITATION.cff','CHANGELOG.md'): shutil.copy2(R/name,t/name)
 names=['data/public-data.json','data/relationship-quality.json','documentation/TANGLE_STATE.md','documentation/NEXT_WORK.md','README.md','CITATION.cff','CHANGELOG.md','docs/index.html','docs/library/index.html','docs/learning/index.html','docs/updates/index.html','docs/reading/conditions-for-action/index.html','docs/updates/2026-11-06-sysprac-six/index.html','docs/sitemap.xml']
 def hashes(): return {n:hashlib.sha256((t/n).read_bytes()).hexdigest() for n in names}
 before=hashes(); subprocess.run([sys.executable,'scripts/apply_update_39.py'],cwd=t,check=True); assert before==hashes(), '0.39 application must be idempotent'
 subprocess.run([sys.executable,'scripts/prepare_update_39_baseline.py'],cwd=t,check=True)
 baseline=json.loads((t/'data/public-data.json').read_text(encoding='utf-8')); assert M not in baseline
 for key,rows in d[M]['originals'].items():
  identity='node_id' if key=='profiles' else 'id'; lookup={r[identity]:r for r in baseline[key]}
  assert all(lookup.get(r[identity])==r for r in rows)
print('0.39 passed: source boundaries, profile, protected hashes, restoration, and idempotence.')
