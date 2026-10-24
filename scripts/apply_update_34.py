"""Reproducible current reading, source depth, and quick contribution route."""
from pathlib import Path
import hashlib, html, json, math, re
from apply_iteration_17 import enc, upsert, source_record, node_record, edge_record
from apply_iteration_09 import graph_metrics
from apply_relational_depth_16 import calculate_relational_depth, write_relational_document
from apply_doncaster_lineage import refresh_counts
from apply_overnight_review import quality_result
from refresh_graph_snapshot import calculate, write

R = Path(__file__).resolve().parents[1]; D = R/'docs'; S = R/'sources/update-2026-10-24'
DATE = '2026-10-24'; RELEASE = '0.34'; MARK = 'update_20261024'
P = json.loads((S/'syscoi-review.json').read_text(encoding='utf-8'))
H = json.loads((S/'events-review.json').read_text(encoding='utf-8'))
d = json.loads((R/'data/public-data.json').read_text(encoding='utf-8'))
E = lambda s: html.escape(str(s), quote=True)
def link(url, title): return '<a href="'+E(url)+'">'+E(title)+'</a>'
def atlas(nid):
    n = next(n for n in d['nodes'] if n['id'] == nid)
    return link('/#view=item&id='+nid, n['label'])
def source(sid, title, url, note, locator):
    row = source_record(sid, title, 'public_source', url, note, [], 'Original author or publisher', '2026', quality='B')
    row.update(connection_pass=MARK, last_checked=DATE, review_status='source_scoped_research_pass', source_locator=locator)
    upsert(d['sources'], [row], 'id'); return sid
def node(nid, title, kind, summary, sids, tags):
    i = int(hashlib.sha256(nid.encode()).hexdigest()[:6], 16)
    row = node_record(nid, title, kind, summary, sids, round(.55+.2*math.cos(i*2.4),6), round(.45+.2*math.sin(i*2.4),6), tags)
    row.update(connection_pass=MARK, status='candidate', review_status='research_pass_needs_editor', reviewed_by='', reviewed_at='', inclusion_reason=MARK, set_tags=enc(['systems','release_0_34',*tags]))
    upsert(d['nodes'], [row], 'id'); return nid
def edge(eid, start, end, typ, sid, locator, scope):
    family = next(t['relation_family'] for t in d['relation_types'] if t['relation_type'] == typ)
    row = edge_record(eid, start, end, typ, family, typ.replace('_',' '), [sid], locator, scope, status='candidate', confidence='', review_label='Source-scoped candidate; editorial review remains open')
    row.update(connection_pass=MARK); upsert(d['edges'], [row], 'id')

sid = source('src_u34_syscoi_collection', 'SysCoI additions, 18–24 October 2026', P['api'], 'Complete overlapping-window reconciliation: five new reading leads and four existing resource routes.', 'Published post IDs, dates, titles, and original outbound destinations')
collection = node('collection_syscoi_20261024', 'SysCoI additions: 18–24 October 2026', 'collection', 'Nine public posts reconciled: five new reading leads and four routes to already represented resources. Discovery does not establish agreement, historical influence, or empirical effectiveness.', [sid], ['syscoi-intake'])
for p in P['posts']:
    if p['status'] != 'new_discovery': continue
    sid = source('src_syscoi_post_'+str(p['id']), p['title'], p['url'], p['summary'], 'Post title, publication date, and outbound destination')
    row = next(s for s in d['sources'] if s['id'] == sid)
    row.update(publisher='Systems Community of Inquiry', date=p['date'][:10], original_urls=enc(p['links']), source_role='discovery provenance')
    nid = node('publication_syscoi_post_'+str(p['id']), p['title'], 'publication', p['summary'], [sid], ['syscoi-intake'])
    edge('e34_collection_'+str(p['id']), collection, nid, 'catalogues_resource', sid, 'Post ID '+str(p['id'])+'; title and date', 'Membership of a dated discovery collection; substantive linked claims require separate review.')

