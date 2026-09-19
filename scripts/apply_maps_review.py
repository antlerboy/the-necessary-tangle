"""Publish a bounded comparator review without adding canonical graph claims."""
from pathlib import Path
import html
import json
import re
from refresh_graph_snapshot import write

ROOT = Path(__file__).resolve().parents[1]
DATE = '2026-09-19'
URL = 'https://transduction.systems/prior-maps/coexplorer/'

def main():
    packet = json.loads((ROOT/'sources/maps-2026-09-19/review.json').read_text(encoding='utf-8'))
    data = json.loads((ROOT/'data/public-data.json').read_text(encoding='utf-8'))
    data['map_source_review'] = packet
    data['meta'].update(release=packet['release'], generated=DATE, release_digest_url=URL,
        latest_map_review_url=URL, iteration_focus='Submitted map comparison and evidence boundaries',
        release_note='Three map descriptions, two curated reading routes, and a scoped primary-paper comparison. Canonical graph unchanged.')
    for key in ['reading_list_inventory', 'reading_list_coverage', 'core_systems_practice', 'relational_depth', 'ai_observations']:
        data[key]['release'] = packet['release']
    write(data)
    for name in ['data/relationship-quality.json', 'docs/assets/relationship-quality.json']:
        path = ROOT/name
        quality = json.loads(path.read_text(encoding='utf-8'))
        quality.update(release=packet['release'], generated=DATE)
        path.write_text(json.dumps(quality,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    cards = ''.join('<article class="source" id="source-'+s['id']+'"><h3><a href="'+html.escape(s['url'],quote=True)+'">'+html.escape(s['title'])+'</a></h3><p class="status">'+html.escape(s['access'])+'</p><p>'+html.escape(s['note'])+'</p><p class="locator">Checked: '+html.escape(s['locator'])+'.</p></article>' for s in packet['sources'])
    body = (ROOT/'sources/maps-2026-09-19/reader.html').read_text(encoding='utf-8').replace('{{SOURCE_CARDS}}',cards)
    page = '''<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Reading the CoExplorer maps | The Necessary Tangle</title><meta name="description" content="A source-scoped comparison of the CoExplorer maps, Troncale's linkage propositions, and submitted reading lists."><link rel="canonical" href="'''+URL+'''"><style>html{scroll-behavior:smooth}*{box-sizing:border-box}body{font:18px/1.65 Georgia,serif;max-width:960px;margin:auto;padding:24px;background:#faf8f3;color:#292621}h1{font-size:clamp(2rem,5vw,3rem);line-height:1.15}h2{margin-top:2rem;line-height:1.25}h3{font-size:1.15rem;line-height:1.4}a{color:#92302c;overflow-wrap:anywhere}a:focus-visible,[tabindex]:focus-visible{outline:3px solid #92302c;outline-offset:4px}nav{display:flex;flex-wrap:wrap;gap:1rem;margin:1rem 0}.eyebrow,.locator{font-size:.92rem}.note,.source{background:#f0ece3;padding:1rem;margin:1rem 0;border-left:3px solid #92302c}.status{font-weight:bold}.table-wrap{overflow-x:auto;max-width:100%}table{width:100%;border-collapse:collapse;font-size:1rem}caption{text-align:left;padding:.75rem 0}th,td{text-align:left;vertical-align:top;border-bottom:1px solid #c4b8a8;padding:.7rem;min-width:145px}thead{background:#ede6d9}.skip{position:absolute;top:-100px}.skip:focus{top:0;background:white}@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}</style></head><body><a class="skip" href="#main">Skip to content</a><nav aria-label="Site"><a href="/">Atlas</a><a href="/prior-maps/">Prior maps</a><a href="/reading-list.html">Reading</a><a href="/updates/">Updates</a></nav><main id="main">'''+body+'''</main></body></html>\n'''
    out = ROOT/'docs/prior-maps/coexplorer'
    out.mkdir(parents=True,exist_ok=True)
    (out/'index.html').write_text(page,encoding='utf-8',newline='\n')
    (out/'source-review.json').write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    for filename in ['docs/updates/index.html','docs/reading-list.html','docs/prior-maps/index.html']:
        path=ROOT/filename
        text=path.read_text(encoding='utf-8')
        text=re.sub(r'<!-- maps-20260919 -->.*?<!-- /maps-20260919 -->','',text,flags=re.S)
        assert '</main>' in text, filename
        text=text.replace('</main>','<!-- maps-20260919 --><section><h2>CoExplorer and submitted reading</h2><p><a href="/prior-maps/coexplorer/">Three maps, their relationship meanings, and source-access limits</a></p></section><!-- /maps-20260919 --></main>',1)
        path.write_text(text,encoding='utf-8',newline='\n')
    path=ROOT/'docs/sitemap.xml';text=path.read_text(encoding='utf-8')
    if URL not in text:text=text.replace('</urlset>','<url><loc>'+URL+'</loc><lastmod>'+DATE+'</lastmod></url></urlset>')
    path.write_text(text,encoding='utf-8',newline='\n')
    note='Release 0.25 adds a source-scoped CoExplorer comparison and compares the two Anselm articles, with their individual recommendations still unverified. Canonical graph counts remain 785 public entries, 912 total nodes, 2,112 statements, 315 sources, and 173 profiles. No new canonical claims or complete external datasets are imported. See '+URL+' and sources/maps-2026-09-19/. Dataset reconciliation and specialist review remain open.'
    for name,heading in [('README.md','## Release 0.25'),('CHANGELOG.md','## 0.25 - 19 September 2026')]:
        path=ROOT/name;text=path.read_text(encoding='utf-8')
        if heading not in text:path.write_text(text.rstrip()+'\n\n'+heading+'\n\n'+note+'\n',encoding='utf-8',newline='\n')
    path=ROOT/'CITATION.cff';text=path.read_text(encoding='utf-8')
    text=re.sub(r'^version:.*$','version: 0.25',text,flags=re.M)
    text=re.sub(r'^date-released:.*$','date-released: '+DATE,text,flags=re.M)
    path.write_text(text,encoding='utf-8',newline='\n')
    path=ROOT/'documentation/TANGLE_STATE.md';text=path.read_text(encoding='utf-8')
    text=re.sub(r'## Map comparison, 19 September 2026\n.*?(?=\n## |\Z)','',text,flags=re.S)
    text=text.replace('# Tangle state\n','# Tangle state\n\n## Map comparison, 19 September 2026\n\n'+note+'\n',1)
    text=text.replace('Last verified: 6 September 2026 (release validation and anonymous event submission receipt)', 'Earlier release verification: 6 September 2026 (anonymous event submission receipt). Current publication checks are recorded in the active work packet.')
    text=text.replace('- Release: `0.22`; publication explicitly authorised on 5 September 2026.','- Release: `0.25`; publication authorised by the overnight website review.')
    text=text.replace('- Canonical public entries: 719; developed profiles: 137; public sources: 224.','- Canonical public entries: 785; developed profiles: 173; public sources: 315.')
    text=text.replace('- Graph records: 846; typed statements: 1,987; guided journeys: 24.','- Graph records: 912; typed statements: 2,112. Other historical metrics below retain their stated release scope.')
    text=text.replace('- Public change digest: https://transduction.systems/updates/0.22/','- Public change digest: '+URL)
    path.write_text(text,encoding='utf-8',newline='\n')
    print('Applied release 0.25 map-source review; canonical graph unchanged')

if __name__=='__main__':main()
