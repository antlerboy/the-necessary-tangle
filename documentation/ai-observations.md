# AI observations

Generated for release `0.9-observations-alpha` on 2026-08-10.

These observations combine reproducible counts from the public graph with model-assisted interpretation. Measurements, interpretations and proposed tests are kept separate. They are not autonomous editorial decisions and should be challenged against the data and sources.

## Measured state

- 411 public entries; 32 developed profiles.
- 542 typed public edges; 174 substantive edges.
- 141 substantively connected entries and 270 substantive isolates.
- 93 sources, of which 80 have public links.

## Breadth has outrun depth

**Basis:** measurement plus interpretation.

**Measured:** The atlas has 411 public entries and 32 developed profiles. Only 7.8% of entries have the fuller profile structure.

**Interpretation:** It is now better at showing that something belongs in the territory than at explaining what the thing means, why it matters, where it is contested and how it enters practice.

**Implication:** Next depth work should follow reader demand, bridge concepts and high-risk ambiguities rather than adding another undifferentiated tranche of names.

**Test:** This observation weakens when developed profiles and item-level source coverage grow without sacrificing the breadth inventory.

## One interface contains two different graphs

**Basis:** measurement plus design inference.

**Measured:** There are 542 typed public edges, but 174 are conceptual, historical, human, practice or contestation relations. The substantive share is 32.1%.

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

**Measured:** 108 of 143 people — 75.5% — are currently represented by initial-form labels.

**Interpretation:** Initials are enough to inventory an authorship string, but not enough to guarantee a unique person. They invite duplicate records, mistaken mergers and false career or influence connections.

**Implication:** Add full names, ORCID or other authority identifiers, affiliations and paper-level checks before deepening those people into intellectual profiles.

**Test:** No initial-only person should acquire interpretive or lineage edges without successful identity resolution.

## The published neighbourhoods are a historical snapshot, not the present graph

**Basis:** measurement plus model warning.

**Measured:** Six published neighbourhoods contain 77 unique nodes, while 141 nodes are now connected; 64 connected nodes sit outside the old grouping pass.

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

**Measured:** 270 entries are isolated in the substantive graph, while the largest substantive component contains 84 entries.

**Interpretation:** Isolation does not mean an idea is naturally peripheral. It often means the current source set, relation vocabulary or research history has not yet made its connections visible.

**Implication:** Treat isolates as hypotheses about missing work, not as evidence that the field itself has no connections there.

**Test:** Source programmes from different traditions should alter which entries appear central, peripheral or absent.

## The graph is unusually useful to AI — and unusually easy for AI to overread

**Basis:** experience-based AI observation.

**Measured:** The atlas provides typed relations, status, source IDs and explicit caveats, but depth and source granularity vary sharply across entries.

**Interpretation:** Structured relation types reduce the usual language-model tendency to collapse every association into ‘related to’. The remaining danger is confident completion: turning bibliographic inclusion into influence, a provisional edge into fact, or missing data into a smooth narrative.

**Implication:** AI outputs should expose the exact entries, relation types and sources used; distinguish retrieval from inference; and state when the graph is silent.

**Test:** A useful AI answer should become less fluent, not more, when the evidence is thin or contradictory.

# Risks of publishing the atlas

## False authority and reputational overclaim

A polished interface can make brief, provisional or collection-derived entries look settled.

Controls: Visible depth and status labels; source locators; explicit rival accounts; release notes that state what was not done.

## False genealogy

Citation, co-presence, chronology, teaching, collaboration and influence can be collapsed into one implied family tree.

Controls: Typed relations; minimum evidence by relation; disputed and unresolved states; no inferred influence from co-occurrence alone.

## Privacy and confidential-source leakage

Private SharePoint, email or client material can enter public data through research notes, URLs, excerpts or generated summaries.

Controls: Separate private lead logs; public-source replacement; automated private-URL scanning; human review before merge; complete deletion from history when secrets appear.

## Copyright and licence error

Open access, public availability and permission to republish are not the same thing.

Controls: Link and summarise; store bibliographic facts and short evidence summaries; record source terms; do not relicense third-party works.

## Identity collision

Initials, alternate names and shared names can merge different people or split one person into several records.

Controls: Authority identifiers, affiliation and publication checks, canonical redirects, and no interpretive edges before resolution.

## Source monoculture and boundary capture

A few corpora define what the atlas notices, making their omissions look like properties of the field.

Controls: Source-mining register; comparator programme; coverage reporting by tradition and domain; deliberate rival and critical sources.

## Automated feedback loops

AI-generated descriptions may be re-ingested, cited or paraphrased until an unsupported statement acquires the appearance of independent repetition.

Controls: Named human sponsor; provenance to non-generated sources; mark AI assistance; never treat generated text as corroboration.

## Vandalism or premature contributor access

A public collaboration request can be mistaken for direct editorial authority.

Controls: Issues and pull requests by default; branch protection; required validation; curator approval; granular roles only in an organisation account.

## Security and operational disclosure

Workflow files, logs, repository history or backups can reveal tokens, internal hostnames and infrastructure detail.

Controls: Least-privilege tokens; secret scanning; protected environments; encrypted off-platform backups; routine restore tests; no credentials in repository data.

## Public permanence

Deletion from the current branch does not guarantee removal from forks, caches, clones or repository history.

Controls: Assume publication is durable; minimise personal data; use GitHub's sensitive-data removal process promptly when required.