commit = '6ab72502741b1a9a9ccdc3dbaa8ad03e259bc536'
base = 'https://framagit.org/dynamicskillset/orglens/-/blob/'+commit+'/'
sid = source('src_u34_orglens_architecture', 'OrgLens technical overview and implemented lenses', base+'docs/ARCHITECTURE.md', 'Doug Belshaw’s experimental tool separates model construction, deterministic checks, plain wording, and report writing. Its checked representation is not the organisation itself.', 'The three lenses; Structure; Feedback loops; Perspectives; From findings to a report')
for target, locator, scope in [
    ('method_or_methodology_viable_system_model_vsm', 'Structure (Viable System Model); orglens/checks.py: check, absence_lint, operations', 'OrgLens implements checks on a submitted VSM representation, including missing functions, autonomy, and channels. Findings are hypotheses about that model, not certified organisational facts.'),
    ('method_or_methodology_system_dynamics', 'Feedback loops; orglens/loops.py: loops, archetypes, check', 'OrgLens classifies represented loops and matches archetype rules using roles as well as graph shape. This does not prove the causal links, strengths, or time behaviour in an organisation.'),
    ('method_or_methodology_soft_systems_methodology_ssm', 'Perspectives: voices with CATWOE and success measures', 'OrgLens uses recorded CATWOE perspectives to raise questions about different transformations and worldviews. This is a selected use of SSM ideas, not evidence that it performs a full SSM intervention.'),
    ('method_or_methodology_critical_systems_heuristics_csh', 'Perspectives: twelve boundary questions, coverage, unsupported_oughts', 'OrgLens records is/ought answers and unheard affected groups. Checking that supporting words exist cannot establish whether they express a legitimate ought judgement.')]:
    edge('e34_orglens_'+target, 'tool_orglens', target, 'uses', sid, locator, scope)

sid42 = source('src_u34_42_about', '42 The Systemic Review: purpose and process', 'https://42systemicreview.org/about/', 'SCiO describes a publication and policy-engagement programme using systems laws, principles, and ways of thinking to examine public-policy problems.', 'Why 42?; What you can expect; How it works')
review42 = node('publication_42_systemic_review', '42 The Systemic Review', 'publication', 'SCiO’s publication and policy-engagement programme. Reviews state a system of concern, distinguish evidence from interpretation, and apply selected systems principles to a policy problem. These are attributed analyses open to challenge, not an exhaustive or independently validated canon.', [sid42], ['policy','systems-practice'])
papers = [
    ('delay', 'The Equilibrium of Delay', 'https://42systemicreview.org/papers/the-equilibrium-of-delay', 'The review interprets Playford’s capital-works backlog through accumulated commitments, a planning/design constraint, and delayed work consuming delivery attention. Its proposed mechanism and capacity claims need comparison with the cited council evidence.', [('concept_feedback','Finding 4; a reinforcing loop involving delayed projects and attention'),('concept_requisite_variety','Finding 3; regulating different demands mainly through financial controls')]),
    ('boxes', 'Between the Boxes', 'https://42systemicreview.org/papers/between-the-boxes', 'The review examines how a bounded air-traffic-control failure can propagate through a wider aviation system. Its system boundary and account of cross-organisational responsibility are analytical choices, separate from a technical incident investigation.', [('concept_boundary','System framing; the boundary between technical recovery and wider aviation disruption')]),
    ('health', 'Neighbourhood Health and Care: Building the System Before the Structure', 'https://42systemicreview.org/papers/neighbourhood-health-and-care', 'The review treats neighbourhood working as the formation of a viable system across established organisations. It examines autonomy, coordination, and stabilising organisational feedback; its policy and causal claims remain attributed to the paper.', [('concept_autonomy','Findings 1–2; new system formation and autonomy/cohesion at nested levels'),('concept_feedback','Finding 3; budgets, referrals, and targets stabilising organisational behaviour'),('concept_boundary','System framing; neighbourhood nested within place and wider arrangements')]),
]
for slug, title, url, summary, targets in papers:
    ps = source('src_u34_42_'+slug, title, url, summary, 'Executive Summary; Findings; System Framing and Method')
    nid = node('publication_42_'+slug, title+' — 42 The Systemic Review', 'publication', summary, [ps], ['policy','systems-practice'])
    edge('e34_42_catalogue_'+slug, review42, nid, 'catalogues_resource', ps, 'Paper title and publication series', 'The paper is presented in this publication; its findings remain the paper’s attributed interpretation.')
    for target, loc in targets: edge('e34_42_'+slug+'_'+target, nid, target, 'uses_in_argument', ps, loc, 'This records the paper’s use of a concept in its analysis, without treating the diagnosis as independently verified.')

