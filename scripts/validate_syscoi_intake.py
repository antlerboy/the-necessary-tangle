#!/usr/bin/env python3
"""Check the new ingestion boundary, reconciliation, and unchanged-run behaviour."""
import copy
import json
from pathlib import Path
from build_syscoi_intake import ROOT, MANIFEST, OWNER, PROTECTED, canonical_url, projection, reconcile, validate_manifest
from merge_syscoi_intake import merge

manifest = json.loads(MANIFEST.read_text(encoding='utf-8'))
data = json.loads((ROOT / 'data/public-data.json').read_text(encoding='utf-8'))
catalogue = json.loads((ROOT / 'docs/library/catalogue.json').read_text(encoding='utf-8'))
after, cat_after, intake = projection(manifest, data, catalogue)
assert after == data and cat_after == catalogue, 'Projection is not idempotent'
assert merge(manifest, manifest['posts']) == manifest, 'Unchanged input rewrote the manifest'
assert len({r['id'] for r in data['sources']}) == len(data['sources']), 'Duplicate source IDs'
assert len({r['id'] for r in catalogue['records']}) == len(catalogue['records']), 'Duplicate catalogue IDs'
assert canonical_url('http://www.example.org/read/?utm_source=mail&x=1#section') == canonical_url('https://example.org/read?x=1')
assert len(intake['posts']) == len(manifest['posts'])
assert intake['atlas_nodes_added'] == intake['graph_edges_added'] == 0
page = (ROOT / 'docs/library/syscoi/index.html').read_text(encoding='utf-8')
assert 'aria-label="Open updates"' in page
download = json.loads((ROOT / 'docs/library/syscoi/intake.json').read_text(encoding='utf-8'))
assert download['manifest_sha256'] == intake['manifest_sha256']
for post in manifest['posts']:
    assert f'id="post-{post["post_id"]}"' in page
    assert post['content_sha256'] in {p['content_sha256'] for p in download['posts']}
    assert f'src_syscoi_post_{post["post_id"]}' in {s['id'] for s in data['sources']}

# A repeated discovery with tracking parameters gets another provenance row,
# while retaining one resource and leaving every graph field unchanged.
sample = copy.deepcopy(next(p for p in manifest['posts'] if p['post_id'] == 29411))
sample['post_id'] = max(p['post_id'] for p in manifest['posts']) + 1000000
sample['primary_url'] += '?utm_source=duplicate-test'
extra = merge(manifest, [sample])
expanded, expanded_cat, extra_intake = projection(extra, data, catalogue)
assert extra_intake['resource_count'] == intake['resource_count']
assert len(expanded_cat['records']) == len(catalogue['records'])
assert len(expanded['sources']) == len(data['sources']) + 1
for key in PROTECTED:
    assert expanded[key] == data[key], key
for source in data['sources']:
    assert next(s for s in expanded['sources'] if s['id'] == source['id']) == source

# A post revision retains its identity and history.
changed = copy.deepcopy(manifest['posts'][0])
changed['content_sha256'] = '0' * 64
changed['modified_local'] = '2026-11-08T00:00:00'
changed['versions'] = [{'modified_local': changed['modified_local'], 'content_sha256': changed['content_sha256'], 'observed_at': '2026-11-08'}]
revised = merge(manifest, [changed])
assert len(revised['posts']) == len(manifest['posts'])
assert len(next(p for p in revised['posts'] if p['post_id'] == changed['post_id'])['versions']) == len(manifest['posts'][0]['versions']) + 1
for bad_kind in ('draft', 'password', 'duplicate'):
    bad = copy.deepcopy(manifest)
    if bad_kind == 'draft': bad['posts'][0]['status'] = 'draft'
    elif bad_kind == 'password': bad['posts'][0]['password_protected'] = True
    else: bad['posts'].append(copy.deepcopy(bad['posts'][0]))
    try:
        validate_manifest(bad)
    except AssertionError:
        pass
    else:
        raise AssertionError('Unsafe/duplicate record accepted: ' + bad_kind)
orourke = next(p for p in intake['posts'] if p['post_id'] == 29386)
assert orourke['resource_id'] == 'cybernetic_reading_orourke'
assert 'publication_syscoi_post_29183' in orourke['existing_node_ids']
assert sum(r['id'] == 'cybernetic_reading_orourke' for r in catalogue['records']) == 1

# Multiple candidate identities require an explicit reconciliation. An
# incidental citation among outbound links must never identify its citing work.
ambiguous_cat = copy.deepcopy(catalogue)
for ident in ('unrelated_a', 'unrelated_b'):
    ambiguous_cat['records'].append({'id': ident, 'url': 'https://worrydream.com/LadderOfAbstraction/', 'title': ident})
_, resolutions = reconcile(manifest, data, ambiguous_cat)
ambiguous = next(p for p in resolutions if p['post_id'] == 29411)
assert ambiguous['resource_id'] == 'resource_syscoi_post_29411'
assert ambiguous['identity_status'] == 'ambiguous_existing_matches'
assert ambiguous['existing_catalogue_ids'] == []
assert ambiguous['match_candidates']['catalogue_ids'] == ['unrelated_a', 'unrelated_b']
citing_data = copy.deepcopy(data)
citing_data['sources'].append({'id': 'incidental_citation', 'url': 'https://example.org/a-different-work', 'original_urls': '["https://worrydream.com/LadderOfAbstraction/", "https://example.org/another-reference"]', 'source_role': 'discovery provenance'})
_, resolutions = reconcile(manifest, citing_data, catalogue)
cited = next(p for p in resolutions if p['post_id'] == 29411)
assert cited['resource_id'] == 'resource_syscoi_post_29411'
assert cited['existing_source_ids'] == []
assert 'incidental_citation' in cited['match_candidates']['source_ids']
print('SysCoI intake passed: public boundary, whole-register reconciliation, preserved graph/source records, version merge, and idempotence.')
