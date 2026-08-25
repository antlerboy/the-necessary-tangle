#!/usr/bin/env python3
"""Patch the reader interface for release 0.18."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
ASSETS = DOCS / "assets"
INDEX = DOCS / "index.html"
APP = ASSETS / "app.js"
VERSION = "0.18.0-public"
RELEASE = "0.18-navigable-tangle-alpha"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if new in text:
        return text
    if old not in text:
        raise RuntimeError(f"Could not find patch marker: {label}")
    return text.replace(old, new, 1)


def page_shell(title: str, eyebrow: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="en-GB">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light dark">
  <meta name="theme-color" content="#9f161b">
  <meta name="description" content="{title} — The Necessary Tangle">
  <link rel="canonical" href="https://transduction.systems/coverage/">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="/assets/styles.css?v={VERSION}">
  <link rel="stylesheet" href="/assets/site-enhancements.css?v={VERSION}">
  <link rel="stylesheet" href="/assets/iteration-17.css?v={VERSION}">
  <link rel="stylesheet" href="/assets/iteration-18.css?v={VERSION}">
  <title>{title} — The Necessary Tangle</title>
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header compact-header">
    <a class="brand" href="/#view=home" aria-label="The Necessary Tangle home">
      <span class="brand-mark tangle-mark" aria-hidden="true"><svg viewBox="0 0 48 48" focusable="false"><path d="M8 24c0-8 6-14 14-14 9 0 18 8 18 18 0 7-5 12-12 12-8 0-14-6-14-13 0-6 5-10 10-10 6 0 10 4 10 9 0 4-3 7-7 7-3 0-6-2-6-5 0-2 2-4 4-4"/><path d="M5 34c7-4 13-11 15-20M28 5c-4 7-4 15 0 22M13 7c8 4 15 11 20 20"/></svg></span>
      <span><strong>The Necessary Tangle</strong><small>A living evidence atlas</small></span>
    </a>
    <a class="button" href="/#view=about">About the atlas</a>
  </header>
  <main id="main" class="coverage-page">
    <header class="page-head"><p class="eyebrow">{eyebrow}</p><h1>{title}</h1></header>
    {body}
  </main>
</body>
</html>
"""


def build_coverage_pages(data: dict) -> None:
    named = data.get("named_coverage_review", {}).get("items", [])
    named_rows = "".join(
        f"<tr><td><a href=\"/#view=item&id={item['node_id']}&from=coverage\">{item['name']}</a></td>"
        f"<td>{item['status'].replace('_', ' ')}</td><td>{item['public_source_count']}</td>"
        f"<td>{item['substantive_connection_count']}</td><td>{', '.join(item.get('aliases', []))}</td></tr>"
        for item in named
    )
    named_body = f"""
      <article class="plain-panel wide">
        <p>This page reports the actual state of every person or institution named in the post-0.17 coverage request. It does not turn a requested name into an unsupported biography or lineage claim. ‘Research queue’ means the name is now findable but source-specific development is still required.</p>
        <p><a class="button primary" href="/#view=browse">Search the atlas</a> <a class="button" href="https://github.com/antlerboy/the-necessary-tangle/issues/2">Canonical feedback record</a></p>
      </article>
      <div class="table-scroll"><table class="coverage-table"><thead><tr><th>Name</th><th>Current depth</th><th>Public sources</th><th>Substantive connections</th><th>Search aliases</th></tr></thead><tbody>{named_rows}</tbody></table></div>
    """
    path = DOCS / "coverage" / "named"
    path.mkdir(parents=True, exist_ok=True)
    (path / "index.html").write_text(page_shell("Named practitioner and institution coverage", "Coverage made inspectable", named_body), encoding="utf-8")

    unfix = data.get("unfix_32_coverage", {})
    unfix_rows = "".join(
        f"<tr><td>{item['concept']}</td><td><a href=\"/#view=item&id={item['node_id']}&from=coverage\">{item['entry_label']}</a></td>"
        f"<td>{item['publication_level'].replace('_', ' ')}</td><td>{'New brief entry' if item['created_in_0_18'] else 'Existing canonical entry'}</td></tr>"
        for item in unfix.get("items", [])
    )
    unfix_body = f"""
      <article class="plain-panel wide">
        <p>All 32 concepts in Jurgen Appelo's unFIX synthesis now resolve to a canonical atlas entry. The source page says that several large language models produced the initial synthesis and prevalence estimates, followed by editorial checking. This is therefore treated as a useful comparator and vocabulary check, not as a neutral canon.</p>
        <p><a class="button primary" href="/#view=item&id=publication_unfix_32_key_concepts&from=coverage">Open the source entry</a> <a class="button" href="https://unfix.com/blog/32-key-concepts">Open the unFIX page</a></p>
      </article>
      <div class="table-scroll"><table class="coverage-table"><thead><tr><th>unFIX concept</th><th>Atlas entry</th><th>Entry depth</th><th>Resolution</th></tr></thead><tbody>{unfix_rows}</tbody></table></div>
    """
    path = DOCS / "coverage" / "unfix-32"
    path.mkdir(parents=True, exist_ok=True)
    (path / "index.html").write_text(page_shell("unFIX 32-concept coverage", "Comparator, not canon", unfix_body), encoding="utf-8")


