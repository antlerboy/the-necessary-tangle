"""Check source depth, usable reading routes, and reversible release generation."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote, parse_qs
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile

R = Path(__file__).resolve().parents[1]
D = R / 'docs'
MARK = 'depth_20261029'
data = json.loads((R / 'data/public-data.json').read_text(encoding='utf-8'))
assert data['meta']['release'] == '0.35'
assert MARK in data and data[MARK]['originals'], 'Keep the records needed for historical reconstruction'

def values(row, key):
    value = row.get(key, [])
    return json.loads(value) if isinstance(value, str) and value else value or []

node_ids = {row['id'] for row in data['nodes']}
source_ids = {row['id'] for row in data['sources']}
evidence_ids = {row['id'] for row in data['evidence']}
journey_ids = {row['id'] for row in data['journeys']}
relation_types = {row['relation_type'] for row in data['relation_types']}
edges = [row for row in data['edges'] if row.get('connection_pass') == MARK]
profiles = [row for row in data['profiles'] if row.get('connection_pass') == MARK]
assert edges and profiles, 'This release must deepen the maintained graph and profiles'
for row in edges:
    assert row['source'] in node_ids and row['target'] in node_ids, row['id']
    assert row['relation_type'] in relation_types, row['id']
    assert row['relation_type'] not in {'conceptually_related_to', 'legacy_association_unspecified', 'associated_with'}, row['id']
    assert values(row, 'source_ids') and set(values(row, 'source_ids')) <= source_ids, row['id']
    assert set(values(row, 'evidence_ids')) <= evidence_ids, row['id']
    for key in ['source_locator', 'scope_conditions', 'plain_phrase', 'public_review_label']:
        assert row.get(key, '').strip(), (row['id'], key)
    assert row.get('directed') in [True, 'true'], row['id']
for row in profiles:
    assert row['node_id'] in node_ids
    assert values(row, 'source_ids') and set(values(row, 'source_ids')) <= source_ids
    assert set(values(row, 'evidence_ids')) <= evidence_ids
for row in data['sources']:
    if row.get('connection_pass') == MARK:
        assert urlsplit(row['url']).scheme in {'http', 'https'}, row['id']
        assert row.get('title') and row.get('source_locator'), row['id']
for row in data['evidence']:
    if row.get('connection_pass') == MARK:
        assert row['source_id'] in source_ids and row['locator'] and row['excerpt_or_summary'], row['id']
for row in data['journeys']:
    if row.get('connection_pass') == MARK:
        assert row['steps'] and all(step['node_id'] in node_ids and step['narrative'] for step in row['steps'])

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.links, self.ids, self.headings = [], set(), []
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            assert attrs['id'] not in self.ids, 'Duplicate HTML ID: ' + attrs['id']
            self.ids.add(attrs['id'])
        if tag == 'a':
            assert attrs.get('href'), 'Navigation must be a usable link'
            self.links.append(attrs['href'])
        if tag in {'h1', 'h2', 'h3', 'h4', 'h5', 'h6'}:
            self.headings.append(int(tag[1]))

routes = ['reading/connections', 'updates/2026-10-29']
pages = {}
for route in routes:
    path = D / route / 'index.html'
    text = path.read_text(encoding='utf-8')
    page = Page(text)
    pages[route] = page
    assert page.headings.count(1) == 1 and all(b <= a + 1 for a, b in zip(page.headings, page.headings[1:])), route
    assert 'aria-label="Open updates"' in text, route
    for forbidden in ['graph.microsoft', 'mail.google', 'file://', 'sandbox:', 'redquadrantltd']:
        assert forbidden not in text, (route, forbidden)
    for href in page.links:
        url = urlsplit(href)
        if url.scheme or url.netloc:
            continue
        target = (D / unquote(url.path.lstrip('/'))) if url.path.startswith('/') else (path.parent / unquote(url.path))
        if target.is_dir():
            target /= 'index.html'
        assert target.is_file(), (route, href)
        fragment = parse_qs(url.fragment)
        if fragment.get('view') == ['item']:
            assert fragment.get('id', [''])[0] in node_ids, href
        elif fragment.get('view') == ['journeys'] and 'id' in fragment:
            assert fragment['id'][0] in journey_ids, href
        elif url.fragment and not fragment.get('view'):
            assert unquote(url.fragment) in Page(target.read_text(encoding='utf-8')).ids, href
assert {'regulation', 'learning', 'transduction'} <= pages['reading/connections'].ids

assert json.loads((D / 'assets/public-data.json').read_text(encoding='utf-8')) == data, 'Canonical and reader data disagree'
from apply_release_21 import COMPARATOR_SHA256, RECONCILIATION_SHA256
for name, expected in [('comparator-systemic-evolution.json', COMPARATOR_SHA256), ('systemic-evolution-reconciliation.json', RECONCILIATION_SHA256)]:
    assert hashlib.sha256((R / 'data' / name).read_bytes()).hexdigest() == expected

# Run baseline reconstruction against a disposable copy, never the working data.
with tempfile.TemporaryDirectory(prefix='tangle-release-35-') as temp:
    temporary = Path(temp)
    for folder in ['scripts', 'data', 'docs']:
        (temporary / folder).mkdir()
    for relative in ['scripts/prepare_update_35_baseline.py', 'data/public-data.json', 'docs/index.html']:
        shutil.copy2(R / relative, temporary / relative)
    subprocess.run([sys.executable, str(temporary / 'scripts/prepare_update_35_baseline.py')], check=True)
    restored = json.loads((temporary / 'data/public-data.json').read_text(encoding='utf-8'))
    assert MARK not in restored
    for key in ['nodes', 'profiles', 'sources', 'edges', 'evidence', 'claims', 'journeys']:
        identity = 'node_id' if key == 'profiles' else 'id'
        lookup = {row[identity]: row for row in restored[key]}
        assert all(row.get('connection_pass') != MARK for row in restored[key])
        assert all(lookup.get(row[identity]) == row for row in data[MARK]['originals'].get(key, [])), key

paths = [R / 'data/public-data.json', D / 'assets/public-data.json', D / 'index.html', *[D / route / 'index.html' for route in routes]]
def hashes():
    return [hashlib.sha256(path.read_bytes()).hexdigest() for path in paths]
before = hashes()
subprocess.run([sys.executable, 'scripts/apply_update_35.py'], cwd=R, check=True)
assert before == hashes(), 'Release 0.35 application is not idempotent'
print(f'0.35 passed: {len(edges)} scoped connections, {len(profiles)} deepened profiles, source and evidence integrity, internal links, original-record restoration, protected comparator hashes, and idempotence.')
