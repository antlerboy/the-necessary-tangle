#!/usr/bin/env python3
"""Apply the source-led 84-publication release after historical gates.

The graph overlay is reversible and repeatable. --reverse restores the graph
baseline for the historical Makefile replay; subsequent historical generators
restore the reader projections. It isn't a standalone website rollback.
Source-owner reviewed artefacts, acceptance decisions, IDs, and existing
relationships are preserved.
"""
import argparse
import copy
import json
import re
import subprocess
import sys
from html import escape
from pathlib import Path

from apply_iteration_17 import enc, parse, source_record, edge_record, merge_encoded
from apply_iteration_09 import graph_metrics
from apply_doncaster_lineage import refresh_counts
from apply_relational_depth_16 import calculate_relational_depth, write_relational_document
from apply_overnight_review import quality_result
from refresh_graph_snapshot import calculate, write
from build_readable_atlas import main as readable, page
from build_public_knowledge import main as knowledge
from version_history import build as history

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
PACKET = ROOT / 'sources/first-pass-depth-44/packet.json'
MARK = 'first_pass_depth_44'
DATE = '2026-11-27'
RELEASE = '0.44'
ROUTE = '/updates/2026-11-27-first-pass-depth/'
TITLE = '84 papers, beyond the catalogue'


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def replace_marked(path, block='', anchor=None, before=False, marker=MARK):
    text = re.sub(r'<!-- ' + marker + r' -->.*?<!-- /' + marker + r' -->\n?', '', path.read_text(encoding='utf-8'), flags=re.S)
    if block:
        assert anchor in text, str(path)
        marked = '<!-- ' + marker + ' -->\n' + block + '\n<!-- /' + marker + ' -->\n'
        text = text.replace(anchor, marked + anchor if before else anchor + marked, 1)
    path.write_text(text, encoding='utf-8')