leadership_url = 'https://chosen-path.org/2026/10/18/where-are-the-systems-in-systems-leadership/'
sid = source('src_u34_taylor_systems_leadership', 'Where are the systems in systems leadership?', leadership_url, 'Benjamin P Taylor’s explicit account of inquiry, action, and the arrangements that enable them.', 'Opening definition; delivery-schedule example; distinction between leadership development and changing system behaviour')
for target, loc, scope in [
    ('approach_family_systems_leadership','Opening definition','Taylor proposes a particular practice account of systems leadership; it is not represented as a field-wide consensus definition.'),
    ('concept_purpose','Whose purposes count, and who decides what better means','The essay treats purpose and judgement of improvement as part of systems-leadership inquiry.'),
    ('concept_feedback','Delivery-schedule example and consequences of interventions','The essay asks how recurring patterns are produced and how interventions can displace harm or change the pattern.')]:
    edge('e34_leadership_'+target, 'publication_syscoi_post_29296', target, 'uses_in_argument', sid, loc, scope)

refresh_counts(d)
d['relational_depth'] = calculate_relational_depth(d); d['relational_depth'].update(release=RELEASE, generated=DATE)
d['graph_snapshot'] = calculate(d); metrics = graph_metrics(d); depth = d['relational_depth']['aggregate']
d[MARK] = dict(date=DATE, posts_checked=9, new_discovery_records=5, reused_resources=4, events=H, orglens_commit=commit)
d['meta'].update(release=RELEASE, generated=DATE, release_digest_url='https://transduction.systems/updates/2026-10-24/', latest_intake_url='https://transduction.systems/updates/2026-10-24/', iteration_focus='Current events, source-led practice guides, and quick contributions', release_note='Recent SysCoI reading reconciled; developed OrgLens and 42 guides; systems leadership and action; current events; quick plain-text contributions.', node_count=len(d['nodes']), edge_count=len(d['edges']), source_count=len(d['sources']), profile_count=len(d['profiles']), public_entry_count=metrics['public_entries'], described_entry_count=metrics['public_entries'], reader_connected_entry_count=depth['reader_connected_entries'], semantic_connected_entry_count=depth['semantic_connected_entries'], unconnected_entry_count=depth['connection_bands'].get('unconnected',0), semantic_gap_entry_count=metrics['public_entries']-depth['semantic_connected_entries'], public_link_source_count=sum(s.get('public_link_status')=='public_link' for s in d['sources']), no_public_link_source_count=sum(s.get('public_link_status')=='no_public_link' for s in d['sources']))
for band in ['rich','developing','thin']: d['meta'][band+'_entry_count'] = depth['connection_bands'].get(band,0)
write(d)
q = quality_result(d); q.update(release=RELEASE, generated=DATE)
for key in ['adversarial_review','doncaster_lineage_review']: q[key] = d[key]
for name in ['data/relationship-quality.json','docs/assets/relationship-quality.json']: (R/name).write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
write_relational_document(d)

css = '*{box-sizing:border-box}body{margin:0;background:#faf8f2;color:#302b26;font:18px/1.65 Georgia,serif}main,nav,footer{max-width:65rem;margin:auto;padding:1.4rem}nav{display:flex;gap:1rem;flex-wrap:wrap;font:1rem/1.5 system-ui}a{color:#973d32;overflow-wrap:anywhere}a:focus-visible,input:focus-visible,textarea:focus-visible,button:focus-visible{outline:3px solid #973d32;outline-offset:3px}h1{font-size:clamp(2rem,6vw,3.5rem);line-height:1.15}h2{line-height:1.3}section,article{border-bottom:1px solid #d8d0c5;padding:1rem 0}.meta,.note,form{font:1rem/1.6 system-ui}.note{background:#f0eadd;padding:1rem}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,25rem),1fr));gap:1.4rem}.grid article{padding:1rem;border:1px solid #d8d0c5;border-top:3px solid #973d32}label{display:block;margin:1rem 0}input,textarea{display:block;max-width:100%;width:100%;padding:.7rem;font:inherit;border:1px solid #938779;background:#fffdf7}button{padding:.7rem 1rem;font:inherit;background:#862719;color:white;border:0;cursor:pointer}button:disabled{opacity:.65}.table-wrap{overflow:auto}table{border-collapse:collapse;width:100%}td,th{padding:.7rem;border-bottom:1px solid #d8d0c5;text-align:left;vertical-align:top}#openUpdates{position:fixed;bottom:0;right:0;width:44px;height:44px}#openUpdates:after{content:"";position:absolute;right:8px;bottom:8px;width:5px;height:5px;background:#862719;border-radius:50%;box-shadow:0 0 0 1px white}@media(max-width:600px){main,nav,footer{padding:1rem}ul,ol{padding-left:1.3rem}.table-wrap table{min-width:35rem}}'
def page(route, title, body, script=''):
    dest = D/route.strip('/'); dest.mkdir(parents=True, exist_ok=True)
    text = '<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+E(title)+' | The Necessary Tangle</title><meta name="description" content="'+E(title)+' — attributed reading and practical questions from The Necessary Tangle."><link rel="canonical" href="https://transduction.systems'+route+'"><style>'+css+'</style></head><body><nav aria-label="Main">'+link('/','Atlas')+link('/learning/','Learning')+link('/events/','Events')+link('/updates/2026-10-24/','Latest update')+link('/contribute/','Quick contribute')+'</nav><main><p class="meta">Release 0.34 · 24 October 2026</p><h1>'+E(title)+'</h1>'+body+'</main><footer><p>Curated by '+link('https://www.antlerboy.com/','Benjamin P Taylor')+'. AI-assisted source research. Linked works retain their authorship and terms. Interpretations and candidate connections remain open to challenge.</p></footer><a id="openUpdates" href="https://github.com/antlerboy/the-necessary-tangle/issues/2" aria-label="Open updates"></a>'+script+'</body></html>\n'
    (dest/'index.html').write_text(text, encoding='utf-8')

