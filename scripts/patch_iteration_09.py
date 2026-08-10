#!/usr/bin/env python3
"""Apply release 0.9 interface changes from the running feedback notebook."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "docs" / "index.html"
APP = ROOT / "docs" / "assets" / "app.js"
CSS = ROOT / "docs" / "assets" / "site-enhancements.css"

AI_PAGE = '''
    <section id="view-ai-observations" class="view">
      <header class="page-head">
        <p class="eyebrow">Machine-assisted second-order observation</p>
        <h1>AI observations</h1>
        <p>What becomes visible when a language model reads the public graph as data, interface and editorial argument. Counts are reproducible. Interpretations are proposals for challenge, not autonomous facts.</p>
      </header>
      <div class="ai-observation-shell">
        <article class="plain-panel wide ai-method-note">
          <h2>How to read this page</h2>
          <p id="aiMethodNote"></p>
          <p>Each observation separates a measurement from an interpretation, an implication and a test. The useful question is not whether ‘AI agrees’, but whether the evidence supports a better next move.</p>
        </article>
        <div id="aiObservationMetrics" class="metrics ai-metrics" aria-label="Current atlas measurements"></div>
        <div id="aiObservationsList" class="observation-grid"></div>
        <article class="plain-panel wide">
          <p class="eyebrow">Publication controls</p>
          <h2>Risks of making the atlas public</h2>
          <p>Public inspectability is part of the method. It also creates reputational, evidential, privacy, copyright, identity, security and automation risks. These are design constraints, not a legalistic tailpiece.</p>
          <div id="aiRiskList" class="risk-grid"></div>
          <p><a href="https://github.com/antlerboy/the-necessary-tangle/blob/main/documentation/publication-risks.md" target="_blank" rel="noopener">Read the maintained risk and control record →</a></p>
        </article>
        <article class="plain-panel wide">
          <p class="eyebrow">Research queue</p>
          <h2>Sources to mine</h2>
          <p>This list distinguishes discovery sources from evidence. A source appearing here means ‘look here deliberately’, not ‘accept everything found here’.</p>
          <div id="sourceMiningList" class="source-mining-grid"></div>
          <p><a href="https://github.com/antlerboy/the-necessary-tangle/blob/main/documentation/sources-to-mine.md" target="_blank" rel="noopener">Read the full source-mining register →</a></p>
        </article>
      </div>
    </section>
'''

ABOUT_AI_CARD = '''
        <article class="plain-panel wide ai-observations-callout">
          <p class="eyebrow">A second observer</p>
          <h2>AI observations</h2>
          <p>The data now supports observations about the atlas itself: where breadth has outrun depth, where provenance is being mistaken for conceptual connection, which entries carry disproportionate traffic, what the source set makes visible, and what publication risks follow.</p>
          <p><a class="button primary" href="#view=ai-observations" data-view-link="ai-observations">Open the AI observations</a> <a class="button" href="https://github.com/antlerboy/the-necessary-tangle/blob/main/documentation/ai-observations.md" target="_blank" rel="noopener">Inspect the maintained text</a></p>
        </article>
'''

ABOUT_LAYERS = '''
        <article class="plain-panel wide">
          <p class="eyebrow">Different questions, different maps</p>
          <h2>Explore the layers</h2>
          <p>The graph is not one kind of relation rendered many times. Conceptual dependence, human lineage, practice, contestation and provenance answer different questions. Open a layer directly; use ‘Everything’ only when you deliberately want the whole tangle.</p>
          <div class="layer-grid">
            <a class="layer-card" href="#view=map&layer=conceptual&depth=all" data-view-link="map"><strong>Conceptual layer</strong><span>Definitions, prerequisites, specialisation and explanatory relationships.</span></a>
            <a class="layer-card" href="#view=map&layer=human&depth=all" data-view-link="map"><strong>Human lineage layer</strong><span>Teaching, collaboration, historical sequence, influence and institutional transmission.</span></a>
            <a class="layer-card" href="#view=map&layer=practice&depth=all" data-view-link="map"><strong>Practice layer</strong><span>Methods, uses, intervention and documented application.</span></a>
            <a class="layer-card" href="#view=map&layer=contestation&depth=all" data-view-link="map"><strong>Contestation layer</strong><span>Critique, disagreement, correction and rival framing.</span></a>
            <a class="layer-card" href="#view=map&layer=provenance&depth=all" data-view-link="map"><strong>Provenance layer</strong><span>Authorship, membership, evidence and collection structure.</span></a>
            <a class="layer-card" href="#view=map&layer=all&depth=all" data-view-link="map"><strong>Everything</strong><span>The complete typed public graph, including its sparse and awkward parts.</span></a>
          </div>
        </article>
'''

MAP_LAYER_CONTROL = '''
          <label>Layer<select id="mapLayer">
            <option value="all" selected>Everything — full typed graph</option>
            <option value="substantive">Reader map — substantive relationships</option>
            <option value="conceptual">Conceptual layer</option>
            <option value="human">Human lineage layer</option>
            <option value="practice">Practice layer</option>
            <option value="contestation">Contestation layer</option>
            <option value="provenance">Provenance and bibliography</option>
          </select></label>
          <p id="mapLayerNote" class="map-layer-note">Everything includes bibliographic and collection structure. Choose a layer when you want the lines to answer one kind of question.</p>
'''

AI_RENDERER = r'''
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
    $('aiRiskList').innerHTML = (report.public_risks || []).map((risk) => `
      <article class="risk-card">
        <h3>${esc(risk.risk)}</h3>
        <p>${esc(risk.mechanism)}</p>
        <p class="small"><strong>Controls:</strong> ${esc(risk.controls)}</p>
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
'''

MAP_LAYER_HELPERS = r'''
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
      substantive: 'The reader map excludes bibliography and collection structure, keeping conceptual, historical, human, practice and contestation relationships.',
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
'''

NAV_HELPERS = r'''
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
'''

CSS_APPEND = r'''

/* 0.9 feedback iteration: observations, explicit layers and link semantics */
.main-nav a { white-space: nowrap; border: 0; background: transparent; padding: .62rem .78rem; border-radius: 8px; font-family: Arial, sans-serif; cursor: pointer; text-decoration: none; color: inherit; }
.main-nav a:hover, .main-nav a.active { background: var(--panel-2); color: var(--accent); }
:where(.hero-panel, .plain-panel, .card, .metric, .author-strip, .button-stack, .button, .journey-choice, .journey-runner, .step-card, .map-controls, .map-inspector, .coverage-card, .source-card, .claim-card, .empty-card, .risk-card, .observation-card, .source-mining-card) { text-align: left !important; }
.button-stack { justify-items: start; }
.button-stack .button { justify-content: flex-start; width: 100%; }
.hero-actions, .section-head, .site-footer { text-align: left; }
.map-layer-note { margin: -.25rem 0 .25rem; color: var(--muted); font: .78rem/1.4 Arial, sans-serif; }
.layer-grid, .risk-grid, .source-mining-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: .8rem; }
.layer-card { display: grid; gap: .35rem; padding: 1rem; border: 1px solid var(--line); border-radius: 10px; background: var(--panel-2); color: inherit; text-decoration: none; }
.layer-card strong { color: var(--accent); font-size: 1.05rem; }
.layer-card span { color: var(--muted); }
.layer-card:hover { border-color: var(--accent); color: inherit; transform: translateY(-1px); }
.ai-observation-shell { display: grid; gap: 1rem; }
.ai-metrics { grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); }
.observation-grid { display: grid; gap: 1rem; }
.observation-card, .risk-card, .source-mining-card { background: var(--panel); border: 1px solid var(--line); border-radius: var(--radius); box-shadow: var(--shadow); padding: 1.15rem; }
.observation-card h2 { margin: .15rem 0 .8rem; color: var(--accent); font-size: clamp(1.55rem, 3vw, 2.35rem); }
.observation-card dl { display: grid; gap: .7rem; margin: 0; }
.observation-card dl div { display: grid; grid-template-columns: minmax(95px, .22fr) minmax(0, 1fr); gap: .8rem; border-top: 1px solid var(--line); padding-top: .7rem; }
.observation-card dt { color: var(--orange); font: 700 .76rem/1.35 Arial, sans-serif; text-transform: uppercase; letter-spacing: .06em; }
.observation-card dd { margin: 0; }
.risk-card h3, .source-mining-card h3 { color: var(--accent); margin: .2rem 0 .5rem; }
.ai-observations-callout { border-left: 5px solid var(--purple); }
.internal-entry-link { color: var(--accent); }
@media (max-width: 680px) { .observation-card dl div { grid-template-columns: 1fr; gap: .2rem; } }
'''


def clean(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.rstrip().splitlines()) + "\n"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if new in text:
        return text
    if old not in text:
        raise RuntimeError(f"Could not find {label}")
    return text.replace(old, new, 1)


def convert_static_navigation(text: str) -> str:
    def nav_repl(match: re.Match[str]) -> str:
        attrs = match.group("attrs")
        label = match.group("label")
        view_match = re.search(r'data-view="([^"]+)"', attrs)
        view = view_match.group(1) if view_match else "home"
        attrs = re.sub(r'\s*type="button"', '', attrs)
        return f'<a href="#view={view}"{attrs}>{label}</a>'

    text = re.sub(
        r'<button(?P<attrs>[^>]*\bdata-view="[^"]+"[^>]*)>(?P<label>.*?)</button>',
        nav_repl,
        text,
        flags=re.S,
    )

    def link_repl(match: re.Match[str]) -> str:
        attrs = match.group("attrs")
        label = match.group("label")
        view_match = re.search(r'data-view-link="([^"]+)"', attrs)
        view = view_match.group(1) if view_match else "home"
        href = f"#view={view}"
        if view == "map" and 'data-map-mode="all"' in attrs:
            href += "&layer=all&depth=all"
        attrs = re.sub(r'\s*type="button"', '', attrs)
        class_match = re.search(r'class="([^"]*)"', attrs)
        if class_match:
            classes = class_match.group(1).split()
            if "text-button" not in classes and "button" not in classes:
                classes.insert(0, "button")
            attrs = attrs[:class_match.start(1)] + " ".join(classes) + attrs[class_match.end(1):]
        else:
            attrs = ' class="button"' + attrs
        return f'<a href="{href}"{attrs}>{label}</a>'

    return re.sub(
        r'<button(?P<attrs>[^>]*\bdata-view-link="[^"]+"[^>]*)>(?P<label>.*?)</button>',
        link_repl,
        text,
        flags=re.S,
    )


def patch_index() -> None:
    text = INDEX.read_text(encoding="utf-8")
    text = convert_static_navigation(text)

    if 'id="mapLayer"' not in text:
        marker = '<label>Show connections about<select id="mapFamily"><option value="all">All connection types</option></select></label>'
        replacement = MAP_LAYER_CONTROL + '          <label>Fine filter<select id="mapFamily"><option value="all">All connection types in this layer</option></select></label>'
        text = replace_once(text, marker, replacement, "map relation selector")

    current_state = '<article class="plain-panel"><h2>Current state</h2><p>This is a public alpha. It has broad seed coverage and a smaller evidence-deepened core. The current build reports its entry, source, connection, profile and journey counts on the home page.</p></article>'
    if 'class="plain-panel wide ai-observations-callout"' not in text:
        text = replace_once(text, current_state, ABOUT_AI_CARD + "\n" + current_state, "current-state About panel")

    replacements = {
        '<article class="plain-panel"><h2>Why ‘necessary’?</h2><p>The project asks which earlier ideas are needed to understand a later one, which adjacent material is needed to explain the field, and what evidence is needed before a connection is treated as established.</p></article>':
            '<article class="plain-panel"><h2>What ‘necessary’ means here</h2><p>‘Necessary’ is a question, not a verdict. For any later idea the atlas asks three separate things: what must be understood first, what surrounding material makes the idea intelligible, and what evidence is required before a particular connection is published. An entry can be useful and still not be logically necessary.</p></article>',
        '<article class="plain-panel"><h2>Every line makes a statement</h2><p>A line may represent logical dependence, historical sequence, influence, teaching, collaboration, practical use, comparison or dispute. Select it to see the wording, limits, status and sources. ‘Related to’ is not enough.</p></article>':
            '<article class="plain-panel"><h2>Every line is a sentence</h2><p>Read a line as ‘A stands in this stated relation to B’. Logical dependence, historical sequence, teaching, collaboration, citation, influence, use and disagreement are different sentences requiring different evidence. A line is not decoration and ‘related to’ is not a usable claim.</p></article>',
        '<article class="plain-panel"><h2>Scope</h2><p>The core is systems | cybernetics | complexity. Adjacent material is included when it materially explains a central idea, practice, lineage or dispute. The aim is not to map all human thought.</p></article>':
            '<article class="plain-panel"><h2>How the boundary is drawn</h2><p>The core is systems | cybernetics | complexity. Adjacent material enters only when it explains a central idea, practice, lineage or dispute. This is an editorial boundary made for a purpose, not a discovery that the world naturally divides here. Exclusions and deferred candidates are part of the evidence about the map.</p></article>',
        '<article class="plain-panel"><h2>Sources</h2><p>Public links are used where they exist. A published book or archive item without an open copy is marked ‘No public link’. Private research may identify a lead, but private URLs and extracts are not published.</p></article>':
            '<article class="plain-panel"><h2>What a source establishes</h2><p>A source is attached to the smallest statement it can support. A table of contents can establish title, author and collection placement; it cannot by itself establish meaning or influence. Public links are preferred. Where no open copy exists, the atlas gives a complete citation and says ‘No public link’. Private research can generate leads but not public evidence by assertion.</p></article>',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)

    origin_marker = '<article class="plain-panel wide"><h2>A practitioner-centred origin</h2><blockquote>‘We need to map the constellation of influences around practitioners.’</blockquote><p>This formulation from David Ing, as recorded by Benjamin P Taylor, is the immediate provocation for the human-lineage layer. It shifts attention from a tidy history of schools to the actual routes through which practitioners encounter, combine, teach and use ideas.</p></article>'
    if 'class="layer-grid"' not in text:
        text = replace_once(text, origin_marker, origin_marker + "\n" + ABOUT_LAYERS, "practitioner origin panel")

    if 'id="view-ai-observations"' not in text:
        text = text.replace('  </main>', AI_PAGE + '\n  </main>', 1)

    INDEX.write_text(clean(text), encoding="utf-8")


def replace_in_function(app: str, start_marker: str, end_marker: str, transform) -> str:
    start = app.find(start_marker)
    end = app.find(end_marker, start + len(start_marker))
    if start < 0 or end < 0:
        raise RuntimeError(f"Could not isolate {start_marker}")
    return app[:start] + transform(app[start:end]) + app[end:]


def patch_app() -> None:
    app = APP.read_text(encoding="utf-8")

    old_map_visible = '''  function mapVisibleEdge(edge) {
    if (substantiveEdge(edge)) return true;
    if ($('mapDepth')?.value !== 'all') return false;
    return ['authored_by', 'part_of', 'member_of'].includes(edge.relation_type)
      && ['documentary', 'classification'].includes(edge.relation_family);
  }
'''
    if 'function edgeInLayer(edge)' not in app:
        app = replace_once(app, old_map_visible, MAP_LAYER_HELPERS.strip("\n") + "\n", "mapVisibleEdge helper")

    if 'function internalHref(view, params = {})' not in app:
        marker = "  function setHash(params) {"
        app = replace_once(app, marker, NAV_HELPERS.strip("\n") + "\n\n" + marker, "navigation helper insertion")

    safe_old = "['home', 'browse', 'journeys', 'map', 'ask', 'contribute', 'about']"
    safe_new = "['home', 'browse', 'journeys', 'map', 'ask', 'contribute', 'about', 'ai-observations']"
    app = app.replace(safe_old, safe_new)

    old_nav_active = "    $$('.main-nav [data-view]').forEach((button) => button.classList.toggle('active', button.dataset.view === safe));"
    new_nav_active = """    const navView = safe === 'ai-observations' ? 'about' : safe;
    $$('.main-nav [data-view]').forEach((link) => link.classList.toggle('active', link.dataset.view === navView));"""
    app = replace_once(app, old_nav_active, new_nav_active, "main navigation active state")

    old_show_tail = """    if (safe === 'map') renderMap({ fit: true });
    if (safe === 'contribute') updateContributionHint();"""
    new_show_tail = """    if (safe === 'map') renderMap({ fit: true });
    if (safe === 'contribute') updateContributionHint();
    if (safe === 'ai-observations') renderAIObservations();"""
    app = replace_once(app, old_show_tail, new_show_tail, "showView render hooks")

    old_route_map = """    if (view === 'map' && sp.get('focus')) {
      mapFocus = canonicalId(sp.get('focus'));
      const focus = nodeById.get(mapFocus);
      if (focus) $('mapSearch').value = focus.label;
      renderMap({ fit: true });
    }"""
    new_route_map = """    if (view === 'map') {
      const layer = sp.get('layer');
      const depth = sp.get('depth');
      if (layer && [...$('mapLayer').options].some((option) => option.value === layer)) $('mapLayer').value = layer;
      if (depth && [...$('mapDepth').options].some((option) => option.value === depth)) $('mapDepth').value = depth;
      if (sp.get('focus')) {
        mapFocus = canonicalId(sp.get('focus'));
        const focus = nodeById.get(mapFocus);
        if (focus) $('mapSearch').value = focus.label;
      }
      updateMapLayerNote();
      renderMap({ fit: true });
    }"""
    app = replace_once(app, old_route_map, new_route_map, "map route parameters")

    if 'function renderAIObservations()' not in app:
        marker = "  function renderHome() {"
        app = replace_once(app, marker, AI_RENDERER.strip("\n") + "\n\n" + marker, "AI observations renderer")

    def patch_graph_selection(block: str) -> str:
        block = block.replace("if (!substantiveEdge(edge)) continue;", "if (!edgeInLayer(edge)) continue;")
        old_all = "    if (mode === 'all') return new Set(allowed);"
        new_all = """    if (mode === 'all') {
      if (($('mapLayer')?.value || 'all') === 'all' && family === 'all') return new Set(allowed);
      const incident = new Set();
      for (const edge of canonicalEdges) {
        if (!edgeInLayer(edge)) continue;
        if (family !== 'all' && edge.relation_family !== family) continue;
        if (allowed.has(edge.source)) incident.add(edge.source);
        if (allowed.has(edge.target)) incident.add(edge.target);
      }
      if (allowed.has(mapFocus)) incident.add(mapFocus);
      return incident;
    }"""
        if old_all not in block and new_all not in block:
            raise RuntimeError("Could not patch full-map layer selection")
        return block.replace(old_all, new_all)

    app = replace_in_function(app, "  function graphSelection() {", "  function mapPositions(ids) {", patch_graph_selection)

    def patch_shortest(block: str) -> str:
        block = block.replace("if (!substantiveEdge(edge)) continue;", "if (!edgeInLayer(edge)) continue;")
        old = """        const other = edge.source === id ? edge.target : edge.source;
        const otherNode = nodeById.get(other);"""
        new = """        if ($('mapFamily').value !== 'all' && edge.relation_family !== $('mapFamily').value) continue;
        const other = edge.source === id ? edge.target : edge.source;
        const otherNode = nodeById.get(other);"""
        return block.replace(old, new, 1)

    app = replace_in_function(app, "  function shortestPath(from, to) {", "  function extractQuestionMatches", patch_shortest)

    old_inspect_relations = "    const relations = (edgesByNode.get(id) || []).filter(substantiveEdge).slice(0, 14);"
    new_inspect_relations = """    const family = $('mapFamily')?.value || 'all';
    const relations = (edgesByNode.get(id) || [])
      .filter((edge) => edgeInLayer(edge) && (family === 'all' || edge.relation_family === family))
      .slice(0, 14);"""
    app = replace_once(app, old_inspect_relations, new_inspect_relations, "map inspector layer filter")

    old_wheel = """    svg.addEventListener('wheel', (event) => {
      event.preventDefault();
      const factor = event.deltaY < 0 ? 1.12 : 0.89;
      mapTransform.scale = Math.min(4, Math.max(0.22, mapTransform.scale * factor));
      applyMapTransform();
    }, { passive: false });"""
    new_wheel = """    function zoomAt(factor, clientX = null, clientY = null) {
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
    $('mapZoomOut')?.addEventListener('click', () => zoomAt(1 / 1.16));"""
    app = replace_once(app, old_wheel, new_wheel, "pointer-centred wheel zoom")

    old_apply_transform = """  function applyMapTransform() {
    $('graphRoot').setAttribute('transform', `translate(${mapTransform.x} ${mapTransform.y}) scale(${mapTransform.scale})`);
  }"""
    new_apply_transform = """  function applyMapTransform() {
    $('graphRoot').setAttribute('transform', `translate(${mapTransform.x} ${mapTransform.y}) scale(${mapTransform.scale})`);
    const status = $('mapZoomStatus');
    if (status) status.textContent = `${Math.round(mapTransform.scale * 100)}%`;
  }"""
    app = replace_once(app, old_apply_transform, new_apply_transform, "map zoom status")

    old_reset = """      $('mapDepth').value = '1';
      $('mapFamily').value = 'all';"""
    new_reset = """      $('mapDepth').value = 'all';
      $('mapLayer').value = 'all';
      $('mapFamily').value = 'all';
      updateMapLayerNote();"""
    app = replace_once(app, old_reset, new_reset, "map reset layer")

    old_change = "    ['mapDepth', 'mapFamily', 'mapIncludeStubs'].forEach((id) => $(id).addEventListener('change', () => {"
    new_change = "    ['mapDepth', 'mapLayer', 'mapFamily', 'mapIncludeStubs'].forEach((id) => $(id).addEventListener('change', () => {"
    app = replace_once(app, old_change, new_change, "map control change list")
    old_change_body = """      mapSelectedEdge = null;
      renderMap({ fit: true });"""
    new_change_body = """      mapSelectedEdge = null;
      if (id === 'mapLayer') updateMapLayerNote();
      renderMap({ fit: true });"""
    app = app.replace(old_change_body, new_change_body, 1)

    # Convert generated entry and journey navigation to real anchors so links can be opened in new tabs.
    app = app.replace(
        "out.push(`<button class=\"text-button entry-link inline-concept\" data-id=\"${esc(hit.node.id)}\">${esc(hit.text)}</button>`);",
        "out.push(`<a href=\"${internalHref('item', { id: hit.node.id, from: baseView })}\" class=\"text-button entry-link inline-concept internal-entry-link\" data-id=\"${esc(hit.node.id)}\">${esc(hit.text)}</a>`);",
    )
    app = app.replace(
        "? `<button class=\"chip entry-link\" data-id=\"${esc(match.node.id)}\">${esc(value)}</button>`",
        "? `<a href=\"${internalHref('item', { id: match.node.id, from: baseView })}\" class=\"chip entry-link internal-entry-link\" data-id=\"${esc(match.node.id)}\">${esc(value)}</a>`",
    )
    app = app.replace(
        "<button class=\"text-button entry-link\" data-id=\"${esc(edge.source)}\">${esc(source?.label || edge.source)}</button>",
        "<a href=\"${internalHref('item', { id: edge.source, from: baseView })}\" class=\"text-button entry-link internal-entry-link\" data-id=\"${esc(edge.source)}\">${esc(source?.label || edge.source)}</a>",
    )
    app = app.replace(
        "<button class=\"text-button entry-link\" data-id=\"${esc(edge.target)}\">${esc(target?.label || edge.target)}</button>",
        "<a href=\"${internalHref('item', { id: edge.target, from: baseView })}\" class=\"text-button entry-link internal-entry-link\" data-id=\"${esc(edge.target)}\">${esc(target?.label || edge.target)}</a>",
    )
    app = app.replace(
        '<button class="text-button open-card" data-id="${esc(node.id)}">Open</button>',
        '<a href="${internalHref(\'item\', { id: node.id, from: baseView })}" class="text-button open-card internal-entry-link" data-id="${esc(node.id)}">Open</a>',
    )
    app = app.replace(
        'return node ? `<button class="chip open-card" data-id="${esc(node.id)}">${esc(label)}</button>` : \'\';',
        'return node ? `<a href="${internalHref(\'item\', { id: node.id, from: \'home\' })}" class="chip open-card internal-entry-link" data-id="${esc(node.id)}">${esc(label)}</a>` : \'\';',
    )
    app = app.replace(
        '<footer><span class="meta">${journey.steps.length} linked steps</span><button class="text-button open-journey" data-id="${esc(journey.id)}">Begin</button></footer>',
        '<footer><span class="meta">${journey.steps.length} linked steps</span><a href="${internalHref(\'journeys\', { id: journey.id, step: 0 })}" class="text-button open-journey" data-id="${esc(journey.id)}">Begin</a></footer>',
    )
    app = app.replace(
        "$('journeyList').innerHTML = journeys.map((journey) => `<button class=\"journey-choice ${journey.id === activeJourney ? 'active' : ''}\" data-id=\"${esc(journey.id)}\">",
        "$('journeyList').innerHTML = journeys.map((journey) => `<a href=\"${internalHref('journeys', { id: journey.id, step: 0 })}\" class=\"journey-choice ${journey.id === activeJourney ? 'active' : ''}\" data-id=\"${esc(journey.id)}\">",
    )
    app = app.replace("    </button>`).join('');", "    </a>`).join('');", 1)
    app = app.replace(
        '<h3><button class="text-button open-card" data-id="${esc(node?.id)}">${esc(node?.label || step.node_id)}</button></h3>',
        '<h3><a href="${internalHref(\'item\', { id: node?.id, from: \'journeys\' })}" class="text-button open-card internal-entry-link" data-id="${esc(node?.id)}">${esc(node?.label || step.node_id)}</a></h3>',
    )
    app = app.replace(
        '<button class="primary open-card" data-id="${esc(node?.id)}">Open the full entry</button>',
        '<a href="${internalHref(\'item\', { id: node?.id, from: \'journeys\' })}" class="button primary open-card internal-entry-link" data-id="${esc(node?.id)}">Open the full entry</a>',
    )
    app = app.replace(
        '<div class="entry-actions"><button class="primary open-card" data-id="${esc(node.id)}">Open full entry</button></div>',
        '<div class="entry-actions"><a href="${internalHref(\'item\', { id: node.id, from: \'map\' })}" class="button primary open-card internal-entry-link" data-id="${esc(node.id)}">Open full entry</a></div>',
    )
    app = app.replace(
        "${index ? '<span>→</span>' : ''}<button class=\"chip path-chip\" data-id=\"${esc(id)}\">${esc(nodeById.get(id)?.label || id)}</button>",
        "${index ? '<span>→</span>' : ''}<a href=\"${internalHref('item', { id, from: 'map' })}\" class=\"chip path-chip internal-entry-link\" data-id=\"${esc(id)}\">${esc(nodeById.get(id)?.label || id)}</a>",
    )

    old_bind_entry = "    $$('.entry-link', root).forEach((button) => button.addEventListener('click', () => renderEntry(button.dataset.id)));"
    new_bind_entry = """    $$('.entry-link', root).forEach((link) => link.addEventListener('click', (event) => {
      if (!plainLeftClick(event)) return;
      event.preventDefault();
      renderEntry(link.dataset.id);
    }));"""
    app = replace_once(app, old_bind_entry, new_bind_entry, "entry-link binding")

    old_bind_cards = "    $$('.open-card', root).forEach((button) => button.addEventListener('click', () => renderEntry(button.dataset.id)));"
    new_bind_cards = """    $$('.open-card', root).forEach((link) => link.addEventListener('click', (event) => {
      if (!plainLeftClick(event)) return;
      event.preventDefault();
      renderEntry(link.dataset.id);
    }));"""
    app = replace_once(app, old_bind_cards, new_bind_cards, "card-link binding")

    old_open_journey = """    $$('.open-journey', $('homeJourneys')).forEach((button) => button.addEventListener('click', () => {
      activeJourney = button.dataset.id;"""
    new_open_journey = """    $$('.open-journey', $('homeJourneys')).forEach((link) => link.addEventListener('click', (event) => {
      if (!plainLeftClick(event)) return;
      event.preventDefault();
      activeJourney = link.dataset.id;"""
    app = replace_once(app, old_open_journey, new_open_journey, "home journey link")

    old_journey_choice = """    $$('.journey-choice', $('journeyList')).forEach((button) => button.addEventListener('click', () => {
      activeJourney = button.dataset.id;"""
    new_journey_choice = """    $$('.journey-choice', $('journeyList')).forEach((link) => link.addEventListener('click', (event) => {
      if (!plainLeftClick(event)) return;
      event.preventDefault();
      activeJourney = link.dataset.id;"""
    app = replace_once(app, old_journey_choice, new_journey_choice, "journey choice link")

    # The inspector uses entry links to refocus the map rather than open the drawer.
    app = app.replace(
        "$$('.entry-link', $('mapInspector')).forEach((button) => button.addEventListener('click', () => activateMapNode(button.dataset.id)));",
        "$$('.entry-link', $('mapInspector')).forEach((link) => link.addEventListener('click', (event) => { if (!plainLeftClick(event)) return; event.preventDefault(); activateMapNode(link.dataset.id); }));",
    )
    app = app.replace(
        "$$('.entry-link', $('drawerBody')).forEach((button) => button.addEventListener('click', () => renderEntry(button.dataset.id)));",
        "$$('.entry-link', $('drawerBody')).forEach((link) => link.addEventListener('click', (event) => { if (!plainLeftClick(event)) return; event.preventDefault(); renderEntry(link.dataset.id); }));",
    )

    old_init_nav = """    $$('.main-nav [data-view]').forEach((button) => button.addEventListener('click', () => showView(button.dataset.view)));
    $$('[data-view-link]').forEach((button) => button.addEventListener('click', () => {
      if (button.dataset.viewLink === 'map' && button.dataset.mapMode === 'all') {
        $('mapDepth').value = 'all';
        mapPath = [];
        mapSelectedEdge = null;
      }
      showView(button.dataset.viewLink);
    }));"""
    new_init_nav = """    $$('.main-nav [data-view]').forEach((link) => link.addEventListener('click', (event) => followInternalAnchor(event, link)));
    $$('[data-view-link]').forEach((link) => link.addEventListener('click', (event) => followInternalAnchor(event, link)));"""
    app = replace_once(app, old_init_nav, new_init_nav, "internal navigation binding")

    # Disable the older CSS-transform zoom listener: graph-root zoom is now mouse-centred and shared by buttons.
    old_legacy_zoom = """    document.getElementById('mapZoomIn')?.addEventListener('click', () => zoomMapAt(1.15));
    document.getElementById('mapZoomOut')?.addEventListener('click', () => zoomMapAt(1 / 1.15));
    const svg = document.getElementById('graphSvg');
    svg?.addEventListener('wheel', (event) => {
      event.preventDefault();
      const box = svg.getBoundingClientRect();
      const x = box.width ? ((event.clientX - box.left) / box.width) * 100 : 50;
      const y = box.height ? ((event.clientY - box.top) / box.height) * 100 : 50;
      zoomMapAt(event.deltaY < 0 ? 1.08 : 1 / 1.08, x, y);
    }, { passive: false });"""
    new_legacy_zoom = """    // Zoom buttons and wheel behaviour are handled by the graph-root transform in initMapInteraction.
    const svg = document.getElementById('graphSvg');"""
    app = replace_once(app, old_legacy_zoom, new_legacy_zoom, "legacy double-zoom handler")

    # Catch any generated quick-link form not covered by the exact replacements above.
    remaining_chip_pattern = re.compile(
        r'<button class="chip open-card" data-id="\$\{esc\(([^)]+)\)\}">(.*?)</button>'
    )
    app = remaining_chip_pattern.sub(
        lambda match: (
            '<a href="${internalHref(\'item\', { id: ' + match.group(1)
            + ', from: baseView })}" class="chip open-card internal-entry-link" data-id="${esc('
            + match.group(1) + ')}">' + match.group(2) + '</a>'
        ),
        app,
    )
    APP.write_text(clean(app), encoding="utf-8")


def patch_css() -> None:
    css = CSS.read_text(encoding="utf-8") if CSS.exists() else ""
    if "0.9 feedback iteration" not in css:
        css = css.rstrip() + "\n" + CSS_APPEND.strip() + "\n"
    CSS.write_text(clean(css), encoding="utf-8")


def main() -> None:
    patch_index()
    patch_app()
    patch_css()
    print("Applied 0.9 AI-observations, layers, links and alignment interface changes")


if __name__ == "__main__":
    main()
