"""Make entry actions honour their advertised map scale and evidence layer."""
import re
from patch_map_dimensions_26 import patch as patch_dimensions, unpatch as unpatch_dimensions

def unpatch(text):
    text=unpatch_dimensions(text)
    text=text.replace("layer: relations.some(substantiveEdge) ? 'substantive' : 'all', depth: 'constellation', focus: node.id", "layer: 'substantive', depth: 'constellation', focus: node.id")
    text=re.sub(r"      // Follow the link's actual map parameters.*?      renderMap\(\{ fit: true \}\);", "      showView('map');\n      setHash({ view: 'map', focus: mapFocus });\n      renderMap({ fit: true });",text,flags=re.S)
    text=re.sub(r'\n    // library-source-links-start.*?    // library-source-links-end\n(?:[ \t]*\n)*','\n',text,flags=re.S)
    return text

def patch(text):
    text=unpatch(text)
    before="""      showView('map');
      setHash({ view: 'map', focus: mapFocus });
      renderMap({ fit: true });"""
    after="""      // Follow the link's actual map parameters rather than retaining a previous full overview.
      const destination = new URLSearchParams(new URL(button.href).hash.slice(1));
      $('mapLayer').value = destination.get('layer') || 'substantive';
      $('mapDepth').value = destination.get('depth') || 'constellation';
      $('mapFamily').value = 'all';
      updateMapLayerNote();
      showView('map');
      setHash({ view: 'map', focus: mapFocus, layer: $('mapLayer').value, depth: $('mapDepth').value });
      renderMap({ fit: true });"""
    if before in text:text=text.replace(before,after,1)
    elif after not in text:raise ValueError('Entry map handler changed; inspect before patching')
    old="class=\"button primary map-entry\" href=\"${internalHref('map', { layer: 'substantive', depth: 'constellation', focus: node.id })}"
    new="class=\"button primary map-entry\" href=\"${internalHref('map', { layer: relations.some(substantiveEdge) ? 'substantive' : 'all', depth: 'constellation', focus: node.id })}"
    if old in text:text=text.replace(old,new,1)
    elif new not in text:raise ValueError('Entry map link changed; inspect before patching')
    return patch_dimensions(text)
