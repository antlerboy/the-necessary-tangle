(() => {
  'use strict';
  const $ = (selector) => document.querySelector(selector);
  const esc = (value) => String(value ?? '').replace(/[&<>"']/g, (char) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
  const sourceWidth = 1868;
  const sourceHeight = 1125;

  fetch('/assets/comparator-castellani-links.json').then((response) => {
    if (!response.ok) throw new Error(`Link data returned ${response.status}`);
    return response.json();
  }).then(start).catch((error) => {
    $('#castBody').innerHTML = `<tr><td colspan="4">The link ledger could not load: ${esc(error.message)}</td></tr>`;
  });

  function start(data) {
    const image = $('#castellaniImage');
    const imageMap = $('#castellaniMap');
    const body = $('#castBody');
    const search = $('#castSearch');
    const status = $('#castStatus');
    const links = data.links;
    $('#castLinkCount').textContent = data.meta.link_count.toLocaleString('en-GB');
    $('#castUniqueCount').textContent = data.meta.unique_destination_count.toLocaleString('en-GB');
    $('#castMismatchCount').textContent = data.meta.label_disagreement_count.toLocaleString('en-GB');

    const areas = links.map((record) => {
      const area = document.createElement('area');
      area.shape = record.shape;
      area.href = record.href;
      area.target = '_blank';
      area.rel = 'noopener';
      area.alt = record.display_label;
      area.title = `${record.display_label} — source link not independently checked`;
      area.dataset.coords = record.coords;
      imageMap.append(area);
      return area;
    });

    function scaleAreas() {
      const width = image.getBoundingClientRect().width || sourceWidth;
      const height = image.getBoundingClientRect().height || sourceHeight;
      const scaleX = width / sourceWidth;
      const scaleY = height / sourceHeight;
      areas.forEach((area) => {
        const values = area.dataset.coords.split(',').map(Number);
        area.coords = values.map((value, index) => Math.round(value * (index % 2 ? scaleY : scaleX))).join(',');
      });
    }
    image.addEventListener('load', scaleAreas);
    addEventListener('resize', scaleAreas);
    scaleAreas();

    function render() {
      const query = search.value.trim().toLocaleLowerCase();
      const filter = status.value;
      const rows = links.filter((record) => {
        if (filter === 'mismatch' && !record.label_disagreement) return false;
        if (filter === 'aligned' && record.label_disagreement) return false;
        return !query || `${record.alt} ${record.title} ${record.href}`.toLocaleLowerCase().includes(query);
      });
      body.innerHTML = rows.map((record) => `<tr>
        <td>${esc(record.alt || '—')}<br><span class="pm-small">${esc(record.source_link_id)}</span></td>
        <td>${esc(record.title || '—')}</td>
        <td><a href="${esc(record.href)}" target="_blank" rel="noopener">${esc(record.href)}</a></td>
        <td><span class="pm-badge ${record.label_disagreement ? 'warn' : ''}">${record.label_disagreement ? 'labels disagree' : 'source link — unchecked'}</span></td>
      </tr>`).join('') || '<tr><td colspan="4">No source links match.</td></tr>';
    }
    search.addEventListener('input', render);
    status.addEventListener('change', render);
    render();
  }
})();
