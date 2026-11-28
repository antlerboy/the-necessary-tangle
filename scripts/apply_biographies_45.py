#!/usr/bin/env python3
"""Apply the reversible 107-biography release after the historical 0.44 gate.

Reversal restores the exact graph baseline. Historical build stages regenerate
their own reader outputs; this is not a standalone website rollback.
"""
import argparse
import copy
import hashlib
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
from apply_first_pass_depth_44 import replace_marked
from reconcile_feedback_observations import restore as restore_observations

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
PACKET = ROOT / 'sources/biographies-107-45/packet.json'
MARK = 'biographies_107_45'
DATE = '2026-11-28'
RELEASE = '0.45'
ROUTE = '/updates/2026-11-28-biographies-and-dependencies/'
TITLE = 'People, predecessors, and what follows'
ROW_KEYS = [('nodes', 'id'), ('profiles', 'node_id'), ('sources', 'id'),
            ('evidence', 'id'), ('edges', 'id')]
LIST_FIELDS = {'key_distinctions', 'historical_lineage', 'logical_antecedents',
               'dependent_subsequents', 'practice_connections', 'common_misreadings',
               'open_checks', 'source_ids', 'evidence_ids'}


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def fingerprint(data):
    return hashlib.sha256(json.dumps(data, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def resolve(ident, redirects):
    seen = set()
    while ident in redirects and redirects[ident] != ident:
        assert ident not in seen, 'Cyclic canonical identity'
        seen.add(ident)
        ident = redirects[ident]
    return ident


def restore(data):
    previous = data.pop(MARK, None)
    if not previous:
        return data
    for key, field in ROW_KEYS:
        original = {r[field]: r for r in previous['originals'][key]}
        added = set(previous['added_ids'][key])
        data[key] = [copy.deepcopy(original.get(row[field], row))
                     for row in data[key] if row[field] not in added]
    for key, value in previous['original_values'].items():
        data[key] = copy.deepcopy(value)
    assert fingerprint(data) == previous['baseline_sha256'], 'Graph reversal drift'
    return data


def profile_merge(prior, incoming, target):
    """Keep prior exposition and checks when an identity already has a profile."""
    result = copy.deepcopy(prior)
    for key, value in incoming.items():
        if key in LIST_FIELDS:
            result[key] = enc(list(dict.fromkeys([*parse(prior.get(key)), *parse(value)])))
        elif prior.get(key) and key in ['summary', 'why_it_matters', 'editorial_note', 'context_and_lineage']:
            old = str(prior[key]).strip()
            new = str(value).strip()
            result[key] = old if new == old or new in old else old + '\n\n' + new
        elif key == 'canonical_definition' and len(str(prior.get(key, '')).split()) >= 12:
            result[key] = prior[key]
        else:
            result[key] = copy.deepcopy(value)
    result.update(node_id=target, connection_pass=MARK, review_status='research_pass_needs_editor',
                  profile_status='source_scoped_research_pass', last_researched=DATE,
                  reviewed_by='', reviewed_at='')
    return result


def apply_packet(data, packet):
    data = restore(copy.deepcopy(data))
    baseline = copy.deepcopy(data)
    assert data['meta']['release'] == '0.44', '0.45 follows the checked 0.44 graph'
    cohort = packet['cohort']
    assert len(cohort) == len(set(cohort)) == len(packet['entries']) == 107
    assert set(cohort) == {e['node_id'] for e in packet['entries']}
    redirects = dict(data.get('canonical_redirects', {}))
    redirects.update(packet.get('identity_redirects', {}))
    redirects = {a: resolve(b, redirects) for a, b in redirects.items()}
    data['canonical_redirects'] = redirects
    nodes = {n['id']: n for n in data['nodes']}
    sources = {s['id']: s for s in data['sources']}
    evidence = {v['id']: v for v in data['evidence']}
    profiles = {p['node_id']: p for p in data['profiles']}
    relation_types = {r['relation_type']: r for r in data['relation_types']}
    existing_edges = {e['id'] for e in data['edges']}
    for edge in data['edges']:
        for key in ['source', 'target']:
            edge[key] = resolve(edge[key], redirects)
    for entry in packet['entries']:
        original_id = entry['node_id']
        target = resolve(original_id, redirects)
        assert target in nodes and original_id in nodes
        prior = copy.deepcopy(profiles.get(target, {}))
        profile = profile_merge(prior, entry['profile'], target)
        if target in profiles:
            profiles[target].clear()
            profiles[target].update(profile)
        else:
            data['profiles'].append(profile)
            profiles[target] = profile
        node = nodes[target]
        catalogue_review = ({key: node.get(key, '') for key in ['review_status', 'reviewed_by', 'reviewed_at']}
                            if target != original_id and node.get('reviewed_by') else None)
        old_label = node['label']
        patch = copy.deepcopy(entry['node_patch'])
        aliases = [*parse(node.get('aliases')), old_label, nodes[original_id]['label'],
                   *parse(patch.pop('aliases', []))]
        if prior and node.get('description'):
            patch.pop('description', None)
        node.update(patch)
        node['canonical_definition'] = profile['canonical_definition']
        node['aliases'] = enc([a for a in dict.fromkeys(aliases) if a != node['label']])
        for ident in dict.fromkeys([target, original_id]):
            row = nodes[ident]
            row.update(connection_pass=MARK, canonical_id=target, publication_level='profile',
                       review_status='research_pass_needs_editor', reviewed_by='', reviewed_at='',
                       public_stub_text='')
            if ident == target and catalogue_review:
                row.update(catalogue_review)
            if ident != target:
                row['description'] = node['description']
                row['canonical_definition'] = node['canonical_definition']
            row['set_tags'] = enc([tag for tag in parse(row.get('set_tags'))
                                   if 'first_pass' not in tag and 'first-pass' not in tag])
            merge_encoded(row, 'source_ids', parse(profile['source_ids']))
            merge_encoded(row, 'evidence_ids', parse(profile['evidence_ids']))
        for incoming in entry['sources']:
            sid = incoming['id']
            if sid in sources:
                continue  # Reuse genuine historical source IDs without rewriting them.
            row = source_record(sid, incoming['title'], incoming['source_type'], incoming.get('url', ''),
                                incoming.get('notes', ''), parse(incoming.get('creators')),
                                incoming.get('publisher', ''), incoming.get('date') or DATE,
                                doi=incoming.get('doi', ''), isbn=incoming.get('isbn', ''))
            row.update(connection_pass=MARK, access=incoming.get('access', row['access']),
                       last_checked=DATE, review_status='research_pass_needs_editor',
                       reviewed_by='', reviewed_at='')
            data['sources'].append(row)
            sources[sid] = row
        for incoming in entry['evidence']:
            if incoming['id'] in evidence:
                continue
            row = dict(incoming, connection_pass=MARK, quality_tier='A', licence='see_source',
                       public_evidence_status='public', reviewed_by='', reviewed_at='',
                       review_status='research_pass_needs_editor')
            data['evidence'].append(row)
            evidence[row['id']] = row
        for incoming in entry['edges']:
            assert incoming['id'] not in existing_edges, incoming['id']
            existing_edges.add(incoming['id'])
            row = edge_record(incoming['id'], resolve(incoming['source'], redirects),
                              resolve(incoming['target'], redirects), incoming['relation_type'],
                              incoming['relation_family'], incoming['plain_phrase'],
                              parse(incoming['source_ids']), incoming['source_locator'], incoming['scope_conditions'],
                              status='candidate', mode=incoming.get('assertion_mode', 'asserted'),
                              confidence='not quantified', review_label='Source-scoped proposal; editorial review pending')
            row.update(incoming)
            row.update(source=resolve(row['source'], redirects), target=resolve(row['target'], redirects),
                       directed=relation_types[row['relation_type']]['directed'],
                       source_ids=enc(parse(row['source_ids'])), evidence_ids=enc(parse(row['evidence_ids'])),
                       connection_pass=MARK, claim_status='candidate', reviewed_by='', reviewed_at='',
                       review_status='research_pass_needs_editor')
            data['edges'].append(row)
    refresh_counts(data)
    data['relational_depth'] = calculate_relational_depth(data)
    data['relational_depth'].update(release=RELEASE, generated=DATE)
    data['graph_snapshot'] = calculate(data)
    metrics = graph_metrics(data)
    aggregate = data['relational_depth']['aggregate']
    public_ids = {n['id'] for n in data['nodes'] if n.get('public_visibility') == 'public'
                  and resolve(n['id'], redirects) == n['id']}
    data['meta'].update(release=RELEASE, generated=DATE, release_digest_url='https://transduction.systems' + ROUTE,
                        iteration_focus=TITLE, release_note='107 original person records developed or resolved to existing identities, with scoped connections and a dependency reader; editorial acceptance remains pending.',
                        node_count=len(data['nodes']), edge_count=len(data['edges']), source_count=len(data['sources']),
                        evidence_count=len(data['evidence']),
                        profile_count=len({p['node_id'] for p in data['profiles'] if p['node_id'] in public_ids}),
                        public_entry_count=len(public_ids), described_entry_count=len(public_ids), surprise_me_eligible_count=len(public_ids),
                        reader_connected_entry_count=aggregate['reader_connected_entries'], semantic_connected_entry_count=aggregate['semantic_connected_entries'],
                        unconnected_entry_count=aggregate['connection_bands'].get('unconnected', 0),
                        rich_entry_count=aggregate['connection_bands'].get('rich', 0),
                        developing_entry_count=aggregate['connection_bands'].get('developing', 0),
                        thin_entry_count=aggregate['connection_bands'].get('thin', 0),
                        typed_edge_count=metrics['typed_edges'], substantive_edge_count=metrics['substantive_edges'],
                        semantic_gap_entry_count=len(public_ids) - aggregate['semantic_connected_entries'],
                        public_link_source_count=sum(s.get('public_link_status') == 'public_link' for s in data['sources']),
                        no_public_link_source_count=sum(s.get('public_link_status') == 'no_public_link' for s in data['sources']))
    originals, added_ids = {}, {}
    for key, field in ROW_KEYS:
        before = {r[field]: r for r in baseline[key]}
        now = {r[field]: r for r in data[key]}
        assert set(before) <= set(now), 'Historical rows must not be deleted'
        originals[key] = [r for r in baseline[key] if r != now[r[field]]]
        added_ids[key] = [r[field] for r in data[key] if r[field] not in before]
    counts = {key: len(value) for key, value in added_ids.items()}
    counts.update(original_person_records=107, canonical_people=len({resolve(n, redirects) for n in cohort}),
                  identity_redirects=len(packet.get('identity_redirects', {})), rewritten_edges=len(originals['edges']))
    data[MARK] = dict(date=DATE, cohort=cohort, identity_redirects=packet.get('identity_redirects', {}),
                     counts=counts, originals=originals, added_ids=added_ids,
                     original_values={k: baseline[k] for k in ['meta', 'relational_depth', 'graph_snapshot', 'canonical_redirects']},
                     baseline_sha256=fingerprint(baseline), source_packet='sources/biographies-107-45/packet.json',
                     human_editorial_acceptance_changed=False)
    return data


def release_outputs(data):
    counts = data[MARK]['counts']
    summary = (f"Release 0.45 develops or resolves all 107 original first-pass person records into {counts['canonical_people']} distinct biographical identities, with {counts['edges']} new scoped connections. "
               'A predecessor-and-dependent reader separates recorded necessary dependencies from other relationships. Sources, limits, and review status remain inspectable; named editorial acceptance is pending.')
    edition = dict(reader_release=RELEASE, graph_release=RELEASE, date=DATE, title=TITLE,
                   reading_url='/dependencies/?entry=concept_boundary', release_url=ROUTE, summary=summary)
    (DOCS / 'reader-edition.json').write_text(json.dumps(edition, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    nodes = {n['id']: n for n in data['nodes']}
    for original, target in data[MARK]['identity_redirects'].items():
        path = '/entries/' + target + '/'
        canonical_url = 'https://transduction.systems' + path
        destination = DOCS / 'entries' / original
        destination.mkdir(parents=True, exist_ok=True)
        title = nodes[target]['label']
        alias_html = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
                      '<meta name="viewport" content="width=device-width,initial-scale=1">'
                      '<title>' + escape(title) + ' – The Necessary Tangle</title>'
                      '<link rel="canonical" href="' + canonical_url + '">'
                      '<meta http-equiv="refresh" content="0; url=' + path + '">'
                      '</head><body><main><h1>' + escape(title) + '</h1>'
                      '<p>This earlier author-name entry resolves to the existing biographical identity.</p>'
                      '<p><a href="' + path + '">Read ' + escape(title) + '</a></p>'
                      '</main></body></html>\n')
        (destination / 'index.html').write_text(alias_html, encoding='utf-8')
        redirect_record = dict(schema_version='1.0', release=RELEASE,
                               requested_entry_id=original, canonical_entry_id=target,
                               canonical_url=canonical_url,
                               redirect={'target': target, 'url': path, 'reason': 'verified_same_person', 'connection_pass': MARK})
        (destination / 'record.json').write_text(json.dumps(redirect_record, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    rows = []
    for ident in data[MARK]['cohort']:
        target = resolve(ident, data['canonical_redirects'])
        suffix = ' · earlier initials resolve to this existing identity' if target != ident else ''
        rows.append('<li><a href="/entries/' + target + '/">' + escape(nodes[target]['label']) + '</a>' + suffix + '</li>')
    body = ('<p>Release 0.45 · 28 November 2026</p><p>' + escape(summary) + '</p>'
            '<p><a href="/dependencies/?entry=concept_boundary">Explore necessary predecessors and dependent entries</a>.</p>'
            '<p>The dependency view takes its navigational cue from SCiO’s SysBoK distinction between Precedents and Dependent Derivatives. '
            'It uses the Tangle’s own sourced graph and does not import or approve relationships merely because they appear in another map.</p>'
            '<p>The 84 source-led publication profiles from release 0.44 remain. This finite biography cohort does not complete the atlas’s other research programmes or resolve the separate moving-logo report.</p>'
            '<h2 id="completed-set">The 107 original records</h2><ol>' + ''.join(rows) + '</ol>')
    destination = DOCS / ROUTE.strip('/')
    destination.mkdir(parents=True, exist_ok=True)
    (destination / 'index.html').write_text(page(TITLE, summary, ROUTE, body, RELEASE), encoding='utf-8')
    for name, anchor, block in [
        ('README.md', '# The Necessary Tangle\n', 'Current research and reader release **0.45, 28 November 2026**. [People, predecessors, and what follows](https://transduction.systems' + ROUTE + '). All 107 original biography records are developed or identity-resolved. Editorial review remains open.'),
        ('documentation/TANGLE_STATE.md', '# Current Tangle state\n', '## Current research and reader edition 0.45\n\n' + summary + '\n\nAll canonical public entries remain in the random pool; identity aliases are de-duplicated. Graph and reader identity, deployment, and live tests remain separately recorded. The source-owner-reviewed Systemic Evolution package is unchanged.'),
        ('docs/updates/index.html', '<main>\n', '<section><h2><a href="' + ROUTE + '">Release 0.45 · ' + TITLE + '</a></h2><p>' + escape(summary) + '</p></section>')]:
        replace_marked(ROOT / name, block, anchor, marker=MARK)
    next_work = ('# Next work\n\n<!-- ' + MARK + ' -->\n'
                 '## Current authorised packet: 107 biographies and the dependency reader\n\n' + summary + '\n\n'
                 f"The maintained graph has {data['meta']['public_entry_count']:,} canonical public entries and {data['meta']['profile_count']:,} developed profiles. "
                 'Every canonical public entry remains eligible for random selection. Verified identity aliases retain their earlier routes and are de-duplicated in the pool.\n\n'
                 'Publication and live verification belong to deployment.json and the Publish workflow. Preserve the 84 publication accounts from release 0.44, identity redirects, and current navigation. Human editorial acceptance, wider corpus research, and the separate moving-logo report remain open.\n'
                 '<!-- /' + MARK + ' -->\n\n'
                 '## Historical random-selection correction, release 0.44\n\n'
                 'On 28 November 2026, the random handler was corrected from a filtered pool of 565 to all 1,295 canonical public entries then present. That audit found 107 person records without developed profiles, including 105 placeholder descriptions, and recorded the request for easier predecessor and dependent navigation. These are dated baseline measurements; release 0.45 addresses the finite biography cohort and adds the dependency view. The separate moving-logo report remains open.\n')
    (ROOT / 'documentation/NEXT_WORK.md').write_text(next_work, encoding='utf-8')
    replace_marked(ROOT / 'documentation/TANGLE_STATE.md', marker='random-entry-all')
    for name in ['README.md', 'documentation/TANGLE_STATE.md']:
        path = ROOT / name
        text = path.read_text(encoding='utf-8')
        text = re.sub(r'(<!-- first_pass_depth_44 -->.*?)(<!-- /first_pass_depth_44 -->)',
                      lambda m: m[1].replace('Current research and reader', 'Previous research and reader') + m[2], text, flags=re.S)
        path.write_text(text, encoding='utf-8')
    home = DOCS / 'index.html'
    text = home.read_text(encoding='utf-8')
    text = re.sub(r'<a id="releaseBadge"[^>]*>Release [^<]+</a>', '<a id="releaseBadge" data-reader-release="0.45" href="/versions/" aria-label="Version history, current release 0.45">Release 0.45</a>', text, count=1)
    text = re.sub(r'assets/public-data.js\?v=[^"\s]+', 'assets/public-data.js?v=0.45-biographies-20261128', text)
    aggregate = data['relational_depth']['aggregate']
    measures = [(data['meta']['public_entry_count'], 'readable public entries'), (aggregate['reader_connected_entries'], 'with reader connections'),
                (aggregate['connection_bands'].get('rich', 0) + aggregate['connection_bands'].get('developing', 0), 'developing or rich'), (aggregate['reader_statements'], 'reader relationship statements')]
    pattern = r'<div class="metrics" id="homeMetrics"[^>]*>(?:\s*<div class="metric">.*?</div>){4}\s*</div>'
    assert re.search(pattern, text, re.S), 'Homepage metric structure changed'
    metrics = ''.join('<div class="metric"><strong>' + str(n) + '</strong><span>' + label + '</span></div>' for n, label in measures)
    home.write_text(re.sub(pattern, '<div class="metrics" id="homeMetrics" aria-label="Atlas counts">' + metrics + '</div>', text, count=1, flags=re.S), encoding='utf-8')
    changelog = ROOT / 'CHANGELOG.md'
    text = changelog.read_text(encoding='utf-8')
    if not re.search(r'^## 0\.45 [—–] ', text, re.M):
        text = text.replace('# Changelog\n', '# Changelog\n\n## 0.45 – 28 November 2026\n\n' + summary + '\n', 1)
    changelog.write_text(text.replace('## 0.45 — ', '## 0.45 – '), encoding='utf-8')
    citation = ROOT / 'CITATION.cff'
    text = re.sub(r'^version:.*$', "version: '0.45'", citation.read_text(encoding='utf-8'), flags=re.M)
    citation.write_text(re.sub(r'^date-released:.*$', "date-released: '2026-11-28'", text, flags=re.M), encoding='utf-8')
    sitemap = DOCS / 'sitemap.xml'
    text = sitemap.read_text(encoding='utf-8')
    if 'https://transduction.systems' + ROUTE not in text:
        sitemap.write_text(text.replace('</urlset>', '<url><loc>https://transduction.systems' + ROUTE + '</loc><lastmod>' + DATE + '</lastmod></url></urlset>'), encoding='utf-8')
    history(ROOT, RELEASE)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reverse', action='store_true')
    args = parser.parse_args()
    data = restore_observations(load(ROOT / 'data/public-data.json'))
    active = MARK in data
    if args.reverse:
        if active:
            for original in data[MARK]['identity_redirects']:
                assert re.fullmatch(r'[a-zA-Z0-9_-]+', original), 'Invalid alias route ID'
                destination = DOCS / 'entries' / original
                record = destination / 'record.json'
                if record.exists() and load(record).get('redirect', {}).get('connection_pass') == MARK:
                    for name in ['index.html', 'record.json']:
                        (destination / name).unlink(missing_ok=True)
                    if not any(destination.iterdir()):
                        destination.rmdir()
            write(restore(data))
            (DOCS / 'reader-edition.json').write_text((PACKET.parent / 'previous-reader-edition044.json').read_text(encoding='utf-8'), encoding='utf-8')
            (ROOT / 'documentation/NEXT_WORK.md').write_text(load(PACKET)['previous_next_work044'], encoding='utf-8')
        for name in ['README.md', 'documentation/TANGLE_STATE.md', 'documentation/NEXT_WORK.md', 'docs/updates/index.html']:
            replace_marked(ROOT / name, marker=MARK)
        return
    data = apply_packet(data, load(PACKET))
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
    release_outputs(data)
    print('0.45 biographies applied:', json.dumps(data[MARK]['counts'], sort_keys=True))


if __name__ == '__main__':
    main()
