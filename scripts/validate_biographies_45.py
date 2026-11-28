#!/usr/bin/env python3
"""Check the finite biography cohort, identity continuity, and reversible graph.

--self-test validates an in-memory 0.45 application against the checked 0.44
baseline without changing the maintained graph or generated reader files.
"""
import argparse
import copy
import hashlib
import json
import re
import subprocess
import unicodedata

from apply_biographies_45 import (ROOT, DOCS, PACKET, MARK, DATE, RELEASE,
                                  ROW_KEYS, apply_packet, fingerprint, load,
                                  resolve, restore)
from apply_iteration_17 import parse
from build_readable_atlas import structured
from apply_relational_depth_16 import calculate_relational_depth
from refresh_graph_snapshot import calculate
from reconcile_feedback_observations import restore as restore_observations

TEXT_FIELDS = ['canonical_definition', 'summary', 'why_it_matters', 'key_distinctions',
               'historical_lineage', 'logical_antecedents', 'dependent_subsequents',
               'practice_connections', 'common_misreadings']
PRIVATE = re.compile(r'(?i)(sharepoint|graph\.microsoft|mail\.google|sandbox:/|file://|localhost|127\.0\.0\.1|\b[a-z]:[\\/]|[?&](?:token|sig|access_token)=)')
FIRST_PASS = re.compile(r'(?i)first[ -_]pass')
EXCLUDED = {'classification', 'evidence', 'documentary', 'legacy'}


def count_words(profile):
    text = []
    for key in TEXT_FIELDS:
        value = profile.get(key, '')
        text.extend(parse(value) if key not in {'canonical_definition', 'summary', 'why_it_matters'} else [value])
    return len(' '.join(str(value) for value in text).split())


def canonical_name(value):
    return ''.join(c for c in unicodedata.normalize('NFKD', value.casefold()) if c.isalnum())


