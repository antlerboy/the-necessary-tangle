# Original vision audit

Status at release `0.16-grammar-connections-presentation-alpha`, 14 August 2026.

This audit compares the current public atlas with the original commissioning conversation and the v0.1 specification/package. It is a delivery test, not a new vision.

## The vision in one sentence

The Necessary Tangle is meant to be a versioned, multiplex evidence graph of systems | cybernetics | complexity in which every line says exactly what it claims, why it is present, how well it is supported and which alternative account might challenge it.

It is not primarily a taxonomy, encyclopaedia, reading list, social graph or attractive force-directed picture. Those may be useful views over the same maintained evidence graph, but none of them is the underlying model.

## Non-negotiable design commitments

The original specification requires the project to:

1. Keep different kinds of connection separate. Conceptual dependence, historical sequence, explicit influence, teaching, mentoring, collaboration, citation, institutional participation, practical use, identity claims, current discourse and challenge must not collapse into `related to`.
2. Make each statement inspectable. Direction, wording, scope, confidence/status, sources and evidence locators must answer “why is this line here?”.
3. Hold more than one map at once. Logical structure, historical transmission, practice, institutions, people and discourse are layers of one tangle, not rivals for a single canonical layout.
4. Make boundaries explicit. Rings 0, 1 and 2 express editorial scope; they do not claim that the field has a natural edge.
5. Distinguish espoused identity from observed proximity. What people call themselves and what graph structure suggests are different observations.
6. Treat categories as provisional and release-specific. Communities should be compared across layers, algorithms and resampled graphs; they are not eternal schools.
7. Represent contestation. Competing definitions, disputed influence, criticism and boundary challenges belong in the graph rather than being edited into false agreement.
8. Include the mandated seed corpora without turning them into isolated lists: the 33 *Grammar of Systems* laws and principles, its nine patterns, systems-practice and SCiO material, and the named source archives and comparison maps.
9. Generate question-shaped views: one- and two-degree neighbourhoods, chronological family trees, strict dependency graphs, practice-to-concept routes, institutional/event histories, people paths, clusters and coverage diagnostics.
10. Remain cheap, static, versioned and publicly inspectable, with human editorial responsibility and a challenge workflow.

## Delivery assessment

| Original capability | Current state | Assessment | Work needed |
|---|---|---|---|
| Stable typed evidence graph | Public nodes, canonical redirects, typed directed edges, relation families, statuses, scope conditions, sources and evidence records exist | Strong foundation | Enforce page- or passage-level locators on interpretive and high-consequence statements |
| No generic association as public meaning | Legacy unresolved associations are separated and hidden from normal reader layers | Substantially achieved | Retire or resolve the remaining legacy records rather than carrying them indefinitely |
| Boundary rings 0/1/2 | Stored on entries and documented | Achieved in data; quiet in the interface | Add a coverage view which explains inclusions, exclusions and boundary challenges |
| Multiple semantic layers | Conceptual, historical/human, practice, contestation and provenance filters exist | Partly achieved | Increase sparse human, institutional, event and documented-use relations; make each layer a useful view in its own right |
| Inspectable evidence trail | Entry and edge inspectors show status, scope and sources | Partly achieved | Fill missing locators and evidence records; expose evidence quality and unresolved challenge more consistently |
| 33 Grammar laws plus nine patterns | All 33 laws and nine patterns are present; release 0.16 adds accepted book membership and 178 provisional semantic crosswalk statements | Structurally repaired, evidential review open | Review every crosswalk, add precise locators, record alternative formulations and add explicit criticism where warranted |
| Search and question-sized navigation | Fuzzy search, entry drawer, one/two-step maps, path finding and guided journeys exist | Strong usable baseline | User-test terminology and starting routes with readers outside the core community |
| Chronological family tree / historical streams | Historical relations exist but no dedicated time view | Missing flagship view | Build a dated, filterable lineage view which distinguishes sequence from evidenced influence |
| Strict conceptual dependency DAG | Dependency types exist but no dedicated acyclic dependency view or cycle report | Missing flagship view | Define allowed dependency relations, surface cycles as errors or disputes, and render prerequisite/dependent paths |
| Theory → method → practice view | Relevant nodes and some practice edges exist | Partial and too sparse | Add documented cases, teaching and use relations, then provide a purpose-built cross-layer view |
| Institution and event histories | Organisations and events exist | Sparse | Research laboratories, societies, conferences, programmes and publication venues as transmission infrastructure |
| People paths and practitioner constellations | General paths and some rich profiles exist | Partial | Deepen teaching, mentoring, collaboration and co-practice evidence, especially around practitioners named in the source material |
| Espoused versus observed comparison | Espoused labels and observed-cluster fields exist | Not delivered as analysis or interface | Compute and present discrepancies without implying that either view is the truth |
| Multiplex community detection | One provisional unweighted partition is present | Below specification | Run layer-specific Leiden and Infomap comparisons, resampling/stability checks and release-to-release change reports |
| Controversy maps | Status and contestation relations are supported | Thin and no dedicated view | Add rival definitions, critiques, rebuttals and disputed priority/influence claims with a controversy-centred view |
| Coverage dashboard | Counts, reading-list depth and a coverage programme exist | Partial | Publish source, entity, layer, boundary, locator and review-depth diagnostics rather than headline totals alone |
| Archive and comparator ingestion | Registers and issues exist for several named corpora | Programme defined, much not mined | Treat every named corpus as an item-level research field: follow relevant substantive content, extract locatable typed statements and connect it across the graph; complete Foundational Papers, Principia Cybernetica, David Ing's public work, the curator's reading list, relevant Monoskop material, SysCoI/model.report and prior maps/BoKs |
| Governance and challenge | Contribution routes, statuses, documentation and curator-controlled release exist | Useful baseline | Add named stewardship, review queues, decision records and service expectations as participation grows |
| Static, reproducible publication | Plain HTML/CSS/JS, generated public data, validation and GitHub Pages deployment | Achieved | Keep builds deterministic and add regression checks for the reader interface as well as data |

