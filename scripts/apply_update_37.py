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
S = R / 'documentation/research-2026-11-06-foundational'
MARK = 'foundational_20261106'
DATE = '2026-11-06'
RELEASE = '0.37'
d = json.loads((R / 'data/public-data.json').read_text(encoding='utf-8'))
packets = [json.loads((S / name).read_text(encoding='utf-8')) for name in ['packet.json']]
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
        for field in ['doi', 'isbn', 'licence', 'archived_url', 'reading_url', 'translator', 'access', 'content_hash']:
            if src.get(field) or prior.get(field):
                row[field] = src.get(field) or prior[field]
        row.update(connection_pass=MARK, last_checked=DATE, source_locator=src['locator'],
                   review_status='research_pass_needs_editor', reviewed_by='', reviewed_at='', access_note=src.get('limits', ''))
        upsert(d['sources'], [row], 'id')
    for incoming in packet.get('evidence_proposals', []):
        remember('evidence', incoming['id'])
        row = {key: copy.deepcopy(value) for key, value in incoming.items() if key != 'action'}
        row.update(connection_pass=MARK, review_status='research_pass_needs_editor', reviewed_by='', reviewed_at='')
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
        node.update(connection_pass=MARK, publication_level='profile', canonical_definition=profile['canonical_definition'], review_status='research_pass_needs_editor', reviewed_by='', reviewed_at='')
        merge_ids(node, 'source_ids', incoming['source_ids'])
        node['public_source_count'] = len(parse(node['source_ids']))

    for journey in packet.get('journeys', []):
        journey = copy.deepcopy(journey)
        journey.update(connection_pass=MARK, review_status='research_pass_needs_editor', reviewed_by='', reviewed_at='', generated=DATE)
        upsert(d['journeys'], [journey], 'id')

refresh_counts(d)
d['relational_depth'] = calculate_relational_depth(d)
d['relational_depth'].update(release=RELEASE, generated=DATE)
d['graph_snapshot'] = calculate(d)
metrics = graph_metrics(d)
depth = d['relational_depth']['aggregate']
changed = {key: len([x for x in d[key] if x.get('connection_pass') == MARK]) for key in ['nodes', 'profiles', 'sources', 'edges', 'evidence', 'claims', 'journeys']}
edge_revisions = 0
edge_additions = changed['edges'] - edge_revisions
d[MARK] = dict(date=DATE, originals=originals, counts=changed,
               edge_additions=edge_additions, edge_revisions=edge_revisions,
               source_packet='documentation/research-2026-11-06-foundational/', reader_url='/reading/models-and-patterns/',
               scope='Located primary exposition and editorial questions; the sequence does not assert influence.')
