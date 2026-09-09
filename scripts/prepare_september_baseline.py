"""Stage current additive records out before historical release validators."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
(R/'docs/assets/iteration-19.js').write_bytes((R/'sources/september-2026/historical-living-mark.js').read_bytes())
p=R/'data/public-data.json'
d=json.loads(p.read_text())
prior=json.loads((R/'sources/september-2026/base-records.json').read_text())
removed={n['id'] for n in d['nodes'] if n.get('inclusion_reason') in {'september_connections_2026','authorised_systems_methods_practice_pack'}}
source_ids={s['id'] for s in d['sources'] if s.get('connection_pass')=='september_connections_2026' or s['id'].startswith('src_practice_') or s['id']=='src_systems_methods_practice_pack'}
for key,identity in [('nodes','id'),('profiles','node_id')]:
    originals={x[identity]:x for x in prior[key]}
    absent=set(prior.get('absent_profiles',[]))|{'intervention_skill_fractal_enterprise_model_and_capabilities'} if key=='profiles' else set()
    d[key]=[originals.get(x[identity],x) for x in d[key] if x[identity] not in removed and (x[identity] not in absent or x[identity] in originals)]
    for row in d[key]:
        values=row.get('source_ids','[]')
        if isinstance(values,str):row['source_ids']=json.dumps([v for v in json.loads(values) if v not in source_ids],ensure_ascii=False)
d['edges']=[e for e in d['edges'] if not e['id'].startswith(('e24_','practice_edge_'))]
d['sources']=[s for s in d['sources'] if s['id'] not in source_ids]
d['relation_types']=[r for r in d['relation_types'] if r['relation_type'] in prior['relation_types']]
for key in ['september_connections','versioned_curriculum','practice_pack']:d.pop(key,None)
d.get('core_systems_practice',{}).pop('practice_pack_url',None)
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print('Staged current practice and September additions out of historical validation')
