"""Reproducible, bounded SysCoI and Ashby Laboratory intake for 18 October."""
from pathlib import Path
import html, json, re, hashlib, math
from apply_iteration_17 import enc, upsert, source_record, node_record, edge_record
from apply_iteration_09 import graph_metrics
from apply_relational_depth_16 import calculate_relational_depth, write_relational_document
from apply_doncaster_lineage import refresh_counts
from apply_overnight_review import quality_result
from refresh_graph_snapshot import calculate, write
R=Path(__file__).resolve().parents[1]; D=R/'docs'; S=R/'sources/update-2026-10-18'
DATE='2026-10-18'; RELEASE='0.33'; MARK='update_20261018'
P=json.loads((S/'syscoi-review.json').read_text(encoding='utf-8'))
A=json.loads((S/'ashby-review.json').read_text(encoding='utf-8'))
H=json.loads((S/'events-review.json').read_text(encoding='utf-8'))
d=json.loads((R/'data/public-data.json').read_text(encoding='utf-8'))
E=lambda s:html.escape(str(s),quote=True)
def link(url,title):return '<a href="'+E(url)+'">'+E(title)+'</a>'
def atlas(nid):
    n=next(n for n in d['nodes'] if n['id']==nid)
    return link('/#view=item&id='+nid,n['label'])
def source(sid,title,url,note,locator):
    r=source_record(sid,title,'public_source',url,note,[],'Source linked through SysCoI' if 'syscoi' in sid else 'Ashby Laboratory','2026',quality='B')
    r.update(connection_pass=MARK,last_checked=DATE,review_status='source_scoped_research_pass',source_locator=locator)
    upsert(d['sources'],[r],'id'); return sid
def node(nid,title,kind,summary,sids,tags):
    i=int(hashlib.sha256(nid.encode()).hexdigest()[:6],16)
    r=node_record(nid,title,kind,summary,sids,round(.55+.2*math.cos(i*2.4),6),round(.45+.2*math.sin(i*2.4),6),tags)
    r.update(connection_pass=MARK,status='candidate',review_status='research_pass_needs_editor',reviewed_by='',reviewed_at='',inclusion_reason=MARK,set_tags=enc(['systems','release_0_33',*tags]))
    upsert(d['nodes'],[r],'id'); return nid
def edge(eid,a,b,typ,sid,locator,scope):
    family=next(r['relation_family'] for r in d['relation_types'] if r['relation_type']==typ)
    r=edge_record(eid,a,b,typ,family,typ.replace('_',' '),[sid],locator,scope,status='candidate',confidence='',review_label='Source-scoped candidate; editorial review remains open')
    r.update(connection_pass=MARK)
    upsert(d['edges'],[r],'id')

cs=source('src_u33_syscoi_collection','SysCoI additions, 8–18 October 2026',P['api'],'Published discovery metadata. Seven announcements reuse existing resources; linked substantive claims are not automatically accepted.','Published post IDs, dates and outbound destinations')
collection=node('collection_syscoi_20261018','SysCoI additions: 8–18 October 2026','collection','A dated discovery collection accounting for 27 published posts. Twenty reading leads receive new records; seven announcements link to material already represented. Collection membership documents discovery, not agreement or historical influence.',[cs],['syscoi-intake'])
for p in P['posts']:
    if p['status']!='new_discovery':continue
    sid=source('src_syscoi_post_'+str(p['id']),p['title'],p['url'],p['summary'],'Post title, publication date and original outbound links')
    sr=next(s for s in d['sources'] if s['id']==sid)
    sr.update(publisher='Systems Community of Inquiry',date=p['date'][:10],original_urls=enc(p['links']),source_role='discovery provenance')
    nid=node('publication_syscoi_post_'+str(p['id']),p['title'],'publication',p['summary'],[sid],['syscoi-intake'])
    edge('e33_collection_'+str(p['id']),collection,nid,'catalogues_resource',sid,'Post ID '+str(p['id'])+'; title and date','Documentary membership of this dated reading collection only. Original sources retain their authorship and claims.')

