#!/usr/bin/env python3
"""Build original adventure and a public-only projection; never mutate the graph."""
from pathlib import Path
import hashlib
import html
import json
import re
import shutil
import sys
from urllib.parse import quote

R = Path(__file__).resolve().parents[1]
S = R / 'sources/adventure-42'
D = R / 'docs'
OUT = D / '42'
MARK = 'adventure-42'
DATE = '2026-11-15'

if '--reverse' in sys.argv:
    for relative in ['docs/index.html', 'docs/updates/index.html', 'README.md',
                     'documentation/TANGLE_STATE.md', 'documentation/NEXT_WORK.md']:
        path = R / relative
        content = path.read_text(encoding='utf-8')
        content = re.sub(r'<!-- ' + MARK + r' -->.*?<!-- /' + MARK + r' -->\s*', '', content, flags=re.S)
        if relative == 'docs/index.html':
            content = re.sub(r'<(?:span|a) id="releaseBadge"[^>]*>Release [^<]+</(?:span|a)>', '<span id="releaseBadge">Release 0.41</span>', content, count=1)
        path.write_text(content, encoding='utf-8')
    app = D / 'assets/app.js'
    content = app.read_text(encoding='utf-8').replace("`Release ${$('releaseBadge').dataset.readerRelease || DATA.meta.release}`", '`Release ${DATA.meta.release}`')
    app.write_text(content, encoding='utf-8')
    print('Prepared pre-adventure reader baseline for historical gates.')
    raise SystemExit(0)


def unpack(value):
    if isinstance(value, list):
        return value
    try:
        result = json.loads(value or '[]')
        return result if isinstance(result, list) else []
    except (ValueError, TypeError):
        return []


def text(value):
    return value if isinstance(value, str) else ''


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, separators=(',', ':')) + '\n', encoding='utf-8')


def source_record(record, locator=''):
    url = record.get('url', '')
    return dict(id=record['id'], title=record.get('title', record['id']),
                url=url if re.match(r'^https?://', url) else '', locator=locator)


raw = (R / 'data/public-data.json').read_bytes()
data = json.loads(raw)
worlds = json.loads((S / 'worlds.json').read_text(encoding='utf-8'))
public = [n for n in data['nodes'] if n.get('public_visibility') == 'public'
          and n.get('canonical_id', n['id']) == n['id']]
ids = {n['id'] for n in public}
assert public and all(room['anchor'] in ids for room in worlds['rooms']), 'Each room needs a real public anchor'
assert len({r['id'] for r in worlds['rooms']}) == len(worlds['rooms'])
room_ids = {r['id'] for r in worlds['rooms']}
assert all(target in room_ids for r in worlds['rooms'] for target in r['exits'].values())
profiles = {p['node_id']: p for p in data['profiles']}
sources = {s['id']: s for s in data['sources']}
evidence = {e['id']: e for e in data['evidence']}


def refs(record, extra=None):
    rows = []
    for ident in dict.fromkeys([*unpack(record.get('source_ids')), *unpack((extra or {}).get('source_ids'))]):
        if ident not in sources:
            continue
        locators = [evidence[e].get('locator', '') for e in unpack(record.get('evidence_ids'))
                    if e in evidence and evidence[e].get('source_id') == ident]
        locator = '; '.join(dict.fromkeys(x for x in locators if x)) or record.get('source_locator', '')
        rows.append(source_record(sources[ident], locator))
    return rows


nodes = []
for n in public:
    p = profiles.get(n['id'], {})
    url = '/entries/' + quote(n['id'], safe='_-') + '/'
    if not (D / url.lstrip('/') / 'index.html').exists():
        url = '/#view=item&id=' + quote(n['id'], safe='_-')
    nodes.append(dict(id=n['id'], label=n['label'], aliases=' '.join(unpack(n.get('aliases'))),
                      type=n.get('entity_type', ''), level=n.get('publication_level', 'brief entry').replace('_', ' '),
                      status=p.get('review_status') or n.get('review_status') or n.get('status') or 'not recorded',
                      summary=text(p.get('summary')) or text(n.get('description')),
                      definition=text(p.get('canonical_definition')) or text(n.get('canonical_definition')),
                      sources=refs(p, n), url=url))
edges = [dict(id=e['id'], source=e['source'], target=e['target'],
              directed=e.get('directed') in [True, 'true', 'True'],
              phrase=e.get('plain_phrase') or e['relation_type'].replace('_', ' '),
              relation_type=e['relation_type'], status=e.get('public_review_label') or e.get('claim_status', 'not recorded'),
              scope=e.get('scope_conditions', ''), locator=e.get('source_locator', ''),
              sources=refs(e)) for e in data['edges'] if e['source'] in ids and e['target'] in ids]
