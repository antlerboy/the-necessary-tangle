#!/usr/bin/env python3
"""Add source-labelled practice resources after the preserved 0.22 release gate."""
from __future__ import annotations
import hashlib
import html
import json
import re
from pathlib import Path
from build_practice_pack import load_content, URL, DATE, DEST
from apply_iteration_17 import enc, parse, upsert, source_record, node_record, profile_record, relation_record, edge_record
from apply_iteration_09 import graph_metrics, make_ai_observations
from apply_relational_depth_16 import calculate_relational_depth, write_relational_document
from apply_overnight_review import quality_result
from apply_doncaster_lineage import refresh_counts
from refresh_graph_snapshot import calculate, write

ROOT=Path(__file__).resolve().parents[1]
RELEASE='0.23-systems-methods-practice-alpha'
HUB='practice_systems_methods_pack'
PREFIX='practice_lab_'


def norm(s):
    return re.sub(r'[^a-z0-9]+',' ',str(s).casefold()).strip()


def match_nodes(data, labels):
    redirects=data.get('canonical_redirects',{})
    found=[]
    for label in labels:
        q=norm(label)
        exact=[]
        partial=[]
        for node in data['nodes']:
            if node['id'].startswith(PREFIX) or node['id']==HUB or node.get('public_visibility')!='public' or redirects.get(node['id'],node['id'])!=node['id']:
                continue
            names=[node['label'],*parse(node.get('aliases'))]
            if any(norm(name)==q for name in names):exact.append(node['id'])
            elif len(q)>12 and node.get('entity_type') not in ['person','publication','institution'] and q in norm(node['label']):partial.append(node['id'])
        found.extend(exact or (partial if len(partial)==1 else []))
    return list(dict.fromkeys(found))


def source(identity,title,url,notes):
    row=source_record(identity,title,'practice_resource',url,notes,['The Necessary Tangle editorial practice pack'],'The Necessary Tangle',DATE)
    row.update(last_checked=DATE,review_status='original_material_and_source_boundary_recorded',licence='Original practice text CC BY-SA 4.0; external material retains source terms')
    return row


def add_profile(data,identity,title,description,url,sids,practice,limits):
    n=node_record(identity,title,'publication',description,sids,0.38,0.34,['practice','learning','apprenticeship'],level='profile')
    n.update(status='candidate',review_status='original_practice_material_specialist_review_not_recorded',reviewed_by='',reviewed_at='',inclusion_reason='authorised_systems_methods_practice_pack',set_tags=enc(['systems','practice','learning','apprenticeship']),external_ids=enc({'practice_url':url}))
    upsert(data['nodes'],[n],'id')
    p=profile_record(identity,description,'A concrete rehearsal with a fictional case, explicit outputs and a way to inspect the result.',['Mechanical correctness is distinct from judgement in an open situation.','Training-case application is distinct from competent organisational practice.'],[],[],[],practice,['A worked comparison is not the only acceptable answer to an open question.'],limits,sids,context='Original educational resource, 7 September 2026.',editorial_note='Prepared with AI assistance. Publication authorised by Benjamin P Taylor. No independent specialist review or source-provider endorsement is claimed.')
    p.update(title=title,last_researched=DATE,profile_status='original_practice_resource',review_status='specialist_review_not_recorded')
    upsert(data['profiles'],[p],'node_id')


def edge(data,source_id,target,kind,sid,scope):
    identity='practice_edge_'+hashlib.sha256((source_id+'|'+target+'|'+kind).encode()).hexdigest()[:18]
    row=edge_record(identity,source_id,target,kind,'practice','provides a practice route for' if kind=='provides_practice_for' else 'includes practice resource',[sid],'Named exercise and its scope statement',scope,status='candidate',mode='asserted',confidence='',review_label='Editorial practice connection, not accreditation or intellectual influence')
    row.update(reviewed_by='',reviewed_at='')
    upsert(data['edges'],[row],'id')


