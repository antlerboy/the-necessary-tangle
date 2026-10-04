"""Remove only the additive Weaver packet before historical gates."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'data/public-data.json';d=json.loads(p.read_text(encoding='utf-8'))
base=json.loads((ROOT/'sources/weaver-2026-10-04/base-records.json').read_text(encoding='utf-8'))
for key in ['sources','edges','evidence','claims']:
    d[key]=[r for r in d[key] if r.get('connection_pass')!='weaver_20261004']
d['nodes']=[base['node'] if n['id']=='publication_fpcs_010' else n for n in d['nodes']]
d['profiles']=[x for x in d['profiles'] if x['node_id']!='publication_fpcs_010']+base['profiles']
d.pop('weaver_20261004',None)
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('Staged the bounded Weaver source pass out of historical validation.')
