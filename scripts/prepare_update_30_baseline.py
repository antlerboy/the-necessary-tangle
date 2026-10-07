"""Remove only release 0.30 before historical gates."""
from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
p=root/'data/public-data.json';d=json.loads(p.read_text())
for key in ['nodes','profiles','sources','edges','evidence','claims']:
    d[key]=[r for r in d[key] if r.get('connection_pass')!='update_20261007']
d.pop('update_20261007',None)
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
