# Work ticket: publish the reviewed Systemic Evolution map

Status: **Complete**

Owner: **Benjamin P Taylor**

Human review point: **Benjamin P Taylor's instruction to publish on 31 August
2026, following Benjamin Hadorn's approval of the exact review package**

## Outcome

Publish the source-owner-reviewed Systemic Evolution map as release 0.21,
without changing its reviewed graph structure or overstating its evidence.

## Reader or user effect

Readers can begin with a legible one- or two-step neighbourhood, recover the
complete source layout, use keyboard and text alternatives, inspect the
reconciliation boundary, and download the exact reviewed package.

## Primary deliverable

Release 0.21 of the public Systemic Evolution comparator page and its reviewed
reader assets.

## In scope

- Publish the exact reviewed reader JavaScript and CSS.
- Preserve all 650 source nodes and 1,320 source-reported links.
- Correct the permission record to distinguish the 26 August scope grant from
  the 31 August approval of the exact enhanced package.
- Publish the review manifest, review archive checksum, approval record, and
  full attribution.
- Advance the maintained release state and deployment workflow to 0.21.

## Out of scope

- Reconcile further nodes or verify further source-reported influence links.
- Promote any comparator link into the canonical Tangle.
- Change the reviewed graph data.
- Claim separate approval from Beat Hirsbrunner where none is recorded.

## Named files or areas

- `sources/systemic-evolution/review-1/`
- `docs/prior-maps/systemic-evolution/`
- `docs/assets/systemic-evolution-*`
- `scripts/apply_release_21.py`
- `scripts/prepare_reader_21_deployment.py`
- `scripts/validate_release_21.py`
- release, rights, acknowledgement, state, and deployment records

## Sources and context

- Required: checksummed review archive
  `systemic-evolution-2026-08-26-review-1`.
- Required: Benjamin Hadorn's 26 August scope permission and 31 August approval
  of the enhanced version.
- Web research: **Not needed**.

## Constraints

- Follow `documentation/DESIGN_AND_CONTENT_RULES.md`.
- The reviewed JavaScript and CSS remain byte-identical to the approved package.
- Post-review publication wording may record the approval but must not alter
  graph data or imply that source-reported influence has been verified.

## Acceptance checks

- [x] The reviewed archive checksum is unchanged.
- [x] The public reader retains all 650 nodes and 1,320 links.
- [x] Focused, complete-layout, realm, mapping, keyboard, and text views are
  present.
- [x] Rights and attribution distinguish the scope grant, package approval, and
  absence of a separate Beat Hirsbrunner reply.
- [x] `make build` and `make validate` pass.
- [x] Desktop and mobile reader inspection passes.
- [x] Human review occurred before merge and publication.

## Stop conditions

- Stop when the acceptance checks pass.
- Stop and ask if the reviewed graph data would need to change or the source
  owner's approval cannot be tied to the package checksum.
- Maximum execution: one implementation pass, one verification pass, and one
  corrective pass tied to a failed check.

## Route and model

- Surface: **Codex**
- Model: **Sol**
- Reason: the task combines release engineering, rights boundaries, and a
  source-owner-reviewed data derivative.
- Escalation: **None**.

## Durable update

Update the changelog, rights record, acknowledgements, current state, next work,
release metadata, and deployment workflow.

## Completion report

- Outcome: release 0.21 publishes the exact source-owner-reviewed Systemic
  Evolution package with focused and complete layouts, a text alternative,
  immutable checksums, full attribution, and a separate approval record.
- Files changed: reviewed source snapshot; release application, reader
  preparation, and validation scripts; deployment workflow; release, rights,
  acknowledgement, state, and comparator documentation; one publication-only
  mobile containment stylesheet.
- Checks run: clean `make build`; clean `make validate`; release checksum and
  JavaScript validation; desktop search, depth, realm, mapping, complete-layout,
  keyboard, and text-view checks; 390 px mobile interaction and overflow checks.
- Residual risks or deferred items: 588 source nodes remain unresolved, and the
  source-reported influence links remain unverified unless independently
  evidenced. No separate Beat Hirsbrunner reply is recorded. Any later graph
  or dataset change reopens the source-owner review gate.
- Exact next decision: merge and deploy this bounded release; require a new
  ticket and renewed review for any later graph-data change.
