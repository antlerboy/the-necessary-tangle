(() => {
  'use strict';
  const $ = (selector) => document.querySelector(selector);
  const esc = (value) => String(value ?? '').replace(/[&<>"']/g, (char) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
  const number = (value) => Number(value || 0).toLocaleString('en-GB');

  fetch('/assets/counted-map-public.json').then((response) => {
    if (!response.ok) throw new Error(`Counted-map data returned ${response.status}`);
    return response.json();
  }).then(start).catch((error) => {
    $('#countedPanel').innerHTML = `<h2>Map unavailable</h2><p>${esc(error.message)}</p>`;
  });

  function start(data) {
    const canvas = $('#countedCanvas');
    const context = canvas.getContext('2d');
    const panel = $('#countedPanel');
    const search = $('#countedSearch');
    const weight = $('#countedWeight');
    const status = $('#countedStatus');
    const reset = $('#countedReset');
    const nodes = data.concepts;
    const edges = data.edges;
    const byId = new Map(nodes.map((node) => [node.id, node]));
    const adjacent = new Map(nodes.map((node) => [node.id, []]));
    edges.forEach((edge) => { adjacent.get(edge.source)?.push(edge); adjacent.get(edge.target)?.push(edge); });
    const maxWorks = Math.max(...nodes.map((node) => node.work_count));
    let width = 0, height = 0, selected = null, positions = new Map();

    function visible(edge) {
      if (edge.weight < Math.max(5, Number(weight.value || 5))) return false;
      if (status.value === 'concentrated' && !edge.concentrated) return false;
      if (status.value === 'stable' && edge.concentrated) return false;
      return true;
    }

    function resize() {
      const box = canvas.getBoundingClientRect();
      const ratio = Math.min(window.devicePixelRatio || 1, 2);
      width = Math.max(320, box.width);height = Math.max(420, box.height);
      canvas.width = Math.round(width * ratio);canvas.height = Math.round(height * ratio);
      context.setTransform(ratio, 0, 0, ratio, 0, 0);
      const ordered = [...nodes].sort((a, b) => b.work_count - a.work_count || a.label.localeCompare(b.label));
      const golden = Math.PI * (3 - Math.sqrt(5));
      positions = new Map(ordered.map((node, index) => {
        const fraction = (index + 1) / (ordered.length + 1);
        const radius = Math.sqrt(fraction) * Math.min(width, height) * .41;
        const angle = index * golden;
        return [node.id, {x: width / 2 + Math.cos(angle) * radius, y: height / 2 + Math.sin(angle) * radius}];
      }));
      draw();
    }

    function nodeRadius(node) {
      return 3.5 + 15 * Math.sqrt(node.work_count / maxWorks);
    }

    function draw() {
      context.clearRect(0, 0, width, height);
      const selectedId = selected?.id;
      edges.forEach((edge) => {
        if (!visible(edge)) return;
        const a = positions.get(edge.source), b = positions.get(edge.target);
        const on = selectedId && (edge.source === selectedId || edge.target === selectedId);
        context.globalAlpha = selectedId ? (on ? .8 : .015) : .075;
        context.strokeStyle = edge.concentrated ? '#ad6b00' : '#777777';
        context.lineWidth = on ? Math.min(4, .8 + Math.log10(edge.weight)) : Math.min(1.3, .25 + Math.log10(edge.weight) / 3);
        context.beginPath();context.moveTo(a.x, a.y);context.lineTo(b.x, b.y);context.stroke();
      });
      context.globalAlpha = 1;
      nodes.forEach((node) => {
        const point = positions.get(node.id);const radius = nodeRadius(node);
        context.beginPath();context.arc(point.x, point.y, radius, 0, Math.PI * 2);
        context.fillStyle = node.id === selectedId ? '#9f161b' : '#f7f1e4';context.fill();
        context.strokeStyle = node.status === 'evidenced' ? '#555555' : '#ad6b00';context.lineWidth = node.id === selectedId ? 2.5 : 1;context.stroke();
      });
      if (selected) {
        const point = positions.get(selected.id);context.font = '600 13px Arial, sans-serif';context.textAlign = 'center';
        context.lineWidth = 4;context.strokeStyle = '#f7f1e4';context.strokeText(selected.label, point.x, point.y - nodeRadius(selected) - 6);
        context.fillStyle = '#111111';context.fillText(selected.label, point.x, point.y - nodeRadius(selected) - 6);
      }
    }

    function selectNode(node) {
      selected = node;draw();
      const links = (adjacent.get(node.id) || []).filter(visible).sort((a, b) => b.weight - a.weight);
      const exemplars = node.exemplar_works || [];
      panel.innerHTML = `<h2>${esc(node.label)}</h2><p class="pm-small">${number(node.work_count)} title matches · ${esc(node.first_year || '?')}–${esc(node.last_year || '?')} · ${esc(node.status)}</p>
        ${exemplars.length ? `<h3>Exemplar DOI handles</h3><ul>${exemplars.map((work) => `<li><a href="https://doi.org/${esc(encodeURI(work.doi))}" target="_blank" rel="noopener">${esc(work.title || work.doi)}</a> <span class="pm-small">${esc(work.year)}</span></li>`).join('')}</ul>` : ''}
        <h3>Visible aggregate links (${number(links.length)})</h3><p class="pm-small">A direction runs from a source-title match to a target cited-reference keyword match.</p>
        <ul>${links.map((edge) => { const outgoing = edge.source === node.id; const other = byId.get(outgoing ? edge.target : edge.source); return `<li><button class="text-button" type="button" data-node="${esc(other.id)}">${outgoing ? '→' : '←'} ${esc(other.label)}</button> <strong>${number(edge.weight)}</strong>${edge.concentrated ? ' <span class="pm-badge warn">concentrated</span>' : ''}</li>`; }).join('')}</ul>`;
      panel.querySelectorAll('[data-node]').forEach((button) => button.addEventListener('click', () => selectNode(byId.get(button.dataset.node))));
    }

    canvas.addEventListener('click', (event) => {
      const box = canvas.getBoundingClientRect();const x = event.clientX - box.left, y = event.clientY - box.top;
      let best = null, distance = 18;
      nodes.forEach((node) => { const point = positions.get(node.id);const current = Math.hypot(point.x - x, point.y - y);if (current < nodeRadius(node) + 5 && current < distance) {best = node;distance = current;} });
      if (best) selectNode(best);
    });
    [weight, status].forEach((control) => control.addEventListener('input', () => {draw();if (selected) selectNode(selected);}));
    search.addEventListener('input', () => { const query = search.value.trim().toLocaleLowerCase();if (query.length < 2) return;const match = nodes.find((node) => node.label.toLocaleLowerCase().includes(query));if (match) selectNode(match); });
    reset.addEventListener('click', () => {selected = null;search.value = '';weight.value = 5;status.value = 'all';panel.innerHTML = '<h2>Reading the counted map</h2><p>Select a concept to inspect every aggregate link that survives the current filter.</p>';draw();});
    addEventListener('resize', resize);resize();
  }
})();
