"""Restore only records changed by 0.31 before historical release gates."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];p=R/'data/public-data.json';d=json.loads(p.read_text())
for key in ['nodes','profiles','sources','edges','evidence','claims']:
 d[key]=[r for r in d[key] if r.get('connection_pass')!='update_20261008']
for key,rows in json.loads((R/'sources/update-2026-10-08/base-records.json').read_text()).items():
 idkey='node_id' if key=='profiles' else 'id'
 for row in rows:
  for i,current in enumerate(d[key]):
   if current[idkey]==row[idkey]:d[key][i]=row;break
d.pop('update_20261008',None)
d['ai_observations']['observations']=[r for r in d['ai_observations']['observations'] if r['id']!='observation_source_depth_31']
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
