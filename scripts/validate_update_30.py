"""Validate completeness, explicit scopes, idempotence and preserved source bytes."""
from pathlib import Path
import hashlib,json,subprocess,sys
R=Path(__file__).resolve().parents[1];M='update_20261007'
d=json.loads((R/'data/public-data.json').read_text());p=json.loads((R/'sources/update-2026-10-07/review.json').read_text())
assert d['meta']['release']=='0.30'
assert p['found']==len(p['posts'])==31
nodes={n['id']:n for n in d['nodes']};edges=[e for e in d['edges'] if e.get('connection_pass')==M]
assert len(edges)==39
assert len({e['id'] for e in edges})==39
for r in p['posts']:
 assert 'publication_syscoi_post_'+str(r['id']) in nodes
 assert r['url'].startswith('https://stream.syscoi.com/')
for e in edges:
 assert e['source_locator'] and e['scope_conditions'] and e['claim_status']=='candidate' and not e['reviewed_by']
 assert json.loads(e['evidence_ids']) and e['claim_id']
 assert e['relation_type']!='conceptually_related_to'
 assert e['source'] in nodes and e['target'] in nodes
page=(R/'docs/updates/2026-10-07/index.html').read_text();assert page.count('<article id="post-')==31
reader=(R/'docs/reading/socio-technical-transitions/index.html').read_text()
for marker in ['Editorial application','not a case studied by Schot','meta-rule','Open updates','Compare a possible response']:assert marker in reader
paths=[R/'data/public-data.json',R/'docs/assets/public-data.json',R/'docs/reading/socio-technical-transitions/index.html',R/'docs/updates/2026-10-07/index.html',R/'sources/systemic-evolution/review-1/review-manifest.json']
hashes=lambda:{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
before=hashes();subprocess.run([sys.executable,str(R/'scripts/apply_update_30.py')],check=True,cwd=R);assert before==hashes(),'Idempotence or comparator integrity failed'
print('Release 0.30: complete discovery intake, 39 scoped statements, evidence records, candidate labels and idempotence passed.')