def patch_index() -> None:
    text = INDEX.read_text(encoding="utf-8")
    text = text.replace("0.17.0-public", VERSION)
    text = replace_once(
        text,
        '<link rel="stylesheet" href="assets/iteration-17.css?v=0.18.0-public">',
        '<link rel="stylesheet" href="assets/iteration-17.css?v=0.18.0-public">\n  <link rel="stylesheet" href="assets/iteration-18.css?v=0.18.0-public">',
        "iteration 18 stylesheet",
    )
    # A successor release may add attributes to the established tangle mark.
    # Treat that as already patched rather than requiring the exact 0.18 tag.
    if 'class="brand-mark tangle-mark"' not in text:
        text = replace_once(
            text,
            '<span class="brand-mark" aria-hidden="true"><i></i><i></i><i></i></span>',
            '<span class="brand-mark tangle-mark" aria-hidden="true"><svg viewBox="0 0 48 48" focusable="false"><path d="M8 24c0-8 6-14 14-14 9 0 18 8 18 18 0 7-5 12-12 12-8 0-14-6-14-13 0-6 5-10 10-10 6 0 10 4 10 9 0 4-3 7-7 7-3 0-6-2-6-5 0-2 2-4 4-4"/><path d="M5 34c7-4 13-11 15-20M28 5c-4 7-4 15 0 22M13 7c8 4 15 11 20 20"/></svg></span>',
            "tangle brand mark",
        )
    text = replace_once(
        text,
        '<button type="button" id="surpriseMeNav" class="surprise-nav">Surprise me</button>',
        '<a href="#view=item&id=concept_viability&from=home" id="surpriseMeNav" class="surprise-nav surprise-me">Surprise me</a>',
        "surprise navigation anchor",
    )
    text = replace_once(
        text,
        '<button type="button" id="surpriseMeHero" class="button surprise-me">Surprise me</button>',
        '<a href="#view=item&id=concept_viability&from=home" id="surpriseMeHero" class="button surprise-me">Surprise me</a>',
        "surprise hero anchor",
    )
    text = replace_once(
        text,
        '<p class="lede">The Necessary Tangle maps ideas, people, methods, publications, institutions, practices and lineages: what they mean, where they came from, what they depend on and how they are used.</p>',
        '<p class="lede">The Necessary Tangle maps ideas, people, methods, publications, institutions, practices and lineages: what they mean, where they came from, what they depend on and how they are used. It’s the connections which are perhaps the most important.</p>',
        "hero connection sentence",
    )
    text = replace_once(
        text,
        '<p class="principle"><strong>Every connection must say what it means.</strong> A historical precursor is not automatically a logical prerequisite. Citation is not mentorship. Resemblance is not evidence of influence.</p>',
        '<p class="principle"><strong>Every connection must say what it means.</strong> A historical precursor is not automatically a logical prerequisite. Citation is not mentorship. Resemblance is not evidence of influence. <a href="#view=about" data-view-link="about">Find out more about how this works.</a></p>',
        "hero about link",
    )
    text = replace_once(
        text,
        '<header class="page-head"><p class="eyebrow">Interactive neighbourhoods</p><h1>Map</h1><p>Begin with a sparse view of the full public graph: a few orientation labels, the current focus and its connections. Select any node to re-layout the map around its immediate neighbourhood; use the larger views for extent and gaps, not simultaneous reading.</p></header>',
        '<header class="page-head"><p class="eyebrow">Interactive neighbourhoods</p><h1>Map</h1><p>Put any entry at the centre, see its immediate and outer relations, and move through the graph without losing the line you followed. The full overview shows extent and gaps; the constellation view is for reading.</p></header>',
        "map introduction",
    )
    text = replace_once(
        text,
        '<option value="2">Two steps</option><option value="path">Path and immediate neighbours</option>',
        '<option value="2">Two steps</option><option value="constellation">Constellation: core and two orbits</option><option value="path">Path and immediate neighbours</option>',
        "constellation map option",
    )
    text = replace_once(
        text,
        '<p id="mapCategoryNote" class="map-category-note">Neighbourhoods are provisional graph groupings, not canonical schools or categories.</p>',
        '<p id="mapCategoryNote" class="map-category-note">Neighbourhoods are provisional graph groupings, not canonical schools or categories.</p><p class="map-constellation-note"><strong>Constellation view:</strong> the selected entry becomes the star; direct connections form the inner orbit and two-step relations the outer orbit. Centrality describes this graph, not intellectual worth.</p>',
        "constellation explanation",
    )
    text = text.replace(
        'aria-label="Map canvas. Use the wheel or zoom slider to change scale; drag to pan."',
        'aria-label="Map canvas. Drag from the background, a node or a connection to pan; use the wheel or zoom slider to change scale."',
    )
    text = replace_once(
        text,
        '<p class="map-canvas-help">Wheel or pinch to zoom around the pointer. Drag to pan. Double-click to zoom in; Shift-double-click to zoom out. Keys: +, −, 0 and F.</p>',
        '<p class="map-canvas-help">Drag from anywhere to pan. A short click selects; a drag moves the map. Wheel or pinch to zoom around the pointer. Double-click zooms; Shift-double-click zooms out. Keys: +, −, 0 and F.</p>',
        "map interaction help",
    )
    about_marker = '<article class="plain-panel wide canon-lineage-panel">'
    if 'href="/coverage/named/"' not in text:
        coverage = '''<article class="plain-panel wide feedback-coverage-panel">
          <p class="eyebrow">Post-0.17 coverage pass</p>
          <h2>Named people, institutions and a 32-concept comparator</h2>
          <p>The requested people and institutions are now resolved through canonical names and search aliases, with their actual source and connection depth exposed. The 32 concepts in the unFIX synthesis each resolve to an atlas entry without treating that AI-assisted list as a settled canon.</p>
          <p><a class="button primary" href="/coverage/named/">Named coverage audit</a> <a class="button" href="/coverage/unfix-32/">unFIX 32-concept coverage</a> <a class="button" href="#view=item&id=person_linda_booth_sweeney&from=about">Linda Booth Sweeney</a></p>
        </article>

        '''
        text = replace_once(text, about_marker, coverage + about_marker, "coverage callout")
    text = replace_once(
        text,
        '<article class="plain-panel wide ai-observations-callout">',
        '<article class="plain-panel wide ai-observations-callout"><p class="release-note-inline"><strong>Updated for 0.18:</strong> observations now include navigation affordances, alias resolution, named-coverage depth and the difference between graph centrality and intellectual importance.</p>',
        "AI observations update notice",
    )
    # The inserted paragraph intentionally precedes the existing eyebrow inside the article.
    text = text.replace('</article><p class="eyebrow">A second observer</p>', '<p class="eyebrow">A second observer</p>', 1)

    script_marker = '<script src="assets/iteration-17.js?v=0.18.0-public"></script>'
    text = replace_once(
        text,
        script_marker,
        script_marker + '\n  <script src="assets/iteration-18.js?v=0.18.0-public"></script>',
        "iteration 18 script",
    )
    INDEX.write_text(text, encoding="utf-8")


