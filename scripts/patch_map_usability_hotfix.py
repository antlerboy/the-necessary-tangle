#!/usr/bin/env python3
"""Repair 0.15 map and guided-journey navigation, including David Ing's route."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "docs" / "index.html"
APP = ROOT / "docs" / "assets" / "app.js"
CSS = ROOT / "docs" / "assets" / "site-enhancements.css"
CHANGELOG = ROOT / "CHANGELOG.md"
MAP_DOC = ROOT / "documentation" / "visual-map.md"


def clean(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.rstrip().splitlines()) + "\n"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if new in text:
        return text
    if old not in text:
        raise RuntimeError(f"Could not find {label}")
    return text.replace(old, new, 1)


def patch_index() -> None:
    text = INDEX.read_text(encoding="utf-8")
    map_nav = '<a href="#view=map&layer=substantive&depth=all&focus=concept_viability" data-view="map">Map</a>'
    for old_nav in (
        '<a href="#view=map" data-view="map">Map</a>',
        '<a href="#view=map&layer=substantive&depth=1&focus=concept_viability" data-view="map">Map</a>',
    ):
        text = text.replace(old_nav, map_nav, 1)
    if map_nav not in text:
        raise RuntimeError("Could not set the normal map entry to the full overview")

    map_intro = "Begin with a sparse view of the full public graph: a few orientation labels, the current focus and its connections. Select any node to re-layout the map around its immediate neighbourhood; use the larger views for extent and gaps, not simultaneous reading."
    for old_intro in (
        "Move between the whole graph, a neighbourhood and a selected entry without losing your bearings. Zoom changes the level of visible detail; the minimap shows where you are. Select a line to inspect its statement, status and sources.",
        "Start with one entry and its immediate substantive connections. Select a neighbouring item to move through the graph. The larger views remain available as overviews, but they no longer pretend that 111 simultaneous labels constitute navigation.",
    ):
        text = text.replace(old_intro, map_intro, 1)

    old_orientation = '''            <p class="eyebrow">Start with less</p>
            <p>The full public map is deliberately untidy. Choose a smaller opening without changing the underlying graph.</p>
            <div class="map-orientation-links">
              <a href="#view=map&layer=substantive&depth=profiles">Developed core</a>
              <a href="#view=map&layer=conceptual&depth=profiles">Conceptual layer</a>
              <a href="#view=journeys&id=journey_viability_balance_and_strategy&step=0">Guided route</a>
              <a href="#view=map&layer=all&depth=all">Everything</a>
            </div>'''
    interim_orientation = '''            <p class="eyebrow">Choose a scale</p>
            <p>Neighbourhoods are for reading connections. Overviews are for seeing extent and gaps. They are different jobs.</p>
            <div class="map-orientation-links">
              <a href="#view=map&layer=substantive&depth=1&focus=concept_viability">Viability neighbourhood</a>
              <a href="#view=map&layer=substantive&depth=profiles&focus=concept_viability">Developed overview</a>
              <a href="#view=map&layer=conceptual&depth=profiles&focus=concept_viability">Conceptual overview</a>
              <a href="#view=map&layer=all&depth=all&focus=concept_viability">Everything</a>
            </div>'''
    neighbourhood_orientation = '''            <p class="eyebrow">Choose a scale</p>
            <p>Neighbourhoods are for reading connections. Overviews are for seeing extent and gaps. They are different jobs.</p>
            <div class="map-orientation-links">
              <a href="#view=map&layer=substantive&depth=1&focus=concept_viability">Viability neighbourhood</a>
              <a href="#view=map&layer=substantive&depth=profiles&focus=concept_viability">Developed overview</a>
              <a href="#view=map&layer=conceptual&depth=profiles&focus=concept_viability">Conceptual overview</a>
              <a href="#view=journeys&id=journey_viability_balance_and_strategy&step=0">Guided route</a>
              <a href="#view=map&layer=all&depth=all&focus=concept_viability">Everything</a>
            </div>'''
    new_orientation = '''            <p class="eyebrow">Choose a scale</p>
            <p>The full overview is a starting picture. Select any node to open its readable neighbourhood; return here when you need the whole field.</p>
            <div class="map-orientation-links">
              <a href="#view=map&layer=substantive&depth=all&focus=concept_viability">Full public overview</a>
              <a href="#view=map&layer=substantive&depth=1&focus=concept_viability">Viability neighbourhood</a>
              <a href="#view=map&layer=substantive&depth=profiles&focus=concept_viability">Developed overview</a>
              <a href="#view=map&layer=conceptual&depth=profiles&focus=concept_viability">Conceptual overview</a>
              <a href="#view=journeys&id=journey_viability_balance_and_strategy&step=0">Guided route</a>
              <a href="#view=map&layer=all&depth=all&focus=concept_viability">Everything</a>
            </div>'''
    text = text.replace(interim_orientation, new_orientation, 1)
    text = text.replace(neighbourhood_orientation, new_orientation, 1)
    text = replace_once(text, old_orientation, new_orientation, "map orientation choices")

    old_depth = '<label>View<select id="mapDepth"><option value="1">Immediate connections</option><option value="2">Two steps</option><option value="path">Path and immediate neighbours</option><option value="profiles">All developed entries</option><option value="all" selected>Full public map</option></select></label>'
    neighbourhood_depth = '<label>Scale<select id="mapDepth"><option value="1" selected>Immediate connections</option><option value="2">Two steps</option><option value="path">Path and immediate neighbours</option><option value="profiles">Developed-entry overview</option><option value="all">Full public overview</option></select></label>'
    new_depth = '<label>Scale<select id="mapDepth"><option value="1">Immediate connections</option><option value="2">Two steps</option><option value="path">Path and immediate neighbours</option><option value="profiles">Developed-entry overview</option><option value="all" selected>Full public overview</option></select></label>'
    text = text.replace(neighbourhood_depth, new_depth, 1)
    text = replace_once(text, old_depth, new_depth, "default map scale")
    text = text.replace(
        '<option value="all" selected>Everything — full typed graph</option>\n            <option value="substantive">Reader map — substantive relationships</option>',
        '<option value="all">Everything — full typed graph</option>\n            <option value="substantive" selected>Reader map — substantive relationships</option>',
        1,
    )
    text = text.replace(
        'Everything includes bibliographic and collection structure. Choose a layer when you want the lines to answer one kind of question.',
        'The reader map starts with conceptual, historical, human, practice and contestation relationships. Bibliography and collection structure remain available under Everything.',
        1,
    )

    shape_key = '''          <div class="map-shape-key" aria-label="Node shape key">
            <span><i class="shape-circle" aria-hidden="true"></i>Ideas and principles</span>
            <span><i class="shape-rounded" aria-hidden="true"></i>People and organisations</span>
            <span><i class="shape-diamond" aria-hidden="true"></i>Methods and practice</span>
            <span><i class="shape-square" aria-hidden="true"></i>Publications</span>
          </div>'''
    layer_note = '          <p id="mapLayerNote" class="map-layer-note">The reader map starts with conceptual, historical, human, practice and contestation relationships. Bibliography and collection structure remain available under Everything.</p>'
    if 'class="map-shape-key"' not in text:
        text = replace_once(text, layer_note, layer_note + "\n" + shape_key, "map shape key")

    history_controls = '''            <div class="map-history-controls">
              <button type="button" id="mapBack" aria-label="Previous map focus" title="Previous map focus" disabled>←</button>
              <button type="button" id="mapForward" aria-label="Next map focus" title="Next map focus" disabled>→</button>
            </div>'''
    old_focus_status = history_controls + '\n            <span id="mapFocusStatus" class="map-focus-status" aria-live="polite">Focus: Viability</span>'
    focus_status = history_controls + '\n            <span id="mapFocusStatus" class="map-focus-status" aria-live="polite">Full overview · select a node to open its neighbourhood</span>'
    text = text.replace(old_focus_status, focus_status, 1)
    text = replace_once(text, history_controls, focus_status, "map focus status")
    text = text.replace(
        '<span id="mapScaleMode" class="map-scale-mode" aria-live="polite">Neighbourhood</span>',
        '<span id="mapScaleMode" class="map-scale-mode" aria-live="polite">Full overview</span>',
        1,
    )
    text = text.replace(
        '<aside id="mapInspector" class="map-inspector"><p class="eyebrow">Inspector</p><h2>Choose an item or line</h2><p>Definitions, connection wording, status and sources will appear here.</p></aside>',
        '<aside id="mapInspector" class="map-inspector"><p class="eyebrow">Move through the graph</p><h2>Viability</h2><p>Select a neighbouring item or a line. Its meaning, status and sources will appear here.</p></aside>',
        1,
    )
    text = text.replace('assets/site-enhancements.css?v=0.15-mapfix"', 'assets/site-enhancements.css?v=0.15-mapfix2"', 1)
    text = text.replace('assets/site-enhancements.css"', 'assets/site-enhancements.css?v=0.15-mapfix2"', 1)
    text = text.replace('assets/app.js?v=0.15-mapfix"', 'assets/app.js?v=0.15-mapfix2"', 1)
    text = text.replace('assets/app.js"', 'assets/app.js?v=0.15-mapfix2"', 1)
    INDEX.write_text(clean(text), encoding="utf-8")


def patch_app() -> None:
    app = APP.read_text(encoding="utf-8")
    colours_end = '''  const colours = {
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
  };'''
    shape_helper = colours_end + r'''

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
  }'''
    app = replace_once(app, colours_end, shape_helper, "graph node shape helper")

    app = app.replace(
        "if (!$('mapDepth').value || $('mapDepth').value === 'path') $('mapDepth').value = '1';",
        "if (!$('mapDepth').value || ['path', 'profiles', 'all'].includes($('mapDepth').value)) $('mapDepth').value = '1';",
        1,
    )
    app = app.replace(
        "if (($('mapLayer')?.value || 'all') === 'all' && family === 'all') return new Set(allowed);",
        "if (family === 'all') return new Set(allowed);",
        1,
    )

    render_start = app.index("  function renderMap(options = {}) {")
    render_end = app.index("  function semanticZoomBand", render_start)
    if render_start < 0 or render_end < 0:
        raise RuntimeError("Could not locate renderMap")
    new_render = r'''  function renderMap(options = {}) {
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
      const contextEdge = wideView && !focusEdge && !selected && !inPath;
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
      const showFocusLabel = !wideView && focusEdge && edges.length <= 28;
      const labelClass = selected || inPath || showFocusLabel ? 'visible' : '';
      return `<g class="graph-edge-group" data-edge="${esc(edge.id)}" tabindex="0" role="button" aria-label="${esc(title)}">
        <line class="graph-edge-hit" x1="${source.x}" y1="${source.y}" x2="${target.x}" y2="${target.y}"></line>
        <line class="${classes}" x1="${source.x}" y1="${source.y}" x2="${target.x}" y2="${target.y}"><title>${esc(title)}</title></line>
        <text class="graph-edge-label ${labelClass}" x="${midpointX}" y="${midpointY - 7}">${esc(edge.plain_phrase || titleCase(edge.relation_type))}</text>
      </g>`;
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
      return `<g class="${classes}" data-id="${esc(node.id)}" data-label-priority="${labelPriority}" tabindex="0" role="button" aria-label="Open ${esc(node.label)}">
        ${graphNodeMark(node, position, radius)}
        <text class="graph-label ${showLabel ? '' : 'dense-hidden'}" data-priority="${labelPriority}" text-anchor="${labelAnchor}" x="${labelX}" y="${position.y + 4}">${esc(node.label)}</text>
      </g>`;
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
        event.stopPropagation();
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
        event.stopPropagation();
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

'''
    app = app[:render_start] + new_render + app[render_end:]

    semantic_old = "    if (label) label.textContent = band === 'overview' ? 'Whole map' : band === 'detail' ? 'Detail' : 'Neighbourhood';"
    semantic_new = '''    if (label) {
      const depth = $('mapDepth')?.value;
      label.textContent = depth === 'all' ? 'Full overview' : depth === 'profiles' ? 'Developed overview' : band === 'overview' ? 'Whole map' : band === 'detail' ? 'Detail' : 'Neighbourhood';
    }'''
    app = replace_once(app, semantic_old, semantic_new, "overview scale label")

    inspect_start = app.index("  function inspectNode(id) {")
    inspect_end = app.index("  function inspectEdge", inspect_start)
    if inspect_start < 0 or inspect_end < 0:
        raise RuntimeError("Could not locate inspectNode")
    new_inspect = r'''  function inspectNode(id) {
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
      ${relations.map((edge) => `<div class="relation-statement">${relationStatement(edge)}<br><button class="text-button inspect-edge" data-edge="${esc(edge.id)}">Inspect this connection</button></div>`).join('')}
      ${allRelations.length > relations.length ? `<p class="small">Showing the first ${relations.length} connections in the selected layer. Use a narrower layer or the full entry for the rest.</p>` : ''}`;
    bindCards($('mapInspector'));
    $$('.entry-link', $('mapInspector')).forEach((link) => link.addEventListener('click', (event) => { if (!plainLeftClick(event)) return; event.preventDefault(); activateMapNode(link.dataset.id); }));
    $$('.inspect-edge', $('mapInspector')).forEach((button) => button.addEventListener('click', () => inspectEdge(button.dataset.edge, false)));
  }

'''
    app = app[:inspect_start] + new_inspect + app[inspect_end:]

    app = app.replace(
        "      $('mapDepth').value = 'all';\n      $('mapLayer').value = 'all';",
        "      $('mapDepth').value = 'all';\n      $('mapLayer').value = 'substantive';",
        1,
    )
    app = app.replace(
        "      $('mapDepth').value = '1';\n      $('mapLayer').value = 'substantive';",
        "      $('mapDepth').value = 'all';\n      $('mapLayer').value = 'substantive';",
        1,
    )
    repeated = "        if ($('mapFamily').value !== 'all' && edge.relation_family !== $('mapFamily').value) continue;\n"
    app = app.replace(repeated * 5, repeated, 1)
    APP.write_text(clean(app), encoding="utf-8")


CSS_APPEND = r'''

/* 0.15 map and guided-journey usability hotfix */
.journey-layout { grid-template-columns: minmax(300px, 380px) minmax(0, 1fr); align-items: start; }
.journey-list { display: grid; gap: .55rem; align-content: start; max-height: calc(100vh - 7rem); overflow: auto; position: sticky; top: 4.1rem; }
.journey-choice { display: grid; gap: .24rem; width: 100%; padding: .78rem .85rem; border: 1px solid var(--line); border-radius: 10px; background: var(--panel); color: var(--text); text-decoration: none; font-family: Arial, sans-serif; line-height: 1.25; }
.journey-choice strong { color: var(--accent); font-size: .96rem; }
.journey-choice small { display: block; color: var(--muted); font-size: .74rem; }
.journey-choice:hover, .journey-choice:focus-visible { border-color: var(--accent); background: var(--panel-2); color: var(--text); }
.journey-choice.active { border-color: var(--accent); background: color-mix(in srgb, var(--accent) 7%, var(--panel)); box-shadow: inset 4px 0 0 var(--accent); }
.journey-runner { min-width: 0; padding: clamp(1rem, 2.4vw, 2rem); }
.journey-step-head { display: flex; flex-wrap: wrap; justify-content: space-between; gap: .35rem 1rem; padding-bottom: .75rem; border-bottom: 1px solid var(--line); color: var(--muted); font: 700 .78rem/1.35 Arial, sans-serif; }
.journey-runner > h2 { margin: 1rem 0 .35rem; color: var(--accent); font-size: clamp(1.8rem, 3vw, 2.6rem); line-height: 1.05; }
.step-track { display: flex; flex-wrap: wrap; gap: .4rem; margin: 1rem 0; }
.step-track button { min-width: 2.65rem; min-height: 2.65rem; padding: .5rem; font: 700 .86rem/1 Arial, sans-serif; }
.step-track button.active { border-color: var(--accent); background: var(--accent); color: white; }
.step-card { padding: 1rem 1.1rem; border: 1px solid var(--line); border-left: 4px solid var(--orange); border-radius: 0 10px 10px 0; background: var(--panel-2); }
.step-card h3 { margin: .15rem 0 .65rem; font-size: 1.45rem; }
.step-card .button { display: inline-flex; margin-top: .25rem; }
.journey-actions { display: flex; gap: .55rem; margin-top: .8rem; }
.journey-actions button:disabled { cursor: not-allowed; opacity: .45; }
.map-layout { grid-template-areas: "controls canvas" "controls inspector"; }
.map-controls { grid-area: controls; }
.graph-wrap { grid-area: canvas; min-width: 0; border: 1px solid var(--line); border-radius: var(--radius); background: var(--panel); box-shadow: var(--shadow); }
.map-inspector { grid-area: inspector; margin-top: 0; }
.map-focus-status { max-width: 25rem; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; padding: .42rem .6rem; border-radius: 999px; background: var(--panel-2); color: var(--text); font: 700 .76rem/1.2 Arial, sans-serif; }
.map-shape-key { display: grid; grid-template-columns: 1fr 1fr; gap: .38rem .7rem; margin: .55rem 0 .85rem; color: var(--muted); font: 700 .72rem/1.25 Arial, sans-serif; }
.map-shape-key span { display: flex; align-items: center; gap: .4rem; }
.map-shape-key i { display: inline-block; flex: 0 0 auto; width: .78rem; height: .78rem; background: var(--accent); border: 2px solid var(--panel); box-shadow: 0 0 0 1px var(--line); }
.map-shape-key .shape-circle { border-radius: 50%; }
.map-shape-key .shape-rounded { border-radius: .25rem; background: var(--blue); }
.map-shape-key .shape-diamond { transform: rotate(45deg) scale(.78); border-radius: .08rem; background: var(--green); }
.map-shape-key .shape-square { background: var(--muted); }
.graph-label { fill: var(--text); paint-order: stroke; stroke: var(--panel); stroke-width: 3.5px; stroke-linejoin: round; font: 600 11px/1.2 Arial, sans-serif; pointer-events: none; }
.graph-node { cursor: pointer; stroke: var(--panel); stroke-width: 2px; vector-effect: non-scaling-stroke; }
.graph-node-group.selected .graph-node { stroke: var(--orange); stroke-width: 4px; }
.graph-node-group.focus-neighbour .graph-node { stroke: color-mix(in srgb, var(--accent) 55%, var(--panel)); stroke-width: 2.6px; }
.graph-node-group.context-node { opacity: .26; }
.graph-node-group.context-node:hover, .graph-node-group.context-node:focus { opacity: 1; }
.graph-edge.focus-edge { stroke: var(--accent); stroke-opacity: .9; stroke-width: 2.2px; }
.graph-edge.context-edge { stroke-opacity: .075 !important; }
.graph-edge-group:hover .graph-edge, .graph-edge-group:focus .graph-edge { stroke: var(--orange); stroke-opacity: 1 !important; stroke-width: 3px; }
.map-inspector .relation-statement { padding: .62rem 0; border-top: 1px solid var(--line); }
@media (max-width: 1080px) {
  .map-layout { grid-template-areas: "controls" "canvas" "inspector"; }
}
@media (max-width: 760px) {
  .journey-layout { grid-template-columns: 1fr; }
  .journey-list { position: static; max-height: 24rem; }
  .journey-runner { padding: 1rem; }
  .journey-step-head { display: grid; }
  .map-focus-status { order: 4; flex-basis: 100%; max-width: 100%; }
  .map-shape-key { grid-template-columns: 1fr; }
  .graph-label { font-size: 10px; }
}
'''


def patch_css() -> None:
    css = CSS.read_text(encoding="utf-8")
    marker = "/* 0.15 map and guided-journey usability hotfix */"
    if marker in css:
        # Remove each exact hotfix block while retaining any enduring styles a
        # previous release patch has moved after it during a repeat build.
        block = CSS_APPEND.strip()
        while block in css:
            css = css.replace(block, "", 1)
    css = css.rstrip() + CSS_APPEND
    CSS.write_text(clean(css), encoding="utf-8")


def patch_documents() -> None:
    changelog = CHANGELOG.read_text(encoding="utf-8")
    marker = "- Kept the reader-controlled light/dark switch and the discreet public updates route."
    old_additions = marker + "\n- Corrected the David Ing home route so it opens the maintained David Ing journey.\n- Repaired map legibility with a neighbourhood-first default, focus-driven drill-down, a strict overview label budget, outward labels, a nearby inspector and shape as well as colour cues.\n- Rebuilt the guided-journey index as distinct, scrollable choices and made the active journey, active step, reading card and controls visually unambiguous."
    additions = marker + "\n- Corrected the David Ing home route so it opens the maintained David Ing journey.\n- Repaired map legibility with a label-light full-public overview, one-click neighbourhood drill-down, a strict overview label budget, outward labels, a nearby inspector and shape as well as colour cues.\n- Rebuilt the guided-journey index as distinct, scrollable choices and made the active journey, active step, reading card and controls visually unambiguous."
    changelog = changelog.replace(old_additions, additions, 1)
    changelog = replace_once(changelog, marker, additions, "0.15 changelog hotfix")
    CHANGELOG.write_text(clean(changelog), encoding="utf-8")

    doc = MAP_DOC.read_text(encoding="utf-8")
    doc = doc.replace(
        "- opens on the full public graph;",
        "- opens on a label-light full-public overview and turns any selected node into a readable immediate neighbourhood;",
        1,
    )
    doc = doc.replace(
        "- opens on one substantive immediate neighbourhood; the full graph remains an explicit overview;",
        "- opens on a label-light full-public overview and turns any selected node into a readable immediate neighbourhood;",
        1,
    )
    heading = "## 0.15 legibility repair"
    if heading not in doc:
        addition = '''## 0.15 legibility repair

The earlier interaction controls did not solve the main legibility failure. In the developed-entry view, every developed profile was treated as a priority label. At 111 entries this produced a dense layer of overlapping words, while the inspector fell below the control column rather than staying with the map.

The repair changes the operating rule. The normal map opens on a label-light full-public overview. Selecting any node immediately drills into that node's neighbourhood. Overviews retain the wider field but ration labels to a small set of highly connected anchors plus the current focus and its neighbours. Labels sit outside radial nodes, the inspector follows the canvas, and node shapes distinguish ideas, people/organisations, methods/practice and publications without relying on colour alone.

The full graph is still available. It is now described honestly as an overview of extent, connectedness and gaps, not as a readable diagram at one glance.

'''
        doc = doc.replace("## What the public map now does\n", addition + "## What the public map now does\n", 1)
    doc = doc.replace(
        "The repair changes the operating rule. The normal map opens on one immediate substantive neighbourhood. Selecting a node in an overview drills into that node's neighbourhood.",
        "The repair changes the operating rule. The normal map opens on a label-light full-public overview. Selecting any node immediately drills into that node's neighbourhood.",
        1,
    )
    MAP_DOC.write_text(clean(doc), encoding="utf-8")


def main() -> None:
    patch_index()
    patch_app()
    patch_css()
    patch_documents()
    print("Applied 0.15 map and guided-journey usability hotfix")


if __name__ == "__main__":
    main()
