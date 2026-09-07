/* Original practice controls: no analytics, account, API or answer transmission. */
(function () {
  'use strict';
  function queue(initial, arrivals, capacities, reopen) {
    reopen = reopen || 0;
    if (![initial, arrivals, reopen].every(Number.isFinite) || initial < 0 || arrivals < 0 || reopen < 0 || reopen > 1 || !Array.isArray(capacities) || capacities.some(x => !Number.isFinite(x) || x < 0)) throw new Error('Invalid model inputs');
    let stock = initial;
    return capacities.map(capacity => { const done = Math.min(capacity, stock + arrivals); stock += arrivals - done + reopen * done; return stock; });
  }
  function closure(matrix) {
    const n = matrix.length;
    if (!n || matrix.some(row => row.length !== n || row.some(v => v !== 0 && v !== 1))) throw new Error('Expected a square binary matrix');
    const out = matrix.map((row,i) => row.map((v,j) => i === j ? 1 : v));
    for (let k=0;k<n;k++) for(let i=0;i<n;i++) for(let j=0;j<n;j++) out[i][j] = out[i][j] || (out[i][k] && out[k][j]) ? 1 : 0;
    return out;
  }
  if (typeof module !== 'undefined' && module.exports) module.exports = {queue, closure};
  if (typeof document === 'undefined') return;
  const body = document.body;
  const lab = body.dataset.labId;
  const key = 'necessary-tangle-practice-v1:' + lab;
  const fields = () => Array.from(document.querySelectorAll('main textarea[name],main input[name],main select[name]'));
  const status = text => { const node=document.querySelector('[data-storage-status]'); if(node) node.textContent=text; };
  const readAttempt = () => fields().map(el => ({name:el.name, type:el.type, value:el.value, checked:!!el.checked}));
  function restore(rows) {
    if (!Array.isArray(rows)) return;
    const current = fields();
    rows.forEach(row => { const el=current.find(x => x.name===row.name && (x.type!=='radio' || x.value===row.value)); if(!el)return; if(el.type==='checkbox'||el.type==='radio')el.checked=!!row.checked; else el.value=String(row.value ?? ''); });
  }
  if (lab) {
    try { const saved=localStorage.getItem(key); if(saved){restore(JSON.parse(saved).fields);status('Restored the attempt saved in this browser.');} } catch (_) { status('Browser storage is unavailable or unreadable. You can still work and export your attempt.'); }
  }
  document.querySelectorAll('[data-check]').forEach(form => form.addEventListener('submit', event => {
    event.preventDefault();
    const selected=form.querySelector('input[type=radio]:checked');
    const result=form.querySelector('[data-result]');
    if(!selected){result.textContent='Choose an answer first. No answer has been marked.';return;}
    const right=selected.value===form.dataset.correct;
    result.textContent=(right?'This matches the supplied case. ':'This does not match the supplied case. ')+form.dataset.explanation;
    result.dataset.outcome=right?'correct':'revise';
  }));
  document.querySelectorAll('[data-model-check]').forEach(form => form.addEventListener('submit', event => {
    event.preventDefault();
    const inputs=Array.from(form.querySelectorAll('[data-expected]'));
    const missing=inputs.filter(el => el.type!=='checkbox' && el.value==='');
    const result=form.querySelector('[data-model-result]');
    if(missing.length){result.textContent='Complete all model entries before checking. Missing: '+missing.map(x=>x.dataset.label).join(', ')+'.';return;}
    const wrong=inputs.filter(el => (el.type==='checkbox'?(el.checked?'1':'0'):el.value)!==el.dataset.expected);
    result.textContent=wrong.length?'Revise '+wrong.length+' model entries: '+wrong.map(el=>el.dataset.label+' should be '+el.dataset.expected).join('; ')+'. Use the worked comparison to inspect why.':'All '+inputs.length+' entries match the supplied model. Explain the relationships and assumptions before treating the exercise as understood.';
    result.dataset.outcome=wrong.length?'revise':'correct';
  }));
  document.querySelectorAll('[data-save]').forEach(button => button.addEventListener('click', () => {
    try {localStorage.setItem(key,JSON.stringify({version:1,lab,savedAt:new Date().toISOString(),fields:readAttempt()}));status('Saved only in this browser. Export a copy for a more durable record.');}
    catch (_) {status('Saving failed because browser storage is unavailable or full. Export your attempt instead.');}
  }));
  document.querySelectorAll('[data-export]').forEach(button => button.addEventListener('click', () => {
    const title=document.querySelector('h1').textContent;
    let text='# '+title+'\n\nPractice attempt exported '+new Date().toISOString()+'\n\nThis is a learner record, not an assessment or accreditation.\n\n';
    fields().forEach(el => {if(el.type==='radio'&&!el.checked)return; const value=el.type==='checkbox'?(el.checked?'checked':'not checked'):el.value; const label=el.closest('label'); const readable=label?label.textContent.trim():el.dataset.label||el.name;text+='## '+readable+'\n\n'+value+'\n\n';});
    document.querySelectorAll('[data-result],[data-model-result]').forEach(el => {if(el.textContent)text+='Check feedback: '+el.textContent+'\n\n';});
    const blob=new Blob([text],{type:'text/markdown;charset=utf-8'});const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download=lab+'-practice-attempt.md';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);status('Attempt exported. Keep the file with your drawing and any tutor feedback.');
  }));
  document.querySelectorAll('[data-reset]').forEach(button => button.addEventListener('click', () => {
    if(!window.confirm('Clear this page\'s notes and saved attempt? Export first to keep a copy.'))return;
    fields().forEach(el => {if(el.type==='radio'||el.type==='checkbox')el.checked=false;else el.value='';});
    document.querySelectorAll('[data-result],[data-model-result]').forEach(el => {el.textContent='';delete el.dataset.outcome;});
    try {localStorage.removeItem(key);status('This page\'s attempt has been cleared.');} catch (_) {status('Visible notes cleared. Browser storage could not be accessed.');}
  }));
  document.querySelectorAll('[data-print]').forEach(button => button.addEventListener('click', () => window.print()));
  const search=document.querySelector('[data-filter]');
  if(search)search.addEventListener('input',()=>{const words=search.value.toLowerCase().trim().split(/\s+/).filter(Boolean);let count=0;document.querySelectorAll('[data-lab-card]').forEach(card=>{const match=words.every(w=>card.dataset.search.includes(w));card.hidden=!match;if(match)count++;});document.querySelector('[data-filter-count]').textContent=count+' practice '+(count===1?'page':'pages')+' match.';});
})();
