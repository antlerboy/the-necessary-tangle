# Specification gap register

Updated: 2026-08-14  
Baseline release: `0.16-grammar-connections-presentation-alpha`  
Baseline commit: `cc50bf8304d2e633f98133cefb9557bd88aa482d`

## Recovered specification

The Necessary Tangle is intended to be a versioned, multiplex evidence graph. Each public connection should make an inspectable claim: what the relationship is, its direction, why it is present, what supports it, what remains interpretive, and what alternative account or disagreement matters. It is not intended to be merely a taxonomy, encyclopaedia, reading list, social graph or decorative force-directed picture.

The recovered non-negotiables are:

- separate relation types rather than a generic “related to” edge;
- inspectable direction, wording, scope, status, sources and locators;
- multiple semantic layers, including conceptual, historical, human, practice, evidence and contestation;
- boundary rings and explicit scope;
- a visible distinction between source-established, interpreted and candidate claims;
- provisional communities rather than canonical schools;
- disagreement, tension and alternative accounts;
- systematic treatment of the named external and supplied internal corpora;
- question-shaped views that keep the full graph available without making it the default reading experience;
- a static, versioned public build with named human responsibility.

The current release already expresses much of this contract in its data model and item/connection views. The gaps below concern completeness, depth and usable access.

## Baseline scorecard

Scores are a five-point judgement anchored in the recovered specification, not a comparison with other knowledge sites.

| Dimension | Score | Evidence | Highest-priority gap |
| --- | ---: | --- | --- |
| Content | 3/5 | 496 readable public entries; 153 sources; 19 journeys | 225 entries remain thin; 80 of 110 reading-list items are inventory-only |
| Relationships | 3/5 | 1,712 typed edges; 1,161 reader statements; 747 semantic statements | Only 329 of 496 public entries have a semantic connection; locator precision is uneven |
| Interaction | 4/5 | Search, item views, inspectable connections, paths, sparse neighbourhood maps | No controversy comparison, time view or dependency inspection |
| Navigation | 4/5 | Question-led home, browse, journeys, map, ask and contribute routes | Coverage gaps and evidential depth are not a first-class reader route |
| Visual design | 4/5 | Strong hierarchy, restrained palette, coherent cards, usable responsive stacking | Map labels and edge semantics become small; full-map controls still demand expert attention |
| Contribution | 3/5 | Correction/contribution route and public issue trail | No schema-guided claim/source proposal flow or visible moderation state |
| Provenance | 2/5 | Every edge names at least one source ID and exposes epistemic fields | 446 edges have no locator; only 220 locators match a conservative page/section locator pattern |

## Gap register

### Content

| ID | Gap | Baseline evidence | Intended state | Priority | Status |
| --- | --- | --- | --- | --- | --- |
| C1 | Depth is concentrated in concepts and laws | 225 thin entries: 112 people and 108 publications account for 220 | Important people and works have several distinct, evidenced routes into concepts, practices, disagreements and lineages | P0 | Open |
| C2 | Reading list is mostly inventory | 29 developed, 1 represented and 80 inventory-only items | Work through each item or record a candid access/priority reason | P0 | Open |
| C3 | Principia coverage is a sample | Maintained note records a nine-entry first pass based on a small public source set | Traverse the internal dictionary, project structure and references with precise locators | P0 | Open |
| C4 | Time, institutions and events are sparse | Time fields exist, but no dedicated time view; only three organisation nodes | Historical claims can be followed through dated people, institutions, events and publications | P1 | Open |
| C5 | Practice evidence trails remain shallow | Practice family exists, but many method/skill nodes depend on classification or broad official pages | Theory → method → practice routes identify documented use and limits | P0 | Open |

### Relationships

| ID | Gap | Baseline evidence | Intended state | Priority | Status |
| --- | --- | --- | --- | --- | --- |
| R1 | Semantic isolation behind documentary connectivity | 496 reader-connected entries but only 329 semantically connected | Documentary authorship does not mask lack of intellectual/practice connection | P0 | Open |
| R2 | Broad rather than precise locators | 1,266/1,712 edges have any locator; 220 match the conservative precision pattern | Page, section, passage, slide, entry or stable fragment whenever available | P0 | Open |
| R3 | Generic relation vocabulary remains | Eight edges use `conceptually_related_to` or reader wording containing “related to” | Replace with the strongest supportable claim or remove | P0 | Open |
| R4 | Route diversity is weak | 189/496 entries have only one reader relation family; 72 have three or more | Important entities have several genuinely different routes | P0 | Open |
| R5 | Repetition can disguise depth | One repeated co-authorship assertion has the same pair/type/broad locator; 39 ordered pairs carry multiple statements | Distinguish multiple warranted claims with work-specific locators; merge duplicates | P1 | Open |
| R6 | Multiplex structure is encoded but not analysed | Relation families exist; communities remain provisional | Layer-specific community results, bridge audit and sparse question views | P1 | Open |
| R7 | Dependency semantics are not inspectable as a system | Dependency kinds exist on edges | A dependency DAG/cycle report distinguishes prerequisite, constraint and historical influence | P1 | Open |
| R8 | Disagreement is underrepresented | Contestation family has 12 edges; one edge is claim-status contested | Alternatives, tensions and contradictions are explicit where sources support them | P0 | Open |

