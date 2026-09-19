"""Located arguments and distinctions, separate from catalogue and phrase matches."""
from apply_iteration_17 import enc,upsert,relation_record

def apply(data,records,edge):
    nodes={n['id']:n for n in data['nodes']}
    def item(title):return next(r for r in records if r['title']==title and r.get('pages'))
    def sid(r):return next(s['id'] for s in data['sources'] if s.get('url')==r['url'])
    for typ,family,phrase in [
        ('offers_practice_heuristic','practice','offers a practice heuristic for'),
        ('qualifies_practice_claim','contestation','qualifies a claim about'),
        ('uses_in_argument','conceptual','uses in its argument'),
        ('proposes_condition_for','conceptual','proposes a condition for'),
        ('includes_practice_component','practice','includes as a practice component'),
        ('questions_default_boundary','contestation','questions the default boundary in'),
    ]:upsert(data['relation_types'],[relation_record(typ,family,'inverse_'+typ,'A specific passage and scoped account of the source argument',phrase)],'relation_type')
    arguments=[
        ('Degrees of relationality','practice_relational_public_services','offers_practice_heuristic','practice','offers a degrees-of-relationality heuristic for','PDF pp. 1–3','The authors distinguish several kinds and scopes of relational change. The ladder is explicitly not a validated scale, moral ranking, or universal sequence.'),
        ('Degrees of relationality','practice_relational_public_services','qualifies_practice_claim','contestation','challenges a simple transactional-versus-relational opposition within','PDF pp. 1–3','The authors argue that reliable transactions can be appropriate and that a warm encounter need not change institutional conditions. This qualifies a binary presentation, not every relational approach.'),
        ('The demand side of public services','concept_form_of_response','uses_in_argument','conceptual','distinguishes forms of response in','PDF pp. 1–3','The response is examined against demand in a citizen’s situation, not against a general preference for relational service. The paper’s four forms are not silently equated with the degrees-of-relationality ladder.'),
        ('The demand side of public services','concept_strategy_ceiling','uses_in_argument','conceptual','uses to explain the fragility of local reform','PDF p. 4, sections 5–6','The strategy ceiling separates changes in doing the job from changes to purpose, money, policy, roles, and legitimate evidence. The paper attributes the earlier concept to Boxer.'),
        ('The demand side of public services','concept_consequential_learning','proposes_condition_for','conceptual','requires a route from evidence to authority for','PDF p. 4, section 6','The authors ask whether learning from a particular situation can change rules, measures, resources, contracts, or boundaries. More feedback alone is not claimed sufficient.'),
        ('The demand side of public services','concept_systemic_governance','qualifies_practice_claim','contestation','questions whether devolved authority alone changes','PDF p. 5, section 8','Devolution may reproduce a strategy ceiling at a larger scale. The argument calls for capability, resources, rights, and learning across levels; it is not an argument against devolution in every case.'),
        ('Anxiety, ideology and the evacuation of the public realm','concept_strategy_ceiling','uses_in_argument','conceptual','uses to explain how private accommodation blocks public learning','PDF p. 1, abstract and section 1','The authors connect the strategy ceiling to sponsoring arrangements, institutional anxiety, and risk displacement. This is an argument in a working paper, not a demonstrated universal causal mechanism.'),
        ('Anxiety, ideology and the evacuation of the public realm','practice_relational_public_services','qualifies_practice_claim','contestation','questions improvement judged only at the encounter in','PDF p. 1, section 1','A humane workaround can protect a person while insulating an institution from learning. The authors distinguish the quality of contact from changes to common rules and resources.'),
        ('Anxiety, ideology and the evacuation of the public realm','concept_systemic_governance','proposes_condition_for','conceptual','proposes an institutional capacity for reframing within','PDF p. 1, abstract','Negative capability is presented as a capacity that needs support in governance, not only as an individual virtue.'),
        ('Service systems, citizen ecosystems, and the politics we deny','approach_family_service_systems_thinking','questions_default_boundary','contestation','questions a provider-centred starting boundary within','PDF pp. 1–2','The paper proposes holding service arrangements and lived ecosystems together, while making political contest over value and legitimacy explicit. It does not claim that every service-systems account excludes these concerns.'),
        ('Service systems, citizen ecosystems, and the politics we deny','concept_boundary','uses_in_argument','conceptual','treats boundary-setting as a contested design decision','PDF pp. 1–2','What a service is responsible for is shaped by institutions, budgets, authority, and ideology. The source argues that this should be part of inquiry and design, rather than assumed away.'),
    ]
    for title,target,typ,family,phrase,loc,scope in arguments:
        r=item(title);edge(r['atlas_id'],target,typ,family,phrase,[sid(r)],loc,scope)
        r['connections'].append(dict(target=target,label=nodes[target]['label'],kind='argument',phrase=phrase,scope=scope,locator=loc,status='Source argument located; interpretation open to review'))
    research_arguments=[
        ('10.1016/j.evalprogplan.2008.04.004','tradition_critical_systems_thinking','uses_in_argument','conceptual','compares DSRP with a critical systems perspective','Section 1.2, printed pp. 323–324','Reynolds offers understanding, practice, and responsibility as interacting frameworks. He explicitly presents the comparison as a conversation, rather than a competition between frameworks.'),
        ('10.1016/j.evalprogplan.2008.04.004','concept_boundary','uses_in_argument','conceptual','makes framing and boundary responsibility explicit through','Section 1.2, printed pp. 323–324','Holism and pluralism remain bounded. Reynolds asks that the limits and responsibility of a framing be made explicit.'),
        ('10.1016/j.evalprogplan.2008.04.004','concept_multiple_perspectives','uses_in_argument','conceptual','joins perspective-taking to responsibility for framing','Sections 1.1–1.2, printed pp. 323–324','Inviting other perspectives is treated as an ongoing inquiry whose framing must also be questioned, rather than a guarantee of completeness.'),
        ('10.1016/j.evalprogplan.2008.04.004','concept_purpose','proposes_condition_for','conceptual','proposes purpose as a defining feature of system-making','Printed pp. 324–325','Reynolds asks whether purpose explains how a system is bounded and its parts identified. This is his proposed distinction, not an agreed definition shared by all traditions.'),
        ('10.1016/j.evalprogplan.2008.04.001','concept_distinction','uses_in_argument','conceptual','treats distinctions as interacting patterns within DSRP','Section 1.2, printed pp. 312–313','Cabrera and Colosi describe distinctions, systems, relationships, and perspectives as interacting patterns with paired elements. Their claim of universality remains the authors’ claim.'),
        ('10.1016/j.evalprogplan.2008.04.001','concept_multiple_perspectives','uses_in_argument','conceptual','includes perspective-taking in a recursive account of thinking','Section 1.2, printed pp. 312–313','The authors apply the patterns to one another, including taking perspectives on a relationship. This does not establish equivalence with every earlier use of perspective-taking.'),
        ('10.1016/j.evalprogplan.2008.04.001','person_gerald_midgley','qualifies_practice_claim','contestation','responds to Midgley on universality and methodological pluralism','Section 1.1, printed pp. 311–312','Cabrera and Colosi reject an opposition between universal formalism and methodological pluralism. They call pluralism useful and necessary while arguing that it does not itself supply a formal theory. This records their response, without adjudicating the dispute.'),
        ('10.1080/09540962.2020.1832738','practice_human_learning_systems','uses_in_argument','conceptual','sets out a complexity-informed account of','Article sections Human, Learning, and Systems, pp. 2–3','The authors organise the approach around humane service relationships, continuous learning, and work across organisational boundaries. Practitioner examples support an emerging account, rather than a general proof of superior outcomes.'),
        ('10.1080/09540962.2020.1832738','practice_organizational_learning','proposes_condition_for','conceptual','treats continuous adaptation as a basis for','Learning section, pp. 2–3','The article proposes learning across planning, implementation, and evaluation, with monitoring used for reflection and commissioning supporting capacity to learn.'),
        ('10.1080/09540962.2020.1832738','intervention_skill_action_learning','uses_in_argument','conceptual','draws on action embedded in learning through','Learning section, p. 3','The authors explicitly identify action learning as an inspiration. They also name other forms; this is not a claim that HLS is identical to action learning.'),
        ('10.1080/09540962.2020.1832738','concept_systemic_governance','offers_practice_heuristic','practice','proposes system-stewarding roles for','Systems section, p. 3','The account places shared purpose, trust, relationships, and funding decisions across organisational boundaries within system stewardship. This is a stated practice proposal, not evidence that every implementation meets it.'),
    ]
    for doi,target,typ,family,phrase,loc,scope in research_arguments:
        r=next(record for record in records if record.get('doi')==doi)
        edge(r['atlas_id'],target,typ,family,phrase,[sid(r)],loc,scope)
        r['connections'].append(dict(target=target,label=nodes[target]['label'],kind='argument',phrase=phrase,scope=scope,locator=loc,status='Named source sections read; interpretation open to review'))
    for doi,person in [('10.1016/j.evalprogplan.2008.04.004','person_martin_reynolds'),('10.1080/09540962.2020.1832738','person_toby_lowe')]:
        r=next(record for record in records if record.get('doi')==doi)
        edge(r['atlas_id'],person,'authored_by','documentary','is authored or co-authored by',[sid(r)],'Opening author credit','Author identity checked against the opening credits and publisher-deposited metadata.')
        r['connections'].append(dict(target=person,label=nodes[person]['label'],kind='authorship',locator='Opening author credit',status='Opening author credit checked'))
    clarity=item('Clarity practices')
    for target,typ,phrase,loc,scope in [
        ('intervention_skill_productive_conversations','includes_practice_component','includes constructive conversations as a foundation','PDF pp. 5–6','The framework names constructive conversations, clarity, and triple-loop learning as foundations for a learning system.'),
        ('practice_organizational_learning','proposes_condition_for','proposes foundations for','PDF pp. 5–7','Taylor’s teaching joins constructive conversations, clarity, and reflective learning; these are practice propositions rather than independently evaluated sufficient conditions.'),
        ('concept_purpose','includes_practice_component','orients intent and measures towards','PDF p. 7','The teaching account ties good and clear intent to customer, user, citizen, and community outcomes, including their experience of the work.'),
    ]:edge('practice_taylor_five_core_practices',target,typ,'practice' if typ=='includes_practice_component' else 'conceptual',phrase,[sid(clarity)],loc,scope)
    # Preserve the co-author credits and their order, rather than attaching every
    # item only to the curator because it was found in his public library.
    for title,authors in [('Degrees of relationality',['Benjamin P Taylor','Philip Boxer']),('The demand side of public services',['Philip Boxer','Benjamin P Taylor']),('Anxiety, ideology and the evacuation of the public realm',['Philip Boxer','Benjamin P Taylor'])]:
        r=item(title);r['authors']=authors
        src=next(s for s in data['sources'] if s['id']==sid(r));src['creators']=enc(authors)
        edge(r['atlas_id'],'person_philip_boxer','authored_by','documentary','is co-authored by',[sid(r)],'PDF page 1: author credits','Title-page author order: '+', then '.join(authors)+'.')
        r['connections'].append(dict(target='person_philip_boxer',label='Philip Boxer',kind='authorship',locator='PDF page 1: co-author credit',status='Public title-page credit checked'))
    for e in data['edges']:
        if e.get('connection_pass')=='library_20260919' and e['relation_type']=='coauthored_with':e['directed']='false'
