#!/usr/bin/env python3
"""Maintain both editions of the public young people's guide."""
from pathlib import Path
from html import escape as h
from urllib.request import Request, urlopen
import hashlib
import json
import re
import time
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
TANGLE = (ROOT / 'sources/making-things-change/guide.json').exists()
DATA_PATH = ROOT / ('sources/making-things-change/guide.json' if TANGLE else 'content/making-things-change.json')
DATA = json.loads(DATA_PATH.read_text())
PUBLIC = ROOT / 'docs' if TANGLE else ROOT
ROUTE = DATA['route']
FOLDER = PUBLIC / ROUTE.strip('/')
MARKER = 'making-things-change-guide'

def marked(text, content, insertion):
    start, end = '<!-- ' + MARKER + ' -->', '<!-- /' + MARKER + ' -->'
    block = start + content + end
    if start in text:
        return re.sub(re.escape(start) + '.*?' + re.escape(end), lambda _: block, text, flags=re.S)
    assert insertion in text, insertion
    return text.replace(insertion, block + insertion, 1)

def fetch_pdf(version):
    target = FOLDER / 'files' / version['filename']
    target.parent.mkdir(parents=True, exist_ok=True)
    def valid(data):
        return data.startswith(b'%PDF-') and len(data) == version['size_bytes'] and hashlib.sha256(data).hexdigest() == version['sha256']
    if target.exists() and valid(target.read_bytes()):
        return
    for attempt in range(3):
        try:
            request = Request(version['source_url'], headers={'User-Agent':'Making-things-change-public-editions/1.0'})
            with urlopen(request, timeout=40) as response:
                data = response.read()
            if not valid(data):
                raise ValueError('PDF identity does not match the authorised edition: ' + version['filename'])
            target.write_bytes(data)
            return
        except OSError:
            if attempt == 2:
                raise
            time.sleep(attempt + 1)

assert len(DATA['versions']) == 2 and sum(v['current'] for v in DATA['versions']) == 1
for version in DATA['versions']:
    assert Path(version['filename']).name == version['filename']
    fetch_pdf(version)
    for legacy_name in version.get('legacy_filenames', []):
        assert Path(legacy_name).name == legacy_name
        assert legacy_name not in [v['filename'] for v in DATA['versions']]
        (FOLDER / 'files' / legacy_name).write_bytes((FOLDER / 'files' / version['filename']).read_bytes())

body = '<p class="lead">' + h(DATA['summary']) + '</p><p>' + h(DATA['introduction']) + '</p>'
body += '<section><h2>Choose an edition</h2><p>Start with the revised draft. The first draft is kept here so you can compare them.</p><div class="guide-editions">'
for version in DATA['versions']:
    name = version['filename']
    body += '<article id="' + version['id'] + '"><h3>' + h(version['label']) + '</h3><p class="meta">' + h(version['version'] + ' · ' + version['date_label']) + ' · 32 pages · PDF</p><p>' + h(version['description']) + '</p>'
    body += '<p><a href="files/' + h(name, quote=True) + '" download="' + h(name, quote=True) + '">' + h(name) + '</a></p></article>'
body += '</div></section><section><h2>What changed in the second draft?</h2><p>' + h(DATA['revision_note']) + '</p></section>'
body += '<section><h2>Use it on a situation you care about</h2><p>Read in any order. Try a question with someone whose view differs from yours. The examples are fictional; the guide offers ways to investigate and act, rather than evidence that a particular intervention will work.</p><p>The worksheet is on page 28 of the revised draft; sources and further learning are on pages 30–31.</p><p><a href="' + h(DATA['discussion_url']) + '">Read the original article</a> · <a href="' + h(DATA['linkedin_url']) + '">Join the LinkedIn discussion</a></p></section>'
body += '<p class="meta">Benjamin P Taylor · Both editions are working drafts. Published here with the author’s permission.</p>'
style = '<style>.guide-editions{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1.5rem}.guide-editions article{min-width:0;padding:1.25rem;border:1px solid #b9aaa0;border-radius:.4rem}.guide-editions a{overflow-wrap:anywhere}.guide-editions h3{margin-top:0}@media(max-width:650px){.guide-editions{grid-template-columns:1fr}}</style>'
title = DATA['title'] + ': a guide to systems change for young people'
if TANGLE:
    from build_readable_atlas import page
    release = json.loads((ROOT / 'data/public-data.json').read_text())['meta']['release']
    output = page(title, DATA['summary'], ROUTE, body, release).replace('</head>', style + '</head>').replace('Readable atlas · Release ' + release, 'Source guide · Two working drafts')
else:
    template = (ROOT / 'library/preprints-and-working-papers/index.html').read_text()
    header = re.search(r'<header>.*?</header>', template, re.S).group()
    footer = re.search(r'<footer>.*?</footer>', template, re.S).group()
    output = '<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>' + h(title) + ' | Benjamin P Taylor</title><meta name="description" content="' + h(DATA['summary'],quote=True) + '"><link rel="canonical" href="https://antlerboy.com' + ROUTE + '"><link rel="stylesheet" href="/library/style.css">' + style + '</head><body>' + header + '<main><section class="hero"><div class="wrap"><p class="eyebrow">Free guide · Two working drafts</p><h1>Making things change</h1><p class="lead">' + h(DATA['subtitle']) + '</p></div></section><section class="section"><div class="wrap" style="max-width:960px">' + body + '</div></section></main>' + footer + '</body></html>\n'
FOLDER.mkdir(parents=True,exist_ok=True)
(FOLDER / 'index.html').write_text(output)

