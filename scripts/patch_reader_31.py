"""Make map navigation reproducible and reversible around historical build gates."""
from pathlib import Path
import sys,re
R=Path(__file__).resolve().parents[1]
patches={
 'docs/assets/app.js':[
 ("  function setHash(params) {\n    const sp = new URLSearchParams(params);", "  function mapHref(params = {}) {\n    const current = new URLSearchParams(location.hash.slice(1));\n    return internalHref('map', { layer: $('mapLayer').value, depth: $('mapDepth').value === 'path' ? '1' : $('mapDepth').value, family: $('mapFamily').value, focus: mapFocus, ...(current.get('display') ? { display: current.get('display') } : {}), ...params });\n  }\n\n  function setHash(params) {\n    if (params.view === 'map') {\n      const current = new URLSearchParams(location.hash.slice(1));\n      params = { ...params, family: params.family ?? $('mapFamily').value, ...(params.display || current.get('display') ? { display: params.display || current.get('display') } : {}) };\n    }\n    const sp = new URLSearchParams(params);"),
 ("if (!$('mapDepth').value || ['path', 'profiles', 'all'].includes($('mapDepth').value)) $('mapDepth').value = '1';", "if (!$('mapDepth').value || $('mapDepth').value === 'path') $('mapDepth').value = '1';"),
 ("${internalHref('map', { layer: $('mapLayer').value, depth: $('mapDepth').value, focus: edge.source, edge: edge.id })}","${mapHref({ edge: edge.id })}"),
 ("<a class=\"graph-node-link\" href=\"${internalHref('item', { id: node.id, from: 'map' })}\">", "<a class=\"graph-node-link\" href=\"${mapHref({ focus: node.id })}\">"),
 ("const open = (event) => {\n        event.preventDefault();\n        event.stopPropagation();\n        if (mapPointerDragged) return;", "const open = (event) => {\n        if (event.type === 'click' && !plainLeftClick(event)) return;\n        if (event.type === 'keydown' && (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey)) return;\n        event.preventDefault();\n        event.stopPropagation();\n        if (mapPointerDragged) return;"),
 ("mapSelectedEdge = group.dataset.edge;\n        inspectEdge(mapSelectedEdge, false);\n        renderMap({ fit: false });", "mapSelectedEdge = group.dataset.edge;\n        setHash({ view: 'map', focus: mapFocus, layer: $('mapLayer').value, depth: $('mapDepth').value, edge: mapSelectedEdge });\n        renderMap({ fit: false });\n        inspectEdge(mapSelectedEdge, false);"),
 ("entries · select a node to open its neighbourhood", "entries · select a node to highlight its connections"),
 ],
 'docs/assets/site-enhancements.js':[
 ("const toggle = document.createElement('button');\n    toggle.id = 'mapCardToggle';\n    toggle.type = 'button';", "const toggle = document.createElement('a');\n    toggle.id = 'mapCardToggle';\n    toggle.href = '#view=map&display=cards';"),
 ("toggle.setAttribute('aria-pressed', 'false');", "toggle.setAttribute('aria-label', 'Switch to card view');"),
 ("const family = document.getElementById('mapFamily')?.value || 'all';\n      const relations", "const family = document.getElementById('mapFamily')?.value || 'all';\n      const selectedDepth = document.getElementById('mapDepth')?.value || sp.get('depth') || '1';\n      const depth = selectedDepth === 'path' ? '1' : selectedDepth;\n      const relations"),
 ("&depth=1&focus=${encodeURIComponent(otherId)}", "&depth=${encodeURIComponent(depth)}&display=cards&focus=${encodeURIComponent(otherId)}"),
 ("toggle.setAttribute('aria-pressed', String(enabled));\n      toggle.textContent = enabled ? 'Graph view' : 'Card view';", "toggle.setAttribute('aria-label', enabled ? 'Switch to graph view' : 'Switch to card view');\n      toggle.textContent = enabled ? 'Graph view' : 'Card view';\n      const params = new URLSearchParams(location.hash.slice(1));\n      params.set('view', 'map');\n      params.set('display', enabled ? 'graph' : 'cards');\n      toggle.href = '#' + params.toString();"),
 ("    let chosenView = false;\n    toggle.addEventListener('click', () => {\n      chosenView = true;\n      setCardMode(!graphWrap.classList.contains('map-card-mode'));\n    });\n    const narrowScreen = window.matchMedia('(max-width: 600px)');\n    const responsiveView = () => { if (!chosenView) setCardMode(narrowScreen.matches); };", "    const narrowScreen = window.matchMedia('(max-width: 600px)');\n    const responsiveView = () => {\n      const display = new URLSearchParams(location.hash.slice(1)).get('display');\n      setCardMode(display === 'cards' || (display !== 'graph' && narrowScreen.matches));\n    };"),
 ("new MutationObserver(() => window.requestAnimationFrame(renderCards))\n      .observe(document.getElementById('graphNodes'), { childList: true });\n    window.addEventListener('hashchange', () => window.requestAnimationFrame(renderCards));", "new MutationObserver(() => window.requestAnimationFrame(responsiveView))\n      .observe(document.getElementById('graphNodes'), { childList: true });\n    window.addEventListener('hashchange', () => window.requestAnimationFrame(responsiveView));\n    window.addEventListener('popstate', () => window.requestAnimationFrame(responsiveView));"),
 ]
}
patches['docs/assets/app.js'] += [
 ("depth: $('mapDepth').value === 'path' ? '1' : $('mapDepth').value, family: $('mapFamily').value, focus: mapFocus,", "depth: params.focus && $('mapDepth').value === 'path' ? '1' : $('mapDepth').value, family: $('mapFamily').value, focus: mapFocus, ...($('mapDepth').value === 'path' && !params.focus && mapPath.length > 1 ? { pathFrom: mapPath[0], pathTo: mapPath[mapPath.length - 1] } : {}),"),
 ("    const sp = new URLSearchParams(params);\n    const hash = sp.toString();", "    if (params.view === 'map' && params.depth === 'path' && mapPath.length > 1) params = { ...params, pathFrom: mapPath[0], pathTo: mapPath[mapPath.length - 1] };\n    const sp = new URLSearchParams(params);\n    const hash = sp.toString();"),
 ("      mapSelectedEdge = sp.get('edge') || null;", "      if (depth === 'path' && nodeById.has(sp.get('pathFrom')) && nodeById.has(sp.get('pathTo'))) {\n        mapPath = shortestPath(sp.get('pathFrom'), sp.get('pathTo'));\n        $('pathFrom').value = nodeById.get(sp.get('pathFrom')).label;\n        $('pathTo').value = nodeById.get(sp.get('pathTo')).label;\n        $('pathFrom').dataset.selectedId = sp.get('pathFrom');\n        $('pathTo').dataset.selectedId = sp.get('pathTo');\n        $('pathResult').innerHTML = mapPath.map(id => `<a class=\"chip\" href=\"${internalHref('item', { id, from: 'map' })}\">${esc(nodeById.get(id)?.label || id)}</a>`).join(' → ');\n      }\n      mapSelectedEdge = sp.get('edge') || null;"),
 ("      mapFocus = from.id;\n      mapSelectedEdge = null;\n      updateMapLayerNote();", "      mapFocus = from.id;\n      mapSelectedEdge = null;\n      setHash({ view: 'map', focus: mapFocus, layer: $('mapLayer').value, depth: 'path' });\n      updateMapLayerNote();")
]
reverse='--reverse' in sys.argv
for filename,changes in patches.items():
 p=R/filename;t=p.read_text()
 if not reverse:
  # Later transformations may refine an earlier inserted block. Normalise in
  # reverse dependency order before applying the complete patch set again.
  for old,new in reversed(changes):
   if new in t:t=t.replace(new,old)
 for old,new in (list(reversed(changes)) if reverse else changes):
  if reverse:old,new=new,old
  if old in t:t=t.replace(old,new)
  elif new not in t and not reverse:raise AssertionError('Expected reader patch anchor missing: '+filename+' '+old[:90])
 p.write_text(t)
if not reverse:
 p=R/'docs/index.html';t=p.read_text()
 for asset in ['app','site-enhancements']:t=re.sub(r'assets/'+asset+r'\.js(?:\?v=[^"\s]+)?', 'assets/'+asset+'.js?v=0.31',t)
 p.write_text(t)
print('Reversed' if reverse else 'Applied','0.31 map navigation patches')