### Interaction

| ID | Gap | Baseline evidence | Intended state | Priority | Status |
| --- | --- | --- | --- | --- | --- |
| I1 | Evidence strength is inspected one connection at a time | Connection views expose status and source data | Filter and compare established, interpretive, candidate and contested claims | P1 | Open |
| I2 | No controversy comparison | Contestation edges exist without a dedicated comparison view | Read competing claims, shared evidence and unresolved questions side by side | P1 | Open |
| I3 | No time-oriented interaction | Date fields exist but have no reader route | Follow intellectual lineages without confusing sequence with influence | P2 | Open |
| I4 | Map overview can exceed readable density | Full overview is explicitly framed as extent/gaps | Question-sized sparse layers with reasons for omitted edges | P1 | Developing |

### Navigation

| ID | Gap | Baseline evidence | Intended state | Priority | Status |
| --- | --- | --- | --- | --- | --- |
| N1 | Coverage and evidential gaps are not a first-class destination | About page provides narrative coverage; machine audits are repository-only | A public, current coverage/evidence dashboard linked from the main experience | P1 | Open |
| N2 | Theory-to-practice navigation is implicit | Some journeys and typed practice edges exist | Dedicated routes from idea → method → practice → evidence → limitation | P1 | Open |
| N3 | Deep corpora are not navigable as source trails | Corpus and source entries exist | Readers can follow a corpus contents traversal and the claims it supports | P1 | Open |

### Visual design

| ID | Gap | Baseline evidence | Intended state | Priority | Status |
| --- | --- | --- | --- | --- | --- |
| V1 | Map text is hard to read at overview scale | Desktop and mobile baseline screenshots | Semantic detail appears in a stable inspector while the canvas stays sparse | P0 | Developing |
| V2 | Mobile map is necessarily long | Controls, canvas and inspector stack correctly at 375px | Essential centre/layer controls remain close to the map; secondary controls collapse | P1 | Open |
| V3 | Status distinctions rely heavily on text | Claim labels are present in connection inspection | Established, interpreted and candidate connections are distinguishable without colour alone | P0 | Open |
| V4 | The magic dot must survive refinement | Bottom-right “Open updates” control is present | Preserve exact affordance and keyboard access | P0 | Protected |

### Contribution

| ID | Gap | Baseline evidence | Intended state | Priority | Status |
| --- | --- | --- | --- | --- | --- |
| K1 | Contribution is link-led rather than schema-led | Public contribute route and correction link | A proposer can name source, locator, direction, relation type, rationale and uncertainty | P1 | Open |
| K2 | Moderation lifecycle is not visible to readers | Review labels are present on accepted data; public issue trail exists | Proposed → reviewed → accepted/rejected/superseded states are inspectable | P1 | Open |
| K3 | Contribution authority needs a durable policy | Human curator is named | Governance, review thresholds and conflict handling are explicit | P1 | Open |

### Provenance

| ID | Gap | Baseline evidence | Intended state | Priority | Status |
| --- | --- | --- | --- | --- | --- |
| P1 | Source IDs overstate practical precision | 100% source-ID coverage; 73.9% locator presence; 12.9% precision-shaped locator text | Coverage reporting separates “source named” from “claim located” | P0 | Open |
| P2 | Source-established and inferred claims need stronger visual separation | Epistemic fields are complete in data and visible on inspection | The distinction is legible in lists and maps, not only deep inspection | P0 | Open |
| P3 | Corpus traversal evidence is uneven | Several collection/table-of-contents locators dominate | Record internal path, page/section and traversal scope for every corpus pass | P0 | Open |
| P4 | Public source links are not universal | 135 source records have public links; 18 do not | Preserve bibliographic provenance while clearly marking access limits | P1 | Open |
| P5 | Review recency is not surfaced as a coverage dimension | Reviewed-at fields exist | Readers can see stale, unreviewed and recently checked claims | P2 | Open |

## Pass 1 conclusion

The release is already a functioning public atlas rather than a prototype. The critical mismatch is not breadth or basic interaction; it is evidential depth. Documentary and collection structure currently make every public entry reachable while 167 entries still lack a semantic connection. The next pass therefore targets relationship quality before adding new breadth.
