#!/usr/bin/env python3
"""Check publication coverage, provenance, links, and deterministic generation."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib
import json
import subprocess
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
manifest = json.loads((DOCS / 'entries/manifest.json').read_text(encoding='utf-8'))
data = json.loads((DOCS / 'assets/public-data.json').read_text(encoding='utf-8'))
public = {n['id'] for n in data['nodes'] if n.get('public_visibility') == 'public' and data.get('canonical_redirects', {}).get(n['id'], n['id']) == n['id']}
expected = {p['node_id'] for p in data['profiles'] if p['node_id'] in public}
records = json.loads((DOCS / 'entries/developed-records.json').read_text(encoding='utf-8'))
assert {r['entry']['id'] for r in records['records']} == expected
assert manifest['entry_count'] == records['record_count'] == len(expected)
assert manifest['journey_count'] == len(data['journeys'])
site_urls = {e.text for e in ET.parse(DOCS / 'sitemap.xml').getroot().iter() if e.tag.endswith('}loc')}


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.h1 = 0
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'h1':
            self.h1 += 1
        if tag == 'a':
            self.links.append(attrs.get('href', ''))


files = [DOCS / 'index.html', DOCS / 'sitemap.xml', DOCS / 'assets/app.js']
for route in manifest['routes']:
    path = DOCS / route.strip('/') / 'index.html'
    text = path.read_text(encoding='utf-8')
    parser = Links()
    parser.feed(text)
    assert parser.h1 == 1, path
    assert f'https://transduction.systems{route}' in site_urls, route
    assert f'<link rel="canonical" href="https://transduction.systems{route}">' in text
    assert 'aria-label="Open updates"' in text
    assert '<script' not in text, 'Readable content must require no JavaScript'
    for href in parser.links:
        assert href, path
        if href.startswith('/') and not href.startswith('//'):
            local = DOCS / href.split('#')[0].split('?')[0].lstrip('/')
            assert local.exists(), (path, href)
        elif href == 'record.json':
            assert (path.parent / href).exists()
    files.append(path)
for record in records['records']:
    assert record['release'] == data['meta']['release']
    original_profile = next(p for p in data['profiles'] if p['node_id'] == record['entry']['id'])
    assert record['profile'].get('review_status') == original_profile.get('review_status')
    assert record['profile'].get('profile_status') == original_profile.get('profile_status')
    assert isinstance(record['profile'].get('source_ids', []), list)
    assert all(isinstance(edge.get('source_ids', []), list) for edge in record['connections'])
    assert all('excerpt_or_summary' not in e for e in record['evidence_locators'])
    files.append(DOCS / 'entries' / record['entry']['id'] / 'record.json')
files += [DOCS / 'entries/manifest.json', DOCS / 'entries/developed-records.json']
before = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
subprocess.run([sys.executable, str(ROOT / 'scripts/build_readable_atlas.py')], check=True)
assert before == {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in files}, 'Generation must be idempotent'
print(f'Readable atlas validation passed: {len(expected)} entries, {len(data["journeys"])} journeys, all generated internal links, sitemap, status preservation, excerpt exclusion, and idempotence.')
