from pathlib import Path
import json,hashlib,re,subprocess,sys,shutil
R=Path(__file__).resolve().parents[1];d=json.loads((R/'data/public-data.json').read_text(encoding='utf8'));M='control_inference_20261107'
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
expected_collections={'nodes':'889da0c1c59fc08e09e801951086c4d9bb7b37dcf712f45ffb73539040732662','edges':'f4db608adba5933986b421d104a3a21063177d46d20028f9a39256dcbd617664','claims':'df6f26b549461803559d42a482e42de3822edbc4212a8a0492562f0217ff248d','journeys':'f743ba3ebdc035e675a7d7145885fe337d1fc64674fb605eabcd8ba5cd78a60c','sources':'92819346455e92eb88b2f1f0f6611cfecba393c8dee9dc56ab170928c6648276','evidence':'40c739243aef6df7974ac7c4be0d1c0a84010413dfb859847ff29bbe817b2de3'}
# Compare the built public records with the exact checked-out candidate before
# the existing guards run. Report all collections even when the first guard fails.
committed=json.loads(subprocess.check_output(['git','show','HEAD:data/public-data.json'],cwd=R).decode('utf-8'))
summary={}
for name in ('nodes','edges','claims','journeys','sources','evidence','profiles'):
 identity='node_id' if name=='profiles' else 'id'
 before=committed[name];after=d[name]
 old={row[identity]:row for row in before};new={row[identity]:row for row in after}
 old_order=[row[identity] for row in before];new_order=[row[identity] for row in after]
 old_pos={value:i for i,value in enumerate(old_order)};new_pos={value:i for i,value in enumerate(new_order)}
 shared=sorted(old.keys() & new.keys())
 changed=[]
 for ident in shared:
  a=old[ident];b=new[ident]
  fields={key:{'committed':a.get(key),'built':b.get(key)} for key in sorted(a.keys() | b.keys()) if key not in a or key not in b or a[key]!=b[key]}
  if fields:changed.append({'id':ident,'fields':fields})
 moved=[{'id':ident,'committed_index':old_pos[ident],'built_index':new_pos[ident]} for ident in shared if old_pos[ident]!=new_pos[ident]]
 # Show coordinate changes and the known 0.41 evidence moves first.
 if name=='nodes':changed.sort(key=lambda item:(not any(key in item['fields'] for key in ('x','y')),item['id']))
 if name=='evidence':moved.sort(key=lambda item:(not item['id'].startswith('ev41_'),item['id']))
 added=sorted(new.keys()-old.keys());removed=sorted(old.keys()-new.keys())
 summary[name]={'committed_count':len(before),'built_count':len(after),'committed_unique_ids':len(old),'built_unique_ids':len(new),'same_id_set':not added and not removed,'same_order':old_order==new_order,'changed_record_count':len(changed),'changed_examples':changed[:20],'added_count':len(added),'added_examples':added[:20],'removed_count':len(removed),'removed_examples':removed[:20],'moved_count':len(moved),'moved_examples':moved[:20]}
 if name in expected_collections:
  checked=[row for row in after if row.get('connection_pass')!=M] if name in ('sources','evidence') else after
  summary[name]['guard_expected_sha256']=expected_collections[name];summary[name]['guard_actual_sha256']=digest(checked)
report={'comparison':'Committed HEAD public data versus built public data','example_limit_per_collection':20,'collections':summary}
output=R/'validation/update-42-diagnostics.json';output.parent.mkdir(parents=True,exist_ok=True);output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('0.42 diagnostic comparison: '+json.dumps(summary,ensure_ascii=False,sort_keys=True),flush=True)
for k,h in expected_collections.items():
 rows=[x for x in d[k] if x.get('connection_pass')!=M] if k in ('sources','evidence') else d[k]
 assert digest(rows)==h,k
assert digest([x for x in d['profiles'] if x['node_id'] not in ('concept_feedforward','concept_black_box')])=='17c89ada34f90fc16e94ffd0c05512e35cdd994b24ebce1bfe7a98977a532eec'
for ident in ['concept_feedforward','concept_black_box']:
 p=next(x for x in d['profiles'] if x['node_id']==ident);n=next(x for x in d['nodes'] if x['id']==ident);assert p['canonical_definition']==n['canonical_definition'];assert p['review_status']=='research_pass_needs_editor'
box=next(x for x in d['evidence'] if x['id']=='ev42_box_limits')
assert box['evidence_type']=='primary_text_paraphrase'
assert box['excerpt_or_summary']=='Some states cannot be revisited at will; different internal networks can realise the same specified behaviour.'
base=json.loads((R/'documentation/research-2026-11-07-control/feedforward/Existing feedforward baseline.json').read_text(encoding='utf-8-sig'))
assert json.loads(next(x for x in d['profiles'] if x['node_id']=='concept_feedforward')['open_checks'])==json.loads(base['profile']['open_checks'])
expected={'feedforward/Evidence note.md':'189d20e9ba2414f391de4bc249388e6a36ba00ce0df9272585a7c10f4feec824','feedforward/Existing feedforward baseline.json':'26a5db86dc821dcbe7e96ff110e794959437facd47a23a79c1df9da3e01015eb','feedforward/Three scenarios.md':'282efb8eccf4cf651a0e455f88c125c009e7c81de7bffadb612e944ead528d06','black-box/Evidence note.md':'f0a81bb6d09d2f51cceed684d79fba3686ae86eaf146cb75bca4bf8480ed43b3','black-box/Existing node baseline.json':'1e6e6acafeaa02f2a13025df8cc314a1c69a6460be1b4aaf3f1d391368d1006a','black-box/Reader.md':'6de35eebd37d0a08b507a06084c9d9799adff3a35b6924a2cbdf6426da14ac90'}
s=R/'documentation/research-2026-11-07-control';assert {str(x.relative_to(s)).replace('\\','/') for x in s.rglob('*') if x.is_file()}==set(expected)
for n,h in expected.items():
 raw=(s/n).read_bytes();assert hashlib.sha256(raw).hexdigest()==h,n;assert not re.search(r'(?i)(?:[a-z]:[\\/](?:users|d)[\\/]|sharepoint\.com|[\w.+-]+@[\w.-]+\.[a-z]{2,})',raw.decode('utf-8-sig')),n
from apply_release_21 import COMPARATOR_SHA256,RECONCILIATION_SHA256
for n,h in [('comparator-systemic-evolution.json',COMPARATOR_SHA256),('systemic-evolution-reconciliation.json',RECONCILIATION_SHA256)]:assert hashlib.sha256((R/'data'/n).read_bytes()).hexdigest()==h
print('0.42 source bytes, graph invariants, profiles, evidence, privacy, and protected hashes passed.')
