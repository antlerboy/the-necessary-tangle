from pathlib import Path
import json
p=Path('data/public-data.json');d=json.loads(p.read_text(encoding='utf8')); m=d.pop('control_inference_20261107',None)
if m:
 d['profiles']=[m['original_profile'] if x['node_id']=='concept_feedforward' else x for x in d['profiles'] if x['node_id']!='concept_black_box'];d['sources']=[x for x in d['sources'] if x.get('connection_pass')!='control_inference_20261107'];d['evidence']=[x for x in d['evidence'] if x.get('connection_pass')!='control_inference_20261107'];p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
