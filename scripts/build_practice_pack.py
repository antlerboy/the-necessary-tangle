#!/usr/bin/env python3
"""Build the original, source-labelled systems practice pages without a framework."""
from __future__ import annotations
import html
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'sources/practice-pack'
DEST = ROOT / 'docs/systems-thinking/practice'
URL = 'https://transduction.systems/systems-thinking/practice/'
DATE = '2026-09-07'


def esc(value):
    return html.escape(str(value), quote=True)


def load_content():
    labs = []
    for path in sorted(SOURCE.glob('[0-9][0-9]-*.json')):
        labs.extend(json.loads(path.read_text(encoding='utf-8')))
    resources = {}
    for path in sorted(SOURCE.glob('resources*.json')):
        for row in json.loads(path.read_text(encoding='utf-8')):
            resources[row['id']] = dict(row, checked_on=DATE)
    for identity, changes in json.loads((SOURCE/'resource-corrections.json').read_text()).items():
        resources[identity].update(changes)
    standards = json.loads((SOURCE/'standards.json').read_text())
    return labs, resources, standards


def paragraph(text, cls=''):
    return '<p'+(' class="'+esc(cls)+'"' if cls else '')+'>'+esc(text)+'</p>'


def listing(items):
    return '<ul>'+''.join('<li>'+esc(x)+'</li>' for x in items)+'</ul>'


def page(title, body, sub='', lab=''):
    base = '../' if sub else './'
    canonical = URL + (sub+'/' if sub else '')
    return '''<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light dark"><title>'''+esc(title)+''' | The Necessary Tangle</title><meta name="description" content="Original systems-method cases, modelling checks, worked comparisons and source-labelled free and paid resources."><link rel="canonical" href="'''+canonical+'''"><link rel="stylesheet" href="'''+base+'''assets/practice.css"><link rel="icon" href="https://transduction.systems/favicon.svg" type="image/svg+xml"></head><body data-lab-id="'''+esc(lab)+'''"><a class="skip" href="#main">Skip to content</a><header><a class="brand" href="https://transduction.systems/">The Necessary Tangle</a><nav aria-label="Practice navigation"><a href="https://transduction.systems/systems-thinking/">Systems thinking</a><a href="'''+base+'''index.html">Practice home</a><a href="'''+base+'''coverage/index.html">Standards coverage</a><a href="'''+base+'''resources/index.html">Resources</a><a href="'''+base+'''tutor-notes/index.html">Using the pack</a></nav></header><main id="main">'''+body+'''</main><footer><p>Original practice material for The Necessary Tangle. Curated by <a href="https://antlerboy.com/">Benjamin P Taylor</a>. Published 7 September 2026.</p><p>Original text: <a href="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA 4.0</a>. Linked resources retain their own terms. This pack is not endorsed by SCiO, the Open University or other source providers, and is not an accreditation decision.</p><p><a href="https://transduction.systems/submissions/">Suggest a correction</a> · <a href="'''+base+'''downloads/systems-methods-practice.zip">Download the offline pack</a></p></footer><a id="openUpdates" class="feedback-dot" href="https://github.com/antlerboy/the-necessary-tangle/issues/2" aria-label="Open updates"></a><script src="'''+base+'''assets/practice.js" defer></script></body></html>'''


def write_page(sub, text):
    path = DEST/sub/'index.html' if sub else DEST/'index.html'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')


def resource_card(row, compact=False):
    out = '<article class="resource" id="'+esc(row['id'])+'"><h'+('3' if compact else '2')+'><a href="'+esc(row['url'])+'">'+esc(row['title'])+'</a></h'+('3' if compact else '2')+'>'
    out += paragraph(row['cost']+' | '+row['kind'], 'meta')
    out += paragraph(row['use'])
    out += '<details><summary>What was checked, and what was not</summary>'+paragraph(row['check'])+paragraph('Research date: '+row['checked_on'], 'meta')+'</details></article>'
    return out


def lab_card(lab, base=''):
    return '<article class="lab-card" data-lab-card data-search="'+esc(' '.join([lab['title'],lab['standard'],*lab['ksb']]).lower())+'">'+paragraph(lab['section']+' | about '+str(lab['time'])+' minutes', 'eyebrow')+'<h3><a href="'+base+lab['id']+'/index.html">'+esc(lab['title'])+'</a></h3>'+paragraph(lab['focus'])+paragraph('Free case, worked answers, checks and a second attempt.', 'meta')+'</article>'


