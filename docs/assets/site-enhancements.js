(() => {
  'use strict';

  const interactiveSelector = "a, button, input, select, textarea, summary, [role='button']";
  const actionSelector = '.open-card, .open-journey, [data-view-link], a[href]';
  const RULES_COMMENT_API = 'https://api.github.com/repos/antlerboy/the-necessary-tangle/issues/comments/5465271322';
  const RULES_CACHE_KEY = 'necessary-tangle:little-rq-rules:v1';
  const RULES_CACHE_MAX_AGE = 7 * 24 * 60 * 60 * 1000;
  const RULES_PAGE = '/little-redquadrant-rules/';
  const MARK_MANIFEST_URL = 'assets/living-marks/manifest.json?v=0.20.3-reader-scio';

  const relationFamilyLabels = {
    conceptual: 'Ideas and dependencies',
    historical: 'History and sequence',
    influence: 'Influence and lineage',
    practice: 'Practice and application',
    contestation: 'Confusion and disagreement',
    human: 'Human transmission',
    identity: 'Identity and affiliation',
    documentary: 'Works, authorship and presentation',
    classification: 'Collection structure',
    evidence: 'Evidence registration',
    legacy: 'Legacy and unresolved'
  };

  function esc(value) {
    return String(value ?? '').replace(/[&<>'"]/g, (ch) => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;'
    }[ch]));
  }

  function parseList(value) {
    if (Array.isArray(value)) return value;
    if (!value) return [];
    try {
      const parsed = JSON.parse(value);
      return Array.isArray(parsed) ? parsed : [];
    } catch (_) {
      return [];
    }
  }

  function randomIndex(length) {
    if (length <= 1) return 0;
    if (window.crypto && window.crypto.getRandomValues) {
      const value = new Uint32Array(1);
      window.crypto.getRandomValues(value);
      return value[0] % length;
    }
    return Math.floor(Math.random() * length);
  }

  function markClickableCards(root = document) {
    root.querySelectorAll?.('.card').forEach((card) => {
      if (card.querySelector(actionSelector)) card.classList.add('is-clickable');
    });
  }

  function refinePublicLanguage(root = document) {
    root.querySelectorAll?.('h2').forEach((heading) => {
      if (heading.textContent.trim() === 'Claims and disputes') {
        heading.textContent = 'Statements and disputes';
      }
    });
  }

  function refine(root = document) {
    markClickableCards(root);
    refinePublicLanguage(root);
  }

  function installStyles() {
    if (document.getElementById('iteration-203-enhancement-styles')) return;
    const style = document.createElement('style');
    style.id = 'iteration-203-enhancement-styles';
    style.textContent = `
      .little-rq-rule { grid-column: 1 / -1; display: flex; align-items: baseline; gap: .55rem; min-width: 0; margin-top: .15rem; font-size: .78rem; line-height: 1.35; color: var(--muted, #665f57); }
      .little-rq-rule button, .little-rq-rule a { font: inherit; }
      .little-rq-rule .rule-randomise { appearance: none; border: 0; background: transparent; color: inherit; padding: 0; text-align: left; cursor: pointer; min-width: 0; }
      .little-rq-rule .rule-randomise:hover, .little-rq-rule .rule-randomise:focus-visible { text-decoration: underline; text-underline-offset: .18em; }
      .little-rq-rule .rule-all { white-space: nowrap; opacity: .76; }
      .tangle-mark[data-living-mark] { cursor: pointer; }
      .tangle-mark[data-living-mark]:focus-visible { outline: 2px solid currentColor; outline-offset: 4px; border-radius: .3rem; }
      .tangle-mark[data-living-mark]:fullscreen { display: grid; place-items: center; width: 100vw; height: 100vh; padding: min(8vw, 5rem); background: #f2eadc; }
      .tangle-mark[data-living-mark]:fullscreen > img, .tangle-mark[data-living-mark]:fullscreen > video, .tangle-mark[data-living-mark]:fullscreen > svg { width: min(90vw, 1200px); height: min(90vh, 900px); max-width: none; max-height: none; object-fit: contain; }
      .map-card-toggle[aria-pressed='true'] { box-shadow: inset 0 0 0 2px currentColor; }
      #mapCardView { display: none; overflow: auto; padding: 1.15rem; height: min(72vh, 760px); background: var(--paper, #f7f1e6); }
      #graphWrap.map-card-mode #graphSvg, #graphWrap.map-card-mode .map-minimap-shell, #graphWrap.map-card-mode .map-canvas-help { display: none !important; }
      #graphWrap.map-card-mode #mapCardView { display: block; }
      .map-card-focus { max-width: 82ch; margin: 0 auto 1.2rem; padding: 1rem 1.1rem; border: 1px solid color-mix(in srgb, currentColor 18%, transparent); border-radius: .45rem; background: color-mix(in srgb, var(--paper, #fff) 92%, currentColor 8%); }
      .map-card-focus h2 { margin: .15rem 0 .35rem; }
      .map-card-groups { display: grid; gap: 1rem; max-width: 1000px; margin: 0 auto; }
      .map-card-family { border-top: 2px solid color-mix(in srgb, currentColor 24%, transparent); padding-top: .7rem; }
      .map-card-family h3 { margin: 0 0 .55rem; font-size: 1rem; }
      .map-card-relations { display: grid; gap: .55rem; }
      .map-card-relation { display: grid; grid-template-columns: minmax(10rem, 1fr) minmax(9rem, auto); gap: .6rem 1rem; align-items: start; padding: .7rem .8rem; border: 1px solid color-mix(in srgb, currentColor 14%, transparent); border-radius: .35rem; background: color-mix(in srgb, var(--paper, #fff) 96%, currentColor 4%); }
      .map-card-relation p { margin: 0; }
      .map-card-relation .map-card-meta { font-size: .76rem; opacity: .72; text-align: right; }
      .map-card-empty { max-width: 70ch; margin: 2rem auto; }
      @media (max-width: 760px) {
        .little-rq-rule { display: block; }
        .little-rq-rule .rule-all { margin-left: .35rem; }
        .map-card-relation { grid-template-columns: 1fr; }
        .map-card-relation .map-card-meta { text-align: left; }
      }
    `;
    document.head.appendChild(style);
  }

  function parseRulesBody(body) {
    const matches = [...String(body || '').matchAll(/^\s*(\d{1,3})\.\s*\t?(.+?)\s*$/gm)];
    return matches
      .map((match) => ({ number: Number(match[1]), text: match[2].trim() }))
      .filter((rule) => rule.number >= 1 && rule.number <= 256 && rule.text);
  }

  function readRulesCache() {
    try {
      const cached = JSON.parse(localStorage.getItem(RULES_CACHE_KEY) || 'null');
      if (!cached || !Array.isArray(cached.rules) || cached.rules.length !== 256) return null;
      if (Date.now() - Number(cached.savedAt || 0) > RULES_CACHE_MAX_AGE) return null;
      return cached.rules;
    } catch (_) {
      return null;
    }
  }

  function writeRulesCache(rules) {
    try {
      localStorage.setItem(RULES_CACHE_KEY, JSON.stringify({ savedAt: Date.now(), rules }));
    } catch (_) { /* caching is optional */ }
  }

  async function loadRules() {
    const cached = readRulesCache();
    if (cached) return cached;
    const response = await fetch(RULES_COMMENT_API, {
      headers: { Accept: 'application/vnd.github+json' },
      cache: 'no-cache'
    });
    if (!response.ok) throw new Error(`Rules source returned ${response.status}`);
    const payload = await response.json();
    const rules = parseRulesBody(payload.body);
    if (rules.length !== 256) throw new Error(`Expected 256 rules, found ${rules.length}`);
    writeRulesCache(rules);
    return rules;
  }

  function setupLittleRules() {
    const header = document.querySelector('.site-header');
    if (!header || document.getElementById('littleRqRule')) return;
    const shell = document.createElement('div');
    shell.id = 'littleRqRule';
    shell.className = 'little-rq-rule';
    shell.innerHTML = `<button type="button" class="rule-randomise" title="Show another little RedQuadrant rule">little RedQuadrant rule: loading…</button><a class="rule-all" href="${RULES_PAGE}">all 256</a>`;
    header.appendChild(shell);
    const button = shell.querySelector('.rule-randomise');
    let rules = [];
    let currentNumber = null;

    const show = () => {
      if (!rules.length) return;
      const candidates = rules.length > 1 ? rules.filter((rule) => rule.number !== currentNumber) : rules;
      const rule = candidates[randomIndex(candidates.length)] || rules[0];
      currentNumber = rule.number;
      button.textContent = `little RedQuadrant rule #${rule.number}: ${rule.text}`;
    };

    button.addEventListener('click', show);
    loadRules().then((loaded) => {
      rules = loaded;
      show();
    }).catch(() => {
      button.textContent = 'little RedQuadrant rules';
      button.disabled = true;
      shell.querySelector('.rule-all').textContent = 'view the source';
      shell.querySelector('.rule-all').href = 'https://github.com/antlerboy/the-necessary-tangle/issues/2#issuecomment-5465271322';
      shell.querySelector('.rule-all').target = '_blank';
      shell.querySelector('.rule-all').rel = 'noopener';
    });
  }

  function setupLivingMarkControls() {
    const host = document.querySelector('[data-living-mark]');
    if (!host || host.dataset.enhanced203 === 'true') return;
    host.dataset.enhanced203 = 'true';
    host.removeAttribute('aria-hidden');
    host.setAttribute('role', 'button');
    host.setAttribute('tabindex', '0');
    host.setAttribute('aria-label', 'Change living mark. Double-click for full screen.');
    host.title = 'Click for another living mark; double-click for full screen';
    const reducedMotion = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;
    let manifestPromise = null;
    let clickTimer = null;

    const loadManifest = () => {
      if (!manifestPromise) {
        manifestPromise = fetch(MARK_MANIFEST_URL, { cache: 'no-cache', credentials: 'same-origin' })
          .then((response) => {
            if (!response.ok) throw new Error(`Living-mark manifest returned ${response.status}`);
            return response.json();
          })
          .then((manifest) => (Array.isArray(manifest.marks) ? manifest.marks : [])
            .filter((mark) => mark && mark.id && mark.src && ['image', 'video'].includes(mark.kind)));
      }
      return manifestPromise;
    };

    const imageFor = (mark, src) => {
      const image = document.createElement('img');
      image.src = src;
      image.alt = '';
      image.decoding = 'async';
      image.setAttribute('aria-hidden', 'true');
      image.addEventListener('load', () => host.replaceChildren(image), { once: true });
      return image;
    };

    const showMark = (mark) => {
      if (!mark) return;
      host.dataset.markId = mark.id;
      host.dataset.markBackground = mark.background || 'light';
      host.title = `Living mark: ${mark.label || mark.id}. Click for another; double-click for full screen.`;
      if (mark.kind === 'image' || reducedMotion) {
        imageFor(mark, mark.poster || mark.src);
        return;
      }
      const video = document.createElement('video');
      video.src = mark.src;
      video.poster = mark.poster || '';
      video.muted = true;
      video.defaultMuted = true;
      video.autoplay = true;
      video.loop = true;
      video.playsInline = true;
      video.preload = 'metadata';
      video.tabIndex = -1;
      video.setAttribute('muted', '');
      video.setAttribute('aria-hidden', 'true');
      video.addEventListener('error', () => imageFor(mark, mark.poster || mark.src), { once: true });
      host.replaceChildren(video);
      const playback = video.play();
      if (playback && typeof playback.catch === 'function') playback.catch(() => imageFor(mark, mark.poster || mark.src));
    };

    const nextMark = () => loadManifest().then((marks) => {
      if (!marks.length) return;
      const current = host.dataset.markId || '';
      const candidates = marks.length > 1 ? marks.filter((mark) => mark.id !== current) : marks;
      showMark(candidates[randomIndex(candidates.length)] || marks[0]);
    }).catch(() => {});

    const fullScreen = () => {
      if (document.fullscreenElement === host) {
        document.exitFullscreen?.();
        return;
      }
      host.requestFullscreen?.().catch?.(() => {});
    };

    host.addEventListener('click', (event) => {
      event.preventDefault();
      event.stopPropagation();
      clearTimeout(clickTimer);
      clickTimer = window.setTimeout(nextMark, 230);
    });
    host.addEventListener('dblclick', (event) => {
      event.preventDefault();
      event.stopPropagation();
      clearTimeout(clickTimer);
      fullScreen();
    });
    host.addEventListener('keydown', (event) => {
      if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        nextMark();
      }
    });
  }

  function canonicalId(id, redirects) {
    return redirects[id] || id;
  }

  function layerAllows(edge, layer) {
    if (edge.claim_status === 'legacy_unresolved' || edge.relation_family === 'legacy') return layer === 'all';
    if (layer === 'all') return true;
    const substantive = !['classification', 'documentary', 'evidence', 'legacy'].includes(edge.relation_family)
      && edge.relation_type !== 'legacy_association_unspecified'
      && edge.claim_status !== 'legacy_unresolved';
    if (layer === 'substantive') return substantive;
    if (layer === 'conceptual') return edge.relation_family === 'conceptual';
    if (layer === 'human') return ['human', 'influence', 'historical'].includes(edge.relation_family);
    if (layer === 'practice') return edge.relation_family === 'practice';
    if (layer === 'contestation') return edge.relation_family === 'contestation'
      || ['disputed', 'challenged'].includes(edge.claim_status);
    if (layer === 'provenance') return ['classification', 'evidence', 'documentary'].includes(edge.relation_family);
    return substantive;
  }

  function publicStatus(value) {
    const labels = {
      accepted: 'accepted',
      corroborated: 'corroborated',
      provisional: 'provisional',
      disputed: 'disputed',
      deferred: 'needs more work',
      superseded: 'superseded',
      rejected: 'not accepted',
      legacy_unresolved: 'unresolved legacy connection'
    };
    return labels[value] || String(value || 'status not stated').replace(/_/g, ' ');
  }

  function setupMapCardView() {
    const data = window.TANGLE_DATA || {};
    const graphWrap = document.getElementById('graphWrap');
    const toolbar = graphWrap?.querySelector('.map-canvas-toolbar');
    if (!graphWrap || !toolbar || !Array.isArray(data.nodes) || !Array.isArray(data.edges)) return;
    if (document.getElementById('mapCardToggle')) return;

    const redirects = data.canonical_redirects || {};
    const nodes = new Map((data.nodes || []).map((node) => [node.id, node]));
    const sources = new Map((data.sources || []).map((source) => [source.id, source]));
    const publicNode = (id) => {
      const node = nodes.get(canonicalId(id, redirects));
      return node && node.public_visibility === 'public' ? node : null;
    };
    const edges = (data.edges || []).map((edge) => ({
      ...edge,
      source: canonicalId(edge.source, redirects),
      target: canonicalId(edge.target, redirects)
    })).filter((edge) => publicNode(edge.source) && publicNode(edge.target) && edge.source !== edge.target);

    const toggle = document.createElement('button');
    toggle.id = 'mapCardToggle';
    toggle.type = 'button';
    toggle.className = 'map-card-toggle';
    toggle.setAttribute('aria-pressed', 'false');
    toggle.textContent = 'Card view';
    const fullscreenButton = document.getElementById('mapFullscreen');
    toolbar.insertBefore(toggle, fullscreenButton || null);

    const cardView = document.createElement('div');
    cardView.id = 'mapCardView';
    cardView.setAttribute('aria-live', 'polite');
    const svg = document.getElementById('graphSvg');
    svg.insertAdjacentElement('afterend', cardView);

    function renderCards() {
      if (!graphWrap.classList.contains('map-card-mode')) return;
      const sp = new URLSearchParams(location.hash.slice(1));
      const focusId = canonicalId(sp.get('focus') || 'concept_viability', redirects);
      const focus = publicNode(focusId);
      if (!focus) {
        cardView.innerHTML = '<div class="map-card-empty"><h2>No current focus</h2><p>Select an entry in the map first.</p></div>';
        return;
      }
      const layer = document.getElementById('mapLayer')?.value || sp.get('layer') || 'substantive';
      const family = document.getElementById('mapFamily')?.value || 'all';
      const relations = edges
        .filter((edge) => edge.source === focusId || edge.target === focusId)
        .filter((edge) => layerAllows(edge, layer))
        .filter((edge) => family === 'all' || edge.relation_family === family)
        .sort((a, b) => {
          const familySort = String(a.relation_family || '').localeCompare(String(b.relation_family || ''));
          if (familySort) return familySort;
          const aOther = publicNode(a.source === focusId ? a.target : a.source)?.label || '';
          const bOther = publicNode(b.source === focusId ? b.target : b.source)?.label || '';
          return aOther.localeCompare(bOther);
        });
      const grouped = new Map();
      relations.forEach((edge) => {
        const key = edge.relation_family || 'other';
        if (!grouped.has(key)) grouped.set(key, []);
        grouped.get(key).push(edge);
      });
      const definition = focus.canonical_definition || focus.description || focus.public_stub_text || 'No public description yet.';
      const groups = [...grouped.entries()].map(([familyKey, familyEdges]) => `
        <section class="map-card-family">
          <h3>${esc(relationFamilyLabels[familyKey] || familyKey.replace(/_/g, ' '))} · ${familyEdges.length}</h3>
          <div class="map-card-relations">
            ${familyEdges.map((edge) => {
              const otherId = edge.source === focusId ? edge.target : edge.source;
              const other = publicNode(otherId);
              const source = publicNode(edge.source);
              const target = publicNode(edge.target);
              const phrase = edge.plain_phrase || String(edge.relation_type || 'relates to').replace(/_/g, ' ');
              const sentence = `${source?.label || edge.source} ${phrase} ${target?.label || edge.target}`;
              const sourceCount = parseList(edge.source_ids).map((id) => sources.get(id)).filter(Boolean).length;
              return `<article class="map-card-relation">
                <p><a href="#view=map&layer=${encodeURIComponent(layer)}&depth=1&focus=${encodeURIComponent(otherId)}"><strong>${esc(other?.label || otherId)}</strong></a><br><span>${esc(sentence)}</span></p>
                <p class="map-card-meta">${esc(publicStatus(edge.claim_status))}${sourceCount ? ` · ${sourceCount} source${sourceCount === 1 ? '' : 's'}` : ''}</p>
              </article>`;
            }).join('')}
          </div>
        </section>`).join('');
      cardView.innerHTML = `
        <article class="map-card-focus">
          <p class="eyebrow">Current centre · ${esc(String(focus.entity_type || 'entry').replace(/_/g, ' '))}</p>
          <h2>${esc(focus.label)}</h2>
          <p>${esc(definition)}</p>
          <p class="small">${relations.length} visible connection${relations.length === 1 ? '' : 's'} in the current layer. Select a connected entry to make it the new centre.</p>
        </article>
        <div class="map-card-groups">${groups || '<div class="map-card-empty"><p>No connections are visible in the current layer or fine filter.</p></div>'}</div>`;
    }

    function setCardMode(enabled) {
      graphWrap.classList.toggle('map-card-mode', enabled);
      toggle.setAttribute('aria-pressed', String(enabled));
      toggle.textContent = enabled ? 'Graph view' : 'Card view';
      if (enabled) renderCards();
    }

    toggle.addEventListener('click', () => setCardMode(!graphWrap.classList.contains('map-card-mode')));
    window.addEventListener('hashchange', () => window.requestAnimationFrame(renderCards));
    document.getElementById('mapLayer')?.addEventListener('change', () => window.requestAnimationFrame(renderCards));
    document.getElementById('mapFamily')?.addEventListener('change', () => window.requestAnimationFrame(renderCards));
  }

  document.addEventListener('click', (event) => {
    if (event.target.closest(interactiveSelector)) return;
    const card = event.target.closest('.card.is-clickable');
    if (!card) return;
    const action = card.querySelector(actionSelector);
    if (action) action.click();
  });

  const observer = new MutationObserver((records) => {
    for (const record of records) {
      for (const node of record.addedNodes) {
        if (!(node instanceof Element)) continue;
        refine(node.matches('.card') ? node.parentElement || document : node);
      }
    }
  });

  function init() {
    installStyles();
    refine();
    // The header rule is retired in 0.22. Its implementation remains here for history;
    // the maintained page and portable component use local data.
    setupLivingMarkControls();
    setupMapCardView();
    observer.observe(document.body, { childList: true, subtree: true });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
