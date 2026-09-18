"""Remove only this additive packet before running historical release gates."""
from pathlib import Path
import json

root = Path(__file__).resolve().parents[1]
path = root / 'data/public-data.json'
data = json.loads(path.read_text(encoding='utf-8'))
removed = {n['id'] for n in data['nodes'] if n.get('inclusion_reason') == 'source_intake_20260918'}
data['nodes'] = [n for n in data['nodes'] if n['id'] not in removed]
data['profiles'] = [p for p in data['profiles'] if p['node_id'] not in removed]
data['edges'] = [e for e in data['edges'] if not e['id'].startswith('e25_')]
data['sources'] = [s for s in data['sources'] if s.get('connection_pass') != 'source_intake_20260918']
data.pop('source_intake_20260918', None)
data['meta'].pop('latest_intake_url', None)
path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
print('Staged the 18 September additive packet out of historical validation')
