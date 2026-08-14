#!/usr/bin/env python3
"""Patch the public interface for release 0.11 whole-to-detail map navigation."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "docs" / "index.html"
APP = ROOT / "docs" / "assets" / "app.js"
CSS = ROOT / "docs" / "assets" / "site-enhancements.css"


GRAPH_OLD = '''        <div class="graph-wrap">
          <svg id="graphSvg" viewBox="0 0 1200 760" aria-label="Interactive map of selected entries and connections">
            <defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="8" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z"></path></marker></defs>
            <g id="graphRoot"><g id="graphEdges"></g><g id="graphNodes"></g></g>
          </svg>
        </div>'''

GRAPH_NEW = '''        <div class="graph-wrap" id="graphWrap" tabindex="0" aria-label="Map canvas. Use the wheel or zoom slider to change scale; drag to pan.">
          <div class="map-canvas-toolbar" aria-label="Map navigation">
            <div class="map-history-controls">
              <button type="button" id="mapBack" aria-label="Previous map focus" title="Previous map focus" disabled>←</button>
              <button type="button" id="mapForward" aria-label="Next map focus" title="Next map focus" disabled>→</button>
            </div>
            <label class="map-zoom-slider" for="mapZoomRange"><span>Zoom</span><input id="mapZoomRange" type="range" min="22" max="400" value="100" step="1"></label>
            <span id="mapScaleMode" class="map-scale-mode" aria-live="polite">Neighbourhood</span>
            <button type="button" id="mapFullscreen" aria-label="Open map full screen" title="Open map full screen">Full screen</button>
          </div>
          <svg id="graphSvg" viewBox="0 0 1200 760" aria-label="Interactive map of selected entries and connections">
            <defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="8" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z"></path></marker></defs>
            <g id="graphRoot"><g id="graphEdges"></g><g id="graphNodes"></g></g>
          </svg>
          <div class="map-minimap-shell" aria-label="Map overview. Click or drag to move the main view.">
            <svg id="mapMiniMap" viewBox="0 0 1200 760" role="img" aria-label="Overview of the current map selection">
              <g id="miniEdges"></g><g id="miniNodes"></g><rect id="miniViewport" x="0" y="0" width="1200" height="760"></rect>
            </svg>
          </div>
          <p class="map-canvas-help">Wheel or pinch to zoom around the pointer. Drag to pan. Double-click to zoom in; Shift-double-click to zoom out. Keys: +, −, 0 and F.</p>
        </div>'''

CSS_APPEND = r'''

/* 0.11 whole-to-detail conceptual map */
.graph-wrap { position: relative; isolation: isolate; min-height: 620px; outline: none; overflow: hidden; }
.graph-wrap:focus-visible { box-shadow: inset 0 0 0 3px rgba(159, 22, 27, .3); }
.map-canvas-toolbar { position: absolute; z-index: 8; top: .65rem; left: .65rem; right: .65rem; display: flex; flex-wrap: wrap; align-items: center; gap: .45rem; padding: .45rem; border: 1px solid color-mix(in srgb, var(--line) 82%, transparent); border-radius: 10px; background: color-mix(in srgb, var(--panel) 88%, transparent); backdrop-filter: blur(8px); box-shadow: 0 8px 22px rgba(62, 9, 8, .09); }
.map-history-controls { display: inline-flex; gap: .25rem; }
.map-canvas-toolbar button { min-height: 2.15rem; }
.map-zoom-slider { display: grid; grid-template-columns: auto minmax(105px, 210px); align-items: center; gap: .45rem; margin: 0; }
.map-zoom-slider span, .map-scale-mode { font: 700 .72rem/1.2 Arial, sans-serif; letter-spacing: .04em; text-transform: uppercase; }
.map-zoom-slider input { width: min(28vw, 210px); }
.map-scale-mode { min-width: 7.6rem; padding: .42rem .55rem; border-radius: 999px; background: var(--panel-2); color: var(--accent); text-align: center; }
#mapFullscreen { margin-left: auto; }
.map-minimap-shell { position: absolute; z-index: 7; left: .75rem; bottom: 2.65rem; width: min(230px, 31%); aspect-ratio: 1200 / 760; overflow: hidden; border: 1px solid var(--line); border-radius: 9px; background: color-mix(in srgb, var(--panel) 92%, transparent); box-shadow: 0 8px 24px rgba(62, 9, 8, .13); opacity: .86; transition: opacity .15s ease, transform .15s ease; }
.map-minimap-shell:hover, .map-minimap-shell:focus-within { opacity: 1; transform: translateY(-1px); }
#mapMiniMap { display: block; width: 100%; height: 100%; cursor: crosshair; touch-action: none; }
#miniEdges line { stroke: var(--muted); stroke-width: 1.2; opacity: .2; vector-effect: non-scaling-stroke; }
#miniNodes circle { fill: var(--accent); opacity: .48; }
#miniNodes circle.focus { fill: var(--orange); opacity: 1; }
#miniViewport { fill: rgba(237, 119, 3, .08); stroke: var(--orange); stroke-width: 9; vector-effect: non-scaling-stroke; rx: 14; ry: 14; pointer-events: none; }
.map-canvas-help { position: absolute; z-index: 6; left: .75rem; right: .75rem; bottom: .45rem; margin: 0; padding: .35rem .55rem; border-radius: 7px; background: color-mix(in srgb, var(--panel) 84%, transparent); color: var(--muted); font: .72rem/1.35 Arial, sans-serif; pointer-events: none; }
.graph-edge-label { display: none; fill: var(--ink); paint-order: stroke; stroke: var(--panel); stroke-width: 5px; stroke-linejoin: round; font: 700 11px/1.2 Arial, sans-serif; text-anchor: middle; pointer-events: none; }
.graph-edge-label.visible { display: block; }
#graphSvg.map-zoom-overview .graph-label { display: none; }
#graphSvg.map-zoom-overview .graph-label[data-priority="3"] { display: block; font-weight: 800; }
#graphSvg.map-zoom-overview .graph-edge.contextual { opacity: .045; }
#graphSvg.map-zoom-neighbourhood .graph-label[data-priority="1"] { display: none; }
#graphSvg.map-zoom-detail .graph-label.dense-hidden { display: block; }
#graphSvg.map-zoom-detail .graph-edge-label.visible { display: block; }
#graphSvg.map-zoom-detail .graph-node-group:hover .graph-label,
#graphSvg.map-zoom-neighbourhood .graph-node-group:hover .graph-label { display: block; font-weight: 800; }
#graphSvg .graph-node-group { cursor: pointer; }
#graphSvg .graph-node-group:hover .graph-node { stroke: var(--orange); stroke-width: 3px; }
.graph-wrap:fullscreen { width: 100vw; height: 100vh; min-height: 100vh; padding: 0; background: var(--paper); }
.graph-wrap:fullscreen #graphSvg { width: 100%; height: 100%; }
.graph-wrap:fullscreen .map-canvas-help { bottom: .7rem; }
@media (max-width: 760px) {
  .map-canvas-toolbar { right: .45rem; left: .45rem; }
  .map-zoom-slider { grid-template-columns: auto minmax(80px, 1fr); flex: 1 1 145px; }
  .map-zoom-slider input { width: 100%; }
  #mapFullscreen { margin-left: 0; }
  .map-minimap-shell { width: 34%; min-width: 125px; }
  .map-canvas-help { font-size: .66rem; }
}
@media (prefers-reduced-motion: reduce) {
  .map-minimap-shell { transition: none; }
}
'''


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if new in text:
        return text
    # Later map releases replace these complete rendering blocks. Treat their
    # explicit markers as an already-applied successor, so rebuilding remains
    # idempotent instead of trying to restore the 0.11 implementation.
    if label == "edge rendering" and "const focusEdges = edges.filter" in text:
        return text
    if label == "node semantic labels" and "function graphNodeMark" in text:
        return text
    if label == "activateMapNode" and "['path', 'profiles', 'all'].includes($('mapDepth').value)" in text:
        return text
    if label == "map render tail" and "renderMapMiniMap(positions, edges);" in text and "updateMapHistoryButtons();" in text:
        return text
    if old not in text:
        raise RuntimeError(f"Could not find {label}")
    return text.replace(old, new, 1)


def clean(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.rstrip().splitlines()) + "\n"


def patch_index() -> None:
    text = INDEX.read_text(encoding="utf-8")
    text = text.replace(
        "Open the full public map or centre on one entry. The layout keeps its bearings and moves with your selection; select a line to inspect the statement, status and sources.",
        "Move between the whole graph, a neighbourhood and a selected entry without losing your bearings. Zoom changes the level of visible detail; the minimap shows where you are. Select a line to inspect its statement, status and sources.",
    )
    if 'id="mapMiniMap"' not in text:
        text = replace_once(text, GRAPH_OLD, GRAPH_NEW, "map canvas")
    INDEX.write_text(clean(text), encoding="utf-8")


def patch_app() -> None:
    app = APP.read_text(encoding="utf-8")

    state_old = '''  let mapSelectedEdge = null;
  let mapPath = [];
  let lastMapPositions = new Map();'''
    state_new = '''  let mapSelectedEdge = null;
  let mapPath = [];
  let lastMapPositions = new Map();
  let mapFocusHistory = [mapFocus];
  let mapFocusHistoryIndex = 0;'''
    app = replace_once(app, state_old, state_new, "map state")

    choose_old = '''      if (role === 'map') {
        mapFocus = node.id;
        mapPath = [];
        mapSelectedEdge = null;
        $('mapDepth').value = '1';
        renderMap({ fit: true });
        setHash({ view: 'map', focus: node.id });
      }'''
    choose_new = '''      if (role === 'map') {
        $('mapDepth').value = '1';
        activateMapNode(node.id);
      }'''
    app = replace_once(app, choose_old, choose_new, "map search selection")

    activate_old = '''  function activateMapNode(id) {
    mapFocus = id;
    mapSelectedEdge = null;
    if (!$('mapDepth').value || $('mapDepth').value === 'path') $('mapDepth').value = '1';
    mapPath = [];
    $('mapSearch').value = nodeById.get(mapFocus)?.label || '';
    const keepsWholeMap = ['all', 'profiles'].includes($('mapDepth').value);
    renderMap({ fit: !keepsWholeMap, focus: keepsWholeMap });
    inspectNode(mapFocus);
    setHash({ view: 'map', focus: mapFocus });
  }'''
    activate_new = '''  function updateMapHistoryButtons() {
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
    if (!$('mapDepth').value || $('mapDepth').value === 'path') $('mapDepth').value = '1';
    mapPath = [];
    $('mapSearch').value = nodeById.get(mapFocus)?.label || '';
    const keepsWholeMap = ['all', 'profiles'].includes($('mapDepth').value);
    renderMap({ fit: !keepsWholeMap, focus: keepsWholeMap });
    inspectNode(mapFocus);
    setHash({ view: 'map', focus: mapFocus, layer: $('mapLayer').value, depth: $('mapDepth').value });
  }'''
    app = replace_once(app, activate_old, activate_new, "activateMapNode")

    app = replace_once(app,
        "      if (sp.get('focus')) {\n        mapFocus = canonicalId(sp.get('focus'));\n        const focus = nodeById.get(mapFocus);\n        if (focus) $('mapSearch').value = focus.label;\n      }",
        "      if (sp.get('focus')) {\n        mapFocus = canonicalId(sp.get('focus'));\n        const focus = nodeById.get(mapFocus);\n        if (focus) $('mapSearch').value = focus.label;\n        recordMapFocus(mapFocus);\n      }",
        "map route history",
    )

    app = replace_once(
        app,
        "      mapFocus = button.dataset.id;\n      mapPath = [];",
        "      mapFocus = button.dataset.id;\n      recordMapFocus(mapFocus);\n      mapPath = [];",
        "entry-to-map history",
    )

    edge_old = '''      return `<g class="graph-edge-group" data-edge="${esc(edge.id)}" tabindex="0" role="button" aria-label="${esc(title)}">
        <line class="graph-edge-hit" x1="${source.x}" y1="${source.y}" x2="${target.x}" y2="${target.y}"></line>
        <line class="${classes}" x1="${source.x}" y1="${source.y}" x2="${target.x}" y2="${target.y}"><title>${esc(title)}</title></line>
      </g>`;'''
    edge_new = '''      const midpointX = (source.x + target.x) / 2;
      const midpointY = (source.y + target.y) / 2;
      const labelClass = selected || inPath ? 'visible' : '';
      return `<g class="graph-edge-group" data-edge="${esc(edge.id)}" tabindex="0" role="button" aria-label="${esc(title)}">
        <line class="graph-edge-hit" x1="${source.x}" y1="${source.y}" x2="${target.x}" y2="${target.y}"></line>
        <line class="${classes}" x1="${source.x}" y1="${source.y}" x2="${target.x}" y2="${target.y}"><title>${esc(title)}</title></line>
        <text class="graph-edge-label ${labelClass}" x="${midpointX}" y="${midpointY - 7}">${esc(edge.plain_phrase || titleCase(edge.relation_type))}</text>
      </g>`;'''
    app = replace_once(app, edge_old, edge_new, "edge rendering")

    node_old = '''      const radius = node.id === mapFocus ? 13 : node.publication_level === 'profile' ? 10 : 7;
      const inPath = mapPath.includes(node.id);
      const showLabel = !dense || node.id === mapFocus || node.publication_level === 'profile' || inPath;
      return `<g class="graph-node-group ${node.id === mapFocus ? 'selected' : ''} ${inPath ? 'path-node' : ''}" data-id="${esc(node.id)}" tabindex="0" role="button" aria-label="Open ${esc(node.label)}">
        <circle class="graph-node" cx="${position.x}" cy="${position.y}" r="${radius}" fill="${colours[node.entity_type] || '#6d625b'}"><title>${esc(node.label)}</title></circle>
        <text class="graph-label ${showLabel ? '' : 'dense-hidden'}" x="${position.x + radius + 4}" y="${position.y - radius - 2}">${esc(node.label)}</text>
      </g>`;'''
    node_new = '''      const radius = node.id === mapFocus ? 13 : node.publication_level === 'profile' ? 10 : 7;
      const inPath = mapPath.includes(node.id);
      const degree = (edgesByNode.get(node.id) || []).filter(mapVisibleEdge).length;
      const labelPriority = node.id === mapFocus || inPath ? 3 : node.publication_level === 'profile' || degree >= 7 ? 2 : 1;
      const showLabel = !dense || labelPriority >= 2;
      return `<g class="graph-node-group ${node.id === mapFocus ? 'selected' : ''} ${inPath ? 'path-node' : ''}" data-id="${esc(node.id)}" data-label-priority="${labelPriority}" tabindex="0" role="button" aria-label="Open ${esc(node.label)}">
        <circle class="graph-node" cx="${position.x}" cy="${position.y}" r="${radius}" fill="${colours[node.entity_type] || '#6d625b'}"><title>${esc(node.label)}</title></circle>
        <text class="graph-label ${showLabel ? '' : 'dense-hidden'}" data-priority="${labelPriority}" x="${position.x + radius + 4}" y="${position.y - radius - 2}">${esc(node.label)}</text>
      </g>`;'''
    app = replace_once(app, node_old, node_new, "node semantic labels")

    render_tail_old = '''    $('mapCount').textContent = nodes.length;
    applyMapTransform();'''
    render_tail_new = '''    $('mapCount').textContent = nodes.length;
    renderMapMiniMap(positions, edges);
    applyMapTransform();
    updateMapHistoryButtons();'''
    app = replace_once(app, render_tail_old, render_tail_new, "map render tail")

    helper_marker = "  function inspectNode(id) {"
    helpers = r'''  function semanticZoomBand(scale = mapTransform.scale) {
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
    if (label) label.textContent = band === 'overview' ? 'Whole map' : band === 'detail' ? 'Detail' : 'Neighbourhood';
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

'''
    if "function semanticZoomBand" not in app:
        app = replace_once(app, helper_marker, helpers + helper_marker, "map semantic helpers")

    transform_old = '''  function applyMapTransform() {
    $('graphRoot').setAttribute('transform', `translate(${mapTransform.x} ${mapTransform.y}) scale(${mapTransform.scale})`);
    const status = $('mapZoomStatus');
    if (status) status.textContent = `${Math.round(mapTransform.scale * 100)}%`;
  }'''
    transform_new = '''  function applyMapTransform() {
    $('graphRoot').setAttribute('transform', `translate(${mapTransform.x} ${mapTransform.y}) scale(${mapTransform.scale})`);
    const percentage = Math.round(mapTransform.scale * 100);
    const status = $('mapZoomStatus');
    if (status) status.textContent = `${percentage}%`;
    const range = $('mapZoomRange');
    if (range && document.activeElement !== range) range.value = String(Math.max(22, Math.min(400, percentage)));
    updateMapSemanticZoom();
    updateMiniViewport();
  }'''
    app = replace_once(app, transform_old, transform_new, "applyMapTransform")

    zoom_controls_old = '''    $('mapZoomIn')?.addEventListener('click', () => zoomAt(1.16));
    $('mapZoomOut')?.addEventListener('click', () => zoomAt(1 / 1.16));'''
    zoom_controls_new = '''    $('mapZoomIn')?.addEventListener('click', () => zoomAt(1.16));
    $('mapZoomOut')?.addEventListener('click', () => zoomAt(1 / 1.16));
    $('mapZoomRange')?.addEventListener('input', (event) => {
      const targetScale = Number(event.target.value) / 100;
      zoomAt(targetScale / Math.max(mapTransform.scale, 0.001));
    });
    svg.addEventListener('dblclick', (event) => {
      if (event.target.closest?.('.graph-node-group, .graph-edge-group')) return;
      event.preventDefault();
      zoomAt(event.shiftKey ? 1 / 1.55 : 1.55, event.clientX, event.clientY);
    });'''
    app = replace_once(app, zoom_controls_old, zoom_controls_new, "zoom controls")

    pointerup_marker = '''    svg.addEventListener('pointerup', (event) => {
      dragging = false;
      wrap.classList.remove('dragging');
      try { svg.releasePointerCapture(event.pointerId); } catch (_) { /* no-op */ }
    });'''
    extra_interactions = pointerup_marker + r'''

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
    });'''
    if "const mini = $('mapMiniMap');" not in app:
        app = replace_once(app, pointerup_marker, extra_interactions, "minimap and navigation interactions")


    app = replace_once(
        app,
        "      mapFocus = 'concept_viability';\n      mapPath = [];\n      mapSelectedEdge = null;",
        "      mapFocus = 'concept_viability';\n      mapFocusHistory = [mapFocus];\n      mapFocusHistoryIndex = 0;\n      updateMapHistoryButtons();\n      mapPath = [];\n      mapSelectedEdge = null;",
        "map reset history",
    )

    legacy_whole_svg_zoom = """  let tangleZoom = 1;

  function zoomMapAt(factor, originX = 50, originY = 50) {
    const svg = document.getElementById('graphSvg');
    if (!svg) return;
    tangleZoom = Math.max(0.55, Math.min(2.5, tangleZoom * factor));
    svg.style.transformOrigin = `${originX}% ${originY}%`;
    svg.style.transform = `scale(${tangleZoom})`;
    const status = document.getElementById('mapZoomStatus');
    if (status) status.textContent = `${Math.round(tangleZoom * 100)}%`;
  }

"""
    app = app.replace(legacy_whole_svg_zoom, "", 1)

    APP.write_text(clean(app), encoding="utf-8")


def patch_css() -> None:
    css = CSS.read_text(encoding="utf-8")
    if "/* 0.11 whole-to-detail conceptual map */" not in css:
        css = css.rstrip() + CSS_APPEND + "\n"
    CSS.write_text(clean(css), encoding="utf-8")


def main() -> None:
    patch_index()
    patch_app()
    patch_css()
    print("Applied 0.11 whole-to-detail map controls and restored the curator comment dot")


if __name__ == "__main__":
    main()
