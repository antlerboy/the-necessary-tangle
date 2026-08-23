(() => {
  'use strict';

  const DATA = window.TANGLE_DATA || {};
  const redirects = DATA.canonical_redirects || {};
  const canonical = (id) => redirects[id] || id;
  const nodes = new Map((DATA.nodes || []).map((node) => [node.id, node]));
  const eligibleTypes = new Set(['profile', 'described']);
  const excludedTypes = new Set(['corpus', 'source', 'evidence', 'claim']);

  function plainLeftClick(event) {
    return event.button === 0 && !event.metaKey && !event.ctrlKey && !event.shiftKey && !event.altKey;
  }

  function randomIndex(length) {
    if (length < 2) return 0;
    if (window.crypto?.getRandomValues) {
      const values = new Uint32Array(1);
      window.crypto.getRandomValues(values);
      return values[0] % length;
    }
    return Math.floor(Math.random() * length);
  }

  function surprisePool() {
    return (DATA.nodes || []).filter((node) =>
      node.public_visibility === 'public'
      && canonical(node.id) === node.id
      && node.status === 'accepted'
      && eligibleTypes.has(node.publication_level)
      && !excludedTypes.has(node.entity_type)
      && String(node.description || node.canonical_definition || '').trim().length >= 80
    );
  }

  function chooseSurprise(anchor) {
    const pool = surprisePool();
    if (!pool.length) return null;
    const params = new URLSearchParams(location.hash.replace(/^#/, ''));
    const current = canonical(params.get('id') || '');
    const alternatives = pool.filter((node) => node.id !== current);
    const source = alternatives.length ? alternatives : pool;
    const choice = source[randomIndex(source.length)];
    anchor.href = `#view=item&id=${encodeURIComponent(choice.id)}&from=surprise`;
    anchor.dataset.surpriseTarget = choice.id;
    return choice;
  }

  function prepareSurpriseAnchors() {
    document.querySelectorAll('#surpriseMeNav, #surpriseMeHero, .surprise-me').forEach((anchor) => {
      if (!(anchor instanceof HTMLAnchorElement) || anchor.dataset.surprise18 === 'true') return;
      anchor.dataset.surprise18 = 'true';
      const prepare = () => chooseSurprise(anchor);
      anchor.addEventListener('pointerenter', prepare);
      anchor.addEventListener('focus', prepare);
      anchor.addEventListener('contextmenu', prepare);
      anchor.addEventListener('auxclick', prepare);
      anchor.addEventListener('click', (event) => {
        if (!plainLeftClick(event)) {
          prepare();
          return;
        }
        event.preventDefault();
        event.stopImmediatePropagation();
        const choice = chooseSurprise(anchor);
        if (choice) location.hash = `view=item&id=${encodeURIComponent(choice.id)}&from=surprise`;
      }, true);
      prepare();
    });
  }

  function currentEntryId() {
    const params = new URLSearchParams(location.hash.replace(/^#/, ''));
    return canonical(params.get('id') || '');
  }

  function currentReturnView() {
    const params = new URLSearchParams(location.hash.replace(/^#/, ''));
    const from = params.get('from') || 'browse';
    return ['home', 'browse', 'journeys', 'map', 'ask', 'contribute', 'about', 'ai-observations'].includes(from) ? from : 'browse';
  }

  function edgeFor(id) {
    return (DATA.edges || []).find((edge) => edge.id === id);
  }

  function enhanceEntry() {
    const drawer = document.getElementById('entryDrawer');
    const body = document.getElementById('drawerBody');
    if (!drawer || !body || !drawer.classList.contains('open')) {
      document.body.classList.remove('entry-open');
      return;
    }
    document.body.classList.add('entry-open');
    const head = body.querySelector('.entry-head');
    if (!head) return;

    const entryId = currentEntryId();
    const node = nodes.get(entryId);
    if (!body.querySelector('.entry-back-link')) {
      const back = document.createElement('a');
      const returnView = currentReturnView();
      back.className = 'entry-back-link';
      back.href = `#view=${encodeURIComponent(returnView)}`;
      back.textContent = returnView === 'map' ? '← Back to the map' : '← Back to the atlas';
      body.insertBefore(back, head);
    }

    const sections = [...body.querySelectorAll('.entry-section')];
    const connections = sections.find((section) => section.querySelector('h2')?.textContent.trim() === 'Connections');
    if (connections) {
      connections.classList.add('connections-priority');
      if (head.nextElementSibling !== connections) head.insertAdjacentElement('afterend', connections);
    }

    if (!body.querySelector('.entry-orientation') && node) {
      const depth = DATA.relational_depth?.by_node?.[entryId] || {};
      const orientation = document.createElement('div');
      orientation.className = 'entry-orientation';
      orientation.innerHTML = `
        <a href="#view=map&layer=substantive&depth=constellation&focus=${encodeURIComponent(entryId)}"><strong>Place in the tangle</strong><br><span>${depth.reader_connections ?? 0} reader connections across ${depth.distinct_reader_families ?? 0} relation families</span></a>
        <a href="#view=ask&seed=${encodeURIComponent(entryId)}"><strong>Ask the atlas</strong><br><span>Use this entry as the starting point for a source-aware question.</span></a>
        <a href="#view=contribute&entry=${encodeURIComponent(entryId)}"><strong>Challenge or add</strong><br><span>Prepare a public correction, source or competing interpretation.</span></a>`;
      if (connections) connections.insertAdjacentElement('beforebegin', orientation);
      else head.insertAdjacentElement('afterend', orientation);
    }

    body.querySelectorAll('button.inspect-edge').forEach((button) => {
      const edge = edgeFor(button.dataset.edge);
      if (!edge) return;
      const link = document.createElement('a');
      link.className = 'text-button inspect-edge-link';
      link.dataset.edge = button.dataset.edge;
      link.href = `#view=map&layer=substantive&depth=constellation&focus=${encodeURIComponent(canonical(edge.source))}&edge=${encodeURIComponent(edge.id)}`;
      link.textContent = button.textContent || 'Inspect this connection';
      button.replaceWith(link);
    });
  }

  function visibleGraphEdges() {
    return [...document.querySelectorAll('#graphEdges .graph-edge-group')]
      .map((group) => edgeFor(group.dataset.edge))
      .filter(Boolean);
  }

  function mapFocus() {
    const params = new URLSearchParams(location.hash.replace(/^#/, ''));
    return canonical(params.get('focus') || document.querySelector('#graphNodes .graph-node-group.selected')?.dataset.id || '');
  }

  function enhanceMap() {
    const svg = document.getElementById('graphSvg');
    if (!svg) return;
    const depth = document.getElementById('mapDepth')?.value || '';
    svg.dataset.depth = depth;
    const focus = mapFocus();
    const nodeGroups = [...svg.querySelectorAll('#graphNodes .graph-node-group')];
    if (!focus || !nodeGroups.length) return;

    const adjacency = new Map();
    visibleGraphEdges().forEach((edge) => {
      const source = canonical(edge.source);
      const target = canonical(edge.target);
      if (!adjacency.has(source)) adjacency.set(source, new Set());
      if (!adjacency.has(target)) adjacency.set(target, new Set());
      adjacency.get(source).add(target);
      adjacency.get(target).add(source);
    });
    const distances = new Map([[focus, 0]]);
    const queue = [focus];
    while (queue.length) {
      const id = queue.shift();
      const distance = distances.get(id);
      if (distance >= 2) continue;
      (adjacency.get(id) || []).forEach((other) => {
        if (!distances.has(other)) {
          distances.set(other, distance + 1);
          queue.push(other);
        }
      });
    }
    nodeGroups.forEach((group) => {
      const distance = distances.get(canonical(group.dataset.id));
      group.dataset.orbit = distance === 0 ? 'core' : distance === 1 ? 'inner' : 'outer';
    });

    const toolbar = document.querySelector('.map-canvas-toolbar');
    if (toolbar && !toolbar.parentElement.querySelector('.map-orbit-key')) {
      const key = document.createElement('div');
      key.className = 'map-orbit-key';
      key.innerHTML = '<span>Star: selected entry</span><span>Inner orbit: direct relations</span><span>Outer orbit: two steps</span>';
      toolbar.insertAdjacentElement('afterend', key);
    }
  }

  function runEnhancements() {
    prepareSurpriseAnchors();
    enhanceEntry();
    enhanceMap();
  }

  document.addEventListener('DOMContentLoaded', () => {
    runEnhancements();
    const observer = new MutationObserver(runEnhancements);
    observer.observe(document.body, { childList: true, subtree: true, attributes: true, attributeFilter: ['class'] });
  });
  window.addEventListener('hashchange', () => requestAnimationFrame(runEnhancements));
})();