sid=source('src_u33_ashby_laboratory',A['title'],A['url'],A['attribution']+' '+A['scope'],'Public chapter collections and exercise names in content.js; app.js navigation and engine.js inspected')
lab=node('tool_ashby_laboratory','Ashby Laboratory','tool','An independent interactive learning resource adapting chapters 3–6 of W. Ross Ashby’s An Introduction to Cybernetics. Its 56 exercises and 45 glossary entries support inquiry into states, transformations, inputs, stability, black boxes and models. Exercise correctness has not been independently certified.',[sid],['learning','cybernetics'])
for target,locator,scope in [
('concept_modelling','Chapters 3 and 6: state descriptions, weak models and lost distinctions','The laboratory provides exercises about state descriptions and model simplification. This records educational coverage; it does not establish the general validity of a model.'),
('concept_boundary','Chapter 4: Whose input is it?','The exercise examines how a chosen boundary changes whether a quantity is treated as input or output.'),
('concept_feedback','Chapter 5: stability exercises','The laboratory examines feedback and stability, including why loop sign alone does not establish stability.'),
('concept_black_box','Chapter 6: A blank is not a self-loop; Choose a revealing experiment','The laboratory provides black-box observation and experiment exercises, retaining unobserved transitions as unknown.'),
('concept_isomorphism','Chapter 6: isomorphism, coordinate changes and coarse-graining','The laboratory distinguishes structure-preserving relabelling from simplifications that may lose distinctions.')]:
    edge('e33_lab_'+target,lab,target,'presents_account_of',sid,locator,scope)

refresh_counts(d)
d['relational_depth']=calculate_relational_depth(d); d['relational_depth'].update(release=RELEASE,generated=DATE)
d['graph_snapshot']=calculate(d); metrics=graph_metrics(d); depth=d['relational_depth']['aggregate']
d[MARK]=dict(date=DATE,posts_checked=len(P['posts']),new_discovery_records=20,reused_resources=7,ashby_url=A['url'],ashby_reader='/reading/ashby-laboratory/',events=H)
d['meta'].update(release=RELEASE,generated=DATE,release_digest_url='https://transduction.systems/updates/2026-10-18/',latest_intake_url='https://transduction.systems/updates/2026-10-18/',iteration_focus='Current SysCoI discovery, event refresh and attributed Ashby Laboratory learning pathways',release_note='27 SysCoI posts reconciled: 20 new reading leads and seven existing routes; Ashby Laboratory with four chapter pathways; current event collection.',node_count=len(d['nodes']),edge_count=len(d['edges']),source_count=len(d['sources']),profile_count=len(d['profiles']),public_entry_count=metrics['public_entries'],described_entry_count=metrics['public_entries'],reader_connected_entry_count=depth['reader_connected_entries'],semantic_connected_entry_count=depth['semantic_connected_entries'],unconnected_entry_count=depth['connection_bands'].get('unconnected',0),semantic_gap_entry_count=metrics['public_entries']-depth['semantic_connected_entries'],public_link_source_count=sum(s.get('public_link_status')=='public_link' for s in d['sources']),no_public_link_source_count=sum(s.get('public_link_status')=='no_public_link' for s in d['sources']))
for band in ['rich','developing','thin']:d['meta'][band+'_entry_count']=depth['connection_bands'].get(band,0)
write(d)
q=quality_result(d); q.update(release=RELEASE,generated=DATE)
for key in ['adversarial_review','doncaster_lineage_review']:q[key]=d[key]
for name in ['data/relationship-quality.json','docs/assets/relationship-quality.json']:(R/name).write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
write_relational_document(d)

