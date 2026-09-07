(() => {
  'use strict';
  const video=document.getElementById('film');
  const status=document.getElementById('playback-status');
  const links=[...document.querySelectorAll('[data-start]')];
  function seek(t){if(!Number.isFinite(t)||t<0)return;const go=()=>{video.currentTime=Math.min(t,video.duration||t);};if(video.readyState)go();else video.addEventListener('loadedmetadata',go,{once:true});}
  function hashTime(){const match=location.hash.match(/^#t=(\d+(?:\.\d+)?)$/);if(match)seek(Number(match[1]));}
  links.forEach(link=>link.addEventListener('click',event=>{if(event.button||event.ctrlKey||event.metaKey||event.shiftKey||event.altKey)return;event.preventDefault();history.pushState(null,'',link.hash);seek(Number(link.dataset.start));video.play().catch(()=>{status.textContent='Press play to start this chapter.';});}));
  video.addEventListener('timeupdate',()=>{let current=links[0];for(const link of links)if(Number(link.dataset.start)<=video.currentTime)current=link;for(const link of links)link.setAttribute('aria-current',String(link===current));});
  video.addEventListener('playing',()=>{status.textContent='';});
  video.addEventListener('error',()=>{status.textContent='The film could not load. Try the download link or read the transcript.';});
  window.addEventListener('hashchange',hashTime);window.addEventListener('popstate',hashTime);hashTime();
})();
