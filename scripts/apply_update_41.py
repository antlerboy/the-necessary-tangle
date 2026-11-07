"""Apply the bounded feedback and regulation research edition."""
from pathlib import Path
import copy, json, re, shutil
from apply_iteration_17 import upsert
from refresh_graph_snapshot import write
from apply_overnight_review import quality_result
from apply_relational_depth_16 import write_relational_document
R=Path(__file__).resolve().parents[1]; D=R/'docs'; S=R/'documentation/research-2026-11-07-feedback'; M='feedback_regulation_20261107'
p=json.loads((S/'Candidate packet.json').read_text(encoding='utf-8-sig'))
d=json.loads((R/'data/public-data.json').read_text(encoding='utf-8')); originals=copy.deepcopy(d.get(M,{}).get('originals',{}))
if not originals:
 originals={'profiles':[copy.deepcopy(x) for x in d['profiles'] if x['node_id'] in p['cohort']]}
for pc in p['profile_candidates']:
 upsert(d['profiles'],[copy.deepcopy(pc['proposed_profile'])],'node_id')
for f,ident in zip(p['source_facts'],['ev41_feedback_maxwell_dynamics','ev41_feedback_rwb_usage','ev41_feedback_ashby_usage','ev41_regulation_ashby_scope']):
 row=dict(id=ident,source_id=f['source'],locator=f['locator'],excerpt_or_summary=f['text'],evidence_type='primary_text_paraphrase',quality_tier='A',licence='see_source',review_status='research_pass_needs_editor',content_hash='',public_evidence_status='public',connection_pass=M)
 upsert(d['evidence'],[row],'id')
d[M]=dict(date='2026-11-07',originals=originals,source_packet='documentation/research-2026-11-07-feedback/',reader_url='/reading/feedback-and-regulation/',scope='Two existing profiles, four primary-text clarifications and original exposition; editorial acceptance pending.')
d['meta'].update(release='0.41',generated='2026-11-07',release_digest_url='https://transduction.systems/updates/2026-11-07-feedback/',iteration_focus='Feedback and regulation: trace the mechanism',release_note='Two bounded profiles and an original discrete response model; editorial acceptance pending.')
d['relational_depth'].update(release='0.41',generated='2026-11-07'); write(d)
q=quality_result(d);q.update(release='0.41',generated='2026-11-07')
for key in ['adversarial_review','doncaster_lineage_review']: q[key]=d[key]
for name in ['data/relationship-quality.json','docs/assets/relationship-quality.json']: (R/name).write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
write_relational_document(d)
out=D/'reading/feedback-and-regulation';out.mkdir(parents=True,exist_ok=True)
for name in ['Candidate packet.json','Existing two-profile baseline.json','reader.css']: shutil.copyfile(S/name,out/name)
shutil.copytree(S/'model',out/'model',dirs_exist_ok=True)
dot='<a id="openUpdates" href="https://github.com/antlerboy/the-necessary-tangle/issues/2" aria-label="Open updates"></a>'
style='<style>#openUpdates{position:fixed;bottom:0;right:0;width:44px;height:44px}#openUpdates:after{content:"";position:absolute;right:8px;bottom:8px;width:5px;height:5px;background:#862719;border-radius:50%;box-shadow:0 0 0 1px white}</style>'
t=(S/'Reader.html').read_text(encoding='utf-8-sig').replace('primary-text working candidate','research edition 0.41').replace('not yet applied or published · human editorial review pending','human editorial review pending').replace('Profile proposals','Existing profiles').replace('Proposals for the existing profiles','The existing profiles').replace('The candidate keeps both canonical definitions, every prior evidence link, and all existing open checks. It proposes four new located-evidence records.','This edition keeps both canonical definitions, every prior evidence link, and all existing open checks. It adds four located-evidence records.').replace('Research candidate; no publication or human editorial acceptance is claimed.','Human editorial acceptance remains pending.')
reader_nav='<nav class="atlas-nav" aria-label="Atlas navigation"><a href="/">Atlas</a><a href="/entries/concept_feedback/">Feedback profile</a><a href="/entries/concept_regulation/">Regulation profile</a></nav>'
model_nav='<nav class="atlas-nav" aria-label="Atlas navigation"><a href="/reading/feedback-and-regulation/">Feedback and regulation</a><a href="/">Atlas</a></nav>'
nav_style='<style>.atlas-nav{display:flex;flex-wrap:wrap;gap:.65rem 1.2rem;margin:0 0 2rem;font:600 .95rem/1.5 system-ui,sans-serif}.atlas-nav a{color:#862719;text-underline-offset:3px}.atlas-nav a:focus-visible{outline:3px solid #862719;outline-offset:4px}</style>'
reader_style='<style>main a{color:#862719}main a.button{background:#862719;color:#fffdf8}main a:hover{color:#5f1c14}main a.button:hover{background:#5f1c14;color:#fffdf8}</style>'
t=t.replace('</head>',style+nav_style+reader_style+'</head>').replace('<body><main>','<body><main>'+reader_nav).replace('</body>',dot+'</body>');(out/'index.html').write_text(t,encoding='utf-8')
pmodel=out/'model/index.html';t=pmodel.read_text(encoding='utf-8-sig').replace('</head>',style+nav_style+'</head>').replace('<body><main>','<body><main>'+model_nav).replace('</body>',dot+'</body>');pmodel.write_text(t,encoding='utf-8')
update=D/'updates/2026-11-07-feedback';update.mkdir(parents=True,exist_ok=True)
(update/'index.html').write_text('<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Feedback and regulation | The Necessary Tangle</title><link rel="stylesheet" href="/assets/readable-atlas.css">'+style+'</head><body><nav><a href="/">Atlas</a> <a href="/updates/">Updates</a></nav><main><h1>Feedback and regulation: trace the mechanism</h1><p>Release 0.41 develops two existing profiles, four located primary-text clarifications, and an original discrete model. Human editorial acceptance remains pending.</p><p><a href="/reading/feedback-and-regulation/">Explore the model and sources</a></p></main>'+dot+'</body></html>',encoding='utf-8')
for name in ['index.html','library/index.html','learning/index.html','updates/index.html']:
 path=D/name;t=path.read_text(encoding='utf-8');t=re.sub(r'<!-- '+M+r' -->.*?<!-- /'+M+r' -->','',t,flags=re.S)
 block='<!-- '+M+' --><section class="resource-pathways plain-panel wide"><h2><a href="/reading/feedback-and-regulation/">Feedback and regulation: trace the mechanism</a></h2><p>Compare sources and explore a discrete response.</p></section><!-- /'+M+' -->'
 t=t.replace('</main>',block+'</main>',1) if name!='index.html' else t.replace('<section id="systemsPracticeCallout"',block+'<section id="systemsPracticeCallout"',1)
 if name=='index.html': t=re.sub(r'<span id="releaseBadge">Release [^<]+</span>','<span id="releaseBadge">Release 0.41</span>',t,count=1);t=re.sub(r'assets/public-data.js\?v=[^"\s]+','assets/public-data.js?v=0.41',t)
 path.write_text(t,encoding='utf-8')