def model_check(lab):
    identity = lab['id']
    if identity == 'system-dynamics':
        cells = ''.join('<label>End of week '+str(i+1)+' (cases)<input type="number" min="0" step="1" inputmode="numeric" name="backlog-'+str(i+1)+'" data-expected="'+str(n)+'" data-label="Week '+str(i+1)+'"></label>' for i,n in enumerate([42,44,40,36]))
        return '<section class="model"><h2>Check your calculated model</h2><p>Calculate the four backlogs before using this check. It tests the supplied accounting model, not a real service.</p><form data-model-check>'+cells+'<button type="submit">Check my four backlogs</button><p role="status" data-model-result></p></form></section>'
    if identity == 'interactive-management':
        matrix = ['10111','01111','00111','00011','00001']
        table = '<table><caption>Reachability matrix including each condition itself</caption><thead><tr><th scope="col">From / to</th>'+''.join('<th scope="col">'+c+'</th>' for c in 'ABCDE')+'</tr></thead><tbody>'
        for i,a in enumerate('ABCDE'):
            table += '<tr><th scope="row">'+a+'</th>'
            for j,b in enumerate('ABCDE'):
                table += '<td><input type="checkbox" name="matrix-'+a+b+'" data-expected="'+matrix[i][j]+'" data-label="'+a+' reaches '+b+'" aria-label="'+a+' reaches '+b+'"></td>'
            table += '</tr>'
        table += '</tbody></table>'
        return '<section class="model"><h2>Build and check the reachability matrix</h2><p>Tick a cell when the row condition reaches the column condition. Include the identity diagonal. A missing tick means zero, not an unanswered cell.</p><form data-model-check>'+table+'<button type="submit">Check my matrix</button><p role="status" data-model-result></p></form></section>'
    if identity == 'viable-system-model':
        rows = [('Local advice delivery','1'),('Interpreter scheduling protocol','2'),('Negotiating shared resources','3'),('Direct agreed sampling of casework','3*'),('Exploring future demand','4'),('Identity and present/future policy balance','5')]
        fields = ''
        for i,(label,expected) in enumerate(rows):
            fields += '<label>'+esc(label)+'<select name="vsm-'+str(i)+'" data-expected="'+expected+'" data-label="'+esc(label)+'"><option value="">Choose a function</option>'+''.join('<option value="'+v+'">System '+v+'</option>' for v in ['1','2','3','3*','4','5'])+'</select></label>'
        return '<section class="model"><h2>Check the case functions</h2><p>Match activities, not people or job grades. This checks the supplied case; other organisations require evidence of what each activity does.</p><form data-model-check>'+fields+'<button type="submit">Check function mapping</button><p role="status" data-model-result></p></form></section>'
    return ''


