# Next work

Status: complete. The interface was published successfully in commit `cf3f4ca9299ac1de4188efff162b65f49652a5db`. Authorised by Benjamin P Taylor on 6 September 2026.

## Outcome

Update the systems events map at `/events/`: add the two queued Toronto and Manchester events; make a public URL the only required submission field; extract published details for review; and support country/region focus and language requirements.

## In scope

The maintained `antlerboy/systemsmap` interface, event data, collector, submission workflow, tests, and calendar feeds. In this repository: `docs/events/`, `scripts/integrate_systems_events.py`, the pinned systemsmap revision in workflows, and the state/work-packet records (including their release-22 build inputs).

## Acceptance checks

- The two queued events have source-verified dates, local times, formats, and locations.
- Only a public URL is required; failed or ambiguous extraction remains in the review queue.
- SCiO Polska is found under Poland and Polish, with an online area marker and its published ‘All welcome’ access retained.
- Geographic focus, language, language requirements, interpretation, and access remain separate. Missing facts are not inferred.
- Shared filter URLs retain country/region and language; calendar exports retain focus, language, and access details.
- Fourteen systemsmap Python tests, JavaScript interaction checks, syntax checks, 37 calendar feeds, and the full Tangle `make validate` gate passed locally.
- Publish to the existing public audience and verify the deployed interface and source revision.

## Out of scope

Changes to atlas graph claims, approved comparator data, domain routing, and unrelated content.

## Stop conditions

The publication workflow passed. The queued events are in the maintained collection and issues 1 and 2 are closed. No further work is active in this packet. No additional permission round is required under AGENTS.md.

## Model route

Repository implementation and focused verification in the current session; no additional agent work is required.
