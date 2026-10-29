"""Deepen a bounded primary-source cohort and publish inspectable reading routes."""
from pathlib import Path
import copy
import hashlib
import html
import json
import math
import re

from apply_iteration_17 import enc, parse, upsert, source_record, node_record, edge_record
from apply_iteration_09 import graph_metrics
from apply_relational_depth_16 import calculate_relational_depth, write_relational_document
from apply_doncaster_lineage import refresh_counts
from apply_overnight_review import quality_result
from refresh_graph_snapshot import calculate, write

R = Path(__file__).resolve().parents[1]
D = R / 'docs'
S = R / 'documentation/research-2026-10-29'
MARK = 'depth_20261029'
DATE = '2026-10-29'
RELEASE = '0.35'
d = json.loads((R / 'data/public-data.json').read_text(encoding='utf-8'))
packets = [json.loads((S / name).read_text(encoding='utf-8')) for name in ['regulation-learning.json', 'transduction.json']]
originals = copy.deepcopy(d.get(MARK, {}).get('originals', {}))


def remember(key, identity, field='id'):
    originals.setdefault(key, [])
    if any(row.get(field) == identity for row in originals[key]):
        return
    row = next((row for row in d[key] if row.get(field) == identity), None)
    if row and row.get('connection_pass') != MARK:
        originals[key].append(copy.deepcopy(row))


def merge_ids(row, key, values):
    row[key] = enc(list(dict.fromkeys([*parse(row.get(key), []), *values])))


def evidence(eid, sid, locator, claim, basis='source_exposition'):
    row = dict(id=eid, source_id=sid, locator=locator, excerpt_or_summary=claim,
               evidence_type='primary_text_paraphrase' if basis == 'source_exposition' else 'curatorial_comparison',
               quality_tier='A', licence='see_source', review_status='research_pass_needs_editor',
               content_hash='', public_evidence_status='public', connection_pass=MARK)
    upsert(d['evidence'], [row], 'id')
    return eid


