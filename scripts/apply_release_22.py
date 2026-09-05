#!/usr/bin/env python3
"""Reproducible early-cybernetics intake, readable routes, and release 0.22."""
from __future__ import annotations
import html
import json
import re
from pathlib import Path
from collections import Counter
from apply_iteration_17 import enc, parse, upsert, source_record, node_record, profile_record, edge_record, relation_record
from apply_iteration_09 import graph_metrics, make_ai_observations
from apply_relational_depth_16 import calculate_relational_depth
from refresh_graph_snapshot import calculate, write
from apply_doncaster_lineage import refresh_counts
from apply_overnight_review import quality_result
from apply_relational_depth_16 import write_relational_document

ROOT=Path(__file__).resolve().parents[1]
RELEASE='0.22'
DATE='2026-09-05'
ASSETS=ROOT/'docs/assets'
INTAKE=ROOT/'sources/cybernetics-bibliographies/intake.json'
W='src_wiener_reading_lists_2026'
B='src_barrett_shepard_intro_1951'
F='src_fano_tr65_1949'
A='src_ashby_design_brain_1952'
S='src_shannon_weaver_book_1949'
T='src_wiener_too_damn_close_1950'


def slug(s):return re.sub('[^a-z0-9]+','_',s.lower()).strip('_')
def jwrite(path,value):path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def esc(s):return html.escape(str(s),quote=True)
def route(n):return '/#view=item&id='+n+'&from=home'


def node(data,nid,label,kind,description,sources,aliases=None,level='described'):
    rows=data['nodes']; redirects=data.get('canonical_redirects',{})
    # Match type as well as label: Cybernetics the book is not Cybernetics the tradition.
    matching=next((n for n in rows if n['entity_type']==kind and (n['id']==nid or n['label'].casefold()==label.casefold() or label.casefold() in [str(a).casefold() for a in parse(n.get('aliases'))])),None)
    if matching:
        nid=redirects.get(matching['id'],matching['id']); matching=next(n for n in rows if n['id']==nid)
        matching['source_ids']=enc(list(dict.fromkeys(parse(matching.get('source_ids'))+sources)))
        matching['aliases']=enc(list(dict.fromkeys(parse(matching.get('aliases'))+(aliases or []))))
        return nid
    n=node_record(nid,label,kind,description,sources,0.1,0.1,['cybernetics','history'],aliases=aliases,level=level)
    n.update(inclusion_reason='early_cybernetics_bibliographic_intake_0_22',status='candidate',review_status='research_pass_needs_editor',reviewed_by='',reviewed_at='',set_tags=enc(['cybernetics','history','release_0_22']))
    rows.append(n);return nid


def link(data,source,target,relation,family,phrase,sources,locator,scope,mode='asserted'):
    # Retain a prior, evidence-bearing assertion instead of duplicating its triple.
    if any(e['source']==source and e['target']==target and e['relation_type']==relation and not e['id'].startswith('e22_') for e in data['edges']):
        return
    e=edge_record('e22_'+slug(source+'_'+relation+'_'+target),source,target,relation,family,phrase,sources,locator,scope,status='candidate',mode=mode,confidence='',review_label='Source located; curator review pending' if mode=='asserted' else 'Interpretive connection; curator review pending')
    e.update(reviewed_by='',reviewed_at='',evidence_ids='[]')
    upsert(data['edges'],[e],'id')


def profile(data,nid,summary,why,distinctions,practice,sources,locator,checks=None):
    p=profile_record(nid,summary,why,distinctions,[],[],[],practice,[],checks or ['Extend the evidence pass beyond the cited passages.'],sources,context=locator,editorial_note='Source passages inspected for this account. Practice questions are editorial applications. Curator review pending.')
    p.update(title=next(n['label'] for n in data['nodes'] if n['id']==nid),last_researched=DATE,profile_status='evidence_deepened_research_pass',review_status='research_pass_needs_editor')
    upsert(data['profiles'],[p],'node_id')
    n=next(n for n in data['nodes'] if n['id']==nid);n.update(publication_level='profile',description=summary,canonical_definition=summary,public_stub_text='')


