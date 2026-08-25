# Work ticket: release 0.20.2 reader hotfix

Status: **Ready for human review**

Owner: **Benjamin P Taylor**

Human review point: **Review the pull request before merge and publication.**

## Outcome

Topic entries open and close without locking the browser, and every distinct
curator-supplied media study in the 25 August `logoso` staging folder is
available to the living-mark rotation.

## Reader or user effect

Readers can follow topic links normally and encounter the full supplied family
of marks without paying the transfer cost for more than the selected mark.

## Primary deliverable

A focused 0.20.2 hotfix pull request.

## In scope

- remove the topic-entry render loop;
- add a regression check for repeated entry opening and enhancement;
- inventory all 84 supplied media files, de-duplicate equivalent studies and
  produce web-sized stills, videos and reduced-motion posters;
- update the living-mark manifest and identity account so every source media
  file has an explicit disposition;
- refresh the release asset keys and hotfix notes.

## Out of scope

- new concepts, sources, relations or comparator reconciliation;
- redesigning the atlas, map or topic-entry layout;
- treating generated visual studies as evidence or relicensing them.

## Named files or areas

- `docs/assets/iteration-18.js`
- `docs/assets/living-marks/`
- `docs/assets/iteration-19.js`
- `docs/assets/iteration-19.css`
- `docs/index.html`
- `scripts/apply_iteration_19.py`
- `scripts/apply_prior_maps_20.py`
- `scripts/patch_iteration_18.py`
- `scripts/validate_iteration_18.py`
- `scripts/validate_iteration_19.py`
- `documentation/visual-identity.md`
- `documentation/TANGLE_STATE.md`
- `documentation/NEXT_WORK.md`
- `CHANGELOG.md`

## Sources and context

- Required: the live failure at `https://transduction.systems/` and the
  curator-supplied `Tangle logo staging 2026-08-25/logoso` folder.
- Optional: release 0.18–0.20 history only where needed to isolate a regression.
- Web research: **Not needed.**

## Constraints

- Follow `documentation/DESIGN_AND_CONTENT_RULES.md`.
- Keep the fixed inline SVG as the no-script and failed-request fallback.
- Load the manifest and one selected mark only; do not preload the family.
- Preserve the bottom-right `Open updates` dot.
- Record every supplied media file as published, duplicate or rejected with a
  concrete technical reason.

## Acceptance checks

- [x] Topic links no longer have an observer path which can react to its own class changes.
- [ ] Direct topic hashes work from a fresh load and browser history remains coherent.
- [x] Every supplied media file has an explicit disposition and every distinct,
      technically usable study appears once in the manifest.
- [x] Video marks have silent, looping web output and still reduced-motion fallbacks.
- [x] Only the selected mark is requested by the main page.
- [x] `make build` and `make validate` pass.
- [ ] Desktop and mobile reader paths are inspected after the fix.
- [ ] Human review occurs before merge or publication.

## Stop conditions

- Stop when the acceptance checks pass.
- Stop and ask if a source file is corrupt, contains private material or cannot
  be made browser-safe without materially changing it.
- Maximum execution: one implementation pass, one verification pass and one
  corrective pass tied to a failed check.

## Route and model

- Surface: **Codex**
- Model: **Sol**
- Reason: the live failure is an event-loop bug and the large mixed-media intake
  needs deterministic accounting, transformation and browser verification.
- Escalation: None.

## Durable update

Update the release state, visual-identity contract, changelog and next-work
record with the verified fix and final media counts.

## Completion report

- Outcome: removed the self-triggering topic observer and expanded the living
  mark family from 10 to all 84 supplied media studies.
- Files changed: reader enhancement and cache-key assets; living-mark manifest,
  source ledger and optimised media; release generators, validators and state
  documents.
- Checks run: live failure reproduced before the fix; 84-source visual and
  media audit; `make build`; `make validate`; JavaScript syntax, observer,
  manifest, size, H.264, dimensions and no-audio gates.
- Residual risks or deferred items: the cloud browser cannot reach this static
  repository's local server and the repository has no `package.json` for the
  managed agent-preview route, so post-fix direct-hash, history, desktop and
  mobile browser checks remain for the deployed branch. The live pre-fix path
  was reproduced in Chrome.
- Exact next decision: review and merge the pull request, then run the remaining
  live desktop/mobile reader checks against the deployed release.