for packet in packets:
    for src in packet.get('sources', []):
        remember('sources', src['id'])
        row = source_record(src['id'], src['title'], 'primary_text', src['url'],
                            src.get('verified', '') + ' ' + src.get('limits', ''), src.get('authors', []),
                            src.get('publisher', ''), src.get('date', ''), quality='A')
        prior = next((x for x in d['sources'] if x['id'] == src['id']), {})
        for field in ['doi', 'isbn', 'licence', 'archived_url']:
            if src.get(field) or prior.get(field):
                row[field] = src.get(field) or prior[field]
        if src.get('reading_url'):
            row['reading_url'] = src['reading_url']
        if src.get('translator'):
            row['translator'] = src['translator']
        row.update(connection_pass=MARK, last_checked=DATE, source_locator=src['locator'],
                   review_status='passage_checked_research_pass', access_note=src.get('limits', ''))
        upsert(d['sources'], [row], 'id')
    for n in packet.get('nodes', []):
        remember('nodes', n['id'])
        angle = int(hashlib.sha256(n['id'].encode()).hexdigest()[:6], 16)
        row = node_record(n['id'], n['label'], n['entity_type'], n['summary'], n['source_ids'],
                          round(.5 + .2 * math.cos(angle), 6), round(.5 + .2 * math.sin(angle), 6), n.get('tags', []))
        row.update(connection_pass=MARK, status='candidate', review_status='research_pass_needs_editor',
                   reviewed_by='', reviewed_at='', inclusion_reason=MARK,
                   set_tags=enc(['systems', 'release_0_35', *n.get('tags', [])]))
        upsert(d['nodes'], [row], 'id')
    for p in packet.get('profiles', []):
        nid = p['node_id']
        remember('profiles', nid, 'node_id')
        remember('nodes', nid)
        node = next(n for n in d['nodes'] if n['id'] == nid)
        profile = copy.deepcopy(next((x for x in d['profiles'] if x['node_id'] == nid), dict(node_id=nid, title=node['label'])))
        original = next((x for x in originals['profiles'] if x['node_id'] == nid), {})
        for key in ['summary', 'canonical_definition', 'why_it_matters', 'context_and_lineage']:
            if p.get(key):
                if key in ['summary', 'why_it_matters'] and original.get(key) and original[key] != p[key]:
                    profile[key] = original[key] + ' ' + p[key]
                elif key == 'canonical_definition' and original.get(key) and p.get('action') in ['deepen_existing', 'append_located_account_to_existing_profile']:
                    profile[key] = original[key]
                else:
                    profile[key] = p[key]
        for key in ['key_distinctions', 'practice_connections', 'common_misreadings', 'open_checks']:
            if key in p:
                merge_ids(profile, key, p[key])
        merge_ids(profile, 'source_ids', p['source_ids'])
        evs = []
        for i, loc in enumerate(p.get('locators', [])):
            evs.append(evidence('ev35_' + nid + '_' + str(i + 1), loc['source_id'], loc['locator'], loc['claim'], loc.get('basis', 'source_exposition')))
        merge_ids(profile, 'evidence_ids', evs)
        profile.update(connection_pass=MARK, profile_status='evidence_deepened_research_pass',
                       last_researched=DATE, review_status='research_pass_needs_editor',
                       editorial_note='Primary passages checked for this bounded research pass. Exposition and editorial comparisons remain distinct; named editorial acceptance is not implied by publication.')
        upsert(d['profiles'], [profile], 'node_id')
        node.update(connection_pass=MARK, publication_level='profile', canonical_definition=profile.get('canonical_definition', p['summary']))
        merge_ids(node, 'source_ids', p['source_ids'])
        node['public_source_count'] = len(parse(node['source_ids']))
    for e in packet.get('edges', []):
        remember('edges', e['id'])
        family = next(r['relation_family'] for r in d['relation_types'] if r['relation_type'] == e['relation_type'])
        basis = e.get('basis', 'source_exposition')
        row = edge_record(e['id'], e['source'], e['target'], e['relation_type'], family, e['label'],
                          e['source_ids'], e['locator'], e['scope'], status='candidate',
                          mode='asserted' if basis == 'source_exposition' else 'inferred', confidence='',
                          review_label='Primary-source exposition; editorial acceptance open' if basis == 'source_exposition' else 'Editorial comparison; no historical influence asserted')
        evs = []
        for i, sid in enumerate(e['source_ids']):
            evs.append(evidence('ev35_edge_' + e['id'] + '_' + str(i + 1), sid, e['locator'], e['scope'], basis))
        row.update(connection_pass=MARK, evidence_ids=enc(evs), claim_id='claim35_' + e['id'])
        prior_edge = next((x for x in originals.get('edges', []) if x['id'] == e['id']), {})
        # Historical references remain inspectable; a repaired claim uses the new evidence.
        if prior_edge:
            row['previous_source_ids'] = prior_edge.get('source_ids', '[]')
            row['previous_evidence_ids'] = prior_edge.get('evidence_ids', '[]')
            row['notes'] = 'Earlier wording and provenance are retained in this release\'s original-record ledger. This statement uses the sources and scope shown here.'
        upsert(d['edges'], [row], 'id')
        claim = dict(id=row['claim_id'], statement=e['scope'], subject_id=e['source'], predicate=e['relation_type'], object_id=e['target'],
                     status='candidate', supporting_source_ids=enc(e['source_ids']), supporting_evidence_ids=enc(evs),
                     contradicting_source_ids='[]', contradicting_evidence_ids='[]', notes=row['public_review_label'],
                     review_status='research_pass_needs_editor', reviewed_by='', reviewed_at='', connection_pass=MARK)
        upsert(d['claims'], [claim], 'id')

# Reader journeys are explicitly editorial routes; their order is not a historical lineage.
journeys = json.loads((S / 'journeys.json').read_text(encoding='utf-8'))
for journey in journeys:
    journey.update(connection_pass=MARK, review_status='editorial_reading_route', generated=DATE)
    upsert(d['journeys'], [journey], 'id')

refresh_counts(d)
d['relational_depth'] = calculate_relational_depth(d)
d['relational_depth'].update(release=RELEASE, generated=DATE)
d['graph_snapshot'] = calculate(d)
metrics = graph_metrics(d)
depth = d['relational_depth']['aggregate']
changed = {key: len([x for x in d[key] if x.get('connection_pass') == MARK]) for key in ['nodes', 'profiles', 'sources', 'edges', 'evidence', 'claims', 'journeys']}
edge_revisions = len(originals.get('edges', []))
edge_additions = changed['edges'] - edge_revisions
d[MARK] = dict(date=DATE, originals=originals, counts=changed,
               edge_additions=edge_additions, edge_revisions=edge_revisions,
               source_packet='documentation/research-2026-10-29/', reader_url='/reading/connections/',
               scope='Passage-level primary exposition and explicitly labelled editorial comparisons; no new claim of historical influence.')