def sources(data,intake):
    items=[
      source_record(W,intake['posts'][0]['title'],'historical_bibliography_transcription',intake['posts'][0]['url'],'Three historical lists shared by Sean Manion, @TheUnjournaling, transcribed by Systems Community of Inquiry. Records inclusion and bibliographic wording; it does not prove influence or full-text review. The reported 1956 list contains a 1957 item.',['Norbert Wiener'],'Systems Community of Inquiry',DATE,quality='B'),
      source_record(B,'A Bibliography of Cybernetics — introduction','historical_bibliography_transcription',intake['posts'][1]['url'],'F. Dermot Barrett and Herbert A. Shepard, MIT, 1951 as reported by the source. Shared by Sean Manion, @TheUnjournaling. Only the three-page introduction is available in this transcription; the bibliography pages are missing.',['F. Dermot Barrett','Herbert A. Shepard'],'Systems Community of Inquiry','1951',quality='B'),
      source_record(F,'The Transmission of Information, Technical Report No. 65','primary_research_report','https://hcs64.com/files/fano-tr65-ocr.pdf','Primary report inspected: title page, abstract, introduction, and sections I–III. 17 March 1949. Public mirror of the MIT report. TR 149 is mentioned by the reading list but was not inspected.',['Robert M. Fano'],'MIT Research Laboratory of Electronics','1949-03-17'),
      source_record(A,'Design for a Brain — 1954 corrected reprint of the 1952 edition','primary_book','https://ia801406.us.archive.org/18/items/designforbrain00ashb/designforbrain00ashb.pdf','Inspected title/edition pages, preface, section 3/14, and sections 8/4–8/7. Chapter numbering refers to this early edition. This is not a claim to have reviewed the whole book.',['W. Ross Ashby'],'John Wiley & Sons','1952; reprint 1954'),
      source_record(S,'The Mathematical Theory of Communication — 1949 volume','primary_book','https://ia801403.us.archive.org/25/items/in.ernet.dli.2015.503815/2015.503815.The-Mathematical_text.pdf','Inspected preface, contents, Shannon introduction pp. 3–5, and Weaver pp. 95–99. The volume contains separately attributed papers, with distinct technical and wider questions.',['Claude E. Shannon','Warren Weaver'],'University of Illinois Press','1949'),
      source_record(T,'Too Damn Close','primary_article','https://www.theatlantic.com/magazine/archive/1950/07/too-damn-close/639607/','Publisher’s complete historical text inspected, sections 1 and 2. Historical political arguments and estimates are not presented as current facts.',['Norbert Wiener'],'The Atlantic','1950-07'),
      source_record('src_ashby_archive_equilibrium','W. Ross Ashby Digital Archive — bibliography','author_archive','https://ashby.info/bibliography.html','Checks the expanded 1946 title Dynamics of the Cerebral Cortex: The Behavioral Properties of Systems in Equilibrium, American Journal of Psychology 59(4), 682–686. Metadata review only.',['W. Ross Ashby Digital Archive'],'W. Ross Ashby Digital Archive',DATE,quality='B'),
      source_record('src_illinois_shannon_weaver','The Mathematical Theory of Communication — publisher record','publisher_record','https://www.press.uillinois.edu/books/?id=p725487','Publisher metadata and author information; distinguishes the later paperback listing from the original 1949 volume.',['University of Illinois Press'],'University of Illinois Press',DATE,quality='B')]
    for s in items:s.update(last_checked=DATE,review_status='passage_checked' if s['id'] in [F,A,S,T] else 'bibliographic_or_source_boundary_checked')
    upsert(data['sources'],items,'id')


