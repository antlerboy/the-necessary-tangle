from pathlib import Path
import hashlib,json,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
d=json.loads((ROOT/'data/public-data.json').read_text(encoding='utf-8'))
packet=json.loads((ROOT/'sources/weaver-2026-10-04/review.json').read_text(encoding='utf-8'))
edges=[e for e in d['edges'] if e.get('connection_pass')=='weaver_20261004']
assert len(edges)==4 and len({e['id'] for e in edges})==4
assert len({(e['source'],e['target'],e['relation_type']) for e in edges})==4
assert len([n for n in d['nodes'] if n['id']=='publication_fpcs_010'])==1
for e in edges:
 assert e['source']=='publication_fpcs_010' and e['target'] in {'concept_modelling','concept_complexity','concept_purpose'}
 assert e['relation_type'] in {'uses_in_argument','presents_account_of','qualifies_practice_claim'}
 assert 'PDF page ' in e['source_locator'] and e['claim_status']=='candidate' and not e['reviewed_by']
 assert json.loads(e['evidence_ids']) and e['claim_id']
page=ROOT/'docs/reading/weaver-complexity/index.html';text=page.read_text(encoding='utf-8')
assert text.count('<article id=')==4
for marker in ['Later transcription','PDF pages','not a facsimile','Organisational application','Open updates','original editorial exercise']:
 assert marker.casefold() in text.casefold(),marker
cat=json.loads((ROOT/'docs/assets/early-cybernetics-bibliography.json').read_text(encoding='utf-8'))
row=next(r for r in cat['entries'] if r['id']=='wiener-06');assert row['review_status']=='selected_passages_reviewed' and row['full_text_reviewed'] is False
paths=[ROOT/'data/public-data.json',ROOT/'docs/assets/public-data.json',page,ROOT/'sources/systemic-evolution/review-1/review-manifest.json']
before={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
subprocess.run([sys.executable,str(ROOT/'scripts/apply_weaver_29.py')],cwd=ROOT,check=True)
assert before=={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},'Idempotence or comparator defect'
print('Weaver 0.29: four nonduplicate typed claims, existing entities, source locators, catalogue status, candidate labels, and idempotence passed.')
