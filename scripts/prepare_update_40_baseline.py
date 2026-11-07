"""Restore exact pre-0.40 records before historical release gates."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]; p=R/'data/public-data.json'; d=json.loads(p.read_text(encoding='utf-8')); M='variety_20261107'
originals={x['node_id']:x for x in d.get(M,{}).get('originals',{}).get('profiles',[])}
d['profiles']=[originals.get(x['node_id'],x) for x in d['profiles']]
d['evidence']=[x for x in d['evidence'] if x.get('connection_pass')!=M]
d.pop(M,None); p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