def enrich(data,intake):
    sources(data,intake)
    for r in [
      relation_record('listed_in_bibliography','documentary','lists_work','An exact entry in the cited bibliography','is listed in'),
      relation_record('edited_by','documentary','edited','A title page or explicit bibliographic editor credit','is edited by'),
      relation_record('presents_account_of','conceptual','account_presented_in','Located passage of the publication','presents an account of'),
      relation_record('reprints_work','documentary','reprinted_in','Publisher or volume preface identifying the reprint','reprints'),
      relation_record('distinguishes_from','conceptual','distinguished_from_by','A located distinction, or an explicitly labelled interpretation','distinguishes from'),
      relation_record('discusses_in_introduction','documentary','discussed_in_introduction_of','An explicit mention in the introduction','discusses in its introduction')]:upsert(data['relation_types'],[r],'relation_type')
    collections={}
    for sec in intake['sections']:
        collections[sec['id']]=node(data,'bibliography_wiener_'+slug(sec['id']),sec['title']+' — Wiener','comparator_corpus','A historical reading-list section retained with its individual entries, original wording, and unresolved bibliographic details. Inclusion records selection; it does not establish intellectual influence.',[W])
    barrett=node(data,'bibliography_barrett_shepard_1951','A Bibliography of Cybernetics (Barrett and Shepard, 1951)','comparator_corpus','A bibliography framed for social scientists. The available introduction names six sections and explains their selection boundary. Its bibliography pages are not present in the supplied transcription.',[B],['Barrett and Shephard bibliography','Barrett–Shepard bibliography'])
    for author in ['F. Dermot Barrett','Herbert A. Shepard']:
        pid=node(data,'person_'+slug(author),author,'person','Co-compiler of A Bibliography of Cybernetics, identified as affiliated with MIT in the transcribed introduction. No broader biographical or intellectual lineage is inferred from this credit.',[B])
        link(data,barrett,pid,'authored_by','documentary','is compiled by',[B],'Title and byline','Compiler credit only; biographical research remains open.')
    existing={'weaver-complexity':'publication_fpcs_010'}
    work_ids={};new_count=0
    for row in intake['entries']:
        key=row['work_key']; row['source_url']=intake['posts'][0]['url'];row['review_status']='bibliographic_entry_transcribed';row['full_text_reviewed']=False
        if key=='current-biography':row.update(node_id=None,reconciliation='unresolved_reference');continue
        requested=existing.get(key,'publication_early_'+slug(key))
        description=f"{row['title']}. Listed in Wiener’s historical cybernetics reading material; the supplied citation gives {row['date_as_listed']}. This entry records the work and its bibliographic context. The full text has not been assessed in this intake."
        before={n['id'] for n in data['nodes']}
        label = 'Information Theory (Goldman)' if key == 'goldman-information' else row['title']
        wid=node(data,requested,label,'publication',description,[W],level='described')
        work_ids[key]=wid
        row.update(node_id=wid,reconciliation='existing_atlas_work' if key in existing else 'reconciled_work')
        link(data,wid,collections[row['section']],'listed_in_bibliography','documentary','is listed in',[W],intake['sections'][[s['id'] for s in intake['sections']].index(row['section'])]['title']+'; '+row['transcribed_entry'],'Bibliographic selection only. No influence, endorsement, or full-text coverage is implied.')
        for author in row['authors']:
            pid=node(data,'person_early_'+slug(author),author,'person',f'Named in the historical reading list as an author or editor of {row["title"]}. The record provides a bibliographic route; a fuller biography remains to be researched.',[W],level='described')
            rel='edited_by' if key in ['macy-seventh','locke-booth-translation'] else 'authored_by'
            # The list explicitly labels von Foerster as editor; Locke/Booth roles await title-page review.
            if key=='locke-booth-translation':rel='authored_by'
            link(data,wid,pid,rel,'documentary','is edited by' if rel=='edited_by' else 'credits',[W],row['transcribed_entry'],'Bibliographic attribution as listed; a credit is not an influence claim.')
    for row in intake['entries']:
        if row['work_key']=='ashby-equilibrium':
            row['notes'].append('Ashby’s archive supplies the fuller title: Dynamics of the Cerebral Cortex: The Behavioral Properties of Systems in Equilibrium. Original citation retained.') if not any('fuller title' in n for n in row['notes']) else None
            row['review_status']='metadata_checked';row['primary_url']='https://ashby.info/bibliography.html'
    primary={'fano-transmission':(F,'https://hcs64.com/files/fano-tr65-ocr.pdf','TR 65: abstract, introduction, and sections I–III; TR 149 not inspected'), 'ashby-brain':(A,'https://ia801406.us.archive.org/18/items/designforbrain00ashb/designforbrain00ashb.pdf','1954 corrected reprint: preface, 3/14, 8/4–8/7'), 'shannon-weaver-book':(S,'https://ia801403.us.archive.org/25/items/in.ernet.dli.2015.503815/2015.503815.The-Mathematical_text.pdf','1949 preface; Shannon pp. 3–5; Weaver pp. 95–99'), 'wiener-close':(T,'https://www.theatlantic.com/magazine/archive/1950/07/too-damn-close/639607/','Sections 1 and 2')}
    for row in intake['entries']:
        if row['work_key'] in primary:
            sid,url,loc=primary[row['work_key']];row.update(review_status='selected_passages_reviewed',primary_url=url,review_locator=loc)
            n=next(n for n in data['nodes'] if n['id']==row['node_id']);n['source_ids']=enc(list(dict.fromkeys(parse(n['source_ids'])+[sid])))
    for item in intake['barrett_shepard_named_works']:
        wid=node(data,'publication_early_'+slug(item['title']),item['title'],'publication',item['role'],[B])
        pid=node(data,'person_early_'+slug(item['author']),item['author'],'person','Author identified through the work discussed in the Barrett–Shepard introduction. This bibliographic connection is distinct from membership in a cybernetics school.',[B])
        item.update(node_id=wid)
        link(data,barrett,wid,'discusses_in_introduction','documentary','discusses in its introduction',[B],'Introduction, page 3, final paragraph','Preserves the compilers’ unequal assessments of the two works.')
        link(data,wid,pid,'authored_by','documentary','credits',[B],'Introduction, page 3, final paragraph','Authorship identification only.')
    for n in data['nodes']:
        if n['id']==work_ids['ashby-equilibrium']:
            n['aliases']=enc(list(dict.fromkeys(parse(n['aliases'])+['Dynamics of the Cerebral Cortex: The Behavioral Properties of Systems in Equilibrium'])))
            n['source_ids']=enc(list(dict.fromkeys(parse(n['source_ids'])+['src_ashby_archive_equilibrium'])))
    # Readable, located accounts. Practice questions below are editorial applications.
    defs=[
      ('concept_communication_levels','Technical, semantic, and effectiveness questions','Weaver separates accurate transmission, intended meaning, and effects on conduct. Shannon’s engineering problem brackets semantics.','A message can arrive accurately and still be misunderstood or fail to change anything.',S),
      ('concept_ultrastability','Ultrastability','Ashby models a system that changes its parameters when its existing dynamics cross critical conditions.','Ask when changing the response rule becomes necessary, and what constrains that change.',A),
      ('concept_essential_variables','Essential variables','Ashby identifies variables whose values must stay within limits for an organism to remain alive.','In an organisational application, make the chosen viability conditions and their beneficiaries explicit.',A),
      ('concept_information_coding','Information coding','Fano studies how messages can be recoded to use fewer selections on average in a noiseless system.','Ask which distinctions a code preserves and what the receiver needs to interpret them.',F),
    ]
    for nid,label,summary,why,sid in defs:
        node(data,nid,label,'concept',summary,[sid])
        loc={S:'Weaver pp. 95–99; Shannon introduction pp. 3–5',A:'Design for a Brain, 3/14 and 8/4–8/7',F:'TR 65, abstract and sections I–III'}[sid]
        profile(data,nid,summary,why,[],[],[sid],loc)
    profile(data,work_ids['fano-transmission'],'A 1949 report on discrete messages and noiseless transmission, including information measures and recoding.','It gives an inspectable technical route into a reading-list reference.', ['TR 65 versus Part II/TR 149'], ['What counts as a possible message?'],[F,W],'TR 65, abstract, introduction, sections I–III')
    profile(data,work_ids['ashby-brain'],'Ashby develops a model of adaptive behaviour centred on stability, essential variables, and ultrastability. The inspected copy is a corrected 1954 reprint of the 1952 edition.','The model makes explicit what must be preserved while behaviour changes.', ['1952 edition versus later editions'],[],[A,W],'Preface; sections 3/14 and 8/4–8/7')
    profile(data,work_ids['shannon-weaver-book'],'The 1949 volume combines Shannon’s technical paper and Weaver’s separately attributed wider discussion.','The preface and contents let readers distinguish the contributors’ questions.', ['Shannon’s 1948 paper versus the 1949 volume'],[],[S,'src_illinois_shannon_weaver',W],'Preface; contents; Shannon pp. 3–5; Weaver pp. 95–99')
    profile(data,work_ids['wiener-close'],'Wiener examines scientific responsibility, changing weapons capability, and the way authority can suppress warnings.','Ask whether people able to detect a danger can get those with power to act on it.', ['A historical argument, with historical estimates'],[],[T,W],'Sections 1–2')
    profile(data,barrett,'The introduction frames cybernetics for social scientists through information and control. It declares six categories and acknowledges selective inclusion.','The stated audience helps explain the bibliography’s boundary.', ['Available introduction versus missing bibliography'],['Whose work would this selection rule make visible?'],[B],'Introduction, pages 1–3',['Recover the bibliography pages before claiming an item-level review of the full work.'])
    scope='Limited to the identified passage. A practice analogy needs its own assumptions and evidence.'
    rels=[
      (work_ids['fano-transmission'],'concept_information_coding',F,'TR 65, abstract; sections I–III'),
      (work_ids['fano-transmission'],'concept_information_theory',F,'TR 65, introduction'),
      (work_ids['ashby-brain'],'concept_ultrastability',A,'Chapter 8, sections 8/4–8/7'),
      (work_ids['ashby-brain'],'concept_essential_variables',A,'Section 3/14'),
      (work_ids['ashby-brain'],'concept_adaptation',A,'Preface'),
      (work_ids['shannon-weaver-book'],'concept_communication_levels',S,'Weaver pp. 95–99'),
      ('publication_fpcs_009','concept_information_theory',S,'Shannon introduction, pp. 3–5'),
      (barrett,'tradition_cybernetics',B,'Introduction, pages 1–2'),
    ]
    for a,b,sid,loc in rels:link(data,a,b,'presents_account_of','conceptual','presents an account of',[sid],loc,scope)
    link(data,work_ids['shannon-weaver-book'],'publication_fpcs_009','reprints_work','documentary','reprints',[S],'Preface, September 1949','The preface identifies the July and October 1948 paper, with minor corrections and extra references.')
    link(data,'concept_ultrastability','concept_essential_variables','formalises','conceptual','uses critical limits on',[A],'Sections 3/14 and 8/4–8/7','Read in the context of Ashby’s particular model.')
    link(data,'concept_ultrastability','concept_adaptation','presents_account_of','conceptual','models a mechanism for',[A],'Preface and chapter 8','A proposed mechanism, not an assertion that all adaptation is ultrastable.')
    # Explicit documentary citations inside a primary report are a separate type from influence.
    for pid in ['person_norbert_wiener','person_claude_e_shannon']:
        link(data,work_ids['fano-transmission'],pid,'discusses_in_introduction','documentary','acknowledges work by',[F],'Introduction, printed pp. 1–3','Fano explicitly discusses this work; no mentorship or collaboration is inferred.')
    journeys=[
      {'id':'journey_early_cybernetics_reading','title':'Reading cybernetics as it was taking shape','subtitle':'Selection, technical questions, and the limits of a bibliography','summary':'Follow the early lists into communication, adaptation, and social purpose, with a visible boundary between cited works and inspected passages.','audience':'historically curious reader','duration_minutes':12,'steps':[
        {'node_id':collections['selected-1952'],'heading':'Start with a dated selection','narrative':'The 21 March 1952 list puts reports, books, a journal article, and conference transactions alongside each other. Inspect the collection before treating it as a single school.'},
        {'node_id':work_ids['fano-transmission'],'heading':'Open one technical reference','narrative':'TR 65 gives the reading list a specific technical object: discrete messages and noiseless transmission. Its companion report is a separate reading task.'},
        {'node_id':'concept_communication_levels','heading':'Separate the questions','narrative':'Transmission accuracy, meaning, and effects require different questions. Use the volume’s attribution to follow who is arguing what.'},
        {'node_id':'concept_ultrastability','heading':'Follow the question of adaptation','narrative':'What must remain within limits, and what can change when the current response fails? Read Ashby’s stated conditions before applying the model elsewhere.'},
        {'node_id':barrett,'heading':'Inspect the compilers’ boundary','narrative':'Barrett and Shepard state an audience and acknowledge selective relevance. Their missing bibliography pages remain a visible gap in this source collection.'}]},
      {'id':'journey_messages_meaning_action','title':'The message arrived. What happened?','subtitle':'Transmission, interpretation, and the capacity to act','summary':'A practical route through communication questions, feedback, and response capacity. The links between the steps are editorial questions, not assertions of historical influence.','audience':'practitioner','duration_minutes':10,'steps':[
        {'node_id':'concept_communication_levels','heading':'Ask which problem you have','narrative':'Did the message arrive accurately? Was it understood as intended? Did it change conduct? Compare the three questions in a real exchange.'},
        {'node_id':'concept_information','heading':'Name the distinction','narrative':'What did the recipient learn that they did not know before? State the meaning of information being used here.'},
        {'node_id':'concept_feedback','heading':'Follow the return','narrative':'What happens to information about the result? Who receives it, and which action can it change?'},
        {'node_id':'concept_requisite_variety','heading':'Check the response repertoire','narrative':'Information alone does not supply time, authority, or possible responses. Examine what the recipient is able to do.'},
        {'node_id':'concept_observer','heading':'Include the interpreter','narrative':'Ask another person to describe the same exchange. Differences in the accounts may expose assumptions the first description hid.'}]},
      {'id':'journey_bibliography_boundaries','title':'How a reading list makes a field','subtitle':'Audience, selection, overlap, and absence','summary':'Read the bibliography as evidence of choices about a field, while keeping historical claims open to verification.','audience':'reader or curator','duration_minutes':8,'steps':[
        {'node_id':barrett,'heading':'Who is the collection for?','narrative':'The compilers explicitly address social scientists. Their categories are part of that editorial decision.'},
        {'node_id':collections['popular-1951'],'heading':'Follow public reception','narrative':'Magazine headlines and reviews record a public encounter with cybernetics. Titles alone cannot tell us whether an article endorses or rejects the ideas.'},
        {'node_id':collections['short-1956'],'heading':'Keep the awkward details','narrative':'A list described as 1956 includes a 1957 book. Preserve the discrepancy until the typescript can settle its date.'},
        {'node_id':'concept_boundary','heading':'Turn the question on this atlas','narrative':'Which sources are accessible to the people maintaining this map? What does that make visible, and what might it obscure?'}]}
    ]
    upsert(data['journeys'],journeys,'id')
    upsert(data['corpus_register'],[{
        'id':'early_cybernetics_reading_lists',
        'label':'Early cybernetics reading lists and Barrett–Shepard bibliography',
        'status':'available_entries_catalogued_primary_reading_in_progress',
        'issue_url':'https://github.com/antlerboy/the-necessary-tangle/issues/2',
        'source_ids':[W,B],
        'completion_test':'Recover the missing Barrett–Shepard bibliography pages, reconcile every supplied entry, and record item-level primary-text review before claiming the corpus fully reviewed.',
    }],'id')
    intake['summary']={'available_entries':len(intake['entries']),'distinct_work_keys':len({r['work_key'] for r in intake['entries']}),'resolved_work_count':len({r['node_id'] for r in intake['entries'] if r.get('node_id')}),'unresolved_references':sum(not r.get('node_id') for r in intake['entries']),'selected_passage_reviews':sum(r['review_status']=='selected_passages_reviewed' for r in intake['entries']),'metadata_checks':sum(r['review_status']=='metadata_checked' for r in intake['entries']),'barrett_shepard_bibliography_rows_available':0}
    data['early_cybernetics_corpus']=intake
    refresh_counts(data)
    data['relational_depth']=calculate_relational_depth(data)
    data['relational_depth'].update(release=RELEASE, generated=DATE)
    data['graph_snapshot']=calculate(data)
    return intake


