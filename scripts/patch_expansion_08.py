#!/usr/bin/env python3
"""Apply the 0.8 map motion, full-map entry and discreet notebook refinements."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "docs" / "index.html"
APP = ROOT / "docs" / "assets" / "app.js"
CSS = ROOT / "docs" / "assets" / "site-enhancements.css"

MAP_HELPERS = r'''
  function mapVisibleEdge(edge) {
    if (substantiveEdge(edge)) return true;
    if ($('mapDepth')?.value !== 'all') return false;
    return ['authored_by', 'part_of', 'member_of'].includes(edge.relation_type)
      && ['documentary', 'classification'].includes(edge.relation_family);
  }
'''

MOTION_HELPERS = r'''
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
'''

CSS_APPEND = r'''

/* 0.8 adaptive map and discreet curator-note link */
.graph-edge.contextual { opacity: .18; stroke-dasharray: 2 5; }
.graph-edge-group:focus .graph-edge.contextual,
.graph-edge-group:hover .graph-edge.contextual { opacity: .62; }
.discreet-note-link { display: inline-block; margin-left: .35rem; font-size: .82rem; opacity: .18; vertical-align: baseline; }
.discreet-note-link:hover, .discreet-note-link:focus-within { opacity: .75; }
.discreet-note-link a { color: inherit; text-decoration: none; padding: .15rem .25rem; }
.graph-node-group { transform-box: fill-box; transform-origin: center; }
'''


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
    text = text.replace(
        '<button data-view-link="map">Open the map</button>',
        '<button data-view-link="map" data-map-mode="all">Full public map</button>',
    )
    text = text.replace(
        'Search for an entry to centre the map. Select an item to refocus. Select a line to inspect the statement, its status and its sources.',
        'Open the full public map or centre on one entry. The layout keeps its bearings and moves with your selection; select a line to inspect the statement, status and sources.',
    )
    text = text.replace(
        '<option value="all">Full public map</option>',
        '<option value="all" selected>Full public map</option>',
    )
    text = re.sub(
        r'\s*<p>\s*<a[^>]*class="curator-notebook-link"[^>]*>.*?</a>\s*</p>',
        '',
        text,
        flags=re.S,
    )
    if 'class="discreet-note-link"' not in text:
        discreet = (
            '<span class="discreet-note-link">'
            '<a class="curator-notebook-link" href="https://github.com/antlerboy/the-necessary-tangle/issues/2" '
            'target="_blank" rel="noopener" aria-label="Curator running notebook" title="Curator notes">·</a>'
            '</span>'
        )
        if '</footer>' in text:
            text = text.replace('</footer>', f'{discreet}</footer>', 1)
        else:
            text = text.replace('</body>', f'{discreet}\n</body>', 1)
    INDEX.write_text(clean(text), encoding="utf-8")


def patch_app() -> None:
    app = APP.read_text(encoding="utf-8")

    if 'function mapVisibleEdge(edge)' not in app:
        marker = "  function linkifyKnownText(value, excludedIds = []) {"
        substantive_end = "  function linkifyKnownText(value, excludedIds = []) {"
        if substantive_end not in app:
            raise RuntimeError("Could not find insertion point after substantiveEdge")
        app = app.replace(substantive_end, MAP_HELPERS.strip("\n") + "\n\n" + substantive_end, 1)

    if 'function animateMapTransition(previous, next)' not in app:
        marker = "  function activateMapNode(id) {"
        if marker not in app:
            raise RuntimeError("Could not find activateMapNode")
        app = app.replace(marker, MOTION_HELPERS.strip("\n") + "\n\n" + marker, 1)

    old_sort = ".sort((a, b) => a.label.localeCompare(b.label));"
    adaptive_sort = """.sort((a, b) => {
          const angleA = previousAngle(a.id);
          const angleB = previousAngle(b.id);
          if (angleA !== null && angleB !== null) return angleA - angleB;
          if (angleA !== null) return -1;
          if (angleB !== null) return 1;
          return a.label.localeCompare(b.label);
        });"""
    if 'const angleA = previousAngle(a.id);' not in app:
        if old_sort not in app:
            raise RuntimeError("Could not find radial ring sort")
        app = app.replace(old_sort, adaptive_sort, 1)

    old_activate = """  function activateMapNode(id) {
    mapFocus = id;
    mapSelectedEdge = null;
    if (!$('mapDepth').value || $('mapDepth').value === 'path') $('mapDepth').value = '1';
    mapPath = [];
    $('mapSearch').value = nodeById.get(mapFocus)?.label || '';
    renderMap({ fit: true });
    inspectNode(mapFocus);
    setHash({ view: 'map', focus: mapFocus });
  }"""
    new_activate = """  function activateMapNode(id) {
    mapFocus = id;
    mapSelectedEdge = null;
    if (!$('mapDepth').value || $('mapDepth').value === 'path') $('mapDepth').value = '1';
    mapPath = [];
    $('mapSearch').value = nodeById.get(mapFocus)?.label || '';
    const keepsWholeMap = ['all', 'profiles'].includes($('mapDepth').value);
    renderMap({ fit: !keepsWholeMap, focus: keepsWholeMap });
    inspectNode(mapFocus);
    setHash({ view: 'map', focus: mapFocus });
  }"""
    if new_activate not in app and "function activateMapNode(id, options = {})" not in app:
        app = replace_once(app, old_activate, new_activate, "activateMapNode block")

    old_top = """  function renderMap(options = {}) {
    const ids = graphSelection();
    if (!ids.has(mapFocus) && ids.size) mapFocus = [...ids][0];
    const positions = mapPositions(ids);
    lastMapPositions = positions;"""
    new_top = """  function renderMap(options = {}) {
    const ids = graphSelection();
    if (!ids.has(mapFocus) && ids.size) mapFocus = [...ids][0];
    const previousPositions = lastMapPositions;
    const positions = mapPositions(ids);
    lastMapPositions = positions;"""
    if new_top not in app:
        app = replace_once(app, old_top, new_top, "renderMap start")

    old_filter = """      ids.has(edge.source)
      && ids.has(edge.target)
      && substantiveEdge(edge)
      && (family === 'all' || edge.relation_family === family)"""
    new_filter = """      ids.has(edge.source)
      && ids.has(edge.target)
      && mapVisibleEdge(edge)
      && (family === 'all' || edge.relation_family === family)"""
    if new_filter not in app:
        app = replace_once(app, old_filter, new_filter, "map edge filter")

    old_classes = """        ['accepted', 'corroborated'].includes(edge.claim_status) ? '' : 'provisional',
        selected || inPath ? 'selected' : ''"""
    new_classes = """        ['accepted', 'corroborated'].includes(edge.claim_status) ? '' : 'provisional',
        substantiveEdge(edge) ? '' : 'contextual',
        selected || inPath ? 'selected' : ''"""
    if new_classes not in app:
        app = replace_once(app, old_classes, new_classes, "map edge classes")

    old_finish = """    if (!mapSelectedEdge) inspectNode(mapFocus);
    if (options.fit) requestAnimationFrame(fitMapToSelection);
  }"""
    new_finish = """    if (!mapSelectedEdge) inspectNode(mapFocus);
    animateMapTransition(previousPositions, positions);
    if (options.fit) requestAnimationFrame(fitMapToSelection);
    else if (options.focus) requestAnimationFrame(() => moveMapToFocus(mapFocus));
  }"""
    if new_finish not in app:
        app = replace_once(app, old_finish, new_finish, "renderMap finish")

    old_view_links = "    $$('[data-view-link]').forEach((button) => button.addEventListener('click', () => showView(button.dataset.viewLink)));"
    new_view_links = """    $$('[data-view-link]').forEach((button) => button.addEventListener('click', () => {
      if (button.dataset.viewLink === 'map' && button.dataset.mapMode === 'all') {
        $('mapDepth').value = 'all';
        mapPath = [];
        mapSelectedEdge = null;
      }
      showView(button.dataset.viewLink);
    }));"""
    if new_view_links not in app and "followInternalAnchor" not in app:
        app = replace_once(app, old_view_links, new_view_links, "view-link handler")

    APP.write_text(clean(app), encoding="utf-8")


def patch_css() -> None:
    css = CSS.read_text(encoding="utf-8") if CSS.exists() else ""
    if "0.8 adaptive map" not in css:
        css = css.rstrip() + "\n" + CSS_APPEND.strip() + "\n"
    CSS.write_text(clean(css), encoding="utf-8")


def main() -> None:
    patch_index()
    if APP.exists() and "semanticZoomBand" in APP.read_text(encoding="utf-8"):
        print("Preserved the 0.11 map application while refreshing the 0.8 page and styles")
    else:
        patch_app()
    patch_css()
    print("Applied 0.8 breadth, adaptive-map and discreet-notebook interface changes")


if __name__ == "__main__":
    main()
