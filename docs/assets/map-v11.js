/* The Necessary Tangle 0.11 — semantic zoom and map orientation aids. */
(() => {
  'use strict';

  const DATA = window.TANGLE_DATA || {};
  const SVG_NS = 'http://www.w3.org/2000/svg';
  const $ = (id) => document.getElementById(id);
  const state = {
    labelMode: localStorage.getItem('tangle-map-label-mode') || 'auto',
    focusTrail: [],
    pins: new Map(),
    arrange: false,
    hovered: null,
    refreshQueued: false,
  };

  const canonical = (id) => (DATA.canonical_redirects || {})[id] || id;
  const publicNodes = (DATA.nodes || []).filter((node) => node.public_visibility === 'public' && canonical(node.id) === node.id);
  const nodeById = new Map(publicNodes.map((node) => [node.id, node]));
  const nodeByLabel = new Map(publicNodes.map((node) => [String(node.label || '').trim().toLocaleLowerCase(), node.id]));
  const degree = new Map(publicNodes.map((node) => [node.id, 0]));
  const neighbours = new Map(publicNodes.map((node) => [node.id, new Set()]));

  for (const edge of DATA.edges || []) {
    const source = canonical(edge.source);
    const target = canonical(edge.target);
    if (!nodeById.has(source) || !nodeById.has(target) || source === target) continue;
    degree.set(source, (degree.get(source) || 0) + 1);
    degree.set(target, (degree.get(target) || 0) + 1);
    neighbours.get(source)?.add(target);
    neighbours.get(target)?.add(source);
  }

  function nodeId(element) {
    if (!element) return null;
    const direct = element.dataset?.nodeId || element.dataset?.id || element.getAttribute?.('data-node-id') || element.getAttribute?.('data-id');
    if (direct && nodeById.has(canonical(direct))) return canonical(direct);
    const nested = element.querySelector?.('[data-node-id], [data-id]');
    const nestedId = nested?.dataset?.nodeId || nested?.dataset?.id;
    if (nestedId && nodeById.has(canonical(nestedId))) return canonical(nestedId);
    const label = element.querySelector?.('text')?.textContent?.trim().toLocaleLowerCase();
    return label ? nodeByLabel.get(label) || null : null;
  }

  function nodeElements() {
    const root = $('graphNodes');
    if (!root) return [];
    const candidates = [...root.querySelectorAll(':scope > g, .graph-node-group, [data-node-id], [data-id]')];
    const seen = new Set();
    return candidates.filter((element) => {
      const id = nodeId(element);
      if (!id || seen.has(element)) return false;
      seen.add(element);
      return true;
    });
  }

  function semanticRank(id) {
    const node = nodeById.get(id) || {};
    const d = degree.get(id) || 0;
    const level = node.publication_level || '';
    if (level === 'profile' || d >= 10) return 3;
    if (d >= 5) return 2;
    if (d >= 2) return 1;
    return 0;
  }

  function currentTransform() {
    if (window.TangleMap?.getTransform) return window.TangleMap.getTransform();
    const transform = $('graphRoot')?.getAttribute('transform') || '';
    const translate = transform.match(/translate\(([-\d.]+)[ ,]+([-\d.]+)\)/);
    const scale = transform.match(/scale\(([-\d.]+)\)/);
    return {
      x: translate ? Number(translate[1]) : 0,
      y: translate ? Number(translate[2]) : 0,
      scale: scale ? Number(scale[1]) : 1,
    };
  }

  function labelThreshold(scale) {
    if (state.labelMode === 'none') return 4;
    if (state.labelMode === 'key') return 3;
    if (state.labelMode === 'all') return 0;
    if (scale < 0.42) return 3;
    if (scale < 0.76) return 2;
    if (scale < 1.28) return 1;
    return 0;
  }

  function decorateNodes() {
    const scale = currentTransform().scale || 1;
    const threshold = labelThreshold(scale);
    for (const element of nodeElements()) {
      const id = nodeId(element);
      if (!id) continue;
      const rank = semanticRank(id);
      element.dataset.semanticRank = String(rank);
      element.dataset.semanticNodeId = id;
      element.dataset.semanticLabel = rank >= threshold ? 'show' : 'hide';
      element.setAttribute('tabindex', '0');
      element.setAttribute('role', 'button');
      element.setAttribute('aria-label', `Inspect ${nodeById.get(id)?.label || id}`);
      const pinned = state.pins.get(id);
      if (pinned && !element.dataset.semanticDragging) {
        element.setAttribute('transform', `translate(${pinned.x} ${pinned.y})`);
        element.classList.add('semantic-pinned');
      }
    }
    const svg = $('graphSvg');
    if (svg) {
      svg.dataset.semanticLabelMode = state.labelMode;
      svg.dataset.semanticThreshold = String(threshold);
      svg.style.setProperty('--semantic-map-scale', String(scale));
    }
    const mode = $('semanticLabelMode');
    if (mode && mode.value !== state.labelMode) mode.value = state.labelMode;
  }

  function mapPoint(clientX, clientY, useRoot = false) {
    const target = useRoot ? $('graphRoot') : $('graphSvg');
    const svg = $('graphSvg');
    if (!target || !svg) return { x: 0, y: 0 };
    const point = svg.createSVGPoint();
    point.x = clientX;
    point.y = clientY;
    const matrix = target.getScreenCTM()?.inverse();
    return matrix ? point.matrixTransform(matrix) : { x: 0, y: 0 };
  }

  function queueRefresh(full = false) {
    if (state.refreshQueued) return;
    state.refreshQueued = true;
    requestAnimationFrame(() => {
      state.refreshQueued = false;
      decorateNodes();
      updateViewport();
      if (full) rebuildMiniMap();
    });
  }

  function rebuildMiniMap() {
    const source = $('graphRoot');
    const miniContent = $('mapMiniContent');
    if (!source || !miniContent) return;
    const clone = source.cloneNode(true);
    clone.removeAttribute('id');
    clone.removeAttribute('transform');
    clone.querySelectorAll('[id]').forEach((element) => element.removeAttribute('id'));
    clone.querySelectorAll('text, foreignObject').forEach((element) => element.remove());
    clone.querySelectorAll('*').forEach((element) => {
      element.removeAttribute('tabindex');
      element.removeAttribute('aria-label');
      element.style.pointerEvents = 'none';
    });
    miniContent.replaceChildren(...clone.childNodes);
    updateViewport();
  }

  function updateViewport() {
    const viewport = $('mapMiniViewport');
    if (!viewport) return;
    const { x, y, scale } = currentTransform();
    const safeScale = Math.max(0.001, scale || 1);
    const width = 1200 / safeScale;
    const height = 760 / safeScale;
    viewport.setAttribute('x', String(-x / safeScale));
    viewport.setAttribute('y', String(-y / safeScale));
    viewport.setAttribute('width', String(width));
    viewport.setAttribute('height', String(height));
    const status = $('semanticMapStatus');
    if (status) {
      const visible = $('mapCount')?.textContent || '0';
      status.textContent = `${Math.round(safeScale * 100)}% · ${visible} items · labels ${state.labelMode}`;
    }
    decorateNodes();
  }

  function setTransform(next) {
    if (window.TangleMap?.setTransform) {
      window.TangleMap.setTransform(next);
      return;
    }
    $('graphRoot')?.setAttribute('transform', `translate(${next.x} ${next.y}) scale(${next.scale})`);
  }

  function zoomBy(factor, clientX = null, clientY = null) {
    const svg = $('graphSvg');
    if (!svg) return;
    const current = currentTransform();
    const rect = svg.getBoundingClientRect();
    const screenX = clientX == null ? 600 : (clientX - rect.left) * 1200 / Math.max(rect.width, 1);
    const screenY = clientY == null ? 380 : (clientY - rect.top) * 760 / Math.max(rect.height, 1);
    const worldX = (screenX - current.x) / current.scale;
    const worldY = (screenY - current.y) / current.scale;
    const scale = Math.min(8, Math.max(0.16, current.scale * factor));
    setTransform({ x: screenX - worldX * scale, y: screenY - worldY * scale, scale });
  }

  function focusHash(id, depth = '1') {
    if (!id) return;
    const params = new URLSearchParams(location.hash.replace(/^#/, ''));
    params.set('view', 'map');
    params.set('focus', id);
    params.set('depth', depth);
    params.set('layer', $('mapLayer')?.value || params.get('layer') || 'substantive');
    location.hash = params.toString();
  }

  function rememberFocus(id) {
    if (!id) return;
    const last = state.focusTrail[state.focusTrail.length - 1];
    if (last?.id === id) return;
    state.focusTrail.push({ id, label: nodeById.get(id)?.label || id });
    if (state.focusTrail.length > 8) state.focusTrail.shift();
    renderTrail();
  }

  function renderTrail() {
    const container = $('semanticFocusTrail');
    if (!container) return;
    if (!state.focusTrail.length) {
      container.innerHTML = '<span>Overview</span>';
      return;
    }
    container.innerHTML = [
      '<button type="button" data-semantic-overview>Overview</button>',
      ...state.focusTrail.map((item, index) => `<button type="button" data-semantic-trail="${index}">${escapeHtml(item.label)}</button>`),
    ].join('<span aria-hidden="true">›</span>');
  }

  function escapeHtml(value) {
    return String(value || '')
      .replaceAll('&', '&amp;')
      .replaceAll('<', '&lt;')
      .replaceAll('>', '&gt;')
      .replaceAll('"', '&quot;')
      .replaceAll("'", '&#039;');
  }

  function clearHover() {
    state.hovered = null;
    $('graphSvg')?.classList.remove('semantic-hover-active');
    nodeElements().forEach((element) => element.classList.remove('semantic-hovered', 'semantic-neighbour', 'semantic-dimmed'));
  }

  function applyHover(id) {
    if (!id || !neighbours.has(id)) return clearHover();
    state.hovered = id;
    const adjacent = neighbours.get(id) || new Set();
    $('graphSvg')?.classList.add('semantic-hover-active');
    for (const element of nodeElements()) {
      const other = nodeId(element);
      element.classList.toggle('semantic-hovered', other === id);
      element.classList.toggle('semantic-neighbour', adjacent.has(other));
      element.classList.toggle('semantic-dimmed', other !== id && !adjacent.has(other));
    }
  }

  function toggleFullscreen() {
    const shell = document.querySelector('.map-layout');
    if (!shell) return;
    if (document.fullscreenElement) document.exitFullscreen?.();
    else shell.requestFullscreen?.();
  }

  function parseTranslate(element) {
    const transform = element.getAttribute('transform') || '';
    const match = transform.match(/translate\(([-\d.]+)[ ,]+([-\d.]+)\)/);
    return match ? { x: Number(match[1]), y: Number(match[2]) } : { x: 0, y: 0 };
  }

  function beginDrag(event, element, id) {
    if (!state.arrange || event.button !== 0) return;
    event.preventDefault();
    event.stopPropagation();
    const start = mapPoint(event.clientX, event.clientY, true);
    const origin = state.pins.get(id) || parseTranslate(element);
    element.dataset.semanticDragging = 'true';
    element.setPointerCapture?.(event.pointerId);

    const move = (moveEvent) => {
      const point = mapPoint(moveEvent.clientX, moveEvent.clientY, true);
      const next = { x: origin.x + point.x - start.x, y: origin.y + point.y - start.y };
      state.pins.set(id, next);
      element.setAttribute('transform', `translate(${next.x} ${next.y})`);
      element.classList.add('semantic-pinned');
      updateViewport();
    };
    const end = () => {
      element.removeEventListener('pointermove', move);
      element.removeEventListener('pointerup', end);
      element.removeEventListener('pointercancel', end);
      delete element.dataset.semanticDragging;
      rebuildMiniMap();
    };
    element.addEventListener('pointermove', move);
    element.addEventListener('pointerup', end);
    element.addEventListener('pointercancel', end);
  }

  function bindNodeEvents() {
    for (const element of nodeElements()) {
      if (element.dataset.semanticBound === 'true') continue;
      element.dataset.semanticBound = 'true';
      const id = nodeId(element);
      if (!id) continue;
      element.addEventListener('click', () => rememberFocus(id));
      element.addEventListener('dblclick', (event) => {
        event.preventDefault();
        event.stopPropagation();
        rememberFocus(id);
        focusHash(id, '1');
      });
      element.addEventListener('mouseenter', () => applyHover(id));
      element.addEventListener('mouseleave', clearHover);
      element.addEventListener('focus', () => applyHover(id));
      element.addEventListener('blur', clearHover);
      element.addEventListener('keydown', (event) => {
        if (event.key === 'Enter' || event.key === ' ') {
          event.preventDefault();
          rememberFocus(id);
          focusHash(id, '1');
        }
      });
      element.addEventListener('pointerdown', (event) => beginDrag(event, element, id));
    }
  }

  function installToolbar() {
    if ($('semanticMapToolbar')) return;
    const wrap = document.querySelector('.graph-wrap');
    if (!wrap) return;
    const toolbar = document.createElement('div');
    toolbar.id = 'semanticMapToolbar';
    toolbar.className = 'semantic-map-toolbar';
    toolbar.setAttribute('aria-label', 'Map orientation and semantic zoom');
    toolbar.innerHTML = `
      <div class="semantic-map-actions">
        <button type="button" id="semanticOverview">Overview</button>
        <button type="button" id="semanticBack" title="Return to the previous focus">Back</button>
        <button type="button" id="semanticZoomOut" aria-label="Zoom out">−</button>
        <button type="button" id="semanticZoomIn" aria-label="Zoom in">+</button>
        <button type="button" id="semanticFit">Fit</button>
        <button type="button" id="semanticFullscreen">Fullscreen</button>
      </div>
      <div class="semantic-map-options">
        <label>Labels
          <select id="semanticLabelMode">
            <option value="auto">Adaptive</option>
            <option value="key">Key labels</option>
            <option value="all">All labels</option>
            <option value="none">No labels</option>
          </select>
        </label>
        <label class="semantic-arrange-label"><input id="semanticArrange" type="checkbox"> Arrange</label>
        <button type="button" id="semanticClearPins">Reset arrangement</button>
      </div>
      <div id="semanticFocusTrail" class="semantic-focus-trail" aria-label="Map focus trail"><span>Overview</span></div>
      <p id="semanticMapStatus" class="semantic-map-status" aria-live="polite"></p>`;
    wrap.prepend(toolbar);

    const mini = document.createElementNS(SVG_NS, 'svg');
    mini.setAttribute('id', 'mapMiniMap');
    mini.setAttribute('class', 'map-minimap');
    mini.setAttribute('viewBox', '0 0 1200 760');
    mini.setAttribute('role', 'img');
    mini.setAttribute('aria-label', 'Map overview. Select a place to move the main map.');
    mini.innerHTML = '<g id="mapMiniContent"></g><rect id="mapMiniViewport" x="0" y="0" width="1200" height="760"></rect>';
    wrap.append(mini);

    $('semanticLabelMode').value = state.labelMode;
    $('semanticLabelMode').addEventListener('change', (event) => {
      state.labelMode = event.target.value;
      localStorage.setItem('tangle-map-label-mode', state.labelMode);
      queueRefresh();
    });
    $('semanticOverview').addEventListener('click', () => {
      state.focusTrail = [];
      renderTrail();
      const params = new URLSearchParams(location.hash.replace(/^#/, ''));
      params.set('view', 'map');
      params.set('depth', 'all');
      params.delete('focus');
      location.hash = params.toString();
      setTimeout(() => window.TangleMap?.fit?.(), 80);
    });
    $('semanticBack').addEventListener('click', () => {
      if (state.focusTrail.length > 1) {
        state.focusTrail.pop();
        const target = state.focusTrail[state.focusTrail.length - 1];
        renderTrail();
        focusHash(target.id, '1');
      } else {
        history.back();
      }
    });
    $('semanticZoomIn').addEventListener('click', () => zoomBy(1.24));
    $('semanticZoomOut').addEventListener('click', () => zoomBy(1 / 1.24));
    $('semanticFit').addEventListener('click', () => window.TangleMap?.fit?.() || $('mapFit')?.click());
    $('semanticFullscreen').addEventListener('click', toggleFullscreen);
    $('semanticArrange').addEventListener('change', (event) => {
      state.arrange = event.target.checked;
      $('graphSvg')?.classList.toggle('semantic-arrange-active', state.arrange);
    });
    $('semanticClearPins').addEventListener('click', () => {
      state.pins.clear();
      document.querySelector('.map-controls #mapReset')?.click();
      queueRefresh(true);
    });
    $('semanticFocusTrail').addEventListener('click', (event) => {
      const overview = event.target.closest('[data-semantic-overview]');
      if (overview) return $('semanticOverview').click();
      const button = event.target.closest('[data-semantic-trail]');
      if (!button) return;
      const index = Number(button.dataset.semanticTrail);
      const target = state.focusTrail[index];
      if (!target) return;
      state.focusTrail = state.focusTrail.slice(0, index + 1);
      renderTrail();
      focusHash(target.id, '1');
    });
    mini.addEventListener('click', (event) => {
      const point = mapPoint(event.clientX, event.clientY, false);
      const current = currentTransform();
      setTransform({ x: 600 - point.x * current.scale, y: 380 - point.y * current.scale, scale: current.scale });
    });
  }

  function bindGlobalEvents() {
    document.addEventListener('keydown', (event) => {
      if (!document.getElementById('view-map')?.classList.contains('active')) return;
      if (/^(INPUT|TEXTAREA|SELECT)$/.test(event.target?.tagName || '')) return;
      if (event.key === '+' || event.key === '=') {
        event.preventDefault();
        zoomBy(1.2);
      } else if (event.key === '-' || event.key === '_') {
        event.preventDefault();
        zoomBy(1 / 1.2);
      } else if (event.key === '0') {
        event.preventDefault();
        window.TangleMap?.fit?.() || $('mapFit')?.click();
      } else if (event.key.toLocaleLowerCase() === 'f') {
        event.preventDefault();
        toggleFullscreen();
      } else if (event.key.toLocaleLowerCase() === 'l') {
        const modes = ['auto', 'key', 'all', 'none'];
        state.labelMode = modes[(modes.indexOf(state.labelMode) + 1) % modes.length];
        localStorage.setItem('tangle-map-label-mode', state.labelMode);
        queueRefresh();
      } else if (event.key === 'Escape') {
        clearHover();
      }
    });
    document.addEventListener('fullscreenchange', () => {
      document.querySelector('.map-layout')?.classList.toggle('semantic-fullscreen', Boolean(document.fullscreenElement));
      setTimeout(() => window.TangleMap?.fit?.(), 50);
    });
  }

  function observeMap() {
    const root = $('graphRoot');
    const nodes = $('graphNodes');
    if (root) {
      new MutationObserver(() => queueRefresh()).observe(root, { attributes: true, attributeFilter: ['transform'] });
    }
    if (nodes) {
      new MutationObserver(() => {
        bindNodeEvents();
        queueRefresh(true);
      }).observe(nodes, { childList: true, subtree: true });
    }
    if (window.ResizeObserver && document.querySelector('.graph-wrap')) {
      new ResizeObserver(() => updateViewport()).observe(document.querySelector('.graph-wrap'));
    }
  }

  function init() {
    if (!$('graphSvg')) return;
    installToolbar();
    bindNodeEvents();
    bindGlobalEvents();
    observeMap();
    renderTrail();
    queueRefresh(true);
    document.documentElement.classList.add('semantic-map-ready');
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
