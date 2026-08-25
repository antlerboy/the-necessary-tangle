#!/usr/bin/env python3
"""Render the map as a self-contained HTML page."""
import json, html
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
D = ROOT / "map" / "data"
c = json.loads((D / "concepts.json").read_text(encoding="utf-8"))
e = json.loads((D / "edges.json").read_text(encoding="utf-8"))
meta = c["meta"]
concepts = [x for x in c["concepts"] if x["status"] == "evidenced"]
keep = {x["id"] for x in concepts}
edges = [x for x in e["edges"] if x["source"] in keep and x["target"] in keep]

payload = {
    "meta": meta,
    "nodes": [{"id": n["id"], "label": n["label"], "w": n["work_count"],
               "y0": n["first_year"], "y1": n["last_year"],
               "ex": n["exemplar_works"][:3]} for n in concepts],
    "edges": [{"s": x["source"], "t": x["target"], "w": x["weight"],
               "cw": x["citing_work_count"], "sh": x["top_citing_share"],
               "cc": x["concentrated"], "y0": x["first_year"], "y1": x["last_year"],
               "ev": [{"d": v["citing_doi"], "y": v["citing_year"]}
                      for v in x["evidence"][:3]]}
              for x in edges],
}
blob = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))

candidates = [x["label"] for x in c["concepts"] if x["status"] != "evidenced"]

