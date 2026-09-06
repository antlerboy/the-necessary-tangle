'use strict';
(async()=>{
 const status=document.querySelector('#queue-status'),list=document.querySelector('#queue');
 try{
  const response=await fetch('https://events.transduction.systems/api/submissions');if(!response.ok)throw Error();const data=await response.json();
  const preview=await fetch('https://raw.githubusercontent.com/antlerboy/systemsmap/main/dist/data/submission-review.json',{cache:'no-cache'}).then(r=>r.ok?r.json():{submissions:[]}).catch(()=>({submissions:[]}));
  const byId=new Map(preview.submissions.map(x=>[x.id,x]));
  status.textContent=data.submissions.length?data.submissions.length+' submitted links'+(data.nextOffset?' (first page)':''):'No links are waiting in the new submission queue.';
  for(const row of data.submissions.reverse()){
   const parsed=byId.get(row.id),item=document.createElement('li'),link=document.createElement('a'),meta=document.createElement('small');
   link.href=row.url;link.rel='noopener noreferrer nofollow';link.target='_blank';link.textContent=parsed?.proposal?.title||row.proposal.title||row.url;
   item.id=row.id;meta.textContent=new Date(row.createdAt).toLocaleDateString('en-GB')+' · '+(parsed?.status==='published'?'Added to the map':parsed?.status==='extracted'?'Details extracted; awaiting review':parsed?.status==='needs-review'?'Needs a manual check':'Awaiting extraction')+' · '+row.id.slice(0,8);
   item.append(link,meta);
   if(parsed?.proposal?.start){const detail=document.createElement('p');detail.textContent=[parsed.proposal.start,parsed.proposal.startTime,parsed.proposal.timezone,parsed.proposal.organiser].filter(Boolean).join(' · ');item.append(detail);}
   list.append(item);
  }
 }catch{status.textContent='The queue couldn’t be loaded. Please try again shortly.';}
})();
