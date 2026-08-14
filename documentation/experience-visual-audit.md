# Experience and visual audit

Date: 2026-08-14  
Pass: 5

## Reference comparison

The strongest older visual milestone is `e498d91`, **Restore the coherent visual foundation**. It established the current serif-led hierarchy, restrained cream/red palette, card composition, control spacing, responsive single-column collapse and bottom-right updates dot. The later map-alignment releases `6f7bb7b` and `cc50bf8` improved layout without replacing that system.

A file-level comparison and rendered desktop inspection found that the current release retains that foundation. The current stylesheet is materially the same in the typography, panels, drawers and responsive rules; restoring an older stylesheet would remove later map and accessibility repairs without recovering a lost visual quality.

Reference renders:

- `docs/screenshots/overnight/pass5-reference-desktop-home.png`
- `docs/screenshots/overnight/pass5-reference-desktop-map.png`

## Measured current experience

- Desktop map: three-column control / canvas / inspector composition at 1,440px.
- Mobile map: single-column collapse at 390px with no horizontal overflow.
- Map lines already distinguish provisional statements with dashes.
- The full entry and edge inspector already expose claim status and sources.
- The map's connection list did not expose assertion basis until a reader opened each edge.
- The bottom-right **Open updates** magic dot is present in both desktop and mobile renders.

## Bounded improvement

Pass 5 adds a compact evidence-basis badge to each map and full-entry connection row. The badge distinguishes:

- source-established or sourced assertions;
- curatorial interpretation or editorial synthesis;
- inferred or candidate connections;
- inherited or otherwise maintained records.

The opened connection view now shows the stored assertion mode and the exact claim-level source locator, or says explicitly that no locator is recorded. A short key explains the badges; the graph canvas gains no new labels or edges.

## Design decision

This is disclosure-on-demand rather than an attempt to render all provenance on the canvas. It strengthens evidence legibility while preserving the sparse neighbourhood view, typographic hierarchy, card composition and magic dot.

## Remaining uncertainty

The labels faithfully translate maintained data fields; they do not independently prove a claim. A `Sourced assertion` can still have a broad locator, which is why the detailed view exposes the locator verbatim. Colour is supplementary: every badge has text, and provisional graph lines remain dashed.
