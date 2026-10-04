#!/usr/bin/env python3
"""Release 0.28: original claim-testing exercises, not canonical graph claims."""
from pathlib import Path
import hashlib, html, json, re

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
SRC = ROOT / 'sources/claim-lab-2026-10-04'
BASE = '/systems-thinking/claim-lab/'
MARK = 'claim-lab-20261004'
E = lambda s: html.escape(str(s), quote=True)
packet = json.loads((SRC / 'cases.json').read_text(encoding='utf-8'))
labs = {x['id']: x for f in sorted((ROOT / 'sources/practice-pack').glob('[0-9][0-9]-*.json')) for x in json.loads(f.read_text(encoding='utf-8'))}
resources = {}
for f in sorted((ROOT / 'sources/practice-pack').glob('resources*.json')):
    resources.update({x['id']: x for x in json.loads(f.read_text(encoding='utf-8'))})
for key, changes in json.loads((ROOT / 'sources/practice-pack/resource-corrections.json').read_text(encoding='utf-8')).items():
    resources[key].update(changes)
canonical = ROOT / 'data/public-data.json'
before = hashlib.sha256(canonical.read_bytes()).hexdigest()
css = '''body{margin:0;background:#faf8f2;color:#302b26;font:18px/1.65 Georgia,serif}main,nav,footer{max-width:62rem;margin:auto;padding:1.4rem}nav{display:flex;flex-wrap:wrap;gap:1rem;border-bottom:1px solid #d8d0c5;font:1rem/1.5 system-ui}a{color:#973d32;overflow-wrap:anywhere}a:focus-visible,summary:focus-visible{outline:3px solid #973d32;outline-offset:4px}h1{font-size:clamp(2.2rem,6vw,3.5rem);line-height:1.15}h2{line-height:1.3}article,section{margin:1.5rem 0;padding-bottom:1.2rem;border-bottom:1px solid #d8d0c5}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1.4rem}.grid article{margin:0;padding:1.2rem;background:#f1ece3}.meta{font:1rem/1.5 system-ui}.claim{font-size:1.3rem;border-left:3px solid #973d32;padding-left:1.2rem;margin:1.5rem 0}summary{cursor:pointer;padding:.65rem 0;font-weight:bold}details{border-top:1px solid #d8d0c5}li{margin:.5rem 0}.skip{position:absolute;left:-9999px}.skip:focus{left:1rem;background:white;padding:1rem;z-index:10}#openUpdates{position:fixed;bottom:0;right:0;width:44px;height:44px;z-index:1000}#openUpdates:after{content:"";position:absolute;bottom:7px;right:7px;width:6px;height:6px;border-radius:50%;background:white;box-shadow:0 0 0 1px #777}@media(max-width:650px){.grid{grid-template-columns:1fr}main,nav,footer{padding:1rem}}@media print{nav,.skip,#openUpdates{display:none}details>*{display:block}main{max-width:none}article{break-inside:avoid}}'''

