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
S = R / 'documentation/research-2026-11-06'
MARK = 'depth_20261106'
DATE = '2026-11-06'
RELEASE = '0.36'
d = json.loads((R / 'data/public-data.json').read_text(encoding='utf-8'))
packets = [json.loads((S / name).read_text(encoding='utf-8')) for name in ['conceptual-deepening.json']]
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
        prior = next((row for row in d['sources'] if row['id'] == src['id']), {})
        row = source_record(src['id'], src['title'], src.get('source_type', 'primary_text'), src['url'],
                            src.get('verified', '') + ' ' + src.get('limits', ''), src.get('authors', []),
                            src.get('publisher', ''), src.get('date', ''), quality=src.get('quality_tier', 'A'))
        for field in ['doi', 'isbn', 'licence', 'archived_url', 'reading_url', 'translator', 'access']:
            if src.get(field) or prior.get(field):
                row[field] = src.get(field) or prior[field]
        row.update(connection_pass=MARK, last_checked=DATE, source_locator=src['locator'],
                   review_status='passage_checked_research_pass', access_note=src.get('limits', ''))
        upsert(d['sources'], [row], 'id')
    for incoming in packet.get('evidence_proposals', []):
        remember('evidence', incoming['id'])
        row = {key: copy.deepcopy(value) for key, value in incoming.items() if key != 'action'}
        row.update(connection_pass=MARK)
        upsert(d['evidence'], [row], 'id')
    for incoming in packet.get('nodes', []):
        nid = incoming['id']
        remember('nodes', nid)
        row = copy.deepcopy(next(n for n in d['nodes'] if n['id'] == nid))
        for key in ['canonical_definition', 'description', 'publication_level', 'review_status', 'reviewed_by', 'reviewed_at']:
            if key in incoming:
                row[key] = incoming[key]
        merge_ids(row, 'source_ids', incoming.get('source_ids', []))
        row.update(connection_pass=MARK, public_source_count=len(parse(row['source_ids'])))
        upsert(d['nodes'], [row], 'id')
    for incoming in packet.get('profiles', []):
        nid = incoming['node_id']
        remember('profiles', nid, 'node_id')
        remember('nodes', nid)
        node = next(n for n in d['nodes'] if n['id'] == nid)
        profile = copy.deepcopy(next((row for row in d['profiles'] if row['node_id'] == nid), dict(node_id=nid, title=node['label'])))
        for key in ['title', 'summary', 'canonical_definition', 'why_it_matters', 'context_and_lineage', 'editorial_note', 'reviewed_by', 'reviewed_at']:
            if key in incoming:
                profile[key] = incoming[key]
        for key in ['key_distinctions', 'historical_lineage', 'logical_antecedents', 'dependent_subsequents', 'practice_connections', 'espoused_lineages', 'observed_clusters', 'common_misreadings', 'open_checks']:
            if key in incoming:
                profile[key] = enc(incoming[key])
        merge_ids(profile, 'source_ids', incoming['source_ids'])
        merge_ids(profile, 'evidence_ids', incoming.get('evidence_ids', []))
        profile.update(connection_pass=MARK, profile_status='evidence_deepened_research_pass',
                       last_researched=DATE, review_status='research_pass_needs_editor', reviewed_by='', reviewed_at='')
        upsert(d['profiles'], [profile], 'node_id')
        node.update(connection_pass=MARK, publication_level='profile', canonical_definition=profile['canonical_definition'])
        merge_ids(node, 'source_ids', incoming['source_ids'])
        node['public_source_count'] = len(parse(node['source_ids']))
    packet_claims = {row['id']: row for row in packet.get('claims', [])}
    for incoming in packet.get('edges', []):
        eid = incoming['id']
        remember('edges', eid)
        family = next(row['relation_family'] for row in d['relation_types'] if row['relation_type'] == incoming['relation_type'])
        basis = incoming.get('basis', 'source_exposition')
        review_label = incoming.get('public_review_label') or ('Secondary reconstruction; no historical priority claimed' if basis == 'secondary_reconstruction' else 'Located source statement; curator review pending' if basis == 'source_exposition' else 'Editorial comparison; curator review pending')
        mode = incoming.get('assertion_mode') or ('asserted' if basis in ['source_exposition', 'secondary_reconstruction'] else 'inferred')
        row = edge_record(eid, incoming['source'], incoming['target'], incoming['relation_type'], family, incoming['label'],
                          incoming['source_ids'], incoming['locator'], incoming['scope'], status='candidate',
                          mode=mode, confidence='', review_label=review_label)
        claim_id = incoming.get('claim_id') or 'claim36_' + eid
        row.update(connection_pass=MARK, evidence_ids=enc(incoming['evidence_ids']), claim_id=claim_id,
                   review_status='research_pass_needs_editor', reviewed_by='', reviewed_at='')
        if incoming.get('inference_method'):
            row['inference_method'] = incoming['inference_method']
        prior = next((old for old in originals.get('edges', []) if old['id'] == eid), {})
        if prior:
            row.update(previous_source_ids=prior.get('source_ids', '[]'), previous_evidence_ids=prior.get('evidence_ids', '[]'),
                       notes='Earlier wording and provenance are retained in this release original-record ledger.')
        upsert(d['edges'], [row], 'id')
        remember('claims', claim_id)
        claim = dict(id=claim_id, statement=incoming['scope'], subject_id=incoming['source'], predicate=incoming['relation_type'], object_id=incoming['target'],
                     status='candidate', supporting_source_ids=enc(incoming['source_ids']), supporting_evidence_ids=enc(incoming['evidence_ids']),
                     contradicting_source_ids='[]', contradicting_evidence_ids='[]', notes=review_label,
                     review_status='research_pass_needs_editor', reviewed_by='', reviewed_at='', connection_pass=MARK)
        for key, value in packet_claims.get(claim_id, {}).items():
            if key in ['action', 'id']:
                continue
            claim[key] = enc(value) if isinstance(value, list) else value
        upsert(d['claims'], [claim], 'id')

