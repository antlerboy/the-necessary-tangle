# Whole-to-detail map navigation

Release `0.11-visual-map-alpha` changes the map from a diagram which can be enlarged into a conceptual territory which can be navigated at several scales.

The interaction pattern is informed by Visual Meaning's description of its Shared Meaning Platform as something like a cross between Google Maps and Wikipedia: people can zoom and pan around conceptual maps, select elements, and move from a large picture into explanation and related material. The Necessary Tangle does not reproduce that platform. It borrows the useful interaction question: how can a reader move between the whole, a neighbourhood and a particular item without losing orientation?

Reference: https://visual-meaning.com/our-platform/

## What the public map now does

- opens on the full public graph;
- zooms around the pointer rather than around an arbitrary centre;
- changes label density at overview, neighbourhood and detail scales;
- provides a minimap showing the current viewport within the selected graph;
- lets the reader click or drag in the minimap to move the main view;
- records a local history of selected map foci, with back and forward controls;
- provides a continuous zoom slider alongside the existing buttons and percentage;
- supports full-screen exploration;
- shows the wording of a selected or path connection on the map itself;
- supports double-click zoom and keyboard zoom, pan and fit controls;
- keeps the inspector, typed relations, sources and uncertainty attached to the same public graph.

## Semantic zoom

Zoom should alter what is legible, not merely magnify the same hairball.

At overview scale, the map suppresses most labels and emphasises the selected item, path items and the most developed or connected entries. At neighbourhood scale, developed entries and major bridges remain labelled. At detail scale, the full set of labels in the current selection becomes available. Hovering a node temporarily reveals its label.

These rules are interface heuristics. They do not make an unlabelled entry less important, nor do they turn graph degree into intellectual authority.

## The minimap

The minimap is an orientation device, not a second analysis. It renders the current selected graph and the rectangular portion visible in the main canvas. Clicking or dragging in it recentres the main view while retaining the current scale.

## Navigation history

Back and forward refer to selected map foci in the current browser session. They do not alter browser history, data or curatorial state. A direct link still records the selected focus, layer and depth in the URL.

## Accessibility and restraint

The map keeps pointer, touch and keyboard routes. It respects reduced-motion preferences. Full-screen mode is optional. Typed statements, evidence and status remain available through the inspector rather than being encoded only through colour or position.

The map remains a view over a selective evidence graph. Smooth navigation does not make the graph complete, neutral or naturally divided into the neighbourhoods it currently displays.
