(() => {
  'use strict';

  const DATA = window.TANGLE_DATA || {};
  const CONFIG = window.TANGLE_CONFIG || {};
  const $ = (id) => document.getElementById(id);
  const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];
  const esc = (value) => String(value ?? '').replace(/[&<>'"]/g, (ch) => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;'
  }[ch]));
  const titleCase = (value) => String(value || '')
    .replace(/_/g, ' ')
    .replace(/\b\w/g, (c) => c.toUpperCase());
  const parse = (value, fallback = []) => {
    if (Array.isArray(value) || (value && typeof value === 'object')) return value;
    if (!value) return fallback;
    try { return JSON.parse(value); } catch (_) { return fallback; }
  };
  const normalise = (value) => String(value || '')
    .normalize('NFKD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .replace(/&/g, ' and ')
    .replace(/[^a-z0-9]+/g, ' ')
    .trim();
  const unique = (items) => [...new Set(items.filter(Boolean))];

  const RELATION_FAMILY_LABELS = {
    conceptual: 'Ideas and dependencies',
    historical: 'History and sequence',
    influence: 'Influence and lineage',
    practice: 'Practice and application',
    contestation: 'Confusion and disagreement',
    human: 'Human transmission',
    identity: 'Identity and affiliation',
    documentary: 'Works, authorship and presentation',
    classification: 'Collection structure',
    evidence: 'Evidence registration'
  };
  const QUESTION_STOPWORDS = new Set([
    'a', 'about', 'an', 'and', 'are', 'as', 'at', 'be', 'been', 'between', 'by',
    'can', 'could', 'did', 'do', 'does', 'for', 'from', 'had', 'has', 'have',
    'how', 'i', 'if', 'in', 'into', 'is', 'it', 'its', 'me', 'my', 'not', 'of',
    'on', 'or', 'our', 'relate', 'related', 'relationship', 'should', 'that',
    'the', 'their', 'them', 'there', 'these', 'they', 'this', 'to', 'use', 'used',
    'was', 'we', 'were', 'what', 'when', 'where', 'which', 'who', 'why', 'with',
    'would', 'you', 'your'
  ]);

  const redirects = DATA.canonical_redirects || {};
  const canonicalId = (id) => redirects[id] || id;
  const allNodes = DATA.nodes || [];
  const nodeById = new Map(allNodes.map((node) => [node.id, node]));
  const publicNodes = allNodes.filter((node) =>
    node.public_visibility === 'public' && canonicalId(node.id) === node.id
  );
  const profileById = new Map((DATA.profiles || []).map((profile) => [profile.node_id, profile]));
  const sourceById = new Map((DATA.sources || []).map((source) => [source.id, source]));
  const evidenceById = new Map((DATA.evidence || []).map((evidence) => [evidence.id, evidence]));
  const relationByType = new Map((DATA.relation_types || []).map((relation) => [relation.relation_type, relation]));
  const relationalDepthByNode = DATA.relational_depth?.by_node || {};

  const canonicalEdges = [];
  const edgeSeen = new Set();
  for (const raw of (DATA.edges || [])) {
    const source = canonicalId(raw.source);
    const target = canonicalId(raw.target);
    if (!nodeById.has(source) || !nodeById.has(target) || source === target) continue;
    const key = `${source}|${raw.relation_type}|${target}|${raw.id}`;
    if (edgeSeen.has(key)) continue;
    edgeSeen.add(key);
    canonicalEdges.push({ ...raw, source, target });
  }

  const edgesByNode = new Map();
  for (const edge of canonicalEdges) {
    if (!edgesByNode.has(edge.source)) edgesByNode.set(edge.source, []);
    if (!edgesByNode.has(edge.target)) edgesByNode.set(edge.target, []);
    edgesByNode.get(edge.source).push(edge);
    edgesByNode.get(edge.target).push(edge);
  }

  const aliasSets = new Map(publicNodes.map((node) => [
    node.id,
    new Set([node.label, ...parse(node.aliases, [])])
  ]));
  for (const node of allNodes) {
    const target = canonicalId(node.id);
    if (target !== node.id && aliasSets.has(target)) {
      aliasSets.get(target).add(node.label);
      parse(node.aliases, []).forEach((alias) => aliasSets.get(target).add(alias));
    }
  }

  const searchRecords = publicNodes.map((node) => {
    const profile = profileById.get(node.id);
    const aliases = [...(aliasSets.get(node.id) || [])];
    const tags = parse(node.set_tags, []);
    const text = [
      node.label,
      ...aliases,
      node.description,
      node.canonical_definition,
      profile?.summary,
      profile?.canonical_definition,
      profile?.why_it_matters,
      ...tags
    ].filter(Boolean).join(' ');
    return {
      node,
      aliases,
      normLabel: normalise(node.label),
      normAliases: aliases.map(normalise),
      normText: normalise(text)
    };
  });

  const linkTerms = [];
  for (const record of searchRecords) {
    const candidates = unique([record.node.label, ...record.aliases])
      .filter((term) => normalise(term).length >= 4)
      .filter((term) => !QUESTION_STOPWORDS.has(normalise(term)));
    for (const term of candidates) {
      linkTerms.push({ term, lower: term.toLowerCase(), node: record.node });
    }
  }
  linkTerms.sort((a, b) => b.term.length - a.term.length || a.term.localeCompare(b.term));

  function editDistance(a, b) {
    if (a === b) return 0;
    if (!a.length) return b.length;
    if (!b.length) return a.length;
    const previous = Array.from({ length: b.length + 1 }, (_, i) => i);
    const current = new Array(b.length + 1);
    for (let i = 1; i <= a.length; i += 1) {
      current[0] = i;
      for (let j = 1; j <= b.length; j += 1) {
        const cost = a[i - 1] === b[j - 1] ? 0 : 1;
        current[j] = Math.min(current[j - 1] + 1, previous[j] + 1, previous[j - 1] + cost);
      }
      for (let j = 0; j <= b.length; j += 1) previous[j] = current[j];
    }
    return previous[b.length];
  }

  function trigrams(text) {
    const padded = `  ${text} `;
    const out = new Set();
    for (let i = 0; i < padded.length - 2; i += 1) out.add(padded.slice(i, i + 3));
    return out;
  }

  function trigramSimilarity(a, b) {
    if (!a || !b) return 0;
    const A = trigrams(a);
    const B = trigrams(b);
    let shared = 0;
    A.forEach((value) => { if (B.has(value)) shared += 1; });
    return (2 * shared) / (A.size + B.size || 1);
  }

  function searchScore(query, record) {
    const q = normalise(query);
    if (!q) return 0;
    const label = record.normLabel;
    const aliases = record.normAliases;
    if (label === q) return 1000;
    if (aliases.includes(q)) return 980;
    if (label.startsWith(q)) return 880 - Math.min(100, label.length - q.length);
    if (aliases.some((alias) => alias.startsWith(q))) return 850;
    const qTokens = q.split(' ').filter(Boolean);
    const labelTokens = label.split(' ');
    const tokenCoverage = qTokens.filter((token) =>
      labelTokens.some((labelToken) => labelToken.startsWith(token))
    ).length / Math.max(qTokens.length, 1);
    let score = tokenCoverage * 680;
    if (label.includes(q)) score = Math.max(score, 720 - Math.min(160, label.indexOf(q) * 3));
    if (record.normText.includes(q)) score = Math.max(score, 470);
    const trigram = Math.max(
      trigramSimilarity(q, label),
      ...aliases.map((alias) => trigramSimilarity(q, alias)),
      0
    );
    score = Math.max(score, trigram * 610);
    if (Math.max(q.length, label.length) <= 28) {
      const distance = editDistance(q, label);
      const ratio = 1 - distance / Math.max(q.length, label.length, 1);
      score = Math.max(score, ratio * 560);
    }
    if (record.node.publication_level === 'profile') score += 18;
    if (record.node.publication_level === 'research_stub') score -= 45;
    return score;
  }

  function rankNode(node) {
    if (node.publication_level === 'profile') return 0;
    if (node.publication_level === 'described') return 1;
    return 2;
  }

  function searchNodes(query, limit = 10, options = {}) {
    const q = normalise(query);
    let records = searchRecords;
    if (options.type && options.type !== 'all') {
      records = records.filter((record) => record.node.entity_type === options.type);
    }
    if (options.tag && options.tag !== 'all') {
      records = records.filter((record) => parse(record.node.set_tags, []).includes(options.tag));
    }
    if (options.level === 'profile') {
      records = records.filter((record) => record.node.publication_level === 'profile');
    }
    if (options.level === 'developed') {
      records = records.filter((record) => record.node.publication_level !== 'research_stub');
    }
    if (!q) {
      return records
        .slice()
        .sort((a, b) => rankNode(a.node) - rankNode(b.node) || a.node.label.localeCompare(b.node.label))
        .slice(0, limit)
        .map((record) => ({ ...record, score: 0 }));
    }
    return records
      .map((record) => ({ ...record, score: searchScore(q, record) }))
      .filter((record) => record.score > 155)
      .sort((a, b) => b.score - a.score || rankNode(a.node) - rankNode(b.node) || a.node.label.localeCompare(b.node.label))
      .slice(0, limit);
  }

  function bestNode(text) {
    return searchNodes(text, 1, { level: 'all' })[0]?.node || null;
  }

  function displayDefinition(node) {
    const profile = profileById.get(node.id);
    return profile?.canonical_definition
      || node.canonical_definition
      || node.description
      || node.public_stub_text
      || 'No public description yet.';
  }

  function entityLabel(type) {
    return ({
      concept: 'Concept',
      person: 'Person',
      method_or_methodology: 'Method or methodology',
      approach_family: 'Approach family',
      law_or_principle: 'Law or principle',
      tool: 'Tool',
      intervention_skill: 'Practice skill',
      tradition: 'Tradition',
      practice: 'Practice',
      technology: 'Technology',
      publication: 'Publication',
      organisation: 'Organisation',
      event: 'Event'
    })[type] || titleCase(type);
  }

  function statusLabel(node) {
    if (node.publication_level === 'profile') return 'Developed entry';
    if (node.publication_level === 'described') return 'Brief entry';
    return 'Outline only';
  }

  function publicStatusLabel(value) {
    const labels = {
      accepted: 'Accepted in this release',
      corroborated: 'Supported by more than one source',
      provisional: 'Provisional',
      disputed: 'Disputed',
      deferred: 'Needs more work',
      superseded: 'Superseded',
      rejected: 'Not accepted',
      legacy_unresolved: 'Unresolved legacy connection'
    };
    return labels[value] || titleCase(value || 'not stated');
  }


  function relationshipBasis(edge) {
    const mode = String(edge.assertion_mode || '').toLowerCase();
    const review = String(edge.public_review_label || '').toLowerCase();
    const hasSources = parse(edge.source_ids, []).length > 0;
    if (['inferred', 'candidate'].includes(mode)) {
      return {
        key: 'inference',
        label: mode === 'candidate' ? 'Candidate connection' : 'Inferred connection',
        description: 'This is a proposed or inferred connection, not a source-established statement.'
      };
    }
    if (['interpreted', 'editorial_research_pass'].includes(mode)) {
      return {
        key: 'interpretation',
        label: mode === 'editorial_research_pass' ? 'Editorial synthesis' : 'Curatorial interpretation',
        description: 'The connection is an editorial interpretation of the cited material.'
      };
    }
    if (mode === 'inherited') {
      return {
        key: 'inherited',
        label: 'Inherited record',
        description: 'The connection was inherited from an earlier register and still needs claim-level review.'
      };
    }
    if (mode === 'asserted' && hasSources && /source-established|source-backed|official bibliographic/.test(review)) {
      return {
        key: 'source-established',
        label: 'Source-established',
        description: 'The maintained statement is explicitly established by the linked source record.'
      };
    }
    if (mode === 'asserted' && hasSources) {
      return {
        key: 'sourced',
        label: 'Sourced assertion',
        description: 'The maintained assertion has a linked source; inspect the locator and status to judge its precision.'
      };
    }
    return {
      key: 'maintained',
      label: 'Maintained assertion',
      description: 'The atlas maintains this statement, but no stronger evidence-basis label is available.'
    };
  }

  function relationshipBasisBadge(edge) {
    const basis = relationshipBasis(edge);
    return `<span class="badge connection-basis ${esc(basis.key)}">${esc(basis.label)}</span>`;
  }

  function relationFamilyLabel(value) {
    return RELATION_FAMILY_LABELS[value] || titleCase(value);
  }

  function connectionBandLabel(value) {
    return ({
      rich: 'Rich connection structure',
      developing: 'Developing connection structure',
      thin: 'Thin connection structure',
      unconnected: 'No reader connections yet'
    })[value] || 'Connection depth not measured';
  }

  function evidenceBandLabel(value) {
    return ({
      supported: 'Mostly source-supported',
      mixed: 'Mixed accepted and provisional evidence',
      provisional: 'Provisional connections',
      none: 'No reader-connection evidence yet'
    })[value] || 'Evidence depth not measured';
  }

  function substantiveEdge(edge) {
    return !['classification', 'documentary', 'evidence', 'legacy'].includes(edge.relation_family)
      && edge.relation_type !== 'legacy_association_unspecified'
      && edge.claim_status !== 'legacy_unresolved';
  }

  function publicEntryEdge(edge) {
    const source = nodeById.get(edge.source);
    const target = nodeById.get(edge.target);
    return source?.public_visibility === 'public'
      && target?.public_visibility === 'public'
      && canonicalId(source.id) === source.id
      && canonicalId(target.id) === target.id
      && edge.relation_type !== 'legacy_association_unspecified'
      && edge.claim_status !== 'legacy_unresolved';
  }

  function edgeInLayer(edge) {
    const layer = $('mapLayer')?.value || 'all';
    if (edge.claim_status === 'legacy_unresolved' || edge.relation_family === 'legacy') {
      return layer === 'all';
    }
    if (layer === 'all') return true;
    if (layer === 'substantive') return substantiveEdge(edge);
    if (layer === 'conceptual') return edge.relation_family === 'conceptual';
    if (layer === 'human') return ['human', 'influence', 'historical'].includes(edge.relation_family);
    if (layer === 'practice') return edge.relation_family === 'practice';
    if (layer === 'contestation') return edge.relation_family === 'contestation'
      || ['disputed', 'challenged'].includes(edge.claim_status);
    if (layer === 'provenance') return ['classification', 'evidence', 'documentary'].includes(edge.relation_family);
    return substantiveEdge(edge);
  }

  function mapVisibleEdge(edge) {
    return edgeInLayer(edge);
  }

  function mapLayerDescription() {
    const descriptions = {
      all: 'Everything includes conceptual, human, practice, contestation, authorship, evidence and collection structure.',
      substantive: 'The reader map focuses on conceptual, historical, human, identity, practice and contestation relationships. Authorship, presentation, collection structure and evidence registration remain available in full entries and the complete graph.',
      conceptual: 'Conceptual lines show definitions, prerequisites, specialisation and explanatory relationships.',
      human: 'Human lineage combines teaching, collaboration, influence and historical transmission. The line type still matters.',
      practice: 'Practice lines connect ideas, methods, interventions and documented use.',
      contestation: 'Contestation makes critiques, corrections and rival framings visible rather than smoothing them away.',
      provenance: 'Provenance shows authorship, evidence, membership and collection structure. It does not imply intellectual influence.'
    };
    return descriptions[$('mapLayer')?.value || 'all'];
  }

  function updateMapLayerNote() {
    const note = $('mapLayerNote');
    if (note) note.textContent = mapLayerDescription();
  }

  function linkifyKnownText(value, excludedIds = []) {
    const text = String(value || '');
    if (!text) return '';
    const lower = text.toLowerCase();
    const excluded = new Set(excludedIds);
    const hits = [];
    const occupied = new Array(text.length).fill(false);
    for (const candidate of linkTerms) {
      if (excluded.has(candidate.node.id)) continue;
      let start = 0;
      while (start < lower.length) {
        const index = lower.indexOf(candidate.lower, start);
        if (index < 0) break;
        const end = index + candidate.term.length;
        const before = index === 0 ? '' : text[index - 1];
        const after = end >= text.length ? '' : text[end];
        const boundaryOK = (!before || /[^A-Za-z0-9]/.test(before))
          && (!after || /[^A-Za-z0-9]/.test(after));
        const free = boundaryOK && !occupied.slice(index, end).some(Boolean);
        if (free) {
          for (let i = index; i < end; i += 1) occupied[i] = true;
          hits.push({ start: index, end, node: candidate.node, text: text.slice(index, end) });
        }
        start = index + Math.max(1, candidate.term.length);
      }
      if (hits.length >= 24) break;
    }
    if (!hits.length) return esc(text);
    hits.sort((a, b) => a.start - b.start || b.end - a.end);
    let cursor = 0;
    const out = [];
    for (const hit of hits) {
      if (hit.start < cursor) continue;
      out.push(esc(text.slice(cursor, hit.start)));
      out.push(`<a href="${internalHref('item', { id: hit.node.id, from: baseView })}" class="text-button entry-link inline-concept internal-entry-link" data-id="${esc(hit.node.id)}">${esc(hit.text)}</a>`);
      cursor = hit.end;
    }
    out.push(esc(text.slice(cursor)));
    return out.join('');
  }

  let baseView = 'home';
  let activeJourney = null;
  let activeStep = 0;
  let mapFocus = 'concept_viability';
  let mapTransform = { x: 0, y: 0, scale: 1 };
  let mapSelectedEdge = null;
  let mapPath = [];
  let lastMapPositions = new Map();
  let mapFocusHistory = [mapFocus];
  let mapFocusHistoryIndex = 0;
  let mapPointerDragged = false;

  function internalHref(view, params = {}) {
    return `#${new URLSearchParams({ view, ...params }).toString()}`;
  }

  function plainLeftClick(event) {
    return event.button === 0 && !event.metaKey && !event.ctrlKey && !event.shiftKey && !event.altKey;
  }

  function followInternalAnchor(event, anchor) {
    if (!plainLeftClick(event)) return;
    event.preventDefault();
    const href = anchor.getAttribute('href') || internalHref(anchor.dataset.viewLink || anchor.dataset.view || 'home');
    if (location.hash !== href) history.pushState(null, '', href);
    route();
  }

  function setHash(params) {
    const sp = new URLSearchParams(params);
    const hash = sp.toString();
    if (location.hash.slice(1) !== hash) history.pushState(null, '', `#${hash}`);
  }

  function showView(view, push = true) {
    const safe = ['home', 'browse', 'journeys', 'map', 'ask', 'contribute', 'about', 'ai-observations'].includes(view)
      ? view
      : 'home';
    baseView = safe;
    $$('.view').forEach((element) => element.classList.toggle('active', element.id === `view-${safe}`));
    const navView = safe === 'ai-observations' ? 'about' : safe;
    $$('.main-nav [data-view]').forEach((link) => link.classList.toggle('active', link.dataset.view === navView));
    if (push) setHash({ view: safe });
    if (safe === 'browse') renderBrowse();
    if (safe === 'journeys') renderJourneys();
    if (safe === 'map') renderMap({ fit: true });
    if (safe === 'contribute') updateContributionHint();
    if (safe === 'ai-observations') renderAIObservations();
    window.scrollTo({ top: 0, behavior: 'instant' });
  }

  function route() {
    const sp = new URLSearchParams(location.hash.slice(1));
    const view = sp.get('view') || 'home';
    if (view === 'item') {
      const id = canonicalId(sp.get('id') || '');
      const returnView = sp.get('from') || baseView || 'browse';
      showView(
        ['home', 'browse', 'journeys', 'map', 'ask', 'contribute', 'about', 'ai-observations'].includes(returnView)
          ? returnView
          : 'browse',
        false
      );
      renderEntry(id);
      return;
    }
    closeDrawer(false);
    showView(view, false);
    if (view === 'journeys' && sp.get('id')) {
      activeJourney = sp.get('id');
      activeStep = Number(sp.get('step') || 0);
      renderJourneys();
    }
    if (view === 'map') {
      const layer = sp.get('layer');
      const depth = sp.get('depth');
      if (layer && [...$('mapLayer').options].some((option) => option.value === layer)) $('mapLayer').value = layer;
      if (depth && [...$('mapDepth').options].some((option) => option.value === depth)) $('mapDepth').value = depth;
      if (sp.get('edge')) mapSelectedEdge = sp.get('edge');
      if (sp.get('focus')) {
        mapFocus = canonicalId(sp.get('focus'));
        const focus = nodeById.get(mapFocus);
        if (focus) $('mapSearch').value = focus.label;
        recordMapFocus(mapFocus);
      }
      updateMapLayerNote();
      renderMap({ fit: true });
      if (mapSelectedEdge) inspectEdge(mapSelectedEdge, false);
    }
  }

  function sourceLink(source) {
    if (!source) return '';
    const creators = parse(source.creators, []).join(', ');
    const date = source.date ? String(source.date).slice(0, 4) : '';
    const details = [creators, date, source.publisher].filter(Boolean).join(' · ');
    return `<article class="source-card">
      <h3>${source.url
        ? `<a href="${esc(source.url)}" target="_blank" rel="noopener">${esc(source.title)}</a>`
        : esc(source.title)}</h3>
      ${details ? `<p class="small">${esc(details)}</p>` : ''}
      ${source.notes ? `<p>${esc(source.notes)}</p>` : ''}
      <div class="badges">
        <span class="badge">${esc(titleCase(source.source_type))}</span>
        <span class="badge ${source.url ? 'supported' : 'stub'}">${source.url ? 'Public link' : 'No public link'}</span>
      </div>
    </article>`;
  }

  function evidenceBlock(id) {
    const evidence = evidenceById.get(id);
    if (!evidence) return '';
    const source = sourceById.get(evidence.source_id);
    return `<div class="source-card">
      <p><strong>${esc(evidence.locator || 'Evidence record')}</strong></p>
      <p>${esc(evidence.excerpt_or_summary || '')}</p>
      <p class="small">Source: ${esc(source?.title || evidence.source_id)} · ${source?.url ? 'public link available' : 'no public link'}</p>
    </div>`;
  }

  function linkedList(items) {
    const values = Array.isArray(items) ? items : parse(items, []);
    return `<ul class="link-list">${values.map((value) => {
      const match = searchNodes(value, 1, { level: 'all' })[0];
      const canLink = match && match.score > 470;
      return `<li>${canLink
        ? `<a href="${internalHref('item', { id: match.node.id, from: baseView })}" class="chip entry-link internal-entry-link" data-id="${esc(match.node.id)}">${esc(value)}</a>`
        : `<span>• ${esc(value)}</span>`}</li>`;
    }).join('')}</ul>`;
  }

  function relationStatement(edge) {
    const source = nodeById.get(edge.source);
    const target = nodeById.get(edge.target);
    return `<span>
      <a href="${internalHref('item', { id: edge.source, from: baseView })}" class="text-button entry-link internal-entry-link" data-id="${esc(edge.source)}">${esc(source?.label || edge.source)}</a>
      <strong>${esc(edge.plain_phrase || edge.relation_type)}</strong>
      <a href="${internalHref('item', { id: edge.target, from: baseView })}" class="text-button entry-link internal-entry-link" data-id="${esc(edge.target)}">${esc(target?.label || edge.target)}</a>
    </span>`;
  }

  function renderEntry(id) {
    const node = nodeById.get(canonicalId(id));
    if (!node || node.public_visibility !== 'public') return;
    const profile = profileById.get(node.id);
    const depth = relationalDepthByNode[node.id];
    const sources = unique([
      ...parse(node.source_ids, []),
      ...(profile ? parse(profile.source_ids, []) : [])
    ]).map((sourceId) => sourceById.get(sourceId)).filter(Boolean);
    // A full entry should expose every meaningful public-to-public statement,
    // including source-backed collection and documentary connections. The map's
    // default reader layer remains deliberately narrower.
    const relations = (edgesByNode.get(node.id) || []).filter(publicEntryEdge);
    const claims = (DATA.claims || []).filter((claim) =>
      canonicalId(claim.subject_id) === node.id || canonicalId(claim.object_id) === node.id
    );
    const sourceLinks = sources.map(sourceLink).join('') || '<p>No sources are linked yet.</p>';
    const sections = [];

    if (profile?.why_it_matters) {
      sections.push(`<section class="entry-section"><h2>Why it matters</h2><p>${linkifyKnownText(profile.why_it_matters, [node.id])}</p></section>`);
    }
    const profileLists = [
      ['Key distinctions', 'key_distinctions'],
      ['Historical development', 'historical_lineage'],
      ['Ideas it depends on', 'logical_antecedents'],
      ['What develops from it', 'dependent_subsequents'],
      ['Connections to practice', 'practice_connections'],
      ['Common confusions', 'common_misreadings'],
      ['Open questions and checks', 'open_checks']
    ];
    for (const [title, key] of profileLists) {
      if (profile?.[key] && parse(profile[key], []).length) {
        sections.push(`<section class="entry-section"><h2>${esc(title)}</h2>${linkedList(profile[key])}</section>`);
      }
    }

    const relationRows = relations
      .sort((a, b) =>
        (a.relation_family || '').localeCompare(b.relation_family || '')
        || (a.plain_phrase || '').localeCompare(b.plain_phrase || '')
      )
      .map((edge) => `<tr>
        <td>${relationStatement(edge)}<div class="small">${esc(edge.scope_conditions || edge.notes || '')}</div></td>
        <td>
          <span class="badge ${['accepted', 'corroborated'].includes(edge.claim_status) ? 'supported' : 'provisional'}">${esc(edge.public_review_label || publicStatusLabel(edge.claim_status))}</span> ${relationshipBasisBadge(edge)}<br>
          <button class="text-button inspect-edge" data-edge="${esc(edge.id)}">Inspect this connection</button>
        </td>
      </tr>`).join('');

    const claimBlocks = claims.map((claim) => `<div class="claim-card">
      <p>${linkifyKnownText(claim.statement, [node.id])}</p>
      <div class="badges">
        <span class="badge">${esc(publicStatusLabel(claim.status))}</span>
        <span class="badge">${esc(titleCase(claim.review_status))}</span>
      </div>
    </div>`).join('');

    const evidenceIds = unique([
      ...(profile ? parse(profile.evidence_ids, []) : []),
      ...relations.flatMap((edge) => parse(edge.evidence_ids, [])),
      ...claims.flatMap((claim) => parse(claim.supporting_evidence_ids, []))
    ]);

    $('drawerBody').innerHTML = `<article class="entry-head">
      <p class="eyebrow">${esc(entityLabel(node.entity_type))}</p>
      <h1>${esc(node.label)}</h1>
      <div class="badges">
        <span class="badge ${node.publication_level === 'research_stub' ? 'status-stub' : node.publication_level === 'profile' ? 'status-profile' : ''}">${esc(statusLabel(node))}</span>
        ${depth ? `<span class="badge connection-band ${esc(depth.connection_band)}">${esc(connectionBandLabel(depth.connection_band))}</span><span class="badge evidence-band ${esc(depth.evidence_band)}">${esc(evidenceBandLabel(depth.evidence_band))}</span>` : ''}
        ${parse(node.set_tags, []).slice(0, 5).map((tag) => `<button class="badge tag-filter" data-tag="${esc(tag)}">${esc(titleCase(tag))}</button>`).join('')}
      </div>
      <p class="entry-definition">${linkifyKnownText(displayDefinition(node), [node.id])}</p>
      ${profile?.summary && profile.summary !== displayDefinition(node)
        ? `<p>${linkifyKnownText(profile.summary, [node.id])}</p>`
        : ''}
      <p class="small">${node.public_source_count || 0} linked public source${node.public_source_count === 1 ? '' : 's'}${node.no_public_link_count ? ` · ${node.no_public_link_count} cited item${node.no_public_link_count === 1 ? '' : 's'} with no public link` : ''}${depth ? ` · ${depth.reader_connections} reader connection${depth.reader_connections === 1 ? '' : 's'} across ${depth.distinct_reader_families} relation famil${depth.distinct_reader_families === 1 ? 'y' : 'ies'}` : ''}</p>
      <div class="entry-actions">
        <a class="button primary map-entry" href="${internalHref('map', { layer: 'substantive', depth: 'constellation', focus: node.id })}" data-id="${esc(node.id)}">Place in the tangle</a>
        <a class="button ask-entry" href="${internalHref('ask', { seed: node.id })}" data-id="${esc(node.id)}">Ask about this</a>
        <a class="button contribute-entry" href="${internalHref('contribute', { entry: node.id })}" data-id="${esc(node.id)}">Suggest a change</a>
        <a class="button" href="${esc(CONFIG.discussionsUrl || `${CONFIG.repositoryUrl}/discussions`)}" target="_blank" rel="noopener">Discuss</a>
        <button id="copyEntryLink">Copy link</button>
      </div>
    </article>
    ${sections.join('')}
    ${relations.length ? `<section class="entry-section"><h2>Connections</h2><p>Each line below is a specific statement. Open it to see its meaning, limits and evidence.</p><table class="relations-table"><tbody>${relationRows}</tbody></table></section>` : ''}
    ${claims.length ? `<section class="entry-section"><h2>Claims and disputes</h2>${claimBlocks}</section>` : ''}
    <section class="entry-section"><h2>Sources</h2>${sourceLinks}</section>
    ${evidenceIds.length ? `<section class="entry-section"><h2>Evidence records</h2>${evidenceIds.map(evidenceBlock).join('')}</section>` : ''}`;

    $('entryDrawer').classList.add('open');
    $('drawerScrim').classList.add('open');
    $('entryDrawer').setAttribute('aria-hidden', 'false');
    bindEntryActions($('drawerBody'));

    $('copyEntryLink').addEventListener('click', async () => {
      const url = new URL(location.href);
      url.hash = new URLSearchParams({ view: 'item', id: node.id, from: baseView }).toString();
      try {
        await navigator.clipboard.writeText(url.toString());
        $('copyEntryLink').textContent = 'Link copied';
      } catch (_) {
        window.prompt('Copy this link', url.toString());
      }
    });

    const expectedHash = `#${new URLSearchParams({ view: 'item', id: node.id, from: baseView }).toString()}`;
    if (location.hash !== expectedHash) setHash({ view: 'item', id: node.id, from: baseView });
  }

  function bindEntryActions(root) {
    $$('.entry-link', root).forEach((link) => link.addEventListener('click', (event) => {
      if (!plainLeftClick(event)) return;
      event.preventDefault();
      renderEntry(link.dataset.id);
    }));
    $$('.tag-filter', root).forEach((button) => button.addEventListener('click', () => {
      closeDrawer(false);
      showView('browse');
      $('browseTag').value = button.dataset.tag;
      renderBrowse();
    }));
    $$('.inspect-edge', root).forEach((button) => button.addEventListener('click', (event) => { if (!plainLeftClick(event)) return; event.preventDefault(); inspectEdge(button.dataset.edge, true); }));
    $$('.map-entry', root).forEach((button) => button.addEventListener('click', (event) => {
      if (!plainLeftClick(event)) return;
      event.preventDefault();
      closeDrawer(false);
      mapFocus = button.dataset.id;
      recordMapFocus(mapFocus);
      mapPath = [];
      $('mapSearch').value = nodeById.get(mapFocus)?.label || '';
      showView('map');
      setHash({ view: 'map', focus: mapFocus });
      renderMap({ fit: true });
    }));
    $$('.ask-entry', root).forEach((button) => button.addEventListener('click', (event) => {
      if (!plainLeftClick(event)) return;
      event.preventDefault();
      const node = nodeById.get(button.dataset.id);
      closeDrawer(false);
      showView('ask');
      $('askQuestion').value = `Explain ${node.label}, its strongest connections, and the evidence behind them.`;
      $('askForm').requestSubmit();
    }));
    $$('.contribute-entry', root).forEach((button) => button.addEventListener('click', (event) => {
      if (!plainLeftClick(event)) return;
      event.preventDefault();
      const node = nodeById.get(button.dataset.id);
      closeDrawer(false);
      showView('contribute');
      $('contributionItem').value = node.label;
      $('contributionItem').dataset.selectedId = node.id;
      $('contributionItemId').value = node.id;
      updateContributionHint();
    }));
  }

  function closeDrawer(update = true) {
    $('entryDrawer').classList.remove('open');
    $('drawerScrim').classList.remove('open');
    $('entryDrawer').setAttribute('aria-hidden', 'true');
    if (update && new URLSearchParams(location.hash.slice(1)).get('view') === 'item') {
      setHash({ view: baseView });
    }
  }

  function card(node) {
    const tags = parse(node.set_tags, [])
      .filter((tag) => ['systems', 'cybernetics', 'complexity', 'practice', 'management_cybernetics', 'critical_systems'].includes(tag))
      .slice(0, 3);
    const depth = relationalDepthByNode[node.id];
    const connectionMeta = depth
      ? `${depth.reader_connections} reader connection${depth.reader_connections === 1 ? '' : 's'} · ${depth.distinct_reader_families} relation famil${depth.distinct_reader_families === 1 ? 'y' : 'ies'} · ${connectionBandLabel(depth.connection_band)}`
      : 'Connection depth not measured';
    return `<article class="card">
      <div class="badges">
        <button class="badge type-filter" data-type="${esc(node.entity_type)}">${esc(entityLabel(node.entity_type))}</button>
        <span class="badge ${node.publication_level === 'profile' ? 'status-profile' : node.publication_level === 'research_stub' ? 'status-stub' : ''}">${esc(statusLabel(node))}</span>
      </div>
      <h3>${esc(node.label)}</h3>
      <p>${esc(displayDefinition(node))}</p>
      <footer>
        <span class="meta">${esc(connectionMeta)}<br>${node.public_source_count || 0} public source${node.public_source_count === 1 ? '' : 's'}${tags.length ? ` · ${tags.map((tag) => esc(titleCase(tag))).join(', ')}` : ''}</span>
        <a href="${internalHref('item', { id: node.id, from: baseView })}" class="text-button open-card internal-entry-link" data-id="${esc(node.id)}">Open</a>
      </footer>
    </article>`;
  }

  function bindCards(root = document) {
    $$('.open-card', root).forEach((link) => link.addEventListener('click', (event) => {
      if (!plainLeftClick(event)) return;
      event.preventDefault();
      renderEntry(link.dataset.id);
    }));
    $$('.type-filter', root).forEach((button) => button.addEventListener('click', () => {
      showView('browse');
      $('browseType').value = button.dataset.type;
      renderBrowse();
    }));
  }

  function renderAIObservations() {
    const report = DATA.ai_observations;
    if (!report) return;
    const metrics = report.metrics || {};
    const metricRows = [
      [metrics.public_entries, 'public entries'],
      [metrics.developed_profiles, 'developed profiles'],
      [metrics.typed_edges, 'typed public edges'],
      [metrics.substantive_edges, 'substantive edges'],
      [metrics.substantive_connected_nodes, 'substantively connected'],
      [metrics.substantive_isolated_nodes, 'substantive isolates'],
      [metrics.sources, 'registered sources'],
      [metrics.connected_nodes_outside_neighbourhoods, 'connected outside old neighbourhoods']
    ];
    $('aiMethodNote').textContent = report.method_note || '';
    $('aiObservationMetrics').innerHTML = metricRows.map(([number, label]) => `
      <div class="metric"><strong>${esc(number ?? '—')}</strong><span>${esc(label)}</span></div>
    `).join('');
    $('aiObservationsList').innerHTML = (report.observations || []).map((observation, index) => `
      <article class="observation-card">
        <p class="eyebrow">Observation ${index + 1} · ${esc(observation.kind || 'interpretation')}</p>
        <h2>${esc(observation.title)}</h2>
        <dl>
          <div><dt>Measured</dt><dd>${esc(observation.measurement)}</dd></div>
          <div><dt>Interpretation</dt><dd>${esc(observation.interpretation)}</dd></div>
          <div><dt>What follows</dt><dd>${esc(observation.implication)}</dd></div>
          <div><dt>Test it</dt><dd>${esc(observation.test)}</dd></div>
        </dl>
      </article>
    `).join('');
    $('sourceMiningList').innerHTML = (DATA.source_mining_register || []).map((source) => `
      <article class="source-mining-card">
        <p class="eyebrow">${esc(titleCase(source.status))}</p>
        <h3><a href="${esc(source.url)}" target="_blank" rel="noopener">${esc(source.label)}</a></h3>
        <p>${esc(source.role)}</p>
        <p class="small"><strong>Caution:</strong> ${esc(source.caveat)}</p>
        <p class="small"><strong>Next:</strong> ${esc(source.next_step)}</p>
      </article>
    `).join('');
  }

  function renderHome() {
    $('releaseBadge').textContent = `Release ${DATA.meta.release}`;
    const relational = DATA.relational_depth?.aggregate || {};
    const bands = relational.connection_bands || {};
    const metrics = [
      [DATA.meta.described_entry_count, 'readable public entries'],
      [relational.reader_connected_entries ?? '—', 'with reader connections'],
      [(bands.rich || 0) + (bands.developing || 0), 'developing or rich'],
      [relational.reader_statements ?? '—', 'reader relationship statements']
    ];
    $('homeMetrics').innerHTML = metrics
      .map(([number, label]) => `<div class="metric"><strong>${esc(number)}</strong><span>${esc(label)}</span></div>`)
      .join('');

    const depthMetrics = $('relationalDepthMetrics');
    if (depthMetrics) {
      const rows = [
        [bands.rich || 0, 'rich'],
        [bands.developing || 0, 'developing'],
        [bands.thin || 0, 'thin'],
        [bands.unconnected || 0, 'unconnected']
      ];
      depthMetrics.innerHTML = rows.map(([number, label]) => `
        <div class="metric"><strong>${esc(number)}</strong><span>${esc(label)}</span></div>
      `).join('');
    }
    $('quickLinks').innerHTML = ['Viability', 'Boundary', 'Feedback', 'Emergence', 'Requisite variety', 'Viable System Model']
      .map((label) => {
        const node = bestNode(label);
        return node ? `<a href="${internalHref('item', { id: node.id, from: 'home' })}" class="chip open-card internal-entry-link" data-id="${esc(node.id)}">${esc(label)}</a>` : '';
      }).join('');

    const journeys = DATA.journeys || [];
    $('homeJourneys').innerHTML = journeys.slice(0, 3).map((journey) => `<article class="card">
      <p class="eyebrow">${esc(journey.audience)} · ${esc(journey.duration_minutes)} minutes</p>
      <h3>${esc(journey.title)}</h3>
      <p>${esc(journey.summary)}</p>
      <footer><span class="meta">${journey.steps.length} linked steps</span><a href="${internalHref('journeys', { id: journey.id, step: 0 })}" class="text-button open-journey" data-id="${esc(journey.id)}">Begin</a></footer>
    </article>`).join('');

    const preferred = [
      'concept_boundary',
      'concept_viability',
      'concept_feedback',
      'concept_emergence',
      'concept_requisite_variety',
      'concept_information',
      'concept_observer',
      'method_or_methodology_viable_system_model_vsm'
    ];
    $('homeEntries').innerHTML = preferred
      .map((id) => nodeById.get(id))
      .filter(Boolean)
      .map(card)
      .join('');
    bindCards($('view-home'));
    $$('.open-journey', $('homeJourneys')).forEach((link) => link.addEventListener('click', (event) => {
      if (!plainLeftClick(event)) return;
      event.preventDefault();
      activeJourney = link.dataset.id;
      activeStep = 0;
      showView('journeys');
      setHash({ view: 'journeys', id: activeJourney, step: 0 });
      renderJourneys();
    }));
  }

  function populateFilters() {
    const types = unique(publicNodes.map((node) => node.entity_type)).sort();
    $('browseType').innerHTML = '<option value="all">All entry types</option>'
      + types.map((type) => `<option value="${esc(type)}">${esc(entityLabel(type))}</option>`).join('');

    const tags = unique(publicNodes
      .flatMap((node) => parse(node.set_tags, []))
      .filter((tag) => [
        'systems', 'cybernetics', 'complexity', 'practice', 'management_cybernetics',
        'critical_systems', 'organisation', 'epistemology', 'information', 'control', 'viability'
      ].includes(tag)))
      .sort();
    $('browseTag').innerHTML = '<option value="all">All fields</option>'
      + tags.map((tag) => `<option value="${esc(tag)}">${esc(titleCase(tag))}</option>`).join('');

    const families = unique(canonicalEdges.filter(substantiveEdge).map((edge) => edge.relation_family).filter(Boolean)).sort();
    $('mapFamily').innerHTML = '<option value="all">All connection types</option>'
      + families.map((family) => `<option value="${esc(family)}">${esc(relationFamilyLabel(family))}</option>`).join('');
  }

  function renderBrowse() {
    const query = $('browseSearch').value.trim();
    const connectionDepth = $('browseConnectionDepth')?.value || 'all';
    const options = {
      type: $('browseType').value,
      tag: $('browseTag').value,
      level: $('browseLevel').value
    };
    const matched = query
      ? searchNodes(query, 500, options).map((result) => result.node)
      : searchNodes('', 1000, options).map((result) => result.node);
    const results = connectionDepth === 'all'
      ? matched
      : matched.filter((node) => relationalDepthByNode[node.id]?.connection_band === connectionDepth);
    $('browseCount').textContent = `${results.length} ${results.length === 1 ? 'entry' : 'entries'}`;
    $('browseCards').innerHTML = results.map(card).join('')
      || '<div class="empty-card"><h2>No matches</h2><p>Try a shorter phrase or include outline-only entries.</p></div>';
    bindCards($('browseCards'));
  }

  function renderJourneys() {
    const journeys = DATA.journeys || [];
    if (!activeJourney) activeJourney = journeys[0]?.id || null;
    $('journeyList').innerHTML = journeys.map((journey) => `<a href="${internalHref('journeys', { id: journey.id, step: 0 })}" class="journey-choice ${journey.id === activeJourney ? 'active' : ''}" data-id="${esc(journey.id)}">
      <strong>${esc(journey.title)}</strong>
      <small>${esc(journey.duration_minutes)} minutes · ${journey.steps.length} steps</small>
    </a>`).join('');
    $$('.journey-choice', $('journeyList')).forEach((link) => link.addEventListener('click', (event) => {
      if (!plainLeftClick(event)) return;
      event.preventDefault();
      activeJourney = link.dataset.id;
      activeStep = 0;
      setHash({ view: 'journeys', id: activeJourney, step: 0 });
      renderJourneys();
    }));

    const journey = journeys.find((candidate) => candidate.id === activeJourney);
    if (!journey) return;
    activeStep = Math.max(0, Math.min(activeStep, journey.steps.length - 1));
    const step = journey.steps[activeStep];
    const node = nodeById.get(canonicalId(step.node_id));
    $('journeyRunner').classList.remove('empty');
    $('journeyRunner').innerHTML = `<div class="journey-step-head">
      <span>Step ${activeStep + 1} of ${journey.steps.length}</span>
      <span>${esc(journey.audience)} · about ${esc(journey.duration_minutes)} minutes</span>
    </div>
    <h2>${esc(journey.title)}</h2>
    <p>${linkifyKnownText(journey.subtitle || journey.summary)}</p>
    <div class="step-track">${journey.steps.map((_, index) => `<button data-step="${index}" class="${index === activeStep ? 'active' : ''}" aria-label="Open step ${index + 1}">${index + 1}</button>`).join('')}</div>
    <div class="step-card">
      <p class="eyebrow">${esc(entityLabel(node?.entity_type))}</p>
      <h3><a href="${internalHref('item', { id: node?.id, from: 'journeys' })}" class="text-button open-card internal-entry-link" data-id="${esc(node?.id)}">${esc(node?.label || step.node_id)}</a></h3>
      <p>${linkifyKnownText(step.narrative, [node?.id])}</p>
      <p class="small">${linkifyKnownText(displayDefinition(node || {}), [node?.id])}</p>
      <a href="${internalHref('item', { id: node?.id, from: 'journeys' })}" class="button primary open-card internal-entry-link" data-id="${esc(node?.id)}">Open the full entry</a>
    </div>
    <div class="journey-actions">
      <button id="journeyPrev" ${activeStep === 0 ? 'disabled' : ''}>Previous</button>
      <button id="journeyNext" class="primary" ${activeStep === journey.steps.length - 1 ? 'disabled' : ''}>Next</button>
    </div>`;
    bindCards($('journeyRunner'));
    $$('.entry-link', $('journeyRunner')).forEach((button) => button.addEventListener('click', () => renderEntry(button.dataset.id)));
    $$('#journeyRunner [data-step]').forEach((button) => button.addEventListener('click', () => {
      activeStep = Number(button.dataset.step);
      setHash({ view: 'journeys', id: activeJourney, step: activeStep });
      renderJourneys();
    }));
    $('journeyPrev').addEventListener('click', () => {
      activeStep -= 1;
      setHash({ view: 'journeys', id: activeJourney, step: activeStep });
      renderJourneys();
    });
    $('journeyNext').addEventListener('click', () => {
      activeStep += 1;
      setHash({ view: 'journeys', id: activeJourney, step: activeStep });
      renderJourneys();
    });
  }

  const colours = {
    concept: '#9f161b',
    person: '#246a86',
    method_or_methodology: '#347255',
    approach_family: '#347255',
    law_or_principle: '#e97014',
    tool: '#6f4b7e',
    intervention_skill: '#8b6a24',
    tradition: '#4f5b6c',
    practice: '#347255',
    technology: '#6d625b',
    publication: '#6d625b',
    organisation: '#246a86',
    event: '#8b6a24'
  };

  function graphNodeMark(node, position, radius) {
    const fill = colours[node.entity_type] || '#6d625b';
    const title = `<title>${esc(node.label)}</title>`;
    const organisational = new Set(['person', 'organisation', 'corpus', 'comparator_corpus', 'event']);
    const practical = new Set(['method_or_methodology', 'approach_family', 'practice', 'tool', 'intervention_skill', 'technology']);
    if (node.entity_type === 'publication') {
      return `<rect class="graph-node node-publication" x="${position.x - radius}" y="${position.y - radius}" width="${radius * 2}" height="${radius * 2}" fill="${fill}">${title}</rect>`;
    }
    if (organisational.has(node.entity_type)) {
      return `<rect class="graph-node node-organisational" x="${position.x - radius}" y="${position.y - radius}" width="${radius * 2}" height="${radius * 2}" rx="${Math.max(3, radius * .42)}" fill="${fill}">${title}</rect>`;
    }
    if (practical.has(node.entity_type)) {
      const points = `${position.x},${position.y - radius - 1} ${position.x + radius + 1},${position.y} ${position.x},${position.y + radius + 1} ${position.x - radius - 1},${position.y}`;
      return `<polygon class="graph-node node-practical" points="${points}" fill="${fill}">${title}</polygon>`;
    }
    return `<circle class="graph-node node-conceptual" cx="${position.x}" cy="${position.y}" r="${radius}" fill="${fill}">${title}</circle>`;
  }

  function graphSelection() {
    const mode = $('mapDepth').value;
    const family = $('mapFamily').value;
    const includeOutline = $('mapIncludeStubs').checked;
    const allowed = new Set(publicNodes
      .filter((node) => includeOutline || node.publication_level !== 'research_stub')
      .map((node) => node.id));

    if (mode === 'path' && mapPath.length) {
      const selected = new Set(mapPath.filter((id) => allowed.has(id)));
      for (const id of mapPath) {
        for (const edge of (edgesByNode.get(id) || [])) {
          if (!edgeInLayer(edge)) continue;
          if (family !== 'all' && edge.relation_family !== family) continue;
          const other = edge.source === id ? edge.target : edge.source;
          if (allowed.has(other)) selected.add(other);
        }
      }
      return selected;
    }
    if (mode === 'all') {
      if (family === 'all') return new Set(allowed);
      const incident = new Set();
      for (const edge of canonicalEdges) {
        if (!edgeInLayer(edge)) continue;
        if (family !== 'all' && edge.relation_family !== family) continue;
        if (allowed.has(edge.source)) incident.add(edge.source);
        if (allowed.has(edge.target)) incident.add(edge.target);
      }
      if (allowed.has(mapFocus)) incident.add(mapFocus);
      return incident;
    }
    if (mode === 'profiles') {
      return new Set(publicNodes.filter((node) => node.publication_level === 'profile').map((node) => node.id));
    }

    const depth = mode === 'constellation' ? 2 : Number(mode);
    const fallback = allowed.has('concept_viability') ? 'concept_viability' : [...allowed][0];
    const focus = allowed.has(mapFocus) ? mapFocus : fallback;
    const visited = new Map([[focus, 0]]);
    const queue = [focus];
    while (queue.length) {
      const id = queue.shift();
      const distance = visited.get(id);
      if (distance >= depth) continue;
      for (const edge of (edgesByNode.get(id) || [])) {
        if (!edgeInLayer(edge)) continue;
        if (family !== 'all' && edge.relation_family !== family) continue;
        const other = edge.source === id ? edge.target : edge.source;
        if (!allowed.has(other) || visited.has(other)) continue;
        visited.set(other, distance + 1);
        queue.push(other);
      }
    }
    const ids = [...visited.keys()];
    return new Set(ids.length > 80 ? ids.slice(0, 80) : ids);
  }

  function mapPositions(ids) {
    const mode = $('mapDepth').value;
    const nodes = [...ids].map((id) => nodeById.get(id)).filter(Boolean);
    const positions = new Map();
    if (mode === 'all' || mode === 'profiles') {
      nodes.forEach((node) => positions.set(node.id, {
        x: 600 + Number(node.x || 0) * 500,
        y: 380 + Number(node.y || 0) * 300
      }));
      return positions;
    }

    const distance = new Map([[mapFocus, 0]]);
    const queue = [mapFocus];
    while (queue.length) {
      const id = queue.shift();
      for (const edge of (edgesByNode.get(id) || [])) {
        if (!substantiveEdge(edge)) continue;
        const other = edge.source === id ? edge.target : edge.source;
        if (!ids.has(other) || distance.has(other)) continue;
        distance.set(other, distance.get(id) + 1);
        queue.push(other);
      }
    }

    if (ids.has(mapFocus)) positions.set(mapFocus, { x: 600, y: 380 });
    const rings = unique([...distance.values()].filter((value) => value > 0)).sort((a, b) => a - b);
    for (const distanceValue of rings) {
      const ring = nodes
        .filter((node) => distance.get(node.id) === distanceValue)
        .sort((a, b) => {
          const angleA = previousAngle(a.id);
          const angleB = previousAngle(b.id);
          if (angleA !== null && angleB !== null) return angleA - angleB;
          if (angleA !== null) return -1;
          if (angleB !== null) return 1;
          return a.label.localeCompare(b.label);
        });
      const radius = distanceValue === 1
        ? Math.min(315, Math.max(215, ring.length * 24))
        : 335 + (distanceValue - 2) * 80;
      ring.forEach((node, index) => {
        const angle = -Math.PI / 2 + (2 * Math.PI * index / Math.max(ring.length, 1));
        positions.set(node.id, {
          x: 600 + Math.cos(angle) * radius,
          y: 380 + Math.sin(angle) * radius
        });
      });
    }

    nodes.filter((node) => !positions.has(node.id)).forEach((node, index, remaining) => {
      const angle = 2 * Math.PI * index / Math.max(remaining.length, 1);
      positions.set(node.id, {
        x: 600 + Math.cos(angle) * 340,
        y: 380 + Math.sin(angle) * 300
      });
    });
    return positions;
  }

  function previousAngle(nodeId) {
    const position = lastMapPositions.get(nodeId);
    if (!position) return null;
    return Math.atan2(position.y - 380, position.x - 600);
  }

  function animateMapTransition(previous, next) {
    if (!previous?.size || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    $$('.graph-node-group', $('graphNodes')).forEach((group) => {
      const before = previous.get(group.dataset.id);
      const after = next.get(group.dataset.id);
      if (!before || !after) return;
      const dx = before.x - after.x;
      const dy = before.y - after.y;
      if (Math.abs(dx) < 1 && Math.abs(dy) < 1) return;
      group.animate(
        [
          { transform: `translate(${dx}px, ${dy}px)`, opacity: 0.72 },
          { transform: 'translate(0px, 0px)', opacity: 1 }
        ],
        { duration: 460, easing: 'cubic-bezier(.2,.75,.25,1)' }
      );
    });
    $$('.graph-edge-group', $('graphEdges')).forEach((group) => {
      group.animate([{ opacity: 0.08 }, { opacity: 1 }], { duration: 420, easing: 'ease-out' });
    });
  }

  function moveMapToFocus(id) {
    const position = lastMapPositions.get(id);
    if (!position) {
      fitMapToSelection();
      return;
    }
    const start = { ...mapTransform };
    const scale = Math.max(0.78, Math.min(1.35, start.scale < 0.58 ? 0.92 : start.scale));
    const target = {
      scale,
      x: 600 - position.x * scale,
      y: 380 - position.y * scale
    };
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      mapTransform = target;
      applyMapTransform();
      return;
    }
    const started = performance.now();
    const duration = 420;
    const step = (now) => {
      const raw = Math.min(1, (now - started) / duration);
      const eased = 1 - Math.pow(1 - raw, 3);
      mapTransform = {
        scale: start.scale + (target.scale - start.scale) * eased,
        x: start.x + (target.x - start.x) * eased,
        y: start.y + (target.y - start.y) * eased
      };
      applyMapTransform();
      if (raw < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  }

  function updateMapHistoryButtons() {
    const back = $('mapBack');
    const forward = $('mapForward');
    if (back) back.disabled = mapFocusHistoryIndex <= 0;
    if (forward) forward.disabled = mapFocusHistoryIndex >= mapFocusHistory.length - 1;
  }

  function recordMapFocus(id) {
    if (!id || mapFocusHistory[mapFocusHistoryIndex] === id) {
      updateMapHistoryButtons();
      return;
    }
    mapFocusHistory = mapFocusHistory.slice(0, mapFocusHistoryIndex + 1);
    mapFocusHistory.push(id);
    mapFocusHistoryIndex = mapFocusHistory.length - 1;
    updateMapHistoryButtons();
  }

  function navigateMapHistory(delta) {
    const next = Math.max(0, Math.min(mapFocusHistory.length - 1, mapFocusHistoryIndex + delta));
    if (next === mapFocusHistoryIndex) return;
    mapFocusHistoryIndex = next;
    mapFocus = mapFocusHistory[mapFocusHistoryIndex];
    mapSelectedEdge = null;
    mapPath = [];
    $('mapSearch').value = nodeById.get(mapFocus)?.label || '';
    const keepsWholeMap = ['all', 'profiles'].includes($('mapDepth').value);
    renderMap({ fit: !keepsWholeMap, focus: keepsWholeMap });
    inspectNode(mapFocus);
    setHash({ view: 'map', focus: mapFocus, layer: $('mapLayer').value, depth: $('mapDepth').value });
    updateMapHistoryButtons();
  }

  function activateMapNode(id, options = {}) {
    if (!nodeById.has(id)) return;
    mapFocus = id;
    if (options.history !== false) recordMapFocus(id);
    mapSelectedEdge = null;
    if (!$('mapDepth').value || ['path', 'profiles', 'all'].includes($('mapDepth').value)) $('mapDepth').value = '1';
    mapPath = [];
    $('mapSearch').value = nodeById.get(mapFocus)?.label || '';
    const keepsWholeMap = ['all', 'profiles'].includes($('mapDepth').value);
    renderMap({ fit: !keepsWholeMap, focus: keepsWholeMap });
    inspectNode(mapFocus);
    setHash({ view: 'map', focus: mapFocus, layer: $('mapLayer').value, depth: $('mapDepth').value });
  }

  function renderMap(options = {}) {
    const ids = graphSelection();
    if (!ids.has(mapFocus) && ids.size) mapFocus = [...ids][0];
    const previousPositions = lastMapPositions;
    const positions = mapPositions(ids);
    lastMapPositions = positions;
    const family = $('mapFamily').value;
    const edges = canonicalEdges.filter((edge) =>
      ids.has(edge.source)
      && ids.has(edge.target)
      && mapVisibleEdge(edge)
      && (family === 'all' || edge.relation_family === family)
    );
    const pathPairs = new Set(mapPath.slice(0, -1).flatMap((id, index) => [
      `${id}|${mapPath[index + 1]}`,
      `${mapPath[index + 1]}|${id}`
    ]));
    const wideView = ['all', 'profiles'].includes($('mapDepth').value);
    const focusEdges = edges.filter((edge) => edge.source === mapFocus || edge.target === mapFocus);
    const focusNeighbours = new Set(focusEdges.map((edge) => edge.source === mapFocus ? edge.target : edge.source));

    $('graphEdges').innerHTML = edges.map((edge) => {
      const source = positions.get(edge.source);
      const target = positions.get(edge.target);
      const selected = edge.id === mapSelectedEdge;
      const inPath = pathPairs.has(`${edge.source}|${edge.target}`);
      const focusEdge = edge.source === mapFocus || edge.target === mapFocus;
      const contextEdge = !focusEdge && !selected && !inPath;
      const classes = [
        'graph-edge',
        ['accepted', 'corroborated'].includes(edge.claim_status) ? '' : 'provisional',
        substantiveEdge(edge) ? '' : 'contextual',
        selected || inPath ? 'selected' : '',
        focusEdge ? 'focus-edge' : '',
        contextEdge ? 'context-edge' : ''
      ].filter(Boolean).join(' ');
      const title = `${nodeById.get(edge.source)?.label || edge.source} ${edge.plain_phrase || edge.relation_type} ${nodeById.get(edge.target)?.label || edge.target}`;
      const midpointX = (source.x + target.x) / 2;
      const midpointY = (source.y + target.y) / 2;
      const showFocusLabel = !wideView && focusEdge && focusEdges.length <= 6;
      const labelClass = selected || inPath || showFocusLabel ? 'visible' : '';
      return `<a class="graph-edge-link" href="${internalHref('map', { layer: $('mapLayer').value, depth: $('mapDepth').value, focus: edge.source, edge: edge.id })}"><g class="graph-edge-group" data-edge="${esc(edge.id)}" tabindex="0" role="button" aria-label="${esc(title)}">
        <line class="graph-edge-hit" x1="${source.x}" y1="${source.y}" x2="${target.x}" y2="${target.y}"></line>
        <line class="${classes}" x1="${source.x}" y1="${source.y}" x2="${target.x}" y2="${target.y}"><title>${esc(title)}</title></line>
        <text class="graph-edge-label ${labelClass}" x="${midpointX}" y="${midpointY - 7}">${esc(edge.plain_phrase || titleCase(edge.relation_type))}</text>
      </g></a>`;
    }).join('');

    const nodes = [...ids].map((id) => nodeById.get(id)).filter(Boolean);
    const dense = nodes.length > 48;
    const currentDegree = new Map(nodes.map((node) => [node.id, 0]));
    edges.forEach((edge) => {
      currentDegree.set(edge.source, (currentDegree.get(edge.source) || 0) + 1);
      currentDegree.set(edge.target, (currentDegree.get(edge.target) || 0) + 1);
    });
    const labelBudget = nodes.length > 150 ? 14 : nodes.length > 80 ? 18 : nodes.length > 48 ? 24 : nodes.length;
    const overviewAnchors = new Set([...nodes]
      .sort((a, b) => (currentDegree.get(b.id) || 0) - (currentDegree.get(a.id) || 0) || a.label.localeCompare(b.label))
      .slice(0, labelBudget)
      .map((node) => node.id));

    $('graphNodes').innerHTML = nodes.map((node) => {
      const position = positions.get(node.id);
      const radius = node.id === mapFocus ? 13 : node.publication_level === 'profile' ? 10 : 7;
      const inPath = mapPath.includes(node.id);
      const neighbour = focusNeighbours.has(node.id);
      const labelPriority = node.id === mapFocus || inPath ? 3 : neighbour || overviewAnchors.has(node.id) ? 2 : 1;
      const showLabel = !dense || labelPriority >= 2;
      const contextNode = wideView && node.id !== mapFocus && !neighbour && !inPath;
      const labelAnchor = position.x < 600 ? 'end' : 'start';
      const labelX = position.x + (labelAnchor === 'end' ? -radius - 6 : radius + 6);
      const classes = [
        'graph-node-group',
        node.id === mapFocus ? 'selected' : '',
        inPath ? 'path-node' : '',
        neighbour ? 'focus-neighbour' : '',
        contextNode ? 'context-node' : ''
      ].filter(Boolean).join(' ');
      return `<a class="graph-node-link" href="${internalHref('item', { id: node.id, from: 'map' })}"><g class="${classes}" data-id="${esc(node.id)}" data-label-priority="${labelPriority}" tabindex="0" role="button" aria-label="Open ${esc(node.label)}">
        ${graphNodeMark(node, position, radius)}
        <text class="graph-label ${showLabel ? '' : 'dense-hidden'}" data-priority="${labelPriority}" text-anchor="${labelAnchor}" x="${labelX}" y="${position.y + 4}">${esc(node.label)}</text>
      </g></a>`;
    }).join('');

    $('mapCount').textContent = nodes.length;
    const focusStatus = $('mapFocusStatus');
    if (focusStatus) {
      const depth = $('mapDepth').value;
      focusStatus.textContent = depth === 'all'
        ? `Full overview · ${nodes.length} entries · select a node to open its neighbourhood`
        : depth === 'profiles'
          ? `Developed overview · ${nodes.length} entries · select a node to open its neighbourhood`
          : `Focus: ${nodeById.get(mapFocus)?.label || mapFocus} · ${focusEdges.length} visible connection${focusEdges.length === 1 ? '' : 's'}`;
    }
    renderMapMiniMap(positions, edges);
    applyMapTransform();
    updateMapHistoryButtons();

    $$('.graph-node-group', $('graphNodes')).forEach((group) => {
      const open = (event) => {
        event.preventDefault();
        event.stopPropagation();
        if (mapPointerDragged) return;
        activateMapNode(group.dataset.id);
      };
      group.addEventListener('click', open);
      group.addEventListener('keydown', (event) => {
        if (event.key === 'Enter' || event.key === ' ') {
          event.preventDefault();
          open(event);
        }
      });
    });

    $$('.graph-edge-group', $('graphEdges')).forEach((group) => {
      const open = (event) => {
        event.preventDefault();
        event.stopPropagation();
        if (mapPointerDragged) return;
        mapSelectedEdge = group.dataset.edge;
        inspectEdge(mapSelectedEdge, false);
        renderMap({ fit: false });
      };
      group.addEventListener('click', open);
      group.addEventListener('keydown', (event) => {
        if (event.key === 'Enter' || event.key === ' ') {
          event.preventDefault();
          open(event);
        }
      });
    });

    if (!mapSelectedEdge) inspectNode(mapFocus);
    animateMapTransition(previousPositions, positions);
    if (options.fit) requestAnimationFrame(fitMapToSelection);
    else if (options.focus) requestAnimationFrame(() => moveMapToFocus(mapFocus));
  }

  function semanticZoomBand(scale = mapTransform.scale) {
    if (scale < 0.58) return 'overview';
    if (scale < 1.22) return 'neighbourhood';
    return 'detail';
  }

  function updateMapSemanticZoom() {
    const svg = $('graphSvg');
    if (!svg) return;
    const band = semanticZoomBand();
    svg.classList.remove('map-zoom-overview', 'map-zoom-neighbourhood', 'map-zoom-detail');
    svg.classList.add(`map-zoom-${band}`);
    const label = $('mapScaleMode');
    if (label) {
      const depth = $('mapDepth')?.value;
      label.textContent = depth === 'all' ? 'Full overview' : depth === 'profiles' ? 'Developed overview' : depth === 'constellation' ? 'Constellation' : band === 'overview' ? 'Whole map' : band === 'detail' ? 'Detail' : 'Neighbourhood';
    }
  }

  function renderMapMiniMap(positions, edges) {
    const miniEdges = $('miniEdges');
    const miniNodes = $('miniNodes');
    if (!miniEdges || !miniNodes) return;
    miniEdges.innerHTML = edges.slice(0, 900).map((edge) => {
      const source = positions.get(edge.source);
      const target = positions.get(edge.target);
      if (!source || !target) return '';
      return `<line x1="${source.x}" y1="${source.y}" x2="${target.x}" y2="${target.y}"></line>`;
    }).join('');
    miniNodes.innerHTML = [...positions.entries()].map(([id, position]) =>
      `<circle class="${id === mapFocus ? 'focus' : ''}" cx="${position.x}" cy="${position.y}" r="${id === mapFocus ? 11 : 5}"></circle>`
    ).join('');
    updateMiniViewport();
  }

  function updateMiniViewport() {
    const viewport = $('miniViewport');
    if (!viewport) return;
    const scale = Math.max(mapTransform.scale, 0.001);
    const width = Math.min(1200, 1200 / scale);
    const height = Math.min(760, 760 / scale);
    const rawX = -mapTransform.x / scale;
    const rawY = -mapTransform.y / scale;
    const x = Math.max(0, Math.min(1200 - width, rawX));
    const y = Math.max(0, Math.min(760 - height, rawY));
    viewport.setAttribute('x', String(x));
    viewport.setAttribute('y', String(y));
    viewport.setAttribute('width', String(width));
    viewport.setAttribute('height', String(height));
  }

  function inspectNode(id) {
    const node = nodeById.get(id);
    if (!node) return;
    const family = $('mapFamily')?.value || 'all';
    const allRelations = (edgesByNode.get(id) || [])
      .filter((edge) => edgeInLayer(edge) && (family === 'all' || edge.relation_family === family))
      .sort((a, b) => {
        const aOther = nodeById.get(a.source === id ? a.target : a.source)?.label || '';
        const bOther = nodeById.get(b.source === id ? b.target : b.source)?.label || '';
        return (a.relation_family || '').localeCompare(b.relation_family || '') || aOther.localeCompare(bOther);
      });
    const relations = allRelations.slice(0, 18);
    $('mapInspector').innerHTML = `<p class="eyebrow">${esc(entityLabel(node.entity_type))}</p>
      <h2>${esc(node.label)}</h2>
      <p>${linkifyKnownText(displayDefinition(node), [node.id])}</p>
      <div class="entry-actions"><a href="${internalHref('item', { id: node.id, from: 'map' })}" class="button primary open-card internal-entry-link" data-id="${esc(node.id)}">Open full entry</a></div>
      <h3>Move through ${allRelations.length} visible connection${allRelations.length === 1 ? '' : 's'}</h3>
      <p class="small">Choose either named item to make it the new centre. Choose ‘Inspect this connection’ for wording, status and sources.</p>
      <p class="small relationship-key"><strong>Evidence basis:</strong> badges distinguish sourced assertions, curatorial interpretation and inference. Dashed lines remain provisional.</p>
      ${relations.map((edge) => `<div class="relation-statement">${relationStatement(edge)}<br>${relationshipBasisBadge(edge)}<br><button class="text-button inspect-edge" data-edge="${esc(edge.id)}">Inspect this connection</button></div>`).join('')}
      ${allRelations.length > relations.length ? `<p class="small">Showing the first ${relations.length} connections in the selected layer. Use a narrower layer or the full entry for the rest.</p>` : ''}`;
    bindCards($('mapInspector'));
    $$('.entry-link', $('mapInspector')).forEach((link) => link.addEventListener('click', (event) => { if (!plainLeftClick(event)) return; event.preventDefault(); activateMapNode(link.dataset.id); }));
    $$('.inspect-edge', $('mapInspector')).forEach((button) => button.addEventListener('click', () => inspectEdge(button.dataset.edge, false)));
  }

  function inspectEdge(edgeId, inDrawer) {
    const edge = canonicalEdges.find((candidate) => candidate.id === edgeId);
    if (!edge) return;
    const sources = parse(edge.source_ids, []).map((id) => sourceById.get(id)).filter(Boolean);
    const evidence = parse(edge.evidence_ids, []);
    const relationDefinition = relationByType.get(edge.relation_type);
    const sourceNode = nodeById.get(edge.source);
    const targetNode = nodeById.get(edge.target);
    const direction = String(edge.directed).toLowerCase() === 'true' || edge.directed === true
      ? `Read this from left to right: ${sourceNode?.label || edge.source} ${edge.plain_phrase || edge.relation_type} ${targetNode?.label || edge.target}.`
      : 'This connection is treated as undirected.';
    const basis = relationshipBasis(edge);
    const locator = String(edge.source_locator || '').trim();
    const html = `<p class="eyebrow">Connection</p>
      <h2>${relationStatement(edge)}</h2>
      <p>${esc(edge.scope_conditions || edge.notes || 'No additional scope note has been written.')}</p>
      <div class="badges">
        <span class="badge">${esc(relationFamilyLabel(edge.relation_family))}</span>
        <span class="badge ${['accepted', 'corroborated'].includes(edge.claim_status) ? 'supported' : 'provisional'}">${esc(edge.public_review_label || publicStatusLabel(edge.claim_status))}</span>
        ${relationshipBasisBadge(edge)}
        <span class="badge">Confidence: ${esc(edge.confidence || 'not stated')}</span>
      </div>
      <section class="entry-section">
        <h2>How to read it</h2>
        <p>${esc(direction)}</p>
        <p><strong>Connection type:</strong> ${esc(relationDefinition?.plain_phrase || edge.plain_phrase || titleCase(edge.relation_type))}</p>
        <div class="relation-inspection-basis">
          <p><strong>Evidence basis:</strong> ${esc(basis.label)}. ${esc(basis.description)}</p>
          <p><strong>Stored assertion mode:</strong> ${esc(titleCase(edge.assertion_mode || 'not stated'))}</p>
          <p><strong>Claim-level locator:</strong> ${esc(locator || 'No claim-level locator is recorded.')}</p>
        </div>
      </section>
      <section class="entry-section"><h2>Sources</h2>${sources.map(sourceLink).join('') || '<p>No source linked.</p>'}</section>
      ${evidence.length ? `<section class="entry-section"><h2>Evidence</h2>${evidence.map(evidenceBlock).join('')}</section>` : ''}`;

    if (inDrawer) {
      $('drawerBody').innerHTML = html;
      $('entryDrawer').classList.add('open');
      $('drawerScrim').classList.add('open');
      $('entryDrawer').setAttribute('aria-hidden', 'false');
      $$('.entry-link', $('drawerBody')).forEach((link) => link.addEventListener('click', (event) => { if (!plainLeftClick(event)) return; event.preventDefault(); renderEntry(link.dataset.id); }));
    } else {
      $('mapInspector').innerHTML = html;
      $$('.entry-link', $('mapInspector')).forEach((link) => link.addEventListener('click', (event) => { if (!plainLeftClick(event)) return; event.preventDefault(); activateMapNode(link.dataset.id); }));
    }
  }

  function applyMapTransform() {
    $('graphRoot').setAttribute('transform', `translate(${mapTransform.x} ${mapTransform.y}) scale(${mapTransform.scale})`);
    const percentage = Math.round(mapTransform.scale * 100);
    const status = $('mapZoomStatus');
    if (status) status.textContent = `${percentage}%`;
    const range = $('mapZoomRange');
    if (range && document.activeElement !== range) range.value = String(Math.max(22, Math.min(400, percentage)));
    updateMapSemanticZoom();
    updateMiniViewport();
  }

  function resetMapTransform() {
    mapTransform = { x: 0, y: 0, scale: 1 };
    applyMapTransform();
  }

  function fitMapToSelection() {
    const positions = [...lastMapPositions.values()];
    if (!positions.length) {
      resetMapTransform();
      return;
    }
    const minX = Math.min(...positions.map((position) => position.x));
    const maxX = Math.max(...positions.map((position) => position.x));
    const minY = Math.min(...positions.map((position) => position.y));
    const maxY = Math.max(...positions.map((position) => position.y));
    const width = Math.max(maxX - minX, 120);
    const height = Math.max(maxY - minY, 100);
    const scale = Math.max(0.3, Math.min(2.2, Math.min(1040 / (width + 130), 620 / (height + 130))));
    const centreX = (minX + maxX) / 2;
    const centreY = (minY + maxY) / 2;
    mapTransform = {
      scale,
      x: 600 - centreX * scale,
      y: 380 - centreY * scale
    };
    applyMapTransform();
  }

  function shortestPath(from, to) {
    const start = canonicalId(from);
    const goal = canonicalId(to);
    if (!nodeById.has(start) || !nodeById.has(goal)) return [];
    const queue = [start];
    const previous = new Map([[start, null]]);
    while (queue.length) {
      const id = queue.shift();
      if (id === goal) break;
      for (const edge of (edgesByNode.get(id) || [])) {
        if (!edgeInLayer(edge)) continue;
        if ($('mapFamily').value !== 'all' && edge.relation_family !== $('mapFamily').value) continue;
        const other = edge.source === id ? edge.target : edge.source;
        const otherNode = nodeById.get(other);
        if (!otherNode || otherNode.public_visibility !== 'public' || previous.has(other)) continue;
        previous.set(other, id);
        queue.push(other);
      }
    }
    if (!previous.has(goal)) return [];
    const path = [];
    let current = goal;
    while (current) {
      path.push(current);
      current = previous.get(current);
    }
    return path.reverse();
  }

  function extractQuestionMatches(question, limit = 6) {
    const normalizedQuestion = normalise(question);
    const words = normalizedQuestion.split(' ').filter((word) => word && !QUESTION_STOPWORDS.has(word));
    const scores = new Map();

    for (const record of searchRecords) {
      const terms = unique([record.normLabel, ...record.normAliases]).filter((term) => term.length >= 3);
      for (const term of terms) {
        const paddedQuestion = ` ${normalizedQuestion} `;
        if (paddedQuestion.includes(` ${term} `)) {
          scores.set(record.node.id, Math.max(scores.get(record.node.id) || 0, 1250 + term.length));
        }
      }
    }

    const maxN = Math.min(5, words.length);
    for (let size = maxN; size >= 1; size -= 1) {
      for (let start = 0; start <= words.length - size; start += 1) {
        const phrase = words.slice(start, start + size).join(' ');
        if (phrase.length < 3) continue;
        for (const match of searchNodes(phrase, 3, { level: 'all' })) {
          const weighted = match.score + size * 85;
          scores.set(match.node.id, Math.max(scores.get(match.node.id) || 0, weighted));
        }
      }
    }

    if (!scores.size) {
      searchNodes(question, limit, { level: 'all' }).forEach((match) => scores.set(match.node.id, match.score));
    }

    return [...scores.entries()]
      .map(([id, score]) => ({ node: nodeById.get(id), score }))
      .filter((match) => match.node)
      .sort((a, b) => b.score - a.score || rankNode(a.node) - rankNode(b.node) || a.node.label.localeCompare(b.node.label))
      .slice(0, limit);
  }

  function relevantClaims(question, matches, limit = 4) {
    const normalizedQuestion = normalise(question);
    const terms = normalizedQuestion.split(' ').filter((word) => word.length >= 4 && !QUESTION_STOPWORDS.has(word));
    const matchedIds = new Set(matches.map((match) => match.node.id));
    return (DATA.claims || [])
      .map((claim) => {
        const subject = canonicalId(claim.subject_id);
        const object = canonicalId(claim.object_id);
        const normalizedStatement = normalise(claim.statement);
        let score = 0;
        if (matchedIds.has(subject)) score += 250;
        if (matchedIds.has(object)) score += 250;
        score += terms.filter((term) => normalizedStatement.includes(term)).length * 60;
        return { claim, score };
      })
      .filter((item) => item.score > 0)
      .sort((a, b) => b.score - a.score)
      .slice(0, limit)
      .map((item) => item.claim);
  }

  function askContext(question, matches, path, claims) {
    const lines = [
      `Question: ${question}`,
      '',
      'Use the following public material from The Necessary Tangle as starting evidence. Distinguish sourced statements, interpretation and uncertainty.'
    ];
    matches.forEach(({ node }) => {
      lines.push('', `## ${node.label}`, displayDefinition(node));
      const sourceIds = unique([
        ...parse(node.source_ids, []),
        ...parse(profileById.get(node.id)?.source_ids, [])
      ]);
      sourceIds.slice(0, 6).forEach((sourceId) => {
        const source = sourceById.get(sourceId);
        if (source) lines.push(`Source: ${source.title} — ${source.url || 'No public link'}`);
      });
    });
    if (claims.length) {
      lines.push('', '## Relevant statements recorded in the atlas');
      claims.forEach((claim) => lines.push(`- ${claim.statement} [${publicStatusLabel(claim.status)}]`));
    }
    if (path.length > 1) {
      lines.push('', `Relevant path: ${path.map((id) => nodeById.get(id)?.label || id).join(' -> ')}`);
    }
    lines.push(
      '',
      'Please cite listed public sources where relevant. Say when the atlas is incomplete, provisional or disputed. Do not infer mentorship, influence or priority from resemblance alone.'
    );
    return lines.join('\n');
  }

  function renderAsk(question) {
    const matches = extractQuestionMatches(question, 6);
    const claims = relevantClaims(question, matches, 4);
    const path = matches.length >= 2 ? shortestPath(matches[0].node.id, matches[1].node.id) : [];
    const preparedContext = askContext(question, matches, path, claims);
    $('askResults').innerHTML = `<section class="ask-context">
      <p class="eyebrow">Matched entries</p>
      <h2>${matches.length ? `The atlas found ${matches.length} likely starting point${matches.length === 1 ? '' : 's'}` : 'No strong match yet'}</h2>
      ${matches.length ? `<div class="card-grid three">${matches.map((match) => card(match.node)).join('')}</div>` : '<p>Try a shorter question or name one concept, person or method.</p>'}
      ${claims.length ? `<section class="entry-section"><h2>Relevant statements in the atlas</h2>${claims.map((claim) => `<div class="claim-card"><p>${linkifyKnownText(claim.statement)}</p><span class="badge">${esc(publicStatusLabel(claim.status))}</span></div>`).join('')}</section>` : ''}
      ${path.length > 1 ? `<section class="entry-section"><h2>A possible connection path</h2><div class="path-step">${path.map((id, index) => `${index ? '<span>→</span>' : ''}<a href="${internalHref('item', { id: id, from: baseView })}" class="chip open-card internal-entry-link" data-id="${esc(id)}">${esc(nodeById.get(id)?.label || id)}</a>`).join('')}</div></section>` : ''}
      <div class="context-actions">
        <button id="copyAskContext" class="primary">Copy atlas context</button>
        <a class="button" href="${esc(CONFIG.discussionsUrl || `${CONFIG.repositoryUrl}/discussions`)}" target="_blank" rel="noopener">Discuss the question</a>
      </div>
      <p class="small">The site does not send your question anywhere. You may copy the prepared public context or open a public discussion.</p>
    </section>`;
    bindCards($('askResults'));
    $$('.entry-link', $('askResults')).forEach((button) => button.addEventListener('click', () => renderEntry(button.dataset.id)));

    const copy = async (button) => {
      try {
        await navigator.clipboard.writeText(preparedContext);
        button.textContent = 'Copied';
        return true;
      } catch (_) {
        window.prompt('Copy this context', preparedContext);
        return false;
      }
    };
    $('copyAskContext').addEventListener('click', () => copy($('copyAskContext')));
  }

  function updateContributionHint() {
    const input = $('contributionItem');
    const query = input.value.trim();
    const selected = input.dataset.selectedId;
    if (selected && nodeById.has(selected)) {
      $('duplicateHint').textContent = `Maintained entry selected: ${nodeById.get(selected).label}`;
      $('contributionItemId').value = selected;
      return;
    }
    $('contributionItemId').value = '';
    if (!query) {
      $('duplicateHint').textContent = 'Choose an existing entry where possible. This prevents accidental duplicates.';
      return;
    }
    const matches = searchNodes(query, 3, { level: 'all' });
    $('duplicateHint').innerHTML = matches.length
      ? `Possible existing entries: ${matches.map((match) => `<button type="button" class="text-button duplicate-choice" data-id="${esc(match.node.id)}">${esc(match.node.label)}</button>`).join(' · ')}`
      : 'No close entry found. You may be proposing something new.';
    $$('.duplicate-choice', $('duplicateHint')).forEach((button) => button.addEventListener('click', () => {
      const node = nodeById.get(button.dataset.id);
      input.value = node.label;
      input.dataset.selectedId = node.id;
      $('contributionItemId').value = node.id;
      updateContributionHint();
    }));
  }

  function issueUrlFromForm(form) {
    const values = Object.fromEntries(new FormData(form).entries());
    const type = values.submission_type || 'Contribution';
    const entry = values.entry_label || 'General';
    const statement = values.statement || '';
    const title = `[${type}] ${entry}${statement ? ` — ${statement.slice(0, 72)}` : ''}`;
    const entryId = values.entry_id || '';
    const entryUrl = entryId
      ? `${DATA.meta.project_url || location.origin + location.pathname}#${new URLSearchParams({ view: 'item', id: entryId, from: 'browse' }).toString()}`
      : '';
    const body = [
      '## Type',
      type,
      '',
      '## Entry',
      entryId ? `${entry} (${entryId})` : entry || 'Not tied to an existing entry',
      entryUrl ? `Public entry: ${entryUrl}` : '',
      '',
      '## Proposed change, challenge or question',
      statement,
      '',
      '## Why this matters',
      values.reason || 'Not supplied.',
      '',
      '## Source',
      values.source_url || values.source_citation || 'No source supplied.',
      '',
      '## Exact evidence or locator',
      values.evidence || 'Not supplied.',
      '',
      '## Contributor',
      values.name || 'GitHub account shown on the issue.',
      '',
      '## Intake marker',
      'site-submission',
      '',
      '---',
      `Prepared from The Necessary Tangle ${DATA.meta.release}. The contributor reviewed this text before submitting it.`
    ].filter((line) => line !== '').join('\n');
    const repository = CONFIG.repositoryUrl || DATA.meta.repository_url;
    const labels = 'site-submission,awaiting-curator-review';
    return `${repository}/issues/new?${new URLSearchParams({ title, body, labels }).toString()}`;
  }

  function initSmartSearch(container) {
    const input = container.querySelector('input:not([type="hidden"])');
    const list = container.querySelector('.suggestions');
    const role = container.dataset.searchRole;
    let active = -1;
    let current = [];

    function hide() {
      list.hidden = true;
      active = -1;
    }

    function choose(node) {
      input.value = node.label;
      input.dataset.selectedId = node.id;
      hide();
      if (role === 'open') { setHash({ view: 'item', id: node.id, from: baseView }); renderEntry(node.id); }
      if (role === 'filter') renderBrowse();
      if (role === 'map') {
        $('mapDepth').value = '1';
        activateMapNode(node.id);
      }
      if (role === 'contribution') {
        $('contributionItemId').value = node.id;
        updateContributionHint();
      }
    }

    function render() {
      const query = input.value.trim();
      current = searchNodes(query, 8, { level: 'all' });
      if (!query || !current.length) {
        hide();
        if (role === 'contribution') updateContributionHint();
        return;
      }
      list.innerHTML = current.map((result, index) => `<a href="${internalHref('item', { id: result.node.id, from: role === 'map' ? 'map' : baseView })}" class="suggestion ${index === active ? 'active' : ''}" role="option" data-id="${esc(result.node.id)}">
        <span><strong>${esc(result.node.label)}</strong><small>${esc(entityLabel(result.node.entity_type))}${result.aliases.some((alias) => normalise(alias) === normalise(query)) ? ' · alias match' : ''}</small></span>
        <span class="badge ${result.node.publication_level === 'research_stub' ? 'status-stub' : result.node.publication_level === 'profile' ? 'status-profile' : ''}">${esc(statusLabel(result.node))}</span>
      </a>`).join('');
      list.hidden = false;
      $$('.suggestion', list).forEach((button) => button.addEventListener('mousedown', (event) => {
        if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
        event.preventDefault();
        choose(nodeById.get(button.dataset.id));
      }));
      if (role === 'contribution') updateContributionHint();
    }

    input.addEventListener('input', () => {
      input.dataset.selectedId = '';
      active = -1;
      render();
    });
    input.addEventListener('focus', render);
    input.addEventListener('keydown', (event) => {
      if (list.hidden && event.key === 'ArrowDown') {
        render();
        return;
      }
      if (event.key === 'ArrowDown') {
        event.preventDefault();
        active = Math.min(current.length - 1, active + 1);
        render();
      } else if (event.key === 'ArrowUp') {
        event.preventDefault();
        active = Math.max(0, active - 1);
        render();
      } else if (event.key === 'Enter' && current.length) {
        event.preventDefault();
        choose(current[Math.max(0, active)].node);
      } else if (event.key === 'Escape') {
        hide();
      }
    });
    document.addEventListener('click', (event) => {
      if (!container.contains(event.target)) hide();
    });
    const openButton = container.querySelector('.search-open');
    if (openButton) {
      openButton.addEventListener('click', () => {
        const node = nodeById.get(input.dataset.selectedId) || bestNode(input.value);
        if (node) choose(node);
      });
    }
  }

  function initMapInteraction() {
    const svg = $('graphSvg');
    const wrap = svg.parentElement;
    let dragging = false;
    let last = { x: 0, y: 0 };

    function zoomAt(factor, clientX = null, clientY = null) {
      const rect = svg.getBoundingClientRect();
      const screenX = clientX === null ? 600 : (clientX - rect.left) * 1200 / Math.max(rect.width, 1);
      const screenY = clientY === null ? 380 : (clientY - rect.top) * 760 / Math.max(rect.height, 1);
      const worldX = (screenX - mapTransform.x) / mapTransform.scale;
      const worldY = (screenY - mapTransform.y) / mapTransform.scale;
      const nextScale = Math.min(4, Math.max(0.22, mapTransform.scale * factor));
      mapTransform = {
        scale: nextScale,
        x: screenX - worldX * nextScale,
        y: screenY - worldY * nextScale
      };
      applyMapTransform();
    }

    svg.addEventListener('wheel', (event) => {
      event.preventDefault();
      zoomAt(event.deltaY < 0 ? 1.12 : 0.89, event.clientX, event.clientY);
    }, { passive: false });
    $('mapZoomIn')?.addEventListener('click', () => zoomAt(1.16));
    $('mapZoomOut')?.addEventListener('click', () => zoomAt(1 / 1.16));
    $('mapZoomRange')?.addEventListener('input', (event) => {
      const targetScale = Number(event.target.value) / 100;
      zoomAt(targetScale / Math.max(mapTransform.scale, 0.001));
    });
    svg.addEventListener('dblclick', (event) => {
      if (event.target.closest?.('.graph-node-group, .graph-edge-group')) return;
      event.preventDefault();
      zoomAt(event.shiftKey ? 1 / 1.55 : 1.55, event.clientX, event.clientY);
    });

    let dragStart = { x: 0, y: 0 };
    svg.addEventListener('pointerdown', (event) => {
      if (event.button !== 0) return;
      dragging = true;
      mapPointerDragged = false;
      dragStart = { x: event.clientX, y: event.clientY };
      last = { x: event.clientX, y: event.clientY };
      wrap.classList.add('dragging');
      svg.setPointerCapture(event.pointerId);
    });
    svg.addEventListener('pointermove', (event) => {
      if (!dragging) return;
      const total = Math.hypot(event.clientX - dragStart.x, event.clientY - dragStart.y);
      if (total > 4) mapPointerDragged = true;
      if (!mapPointerDragged) return;
      mapTransform.x += event.clientX - last.x;
      mapTransform.y += event.clientY - last.y;
      last = { x: event.clientX, y: event.clientY };
      applyMapTransform();
    });
    const finishMapPointer = (event) => {
      if (!dragging) return;
      dragging = false;
      wrap.classList.remove('dragging');
      try { svg.releasePointerCapture(event.pointerId); } catch (_) { /* no-op */ }
      if (mapPointerDragged) setTimeout(() => { mapPointerDragged = false; }, 0);
    };
    svg.addEventListener('pointerup', finishMapPointer);
    svg.addEventListener('pointercancel', finishMapPointer);

    const mini = $('mapMiniMap');
    let miniDragging = false;
    const centreFromMini = (event) => {
      if (!mini) return;
      const rect = mini.getBoundingClientRect();
      const worldX = (event.clientX - rect.left) * 1200 / Math.max(rect.width, 1);
      const worldY = (event.clientY - rect.top) * 760 / Math.max(rect.height, 1);
      mapTransform.x = 600 - worldX * mapTransform.scale;
      mapTransform.y = 380 - worldY * mapTransform.scale;
      applyMapTransform();
    };
    mini?.addEventListener('pointerdown', (event) => {
      miniDragging = true;
      mini.setPointerCapture(event.pointerId);
      centreFromMini(event);
    });
    mini?.addEventListener('pointermove', (event) => {
      if (miniDragging) centreFromMini(event);
    });
    mini?.addEventListener('pointerup', (event) => {
      miniDragging = false;
      try { mini.releasePointerCapture(event.pointerId); } catch (_) { /* no-op */ }
    });

    $('mapBack')?.addEventListener('click', () => navigateMapHistory(-1));
    $('mapForward')?.addEventListener('click', () => navigateMapHistory(1));
    $('mapFullscreen')?.addEventListener('click', async () => {
      try {
        if (document.fullscreenElement === wrap) await document.exitFullscreen();
        else await wrap.requestFullscreen();
      } catch (_) { /* Fullscreen may be blocked by the browser. */ }
    });
    document.addEventListener('fullscreenchange', () => {
      const button = $('mapFullscreen');
      if (!button) return;
      const active = document.fullscreenElement === wrap;
      button.textContent = active ? 'Exit full screen' : 'Full screen';
      button.setAttribute('aria-label', active ? 'Exit map full screen' : 'Open map full screen');
      requestAnimationFrame(() => {
        applyMapTransform();
        updateMiniViewport();
      });
    });

    wrap.addEventListener('keydown', (event) => {
      if (event.target.matches?.('input, select, textarea, button')) return;
      if (event.key === '+' || event.key === '=') { event.preventDefault(); zoomAt(1.16); }
      else if (event.key === '-' || event.key === '_') { event.preventDefault(); zoomAt(1 / 1.16); }
      else if (event.key === '0') { event.preventDefault(); resetMapTransform(); }
      else if (event.key.toLowerCase() === 'f') { event.preventDefault(); fitMapToSelection(); }
      else if (event.key === 'ArrowLeft') { event.preventDefault(); mapTransform.x += 45; applyMapTransform(); }
      else if (event.key === 'ArrowRight') { event.preventDefault(); mapTransform.x -= 45; applyMapTransform(); }
      else if (event.key === 'ArrowUp') { event.preventDefault(); mapTransform.y += 45; applyMapTransform(); }
      else if (event.key === 'ArrowDown') { event.preventDefault(); mapTransform.y -= 45; applyMapTransform(); }
    });

    $('mapFit').addEventListener('click', fitMapToSelection);
    $('mapReset').addEventListener('click', () => {
      mapFocus = 'concept_viability';
      mapFocusHistory = [mapFocus];
      mapFocusHistoryIndex = 0;
      updateMapHistoryButtons();
      mapPath = [];
      mapSelectedEdge = null;
      $('mapSearch').value = 'Viability';
      $('mapDepth').value = 'all';
      $('mapLayer').value = 'substantive';
      $('mapFamily').value = 'all';
      updateMapLayerNote();
      $('mapIncludeStubs').checked = false;
      resetMapTransform();
      renderMap({ fit: true });
    });
    ['mapDepth', 'mapLayer', 'mapFamily', 'mapIncludeStubs'].forEach((id) => $(id).addEventListener('change', () => {
      if (id !== 'mapDepth' || $('mapDepth').value !== 'path') mapPath = [];
      mapSelectedEdge = null;
      if (id === 'mapLayer') updateMapLayerNote();
      renderMap({ fit: true });
    }));

    $('findPath').addEventListener('click', () => {
      const from = nodeById.get($('pathFrom').dataset.selectedId) || bestNode($('pathFrom').value);
      const to = nodeById.get($('pathTo').dataset.selectedId) || bestNode($('pathTo').value);
      if (!from || !to) {
        $('pathResult').textContent = 'Choose two entries.';
        return;
      }
      mapPath = shortestPath(from.id, to.id);
      if (!mapPath.length) {
        $('pathResult').textContent = 'No path was found in the current public evidence graph.';
        return;
      }
      $('pathResult').innerHTML = mapPath.map((id, index) => `${index ? '<span>→</span>' : ''}<a href="${internalHref('item', { id, from: 'map' })}" class="chip path-chip internal-entry-link" data-id="${esc(id)}">${esc(nodeById.get(id)?.label || id)}</a>`).join(' ');
      $$('.path-chip', $('pathResult')).forEach((button) => button.addEventListener('click', (event) => { if (!plainLeftClick(event)) return; event.preventDefault(); renderEntry(button.dataset.id); }));
      $('mapDepth').value = 'path';
      mapFocus = from.id;
      mapSelectedEdge = null;
      if (id === 'mapLayer') updateMapLayerNote();
      renderMap({ fit: true });
    });
  }

  function init() {
    renderHome();
    populateFilters();
    renderBrowse();
    renderJourneys();

    $$('.main-nav [data-view]').forEach((link) => link.addEventListener('click', (event) => followInternalAnchor(event, link)));
    $$('[data-view-link]').forEach((link) => link.addEventListener('click', (event) => followInternalAnchor(event, link)));
    $$('.smart-search').forEach(initSmartSearch);
    $('browseSearch').addEventListener('input', renderBrowse);
    ['browseType', 'browseTag', 'browseLevel', 'browseConnectionDepth'].forEach((id) => $(id).addEventListener('change', renderBrowse));
    $('clearBrowse').addEventListener('click', () => {
      $('browseSearch').value = '';
      $('browseType').value = 'all';
      $('browseTag').value = 'all';
      $('browseLevel').value = 'developed';
      $('browseConnectionDepth').value = 'all';
      renderBrowse();
    });

    $('drawerClose').addEventListener('click', () => closeDrawer());
    $('drawerScrim').addEventListener('click', () => closeDrawer());
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape') closeDrawer();
    });

    $('askForm').addEventListener('submit', (event) => {
      event.preventDefault();
      const question = $('askQuestion').value.trim();
      if (question) renderAsk(question);
    });

    $('contributionItem').addEventListener('blur', updateContributionHint);
    updateContributionHint();
    $('contributionForm').addEventListener('submit', (event) => {
      event.preventDefault();
      const url = issueUrlFromForm(event.currentTarget);
      $('formStatus').textContent = 'A labelled GitHub issue has opened in a new tab. Review the wording there, then submit it for curator review.';
      window.open(url, '_blank', 'noopener');
    });

    initMapInteraction();
    window.addEventListener('hashchange', route);
    route();
  }

  document.addEventListener('DOMContentLoaded', init);
})();
/* 0.7 constellation controls: provisional neighbourhoods, zoom and participation. */
(() => {
  const emergentCategories = () => window.TANGLE_DATA?.emergent_categories || [];
  function categoryMembers(category) {
    return new Set(category?.member_node_ids || category?.members || []);
  }

  function applyCategory(categoryId) {
    const category = emergentCategories().find((item) => (item.id || item.category_id) === categoryId);
    const members = categoryMembers(category);
    const svg = document.getElementById('graphSvg');
    if (svg) {
      svg.querySelectorAll('[data-node-id], [data-id]').forEach((node) => {
        const id = node.dataset.nodeId || node.dataset.id;
        node.classList.toggle('category-halo', Boolean(category && members.has(id)));
        node.classList.toggle('category-muted', Boolean(category && !members.has(id)));
      });
    }
    const note = document.getElementById('mapCategoryNote');
    if (note) note.textContent = category
      ? `${category.label || category.name || 'Selected neighbourhood'} — provisional graph grouping; inspect the typed lines rather than treating it as a canon.`
      : 'Neighbourhoods are provisional graph groupings, not canonical schools or categories.';
  }

  function initConstellationControls() {
    const select = document.getElementById('mapCategory');
    if (select && !select.dataset.ready) {
      emergentCategories().forEach((category) => {
        const option = document.createElement('option');
        option.value = category.id || category.category_id || '';
        option.textContent = category.label || category.name || option.value;
        select.append(option);
      });
      select.addEventListener('change', () => applyCategory(select.value));
      select.dataset.ready = 'true';
    }

    // Zoom buttons and wheel behaviour are handled by the graph-root transform in initMapInteraction.
    const svg = document.getElementById('graphSvg');

    document.getElementById('mapShowLabels')?.addEventListener('change', (event) => {
      document.getElementById('graphSvg')?.classList.toggle('hide-map-labels', !event.target.checked);
    });

    const membershipForm = document.getElementById('membershipForm');
    membershipForm?.addEventListener('submit', (event) => {
      event.preventDefault();
      const form = new FormData(membershipForm);
      const role = String(form.get('role') || 'participant').replaceAll('_', ' ');
      const interest = String(form.get('interest') || '').trim();
      const status = document.getElementById('membershipStatus');
      if (status) status.innerHTML = `Contribution note ready: <strong>${role}</strong>${interest ? ` — ${interest}` : ''}. Continue through <a href="https://github.com/antlerboy/the-necessary-tangle/issues/new?template=membership.yml" target="_blank" rel="noopener">the structured participation form</a>. If automation helped, name the human sponsor.`;
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initConstellationControls);
  else initConstellationControls();
})();



/* 0.18 navigable map and link contract */
