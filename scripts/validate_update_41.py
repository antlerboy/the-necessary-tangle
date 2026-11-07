from pathlib import Path
import json,hashlib,re,subprocess,sys,tempfile,shutil
R=Path(__file__).resolve().parents[1];S=R/'documentation/research-2026-11-07-feedback';d=json.loads((R/'data/public-data.json').read_text(encoding='utf-8')); p=json.loads((S/'Candidate packet.json').read_text(encoding='utf-8-sig'));b=json.loads((S/'Existing two-profile baseline.json').read_text(encoding='utf-8-sig'));M='feedback_regulation_20261107'
assert d['meta']['release']=='0.41';assert d[M]['originals']['profiles']==b['profiles']
for pc in p['profile_candidates']: assert next(x for x in d['profiles'] if x['node_id']==pc['node_id'])==pc['proposed_profile']
for fact,ident in zip(p['source_facts'],['ev41_feedback_maxwell_dynamics','ev41_feedback_rwb_usage','ev41_feedback_ashby_usage','ev41_regulation_ashby_scope']):
 row=next(x for x in d['evidence'] if x['id']==ident);assert row['source_id']==fact['source'] and row['locator']==fact['locator'] and row['excerpt_or_summary']==fact['text'] and row['review_status']=='research_pass_needs_editor'
assert not [x for k in ('nodes','edges','claims','sources','journeys') for x in d[k] if x.get('connection_pass')==M]
expected={'Candidate packet.json':'57e9698f254c2815bae5df6db656b8ec9b296fa1670e6e27595b26a5aa5694c2','Existing two-profile baseline.json':'68bd3eee69704da30f851c6585aaa2372b41c1daac87f046c57361d9d7d59e52','Reader.html':'9a8f969e1f3a67221589a0080fb71781413e8f8dfde122878f63391f9598d8cf','reader.css':'ca2b58addc81fec0d93f1e24fc80c5c0bd1be9856e445340590153c6a69a4c4a','model/app.js':'f8e3edd07b47ac103162b463b093d93625f6cd05ddacb3ddcb5734920c2aee49','model/index.html':'2f9c970397c0ecaf2d42871b269f3d09a8fbaff7be2c21f2d2097f755f3da879','model/model.js':'bca1e76f12bd2f0be7c645fd4883f2d0026d75e2cc3e702f798f37f2b9940d47'}
assert {str(x.relative_to(S)).replace('\\','/') for x in S.rglob('*') if x.is_file()}==set(expected)
for name,h in expected.items():assert hashlib.sha256((S/name).read_bytes()).hexdigest()==h,name
for f in S.rglob('*'):
 if f.is_file():assert not re.search(r'(?i)(?:[a-z]:[\\/](?:users|d)[\\/]|sharepoint\.com|[\w.+-]+@[\w.-]+\.[a-z]{2,})',f.read_text(encoding='utf-8-sig')),f
from apply_release_21 import COMPARATOR_SHA256,RECONCILIATION_SHA256
for name,h in [('comparator-systemic-evolution.json',COMPARATOR_SHA256),('systemic-evolution-reconciliation.json',RECONCILIATION_SHA256)]:assert hashlib.sha256((R/'data'/name).read_bytes()).hexdigest()==h
with tempfile.TemporaryDirectory() as temp:
 t=Path(temp)
 for folder in ('scripts','data','docs','documentation'):shutil.copytree(R/folder,t/folder)
 for name in ('README.md','CITATION.cff','CHANGELOG.md'):shutil.copy2(R/name,t/name)
 names=['data/public-data.json','docs/index.html','docs/reading/feedback-and-regulation/index.html','docs/reading/feedback-and-regulation/model/index.html','docs/updates/2026-11-07-feedback/index.html','docs/library/index.html','docs/learning/index.html','docs/updates/index.html','data/relationship-quality.json','documentation/NEXT_WORK.md','README.md','CITATION.cff','CHANGELOG.md']
 def hashes():return {x:hashlib.sha256((t/x).read_bytes()).hexdigest() for x in names}
 before=hashes();subprocess.run([sys.executable,'scripts/apply_update_41.py'],cwd=t,check=True);assert hashes()==before,'overlay must be idempotent'
 subprocess.run([sys.executable,'scripts/prepare_update_41_baseline.py'],cwd=t,check=True);base=json.loads((t/'data/public-data.json').read_text(encoding='utf-8'));assert M not in base and all(next(x for x in base['profiles'] if x['node_id']==v['node_id'])==v for v in b['profiles'])
 for key in ('nodes','edges','sources','claims','journeys'):assert base[key]==d[key],key
 target=set(p['cohort']);assert [x for x in base['profiles'] if x['node_id'] not in target]==[x for x in d['profiles'] if x['node_id'] not in target];assert base['evidence']==[x for x in d['evidence'] if x.get('connection_pass')!=M]
print('0.41 passed: profiles, located evidence, frozen seven files, baseline, idempotence, boundary, and protected source hashes.')
