"""Connect the public library without turning catalogue matches into scholarly claims."""
from pathlib import Path
from apply_taylor_profile_26 import apply as apply_taylor_profile
from patch_library_navigation_26 import patch as patch_navigation
import hashlib,html,json,re
from apply_iteration_17 import enc,parse,upsert,source_record,node_record,edge_record,relation_record,merge_encoded
from apply_iteration_09 import graph_metrics,make_ai_observations
from apply_overnight_review import quality_result
from apply_doncaster_lineage import refresh_counts
from apply_relational_depth_16 import calculate_relational_depth,write_relational_document
from refresh_graph_snapshot import calculate,write
R=Path(__file__).resolve().parents[1];DATE='2026-09-19';MARK='library_20260919';URL='https://transduction.systems/library/';h=html.escape
def load(p):return json.loads((R/p).read_text(encoding='utf-8'))
def slug(s):return re.sub(r'[^a-z0-9]+','_',s.lower()).strip('_')
def main():
    packet=load('sources/library-2026-09-19/public-library.json');research=load('sources/library-2026-09-19/research-bibliography.json');data=load('data/public-data.json')
    records=json.loads(json.dumps(packet['records']+research['records']))
    nodes={n['id']:n for n in data['nodes']};sources={s['id']:s for s in data['sources']}
    # Existing named source records gain their now-public author PDFs.
    for update in packet['source_updates']:
        src=sources[update['id']];src.update(url=update['url'],access='public',public_link_status='public_link',source_type='public_teaching_material',last_checked=DATE,review_status='public_file_identity_checked',publisher='Benjamin P Taylor public work library',notes=re.sub(r' Public PDF linked on .*? superseded\.', '', src.get('notes','')).replace('Unpublished author teaching deck','Public author teaching deck').replace('Unpublished teaching presentation; no public link.','Public teaching presentation.').replace('Unpublished','Public')+' Public PDF linked on '+DATE+'; the earlier unpublished access description is superseded.')
    def newnode(nid,label,kind,description,sids,level='described'):
        if nid in nodes:
            if nodes[nid].get('inclusion_reason')==MARK:nodes[nid].update(label=label,description=description,canonical_definition=description,entity_type=kind)
            return nodes[nid]
        v=int(hashlib.sha256(nid.encode()).hexdigest()[:8],16)
        n=node_record(nid,label,kind,description,sids,(v%1000)/1000-.5,((v//1000)%1000)/1000-.5,['systems',MARK],level=level)
        n.update(inclusion_reason=MARK,status='candidate',review_status='source_scoped_ai_assisted',reviewed_by='',reviewed_at='',set_tags=enc(['systems',MARK]))
        upsert(data['nodes'],[n],'id');nodes[nid]=n;return n
    def source(sid,title,url,notes,kind='public_catalogue_record',authors=None):
        if sid in sources:return sid
        s=source_record(sid,title,kind,url,notes,authors or [],'Source publisher',DATE,quality='C')
        s.update(connection_pass=MARK,review_status='located_public_record',last_checked=DATE,creators=enc(authors or []))
        upsert(data['sources'],[s],'id');sources[sid]=s;return sid
    manifest_sid=source('src_antlerboy_manifest_20260919','Antlerboy public library manifest','https://antlerboy.com/library/manifest.json','Public catalogue membership and supplied descriptions, not proof of authorship of linked works.')
    corpus=newnode('corpus_antlerboy_public_library','Antlerboy public work library','corpus','A public collection of writing, teaching, recordings, tools, and community links maintained by Benjamin P Taylor. Linked materials retain their individual authorship and source terms.',[manifest_sid])
    types=[('catalogues_resource','documentary','is_catalogued_by','A specific item in the dated public catalogue','catalogues this public resource'),('teaching_account_of','teaching','has_teaching_account','A located teaching page that presents the named method','presents a teaching account of'),('source_text_mentions','documentary','is_mentioned_in_source','An exact phrase and page in the cited source; does not assert meaning or influence','contains a located mention of')]
    for typ,fam,inv,minimum,phrase in types:
        upsert(data['relation_types'],[relation_record(typ,fam,inv,minimum,phrase)],'relation_type')
    def edge(a,b,typ,fam,phrase,sids,loc,scope):
        eid='e26_'+hashlib.sha256((a+'|'+typ+'|'+b+'|'+loc).encode()).hexdigest()[:22]
        e=edge_record(eid,a,b,typ,fam,phrase,sids,loc,scope,status='candidate',confidence='',review_label='Located source statement; independent review not recorded')
        e.update(reviewed_by='',reviewed_at='',connection_pass=MARK);upsert(data['edges'],[e],'id')
    # Only direct public-library records enter the main atlas. Thousands of blog
    # records remain in the searchable source register with explicit discovery labels.
    current_labels={slug(n['label']):n['id'] for n in data['nodes'] if n.get('public_visibility')=='public' and n.get('inclusion_reason')!=MARK}
    by_url={s['url']:s['id'] for s in data['sources'] if s.get('url')}
    for item in records:
        if item['collection'] not in ['Antlerboy library','Large-group methods','Research bibliography']:continue
        if item['url'].startswith(URL):continue
        sid=by_url.get(item['url']) or 'src_'+item['id']
        source(sid,item['title'],item['url'],item.get('locator','Public catalogue')+'. '+item.get('review','Catalogue record')+'. '+packet['interpretation'],authors=item.get('authors',[]))
        if sources[sid].get('connection_pass')==MARK:sources[sid].update(year=str(item.get('year','')),publisher=item.get('publisher') or ('Benjamin P Taylor public work library' if item['collection']!='Research bibliography' else 'Publisher DOI record'))
        method=item.get('method');existing=item.get('canonical_target','')
        # Method identities explicitly reconciled in the evidence packet.
        if existing:
            n=nodes[existing];merge_encoded(n,'source_ids',[sid]);nid=existing
        else:
            nid=('method_lg26_'+method['id'].replace('-','_')) if method and method['collection']=='Overview' else 'resource_'+item['id']
            label=item['title'] if method and method['collection']=='Overview' else 'Public resource: '+item['title']
            if slug(label) in current_labels and current_labels[slug(label)]!=nid:
                # Separate editions/renditions remain distinguishable; do not silently
                # replace an existing canonical identity on a fuzzy title match.
                label+=' ('+(item.get('format') or 'catalogue record')+')'
                if slug(label) in current_labels and current_labels[slug(label)]!=nid:label+=' — additional edition'
            description=item['summary'] or 'A public catalogue entry in the Antlerboy library. Open the cited resource for its own content, authorship, and terms.'
            description+=' This record identifies the cited public resource; catalogue inclusion does not establish authorship or independent endorsement.'
            n=newnode(nid,label,'method_or_methodology' if method and method['collection']=='Overview' else ('publication' if item['collection']=='Research bibliography' else 'source'),description,[sid])
            current_labels[slug(label)]=nid
        item['atlas_id']=nid
        edge(corpus['id'],nid,'catalogues_resource','documentary','catalogues this public resource',[manifest_sid],item['title']+'; URL '+item['url'],'Catalogue membership only. This is not a conceptual dependency, influence claim, or authorship assertion.')
        for connection in item['connections']:
            if connection['kind']!='text_mention' or not connection.get('locator'):continue
            edge(nid,connection['target'],'source_text_mentions','documentary','contains a located mention of '+connection['term'],[sid],connection['locator'],'Exact phrase in extracted source text; page-level checking may remain pending as recorded by the locator. Its appearance may be in discussion, a quotation, a reference, or a critical comparison. No semantic or historical claim is inferred.')
    # The teaching deck explicitly presents these methods at the cited pages.
    deck=next(i for i in records if i['url']=='https://antlerboy.com/library/files/talks/large-group-processes.pdf')
    for item in records:
        method=item.get('method')
        if method and method['status']=='Teaching account' and item.get('atlas_id'):
            edge(deck['atlas_id'],item['atlas_id'],'teaching_account_of','teaching','presents a teaching account of', [next(s['id'] for s in data['sources'] if s.get('url')==deck['url'])], 'Large-group processes, PDF page '+str(method['page']),'Benjamin Taylor’s teaching account, not an assertion that he originated the method or that the source provides independent efficacy evidence.')
            deck['connections'].append(dict(target=item['atlas_id'],label=item['title'],kind='teaching_account',locator='Large-group processes, PDF page '+str(method['page']),pages=[method['page']],status='Located teaching account; independent review not recorded'))
    # Add a reader route from the existing systems-convening and VSM concepts.
    named=[('Systems convening and boundary work','practice_systems_convening','PDF pages 1–4'),('A simplification of the Viable System Model','method_or_methodology_viable_system_model_vsm','PDF pages 1–3'),('Viable System Model lecture','method_or_methodology_viable_system_model_vsm','PDF title and lecture'),('Better conversations for better realities','intervention_skill_productive_conversations','PDF title and teaching account')]
    for title,target,loc in named:
        item=next(i for i in records if i['title']==title and i.get('pages'))
        sid=next(s['id'] for s in data['sources'] if s.get('url')==item['url'])
        edge(item['atlas_id'],target,'teaching_account_of','teaching','presents a teaching account of',[sid],loc,'The linked public teaching source treats the named practice or model. The relation records teaching coverage, not origin, influence, or universal applicability.')
        item['connections'].append(dict(target=target,label=nodes[target]['label'],kind='teaching_account',locator=loc,status='Located public teaching account; independent review not recorded'))
    apply_taylor_profile(data,records,source,newnode,edge)
    # Recalculate source accessibility after the eight corrections, including old nodes.
    for node in data['nodes']:
        ss=[sources[s] for s in parse(node.get('source_ids')) if s in sources]
        node['public_source_count']=sum(s.get('public_link_status')=='public_link' for s in ss)
        node['no_public_link_count']=sum(s.get('public_link_status')!='public_link' for s in ss)
    packet['counts'].update(research_bibliographic_records=len(research['records']),source_register_records=len(records))
    data['library_integration']={k:packet[k] for k in ['release','date','scope','authorship','interpretation','counts','research_collection']}
    data['library_integration']['url']=URL
    concepts={}
    for record in records:
        for target in {c['target'] for c in record['connections']}:concepts[target]=concepts.get(target,0)+1
    data['library_integration']['concept_counts']=concepts
    introduced={n['id'] for n in data['nodes'] if n.get('inclusion_reason')==MARK}
    linked={e[end] for e in data['edges'] if e.get('connection_pass')==MARK for end in ['source','target']}
    data['library_integration']['impact']={'new_entries':len(introduced),'existing_entries_with_new_graph_connections':len(linked-introduced),'entries_with_source_register_routes':len(concepts),'new_graph_statements':sum(e.get('connection_pass')==MARK for e in data['edges'])}
    refresh_counts(data);data['meta'].update(release='0.26',generated=DATE,release_digest_url=URL,iteration_focus='Public library, training, and source-to-concept connections',release_note='Public Antlerboy resources and teaching methods are connected to the atlas. Catalogue, text-location, and teaching relations retain separate evidence meanings.',node_count=len(data['nodes']),edge_count=len(data['edges']),source_count=len(data['sources']),profile_count=len(data['profiles']))
    data['relational_depth']=calculate_relational_depth(data);data['relational_depth'].update(release='0.26',generated=DATE);data['graph_snapshot']=calculate(data);metrics=graph_metrics(data);depth=data['relational_depth']['aggregate']
    data['meta'].update(public_entry_count=metrics['public_entries'],described_entry_count=metrics['public_entries'],reader_connected_entry_count=depth['reader_connected_entries'],semantic_connected_entry_count=depth['semantic_connected_entries'],unconnected_entry_count=depth['connection_bands'].get('unconnected',0),semantic_gap_entry_count=metrics['public_entries']-depth['semantic_connected_entries'],public_link_source_count=sum(s.get('public_link_status')=='public_link' for s in data['sources']),no_public_link_source_count=sum(s.get('public_link_status')=='no_public_link' for s in data['sources']))
    for band in ['rich','developing','thin']:data['meta'][band+'_entry_count']=depth['connection_bands'].get(band,0)
    for k in ['reading_list_inventory','reading_list_coverage','core_systems_practice']:data[k]['release']='0.26'
    data['ai_observations'].update(release='0.26',generated=DATE,metrics=metrics);upsert(data['ai_observations']['observations'],make_ai_observations(metrics)['observations'],'id');write(data)
    quality=quality_result(data);quality.update(release='0.26',generated=DATE)
    for k in ['adversarial_review','doncaster_lineage_review']:quality[k]=data[k]
    for name in ['data/relationship-quality.json','docs/assets/relationship-quality.json']:(R/name).write_text(json.dumps(quality,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    write_relational_document(data)
    public=dict(release='0.26',date=DATE,counts=packet['counts'],interpretation=packet['interpretation'],authorship=packet['authorship'],research_collection=packet['research_collection'],records=records)
    out=R/'docs/library';out.mkdir(exist_ok=True);(out/'catalogue.json').write_text(json.dumps(public,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8',newline='\n')
    for file in ['index.html','library.css','library.js']:(out/file).write_text((R/'sources/library-2026-09-19'/file).read_text(encoding='utf-8'),encoding='utf-8',newline='\n')
    for name in ['docs/index.html','docs/reading-list.html','docs/updates/index.html']:
        p=R/name;s=p.read_text(encoding='utf-8');s=re.sub(r'<!-- library-26 -->.*?<!-- /library-26 -->','',s,flags=re.S)
        section='<section class="library-source-route"><h2><a href="/library/">Sources, teaching, and concept connections</a></h2><p>Search the public Antlerboy library, Chosen Path, SysCoi, and the developing research bibliography. Follow located source passages into the atlas.</p></section>'
        anchor='</main>'
        if anchor not in s:raise ValueError('Missing main landmark: '+name)
        s=s.replace(anchor,'<!-- library-26 -->'+section+'<!-- /library-26 -->'+anchor,1);p.write_text(s,encoding='utf-8',newline='\n')
    p=R/'docs/index.html';s=p.read_text(encoding='utf-8')
    s=re.sub(r'(<span id="releaseBadge">)Release [^<]+',r'\g<1>Release 0.26',s)
    if 'data-library-nav' not in s:s=s.replace('<nav class="main-nav" aria-label="Main navigation">','<nav class="main-nav" aria-label="Main navigation"><a data-library-nav class="static-nav-link" href="/library/">Sources</a>',1)
    p.write_text(s,encoding='utf-8',newline='\n')
    p=R/'docs/assets/app.js';s=patch_navigation(p.read_text(encoding='utf-8'))
    s=re.sub(r'    // library-source-links-start.*?    // library-source-links-end\n','',s,flags=re.S)
    anchor='    const sections = [];'
    if anchor not in s:raise ValueError('Entry section insertion point missing')
    s=s.replace(anchor,anchor+'\n'+'''    // library-source-links-start
    const sourceRegisterCount = DATA.library_integration?.concept_counts?.[node.id] || 0;
    if (sourceRegisterCount) sections.push(`<section class="entry-section source-register-route"><h2>Sources and teaching</h2><p><a href="/library/?concept=${encodeURIComponent(node.id)}">Explore ${sourceRegisterCount} source records connected to this entry</a>. Each result distinguishes title-page credit, a teaching account, an identity link, a located text mention, and an automatic title match.</p></section>`);
    // library-source-links-end
''',1)
    p.write_text(s,encoding='utf-8',newline='\n')
    p=R/'docs/sitemap.xml';s=p.read_text(encoding='utf-8')
    if URL not in s:s=s.replace('</urlset>','<url><loc>'+URL+'</loc><lastmod>'+DATE+'</lastmod></url></urlset>')
    p.write_text(s,encoding='utf-8',newline='\n')
    note='Release 0.26 connects '+str(packet['counts']['antlerboy_manifest_resources'])+' public-library resource records, '+str(packet['counts']['large_group_entries'])+' large-group entries, and eight now-public teaching-source URLs. The source register also includes Chosen Path and SysCoi post metadata, with automated discovery matches explicitly separated from located teaching claims. The private research inventory contains 2,943 indexed records; public bibliographic reconciliation is tracked separately. Current atlas: '+str(metrics['public_entries'])+' public entries, '+str(len(data['nodes']))+' nodes, '+str(len(data['edges']))+' statements, and '+str(len(data['sources']))+' sources. No independent specialist review is claimed. See '+URL+'.'
    for filename,heading in [('README.md','## Release 0.26'),('CHANGELOG.md','## 0.26 - 19 September 2026'),('documentation/TANGLE_STATE.md','## Library integration, 19 September 2026')]:
        p=R/filename;s=p.read_text(encoding='utf-8');s=re.sub(re.escape(heading)+r'\n.*?(?=\n## |\Z)','',s,flags=re.S);s=s.rstrip()+'\n\n'+heading+'\n\n'+note+'\n';p.write_text(s,encoding='utf-8',newline='\n')
    p=R/'CITATION.cff';s=p.read_text(encoding='utf-8');s=re.sub(r'^version:.*$','version: 0.26',s,flags=re.M);p.write_text(s,encoding='utf-8',newline='\n')
    print('Applied release 0.26:',len(records),'source records;',metrics['public_entries'],'public atlas entries')
if __name__=='__main__':main()
