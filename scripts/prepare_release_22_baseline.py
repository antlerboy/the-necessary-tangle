#!/usr/bin/env python3
"""Remove the reproducible 0.22 overlay before historical snapshot validation.

The canonical dataset is cumulative. Earlier gates assert their own release
counts, so current additions must be staged out before running those gates.
Only this overlay's records and the exact prior records it enriches are reset;
the historical builders then reconstruct their maintained baseline.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# The maintained historical HTML is a source snapshot, not a deployed page.
(ROOT / 'docs/index.html').write_bytes((ROOT / 'sources/release-22/reader-base.html').read_bytes())
if '--reader-only' in sys.argv:
    raise SystemExit(0)
path = ROOT / 'data/public-data.json'
data = json.loads(path.read_text())
if 'early_cybernetics_corpus' in data:
    prior = json.loads((ROOT / 'sources/release-22/base-records.json').read_text())
    source_ids = {
        'src_wiener_reading_lists_2026', 'src_barrett_shepard_intro_1951',
        'src_fano_tr65_1949', 'src_ashby_design_brain_1952',
        'src_shannon_weaver_book_1949', 'src_wiener_too_damn_close_1950',
        'src_ashby_archive_equilibrium', 'src_illinois_shannon_weaver',
    }
    removed = {n['id'] for n in data['nodes'] if n.get('inclusion_reason') == 'early_cybernetics_bibliographic_intake_0_22'}
    data['nodes'] = [n for n in data['nodes'] if n['id'] not in removed]
    data['edges'] = [e for e in data['edges'] if not e['id'].startswith('e22_')]
    data['profiles'] = [p for p in data['profiles'] if p['node_id'] not in removed]
    data['sources'] = [s for s in data['sources'] if s['id'] not in source_ids]
    data['journeys'] = [j for j in data['journeys'] if j['id'] not in {'journey_early_cybernetics_reading', 'journey_messages_meaning_action', 'journey_bibliography_boundaries'}]
    data['corpus_register'] = [c for c in data['corpus_register'] if c['id'] != 'early_cybernetics_reading_lists']
    data['relation_types'] = [r for r in data['relation_types'] if r['relation_type'] in prior['existing_relation_types']]
    for key, identity in [('nodes', 'id'), ('profiles', 'node_id')]:
        previous = {r[identity]: r for r in prior[key]}
        data[key] = [previous.get(r[identity], r) for r in data[key]]
    del data['early_cybernetics_corpus']
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    print('Staged the reproducible 0.22 overlay out of historical validation.')
