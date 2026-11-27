#!/usr/bin/env python3
"""Validate the finite source-led cohort, provenance, preservation, and replay."""
import copy
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

from apply_first_pass_depth_44 import ROOT, DOCS, PACKET, MARK, restore
from apply_iteration_17 import parse
from reconcile_feedback_observations import restore as restore_observations


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


packet=json.loads(PACKET.read_text(encoding='utf-8'))
data=json.loads((ROOT/'data/public-data.json').read_text(encoding='utf-8'))
data=restore_observations(data)
assert data['meta']['release']=='0.44'
cohort=set(packet['cohort'])
assert len(cohort)==len(packet['entries'])==84
assert {entry['node_id'] for entry in packet['entries']}==cohort
nodes={row['id']:row for row in data['nodes']}
profiles={row['node_id']:row for row in data['profiles']}
sources={row['id']:row for row in data['sources']}
evidence={row['id']:row for row in data['evidence']}
relations={row['relation_type'] for row in data['relation_types']}
new_edges=[row for row in data['edges'] if row.get('connection_pass')==MARK]
assert len(new_edges)>=84
assert not [row['id'] for row in data['nodes'] if row.get('public_visibility')=='public' and 'first-pass entry' in ' '.join(str(x) for x in row.values()).lower()]
assert all(len({row.get('id') for row in data[key]})==len(data[key]) for key in ['nodes','edges','sources','evidence'])
private=re.compile(r'(?i)(sharepoint|graph\.microsoft|mail\.google|gmail|sandbox:/|file://|localhost|127\.0\.0\.1|\b[a-z]:[\\/]|[?&](?:token|sig|access_token)=)')
assert not private.search(PACKET.read_text(encoding='utf-8')), 'Private provenance must stay outside the public packet'

for entry in packet['entries']:
    nid=entry['node_id']; profile=profiles[nid]
    assert nodes[nid]['publication_level']=='profile'
    assert profile['review_status']==nodes[nid]['review_status']=='research_pass_needs_editor'
    assert not profile.get('reviewed_by') and not nodes[nid].get('reviewed_by')
    texts=[profile.get(key,'') for key in ['canonical_definition','summary','why_it_matters','key_distinctions','historical_lineage','logical_antecedents','dependent_subsequents','practice_connections','common_misreadings']]
    assert len(' '.join(texts).split())>=200, nid+' lacks substantive exposition'
    assert len(profile.get('canonical_definition','').split())>=12, nid
    assert parse(profile['source_ids']) and parse(profile['evidence_ids'])
    assert len({row['target'] if row['source']==nid else row['source'] for row in new_edges if nid in [row['source'],row['target']]})>=1
    assert any(nid in [row['source'],row['target']] and row['relation_family'] not in ['classification','evidence','documentary','legacy'] for row in new_edges), nid+' needs a substantive connection'
    for sid in parse(profile['source_ids']):assert sid in sources
    for eid in parse(profile['evidence_ids']):
        assert eid in evidence and evidence[eid]['source_id'] in sources
        assert len(evidence[eid].get('locator','').strip())>=5
    route=DOCS/'entries'/nid
    record=json.loads((route/'record.json').read_text(encoding='utf-8'))
    assert record['release']=='0.44' and record['entry']['id']==nid
    assert record['profile']['summary']==profile['summary']
    html=(route/'index.html').read_text(encoding='utf-8')
    assert 'Sources and passage locators' in html and 'Review status' in html
    assert '<script' not in html and 'aria-label="Open updates"' in html
    assert all('excerpt_or_summary' not in row for row in record['evidence_locators'])

for edge in new_edges:
    assert edge['source'] in nodes and edge['target'] in nodes
    assert edge['relation_type'] in relations and edge['relation_type']!='legacy_association_unspecified'
    assert edge['relation_family'] not in ['classification','evidence','legacy']
    assert edge['claim_status']=='candidate' and not edge.get('reviewed_by')
    assert edge['scope_conditions'] and edge['source_locator'] and edge['plain_phrase']
    assert all(sid in sources for sid in parse(edge['source_ids']))
    assert parse(edge['evidence_ids']) and all(eid in evidence for eid in parse(edge['evidence_ids']))

# Every original row is retained verbatim by reversal; every new row is removed.
baseline=restore(copy.deepcopy(data))
assert MARK not in baseline
for key,field in [('nodes','id'),('profiles','node_id'),('sources','id'),('evidence','id'),('edges','id')]:
    restored={row[field]:row for row in baseline[key]}
    for row in data[MARK]['originals'][key]:assert restored[row[field]]==row
    assert not any(row.get('connection_pass')==MARK for row in baseline[key])
    current={row[field]:row for row in data[key]}
    for ident,row in restored.items():
        if key=='nodes' and ident in cohort:continue
        if key=='profiles' and ident in cohort:continue
        assert current[ident]==row, f'Historical {key} changed: {ident}'
assert set(nodes)=={row['id'] for row in baseline['nodes']}, 'No new or removed entry IDs'
assert len(baseline['edges'])+len(new_edges)==len(data['edges'])
assert len(profiles)==len(baseline['profiles'])+84-len(data[MARK]['originals']['profiles'])
assert set(data['canonical_redirects'])==set(baseline['canonical_redirects'])
edition=json.loads((DOCS/'reader-edition.json').read_text(encoding='utf-8'))
assert edition['reader_release']==edition['graph_release']=='0.44'
assert 'data-reader-release="0.44"' in (DOCS/'index.html').read_text(encoding='utf-8')
assert '<article id="v0-44">' in (DOCS/'versions/index.html').read_text(encoding='utf-8')

# A second application must reproduce the source, records, release, and home.
# The observation report is a separate final overlay, reversed before replay.
subprocess.run([sys.executable,'scripts/reconcile_feedback_observations.py','--reverse'],cwd=ROOT,check=True)
files=[ROOT/'data/public-data.json', DOCS/'index.html',DOCS/'reader-edition.json',DOCS/'entries/manifest.json',DOCS/'entries/developed-records.json',ROOT/'documentation/NEXT_WORK.md']
before={str(path):digest(path) for path in files}
subprocess.run([sys.executable,'scripts/apply_first_pass_depth_44.py','--reverse'],cwd=ROOT,check=True)
actual_baseline=json.loads((ROOT/'data/public-data.json').read_text(encoding='utf-8'))
assert actual_baseline==baseline, 'CLI reversal must restore the exact graph baseline'
subprocess.run([sys.executable,'scripts/apply_first_pass_depth_44.py'],cwd=ROOT,check=True)
assert before=={str(path):digest(path) for path in files}, '0.44 must apply without drift'
subprocess.run([sys.executable,'scripts/reconcile_feedback_observations.py'],cwd=ROOT,check=True)
print(f'0.44 validated: 84 complete profiles, {len(new_edges)} located candidate connections, 0 catalogue placeholders, unchanged IDs and historical rows, public provenance, deterministic replay.')
