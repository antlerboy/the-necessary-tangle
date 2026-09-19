"""Capture graph records immediately before the additive map-review stage.

Historical rebuilds may regenerate record metadata. Compare this stage with its
actual input, and separately preserve the reviewed canonical identity set.
"""
from pathlib import Path
import hashlib
import json

root=Path(__file__).resolve().parents[1]
data=json.loads((root/'data/public-data.json').read_text(encoding='utf-8'))
snapshot={}
for key in ['nodes','edges','profiles','sources']:
    records=sorted(data[key],key=lambda x:x.get('id',x.get('node_id','')))
    snapshot[key]=hashlib.sha256(json.dumps(records,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
path=root/'validation/maps-input.json'
path.parent.mkdir(exist_ok=True)
path.write_text(json.dumps(snapshot,indent=2)+'\n',encoding='utf-8')
