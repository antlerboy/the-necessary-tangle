# AI observations

Generated for release `0.10-practice-safety-alpha` on 2026-08-10.

These observations combine reproducible counts from the public graph with model-assisted interpretation. Measurements, interpretations and proposed tests are kept separate. Detailed risk working notes are kept outside the public release; the public record shows the controls which govern publication.

## Measured state

- 442 public entries; 58 developed profiles.
- 597 typed public edges; 217 substantive edges.
- 169 substantively connected entries and 273 substantive isolates.
- 114 sources, of which 101 have public links.

## Breadth has outrun depth

**Basis:** measurement plus interpretation.

**Measured:** The atlas has 442 public entries and 58 developed profiles. Only 13.1% of entries have the fuller profile structure.

**Interpretation:** It is now better at showing that something belongs in the territory than at explaining what the thing means, why it matters, where it is contested and how it enters practice.

**Implication:** Next depth work should follow reader demand, bridge concepts and high-risk ambiguities rather than adding another undifferentiated tranche of names.

**Test:** This observation weakens when developed profiles and item-level source coverage grow without sacrificing the breadth inventory.

## One interface contains two different graphs

**Basis:** measurement plus design inference.

**Measured:** There are 597 typed public edges, but 217 are conceptual, historical, human, practice or contestation relations. The substantive share is 36.3%.

**Interpretation:** Authorship, collection membership and other provenance lines answer different questions from influence, dependence or use. Combining them without visible layers makes bibliographic density look like intellectual agreement.

**Implication:** The interface should let readers choose conceptual, human-lineage, practice, contestation and provenance layers explicitly.

**Test:** Readers should be able to explain what became visible or hidden when they change layer, without learning database vocabulary first.

## Practice is named more often than it is connected

**Basis:** measurement plus curatorial inference.

**Measured:** The isolate count is concentrated among intervention skills, laws, tools, methods and publications rather than the small conceptual core.

**Interpretation:** The source programme has imported lists of capabilities and publications faster than it has documented how ideas are enacted, taught, combined, resisted and changed in use.

**Implication:** Practice cases, practitioner journals, project histories and teaching lineages should now receive deliberate connection work.

**Test:** The practice layer should develop multiple well-sourced routes between concepts, methods, settings, people and consequences.

## Auditability is not yet source diversity

**Basis:** measurement plus evidential risk.

**Measured:** The most reused source is ‘Foundational Papers in Complexity Science — official tables of contents’, attached to 618 public nodes or edges.

**Interpretation:** A table of contents can establish titles, authors and collection placement. It cannot establish the meaning, influence or quality of every work it lists. Repetition of one source creates an appearance of corroboration without independent evidence.

**Implication:** Paper-level primary records, publisher pages, DOI metadata, archives, reviews and critical accounts must replace collection-level evidence where stronger statements are made.

**Test:** Source concentration should fall as the number and independence of item-level sources rise.

## The people layer contains an identity-resolution debt

**Basis:** measurement plus data-quality risk.

**Measured:** 108 of 155 people — 69.7% — are currently represented by initial-form labels.

**Interpretation:** Initials are enough to inventory an authorship string, but not enough to guarantee a unique person. They invite duplicate records, mistaken mergers and false career or influence connections.

**Implication:** Add full names, ORCID or other authority identifiers, affiliations and paper-level checks before deepening those people into intellectual profiles.

**Test:** No initial-only person should acquire interpretive or lineage edges without successful identity resolution.

## The published neighbourhoods are a historical snapshot, not the present graph

**Basis:** measurement plus model warning.

**Measured:** Six published neighbourhoods contain 77 unique nodes, while 169 nodes are now connected; 92 connected nodes sit outside the old grouping pass.

**Interpretation:** An algorithmic cluster is produced by the current edges, exclusions, resolution setting and seed. It is not a natural school waiting to be discovered.

**Implication:** Recompute neighbourhoods at each suitable release, record the algorithm and version, and retain change over time rather than silently replacing one partition with another.

**Test:** A reader should be able to inspect why two entries share a neighbourhood and see when that grouping changed.

## A few bridge concepts carry much of the atlas's traffic

**Basis:** network measurement plus editorial inference.

**Measured:** Feedback, recursion, the Viable System Model, boundary, requisite variety and related bridge entries have markedly higher substantive degree than most of the graph.

**Interpretation:** The wording and omissions in those entries influence many possible routes through the atlas. They are single points of interpretive failure as well as useful orientation points.

**Implication:** Give bridge entries multi-source review, rival definitions, domain distinctions and explicit limits before relying on them as navigation hubs.

**Test:** Alternative routes and counter-accounts should reduce dependence on any one bridge without hiding genuine centrality.

## The gaps map the curator's attention as much as they map the field

**Basis:** second-order observation.

**Measured:** 273 entries are isolated in the substantive graph, while the largest substantive component contains 112 entries.

**Interpretation:** Isolation does not mean an idea is naturally peripheral. It often means the current source set, relation vocabulary or research history has not yet made its connections visible.

**Implication:** Treat isolates as hypotheses about missing work, not as evidence that the field itself has no connections there.

**Test:** Source programmes from different traditions should alter which entries appear central, peripheral or absent.

## The graph is unusually useful to AI — and unusually easy for AI to overread

**Basis:** experience-based AI observation.

**Measured:** The atlas provides typed relations, status, source IDs and explicit caveats, but depth and source granularity vary sharply across entries.

**Interpretation:** Structured relation types reduce the usual language-model tendency to collapse every association into ‘related to’. The remaining danger is confident completion: turning bibliographic inclusion into influence, a provisional edge into fact, or missing data into a smooth narrative.

**Implication:** AI outputs should expose the exact entries, relation types and sources used; distinguish retrieval from inference; and state when the graph is silent.

**Test:** A useful AI answer should become less fluent, not more, when the evidence is thin or contradictory.

## Publication controls

The detailed working risk register is kept outside the public release. The public site exposes the controls which shape publication, not a catalogue of exploitable operational weaknesses.

See [publication safety and controls](publication-safety.md).