css='*{box-sizing:border-box}body{margin:0;background:#faf8f2;color:#302b26;font:18px/1.65 Georgia,serif}main,nav,footer{max-width:62rem;margin:auto;padding:1.4rem}nav{display:flex;gap:1rem;flex-wrap:wrap;font:1rem/1.5 system-ui}a{color:#973d32;overflow-wrap:anywhere}a:focus-visible,summary:focus-visible{outline:3px solid #973d32;outline-offset:3px}h1{font-size:clamp(2rem,6vw,3.5rem);line-height:1.15}h2{line-height:1.3}section,article{border-bottom:1px solid #d8d0c5;padding:1rem 0}.meta,.status{font:1rem/1.5 system-ui}.status{color:#63574a}.note{background:#f0eadd;padding:1rem}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,25rem),1fr));gap:1.4rem}.grid article{padding:1rem;border:1px solid #d8d0c5;border-top:3px solid #973d32}summary{cursor:pointer;font-weight:bold}#openUpdates{position:fixed;bottom:0;right:0;width:44px;height:44px}#openUpdates:after{content:"";position:absolute;right:8px;bottom:8px;width:5px;height:5px;background:#862719;border-radius:50%;box-shadow:0 0 0 1px white}@media(max-width:600px){main,nav,footer{padding:1rem}ul,ol{padding-left:1.3rem}}'
def page(route,title,body):
    dest=D/route.strip('/');dest.mkdir(parents=True,exist_ok=True)
    text='<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+E(title)+' | The Necessary Tangle</title><link rel="canonical" href="https://transduction.systems'+route+'"><style>'+css+'</style></head><body><nav aria-label="Main">'+link('/','Atlas')+link('/learning/','Learning')+link('/events/','Events')+link('/updates/2026-10-18/','Latest update')+'</nav><main><p class="meta">Release 0.33 · 18 October 2026</p><h1>'+E(title)+'</h1>'+body+'</main><footer><p>Curated by '+link('https://www.antlerboy.com/','Benjamin P Taylor')+'. AI-assisted source intake. Linked works retain their authorship and terms; editorial comparisons remain open to challenge.</p><p>'+link('/#view=contribute','Suggest a correction')+'</p></footer><a id="openUpdates" href="https://github.com/antlerboy/the-necessary-tangle/issues/2" aria-label="Open updates"></a></body></html>\n'
    (dest/'index.html').write_text(text,encoding='utf-8')

body='<p>'+link(A['url'],'Open the Ashby Laboratory')+' to explore interactive adaptations of chapters 3–6 of W. Ross Ashby’s <em>An Introduction to Cybernetics</em> (1956). The application contains 56 exercises and 45 glossary entries. These four pathways help you choose a question and connect it to the atlas.</p><p>'+E(A['attribution'])+'</p><p class="note">'+E(A['navigation'])+'</p><div class="grid">'
for c in A['chapters']:
    body+='<article id="chapter-'+str(c['chapter'])+'"><p class="meta">Chapter '+str(c['chapter'])+' · '+str(c['exercises'])+' exercises</p><h2>'+E(c['title'])+'</h2><p>'+E(c['summary'])+'</p><p><strong>Try this question:</strong> '+E(c['question'])+'</p><p>'+link(A['url'],'Open the app and choose chapter '+str(c['chapter']))+'</p><p>Compare in the atlas: '+' · '.join(atlas(n) for n in c['atlas_ids'])+'</p><details><summary>Find the relevant exercises</summary><p>'+E(c['locator'])+'</p></details></article>'
body+='</div><section><h2>Read Ashby alongside the exercises</h2><p>'+link(A['book_url'],'An Introduction to Cybernetics: public archive PDF')+' · '+link(A['bibliography_url'],'Ashby bibliography')+' · '+atlas('person_w_ross_ashby')+'. The modern exercise wording and interface belong to the laboratory; the original book supplies a separate primary reading route.</p></section><section><h2>What has been checked</h2><p>'+E(A['scope'])+'</p><p>'+E(A['limits'])+'</p><p>'+E(A['rights'])+'</p><p>'+atlas(lab)+' · '+link('/reading/researcher-modules/','Compare the separately attributed Challoner researcher modules')+'</p></section>'
page('/reading/ashby-laboratory/','Ashby Laboratory: states, stability and learning from a black box',body)

body='<p>This bounded refresh accounts for all 27 published SysCoI posts returned for 8–18 October 2026. Twenty new reading leads are added to the atlas; seven announcements reuse existing resources. Discovery records identify material worth inspecting. They do not accept every linked claim.</p><p>'+link('/reading/ashby-laboratory/','Explore the Ashby Laboratory through four chapter pathways')+' · '+link('/events/','Current events and subscriptions')+'</p><section id="events"><h2>Events refreshed</h2><p>'+E(H['summary'])+'</p><p>'+link(H['new_event']['url'],H['new_event']['title'])+' — '+E(H['new_event']['display_time'])+'. '+link(H['workflow_url'],'Collection and publication evidence')+'.</p><p>Organisers remain authoritative. Source failures and stale records remain visible; missing listings are not treated as cancellations.</p></section><section id="recent"><h2>Recent SysCoI reading and announcements</h2>'
for p in P['posts']:
    body+='<article id="post-'+str(p['id'])+'" data-status="'+p['status']+'"><p class="meta">'+E(p['date'][:10])+' · '+('Already represented' if p['status']=='already_represented' else 'New discovery record')+'</p><h3>'+link(p['url'],p['title'])+'</h3><p>'+E(p['summary'])+'</p>'
    body+='<p>'+ (link(p['existing_route'],'Continue at the existing TNT route') if p['status']=='already_represented' else atlas('publication_syscoi_post_'+str(p['id'])))+'</p>'
    if p['atlas_ids']:body+='<p>Editorial comparisons: '+' · '.join(atlas(n) for n in p['atlas_ids'])+'</p>'
    if p['links']:body+='<details><summary>Original source links</summary><ul>'+''.join('<li>'+link(u,u)+'</li>' for u in p['links'])+'</ul></details>'
    body+='</article>'
