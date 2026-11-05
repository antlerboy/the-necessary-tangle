#!/usr/bin/env python3
"""Publish readable entry/journey pages from the already-public atlas projection.

No new research, acceptance decisions, or third-party source texts are added.
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path
from urllib.parse import quote
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
BASE = 'https://transduction.systems'
MARKER = 'readable-atlas-20261105'


def esc(value):
    return html.escape(str(value or ''), quote=True)


def unpack(value):
    if isinstance(value, list):
        return value
    try:
        parsed = json.loads(value or '[]')
        return parsed if isinstance(parsed, list) else []
    except (ValueError, TypeError):
        return []


def human(value):
    return str(value or 'not recorded').replace('_', ' ')


def structured(record):
    """Decode the source's legacy list fields for ordinary JSON consumers."""
    fields = {'aliases', 'source_ids', 'evidence_ids', 'set_tags', 'espoused_labels',
              'observed_clusters', 'geographies', 'key_distinctions',
              'historical_lineage', 'logical_antecedents', 'dependent_subsequents',
              'practice_connections', 'espoused_lineages', 'common_misreadings',
              'open_checks', 'supporting_source_ids', 'supporting_evidence_ids',
              'contradicting_source_ids', 'contradicting_evidence_ids', 'creators'}
    result = {}
    for key, value in record.items():
        if key in fields:
            decoded = unpack(value)
            # Preserve a legacy plain-text value rather than silently dropping it.
            result[key] = decoded if decoded or not value or value == '[]' else [value]
        else:
            result[key] = value
    return result


def route(kind, ident):
    if not re.fullmatch(r'[a-zA-Z0-9_-]+', ident):
        raise ValueError('Unsafe atlas identifier: ' + ident)
    return f'/{kind}/{ident}/'


def write(relative, text):
    target = DOCS / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding='utf-8')


def paragraph(value):
    return '<p>' + esc(value) + '</p>' if value else ''


def page(title, description, path, body, release):
    return f'''<!doctype html>
<html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} | The Necessary Tangle</title><meta name="description" content="{esc(description[:260])}">
<meta name="author" content="Benjamin P Taylor"><meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description[:260])}"><meta property="og:url" content="{BASE}{path}">
<link rel="canonical" href="{BASE}{path}"><link rel="icon" href="/favicon.svg"><link rel="stylesheet" href="/assets/readable-atlas.css">
</head><body class="readable-atlas"><a class="skip-link" href="#main">Skip to content</a>
<header><a class="brand" href="/">The Necessary Tangle</a><nav aria-label="Main navigation"><a href="/entries/">Entries</a><a href="/journeys/">Reading journeys</a><a href="/systems-thinking/claim-lab/">Test a claim</a><a href="/systems-thinking/practice/">Practice</a><a href="/library/">Sources</a></nav></header>
<main id="main"><p class="eyebrow">Readable atlas · Release {esc(release)}</p><h1>{esc(title)}</h1>{body}</main>
<footer><p>Curated by <a href="https://antlerboy.com/">Benjamin P Taylor</a>. AI-assisted research and publishing. These pages preserve the atlas's recorded review status; generation is not independent review.</p>
<p>Original atlas text and data: <a href="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA 4.0</a>. Linked works retain their authorship and terms. <a href="/stewardship/">Responsibility and maintenance</a> · <a href="/#view=contribute">Suggest a correction</a>.</p></footer>
<a class="update-thread-dot" href="https://github.com/antlerboy/the-necessary-tangle/issues/2" target="_blank" rel="noopener" aria-label="Open updates"></a></body></html>'''


