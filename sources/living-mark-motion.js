/* Muted autoplay with a compact, accessible pause control. No text-width button. */
(() => {
  'use strict';
  const host = document.querySelector('[data-living-mark]');
  if (!host) return;
  document.querySelectorAll('.living-mark-playback').forEach(el => el.remove());
  const preference = window.matchMedia('(prefers-reduced-motion: reduce)');
  const anchor = host.closest('a');
  let userPaused = false;
  let observed;
  const button = document.createElement('button');
  button.type = 'button';
  button.className = 'living-mark-toggle';
  button.hidden = true;
  (anchor || host).insertAdjacentElement('afterend', button);
  const icons = {
    pause: '<svg aria-hidden="true" viewBox="0 0 24 24"><path d="M7 5h4v14H7zm6 0h4v14h-4z"/></svg>',
    play: '<svg aria-hidden="true" viewBox="0 0 24 24"><path d="M7 4l14 8-14 8z"/></svg>'
  };
  function sync() {
    const video = host.querySelector('video');
    button.hidden = !video || preference.matches;
    if (!video) return;
    const label = video.paused ? 'Resume animation' : 'Pause animation';
    button.innerHTML = video.paused ? icons.play : icons.pause;
    button.setAttribute('aria-label', label);
    button.title = label;
  }
  function play(video) {
    if (!video || preference.matches || userPaused || document.hidden) return;
    video.muted = true;
    video.defaultMuted = true;
    video.autoplay = true;
    video.loop = true;
    video.playsInline = true;
    video.preload = 'auto';
    ['autoplay', 'muted', 'loop', 'playsinline'].forEach(name => video.setAttribute(name, ''));
    const attempt = video.play();
    if (attempt && attempt.catch) attempt.catch(() => sync());
  }
  function observe() {
    const video = host.querySelector('video');
    if (video && video !== observed) {
      observed = video;
      ['play', 'pause', 'loadeddata'].forEach(name => video.addEventListener(name, sync));
      if (preference.matches) video.pause(); else play(video);
    }
    sync();
  }
  new MutationObserver(observe).observe(host, {childList: true});
  button.addEventListener('click', () => {
    const video = host.querySelector('video');
    if (!video) return;
    userPaused = !video.paused;
    if (userPaused) video.pause(); else play(video);
    sync();
  });
  document.addEventListener('visibilitychange', () => {
    if (!document.hidden) play(host.querySelector('video'));
  });
  // Respect browser autoplay policy; one ordinary user interaction can permit playback.
  ['pointerdown', 'keydown'].forEach(name => document.addEventListener(name, event => {
    if (!button.contains(event.target)) play(host.querySelector('video'));
  }, {once: true}));
  preference.addEventListener('change', () => {
    const video = host.querySelector('video');
    if (video && preference.matches) video.pause(); else play(video);
    sync();
  });
  observe();
})();
