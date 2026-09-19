"""Check source coverage, evidence boundaries, and preserved reviewed material."""
from pathlib import Path
import hashlib,json
from apply_release_21 import PACKAGE_SHA256,COMPARATOR_SHA256,RECONCILIATION_SHA256
R=Path(__file__).resolve().parents[1]
def load(p):return json.loads((R/p).read_text(encoding='utf-8'))
d=load('data/public-data.json');p=load('sources/library-2026-09-19/public-library.json');c=load('docs/library/catalogue.json')
assert d['meta']['release']==c['release']=='0.26'
ids={n['id'] for n in d['nodes']};sourceids={s['id'] for s in d['sources']}
assert len(c['records'])==len({r['id'] for r in c['records']})
assert len(c['records'])>=6614
assert c['counts']['large_group_entries']==114
assert c['research_collection']['indexed_files']==2943
assert {r['id'] for r in p['records']} <= {r['id'] for r in c['records']}
for r in c['records']:
    assert r['url'].startswith('https://'),r['id']
    if r.get('atlas_id'):assert r['atlas_id'] in ids
    for x in r['connections']:
        assert x['target'] in ids,(r['title'],x['target'])
        assert x['kind'] in ['identity','title_match','text_mention','teaching_account','authorship','argument']
        assert x.get('locator'),r['title']
        for page in x.get('pages',[]):assert isinstance(page,int) and page>0 and page<=r.get('pages',10000)
    if r['collection']=='SysCoi':assert 'author' in c['authorship'].lower()
for e in d['edges']:
    if e.get('connection_pass')!='library_20260919':continue
    assert e['source'] in ids and e['target'] in ids
    assert e['claim_status']=='candidate' and not e.get('reviewed_by') and not e.get('reviewed_at')
    assert e['relation_family'] in ['documentary','teaching','practice','human','historical','conceptual','contestation']
for update in p['source_updates']:
    s=next(s for s in d['sources'] if s['id']==update['id'])
    assert s['url']==update['url'] and s['access']=='public'
    assert s['notes'].count('Public PDF linked on ')==1
for path in [R/'docs/library/catalogue.json',R/'sources/library-2026-09-19/public-library.json',R/'sources/library-2026-09-19/research-bibliography.json']:
    raw=path.read_text(encoding='utf-8').lower()
    for forbidden in ['sharepoint.com','graph.microsoft.com','benjamin.taylor/systems','downloadurl','access_token','c:/users/','c:\\\\users\\\\']:
        assert forbidden not in raw,(path.name,forbidden)
assert d['meta']['systemic_evolution_review_archive_sha256']==PACKAGE_SHA256
for filename,expected in [('comparator-systemic-evolution.json',COMPARATOR_SHA256),('systemic-evolution-reconciliation.json',RECONCILIATION_SHA256)]:
    assert hashlib.sha256((R/'data'/filename).read_bytes()).hexdigest()==expected
    assert (R/'data'/filename).read_bytes()==(R/'docs/assets'/filename).read_bytes()
assert 'living-mark-playback' not in (R/'docs/assets/reader-motion.js').read_text(encoding='utf-8')
assert 'data-library-nav' in (R/'docs/index.html').read_text(encoding='utf-8')
person='person_benjamin_p_taylor'
assert next(n for n in d['nodes'] if n['id']==person)['publication_level']=='profile'
assert next(p for p in d['profiles'] if p['node_id']==person)['last_researched']=='2026-09-19'
assert len([e for e in d['edges'] if person in [e['source'],e['target']] and e['relation_family'] not in ['classification','documentary','evidence','legacy']])>=15
out={'status':'passed','release':'0.26','records':len(c['records']),'teaching_connections':sum(x['kind']=='teaching_account' for r in c['records'] for x in r['connections']),'privacy_boundary':'No private source addresses or local paths in public packets','reviewed_package':'All three approved hashes preserved'}
(R/'validation/library-structure.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(json.dumps(out))
