(() => {
  'use strict';

  const $ = (selector) => document.querySelector(selector);
  const esc = (value) => String(value ?? '').replace(/[&<>"']/g, (char) => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[char]));
  const number = (value) => Number(value || 0).toLocaleString('en-GB');
  const clamp = (value, lower, upper) => Math.max(lower, Math.min(upper, value));
  const DEFAULT_NODE = 'n1';
  const DEFAULT_STATE = { view: 'focus', depth: 1, realm: 'all', filter: 'all' };

  Promise.all([
    fetch('/assets/comparator-systemic-evolution.json').then((response) => {
      if (!response.ok) throw new Error(`Comparator data returned ${response.status}`);
      return response.json();
    }),
    fetch('/assets/systemic-evolution-reconciliation.json').then((response) => {
      if (!response.ok) throw new Error(`Reconciliation data returned ${response.status}`);
      return response.json();
    })
  ]).then(([map, reconciliation]) => start(map, reconciliation)).catch((error) => {
    $('#systemicPanel').innerHTML = `<h2>Map unavailable</h2><p>${esc(error.message)}</p><p><a href="/assets/comparator-systemic-evolution.json">Open the source data directly</a>.</p>`;
    $('#systemicViewSummary').textContent = 'The interactive view could not be loaded. The complete data downloads remain available.';
  });

  function start(map, reconciliation) {
    const canvas = $('#systemicCanvas');
    const context = canvas.getContext('2d');
    const panel = $('#systemicPanel');
    const search = $('#systemicSearch');
    const suggestions = $('#systemicSuggestions');
    const viewControl = $('#systemicView');
    const depthControl = $('#systemicDepth');
    const realmControl = $('#systemicRealm');
    const filterControl = $('#systemicFilter');
    const reset = $('#systemicReset');
    const zoomIn = $('#systemicZoomIn');
    const zoomOut = $('#systemicZoomOut');
    const fit = $('#systemicFit');
    const summaryElement = $('#systemicViewSummary');
    const textView = $('#systemicTextView');
    const visibleNodesElement = $('#systemicVisibleNodes');
    const visibleLinksElement = $('#systemicVisibleLinks');

    const nodes = map.nodes;
    const edges = map.edges;
    const byId = new Map(nodes.map((node) => [node.source_node_id, node]));
    const adjacent = new Map(nodes.map((node) => [node.source_node_id, []]));
    edges.forEach((edge) => {
      adjacent.get(edge.source_node_id)?.push(edge);
      adjacent.get(edge.target_node_id)?.push(edge);
    });

    const reconciliationSummary = reconciliation.meta.summary;
    $('#statNodes').textContent = number(reconciliationSummary.source_nodes_retained);
    $('#statLinks').textContent = number(reconciliationSummary.source_links_retained);
    $('#statMapped').textContent = number(
      reconciliationSummary.source_nodes_confirmed +
      reconciliationSummary.source_nodes_partially_reconciled
    );
    $('#statAtlas').textContent = number(reconciliationSummary.distinct_atlas_entries_linked);

    suggestions.innerHTML = [...nodes]
      .sort((a, b) => a.label.localeCompare(b.label))
      .map((node) => `<option value="${esc(node.label)}"></option>`)
      .join('');
    const realms = [...new Set(nodes.map((node) => node.official_realm).filter(Boolean))].sort();
    realms.forEach((realm) => {
      const option = document.createElement('option');
      option.value = realm;
      option.textContent = realm;
      realmControl.append(option);
    });

    const allowedViews = new Set(['focus', 'full']);
    const allowedFilters = new Set(['all', 'both', 'one', 'none']);
    const allowedRealms = new Set(['all', ...realms]);
    const query = new URLSearchParams(location.search);
    const state = {
      selectedId: byId.has(query.get('node')) ? query.get('node') : DEFAULT_NODE,
      view: allowedViews.has(query.get('view')) ? query.get('view') : DEFAULT_STATE.view,
      depth: query.get('depth') === '2' ? 2 : DEFAULT_STATE.depth,
      realm: allowedRealms.has(query.get('realm')) ? query.get('realm') : DEFAULT_STATE.realm,
      filter: allowedFilters.has(query.get('status')) ? query.get('status') : DEFAULT_STATE.filter,
      hoverId: null,
      transform: { scale: 1, x: 0, y: 0 }
    };

    let width = 0;
    let height = 0;
    let positions = new Map();
    let distances = new Map();
    let visibleNodes = [];
    let visibleEdges = [];
    let visibleNodeIds = new Set();
    let hitRegions = new Map();
    let pointer = null;
    let textViewDirty = true;

    function selectedNode() {
      return byId.get(state.selectedId) || byId.get(DEFAULT_NODE) || nodes[0];
    }

    function edgePasses(edge) {
      return state.filter === 'all' || edge.reconciliation_status === state.filter;
    }

    function edgeFlow(edge) {
      if (edge.direction_status === 'bidirectional') {
        return { from: edge.source_node_id, to: edge.target_node_id, bidirectional: true };
      }
      if (edge.direction_status === 'target_to_source') {
        return { from: edge.target_node_id, to: edge.source_node_id, bidirectional: false };
      }
      return { from: edge.source_node_id, to: edge.target_node_id, bidirectional: false };
    }

    function computeVisibleGraph() {
      distances = new Map([[state.selectedId, 0]]);
      let candidateIds;
      if (state.view === 'full') {
        candidateIds = new Set(nodes.map((node) => node.source_node_id));
      } else {
        const queue = [state.selectedId];
        while (queue.length) {
          const current = queue.shift();
          const distance = distances.get(current);
          if (distance >= state.depth) continue;
          (adjacent.get(current) || []).filter(edgePasses).forEach((edge) => {
            const other = edge.source_node_id === current ? edge.target_node_id : edge.source_node_id;
            if (!distances.has(other)) {
              distances.set(other, distance + 1);
              queue.push(other);
            }
          });
        }
        candidateIds = new Set(distances.keys());
      }

      if (state.realm !== 'all') {
        candidateIds = new Set([...candidateIds].filter((id) => (
          id === state.selectedId || byId.get(id)?.official_realm === state.realm
        )));
      }
      visibleNodeIds = candidateIds;
      visibleNodes = nodes.filter((node) => candidateIds.has(node.source_node_id));
      visibleEdges = edges.filter((edge) => (
        edgePasses(edge) &&
        candidateIds.has(edge.source_node_id) &&
        candidateIds.has(edge.target_node_id)
      ));
    }

    function placeColumns(ids, side, result) {
      const maxRows = 9;
      const columnWidth = 260;
      const rowHeight = 65;
      ids.forEach((id, index) => {
        const column = Math.floor(index / maxRows);
        const positionInColumn = index % maxRows;
        const countInColumn = Math.min(maxRows, ids.length - column * maxRows);
        result.set(id, {
          x: side * (290 + column * columnWidth),
          y: (positionInColumn - (countInColumn - 1) / 2) * rowHeight
        });
      });
    }

    function computePositions() {
      if (state.view === 'full') {
        positions = new Map(visibleNodes.map((node) => [node.source_node_id, {
          x: Number(node.x || 0) + Number(node.width || 0) / 2,
          y: Number(node.y || 0) + Number(node.height || 0) / 2
        }]));
        return;
      }

      const result = new Map([[state.selectedId, { x: 0, y: 0 }]]);
      const direct = visibleNodes
        .filter((node) => distances.get(node.source_node_id) === 1)
        .map((node) => node.source_node_id)
        .sort((a, b) => byId.get(a).label.localeCompare(byId.get(b).label));
      const incoming = [];
      const outgoing = [];
      const reciprocal = [];
      direct.forEach((id) => {
        const flows = (adjacent.get(state.selectedId) || [])
          .filter((edge) => edgePasses(edge) && (
            edge.source_node_id === id || edge.target_node_id === id
          ))
          .map(edgeFlow);
        const isIncoming = flows.some((flow) => flow.bidirectional || flow.to === state.selectedId);
        const isOutgoing = flows.some((flow) => flow.bidirectional || flow.from === state.selectedId);
        if (isIncoming && isOutgoing) reciprocal.push(id);
        else if (isIncoming) incoming.push(id);
        else outgoing.push(id);
      });
      reciprocal.forEach((id, index) => (index % 2 ? outgoing : incoming).push(id));
      const balancedSideCount = Math.ceil(direct.length / 2);
      while (outgoing.length > balancedSideCount) incoming.push(outgoing.pop());
      while (incoming.length > balancedSideCount) outgoing.push(incoming.pop());
      placeColumns(incoming, -1, result);
      placeColumns(outgoing, 1, result);

      const second = visibleNodes
        .filter((node) => distances.get(node.source_node_id) === 2)
        .sort((a, b) => a.label.localeCompare(b.label));
      second.forEach((node, index) => {
        const angle = (Math.PI * 2 * index) / Math.max(1, second.length) - Math.PI / 2;
        const radiusX = 650 + (index % 3) * 28;
        const radiusY = 430 + (index % 4) * 22;
        result.set(node.source_node_id, {
          x: Math.cos(angle) * radiusX,
          y: Math.sin(angle) * radiusY
        });
      });
      positions = result;
    }

    function screenPoint(point) {
      return {
        x: point.x * state.transform.scale + state.transform.x,
        y: point.y * state.transform.scale + state.transform.y
      };
    }

    function fitView() {
      if (!positions.size || !width || !height) return;
      const points = [...positions.values()];
      const xs = points.map((point) => point.x);
      const ys = points.map((point) => point.y);
      const minX = Math.min(...xs);
      const maxX = Math.max(...xs);
      const minY = Math.min(...ys);
      const maxY = Math.max(...ys);
      const padding = state.view === 'focus' ? 112 : 34;
      const scaleX = (width - padding * 2) / Math.max(1, maxX - minX);
      const scaleY = (height - padding * 2) / Math.max(1, maxY - minY);
      const maximum = state.view === 'focus' ? 1.15 : 2;
      const minimum = state.view === 'focus' && state.depth === 1 ? 0.62 : 0.06;
      state.transform.scale = clamp(Math.min(scaleX, scaleY), minimum, maximum);
      state.transform.x = width / 2 - ((minX + maxX) / 2) * state.transform.scale;
      state.transform.y = height / 2 - ((minY + maxY) / 2) * state.transform.scale;
      draw();
    }

    function zoomAt(factor, x = width / 2, y = height / 2) {
      const previous = state.transform.scale;
      const next = clamp(previous * factor, 0.04, 8);
      const ratio = next / previous;
      state.transform.x = x - (x - state.transform.x) * ratio;
      state.transform.y = y - (y - state.transform.y) * ratio;
      state.transform.scale = next;
      draw();
    }

    function sourceColour(value) {
      return /^#[0-9a-f]{6}$/i.test(value || '') ? value : '#777777';
    }

    function roundedRect(x, y, w, h, radius) {
      const r = Math.min(radius, w / 2, h / 2);
      context.beginPath();
      context.moveTo(x + r, y);
      context.arcTo(x + w, y, x + w, y + h, r);
      context.arcTo(x + w, y + h, x, y + h, r);
      context.arcTo(x, y + h, x, y, r);
      context.arcTo(x, y, x + w, y, r);
      context.closePath();
    }

    function labelLines(label, limit = 25) {
      const words = String(label).split(/\s+/).filter(Boolean);
      const lines = ['', ''];
      words.forEach((word) => {
        const index = lines[0].length < limit ? 0 : 1;
        if (index === 1 && `${lines[1]} ${word}`.trim().length > limit) return;
        lines[index] = `${lines[index]} ${word}`.trim();
      });
      if (words.join(' ').length > lines.join(' ').length) {
        lines[1] = `${lines[1].slice(0, Math.max(0, limit - 1)).trim()}…`;
      }
      return lines.filter(Boolean);
    }

    function drawArrow(a, b, colour, reverse = false) {
      const start = reverse ? b : a;
      const end = reverse ? a : b;
      const angle = Math.atan2(end.y - start.y, end.x - start.x);
      const size = 5.5;
      const tip = {
        x: end.x - Math.cos(angle) * 7,
        y: end.y - Math.sin(angle) * 7
      };
      context.fillStyle = colour;
      context.beginPath();
      context.moveTo(tip.x, tip.y);
      context.lineTo(tip.x - Math.cos(angle - 0.55) * size, tip.y - Math.sin(angle - 0.55) * size);
      context.lineTo(tip.x - Math.cos(angle + 0.55) * size, tip.y - Math.sin(angle + 0.55) * size);
      context.closePath();
      context.fill();
    }

    function shouldLabel(node) {
      if (node.source_node_id === state.selectedId || node.source_node_id === state.hoverId) return true;
      return state.view === 'focus' && distances.get(node.source_node_id) === 1 && (
        state.depth === 1 || state.transform.scale >= 0.55
      );
    }

    function drawNode(node, point) {
      const selected = node.source_node_id === state.selectedId;
      const hovered = node.source_node_id === state.hoverId;
      const mapped = node.reconciliation_status !== 'unresolved';
      const labelled = shouldLabel(node);
      const border = sourceColour(node.border_colour);
      if (labelled) {
        const boxWidth = selected ? 190 : 156;
        const boxHeight = selected ? 48 : 38;
        const x = point.x - boxWidth / 2;
        const y = point.y - boxHeight / 2;
        roundedRect(x, y, boxWidth, boxHeight, 7);
        context.fillStyle = selected ? '#171717' : hovered ? '#fff1cf' : '#fffdf7';
        context.fill();
        context.strokeStyle = selected ? '#171717' : border;
        context.lineWidth = selected ? 2.5 : hovered ? 2.2 : 1.4;
        context.stroke();
        context.beginPath();
        context.arc(x + 10, y + 10, mapped ? 4 : 3, 0, Math.PI * 2);
        context.fillStyle = mapped ? '#9f161b' : '#f7f1e4';
        context.fill();
        context.strokeStyle = mapped ? '#9f161b' : '#777777';
        context.lineWidth = 1;
        context.stroke();
        const lines = labelLines(node.label, selected ? 27 : 22);
        context.fillStyle = selected ? '#ffffff' : '#171717';
        context.font = `${selected ? 600 : 500} ${selected ? 12.5 : 11.5}px system-ui, sans-serif`;
        context.textAlign = 'center';
        context.textBaseline = 'middle';
        const lineHeight = selected ? 15 : 14;
        lines.forEach((line, index) => {
          context.fillText(line, point.x, point.y + (index - (lines.length - 1) / 2) * lineHeight, boxWidth - 24);
        });
        hitRegions.set(node.source_node_id, { x, y, width: boxWidth, height: boxHeight });
        return;
      }

      const radius = mapped ? 4 : 2.5;
      context.beginPath();
      context.arc(point.x, point.y, radius, 0, Math.PI * 2);
      context.fillStyle = mapped ? '#9f161b' : '#f7f1e4';
      context.fill();
      context.strokeStyle = mapped ? '#9f161b' : border;
      context.lineWidth = hovered ? 2 : 0.9;
      context.stroke();
      hitRegions.set(node.source_node_id, {
        x: point.x - 9, y: point.y - 9, width: 18, height: 18
      });
    }

    function draw() {
      context.clearRect(0, 0, width, height);
      context.fillStyle = '#fcfaf4';
      context.fillRect(0, 0, width, height);
      hitRegions = new Map();
      const selectedId = state.selectedId;
      visibleEdges.forEach((edge) => {
        const source = positions.get(edge.source_node_id);
        const target = positions.get(edge.target_node_id);
        if (!source || !target) return;
        const a = screenPoint(source);
        const b = screenPoint(target);
        const onSelected = edge.source_node_id === selectedId || edge.target_node_id === selectedId;
        const colour = sourceColour(edge.line_colour);
        context.globalAlpha = onSelected ? 0.88 : state.view === 'focus' ? 0.22 : selectedId ? 0.045 : 0.12;
        context.strokeStyle = colour;
        context.lineWidth = onSelected ? 2 : clamp(Number(edge.line_width || 1) / 3, 0.45, 1.2);
        context.setLineDash(edge.line_style === 'dashed' ? [4, 3] : []);
        context.beginPath();
        context.moveTo(a.x, a.y);
        context.lineTo(b.x, b.y);
        context.stroke();
        const length = Math.hypot(b.x - a.x, b.y - a.y);
        if (length > 18 && (state.view === 'focus' || onSelected || state.transform.scale > 0.6)) {
          if (edge.direction_status === 'target_to_source') drawArrow(a, b, colour, true);
          else drawArrow(a, b, colour);
          if (edge.direction_status === 'bidirectional') drawArrow(a, b, colour, true);
        }
      });
      context.setLineDash([]);
      context.globalAlpha = 1;
      [...visibleNodes]
        .sort((a, b) => Number(shouldLabel(a)) - Number(shouldLabel(b)))
        .forEach((node) => {
          const position = positions.get(node.source_node_id);
          if (position) drawNode(node, screenPoint(position));
        });
    }

    function pointInRegion(x, y, region) {
      return x >= region.x && x <= region.x + region.width && y >= region.y && y <= region.y + region.height;
    }

    function hitNode(x, y) {
      const ordered = [...hitRegions.entries()].reverse();
      const match = ordered.find(([, region]) => pointInRegion(x, y, region));
      return match ? byId.get(match[0]) : null;
    }

    function edgeText(edge, node) {
      const otherId = edge.source_node_id === node.source_node_id ? edge.target_node_id : edge.source_node_id;
      const other = byId.get(otherId);
      const flow = edgeFlow(edge);
      if (flow.bidirectional) return `↔ ${other.label}`;
      return flow.from === node.source_node_id ? `→ ${other.label}` : `← ${other.label}`;
    }

    function safeSourceUrl(value) {
      try {
        const url = new URL(value);
        return ['http:', 'https:'].includes(url.protocol) ? url.href : '';
      } catch (_) {
        return '';
      }
    }

    function renderPanel() {
      const node = selectedNode();
      const links = (adjacent.get(node.source_node_id) || [])
        .filter(edgePasses)
        .sort((a, b) => edgeText(a, node).localeCompare(edgeText(b, node)));
      const targets = node.atlas_targets || [];
      const sourceUrl = safeSourceUrl(node.source_url);
      panel.innerHTML = `<h2>${esc(node.label)}</h2>
        <p class="pm-small">${esc(node.official_realm)} · source node ${esc(node.source_node_id)}</p>
        <p><span class="pm-badge ${node.reconciliation_status === 'confirmed' ? 'good' : node.reconciliation_status === 'partial' ? 'warn' : ''}">${esc(node.reconciliation_status)}</span></p>
        ${node.source_description ? `<p>${esc(node.source_description)}</p>` : ''}
        ${sourceUrl ? `<p><a href="${esc(sourceUrl)}" target="_blank" rel="noopener">Open the source node’s link</a></p>` : ''}
        ${state.view === 'full' ? '<p><button type="button" id="systemicFocusHere">Focus on this topic</button></p>' : ''}
        ${targets.length ? `<h3>Tangle reconciliation</h3><ul>${targets.map((target) => `<li><a href="/#view=item&id=${encodeURIComponent(target.atlas_id)}&from=home">${esc(target.atlas_label || target.atlas_id)}</a> <span class="pm-small">${esc(target.match_kind)}</span></li>`).join('')}</ul>` : '<p>No human-reviewed Tangle mapping is recorded yet.</p>'}
        <h3>Source-reported links (${number(links.length)})</h3>
        <p class="pm-small">Arrows follow the source and report major influence. Individual lines remain unverified unless separately evidenced in the canonical atlas.</p>
        <ul class="pm-adjacency-list">${links.map((edge) => `<li><button type="button" class="text-button" data-node="${esc(edge.source_node_id === node.source_node_id ? edge.target_node_id : edge.source_node_id)}">${esc(edgeText(edge, node))}</button> <span class="pm-small">${esc(edge.official_realm)} · ${esc(edge.reconciliation_status)}</span></li>`).join('')}</ul>`;
      panel.querySelectorAll('[data-node]').forEach((button) => {
        button.addEventListener('click', () => selectNode(button.dataset.node, true));
      });
      panel.querySelector('#systemicFocusHere')?.addEventListener('click', () => {
        state.view = 'focus';
        viewControl.value = 'focus';
        updateView({ fit: true });
      });
    }

    function directionCells(edge) {
      const flow = edgeFlow(edge);
      if (flow.bidirectional) {
        return { from: byId.get(edge.source_node_id), arrow: '↔', to: byId.get(edge.target_node_id) };
      }
      return { from: byId.get(flow.from), arrow: '→', to: byId.get(flow.to) };
    }

    function renderTextView() {
      textViewDirty = false;
      visibleNodesElement.innerHTML = [...visibleNodes]
        .sort((a, b) => a.label.localeCompare(b.label))
        .map((node) => `<li><button type="button" class="text-button" data-node="${esc(node.source_node_id)}">${esc(node.label)}</button> <span class="pm-small">${esc(node.official_realm)} · ${esc(node.reconciliation_status)}</span></li>`)
        .join('') || '<li>No topics match these controls.</li>';
      visibleLinksElement.innerHTML = visibleEdges.map((edge) => {
        const cells = directionCells(edge);
        return `<tr><td><button type="button" class="text-button" data-node="${esc(cells.from.source_node_id)}">${esc(cells.from.label)}</button></td><td aria-label="${cells.arrow === '↔' ? 'in both directions' : 'influences'}">${cells.arrow}</td><td><button type="button" class="text-button" data-node="${esc(cells.to.source_node_id)}">${esc(cells.to.label)}</button></td><td>${esc(edge.reconciliation_status)}</td></tr>`;
      }).join('') || '<tr><td colspan="4">No source links match these controls.</td></tr>';
      textView.querySelectorAll('[data-node]').forEach((button) => {
        button.addEventListener('click', () => selectNode(button.dataset.node, true));
      });
    }

    function updateUrl() {
      const url = new URL(location.href);
      url.searchParams.set('node', state.selectedId);
      url.searchParams.set('view', state.view);
      url.searchParams.set('depth', String(state.depth));
      url.searchParams.set('realm', state.realm);
      url.searchParams.set('status', state.filter);
      history.replaceState(null, '', url);
    }

    function renderSummary() {
      const node = selectedNode();
      const mode = state.view === 'focus'
        ? `${state.depth === 1 ? 'one' : 'two'}-step neighbourhood of ${node.label}`
        : 'complete source layout';
      const realm = state.realm === 'all' ? 'all realms' : state.realm;
      summaryElement.textContent = `${mode}: ${number(visibleNodes.length)} of ${number(nodes.length)} topics and ${number(visibleEdges.length)} of ${number(edges.length)} source-reported links · ${realm}.`;
    }

    function updateView(options = {}) {
      computeVisibleGraph();
      computePositions();
      depthControl.disabled = state.view === 'full';
      renderSummary();
      renderPanel();
      textViewDirty = true;
      if (textView.open) renderTextView();
      if (options.fit !== false) fitView(); else draw();
      if (options.url !== false) updateUrl();
    }

    function selectNode(id, focusNode, keepFull = false) {
      if (!byId.has(id)) return;
      state.selectedId = id;
      state.hoverId = null;
      search.value = byId.get(id).label;
      if (focusNode && !(keepFull && state.view === 'full')) {
        state.view = 'focus';
        viewControl.value = 'focus';
      }
      updateView({ fit: true });
    }

    function resolveSearch() {
      const value = search.value.trim().toLocaleLowerCase();
      if (!value) return;
      const exact = nodes.find((node) => node.label.toLocaleLowerCase() === value);
      const partial = nodes.find((node) => node.label.toLocaleLowerCase().includes(value));
      if (exact || partial) selectNode((exact || partial).source_node_id, true);
    }

    function resetView() {
      state.selectedId = DEFAULT_NODE;
      state.view = DEFAULT_STATE.view;
      state.depth = DEFAULT_STATE.depth;
      state.realm = DEFAULT_STATE.realm;
      state.filter = DEFAULT_STATE.filter;
      state.hoverId = null;
      search.value = '';
      viewControl.value = state.view;
      depthControl.value = String(state.depth);
      realmControl.value = state.realm;
      filterControl.value = state.filter;
      updateView({ fit: true });
    }

    function canvasCoordinates(event) {
      const box = canvas.getBoundingClientRect();
      return { x: event.clientX - box.left, y: event.clientY - box.top };
    }

    function resize() {
      const box = canvas.getBoundingClientRect();
      const ratio = Math.min(window.devicePixelRatio || 1, 2);
      width = Math.max(320, box.width);
      height = Math.max(460, box.height);
      canvas.width = Math.round(width * ratio);
      canvas.height = Math.round(height * ratio);
      context.setTransform(ratio, 0, 0, ratio, 0, 0);
      fitView();
    }

    canvas.addEventListener('pointerdown', (event) => {
      const point = canvasCoordinates(event);
      pointer = {
        id: event.pointerId,
        startX: point.x,
        startY: point.y,
        transformX: state.transform.x,
        transformY: state.transform.y,
        moved: false
      };
      canvas.setPointerCapture(event.pointerId);
    });
    canvas.addEventListener('pointermove', (event) => {
      const point = canvasCoordinates(event);
      if (pointer && pointer.id === event.pointerId) {
        const dx = point.x - pointer.startX;
        const dy = point.y - pointer.startY;
        if (Math.hypot(dx, dy) > 4) pointer.moved = true;
        state.transform.x = pointer.transformX + dx;
        state.transform.y = pointer.transformY + dy;
        draw();
        return;
      }
      const hovered = hitNode(point.x, point.y)?.source_node_id || null;
      if (hovered !== state.hoverId) {
        state.hoverId = hovered;
        canvas.style.cursor = hovered ? 'pointer' : 'grab';
        draw();
      }
    });
    canvas.addEventListener('pointerup', (event) => {
      if (!pointer || pointer.id !== event.pointerId) return;
      const point = canvasCoordinates(event);
      const moved = pointer.moved;
      pointer = null;
      canvas.releasePointerCapture(event.pointerId);
      if (!moved) {
        const node = hitNode(point.x, point.y);
        if (node) selectNode(node.source_node_id, state.view === 'focus', true);
      }
    });
    canvas.addEventListener('pointercancel', () => { pointer = null; });
    canvas.addEventListener('pointerleave', () => {
      if (!pointer && state.hoverId) {
        state.hoverId = null;
        draw();
      }
    });
    canvas.addEventListener('dblclick', (event) => {
      const point = canvasCoordinates(event);
      const node = hitNode(point.x, point.y);
      if (node) selectNode(node.source_node_id, true);
    });
    canvas.addEventListener('wheel', (event) => {
      event.preventDefault();
      const point = canvasCoordinates(event);
      zoomAt(event.deltaY < 0 ? 1.16 : 0.86, point.x, point.y);
    }, { passive: false });
    canvas.addEventListener('keydown', (event) => {
      const pan = 44;
      if (event.key === '+' || event.key === '=') zoomAt(1.2);
      else if (event.key === '-' || event.key === '_') zoomAt(0.82);
      else if (event.key === 'Home') fitView();
      else if (event.key === 'Escape') resetView();
      else if (event.key === 'ArrowLeft') state.transform.x += pan;
      else if (event.key === 'ArrowRight') state.transform.x -= pan;
      else if (event.key === 'ArrowUp') state.transform.y += pan;
      else if (event.key === 'ArrowDown') state.transform.y -= pan;
      else return;
      event.preventDefault();
      draw();
    });

    search.addEventListener('change', resolveSearch);
    search.addEventListener('input', () => {
      const value = search.value.trim().toLocaleLowerCase();
      const exact = nodes.find((node) => node.label.toLocaleLowerCase() === value);
      if (exact) selectNode(exact.source_node_id, true);
    });
    search.addEventListener('keydown', (event) => {
      if (event.key === 'Enter') {
        event.preventDefault();
        resolveSearch();
      }
    });
    viewControl.addEventListener('change', () => {
      state.view = viewControl.value;
      updateView({ fit: true });
    });
    depthControl.addEventListener('change', () => {
      state.depth = Number(depthControl.value);
      updateView({ fit: true });
    });
    realmControl.addEventListener('change', () => {
      state.realm = realmControl.value;
      updateView({ fit: true });
    });
    filterControl.addEventListener('change', () => {
      state.filter = filterControl.value;
      updateView({ fit: true });
    });
    reset.addEventListener('click', resetView);
    zoomIn.addEventListener('click', () => zoomAt(1.25));
    zoomOut.addEventListener('click', () => zoomAt(0.8));
    fit.addEventListener('click', fitView);
    textView.addEventListener('toggle', () => {
      if (textView.open && textViewDirty) renderTextView();
    });
    addEventListener('popstate', () => location.reload());
    if ('ResizeObserver' in window) new ResizeObserver(resize).observe(canvas);
    else addEventListener('resize', resize);

    viewControl.value = state.view;
    depthControl.value = String(state.depth);
    realmControl.value = state.realm;
    filterControl.value = state.filter;
    search.value = selectedNode().label;
    updateView({ fit: false, url: false });
    resize();
    updateUrl();

    const ledgerBody = $('#ledgerBody');
    const ledgerSearch = $('#ledgerSearch');
    const ledgerStatus = $('#ledgerStatus');
    function renderLedger() {
      const searchValue = ledgerSearch.value.trim().toLocaleLowerCase();
      const status = ledgerStatus.value;
      const rows = reconciliation.nodes.filter((row) => {
        if (status === 'mapped' && row.status === 'unresolved') return false;
        if (!['mapped', 'all'].includes(status) && row.status !== status) return false;
        const haystack = [
          row.source_label,
          row.review_note,
          ...row.atlas_targets.flatMap((target) => [target.atlas_label, target.atlas_id])
        ].join(' ').toLocaleLowerCase();
        return !searchValue || haystack.includes(searchValue);
      });
      ledgerBody.innerHTML = rows.map((row) => `<tr><td>${esc(row.source_label)}<br><span class="pm-small">${esc(row.source_node_id)}</span></td><td><span class="pm-badge ${row.status === 'confirmed' ? 'good' : row.status === 'partial' ? 'warn' : ''}">${esc(row.status)}</span></td><td>${row.atlas_targets.length ? row.atlas_targets.map((target) => `<a href="/#view=item&id=${encodeURIComponent(target.atlas_id)}&from=home">${esc(target.atlas_label)}</a><br>`).join('') : '—'}</td><td>${esc(row.review_note)}</td></tr>`).join('') || '<tr><td colspan="4">No ledger rows match.</td></tr>';
    }
    ledgerSearch.addEventListener('input', renderLedger);
    ledgerStatus.addEventListener('change', renderLedger);
    renderLedger();
  }
})();