body+='</section><section><h2>Attribution and remaining checks</h2><p>SysCoI is the discovery route. The original publications, organisers, artwork and tools retain their attribution. New graph connections document collection membership or the laboratory’s stated educational coverage; they do not infer intellectual influence. Linked claims, podcast arguments and research results need passage-level review before further claims are accepted.</p><p>'+link('syscoi-review.json','Download the SysCoI reconciliation')+' · '+link('ashby-review.json','Download the laboratory source account')+' · '+link('events-review.json','Download the event verification record')+'</p></section>'
page('/updates/2026-10-18/','Current events, recent SysCoI reading and the Ashby Laboratory',body)
for name in ['syscoi-review.json','ashby-review.json','events-review.json']:(D/'updates/2026-10-18'/name).write_bytes((S/name).read_bytes())
for path in ['learning/index.html','reading-list.html','updates/index.html']:
    p=D/path;t=p.read_text(encoding='utf-8');t=re.sub('<!-- '+MARK+' -->.*?<!-- /'+MARK+' -->','',t,flags=re.S)
    text='<section><h2>'+link('/updates/2026-10-18/','18 October: current events and recent reading')+'</h2><p>'+link('/reading/ashby-laboratory/','Ashby Laboratory: four pathways through 56 exercises')+' · 20 new SysCoI reading leads; seven announcements connected to existing resources.</p></section>'
    p.write_text(t.replace('</main>','<!-- '+MARK+' -->'+text+'<!-- /'+MARK+' --></main>',1),encoding='utf-8')
p=D/'index.html';t=p.read_text(encoding='utf-8');t=re.sub(r'<span id="releaseBadge">Release [^<]+</span>','<span id="releaseBadge">Release 0.33</span>',t,count=1)
t=re.sub(r'assets/public-data.js\?v=[^"\s]+','assets/public-data.js?v=0.33',t)
t=t.replace('href="/updates/2026-10-13/"','href="/updates/2026-10-18/"',1)
p.write_text(t,encoding='utf-8')
p=D/'sitemap.xml';t=p.read_text(encoding='utf-8')
for route in ['/reading/ashby-laboratory/','/updates/2026-10-18/']:
    url='https://transduction.systems'+route
    if url not in t:t=t.replace('</urlset>','<url><loc>'+url+'</loc><lastmod>'+DATE+'</lastmod></url></urlset>')
p.write_text(t,encoding='utf-8')
p=R/'README.md';t=p.read_text(encoding='utf-8');t=re.sub(r'<!-- current-31 -->.*?<!-- /current-31 -->','<!-- current-31 -->\nCurrent release: **0.33, 18 October 2026**. [Current events, recent SysCoI reading and the Ashby Laboratory](https://transduction.systems/updates/2026-10-18/). [Four Ashby Laboratory learning pathways](https://transduction.systems/reading/ashby-laboratory/).\n<!-- /current-31 -->',t,flags=re.S);p.write_text(t,encoding='utf-8')
p=R/'CITATION.cff';t=p.read_text(encoding='utf-8');t=re.sub(r'^version:.*$',"version: '0.33'",t,flags=re.M);t=re.sub(r'^date-released:.*$',"date-released: '2026-10-18'",t,flags=re.M);p.write_text(t,encoding='utf-8')
print('Applied 0.33: 20 new SysCoI leads, seven reused routes and one Ashby Laboratory tool with four reading pathways.')