def shell(title,description,body,path,script=''):
    return f'''<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light dark"><title>{esc(title)} · The Necessary Tangle</title><meta name="description" content="{esc(description)}"><link rel="canonical" href="https://transduction.systems/{path}"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/assets/learning-pages.css?v=0.22"></head><body><a class="skip-link" href="#main">Skip to content</a><header><a href="/">The Necessary Tangle</a><nav aria-label="Main navigation"><a href="/systems-thinking/">Start here</a><a href="/#view=browse">Atlas</a><a href="/#view=journeys">Guided journeys</a></nav></header><main id="main">{body}</main><footer><p>Curated by <a href="https://antlerboy.com/">Benjamin P Taylor</a> · 5 September 2026 · <a href="/submissions/">Corrections and additions</a></p></footer><a id="openUpdates" href="https://github.com/antlerboy/the-necessary-tangle/issues/2" aria-label="Open updates"></a>{script}</body></html>'''


def pages(intake):
    sec={s['id']:s['title'] for s in intake['sections']}
    body='''<p class="eyebrow">Historical sources · 1948–1957</p><h1>Reading cybernetics as it took shape</h1><p class="lead">Wiener’s selected reading, technical books, conference records, and popular treatments, alongside Barrett and Shepard’s explanation of their bibliography.</p><p>Historical material shared by <a href="https://x.com/TheUnjournaling">Sean Manion, @TheUnjournaling</a>, and transcribed on Systems Community of Inquiry. The original compilers and publication authors retain their separate credits.</p><div class="actions"><a class="button primary" href="/#view=journeys&amp;id=journey_early_cybernetics_reading&amp;step=0">Follow the reading journey</a><a class="button" href="#bibliography">Browse all 48 entries</a><a class="button" href="/assets/early-cybernetics-bibliography.json" download>Download the catalogue</a></div>
<section class="section" id="scope"><h2>What you can inspect here</h2><div class="grid"><article class="card"><h3>Wiener’s lists</h3><p>All 48 transcribed entries are retained: eight selected readings, 20 short-bibliography entries, 15 popular treatments, and five popular pieces by Wiener. They resolve to 45 distinct atlas works; one issue reference remains unidentified.</p><p>Four entries have selected primary passages reviewed, and Ashby’s 1946 title has an archive metadata check. The remaining entries have a bibliographic account. This is not a claim that every paper has been read.</p></article><article class="card"><h3>Barrett and Shepard</h3><p>The linked post supplies three pages of introduction. It describes six categories and names two illustrative books, but contains none of the bibliography’s hundreds of entries. Those missing pages are needed for a full paper-by-paper pass.</p><p>The byline is F. Dermot Barrett and Herbert A. Shepard. The source URL’s spelling ‘Shephard’ is retained only as part of its address.</p></article></div></section>
<section class="section"><h2>Two source posts, three original shares</h2><ul class="plain-list">'''
    for post in intake['posts']:
        body+=f'<li><a href="{esc(post["url"])}">{esc(post["title"])}</a><ul>'
        for i,url in enumerate(post['original_posts']):body+=f'<li><a href="{esc(url)}">Sean Manion’s original share {i+1}</a></li>'
        body+='</ul></li>'
    body+='''</ul><p class="note">The dated 1952 list is distinct from the approximate 1951 popular list and the short bibliography described as 1956. That last list includes Cherry’s 1957 book; its exact date needs the archival typescript. No silent correction has been made.</p></section>
<section class="section" id="barrett-shepard"><h2>The six categories of the 1951 bibliography</h2><p>These are the compilers’ categories, framed for social scientists. They remain a historical classification, with overlaps acknowledged in the introduction.</p><ol class="plain-list">'''
    for cat in intake['barrett_shepard_categories']:body+='<li>'+esc(cat)+'</li>'
    body+='</ol><p><a href="'+esc(route('bibliography_barrett_shepard_1951'))+'">Open the bibliography’s atlas entry</a>.</p><div class="grid">'
    for item in intake['barrett_shepard_named_works']:body+=f'<article class="card"><h3><a href="{esc(route(item["node_id"]))}">{esc(item["title"])}</a></h3><p>{esc(item["role"])}</p></article>'
    body+='''</div></section><section class="section" id="bibliography"><h2>Every available entry</h2><p>Search the original wording, author, title, or note. An atlas link identifies a work; the review label says how far the evidence pass has gone.</p><form id="bibliographyFilters" class="filters" hidden><label>Search the bibliography<input id="bibliographySearch" type="search" placeholder="Try Ashby, translation, or 1950"></label><label>Source section<select id="bibliographySection"><option value="">All sections</option>'''
    for sid,title in sec.items():body+=f'<option value="{sid}">{esc(title)}</option>'
    body+='''</select></label><label>Evidence reviewed<select id="bibliographyReview"><option value="">All entries</option><option value="selected_passages_reviewed">Selected primary passages</option><option value="metadata_checked">Archive metadata checked</option><option value="bibliographic_entry_transcribed">Bibliographic record only</option></select></label><button type="reset">Clear filters</button></form><p id="bibliographyCount" class="meta" role="status">48 source entries.</p><ol class="entries">'''
    statuses={'bibliographic_entry_transcribed':'Bibliographic record only','selected_passages_reviewed':'Selected primary passages reviewed','metadata_checked':'Archive metadata checked'}
    for row in intake['entries']:
        title=esc(row['title']);link_html=f'<a href="{esc(route(row["node_id"]))}">{title}</a>' if row.get('node_id') else title
        body+=f'<li id="{row["id"]}" class="entry" data-bibliography-entry data-section="{row["section"]}" data-review="{row["review_status"]}"><p class="meta">{esc(sec[row["section"]])}</p><h3>{link_html}</h3><p class="citation">{esc(row["transcribed_entry"])}</p><span class="status">{statuses[row["review_status"]]}</span>'
        if row.get('primary_url'):body+=f'<p><a href="{esc(row["primary_url"])}">Open the primary text or archive record</a>'+(' · '+esc(row['review_locator']) if row.get('review_locator') else '')+'</p>'
        for note in row['notes']:body+=f'<p class="note">{esc(note)}</p>'
        body+='</li>'
    body+='''</ol></section><section class="section"><h2>What a bibliography can show</h2><p>A listed title establishes that a compiler selected a work. It can help locate a text, recognise an audience, or trace public reception. Claims about influence, agreement, authorship, or the meaning of a theory need evidence appropriate to that claim.</p><p>Follow <a href="/#view=journeys&amp;id=journey_bibliography_boundaries&amp;step=0">How a reading list makes a field</a>, or <a href="/#view=journeys&amp;id=journey_messages_meaning_action&amp;step=0">The message arrived. What happened?</a></p></section>'''
    path=ROOT/'docs/corpora/early-cybernetics/index.html';path.parent.mkdir(parents=True,exist_ok=True);path.write_text(shell('Early cybernetics reading lists','A credited catalogue of 48 historical bibliography entries, their atlas identities, primary passage reviews, and unresolved references.',body,'corpora/early-cybernetics/','<script src="/assets/early-cybernetics.js?v=0.22" defer></script>'))
    jwrite(ASSETS/'early-cybernetics-bibliography.json',intake)
    rules=json.loads((ROOT/'sources/redquadrant-rules.json').read_text());jwrite(ASSETS/'redquadrant-rules.json',rules)
    rb='''<p class="eyebrow">RedQuadrant · Practice</p><h1>The little RedQuadrant rules</h1><p class="lead">256 binary rules for changing things that contain people.</p><p>Short provocations for practice. Bring a live situation to a rule, question its assumptions, and decide whether it helps.</p><div data-rq-rules><div class="actions"><button type="button" data-rule-next hidden>Give me another rule</button><a href="https://github.com/antlerboy/the-necessary-tangle/issues/2#issuecomment-5465271322">Original source</a><a href="https://chosen-path.org/2020/08/28/an-invitation-to-the-redquadrant-tool-shed/">The RedQuadrant Tool Shed</a></div><p data-rule-text class="featured-rule" aria-live="polite">Little RedQuadrant rule #1: Start with purpose. A project plan without purpose is decorative administration.</p><ol id="rules">'''
    for r in rules['rules']:rb+=f'<li id="rule-{r["number"]}" data-rule-number="{r["number"]}">{esc(r["text"])}</li>'
    rb+='</ol></div>'
    (ROOT/'docs/little-redquadrant-rules/index.html').write_text(shell('Little RedQuadrant rules','All 256 little RedQuadrant rules, readable without JavaScript, with a random-rule control.',rb,'little-redquadrant-rules/','<script src="/assets/redquadrant-rules.js?v=0.22" defer></script>'))


