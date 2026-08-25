# External map link policy

Status: active from release `0.20-prior-maps-alpha`.

## Principle

Retain every available link from a prior map when use is permitted and the
endpoints can be represented faithfully. Retention records what the source map
says. It does not make the claim accurate, accepted or canonical.

## Required fields

Every imported comparator link must record:

- the source map and its own stable link identifier;
- source and target, or the outward URL for an image-map reference;
- the most specific meaning the source itself supplies;
- direction where the source supplies it;
- provenance and permission or licence status;
- `accuracy_status`, distinguishing source-reported from independently checked;
- whether a more specific relation and edge-level evidence are absent;
- any reconciliation with canonical Tangle entries or relations.

## Source meaning is the ceiling

If a source says “major influence”, the comparator may say “the source reports
a major influence”. It may not silently translate the line into teaching,
citation, derivation, collaboration or conceptual dependence. If a source says
nothing, the link stays visually preserved and explicitly untyped.

Colour, proximity and layout may be retained as source features. They do not
create a relation meaning that the source has not stated.

## Accuracy and promotion

Comparator links use one of these accuracy states:

- `source_reported_not_independently_verified`;
- `source_link_not_independently_checked`;
- `aggregate_signal_not_independently_reproduced`;
- `independently_checked` only after a bounded evidence review.

A comparator link never becomes a canonical atlas relation by import. Promotion
requires reconciled identities, a controlled relation type, a meaningful source
locator, scope conditions and named editorial review. A separately evidenced
atlas relation may coexist with a comparator link without being derived from it.

## Broken, surprising and mismatched links

Preserve a source-published URL in the comparator dataset unless it is unsafe.
Expose an apparent label mismatch or dead route rather than silently correcting
another author's map. A proposed correction belongs in a review field and, where
appropriate, should be returned to the source maintainer.

Reject executable or unsafe URL schemes. Open external links with ordinary
browser protections.

## Rights boundary

Permission or an applicable licence governs whether the source structure can be
republished. A citation alone does not relicense a map. When full structure
cannot be republished, retain the public source route, a concise analysis and a
reproducible extractor; do not reconstruct copyrighted arrangement by stealth.

Licensed bibliographic corpora are a separate layer. Public projections may
retain aggregate facts and permitted identifiers while excluding private source
records and licensed text fields.

## Current applications

- *Map of Systemic Evolution*: all 650 nodes and 1,320 source-reported major
  influences, used with Benjamin Hadorn's permission.
- *Map of the Complexity Sciences*: all 307 clickable outward references in the
  May 2026 public image map; its drawn lines remain visible but untyped.
- *The Counted Map*: all 1,856 aggregate keyword-labelled citation signals;
  private corpus data and raw Scopus cited-reference strings excluded.
