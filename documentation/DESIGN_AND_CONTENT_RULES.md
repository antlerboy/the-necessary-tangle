# Design and content rules

These are the compact non-negotiables for implementation. Where a work packet
conflicts with them, stop and ask for a human decision.

## Meaning before volume

1. The maintained object is a multiplex evidence graph. Every public line must
   make a specific claim; never use a generic ‘related to’ edge to create reach.
2. Keep relation kinds distinct: logical dependence, historical sequence,
   influence, teaching, mentoring, collaboration, citation, practical use,
   identity, comparison and challenge are not interchangeable.
3. Make a statement inspectable through direction, reader wording, scope, status,
   source and the most precise available locator.
4. Distinguish source-established claims, curatorial interpretation, candidate
   claims and contestation. Plausibility is not evidence.
5. Prefer fewer locatable, scoped statements to a large set of suggestive ones.
6. Treat boundaries and communities as explicit, provisional editorial devices,
   not natural or final divisions of the field.
7. Preserve disagreement, rival definitions and uncertain lineage when sources
   support them. Do not edit the graph into false consensus.
8. A view is a projection of maintained statements. It must not imply new
   relationships merely through layout, proximity or sequence.

## Sources and publication

- Only public-safe material belongs in the repository. Sources must be public
  HTTP(S) resources or candid bibliographic records with access limitations.
- Never introduce private mail, SharePoint paths, client material, credentials or
  internal research notes into public data, fixtures, logs or screenshots.
- Record an exact page, section, passage, slide, entry or stable fragment whenever
  it is available. A source ID alone is not claim-level evidence.
- Use UK English and plain language. Preserve names, quotations and source titles
  accurately.
- The curator remains responsible for editorial acceptance. Automated checks may
  reject defects; they do not confer truth or permission to publish.

## Reader experience

- Preserve the restrained cream/red palette, serif-led hierarchy, composed cards,
  generous spacing and responsive stacking documented in
  `documentation/experience-visual-audit.md`.
- Keep status and evidence distinctions legible without relying on colour alone.
- Keep the full graph available, but prefer sparse, question-shaped starting views.
- Protect keyboard access, heading order, readable type and mobile containment.
- Preserve the fixed bottom-right magic dot exactly as the reader's quiet updates
  route. Its accessible control remains `aria-label="Open updates"`.
- Do not trade existing clarity or accessibility for visual novelty.

## Change discipline

- Change only the named files or areas in the active work packet.
- Keep generated outputs and their generating scripts consistent.
- Treat a no-op as a no-op; do not record it as substantive progress.
- Run `make validate`, then inspect every changed reader path at relevant desktop
  and mobile widths.
- Publish authorised changes directly after validation, following the standing
  authorisation in `AGENTS.md`. Pull requests can record the change without an
  additional human-review stop. Substantive curatorial batches receive a
  numbered release; source-owner permissions and access controls still apply.


## Navigational link contract

Anything whose purpose is to take a reader to another stable atlas state must be an actual link with an `href`, including cards, search suggestions, map nodes, map connections, entry actions and serendipity routes. Plain left-click may be enhanced in place. Copy link, open in new tab, modified-click and browser history must remain coherent. Use buttons only for actions which cannot sensibly be represented as a URL, such as filtering, zooming, copying or submitting a form.

Public prose must stand alone. It must not answer an unseen prompt, refer to a person only by a private-conversation shorthand, or depend on knowledge of the development chat. Feedback and provenance belong in the ledger or source record; definitions and explanations must carry their own context.
