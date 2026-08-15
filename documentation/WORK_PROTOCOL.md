# Cost-effective work protocol

This protocol turns a rough request into one bounded work packet. It applies to
AI-assisted research, analysis and implementation; it does not replace editorial
judgement or repository validation.

Model names and relative prices change. The routing below is a capability ladder,
not a permanent price promise. Check the current account usage dashboard before making a
budget decision.

## 1. Route the request before doing the work

Choose one surface:

- **Chat** — clarification, brainstorming, a quick judgement, a small draft or
  shaping the packet.
- **Work** — multi-source research, file analysis and a durable non-code output.
- **Codex** — repository inspection, implementation, tests and a reviewable change.

Do not pay Work or Codex to rediscover an outcome that can first be settled in
Chat. Move the settled packet, not the entire exploratory conversation.

Choose the smallest capable model:

- **Luna** — extraction, inventories, link checks, de-duplication, formatting,
  routine tests and other mechanical work. Approximate relative cost: 4.
- **Terra** — the default for structured analysis, normal implementation, content
  work, CSS and debugging. Approximate relative cost: 40.
- **Sol** — conceptual architecture, genuinely hard judgement, difficult bugs and
  final critique when a cheaper model cannot reliably decide. Relative cost: 100.

Use a stronger model for one decision or review, not automatically for every step.
Do not use multi-agent work unless two or more tasks are genuinely independent and
their parallel value justifies multiplied consumption.

## 2. Make one complete packet

Use `documentation/WORK_TICKET_TEMPLATE.md`. A runnable packet states:

- one outcome and one primary deliverable;
- the audience or reader effect;
- relevant context and only the necessary sources;
- named files or areas;
- explicit in-scope and out-of-scope boundaries;
- acceptance checks and verification commands;
- stop conditions and the human decision point;
- the durable state that must be updated.

Required and optional work must be visibly separate. If a missing answer would
materially change the route, ask one concise clarifying question; otherwise state a
reasonable assumption and proceed.

## 3. Keep context lean

- Start from `AGENTS.md`, `TANGLE_STATE.md`, the rules and `NEXT_WORK.md`.
- Open only the named implementation files and the exact references needed.
- For repeated research, extract a concise, cited finding once and reuse that
  durable result rather than repeatedly ingesting the source corpus.
- Keep research and build work in separate contexts. Research produces a bounded
  evidence packet; build consumes that packet.
- Do not attach the whole project, dump long tool output or perform fresh web
  research unless the outcome requires it.
- Disable or avoid unused connectors and tools for the packet.

## 4. Execute and stop

The normal run has:

1. one implementation pass;
2. one verification pass;
3. at most one corrective pass tied to a named failed check.

Three passes are the maximum. Stop sooner when acceptance checks pass. Also stop
when a blocker needs human judgement, the source boundary would be crossed, or
another pass would not materially improve the stated outcome. Do not turn spare
time or remaining context into extra scope.

Return a concise report containing the outcome, files changed, checks run, failed
or deferred items and exact next decision. Avoid a long narration of routine work.

## 5. Close the loop

- Update durable repository state only when facts, rules or the authorised next
  action changed.
- Record dashboard credits before and after large runs in a private usage record;
  do not publish personal or workspace billing data in this public repository.
- Compare cost with the completed outcome, not token or message volume.
- If the weekly Work/Codex allowance is exhausted, preserve the packet and wait for
  reset unless the value and urgency justify paid credits. The repository and
  public site do not depend on starting another AI run.
