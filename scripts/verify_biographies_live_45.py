#!/usr/bin/env python3
"""Verify the deployed biography cohort, canonical routes, and readable evidence."""
import concurrent.futures
import json
import os
import re
from datetime import datetime, timezone
from html import unescape
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urlencode

ROOT = Path(__file__).resolve().parents[1]
BASE = os.environ.get('TANGLE_BASE_URL', 'https://transduction.systems').rstrip('/')
PACKET = json.loads((ROOT / 'sources/biographies-107-45/packet.json').read_text(encoding='utf-8'))


def fetch(route, as_json=False):
    separator = '&' if '?' in route else '?'
    url = BASE + route + separator + urlencode({'verify': os.environ.get('DEPLOY_COMMIT', 'biographies-0.45')})
    request = Request(url, headers={'User-Agent': 'Tangle-release-verification/0.45', 'Cache-Control': 'no-cache'})
    with urlopen(request, timeout=60) as response:
        assert response.status == 200, route
        body = response.read().decode('utf-8')
    return json.loads(body) if as_json else body


def main():
    data = fetch('/assets/public-data.json', True)
    edition = fetch('/reader-edition.json', True)
    assert data['meta']['release'] == edition['graph_release'] == edition['reader_release'] == '0.45'
    if os.environ.get('DEPLOY_COMMIT'):
        deployment = fetch('/deployment.json', True)
        assert deployment['commit'] == os.environ['DEPLOY_COMMIT'], 'Live deployment differs from this revision'
    marker = data['biographies_107_45']
    assert set(marker['cohort']) == set(PACKET['cohort']) and len(marker['cohort']) == 107
    redirects = data['canonical_redirects']
    nodes = {n['id']: n for n in data['nodes']}
    profiles = {p['node_id']: p for p in data['profiles']}
    def canonical(ident):
        seen = set()
        while ident in redirects and redirects[ident] != ident:
            assert ident not in seen, 'Canonical cycle'
            seen.add(ident)
            ident = redirects[ident]
        return ident
    targets = sorted({canonical(ident) for ident in PACKET['cohort']})
    assert len(targets) == 107
    for original in PACKET['cohort']:
        target = canonical(original)
        assert nodes[target]['public_visibility'] == 'public'
        assert nodes[original].get('canonical_id') == target
        assert profiles[target]['review_status'] == 'research_pass_needs_editor'
        assert not re.search(r'first[\s_-]*pass', nodes[target]['description'], re.I), target
        assert nodes[original]['review_status'] != 'official_toc_bibliographic_first_pass'
    def check_entry(ident):
        route = '/entries/' + ident + '/'
        html = fetch(route)
        record = fetch(route + 'record.json', True)
        assert record['release'] == '0.45' and record['entry']['id'] == ident
        assert record['profile']['review_status'] == 'research_pass_needs_editor'
        assert record['sources'] and record['evidence_locators']
        assert any(e.get('connection_pass') == 'biographies_107_45' for e in record['connections']), ident
        assert 'dependency-summary' in html and '/dependencies/?entry=' + ident in unescape(html)
        assert 'Sources and passage locators' in html and 'Review status' in html
        assert len(re.findall(r'<h1\b', html)) == 1
        return dict(id=ident, route=route, sources=len(record['sources']), connections=len(record['connections']))
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(check_entry, targets))
    alias_results = []
    for original, target in PACKET['identity_redirects'].items():
        route = '/entries/' + original + '/'
        html = unescape(fetch(route))
        record = fetch(route + 'record.json', True)
        assert 'rel="canonical"' in html and '/entries/' + target + '/' in html
        assert record['requested_entry_id'] == original and record['canonical_entry_id'] == target
        alias_results.append(dict(requested=original, canonical=target, route=route))
    home = fetch('/')
    assert 'dependency-reader-45-model' in home and 'Predecessors and dependents' in home
    reader = fetch('/dependencies/?entry=concept_boundary')
    assert 'dependency-model.js?v=0.45' in reader and 'dependency-reader.js?v=0.45' in reader
    public_ids = {n['id'] for n in data['nodes'] if n.get('public_visibility') == 'public' and canonical(n['id']) == n['id']}
    assert data['meta']['surprise_me_eligible_count'] == len(public_ids)
    report = dict(passed=True, base=BASE, release='0.45', checked_at_utc=datetime.now(timezone.utc).isoformat(),
                  original_records=107, canonical_accounts=len(results), alias_routes=alias_results,
                  counts=marker['counts'], public_canonical_entries=len(public_ids), results=results)
    destination = ROOT / 'validation/biographies-45/live.json'
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Live 0.45 verified: all 107 biographies, five identity redirects, sources, review labels, and the dependency-reader route.')


if __name__ == '__main__':
    main()
