(() => {
  'use strict';

  const host = document.querySelector('[data-living-mark]');
  if (!host) return;

  const manifestUrl = 'assets/living-marks/manifest.json?v=0.20.2-reader-hotfix';
  const reducedMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const previousKey = 'necessary-tangle:last-living-mark';

  function randomIndex(length) {
    if (length <= 1) return 0;
    if (window.crypto && window.crypto.getRandomValues) {
      const value = new Uint32Array(1);
      window.crypto.getRandomValues(value);
      return value[0] % length;
    }
    return Math.floor(Math.random() * length);
  }

  function chooseMark(marks) {
    const usable = marks.filter(mark => mark && mark.id && mark.src && (mark.kind === 'image' || mark.kind === 'video'));
    if (!usable.length) return null;
    let previous = '';
    try { previous = window.sessionStorage.getItem(previousKey) || ''; } catch (_) { /* storage is optional */ }
    const moving = reducedMotion ? [] : usable.filter(mark => mark.kind === "video");
    const pool = moving.length ? moving : usable;
    const candidates = pool.length > 1 ? pool.filter(mark => mark.id !== previous) : pool;
    const chosen = candidates[randomIndex(candidates.length)] || pool[0];
    try { window.sessionStorage.setItem(previousKey, chosen.id); } catch (_) { /* storage is optional */ }
    return chosen;
  }

  function imageFor(mark, src) {
    const image = document.createElement('img');
    image.src = src;
    image.alt = '';
    image.decoding = 'async';
    image.fetchPriority = 'high';
    image.setAttribute('aria-hidden', 'true');
    image.addEventListener('load', () => host.replaceChildren(image), { once: true });
    return image;
  }

  function showPoster(mark) {
    const poster = mark.poster || mark.src;
    imageFor(mark, poster);
  }

  function showMark(mark) {
    host.dataset.markId = mark.id;
    host.dataset.markBackground = mark.background || 'light';
    host.title = `Living mark: ${mark.label || mark.id}`;

    if (mark.kind === 'image' || reducedMotion) {
      showPoster(mark);
      return;
    }

    const video = document.createElement('video');
    video.src = mark.src;
    video.poster = mark.poster || '';
    video.muted = true;
    video.defaultMuted = true;
    video.autoplay = true;
    video.loop = true;
    video.playsInline = true;
    video.preload = 'metadata';
    video.tabIndex = -1;
    video.setAttribute('muted', '');
    video.setAttribute('aria-hidden', 'true');
    video.addEventListener('error', () => showPoster(mark), { once: true });
    host.replaceChildren(video);
    const playback = video.play();
    if (playback && typeof playback.catch === 'function') playback.catch(() => showPoster(mark));
  }

  fetch(manifestUrl, { cache: 'no-cache', credentials: 'same-origin' })
    .then(response => {
      if (!response.ok) throw new Error(`Living-mark manifest returned ${response.status}`);
      return response.json();
    })
    .then(manifest => {
      const chosen = chooseMark(Array.isArray(manifest.marks) ? manifest.marks : []);
      if (chosen) showMark(chosen);
    })
    .catch(() => {
      // The checked-in SVG remains visible as the no-script and failed-request fallback.
    });
})();