body = '<p>OrgLens turns accounts of an organisation into a report through three systems lenses. Doug Belshaw’s '+link(base+'README.md','source repository')+' describes an experiment tested on fictional organisations, simulated participants, and AI judges. Its usefulness in a real organisation remains to be established.</p><p>'+atlas('tool_orglens')+' · '+link('https://orglens.dynamicskillset.com/','Open the tool')+' · '+link(base+'docs/GUIDE.md','Plain-English guide')+'</p><section><h2>Follow the evidence through the pipeline</h2><p>The '+link(base+'docs/ARCHITECTURE.md','technical account')+' separates four operations: a model represents what people said; code checks that representation; fixed wording describes the findings; and a language model writes a report that receives further quotation and consistency checks. A correct quotation establishes that the words were present. It does not establish that the speaker’s account was complete or that the diagnosis follows.</p><div class="table-wrap"><table><thead><tr><th>Lens</th><th>What the source implements</th><th>What still requires judgement</th></tr></thead><tbody><tr><th>Structure</th><td>Checks for recorded operations, coordination, control, audit, intelligence, policy, and channels.</td><td>Whether a missing model element reflects a missing capability, poor questioning, or an inappropriate system boundary.</td></tr><tr><th>Feedback</th><td>Loop sign, delays, and archetype rules combining graph structure with variable roles.</td><td>Whether the causal links hold, how strong they are, and what behaviour their interaction produces over time.</td></tr><tr><th>Perspectives</th><td>CATWOE accounts, different success measures, unheard groups, and is/ought boundary answers.</td><td>Who was able to speak, whose interpretation prevailed, and whether an attributed ought says what the report claims.</td></tr></tbody></table></div><p>Source locators: '+link(base+'orglens/checks.py','structure checks')+'; '+link(base+'orglens/loops.py','loop and archetype checks')+'; '+link(base+'orglens/perspectives.py','perspective checks')+'. Repository revision '+E(commit[:8])+'. Code was inspected; the complete experiment was not rerun.</p></section>'
body += '<section><h2>Use the differences between the lenses</h2><p>The '+link(base+'SURVEY-SYSTEMS-MODELS.md','lens-selection survey')+' explains why the project added feedback and perspective checks. Its compressed descriptions of the parent methods also need scrutiny. For example, treating VSM as assuming an uncontested purpose would turn a modelling choice into a property of the method. A finding about an interview representation cannot settle a dispute about an organisation.</p><p>Compare '+atlas('method_or_methodology_viable_system_model_vsm')+', '+atlas('method_or_methodology_system_dynamics')+', '+atlas('method_or_methodology_soft_systems_methodology_ssm')+', and '+atlas('method_or_methodology_critical_systems_heuristics_csh')+'. The tool selects parts of these traditions; it does not replace their broader practice.</p></section><section><h2>Questions for a practitioner</h2><ol><li>Invite the people described to correct the model and identify voices it missed.</li><li>Separate the report’s quotations, inferences, and suggested actions.</li><li>Check a proposed causal pattern against events over time and competing explanations.</li><li>Find who could authorise the suggested change and what constraints they face.</li><li>Record what happened after using the report, including harm, disagreement, and conclusions that failed.</li></ol><p>These are editorial questions for using a diagnostic aid, not findings from OrgLens trials.</p></section><section><h2>Evaluation, data, and reuse</h2><p>The '+link(base+'README.md#what-weve-found','project’s evaluation account')+' reports experiments on three fictional cases. Simulated reader clarity and checked quotations do not demonstrate organisational improvement. Its README also says submitted material goes to third-party model services and asks users to leave out private information; consult the current service before using it.</p><p>The repository states '+link(base+'LICENSE','GNU AGPL version 3 or later')+'. This guide links and paraphrases; no OrgLens code is included in the atlas. The '+link('https://substrate.dougbelshaw.com/orglens-2-making-an-organisational-health-check-people-can-actually-use','earlier development article')+' supplies a separate account of the plain-language reporting work.</p></section>'
page('/reading/orglens/', 'OrgLens: models, checks, and organisational judgement', body)

