"""Publish the maintained systemsmap interface inside The Necessary Tangle."""
from pathlib import Path
import json,shutil,re,html
root=Path(__file__).resolve().parents[1]
source=next((p for p in [root/'_systemsmap/dist',root.parent/'systemsmap/dist'] if (p/'index.html').exists()),None)
if source is None:raise SystemExit('Clone antlerboy/systemsmap into _systemsmap before building the events integration.')
target=root/'docs/events';shutil.copytree(source,target,dirs_exist_ok=True)
canonical='https://transduction.systems/events/'
s=(target/'index.html').read_text().replace('<html lang="en">','<html lang="en-GB">')
s=s.replace('</head>','<link rel="canonical" href="'+canonical+'"><meta property="og:title" content="Systems events map | The Necessary Tangle"><meta property="og:description" content="Find systems thinking, cybernetics, and complexity events worldwide, and subscribe to maintained calendars."><meta property="og:url" content="'+canonical+'"><meta property="og:type" content="website"><meta name="twitter:card" content="summary"><link rel="stylesheet" href="tangle-context.css"></head>')
s=s.replace('<header>','<div class="tangle-context"><a href="/">The Necessary Tangle</a> / <span>Systems events map</span></div><header>',1)
links='''<section class="related-practice" aria-labelledby="related-title"><h2 id="related-title">Follow the connections</h2><div><article><h3><a href="/systems-thinking/">Find your way into systems thinking</a></h3><p>A plain-language introduction, then the ideas, people, methods, and evidence in The Necessary Tangle.</p></article><article><h3><a href="https://syscoi.com/">Systems Community of Inquiry</a></h3><p>Current writing, papers, events, and open conversation around systems, cybernetics, and complexity.</p></article><article><h3><a href="https://antlerboy.com/library/">Benjamin’s writing and resources</a></h3><p>Books, articles, talks, and practical materials. Explore <a href="https://antlerboy.com/toolshed/">the Tool Shed</a> for supported practice.</p></article><article><h3><a href="https://chosen-path.org/">Chosen Path</a></h3><p>Essays and developing arguments. Follow their connections through <a href="https://greebling.com/">Greebling</a>.</p></article></div></section>'''
s=s.replace('</main>',links+'</main>',1)
data={'@context':'https://schema.org','@type':'CollectionPage','name':'Systems events map','description':'Find systems thinking, cybernetics, and complexity events worldwide.','url':canonical,'isPartOf':{'@type':'WebSite','name':'The Necessary Tangle','url':'https://transduction.systems/'}}
s=s.replace('</head>','<script type="application/ld+json">'+json.dumps(data)+'</script></head>')
(target/'index.html').write_text(s)
(target/'tangle-context.css').write_text('''.tangle-context{background:#f2eadc;padding:16px max(18px,calc((100vw - 1452px)/2));font-size:16px;color:#241f1a}.tangle-context a{font-weight:bold;color:#862719}.related-practice{padding:35px 0 50px;border-top:1px solid #ccc}.related-practice>div{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:25px}.related-practice h3{font-size:20px;line-height:1.3}.related-practice p{font-size:16px;line-height:1.6}.related-practice a{color:#862719}@media(max-width:650px){.related-practice>div{grid-template-columns:1fr}}''')
# Navigation links, not new claims in the evidence graph.
p=root/'docs/index.html';s=p.read_text()
if 'href="/events/"' not in s:
 s=s.replace('<nav class="main-nav" aria-label="Main navigation">','<nav class="main-nav" aria-label="Main navigation"><a href="/events/" class="static-nav-link">Events</a>',1)
 s=s.replace('The living field around the atlas','<a href="/events/">Find systems events worldwide</a> · The living field around the atlas',1)
p.write_text(s)
p=root/'docs/systems-thinking/index.html';s=p.read_text()
if 'href="/events/"' not in s:s=s.replace('</main>','<section><h2>Meet the living field</h2><p><a href="/events/">Find systems events worldwide</a> and follow <a href="https://syscoi.com/">the Systems Community of Inquiry</a>.</p></section></main>',1)
p.write_text(s)
p=root/'docs/sitemap.xml';s=p.read_text()
if canonical not in s:s=s.replace('</urlset>','<url><loc>'+canonical+'</loc></url></urlset>')
p.write_text(s)
assert all(x in (target/'index.html').read_text() for x in ['vendor/leaflet.js','id="submission"','id="language"','name="languageRequirement"','Quick submission — just a link','https://syscoi.com/','https://antlerboy.com/library/',canonical])
assert 'https://raw.githubusercontent.com/antlerboy/systemsmap/main/dist/' in (target/'app.js').read_text()
print('Integrated systems events at /events/; collector, stable feeds, and submission queue remain in systemsmap.')
