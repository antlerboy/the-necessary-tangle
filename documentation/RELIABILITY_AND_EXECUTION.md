# Reliability and execution protocol

This protocol governs AI-assisted work in this repository. It exists to prevent plausible narrative from being mistaken for evidence, partial work from being called complete, and changing project state from being left to chat memory.

## Completion words are evidence claims

Do not say `done`, `published`, `sent`, `merged`, `deployed`, `live`, `passed` or an equivalent unless the relevant canonical system has been checked after the action.

Keep these states distinct:

1. planned;
2. attempted;
3. changed locally;
4. committed;
5. pushed;
6. pull request opened;
7. validated;
8. merged;
9. deployment triggered;
10. deployment succeeded;
11. live endpoint independently verified.

Never collapse several of these into one reassuring word.

## Before starting substantial work

- Derive explicit acceptance criteria from the user's request and the established project context.
- Enumerate every named input feed: the active work packet, issue #2, structured site submissions, standing research issues, review comments and any other source named in the request.
- Do not silently narrow `complete`, `all`, `publish`, `update` or similar language.
- Ask one concise question only when an ambiguity would materially change the result. Otherwise state the assumption and proceed.
- Identify which facts are stable instructions and which are mutable project state.

## During execution

- Continue until every acceptance criterion is met or a concrete blocker exists.
- Do not substitute a plan, an intermediate green check, a successful tool call, a workflow trigger or a plausible inference for completion.
- Reconcile each named input as one of: `implemented`, `partly implemented`, `open`, `deferred`, `rejected` or `not checked`.
- Do not claim work is happening in the background unless an actual asynchronous or scheduled mechanism has been invoked.
- Read mutable facts from their canonical project records rather than relying on recollection from a chat.
- Preserve the public/private boundary and named human editorial responsibility.

## Evidence ledger

Before reporting completion, produce a compact evidence ledger containing:

- acceptance criterion;
- status;
- direct evidence;
- remaining limitation.

No evidence means `not verified`.

The final report must distinguish work performed from work merely proposed, inferred or still awaiting review.

## Publication gate for The Necessary Tangle

`Published` means all of the following have been demonstrated:

1. the complete requested input set has been enumerated;
2. every input has been classified as implemented, partial, open, deferred, rejected or not checked;
3. the generated public artefact identifies the intended release;
4. validation passes against that exact artefact;
5. the release branch is pushed;
6. the release pull request is merged into `main`;
7. the Pages deployment succeeds;
8. `https://transduction.systems/deployment.json` identifies the expected release and commit;
9. the custom-domain homepage and every new public route are checked directly;
10. issue #2 receives the final release reconciliation;
11. relevant contribution issues receive an appropriate public response and status;
12. remaining work is reported plainly rather than translated from `first pass` into `complete`.

A repository commit, merged pull request or green validation run is not by itself publication.

## Canonical records

Use these records for their stated purpose:

- `AGENTS.md` — entry point and operating order;
- `documentation/TANGLE_STATE.md` — current project state;
- `documentation/DESIGN_AND_CONTENT_RULES.md` — enduring design and content constraints;
- `documentation/NEXT_WORK.md` — authorised current work packet;
- `documentation/WORK_PROTOCOL.md` — bounded execution and cost discipline;
- `documentation/feedback-ledger.md` — reconciliation of issue #2 and other feedback;
- GitHub Issues — research, development and contribution records;
- `docs/deployment.json` on the live site — deployed release and commit.

When these disagree, stop and report the inconsistency rather than choosing the most convenient account.

## Memory and mutable state

Use saved memory only for stable facts and preferences about the account holders, such as names, roles, writing preferences and standing personal constraints.

Do not use saved memory as the source of truth for release numbers, open issues, deployment state, current acceptance criteria or other changing project facts. Put those in versioned repository records and verify them at the point of use.

## Failure and uncertainty

- State the failed step and the evidence for failure.
- Say what remains safe to conclude.
- Do not invent a likely explanation where logs or state are unavailable.
- Do not describe a limitation more broadly than the evidence supports.
- Correct an earlier false statement explicitly and update the canonical project record where required.