body = '<p>'+link('https://42systemicreview.org/','42 The Systemic Review')+' is SCiO’s publication and policy-engagement programme. Its '+link('https://42systemicreview.org/about/','About page')+' describes a way to examine a public-policy problem through selected systems laws, principles, and ways of thinking. The publication says it makes evidence, interpretation, boundaries, and assumptions visible. Those commitments can be tested against each paper.</p><p>'+atlas(review42)+' · '+link('https://42systemicreview.org/papers','Browse the publication’s papers')+'</p><section><h2>Three current applications</h2><div class="grid">'
for slug, title, url, summary, targets in papers:
    body += '<article><h3>'+link(url,title)+'</h3><p>'+E(summary)+'</p><p>Read the executive summary, findings, and system-framing sections. Compare: '+' · '.join(atlas(t) for t,_ in targets)+'.</p><p>'+atlas('publication_42_'+slug)+'</p></article>'
body += '</div></section><section><h2>Read a diagnosis as an argument</h2><ol><li>Check what the selected system includes and what it leaves outside.</li><li>Follow the factual claims back to the cited evidence.</li><li>Identify the mechanism linking the stated principle to the observed pattern.</li><li>Ask what observation would weaken that explanation.</li><li>Consider the effects on people outside the diagnosis and who could change the relevant conditions.</li></ol><p>These are editorial reading questions. Naming a principle does not establish that its application fits the case. Agreement between two methods may help expose an explanation, but shared assumptions can also make them repeat the same error.</p></section><section><h2>Keep the scope visible</h2><p>The publication’s name refers to its chosen set of 42 laws, principles, and ways of thinking, with a Douglas Adams reference. This guide does not treat that selection as a universally agreed canon. Its account of a rapid, usually free initial review is a statement of the programme’s offer; consult its current '+link('https://42systemicreview.org/contact','contact page')+' about a specific proposal.</p><p>'+link('/reading/systems-leadership-and-action/','Continue: when diagnosis changes who needs to act')+'</p></section>'
page('/reading/42-systemic-review/', '42 The Systemic Review: examining the diagnosis', body)

body = '<p>Systems leadership can include making inquiry and action possible when the patterns producing a problem cross organisational boundaries. This route develops '+link(leadership_url,'Benjamin P Taylor’s published argument')+' into questions for practice. It is an attributed position, not a consensus definition of the field.</p><section><h2>Start with something that keeps happening</h2><p>Describe the recurring experience in words that the people affected would recognise. Trace the decisions, rules, resource arrangements, interactions, and delays that help produce it. Test that explanation against another account. A map which many people recognise can still omit the people carrying its costs.</p><p>Compare '+atlas('concept_feedback')+', '+atlas('concept_boundary')+', and '+atlas('concept_modelling')+'.</p></section><section><h2>Follow the pattern to the authority</h2><p>Identify a concrete condition that could change: a referral rule, an approval threshold, a contract, a resource allocation, or the way competing obligations are settled. Find who can change it, what stops them, and whose cooperation they need. The person closest to the difficulty may know most about it while controlling very little of what maintains it.</p><p>Bring that person’s evidence to a decision in a form that shows the consequences and the available choices. Where nobody has sole authority, the practical work includes convening the parties who control different conditions and agreeing what each will change. An invitation to collaborate does not itself confer authority or settle a conflict of purpose.</p></section><section><h2>Distinguish an exception from a changed arrangement</h2><p>A senior intervention may help one person receive support. Follow the next comparable case. If it encounters the same barrier, the original intervention left the recurring mechanism largely intact. Useful learning includes finding the rule or relationship which allowed the exception, and deciding whether it should change for others.</p><p>Be precise about what was improved: one outcome, the handling of comparable cases, or the conditions producing those cases. These are different claims and need different evidence.</p></section><section><h2>Keep inquiry inside the action</h2><p>Agree what will change, who will act, when the effects should become visible, and what would justify revising the explanation. Check whether delay or risk moved somewhere else. Give affected people a route to challenge both the account and the change. Our own framing, commitments, and participation belong in that examination.</p><p>Continue through '+atlas('approach_family_systems_leadership')+', '+atlas('concept_purpose')+', '+link('/reading/42-systemic-review/','the 42 policy reviews')+', or '+link('/reading/orglens/','OrgLens and the limits of diagnostic reports')+'. More public sources are gathered in '+link('https://antlerboy.com/library/systems-leadership-change-practice/','the systems-leadership practice collection')+'.</p></section>'
page('/reading/systems-leadership-and-action/', 'Systems leadership: make inquiry actionable', body)