path=D/'sitemap.xml';t=path.read_text(encoding='utf-8')
for route in ['/reading/feedback-and-regulation/','/reading/feedback-and-regulation/model/','/updates/2026-11-07-feedback/']:
 url='https://transduction.systems'+route
 if url not in t:t=t.replace('</urlset>','<url><loc>'+url+'</loc><lastmod>2026-11-07</lastmod></url></urlset>')
path.write_text(t,encoding='utf-8')
path=R/'documentation/TANGLE_STATE.md';t=path.read_text(encoding='utf-8');t=re.sub(r'<!-- '+M+r' -->.*?<!-- /'+M+r' -->\s*','',t,flags=re.S).replace('## Current research edition 0.40','## Previous research edition 0.40');block='<!-- '+M+' -->\n## Current research edition 0.41\n\n7 November 2026. Two existing profiles receive four located primary clarifications and an original discrete response model. Reader route: https://transduction.systems/reading/feedback-and-regulation/. Human editorial acceptance remains pending. Deployment identity and live checks belong to deployment.json and the Publish workflow.\n<!-- /'+M+' -->\n\n';path.write_text(t.replace('# Current Tangle state\n','# Current Tangle state\n\n'+block,1),encoding='utf-8')
path=R/'README.md';t=path.read_text(encoding='utf-8');t=re.sub(r'<!-- current-31 -->.*?<!-- /current-31 -->','<!-- current-31 -->\nCurrent research edition: **0.41, 7 November 2026**. [Feedback and regulation](https://transduction.systems/reading/feedback-and-regulation/). Human editorial acceptance remains pending.\n<!-- /current-31 -->',t,flags=re.S);path.write_text(t,encoding='utf-8')
path=R/'CITATION.cff';path.write_text(re.sub(r'^version:.*$',"version: '0.41'",path.read_text(encoding='utf-8'),flags=re.M),encoding='utf-8')
path=R/'CHANGELOG.md';t=path.read_text(encoding='utf-8');entry='\n\n## 0.41 — 7 November 2026\n\nTwo existing profiles, four located primary clarifications, and an original discrete response model. Human editorial acceptance remains pending.\n';path.write_text(t if '## 0.41 — 7 November 2026' in t else t.replace('# Changelog','# Changelog'+entry,1),encoding='utf-8')
(R/'documentation/NEXT_WORK.md').write_text('# Next work\n\n## Current packet: feedback and regulation 0.41\n\nStatus: local candidate under review. CI, publication, and live verification are pending; human editorial acceptance remains pending. Two existing profiles, four located primary clarifications, and an original discrete model. Preserve the source packet and prior source-owner-reviewed material; no new nodes, edges, journeys, or historical influence are implied.\n',encoding='utf-8')
print('0.41 feedback and regulation overlay applied')
