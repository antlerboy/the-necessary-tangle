# Semantic map interaction

Release 0.11 changes the map from a zoomable picture into a set of coordinated observations over the same evidence graph.

## Why ordinary zoom was not enough

Making every node and label larger or smaller does not solve graph density. At overview scale, hundreds of equally insistent labels become wallpaper. At close range, hiding all context makes a neighbourhood look more self-contained than it is.

The map therefore uses semantic zoom. Scale changes what is disclosed:

- at the widest overview, labels are limited to developed entries and high-degree bridges;
- as the reader moves closer, medium- and lower-degree labels appear;
- ‘all labels’ remains available when deliberate clutter is useful;
- ‘key labels’ and ‘no labels’ remain available when structure matters more than names.

This is a reading aid. Degree and profile depth are not importance, truth or intellectual rank.

## Keeping bearings

The interaction adds four devices for retaining orientation:

1. A minimap shows the entire selected graph and the current viewport.
2. A focus trail records recently inspected entries and provides a route back.
3. Double-clicking an entry opens its immediate neighbourhood without pretending that the wider graph disappeared.
4. Hovering emphasises immediate neighbours while leaving the rest faintly present.

The aim is not a frictionless flight through information. Some friction is useful: it reminds the reader that every local view is produced by a choice of layer, depth and focus.

## Reader controls

- Mouse wheel or trackpad: zoom around the pointer.
- Drag the background: pan.
- `+` / `−`: zoom around the centre.
- `0`: fit the current graph.
- `L`: cycle adaptive, key, all and no-label modes.
- `F`: enter or leave fullscreen.
- Double-click a node: focus on its immediate neighbourhood.
- Select the minimap: move the main viewport.
- Enable ‘Arrange’: drag individual nodes to make a local reading clearer. Reset arrangement returns to the generated layout.

## What remains generated

The layout remains a projection of the current data and rendering rules. Manual arrangement is temporary reading work, not a curatorial change to the graph. The minimap, label ranking and focus trail are interface state. They do not create new statements or alter sources.

## Design constraints

The map must continue to satisfy these conditions:

- every visible line has a typed meaning;
- conceptual, human, practice, contestation and provenance layers remain distinguishable;
- the full graph is available without pretending it is equally readable at every scale;
- isolated and weakly connected entries remain visible as research debt rather than being forced into invented schools;
- provisional neighbourhoods remain computational groupings, not canonical traditions;
- keyboard and reduced-motion use remain possible;
- an attractive visual pattern must not outrun the evidence which produced it.

## Next test

The next map decision should be based on observed use. In particular:

- can readers move between overview and a local neighbourhood without losing their place?
- do adaptive labels reveal useful structure or merely reproduce the degree distribution?
- does the minimap help, or does it become another tiny diagram nobody reads?
- which layer do readers think they are seeing before and after the layer controls are explained?
- does ‘Arrange’ help local sense-making without implying that a manually pleasing picture is evidence?

Those questions should be answered before replacing the current SVG implementation with a larger graph library.