quick = '<article class="plain-panel wide" id="quick-contribution"><h2>Quick contribute</h2><p>A correction, question, missing source, or rough thought is enough. Send it straight to Benjamin’s review inbox.</p><form id="quickContributionForm"><label for="quickContributionText">Your contribution<textarea id="quickContributionText" name="text" rows="6" maxlength="6000" required placeholder="Write in ordinary language. Add a link if it helps."></textarea></label><label for="quickContributionEmail">Email address — optional, only for follow-ups<input id="quickContributionEmail" name="email" type="email" maxlength="254" autocomplete="email"></label><div style="position:absolute;left:-10000px;width:1px;height:1px;overflow:hidden" aria-hidden="true"><label>Leave this blank<input name="website" tabindex="-1" autocomplete="off"></label></div><p class="small">Your message and optional email are sent privately for review. Your email won’t appear in the atlas or the public submission queue. Nothing is added to the atlas automatically. Up to 6,000 characters.</p><button type="submit" class="primary">Send contribution</button><p id="quickContributionStatus" role="status" aria-live="polite"></p><noscript><p>This form needs JavaScript to confirm receipt. '+link('mailto:benjamin.taylor@redquadrant.com','Email Benjamin instead')+'.</p></noscript></form></article>'
script = '<script src="/assets/quick-contribute.js?v='+hashlib.sha256((D/'assets/quick-contribute.js').read_bytes()).hexdigest()[:12]+'" defer></script>'
page('/contribute/', 'Send a quick contribution', quick+'<p>For a structured proposal, '+link('/#view=contribute','use the full contribution page')+'. Public proposals and curator responses remain in '+link('/submissions/','the public record')+'.</p>', script)
p = D/'index.html'; text = p.read_text(encoding='utf-8')
text = re.sub(r'<!-- '+MARK+r'_quick -->.*?<!-- /'+MARK+r'_quick -->', '', text, flags=re.S)
text = text.replace('<div class="contribute-layout">', '<div class="contribute-layout"><!-- '+MARK+'_quick -->'+quick+'<!-- /'+MARK+'_quick -->', 1)
text = re.sub(r'<script src="/assets/quick-contribute.js[^>]*></script>', '', text)
text = text.replace('</body>', script+'</body>')
text = re.sub(r'<span id="releaseBadge">Release [^<]+</span>', '<span id="releaseBadge">Release 0.34</span>', text, count=1)
text = re.sub(r'assets/public-data.js\?v=[^"\s]+', 'assets/public-data.js?v=0.34', text)
text = text.replace('href="/updates/2026-10-18/"', 'href="/updates/2026-10-24/"', 1)
text = text.replace('<p>Use the form to prepare an email to Benjamin P Taylor. You can also submit a public GitHub issue. Contributions are reviewed before they are incorporated.</p>', '<p>Use Quick contribute for a private note, prepare an email with the detailed form, or submit a public GitHub issue. Contributions are reviewed before they are incorporated.</p>')
p.write_text(text, encoding='utf-8')

