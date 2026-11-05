# Readable atlas implementation

Status: implemented and locally verified, 5 November 2026. Publication is held pending the exact Benjamin writing-style skill pass and coordination with the estate task.

Owner: Benjamin P Taylor. This packet follows the user's authorisation to implement the web-estate recommendations, excluding independent teaching review. It supersedes the previous completed packet for this bounded change. Publication is held for coordination with the parent task.

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

## New-copy pass still required

Read the exact Benjamin writing-style skill once it is available, then review the shared page navigation/footer, new entry section/action labels, journey orientation, index descriptions, stewardship text, and three practical entrance cards in `scripts/build_readable_atlas.py`. The two interactive action labels are patched from the same generator. Regenerate after edits; preserve existing profile, journey, source, claim, and evidence prose. No push or deployment has been performed.
