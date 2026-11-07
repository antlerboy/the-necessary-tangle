"""Apply the bounded variety research edition to three existing profiles."""
from pathlib import Path
import copy, json, re, shutil
from apply_iteration_17 import enc, parse, upsert
from refresh_graph_snapshot import write
from apply_overnight_review import quality_result
from apply_relational_depth_16 import write_relational_document
R=Path(__file__).resolve().parents[1]; D=R/'docs'; S=R/'documentation/research-2026-11-07-variety'
M='variety_20261107'; P=json.loads((S/'Candidate packet.json').read_text(encoding='utf-8-sig'))
d=json.loads((R/'data/public-data.json').read_text(encoding='utf-8')); originals=copy.deepcopy(d.get(M,{}).get('originals',{}))
for pc in P['profile_candidates']:
 n=pc['node_id']; old=next(x for x in d['profiles'] if x['node_id']==n)
 if 'profiles' not in originals: originals['profiles']=[]
 if not any(x['node_id']==n for x in originals['profiles']): originals['profiles'].append(copy.deepcopy(old))
 profile=copy.deepcopy(pc['proposed_profile'])
 ids=[f'ev_u40_variety_{x.lower()}' for x in pc['new_source_fact_ids']]
 profile['evidence_ids']=enc(list(dict.fromkeys(parse(profile['evidence_ids'])+ids)))
 profile['connection_pass']=M
 upsert(d['profiles'],[profile],'node_id')
for f in P['source_facts']:
 row=dict(id=f"ev_u40_variety_{f['id'].lower()}",source_id=f['source'],locator=f['locator'],excerpt_or_summary=f['text'],evidence_type='primary_text_paraphrase',quality_tier='A',licence='see_source',review_status='research_pass_needs_editor',content_hash='',public_evidence_status='public',connection_pass=M)
 upsert(d['evidence'],[row],'id')
d[M]=dict(date='2026-11-07',originals=originals,source_packet='documentation/research-2026-11-07-variety/',reader_url='/reading/which-distinctions/',scope='Three existing profiles; primary clarifications and original finite exposition; editorial acceptance pending.')
d['meta'].update(release='0.40',generated='2026-11-07',release_digest_url='https://transduction.systems/updates/2026-11-07-variety/',iteration_focus='Which distinctions change the decision?',release_note='Three bounded variety profiles and an original finite model; editorial acceptance pending.')
d['relational_depth'].update(release='0.40',generated='2026-11-07')
write(d)
q=quality_result(d); q.update(release='0.40',generated='2026-11-07')
for key in ['adversarial_review','doncaster_lineage_review']: q[key]=d[key]
for name in ['data/relationship-quality.json','docs/assets/relationship-quality.json']: (R/name).write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
write_relational_document(d)
# Keep the independently checked model byte-for-byte; adapt only stage wording and framing.
out=D/'reading/which-distinctions'; out.mkdir(parents=True,exist_ok=True)
for name in ['model-core.js','candidate-data.js','reader.js','reader.css']:
 shutil.copyfile(S/name,out/name)
