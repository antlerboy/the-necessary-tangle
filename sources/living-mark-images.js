/* Living marks are animated images, not autoplay-dependent video players. */
(() => {
  'use strict';
  const host = document.querySelector('[data-living-mark]');
  if (!host) return;
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  const preferenceKey = 'necessary-tangle:mark-motion';
  const previousKey = 'necessary-tangle:last-living-mark';
  const query = new URLSearchParams(location.search);
  let choice = '';
  try { choice = sessionStorage.getItem(preferenceKey) || ''; } catch (_) {}
  if (['on', 'off'].includes(query.get('motion'))) {
    choice = query.get('motion');
    try { sessionStorage.setItem(preferenceKey, choice); } catch (_) {}
  }
  const shouldMove = () => choice === 'on' || (choice !== 'off' && !motion.matches);
  let current, generation = 0;
  document.querySelectorAll('.living-mark-playback,.living-mark-toggle').forEach(el => el.remove());
  const control = document.createElement('button');
  control.type = 'button';
  control.className = 'living-mark-toggle';
  control.hidden = true;
  (host.closest('a') || host).insertAdjacentElement('afterend', control);
  const icons = {
    play: '<svg aria-hidden="true" viewBox="0 0 24 24"><path d="M7 4l14 8-14 8z"/></svg>',
    pause: '<svg aria-hidden="true" viewBox="0 0 24 24"><path d="M7 5h4v14H7zm6 0h4v14h-4z"/></svg>'
  };
  function sync() {
    control.hidden = !current || !current.animated_src;
    const running = host.dataset.motionState === 'playing';
    control.innerHTML = running ? icons.pause : icons.play;
    let label = running ? 'Pause animation' : 'Play animation';
    if (!running && !choice && motion.matches) label += ' (reduced motion is enabled)';
    control.setAttribute('aria-label', label);
    control.title = label;
  }
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
      sync();
    }, {once: true});
    image.addEventListener('error', () => {
      if (ticket !== generation) return;
      host.dataset.motionState = 'unavailable';
      if (moving) show(false); else sync();
    }, {once: true});
    image.src = new URL(moving ? current.animated_src : (current.poster || current.src), document.baseURI).href;
    sync();
  }
  control.addEventListener('click', () => {
    choice = host.dataset.motionState === 'playing' ? 'off' : 'on';
    try { sessionStorage.setItem(preferenceKey, choice); } catch (_) {}
    show();
  });
  motion.addEventListener('change', () => { if (!choice) show(); });
  fetch(new URL('assets/living-marks/playback-manifest.json?v=20260907-images-1', document.baseURI), {cache: 'no-cache', credentials: 'same-origin'})
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
