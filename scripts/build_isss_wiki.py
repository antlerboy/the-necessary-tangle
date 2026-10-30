"""Build a source-scoped ISSS wiki guide and complete, dated page inventory."""
from pathlib import Path
from html import escape as E
import json
import re

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
SOURCE = ROOT / 'sources/isss-wiki'
packet = json.loads((SOURCE / 'inventory.json').read_text())
guide = json.loads((SOURCE / 'routes.json').read_text())
records = packet['records']
by_id = {row['page_id']: row for row in records}
assert len(records) == len(by_id) == 704
assert sum(row['kind'] == 'Redirect' for row in records) == 202
assert {i for route in guide['routes'] for i in route['sources']} == set(packet['full_reading_page_ids'])
assert all(row['url'].startswith('https://wiki.isss.org/') for row in records)
assert all(row['revision_id'] and row['source_text_sha256'] for row in records)


def link(url, title):
    return '<a href="' + E(url, quote=True) + '">' + E(title) + '</a>'


body = '''<p class="eyebrow">Companion reading guide · Edition 1.0 · 30 October 2026</p>
<h1>Reading the ISSS wiki</h1>
<p class="lead">Routes through systems theories, intervention, dialogue and cybernetic practice, with the source and its limits beside each account.</p>
<p>The International Society for the Systems Sciences’ member-maintained wiki brings together books, recordings, people, groups and historical programmes. It is a developing collection: a substantial description, a title-only recording and an unfinished template offer different kinds of evidence.</p>
<p>This guide draws on full reading of <strong>19 wiki pages</strong>. The dated index covers <strong>all 704 pages in the main article namespace</strong>: 502 pages that are not redirects and 202 redirects. It includes 194 unfinished profile templates. The wiki’s own article counter is 248; that is a different measure from the number of pages in this inventory.</p>
<p>All main-namespace revision texts were retrieved for the inventory. That does not mean that every page has received substantive reading, or that the books, papers, slides and recordings it lists have been read or watched. Each index record states its reading status.</p>
<p>Start with a question below, or <a href="#wiki-index">search the complete page index</a>. Continue with the existing <a href="/learning/isss/">ISSS student bibliography and learning resources</a> for a separate, 57-entry reading route.</p>
<nav class="questions" aria-label="Reading questions">'''
body += ''.join(link('#' + route['id'], route['title']) for route in guide['routes']) + '</nav>'
for route in guide['routes']:
    body += '<section id="' + E(route['id']) + '"><h2>' + E(route['title']) + '</h2><p>' + E(route['summary']) + '</p><h3>A question to take into the source</h3><p>' + E(route['question']) + '</p><p class="limits"><strong>Reading limits:</strong> ' + E(route['limits']) + '</p><details><summary>Sources and revision locators</summary><ul>'
    for ident in route['sources']:
        row = by_id[ident]
        body += '<li>' + link(row['url'], row['title']) + ' · ' + link(row['revision_url'], 'Revision ' + str(row['revision_id'])) + ' · ' + link(row['history_url'], 'Contributors and history') + '</li>'
    body += '</ul></details>'
    if route.get('compare'):
        body += '<p class="meta">Editorial comparison routes: ' + ' · '.join(link(x['url'], x['label']) for x in route['compare']) + '. These links do not create new evidence-graph claims.</p>'
    body += '</section>'
body += '<section id="source-gaps"><h2>Read around the gaps</h2><p>Keep incomplete and inconsistent source material visible. A wiki description is a starting point for inquiry, rather than independent verification of the work or its present availability.</p><ul>'
for gap in guide['source_gaps']:
    row = by_id[gap['page_id']]
    body += '<li>' + link(row['revision_url'], row['title']) + ': ' + E(gap['finding']) + '</li>'