def render_lab(lab, resources):
    body = paragraph(lab['section']+' | about '+str(lab['time'])+' minutes | free', 'eyebrow')+'<h1>'+esc(lab['title'])+'</h1>'+paragraph(lab['focus'], 'lead')
    body += '<p class="meta">Framework link: '+esc(lab['standard'])+'. Apprenticeship practice links: '+', '.join('<a href="../coverage/index.html#'+k+'">'+k+'</a>' for k in lab['ksb'])+'.</p>'
    body += '<details class="scope"><summary>What this exercise can and cannot establish</summary>'+paragraph(lab['scope'])+paragraph('This is original learning material, not a reproduced official course. Mechanical checks have determinate answers within the stated case. Worked comparisons for open judgements show defensible reasoning, not the only possible model. Specialist pedagogical review is not recorded.')+'</details>'
    body += '<nav class="jump" aria-label="On this practice page"><a href="#case">Case</a><a href="#work">Work through it</a><a href="#checks">Checks</a><a href="#repair">Repair a model</a><a href="#retry">Try again</a><a href="#sources">Sources</a></nav>'
    body += '<section id="case"><h2>The case</h2>'+paragraph(lab['scenario'])+'</section>'
    body += '<section id="work"><h2>Work through it</h2><p>Use paper, your own drawing tool or the notes below. Attempt each step before opening its comparison. Describe a diagram in words when that is more accessible.</p><ol class="steps">'
    for i,step in enumerate(lab['rounds'],1):
        body += '<li><h3>'+str(i)+'. '+esc(step['task'])+'</h3>'+paragraph('Produce: '+step['output'])+'<label>Your attempt for step '+str(i)+'<textarea name="step-'+str(i)+'" rows="4" placeholder="Record your model, reasoning or a description of your drawing."></textarea></label><details class="answer"><summary>Compare your work for step '+str(i)+'</summary>'+paragraph(step['answer'])+'</details></li>'
    body += '</ol></section>'+model_check(lab)
    body += '<section id="checks"><h2>Check the basic distinctions</h2><p>These checks test the supplied case, not your overall competence. Open answers and model variants still need your judgement.</p>'
    for i,check in enumerate(lab['checks'],1):
        body += '<form class="check" data-check data-correct="'+str(check['correct'])+'" data-explanation="'+esc(check['explanation'])+'"><fieldset><legend>'+str(i)+'. '+esc(check['q'])+'</legend>'
        for j,option in enumerate(check['options']):
            body += '<label class="option"><input type="radio" name="question-'+str(i)+'" value="'+str(j)+'"> <span>'+esc(option)+'</span></label>'
        body += '</fieldset><button type="submit">Check answer '+str(i)+'</button><p class="result" data-result role="status"></p><details class="answer"><summary>Answer and reasoning '+str(i)+'</summary>'+paragraph(check['options'][check['correct']])+paragraph(check['explanation'])+'</details></form>'
    body += '</section><section id="repair"><h2>Repair a defective model or claim</h2><blockquote>'+esc(lab['repair']['broken'])+'</blockquote><label>Your repair<textarea name="repair" rows="4"></textarea></label><details class="answer"><summary>Compare your repair</summary>'+paragraph(lab['repair']['fix'])+'</details></section>'
    body += '<section id="retry"><h2>Try a changed case before looking</h2>'+paragraph(lab['retry']['task'])+'<label>Your second attempt<textarea name="retry" rows="4"></textarea></label><details class="answer"><summary>Compare the changed case</summary>'+paragraph(lab['retry']['answer'])+'</details></section>'
    body += '<section id="review"><h2>Review the process, not just the score</h2>'+listing(lab['criteria'])+'<p>A different model can be defensible when its purpose, assumptions and reasoning are explicit. A contradiction, incorrect unit, invented fact or unacknowledged change of purpose needs repair. Keep both your first attempt and revision.</p><label>What changed in your understanding?<textarea name="reflection" rows="4"></textarea></label><label>What would you need to test with people in a real situation?<textarea name="transfer" rows="3"></textarea></label><label class="option"><input type="checkbox" name="reviewed"> I have compared my attempt and recorded a revision. This is my own review, not accreditation.</label></section>'
    body += '<section class="storage"><h2>Keep your attempt</h2><p>No sign-in or submission is required. Notes are not sent by this practice tool. Use fictional information, not identifiable client or learner data. Saving stores this page\'s attempt only in this browser; clearing browser data can remove it. Export a copy to keep it elsewhere.</p><div class="actions"><button type="button" data-save>Save in this browser</button><button type="button" data-export>Export my attempt</button><button type="button" data-reset>Clear this attempt</button><button type="button" data-print>Print this page</button></div><p role="status" data-storage-status></p><noscript><p>JavaScript is off. The cases, comparisons and answer keys still work. Use paper or your browser\'s print/save function to keep your attempt; the interactive checks and local notes controls need JavaScript.</p></noscript></section>'
    body += '<section id="sources"><h2>External resources and their limits</h2><p>The complete original case above is free. Links below distinguish exercises from explanations, recordings, software and paid study. Reading a page or drawing in a tool is not itself a model check.</p>'
    for identity in dict.fromkeys(lab['resources']+lab['paid']):
        body += resource_card(resources[identity], compact=True)
    body += '</section><p><a href="../index.html">Choose another practice area</a> · <a href="../worksheets/index.html#'+lab['id']+'">Task-only version</a> · <a href="../answers/index.html#'+lab['id']+'">Worked-answer version</a></p>'
    return page(lab['title'], body, lab['id'], lab['id'])


