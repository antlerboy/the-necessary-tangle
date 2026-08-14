# Relationship audit

Updated: 2026-08-14  
Machine-readable companion: [`data/relationship-quality.json`](../data/relationship-quality.json)

## Audit contract

A relationship is treated as a public claim, not a visual line. The audit asks whether it has:

1. a meaningful reader-facing phrase and rationale;
2. an explicit type, family and direction decision;
3. named evidence and the most precise available locator;
4. an epistemic status that distinguishes source-established, interpreted, candidate and contested claims;
5. agreement, extension, tension or contradiction semantics where relevant;
6. a route between different intellectual or practice families;
7. enough distinct routes to prevent an important entity being defined by one repetitive connection;
8. no generic “related to” wording when a stronger claim is supportable.

## Baseline

| Measure | Result | Interpretation |
| --- | ---: | --- |
| Public entries | 496 | Reader-facing denominator |
| All typed edges | 1,712 / 1,712 | Strong schema coverage |
| Directed edges | 1,610 / 1,712 | 102 are explicitly undirected; many are valid co-authorship/similarity relations and require semantic review rather than blanket conversion |
| Human-readable phrases | 1,712 / 1,712 | Strong wording coverage |
| Explicit rationale fields | 1,407 / 1,712 | 305 rely on phrase/locator without notes, scope or inference explanation |
| Source identifier present | 1,712 / 1,712 | Necessary but not sufficient |
| Locator present | 1,266 / 1,712 | 446 have no locator |
| Precision-shaped locator | 220 / 1,712 | Conservative text-pattern count for pages, chapters, sections, slides or similar; manual review remains necessary |
| Reader-connected entries | 496 / 496 | No public entry is unreachable |
| Semantically connected entries | 329 / 496 | 167 are connected only through documentary/collection structure |
| Rich / developing / thin | 35 / 236 / 225 | Depth remains highly uneven |
| Three or more reader relation families | 72 / 496 | Stronger route diversity is uncommon |
| One reader relation family | 189 / 496 | High risk of repetitive or documentary-only identity |
| Generic relation review targets | 8 | `conceptually_related_to` or “related to” wording |
| Disjoint-set semantic edges | 197 / 757 eligible | Rough cross-family proxy only; set tags are not an intellectual-family ontology |

## Thin and weakly connected entities

The thin cohort is overwhelmingly people and publications:

| Entity type | Thin | Total | Share thin |
| --- | ---: | ---: | ---: |
| Person | 112 | 169 | 66% |
| Publication | 108 | 121 | 89% |
| Law or principle | 0 | 33 | 0% |
| Concept | 0 | 60 | 0% |
| Intervention skill | 0 | 47 | 0% |

The machine-readable priority queue records every candidate with its current connection and evidence bands. The immediate review order is:

1. developed people and works that still have only one documentary edge;
2. publications already present in a named corpus but not connected to the claims they make;
3. people represented only as authors, before inferring influence or mentorship;
4. inventory-only reading-list items, without manufacturing semantic connections from titles.

Representative thin developed profiles include Alessandro Rancati, Alfonso Reyes, Arthur Battram, Lucy Loh, Mary Boone, Michael Jackson, Tony Korycki, *Flawless Consulting*, *Steps to an Ecology of Mind*, *Systems Thinkers* and *Understanding Understanding*.

## Generic relation register

Eight edges require replacement or removal:

| Edge | Current wording | Review question |
| --- | --- | --- |
| Semantic network → Self-organisation | conceptually related to | Does the Principia semantic-network architecture model, enable or merely co-occur with self-organisation? |
| Complex responsive processes → Emergence | conceptually related to | Does the account explain emergent pattern through local interaction? |
| Complex responsive processes → Self-organisation | conceptually related to | Does the source affirm, qualify or reject self-organisation language? |
| *Murmurations* → Complex responsive processes | conceptually related to | Is the journal a publication venue, an intellectual home, or evidence of adoption? |
| Explicit semantics → Semantic network | is conceptually related to | Does explicit semantics specify the edge vocabulary of a semantic network? |
| Natural drift → Viability | is conceptually related to | Does natural drift offer an alternative account of viability rather than a supporting prerequisite? |
| Requisite inefficiency → Viability | is conceptually related to | Does the source state an operational constraint or balancing condition for viability? |
| Bounded applicability → Boundary | relation type is generic; phrase says “requires explicit boundaries around” | Retype to the already-supported boundary requirement |

No generic edge should be upgraded merely because a stronger phrase sounds plausible. Pass 2 must inspect the named source and locator for each.

## Repetitive connections

One repeated assertion group uses the same ordered pair, type and broad locator twice: Arturo Rosenblueth → Norbert Wiener, `coauthored_with`. The two records refer to different publications but the locator is the collection table of contents. Retain both only if each receives a work-specific locator or a distinct publication-mediated path; otherwise consolidate.

Thirty-nine ordered pairs carry more than one statement. Most are semantically legitimate—for example a work can both instantiate and historically precede a concept—but each must remain independently explainable. Pair count is therefore a review trigger, not a duplicate count.

## Source and locator audit

The strongest current practice uses page ranges, chapter/section names, slide ranges or stable entry names. The weakest uses broad locators such as:

- “Official collection table of contents”;
- “Release 0.12 public practitioner and publication sources”;
- “Principia Cybernetica first-pass public source set”;
- “source record” or “bibliographic record”;
- an interpretive crosswalk description with no source passage.

The next corpus work must preserve both the source ID and a claim-locating path. A landing page can establish that a project exists; it cannot by itself establish a particular conceptual relation.