body += '</ul><p>The inventory also retains a self-redirect, an unmatched mini-symposium redirect and a redirect outside the inventoried page set. They are not counted as additional works or exported to the main source search.</p></section>'
body += '''<section id="wiki-index"><h2>Search the dated wiki index</h2>
<p>Search titles, source-listed credits, categories and wiki descriptions. Redirects and unfinished profiles are hidden initially; choose “All handling states” to include them. Dates and credits are retained as source statements, with discrepancies preserved.</p>
<form id="wiki-search" role="search"><label>Search the wiki index<input id="wiki-query" type="search" autocomplete="off" placeholder="For example: dialogue, Midgley, cybernetics"></label><label>Page kind<select id="wiki-kind"><option value="">All kinds</option></select></label><label>Handling state<select id="wiki-state"><option value="usable">Hide redirects and unfinished profiles</option><option value="all">All handling states</option><option value="read">Wiki pages read in full</option><option value="unfinished">Unfinished profiles</option><option value="redirect">Redirects</option></select></label><button type="reset">Reset</button></form>
<p id="wiki-count" role="status" aria-live="polite"></p><p id="wiki-error" role="alert" hidden>The index could not be loaded. <a href="inventory.json">Download its data</a> or <a href="https://wiki.isss.org/">open the wiki</a>.</p><div id="wiki-results"></div><nav class="pagination" aria-label="Wiki index pages"><button id="wiki-previous" type="button">Previous</button><span id="wiki-page-number"></span><button id="wiki-next" type="button">Next</button></nav>
<noscript><p>The index search needs JavaScript. <a href="inventory.json">Download the complete dated inventory</a> or follow the source links in the reading guide above.</p></noscript></section>
<section id="provenance"><h2>Sources, credits and scope</h2>
<p>Wiki-derived metadata and descriptions are adapted or excerpted from <a href="https://wiki.isss.org/">ISSS Wiki contributors</a> under <a href="https://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0</a>. Wiki markup has been removed and descriptions shortened. Every record links to its exact revision and contributor history. Book authors and presenters are credited as the source lists them; they are not thereby the authors of the wiki description.</p>
<p>The reading questions and comparisons are editorial additions, curated by Benjamin P Taylor with AI assistance. They are not claims of agreement, influence, institutional endorsement or human acceptance of new graph relationships. Books, papers, slides, images and recordings retain their own rights; they are not reproduced here.</p>
<p>This inventory exhausts the public API’s main-namespace pagination on 30 October 2026. File, category, template, user and talk namespaces are outside its scope. External source-listed links have not all been checked for availability. This is a dated snapshot, not a mirror that follows later changes automatically.</p>
<p><a href="inventory.json">Download the complete inventory and provenance</a> · <a href="routes.json">Download the reading and gap ledger</a> · <a href="/library/?collection=ISSS%20Wiki">Search the selected wiki descriptions in the source library</a></p></section>'''
css = ''':root{color-scheme:light;--red:#862719;--paper:#f6f0e5}*{box-sizing:border-box}body{margin:0;background:var(--paper);color:#29221b;font:19px/1.65 Georgia,serif}body>a:first-child{display:block;padding:8px 24px}nav.site,main,footer{max-width:1000px;margin:auto;padding:24px}nav.site{display:flex;gap:24px;flex-wrap:wrap;font:16px/1.5 system-ui}a{color:var(--red);overflow-wrap:anywhere}h1{font-size:clamp(2.2rem,6vw,3.7rem);line-height:1.1}h2{font-size:1.65rem;line-height:1.3}h3{font-size:1.1rem}section{padding:28px 0;border-top:1px solid #cdbda6}.meta,.eyebrow,footer,summary,.limits{font:15px/1.6 system-ui}.lead{font-size:1.3rem}.questions{display:grid;gap:8px;padding:20px 0}li{margin:.75em 0}a:focus-visible,button:focus-visible,input:focus-visible,select:focus-visible,summary:focus-visible{outline:3px solid #b56600;outline-offset:3px}form{display:grid;gap:16px}label{display:grid;gap:4px;font:16px/1.5 system-ui}input,select,button{font:inherit;max-width:100%;min-width:0;padding:10px;border:1px solid #b9a88e;background:#fffdf8;color:#29221b}button{cursor:pointer}button:disabled{opacity:.55;cursor:default}.wiki-card{padding:18px 0;border-top:1px solid #cdbda6}.wiki-card h3{font-size:1.25rem;margin:.2em 0}.wiki-card blockquote{margin:12px 0;padding-left:16px;border-left:3px solid #cdbda6;font-size:1rem}.pagination{display:flex;align-items:center;gap:16px;flex-wrap:wrap}.source-links{font:15px/1.6 system-ui}#openUpdates{position:fixed;right:0;bottom:0;width:44px;height:44px}#openUpdates:after{content:"";position:absolute;right:8px;bottom:8px;width:5px;height:5px;border-radius:50%;background:var(--red)}'''
page = '<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Reading the ISSS wiki | The Necessary Tangle</title><meta name="description" content="Seven question-led reading routes and a complete dated ISSS wiki page index, with attribution, revision locators and reading limits."><link rel="canonical" href="https://transduction.systems/reading/isss-wiki/"><style>' + css + '</style></head><body><a href="#main-content">Skip to reading</a><nav class="site" aria-label="Main">' + link('/', 'Atlas') + link('/library/', 'Sources') + link('/learning/', 'Learning') + '</nav><main id="main-content">' + body + '</main><footer>Curated by Benjamin P Taylor. Wiki excerpts: ISSS Wiki contributors, CC BY 4.0. Underlying works retain their authorship and terms.</footer><a id="openUpdates" href="https://github.com/antlerboy/the-necessary-tangle/issues/2" aria-label="Open updates"></a><script src="index.js"></script></body></html>\n'
folder = DOCS / 'reading/isss-wiki'
folder.mkdir(parents=True, exist_ok=True)
(folder / 'index.html').write_text(page)
(folder / 'inventory.json').write_text(json.dumps(packet, ensure_ascii=False, separators=(',', ':')) + '\n')
(folder / 'routes.json').write_text(json.dumps(guide, ensure_ascii=False, indent=2) + '\n')

