# Release 0.18: navigable tangle

Release: `0.18-navigable-tangle-alpha`  
Generated: `2026-08-23`  
Public site: https://transduction.systems/

## Outcome

Make the atlas genuinely navigable from search result to entry to map, then incorporate the complete set of post-0.17 feedback without hiding unfinished scholarship.

## Reader-visible changes

- Entries open as a full-screen reading surface rather than a narrow right-hand strip.
- Connections are hoisted directly beneath the definition and summary.
- The map occupies most of the available screen and can be panned from nodes, connections or empty space; a movement threshold distinguishes dragging from selecting.
- ‘Constellation’ view places the selected entry at the centre, direct relations in an inner orbit and two-step relations in an outer orbit. This is question-relative placement, not a ranking of intellectual worth.
- Navigational cards, search suggestions, map nodes, map connections, entry actions and ‘Surprise me’ expose stable links which can be copied or opened in a separate tab.
- The brand mark is a tangle rather than the previous half-star/back-arrow form, and ‘Surprise me’ inherits the site typeface.
- The requested front-page sentence and ‘Find out more about how this works’ route are present.

## Content and source work

- Linda Booth Sweeney, *The Noisy Puddle* and *Do Bees Pee?* have source-backed profiles and typed connections. The Massachusetts Center for the Book establishes the 2025 picture-book award; the author's current publication notice establishes the June 2026 publication date for *Do Bees Pee?*.
- All 32 concepts in Jurgen Appelo's unFIX synthesis resolve to canonical entries. Documentary inclusion is recorded without treating the source's AI-assisted list or scores as a settled canon.
- 37 requested people and institutions are canonicalised and searchable: 3 developed, 3 represented more briefly and 31 left visibly in the research queue rather than padded with unsupported claims.
- Search aliases include Donna/Donella Meadows, Russ/Russell Ackoff and the supplied misspellings.
- Isolated ‘Damian’ references are expanded to Damian Allen and public-facing prose is scanned for wording which depends on an unseen prompt or conversation.
- AI observations are regenerated for the current graph and the new interaction model.

## Acceptance checks

- `make validate` completes the full historical build and all release validators.
- JavaScript syntax checks pass for the base application and both release overlays.
- Every unFIX concept resolves to a public canonical node.
- Every named item resolves to a public node and exposes actual depth.
- Navigational interactive elements have stable `href` targets; action buttons remain buttons.
- All internal item targets and redirect targets resolve.
- Public output contains no isolated `Damian` reference or banned hidden-conversation phrase.
- Desktop and mobile Playwright smoke tests can pan the map, open a full-screen entry and follow a right-clickable route.

## Deliberate limits

This release completes the submitted tasks as interface, indexing, source and audit work. It does not claim that every named thinker now has an equally deep scholarly profile, nor that the Monoskop, SysCoI, reading-list, Foundational Papers and company-knowledge programmes are exhausted. Those remain measured research programmes rather than invisible promises.