def render_home(labs):
    body = paragraph('Systems thinking | Basic practice', 'eyebrow')+'<h1>Systems methods practice</h1><p class="lead">Work through a fictional case, then compare your model and reasoning with a worked answer.</p><p>There are 26 free practice pages: all 13 approaches and three theory rows in the public SCiO framework, plus ten supporting areas of systemic inquiry and intervention. You do not need to complete every approach for the apprenticeship. Agree your selection and depth with your tutor.</p><div class="actions"><a class="button" href="systems-concepts/index.html">Start with a systems map</a><a class="button secondary" href="#methods">Find a method</a><a href="downloads/systems-methods-practice.zip">Download the whole pack</a></div>'
    body += '<section><h2>Use the external exercises that genuinely help</h2><div class="grid"><article class="lab-card"><h3><a href="https://www.open.edu/openlearn/digital-computing/managing-complexity-a-systems-approach-introduction/content-section-9.3">Open University: defective maps, your own map and worked comparisons</a></h3><p>Start with SAQ 3, then Activities 19-22. Attempt the task before opening the answer or comparing the author\'s map. The historical case is for practice, not current policy advice.</p></article><article class="lab-card"><h3><a href="https://ocw.mit.edu/courses/15-988-system-dynamics-self-study-fall-1998-spring-1999/pages/assignments/">MIT: system dynamics assignments with paired solutions</a></h3><p>Start with the early problem sets and their solution files. Some software instructions are historical; the questions and solutions are distinct from simply playing a simulation.</p></article></div><p>Other resources often supply only part of the practice process. Each page below therefore includes its own scenario, explicit outputs, checks, a defective model to repair, a changed case and answers. <a href="resources/index.html">See the checked resource register, including paid routes and access problems.</a></p></section>'
    body += '<section><h2>How to use a page</h2><p>Read the case and state your assumptions. Make the requested model before opening its comparison. Use the mechanical checks where available, then repair your work and try the changed case. Keep a note of why your answer changed. For open questions, compare the reasoning rather than copying the picture.</p><p>This is low-stakes rehearsal, not an end-point assessment or evidence that you have already worked effectively with people in an organisation. <a href="coverage/index.html">The coverage register shows those limits.</a></p></section>'
    body += '<section id="methods"><h2>Choose a practice area</h2><label class="filter">Find a method, framework term or KSB code<input type="search" data-filter placeholder="For example SSM, variety, K2 or inquiry"></label><p data-filter-count role="status">26 practice pages.</p>'
    for section in ['Foundations','Core methods','Systemic intervention']:
        body += '<section class="lab-group"><h3>'+section+'</h3><div class="grid">'
        for lab in labs:
            if lab['section'] == section:
                body += lab_card(lab).replace('<h3>','<h4>').replace('</h3>','</h4>')
        body += '</div></section>'
    body += '</section><section><h2>For a tutor or practice partner</h2><p>Ask to see the first model, the revision and the reason for the change. Check for purpose drift, missing boundaries, invented evidence and incorrect notation. Do not turn a worked comparison into the only permitted answer.</p><p><a href="tutor-notes/index.html">Tutor and learner guidance</a> · <a href="worksheets/index.html">All task sheets without answers</a> · <a href="answers/index.html">All worked comparisons</a> · <a href="coverage/index.html">Standards mapping</a></p></section>'
    return page('Systems methods practice', body)


