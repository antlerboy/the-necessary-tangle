(() => {
 const host=document.querySelector('[data-living-mark]'); if(!host)return;
 const button=document.createElement('button');button.type='button';button.className='living-mark-playback';button.textContent='Play mark';
 const home=host.closest('a');(home||host).insertAdjacentElement('afterend',button);
 function sync(){const video=host.querySelector('video');button.textContent=video&&!video.paused?'Pause mark':'Play mark';button.setAttribute('aria-label',video&&!video.paused?'Pause living mark animation':'Play living mark animation');}
 function observe(){const v=host.querySelector('video');if(v){v.addEventListener('play',sync);v.addEventListener('pause',sync);}sync();}
 new MutationObserver(observe).observe(host,{childList:true});observe();
 button.addEventListener('click',async()=>{let video=host.querySelector('video');if(video&&!video.paused){video.pause();sync();return;}if(!video){try{const r=await fetch('assets/living-marks/manifest.json');const manifest=await r.json();const mark=manifest.marks.find(m=>m.id===host.dataset.markId&&m.kind==='video')||manifest.marks.find(m=>m.kind==='video');if(!mark)return;video=document.createElement('video');video.src=mark.src;video.poster=mark.poster||'';video.loop=true;video.muted=true;video.defaultMuted=true;video.playsInline=true;video.setAttribute('aria-hidden','true');host.replaceChildren(video);}catch{button.textContent='Animation unavailable';return;}}try{await video.play();}catch{button.textContent='Animation unavailable';}sync();});
})();