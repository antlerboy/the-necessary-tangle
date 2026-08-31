# Source-owner review: Systemic Evolution derivative

Review package: `systemic-evolution-2026-08-26-review-1`

This package is for review and verification before publication. It implements
the scope authorised by Benjamin Hadorn on 26 August 2026 and is not a claim
that the underlying source is generally CC BY-SA licensed.

## What to review

1. `original/systemic_evolution.graphml` is the unmodified source copy.
2. `derivative/systemic_evolution-the-necessary-tangle.graphml` retains the
   source graph and adds fields whose names begin `tangle.`.
3. `comparator-systemic-evolution.json` is the browser-oriented extraction.
4. `systemic-evolution-reconciliation.json` records cumulative identity/scope
   matching and keeps it separate from source-link verification.
5. `site/` contains the proposed page, map scripts, stylesheets and data assets.
6. `review-manifest.json` supplies the exact hashes, counts, attribution and
   change summary.

## Preview the proposed reader view

From the package directory, run:

```sh
python3 -m http.server 8000 --directory site
```

Then open the server address printed in the terminal and add
`/prior-maps/systemic-evolution/`. The preview must be served over HTTP because
the page loads its checksummed JSON assets with `fetch()`; opening the HTML
directly from a file manager will not work.

## Points on which verification is requested

- Is the attribution to Eric Schwarz, Benjamin Hadorn and Beat Hirsbrunner, and
  the longer Schwarz–Durant–IIGSS–Hadorn history, accurate and sufficient?
- Does the wording “source-reported major influence” preserve the source's
  intended meaning without overstating individual links?
- Does the enriched GraphML preserve the complete source node and edge set?
- Are any added fields, corrections, interface statements or download labels
  misleading or inappropriate?
- May this exact checksummed derivative package be published in The Necessary
  Tangle under the permission already granted?

## Deliberate limits

- No source-reported line is promoted into the canonical Tangle by import.
- Existing node reconciliation identifies same, component, broader/narrower or
  adjacent entries; it does not verify an influence claim.
- The full-layout and focused views are alternative renderings of the same
  filtered source structure.
- Any later graph-data modification will be returned for another review.
