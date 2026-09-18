#!/usr/bin/env python3
"""Publish a bounded, source-scoped response to seven public submissions."""
from pathlib import Path
import hashlib
import html
import json
import re
from apply_iteration_17 import enc, parse, upsert, source_record, node_record, profile_record, edge_record, relation_record
from apply_iteration_09 import graph_metrics, make_ai_observations
from apply_overnight_review import quality_result
from apply_doncaster_lineage import refresh_counts
from apply_relational_depth_16 import calculate_relational_depth, write_relational_document
from refresh_graph_snapshot import calculate, write

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / 'sources/intake-2026-09-18/entries.json'
MARK = 'source_intake_20260918'
DATE = '2026-09-18'
URL = 'https://transduction.systems/updates/2026-09-18/'


def main():
    packet = json.loads(PACKET.read_text(encoding='utf-8'))
    data = json.loads((ROOT / 'data/public-data.json').read_text(encoding='utf-8'))
    for item in packet['sources']:
        source = source_record(item['id'], item['title'], 'primary_public_record', item['url'],
                               item['locator'] + ': ' + item['scope'], [], item['publisher'], 'checked ' + DATE)
        source.update(date=item.get('published', ''), last_checked=DATE, review_status='source_scope_checked', connection_pass=MARK)
        upsert(data['sources'], [source], 'id')
    mapping = {}
    for item in packet['entries'] + packet['supporting_nodes']:
        sources = item.get('sources', [item.get('source')])
        aliases = item.get('aliases', [])
        kind = item.get('kind', 'person')
        existing = next((n for n in data['nodes'] if n['entity_type'] == kind and
                        (n['id'] == item['id'] or n['label'].casefold() in [item['label'].casefold(), *[a.casefold() for a in aliases]])), None)
        if existing and existing.get('inclusion_reason') != MARK:
            # This packet was checked against the existing graph. A later identity
            # collision must receive an explicit merge decision, not silent replacement.
            raise ValueError('Existing canonical identity needs reconciliation: ' + existing['id'])
        key = item['id']
        mapping[item['id']] = key
        value = int(hashlib.sha256(key.encode()).hexdigest()[:8], 16)
        node = node_record(key, item['label'], kind, item['summary'], sources,
                           (value % 1000)/1000-.5, ((value//1000) % 1000)/1000-.5,
                           ['systems', MARK], aliases=aliases, level='profile' if 'issue' in item else 'described')
        node.update(inclusion_reason=MARK, status='candidate', review_status='source_scoped_research_pass',
                    reviewed_by='', reviewed_at='', set_tags=enc(['systems']))
        upsert(data['nodes'], [node], 'id')
        if 'issue' in item:
            profile = profile_record(key, item['summary'], item['why'], item['distinctions'], [], [], [], [], [],
                                     item['limits'], sources, context='See the cited source locators and scoped graph statements.',
                                     editorial_note='Prepared with AI assistance from the named public records. Independent specialist review is not recorded. The wider submitted claims remain open.')
            profile.update(title=item['label'], last_researched=DATE, profile_status='source_scoped_research_pass',
                           review_status='independent_review_not_recorded', reviewed_by='', reviewed_at='')
            upsert(data['profiles'], [profile], 'node_id')
    known = {n['id'] for n in data['nodes']}
    for a, b, typ, family, phrase, sid, locator, scope in packet['relations']:
        assert a in known and b in known, (a, b)
        if not any(r['relation_type'] == typ for r in data['relation_types']):
            upsert(data['relation_types'], [relation_record(typ, family, 'inverse_' + typ,
                   'A located primary statement establishing the specified role or contribution', phrase)], 'relation_type')
        relation = edge_record('e25_' + a + '_' + typ + '_' + b, a, b, typ, family, phrase, [sid], locator,
                               scope, status='candidate', confidence='', review_label='Located source statement; independent review not recorded')
        relation.update(reviewed_by='', reviewed_at='')
        upsert(data['edges'], [relation], 'id')
    reviewed = {i['issue']: i for i in packet['entries']}
    for item in data.get('september_connections', {}).get('queue', []):
        match = re.search(r'/issues/(\d+)', item.get('url', ''))
        if match and int(match[1]) in reviewed:
            entry = reviewed[int(match[1])]
            item.update(canonical_id=entry['id'], status='located_claims_published_deeper_claims_pending',
                        latest_review=DATE, review_url=URL)
    data['source_intake_20260918'] = {'checked': DATE, 'release': packet['release'], 'url': URL,
        'issues': sorted(reviewed), 'scope': 'Seven profiles and twelve specific statements; wider submissions remain open.',
        'independent_review': 'not_recorded'}
    refresh_counts(data)
    data['meta'].update(release=packet['release'], generated=DATE, latest_intake_url=URL,
                        release_digest_url=URL, iteration_focus='Seven source-scoped responses to public submissions',
                        release_note='Seven profiles and twelve located statements; wider claims remain open.',
                        node_count=len(data['nodes']), edge_count=len(data['edges']),
                        source_count=len(data['sources']), profile_count=len(data['profiles']))
    data['relational_depth'] = calculate_relational_depth(data)
    data['relational_depth'].update(release=packet['release'], generated=DATE)
    data['graph_snapshot'] = calculate(data)
    metrics = graph_metrics(data)
    data['meta'].update(public_entry_count=metrics['public_entries'], described_entry_count=metrics['public_entries'])
    for field, metric in [('reader_connected_entry_count', 'reader_connected_entries'), ('semantic_connected_entry_count', 'semantic_connected_entries')]:
        data['meta'][field] = data['relational_depth']['aggregate'][metric]
    depth = data['relational_depth']['aggregate']
    data['meta'].update(unconnected_entry_count=depth['connection_bands'].get('unconnected', 0),
        semantic_gap_entry_count=metrics['public_entries']-depth['semantic_connected_entries'],
        public_link_source_count=sum(s.get('public_link_status') == 'public_link' for s in data['sources']),
        no_public_link_source_count=sum(s.get('public_link_status') == 'no_public_link' for s in data['sources']))
    for band in ['rich', 'developing', 'thin']:
        data['meta'][band+'_entry_count'] = depth['connection_bands'].get(band, 0)
    for key in ['reading_list_inventory', 'reading_list_coverage', 'core_systems_practice']:
        data[key]['release'] = packet['release']
    data['ai_observations'].update(release=packet['release'], generated=DATE, metrics=metrics)
    upsert(data['ai_observations']['observations'], make_ai_observations(metrics)['observations'], 'id')
    write(data)
    quality = quality_result(data)
    quality.update(release=packet['release'], generated=DATE)
    for key in ['adversarial_review', 'doncaster_lineage_review']:
        quality[key] = data[key]
    for name in ['data/relationship-quality.json', 'docs/assets/relationship-quality.json']:
        (ROOT/name).write_text(json.dumps(quality, ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')
    write_relational_document(data)
    rows = ''.join('<li><a href="/#view=item&amp;id=' + i['id'] + '">' + html.escape(i['label']) +
                   '</a>: ' + html.escape(i['summary']) + ' <a href="https://github.com/antlerboy/the-necessary-tangle/issues/' +
                   str(i['issue']) + '">Submission and remaining claims</a>.</li>' for i in packet['entries'])
    page = '''<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Seven source-scoped profiles | The Necessary Tangle</title><link rel="canonical" href="''' + URL + '''"><style>body{font:18px/1.65 Georgia,serif;max-width:850px;margin:auto;padding:24px;background:#faf8f3;color:#292621}h1{line-height:1.2}a{color:#9a302c;overflow-wrap:anywhere}li{margin-bottom:1.2em}nav{display:flex;flex-wrap:wrap;gap:1em}.note{padding:1em;border-left:3px solid #9a302c;background:#f0ece3}</style></head><body><nav><a href="/">Atlas</a><a href="/updates/">Updates</a><a href="/reading-list.html">Reading</a></nav><main><h1>Seven source-scoped profiles</h1><p>18 September 2026 · Release 0.24</p><p>Seven submitted names now have entries linked to specific publications, institutional records, or practitioner accounts. Twelve new statements identify authorship, contributions, institutional roles, collaboration, or reported use of a method.</p><ul>''' + rows + '''</ul><h2>What this pass establishes</h2><p>Judith Rosen's contributions are identified separately from Robert Rosen's authorship. Hawk's discussion of Ackoff and Trist does not establish a teacher–student relationship. Allen's co-authorship retains Valerie Ahl's credit. Institutional announcements are dated rather than treated as permanent appointments.</p><p class="note">Prepared with AI assistance from the linked sources. Independent specialist review is not recorded. The full books and papers have not been read in this pass, and the wider submitted claims remain open. These entries provide documented starting points for that work.</p><h2>Source access</h2><p>Each atlas entry links to its source records and identifies what remains to be checked. The source-owner-reviewed Systemic Evolution package is unchanged.</p></main></body></html>\n'''
    out = ROOT / 'docs/updates/2026-09-18/index.html'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding='utf-8', newline='\n')
    index = ROOT / 'docs/updates/index.html'
    index.write_text('<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Updates | The Necessary Tangle</title><link rel="canonical" href="https://transduction.systems/updates/"><style>body{font:18px/1.7 Georgia,serif;max-width:800px;margin:auto;padding:24px;background:#faf8f3;color:#292621}a{color:#9a302c}</style></head><body><nav><a href="/">Atlas</a></nav><main><h1>Updates</h1><ul><li><a href="/updates/2026-09-09/">9 September: source connections and events</a></li><li><a href="/updates/0.23/">Release 0.23: systems methods practice</a></li><li><a href="/updates/0.22/">Release 0.22: reader routes and early cybernetics</a></li></ul></main></body></html>\n', encoding='utf-8', newline='\n')
    for filename in ['docs/updates/index.html', 'docs/reading-list.html']:
        path = ROOT / filename
        text = path.read_text(encoding='utf-8')
        text = re.sub(r'<!-- intake-20260918 -->.*?<!-- /intake-20260918 -->', '', text, flags=re.S)
        text = text.replace('</main>', '<!-- intake-20260918 --><section><h2>18 September source review</h2><p><a href="/updates/2026-09-18/">Seven profiles, their sources, and remaining work</a></p></section><!-- /intake-20260918 --></main>', 1)
        path.write_text(text, encoding='utf-8', newline='\n')
    sitemap = ROOT / 'docs/sitemap.xml'
    text = sitemap.read_text(encoding='utf-8')
    if URL not in text:
        text = text.replace('</urlset>', '<url><loc>' + URL + '</loc><lastmod>' + DATE + '</lastmod></url></urlset>')
    sitemap.write_text(text, encoding='utf-8', newline='\n')
    note = ('## Source intake, 18 September 2026\n\nRelease 0.24 adds seven profiles and twelve scoped statements from eight primary public records. '
            'There are now ' + str(metrics['public_entries']) + ' canonical public entries. The wider submissions and independent specialist review remain open. '
            'See ' + URL + ' and sources/intake-2026-09-18/entries.json. The approved Systemic Evolution files retain their exact checksums.\n\n')
    state = ROOT/'documentation/TANGLE_STATE.md'
    text = state.read_text(encoding='utf-8')
    text = re.sub(r'## Source intake, 18 September 2026\n.*?(?=\n## |\Z)', '', text, flags=re.S)
    text = text.replace('# Tangle state\n', '# Tangle state\n\n'+note, 1)
    state.write_text(text, encoding='utf-8', newline='\n')
    for name, heading in [('README.md', '## Release 0.24'), ('CHANGELOG.md', '## 0.24 - 18 September 2026')]:
        path = ROOT/name
        text = path.read_text(encoding='utf-8')
        if heading not in text:
            path.write_text(text.rstrip()+'\n\n'+heading+'\n\n'+note.split('\n\n', 1)[1].rstrip()+'\n', encoding='utf-8', newline='\n')
    citation = ROOT/'CITATION.cff'
    text = citation.read_text(encoding='utf-8')
    text = re.sub(r'^version:.*$', 'version: '+packet['release'], text, flags=re.M)
    text = re.sub(r'^date-released:.*$', 'date-released: '+DATE, text, flags=re.M)
    citation.write_text(text, encoding='utf-8', newline='\n')
    app = ROOT/'docs/assets/app.js'
    text = app.read_text(encoding='utf-8')
    if 'entry-editorial-note' not in text:
        anchor = "    ${sections.join('')}"
        if anchor not in text:
            raise ValueError('Entry renderer changed; editorial provenance needs manual reconciliation')
        text = text.replace(anchor, anchor + '''
    ${profile?.editorial_note ? `<section class="entry-section entry-editorial-note"><h2>Editorial status</h2><p>${esc(profile.editorial_note)}</p></section>` : ''}''', 1)
        app.write_text(text, encoding='utf-8', newline='\n')
    print('Applied release 0.24: seven profiles, twelve scoped statements; independent review not recorded')


if __name__ == '__main__':
    main()