# Preserve the saved link while repairing its endpoint-sense mismatch.
audit = json.loads((S / 'connection-integrity.json').read_text(encoding='utf-8'))
for incoming in audit['evidence_additions']:
    row = copy.deepcopy(incoming)
    remember('evidence', row['id'])
    row.update(connection_pass=MARK)
    upsert(d['evidence'], [row], 'id')
for incoming in audit['profile_updates']:
    nid = incoming['node_id']
    remember('profiles', nid, 'node_id')
    remember('nodes', nid)
    saved = next(x for x in originals['profiles'] if x['node_id'] == nid)
    row = copy.deepcopy(saved)
    row['summary'] = saved.get('summary', '') + ' ' + incoming['append_to_summary']
    for field, key in [('key_distinctions', 'append_key_distinctions'), ('open_checks', 'append_open_checks'), ('source_ids', 'source_ids_to_add'), ('evidence_ids', 'evidence_ids_to_add')]:
        merge_ids(row, field, incoming.get(key, []))
    row.update(connection_pass=MARK, last_researched=DATE, review_status='research_pass_needs_editor', reviewed_by='', reviewed_at='',
               editorial_note='Biological self-production and operational discretion are compared explicitly. This source-located distinction remains a candidate for editorial acceptance.')
    upsert(d['profiles'], [row], 'node_id')
    node = next(x for x in d['nodes'] if x['id'] == nid)
    node.update(connection_pass=MARK, review_status='research_pass_needs_editor', reviewed_by='', reviewed_at='')
    merge_ids(node, 'source_ids', incoming.get('source_ids_to_add', []))
    node['public_source_count'] = len(parse(node['source_ids']))
for incoming in audit['edge_updates']:
    remember('edges', incoming['id'])
    row = {key: copy.deepcopy(value) for key, value in incoming.items() if key != 'provenance_instruction'}
    for key in ['source_ids', 'evidence_ids']:
        row[key] = enc(row[key])
    row.update(connection_pass=MARK, review_status='research_pass_needs_editor', reviewed_by='', reviewed_at='', notes='The previous statement and its provenance are retained in this release original-record ledger.')
    upsert(d['edges'], [row], 'id')
for incoming in audit['claim_updates']:
    remember('claims', incoming['id'])
    row = copy.deepcopy(incoming)
    for key in ['supporting_source_ids', 'supporting_evidence_ids', 'contradicting_source_ids', 'contradicting_evidence_ids']:
        row[key] = enc(row[key])
    row.update(connection_pass=MARK, reviewed_by='', reviewed_at='')
    upsert(d['claims'], [row], 'id')

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
               source_packet='documentation/research-2026-11-06/', reader_url='/reading/from-observation-to-action/',
               scope='Passage-level primary exposition and explicitly labelled editorial comparisons; no new claim of historical influence.')
