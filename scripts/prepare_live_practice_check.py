#!/usr/bin/env python3
"""Verify the deployed commit over HTTPS and fetch only data needed by browser tests."""
from __future__ import annotations
import hashlib
import json
import os
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BASE='https://transduction.systems'
EXPECTED=os.environ['DEPLOY_COMMIT']
OUT=ROOT/'validation/practice-live'
OUT.mkdir(parents=True,exist_ok=True)

def fetch(route, fresh=True):
    url=BASE+route+('?publication_check='+EXPECTED if fresh else '')
    request=urllib.request.Request(url,headers={'User-Agent':'Necessary-Tangle-publication-check/1.0','Cache-Control':'no-cache'})
    with urllib.request.urlopen(request,timeout=30) as response:
        assert response.status==200,(url,response.status)
        return response.read()

manifest=None
last='No response'
for attempt in range(18):
    try:
        candidate=json.loads(fetch('/deployment.json'))
        if candidate.get('commit')==EXPECTED:
            manifest=candidate
            break
        last='Served commit '+str(candidate.get('commit'))
    except Exception as exc:
        last=str(exc)
    if attempt<17:time.sleep(10)
if manifest is None:raise RuntimeError('Live deployment did not serve the expected commit: '+last)

for route,destination in [('/systems-thinking/practice/assets/pack.json','docs/systems-thinking/practice/assets/pack.json'),('/assets/public-data.json','docs/assets/public-data.json')]:
    payload=fetch(route)
    json.loads(payload)
    path=ROOT/destination;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(payload)
pack=json.loads((ROOT/'docs/systems-thinking/practice/assets/pack.json').read_text())
data=json.loads((ROOT/'docs/assets/public-data.json').read_text())
assert len(pack['labs'])==26
assert data['practice_pack']['lab_count']==26
assert data['meta']['release']==manifest['release']
# Check the ordinary, unqualified URL as readers encounter it, not just a cache-buster.
ordinary=json.loads(fetch('/deployment.json',False))
assert ordinary['commit']==EXPECTED,('Ordinary URL serves another commit',ordinary)
archive=fetch('/systems-thinking/practice/downloads/systems-methods-practice.zip',False)
assert archive[:2]==b'PK' and len(archive)>30000
(OUT/'systems-methods-practice.zip').write_bytes(archive)
result={'status':'passed','checked_at':datetime.now(timezone.utc).isoformat(),'base':BASE,'expected_commit':EXPECTED,'deployment':manifest,'ordinary_url_commit_matches':True,'lab_count':26,'download_bytes':len(archive),'download_sha256':hashlib.sha256(archive).hexdigest()}
(OUT/'deployment-check.json').write_text(json.dumps(result,indent=2)+'\n')
print('LIVE_DEPLOYMENT',json.dumps(result))