def render_coverage(labs, standards, resources):
    byid = {x['id']:x for x in labs}
    link = lambda identity: '<a href="../'+identity+'/index.html">'+esc(byid[identity]['title'])+'</a>'
    body = '<h1>Standards coverage and limits</h1>'+paragraph(standards['crosswalk_status'], 'lead')
    body += '<p>Sources: <a href="'+esc(resources['scio-portfolio']['url'])+'">'+esc(standards['scio_version'])+'</a> and <a href="'+resources['st0787']['url']+'">'+esc(standards['apprenticeship_version'])+'</a>. Checked 7 September 2026. This mapping is editorial, not a replacement for either standard.</p><p>Apprenticeship K2 requires working knowledge of at least three approaches, including at least two of CSH, SSM, System Dynamics and VSM. This wider library offers choice; it does not make all thirteen compulsory.</p>'
    for title, identities in [('SCiO approaches',standards['core_order']),('SCiO theory rows',standards['theory_order'])]:
        body += '<section><h2>'+title+'</h2><div class="table-wrap"><table><thead><tr><th scope="col">Framework row</th><th scope="col">Free practice</th><th scope="col">Depth and limit</th></tr></thead><tbody>'
        for identity in identities:
            lab=byid[identity]
            body += '<tr><th scope="row">'+esc(lab['standard'])+'</th><td>'+link(identity)+'</td><td>'+esc(lab['scope'])+'</td></tr>'
        body += '</tbody></table></div></section>'
    body += '<section><h2>Systemic intervention and inquiry</h2>'+paragraph(standards['supporting_scope'])+'<ul>'
    for lab in labs:
        if lab['section']=='Systemic intervention':
            body += '<li>'+esc(lab['standard'])+': '+link(lab['id'])+'</li>'
    body += '</ul></section><section><h2>Every apprenticeship KSB: practice contribution, not a pass claim</h2><p>Links indicate opportunities to rehearse. All skills require application and evidence in context. Behaviours require observation over time. K4 also needs sector-specific legal, professional and safeguarding study.</p>'
    for code, label in standards['ksb'].items():
        matches=[lab for lab in labs if code in lab['ksb']]
        body += '<article class="coverage-row" id="'+code+'"><h3>'+code+': '+esc(label)+'</h3><p>'+', '.join(link(lab['id']) for lab in matches)+'</p>'
        status = 'Reflection prompt only. Real behaviour cannot be scored by this page.' if code.startswith('B') else ('Case rehearsal only. Transfer and observed application remain to be demonstrated.' if code.startswith('S') else 'Introductory practice and source route, not exhaustive knowledge coverage.')
        body += paragraph(status,'meta')+'</article>'
    body += '</section><section><h2>Duty cross-reference</h2><p>The numbered duties remain defined in the official standard. These links identify relevant rehearsal; they do not claim completion of the duty.</p><ul>'
    for duty, identities in standards['duties'].items():
        body += '<li>Duty '+duty+': '+', '.join(link(x) for x in identities)+'</li>'
    body += '</ul></section><section><h2>What this pack does not supply</h2>'+listing(standards['outside_scope'])+'</section><p><a href="../assets/coverage.json" download>Download the machine-readable coverage register</a></p>'
    return page('Standards coverage',body,'coverage')


def render_aggregate(labs, answers=False):
    title = 'Worked comparisons and answer keys' if answers else 'Task sheets without answers'
    body = '<h1>'+title+'</h1><p>Original fictional cases for basic practice. Open judgements have defensible alternatives. Use the separate comparison pages after making your own attempt.</p><p><button type="button" data-print>Print this collection</button></p><nav aria-label="Practice areas">'+listing([])+'</nav>'
    body = body.replace(listing([]),'<ul>'+''.join('<li><a href="#'+lab['id']+'">'+esc(lab['title'])+'</a></li>' for lab in labs)+'</ul>')
    for lab in labs:
        body += '<section class="print-case" id="'+lab['id']+'"><h2>'+esc(lab['title'])+'</h2>'+paragraph(lab['scope'],'meta')+paragraph(lab['scenario'])+'<ol>'
        for step in lab['rounds']:
            body += '<li>'+paragraph(step['task'])+paragraph('Produce: '+step['output'])+(paragraph(step['answer']) if answers else '<div class="writing-space" aria-label="Space for your attempt"></div>')+'</li>'
        body += '</ol><h3>Checks</h3><ol>'
        for q in lab['checks']:
            body += '<li>'+paragraph(q['q'])+listing(q['options'])+(paragraph('Answer: '+q['options'][q['correct']]+'. '+q['explanation']) if answers else '')+'</li>'
        body += '</ol><h3>Repair</h3>'+paragraph(lab['repair']['broken'])+(paragraph(lab['repair']['fix']) if answers else '<div class="writing-space"></div>')+'<h3>Changed case</h3>'+paragraph(lab['retry']['task'])+(paragraph(lab['retry']['answer']) if answers else '<div class="writing-space"></div>')+'<h3>Review criteria</h3>'+listing(lab['criteria'])+'</section>'
    return page(title,body,'answers' if answers else 'worksheets')


