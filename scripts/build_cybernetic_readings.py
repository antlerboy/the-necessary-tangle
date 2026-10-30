"""Build an attributed companion reading guide without changing atlas claims."""
from pathlib import Path
from html import escape as E
import json,re
R=Path(__file__).resolve().parents[1];D=R/'docs';S=R/'sources/cybernetic-readings'
packet=json.loads((S/'sources.json').read_text());rows=packet['sources']
node_ids={n['id'] for n in json.loads((R/'data/public-data.json').read_text())['nodes']}
assert len({r['id'] for r in rows})==4
assert all(c['target'] in node_ids for r in rows for c in r['connections'])
def a(url,title):return '<a href="'+E(url,quote=True)+'">'+E(title)+'</a>'
intro='<p class="eyebrow">Companion reading guide · Edition 1.0 · 30 October 2026</p><h1>Sayings, regulation and conversation</h1><p class="lead">Four ways into cybernetics, with the source, the question it opens and the limits of this reading kept together.</p><p>Read a saying as an invitation to examine something, then follow the argument and its conditions. These routes bring different kinds of material into view: a curated register, a transcription, a developing research programme and an author’s archive. The questions below are editorial reading prompts.</p>'
body=intro
for r in rows:
 body+='<section id="'+E(r['id'])+'"><h2>'+a(r['url'],r['title'])+'</h2><p class="meta">'+E('; '.join(r['authors']))+' · '+E(r['date'])+'</p><p>'+E(r['summary'])+'</p><h3>A question to take into the reading</h3><p>'+E(r['question'])+'</p><p class="source"><strong>Source locator:</strong> '+E(r['locator'])+'</p><p><strong>Limits:</strong> '+E(r['limits'])+'</p><ul>'
 for c in r['connections']:body+='<li>'+a('/#view=item&id='+c['target'],c['label'])+' — '+E(c['phrase'])+'. '+E(c['scope'])+'</li>'
 for x in r.get('further',[]):body+='<li>'+a(x['url'],x['title'])+'</li>'
 body+='</ul></section>'
body+='<section><h2>Continue with the argument</h2><p>'+a('/reading/connections/#regulation','Ashby, models and regulation')+' · '+a('/reading/connections/#learning','What changes when we learn?')+' · '+a('/saidtosomeone/','The von Foerster source register')+'</p><p>These are reading routes, not additional evidence-graph relationships or a claim that the sources agree. Public source access does not transfer rights.</p><p>'+a('sources.json','Download the source and scope ledger')+'</p></section>'
css=':root{color-scheme:light;--red:#862719;--paper:#f6f0e5}*{box-sizing:border-box}body{margin:0;background:var(--paper);color:#29221b;font:19px/1.65 Georgia,serif}nav,main,footer{max-width:900px;margin:auto;padding:24px}nav{display:flex;gap:24px;flex-wrap:wrap;font:16px/1.5 system-ui}a{color:var(--red);overflow-wrap:anywhere}h1{font-size:clamp(2.2rem,6vw,3.7rem);line-height:1.1}h2{font-size:1.65rem;line-height:1.3}h3{font-size:1.1rem}section{padding:24px 0;border-top:1px solid #cdbda6}.meta,.eyebrow,.source,footer{font:15px/1.6 system-ui}.lead{font-size:1.3rem}li{margin:.75em 0}a:focus-visible{outline:3px solid #d58c11;outline-offset:3px}#openUpdates{position:fixed;right:0;bottom:0;width:44px;height:44px}#openUpdates:after{content:"";position:absolute;right:8px;bottom:8px;width:5px;height:5px;border-radius:50%;background:var(--red)}'
page='<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Sayings, regulation and conversation | The Necessary Tangle</title><meta name="description" content="Read Ashby, von Foerster, Richard S O’Rourke and Paul Pangaro with clear attribution, source locators and reading questions."><link rel="canonical" href="https://transduction.systems/reading/cybernetic-sources/"><style>'+css+'</style></head><body><a href="#main-content">Skip to reading</a><nav aria-label="Main">'+a('/','Atlas')+a('/library/','Sources')+a('/learning/','Learning')+'</nav><main id="main-content">'+body+'</main><footer>Curated by Benjamin P Taylor. Primary-source reading assisted by AI. Sources retain their authorship and terms.</footer><a id="openUpdates" href="https://github.com/antlerboy/the-necessary-tangle/issues/2" aria-label="Open updates"></a></body></html>\n'
folder=D/'reading/cybernetic-sources';folder.mkdir(parents=True,exist_ok=True);(folder/'index.html').write_text(page);(folder/'sources.json').write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n')
# Extend the existing source search without fabricating atlas nodes or edges.
p=D/'library/catalogue.json';cat=json.loads(p.read_text());ids={r['id'] for r in rows};cat['records']=[r for r in cat['records'] if r['id'] not in ids]
for r in rows:cat['records'].append({**{k:r[k] for k in ['id','title','url','authors','summary','locator','connections']},'collection':'Cybernetic readings','format':'Attributed reading route','year':'2026' if r['id']!='cybernetic_reading_ashby' else '1981','review':'Source-scoped reading; see guide for access and attribution limits','atlas_id':''})
cat['counts']['source_register_records']=len(cat['records']);cat['counts']['cybernetic_readings']=4;p.write_text(json.dumps(cat,ensure_ascii=False,separators=(',',':'))+'\n')
marker='cybernetic-readings-20261030';block='<section class="resource-pathways" id="cyberneticReadings"><h2>'+a('/reading/cybernetic-sources/','Sayings, regulation and conversation')+'</h2><p>Read Ashby, von Foerster, Richard S O’Rourke and Paul Pangaro through attributed sources, precise questions and explicit limits.</p></section>'
for rel in ['index.html','library/index.html','learning/index.html']:
 p=D/rel;text=p.read_text();start='<!-- '+marker+' -->';end='<!-- /'+marker+' -->';rep=start+block+end
 if start in text:text=re.sub(re.escape(start)+'.*?'+re.escape(end),lambda _:rep,text,flags=re.S)
 else:text=text.replace('</main>',rep+'</main>',1)
 p.write_text(text)
p=D/'sitemap.xml';text=p.read_text();url='https://transduction.systems/reading/cybernetic-sources/'
if '<loc>'+url+'</loc>' not in text:text=text.replace('</urlset>','<url><loc>'+url+'</loc></url></urlset>')
p.write_text(text)
assert all(r['url'] in page for r in rows) and 'aria-label="Open updates"' in page
assert len({r['id'] for r in cat['records']})==len(cat['records'])
print('Cybernetic readings: four attributed source routes, valid concept targets, searchable library and navigation; graph unchanged.')