d['meta'].update(release=RELEASE, generated=DATE, release_digest_url='https://transduction.systems/updates/2026-11-06/',
                 iteration_focus='Observation, boundary judgement, agency, and defensible intervention',
                 release_note='Deeper conceptual profiles, three worked practice labs, and a repaired autonomy comparison with inspectable evidence.',
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

css = '*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#faf8f2;color:#302b26;font:18px/1.7 Georgia,serif}main,nav,footer{max-width:65rem;margin:auto;padding:1.4rem}main{overflow-wrap:anywhere}nav{display:flex;gap:1rem;flex-wrap:wrap;font:1rem/1.5 system-ui}a{color:#973d32;overflow-wrap:anywhere}a:focus-visible,summary:focus-visible{outline:3px solid #973d32;outline-offset:3px}h1{font-size:clamp(2.1rem,6vw,3.6rem);line-height:1.14;max-width:19ch}h2{font-size:1.8rem;line-height:1.25}h3{font-size:1.3rem}section{border-top:1px solid #d8d0c5;padding:1.4rem 0;margin-top:1.4rem;scroll-margin-top:1rem}.meta,.source,.note{font:1rem/1.6 system-ui}.note{background:#f0eadd;padding:1rem;border-left:3px solid #973d32}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,17rem),1fr));gap:1.2rem}.grid article{border:1px solid #d8d0c5;border-top:3px solid #973d32;padding:1rem}.grid h2{font-size:1.4rem}li{margin-bottom:.6rem}details{padding:.8rem 0}summary{cursor:pointer}#openUpdates{position:fixed;bottom:0;right:0;width:44px;height:44px}#openUpdates:after{content:"";position:absolute;right:8px;bottom:8px;width:5px;height:5px;background:#862719;border-radius:50%;box-shadow:0 0 0 1px white}@media(max-width:600px){main,nav,footer{padding:1rem}ul,ol{padding-left:1.3rem}}@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}'

def page(route, title, body):
    dest = D/route.strip('/')
    dest.mkdir(parents=True, exist_ok=True)
    content = '<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+E(title)+' | The Necessary Tangle</title><meta name="description" content="Primary reading and worked inquiry across observation, boundaries, agency, and decision rights."><link rel="canonical" href="https://transduction.systems'+route+'"><style>'+css+'</style></head><body><nav aria-label="Main">'+link('/','Atlas')+link('/library/','Sources')+link('/learning/','Learning')+link('/updates/2026-11-06/','Latest update')+'</nav><main><p class="meta">Release 0.36 · 6 November 2026</p><h1>'+E(title)+'</h1>'+body+'</main><footer><p>Curated by '+link('https://www.antlerboy.com/','Benjamin P Taylor')+'. Primary-source research assisted by AI. Sources retain their authorship and terms. Editorial comparisons are identified where they occur.</p><p>'+link('/contribute/','Suggest a source or challenge a connection')+'</p></footer><a id="openUpdates" href="https://github.com/antlerboy/the-necessary-tangle/issues/2" aria-label="Open updates"></a></body></html>\n'
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
body += '<p>'+link('/updates/2026-11-06/evidence.json','Download the evidence packet')+'</p></section>'
page('/reading/from-observation-to-action/', 'Who can see, judge, and act?', body)

cards = '<div class="grid card-grid three">'
for anchor, title, description in [
    ('observation', 'What does an observer select?', 'Distinguish a situated account from a claim that every account is equally defensible.'),
    ('judgement', 'Whose account can change the decision?', 'Keep affected people, boundary judgements, and unresolved disagreement visible.'),
    ('action', 'Who can act, and on what terms?', 'Follow structure, agency, method transitions, and the difference between self-production and operational discretion.')]:
    cards += '<article class="card"><h2>'+link('/reading/from-observation-to-action/#'+anchor, title)+'</h2><p>'+E(description)+'</p></article>'
cards += '</div>'
digest = '<p>This release follows a practical difficulty: recognising different accounts of a situation does not decide whose judgement governs, who can act, or how an intervention should change when its assumptions fail.</p>'+cards
digest += '<section><h2>What changed</h2><p>'+str(changed['profiles'])+' profiles deepened or qualified; '+str(edge_additions)+' connections added and '+str(edge_revisions)+' revised. Three existing practice labs gain six worked rounds and four checks. The autonomy comparison retains its saved identifier but now distinguishes biological self-production from operational discretion.</p><p>'+link('/reading/from-observation-to-action/','Read the source guide')+' · '+link('/systems-thinking/practice/','Try the practice labs')+' · '+link('evidence.json','Inspect the evidence packet')+'</p></section><section><h2>Limits</h2><p>Source exposition and editorial comparison retain their distinct research status. Worked cases and counterexamples are explicitly invented for testing an inference. They are not evidence that an intervention worked in an actual organisation. Publication does not record a named curator’s acceptance, historical influence, or independent teaching review.</p></section>'
page('/updates/2026-11-06/', 'Observation, boundaries, and the authority to act', digest)
(D/'updates/2026-11-06/evidence.json').write_text(json.dumps(dict(date=DATE, scope=d[MARK]['scope'], packets=packets, connection_audit=audit, practice=json.loads((S/'practice-deepening.json').read_text(encoding='utf-8'))), ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
block = '<section class="resource-pathways plain-panel wide" id="observation-and-action"><p class="eyebrow">Primary reading · Release 0.36</p><h2>'+link('/reading/from-observation-to-action/','Observation, boundaries, and the authority to act')+'</h2><p>Follow situated accounts through boundary judgement, practical inquiry, and the conditions for action.</p>'+cards.replace('<h2>', '<h3>').replace('</h2>', '</h3>')+'</section>'
for name in ['index.html', 'library/index.html', 'learning/index.html', 'updates/index.html']:
    p = D/name
    text = p.read_text(encoding='utf-8')
    text = re.sub(r'<!-- '+MARK+r' -->.*?<!-- /'+MARK+r' -->', '', text, flags=re.S)
    insertion = '<!-- '+MARK+' -->'+block+'<!-- /'+MARK+' -->'
    if name == 'index.html':
        text = text.replace('<section id="systemsPracticeCallout"', insertion+'<section id="systemsPracticeCallout"', 1)
        if '<!-- '+MARK+' -->' not in text:
            raise RuntimeError('Cannot locate the homepage view')
        text = re.sub(r'<span id="releaseBadge">Release [^<]+</span>', '<span id="releaseBadge">Release 0.36</span>', text, count=1)
        text = re.sub(r'assets/public-data.js\?v=[^"\s]+', 'assets/public-data.js?v=0.36', text)
    else:
        text = text.replace('</main>', insertion+'</main>', 1)
    p.write_text(text, encoding='utf-8')

p = D/'sitemap.xml'
text = p.read_text(encoding='utf-8')
for route in ['/reading/from-observation-to-action/', '/updates/2026-11-06/']:
    url = 'https://transduction.systems'+route
    if url not in text:
        text = text.replace('</urlset>', '<url><loc>'+url+'</loc><lastmod>'+DATE+'</lastmod></url></urlset>')
p.write_text(text, encoding='utf-8')
p = R/'README.md'
text = p.read_text(encoding='utf-8')
current = 'Current release: **0.36, 6 November 2026**. [Deeper references and connections](https://transduction.systems/updates/2026-11-06/). [Read the connected source guide](https://transduction.systems/reading/from-observation-to-action/).'
text = re.sub(r'<!-- current-31 -->.*?<!-- /current-31 -->', '<!-- current-31 -->\n'+current+'\n<!-- /current-31 -->', text, flags=re.S)
p.write_text(text, encoding='utf-8')
p = R/'CITATION.cff'
text = re.sub(r'^version:.*$', "version: '0.36'", p.read_text(encoding='utf-8'), flags=re.M)
text = re.sub(r'^date-released:.*$', "date-released: '2026-11-06'", text, flags=re.M)
p.write_text(text, encoding='utf-8')
p = R/'CHANGELOG.md'
text = p.read_text(encoding='utf-8')
entry = '\n\n## 0.36 — 6 November 2026\n\nSource-located distinctions across observation, plural perspectives, boundary critique, structure and agency, plus deeper practice labs and an explicit autonomy comparison. '+str(changed['profiles'])+' profiles deepened or developed, '+str(changed['edges'])+' connections, '+str(changed['sources'])+' source records, and one guided journey. Passage locators and evidence records distinguish exposition from editorial comparison. A connected reading guide, evidence download, homepage and library routes, and reproducible baseline accompany the release. Exact publication and live verification are recorded by the Publish workflow and deployment.json.\n'
if '## 0.36 — 6 November 2026' not in text:
    text = text.replace('# Changelog', '# Changelog'+entry, 1)
p.write_text(text, encoding='utf-8')

p = R/'documentation/TANGLE_STATE.md'
text = p.read_text(encoding='utf-8')
text = re.sub(r'<!-- '+MARK+r' -->.*?<!-- /'+MARK+r' -->\s*', '', text, flags=re.S)
state = '<!-- '+MARK+' -->\n## Current release 0.36\n\n6 November 2026. '+str(metrics['public_entries'])+' public entries, '+str(len(d['edges']))+' edges, '+str(len(d['sources']))+' sources, and '+str(len(d['profiles']))+' profiles. This release deepens '+str(changed['profiles'])+' profiles, adds '+str(edge_additions)+' scoped connections, revises '+str(edge_revisions)+', and adds one journey. The source packet is documentation/research-2026-11-06/. Reader route: https://transduction.systems/reading/from-observation-to-action/. Publication identity and live test completion belong to deployment.json and the Publish workflow. Source exposition and editorial comparison remain candidates for editorial acceptance; no historical influence is inferred from resemblance. The previous release account and companion-page record below remain historical context.\n<!-- /'+MARK+' -->\n\n'
text = text.replace('## Current release 0.35', '## Previous graph release 0.35')
text = text.replace('# Current Tangle state\n', '# Current Tangle state\n\n'+state, 1)
p.write_text(text, encoding='utf-8')
packet = (S/'work-packet.md').read_text(encoding='utf-8')
(R/'documentation/NEXT_WORK.md').write_text(packet, encoding='utf-8')
print('Release 0.36 prepared:', json.dumps(changed, sort_keys=True))