def render_tutor():
    body='''<h1>Using the practice pack</h1><p class="lead">The useful evidence is the model, the correction and the reason for changing it.</p><section><h2>For a learner</h2><p>Choose one approach with your tutor. Read only the case and task first. Use paper, text or your preferred drawing tool. State the purpose, boundary, assumptions and notation. Keep the first attempt. Open a comparison only after attempting the step, and record a revision. Then do the changed case without copying the first answer.</p><p>The suggested times are practice timeboxes, not measured completion guarantees. Pause where needed. You can use the task-only collection offline, and a practice partner can hold the answer key.</p></section><section><h2>What the feedback means</h2><p>A calculation, unit, named function or specified relation can have a determinate answer within a fictional case. The check can identify a mismatch. It cannot determine whether your chosen purpose is legitimate, whether people agree, or whether the method works in your organisation.</p><p>For an open answer, ask whether the reasoning follows its purpose, whether the model uses the method coherently, whether observations and interpretations are separated, and whether alternatives and exclusions are visible. A different answer is not automatically wrong. An unsupported assertion is not rescued by calling it another perspective.</p></section><section><h2>For a tutor or peer</h2><p>Use a short teach-back: ask the learner to explain a link, a boundary, an omitted activity or a changed assumption. Give them a fresh variation and see what they revise. Mark a specific technical defect where there is one. For a defensible alternative, record the assumptions that make it work.</p><p>Use three outcomes: ready for another basic case; revise a named technical point; or needs guided practice. These are local learning judgements, not professional accreditation. Ask for real-world evidence separately and use the actual programme assessment requirements.</p></section><section><h2>Accessibility and privacy</h2><p>Every case, question, comparison and answer is ordinary HTML and can be read without JavaScript. A text description is accepted as an alternative to drawing or physical positioning. Interactive checks, browser saving and export need JavaScript. No account is required by this pack.</p><p>Use fictional information in the notes. The practice script does not transmit answers. Saving is limited to this browser and can fail when storage is blocked. Export a copy rather than relying on browser storage as a permanent record. External sites have their own access and privacy terms.</p></section><section><h2>Research and review status</h2><p>External links were researched on 7 September 2026. Each record states whether the exercise, page, listing or access route was inspected. A paid course description is not evidence that its exercises or tutor feedback were tested. A source access problem is recorded rather than silently presented as a working exercise.</p><p>The cases and comparisons are original material prepared with AI assistance for this publication. The build includes deterministic checks of the numerical examples, coverage and page behaviour. No independent specialist pedagogical review or provider endorsement is claimed. Send a specific correction through the site's feedback route; preserve the case, disputed step and proposed repair.</p></section><section><h2>Moving beyond rehearsal</h2><p>Before using a method with people, establish your remit, competence, consent, data handling and sector-specific duties. Agree what the model is for and how participants can challenge it. Transfer is a new inquiry, not permission to impose a worked example on a real situation.</p><p>Do not use completion of these pages as proof of sustained collaboration, resilience, ethical conduct, change implementation or level-7 competence. The pack supplies a place to practise the basics and expose mistakes before that work.</p></section>'''
    return page('Using the practice pack',body,'tutor-notes')


def main():
    labs, resources, standards = load_content()
    DEST.mkdir(parents=True,exist_ok=True)
    (DEST/'assets').mkdir(exist_ok=True)
    for name in ['practice.css','practice.js']:
        shutil.copyfile(SOURCE/name,DEST/'assets'/name)
    for lab in labs:
        write_page(lab['id'],render_lab(lab,resources))
    write_page('',render_home(labs))
    write_page('coverage',render_coverage(labs,standards,resources))
    body='<h1>Checked resources: free practice and paid routes</h1><p class="lead">A resource must do more than describe a method to provide self-checking practice. The record below says what each link actually supplies and what was inspected.</p><p>Every practice page in this pack has a free original case and answers. Paid links are optional routes to more study or supported practice; no purchase has been made on your behalf. Prices and access can change. No affiliate links are used.</p>'
    body += ''.join(resource_card(r) for r in resources.values())
    write_page('resources',page('Checked practice resources',body,'resources'))
    write_page('worksheets',render_aggregate(labs))
    write_page('answers',render_aggregate(labs,True))
    write_page('tutor-notes',render_tutor())
    payload={'version':'1.0','checked_on':DATE,'labs':labs,'resources':list(resources.values()),'standards':standards}
    (DEST/'assets/pack.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
    coverage=dict(standards,labs=[{'id':x['id'],'standard':x['standard'],'ksb':x['ksb'],'scope':x['scope']} for x in labs])
    (DEST/'assets/coverage.json').write_text(json.dumps(coverage,ensure_ascii=False,indent=2)+'\n')
    print('Built practice pack:',len(labs),'labs,',len(resources),'resource routes.')


if __name__=='__main__':
    main()
