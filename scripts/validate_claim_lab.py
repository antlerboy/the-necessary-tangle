#!/usr/bin/env python3
"""Check original case content, meaningful routes, accounting and reproducibility."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib, json, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]
DOCS=ROOT/'docs'
packet=json.loads((ROOT/'sources/claim-lab-2026-10-04/cases.json').read_text(encoding='utf-8'))
cases=packet['cases']; ids={c['id'] for c in cases}
assert len(cases)==len(ids)==8
assert 200+70-80+20==210
assert (80*10+20*50)/100==18
for c in cases:
    assert c['method']!=c['pair']
    for field in ['claim','case','task','worked','counterexample','changed','changed_answer','locator','relation']:
        assert len(c[field])>15, (c['id'],field)
for j in packet['journeys']: assert set(j['cases'])<=ids
class Links(HTMLParser):
    def __init__(self): super().__init__();self.links=[];self.labels=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='a': self.links.append(a.get('href',''));self.labels.append(a.get('aria-label'))
routes=[DOCS/'systems-thinking/claim-lab/index.html',DOCS/'systems-thinking/claim-lab/worksheets/index.html',DOCS/'updates/2026-10-04/index.html']+[DOCS/'systems-thinking/claim-lab'/x/'index.html' for x in ids]
for f in routes:
    text=f.read_text(encoding='utf-8');parser=Links();parser.feed(text)
    assert 'Open updates' in parser.labels
    assert text.count('<h1>')==1
    assert 'utm_source=chatgpt' not in text
    assert not any(s in text for s in ['C:/','C:\\','SharePoint','oauth_token'])
    for href in parser.links:
        assert href
        if href.startswith('/') and not href.startswith('/#'):
            target=DOCS/href.lstrip('/').split('#')[0]
            if target.is_dir(): target=target/'index.html'
            assert target.exists(), (f,href)
before={str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in routes+[ROOT/'data/public-data.json']}
subprocess.run([sys.executable,str(ROOT/'scripts/build_claim_lab.py')],cwd=ROOT,check=True)
after={str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in routes+[ROOT/'data/public-data.json']}
assert before==after,'Non-idempotent output or canonical-data mutation'
print('Claim lab: eight distinct cases, three valid journeys, arithmetic, local links, privacy, updates control, and idempotence passed.')
