(() => {
  'use strict';
  const $ = (selector) => document.querySelector(selector);
  const esc = (value) => String(value ?? '').replace(/[&<>"']/g, (char) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
  const number = (value) => Number(value || 0).toLocaleString('en-GB');

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
  });

  function start(map, reconciliation) {
    const canvas = $('#systemicCanvas');
    const context = canvas.getContext('2d');
    const panel = $('#systemicPanel');
    const search = $('#systemicSearch');
    const filter = $('#systemicFilter');
    const reset = $('#systemicReset');
    const nodes = map.nodes;
    const edges = map.edges;
    const byId = new Map(nodes.map((node) => [node.source_node_id, node]));
    const adjacent = new Map(nodes.map((node) => [node.source_node_id, []]));
    edges.forEach((edge) => {
      adjacent.get(edge.source_node_id)?.push(edge);
      adjacent.get(edge.target_node_id)?.push(edge);
    });

    const summary = reconciliation.meta.summary;
    $('#statNodes').textContent = number(summary.source_nodes_retained);
    $('#statLinks').textContent = number(summary.source_links_retained);
    $('#statMapped').textContent = number(summary.source_nodes_confirmed + summary.source_nodes_partially_reconciled);
    $('#statAtlas').textContent = number(summary.distinct_atlas_entries_linked);

    let width = 0;
    let height = 0;
    let selected = null;
    let positions = new Map();

    function visible(edge) {
      return filter.value === 'all' || edge.reconciliation_status === filter.value;
    }

    function resize() {
      const box = canvas.getBoundingClientRect();
      const ratio = Math.min(window.devicePixelRatio || 1, 2);
      width = Math.max(320, box.width);
      height = Math.max(420, box.height);
      canvas.width = Math.round(width * ratio);
      canvas.height = Math.round(height * ratio);
      context.setTransform(ratio, 0, 0, ratio, 0, 0);

      const xs = nodes.map((node) => Number(node.x || 0) + Number(node.width || 0) / 2);
      const ys = nodes.map((node) => Number(node.y || 0) + Number(node.height || 0) / 2);
      const minX = Math.min(...xs), maxX = Math.max(...xs);
      const minY = Math.min(...ys), maxY = Math.max(...ys);
      const pad = 24;
      const scale = Math.min((width - pad * 2) / Math.max(1, maxX - minX), (height - pad * 2) / Math.max(1, maxY - minY));
      positions = new Map(nodes.map((node, index) => [node.source_node_id, {
        x: pad + (xs[index] - minX) * scale,
        y: pad + (ys[index] - minY) * scale
      }]));
      draw();
    }

    function colour(value) {
      if (!/^#[0-9a-f]{6}$/i.test(value || '')) return '#777777';
      return value;
    }

    function arrow(a, b, colourValue) {
      const angle = Math.atan2(b.y - a.y, b.x - a.x);
      const size = 5;
      context.fillStyle = colourValue;
      context.beginPath();
      context.moveTo(b.x, b.y);
      context.lineTo(b.x - Math.cos(angle - .55) * size, b.y - Math.sin(angle - .55) * size);
      context.lineTo(b.x - Math.cos(angle + .55) * size, b.y - Math.sin(angle + .55) * size);
      context.closePath();
      context.fill();
    }

    function draw() {
      context.clearRect(0, 0, width, height);
      const selectedId = selected?.source_node_id;
      edges.forEach((edge) => {
        if (!visible(edge)) return;
        const a = positions.get(edge.source_node_id);
        const b = positions.get(edge.target_node_id);
        if (!a || !b) return;
        const on = selectedId && (edge.source_node_id === selectedId || edge.target_node_id === selectedId);
        context.globalAlpha = selectedId ? (on ? .85 : .025) : .17;
        const stroke = colour(edge.line_colour);
        context.strokeStyle = stroke;
        context.lineWidth = on ? 1.8 : Math.max(.35, Math.min(1.15, Number(edge.line_width || 1) / 3));
        context.setLineDash(edge.line_style === 'dashed' ? [3, 3] : []);
        context.beginPath();context.moveTo(a.x, a.y);context.lineTo(b.x, b.y);context.stroke();
        if (on) {
          if (edge.direction_status === 'bidirectional' || edge.direction_status === 'target_to_source') arrow(b, a, stroke);
          if (edge.direction_status !== 'target_to_source') arrow(a, b, stroke);
        }
      });
      context.setLineDash([]);
      context.globalAlpha = 1;
      nodes.forEach((node) => {
        const point = positions.get(node.source_node_id);
        const isSelected = selectedId === node.source_node_id;
        const mapped = node.reconciliation_status !== 'unresolved';
        const radius = isSelected ? 6 : mapped ? 3.5 : 1.65;
        context.beginPath();context.arc(point.x, point.y, radius, 0, Math.PI * 2);
        context.fillStyle = isSelected ? '#111111' : mapped ? '#9f161b' : '#f7f1e4';
        context.fill();
        context.strokeStyle = mapped ? '#9f161b' : '#777777';
        context.lineWidth = isSelected ? 2 : .7;
        context.stroke();
      });
      if (selected) {
        const point = positions.get(selected.source_node_id);
        context.font = '600 13px Arial, sans-serif';
        context.textAlign = 'center';
        context.lineWidth = 4;context.strokeStyle = '#f7f1e4';context.strokeText(selected.label, point.x, point.y - 10);
        context.fillStyle = '#111111';context.fillText(selected.label, point.x, point.y - 10);
      }
    }

    function edgeText(edge, node) {
      const otherId = edge.source_node_id === node.source_node_id ? edge.target_node_id : edge.source_node_id;
      const other = byId.get(otherId);
      if (edge.direction_status === 'bidirectional') return `↔ ${other.label}`;
      if (edge.direction_status === 'target_to_source') {
        return edge.source_node_id === node.source_node_id ? `← ${other.label}` : `→ ${other.label}`;
      }
      return edge.source_node_id === node.source_node_id ? `→ ${other.label}` : `← ${other.label}`;
    }

    function selectNode(node) {
      selected = node;
      draw();
      const links = (adjacent.get(node.source_node_id) || []).filter(visible).sort((a, b) => edgeText(a, node).localeCompare(edgeText(b, node)));
      const targets = node.atlas_targets || [];
      panel.innerHTML = `<h2>${esc(node.label)}</h2>
        <p class="pm-small">${esc(node.official_realm)} · source node ${esc(node.source_node_id)}</p>
        <p><span class="pm-badge ${node.reconciliation_status === 'confirmed' ? 'good' : node.reconciliation_status === 'partial' ? 'warn' : ''}">${esc(node.reconciliation_status)}</span></p>
        ${targets.length ? `<h3>Tangle reconciliation</h3><ul>${targets.map((target) => `<li><a href="/#view=item&id=${encodeURIComponent(target.atlas_id)}&from=home">${esc(target.atlas_label || target.atlas_id)}</a> <span class="pm-small">${esc(target.match_kind)}</span></li>`).join('')}</ul>` : '<p>No human-reviewed Tangle mapping is recorded yet.</p>'}
        <h3>Source-reported links (${number(links.length)})</h3>
        <p class="pm-small">Arrows follow the source. They report major influence and remain unverified here.</p>
        <ul>${links.map((edge) => `<li><button type="button" class="text-button" data-node="${esc(edge.source_node_id === node.source_node_id ? edge.target_node_id : edge.source_node_id)}">${esc(edgeText(edge, node))}</button> <span class="pm-small">${esc(edge.official_realm)}</span></li>`).join('')}</ul>`;
      panel.querySelectorAll('[data-node]').forEach((button) => button.addEventListener('click', () => selectNode(byId.get(button.dataset.node))));
    }

    canvas.addEventListener('click', (event) => {
      const box = canvas.getBoundingClientRect();
      const x = event.clientX - box.left, y = event.clientY - box.top;
      let best = null, distance = 11;
      nodes.forEach((node) => {
        const point = positions.get(node.source_node_id);
        const current = Math.hypot(point.x - x, point.y - y);
        if (current < distance) { best = node; distance = current; }
      });
      if (best) selectNode(best);
    });
    filter.addEventListener('change', () => { draw(); if (selected) selectNode(selected); });
    reset.addEventListener('click', () => { selected = null; search.value = ''; panel.innerHTML = '<h2>Reading the map</h2><p>Select a node to see its source-reported links and any conservative Tangle reconciliation.</p>'; draw(); });
    search.addEventListener('input', () => {
      const query = search.value.trim().toLocaleLowerCase();
      if (query.length < 2) return;
      const match = nodes.find((node) => node.label.toLocaleLowerCase().includes(query));
      if (match) selectNode(match);
    });
    addEventListener('resize', resize);
    resize();

    const ledgerBody = $('#ledgerBody');
    const ledgerSearch = $('#ledgerSearch');
    const ledgerStatus = $('#ledgerStatus');
    function renderLedger() {
      const query = ledgerSearch.value.trim().toLocaleLowerCase();
      const status = ledgerStatus.value;
      const rows = reconciliation.nodes.filter((row) => {
        if (status === 'mapped' && row.status === 'unresolved') return false;
        if (!['mapped', 'all'].includes(status) && row.status !== status) return false;
        const haystack = [row.source_label, row.review_note, ...row.atlas_targets.flatMap((target) => [target.atlas_label, target.atlas_id])].join(' ').toLocaleLowerCase();
        return !query || haystack.includes(query);
      });
      ledgerBody.innerHTML = rows.map((row) => `<tr><td>${esc(row.source_label)}<br><span class="pm-small">${esc(row.source_node_id)}</span></td><td><span class="pm-badge ${row.status === 'confirmed' ? 'good' : row.status === 'partial' ? 'warn' : ''}">${esc(row.status)}</span></td><td>${row.atlas_targets.length ? row.atlas_targets.map((target) => `<a href="/#view=item&id=${encodeURIComponent(target.atlas_id)}&from=home">${esc(target.atlas_label)}</a><br>`).join('') : '—'}</td><td>${esc(row.review_note)}</td></tr>`).join('') || '<tr><td colspan="4">No ledger rows match.</td></tr>';
    }
    ledgerSearch.addEventListener('input', renderLedger);
    ledgerStatus.addEventListener('change', renderLedger);
    renderLedger();
  }
})();
