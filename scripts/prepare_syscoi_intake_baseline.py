#!/usr/bin/env python3
"""Remove only this generated projection before historical release assertions."""
import json
import shutil
from build_syscoi_intake import ROOT, OWNER
from refresh_graph_snapshot import write

path = ROOT / 'data/public-data.json'
data = json.loads(path.read_text(encoding='utf-8'))
data['sources'] = [s for s in data['sources'] if s.get('intake_owner') != OWNER]
data.pop('syscoi_intake', None)
data['meta'].pop('latest_syscoi_intake_url', None)
data['meta']['source_count'] = len(data['sources'])
data['meta']['public_link_source_count'] = sum(s.get('public_link_status') == 'public_link' for s in data['sources'])
write(data)
generated = ROOT / 'docs/library/syscoi'
if generated.exists():
    shutil.rmtree(generated)
print('Staged continuous SysCoI source projection out of historical validation; manifest retained.')
