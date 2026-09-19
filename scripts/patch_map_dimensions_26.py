"""Keep map dimensions selectable, shareable, and consistent with their labels."""

FILTER_OLD = """    const families = unique(canonicalEdges.filter(substantiveEdge).map((edge) => edge.relation_family).filter(Boolean)).sort();
    $('mapFamily').innerHTML = '<option value="all">All connection types</option>'
      + families.map((family) => `<option value="${esc(family)}">${esc(relationFamilyLabel(family))}</option>`).join('');"""
FILTER_NEW = """    updateMapFamilyOptions();"""
HELPER = """  // map-dimensions-26-start
  function updateMapFamilyOptions() {
    const control = $('mapFamily');
    if (!control) return;
    const selected = control.value;
    const families = unique(canonicalEdges.filter(edgeInLayer).map((edge) => edge.relation_family).filter(Boolean)).sort();
    control.innerHTML = '<option value="all">All connection types in this layer</option>'
      + families.map((family) => `<option value="${esc(family)}">${esc(relationFamilyLabel(family))}</option>`).join('');
    control.value = families.includes(selected) ? selected : 'all';
  }
  // map-dimensions-26-end

"""
REPLACEMENTS = [
    ("    if (node.entity_type === 'publication') {", "    if (['publication', 'source'].includes(node.entity_type)) {"),
    ("neighbour || overviewAnchors.has(node.id) ? 2 : 1;", "neighbour || (wideView && overviewAnchors.has(node.id)) ? 2 : 1;"),
    ("    document.addEventListener('fullscreenchange', () => {", "    window.addEventListener('resize', () => { if (baseView === 'map') updateMapSemanticZoom(); });\n    document.addEventListener('fullscreenchange', () => {"),
    ("        if (!substantiveEdge(edge)) continue;\n        const other = edge.source === id ? edge.target : edge.source;\n        if (!ids.has(other)", "        if (!edgeInLayer(edge) || ($('mapFamily').value !== 'all' && edge.relation_family !== $('mapFamily').value)) continue;\n        const other = edge.source === id ? edge.target : edge.source;\n        if (!ids.has(other)"),
    ("    human: 'Human transmission',", "    human: 'Human transmission',\n    teaching: 'Teaching and learning',"),
    ("['human', 'influence', 'historical'].includes(edge.relation_family)", "['human', 'teaching', 'influence', 'historical'].includes(edge.relation_family)"),
    ("conceptual, historical, human, identity, practice and contestation relationships", "conceptual, historical, human, teaching, identity, practice, and contestation relationships"),
    (FILTER_OLD, FILTER_NEW),
    ("  function updateMapLayerNote() {\n", HELPER + "  function updateMapLayerNote() {\n    updateMapFamilyOptions();\n"),
    ("      if (sp.get('edge')) mapSelectedEdge = sp.get('edge');", "      updateMapFamilyOptions();\n      const family = sp.get('family') || 'all';\n      $('mapFamily').value = [...$('mapFamily').options].some((option) => option.value === family) ? family : 'all';\n      mapSelectedEdge = sp.get('edge') || null;"),
    ("      if (id === 'mapLayer') updateMapLayerNote();\n      renderMap({ fit: true });\n    }));", "      if (id === 'mapLayer') updateMapLayerNote();\n      setHash({ view: 'map', focus: mapFocus, layer: $('mapLayer').value, depth: $('mapDepth').value, family: $('mapFamily').value });\n      renderMap({ fit: true });\n    }));"),
    ("      mapFocus = from.id;\n      mapSelectedEdge = null;\n      if (id === 'mapLayer') updateMapLayerNote();", "      mapFocus = from.id;\n      mapSelectedEdge = null;\n      updateMapLayerNote();"),
    ("    svg.classList.add(`map-zoom-${band}`);", """    svg.classList.add(`map-zoom-${band}`);
    const focusedView = !['all', 'profiles'].includes($('mapDepth')?.value);
    svg.classList.toggle('map-focused-reading', focusedView);
    const matrix = $('graphRoot').getScreenCTM();
    const screenScale = matrix ? Math.hypot(matrix.a, matrix.b) : 1;
    svg.style.setProperty('--focused-label-size', `${Math.min(80, 13 / Math.max(screenScale, 0.1))}px`);"""),
    ("${esc(node.label)}</text>\n      </g></a>`;", "${mapNodeLabel(node, labelX)}</text>\n      </g></a>`;"),
]
LABEL_HELPER = """  // map-labels-26-start
  function mapNodeLabel(node, x) {
    const words = node.label.replace(/^Public resource: /, '').split(/\\s+/);
    const lines = [''];
    for (const word of words) {
      const last = lines.length - 1;
      if (lines[last] && (lines[last] + ' ' + word).length > 30) lines.push(word);
      else lines[last] += (lines[last] ? ' ' : '') + word;
    }
    const shown = lines.slice(0, 2);
    if (lines.length > 2) shown[1] += '…';
    return `<title>${esc(node.label)}</title>` + shown.map((line, index) => `<tspan x="${x}" dy="${index ? '1.15em' : '0'}">${esc(line)}</tspan>`).join('');
  }
  // map-labels-26-end

"""
REPLACEMENTS.append(("  function renderMap(options = {}) {", LABEL_HELPER + "  function renderMap(options = {}) {"))

def patch(text):
    for before, after in REPLACEMENTS:
        if after in text:
            continue
        if before not in text:
            raise ValueError('Map dimension anchor changed: ' + before[:90])
        text = text.replace(before, after, 1)
    return text

def unpatch(text):
    for before, after in reversed(REPLACEMENTS):
        text = text.replace(after, before, 1)
    return text
