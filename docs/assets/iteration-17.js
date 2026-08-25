(() => {
  'use strict';
  const DATA = window.TANGLE_DATA || {};
  const redirects = DATA.canonical_redirects || {};
  const canonical = (id) => redirects[id] || id;
  const excludedTypes = new Set(['corpus', 'source', 'evidence', 'claim']);

  function eligible() {
    return (DATA.nodes || []).filter((node) =>
      node.public_visibility === 'public'
      && canonical(node.id) === node.id
      && node.status === 'accepted'
      && ['profile', 'described'].includes(node.publication_level)
      && !excludedTypes.has(node.entity_type)
      && String(node.description || node.canonical_definition || '').trim().length >= 80
    );
  }

  function currentId() {
    const params = new URLSearchParams(window.location.hash.replace(/^#/, ''));
    return params.get('id') || '';
  }

  function randomIndex(length) {
    if (length < 2) return 0;
    if (window.crypto && window.crypto.getRandomValues) {
      const values = new Uint32Array(1);
      window.crypto.getRandomValues(values);
      return values[0] % length;
    }
    return Math.floor(Math.random() * length);
  }

  function surprise() {
    const pool = eligible();
    if (!pool.length) return;
    const current = currentId();
    const alternatives = pool.filter((node) => node.id !== current);
    const choicePool = alternatives.length ? alternatives : pool;
    const node = choicePool[randomIndex(choicePool.length)];
    window.location.hash = `view=item&id=${encodeURIComponent(node.id)}&from=surprise`;
  }

  function attach() {
    document.querySelectorAll('#surpriseMeNav, #surpriseMeHero, .surprise-me').forEach((button) => {
      // Release 0.18 turns these controls into genuine links and owns their
      // pointer, keyboard and modified-click behaviour. Retain this handler
      // only for an older generated button.
      if (button instanceof HTMLAnchorElement) return;
      if (button.dataset.surpriseReady === 'true') return;
      button.dataset.surpriseReady = 'true';
      button.addEventListener('click', surprise);
    });
  }

  document.addEventListener('DOMContentLoaded', attach);
  window.addEventListener('hashchange', attach);
  attach();
})();