def reader():
    p=ROOT/'docs/index.html';s=p.read_text()
    s=re.sub(r'<span id="releaseBadge">.*?</span>','<span id="releaseBadge">Release 0.22</span>',s)
    s=re.sub(r'assets/iteration-20.js\?v=[^"\s]+','assets/iteration-20.js?v=0.22',s)
    s=re.sub(r'assets/site-enhancements.js\?v=[^"\s]+','assets/site-enhancements.js?v=0.22',s)
    s=re.sub(r'assets/public-data.js\?v=[^"\s]+','assets/public-data.js?v=0.22',s)
    s=re.sub(r'<p class="release-note-inline"><strong>Updated for 0\.21:</strong>.*?</p>','<p class="release-note-inline"><strong>Updated for 0.22:</strong> early cybernetics bibliographies, primary-passage accounts, three new guided journeys, and an accessible systems-thinking introduction. <a href="/corpora/early-cybernetics/">Inspect the source collection and its remaining gaps.</a></p>',s)
    marker='<div class="hero-actions">'
    if 'class="start-here-link"' not in s:s=s.replace(marker,'<p class="start-here-link">New to the subject? <a href="/systems-thinking/">Start with a plain-language introduction to systems thinking.</a></p>\n          '+marker,1)
    if 'id="earlyCyberneticsCallout"' not in s:
        marker='<section class="resource-pathways"'
        addition='<section class="resource-pathways" id="earlyCyberneticsCallout"><h2>Early cybernetics, through its reading lists</h2><p>Explore 48 historical entries, their authors, and the questions they open. Source inclusion, passage review, and unresolved details remain visible.</p><div class="button-row wrap"><a class="button" href="/corpora/early-cybernetics/">Read the historical collection</a><a class="button" href="#view=journeys&amp;id=journey_messages_meaning_action&amp;step=0">The message arrived. What happened?</a></div></section>\n      '
        s=s.replace(marker,addition+marker,1)
    if '/assets/release-22.css?v=0.22' not in s:s=s.replace('</head>','  <link rel="stylesheet" href="/assets/release-22.css?v=0.22">\n</head>',1)
    # A non-JavaScript visitor still has useful content and an entrance to the static collection.
    if '<noscript>' not in s:s=s.replace('<main id="main">','<main id="main"><noscript><p>The interactive atlas needs JavaScript. You can read the <a href="/systems-thinking/">systems-thinking introduction</a>, <a href="/corpora/early-cybernetics/">historical reading lists</a>, and <a href="/little-redquadrant-rules/">RedQuadrant rules</a> without it.</p></noscript>',1)
    p.write_text(s)
    sitemap=ROOT/'docs/sitemap.xml';text=sitemap.read_text()
    for path in ['systems-thinking/','corpora/early-cybernetics/','little-redquadrant-rules/']:
        url='https://transduction.systems/'+path
        if url not in text:text=text.replace('</urlset>',f'  <url><loc>{url}</loc><lastmod>{DATE}</lastmod></url>\n</urlset>')
    sitemap.write_text(text)