def p(text): return '<p>' + E(text) + '</p>'
def page(route, title, body):
    dest = DOCS / route / 'index.html'
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text('<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+E(title)+' | The Necessary Tangle</title><meta name="description" content="Eight original cases for testing systems claims, with counterexamples, worked repairs, and source-labelled method routes."><link rel="canonical" href="https://transduction.systems/'+route+'/"><style>'+css+'</style></head><body><a class="skip" href="#main">Skip to content</a><nav aria-label="Main"><a href="/">Atlas</a><a href="/systems-thinking/">Systems thinking</a><a href="/systems-thinking/practice/">Method practice</a><a href="'+BASE+'">Test a claim</a><a href="/reading-list.html">Reading</a></nav><main id="main"><p class="meta">Release 0.28 · Original practice · 4 October 2026</p><h1>'+E(title)+'</h1>'+body+'</main><footer>'+p(packet['status'])+'<p>Prepared with AI assistance. Curator: Benjamin P Taylor. Fictional cases are not evidence about a named organisation. <a href="https://creativecommons.org/licenses/by-sa/4.0/">Original text: CC BY-SA 4.0</a>. Linked resources retain their terms.</p></footer><a id="openUpdates" href="https://github.com/antlerboy/the-necessary-tangle/issues/2" aria-label="Open updates" title="Tangle feedback"></a></body></html>', encoding='utf-8')

byid = {x['id']: x for x in packet['cases']}
home = p('A plausible systems claim can survive a workshop and still fail a simple question. Work through a short fictional case, then test your answer against a counterexample. The point is to find the next useful observation or decision.')
home += '<p>Allow about 15 minutes per case. Write your answer before opening the comparison. These are editorial learning routes, not new relationships in the evidence graph, an assessment, or a substitute for work with people in the situation.</p><section><h2>Choose the decision you face</h2>'
for journey in packet['journeys']:
    home += '<h3>'+E(journey['title'])+'</h3><ol>'+''.join('<li><a href="'+BASE+x+'/">'+E(byid[x]['title'])+'</a></li>' for x in journey['cases'])+'</ol>'
home += '</section><section><h2>Eight claims to test</h2><div class="grid">'
for c in packet['cases']:
    home += '<article><h3><a href="'+BASE+c['id']+'/">'+E(c['title'])+'</a></h3>'+p(c['claim'])+'<p class="meta">'+E(c['relation'])+'</p></article>'
    body = '<blockquote class="claim">'+E(c['claim'])+'</blockquote><section id="case"><h2>The case</h2>'+p(c['case'])+'</section><section id="attempt"><h2>Try it before reading on</h2>'+p(c['task'])+'<p>Use paper or your own notes. Keep the first answer as well as any revision.</p><details><summary>Compare your reasoning</summary>'+p(c['worked'])+'</details></section><section id="counterexample"><h2>When could the claim be defensible?</h2>'+p(c['counterexample'])+'</section><section id="changed"><h2>Change the conditions</h2>'+p(c['changed'])+'<details><summary>Compare the changed case</summary>'+p(c['changed_answer'])+'</details></section><section id="connections"><h2>Follow the specific connection</h2><p class="meta">Editorial route: '+E(c['relation'])+'</p>'
    for key in [c['method'], c['pair']]:
        lab = labs[key]
        body += '<h3><a href="/systems-thinking/practice/'+key+'/">'+E(lab['title'])+'</a></h3>'+p(lab['scope'])
    body += '<p class="meta">Maintained exercise locators: '+E(c['locator'])+'.</p></section><section id="sources"><h2>Source routes and reading limits</h2><p>The methodological route below uses the existing practice pack\'s checked resource descriptions. This release does not claim fresh reading of the external works.</p>'
    for key in dict.fromkeys(labs[c['method']]['resources'] + labs[c['pair']]['resources']):
        r = resources[key]
        body += '<details><summary>'+E(r['title'])+'</summary><p><a href="'+E(r['url'])+'">Open the source route</a></p>'+p(r['use'])+p('Existing check: '+r['check'])+'</details>'
    body += '</section><section><h2>Take one revision away</h2><p>Write the claim you can now support, the assumption you changed, and the observation or decision still needed. Do not turn the worked comparison into a compulsory answer where the question admits alternatives.</p></section><p><a href="'+BASE+'">Choose another claim</a> · <a href="'+BASE+'worksheets/">Print all task sheets</a> · <a href="'+BASE+'cases.json">Download the cases and route record</a></p>'
    page('systems-thinking/claim-lab/'+c['id'], c['title'], body)
home += '</div></section><p><a href="'+BASE+'worksheets/">All task sheets without answers</a> · <a href="'+BASE+'cases.json">Download the cases and route record</a></p>'
page('systems-thinking/claim-lab','Test the claim',home)
sheet = p('Task-only version. Cases are fictional. Use the linked pages after attempting the questions to see worked comparisons, counterexamples, and sources.')
for c in packet['cases']:
    sheet += '<article><h2><a href="'+BASE+c['id']+'/">'+E(c['title'])+'</a></h2><blockquote class="claim">'+E(c['claim'])+'</blockquote>'+p(c['case'])+'<h3>Your task</h3>'+p(c['task'])+'<h3>Change the conditions</h3>'+p(c['changed'])+'</article>'
page('systems-thinking/claim-lab/worksheets','Eight task sheets',sheet)
(DOCS / 'systems-thinking/claim-lab/cases.json').write_text(json.dumps(packet, ensure_ascii=False, indent=2)+'\n',encoding='utf-8')
page('updates/2026-10-04','Eight claims worth testing','<p>The <a href="'+BASE+'">new claim lab</a> offers eight short cases: boundaries, queue accounting, effective variety, organisational functions, participation, method choice, averages, and causal hypotheses.</p><p>Each has a worked comparison, a counterexample, a changed case, and labelled connections to existing method practice and source routes. Three journeys start with an actual decision. A task-only worksheet supports teaching and discussion.</p><p>Release 0.28 expands the reader material. The canonical graph and source-owner-reviewed comparator are unchanged. No independent pedagogical review or fresh primary-source review is claimed.</p>')
for route in ['systems-thinking/index.html','systems-thinking/practice/index.html','reading-list.html','updates/index.html']:
    path=DOCS/route; text=path.read_text(encoding='utf-8')
    text=re.sub('<!-- '+MARK+' -->.*?<!-- /'+MARK+' -->','',text,flags=re.S)
    assert '</main>' in text, route
    link='<section><h2>Test a systems claim</h2><p><a href="'+BASE+'">Eight cases with counterexamples, worked repairs, and source-labelled routes</a>. Start with an improvement claim, a service redesign, or a workshop brief.</p></section>'
    path.write_text(text.replace('</main>','<!-- '+MARK+' -->'+link+'<!-- /'+MARK+' --></main>',1),encoding='utf-8')
path=DOCS/'sitemap.xml';text=path.read_text(encoding='utf-8')
for route in ['systems-thinking/claim-lab','systems-thinking/claim-lab/worksheets','updates/2026-10-04']+['systems-thinking/claim-lab/'+c['id'] for c in packet['cases']]:
    url='https://transduction.systems/'+route+'/'
    if url not in text: text=text.replace('</urlset>','<url><loc>'+url+'</loc><lastmod>2026-10-04</lastmod></url></urlset>')
path.write_text(text,encoding='utf-8')
assert before == hashlib.sha256(canonical.read_bytes()).hexdigest(), 'Canonical graph changed'
for name in ['TANGLE_STATE.md','NEXT_WORK.md']:
    path=ROOT/'documentation'/name; text=path.read_text(encoding='utf-8')
    heading='## Claim-testing practice, 4 October 2026'
    if heading not in text:
        text += '\n\n'+heading+'\n\nRelease 0.28 adds eight original cases, counterexamples, worked repairs, three decision-led journeys, and task-only sheets at `/systems-thinking/claim-lab/`. This is a reader release; canonical graph data and the approved comparator are unchanged. The active packet, source limits, acceptance checks, publication gate, and remaining source work are recorded in `sources/claim-lab-2026-10-04/PACKET.md`. No independent pedagogical review or new primary-source review is claimed.\n'
        path.write_text(text,encoding='utf-8')
print('Built release 0.28 reader packet: eight cases, three journeys, and task sheets; canonical graph unchanged.')
