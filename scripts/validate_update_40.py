from pathlib import Path
import json,hashlib,re,subprocess,sys,tempfile,shutil
R=Path(__file__).resolve().parents[1]; S=R/'documentation/research-2026-11-07-variety'; d=json.loads((R/'data/public-data.json').read_text(encoding='utf-8')); p=json.loads((S/'Candidate packet.json').read_text(encoding='utf-8-sig')); b=json.loads((S/'Existing three-profile baseline.json').read_text(encoding='utf-8-sig')); M='variety_20261107'
assert d['meta']['release']=='0.40'
assert d[M]['originals']['profiles']==b['profiles']
for pc in p['profile_candidates']:
 row=next(x for x in d['profiles'] if x['node_id']==pc['node_id']); expected=pc['proposed_profile']; assert all(row[k]==v for k,v in expected.items() if k!='evidence_ids'); assert set(json.loads(expected['evidence_ids'])).issubset(json.loads(row['evidence_ids']))
 for fact in pc['new_source_fact_ids']: assert 'ev_u40_variety_'+fact.lower() in json.loads(row['evidence_ids'])
for f in p['source_facts']:
 row=next(x for x in d['evidence'] if x['id']=='ev_u40_variety_'+f['id'].lower()); assert row['source_id']==f['source'] and row['locator']==f['locator'] and row['excerpt_or_summary']==f['text'] and row['review_status']=='research_pass_needs_editor'
assert not [x for k in ('nodes','edges','claims','sources','journeys') for x in d[k] if x.get('connection_pass')==M]
assert hashlib.sha256((S/'model-core.js').read_bytes()).hexdigest()=='280a3df81354731c94c8da9ed8b0619892624ac56bf841e4a7dd312672360ebd'
assert (S/'model-core.js').read_bytes()==(R/'docs/reading/which-distinctions/model-core.js').read_bytes()
from apply_release_21 import COMPARATOR_SHA256,RECONCILIATION_SHA256
for name,expected in [('comparator-systemic-evolution.json',COMPARATOR_SHA256),('systemic-evolution-reconciliation.json',RECONCILIATION_SHA256)]: assert hashlib.sha256((R/'data'/name).read_bytes()).hexdigest()==expected
for f in S.iterdir():
 if f.suffix in ('.json','.md','.html','.js','.css'): assert not re.search(r'(?i)(?:[a-z]:[\\\\/](?:users|d)[\\\\/]|sharepoint\.com|[\w.+-]+@[\w.-]+\.[a-z]{2,})',f.read_text(encoding='utf-8-sig')),f
with tempfile.TemporaryDirectory() as temp:
 t=Path(temp)
 for folder in ('scripts','data','docs','documentation'): shutil.copytree(R/folder,t/folder)
 for name in ('README.md','CITATION.cff','CHANGELOG.md'): shutil.copy2(R/name,t/name)
 names=['data/public-data.json','docs/index.html','docs/reading/which-distinctions/index.html','docs/reading/which-distinctions/model-core.js','docs/reading/which-distinctions/reader.css','docs/reading/which-distinctions/reader.js','docs/reading/which-distinctions/candidate-data.js','docs/updates/2026-11-07-variety/index.html','docs/library/index.html','docs/learning/index.html','docs/updates/index.html','docs/sitemap.xml','data/relationship-quality.json','docs/assets/relationship-quality.json','documentation/TANGLE_STATE.md','documentation/NEXT_WORK.md','README.md','CITATION.cff','CHANGELOG.md']
 def hashes(): return {x:hashlib.sha256((t/x).read_bytes()).hexdigest() for x in names}
 before=hashes(); subprocess.run([sys.executable,'scripts/apply_update_40.py'],cwd=t,check=True); assert hashes()==before
 (t/'documentation/NEXT_WORK.md').write_bytes((t/'documentation/research-2026-11-06-sysprac-six/work-packet.md').read_bytes())
 subprocess.run([sys.executable,'scripts/apply_update_40.py'],cwd=t,check=True); assert hashes()==before, '0.40 must restore the current packet after the 0.39 overlay'
 subprocess.run([sys.executable,'scripts/prepare_update_40_baseline.py'],cwd=t,check=True); base=json.loads((t/'data/public-data.json').read_text(encoding='utf-8')); assert M not in base and all(next(x for x in base['profiles'] if x['node_id']==v['node_id'])==v for v in b['profiles'])
 for key in ('nodes','edges','sources','claims','journeys'):
  assert base[key]==d[key], 'non-target records changed: '+key
 target={x['node_id'] for x in b['profiles']}
 assert [x for x in base['profiles'] if x['node_id'] not in target]==[x for x in d['profiles'] if x['node_id'] not in target]
 assert base['evidence']==[x for x in d['evidence'] if x.get('connection_pass')!=M]
print('0.40 passed: source locators, exact baseline restoration, idempotence, public boundary, and protected source hashes.')
