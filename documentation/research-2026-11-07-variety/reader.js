'use strict';
const $=id=>document.getElementById(id),e=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])),pct=n=>(100*n).toFixed(2)+'%',bits=n=>n.toFixed(5)+' bits';
function render(){
 const q=Number($('rare').value)/100,task=$('task').value,d=VarietyModel.analyse(q,task);$('rare-value').textContent=pct(q).replace('.00','');
 $('states').innerHTML=['A','B','C','D'].map((s,i)=>`<tr><th scope="row">${s}</th><td>${pct(d.probabilities[i])}</td><td>${e(d.actions[i])}</td><td>${e(d.rows.find(x=>x.id==='poor').labels[i])}</td><td>${e(d.rows.find(x=>x.id==='task_preserving').labels[i])}</td></tr>`).join('');
 $('input-entropy').textContent=bits(d.inputEntropy);
 const names={full:'Full state distinction',poor:'Poor grouping',task_preserving:'Default-task grouping'};
 $('results').innerHTML=d.rows.map(r=>`<tr data-model="${r.id}"><th scope="row">${names[r.id]}</th><td>${r.count}</td><td>${bits(r.logCount)}</td><td>${bits(r.entropy)}</td><td>${bits(r.conditional)}</td><td>${r.taskPreserved?'Yes':'No · '+r.ambiguous+' incompatible group'+(r.ambiguous===1?'':'s')}</td><td>${pct(r.bestSuccess)}</td></tr>`).join('');
 const good=d.rows.find(r=>r.id==='task_preserving'),poor=d.rows.find(r=>r.id==='poor');
 $('finding').textContent=task==='shared'?`The default-task grouping preserves every required action. Its output entropy is ${bits(good.entropy)}; the poor grouping's is ${bits(poor.entropy)}. The poor grouping's best expected correctness is ${pct(poor.bestSuccess)}, with incompatible actions still inside ‘other’.`:`For this task, the fixed default-task grouping ${good.taskPreserved?'preserves every required action':'loses a required distinction'}. The poor grouping ${poor.taskPreserved?'also preserves the task':'contains incompatible actions'}. The probabilities change expected scores; the pairwise sufficiency test depends on the grouping and required actions.`;
 const s=VarietyModel.supplementation($('extra').checked);$('pattern-count').textContent=s.count;$('pattern-log').textContent=bits(s.logCount);$('patterns').textContent=s.patterns.join('   ');$('supplement-assumption').textContent=s.assumption;
 globalThis.currentVarietyResult=d;
}
$('rare').addEventListener('input',render);$('task').addEventListener('change',render);$('extra').addEventListener('change',render);$('reset').addEventListener('click',()=>{$('rare').value=3;$('task').value='shared';$('extra').checked=false;render();$('rare').focus();});
$('profile-cards').innerHTML=VarietyPacket.profile_candidates.map(p=>`<article><h3>${e(p.proposed_profile.title)}</h3><p>${e(p.proposed_profile.summary)}</p><p class="small">Located new facts: ${p.new_source_fact_ids.map(id=>`<a href="#${id}">${id}</a>`).join(' · ')}</p><p><strong>Still open:</strong> ${e(p.remaining_checks.join('; '))}.</p></article>`).join('');
$('facts').innerHTML=VarietyPacket.source_facts.map(f=>`<article id="${f.id}"><h3>${f.id}</h3><p>${e(f.text)}</p><p class="small">${e(f.locator)} · <a href="#source-${e(f.source)}">Source</a></p></article>`).join('');
$('source-list').innerHTML=VarietyPacket.sources.map(s=>`<article id="source-${e(s.id)}"><h3>${e(s.author)} · ${e(s.title)}</h3><p>${e(s.date)}. <a href="${e(s.url)}">Primary text</a>.</p><p class="small">${e(s.locator)}. ${e(s.access)}</p></article>`).join('');render();
