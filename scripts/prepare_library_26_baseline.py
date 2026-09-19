"""Stage this additive release out before historical assertions run."""
from pathlib import Path
import json
from patch_library_navigation_26 import unpatch
R=Path(__file__).resolve().parents[1];p=R/'data/public-data.json'
app=R/'docs/assets/app.js'
app.write_text(unpatch(app.read_text(encoding='utf-8')),encoding='utf-8',newline='\n')
d=json.loads(p.read_text(encoding='utf-8'));base=json.loads((R/'sources/library-2026-09-19/base-records.json').read_text(encoding='utf-8'))
removed={n['id'] for n in d['nodes'] if n.get('inclusion_reason')=='library_20260919'}
removed_sources={s['id'] for s in d['sources'] if s.get('connection_pass')=='library_20260919'}
for key,field in [('nodes','id'),('sources','id'),('profiles','node_id')]:
    originals={r[field]:r for r in base[key]}
    excluded=removed_sources if key=='sources' else removed | (set(base['absent_profiles']) if key=='profiles' else set())
    d[key]=[originals.get(r[field],r) for r in d[key] if r[field] not in excluded]
    for r in d[key]:
        if isinstance(r.get('source_ids'),str):r['source_ids']=json.dumps([sid for sid in json.loads(r['source_ids']) if sid not in removed_sources],ensure_ascii=False)
d['edges']=[e for e in d['edges'] if e.get('connection_pass')!='library_20260919']
d['relation_types']=[r for r in d['relation_types'] if r['relation_type'] in base['relation_types']]
d.pop('library_integration',None)
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
# These generated outputs belong to the final stage, not the historical prose gate.
for filename in ['index.html','library.css','library.js','catalogue.json']:
    generated=R/'docs/library'/filename
    if generated.exists():generated.unlink()
print('Staged the source-library packet out of historical validation')
