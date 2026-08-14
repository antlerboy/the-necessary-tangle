# Overnight improvement log

Date: 2026-08-14  
Stop condition: six sequential passes or seven hours, whichever comes first  
Starting release: `0.16-grammar-connections-presentation-alpha`  
Starting main commit: `cc50bf8304d2e633f98133cefb9557bd88aa482d`

This is a maintainer record of measurements, bounded changes, validation, rendered inspection, regressions and uncertainty. A pass is not counted complete until its commit has passed checks, reached `main`, deployed successfully and been inspected on the live site.

## Preflight — recovery and baseline

### Recovered

- The original one-sentence vision and non-negotiables from `documentation/original-vision-audit.md`.
- Release history through 0.16, including the distinction between repository state, successful build state and live deployment.
- The maintained source/corpus coverage notes, reading-list inventory, Principia first pass, David Ing pass, SCiO coverage, relational-depth model and visual-map notes.
- The current live site, main branch, open issue programme and successful Pages/backup runs.
- The strongest older visual direction preserved in 0.16: editorial typography, warm restrained palette, composed cards, question-led home and bottom-right magic dot.

### Baseline measurements

- 496 public entries; 606 total nodes.
- 1,712 typed edges; 1,161 reader statements; 747 semantic statements.
- 496 reader-connected entries but only 329 semantically connected entries.
- 35 rich, 236 developing and 225 thin entries.
- 153 sources, of which 135 have public links and 18 do not.
- 110 reading-list items: 29 developed, 1 represented and 80 inventory-only.
- Every edge names a source ID and exposes epistemic fields.
- 446 edges have no locator; 220 locators match a conservative precision-shaped pattern.
- Eight generic relation targets and one repeated assertion group entered the review queue.
- Largest thin cohorts: 112 people and 108 publications.

### Baseline rendered inspection

- Desktop home: [screenshot](screenshots/overnight/baseline-desktop-home.png)
- Desktop map: [screenshot](screenshots/overnight/baseline-desktop-map.png)
- Mobile home, 375px: [screenshot](screenshots/overnight/baseline-mobile-home.png)
- Mobile map, 375px: [screenshot](screenshots/overnight/baseline-mobile-map.png)

The live home page has strong hierarchy and readable card composition at desktop and mobile sizes. The mobile map stacks controls, canvas and inspector in a usable order, but the page is long and the graph labels are small. The bottom-right “Open updates” magic dot is present and keyboard-addressable.

### Operational constraint

The review environment did not provide a working local HTTPS git transport. Repository changes, pull requests, checks and merge gates therefore use GitHub's authenticated API; build and deployment evidence comes from GitHub Actions, and rendered evidence from the live site. This changes the mechanics, not the publication gate.

## Pass 1 — specification recovery

Status: complete and live.

### Previous findings read

Original vision audit, relational depth, explicit semantics, data model, visual map, source-mining notes, reading-list coverage, Principia first pass, David Ing release notes and publishing method.

### Measured current state

See the baseline above and `data/relationship-quality.json`.

### Bounded improvement

- Established a public specification gap register across content, relationships, interaction, navigation, visual design, contribution and provenance.
- Established a machine-readable relationship-quality baseline with criteria, weak-edge queue, repetitive-assertion queue, thin cohorts and limitations.
- Established this sequential log and a morning change list.
- Captured representative desktop and mobile baseline evidence.

### Build and test

Validation run 31839692364 succeeded. PR #38 merged to `main` as `9e4159d0c70217bbaea78ed479b065423166861d`. Pages run 31839752373 and content-backup run 31839752411 both succeeded.

### Rendered inspection

Baseline live views were inspected before and after deployment at desktop and 375px mobile widths. The pass changed documentation and audit artifacts only; no product-rendering regression was observed. The committed baseline mobile-map image was also fetched from the live domain.

### Improved

The original vision is now converted into falsifiable checks and prioritised gaps. “Source named” is separated from “claim located”, and documentary reachability is separated from semantic depth.

### Regressed

No product surface change is intended in this pass. Repository size increases because screenshot evidence is retained.

### Uncertain

The conservative locator-pattern count can undercount precise named-entry locators and overcount weak section wording. It is a review aid, not a claim-quality verdict.

## Pass 2 — relational architecture

Status: complete and live.

### Previous findings read

Pass 1 gap register, relationship audit and machine-readable queue.

### Measured current state

All 496 public entries were re-audited through the per-node relational-depth record. Baseline review targets were eight generic edges and one repeated assertion group.

### Bounded improvement

- Replaced all eight generic targets with narrower, typed and directed claims grounded in the cited page, abstract, README or internal section.
- Added two public source records for the Stacey institutional abstract and Mowles author explanation.
- Replaced the Natural drift → Viability resemblance with an explicit tension between primary mechanism claims.
- Replaced the Murmurations → complex responsive processes resemblance with the narrower official journal-scope claim.
- Gave two co-authorship assertions work-specific locators.
- Added an idempotent final build overlay and regenerated the machine audit for clean-build reproducibility.

