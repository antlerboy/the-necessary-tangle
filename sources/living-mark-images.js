/* One living-mark controller: animated images, new marks, and full screen. */
(() => {
  'use strict';
  const host = document.querySelector('[data-living-mark]');
  if (!host) return;
  host.dataset.motionOwner = 'living-images';
  host.removeAttribute('aria-hidden');
  host.setAttribute('role', 'button');
  host.setAttribute('tabindex', '0');
  host.setAttribute('aria-label', 'Change living mark. Double-click for full screen.');
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  const query = new URLSearchParams(location.search);
  const previousKey = 'necessary-tangle:last-living-mark';
  const shouldMove = () => query.get('motion') !== 'off' && !motion.matches;
  let current, marks = [], generation = 0, clickTimer;
  document.querySelectorAll('.living-mark-playback,.living-mark-toggle').forEach(element => element.remove());

  function show(animate = shouldMove()) {
    if (!current) return;
    const mark = current;
    const ticket = ++generation;
    const moving = animate && !!mark.animated_src;
    const image = new Image();
    image.alt = '';
    image.setAttribute('aria-hidden', 'true');
    image.decoding = 'async';
    image.fetchPriority = 'high';
    image.dataset.markFormat = moving ? 'animated-webp' : 'still';
    image.addEventListener('load', () => {
      if (ticket !== generation) return;
      host.replaceChildren(image);
      host.dataset.markId = mark.id;
      host.dataset.markBackground = mark.background || 'light';
      host.dataset.motionState = moving ? 'playing' : 'paused';
      host.title = 'Living mark: ' + (mark.label || mark.id) + '. Click for another; double-click for full screen.';
    }, {once: true});
    image.addEventListener('error', () => {
      if (ticket !== generation) return;
      host.dataset.motionState = 'unavailable';
      if (moving) show(false);
    }, {once: true});
    image.src = new URL(moving ? mark.animated_src : (mark.poster || mark.src), document.baseURI).href;
  }

  function nextMark() {
    if (!marks.length) return;
    let previous = current?.id || '';
    if (!previous) {
      try { previous = sessionStorage.getItem(previousKey) || ''; } catch (_) {}
    }
    const eligible = marks.length > 1 ? marks.filter(mark => mark.id !== previous) : marks;
    const value = new Uint32Array(1);
    crypto.getRandomValues(value);
    current = eligible[value[0] % eligible.length];
    try { sessionStorage.setItem(previousKey, current.id); } catch (_) {}
    show();
  }

  function fullScreen() {
    if (document.fullscreenElement === host) {
      document.exitFullscreen?.().catch?.(() => {});
    } else {
      host.requestFullscreen?.().catch?.(() => {});
    }
  }

  host.addEventListener('click', event => {
    event.preventDefault();
    event.stopPropagation();
    clearTimeout(clickTimer);
    clickTimer = window.setTimeout(nextMark, 230);
  });
  host.addEventListener('dblclick', event => {
    event.preventDefault();
    event.stopPropagation();
    clearTimeout(clickTimer);
    fullScreen();
  });
  host.addEventListener('keydown', event => {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      event.stopPropagation();
      nextMark();
    }
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && document.fullscreenElement === host) {
      document.exitFullscreen?.().catch?.(() => {});
    }
  });
  motion.addEventListener('change', () => show());
  fetch(new URL('assets/living-marks/playback-manifest.json?v=20261126-controls', document.baseURI), {cache: 'no-cache', credentials: 'same-origin'})
    .then(response => { if (!response.ok) throw Error('Mark manifest unavailable'); return response.json(); })
    .then(manifest => {
      marks = manifest.marks.filter(mark => mark.kind === 'video' && mark.animated_src && mark.poster);
      if (!marks.length) return;
      current = marks.find(mark => mark.id === query.get('mark'));
      if (current) show();
      else nextMark();
    })
    .catch(() => { /* Keep the existing inline mark if the network is unavailable. */ });
})();
