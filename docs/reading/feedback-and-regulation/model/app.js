(function () {
  'use strict';
  const ids = ['gain','initial','tolerance','horizon'];
  const controls = Object.fromEntries(ids.map(id => [id, document.getElementById(id)]));
  const defaults = {gain:'0.5', initial:'1', tolerance:'0.25', horizon:'12'};
  const format = n => n === 0 ? '0' : Number(n.toPrecision(6)).toString();
  const svg = document.getElementById('chart');
  function element(name, attrs, text) {
    const x = document.createElementNS('http://www.w3.org/2000/svg', name);
    for (const [key, value] of Object.entries(attrs)) x.setAttribute(key, value);
    if (text !== undefined) x.textContent = text;
    return x;
  }
  function draw(result, tolerance, horizon) {
    svg.querySelectorAll('[data-drawn]').forEach(x => x.remove());
    const add = (name, attrs, content) => {const x=element(name, {...attrs, 'data-drawn':'true'}, content); svg.appendChild(x);};
    const left=105,right=655,top=22,bottom=265;
    const max=Math.max(tolerance, ...result.values.map(p => Math.abs(p.error)), 0.1)*1.1;
    const axisFormat = n => Math.abs(n) >= 1000 || (Math.abs(n) > 0 && Math.abs(n) < 0.01) ? n.toExponential(1) : Number(n.toPrecision(3)).toString();
    const X=n => left + (right-left)*n/Math.max(horizon,1);
    const Y=v => top + (bottom-top)*(max-v)/(2*max);
    add('rect',{x:left,y:Y(tolerance),width:right-left,height:Y(-tolerance)-Y(tolerance),fill:'#e9e5d7'});
    add('line',{x1:left,y1:Y(0),x2:right,y2:Y(0),stroke:'#766d60','stroke-width':1});
    add('line',{x1:left,y1:top,x2:left,y2:bottom,stroke:'#766d60','stroke-width':1});
    add('line',{x1:left,y1:bottom,x2:right,y2:bottom,stroke:'#766d60','stroke-width':1});
    add('text',{x:left-8,y:top+5,'text-anchor':'end','font-size':18,fill:'#29251f'},axisFormat(max));
    add('text',{x:left-8,y:Y(0)+4,'text-anchor':'end','font-size':18,fill:'#29251f'},'0');
    add('text',{x:left-8,y:bottom,'text-anchor':'end','font-size':18,fill:'#29251f'},axisFormat(-max));
    add('text',{x:left,y:285,'text-anchor':'middle','font-size':18,fill:'#29251f'},'0');
    if(horizon) add('text',{x:right,y:285,'text-anchor':'middle','font-size':18,fill:'#29251f'},String(horizon));
    add('polyline',{points:result.values.map(p=>`${X(p.n)},${Y(p.error)}`).join(' '),fill:'none',stroke:'#a32f25','stroke-width':2});
    result.values.forEach(p=>add('circle',{cx:X(p.n),cy:Y(p.error),r:3.2,fill:'#a32f25'}));
  }
  function update() {
    ids.forEach(id=>document.getElementById(id+'-value').value=controls[id].value);
    const k=+controls.gain.value,e0=+controls.initial.value,t=+controls.tolerance.value,h=+controls.horizon.value;
    const result=ResponseModel.calculate(k,e0,t,h);
    document.getElementById('regime').textContent=result.regime + (result.asymptotic ? ' The zero-error equilibrium is asymptotically stable.' : ' The zero-error equilibrium is not asymptotically stable.');
    document.getElementById('zero-note').textContent=e0===0 ? 'This run starts at zero and remains there. That alone does not prove stability under perturbation.' : '';
    document.getElementById('compliance').textContent=result.allInside ? `Every observed state from step 0 to ${h} is within the band.` : `At least one observed state from step 0 to ${h} is outside the band.`;
    document.getElementById('final').textContent=`At step ${h}, the error is ${format(result.values[h].error)}: ${result.finalInside ? 'within' : 'outside'} the band.`;
    const rows=document.getElementById('rows'); rows.replaceChildren(...result.values.map((p,i)=>{const tr=document.createElement('tr'); [p.n,format(-p.error),format(p.error),result.inside[i]?'Yes':'No'].forEach(v=>{const td=document.createElement('td');td.textContent=v;tr.appendChild(td);});return tr;}));
    draw(result,t,h);
  }
  ids.forEach(id=>controls[id].addEventListener('input',update));
  document.getElementById('reset').addEventListener('click',()=>{ids.forEach(id=>controls[id].value=defaults[id]);update();});
  update();
})();


