"""Remove only release 0.34 additions before historical validation."""
from pathlib import Path
import json
R = Path(__file__).resolve().parents[1]
p = R / 'data/public-data.json'
d = json.loads(p.read_text(encoding='utf-8'))
for key in ['nodes', 'profiles', 'sources', 'edges', 'evidence', 'claims']:
    d[key] = [row for row in d[key] if row.get('connection_pass') != 'update_20261024']
d.pop('update_20261024', None)
p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
p = R / 'docs/index.html'
p.write_text(p.read_text(encoding='utf-8').replace('Release 0.34', 'Release 0.33'), encoding='utf-8')
