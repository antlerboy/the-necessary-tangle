"""Restore the pre-0.35 records before the historical release validation chain."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
MARK = 'depth_20261029'
path = ROOT / 'data/public-data.json'
data = json.loads(path.read_text(encoding='utf-8'))
originals = data.get(MARK, {}).get('originals', {})

for key in ['nodes', 'profiles', 'sources', 'edges', 'evidence', 'claims', 'journeys']:
    identity = 'node_id' if key == 'profiles' else 'id'
    saved = {row[identity]: row for row in originals.get(key, [])}
    restored = [saved.get(row[identity], row) for row in data.get(key, [])]
    present = {row[identity] for row in restored}
    restored.extend(row for row_id, row in saved.items() if row_id not in present)
    data[key] = [row for row in restored if row.get('connection_pass') != MARK]

data.pop(MARK, None)
path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
path = ROOT / 'docs/index.html'
path.write_text(path.read_text(encoding='utf-8').replace('Release 0.35', 'Release 0.34'), encoding='utf-8')