t=(S/'Reader.html').read_text(encoding='utf-8')
t=t.replace('Tangle research candidate · 7 November 2026','The Necessary Tangle · research edition 0.40 · 7 November 2026')
t=t.replace('Three existing profiles, two primary texts, and one original finite model. Candidate for editorial review; the shared graph and public release are unchanged.','Three existing profiles, two primary texts, and one original finite model. This research edition awaits human editorial acceptance.')
t=t.replace('Profile proposals','Three profiles').replace('Three bounded profile proposals','Three bounded profiles')
t=t.replace('The existing records are retained in an exact baseline. Each proposal adds a primary clarification and a distinction tested by the finite model.','Each profile adds a primary clarification and a distinction tested by the finite model.')
t=t.replace('<p><a href="Candidate%20packet.json">Inspect the complete candidate and deferrals</a> · <a href="Existing%20three-profile%20baseline.json">Inspect the unchanged profile baseline</a></p>','<p><a href="/entries/concept_variety/">Variety</a> · <a href="/entries/concept_variety_amplification/">Variety amplification</a> · <a href="/entries/concept_variety_attenuation/">Variety attenuation</a></p>')
t=t.replace('Full texts, page images, and private recovery material are kept outside any public-safe candidate.','The linked primary texts retain their authorship and terms.')
t=t.replace('No historical influence, new graph edge, canonical acceptance, or publication is inferred. The existing deployment checkpoint remains separate.','No historical influence or new graph edge is inferred. Human editorial acceptance remains pending.')
t=t.replace('Local candidate for Benjamin P Taylor’s Tangle research. The examples are stipulated, the interpretation is editorial, and human acceptance remains pending. No current website release or cloud synchronisation is claimed.','Curated by Benjamin P Taylor. The examples are stipulated, the interpretation is editorial, and human acceptance remains pending.')
t=t.replace('<body><main>','<body><nav class="site-nav" aria-label="Main"><a href="/">Atlas</a><a href="/library/">Sources</a><a href="/learning/">Learning</a><a href="/updates/2026-11-07-variety/">Release update</a></nav><main>')
t=t.replace('</body>','<a id="openUpdates" href="https://github.com/antlerboy/the-necessary-tangle/issues/2" aria-label="Open updates"></a></body>')
(out/'index.html').write_text(t,encoding='utf-8')
with (out/'reader.css').open('a',encoding='utf-8') as f: f.write('\n.site-nav{max-width:1120px;margin:auto;padding:1.4rem 26px 0;font:1rem/1.5 system-ui;display:flex;gap:1rem;flex-wrap:wrap}h1,h2,h3{font-family:Georgia,serif}#openUpdates{position:fixed;bottom:0;right:0;width:44px;height:44px}#openUpdates:after{content:"";position:absolute;right:8px;bottom:8px;width:5px;height:5px;background:#862719;border-radius:50%;box-shadow:0 0 0 1px white}\n')
update=D/'updates/2026-11-07-variety'; update.mkdir(parents=True,exist_ok=True)
(update/'index.html').write_text('<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Variety | The Necessary Tangle</title><link rel="stylesheet" href="/assets/readable-atlas.css"><style>#openUpdates{position:fixed;bottom:0;right:0;width:44px;height:44px}#openUpdates:after{content:"";position:absolute;right:8px;bottom:8px;width:5px;height:5px;background:#862719;border-radius:50%;box-shadow:0 0 0 1px white}</style></head><body><nav><a href="/">Atlas</a> <a href="/updates/">Updates</a></nav><main><h1>Which distinctions change the decision?</h1><p>Release 0.40 develops three existing variety profiles using located primary passages and an original finite model. Human editorial acceptance remains pending.</p><p><a href="/reading/which-distinctions/">Explore the model and sources</a></p></main><a id="openUpdates" href="https://github.com/antlerboy/the-necessary-tangle/issues/2" aria-label="Open updates"></a></body></html>',encoding='utf-8')
for name in ['index.html','library/index.html','learning/index.html','updates/index.html']:
 p=D/name; t=p.read_text(encoding='utf-8'); t=re.sub(r'<!-- '+M+r' -->.*?<!-- /'+M+r' -->','',t,flags=re.S)
 block='<!-- '+M+' --><section class="resource-pathways plain-panel wide"><h2><a href="/reading/which-distinctions/">Which distinctions change the decision?</a></h2><p>Explore variety, classification, and a finite model.</p></section><!-- /'+M+' -->'
 t=t.replace('</main>',block+'</main>',1) if name!='index.html' else t.replace('<section id="systemsPracticeCallout"',block+'<section id="systemsPracticeCallout"',1)
 if name=='index.html':
  t=re.sub(r'<span id="releaseBadge">Release [^<]+</span>','<span id="releaseBadge">Release 0.40</span>',t,count=1); t=re.sub(r'assets/public-data.js\?v=[^"\s]+','assets/public-data.js?v=0.40',t)
 p.write_text(t,encoding='utf-8')
p=D/'sitemap.xml'; t=p.read_text(encoding='utf-8')
for route in ['/reading/which-distinctions/','/updates/2026-11-07-variety/']:
 url='https://transduction.systems'+route
 if url not in t: t=t.replace('</urlset>','<url><loc>'+url+'</loc><lastmod>2026-11-07</lastmod></url></urlset>')
p.write_text(t,encoding='utf-8')
print('0.40 variety overlay applied')
# Record the local research edition in generated release documentation.
p=R/'documentation/TANGLE_STATE.md'; t=p.read_text(encoding='utf-8'); t=re.sub(r'<!-- '+M+r' -->.*?<!-- /'+M+r' -->\s*','',t,flags=re.S).replace('## Current release 0.39','## Previous graph release 0.39'); block='<!-- '+M+' -->\n## Current research edition 0.40\n\n7 November 2026. Three existing variety profiles receive located primary-source clarifications and a finite editorial model. Reader route: https://transduction.systems/reading/which-distinctions/. Human editorial acceptance remains pending. Deployment identity and live checks belong to deployment.json and the Publish workflow.\n<!-- /'+M+' -->\n\n'; t=t.replace('# Current Tangle state\n','# Current Tangle state\n\n'+block,1); p.write_text(t,encoding='utf-8')
p=R/'README.md'; t=p.read_text(encoding='utf-8'); t=re.sub(r'<!-- current-31 -->.*?<!-- /current-31 -->','<!-- current-31 -->\nCurrent research edition: **0.40, 7 November 2026**. [Variety and classification](https://transduction.systems/reading/which-distinctions/). Human editorial acceptance remains pending.\n<!-- /current-31 -->',t,flags=re.S); p.write_text(t,encoding='utf-8')
p=R/'CITATION.cff'; t=re.sub(r'^version:.*$',"version: '0.40'",p.read_text(encoding='utf-8'),flags=re.M); p.write_text(t,encoding='utf-8')
p=R/'CHANGELOG.md'; t=p.read_text(encoding='utf-8'); entry='\n\n## 0.40 — 7 November 2026\n\nThree existing variety profiles, located primary evidence, and an original finite model. Human editorial acceptance remains pending.\n'; t=t if '## 0.40 — 7 November 2026' in t else t.replace('# Changelog','# Changelog'+entry,1); p.write_text(t,encoding='utf-8')

# The final overlay owns the current packet; earlier overlays may restore their historical packet.
(R/'documentation/NEXT_WORK.md').write_text((S/'work-packet.md').read_text(encoding='utf-8'),encoding='utf-8')