# Keep source descriptions separate from the works they describe. Redirects,
# unfinished biographies, navigation and conference pages are not extra works.
allowed = {'Book', 'Software', 'Journal article', 'Theory account', 'Mini-symposium recording', 'Special Integration Group', 'Programme archive'}
selected = [row for row in records if row['kind'] in allowed and not row['placeholder']]
catalogue_path = DOCS / 'library/catalogue.json'
catalogue = json.loads(catalogue_path.read_text())
catalogue['records'] = [row for row in catalogue['records'] if not row['id'].startswith('isss_wiki_')]
seen = set()
exported = []
for row in selected:
    # Repeated mini-symposium pages with the same primary recording remain in
    # the inventory, but have one record in the main search.
    media = next((url for url in row['source_listed_urls'] if re.fullmatch(r'https://vimeo.com/\d+', url)), None)
    key = ('video', media) if row['kind'] == 'Mini-symposium recording' and media else ('page', row['page_id'])
    if key in seen:
        continue
    seen.add(key)
    summary = 'Wiki description of ' + row['title'] + '.'
    if row['work_credit_as_listed']:
        summary += ' Work credit as listed: ' + row['work_credit_as_listed'] + '.'
    if row['wiki_excerpt']:
        summary += ' Wiki excerpt: “' + row['wiki_excerpt'] + '”'
    exported.append({'id':row['id'], 'title':row['title'], 'url':row['url'], 'authors':['ISSS Wiki contributors'], 'summary':summary, 'collection':'ISSS Wiki', 'format':row['kind'] + ' — wiki description', 'year':row['work_date_as_listed'], 'review':row['review'] + '; CC BY 4.0; underlying-work rights separate', 'locator':row['revision_url'], 'connections':[], 'atlas_id':''})
catalogue['records'].extend(exported)
assert len(catalogue['records']) == len({row['id'] for row in catalogue['records']})
catalogue['counts']['source_register_records'] = len(catalogue['records'])
catalogue['counts']['isss_wiki_descriptions'] = len(exported)
catalogue_path.write_text(json.dumps(catalogue, ensure_ascii=False, separators=(',', ':')) + '\n')
marker = 'isss-wiki-20261030'
block = '<section class="resource-pathways" id="isssWikiGuide"><h2>' + link('/reading/isss-wiki/', 'Reading the ISSS wiki') + '</h2><p>Seven questions through systems theories, intervention, dialogue and cybernetic practice, with a complete dated wiki page index and explicit reading limits.</p></section>'
for relative in ['index.html', 'library/index.html', 'learning/index.html', 'learning/isss/index.html']:
    path = DOCS / relative
    text = path.read_text()
    start = '<!-- ' + marker + ' -->'
    end = '<!-- /' + marker + ' -->'
    replacement = start + block + end
    if start in text:
        text = re.sub(re.escape(start) + '.*?' + re.escape(end), lambda _: replacement, text, flags=re.S)
    else:
        assert '</main>' in text, relative
        text = text.replace('</main>', replacement + '</main>', 1)
    path.write_text(text)
path = DOCS / 'sitemap.xml'
text = path.read_text()
url = 'https://transduction.systems/reading/isss-wiki/'
if '<loc>' + url + '</loc>' not in text:
    text = text.replace('</urlset>', '<url><loc>' + url + '</loc><lastmod>2026-10-30</lastmod></url></urlset>')
path.write_text(text)
print('ISSS wiki: 704 pages accounted for; 19 wiki pages read; seven reading routes; ' + str(len(exported)) + ' searchable wiki descriptions. Graph unchanged.')