def restore(data):
    previous = data.pop(MARK, None)
    if not previous:
        return data
    for key, field in [('nodes', 'id'), ('profiles', 'node_id'), ('sources', 'id'), ('evidence', 'id'), ('edges', 'id')]:
        originals = {row[field]: row for row in previous['originals'][key]}
        data[key] = [copy.deepcopy(originals.get(row[field], row)) for row in data[key]
                     if row.get('connection_pass') != MARK or row[field] in originals]
    for key, value in previous['original_values'].items():
        data[key] = value
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reverse', action='store_true')
    args = parser.parse_args()
    data = load(ROOT / 'data/public-data.json')
    active = MARK in data
    data = restore(data)
    if args.reverse:
        if active:
            write(data)
            (DOCS / 'reader-edition.json').write_text((PACKET.parent / 'previous-reader-edition.json').read_text(encoding='utf-8'), encoding='utf-8')
        for name in ['README.md', 'documentation/TANGLE_STATE.md', 'documentation/NEXT_WORK.md', 'docs/updates/index.html', 'docs/index.html']:
            replace_marked(ROOT / name)
            replace_marked(ROOT / name, marker='random-entry-all')
        return
    packet = load(PACKET)
    cohort = packet['cohort']
    assert len(cohort) == len(set(cohort)) == len(packet['entries']) == 84
    assert set(cohort) == {entry['node_id'] for entry in packet['entries']}
    before_ids = {key: {row['id'] for row in data[key]} for key in ['nodes', 'sources', 'evidence', 'edges']}
    originals = {key: [] for key in ['nodes', 'profiles', 'sources', 'evidence', 'edges']}
    baseline_values = {key: copy.deepcopy(data[key]) for key in ['meta', 'relational_depth', 'graph_snapshot']}

    def put(key, incoming, field='id'):
        prior = next((row for row in data[key] if row[field] == incoming[field]), None)
        if prior:
            originals[key].append(copy.deepcopy(prior))
            prior.update(copy.deepcopy(incoming))
        else:
            data[key].append(copy.deepcopy(incoming))

    for entry in packet['entries']:
        nid = entry['node_id']
        node = copy.deepcopy(next(row for row in data['nodes'] if row['id'] == nid))
        node.update(entry['node_patch'])
        prior_profile = copy.deepcopy(next((row for row in data['profiles'] if row['node_id'] == nid), {}))
        profile = copy.deepcopy(prior_profile)
        profile.update(copy.deepcopy(entry['profile']))
        assert profile['review_status'] == 'research_pass_needs_editor'
        for key, value in list(profile.items()):
            if isinstance(value, list):
                profile[key] = enc(value)
        for key in ['source_ids', 'evidence_ids', 'open_checks']:
            merge_encoded(profile, key, parse(prior_profile.get(key)))
        profile.update(node_id=nid, connection_pass=MARK, profile_status='source_scoped_research_pass',
                       last_researched=DATE, reviewed_by='', reviewed_at='')
        node.update(connection_pass=MARK, publication_level='profile', review_status='research_pass_needs_editor', reviewed_by='', reviewed_at='')
        # Replace every retired catalogue-only placeholder field, preserving its
        # exact historical wording in the reversible baseline above.
        for key, value in list(node.items()):
            if isinstance(value, str) and 'first-pass entry' in value.lower():
                node[key] = profile['canonical_definition'] if key in ['public_stub_text', 'canonical_definition', 'description'] else 'Primary-source account with passage locators; editorial review pending.'
        merge_encoded(node, 'source_ids', parse(profile['source_ids']))
        merge_encoded(node, 'evidence_ids', parse(profile['evidence_ids']))
        node['public_source_count'] = len(parse(node['source_ids']))
        put('nodes', node)
        put('profiles', profile, 'node_id')
        for incoming in entry['sources']:
            sid = incoming['id']
            assert sid not in before_ids['sources'], 'New source IDs must not overwrite historical sources'
            row = source_record(sid, incoming['title'], incoming['source_type'], incoming.get('url', ''), incoming.get('notes', ''), incoming.get('creators', []), incoming.get('publisher', ''), incoming.get('date', ''))
            row.update(connection_pass=MARK, access=incoming.get('access', row['access']), last_checked=DATE,
                       review_status='research_pass_needs_editor', reviewed_by='', reviewed_at='')
            put('sources', row)
        for incoming in entry['evidence']:
            assert incoming['id'] not in before_ids['evidence']
            row = dict(incoming, connection_pass=MARK, quality_tier='A', licence='see_source',
                       public_evidence_status='public', content_hash='', reviewed_by='', reviewed_at='')
            put('evidence', row)
        for incoming in entry['edges']:
            assert incoming['id'] not in before_ids['edges'], 'Historical edges are immutable in this packet'
            row = edge_record(incoming['id'], incoming['source'], incoming['target'], incoming['relation_type'], incoming['relation_family'], incoming['plain_phrase'], incoming['source_ids'], incoming['source_locator'], incoming['scope_conditions'], status='candidate', mode=incoming['assertion_mode'], confidence='not quantified', review_label='Source-scoped proposal; editorial review pending')
            row.update(incoming)
            row.update(source_ids=enc(incoming['source_ids']), evidence_ids=enc(incoming['evidence_ids']),
                       connection_pass=MARK, reviewed_by='', reviewed_at='', review_status='research_pass_needs_editor')
            put('edges', row)

    refresh_counts(data)
    data['relational_depth'] = calculate_relational_depth(data)
    data['relational_depth'].update(release=RELEASE, generated=DATE)
    data['graph_snapshot'] = calculate(data)
    metrics = graph_metrics(data)
    aggregate = data['relational_depth']['aggregate']
    data['meta'].update(release=RELEASE, generated=DATE, release_digest_url='https://transduction.systems' + ROUTE,
                        iteration_focus=TITLE, release_note='84 source-led publication profiles with scoped typed connections; editorial acceptance pending.',
                        node_count=len(data['nodes']), edge_count=len(data['edges']), source_count=len(data['sources']), profile_count=len(data['profiles']),
                        public_entry_count=metrics['public_entries'], described_entry_count=metrics['public_entries'], surprise_me_eligible_count=metrics['public_entries'],
                        reader_connected_entry_count=aggregate['reader_connected_entries'], semantic_connected_entry_count=aggregate['semantic_connected_entries'],
                        unconnected_entry_count=aggregate['connection_bands'].get('unconnected', 0), semantic_gap_entry_count=metrics['public_entries'] - aggregate['semantic_connected_entries'],
                        public_link_source_count=sum(s.get('public_link_status') == 'public_link' for s in data['sources']),
                        no_public_link_source_count=sum(s.get('public_link_status') == 'no_public_link' for s in data['sources']))
    counts = {key: sum(row.get('connection_pass') == MARK for row in data[key]) for key in originals}
    data[MARK] = dict(date=DATE, cohort=cohort, counts=counts, originals=originals, original_values=baseline_values,
                     source_packet='sources/first-pass-depth-44/packet.json', human_editorial_acceptance_changed=False)
    write(data)
    quality = quality_result(data)
    quality.update(release=RELEASE, generated=DATE)
    for key in ['adversarial_review', 'doncaster_lineage_review']:
        quality[key] = data[key]
    for name in ['data/relationship-quality.json', 'docs/assets/relationship-quality.json']:
        (ROOT / name).write_text(json.dumps(quality, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    write_relational_document(data)
    readable()
    knowledge()
    subprocess.run([sys.executable, str(ROOT / 'scripts/build_adventure_42.py'), '--atlas-only'], check=True)

    summary = f"Research release 0.44 develops all 84 remaining publication records carrying the catalogue placeholder, with {counts['edges']} new typed connections and located source evidence. The accounts explain the papers' mechanisms, limits, and connections. Editorial applications are identified; named human acceptance remains pending."
    edition = dict(reader_release=RELEASE, graph_release=RELEASE, date=DATE, title=TITLE, reading_url=ROUTE + '#completed-set',
                   release_url=ROUTE, summary=summary)
    (DOCS / 'reader-edition.json').write_text(json.dumps(edition, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    rows = {node['id']: node for node in data['nodes']}
    listed = '<ol>' + ''.join('<li><a href="/entries/' + nid + '/">' + escape(rows[nid]['label']) + '</a></li>' for nid in cohort) + '</ol>'
    body = '<p>Release 0.44 · 27 November 2026</p><p>' + escape(summary) + '</p><p><a href="' + ROUTE + '#completed-set">Browse the 84 papers</a>.</p><p>This completes the recorded publication placeholder set. The atlas’s other registered research programmes remain open.</p><p>Sources include original publications, author manuscripts, and published reprints. Each entry states its sources and passage locators. The linked works retain their own copyright and terms.</p><h2 id="completed-set">The completed set</h2>' + listed
    destination = DOCS / ROUTE.strip('/')
    destination.mkdir(parents=True, exist_ok=True)
    (destination / 'index.html').write_text(page(TITLE, summary, ROUTE, body, RELEASE), encoding='utf-8')
    for name, anchor, block in [
        ('README.md', '# The Necessary Tangle\n', 'Current research and reader release **0.44, 27 November 2026**. [84 papers, beyond the catalogue](https://transduction.systems' + ROUTE + '). Source-led accounts; editorial review pending.'),
        ('documentation/TANGLE_STATE.md', '# Current Tangle state\n', '## Current research and reader edition 0.44\n\n' + summary + '\n\nThe packet and cohort are in sources/first-pass-depth-44/packet.json. Deployment identity and live checks belong to deployment.json and the Publish workflow. Broader corpus requests remain open.'),
        ('documentation/NEXT_WORK.md', '# Next work\n', '## Current packet: all 84 catalogue placeholders\n\nThe source-led profiles and connections are implemented. Publication status is recorded in the deployment manifest and workflow, not inferred from this build. Human editorial review remains open. Preserve every site-specific unresolved programme in the private feedback register; this finite cohort does not close the full research agenda.'),
        ('docs/updates/index.html', '<main>\n', '<section><h2><a href="' + ROUTE + '">Release 0.44 · ' + TITLE + '</a></h2><p>' + escape(summary) + '</p></section>'),
    ]:
        replace_marked(ROOT / name, block, anchor)
    next_work = ROOT / 'documentation/NEXT_WORK.md'
    next_work.write_text('# Next work\n\n' + (ROOT / 'sources/random-entry-all/packet.md').read_text(encoding='utf-8'), encoding='utf-8')
    replace_marked(ROOT / 'documentation/TANGLE_STATE.md', '## Random-entry coverage correction, 28 November 2026\n\nThe active random-entry handler uses every canonical public entry, independent of status, publication level, entity type, and description length. The current graph has 1,295 such entries. The prior 84-entry work covered publications only; 107 person records still retain first-pass status without developed profiles, including 105 placeholder descriptions. Their source-led development remains open. The running feedback instruction must not be marked complete from the publication-only count. Deployment identity and live checks remain in the publication workflow and manifest.', '# Current Tangle state\n', marker='random-entry-all')
    for name in ['README.md', 'documentation/TANGLE_STATE.md']:
        path = ROOT / name
        text = path.read_text(encoding='utf-8').replace('Current reader release **0.43', 'Previous reader release **0.43').replace('## Current reader release 0.43', '## Previous reader release 0.43').replace('## Current research edition 0.41', '## Previous research edition 0.41').replace('Current research edition: **0.41', 'Previous research edition: **0.41')
        path.write_text(text, encoding='utf-8')
    home = DOCS / 'index.html'
    text = home.read_text(encoding='utf-8')
    text = re.sub(r'<a id="releaseBadge"[^>]*>Release [^<]+</a>', '<a id="releaseBadge" data-reader-release="0.44" href="/versions/" aria-label="Version history, current release 0.44">Release 0.44</a>', text, count=1)
    text = re.sub(r'assets/public-data.js\?v=[^"\s]+', 'assets/public-data.js?v=0.44-random-all-20261128', text)
    text = re.sub(r'assets/iteration-18.js\?v=[^"\s]+', 'assets/iteration-18.js?v=random-all-20261128', text)
    measures = [(metrics['public_entries'], 'readable public entries'), (aggregate['reader_connected_entries'], 'with reader connections'), (aggregate['connection_bands'].get('rich', 0) + aggregate['connection_bands'].get('developing', 0), 'developing or rich'), (aggregate['reader_statements'], 'reader relationship statements')]
    pattern = r'<div class="metrics" id="homeMetrics"[^>]*>(?:\s*<div class="metric">.*?</div>){4}\s*</div>'
    match = re.search(pattern, text, flags=re.S)
    assert match, 'Homepage metric structure changed'
    metrics_html = ''.join('<div class="metric"><strong>' + str(number) + '</strong><span>' + label + '</span></div>' for number, label in measures)
    text = text[:match.start()] + '<div class="metrics" id="homeMetrics" aria-label="Atlas counts">' + metrics_html + '</div>' + text[match.end():]
    home.write_text(text, encoding='utf-8')
    replace_marked(home, '<section class="resource-pathways plain-panel wide"><h2><a href="' + ROUTE + '">' + TITLE + '</a></h2><p>Read the papers’ arguments, limits, and connections.</p></section>', '<section id="systemsPracticeCallout"', before=True)
    changelog = ROOT / 'CHANGELOG.md'
    text = changelog.read_text(encoding='utf-8')
    if '## 0.44 — ' not in text:
        changelog.write_text(text.replace('# Changelog\n', '# Changelog\n\n## 0.44 — 27 November 2026\n\n' + summary + '\n', 1), encoding='utf-8')
    citation = ROOT / 'CITATION.cff'
    text = re.sub(r'^version:.*$', "version: '0.44'", citation.read_text(encoding='utf-8'), flags=re.M)
    text = re.sub(r'^date-released:.*$', "date-released: '2026-11-27'", text, flags=re.M)
    citation.write_text(text, encoding='utf-8')
    sitemap = DOCS / 'sitemap.xml'
    text = sitemap.read_text(encoding='utf-8')
    if 'https://transduction.systems' + ROUTE not in text:
        sitemap.write_text(text.replace('</urlset>', '<url><loc>https://transduction.systems' + ROUTE + '</loc><lastmod>' + DATE + '</lastmod></url></urlset>'), encoding='utf-8')
    history(ROOT, RELEASE)
    print('Source-led 0.44 applied:', json.dumps(counts, sort_keys=True))


if __name__ == '__main__':
    main()