d['meta'].update(release=RELEASE, generated=DATE, release_digest_url='https://transduction.systems/updates/2026-11-06-foundational/',
                 iteration_focus='Models and patterns',
                 release_note='Four primary-paper accounts and an editorial reading journey.',
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
    content = '<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+E(title)+' | The Necessary Tangle</title><meta name="description" content="Primary sources, models, patterns, and the limits of transfer."><link rel="canonical" href="https://transduction.systems'+route+'"><style>'+css+'</style></head><body><nav aria-label="Main">'+link('/','Atlas')+link('/library/','Sources')+link('/learning/','Learning')+link('/updates/2026-11-06-foundational/','Latest update')+'</nav><main><p class="meta">Release 0.37 · 6 November 2026</p><h1>'+E(title)+'</h1>'+body+'</main><footer><p>Curated by '+link('https://www.antlerboy.com/','Benjamin P Taylor')+'. Primary-source research assisted by AI. Sources retain their authorship and terms. Editorial comparisons are identified where they occur.</p><p>'+link('/contribute/','Suggest a source or challenge a connection')+'</p></footer><a id="openUpdates" href="https://github.com/antlerboy/the-necessary-tangle/issues/2" aria-label="Open updates"></a></body></html>\n'
    (dest/'index.html').write_text(content, encoding='utf-8')

body = (S/'reading.html').read_text(encoding='utf-8')
body = re.sub(r'\{\{atlas:([^}]+)\}\}', lambda m: atlas(m[1]), body)
sources = {s['id']: s for s in d['sources']}
body = re.sub(r'\{\{source:([^}]+)\}\}', lambda m: link(sources[m[1]]['url'], sources[m[1]]['title']), body)
body += '<section id="sources"><h2>Primary sources and passage checks</h2>'
for src in packets[0]['sources']:
    body += '<article id="'+E(src['id'])+'"><h3>'+link(src['url'], src['title'])+'</h3><p>'+E(src['locator'])+'</p><p>'+E(src.get('verified',''))+'</p><p>'+E(src.get('limits',''))+'</p>'
    if src.get('reading_url'):
        body += '<p>'+link(src['reading_url'], 'Inspected reading copy')+'</p>'
    body += '</article>'
body += '<p>'+link('/updates/2026-11-06-foundational/evidence.json','Download the evidence packet')+'</p></section>'
page('/reading/models-and-patterns/', 'What can a model show?', body)
digest = '<p>Four source-located accounts explore patterns, sensitivity, segregation, and cooperation. Each makes its assumptions visible and asks what, if anything, can be carried into organisational inquiry.</p><section><h2>Read the models</h2><p>'+link('/reading/models-and-patterns/','Read the source guide')+' · '+link('evidence.json','Inspect the evidence packet')+'</p></section><section><h2>Limits</h2><p>The journey is an editorial sequence, not a claim of historical influence. Model results depend on their rules and conditions; they do not establish universal causes or organisational laws. New exposition awaits editorial acceptance.</p></section>'
page('/updates/2026-11-06-foundational/', 'Models, patterns, and their limits', digest)
(D/'updates/2026-11-06-foundational/evidence.json').write_text(json.dumps(dict(date=DATE, scope=d[MARK]['scope'], packet=packets[0]), ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
block = '<section class="resource-pathways plain-panel wide" id="models-and-patterns"><p class="eyebrow">Primary reading · Release 0.37</p><h2>'+link('/reading/models-and-patterns/','What can a model show?')+'</h2><p>Explore four models, their conditions, and questions about transferring their results.</p></section>'
for name in ['index.html', 'library/index.html', 'learning/index.html', 'updates/index.html']:
    p = D/name
    text = p.read_text(encoding='utf-8')
    text = re.sub(r'<!-- '+MARK+r' -->.*?<!-- /'+MARK+r' -->', '', text, flags=re.S)
    insertion = '<!-- '+MARK+' -->'+block+'<!-- /'+MARK+' -->'
    if name == 'index.html':
        text = text.replace('<section id="systemsPracticeCallout"', insertion+'<section id="systemsPracticeCallout"', 1)
        assert '<!-- '+MARK+' -->' in text
        text = re.sub(r'<span id="releaseBadge">Release [^<]+</span>', '<span id="releaseBadge">Release 0.37</span>', text, count=1)
        text = re.sub(r'assets/public-data.js\?v=[^"\s]+', 'assets/public-data.js?v=0.37', text)
    else:
        text = text.replace('</main>', insertion+'</main>', 1)
    p.write_text(text, encoding='utf-8')
p = D/'sitemap.xml'
text = p.read_text(encoding='utf-8')
for route in ['/reading/models-and-patterns/', '/updates/2026-11-06-foundational/']:
    url = 'https://transduction.systems'+route
    if url not in text:
        text = text.replace('</urlset>', '<url><loc>'+url+'</loc><lastmod>'+DATE+'</lastmod></url></urlset>')
p.write_text(text, encoding='utf-8')
p = R/'README.md'
text = re.sub(r'<!-- current-31 -->.*?<!-- /current-31 -->', '<!-- current-31 -->\nCurrent release: **0.37, 6 November 2026**. [Models, patterns, and their limits](https://transduction.systems/updates/2026-11-06-foundational/). [Read the source guide](https://transduction.systems/reading/models-and-patterns/).\n<!-- /current-31 -->', p.read_text(encoding='utf-8'), flags=re.S)
p.write_text(text, encoding='utf-8')
p = R/'CITATION.cff'
text = re.sub(r'^version:.*$', "version: '0.37'", p.read_text(encoding='utf-8'), flags=re.M)
text = re.sub(r'^date-released:.*$', "date-released: '2026-11-06'", text, flags=re.M)
p.write_text(text, encoding='utf-8')
p = R/'CHANGELOG.md'
text = p.read_text(encoding='utf-8')
entry = '\n\n## 0.37 — 6 November 2026\n\nFour existing foundational-paper entries gain primary-source-located profiles and an editorial reading journey. Model rules, examples, and limits remain visible; new exposition awaits editorial acceptance. The earlier 6 November digest is retained.\n'
if '## 0.37 — 6 November 2026' not in text:
    text = text.replace('# Changelog', '# Changelog'+entry, 1)
p.write_text(text, encoding='utf-8')
p = R/'documentation/TANGLE_STATE.md'
text = re.sub(r'<!-- '+MARK+r' -->.*?<!-- /'+MARK+r' -->\s*', '', p.read_text(encoding='utf-8'), flags=re.S)
text = text.replace('## Current release 0.36', '## Previous graph release 0.36')
state = '<!-- '+MARK+' -->\n## Current release 0.37\n\n6 November 2026. '+str(metrics['public_entries'])+' public entries, '+str(len(d['edges']))+' edges, '+str(len(d['sources']))+' sources, and '+str(len(d['profiles']))+' profiles. Four existing publication entries have source-located profiles and one editorial reading journey. The source packet is documentation/research-2026-11-06-foundational/. Reader route: https://transduction.systems/reading/models-and-patterns/. New exposition awaits editorial acceptance. Deployment identity and live checks belong to deployment.json and the Publish workflow.\n<!-- /'+MARK+' -->\n\n'
text = text.replace('# Current Tangle state\n', '# Current Tangle state\n\n'+state, 1)
p.write_text(text, encoding='utf-8')
(R/'documentation/NEXT_WORK.md').write_text((S/'work-packet.md').read_text(encoding='utf-8'), encoding='utf-8')
print('Release 0.37 prepared:', json.dumps(changed, sort_keys=True))

