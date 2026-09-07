/* Add a concrete practice route to an existing atlas item without changing its claims. */
(() => {
  'use strict';
  let scheduled=false;
  function render(){
    scheduled=false;
    const query=new URLSearchParams(location.hash.replace(/^#/,''));
    const id=query.get('id');
    const links=window.TANGLE_PRACTICE_LINKS?.[id];
    const host=document.getElementById('drawerBody');
    if(!host||!links||query.get('view')!=='item')return;
    const existing=host.querySelector('[data-practice-for]');
    if(existing?.dataset.practiceFor===id)return;
    if(existing)existing.remove();
    const section=document.createElement('section');section.dataset.practiceFor=id;section.className='practice-resource-links';
    const title=document.createElement('h3');title.textContent='Try a basic case';section.append(title);
    const intro=document.createElement('p');intro.textContent='Make your own model before opening the comparison. These are original learning exercises, not accreditation.';section.append(intro);
    const list=document.createElement('ul');
    links.forEach(item=>{const li=document.createElement('li');const a=document.createElement('a');a.href=item.url;a.textContent=item.title;li.append(a);list.append(li);});
    section.append(list);host.append(section);
  }
  function schedule(){if(!scheduled){scheduled=true;requestAnimationFrame(render);}}
  window.addEventListener('hashchange',schedule);
  const host=document.getElementById('drawerBody');
  if(host)new MutationObserver(schedule).observe(host,{childList:true});
  schedule();
})();