body = '<p>Recent sources are reconciled, three developed reading routes connect diagnosis to practice, and a new '+link('/contribute/','quick-contribution form')+' accepts plain text with an optional private follow-up email.</p><ul><li>'+link('/reading/orglens/','OrgLens: models, checks, and organisational judgement')+' — three lenses, inspected source modules, evaluation limits, and attribution.</li><li>'+link('/reading/42-systemic-review/','42 The Systemic Review')+' — its approach and three current applications.</li><li>'+link('/reading/systems-leadership-and-action/','Systems leadership: make inquiry actionable')+' — recurring patterns, authority, exceptions, and learning.</li></ul><section><h2>Events and source coverage</h2><p>The 24 October collection returned 271 listings, with 115 upcoming, from 36 checked sources. Nine sources yielded dated events; nine could not be collected. Source health, previously verified records, calendar identity, and the review queue are retained. Visit '+link('/events/','the maintained event map')+' for the current collection rather than treating these release counts as live totals.</p><p>Six public submission links were reconciled. Reading resources and undated announcements are kept separate from events; nothing is automatically accepted from a submitted link.</p></section><section><h2>SysCoI reading: nine posts accounted for</h2><p>Five reading leads are new. Four announcements link to existing resources, including the Ashby Laboratory. The overlapping date window avoids losing late posts from 18 October.</p>'
for p in P['posts']:
    body += '<article id="post-'+str(p['id'])+'" data-status="'+p['status']+'"><p class="meta">'+E(p['date'][:10])+' · '+('New discovery' if p['status']=='new_discovery' else 'Already represented')+'</p><h3>'+link(p['url'],p['title'])+'</h3><p>'+E(p['summary'])+'</p><p>'+(atlas('publication_syscoi_post_'+str(p['id'])) if p['status']=='new_discovery' else link(p['existing_route'],'Continue at the existing resource'))+'</p><ul>'+''.join('<li>'+link(u,u)+'</li>' for u in p['links'])+'</ul></article>'
body += '</section><section><h2>What remains open</h2><p>New connections record source-scoped uses of methods, concepts, or arguments. They remain candidates for editorial review. Full primary reading of every discovery, historical attribution disputes, exhaustive corpus work, and inaccessible event sources remain open. The source-owner-reviewed Systemic Evolution package is unchanged.</p><p>'+link('syscoi-review.json','SysCoI reconciliation')+' · '+link('events-review.json','Event collection account')+' · '+link('https://github.com/antlerboy/the-necessary-tangle/tree/main/sources/update-2026-10-24','Source packet and locators')+'</p></section>'
page('/updates/2026-10-24/', '24 October: current reading, practice, events, and contributions', body)
for name in ['syscoi-review.json','events-review.json']: (D/'updates/2026-10-24'/name).write_bytes((S/name).read_bytes())
for route in ['learning/index.html','reading-list.html','updates/index.html']:
    p = D/route; text = p.read_text(encoding='utf-8'); text = re.sub('<!-- '+MARK+' -->.*?<!-- /'+MARK+' -->','',text,flags=re.S)
    block = '<section><h2>'+link('/updates/2026-10-24/','24 October: current reading and practice')+'</h2><p>'+link('/reading/orglens/','OrgLens')+' · '+link('/reading/42-systemic-review/','42 policy reviews')+' · '+link('/reading/systems-leadership-and-action/','Systems leadership and action')+' · '+link('/contribute/','Quick contribute')+'. Five new SysCoI reading leads; four existing routes.</p></section>'
    text = text.replace('</main>', '<!-- '+MARK+' -->'+block+'<!-- /'+MARK+' --></main>', 1); p.write_text(text,encoding='utf-8')
for p in D.rglob('*.html'):
    text = p.read_text(encoding='utf-8')
    text = re.sub(r'href="/updates/2026-10-(?:07|08|13|18)/"(>Latest update</a>)', r'href="/updates/2026-10-24/"\1', text)
    p.write_text(text,encoding='utf-8')
p = D/'sitemap.xml'; text = p.read_text(encoding='utf-8')
for route in ['/reading/42-systemic-review/','/reading/systems-leadership-and-action/','/contribute/','/updates/2026-10-24/']:
    url = 'https://transduction.systems'+route
    if url not in text: text = text.replace('</urlset>', '<url><loc>'+url+'</loc><lastmod>'+DATE+'</lastmod></url></urlset>')
