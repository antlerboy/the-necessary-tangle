(async function () {
  'use strict';
  const $=id=>document.getElementById(id), automatic='tnt42.resume.v1', manual='tnt42.save.v1';
  const transcript=$('transcript'), input=$('command'), history=[];let historyIndex=0,engine,worlds,atlas;
  function append(text,style='',link) {
    if(!text&&!link)return;
    const p=document.createElement('p');p.className='entry '+style;
    p.textContent=text||'';
    if(link){const a=document.createElement('a');a.href=link.url;a.textContent=link.label;p.append(document.createElement('br'),a);}
    transcript.append(p);
    while(transcript.children.length>160)transcript.firstChild.remove();
    transcript.scrollTop=transcript.scrollHeight;
  }
  function stored(key){try{return JSON.parse(localStorage.getItem(key)||'null');}catch{return null;}}
  function persist(key) {
    try {
      const json=JSON.stringify(engine.snapshot());localStorage.setItem(key,json);
      if(localStorage.getItem(key)!==json)throw Error('readback');
      $('storageStatus').textContent=key===manual?'Manual checkpoint saved and read back in this browser. RESTORE returns to it.':'Automatic resume is available in this browser. SAVE keeps a separate manual checkpoint.';
      return true;
    }catch {
      $('storageStatus').textContent='Browser storage is unavailable or full. You can continue playing, but this position has not been saved.';return false;
    }
  }
  function nodeLink(n,label) {const a=document.createElement('a');a.href=n.url;a.className='atlas-link';a.textContent=label||'Open '+n.label+' in the atlas';return a;}
  function paragraph(text,parent,tag='p'){const e=document.createElement(tag);e.textContent=text;parent.append(e);return e;}
  function renderRecord(n) {
    const box=$('record');box.replaceChildren();if(!n)return;
    paragraph('MAINTAINED ATLAS RECORD',box).className='eyebrow';paragraph(n.label,box,'h2');
    paragraph(n.level+' · '+n.status,box).className='record-status';
    if(n.summary||n.definition)paragraph(n.summary||n.definition,box);
    else paragraph('This public record is thin. Its existing scope and sources are available through the atlas.',box);
    box.append(nodeLink(n));
    const detail=document.createElement('details'),sum=document.createElement('summary');sum.textContent='Sources and locators';detail.append(sum);
    if(!n.sources.length)paragraph('No public source link is recorded here. Open the maintained record for its bibliographic limits.',detail);
    n.sources.forEach(s=>{const p=document.createElement('p');if(s.url){const a=document.createElement('a');a.href=s.url;a.textContent=s.title;p.append(a);}else p.textContent=s.title+' — bibliographic record';if(s.locator)p.append(document.createTextNode(' / '+s.locator));detail.append(p);});
    box.append(detail);
    if(engine.state.complete){const p=paragraph('Passage completed. Your expedition can continue.',box);p.className='completion';}
  }
  function address(replace=false) {
    const u=new URL(location.href);u.searchParams.set('place',engine.state.room);
    if(engine.state.selected)u.searchParams.set('entry',engine.state.selected);else u.searchParams.delete('entry');
    if(u.href!==location.href)window.history[replace?'replaceState':'pushState']({},'',u);
  }
  function render(result,changeAddress=true) {
    result.text.forEach(t=>append(t));
    if(result.openAtlas&&result.record)append('Continue in the maintained atlas:', '', {url:result.record.url,label:result.record.label});
    if(result.destination)append('Your chart leads here:', '', {url:result.destination.url,label:result.destination.label});
    $('location').textContent=engine.room().name;$('moves').textContent='Moves: '+engine.state.turn;
    const suggestions=$('suggestions');suggestions.replaceChildren();
    engine.room().actions.forEach(c=>{const b=document.createElement('button');b.type='button';b.textContent=c;b.addEventListener('click',()=>execute(c));suggestions.append(b);});
    const exits=$('exits');exits.replaceChildren();
    Object.entries(engine.room().exits).forEach(([direction,id])=>{const a=document.createElement('a');a.href='/42/?place='+encodeURIComponent(id);a.textContent=direction.toUpperCase()+' / '+engine.rooms.get(id).name;a.addEventListener('click',e=>{if(e.button!==0||e.metaKey||e.ctrlKey||e.shiftKey||e.altKey)return;e.preventDefault();execute(direction);});exits.append(a);});
    renderRecord(result.record||engine.selected());
    if(result.showSources){const details=$('record').querySelector('details');details.open=true;details.scrollIntoView({block:'nearest'});}
    if(result.connection){const b=$('passage');b.hidden=false;b.replaceChildren();paragraph('RECORDED CONNECTION',b).className='eyebrow';paragraph(engine.nodes.get(result.connection.source).label+' — '+result.connection.phrase+' '+(result.connection.directed?'→':'↔')+' '+engine.nodes.get(result.connection.target).label,b);paragraph(result.connection.status+(result.connection.locator?' / '+result.connection.locator:''),b);paragraph(result.connection.scope,b);result.connection.sources.forEach(s=>{const p=document.createElement('p');if(s.url){const a=document.createElement('a');a.href=s.url;a.textContent=s.title;p.append(a);}else p.textContent=s.title;b.append(p);});}
    if(changeAddress)address();
    persist(automatic);
  }
  function execute(command) {
    append('> '+command,'command');history.push(command);historyIndex=history.length;
    const result=engine.run(command);
    if(result.storage==='save'){
      const success=persist(manual);result.text.push(success?'Checkpoint saved and verified.':'The checkpoint could not be saved. This browser has refused or exhausted local storage.');
    }
    if(result.storage==='restore'){
      const saved=stored(manual);
      if(window.Tangle42.validSave(saved,worlds,atlas)){engine=new window.Tangle42.Engine(worlds,atlas,saved);render(engine.look());append('Manual checkpoint restored.');input.focus({preventScroll:true});return;}
      result.text.push('No valid manual checkpoint was found. Your present expedition is unchanged.');
    }
    render(result);input.value='';input.focus({preventScroll:true});
  }
  $('palette').addEventListener('change',e=>{document.documentElement.dataset.palette=e.target.value;try{localStorage.setItem('tnt42.palette',e.target.value);}catch{}});
  try {const p=localStorage.getItem('tnt42.palette');if(['green','amber','paper'].includes(p)){document.documentElement.dataset.palette=p;$('palette').value=p;}}catch{}
  try {
    const responses=await Promise.all([fetch('worlds.json'),fetch('atlas.json')]);
    if(responses.some(r=>!r.ok))throw Error('Edition files could not be loaded');
    [worlds,atlas]=await Promise.all(responses.map(r=>r.json()));
    const saved=stored(automatic),resumed=window.Tangle42.validSave(saved,worlds,atlas);
    engine=new window.Tangle42.Engine(worlds,atlas,saved);
    const query=new URLSearchParams(location.search),place=query.get('place'),entry=query.get('entry');
    if(place&&engine.rooms.has(place)){engine.state.room=place;if(!engine.state.visits.includes(place))engine.state.visits.push(place);engine.state.selected=engine.room().anchor;}
    if(entry&&engine.nodes.has(entry))engine.state.selected=entry;
    $('graphRelease').textContent=atlas.graph_release;
    if(!resumed)worlds.opening.forEach(p=>append(p,'opening'));
    else append('Resumed your expedition from this browser. SAVE and RESTORE use a separate manual checkpoint.','opening');
    render(engine.look(),false);address(true);
    input.disabled=false;$('submit').disabled=false;
    $('commandForm').addEventListener('submit',e=>{e.preventDefault();if(input.value.trim())execute(input.value.trim());});
    input.addEventListener('keydown',e=>{if(e.key==='ArrowUp'){e.preventDefault();historyIndex=Math.max(0,historyIndex-1);input.value=history[historyIndex]||'';}else if(e.key==='ArrowDown'){e.preventDefault();historyIndex=Math.min(history.length,historyIndex+1);input.value=history[historyIndex]||'';}});
    document.querySelectorAll('[data-command]').forEach(b=>b.addEventListener('click',()=>execute(b.dataset.command)));
    addEventListener('popstate',()=>{const p=new URLSearchParams(location.search),r=p.get('place'),n=p.get('entry');if(engine.rooms.has(r))engine.state.room=r;if(engine.nodes.has(n))engine.state.selected=n;else engine.state.selected=engine.room().anchor;render(engine.look(),false);});
  }catch(error){
    $('location').textContent='The edition could not be loaded';
    append('The adventure files are unavailable. Your saved position has not been replaced. You can return to the readable atlas below.');
    append('Explore the atlas:', '', {url:'/entries/',label:'Public entries and sources'});
  }
})();