def patch_app() -> None:
    text = APP.read_text(encoding="utf-8")
    if "/* 0.18 navigable map and link contract */" in text:
        return

    text = replace_once(
        text,
        "  let mapFocusHistoryIndex = 0;\n",
        "  let mapFocusHistoryIndex = 0;\n  let mapPointerDragged = false;\n",
        "map drag state",
    )
    text = replace_once(
        text,
        "      if (sp.get('focus')) {\n        mapFocus = canonicalId(sp.get('focus'));",
        "      if (sp.get('edge')) mapSelectedEdge = sp.get('edge');\n      if (sp.get('focus')) {\n        mapFocus = canonicalId(sp.get('focus'));",
        "edge route state",
    )
    text = replace_once(
        text,
        "      renderMap({ fit: true });\n    }\n  }\n\n  function sourceLink",
        "      renderMap({ fit: true });\n      if (mapSelectedEdge) inspectEdge(mapSelectedEdge, false);\n    }\n  }\n\n  function sourceLink",
        "edge route inspection",
    )
    text = replace_once(
        text,
        '<button class="primary map-entry" data-id="${esc(node.id)}">Explore connections</button>\n        <button class="ask-entry" data-id="${esc(node.id)}">Ask about this</button>\n        <button class="contribute-entry" data-id="${esc(node.id)}">Suggest a change</button>',
        '<a class="button primary map-entry" href="${internalHref(\'map\', { layer: \'substantive\', depth: \'constellation\', focus: node.id })}" data-id="${esc(node.id)}">Place in the tangle</a>\n        <a class="button ask-entry" href="${internalHref(\'ask\', { seed: node.id })}" data-id="${esc(node.id)}">Ask about this</a>\n        <a class="button contribute-entry" href="${internalHref(\'contribute\', { entry: node.id })}" data-id="${esc(node.id)}">Suggest a change</a>',
        "entry route anchors",
    )
    text = replace_once(
        text,
        "    $$('.inspect-edge', root).forEach((button) => button.addEventListener('click', () => inspectEdge(button.dataset.edge, true)));\n    $$('.map-entry', root).forEach((button) => button.addEventListener('click', () => {",
        "    $$('.inspect-edge', root).forEach((button) => button.addEventListener('click', (event) => { if (!plainLeftClick(event)) return; event.preventDefault(); inspectEdge(button.dataset.edge, true); }));\n    $$('.map-entry', root).forEach((button) => button.addEventListener('click', (event) => {\n      if (!plainLeftClick(event)) return;\n      event.preventDefault();",
        "map anchor click contract",
    )
    text = replace_once(
        text,
        "    $$('.ask-entry', root).forEach((button) => button.addEventListener('click', () => {\n      const node = nodeById.get(button.dataset.id);",
        "    $$('.ask-entry', root).forEach((button) => button.addEventListener('click', (event) => {\n      if (!plainLeftClick(event)) return;\n      event.preventDefault();\n      const node = nodeById.get(button.dataset.id);",
        "ask anchor click contract",
    )
    text = replace_once(
        text,
        "    $$('.contribute-entry', root).forEach((button) => button.addEventListener('click', () => {\n      const node = nodeById.get(button.dataset.id);",
        "    $$('.contribute-entry', root).forEach((button) => button.addEventListener('click', (event) => {\n      if (!plainLeftClick(event)) return;\n      event.preventDefault();\n      const node = nodeById.get(button.dataset.id);",
        "contribute anchor click contract",
    )
    text = replace_once(
        text,
        "    const depth = Number(mode);",
        "    const depth = mode === 'constellation' ? 2 : Number(mode);",
        "constellation selection depth",
    )
    text = text.replace(
        "      label.textContent = depth === 'all' ? 'Full overview' : depth === 'profiles' ? 'Developed overview' : band === 'overview' ? 'Whole map' : band === 'detail' ? 'Detail' : 'Neighbourhood';",
        "      label.textContent = depth === 'all' ? 'Full overview' : depth === 'profiles' ? 'Developed overview' : depth === 'constellation' ? 'Constellation' : band === 'overview' ? 'Whole map' : band === 'detail' ? 'Detail' : 'Neighbourhood';",
    )
    text = replace_once(
        text,
        "      return `<g class=\"graph-edge-group\" data-edge=\"${esc(edge.id)}\" tabindex=\"0\" role=\"button\" aria-label=\"${esc(title)}\">\n        <line class=\"graph-edge-hit\" x1=\"${source.x}\" y1=\"${source.y}\" x2=\"${target.x}\" y2=\"${target.y}\"></line>\n        <line class=\"${classes}\" x1=\"${source.x}\" y1=\"${source.y}\" x2=\"${target.x}\" y2=\"${target.y}\"><title>${esc(title)}</title></line>\n        <text class=\"graph-edge-label ${labelClass}\" x=\"${midpointX}\" y=\"${midpointY - 7}\">${esc(edge.plain_phrase || titleCase(edge.relation_type))}</text>\n      </g>`;",
        "      return `<a class=\"graph-edge-link\" href=\"${internalHref('map', { layer: $('mapLayer').value, depth: $('mapDepth').value, focus: edge.source, edge: edge.id })}\"><g class=\"graph-edge-group\" data-edge=\"${esc(edge.id)}\" tabindex=\"0\" role=\"button\" aria-label=\"${esc(title)}\">\n        <line class=\"graph-edge-hit\" x1=\"${source.x}\" y1=\"${source.y}\" x2=\"${target.x}\" y2=\"${target.y}\"></line>\n        <line class=\"${classes}\" x1=\"${source.x}\" y1=\"${source.y}\" x2=\"${target.x}\" y2=\"${target.y}\"><title>${esc(title)}</title></line>\n        <text class=\"graph-edge-label ${labelClass}\" x=\"${midpointX}\" y=\"${midpointY - 7}\">${esc(edge.plain_phrase || titleCase(edge.relation_type))}</text>\n      </g></a>`;",
        "edge anchors",
    )
    text = replace_once(
        text,
        "      return `<g class=\"${classes}\" data-id=\"${esc(node.id)}\" data-label-priority=\"${labelPriority}\" tabindex=\"0\" role=\"button\" aria-label=\"Open ${esc(node.label)}\">\n        ${graphNodeMark(node, position, radius)}\n        <text class=\"graph-label ${showLabel ? '' : 'dense-hidden'}\" data-priority=\"${labelPriority}\" text-anchor=\"${labelAnchor}\" x=\"${labelX}\" y=\"${position.y + 4}\">${esc(node.label)}</text>\n      </g>`;",
        "      return `<a class=\"graph-node-link\" href=\"${internalHref('item', { id: node.id, from: 'map' })}\"><g class=\"${classes}\" data-id=\"${esc(node.id)}\" data-label-priority=\"${labelPriority}\" tabindex=\"0\" role=\"button\" aria-label=\"Open ${esc(node.label)}\">\n        ${graphNodeMark(node, position, radius)}\n        <text class=\"graph-label ${showLabel ? '' : 'dense-hidden'}\" data-priority=\"${labelPriority}\" text-anchor=\"${labelAnchor}\" x=\"${labelX}\" y=\"${position.y + 4}\">${esc(node.label)}</text>\n      </g></a>`;",
        "node anchors",
    )
    text = replace_once(
        text,
        "      const open = (event) => {\n        event.stopPropagation();\n        activateMapNode(group.dataset.id);",
        "      const open = (event) => {\n        event.preventDefault();\n        event.stopPropagation();\n        if (mapPointerDragged) return;\n        activateMapNode(group.dataset.id);",
        "node drag suppression",
    )
    # This marker appears again for edges after the node block.
    edge_old = "      const open = (event) => {\n        event.stopPropagation();\n        mapSelectedEdge = group.dataset.edge;"
    edge_new = "      const open = (event) => {\n        event.preventDefault();\n        event.stopPropagation();\n        if (mapPointerDragged) return;\n        mapSelectedEdge = group.dataset.edge;"
    text = replace_once(text, edge_old, edge_new, "edge drag suppression")

    text = replace_once(
        text,
        "      list.innerHTML = current.map((result, index) => `<button type=\"button\" class=\"suggestion ${index === active ? 'active' : ''}\" role=\"option\" data-id=\"${esc(result.node.id)}\">",
        "      list.innerHTML = current.map((result, index) => `<a href=\"${internalHref('item', { id: result.node.id, from: role === 'map' ? 'map' : baseView })}\" class=\"suggestion ${index === active ? 'active' : ''}\" role=\"option\" data-id=\"${esc(result.node.id)}\">",
        "search suggestion anchors",
    )
    text = replace_once(
        text,
        "      $$('.suggestion', list).forEach((button) => button.addEventListener('mousedown', (event) => {\n        event.preventDefault();\n        choose(nodeById.get(button.dataset.id));",
        "      $$('.suggestion', list).forEach((button) => button.addEventListener('mousedown', (event) => {\n        if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;\n        event.preventDefault();\n        choose(nodeById.get(button.dataset.id));",
        "suggestion modified-click contract",
    )
    text = replace_once(
        text,
        "      if (role === 'open') renderEntry(node.id);",
        "      if (role === 'open') { setHash({ view: 'item', id: node.id, from: baseView }); renderEntry(node.id); }",
        "open search hash",
    )

    old_drag = """    svg.addEventListener('pointerdown', (event) => {
      if (event.target.closest?.('.graph-node-group, .graph-edge-group')) return;
      dragging = true;
      last = { x: event.clientX, y: event.clientY };
      wrap.classList.add('dragging');
      svg.setPointerCapture(event.pointerId);
    });
    svg.addEventListener('pointermove', (event) => {
      if (!dragging) return;
      mapTransform.x += event.clientX - last.x;
      mapTransform.y += event.clientY - last.y;
      last = { x: event.clientX, y: event.clientY };
      applyMapTransform();
    });
    svg.addEventListener('pointerup', (event) => {
      dragging = false;
      wrap.classList.remove('dragging');
      try { svg.releasePointerCapture(event.pointerId); } catch (_) { /* no-op */ }
    });"""
    new_drag = """    let dragStart = { x: 0, y: 0 };
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
    svg.addEventListener('pointercancel', finishMapPointer);"""
    text = replace_once(text, old_drag, new_drag, "pan from nodes and edges")

    text = text.replace(
        "      $$('.path-chip', $('pathResult')).forEach((button) => button.addEventListener('click', () => renderEntry(button.dataset.id)));",
        "      $$('.path-chip', $('pathResult')).forEach((button) => button.addEventListener('click', (event) => { if (!plainLeftClick(event)) return; event.preventDefault(); renderEntry(button.dataset.id); }));",
    )
    text += "\n/* 0.18 navigable map and link contract */\n"
    APP.write_text(text, encoding="utf-8")


def main() -> None:
    data = json.loads((ROOT / "data" / "public-data.json").read_text(encoding="utf-8"))
    patch_index()
    patch_app()
    build_coverage_pages(data)
    print(f"Patched reader interface for {RELEASE}")


if __name__ == "__main__":
    main()
