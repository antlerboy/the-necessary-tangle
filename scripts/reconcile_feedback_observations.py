#!/usr/bin/env python3
"""Refresh measured observations after historical release validators have run.

This final overlay changes no graph, source, acceptance, or research-release
record. Reverse it before replaying the historical build sequence.
"""
from __future__ import annotations

import argparse
import copy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

from apply_iteration_09 import graph_metrics

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data/public-data.json'
ASSETS = ROOT / 'docs/assets'
PACKET = ROOT / 'data/feedback-observations-2026-11-26.json'
MARKER = 'feedback_observations_overlay'


def graph_identity(data):
    stable = {key: value for key, value in data.items() if key not in ['ai_observations', MARKER]}
    return hashlib.sha256(json.dumps(stable, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def canonical_nodes(data):
    redirects = data.get('canonical_redirects', {})
    return {node['id']: node for node in data['nodes']
            if node.get('public_visibility') == 'public'
            and redirects.get(node['id'], node['id']) == node['id']}


def measurements(data):
    nodes = canonical_nodes(data)
    profile_ids = {profile['node_id'] for profile in data['profiles']} & nodes.keys()
    first_pass = sorted(node['id'] for node in nodes.values()
                        if 'first-pass entry' in ' '.join(str(value) for value in node.values()).lower())
    person_first_pass = sorted(node['id'] for node in nodes.values()
                               if node.get('entity_type') == 'person'
                               and 'first_pass' in node.get('review_status', ''))
    metrics = graph_metrics(data)
    assert metrics['public_entries'] == len(nodes)
    assert metrics['developed_profiles'] == len(profile_ids)
    metrics.update(
        profile_coverage_percent=round(100 * len(profile_ids) / len(nodes), 1) if nodes else 0,
        unprofiled_public_entries=len(nodes.keys() - profile_ids),
        profile_label_entries=sum(node.get('publication_level') == 'profile' for node in nodes.values()),
        literal_first_pass_entries=len(first_pass),
        first_pass_person_review_records=len(person_first_pass),
        total_recorded_edge_rows=len(data['edges']),
    )
    gaps = {'literal_first_pass_entry_ids': first_pass,
            'bibliographic_first_pass_person_ids': person_first_pass,
            'unprofiled_canonical_entry_ids': sorted(nodes.keys() - profile_ids)}
    return metrics, gaps


def write_projection(data):
    rendered = json.dumps(data, ensure_ascii=False, indent=2) + '\n'
    DATA.write_text(rendered, encoding='utf-8')
    (ASSETS / 'public-data.json').write_text(rendered, encoding='utf-8')
    (ASSETS / 'public-data.js').write_text('window.TANGLE_DATA = ' + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + ';\n', encoding='utf-8')


def archive_note(report):
    return f"Retained from the observation report dated {report.get('generated', 'date not stated')} (release {report.get('release', 'not stated')}); not re-reviewed as a current finding. "


def restore(data):
    overlay = data.pop(MARKER, None)
    if overlay:
        data['ai_observations'] = overlay['historical_report']
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reverse', action='store_true')
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--as-of', help='Measurement date, for a reproducible check (YYYY-MM-DD)')
    args = parser.parse_args()
    data = json.loads(DATA.read_text(encoding='utf-8'))
    identity = graph_identity(data)
    packet = json.loads(PACKET.read_text(encoding='utf-8'))
    if args.check:
        overlay = data[MARKER]
        metrics, gaps = measurements(data)
        assert data['ai_observations']['metrics'] == metrics
        assert overlay['gaps'] == gaps
        assert overlay['graph_identity_sha256'] == identity
        assert data['ai_observations']['release'] == data['meta']['release']
        assert len(data['ai_observations']['observations']) == len(packet['observations']) + len(overlay['historical_report']['observations'])
        assert all('Historical record' in item['kind'] for item in data['ai_observations']['observations'][len(packet['observations']):])
        assert json.loads((ASSETS / 'public-data.json').read_text(encoding='utf-8')) == data
        js = (ASSETS / 'public-data.js').read_text(encoding='utf-8')
        assert json.loads(js.removeprefix('window.TANGLE_DATA = ').rstrip().removesuffix(';')) == data
        assert json.loads((ASSETS / 'feedback-observations-current.json').read_text(encoding='utf-8'))['metrics'] == metrics
        assert graph_identity(restore(copy.deepcopy(data))) == identity
        print('Feedback observations checked: current measurements, canonical scope, historical labels, projections, and unchanged graph identity')
        return
    if args.reverse:
        if MARKER in data:
            write_projection(restore(data))
        return
    data = restore(data)
    metrics, gaps = measurements(data)
    measured_on = args.as_of or datetime.now(timezone.utc).date().isoformat()
    datetime.strptime(measured_on, '%Y-%m-%d')
    historical = copy.deepcopy(data['ai_observations'])
    current = [{key: (value.format(**metrics) if isinstance(value, str) else value) for key, value in item.items()}
               for item in packet['observations']]
    retained = []
    note = archive_note(historical)
    for item in historical['observations']:
        entry = copy.deepcopy(item)
        entry['kind'] = 'Historical record · ' + historical.get('generated', 'date not stated')
        entry['measurement'] = note + entry.get('measurement', '')
        entry['interpretation'] = 'Historical interpretation; not re-reviewed in this measurement refresh. ' + entry.get('interpretation', '')
        retained.append(entry)
    data['ai_observations'] = {
        'release': data['meta']['release'], 'generated': measured_on,
        'method_note': f"Measurements recomputed on {measured_on} from the maintained graph, research release {data['meta']['release']} dated {data['meta']['generated']}. The three scope explanations were written on {packet['written_on']}; no new source research or human editorial acceptance is implied. The older observations below are retained as dated historical interpretations, not freshly verified findings.",
        'metrics': metrics, 'observations': current + retained,
    }
    data[MARKER] = {'id': packet['id'], 'measured_on': measured_on,
                    'graph_identity_sha256': identity, 'method': packet['method'],
                    'gaps': gaps, 'historical_report': historical}
    assert graph_identity(data) == identity
    write_projection(data)
    snapshot = {'measured_on': measured_on, 'research_release': data['meta']['release'],
                'research_generated': data['meta']['generated'], 'metrics': metrics,
                'method': packet['method'], 'gaps': gaps,
                'historical_report_date': historical.get('generated'),
                'human_editorial_acceptance_changed': False}
    (ASSETS / 'feedback-observations-current.json').write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    lines = ['# AI observations', '', f"Measurements recomputed {measured_on}; graph research release {data['meta']['release']} dated {data['meta']['generated']}. No research-release or review status changed.", '', data['ai_observations']['method_note'], '', '## Current measured state', '',
             f"- {metrics['public_entries']} canonical public entries; {metrics['developed_profiles']} actual developed profile records; {metrics['unprofiled_public_entries']} canonical entries without one.",
             f"- {metrics['profile_label_entries']} publication-level profile labels, counted separately from actual profile records.",
             f"- {metrics['literal_first_pass_entries']} literal first-pass-entry placeholders; separately, {metrics['first_pass_person_review_records']} bibliographic first-pass person review records.",
             f"- {metrics['typed_edges']} typed public relation rows; {metrics['substantive_edges']} substantive rows; {metrics['substantive_connected_nodes']} substantively connected entries and {metrics['substantive_isolated_nodes']} isolates.",
             f"- {metrics['sources']} source records, including {metrics['sources_with_public_links']} with public links.", '', '[Download current measurements, definitions, and gap entry IDs](https://transduction.systems/assets/feedback-observations-current.json).', '', '## Current scope explanations', '']
    for item in current:
        lines += ['### ' + item['title'], '', '**Measured:** ' + item['measurement'], '', '**Interpretation:** ' + item['interpretation'], '', '**What follows:** ' + item['implication'], '', '**Test:** ' + item['test'], '']
    lines += ['## Historical observations', '', note, '']
    for item in historical['observations']:
        lines += ['### ' + item['title'], '', '**Historical measurement:** ' + item.get('measurement', ''), '', '**Historical interpretation:** ' + item.get('interpretation', ''), '', '**Proposed implication:** ' + item.get('implication', ''), '', '**Proposed test:** ' + item.get('test', ''), '']
    (ROOT / 'documentation/ai-observations.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f"Refreshed feedback observations: {metrics['public_entries']} canonical entries, {metrics['developed_profiles']} profiles, {metrics['literal_first_pass_entries']} literal placeholders; graph and review records unchanged")


if __name__ == '__main__':
    main()