### Build and test

The first validation run, 31840708806, correctly failed because a derived AI-observation metric was stale. The overlay was repaired to regenerate that metric. Validation run 31840893303 then succeeded. PR #39 merged to `main` as `3e1c923ef8995a60a882e6f02ccfebc4ed1858c2`. Pages run 31840949307 and content-backup run 31840949277 both succeeded.

### Rendered inspection

The cache-busted live Viability and Natural drift item views were inspected after deployment. The precise public phrases were present, the retired generic phrases were absent, navigation remained usable and the bottom-right Open updates dot remained present.

### Improved

Generic review targets fall from eight to zero; repeated groups from one to zero; directed edges rise from 1,610 to 1,617; conservative precision-shaped locators rise from 220 to 231.

### Regressed

Semantic connectivity falls from 329 to 328 and substantive edges from 750 to 749 because the official Murmurations page supports a documentary scope claim, not the former semantic resemblance. The thin cohort remains 225.

### Uncertain

The Stacey emergence edge remains explicitly interpreted and provisional. It is narrow to organisational knowledge; it should not be read as a general theory of emergence.

## Pass 3 — external corpus

Status: complete and live.

### Previous findings read

Pass 2's decision rule, reviewed replacements, remaining thin cohorts and the machine-readable priority queue.

### Measured current state

The graph began this pass with 1,712 edges, 155 public source records, 225 thin entries, 35 rich entries and 72 entries with at least three reader relation families. The reading-list inventory contained 110 items: 29 developed, one represented and 80 inventory-only.

### Bounded improvement

- Traversed eight internal Principia pages, David Ing's publication and digest routes, the supplied 110-item reading inventory, and six substantial comparison archives.
- Added a nine-corpus machine traversal record with page routes, reference trails, relationship decisions, disagreements and uncertainties.
- Added eleven public source records and repaired the Complexity Explorer and reading-list records.
- Added eight typed, directed and located edges; strengthened six existing edges.
- Deliberately added no semantic edge from the Ashby, ISSS or reading-list traversals because index co-occurrence, meeting co-presence and titles were insufficient warrants.

### Build and test

The clean local reconstruction and all maintained Python validators passed after one useful rejection: the validator refused six newly coined relation types. They were remapped to the project's controlled vocabulary while preserving their more precise human-readable phrases. JavaScript syntax checks passed. Validation run 31843713399 then succeeded. PR #40 merged to `main` as `5483611fc0ebcf5c2e71ea5c008694bc07b639b0`. Pages run 31843781768 and content-backup run 31843781744 both succeeded.

### Rendered inspection

The Self-organisation and Pattern Manual item views were rendered at 1,440px desktop and 375px mobile widths. The two new feedback-mechanism statements appear in the Self-organisation view, the item drawer remains readable, no horizontal overflow was observed, navigation remains available and the Open updates magic dot remains present.

The same checks were repeated against the cache-busted live Self-organisation item after deployment. Both feedback-mechanism phrases were present, generic relation wording was absent, desktop and mobile had no horizontal overflow, and the magic dot remained present.

- [Desktop Self-organisation](screenshots/overnight/pass3-desktop-self-organisation.png)
- [Mobile Self-organisation](screenshots/overnight/pass3-mobile-self-organisation.png)
- [Desktop Pattern Manual](screenshots/overnight/pass3-desktop-pattern-manual.png)
- [Mobile Pattern Manual](screenshots/overnight/pass3-mobile-pattern-manual.png)

### Improved

- Edges: 1,712 to 1,720.
- Sources: 155 to 166.
- Thin / rich: 225 / 35 to 224 / 36.
- Entries with at least three reader relation families: 72 to 74.
- Conservative precision-shaped locators: 232 to 244.
- Evidence bands move from 188 supported / 195 mixed / 113 provisional to 193 / 192 / 111.

### Regressed

The graph gains eight statements and therefore adds visual and review load. Semantic reach remains 328 rather than being inflated by the archive traversals. No additional isolated entity was connected merely to improve the count.

### Uncertain

The SFI emergence framing and the IFSR convening example remain explicitly interpreted. The ASC feedback-history edge remains provisional until a primary Wiener page locator replaces the publisher-level reference. Eighty reading-list items remain inventory-only.

## Pass 4 — internal corpus

Status: complete and live.

### Previous findings read

Pass 3's external traversal decisions, no-edge decisions, uncertainty register and current machine relationship-quality result.

### Measured current state

Eighteen non-public source records were in scope: six supplied author decks, five earlier author syntheses or lectures, six legacy SCiO/framework records, and one permission-limited discovery image. They are cited 501 times across the graph, including 412 substantive citations, but only 34 of those citations have slide-, page-, section- or chapter-shaped locators. The six supplied decks already supported 17 direct slide-level crosswalk statements.

