/* Automatic living marks. No video autoplay dependency and no playback controls. */
(() => {
  'use strict';
  const host = document.querySelector('[data-living-mark]');
  if (!host) return;
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  const query = new URLSearchParams(location.search);
  const previousKey = 'necessary-tangle:last-living-mark';
  // Explicit URL choices are optional; old player-button state cannot stop autoplay.
  const shouldMove = () => query.get('motion') === 'on' || (query.get('motion') !== 'off' && !motion.matches);
  let current, generation = 0;
  document.querySelectorAll('.living-mark-playback,.living-mark-toggle').forEach(el => el.remove());
  function show(animate = shouldMove()) {
    if (!current) return;
    const ticket = ++generation;
    const moving = animate && !!current.animated_src;
    const image = new Image();
    image.alt = '';
    image.setAttribute('aria-hidden', 'true');
    image.decoding = 'async';
    image.fetchPriority = 'high';
    image.dataset.markFormat = moving ? 'animated-webp' : 'still';
    image.addEventListener('load', () => {
      if (ticket !== generation) return;
      host.replaceChildren(image);
      host.dataset.motionState = moving ? 'playing' : 'paused';
    }, {once: true});
    image.addEventListener('error', () => {
      if (ticket !== generation) return;
      host.dataset.motionState = 'unavailable';
      if (moving) show(false);
    }, {once: true});
    image.src = new URL(moving ? current.animated_src : (current.poster || current.src), document.baseURI).href;
  }
  motion.addEventListener('change', () => show());
  fetch(new URL('assets/living-marks/playback-manifest.json?v=20260907-automatic-2', document.baseURI), {cache: 'no-cache', credentials: 'same-origin'})
    .then(response => { if (!response.ok) throw Error('Mark manifest unavailable'); return response.json(); })
    .then(manifest => {
      const marks = manifest.marks.filter(mark => mark.kind === 'video' && mark.animated_src && mark.poster);
      if (!marks.length) return;
      let previous = '';
      try { previous = sessionStorage.getItem(previousKey) || ''; } catch (_) {}
      const eligible = marks.length > 1 ? marks.filter(mark => mark.id !== previous) : marks;
      const value = new Uint32Array(1); crypto.getRandomValues(value);
      current = marks.find(mark => mark.id === query.get('mark')) || eligible[value[0] % eligible.length];
      try { sessionStorage.setItem(previousKey, current.id); } catch (_) {}
      host.dataset.markId = current.id;
      host.dataset.markBackground = current.background || 'light';
      host.title = 'Living mark: ' + (current.label || current.id);
      show();
    })
    .catch(() => { /* Keep the existing inline mark if the network is unavailable. */ });
})();