## Direction and epistemic status

All 1,712 edges carry claim status, assertion mode and public review label. That is a strong foundation. Direction still needs semantic attention:

- co-authorship can remain undirected;
- “developed or extended”, “criticises”, “requires”, “constrains”, “documents” and “applies” should be directed;
- historical sequence must not be used as evidence of influence;
- citation must not be used as evidence of mentorship;
- similarity must not be used as evidence of lineage.

Inferred or interpreted relations should remain visible but must not be styled or worded as if source-established. A missing primary check should not be hidden by high graph degree.

## Cross-family routes

There are 197 semantic edges between nodes whose maintained set tags do not overlap, out of 757 eligible semantic edges. This is a useful bridge-review queue, not a quality score: set tags partly encode release history and collection membership. The higher-quality route is explicit and inspectable, for example:

publication → makes claim → concept → informs method → documented use → limitation or counter-claim.

Passes 3 and 4 should prefer such mixed routes over adding more same-type bibliography edges.

## Pass 2 decision rule

For every candidate relationship:

1. open the source;
2. locate the passage or internal entry;
3. write the narrowest supported directed phrase;
4. record type, family, status, assertion mode and uncertainty;
5. reject the edge if the source supports only resemblance;
6. test whether it adds a genuinely different route;
7. re-run the machine audit and inspect the affected entries in desktop and mobile views.

## Pass 2 result

Pass 2 inspected every public entity through the maintained per-node depth record, then reviewed each generic or repetitive relationship against its cited source.

| Measure | Baseline | Pass 2 | Change |
| --- | ---: | ---: | ---: |
| Generic relation review targets | 8 | 0 | −8 |
| Repeated assertion groups | 1 | 0 | −1 |
| Directed edges | 1,610 | 1,617 | +7 |
| Precision-shaped locators | 220 | 231 | +11 |
| Public sources | 153 | 155 | +2 |
| Reader-connected entries | 496 | 496 | — |
| Semantically connected entries | 329 | 328 | −1 |
| Substantive edges | 750 | 749 | −1 |

### Reviewed replacements

- **Semantic network → Self-organisation:** now says the Principia implementation *puts into practical form the project's account of* self-organisation, located to the two relevant introduction paragraphs.
- **Complex responsive processes → Emergence:** now an explicitly interpreted, provisional claim about the emergence of organisational knowledge through interaction, located to Stacey's institutional abstract and article pages.
- **Complex responsive processes → Self-organisation:** now a source-established specialisation that defines social self-organisation as local interaction rather than self-management.
- **Murmurations → Systems practice:** now a documentary journal-scope claim. The earlier complex-responsive-process edge was not supported by the official journal description.
- **Explicit semantics → Semantic network:** now says that RDF configuration and labelled predicates *formalise the node, edge and display vocabulary*.
- **Natural drift → Evolutionary cybernetics:** now records a tension between Maturana and Mpodozis's natural-drift mechanism and Principia's natural-selection mechanism. It no longer implies a vague relation to viability.
- **Requisite inefficiency → Viability:** now records Velitchkov's proposed excess-variety constraint on long-run viability.
- **Boundary → Bounded applicability:** direction is reversed and typed as definitional prerequisite, following the maintained Cynefin definition.
- **Rosenblueth ↔ Wiener:** two co-authorship assertions remain, but each is now located to the specific work that warrants it.

### Deliberate regression

The Murmurations correction removes one semantic connection because the source supports a venue/scope claim, not adherence to complex responsive processes. Semantic reach falls by one. This is preferable to preserving a misleading edge.

### Remaining structural risk

The overall thin cohort is unchanged: 225 entries, including 112 people and 108 publications. Route diversity is also unchanged at 72 entries with three or more reader relation families and 189 with only one. The corpus passes must add new routes only where passages, not titles or similarity, warrant them.

## Pass 3 external-corpus result

The nine-corpus traversal added eight edges and strengthened six. Source count rises from 155 to 166; precision-shaped locators from 232 to 244; rich entries from 35 to 36; thin entries fall from 225 to 224; and entries with three or more relation families rise from 72 to 74.

Three traversals produced no semantic edge. The Ashby archive provides extraordinary primary provenance but index co-occurrence is not influence. The ISSS meeting history establishes organisational chronology but participant co-presence is not conceptual transmission. The reading list establishes intended coverage but titles are not relationship evidence.

The strongest additions are mechanism- or work-specific: Principia's positive/negative feedback account of self-organisation, Ing's pattern-form treatment of voices, Systems Changes Learning's contextural action-learning formulation, and the System Dynamics Society's explicit stocks-flows-feedback method structure. The SFI and IFSR additions remain interpreted and visibly provisional.

## Pass 4 internal-corpus result

The internal inventory contains 18 non-public source records: six supplied slide-level decks, five earlier author syntheses or lectures, six legacy internal registers and one discovery-only network image. Across the graph these records appear in 501 edge citations, including 412 substantive citations, but only 34 citations have slide-, page-, section- or chapter-shaped locators.

All 17 direct supplied-deck crosswalk statements now have claim-specific rationales and material-specific limits. Seven degraded slide ranges were normalised. No new edge was added: the outcomes deck remains documentary-only, duplicate Core Thinking titles do not multiply support, and visual proximity in the Perko network remains discovery rather than lineage evidence.

The largest internal provenance debt is concentrated in the SCiO CF Resources draft and the legacy Feedback and Recursion SysBoK decks. Their broad use in generated crosswalks should be replaced by public, claim-level sources for high-value relationships.