def main():
    manifest_path = DOCS / 'entries/manifest.json'
    previous_routes = json.loads(manifest_path.read_text(encoding='utf-8')).get('routes', []) if manifest_path.exists() else []
    data = json.loads((DOCS / 'assets/public-data.json').read_text(encoding='utf-8'))
    release = data['meta']['release']
    redirects = data.get('canonical_redirects', {})
    nodes = {n['id']: n for n in data['nodes'] if n.get('public_visibility') == 'public' and redirects.get(n['id'], n['id']) == n['id']}
    profiles = {p['node_id']: p for p in data['profiles'] if p['node_id'] in nodes}
    sources = {s['id']: s for s in data['sources']}
    evidence = {e['id']: e for e in data['evidence']}
    edges = [e for e in data['edges'] if e['source'] in nodes and e['target'] in nodes]
    journeys = data['journeys']
    urls = ['/entries/', '/journeys/', '/stewardship/']
    records = []

    def node_link(ident):
        n = nodes.get(ident)
        return route('entries', ident) if ident in profiles else '/#view=item&id=' + quote(ident)

    def source_html(ident):
        source = sources.get(ident)
        if not source:
            return '<li>Source record unavailable: ' + esc(ident) + '</li>'
        url = source.get('url', '')
        title = '<a href="' + esc(url) + '">' + esc(source['title']) + '</a>' if url.startswith(('https://', 'http://')) else esc(source['title']) + ' · No public link'
        return '<li>' + title + ' <small>(' + esc(human(source.get('review_status'))) + ')</small></li>'

    sections = [('Summary', 'summary'), ('Why use this distinction?', 'why_it_matters'), ('Key distinctions', 'key_distinctions'), ('Historical development', 'historical_lineage'), ('Ideas it depends on', 'logical_antecedents'), ('What develops from it', 'dependent_subsequents'), ('Connections to practice', 'practice_connections'), ('Common confusions', 'common_misreadings'), ('Open questions', 'open_checks')]
    for ident, profile in sorted(profiles.items(), key=lambda pair: nodes[pair[0]]['label'].casefold()):
        node = nodes[ident]
        title = node['label']
        path = route('entries', ident)
        urls.append(path)
        definition = profile.get('canonical_definition') or node.get('canonical_definition') or node.get('description') or ''
        source_ids = list(dict.fromkeys(unpack(node.get('source_ids')) + unpack(profile.get('source_ids'))))
        attached = [e for e in edges if ident in (e['source'], e['target'])]
        claims = [c for c in data.get('claims', []) if ident in (c.get('subject_id'), c.get('object_id'))]
        evidence_ids = list(dict.fromkeys(unpack(profile.get('evidence_ids')) + [eid for edge in attached for eid in unpack(edge.get('evidence_ids'))] + [eid for claim in claims for key in ('supporting_evidence_ids', 'contradicting_evidence_ids') for eid in unpack(claim.get(key))]))
        source_ids = list(dict.fromkeys(source_ids + [sid for edge in attached for sid in unpack(edge.get('source_ids'))] + [evidence[eid]['source_id'] for eid in evidence_ids if eid in evidence] + [sid for claim in claims for key in ('supporting_source_ids', 'contradicting_source_ids') for sid in unpack(claim.get(key))]))
        body = paragraph(definition)
        body += '<aside class="status"><h2>Review status</h2><p>Profile: ' + esc(human(profile.get('review_status') or profile.get('profile_status'))) + '. Entry: ' + esc(human(node.get('review_status'))) + '.</p>' + paragraph(profile.get('editorial_note'))
        body += '<p>Named reviewer: ' + esc(profile.get('reviewed_by') or 'not recorded for this profile') + '. Last researched: ' + esc(profile.get('last_researched') or 'not recorded') + '.</p></aside>'
        body += '<p class="actions"><a href="/#view=item&amp;id=' + esc(ident) + '">Open the interactive entry</a> · <a href="/#view=map&amp;focus=' + esc(ident) + '">Explore its map</a> · <a download href="record.json">Download the sourced record (JSON)</a></p>'
        for heading, key in sections:
            value = profile.get(key)
            if value:
                values = unpack(value)
                body += '<section><h2>' + heading + '</h2>' + ('<ul>' + ''.join('<li>' + esc(v) + '</li>' for v in values) + '</ul>' if values else paragraph(value)) + '</section>'
        body += '<section><h2>Recorded connections</h2><p>Each statement keeps its direction, scope, and recorded status. A connection is not automatically an accepted conclusion.</p><ul class="connections">'
        for edge in attached:
            other = edge['target'] if edge['source'] == ident else edge['source']
            wording = nodes[edge['source']]['label'] + ' ' + (edge.get('plain_phrase') or human(edge.get('relation_type'))) + ' ' + nodes[edge['target']]['label']
            body += '<li><p><a href="' + esc(node_link(other)) + '">' + esc(wording) + '</a></p><p><small>Status: ' + esc(human(edge.get('claim_status'))) + ' · Relation: ' + esc(human(edge.get('relation_type'))) + '</small></p>'
            body += paragraph(edge.get('scope_conditions')) + paragraph('Locator: ' + edge['source_locator'] if edge.get('source_locator') else 'No statement-level locator recorded.')
            body += '<ul>' + ''.join(source_html(sid) for sid in unpack(edge.get('source_ids'))) + '</ul></li>'
        body += '</ul></section>'
        if claims:
            body += '<section><h2>Claims and disputes</h2><ul>'
            for claim in claims:
                body += '<li>' + paragraph(claim.get('statement')) + paragraph('Claim status: ' + human(claim.get('status')) + '. Review status: ' + human(claim.get('review_status')) + '.') + paragraph(claim.get('notes'))
                body += '<p>Supporting sources</p><ul>' + ''.join(source_html(sid) for sid in unpack(claim.get('supporting_source_ids'))) + '</ul>'
                contrary = unpack(claim.get('contradicting_source_ids'))
                if contrary:
                    body += '<p>Contradicting sources</p><ul>' + ''.join(source_html(sid) for sid in contrary) + '</ul>'
                body += '</li>'
            body += '</ul></section>'
        body += '<section><h2>Sources and passage locators</h2><ul>' + ''.join(source_html(sid) for sid in source_ids) + '</ul>'
        locators = [{'id': eid, 'source_id': evidence[eid]['source_id'], 'locator': evidence[eid].get('locator', ''), 'review_status': evidence[eid].get('review_status', '')} for eid in evidence_ids if eid in evidence]
        body += '<ul>' + ''.join('<li>' + esc(sources.get(e['source_id'], {}).get('title', e['source_id'])) + ': ' + esc(e['locator'] or 'No precise locator recorded') + ' · ' + esc(human(e['review_status'])) + '</li>' for e in locators) + '</ul></section>'
        citation = f'Taylor, B. P. (2026). {title}. The Necessary Tangle, release {release}. {BASE}{path}'
        body += '<section><h2>Cite this entry</h2>' + paragraph(citation) + '<p>Retain the release and review status when quoting or reusing this account.</p></section>'
        record = {'schema_version': '1.0', 'canonical_url': BASE + path, 'release': release, 'citation': citation, 'licence': 'CC BY-SA 4.0 for original atlas text and data; linked works retain their own terms', 'entry': node, 'profile': profile, 'connections': attached, 'claims': claims, 'sources': [sources[sid] for sid in source_ids if sid in sources], 'evidence_locators': locators, 'reuse_note': 'Preserve source attribution, scope, and review status. Source documents and evidence excerpts are excluded.'}
        for key in ('entry', 'profile'):
            record[key] = structured(record[key])
        for key in ('connections', 'claims', 'sources'):
            record[key] = [structured(item) for item in record[key]]
        records.append(record)
        write(path.strip('/') + '/index.html', page(title, definition, path, body, release))
        write(path.strip('/') + '/record.json', json.dumps(record, ensure_ascii=False, indent=2) + '\n')

    for journey in journeys:
        path = route('journeys', journey['id'])
        urls.append(path)
        body = paragraph(journey.get('subtitle')) + paragraph(journey.get('summary'))
        body += '<aside class="status"><p>This is an editorial reading route through maintained entries. Its sequence does not establish influence, logical dependence, or independent review. Check each entry\'s sources and status.</p></aside>'
        body += '<p><a href="/#view=journeys&amp;id=' + esc(journey['id']) + '&amp;step=0">Follow this journey interactively</a></p><ol class="journey">'
        for step in journey.get('steps', []):
            ident = step['node_id']
            body += '<li><h2>' + esc(step.get('heading') or nodes.get(ident, {}).get('label', ident)) + '</h2>' + paragraph(step.get('narrative')) + '<p><a href="' + esc(node_link(ident)) + '">Read ' + esc(nodes.get(ident, {}).get('label', ident)) + '</a></p></li>'
        body += '</ol>' + paragraph(f'Taylor, B. P. (2026). {journey["title"]}. The Necessary Tangle, release {release}. {BASE}{path}')
        write(path.strip('/') + '/index.html', page(journey['title'], journey.get('summary', journey['title']), path, body, release))

    entry_list = '<p>Developed profiles from the current public release, readable without JavaScript. Development depth and editorial acceptance are different things; each page retains its recorded status.</p><p><a download href="developed-records.json">Download all developed records (JSON)</a> · <a href="/journeys/">Choose a reading journey</a></p><ul class="entry-index">'
    entry_list += ''.join('<li><a href="' + route('entries', ident) + '">' + esc(nodes[ident]['label']) + '</a> <small>· ' + esc(human(profile.get('review_status') or profile.get('profile_status'))) + '</small></li>' for ident, profile in sorted(profiles.items(), key=lambda p: nodes[p[0]]['label'].casefold())) + '</ul>'
    write('entries/index.html', page('Read the developed entries', 'Readable, citable systems, cybernetics, and complexity entries with sources and review status.', '/entries/', entry_list, release))
    write('entries/developed-records.json', json.dumps({'schema_version': '1.0', 'release': release, 'record_count': len(records), 'records': records}, ensure_ascii=False, indent=2) + '\n')
    journey_list = '<p>Choose a question and read the whole route without JavaScript. Follow a named entry to inspect its sources and status.</p><ul>' + ''.join('<li><h2><a href="' + route('journeys', j['id']) + '">' + esc(j['title']) + '</a></h2>' + paragraph(j.get('summary')) + '</li>' for j in journeys) + '</ul>'
    write('journeys/index.html', page('Choose a reading journey', 'Question-led reading routes through the evidence atlas.', '/journeys/', journey_list, release))
    stewardship = '<p>Benjamin P Taylor is the curator and remains responsible for editorial acceptance and publication. Reviewer names and decisions belong on the records they have reviewed. The roles below describe responsibilities, rather than appointments or publishing permissions.</p><h2>Contribute a bounded review</h2><p>Choose one entry, source passage, or connection. Give its URL, the exact statement, what should change, the evidence and locator, and any relevant limits or competing interpretation. A proposal does not grant publishing access.</p><p><a href="/#view=contribute">Send a correction or review proposal</a>.</p><h2>What maintenance involves</h2><p>The static entry and journey pages are generated from the existing public projection. They do not form a second evidence store. Corrections belong in the maintained atlas records and their release generator.</p><p>Sources, recorded status, passage locators, interactive routes, and calendar subscriptions must survive a release. A failed source check is a maintenance problem, not permission to remove uncertainty or invent a replacement.</p><h2>Maintenance responsibilities</h2><ul><li>Curator: acceptance, wording, disputed claims, and release decisions.</li><li>Contributors: a specific attributed proposal, source, and locator.</li><li>Maintainers: generation, links, sitemap, accessibility, downloads, and preservation of existing interactive behaviour.</li><li>Automated checks: defects and consistency only; they cannot confer truth, competence, or editorial acceptance.</li></ul><h2>Reuse</h2><p>Entry downloads contain existing original atlas records, source metadata, and locators. They exclude source documents and evidence excerpts. Retain attribution, scope, release, and review status; linked third-party works keep their own terms.</p>'
    write('stewardship/index.html', page('Responsibility and maintenance', 'Who maintains the atlas, how to propose a bounded review, and what its reusable records contain.', '/stewardship/', stewardship, release))

    home_path = DOCS / 'index.html'
    home = home_path.read_text(encoding='utf-8')
    home = re.sub(r'<!-- ' + MARKER + r' -->.*?<!-- /' + MARKER + r' -->', '', home, flags=re.S)
    cards = f'''<!-- {MARKER} --><section class="resource-pathways" aria-labelledby="practicalRoutesTitle" id="practical-routes"><h2 id="practicalRoutesTitle">What are you working on?</h2><div class="grid card-grid three"><article class="card"><h3><a href="/systems-thinking/claim-lab/">Check a transformation claim</a></h3><p>Test an improvement claim, a service redesign, or a workshop brief against a short case and counterexample.</p></article><article class="card"><h3><a href="/systems-thinking/practice/">Practise a systems method</a></h3><p>Try a fictional case, compare your reasoning, and repair a model before returning to live work.</p></article><article class="card"><h3><a href="/entries/">Find reliable reading</a></h3><p>Read developed entries, inspect their sources and status, or <a href="/journeys/">follow a complete reading journey</a>.</p></article></div></section><!-- /{MARKER} -->'''
    anchor = '<!-- depth_20261029 -->'
    if anchor not in home:
        raise ValueError('Practical-route insertion point is missing')
    home = home.replace(anchor, cards + anchor, 1)
    if 'href="/assets/readable-atlas.css"' not in home:
        home = home.replace('</head>', '<link rel="stylesheet" href="/assets/readable-atlas.css">\n</head>')
    home_path.write_text(home, encoding='utf-8')

    # The atlas keeps its existing interaction and history contract. Add ordinary
    # links to the citable editions; do not replace its stateful share links.
    app_path = DOCS / 'assets/app.js'
    app = app_path.read_text(encoding='utf-8')
    entry_action = '<button id="copyEntryLink">Copy link</button>'
    if 'Read or cite this entry' not in app:
        app = app.replace(entry_action, '${profile ? `<a class="button" href="/entries/${encodeURIComponent(node.id)}/">Read or cite this entry</a>` : \'\'}\n        ' + entry_action, 1)
    journey_action = '<div class="journey-actions">'
    if 'Read the whole journey' not in app:
        app = app.replace(journey_action, journey_action + '\n      <a class="button" href="/journeys/${encodeURIComponent(journey.id)}/">Read the whole journey</a>', 1)
    app_path.write_text(app, encoding='utf-8')

    sitemap_path = DOCS / 'sitemap.xml'
    namespace = 'http://www.sitemaps.org/schemas/sitemap/0.9'
    ET.register_namespace('', namespace)
    tree = ET.parse(sitemap_path)
    root = tree.getroot()
    for item in list(root):
        loc = item.find('{' + namespace + '}loc')
        if loc is not None and any((loc.text or '').startswith(BASE + prefix) for prefix in ('/entries/', '/journeys/', '/stewardship/')):
            root.remove(item)
    for path in urls:
        item = ET.SubElement(root, '{' + namespace + '}url')
        ET.SubElement(item, '{' + namespace + '}loc').text = BASE + path
    ET.indent(tree, space='  ')
    tree.write(sitemap_path, encoding='utf-8', xml_declaration=True)
    # Retire only files previously generated by this script, never an arbitrary
    # directory supplied by an input path. Keep unrelated content untouched.
    for old_route in set(previous_routes) - set(urls):
        match = re.fullmatch(r'/(entries|journeys)/([a-zA-Z0-9_-]+)/', old_route)
        if not match:
            continue
        directory = (DOCS / match[1] / match[2]).resolve()
        if not directory.is_relative_to((DOCS / match[1]).resolve()):
            raise ValueError('Generated route escaped its output directory')
        for name in ('index.html', 'record.json'):
            (directory / name).unlink(missing_ok=True)
        try:
            directory.rmdir()
        except OSError:
            pass
    write('entries/manifest.json', json.dumps({'release': release, 'entry_count': len(profiles), 'journey_count': len(journeys), 'routes': urls}, indent=2) + '\n')
    state_path = ROOT / 'documentation/TANGLE_STATE.md'
    state = state_path.read_text(encoding='utf-8')
    state = re.sub(r'\n<!-- readable-atlas-state -->.*?<!-- /readable-atlas-state -->\n?', '', state, flags=re.S)
    state += f'''\n<!-- readable-atlas-state -->
## Readable atlas editions: 5 November 2026

The existing public projection now generates {len(profiles)} developed entry pages and {len(journeys)} complete reading journeys, each with a stable URL. Entries preserve recorded status, sources, passage locators, claims, and typed connections. Sourced JSON downloads omit evidence excerpts and retain attribution and licence boundaries. Practical home routes, readable indexes, interactive edition links, a stewardship page, and sitemap entries are generated from the same maintained data. Graph release {release} and its claims remain unchanged. No independent teaching review or reviewer appointment is implied. Verification and publication are separate records; see documentation/estate-implementation-20261105.md.
<!-- /readable-atlas-state -->
'''
    state_path.write_text(state, encoding='utf-8')
    (ROOT / 'documentation/NEXT_WORK.md').write_text('''# Next work

Status: the authorised 5 November 2026 readable-atlas implementation is generated. Verification and coordinated publication are tracked in `documentation/estate-implementation-20261105.md`.

## Outcome

Make existing developed entries and journeys readable, citable, and reusable through stable web pages, with practical home entrances and preserved evidence distinctions.

## In scope

The readable-atlas generator, validator, generated entries and journeys, home routes, stewardship, sitemap, and build integration. Use only the existing public projection.

## Out of scope

Independent teaching review, new reviewers, corpus research, graph acceptance changes, event refresh, private disclosures, external correspondence, and uncoordinated publication.

## Acceptance checks

Full repository validation, profile/journey coverage, source/status preservation, internal links, sitemap, idempotence, sourced downloads, and desktop/mobile browser checks.

## Stop conditions

Stop when these checks pass and report the reviewable change to the coordinating task. No further research or product expansion is automatically authorised.

## Model route

Codex implementation using the current task model. No new research or model change is required.
''', encoding='utf-8')
    print(f'Readable atlas: {len(profiles)} developed entries, {len(journeys)} journeys, sourced JSON, practical home routes, and sitemap.')


if __name__ == '__main__':
    main()
