#!/usr/bin/env python3
"""Publish the selected SysPrac26 sources and two public follow-up workshops."""
from datetime import date
from html import escape
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit
import json
import re
import xml.etree.ElementTree as ET

from build_readable_atlas import page

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
ROUTE = '/library/sysprac26/'
MARKER = 'sysprac26-collection'


def link(url, label):
    return '<a href="' + escape(url, quote=True) + '">' + escape(label) + '</a>'


def marked(text, body, insertion):
    start, end = '<!-- ' + MARKER + ' -->', '<!-- /' + MARKER + ' -->'
    block = start + body + end
    if start in text:
        return re.sub(re.escape(start) + '.*?' + re.escape(end), lambda _: block, text, flags=re.S)
    assert insertion in text, insertion
    return text.replace(insertion, insertion + block, 1)


def canonical(url):
    parts = urlsplit(url)
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower().removeprefix('www.'), parts.path.rstrip('/'), parts.query, ''))


def main():
    manifest = json.loads((ROOT / 'sources/sysprac26/collection.json').read_text())
    evidence = json.loads((ROOT / manifest['conference_packet']).read_text())
    sources = {row['id']: row for row in evidence['sources']}
    data = json.loads((ROOT / 'data/public-data.json').read_text())
    workshops = manifest['workshops']
    assert len(workshops) == 2 and len(manifest['conference']) == 6
    assert len({w['id'] for w in workshops}) == len(workshops)
    for workshop in workshops:
        date.fromisoformat(workshop['date'])
        assert re.fullmatch('[a-z][a-z0-9-]+', workshop['anchor'])

    body = '<p class="lead">Six conference sessions and two follow-up workshops from Systems Practice 2026.</p>'
    body += '<p>Read the conference accounts, explore Benjamin P Taylor’s workshop resources, or visit the ' + link(manifest['catalogue_url'], 'full SCiO conference resource catalogue') + '.</p>'
    body += '<nav aria-label="On this page">' + link('#conference-sessions', 'Conference sessions')
    for workshop in workshops:
        body += link('#' + workshop['anchor'], workshop['title'])
    body += '</nav><section aria-labelledby="follow-up-workshops"><h2 id="follow-up-workshops">Follow-up workshops</h2>'
    records = []
    for workshop in workshops:
        body += '<article id="' + workshop['anchor'] + '"><h3>' + escape(workshop['title']) + '</h3>'
        body += '<p class="eyebrow">Benjamin P Taylor · <time datetime="' + workshop['date'] + '">' + workshop['date_label'] + '</time> · Online</p>'
        for paragraph in workshop['paragraphs']:
            body += '<p>' + escape(paragraph) + '</p>'
        body += '<p>' + link(workshop['url'], 'Open the practical guide')
        if workshop.get('account_url'):
            body += ' · ' + link(workshop['account_url'], 'Read the September session account')
        body += '</p><p><em>A question to take into practice:</em> ' + escape(workshop['question']) + '</p>'
        body += '<details><summary>Session title, sources, and scope</summary><p>Advertised as ‘' + escape(workshop['advertised_title']) + '’. ' + link(workshop['announcement_url'], 'Original workshop announcement') + '.</p>'
        body += '<p>' + escape(workshop['scope']) + '</p><p>Source locations: ' + escape(workshop['locator']) + '.</p></details></article>'
        records.append({
            'id': workshop['id'], 'title': workshop['title'], 'url': workshop['url'],
            'authors': workshop['authors'], 'collection': 'SysPrac26',
            'format': 'Workshop and practical guide', 'year': '2026',
            'event_date': workshop['date'], 'summary': workshop['summary'],
            'review': 'Public workshop account and developed resources read; later teaching development distinguished from the event.',
            'locator': workshop['locator'], 'reading_url': ROUTE + '#' + workshop['anchor'],
            'announcement_url': workshop['announcement_url'], 'connections': [], 'atlas_id': ''
        })
    body += '</section><section id="conference-sessions"><h2>Six conference sessions</h2>'
    body += '<p>' + link(manifest['conference_guide'], 'What makes action possible?') + ' brings these six attributed accounts together through questions about action, autonomy, meaning, and strategy. The comparison is editorial; the speakers do not present a shared framework.</p><ul class="connections">'
    for selected in manifest['conference']:
        source = sources[selected['source_id']]
        body += '<li><h3>' + escape(source['title']) + '</h3><p>' + escape(', '.join(source['authors'])) + ' · ' + escape(selected['summary']) + '</p><p>' + link(source['url'], 'Watch the public recording') + '</p></li>'
        records.append({
            'id': source['id'], 'title': source['title'], 'url': source['url'],
            'authors': source['authors'], 'collection': 'SysPrac26', 'format': 'Conference session',
            'year': '2026', 'summary': 'SysPrac26 conference session. ' + selected['summary'],
            'review': source['verified'] + ' ' + source['limits'] + ' Human editorial acceptance of the account remains pending.',
            'locator': source['locator'], 'reading_url': manifest['conference_guide'],
            'connections': [], 'atlas_id': ''
        })
    body += '</ul><p>' + link(manifest['conference_guide'], 'Read the six-session guide and its source limits') + ' · ' + link('/library/?collection=SysPrac26', 'Search this collection') + '</p></section>'
    body += '<section><h2>Collection scope</h2><p>This selection has six conference accounts and two subsequent workshops. Full conference harvesting and review are still in progress. The conference accounts draw on public descriptions and recovered captions, with the limits recorded in the guide; human editorial acceptance remains pending. Workshop resources distinguish actual discussion from later teaching development.</p>'
    body += '<p>The ' + link(manifest['catalogue_url'], 'SCiO catalogue') + ' contains the wider programme. Original sources retain their authorship, access conditions, and terms.</p></section>'
    html = page(manifest['title'], 'SysPrac26 conference accounts and Benjamin P Taylor’s two follow-up workshops, with public sources and practical resources.', ROUTE, body, data['meta']['release'])
    html = html.replace('Readable atlas · Release ' + data['meta']['release'], 'Source collection · Updated 9 November 2026')
    folder = DOCS / ROUTE.strip('/')
    folder.mkdir(parents=True, exist_ok=True)
    (folder / 'index.html').write_text(html, encoding='utf-8')

    # Upsert by stable ID or the same public source URL; preserve earlier identities
    # and any evidenced concept connections instead of manufacturing new ones.
    catalogue_path = DOCS / 'library/catalogue.json'
    catalogue = json.loads(catalogue_path.read_text())
    for incoming in records:
        matches = [i for i, row in enumerate(catalogue['records']) if row['id'] == incoming['id'] or canonical(row['url']) == canonical(incoming['url'])]
        assert len(matches) <= 1, 'Resolve ambiguous source identity: ' + incoming['url']
        if matches:
            index = matches[0]
            old = catalogue['records'][index]
            incoming['id'] = old['id']
            incoming['connections'] = old.get('connections', [])
            incoming['atlas_id'] = old.get('atlas_id', '')
            catalogue['records'][index] = {**old, **incoming}
        else:
            catalogue['records'].append(incoming)
    catalogue['counts']['source_register_records'] = len(catalogue['records'])
    catalogue['counts']['sysprac26_records'] = len(records)
    catalogue_path.write_text(json.dumps(catalogue, ensure_ascii=False, separators=(',', ':')) + '\n', encoding='utf-8')

    index_path = DOCS / 'library/index.html'
    index_block = '<section class="resource-pathways" id="sysprac26-collection"><h2>' + link(ROUTE, 'SysPrac26 collection') + '</h2><p>Six conference accounts and Benjamin P Taylor’s follow-up workshops on systemic consulting and relational public services.</p></section>'
    index_path.write_text(marked(index_path.read_text(), index_block, '</header>'), encoding='utf-8')
    guide_path = DOCS / manifest['conference_guide'].strip('/') / 'index.html'
    guide_block = '<p class="meta">Part of the ' + link(ROUTE, 'SysPrac26 collection') + ', including Benjamin P Taylor’s two follow-up workshops.</p>'
    guide_path.write_text(marked(guide_path.read_text(), guide_block, '<h1>What makes action possible?</h1>'), encoding='utf-8')

    namespace = 'http://www.sitemaps.org/schemas/sitemap/0.9'
    ET.register_namespace('', namespace)
    sitemap = ET.parse(DOCS / 'sitemap.xml')
    root = sitemap.getroot()
    url = 'https://transduction.systems' + ROUTE
    if not any(row.findtext('{' + namespace + '}loc') == url for row in root):
        row = ET.Element('{' + namespace + '}url')
        ET.SubElement(row, '{' + namespace + '}loc').text = url
        generated = ('https://transduction.systems/entries/', 'https://transduction.systems/journeys/', 'https://transduction.systems/stewardship/')
        position = next((i for i, child in enumerate(root) if (child.findtext('{' + namespace + '}loc') or '').startswith(generated)), len(root))
        root.insert(position, row)
    ET.indent(sitemap, space='  ')
    sitemap.write(DOCS / 'sitemap.xml', encoding='utf-8', xml_declaration=True)

    next_path = ROOT / 'documentation/NEXT_WORK.md'
    next_text = next_path.read_text(encoding='utf-8').replace('## Current packet: feedback and regulation 0.41', '## Previous packet: feedback and regulation 0.41')
    note = '''
## Current packet: SysPrac26 collection and follow-up workshops

Benjamin P Taylor authorised this addition on 9 November 2026. The maintained collection is `/library/sysprac26/`: six previously published conference accounts and two public follow-up workshop resources, with eight searchable source records. The bounded packet is `sources/sysprac26/PACKET.md`. Full conference harvesting and review remain incomplete; this addition does not complete the wider corpus work in issue 96. The graph and release number are unchanged. `make validate` passed locally. The Publish workflow supplies the required desktop/mobile browser gate, deployment identity, and live verification; consult its current result and `deployment.json` before claiming a live release. No further work is authorised by this packet after these checks succeed.
'''
    next_path.write_text(marked(next_text, note, '# Next work\n'), encoding='utf-8')
    print('SysPrac26: six existing conference sources, two follow-up workshops, and a discoverable collection; graph unchanged.')


if __name__ == '__main__':
    main()