OUT.mkdir(parents=True, exist_ok=True)
if '--atlas-only' not in sys.argv:
    for name in ['worlds.json', 'index.html', 'adventure.css', 'engine.js', 'app.js']:
        shutil.copyfile(S / name, OUT / name)
dump(OUT / 'atlas.json', dict(graph_release=data['meta']['release'], nodes=nodes, edges=edges))
dump(OUT / 'manifest.json', dict(reader_release='0.42', graph_release=data['meta']['release'], date=DATE,
                               places=len(worlds['rooms']), public_entries=len(nodes), recorded_connections=len(edges),
                               graph_sha256=hashlib.sha256(raw).hexdigest(),
                               fiction='Original authored places and encounters; not historical testimony',
                               source_packet='sources/adventure-42/'))

if '--atlas-only' in sys.argv:
    print('Refreshed the adventure library from graph release ' + data['meta']['release'] + '; fiction and interface unchanged.')
    raise SystemExit(0)


def replace_block(path, block, after):
    content = path.read_text(encoding='utf-8')
    content = re.sub(r'<!-- ' + MARK + r' -->.*?<!-- /' + MARK + r' -->\s*', '', content, flags=re.S)
    content = content.replace(after, after + '\n<!-- ' + MARK + ' -->\n' + block + '\n<!-- /' + MARK + ' -->\n', 1)
    path.write_text(content, encoding='utf-8')


home = D / 'index.html'
content = home.read_text(encoding='utf-8')
content = re.sub(r'<!-- ' + MARK + r' -->.*?<!-- /' + MARK + r' -->\s*', '', content, flags=re.S)
feature = '''<!-- adventure-42 --><section class="resource-pathways plain-panel wide" id="adventure-42"><p class="eyebrow">Release 0.42 · An original text adventure</p><h2><a href="/42/">A&gt;TANGLE</a></h2><p>An unlisted platform, a listening instrument, weather in two glass globes, and a library with doors in its shelves. Explore systems | cybernetics | complexity through a CP/M-inspired adventure.</p><p><a class="button primary" href="/42/">Enter the adventure</a> <a href="/updates/2026-11-15-42/">About this release</a></p></section><!-- /adventure-42 -->'''
content = content.replace('<!-- readable-atlas-20261105 -->', feature + '<!-- readable-atlas-20261105 -->', 1)
reader_release = (json.loads((D / 'reader-edition.json').read_text())['reader_release']
                  if '<!-- reader-opening -->' in content else '0.42')
badge = f'<a id="releaseBadge" data-reader-release="{reader_release}" href="/versions/" aria-label="Version history, current release {reader_release}">Release {reader_release}</a>'
content = re.sub(r'<(?:span|a) id="releaseBadge"[^>]*>Release [^<]+</(?:span|a)>', badge, content, count=1)
home.write_text(content, encoding='utf-8')
# The interface can advance independently of the maintained research graph.
app = D / 'assets/app.js'
content = app.read_text(encoding='utf-8')
content = content.replace('`Release ${DATA.meta.release}`', "`Release ${$('releaseBadge').dataset.readerRelease || DATA.meta.release}`")
app.write_text(content, encoding='utf-8')

dot = '<a id="openUpdates" href="https://github.com/antlerboy/the-necessary-tangle/issues/2" aria-label="Open updates"></a>'
dot_style = '<style>#openUpdates{position:fixed;right:0;bottom:0;width:44px;height:44px;z-index:99999}#openUpdates:after{content:"";position:absolute;right:8px;bottom:8px;width:5px;height:5px;background:#862719;border-radius:50%;box-shadow:0 0 0 1px white}#openUpdates:focus-visible{outline:3px solid #ffbf47;outline-offset:-3px}</style>'
update = D / 'updates/2026-11-15-42/index.html'
update.parent.mkdir(parents=True, exist_ok=True)
update.write_text('''<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>An adventure in the Tangle | Release 0.42</title><link rel="stylesheet" href="/assets/readable-atlas.css">''' + dot_style + '''</head><body><nav aria-label="Atlas navigation"><a href="/">Atlas</a> <a href="/42/">Adventure</a> <a href="/updates/">Updates</a></nav><main><p>Reader release 0.42 · 15 November 2026</p><h1>An adventure in the Tangle</h1><p>An original, branching text adventure through systems | cybernetics | complexity, inspired by the CP/M edition of Douglas Adams and Steve Meretzky’s Infocom game. An unlisted platform opens onto laboratories, a cellular-automaton garden, a chemical conservatory, a listening instrument, an observatory, a forest, and a library of actual atlas passages.</p><p><a href="/42/">Enter the adventure</a></p><h2>Explore and investigate</h2><p>Use a command prompt or suggested actions. Investigate finite apparatus, collect what the ferry needs, take another route, and save your position. The library searches all ''' + str(len(nodes)) + ''' canonical public atlas entries. Its improbability lever draws from that entire collection and avoids repeated discoveries until the pool is exhausted. Follow a recorded connection to inspect its meaning, source, scope, and review status.</p><h2>Fiction and sources</h2><p>Rooms, objects, voices, and exits are original fiction. Maintained atlas records keep their own evidence and status. Mathematical and numerical apparatus has explicit rules and limits. No invented encounter is attributed as historical dialogue, and an authored route does not establish historical influence.</p><p>The graph research release remains ''' + html.escape(data['meta']['release']) + '''. This interface release changes no canonical nodes, relationships, profiles, or editorial acceptance. The release manifest distinguishes the reader and graph versions; deployment.json identifies the deployed revision and Publish workflow.</p><h2>The original</h2><p>The Hitchhiker’s Guide to the Galaxy, Douglas Adams and Steve Meretzky, Infocom, 1984. <a href="https://ifdb.org/viewgame?id=ouv80gvsl32xlion">Credits, history, and play links</a>. Original adventure text and puzzles here are newly authored; the original game’s text and software are not redistributed.</p></main>''' + dot + '</body></html>', encoding='utf-8')