p.write_text(text,encoding='utf-8')
current = 'Current release: **0.34, 24 October 2026**. [Current reading, practice, events, and contributions](https://transduction.systems/updates/2026-10-24/). [Quick contribute](https://transduction.systems/contribute/).'
p = R/'README.md'; text = p.read_text(encoding='utf-8')
text = re.sub(r'<!-- current-31 -->.*?<!-- /current-31 -->', '<!-- current-31 -->\n'+current+'\n<!-- /current-31 -->', text, flags=re.S)
p.write_text(text,encoding='utf-8')
p = R/'CITATION.cff'; text = p.read_text(encoding='utf-8')
text = re.sub(r'^version:.*$', "version: '0.34'", text, flags=re.M)
text = re.sub(r'^date-released:.*$', "date-released: '2026-10-24'", text, flags=re.M); p.write_text(text,encoding='utf-8')
p = R/'CHANGELOG.md'; text = p.read_text(encoding='utf-8')
if '## 0.34 — 24 October 2026' not in text:
    text = text.replace('# Changelog', '# Changelog\n\n## 0.34 — 24 October 2026\n\nFive new SysCoI reading leads and four existing routes reconciled. Developed OrgLens and 42 guides, a systems-leadership action route, 21 source-scoped candidate connections, current events, and a quick plain-text contribution form with optional private follow-up email. Full source validation and the service/calendar tests pass; publication and live browser checks are recorded by the deployment workflow.\n', 1)
p.write_text(text,encoding='utf-8')
(R/'documentation/TANGLE_STATE.md').write_text(f'''# Current Tangle state

Last verified: 24 October 2026 — full source gate, current source review, private contribution service, and event/calendar checks. Exact publication identity and final live reader checks are recorded by deployment.json and the Publish workflow.

Public site: https://transduction.systems/

Release 0.34. {metrics['public_entries']} public entries, {len(d['edges'])} recorded edges, {len(d['sources'])} sources, and {len(d['profiles'])} profiles. These are dataset counts, not evidence of universal coverage or human acceptance. Machine quality snapshot: data/relationship-quality.json.

The source packet is sources/update-2026-10-24/PACKET.md. Nine SysCoI posts from the overlapping 18–24 October window are reconciled: five new leads and four existing routes. OrgLens is inspected at revision {commit}; its three implemented lenses, evidence checks, and fictional evaluation remain distinct. 42 has an attributed programme guide and three paper routes. The systems-leadership guide develops Taylor's public argument into practical questions about patterns, authority, and action. New relationships remain source-scoped candidates.

Quick contributions are received at /api/contributions on the existing events service. The separate tangle_contributions table is private to the owner; optional email is only for follow-ups and is excluded from public queues and atlas data. The form clears only after a durable receipt. Existing event submissions, analytics, and legacy PSTA redirects are preserved. Review the private inbox through the owner’s Sites database tools; do not publish its contents automatically.

The 24 October collection has 271 event listings, 115 upcoming, from 36 checked sources. Nine sources yielded dated events and nine failed. Six public link submissions were reconciled. The maintained systemsmap workflow owns live collection data; calendar subscription identity and explicit source failures remain visible.

The full historical corpus reviews, exact inventory of private map collections, historical attribution disputes, real-organisation OrgLens effectiveness, and independent exercise QA remain open. Public-safe sources only; the source-owner-reviewed Systemic Evolution package is unchanged. Curator: Benjamin P Taylor. No external correspondence, access, membership, or invitations changed.
''',encoding='utf-8')
(R/'documentation/NEXT_WORK.md').write_text('''# Next work

Status: release 0.34 implementation and source validation complete. Publication and live acceptance are determined by deployment.json and the Publish workflow. No continuing research packet is automatically active.

## Outcome

Complete the authorised 24 October maintenance release and verify its exact deployed revision. Source packet: sources/update-2026-10-24/PACKET.md.

## In scope

Current SysCoI reconciliation, source-led OrgLens/42/systems-leadership guides, current events, quick contributions with private optional email, release metadata, and bounded public-estate checks. Resolve only named acceptance failures during publication.

## Out of scope

No private teaching material, correspondence, client sources, permissions changes, unverified influence, wholesale corpus-completion claims, or changes to the source-owner comparator.

## Acceptance checks

make validate; scripts/test_update_34_browser.js at desktop/mobile widths; event/calendar and contribution-service tests; unchanged comparator checksums; exact live deployment identity and changed reader routes. Optional contact data must remain absent from all public APIs.

## Stop conditions

Stop after successful publication and live checks. Historical corpus research and disputed claims need a finite source cohort and explicit completion criteria. Review new private contributions under the curator’s responsibility before public incorporation.

## Model route

One agent. One implementation and verification pass, with a corrective pass tied to named failures. No delegated research or publishing.
''',encoding='utf-8')
print('Applied 0.34: nine posts reconciled, five new leads, source-led guides, candidate claims, and quick contributions.')