page = """<title>The Counted Map</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Spectral:ital,wght@0,400;0,600;1,400&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
:root{
  --paper:#e9edf2; --surface:#f7f9fb; --raised:#ffffff;
  --ink:#141b24; --muted:#5a6672; --line:#c9d2dc;
  --accent:#1f6b7a; --accent-soft:#8fc2cc; --warn:#9a5218;
  --edge:#8e9aa6;
}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    --paper:#0d1219; --surface:#131b24; --raised:#1a232e;
    --ink:#dfe7ef; --muted:#8b97a4; --line:#2a3642;
    --accent:#5fb3c4; --accent-soft:#2b5b66; --warn:#d08a4a;
    --edge:#495764;
  }
}
:root[data-theme="dark"]{
  --paper:#0d1219; --surface:#131b24; --raised:#1a232e;
  --ink:#dfe7ef; --muted:#8b97a4; --line:#2a3642;
  --accent:#5fb3c4; --accent-soft:#2b5b66; --warn:#d08a4a;
  --edge:#495764;
}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);
  font-family:"IBM Plex Sans",system-ui,-apple-system,sans-serif;
  font-size:15px;line-height:1.55;-webkit-font-smoothing:antialiased}
header{padding:22px 26px 16px;border-bottom:1px solid var(--line);background:var(--surface)}
h1{font-family:Spectral,Georgia,serif;font-weight:600;font-size:27px;margin:0;
  letter-spacing:-.01em;text-wrap:balance}
.rule{font-family:Spectral,Georgia,serif;font-style:italic;color:var(--muted);
  margin:6px 0 0;max-width:62ch;font-size:16px}
.stats{display:flex;flex-wrap:wrap;gap:26px;margin-top:16px}
.stat b{display:block;font-family:"IBM Plex Mono",monospace;font-size:20px;
  font-variant-numeric:tabular-nums;font-weight:500;color:var(--accent)}
.stat span{font-size:11px;letter-spacing:.09em;text-transform:uppercase;color:var(--muted)}
main{display:grid;grid-template-columns:1fr 350px;gap:0;height:calc(100vh - 168px);min-height:520px}
#stage{position:relative;background:var(--paper);overflow:hidden}
canvas{display:block;width:100%;height:100%}
aside{border-left:1px solid var(--line);background:var(--surface);overflow-y:auto;padding:20px}
aside h2{font-family:Spectral,Georgia,serif;font-size:19px;margin:0 0 2px;font-weight:600}
.sub{font-size:12px;color:var(--muted);margin:0 0 16px}
.k{display:flex;justify-content:space-between;gap:12px;padding:7px 0;
  border-bottom:1px solid var(--line);font-size:13px}
.k span:last-child{font-family:"IBM Plex Mono",monospace;font-variant-numeric:tabular-nums}
.flag{display:inline-block;margin-top:14px;padding:7px 10px;border-left:3px solid var(--warn);
  background:color-mix(in srgb,var(--warn) 9%,transparent);font-size:12.5px;color:var(--ink)}
.evh{font-size:11px;letter-spacing:.09em;text-transform:uppercase;color:var(--muted);
  margin:20px 0 8px}
.ev{border:1px solid var(--line);border-radius:3px;padding:10px;margin-bottom:9px;
  background:var(--raised)}
.ev p{margin:0;font-size:12.5px;line-height:1.5}
.ev a{font-family:"IBM Plex Mono",monospace;font-size:11.5px;color:var(--accent);
  word-break:break-all;display:block;margin-top:6px;text-decoration:none}
.ev a:hover,.ev a:focus-visible{text-decoration:underline}
ul.links{list-style:none;margin:0;padding:0}
ul.links li{padding:6px 0;border-bottom:1px solid var(--line);font-size:13px;
  display:flex;justify-content:space-between;gap:10px;cursor:pointer}
ul.links li:hover{color:var(--accent)}
ul.links b{font-family:"IBM Plex Mono",monospace;font-weight:500;font-variant-numeric:tabular-nums}
footer{padding:14px 26px;border-top:1px solid var(--line);background:var(--surface);
  font-size:12.5px;color:var(--muted)}
footer b{color:var(--ink);font-weight:500}
.hint{position:absolute;left:18px;bottom:16px;font-size:12px;color:var(--muted);
  background:color-mix(in srgb,var(--surface) 88%,transparent);padding:6px 10px;border-radius:3px}
:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
@media (max-width:820px){
  main{grid-template-columns:1fr;height:auto}
  #stage{height:60vh}
  aside{border-left:0;border-top:1px solid var(--line);max-height:none}
}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
</style>

<header>
  <h1>The Counted Map</h1>
  <p class="rule">A concept is here because it has a literature. A line is here because that literature cites across it. Both are counted, not asserted.</p>
  <div class="stats">
    <div class="stat"><b id="sN">0</b><span>Concepts</span></div>
    <div class="stat"><b id="sE">0</b><span>Lines</span></div>
    <div class="stat"><b id="sW">0</b><span>Works matched</span></div>
    <div class="stat"><b id="sR">13.8M</b><span>References scanned</span></div>
    <div class="stat"><b id="sC">0</b><span>Lines flagged thin</span></div>
  </div>
</header>
<main>
  <div id="stage">
    <canvas id="cv"></canvas>
    <div class="hint">Click a concept, then a link, to see the citations under it.</div>
  </div>
  <aside id="panel"></aside>
</main>
<footer>
  <b>Not influence.</b> Every line counts references and nothing more &mdash; not teaching, agreement, derivation or logical dependence.
  Seventeen seeded concepts fall below the evidence threshold in this corpus and are held back rather than drawn:
  __CANDIDATES__.
</footer>
<script>
const DATA=__BLOB__;
const cv=document.getElementById('cv'),ctx=cv.getContext('2d'),stage=document.getElementById('stage');
const panel=document.getElementById('panel');
document.getElementById('sN').textContent=DATA.nodes.length;
document.getElementById('sW').textContent=(DATA.meta.concept_matched_work_count||0).toLocaleString();
document.getElementById('sE').textContent=DATA.edges.length;
document.getElementById('sC').textContent=DATA.edges.filter(e=>e.cc).length;

const N=DATA.nodes,E=DATA.edges,byId={};
N.forEach((n,i)=>{n.i=i;byId[n.id]=n});
const maxW=Math.max(...N.map(n=>n.w));
N.forEach(n=>{n.r=7+18*Math.sqrt(n.w/maxW);n.deg=0});
E.forEach(e=>{e.a=byId[e.s];e.b=byId[e.t];if(e.a&&e.b){e.a.deg++;e.b.deg++}});
const maxE=Math.max(...E.map(e=>e.w));

let W=0,H=0,sel=null,selEdge=null,hover=null;
function size(){const r=stage.getBoundingClientRect(),d=window.devicePixelRatio||1;
  W=r.width;H=r.height;cv.width=W*d;cv.height=H*d;ctx.setTransform(d,0,0,d,0,0)}
size();
N.forEach((n,i)=>{const a=2*Math.PI*i/N.length;n.x=W/2+Math.cos(a)*Math.min(W,H)*0.32;
  n.y=H/2+Math.sin(a)*Math.min(W,H)*0.32;n.vx=0;n.vy=0});

function tick(){
  // Cooling: strong early moves, small late ones, so the layout settles rather
  // than oscillating. Without it 1,850 edges pump energy in faster than damping
  // takes it out and the graph flies apart.
  const alpha=Math.max(0.06,1-frames/400);
  for(let i=0;i<N.length;i++){const p=N[i];
    for(let j=i+1;j<N.length;j++){const q=N[j];
      let dx=q.x-p.x,dy=q.y-p.y,d2=dx*dx+dy*dy||1,d=Math.sqrt(d2);
      const f=Math.min(40,(9000+140*N.length)/d2)*alpha;
      const ux=dx/d,uy=dy/d;
      p.vx-=ux*f;p.vy-=uy*f;q.vx+=ux*f;q.vy+=uy*f;}}
  E.forEach(e=>{if(!e.a||!e.b)return;
    let dx=e.b.x-e.a.x,dy=e.b.y-e.a.y,d=Math.sqrt(dx*dx+dy*dy)||1;
    // Divide by each endpoint's degree so a hub with 200 lines is not dragged
    // 200 times harder than a leaf with one.
    const k=0.02*Math.log(1+e.w)*alpha,f=(d-210)*k,ux=dx/d,uy=dy/d;
    const fa=f/Math.sqrt(e.a.deg||1),fb=f/Math.sqrt(e.b.deg||1);
    e.a.vx+=ux*fa;e.a.vy+=uy*fa;e.b.vx-=ux*fb;e.b.vy-=uy*fb});
  const CAP=14;
  N.forEach(n=>{n.vx+=(W/2-n.x)*0.0011;n.vy+=(H/2-n.y)*0.0018;
    n.vx*=0.80;n.vy*=0.80;
    const sp=Math.hypot(n.vx,n.vy);
    if(sp>CAP){n.vx=n.vx/sp*CAP;n.vy=n.vy/sp*CAP}
    n.x+=n.vx;n.y+=n.vy;});
}
function css(v){return getComputedStyle(document.documentElement).getPropertyValue(v).trim()}
function draw(){
  const C={ink:css('--ink'),ac:css('--accent'),ed:css('--edge'),wn:css('--warn'),
           su:css('--surface'),mu:css('--muted'),soft:css('--accent-soft')};
  ctx.clearRect(0,0,W,H);
  E.forEach(e=>{if(!e.a||!e.b)return;
    const on=sel&&(e.a===sel||e.b===sel);
    if(sel&&!on){ctx.globalAlpha=.06}else{ctx.globalAlpha=on?.85:.3}
    ctx.strokeStyle=e===selEdge?C.ac:(on&&e.cc?C.wn:(on?C.ac:C.ed));
    ctx.lineWidth=e===selEdge?3:Math.max(.6,Math.min(4,Math.log(1+e.w)/2.2));
    ctx.beginPath();ctx.moveTo(e.a.x,e.a.y);ctx.lineTo(e.b.x,e.b.y);ctx.stroke()});
  ctx.globalAlpha=1;
  const order=N.slice().sort((a,b)=>b.r-a.r),boxes=[];
  order.forEach(n=>{
    const dim=sel&&n!==sel&&!E.some(e=>(e.a===sel&&e.b===n)||(e.b===sel&&e.a===n));
    ctx.globalAlpha=dim?.22:1;
    ctx.beginPath();ctx.arc(n.x,n.y,n.r,0,7);
    ctx.fillStyle=n===sel?C.ac:(n===hover?C.soft:C.su);
    ctx.fill();ctx.lineWidth=n===sel?2.5:1.2;
    ctx.strokeStyle=n===sel?C.ac:C.mu;ctx.stroke();});
  ctx.font='500 12px "IBM Plex Sans",sans-serif';ctx.textAlign='center';
  order.forEach(n=>{
    const dim=sel&&n!==sel&&!E.some(e=>(e.a===sel&&e.b===n)||(e.b===sel&&e.a===n));
    const must=(n===sel||n===hover);
    if(dim&&!must)return;
    const w=ctx.measureText(n.label).width,x=n.x-w/2,y=n.y+n.r+5,h=15;
    const clash=boxes.some(b=>x<b.x+b.w+5&&x+w+5>b.x&&y<b.y+b.h+3&&y+h+3>b.y);
    if(clash&&!must)return;
    boxes.push({x:x,y:y,w:w,h:h});
    ctx.globalAlpha=dim?.5:1;
    ctx.lineWidth=3;ctx.strokeStyle=C.su;ctx.strokeText(n.label,n.x,n.y+n.r+15);
    ctx.fillStyle=C.ink;ctx.fillText(n.label,n.x,n.y+n.r+15)});
  ctx.globalAlpha=1;
}
let frames=0;
function fit(){
  // Scale and centre the settled layout so nothing sits under the edge, leaving
  // room for the labels that hang below each node.
  // Labels are far wider than the circles they sit under, so the horizontal
  // margin has to allow for half a label on each side.
  const PADX=120,PADY=42,BOT=26;
  let x0=1e9,y0=1e9,x1=-1e9,y1=-1e9;
  N.forEach(n=>{x0=Math.min(x0,n.x-n.r);y0=Math.min(y0,n.y-n.r);
                x1=Math.max(x1,n.x+n.r);y1=Math.max(y1,n.y+n.r+BOT)});
  const sx=(W-2*PADX)/Math.max(1,x1-x0),sy=(H-2*PADY)/Math.max(1,y1-y0);
  const k=Math.min(sx,sy,1.6);
  const cx=(x0+x1)/2,cy=(y0+y1)/2;
  N.forEach(n=>{n.x=W/2+(n.x-cx)*k;n.y=H/2+(n.y-cy)*k;n.vx=0;n.vy=0});
}
function loop(){
  if(frames<400){
    tick();frames++;
    // Re-fit while settling so the map is never seen spilling off the canvas.
    if(frames>140&&frames%40===0)fit();
    if(frames===400)fit();
  }
  draw();requestAnimationFrame(loop)}
loop();

function hit(x,y){let best=null,bd=1e9;
  N.forEach(n=>{const d=Math.hypot(n.x-x,n.y-y);if(d<n.r+7&&d<bd){bd=d;best=n}});return best}
cv.addEventListener('mousemove',ev=>{const r=cv.getBoundingClientRect();
  hover=hit(ev.clientX-r.left,ev.clientY-r.top);cv.style.cursor=hover?'pointer':'default'});
cv.addEventListener('click',ev=>{const r=cv.getBoundingClientRect();
  const n=hit(ev.clientX-r.left,ev.clientY-r.top);
  if(n){sel=n;selEdge=null;showNode(n)}else{sel=null;selEdge=null;intro()}});

function esc(s){return String(s).replace(/[&<>"]/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[m]))}
function intro(){panel.innerHTML=
  '<h2>Reading this map</h2><p class="sub">'+DATA.nodes.length+' concepts that met the evidence threshold</p>'+
  '<p style="font-size:13.5px">Circle size is how much literature places a concept here. Line thickness is how many references support it.</p>'+
  '<p style="font-size:13.5px">Amber lines are ones where a single bibliography supplies half the support or more &mdash; real citations, but a thin basis for a claim about the field.</p>'+
  '<div class="evh">Largest literatures</div><ul class="links">'+
  N.slice().sort((a,b)=>b.w-a.w).slice(0,10).map(n=>
    '<li data-n="'+n.id+'"><span>'+esc(n.label)+'</span><b>'+n.w+'</b></li>').join('')+'</ul>';
  panel.querySelectorAll('li[data-n]').forEach(li=>li.onclick=()=>{sel=byId[li.dataset.n];showNode(sel)});
}
function showNode(n){
  const links=E.filter(e=>e.a===n||e.b===n).sort((a,b)=>b.w-a.w);
  panel.innerHTML='<h2>'+esc(n.label)+'</h2><p class="sub">'+
    n.w+' works, '+(n.y0||'?')+'&ndash;'+(n.y1||'?')+'</p>'+
    '<div class="k"><span>Lines</span><span>'+links.length+'</span></div>'+
    '<div class="k"><span>Works placing it here</span><span>'+n.w+'</span></div>'+
    (n.ex.length?'<div class="evh">Most-cited works</div>'+n.ex.map(x=>
      '<div class="ev"><p>'+esc(x.title)+' <span style="color:var(--muted)">('+x.year+', cited '+x.cited_by+')</span></p>'+
      '<a href="https://doi.org/'+esc(x.doi)+'" target="_blank" rel="noopener">'+esc(x.doi)+'</a></div>').join(''):'')+
    '<div class="evh">Aggregate keyword links</div><ul class="links">'+links.slice(0,18).map((e,i)=>
      '<li data-e="'+E.indexOf(e)+'"><span>'+(e.a===n?'&rarr; ':'&larr; ')+
      esc((e.a===n?e.b:e.a).label)+(e.cc?' <span style="color:var(--warn)">&#9679;</span>':'')+
      '</span><b>'+e.w+'</b></li>').join('')+'</ul>';
  panel.querySelectorAll('li[data-e]').forEach(li=>li.onclick=()=>{
    selEdge=E[+li.dataset.e];showEdge(selEdge)});
}
function showEdge(e){
  panel.innerHTML='<h2>'+esc(e.a.label)+' &rarr; '+esc(e.b.label)+'</h2>'+
    '<p class="sub">source-title records matching '+esc(e.a.label.toLowerCase())+' contain cited-reference strings matching '+esc(e.b.label.toLowerCase())+'</p>'+
    '<div class="k"><span>Supporting references</span><span>'+e.w+'</span></div>'+
    '<div class="k"><span>Distinct citing works</span><span>'+e.cw+'</span></div>'+
    '<div class="k"><span>Largest single share</span><span>'+Math.round(e.sh*100)+'%</span></div>'+
    '<div class="k"><span>Span</span><span>'+(e.y0||'?')+'&ndash;'+(e.y1||'?')+'</span></div>'+
    (e.cc?'<div class="flag">One citing work supplies '+Math.round(e.sh*100)+
      '% of this line&rsquo;s support. Read it as one author&rsquo;s reading list, not as a property of the field.</div>':'')+
    '<div class="evh">Example citing DOI handles</div>'+
    e.ev.map(v=>'<div class="ev"><a href="https://doi.org/'+esc(v.d)+'" target="_blank" rel="noopener">'+esc(v.d)+' ('+esc(v.y)+')</a></div>').join('')+
    '<p style="font-size:12.5px;color:var(--muted);margin-top:16px">Keyword-labelled aggregate signal only. Not influence, teaching, agreement, derivation, importance or a clean citation between two unambiguous literatures.</p>';
}
intro();
addEventListener('resize',()=>{size();frames=Math.min(frames,360)});
</script>"""

page = page.replace("__BLOB__", blob).replace("__CANDIDATES__", html.escape(", ".join(candidates)))
out = ROOT / "map" / "view.html"
out.write_text(page, encoding="utf-8")
print(f"wrote {out.relative_to(ROOT)}  {out.stat().st_size/1024:.0f} KB  "
      f"{len(concepts)} concepts, {len(edges)} edges")
