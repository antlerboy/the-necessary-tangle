(function(root){
  'use strict';
  const entropy=ps=>-ps.filter(p=>p>0).reduce((s,p)=>s+p*Math.log2(p),0);
  const maps={full:['A','B','C','D'],poor:['A','other','other','other'],task_preserving:['routine','routine','callback','partner']};
  const tasks={shared:['routine','routine','callback','partner'],distinct:['a','b','c','d'],same:['one','one','one','one']};
  function analyse(rareTotal=.03,task='shared'){
    if(!Number.isFinite(rareTotal)||rareTotal<=0||rareTotal>.75||typeof task!=='string'||!Object.hasOwn(tasks,task))throw Error('Use a probability in (0,.75] and a known task');
    const probabilities=[1-rareTotal,rareTotal/3,rareTotal/3,rareTotal/3],actions=tasks[task];
    const rows=Object.entries(maps).map(([id,labels])=>{
      const groups=new Map();labels.forEach((label,i)=>{if(!groups.has(label))groups.set(label,[]);groups.get(label).push(i);});
      const outputProbabilities=[...groups.values()].map(indices=>indices.reduce((s,i)=>s+probabilities[i],0));
      let ambiguous=0,best=0,conditional=0;const downstream={};
      for(const [label,indices]of groups){
        const byAction=new Map(),mass=indices.reduce((s,i)=>s+probabilities[i],0);
        for(const i of indices)byAction.set(actions[i],(byAction.get(actions[i])||0)+probabilities[i]);
        if(byAction.size>1)ambiguous++;
        const entries=[...byAction.entries()].sort((a,b)=>b[1]-a[1]);best+=entries[0][1];downstream[label]=entries[0][0];
        conditional+=mass*entropy(indices.map(i=>probabilities[i]/mass));
      }
      return{id,labels,groups:[...groups].map(([label,indices])=>({label,indices})),count:groups.size,logCount:Math.log2(groups.size),entropy:entropy(outputProbabilities),conditional,ambiguous,taskPreserved:ambiguous===0,bestSuccess:best,downstream};
    });
    return{probabilities,actions,inputEntropy:entropy(probabilities),inputLogCount:2,rows};
  }
  function supplementation(extra=false){
    const outputs=[];
    for(const r of [0,1])for(const s of extra?[0,1,2]:[null])outputs.push(extra?`${r}:${s}`:`${r}${r}${r}`);
    return{extra,patterns:outputs,count:new Set(outputs).size,logCount:Math.log2(new Set(outputs).size),inputControlLog:1,supplementLog:extra?Math.log2(3):0,assumption:extra?'All six joint states are possible; control and supplement are independently uniform for the entropy comparison.':'The three repeated symbols are determined by the same two-valued input.'};
  }
  const api={entropy,analyse,supplementation};if(typeof module!=='undefined'&&module.exports)module.exports=api;root.VarietyModel=api;
})(typeof globalThis!=='undefined'?globalThis:this);