### Bounded improvement

- Added an 18-record machine-readable internal-corpus audit with evidence class, access, citation counts, review decision and uncertainty.
- Replaced the uniform boilerplate on all 17 supplied-deck relationships with claim-specific rationales and material-specific scope conditions.
- Normalised seven degraded slide-range locators.
- Marked the duplicate Core Thinking Integration title as one intellectual source rather than independent corroboration.
- Kept the outcomes presentation documentary-only and the Perko network image discovery-only.
- Added no new edge where only a broad internal register or visual proximity was available.

### Build and test

The final overlay, graph snapshot, public-knowledge build, all maintained Python validators and JavaScript syntax checks passed locally. PR #41 merged to `main` as `fa7af2c065f81134831c78be615af99ea3c22003`; validation run 31844817948, Pages run 31844888250 and content-backup run 31844888259 all succeeded.

### Rendered inspection

The Ladder of inference item was rendered at 1,440px desktop and 375px mobile widths. Both reviewed public phrases are visible, the connection drawer remains readable, no horizontal overflow was observed and the Open updates magic dot remains present.

- [Desktop Ladder of inference](screenshots/overnight/pass4-desktop-ladder-of-inference.png)
- [Mobile Ladder of inference](screenshots/overnight/pass4-mobile-ladder-of-inference.png)

### Improved

All 18 internal records now state what was actually inspected and what remains inaccessible. The 17 supplied-deck claims now explain their warrant individually rather than sharing one generic caveat. The audit makes the mismatch between 501 citations and only 34 precision-shaped locators visible.

### Regressed

No structural graph metric changes. The machine-readable payload grows, and the public graph still carries many generated comparisons which cite broad internal registers.

### Uncertain

Readers cannot open the non-public originals. The SCiO CF Resources draft, legacy Feedback deck and legacy Recursion deck are cited by many generated comparisons without claim-level locators. Those citations remain provenance debt, not independently supported claims.

## Pass 5 — experience and visual improvement

Status: bounded change prepared; publication gate pending at the time of this record.

### Previous findings read

Pass 4's internal-provenance debt, the original visual specification, the current stylesheet, and the strongest older visual milestones: `e498d91` (coherent visual foundation), `6f7bb7b` (responsive map grid) and `cc50bf8` (map above the fold).

### Measured current state

The current release retains the strongest older typography, palette, spacing, card composition, responsive collapse and magic dot. Desktop and 390px mobile map renders had no horizontal overflow. Provisional connections were already dashed, but connection rows did not expose whether a claim was asserted, interpreted, inferred, inherited or still a candidate until it was opened.

### Bounded improvement

- Added compact evidence-basis badges to map and full-entry connection rows.
- Distinguished source-established and sourced assertions from curatorial interpretation, editorial synthesis, inference, candidate and inherited records.
- Added the stored assertion mode and exact claim-level source locator to the opened connection view.
- Kept the graph canvas, typography, spacing, responsive rules and bottom-right Open updates dot unchanged.
- Added an idempotent interface patch, eight-check validator and `documentation/experience-visual-audit.md`.

### Build and test

The entire data and site pipeline was reconstructed from its source layers. All maintained Python validators, the new Pass 5 validator, and JavaScript syntax checks passed. The clean build retained 496 entries, 1,720 edges, 166 sources and the Pass 3/4 corpus audits.

### Rendered inspection

The reference release and current Self-organisation map were rendered at 1,440px desktop and 390px mobile widths. The changed connection list and opened connection inspector were then rendered at both widths. Text badges remain legible without relying on colour; the locator is visible on mobile; no horizontal overflow or page error was observed; and the Open updates magic dot remains present.

- [Older visual reference](screenshots/overnight/pass5-reference-desktop-map.png)
- [Before, desktop](screenshots/overnight/pass5-before-desktop-map.png)
- [After, desktop](screenshots/overnight/pass5-after-desktop-map.png)
- [After connection inspection, desktop](screenshots/overnight/pass5-after-desktop-connection.png)
- [Before, mobile](screenshots/overnight/pass5-before-mobile-map.png)
- [After, mobile](screenshots/overnight/pass5-after-mobile-map.png)
- [After connection inspection, mobile](screenshots/overnight/pass5-after-mobile-connection.png)

### Improved

Relationship epistemics are visible before a reader opens an edge, and the detailed view now exposes the claim locator rather than only the source card. The richer relational data becomes more inspectable without adding lines or labels to the map itself.

### Regressed

Connection lists are taller because every row gains one compact badge. On a 390px viewport this adds scrolling, although it does not add horizontal overflow or obscure controls.

### Uncertain

The badges translate maintained fields; they do not independently validate claims. A `Sourced assertion` can still have a broad locator, which is why the verbatim locator remains part of the detailed view.

## Pass 6 — adversarial review and refinement

Status: not started.
