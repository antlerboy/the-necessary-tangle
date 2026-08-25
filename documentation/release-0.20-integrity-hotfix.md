# Work ticket: release 0.20 integrity hotfix

Status: **Ready for review**

Owner: **Benjamin P Taylor**

Human review point: **Review the pull request before merge and publication.**

## Outcome

The deployed Surprise-me route works for fresh and legacy links, and the public
AI observations state the findings specific to the release 0.20 comparator pass.

## Reader or user effect

Readers reach a random entry without an avoidable Browse render or stale script,
and can inspect what the three prior maps reveal rather than seeing a relabelled
0.18 observation set.

## Primary deliverable

A focused release-integrity pull request against release 0.20.

## In scope

- give the corrected Surprise-me asset a new cache key;
- normalise legacy `from=surprise` hashes before the main router runs;
- add comparator-specific AI observations to the maintained and public data;
- replace the stale public “Updated for 0.18” notice;
- add regression checks for all four corrections.

## Out of scope

- further comparator ingestion or canonical relation promotion;
- wider interface, visual or performance redesign;
- changing the release 0.20 evidence and rights boundaries.

## Named files or areas

- `docs/assets/iteration-18.js`
- `docs/index.html`
- `data/public-data.json`
- `docs/assets/public-data.json`
- `docs/assets/public-data.js`
- `documentation/ai-observations.md`
- `scripts/apply_prior_maps_20.py`
- `scripts/validate_iteration_18.py`
- `scripts/validate_prior_maps_20.py`

## Sources and context

- Required: release 0.20 generated data and the deployed reader assets.
- Web research: **Not needed**.

## Constraints

- Follow `documentation/DESIGN_AND_CONTENT_RULES.md`.
- Preserve every comparator layer separately from canonical atlas relations.
- Preserve genuine-link behaviour for modified click, copy and new tabs.

## Acceptance checks

- [x] A legacy `#view=item&...&from=surprise` hash is normalised to `from=home`
  before the main application router runs.
- [x] The release HTML requests the corrected script with a new cache key.
- [x] The public AI page contains four release-0.20 comparator observations.
- [x] `make build`, `make validate` and `git diff --check` pass.
- [ ] Human review occurs before merge or publication.

## Stop conditions

- Stop when the acceptance checks pass.
- Stop if the correction requires changing any comparator evidence or rights
  decision.
- Maximum execution: one implementation pass, one verification pass and one
  corrective pass tied to a failed check.

## Route and model

- Surface: **Codex**
- Model: **Terra**
- Reason: bounded debugging, generated-data propagation and regression testing.
- Escalation: **None**.

## Durable update

Update the changelog, state record and this ticket's completion report.

## Completion report

- Outcome: the two release-integrity defects are corrected in a reviewable
  branch.
- Files changed: reader route/cache asset, generated AI-observation projections,
  release documents, generating script and validators.
- Checks run: `make build`, `make validate`, `git diff --check`, JavaScript syntax
  check and a focused legacy-hash normalisation test.
- Residual risks or deferred items: production click-through follows deployment;
  the cloud test browser could not open a tab during diagnosis.
- Exact next decision: human review, then merge and verify the deployed asset key,
  legacy route and AI-observation page.
