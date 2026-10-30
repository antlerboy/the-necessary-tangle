(() => {
  'use strict';
  const $ = id => document.getElementById(id);
  const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const norm = value => String(value).normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  const params = new URLSearchParams(location.search);
  let records = [], matching = [], page = 0;
  const size = 25;
  function card(row) {
    return '<article class="wiki-card" id="wiki-page-' + row.page_id + '"><h3><a href="' + esc(row.url) + '">' + esc(row.title) + '</a></h3><p class="meta">' + esc(row.kind) + (row.work_date_as_listed ? ' · Source-listed date: ' + esc(row.work_date_as_listed) : '') + '</p>' +
      (row.work_credit_as_listed ? '<p class="meta">Work credit as listed: ' + esc(row.work_credit_as_listed) + '</p>' : '') +
      (row.wiki_excerpt ? '<blockquote><p>' + esc(row.wiki_excerpt) + '</p><footer>Wiki excerpt · ISSS Wiki contributors · CC BY 4.0</footer></blockquote>' : '') +
      (row.placeholder ? '<p><strong>Unfinished profile:</strong> do not use this template as biographical evidence.</p>' : '') +
      (row.kind === 'Redirect' ? '<p>Source redirect to ' + esc(row.redirect_target) + '. ' + esc(row.redirect_resolution) + '. ' + (row.redirect_resolution === 'Resolved within inventory' ? '<a href="' + esc(row.canonical_url) + '">Canonical wiki page</a>' : 'Retained as an unresolved or out-of-scope source route.') + '</p>' : '') +
      '<p class="meta">' + esc(row.review) + '. Source modified: ' + esc(row.modified) + '.</p><p class="source-links"><a href="' + esc(row.revision_url) + '">Revision ' + row.revision_id + '</a> · <a href="' + esc(row.history_url) + '">Contributors and history</a> · <a href="?page=' + row.page_id + '#wiki-index">Link to this record</a></p></article>';
  }
  function render() {
    const total = Math.max(1, Math.ceil(matching.length / size));
    page = Math.min(page, total - 1);
    $('wiki-results').innerHTML = matching.slice(page * size, (page + 1) * size).map(card).join('');
    $('wiki-count').textContent = matching.length + ' of ' + records.length + ' pages match. ' + (matching.length ? 'Showing ' + (page * size + 1) + '–' + Math.min((page + 1) * size, matching.length) + '.' : 'Try fewer words or a different handling state.');
    $('wiki-page-number').textContent = 'Page ' + (page + 1) + ' of ' + total;
    $('wiki-previous').disabled = page === 0;
    $('wiki-next').disabled = page >= total - 1;
  }
  function filter() {
    const words = norm($('wiki-query').value).trim().split(/\s+/).filter(Boolean);
    const kind = $('wiki-kind').value, state = $('wiki-state').value;
    matching = records.filter(row => (!kind || row.kind === kind) && words.every(word => row.search.includes(word)) &&
      (state === 'all' || state === 'usable' && !row.placeholder && row.kind !== 'Redirect' || state === 'unfinished' && row.placeholder || state === 'redirect' && row.kind === 'Redirect' || state === 'read' && row.review.startsWith('Wiki page read in full')));
    page = 0;
    render();
  }
  $('wiki-search').addEventListener('submit', event => { event.preventDefault(); filter(); });
  $('wiki-search').addEventListener('reset', event => { event.preventDefault(); $('wiki-query').value = ''; $('wiki-kind').value = ''; $('wiki-state').value = 'usable'; filter(); $('wiki-query').focus(); });
  $('wiki-query').addEventListener('input', filter);
  ['wiki-kind', 'wiki-state'].forEach(id => $(id).addEventListener('change', filter));
  $('wiki-previous').addEventListener('click', () => { page--; render(); $('wiki-count').scrollIntoView({block:'start'}); });
  $('wiki-next').addEventListener('click', () => { page++; render(); $('wiki-count').scrollIntoView({block:'start'}); });
  fetch('inventory.json').then(response => { if (!response.ok) throw Error('Index unavailable'); return response.json(); }).then(packet => {
    records = packet.records.map(row => ({...row, search:norm([row.title, row.work_credit_as_listed, row.wiki_excerpt, ...row.categories].join(' '))}));
    [...new Set(records.map(row => row.kind))].sort().forEach(kind => $('wiki-kind').add(new Option(kind, kind)));
    $('wiki-query').value = params.get('q') || '';
    if (params.has('page')) {
      $('wiki-state').value = 'all';
      matching = records.filter(row => String(row.page_id) === params.get('page'));
      render();
    } else filter();
  }).catch(() => { $('wiki-error').hidden = false; $('wiki-count').textContent = 'Index unavailable'; });
})();
