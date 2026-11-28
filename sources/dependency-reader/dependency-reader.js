(() => {
  'use strict';
  const data = window.TANGLE_DATA || {};
  const model = window.TANGLE_DEPENDENCIES || window.TANGLE_DEPENDENCY_MODEL.create(data);
  const $ = (id) => document.getElementById(id);
  const esc = (value) => String(value ?? '').replace(/[&<>"']/g, (ch) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[ch]));
  const normal = (value) => String(value || '').normalize('NFKD').replace(/[\u0300-\u036f]/g, '').toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim();
  const label = (value) => String(value || 'not stated').replace(/_/g, ' ');
  const review = (value) => ({ candidate: 'Proposed', disputed: 'Disputed', accepted: 'Accepted record', corroborated: 'Supported by multiple sources', research_pass_needs_editor: 'Awaiting editorial review', rejected: 'Rejected', superseded: 'Superseded' })[value] || label(value);
  const entries = [...model.nodes.values()].sort((a, b) => a.label.localeCompare(b.label));
  let focus, mode = 'necessary', depth = 1, relatedLimit = 40;
  function href(id, params = {}) {
    const query = new URLSearchParams({ entry: model.canonical(id), mode, depth: String(depth), ...params });
    return '/dependencies/?' + query.toString();
  }
  function sourceLinks(edge) {
    const ids = model.unpack(edge.source_ids);
    if (!ids.length) return '<li>No source is linked to this statement.</li>';
    return ids.map((id) => {
      const source = model.sources.get(id); if (!source) return '<li>Source record unavailable</li>';
      const url = String(source.url || '');
      return '<li>' + (/^https?:\/\//.test(url) ? '<a href="' + esc(url) + '">' + esc(source.title) + '</a>' : esc(source.title) + ' · no public link') + '</li>';
    }).join('');
  }
  function claimHtml(edge) {
    const a = model.nodes.get(edge.source), b = model.nodes.get(edge.target);
    const relation = edge.plain_phrase || label(edge.relation_type);
    const statement = (a?.label || edge.source) + ' ' + relation + ' ' + (b?.label || edge.target);
    const locators = [...new Set([edge.source_locator, ...model.unpack(edge.evidence_ids).map((id) => model.evidence.get(id)?.locator)].filter(Boolean))];
    return '<article class="dependency-claim" data-edge-id="' + esc(edge.id) + '"><p><strong>' + esc(statement) + '</strong></p><p class="dependency-review" data-state="' + esc(edge.claim_status) + '">' + esc(review(edge.claim_status)) + ' · ' + esc(label(edge.relation_type)) + '</p>'
      + (edge.scope_conditions ? '<p>' + esc(edge.scope_conditions) + '</p>' : '')
      + (locators.length ? '<p>Source passage: ' + esc(locators.join('; ')) + '</p>' : '<p>No passage locator is recorded.</p>')
      + '<ul>' + sourceLinks(edge) + '</ul></article>';
  }
  function cardHtml(group, side) {
    const node = group.node;
    const paths = group.paths || [group.edges];
    const claims = [...new Map(paths.flat().map((edge) => [edge.id, edge])).values()];
    const definition = model.profiles.get(node.id)?.canonical_definition || node.canonical_definition || node.description || '';
    return '<article class="dependency-card" data-node-id="' + esc(node.id) + '"><p class="dependency-card-meta">' + esc(label(node.entity_type)) + (group.distance ? ' · ' + group.distance + (group.distance === 1 ? ' step' : ' steps') : '') + '</p><h3><a class="focus-link" href="' + esc(href(node.id)) + '">' + esc(node.label) + '</a></h3><p>' + esc(definition) + '</p><details><summary>Why this connection? (' + claims.length + ' ' + (claims.length === 1 ? 'claim' : 'claims') + ')</summary>'
      + (group.distance > 1 ? '<p>These statements form a recorded chain. Each retains its own scope and review status.</p>' : '')
      + claims.map(claimHtml).join('') + '</details><p><a href="/#view=item&amp;id=' + encodeURIComponent(node.id) + '&amp;from=home">Open full entry</a></p></article>';
  }
  function emptyHtml(side) {
    return '<div class="dependency-empty"><p>No prerequisite claim is recorded in this direction for this entry.</p><a class="focus-link" href="' + esc(href(focus.id, { mode: 'connections', depth: '1' })) + '">Explore its other recorded relationships</a></div>';
  }
  function renderRelated() {
    const query = normal($('dependency-filter').value);
    const groups = model.related(focus.id).filter((group) => !query || normal(group.node.label + ' ' + group.node.description).includes(query));
    $('related-cards').innerHTML = groups.slice(0, relatedLimit).map((group) => cardHtml(group)).join('') || '<p class="dependency-empty">No matching recorded relationship.</p>';
    $('dependency-more').hidden = groups.length <= relatedLimit;
    $('dependency-more').textContent = 'Show more connections (' + Math.min(relatedLimit, groups.length) + ' of ' + groups.length + ' shown)';
  }
  function render() {
    const params = new URLSearchParams(location.search);
    const requested = params.get('entry') || 'concept_feedback';
    const id = model.canonical(requested);
    focus = model.nodes.get(id);
    if (!focus) {
      $('dependency-status').textContent = 'That entry is not in the public atlas. Choose an entry above.';
      $('dependency-columns').hidden = true; $('dependency-related').hidden = true;
      $('dependency-mode').disabled = true; $('dependency-depth').disabled = true; $('dependency-copy').disabled = true; return;
    }
    mode = params.get('mode') === 'connections' ? 'connections' : 'necessary';
    depth = mode === 'connections' ? 1 : Math.max(1, Math.min(3, Math.floor(Number(params.get('depth'))) || 1));
    if (id !== requested) history.replaceState(null, '', href(id, ['predecessors', 'dependents'].includes(params.get('side')) ? { side: params.get('side') } : {}));
    $('dependency-mode').disabled = false; $('dependency-copy').disabled = false;
    $('dependency-mode').value = mode; $('dependency-depth').value = String(depth); $('dependency-depth').disabled = mode === 'connections';
    $('dependency-query').value = focus.label;
    $('dependency-search-results').innerHTML = '';
    $('dependency-filter').value = '';
    $('dependency-columns').hidden = false;
    $('dependency-predecessors').hidden = mode !== 'necessary'; $('dependency-dependents').hidden = mode !== 'necessary';
    $('dependency-columns').classList.toggle('connections-mode', mode === 'connections');
    $('dependency-related').hidden = mode !== 'connections';
    const profile = model.profiles.get(id);
    const definition = profile?.canonical_definition || focus.canonical_definition || focus.description || '';
    const developed = !!profile;
    $('dependency-focus').innerHTML = '<p class="dependency-type">Focused entry · ' + esc(label(focus.entity_type)) + '</p><h2 id="dependency-focus-title" tabindex="-1">' + esc(focus.label) + '</h2><p>' + esc(definition) + '</p><p class="dependency-review">' + esc(review(profile?.review_status || focus.review_status)) + '</p><div class="dependency-actions"><a href="/#view=item&amp;id=' + encodeURIComponent(id) + '&amp;from=home">Open full entry</a>' + (developed ? '<a href="/entries/' + encodeURIComponent(id) + '/">Read sources and account</a>' : '') + '<a class="focus-link" href="' + esc(href(id, { mode: mode === 'necessary' ? 'connections' : 'necessary', depth: '1' })) + '">' + (mode === 'necessary' ? 'Other recorded relationships' : 'Prerequisite view') + '</a></div>';
    $('dependency-focus').setAttribute('aria-labelledby', 'dependency-focus-title');
    const before = model.trace(id, 'predecessors', depth), after = model.trace(id, 'dependents', depth);
    $('predecessor-title').textContent = 'Necessary predecessors (' + before.entries.length + ')';
    $('dependent-title').textContent = 'Dependent entries (' + after.entries.length + ')';
    $('predecessor-cards').innerHTML = before.entries.map((group) => cardHtml(group, 'predecessors')).join('') || emptyHtml('predecessors');
    $('dependent-cards').innerHTML = after.entries.map((group) => cardHtml(group, 'dependents')).join('') || emptyHtml('dependents');
    const both = before.entries.some((group) => after.entries.some((other) => other.node.id === group.node.id));
    const cyclic = both || before.cycles.length || after.cycles.length;
    $('dependency-cycle').hidden = mode !== 'necessary' || !cyclic;
    $('dependency-cycle').textContent = 'The visible prerequisite claims contain a circular or mutual relationship. Inspect the individual statements and their scopes; this view does not turn the graph into a single hierarchy.';
    $('dependency-status').textContent = mode === 'necessary' ? before.entries.length + (before.entries.length === 1 ? ' predecessor entry and ' : ' predecessor entries and ') + after.entries.length + (after.entries.length === 1 ? ' dependent entry within ' : ' dependent entries within ') + depth + (depth === 1 ? ' step.' : ' steps.') : model.related(id).length + ' connected entries. Relation kinds and recorded directions remain explicit.';
    if (mode === 'connections') { relatedLimit = 40; renderRelated(); }
    document.title = focus.label + ' – predecessors and dependents | The Necessary Tangle';
    const canonical = document.querySelector('link[rel="canonical"]'); if (canonical) canonical.href = location.origin + href(id);
    const side = params.get('side');
    if (side === 'predecessors' || side === 'dependents') requestAnimationFrame(() => $('dependency-' + side).scrollIntoView({ block: 'start' }));
  }
  function navigate(url) {
    history.pushState(null, '', url); render();
    if (focus) { $('dependency-focus-title').focus({ preventScroll: true }); $('dependency-focus').scrollIntoView({ block: 'nearest' }); }
  }
  document.addEventListener('click', (event) => {
    const link = event.target.closest('a.focus-link');
    if (!link || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    event.preventDefault(); navigate(link.href);
  });
  $('dependency-mode').addEventListener('change', () => { if (focus) navigate(href(focus.id, { mode: $('dependency-mode').value, depth: '1' })); });
  $('dependency-depth').addEventListener('change', () => { if (focus) navigate(href(focus.id, { depth: $('dependency-depth').value })); });
  $('dependency-filter').addEventListener('input', () => { relatedLimit = 40; renderRelated(); });
  $('dependency-more').addEventListener('click', () => { relatedLimit += 40; renderRelated(); });
  $('dependency-copy').addEventListener('click', async () => {
    const side = new URLSearchParams(location.search).get('side');
    const safeUrl = location.origin + href(focus.id, ['predecessors', 'dependents'].includes(side) ? { side } : {});
    try { await navigator.clipboard.writeText(safeUrl); $('dependency-copy').textContent = 'View link copied'; }
    catch (_) { $('dependency-status').textContent = 'Copy the view URL from the address bar.'; }
  });
  $('dependency-search').addEventListener('submit', (event) => {
    event.preventDefault(); const query = normal($('dependency-query').value);
    const ranked = entries.map((node) => ({ node, names: [node.label, ...model.unpack(node.aliases)].map(normal) }))
      .map((row) => ({ node: row.node, score: Math.max(0, ...row.names.map((name) => name === query ? 100 : name.startsWith(query) ? 30 : name.includes(query) ? 10 : 0)) }))
      .filter((row) => row.score > 0 && query).sort((a, b) => b.score - a.score || a.node.label.localeCompare(b.node.label));
    if (ranked.length && (ranked.length === 1 || ranked[0].score > ranked[1].score)) navigate(href(ranked[0].node.id));
    else $('dependency-search-results').innerHTML = ranked.length ? '<p>Choose an entry:</p><ul>' + ranked.slice(0, 12).map((row) => '<li><a class="focus-link" href="' + esc(href(row.node.id)) + '">' + esc(row.node.label) + '</a></li>').join('') + '</ul>' : '<p>No public entry matched that search.</p>';
  });
  $('dependency-options').innerHTML = entries.map((node) => '<option value="' + esc(node.label) + '"></option>').join('');
  window.addEventListener('popstate', render); render();
})();
