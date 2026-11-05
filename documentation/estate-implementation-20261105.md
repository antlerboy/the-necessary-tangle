# Readable atlas implementation

Status: implemented and locally verified, 5 November 2026. New copy has been reviewed against the user-selected writing references and current writing instructions. Publication is authorised by the coordinating estate task after the checks pass.

Owner: Benjamin P Taylor. This packet follows the user's authorisation to implement the web-estate recommendations, excluding independent teaching review. It supersedes the previous completed packet for this bounded change. Publication follows the coordinating task’s authorisation after verification.

## Outcome

Existing developed entries and reading journeys can be read, cited, and reused through stable ordinary web pages, with practical home entrances and preserved evidence distinctions.

## In scope

`scripts/build_readable_atlas.py`, its validator and browser checks, `Makefile`, generated `docs/entries/`, `docs/journeys/`, `docs/stewardship/`, home entrance cards, `docs/assets/readable-atlas.css`, the entry/journey actions in `docs/assets/app.js`, sitemap, and the existing validation/publication workflows. The input is the existing public projection. No new corpus research is needed.

## Out of scope

Independent teaching review, new reviewers or appointments, new evidence claims, altered graph status, external correspondence, event collection changes, new account access, and uncoordinated publication.

## Acceptance checks

- Every public developed profile and maintained journey has a stable HTML page and canonical URL.
- Pages retain sources, locators, recorded review status, interactive routes, and the fixed updates dot.
- Sourced JSON exports contain original atlas data and source metadata, with no third-party evidence excerpts.
- Internal links, sitemap coverage, and deterministic rebuild pass.
- Full `make validate` equivalent, and desktop/mobile checks of changed reader paths.

## Stop conditions

Stop once the acceptance checks pass. Fix only named failures. Do not infer independent review or publish without coordination.

## Model route

Codex implementation; use the current task model. No model change or fresh research is required.

## Verification completed

- The complete `make validate` command sequence passed through a Windows runner because GNU make is absent. The run resumed at the named 0.19 check after the existing ffprobe directory was added to PATH; no failed check was skipped.
- `scripts/validate_readable_atlas.py` passed for 220 developed entries, 27 journeys, internal links, canonical URLs, sitemap, review-status preservation, excerpt exclusion, proper JSON arrays, and idempotence.
- `scripts/validate_public.py` passed after the new layer: 1,295 canonical public entries, 220 profiles, 827 sources, 3,154 edges, and 27 journeys.
- `scripts/validate_work_spine.py` passed all 23 checks.
- `scripts/test_readable_atlas_browser.js` passed at 1,440 px and 390 px, including JavaScript-disabled reading, keyboard entry, mobile containment, sourced downloads, practical home links, and interactive-to-readable links. Desktop and mobile screenshots were inspected.
- JavaScript syntax checks passed. The canonical dataset and its public projection have no changes. Unrelated rebuild cache hashes, cross-platform churn, and missing companion-state prose were restored to the checked-out baseline.

## Copy review completed

The new wrapper copy was reviewed against the two writing records selected by the user, with the current writing instructions taking precedence. Headings now describe the material directly. Actions identify what a reader can do; responsibility identifies the curator, contributors, maintainers, and the checks they use. The reading entrance no longer claims general reliability. Existing profile, journey, source, claim, and evidence prose remains unchanged.

The copy lives in `scripts/build_readable_atlas.py`; generated pages and matching browser assertions are updated from it. The publication task is authorised to push after the final checks and verify the resulting deployment.

The original Benjamin writing style skill was subsequently supplied and read. The new wrapper copy needs no organisation-name corrections under its naming rule. Exact original source titles, records, and profile text are preserved.

The browser runner now closes its own persistent HTTP connections during teardown. Local assertions also ran against a newer installed Chromium; the publication workflow installs the browser version matching its pinned Playwright runner.