def validate_graph(data, packet):
    assert data['meta']['release'] == RELEASE and data['meta']['generated'] == DATE
    assert data.get(MARK), 'The biography overlay is missing'
    cohort = packet['cohort']
    assert len(cohort) == len(set(cohort)) == len(packet['entries']) == 107
    assert set(cohort) == {entry['node_id'] for entry in packet['entries']}
    assert data[MARK]['cohort'] == cohort
    assert not packet['human_editorial_acceptance_changed'] and not data[MARK]['human_editorial_acceptance_changed']
    assert not PRIVATE.search(json.dumps(packet, ensure_ascii=False)), 'Private provenance in the public packet'
    baseline = restore(copy.deepcopy(data))
    before = {key: {row[field]: row for row in baseline[key]} for key, field in ROW_KEYS}
    rows = {key: {row[field]: row for row in data[key]} for key, field in ROW_KEYS}
    for key, field in ROW_KEYS:
        assert len(rows[key]) == len(data[key]), 'Duplicate ID in ' + key
    nodes, profiles, sources, evidence = (rows[key] for key in ['nodes', 'profiles', 'sources', 'evidence'])
    redirects = data.get('canonical_redirects', {})
    targets = {resolve(nid, redirects) for nid in cohort}
    public_ids = {nid for nid, node in nodes.items() if node.get('public_visibility') == 'public' and resolve(nid, redirects) == nid}
    types = {row['relation_type']: row for row in data['relation_types']}
    new_edges = [edge for edge in data['edges'] if edge.get('connection_pass') == MARK]
    assert len(new_edges) == data[MARK]['counts']['edges']
    assert set(data[MARK]['identity_redirects'].items()) == set(packet['identity_redirects'].items())
    assert data[MARK]['counts']['canonical_people'] == len(targets)
    assert data[MARK]['counts']['identity_redirects'] == len(packet['identity_redirects'])
    for entry in packet['entries']:
        nid = entry['node_id']; target = resolve(nid, redirects)
        assert nid in nodes and target in public_ids and target in profiles, nid
        node, profile = nodes[target], profiles[target]
        assert nodes[nid]['canonical_id'] == target and node['canonical_id'] == target, nid
        assert node['label'] == entry['node_patch']['label'], nid
        assert count_words(profile) >= 200 and len(profile['canonical_definition'].split()) >= 12, nid
        assert profile['review_status'] == 'research_pass_needs_editor', nid
        assert profile.get('profile_status') == 'source_scoped_research_pass', nid
        catalogue_review = target != nid and before['nodes'][target].get('reviewed_by')
        if catalogue_review:
            for key in ['review_status', 'reviewed_by', 'reviewed_at']:
                assert node.get(key, '') == before['nodes'][target].get(key, ''), (nid, 'Prior catalogue review changed', key)
        else:
            assert node['review_status'] == 'research_pass_needs_editor', nid
        for row in [nodes[nid], profile] if catalogue_review else [nodes[nid], node, profile]:
            assert not row.get('reviewed_by') and not row.get('reviewed_at'), nid
        for row in [nodes[nid], node]:
            assert row['publication_level'] == 'profile', nid
            assert not FIRST_PASS.search(' '.join([str(row.get(k, '')) for k in ['description', 'public_stub_text', 'review_status', 'publication_level', 'set_tags']])), nid
        assert parse(profile.get('source_ids')) and parse(profile.get('evidence_ids')), nid
        for sid in parse(profile['source_ids']):
            assert sid in sources, (nid, sid)
        for eid in parse(profile['evidence_ids']):
            assert eid in evidence and evidence[eid]['source_id'] in sources, (nid, eid)
            assert len(evidence[eid].get('locator', '').strip()) >= 5, eid
        assert any(sid.startswith('src_bio45_') for sid in parse(profile['source_ids'])), nid
        assert any(target in [edge['source'], edge['target']] and edge['relation_family'] not in EXCLUDED for edge in new_edges), nid + ': no new substantive connection'
        same_name = {ident for ident in public_ids if canonical_name(nodes[ident]['label']) == canonical_name(node['label'])}
        assert same_name == {target}, (nid, 'Duplicate canonical name', same_name)
    for edge in new_edges:
        assert edge['source'] in public_ids and edge['target'] in public_ids and edge['source'] != edge['target'], edge['id']
        assert edge['relation_type'] in types and edge['relation_type'] not in {'related_to', 'legacy_association_unspecified', 'authored_by'}, edge['id']
        assert edge['relation_family'] == types[edge['relation_type']]['relation_family'], edge['id']
        assert edge['claim_status'] == 'candidate' and edge['review_status'] == 'research_pass_needs_editor', edge['id']
        assert not edge.get('reviewed_by') and not edge.get('reviewed_at'), edge['id']
        assert all(edge.get(key, '').strip() for key in ['scope_conditions', 'source_locator', 'plain_phrase']), edge['id']
        assert parse(edge['source_ids']) and all(sid in sources for sid in parse(edge['source_ids'])), edge['id']
        assert parse(edge['evidence_ids']) and all(eid in evidence for eid in parse(edge['evidence_ids'])), edge['id']
    assert not any(edge['source'] in redirects or edge['target'] in redirects for edge in data['edges']), 'Alias endpoint survived canonicalisation'
    assert calculate(data) == data['graph_snapshot'], 'Stale graph snapshot'
    expected_depth = calculate_relational_depth(data)
    expected_depth.update(release=RELEASE, generated=DATE)
    assert expected_depth == data['relational_depth'], 'Stale relational depth'
    meta = data['meta']
    assert meta['public_entry_count'] == meta['described_entry_count'] == meta['surprise_me_eligible_count'] == len(public_ids)
    assert meta['profile_count'] == len(set(profiles) & public_ids)
    assert meta['node_count'] == len(nodes) and meta['edge_count'] == len(data['edges'])
    assert meta['source_count'] == len(sources) and meta['evidence_count'] == len(evidence)

    # Exact reversal preserves every old row, and application is deterministic.
    assert fingerprint(baseline) == data[MARK]['baseline_sha256']
    assert baseline['meta']['release'] == '0.44' and MARK not in baseline
    assert apply_packet(baseline, packet) == data, 'Apply after reversal drifted'
    assert apply_packet(data, packet) == data, 'Repeated application drifted'
    assert set(nodes) == set(before['nodes']), 'Entry IDs added or removed'
    for key in ['sources', 'evidence']:
        assert all(rows[key][ident] == row for ident, row in before[key].items()), 'Historical ' + key + ' rewritten'
    original_cohort = set(baseline['first_pass_depth_44']['cohort'])
    assert len(original_cohort) == 84
    for nid in original_cohort:
        assert nodes[nid] == before['nodes'][nid] and profiles[nid] == before['profiles'][nid], '0.44 publication changed: ' + nid
    for ident, edge in before['edges'].items():
        expected = copy.deepcopy(edge)
        for key in ['source', 'target']:
            expected[key] = resolve(expected[key], redirects)
        assert rows['edges'][ident] == expected, 'Historical edge changed beyond identity endpoints: ' + ident
    for entry in packet['entries']:
        nid = entry['node_id']; target = resolve(nid, redirects)
        old = before['nodes'][nid]['label']
        assert old == nodes[target]['label'] or old in parse(nodes[target]['aliases']), nid + ': previous name missing from search aliases'
        prior = before['profiles'].get(target)
        if prior:
            current = profiles[target]
            for key in ['source_ids', 'evidence_ids', 'open_checks']:
                assert set(parse(prior.get(key))) <= set(parse(current.get(key))), (nid, key)
            for key in ['summary', 'why_it_matters']:
                assert not prior.get(key) or prior[key] in current[key], (nid, 'Prior profile text lost', key)
    for name, expected in packet.get('protected_file_sha256', {}).items():
        path = ROOT / name
        assert path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == expected, 'Source-owner-approved file changed: ' + name
    for name, expected in packet.get('protected_normalised_text_sha256', {}).items():
        content = (ROOT / name).read_bytes()
        normalised = re.sub(rb'\r+(?=\n)', b'', content).replace(b'\r', b'\n')
        assert hashlib.sha256(normalised).hexdigest() == expected, 'Protected wrapper content changed: ' + name
    return len(targets), len(new_edges), len(public_ids)


