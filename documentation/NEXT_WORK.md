# Next work

Status: **Candidate prepared; human review required before merge or publication**. Requested by Benjamin P Taylor on 5 September 2026.

## Outcome

Release 0.22: a richer, source-accounted atlas and an accessible systems-thinking entrance, with the RedQuadrant rules preserved for reuse.

## In scope

- Fully account for the two September source posts in running feedback issue #2, including every available bibliographic entry and explicit gaps in the supplied source material.
- Reconcile bibliographic identities, deepen source-supported entries and typed connections, and add readable routes through the historical material.
- Build `docs/systems-thinking/index.html` as the canonical educational gateway for systemsthinking.info.
- Remove the random RedQuadrant rule from the atlas header; preserve the 256 rules, page, and reusable code; add concrete handoffs to RedQuadrant and antlerboy.com update streams.
- Correct release consistency, accessible navigation, source discoverability, and independent public copy within the affected reader surfaces.

## Named files or areas

- `sources/cybernetics-bibliographies/`, `scripts/apply_release_22.py`, `scripts/validate_release_22.py`.
- `data/public-data.json`, generated public assets, knowledge, and graph snapshots.
- `docs/systems-thinking/`, `docs/corpora/early-cybernetics/`, `docs/little-redquadrant-rules/`, and relevant reader scripts/styles.
- `Makefile`, current workflows, release documents, state, and feedback ledger.

## Acceptance checks

- Every available bibliography entry is retained with its source, section, reconciliation, and review status. Bibliographic inclusion never becomes an influence claim.
- No unseen paper is represented as read; no missing bibliography pages are invented.
- Intro page works without JavaScript and provides keyboard-accessible links, readable type, responsive layout, and stable destinations.
- All 256 rule texts and stable rule anchors survive; header randomiser is disabled; reusable component works independently.
- Existing comparator files and source-owner review boundaries are preserved.
- `make build`, `make validate`, JavaScript syntax, internal-link validation, and focused interaction checks pass.
- Human review before merge or publication.

## Out of scope

Unreviewed changes to Hadorn’s approved comparator, publication of private material, DNS changes without a resolved account, and claiming completion of the open-ended corpus programme.

## Stop conditions

Stop at a validated reviewable pull request. Record any inaccessible primary source explicitly.

## Model route

Repository implementation in Codex. Research is captured in the bounded source intake; no additional agent work is needed.

## Durable update

Update the release account, feedback ledger, current state, and next action after verification.