## What release 0.16 repairs

The Grammar principles appeared disconnected because almost every law had only two administrative edges: membership of a corpus and attribution to a source. The default entry view then removed documentary/classification edges, leaving no reader-visible connection at all. That was a data-depth problem compounded by a presentation filter.

Release 0.16 makes three deliberate changes:

- the *Grammar of Systems II* publication now has an accepted `presents` statement to every one of the 33 laws and principles;
- every law has multiple public conceptual, law-to-law and/or practice connections, with explicit phrases and scope conditions; these 178 crosswalk statements are provisional interpretations, not invented claims of historical influence or formal equivalence;
- full entries show meaningful public-to-public documentary statements as well as the narrower “substantive” map layer, and a new guided journey demonstrates the Grammar as a web through all nine patterns.

The repair now extends beyond the Grammar. Relational depth is calculated for every canonical public entry, with structural breadth kept separate from evidential strength. All 496 entries have at least one reader connection; the first enrichment cohort gives every maintained intervention skill and the previously isolated concept, method, tool and tradition entries multiple typed routes. The remaining thin queue is concentrated overwhelmingly in people and publications, where authorship alone is not enough and historical, institutional, influence and practice claims require item-level research. See [the relational-depth programme](relational-depth.md) for the live measurements and cohort method.

The release also restores missing presentation primitives for metrics, chips, grids, filters, entry cards and the entry drawer. The discreet update dot remains fixed at the bottom right.

## Ordered work to reach the original vision

### 1. Harden the Grammar repair

Treat the new crosswalk as a visible review queue. For each statement, add a page/section locator, decide whether the relation type and direction survive review, and record rival accounts or criticism. Completion means that all 33 laws retain several useful connections without relying on uncited curator inference.

### 2. Deliver the original flagship views

Build dedicated views in this order:

1. strict conceptual dependencies, including cycle detection;
2. dated historical streams and family trees;
3. theory → method → practice and documented cases;
4. institutions/events as transmission infrastructure;
5. controversies and alternative accounts;
6. espoused identity versus observed proximity;
7. a coverage and evidence-depth dashboard.

Each view must be a filter or projection of typed statements, never a new source of implied relationships.

### 3. Deepen the evidence graph where the views expose gaps

Prioritise bridge concepts and heavily visited paths, then teaching/mentoring/collaboration, institutions/events and actual use in practice. Complete the named archive and comparator passes. Prefer a smaller number of locatable, scoped statements to a larger mass of suggestive lines.

### 4. Implement proper multiplex analysis

Run community detection per relation layer and across declared multiplex combinations. Compare Leiden and Infomap results, resample edges according to confidence, report stability and preserve release-specific results. Observed clusters should be presented alongside—not substituted for—espoused affiliations and historical traditions.

### 5. Mature governance and release quality

Give challenges, corrections and disputed statements visible states; add named reviewers/stewards where possible; record decisions; and test the interface at desktop/mobile widths, in both themes, on each release. Data validation alone is insufficient when a missing CSS primitive can make valid content effectively inaccessible.

## Definition of the original vision being met

The original vision is credibly achieved when a reader can choose any important proposition and move, with inspectable evidence, among its logical prerequisites, historical development, human and institutional transmission, practical use and live disputes; compare that account with alternative boundaries and clusters; and understand exactly which parts are sourced, inferred, challenged or still missing.

Node count is not the acceptance test. Traceable meaning across multiple views is.