d['meta'].update(release=RELEASE, generated=DATE, release_digest_url='https://transduction.systems/updates/2026-10-29/',
                 iteration_focus='Primary references and meaningful connections: regulation, learning, and transduction',
                 release_note='Locatable primary sources, deeper profiles, three reading journeys, and explicit differences between connected ideas.',
                 node_count=len(d['nodes']), edge_count=len(d['edges']), source_count=len(d['sources']), profile_count=len(d['profiles']),
                 public_entry_count=metrics['public_entries'], described_entry_count=metrics['public_entries'],
                 reader_connected_entry_count=depth['reader_connected_entries'], semantic_connected_entry_count=depth['semantic_connected_entries'],
                 unconnected_entry_count=depth['connection_bands'].get('unconnected', 0), semantic_gap_entry_count=metrics['public_entries']-depth['semantic_connected_entries'],
                 public_link_source_count=sum(s.get('public_link_status')=='public_link' for s in d['sources']),
                 no_public_link_source_count=sum(s.get('public_link_status')=='no_public_link' for s in d['sources']))
for band in ['rich', 'developing', 'thin']:
    d['meta'][band + '_entry_count'] = depth['connection_bands'].get(band, 0)
write(d)
q = quality_result(d)
q.update(release=RELEASE, generated=DATE)
for key in ['adversarial_review', 'doncaster_lineage_review']:
    q[key] = d[key]
