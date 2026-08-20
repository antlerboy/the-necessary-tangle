# AI-assisted work

Start with this file. Do not ingest the whole repository by default.

Read, in order:

1. `documentation/TANGLE_STATE.md` — what is true now;
2. `documentation/RELIABILITY_AND_EXECUTION.md` — what may be claimed, and what evidence completion requires;
3. `documentation/DESIGN_AND_CONTENT_RULES.md` — what must not be broken;
4. `documentation/NEXT_WORK.md` — the only authorised work packet;
5. `documentation/WORK_PROTOCOL.md` — how to execute it economically.

Then open only the files named by the active work packet. Follow links into the
larger documentation set only when they are needed to resolve a decision.

## Default operating rules

- Follow `documentation/RELIABILITY_AND_EXECUTION.md` without exception.
- Treat `done`, `published`, `merged`, `deployed`, `live` and `passed` as evidence claims, not conversational shorthand.
- Derive acceptance criteria before substantial work and do not silently narrow the request.
- Reconcile every named input source, including issue #2, structured submissions and standing issues where the request brings them into scope.
- Work towards one stated outcome and one deliverable.
- Preserve the public/private boundary and named human editorial responsibility.
- Use the smallest capable model and the smallest relevant source set.
- Do not start implementation when `NEXT_WORK.md` says that no packet is active.
- Do not browse or expand the corpus unless the packet requires current or missing
  evidence.
- Use one implementation pass and one verification pass. A third pass is the
  maximum and must address a named failed check.
- Run the acceptance checks named in the packet. `make validate` remains the
  repository-wide gate, but a green validation run is not proof of deployment or publication.
- Stop when the acceptance checks pass, when a stop condition is reached, or when
  another pass would not materially improve the named outcome.
- Do not create generic ‘related to’ edges to improve coverage figures.
- Do not remove or relocate the bottom-right ‘Open updates’ magic dot.
- Do not publish or merge without human review.

Finish with a concise evidence ledger: acceptance criterion, status, direct evidence and remaining limitation. Then report outcome, files changed, checks run, residual risks and the exact next decision. Update durable state files only when their facts or authorised next action have materially changed.