replace_block(D / 'updates/index.html', '<section><h2><a href="/updates/2026-11-15-42/">0.42: an adventure in the Tangle</a></h2><p>A CP/M-inspired adventure through the field, connected to the maintained public atlas.</p></section>', '<main>')
sitemap = D / 'sitemap.xml'
content = sitemap.read_text(encoding='utf-8')
for route in ['/42/', '/updates/2026-11-15-42/']:
    url = 'https://transduction.systems' + route
    if url not in content:
        content = content.replace('</urlset>', '<url><loc>' + url + '</loc><lastmod>' + DATE + '</lastmod></url></urlset>')
sitemap.write_text(content, encoding='utf-8')

replace_block(R / 'documentation/TANGLE_STATE.md', '## Reader release 0.42\n\n15 November 2026. An original text adventure at https://transduction.systems/42/\nprojects the complete canonical public atlas into a searchable, source-labelled\nlibrary. Fictional places and finite apparatus remain separate from atlas\nevidence. The graph research release remains 0.41. Deployment and actual test\nresults belong to deployment.json, the Publish workflow, and the adventure\ncompletion record. No claim of successful publication follows from this build.', '# Current Tangle state')
replace_block(R / 'documentation/NEXT_WORK.md', '## Current packet: version history navigation\n\nOn 16 November 2026 Benjamin P Taylor authorised the version badge to open\n`/versions/`, with its v0.42 entry opening the existing `/42/` adventure. Scope:\nversion-history helper, adventure builder and generated header/history, sitemap,\nand the existing browser navigation check. Preserve release identities, source\nevidence, game state, and the fixed Open updates control. Acceptance: make\nvalidate, desktop/mobile badge → history → adventure navigation, keyboard and\nmodified-click links, and live deployment verification. The original adventure\nis already verified live in `documentation/adventure-42-status.json`; this is a\nnavigation follow-up. Preserve all other intake and source obligations below.', '# Next work')
replace_block(R / 'README.md', 'Reader release **0.42, 15 November 2026**: [An adventure in the Tangle](https://transduction.systems/42/). An original CP/M-inspired text adventure connected to the complete public atlas. Graph research release remains 0.41. See the Publish workflow and deployment.json for actual publication identity.', '# The Necessary Tangle')
changelog = R / 'CHANGELOG.md'
content = changelog.read_text(encoding='utf-8')
entry = '\n\n## 0.42 — 15 November 2026\n\nAn original branching text adventure, inspired by the CP/M Hitchhiker’s game,\nwith a complete-public-atlas library, source-labelled connections, finite\ninteractive apparatus, browser-local save/restore, keyboard access, and mobile\nlayout. Graph research release remains 0.41; no canonical claims are changed.\n'
if '## 0.42 — 15 November 2026' not in content:
    changelog.write_text(content.replace('# Changelog', '# Changelog' + entry, 1), encoding='utf-8')
assert (R / 'data/public-data.json').read_bytes() == raw, 'Adventure must not mutate the graph'
from version_history import build as build_version_history
build_version_history(R, reader_release)
print(f'Adventure 0.42 built: {len(worlds["rooms"])} places, {len(nodes)} public entries, {len(edges)} recorded connections; graph {data["meta"]["release"]} unchanged.')