for name in ['data/relationship-quality.json', 'docs/assets/relationship-quality.json']:
    (R/name).write_text(json.dumps(q, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
write_relational_document(d)

E = lambda s: html.escape(str(s), quote=True)
def link(url, title):
    return '<a href="' + E(url) + '">' + E(title) + '</a>'
def atlas(nid):
    node = next(n for n in d['nodes'] if n['id'] == nid)
    return link('/#view=item&id=' + nid, node['label'])

css = '*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#faf8f2;color:#302b26;font:18px/1.7 Georgia,serif}main,nav,footer{max-width:65rem;margin:auto;padding:1.4rem}nav{display:flex;gap:1rem;flex-wrap:wrap;font:1rem/1.5 system-ui}a{color:#973d32;overflow-wrap:anywhere}a:focus-visible,summary:focus-visible{outline:3px solid #973d32;outline-offset:3px}h1{font-size:clamp(2.1rem,6vw,3.6rem);line-height:1.14;max-width:19ch}h2{font-size:1.8rem;line-height:1.25}h3{font-size:1.3rem}section{border-top:1px solid #d8d0c5;padding:1.4rem 0;margin-top:1.4rem;scroll-margin-top:1rem}.meta,.source,.note{font:1rem/1.6 system-ui}.note{background:#f0eadd;padding:1rem;border-left:3px solid #973d32}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,17rem),1fr));gap:1.2rem}.grid article{border:1px solid #d8d0c5;border-top:3px solid #973d32;padding:1rem}.grid h2{font-size:1.4rem}li{margin-bottom:.6rem}details{padding:.8rem 0}summary{cursor:pointer}#openUpdates{position:fixed;bottom:0;right:0;width:44px;height:44px}#openUpdates:after{content:"";position:absolute;right:8px;bottom:8px;width:5px;height:5px;background:#862719;border-radius:50%;box-shadow:0 0 0 1px white}@media(max-width:600px){main,nav,footer{padding:1rem}ul,ol{padding-left:1.3rem}}@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}'

def page(route, title, body):
    dest = D/route.strip('/')
    dest.mkdir(parents=True, exist_ok=True)
    content = '<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+E(title)+' | The Necessary Tangle</title><meta name="description" content="Primary reading and inspectable connections across regulation, learning, transduction, and living organisation."><link rel="canonical" href="https://transduction.systems'+route+'"><style>'+css+'</style></head><body><nav aria-label="Main">'+link('/','Atlas')+link('/library/','Sources')+link('/learning/','Learning')+link('/updates/2026-10-29/','Latest update')+'</nav><main><p class="meta">Release 0.35 · 29 October 2026</p><h1>'+E(title)+'</h1>'+body+'</main><footer><p>Curated by '+link('https://www.antlerboy.com/','Benjamin P Taylor')+'. Primary-source research assisted by AI. Sources retain their authorship and terms. Editorial comparisons are identified where they occur.</p><p>'+link('/contribute/','Suggest a source or challenge a connection')+'</p></footer><a id="openUpdates" href="https://github.com/antlerboy/the-necessary-tangle/issues/2" aria-label="Open updates"></a></body></html>\n'
    (dest/'index.html').write_text(content, encoding='utf-8')

body = (S/'reading.html').read_text(encoding='utf-8')
# Resolve readable placeholders from the canonical data and evidence packet.
body = re.sub(r'\{\{atlas:([^}]+)\}\}', lambda m: atlas(m[1]), body)
sources = {s['id']: s for s in d['sources']}
body = re.sub(r'\{\{source:([^}]+)\}\}', lambda m: link(sources[m[1]]['url'], sources[m[1]]['title']), body)
body += '<section id="sources"><h2>Primary sources and passage checks</h2><p>These records identify the passages used in this release. An open copy establishes access; it does not remove copyright or turn every claim in a work into an accepted atlas statement.</p>'
for packet in packets:
    for src in packet['sources']:
        body += '<article id="'+E(src['id'])+'"><h3>'+link(src['url'], src['title'])+'</h3><p class="source">'+E(', '.join(src.get('authors', [])))+' · '+E(src.get('date', ''))+'</p><p>'+E(src['locator'])+'</p><p>'+E(src.get('verified', ''))+'</p>'
        if src.get('limits'):
            body += '<p class="source">'+E(src['limits'])+'</p>'
        if src.get('reading_url'):
            body += '<p class="source">'+link(src['reading_url'], 'Inspected reading copy')+'</p>'
        body += '</article>'
body += '<p>'+link('/updates/2026-10-29/evidence.json','Download the evidence packet')+'</p></section>'
page('/reading/connections/', 'What crosses a boundary? Regulation, learning, and transduction', body)

cards = '<div class="grid card-grid three">'
for anchor, title, description in [
    ('regulation', 'What must a regulator distinguish?', 'Ashby’s variety, Conant and Ashby’s model theorem, and Beer’s channels and transducers.'),
    ('learning', 'What changes when we learn?', 'Bateson’s logical levels, changes to governing variables, and why two familiar accounts are not interchangeable.'),
    ('transduction', 'Does a boundary separate things already formed?', 'Beer’s conversion across boundaries, Simondon’s individuation, and autopoiesis as the production of a living unity.')]:
    cards += '<article class="card"><h2>'+link('/reading/connections/#'+anchor, title)+'</h2><p>'+E(description)+'</p></article>'
cards += '</div>'
digest = '<p>Three routes deepen the references behind familiar words and make the differences between connected ideas inspectable. Each route leads to original passages, developed atlas entries, and statements whose direction and scope can be checked.</p>'+cards
digest += '<section><h2>What changed in the atlas</h2><p>'+str(changed['profiles'])+' profiles developed or revised; '+str(changed['sources'])+' primary source records checked; '+str(edge_additions)+' connections added and '+str(edge_revisions)+' revised; and '+str(changed['journeys'])+' guided journeys. Earlier provenance is retained in the release ledger. The counts describe this bounded pass, not the coverage or settled agreement of the field.</p><ul>'
for j in journeys:
    digest += '<li>'+link('/#view=journeys&id='+j['id']+'&step=0', j['title'])+' — '+E(j['summary'])+'</li>'
digest += '</ul><p>'+link('/reading/connections/','Read the connected source guide')+' · '+link('evidence.json','Inspect the evidence packet')+'</p></section><section><h2>What the connections claim</h2><p>Primary-source exposition records what a specified passage says. Editorial comparisons bring passages into conversation without claiming that one author influenced another. Both retain visible research status; publication does not invent a named curator’s acceptance.</p><p>In particular, an entropy-based regulation theorem does not establish organisational wisdom; Bateson’s Learning II is not simply another name for double-loop learning; and transduction does not have a single interchangeable meaning across Beer and Simondon. A self-producing living unity also requires a more specific account than a self-organising group.</p></section><section><h2>Further work</h2><p>The most useful next evidence would be documented cases following these distinctions through an intervention: which distinctions a reporting system loses, what learning changed beyond the response, and how a boundary is produced and contested. That is a separate inquiry from source exposition.</p><p>The existing '+link('/saidtosomeone/','Heinz von Foerster companion page')+', event collection, contribution service, and approved historical comparator remain available.</p></section>'
page('/updates/2026-10-29/', 'Deeper references and connections', digest)
(D/'updates/2026-10-29/evidence.json').write_text(json.dumps(dict(date=DATE, scope=d[MARK]['scope'], packets=packets), ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

block = '<section class="resource-pathways plain-panel wide" id="deeper-connections"><p class="eyebrow">Primary reading · Release 0.35</p><h2>'+link('/reading/connections/','Regulation, learning, and what crosses a boundary')+'</h2><p>Follow Ashby, Conant, Beer, Bateson, Simondon, Maturana, and Varela through precise passages and connections whose limits remain visible.</p>'+cards.replace('<h2>', '<h3>').replace('</h2>', '</h3>')+'</section>'
for name in ['index.html', 'library/index.html', 'learning/index.html', 'updates/index.html']:
    p = D/name
    text = p.read_text(encoding='utf-8')
    text = re.sub(r'<!-- '+MARK+r' -->.*?<!-- /'+MARK+r' -->', '', text, flags=re.S)
    insertion = '<!-- '+MARK+' -->'+block+'<!-- /'+MARK+' -->'
    if name == 'index.html':
        # Place within the existing home view so the atlas router remains in charge.
        text = text.replace('<section id="systemsPracticeCallout"', insertion+'<section id="systemsPracticeCallout"', 1)
        if '<!-- '+MARK+' -->' not in text:
            raise RuntimeError('Cannot locate the homepage view for the new reading route')
        text = re.sub(r'<span id="releaseBadge">Release [^<]+</span>', '<span id="releaseBadge">Release 0.35</span>', text, count=1)
        text = re.sub(r'assets/public-data.js\?v=[^"\s]+', 'assets/public-data.js?v=0.35', text)
    else:
        text = text.replace('</main>', insertion+'</main>', 1)
    p.write_text(text, encoding='utf-8')

p = D/'sitemap.xml'
text = p.read_text(encoding='utf-8')
for route in ['/reading/connections/', '/updates/2026-10-29/']:
    url = 'https://transduction.systems'+route
    if url not in text:
        text = text.replace('</urlset>', '<url><loc>'+url+'</loc><lastmod>'+DATE+'</lastmod></url></urlset>')
p.write_text(text, encoding='utf-8')
p = R/'README.md'
text = p.read_text(encoding='utf-8')
current = 'Current release: **0.35, 29 October 2026**. [Deeper references and connections](https://transduction.systems/updates/2026-10-29/). [Read the connected source guide](https://transduction.systems/reading/connections/).'
text = re.sub(r'<!-- current-31 -->.*?<!-- /current-31 -->', '<!-- current-31 -->\n'+current+'\n<!-- /current-31 -->', text, flags=re.S)
p.write_text(text, encoding='utf-8')
p = R/'CITATION.cff'
text = re.sub(r'^version:.*$', "version: '0.35'", p.read_text(encoding='utf-8'), flags=re.M)
text = re.sub(r'^date-released:.*$', "date-released: '2026-10-29'", text, flags=re.M)
p.write_text(text, encoding='utf-8')
p = R/'CHANGELOG.md'
text = p.read_text(encoding='utf-8')
entry = '\n\n## 0.35 — 29 October 2026\n\nPrimary references and scoped connections across regulation, models, learning, transduction, and living organisation. '+str(changed['profiles'])+' profiles deepened or developed, '+str(changed['edges'])+' connections, '+str(changed['sources'])+' source records, and three guided journeys. Passage locators and evidence records distinguish exposition from editorial comparison. A connected reading guide, evidence download, homepage and library routes, and reproducible baseline accompany the release. Exact publication and live verification are recorded by the Publish workflow and deployment.json.\n'
if '## 0.35 — 29 October 2026' not in text:
    text = text.replace('# Changelog', '# Changelog'+entry, 1)
p.write_text(text, encoding='utf-8')

p = R/'documentation/TANGLE_STATE.md'
text = p.read_text(encoding='utf-8')
text = re.sub(r'<!-- '+MARK+r' -->.*?<!-- /'+MARK+r' -->\s*', '', text, flags=re.S)
state = '<!-- '+MARK+' -->\n## Current release 0.35\n\n29 October 2026. '+str(metrics['public_entries'])+' public entries, '+str(len(d['edges']))+' edges, '+str(len(d['sources']))+' sources, and '+str(len(d['profiles']))+' profiles. This release deepens '+str(changed['profiles'])+' profiles, adds '+str(edge_additions)+' scoped connections, revises '+str(edge_revisions)+', and adds three journeys. The source packet is documentation/research-2026-10-29/. Reader route: https://transduction.systems/reading/connections/. Publication identity and live test completion belong to deployment.json and the Publish workflow. Source exposition and editorial comparison remain candidates for editorial acceptance; no historical influence is inferred from resemblance. The previous release account and companion-page record below remain historical context.\n<!-- /'+MARK+' -->\n\n'
text = text.replace('# Current Tangle state\n', '# Current Tangle state\n\n'+state, 1)
p.write_text(text, encoding='utf-8')
packet = (S/'work-packet.md').read_text(encoding='utf-8')
(R/'documentation/NEXT_WORK.md').write_text(packet, encoding='utf-8')
print('Release 0.35 prepared:', json.dumps(changed, sort_keys=True))
