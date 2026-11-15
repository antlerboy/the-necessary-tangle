/* Original Tangle adventure. Pure state machine is shared by the browser and tests. */
(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.Tangle42 = api;
})(typeof window !== 'undefined' ? window : this, function () {
  'use strict';
  const clean = value => String(value || '').normalize('NFKD').replace(/[\u0300-\u036f]/g, '').toLowerCase().trim();
  const items = ['ticket', 'compass', 'lamp', 'chart'];
  const directions = {n:'north',s:'south',e:'east',w:'west',u:'up',d:'down',out:'back'};
  const initialRow = '0'.repeat(20) + '1' + '0'.repeat(20);
  function cellStep(row) {
    return [...row].map((_, i) => String((110 >> (Number(row[i-1] || 0)*4 + Number(row[i])*2 + Number(row[i+1] || 0))) & 1)).join('');
  }
  function cells(steps) { const rows=[initialRow]; for(let i=0;i<steps;i++) rows.push(cellStep(rows[rows.length-1])); return rows.slice(-6); }
  function derivative([x,y,z]) { return [10*(y-x), x*(28-z)-y, x*y-(8/3)*z]; }
  function rk4(p) {
    const h=.01, add=(a,b,k)=>a.map((v,i)=>v+k*b[i]);
    const a=derivative(p),b=derivative(add(p,a,h/2)),c=derivative(add(p,b,h/2)),d=derivative(add(p,c,h));
    return p.map((v,i)=>v+h*(a[i]+2*b[i]+2*c[i]+d[i])/6);
  }
  function weather(turns) {
    let a=[1,1,1],b=[1.000001,1,1];
    for(let i=0;i<turns*100;i++) {a=rk4(a);b=rk4(b);}
    return {a,b,distance:Math.hypot(...a.map((v,i)=>v-b[i]))};
  }
  function fresh() {
    return {version:1,room:'platform',turn:0,inventory:['ticket'],visits:['platform'],selected:null,destination:null,
      recent:[],results:[],relations:[],log:[],hints:{},complete:false,
      machine:{setting:0,x:0,disturbed:false,inlet:false,drain:false,flow:0,life:0,weather:0,note:'',repeats:0,signed:false,seated:false}};
  }
  function validSave(candidate, worlds, atlas) {
    if(!candidate || candidate.version!==1 || !worlds.rooms.some(r=>r.id===candidate.room)) return false;
    const m=candidate.machine;
    if(!m || !Number.isInteger(candidate.turn) || candidate.turn<0 || candidate.turn>1000000) return false;
    if(![0,1,2].includes(m.setting) || !Number.isFinite(m.x) || Math.abs(m.x)>100) return false;
    for(const [key,max] of [['flow',1000000],['life',500],['weather',50],['repeats',1000000]])
      if(!Number.isInteger(m[key]) || m[key]<0 || m[key]>max) return false;
    for(const key of ['disturbed','inlet','drain','signed','seated']) if(typeof m[key]!=='boolean') return false;
    if(!['','A','B','C'].includes(m.note) || typeof candidate.complete!=='boolean') return false;
    if(!Array.isArray(candidate.inventory) || candidate.inventory.some(x=>!items.includes(x))) return false;
    const ids=new Set(atlas.nodes.map(n=>n.id)), rooms=new Set(worlds.rooms.map(r=>r.id));
    for(const key of ['selected','destination']) if(candidate[key]!==null && !ids.has(candidate[key])) return false;
    if(candidate.inventory.includes('chart') && candidate.destination===null) return false;
    if(candidate.complete && ['compass','lamp','chart'].some(x=>!candidate.inventory.includes(x))) return false;
    if(!Array.isArray(candidate.visits) || candidate.visits.length>rooms.size || candidate.visits.some(x=>!rooms.has(x))) return false;
    for(const key of ['recent','results']) if(!Array.isArray(candidate[key]) || candidate[key].length>ids.size || candidate[key].some(x=>!ids.has(x))) return false;
    if(!Array.isArray(candidate.relations) || candidate.relations.length>atlas.edges.length || candidate.relations.some(x=>!atlas.edges.some(e=>e.id===x))) return false;
    if(!Array.isArray(candidate.log) || candidate.log.length>120 || candidate.log.some(x=>!x || typeof x.command!=='string' || x.command.length>200 || !rooms.has(x.room))) return false;
    if(!candidate.hints || typeof candidate.hints!=='object' || Array.isArray(candidate.hints)) return false;
    for(const [key,value] of Object.entries(candidate.hints)) if(!rooms.has(key)||!Number.isInteger(value)||value<0||value>3) return false;
    return true;
  }
  class Engine {
    constructor(worlds, atlas, saved) {
      this.worlds=worlds;this.atlas=atlas;
      this.nodes=new Map(atlas.nodes.map(n=>[n.id,n]));this.edges=new Map(atlas.edges.map(e=>[e.id,e]));
      this.rooms=new Map(worlds.rooms.map(r=>[r.id,r]));
      this.state=validSave(saved,worlds,atlas)?JSON.parse(JSON.stringify(saved)):fresh();
    }
    snapshot() {return JSON.parse(JSON.stringify(this.state));}
    room() {return this.rooms.get(this.state.room);}
    selected() {return this.nodes.get(this.state.selected || this.room().anchor);}
    move(id) {
      if(!this.rooms.has(id)) return this.reply('There is no such place on this map.');
      this.state.room=id;if(!this.state.visits.includes(id))this.state.visits.push(id);
      this.state.selected=this.room().anchor;
      return this.look();
    }
    reply(...text) {return {text,record:this.selected(),room:this.room()};}
    look() {return this.reply(this.room().name.toUpperCase(),this.room().description,this.observe());}
    observe() {
      const m=this.state.machine;
      switch(this.state.room) {
        case 'workshop':return `Response switch: ${m.setting}. Needle: ${m.x}. ${m.disturbed&&m.x===0?'The shutter is open.':'The compass shutter is closed.'}`;
        case 'conservatory':return `Inlet ${m.inlet?'open':'closed'}; drain ${m.drain?'open':'closed'}. ${m.inlet&&m.drain?(m.flow>=2?'The lamp has a steady cycle of colours.':'A current has begun. Wait for the colours.'):'The travelling lamp is dark.'}`;
        case 'garden':return `Rule 110 / generation ${m.life} / 41 cells / fixed empty exterior\n`+cells(m.life).map(r=>r.replace(/0/g,'·').replace(/1/g,'█')).join('\n');
        case 'observatory': {const w=weather(m.weather);return `Crank turns: ${m.weather}. Model time: ${m.weather.toFixed(2)}. Separation: ${w.distance.toExponential(6)}.\nGlobe A: ${w.a.map(n=>n.toFixed(6)).join(', ')}\nGlobe B: ${w.b.map(n=>n.toFixed(6)).join(', ')}`;}
        case 'music':return m.note?`Last note: ${m.note}; successive repeats: ${m.repeats}. ${m.repeats>=3?'The lamp has gone dim.':'The lamp answers.'}`:'The instrument is waiting for a note.';
        case 'membrane':return `A patch of the wall numbered ${this.state.turn%17+1} is being replaced. Material continues to pass through the openings.`;
        case 'conversation':return this.state.machine.seated?'The room now records a seated listener. The tubes remain separate.':'The chair is still empty. The notebook records a visitor standing beside it.';
        case 'mirrors':return `Catalogue author: ${m.signed?'the present visitor':'not entered'}. Objects described: mirror, catalogue, pencil, visitor.`;
        case 'ferry':return 'Passage completed. READ CHART opens the chosen atlas destination. You can return and continue exploring.';
        default:return '';
      }
    }
    discover(id) {
      const n=this.nodes.get(id);if(!n)return this.reply('That public atlas entry is not in this edition.');
      this.state.selected=id;this.state.relations=[];
      return this.reply(n.label.toUpperCase(),n.summary || n.definition || 'This is a thin public record. Its scope and sources remain visible in the atlas.',`Record: ${n.level}. Review: ${n.status}. READ ATLAS opens its maintained page; FOLLOW lists recorded connections.`);
    }
    search(query) {
      const q=clean(query);if(!q)return this.reply('FIND needs a name, phrase, or part of a word.');
      const found=this.atlas.nodes.filter(n=>clean(n.label+' '+n.aliases).includes(q))
        .sort((a,b)=>Number(clean(b.label).startsWith(q))-Number(clean(a.label).startsWith(q))||a.label.localeCompare(b.label)).slice(0,25);
      this.state.results=found.map(n=>n.id);this.state.relations=[];
      return this.reply(found.length?`Atlas search: ${query}\n`+found.map((n,i)=>`${i+1}. ${n.label} [${n.level}]`).join('\n')+'\nOPEN a result number.':'No matching public label or alias was found. Try fewer words or another spelling.');
    }
    follow(number) {
      if(number) {
        const e=this.edges.get(this.state.relations[Number(number)-1]);if(!e)return this.reply('Use FOLLOW first, then FOLLOW and a displayed number.');
        const current=this.selected()?.id,other=this.nodes.get(e.source===current?e.target:e.source);
        const text=`${this.nodes.get(e.source).label} — ${e.phrase} ${e.directed?'→':'↔'} ${this.nodes.get(e.target).label}\n${e.scope || ''}\nStatus: ${e.status}. ${e.locator?'Locator: '+e.locator:''}`;
        this.state.selected=other.id;this.state.relations=[];
        return {...this.reply(text,'The selected atlas record has changed. This is a recorded atlas relationship; fictional room exits make separate claims.'),connection:e};
      }
      const id=this.selected()?.id,edges=this.atlas.edges.filter(e=>e.source===id||e.target===id);
      this.state.relations=edges.map(e=>e.id);this.state.results=[];
      return this.reply(edges.length?edges.map((e,i)=>`${i+1}. ${this.nodes.get(e.source).label} — ${e.phrase} ${e.directed?'→':'↔'} ${this.nodes.get(e.target).label} [${e.status}]`).join('\n')+'\nFOLLOW a displayed number to inspect that passage.':'No relationship is recorded for this entry in the public graph. The gap has not been filled with an invented link.');
    }
    improbable(random=Math.random) {
      const seen=new Set(this.state.recent);
      let pool=this.atlas.nodes.filter(n=>!seen.has(n.id));
      if(!pool.length){this.state.recent=[];pool=this.atlas.nodes;}
      if(!pool.length)return this.reply('The public index has not loaded. The lever has declined to improvise one.');
      const n=pool[Math.min(pool.length-1,Math.floor(Math.max(0,random())*pool.length))];
      this.state.recent.push(n.id);
      return this.discover(n.id);
    }
    hint() {
      const id=this.state.room,n=Math.min(3,(this.state.hints[id]||0)+1);this.state.hints[id]=n;
      const hints={
        platform:['The ferry fittings name the objects it needs. Every other place can be explored before departure.','The workshop is north, the lamp south, the chart printer east.','Compass: DISTURB, SET 1, WAIT, TAKE COMPASS in the workshop. Lamp: OPEN INLET, OPEN DRAIN, WAIT twice, TAKE LAMP in the conservatory. PRINT CHART in the library, then return and LAUNCH.'],
        workshop:['Read the notebook. The shutter requires a disturbance followed by settling.','The switch changes the correction applied on WAIT.','DISTURB, SET 1, WAIT, TAKE COMPASS. SET 0 leaves the displacement; SET 2 alternates it.'],
        conservatory:['The label calls for a continuing supply. Read it.','An open inlet needs an open drain, and the colours need time.','OPEN INLET, OPEN DRAIN, WAIT, WAIT, TAKE LAMP.'],
        library:['FIND searches the whole public index. OPEN selects a result.','The chart printer uses your selected atlas record.','FIND EMERGENCE, OPEN 1, PRINT CHART. Any selected public entry can be a destination.']
      };
      return this.reply((hints[id]||['Try the suggested commands, EXAMINE an object, or READ ATLAS.','MAP lists the fictional exits. FIND and IMPROBABILITY work everywhere.','HELP lists the available commands. There is no hidden requirement to complete this room.'])[n-1]);
    }
    run(raw) {
      const input=String(raw||'').trim().slice(0,200),s=this.state,m=s.machine;
      if(!input)return this.reply('Type a command, or choose one of the suggestions.');
      const command=clean(input).replace(/[.!?]+$/,'').replace(/\bthe\s+/g,'');
      s.turn++;s.log.push({command:input,room:s.room});s.log=s.log.slice(-120);
      if(command==='help'||command==='commands')return this.reply('LOOK / EXAMINE object / READ object / OBSERVE / WAIT\nNORTH, SOUTH, EAST, WEST (N, S, E, W) / GO place / MAP\nFIND words / OPEN number / FOLLOW [number] / READ ATLAS / SOURCES\nINVENTORY (I) / HINT / SAVE / RESTORE / RESTART YES\nIMPROBABILITY chooses from the whole public atlas. Fictional exits and recorded atlas connections are distinguished. Suggestions are optional; commands are not case-sensitive.');
      if(command==='look'||command==='l')return this.look();
      if(command==='inventory'||command==='i')return this.reply('You are carrying: '+s.inventory.join(', ')+'.');
      if(command==='version')return this.reply('The Necessary Tangle / reader release 0.42. Original adventure inspired by the CP/M Infocom game. Graph research release: '+this.atlas.graph_release+'.');
      if(command==='hint')return this.hint();
      if(command==='save'||command==='restore')return {...this.reply(),storage:command};
      if(command==='restart')return this.reply('RESTART YES begins a fresh expedition. A separately saved manual checkpoint remains available with RESTORE.');
      if(command==='restart yes'){this.state=fresh();return this.look();}
      if(command==='read log'||command==='log')return this.reply('Expedition log (latest 120 commands)\n'+s.log.map(x=>`${this.rooms.get(x.room).name}: ${x.command}`).join('\n'));
      if(command==='map')return this.reply('Authored places from here:\n'+Object.entries(this.room().exits).map(([d,id])=>`${d.toUpperCase()}: ${this.rooms.get(id).name}`).join('\n')+'\nVisited: '+s.visits.map(id=>this.rooms.get(id).name).join('; ')+'.\nThese are fictional routes, not claims of historical influence.');
      let match=command.match(/^(?:go |walk )?([a-z]+)$/),direction=match?(directions[match[1]]||match[1]):null;
      if(direction && this.room().exits[direction])return this.move(this.room().exits[direction]);
      if(Object.values(directions).includes(direction)||direction==='back')return this.reply('There is no exit that way. MAP lists the exits from here.');
      if(command.startsWith('go ')){
        const q=command.slice(3),found=this.worlds.rooms.filter(r=>Object.values(this.room().exits).includes(r.id)&&(clean(r.name).includes(q)||r.id===q));
        if(found.length===1)return this.move(found[0].id);
        return this.reply('Choose an exit shown by MAP. GO does not invent a passage between rooms.');
      }
      if(command.startsWith('find '))return this.search(input.slice(5));
      if(command.startsWith('ask about '))return this.search(input.slice(10));
      if(command==='find')return this.search('');
      if((match=command.match(/^open (\d+)$/)))return this.discover(s.results[Number(match[1])-1]);
      if((match=command.match(/^follow(?: (\d+))?$/)))return this.follow(match[1]);
      if(['improbability','pull lever','surprise me'].includes(command))return this.improbable();
      if(command==='sources')return {...this.reply('Public source records and their locators appear beside the selected entry. READ ATLAS opens the maintained account.'),showSources:true};
      if(command==='read atlas')return {...this.discover(this.selected()?.id),openAtlas:true};
      if(command==='observe')return this.reply(this.observe()||'The room is as described by LOOK.');
      if(command==='wait'||command==='z'){
        if(s.room==='workshop')m.x=(1-m.setting)*m.x;
        if(s.room==='conservatory')m.flow=m.inlet&&m.drain?Math.min(1000000,m.flow+1):0;
        if(s.room==='garden')m.life=Math.min(500,m.life+1);
        return this.reply(this.observe()||'A little time passes. Your route remains open.');
      }
      if(s.room==='workshop'){
        if(command==='disturb'){m.x=6;m.disturbed=true;return this.reply('A displacement of six divisions. The needles move.',this.observe());}
        if((match=command.match(/^set ([012])$/))){m.setting=Number(match[1]);return this.reply(this.observe());}
        if(command==='take compass'){
          if(!m.disturbed||m.x!==0)return this.reply('The compass shutter remains closed. Read the notebook, or use HINT.');
          if(!s.inventory.includes('compass'))s.inventory.push('compass');
          return this.reply('The shutter opens. You take the compass. Its needle has no opinion about your destination.');
        }
      }
      if(s.room==='conservatory'){
        if((match=command.match(/^(open|close) (inlet|drain)$/))){m[match[2]]=match[1]==='open';if(!m.inlet||!m.drain)m.flow=0;return this.reply(this.observe());}
        if(command==='take lamp'){
          if(m.flow<2||!m.inlet||!m.drain)return this.reply('The travelling lamp has not settled into its cycle. Read its label, or use HINT.');
          if(!s.inventory.includes('lamp'))s.inventory.push('lamp');
          return this.reply('You detach the travelling lamp with its small reservoir. The conservatory continues without it.');
        }
      }
      if(s.room==='garden'&&command==='seed'){m.life=0;return this.reply(this.observe());}
      if(s.room==='observatory'){
        if(command==='turn crank'){m.weather=Math.min(50,m.weather+1);return this.reply(this.observe());}
        if(command==='reset weather'){m.weather=0;return this.reply(this.observe());}
      }
      if(s.room==='coast'&&(match=command.match(/^measure ([0-4])$/))){const n=Number(match[1]);return this.reply(`Koch construction / iteration ${n}\nSegments: ${3*4**n}. Segment length: ${(1/3**n).toFixed(6)}. Perimeter: ${(3*(4/3)**n).toFixed(6)} chosen units.\nThe paper construction is exact; a natural coast would require a measurement convention.`);}
      if(s.room==='music'&&(match=command.match(/^play ([abc])$/))){const note=match[1].toUpperCase();m.repeats=m.note===note?m.repeats+1:1;m.note=note;return this.reply(this.observe());}
      if(s.room==='conversation'){
        if(command==='sit'){m.seated=true;return this.reply('You sit. The notebook adds a listener.',this.observe());}
        if(command==='listen')return this.reply('First tube: a sound, a pause, another sound.\nSecond tube: are we rehearsing, arguing, or describing a rehearsal?\nThird tube: '+(m.seated?'the listener has taken a seat.':'someone appears to be listening from beside the chair.'));
      }
      if(s.room==='mirrors'){
        if(command==='sign catalogue'){m.signed=true;return this.reply('You enter: the present visitor.',this.observe());}
        if(command==='read catalogue')return this.reply(this.observe());
      }
      if(s.room==='library'&&command==='print chart'){
        s.destination=this.selected().id;if(!s.inventory.includes('chart'))s.inventory.push('chart');
        return this.reply('A chart emerges. Destination: '+this.nodes.get(s.destination).label+'. A real atlas address is printed underneath.');
      }
      if(command==='read chart'&&s.inventory.includes('chart'))return {...this.reply('Destination: '+this.nodes.get(s.destination).label+'.'),destination:this.nodes.get(s.destination)};
      if(s.room==='platform'&&['launch','board ferry','enter ferry'].includes(command)){
        const missing=['compass','lamp','chart'].filter(x=>!s.inventory.includes(x));
        if(missing.length)return this.reply('The ferry still needs: '+missing.join(', ')+'. READ PLATE or HINT can help.');
        s.complete=true;return this.move('ferry');
      }
      if(command==='sit'&&s.room==='forest')return this.reply('You sit. A bird moves through a gap which is missing from the map. After a while, you notice the map is missing from the bird.');
      if((match=command.match(/^(?:examine|x|read|look at) (.+)$/))){
        const object=match[1];
        if(this.room().objects[object])return this.reply(this.room().objects[object]);
        if(object==='ticket')return this.reply(this.rooms.get('platform').objects.ticket);
        return this.reply('You cannot find that object here. LOOK describes the room; FIND searches the atlas.');
      }
      return this.reply('That command has no defined action here. Try HELP, HINT, or one of the suggestions. The adventure recognises a finite vocabulary; the atlas search accepts ordinary names and phrases.');
    }
  }
  return {Engine,validSave,fresh,cellStep,cells,rk4,weather};
});