def main():
    labs,resources,standards=load_content()
    data=json.loads((ROOT/'data/public-data.json').read_text())
    for row in [relation_record('provides_practice_for','practice','has_practice_resource','Named practice task and an explicit scope statement','provides a practice route for'),relation_record('includes_practice_resource','practice','included_in_practice_pack','Direct resource inventory','includes practice resource')]:
        upsert(data['relation_types'],[row],'relation_type')
    external={}
    for rid,res in resources.items():
        existing=next((s for s in data['sources'] if s.get('url')==res['url']),None)
        if existing:external[rid]=existing['id'];continue
        sid='src_practice_external_'+rid.replace('-','_')
        s=source(sid,res['title'],res['url'],res['check']+' Use: '+res['use'])
        s.update(source_type='public_learning_resource',publisher=res['url'].split('/')[2],creators=enc([]),licence='External source terms; linked, not reproduced',review_status='specific_access_and_content_limit_recorded')
        upsert(data['sources'],[s],'id');external[rid]=sid
    hubs='src_systems_methods_practice_pack'
    upsert(data['sources'],[source(hubs,'Systems methods practice: cases and checks',URL,'Original cases, checks, worked comparisons, resource register and editorial standards crosswalk. No accreditation or provider endorsement.')],'id')
    desc='A free collection of 26 original systems-method practice pages, with fictional scenarios, modelling tasks, worked comparisons, error-repair exercises and changed cases. It maps all thirteen approaches and three theory rows in the public SCiO portfolio, plus ten supporting areas, with explicit limits on depth and assessment.'
    add_profile(data,HUB,'Systems methods practice pack',desc,URL,[hubs,external['scio-portfolio'],external['st0787']],['Choose a method, make a model, compare the reasoning, repair it and try the changed case.','Open the free practice pages and the resource register through the linked source.'],['Independent specialist pedagogical review remains open.','Organisational competence and behaviours require real-world evidence.'])
    bynode={}
    mappings=[]
    for lab in labs:
        identity=PREFIX+lab['id'].replace('-','_');sid='src_'+identity;url=URL+lab['id']+'/'
        upsert(data['sources'],[source(sid,lab['title'],url,'Original fictional exercise. '+lab['scope'])],'id')
        sids=list(dict.fromkeys([sid,*[external[x] for x in lab['resources']+lab['paid']]]))
        add_profile(data,identity,'Practice: '+lab['title'],lab['focus']+' '+lab['scope'],url,sids,[step['task'] for step in lab['rounds']],[lab['scope'],'Compare an independent attempt before revealing the worked answer.'])
        edge(data,HUB,identity,'includes_practice_resource',hubs,'Resource inventory only; completing a page is not accreditation.')
        matches=match_nodes(data,lab['atlas'])
        for target in matches:
            edge(data,identity,target,'provides_practice_for',sid,lab['scope'])
            bynode.setdefault(target,[]).append({'id':lab['id'],'title':lab['title'],'url':url})
        bynode[identity]=[{'id':lab['id'],'title':lab['title'],'url':url}]
        mappings.append({'lab_id':lab['id'],'resource_node_id':identity,'method_node_ids':matches,'scope':lab['scope']})
    spine='practice_core_systems_practice_spine'
    if any(n['id']==spine for n in data['nodes']):
        edge(data,HUB,spine,'provides_practice_for',hubs,'Basic case rehearsal complements the existing practice and reading spine; not a substitute for organisational application.')
        bynode[spine]=[{'id':'pack','title':'Open the complete systems methods practice pack','url':URL}]
    bynode[HUB]=[{'id':'pack','title':'Open the free practice pages','url':URL}]
    data['practice_pack']={'version':'1.0','published':DATE,'url':URL,'lab_count':len(labs),'resource_count':len(resources),'core_approach_count':len(standards['core_order']),'theory_row_count':len(standards['theory_order']),'mapping_status':standards['crosswalk_status'],'mappings':mappings,'by_node':bynode}
    data['core_systems_practice']['practice_pack_url']=URL
    refresh_counts(data)
    metrics=graph_metrics(data)
    data['relational_depth']=calculate_relational_depth(data)
    data['relational_depth'].update(release=RELEASE,generated=DATE)
    data['graph_snapshot']=calculate(data)
    meta=data['meta']
    meta.update(release=RELEASE,generated=DATE,iteration_focus='basic systems-method rehearsal and standards crosswalk',practice_pack_url=URL,practice_lab_count=len(labs),node_count=len(data['nodes']),edge_count=len(data['edges']),source_count=len(data['sources']),profile_count=len(data['profiles']),journey_count=len(data['journeys']),public_entry_count=metrics['public_entries'],described_entry_count=metrics['public_entries'],release_note='26 free original practice pages, source-labelled external and paid routes, and explicit SCiO/ST0787 practice mapping.',release_digest_url='https://transduction.systems/updates/0.23/')
    depth=data['relational_depth']['aggregate']
    meta.update(reader_connected_entry_count=depth['reader_connected_entries'],semantic_connected_entry_count=depth['semantic_connected_entries'],unconnected_entry_count=depth['connection_bands'].get('unconnected',0),semantic_gap_entry_count=metrics['public_entries']-depth['semantic_connected_entries'],public_link_source_count=sum(s.get('public_link_status')=='public_link' for s in data['sources']),no_public_link_source_count=sum(s.get('public_link_status')=='no_public_link' for s in data['sources']))
    for band in ['rich','developing','thin']:meta[band+'_entry_count']=depth['connection_bands'].get(band,0)
    for key in ['reading_list_inventory','reading_list_coverage','core_systems_practice']:data[key]['release']=RELEASE
    obs=data['ai_observations'];obs.update(release=RELEASE,generated=DATE,metrics=metrics)
    upsert(obs['observations'],make_ai_observations(metrics)['observations'],'id')
    upsert(obs['observations'],[{'id':'practice_and_accreditation_are_different','title':'A checkable exercise is not accreditation','kind':'editorial practice boundary','measurement':'26 original practice pages cover every core approach and theory row in the inspected public SCiO portfolio, with different depth limits.','interpretation':'Mechanical model checks can expose errors without establishing competence in organisational application.','implication':'Preserve attempts, revisions, scope limits and the need for observed practice.','test':'Can a learner distinguish a case check from a professional assessment?'}],'id')
    write(data)
    quality=quality_result(data);quality.update(release=RELEASE,generated=DATE)
    for key in ['adversarial_review','doncaster_lineage_review']:quality[key]=data[key]
    for p in ['data/relationship-quality.json','docs/assets/relationship-quality.json']:(ROOT/p).write_text(json.dumps(quality,ensure_ascii=False,indent=2)+'\n')
    write_relational_document(data)
    (ROOT/'docs/assets/practice-links.js').write_text('window.TANGLE_PRACTICE_LINKS = '+json.dumps(bynode,ensure_ascii=False,separators=(',',':'))+';\n')
    (DEST/'assets/atlas-mapping.json').write_text(json.dumps(mappings,ensure_ascii=False,indent=2)+'\n')
    cite=ROOT/'CITATION.cff';text=cite.read_text();text=re.sub(r'^version:.*$',f'version: {RELEASE}',text,flags=re.M);text=re.sub(r'^date-released:.*$',f'date-released: {DATE}',text,flags=re.M);cite.write_text(text)
    summary=f'26 original practice pages; {len(resources)} source-labelled resource routes; {metrics["public_entries"]} public atlas entries after the additive resource integration. All 13 core approaches and three theory rows have an explicit rehearsal, with depth limits. Ten further pages support systemic inquiry and intervention.'
    note='\n\n## Systems methods practice, 7 September 2026\n\n'+summary+'\n\nPublished route: '+URL+'\n\nPublication is explicitly authorised. See `sources/practice-pack/PACKET.md`, the public coverage page and `documentation/practice-pack.md`. No independent specialist pedagogical review is recorded; this remains an open review task. Existing unrelated work below or above remains open.\n'
    for name in ['documentation/TANGLE_STATE.md','documentation/NEXT_WORK.md','documentation/scio-coverage.md','documentation/feedback-ledger.md']:
        p=ROOT/name;text=p.read_text();heading='## Systems methods practice, 7 September 2026'
        if heading not in text:p.write_text(text.rstrip()+note)
    readme=ROOT/'README.md';text=readme.read_text()
    if '## Release 0.23' not in text:text=text.replace('# The Necessary Tangle\n','# The Necessary Tangle\n\n## Release 0.23\n\n'+summary+' [Open the practice pack]('+URL+'). The previous release accounts remain below as history.\n',1)
    readme.write_text(text)
    changelog=ROOT/'CHANGELOG.md';text=changelog.read_text()
    if '## 0.23' not in text:changelog.write_text(text.rstrip()+'\n\n## 0.23 - 7 September 2026\n\n'+summary+'\n')
    lines=['# AI observations','',f'Generated for release {RELEASE} on {DATE}.','']
    for o in obs['observations']:
        lines+=['## '+o.get('title','Observation'),'']
        for key in ['kind','measurement','interpretation','implication','test']:lines += [key.capitalize()+': '+o.get(key,''),'']
    (ROOT/'documentation/ai-observations.md').write_text('\n'.join(lines))
    (ROOT/'documentation/practice-pack.md').write_text('# Systems methods practice pack\n\n'+summary+'\n\n## Scope and evidence\n\n'+standards['crosswalk_status']+'\n\nSource content lives in `sources/practice-pack`. The renderer is `scripts/build_practice_pack.py`; the atlas integration is `scripts/apply_practice_pack.py`. Tests and browser checks must pass before publication. A passing build is not a specialist pedagogical review.\n\n## Original material and external sources\n\nAll scenarios and comparisons are original and fictional. External records distinguish actual exercises from page descriptions, recordings, books and uncertain access. No paid course was purchased or validated. The OU defective-map case and MIT assignment/solution pairs are the strongest direct free practice routes. Ackoff\'s linked attachment returned 404 and is labelled accordingly.\n\n## Continued review\n\nAsk a method specialist and learners to test the questions and alternative models. Review the theory-row depth, the explicitly partial INFORMED and Syntegration rehearsals, and the transfer from individual exercises to group work. Do not close unrelated existing work on the basis of this publication.\n')
    print('Applied practice resource overlay:',summary)
    print('Core lab mappings:',json.dumps({x['lab_id']:x['method_node_ids'] for x in mappings if x['lab_id'] in standards['core_order']}))


if __name__=='__main__':main()