if TANGLE:
    path = PUBLIC / 'library/catalogue.json'
    catalogue = json.loads(path.read_text())
    versions = [{'version':v['version'],'date':v['date'],'url':ROUTE+'files/'+v['filename'],'sha256':v['sha256']} for v in DATA['versions']]
    record = {'id':'making_things_change_taylor_2026','title':title,'url':'https://antlerboy.com'+ROUTE,'reading_url':ROUTE,'authors':['Benjamin P Taylor'],'collection':'Practical guides','format':'Illustrated guide · two working drafts','year':'2026','summary':DATA['summary']+' '+DATA['introduction'],'review':'Authorised public working drafts. Version dates and byte identities checked 11 November 2026; no independent teaching evaluation is claimed.','locator':'v0.02: framework p. 4, systems leadership p. 10, approaches p. 13, worksheet p. 28, sources pp. 30–31.','connections':[],'atlas_id':'','versions':versions}
    matches = [r for r in catalogue['records'] if 29454 in r.get('syscoi_post_ids', []) or r['id'] == record['id']]
    assert len(matches) <= 1, 'Resolve duplicate guide identity before publishing'
    if matches:
        old = matches[0]
        record = {**old, **record, 'id':old['id'], 'url':old['url'], 'connections':old.get('connections', []), 'atlas_id':old.get('atlas_id', '')}
    catalogue['records'] = [r for r in catalogue['records'] if r['id'] != record['id']] + [record]
    catalogue['counts']['source_register_records'] = len(catalogue['records'])
    path.write_text(json.dumps(catalogue,ensure_ascii=False,separators=(',',':'))+'\n')
    note = '\n## Guide editions: Making things change\n\nBenjamin P Taylor authorised both 32-page working drafts on 11 November 2026. The guide at /library/making-things-change/ offers v0.02 first, retains the first draft with resource links corrected on 11 November 2026, and reuses SysCoI resource identity resource_syscoi_post_29454. No graph or release change. Source packet: sources/making-things-change/PACKET.md. The Publish workflow and deployment.json identify validation and publication.\n'
    for relative in ['documentation/NEXT_WORK.md', 'documentation/TANGLE_STATE.md']:
        path = ROOT / relative
        text = path.read_text()
        start, end = '<!-- guide-editions -->', '<!-- /guide-editions -->'
        content = start + note + end
        if start in text:
            text = re.sub(re.escape(start) + '.*?' + re.escape(end), lambda _: content, text, flags=re.S)
        else:
            pos = text.find('\n') + 1
            text = text[:pos] + content + text[pos:]
        path.write_text(text)
    card = '<section class="resource-pathways" id="making-things-change"><h2><a href="'+ROUTE+'">Making things change</a></h2><p>A free systems change guide for young people. Read the revised draft or compare both 32-page editions.</p></section>'
    for relative in ['library/index.html','systems-thinking/index.html','index.html']:
        path = PUBLIC / relative
        text = path.read_text()
        insertion = '<section id="systemsPracticeCallout"' if relative == 'index.html' else '</main>'
        if insertion not in text:
            insertion = '</body>'
        path.write_text(marked(text,card,insertion))
else:
    path = ROOT / 'library/manifest.json'
    manifest = json.loads(path.read_text())
    manifest['pages'] = [p for p in manifest['pages'] if p['slug'] != 'making-things-change'] + [{'slug':'making-things-change','title':title,'type':'guide','description':DATA['summary'],'tags':['systems','change','practice','writing']}]
    manifest['resources'] = [r for r in manifest['resources'] if r.get('url') != ROUTE]
    manifest['resources'].append({'title':title,'date':'2026-11-10','year':2026,'format':'Illustrated guide · two working drafts','url':ROUTE,'description':DATA['summary'],'tags':['systems','change','practice','writing'],'pages':['articles-and-essays','preprints-and-working-papers']})
    manifest['updated'] = max(manifest.get('updated',''),DATA['checked_on'])
    path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    card = '<section class="section"><div class="wrap"><h2><a href="'+ROUTE+'">Making things change</a></h2><p>'+h(DATA['summary'])+'</p><p><a href="'+ROUTE+'">Read the revised draft and compare both editions →</a></p></div></section>'
    for relative in ['library/index.html','library/articles-and-essays/index.html','library/preprints-and-working-papers/index.html']:
        path = ROOT / relative
        path.write_text(marked(path.read_text(),card,'</main>'))

sitemap = PUBLIC / 'sitemap.xml'
namespace='http://www.sitemaps.org/schemas/sitemap/0.9'
ET.register_namespace('',namespace)
tree=ET.parse(sitemap);root=tree.getroot()
location=('https://transduction.systems' if TANGLE else 'https://antlerboy.com')+ROUTE
row=next((r for r in root if r.findtext('{'+namespace+'}loc') == location),None)
if row is None:
    row=ET.Element('{'+namespace+'}url')
    ET.SubElement(row,'{'+namespace+'}loc').text=location
    generated=('https://transduction.systems/entries/', 'https://transduction.systems/journeys/', 'https://transduction.systems/stewardship/')
    position=next((i for i,child in enumerate(root) if (child.findtext('{'+namespace+'}loc') or '').startswith(generated)),len(root))
    root.insert(position,row)
lastmod=row.find('{'+namespace+'}lastmod')
if lastmod is None:
    lastmod=ET.SubElement(row,'{'+namespace+'}lastmod')
lastmod.text=DATA['checked_on']
ET.indent(tree, space='  ')
tree.write(sitemap,encoding='utf-8',xml_declaration=True)
print('Published two verified guide editions at '+location)