def validate_reader(data, packet):
    assert load(DOCS / 'assets/public-data.json') == load(ROOT / 'data/public-data.json')
    edition = load(DOCS / 'reader-edition.json')
    assert edition['reader_release'] == edition['graph_release'] == RELEASE
    assert 'data-reader-release="0.45"' in (DOCS / 'index.html').read_text(encoding='utf-8')
    assert '<article id="v0-45">' in (DOCS / 'versions/index.html').read_text(encoding='utf-8')
    assert "version: '0.45'" in (ROOT / 'CITATION.cff').read_text(encoding='utf-8')
    assert 'Generated from public release 0.45' in (ROOT / 'documentation/public-knowledge.md').read_text(encoding='utf-8')
    profiles = {row['node_id']: row for row in data['profiles']}
    adventure = load(DOCS / '42/atlas.json')
    assert adventure['graph_release'] == RELEASE
    adventure_nodes = {row['id']: row for row in adventure['nodes']}
    for nid in packet['cohort']:
        target = resolve(nid, data['canonical_redirects'])
        route = DOCS / 'entries' / target
        record = load(route / 'record.json')
        assert record['release'] == RELEASE and record['entry']['id'] == target
        assert record['profile'] == structured(profiles[target]), target
        assert adventure_nodes[target]['summary'] == profiles[target]['summary'], target
        html = (route / 'index.html').read_text(encoding='utf-8')
        assert 'Sources and passage locators' in html and 'Review status' in html
        assert '<script' not in html and 'aria-label="Open updates"' in html
        assert all('excerpt_or_summary' not in ev for ev in record['evidence_locators'])
        if target != nid:
            alias_route = DOCS / 'entries' / nid
            alias = load(alias_route / 'record.json')
            assert alias['release'] == RELEASE and alias['requested_entry_id'] == nid
            assert alias['canonical_entry_id'] == target and alias['redirect']['target'] == target
            alias_html = (alias_route / 'index.html').read_text(encoding='utf-8')
            assert '<link rel="canonical" href="https://transduction.systems/entries/' + target + '/">' in alias_html
            assert '<meta http-equiv="refresh"' in alias_html and '<a href="/entries/' + target + '/">' in alias_html
    subprocess.run(['node', 'scripts/test_random_entry_all.cjs'], cwd=ROOT, check=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    packet = load(PACKET)
    data = restore_observations(load(ROOT / 'data/public-data.json'))
    if args.self_test:
        data = apply_packet(data, packet)
    people, edges, public = validate_graph(data, packet)
    if not args.self_test:
        validate_reader(data, packet)
    print(f'0.45 validated: 107 original person IDs, {people} canonical people, {edges} new located candidate connections, {public} canonical public random-eligible entries; exact reversal and repeat application, preserved 84 publication profiles and source-owner files.')


if __name__ == '__main__':
    main()