def release(data,intake):
    metrics=graph_metrics(data);meta=data['meta']
    meta.update(release=RELEASE,generated=DATE,iteration_focus='accessible gateway and source-accounted early cybernetics',node_count=len(data['nodes']),edge_count=len(data['edges']),source_count=len(data['sources']),profile_count=len(data['profiles']),journey_count=len(data['journeys']),public_entry_count=metrics['public_entries'],early_cybernetics_entry_count=48,early_cybernetics_url='https://transduction.systems/corpora/early-cybernetics/',systems_thinking_intro_url='https://transduction.systems/systems-thinking/',coverage_status='Early bibliography entries are fully accounted for where supplied. Four selected primary-passage reviews deepen this intake; Barrett–Shepard bibliography pages remain unavailable.')
    depth=data['relational_depth']['aggregate']
    meta.update(reader_connected_entry_count=depth['reader_connected_entries'], semantic_connected_entry_count=depth['semantic_connected_entries'], unconnected_entry_count=depth['connection_bands'].get('unconnected',0))
    meta.update(described_entry_count=metrics['public_entries'], public_link_source_count=sum(s.get('public_link_status')=='public_link' for s in data['sources']), no_public_link_source_count=sum(s.get('public_link_status')=='no_public_link' for s in data['sources']), semantic_gap_entry_count=metrics['public_entries']-depth['semantic_connected_entries'])
    for band in ('rich','developing','thin'):
        meta[band+'_entry_count']=depth['connection_bands'].get(band,0)
    for k in ['reading_list_inventory','reading_list_coverage','core_systems_practice']:data[k]['release']=RELEASE
    obs=data['ai_observations'];obs.update(release=RELEASE,generated=DATE,metrics=metrics)
    # Regenerate measurements rather than retaining the previous graph's counts.
    current_observations=make_ai_observations(metrics)
    upsert(obs['observations'],current_observations['observations'],'id')
    extras=[
      {'id':'bibliographic_selection_has_an_audience','title':'A bibliography has an audience','kind':'source-boundary observation','measurement':'The Barrett–Shepard introduction explicitly frames its selection for social scientists and distinguishes six categories. Its bibliography pages are absent from the supplied post.','interpretation':'The source explains a boundary, but cannot supply item-level coverage that is not present in the available text.','implication':'Catalogue the available entries and the missing pages separately.','test':'Can every claimed ingested item be found in the actual supplied material?'},
      {'id':'historical_lists_preserve_discrepancies','title':'An awkward date belongs in the record','kind':'bibliographic observation','measurement':'The short list described as 1956 includes a 1957 publication. Fano’s single entry names two reports, and Current Biography supplies no article title.','interpretation':'Silently regularising dates or titles would replace documentary evidence with a cleaner story.','implication':'Retain source wording alongside reconciliation and review status.','test':'Check that source entries survive even where a canonical identity remains unresolved.'},
      {'id':'breadth_and_reading_are_separate','title':'A catalogue entry is a distinct unit of work','kind':'coverage observation','measurement':'The intake accounts for 48 entries, four selected-passage reviews, one archive metadata check, and one unidentified reference.','interpretation':'Adding searchable records increases access to material while leaving a larger close-reading task open.','implication':'Show review depth beside each entry and keep bibliography membership outside influence relations.','test':'Filter by evidence reviewed; verify that catalogue-only entries do not appear as fully read.'},
      {'id':'an_entrance_changes_access','title':'An entrance changes who can use the atlas','kind':'reader-design observation','measurement':'The systems-thinking entrance presents a worked example and inquiry before exposing the larger graph. The rules are retained on a static page and removed from the atlas header.','interpretation':'The route into a knowledge collection affects who can participate without prior familiarity.','implication':'Provide useful static content and followable links alongside richer interactive views.','test':'Read the gateway and source catalogue with JavaScript unavailable; follow each named route.'}
    ]
    upsert(obs['observations'],extras,'id')
    for k in ['node_count','edge_count','source_count','profile_count','journey_count']:assert isinstance(meta[k],int)
    write(data)
    cite=ROOT/'CITATION.cff';c=cite.read_text();c=re.sub(r'^version:.*$',f'version: {RELEASE}',c,flags=re.M);c=re.sub(r'^date-released:.*$',f'date-released: {DATE}',c,flags=re.M);cite.write_text(c)
    lines=['# AI observations','',f'Generated for release `{RELEASE}` on {DATE}.','','Measurements describe this atlas. Interpretations and practice implications remain open to challenge.','']
    for o in obs['observations']:
        lines+=['## '+o.get('title','Observation'),'']
        for k in ['kind','measurement','interpretation','implication','test']:lines += [f'**{k.capitalize()}:** {o.get(k, "")}','']
    (ROOT/'documentation/ai-observations.md').write_text('\n'.join(lines))
    jwrite(ASSETS/'early-cybernetics-bibliography.json',intake)
    quality=quality_result(data)
    quality.update(release=RELEASE,generated=DATE)
    for key in ('adversarial_review','doncaster_lineage_review'):
        quality[key]=data[key]
    jwrite(ROOT/'data/relationship-quality.json',quality)
    jwrite(ASSETS/'relationship-quality.json',quality)
    write_relational_document(data)
    for name in ('TANGLE_STATE.md','NEXT_WORK.md'):
        (ROOT/'documentation'/name).write_text((ROOT/'sources/release-22'/name).read_text())
    readme=ROOT/'README.md';text=readme.read_text()
    if '## Release 0.22' not in text:
        text=text.replace('# The Necessary Tangle\n', '# The Necessary Tangle\n\n## Release 0.22\n\nA plain-language [systems-thinking entrance](https://transduction.systems/systems-thinking/), a [credited early cybernetics collection](https://transduction.systems/corpora/early-cybernetics/), three new guided journeys, and portable RedQuadrant rules. The candidate contains 719 canonical public entries, 137 profiles, 224 source records, and 1,987 typed statements. Bibliographic coverage and primary reading remain separately measured. See [the release account](documentation/release-0.22.md) for evidence, limits, and verification.\n',1)
    readme.write_text(text)
    # Legacy builders carry a dated SCiO document. Preserve the maintained source
    # instead of letting this unrelated release remove its later corpus notes.
    (ROOT/'documentation/scio-coverage.md').write_text((ROOT/'sources/release-22/scio-coverage-base.md').read_text())
    for name, heading, text in [
        ('CHANGELOG.md','## 0.22 — 5 September 2026', 'Accessible systems-thinking gateway; 48-entry early cybernetics catalogue with Sean Manion credited; nine developed profiles and three journeys; 256 RedQuadrant rules preserved for reuse with the header rule retired. See `documentation/release-0.22.md` for evidence depth and remaining gaps.'),
        ('documentation/feedback-ledger.md','## Release 0.22 — accessible entrance and September source intake', 'The two issue #2 source posts are accounted for with original wording, review labels, explicit gaps, and corrected Sean Manion credit. `/systems-thinking/` is built as the gateway. The header rule is retired; all 256 texts, stable page, and portable code are preserved. Receiving-site placement and domain routing are recorded in `redquadrant-rules-handoff.md`. Publication remains subject to human review.'),
        ('ACKNOWLEDGEMENTS.md','## Early cybernetics source discovery', 'Sean Manion, @TheUnjournaling, shared the historical Wiener reading lists and the Barrett–Shepard bibliography introduction used in release 0.22. Systems Community of Inquiry supplied the linked transcriptions. Norbert Wiener, F. Dermot Barrett, Herbert A. Shepard, and the authors and editors of the listed publications retain their separate credits. Source discovery, compilation, transcription, and authorship are distinct contributions.'),
    ]:
        p=ROOT/name;s=p.read_text()
        if heading not in s:p.write_text(s.rstrip()+'\n\n'+heading+'\n\n'+text+'\n')


def main():
    data=json.loads((ROOT/'data/public-data.json').read_text());intake=json.loads(INTAKE.read_text())
    enrich(data,intake);pages(intake);release(data,intake);reader()
    print('Applied 0.22:',json.dumps(intake['summary']),';',data['meta']['public_entry_count'],'public entries;',len(data['profiles']),'profiles;',len(data['edges']),'edges')
if __name__=='__main__':main()
