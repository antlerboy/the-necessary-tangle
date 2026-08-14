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

Status: bounded change prepared; publication gate pending at the time of this record.

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

Pending branch validation. The pass cannot be marked complete until validation, merge, Pages deployment and live inspection succeed.

### Rendered inspection

Pending deployment. Affected item and connection views will be inspected at desktop and 375px mobile widths.

### Improved

Generic review targets fall from eight to zero; repeated groups from one to zero; directed edges rise from 1,610 to 1,617; conservative precision-shaped locators rise from 220 to 231.

### Regressed

Semantic connectivity falls from 329 to 328 and substantive edges from 750 to 749 because the official Murmurations page supports a documentary scope claim, not the former semantic resemblance. The thin cohort remains 225.

### Uncertain

The Stacey emergence edge remains explicitly interpreted and provisional. It is narrow to organisational knowledge; it should not be read as a general theory of emergence.

## Pass 3 — external corpus

Status: not started.

## Pass 4 — internal corpus

Status: not started.

## Pass 5 — experience and visual improvement

Status: not started.

## Pass 6 — adversarial review and refinement

Status: not started.
