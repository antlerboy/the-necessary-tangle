"""Build the reader-first About entrance and attributed public reading routes."""
from pathlib import Path
import html, json, re
R = Path(__file__).resolve().parents[1]
S = R / 'sources/update-2026-10-13'
D = R / 'docs'
P = json.loads((S/'review.json').read_text())
E = lambda s: html.escape(s, quote=True)
def link(url, title):
    return '<a href="'+E(url)+'">'+E(title)+'</a>'

def page(route, title, body):
    dest = D / route.strip('/')
    dest.mkdir(parents=True, exist_ok=True)
    css = '''*{box-sizing:border-box}body{margin:0;background:#faf8f2;color:#302b26;font:18px/1.65 Georgia,serif}main,nav,footer{max-width:60rem;margin:auto;padding:1.4rem}nav{display:flex;gap:1rem;flex-wrap:wrap;font:1rem/1.5 system-ui}a{color:#973d32;overflow-wrap:anywhere}a:focus-visible,summary:focus-visible{outline:3px solid #973d32;outline-offset:3px}h1{font-size:clamp(2rem,6vw,3.5rem);line-height:1.15}h2{line-height:1.3}section,article{border-bottom:1px solid #d8d0c5;padding:1rem 0}.meta,.status{font:1rem/1.5 system-ui}.status{color:#63574a}.note{background:#f0eadd;padding:1rem}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,24rem),1fr));gap:1.4rem}.grid article{padding:1rem;border:1px solid #d8d0c5;border-top:3px solid #973d32}summary{cursor:pointer;font-weight:bold;padding:1rem 0}#openUpdates{position:fixed;bottom:0;right:0;width:44px;height:44px}#openUpdates:after{content:"";position:absolute;right:8px;bottom:8px;width:5px;height:5px;background:#862719;border-radius:50%;box-shadow:0 0 0 1px white}@media(max-width:600px){main,nav,footer{padding:1rem}ul,ol{padding-left:1.3rem}}'''
    (dest/'index.html').write_text('<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+E(title)+' | The Necessary Tangle</title><link rel="canonical" href="https://transduction.systems'+route+'"><style>'+css+'</style></head><body><nav aria-label="Main"><a href="/">Atlas</a><a href="/#view=about">About</a><a href="/about/how-to-use/">How to use it</a><a href="/prior-maps/">Earlier maps</a><a href="/learning/">Learning</a></nav><main><p class="meta">Release 0.32 · 13 October 2026</p><h1>'+E(title)+'</h1>'+body+'</main><footer><p>Curated by <a href="https://www.antlerboy.com/">Benjamin P Taylor</a>. Original reader guidance is editorial; linked works retain their own authorship and terms.</p><p><a href="/#view=contribute">Suggest a correction</a> · <a href="/updates/2026-10-13/">Update and remaining work</a></p></footer><a id="openUpdates" href="https://github.com/antlerboy/the-necessary-tangle/issues/2" aria-label="Open updates"></a></body></html>\n')

about = (S/'about.html').read_text()
p = D/'index.html'; s = p.read_text()
s = re.sub(r'    <section id="view-about".*?(?=    <section id="view-ai-observations")', lambda _: about, s, flags=re.S)
s = s.replace('<span id="releaseBadge">Release 0.31</span>', '<span id="releaseBadge">Release 0.32</span>')
s = s.replace('What becomes visible when the public graph is analysed as data, interface and editorial argument. Counts are reproducible. Interpretations are proposals for challenge, not autonomous facts.', "These observations examine the atlas itself: what is well connected, what is missing, and how the interface shapes what readers see. Each separates a measurement, an interpretation, a practical implication and a way to test it.")
s = s.replace('<p class="eyebrow">Second-order observation</p>', '<p class="eyebrow">Looking at how the atlas works</p>')
s = s.replace('href="/updates/2026-10-08/"', 'href="/updates/2026-10-13/"', 1)
p.write_text(s)

body = '''<p>You can use The Necessary Tangle to look up an idea, discover its context, or compare accounts of it. Start with something you want to understand; the complete map can wait.</p>
<section><h2>A first visit: follow feedback</h2><ol><li>Open <a href="/#view=browse">Explore</a> and search for 'feedback'. Choose the entry matching your question.</li><li>Read the short explanation and its status. Follow a source if you need the author's fuller argument.</li><li>Open a connection. Read what it says before assuming it means influence or agreement.</li><li>Choose the map to see neighbouring ideas. Start with one or two steps from the entry; use filters to show ideas, people, practice or disagreement.</li><li>Follow one useful link, or return to the entry. A shared map URL retains the selected focus and filters.</li></ol></section>
<section><h2>Choose between the views</h2><p><strong>Explore</strong> is the searchable list. <strong>Guided journeys</strong> explain a sequence of ideas. <strong>Map</strong> lets you inspect recorded connections; on a small screen, card view provides a readable alternative. <strong>Ask</strong> helps locate relevant entries and prepares source context for inspection; it doesn’t send your question to an AI service automatically.</p></section>
<section><h2>Read the map without overreading it</h2><p>Select an entry to highlight its connections. Select a line to inspect its exact relationship and evidence. Zoom or switch to cards when labels become crowded. Use 'Everything' for the complete recorded graph; the other layers show selected kinds of connection.</p><p>Position, size and density are features of this representation. They don't establish intellectual importance, historical priority or agreement. The number of links reflects what's recorded here.</p></section>
<section><h2>Practice and further reading</h2><p>The <a href="/systems-thinking/practice/">practice collection</a> provides exercises and worked cases with stated limits. <a href="/learning/">Learning and training</a> links to courses and provider resources. <a href="/reading/design-horizon/">Design Horizon selections</a> offer another way into design and systems change.</p></section>
<section><h2>When something looks wrong</h2><p>Use <a href="/#view=contribute">Contribute</a>. Name the entry or connection, explain the change and give a source or passage. The form prepares an email or GitHub issue; you decide whether to send it. A submitted item enters review, not automatic publication.</p></section>'''
page('/about/how-to-use/', 'How to use The Necessary Tangle', body)

body = '''<p>The atlas contains explanations, proposed connections and source records. Their labels tell you how each item has been handled. They don't replace reading the evidence.</p>
<section><h2>An entry's depth</h2><p><strong>Developed entry</strong> means a fuller account with distinctions, history, uses, limits and sources. <strong>Brief entry</strong> provides a shorter orientation. These labels describe the work done here, not the importance of the subject.</p></section>
<section><h2>A statement's status</h2><p><strong>Candidate or provisional</strong> means a proposed interpretation still needs checking. <strong>Accepted or corroborated</strong> means the current evidence supports the stated wording within its scope; it isn't a verdict on every broader claim. <strong>Disputed</strong> keeps a disagreement visible. <strong>Superseded</strong> records a statement replaced by a later account.</p><p>Automated validation checks structure and consistency. It doesn’t accept a historical claim on the curator's behalf.</p></section>
<section><h2>What a source can establish</h2><p>A title page can establish a book's author and title. A bibliography can establish that an author cited it. Neither alone proves that the book influenced a method or that the method works. Look for the precise page, section or passage attached to the statement.</p><p>'Public link' gives a route to the source, which may still have access restrictions. 'No public link' means an identifiable published work is cited without an open copy. A private email or internal document isn't made public by giving it that label.</p></section>
<section><h2>Original maps and atlas connections</h2><p>An earlier map may draw an influence line that the atlas hasn't independently checked. Its own wording and attribution stay with that source. Compare maps to notice different boundaries and possible connections; don't assume that importing a diagram verifies its history.</p><p><a href="/prior-maps/sources/">Referenced maps and histories</a> · <a href="/prior-maps/principles/">Principles for a revisable map</a></p></section>
<section><h2>How to challenge an account</h2><p>Point to the exact wording, offer evidence and explain whether it changes the meaning, scope or status. Competing interpretations can remain visible. You don't need to force agreement before making a useful correction.</p></section>'''
page('/about/evidence/', 'Sources, evidence and uncertainty', body)

intro = '<p>'+link(P['design_horizon']['url'],'Design Horizon')+' is Ruth Guerra’s free resource library, developed through Phenomena Co-Design. It connects systemic, transition, regenerative, values-based and other design approaches. Its '+link(P['design_horizon']['about_url'],'About page')+' says the copy and resource selection are human-curated and suggestions are reviewed by hand.</p><p>Benjamin P Taylor highlighted it in '+link(P['design_horizon']['discovery_url'],'a SysCoI post on 11 October 2026')+'. The eight selections below offer useful routes into systems practice. The short descriptions summarise the inspected source pages; the questions and atlas cross-links are editorial invitations, not claims of influence or evidence that a method works.</p><div class="grid">'
for item in P['design_horizon']['resources']:
    intro += '<article id="'+item['id']+'"><p class="meta">'+E(item['author'])+'</p><h2>'+link(item['url'],item['title'])+'</h2><p>'+E(item['summary'])+'</p><p><strong>Try this question:</strong> '+E(item['question'])+'</p><p>'+link('/#view=item&id='+item['atlas_id'],'Compare: '+item['atlas_label'])+'</p><p class="status">'+E(item['date'])+' · '+E(item['status'])+'</p><details><summary>Source reference</summary><p>'+E(item['locator'])+'. Route discovered through Design Horizon; destination inspected 13 October 2026.</p></details></article>'
intro += '</div><section><h2>Continue at the source</h2><p>Open Design Horizon for the wider collection and its current selection. This page doesn’t mirror its whole library or claim to have read every linked publication. Source authors retain their own wording, rights and responsibility.</p></section>'
page('/reading/design-horizon/', 'Design Horizon: routes into systems practice', intro)

body = '<p>Earlier maps help you see how people have organised the field: as a history, a family tree, a classification or a route into practice. Those forms answer different questions. This directory gives attribution, a reference route and the limits of what has been checked.</p><p>Use it alongside '+link('/prior-maps/','the interactive map collection')+' and '+link('/prior-maps/principles/','the atlas’s mapping principles')+'. A source map’s lines aren’t automatically accepted as atlas relationships.</p>'
for item in P['maps']:
    body += '<section id="'+item['id']+'"><p class="meta">'+E(item['author'])+' · '+E(item['date'])+'</p><h2>'+E(item['title'])+'</h2><p>'+E(item['summary'])+'</p><p>'+link(item['url'],'Open the public reference route')+' · '+link(item['atlas_url'],'Compare in The Necessary Tangle')+'</p><p class="status">'+E(item['status'])+'</p><details><summary>Reference and locator</summary><p>'+E(item['locator'])+'</p></details></section>'
body += '<section><h2>Related institutional reading</h2><p>'+link('https://revistia.com/ejser/article/view/525','Mobus, Sankaran and Smith: The International Society for the Systems Sciences: Contributions to the Future World')+' (2022), European Journal of Social Science Education and Research 9(4), 81–97. DOI: 10.26417/950aeu54p. This is a discussion of institutional purpose and renewal, rather than another genealogy map.</p></section><section><h2>Coverage still to check</h2><p>Some retrieved copies were duplicates or incomplete images. Some original destinations no longer work, and not every item in the requested collection could be enumerated. Restricted material has been kept outside this public directory. Individual map links, original editions and diagram relationships still need further verification before a complete comparison or graph import can be claimed.</p></section>'
page('/prior-maps/sources/', 'Referenced maps and histories', body)

page('/updates/2026-10-13/', 'A clearer entrance and new reading routes', '<p>This release rewrites About around what a visitor can do, why the atlas exists and how to read its evidence. Specialist detail remains available underneath.</p><ul><li>'+link('/#view=about','Rewritten About')+'; '+link('/about/how-to-use/','a practical guide')+'; '+link('/about/evidence/','sources and uncertainty')+'.</li><li>'+link('/prior-maps/sources/','Eleven attributed map and collection reference routes')+', with duplicates grouped and access limits recorded.</li><li>'+link('/reading/design-horizon/','Eight resources discovered through Design Horizon')+', linking to original sources and relevant atlas entries.</li></ul><p>The canonical graph and source-owner-reviewed Systemic Evolution comparator are unchanged. This release adds reader guidance and source routes; it doesn’t certify every map’s historical links or complete the reading of all linked works.</p><section><h2>Remaining work</h2><p>Complete collection enumeration; check unavailable original map destinations and ambiguous versions; read linked works at claim level before proposing new relationships. Confidential source material requires a public equivalent or a specific source-owner permission.</p></section>')

# Link new material from the existing public reader routes; rebuilds are idempotent.
for name, marker, title, url in [
    ('prior-maps/index.html','maps-directory-32','Referenced maps and histories','/prior-maps/sources/'),
    ('learning/index.html','design-horizon-32','Design Horizon: selected design and systems-change resources','/reading/design-horizon/'),
    ('reading-list.html','reading-32','Design Horizon and referenced maps','/reading/design-horizon/'),
    ('updates/index.html','update-32','A clearer entrance and new reading routes — 13 October 2026','/updates/2026-10-13/')]:
    path=D/name; text=path.read_text()
    text=re.sub('<!-- '+marker+' -->.*?<!-- /'+marker+' -->','',text,flags=re.S)
    text=text.replace('</main>','<!-- '+marker+' --><section><h2>'+link(url,title)+'</h2><p>Attribution, useful reading routes and explicit coverage limits.</p></section><!-- /'+marker+' --></main>',1)
    path.write_text(text)

d=json.loads((R/'data/public-data.json').read_text())
d['reader_update_32']=P
d['meta'].update(release='0.32',generated='2026-10-13',release_digest_url='https://transduction.systems/updates/2026-10-13/',iteration_focus='Reader-first explanations and referenced maps and design resources',release_note='Rewritten About; how-to and evidence guides; eleven map reference routes; eight selected Design Horizon sources. Canonical graph unchanged.')
from refresh_graph_snapshot import write
write(d)
for name in ['data/relationship-quality.json','docs/assets/relationship-quality.json']:
    path=R/name;q=json.loads(path.read_text());q.update(release='0.32',generated='2026-10-13');path.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
p=D/'sitemap.xml'; text=p.read_text()
for route in ['/about/how-to-use/','/about/evidence/','/reading/design-horizon/','/prior-maps/sources/','/updates/2026-10-13/']:
    url='https://transduction.systems'+route
    if url not in text:text=text.replace('</urlset>','<url><loc>'+url+'</loc><lastmod>2026-10-13</lastmod></url></urlset>')
p.write_text(text)
path=R/'README.md';text=path.read_text()
text=re.sub(r'<!-- current-31 -->.*?<!-- /current-31 -->', '<!-- current-31 -->\nCurrent release: **0.32, 13 October 2026**. [About](https://transduction.systems/#view=about), [how to use the atlas](https://transduction.systems/about/how-to-use/), [referenced maps](https://transduction.systems/prior-maps/sources/), and [Design Horizon reading routes](https://transduction.systems/reading/design-horizon/). [Read the update and remaining work](https://transduction.systems/updates/2026-10-13/).\n<!-- /current-31 -->',text,flags=re.S)
path.write_text(text)
path=R/'CITATION.cff';text=path.read_text();text=re.sub(r'^version:.*$', "version: '0.32'", text, flags=re.M);text=re.sub(r'^date-released:.*$', "date-released: '2026-10-13'", text, flags=re.M);path.write_text(text)
print('Applied release 0.32: About, two reader guides, eleven map routes and eight Design Horizon selections; canonical graph unchanged.')
