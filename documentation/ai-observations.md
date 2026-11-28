# AI observations

Measurements recomputed 2026-11-28; graph research release 0.44 dated 2026-11-27. No research-release or review status changed.

Measurements recomputed on 2026-11-28 from the maintained graph, research release 0.44 dated 2026-11-27. The three scope explanations were written on 2026-11-28; no new source research or human editorial acceptance is implied. The older observations below are retained as dated historical interpretations, not freshly verified findings.

## Current measured state

- 1295 canonical public entries; 316 actual developed profile records; 979 canonical entries without one.
- 389 publication-level profile labels, counted separately from actual profile records.
- 105 biographical placeholder descriptions; 107 person records retain first-pass status, including 107 without a developed profile.
- The legacy exact-phrase test for ‘first-pass entry’ returns 0. It does not count the biographical wording and is not an overall completion measure.
- 2992 typed public relation rows; 1302 substantive rows; 649 substantively connected entries and 646 isolates.
- 982 source records, including 957 with public links.

[Download current measurements, definitions, and gap entry IDs](https://transduction.systems/assets/feedback-observations-current.json).

## Current scope explanations

### A readable entry and a developed profile are different records

**Measured:** The current canonical public graph has 1295 entries and 316 developed profile records (24.4%); 979 canonical entries have no developed profile. Separately, 389 entries carry the publication-level label profile. Those labels do not create additional profile records.

**Interpretation:** An orientation, a publication label, and a developed account with sources are different units of work. Counting them together would overstate depth.

**What follows:** Choose a bounded set of entries, read the relevant sources, and develop specific accounts with locators and explicit uncertainty. Do not fill the gap with generic prose.

**Test:** Count canonical entries and actual profile records separately, then inspect the selected accounts and their source locators. A passing build is not editorial acceptance.

### Biographical placeholders remain unfinished

**Measured:** 105 biographical descriptions still contain first-pass wording. 107 person records retain first-pass status; 107 of them have no developed profile. Separately, the legacy exact phrase first-pass entry occurs in 0 canonical records. That exact-phrase count does not measure all unfinished first-pass content.

**Interpretation:** Publication-placeholder work does not establish biographical coverage. The biographical wording, review status, and actual profile records require separate checks.

**What follows:** Develop the unprofiled biographies from primary sources, explaining contributions, limits, and specific connections. Keep all public entries available for random exploration.

**Test:** Recompute each stated predicate and inspect the resulting IDs and profiles. Check that random selection reaches every canonical public entry; an exact-phrase count is not a completion test.

### Graph coverage does not establish agreement or source depth

**Measured:** The canonical public projection has 2992 typed relation rows, including 1302 substantive rows; 649 entries have a substantive connection and 646 do not. The source register contains 982 records, including 957 with public links.

**Interpretation:** The measurement describes this atlas and the chosen relation filters. Source registration, an available link, a source reading, and an accepted claim are distinct.

**What follows:** Keep relation kinds, passage locators, review status, and rival interpretations visible. Refer to the dated research packets for what was actually read and to the unfinished-work register for what remains.

**Test:** Recompute the projection with the stated endpoint and relation rules. Trace an asserted connection to its source and locator; do not treat adjacency, a high degree, or a source count as proof.

## Historical observations

Retained from the observation report dated 2026-10-08 (release 0.31); not re-reviewed as a current finding. 

### Breadth has outrun depth

**Historical measurement:** The atlas has 1259 public entries and 212 developed profiles. Only 16.8% of entries have the fuller profile structure.

**Historical interpretation:** It is now better at showing that something belongs in the territory than at explaining what the thing means, why it matters, where it is contested and how it enters practice.

**Proposed implication:** Next depth work should follow reader demand, bridge concepts and high-risk ambiguities rather than adding another undifferentiated tranche of names.

**Proposed test:** This observation weakens when developed profiles and item-level source coverage grow without sacrificing the breadth inventory.

### One interface contains two different graphs

**Historical measurement:** There are 2763 typed public edges, but 1102 are conceptual, historical, human, practice or contestation relations. The substantive share is 39.9%.

**Historical interpretation:** Authorship, collection membership and other provenance lines answer different questions from influence, dependence or use. Combining them without visible layers makes bibliographic density look like intellectual agreement.

**Proposed implication:** The interface should let readers choose conceptual, human-lineage, practice, contestation and provenance layers explicitly.

**Proposed test:** Readers should be able to explain what became visible or hidden when they change layer, without learning database vocabulary first.

### Expertise needs relations, not biography alone

**Historical measurement:** The named-coverage review separates developed, represented and research-queue states.

**Historical interpretation:** A person's significance becomes useful in the atlas when their work, concepts, disagreements and practice consequences are connected explicitly.

**Proposed implication:** Do not promote requested names to developed profiles merely because they are canonical or famous.

**Proposed test:** Check that each developed person profile has sourced work-level and concept-level relations rather than only a short biography.

### A catalogue is not a critique

**Historical measurement:** Release 0.18 records all 32 terms in one published unFIX synthesis but marks the shared source and bounded status.

**Historical interpretation:** Enumerating a framework's vocabulary does not test its definitions, ancestry, omissions or internal tensions.

**Proposed implication:** Coverage pages should state whether a pass is inventory, interpretation, comparison or critique.

**Proposed test:** Confirm that the unFIX coverage page does not present the 32-item inventory as independent validation of the concepts.

### Practice is named more often than it is connected

**Historical measurement:** The isolate count is concentrated among intervention skills, laws, tools, methods and publications rather than the small conceptual core.

**Historical interpretation:** The source programme has imported lists of capabilities and publications faster than it has documented how ideas are enacted, taught, combined, resisted and changed in use.

**Proposed implication:** Practice cases, practitioner journals, project histories and teaching lineages should now receive deliberate connection work.

**Proposed test:** The practice layer should develop multiple well-sourced routes between concepts, methods, settings, people and consequences.

### Auditability is not yet source diversity

**Historical measurement:** The most reused source is ‘Foundational Papers in Complexity Science — official tables of contents’, attached to 782 public nodes or edges.

**Historical interpretation:** A table of contents can establish titles, authors and collection placement. It cannot establish the meaning, influence or quality of every work it lists. Repetition of one source creates an appearance of corroboration without independent evidence.

**Proposed implication:** Paper-level primary records, publisher pages, DOI metadata, archives, reviews and critical accounts must replace collection-level evidence where stronger statements are made.

**Proposed test:** Source concentration should fall as the number and independence of item-level sources rise.

### The people layer contains an identity-resolution debt

**Historical measurement:** 124 of 275 people — 45.1% — are currently represented by initial-form labels.

**Historical interpretation:** Initials are enough to inventory an authorship string, but not enough to guarantee a unique person. They invite duplicate records, mistaken mergers and false career or influence connections.

**Proposed implication:** Add full names, ORCID or other authority identifiers, affiliations and paper-level checks before deepening those people into intellectual profiles.

**Proposed test:** No initial-only person should acquire interpretive or lineage edges without successful identity resolution.

### The published neighbourhoods are a historical snapshot, not the present graph

**Historical measurement:** Six published neighbourhoods contain 77 unique nodes, while 547 nodes are now connected; 482 connected nodes sit outside the old grouping pass.

**Historical interpretation:** An algorithmic cluster is produced by the current edges, exclusions, resolution setting and seed. It is not a natural school waiting to be discovered.

**Proposed implication:** Recompute neighbourhoods at each suitable release, record the algorithm and version, and retain change over time rather than silently replacing one partition with another.

**Proposed test:** A reader should be able to inspect why two entries share a neighbourhood and see when that grouping changed.

### A few bridge concepts carry much of the atlas's traffic

**Historical measurement:** Feedback, recursion, the Viable System Model, boundary, requisite variety and related bridge entries have markedly higher substantive degree than most of the graph.

**Historical interpretation:** The wording and omissions in those entries influence many possible routes through the atlas. They are single points of interpretive failure as well as useful orientation points.

**Proposed implication:** Give bridge entries multi-source review, rival definitions, domain distinctions and explicit limits before relying on them as navigation hubs.

**Proposed test:** Alternative routes and counter-accounts should reduce dependence on any one bridge without hiding genuine centrality.

### The gaps map the curator's attention as much as they map the field

**Historical measurement:** 712 entries are isolated in the substantive graph, while the largest substantive component contains 465 entries.

**Historical interpretation:** Isolation does not mean an idea is naturally peripheral. It often means the current source set, relation vocabulary or research history has not yet made its connections visible.

**Proposed implication:** Treat isolates as hypotheses about missing work, not as evidence that the field itself has no connections there.

**Proposed test:** Source programmes from different traditions should alter which entries appear central, peripheral or absent.

### Automation readily overreads weak evidence

**Historical measurement:** This release keeps source roles, claim status and open research programmes visible while using scripts to generate and validate the site.

**Historical interpretation:** Automation is good at consistency and propagation; it is also good at propagating an unjustified inference everywhere at once.

**Proposed implication:** Generated breadth needs adversarial checks, source boundaries and explicit stop conditions.

**Proposed test:** Trace a sample of generated relations back to locators and verify that no discovery source has silently become evidence for a stronger claim.

### Presence is not depth

**Historical measurement:** Requested names are published as developed, represented or research-queue entries rather than being forced into one apparent level of completeness.

**Historical interpretation:** A searchable name is an index achievement, not evidence that the atlas explains the person's work, lineage or disputes.

**Proposed implication:** Prominence should follow sourced relational depth rather than the fact that a name win this release.

**Proposed test:** Confirm that research-queue entries do not appear as developed profiles or acquire unsupported influence claims.

### Source duplication hides claim compression

**Historical measurement:** Linda Booth Sweeney's author profile, official site and award record are stored as distinct source roles rather than duplicate records for one URL.

**Historical interpretation:** One page may support several claims, but cloning it as several sources overstates independence and obscures what each citation does.

**Proposed implication:** Source records should identify a distinct public route and a bounded evidential use.

**Proposed test:** Check for duplicate URLs and inspect whether each Sweeney relation cites the source that actually supports it.

### Unfinished corpus work belongs in the public model

**Historical measurement:** Monoskop, Foundational Papers in Complexity Science, SysCoI/model.report, the reading list and company-knowledge discovery remain separately named open programmes.

**Historical interpretation:** A bounded pass can be complete while the wider field remains unfinished; conflating the scales turns project management into an epistemic claim.

**Proposed implication:** Each future pass needs a stated corpus, method, stop condition and visible residual queue.

**Proposed test:** Check that release notes state what was examined and leave the remainder visible rather than calling the whole programme complete.

### Canonical sources have jobs

**Historical measurement:** The canonical source register distinguishes author archives, official organisations, primary works, publisher records and independent counterweights.

**Historical interpretation:** Calling a source canonical does not make it universally authoritative; it identifies the job for which it is the preferred route.

**Proposed implication:** Each source record should state what it can establish and what it cannot.

**Proposed test:** Sample canonical sources and verify that their registered use matches the claims that cite them.

### First-party sources need counterweight

**Historical measurement:** Many profiles begin with author, institutional or publisher sources because these best establish names, dates, declared concepts and official lineages.

**Historical interpretation:** First-party evidence is indispensable for self-description but weak for criticism, contested influence and assessment of consequences.

**Proposed implication:** Developed entries should add independent scholarship or practitioner evidence where interpretation matters.

**Proposed test:** Review high-connectivity profiles and identify claims resting only on the subject's own account.

### A reading-list item is not yet a reading

**Historical measurement:** The reading-list inventory distinguishes developed profiles, represented items and inventory-only records.

**Historical interpretation:** Bibliographic presence records attention and intent; it does not imply that a work has been critically read into the atlas.

**Proposed implication:** Item-level status must remain visible and the wider reading-list programme must stay explicitly partial.

**Proposed test:** Check that inventory-only works do not inherit summaries or relations from title similarity alone.

### Lineage needs infrastructure

**Historical measurement:** The David Ing and systems-in-plural routes connect people, publications, traditions and institutional settings rather than treating a lineage as a list of names.

**Historical interpretation:** Intellectual transmission happens through teaching, collaboration, organisations, conferences and practice as well as citation.

**Proposed implication:** Lineage work should model carriers and settings alongside conceptual influence.

**Proposed test:** Inspect a lineage journey and confirm that it includes at least one institutional or practice-bearing connection.

### Core systems practice is not four tools

**Historical measurement:** The core practice spine holds several approaches together without collapsing them into a single method sequence.

**Historical interpretation:** A compact orientation can aid action while still preserving different purposes, assumptions and forms of evidence.

**Proposed implication:** Guided routes should expose choice and boundary conditions rather than imply one universal workflow.

**Proposed test:** Check whether a reader can see why two adjacent approaches would lead to different interventions in the same situation.

### Attention is not importance

**Historical measurement:** Reading lists, submitted tickets and available corpora shape which people and ideas receive depth first.

**Historical interpretation:** Editorial attention creates visibility and connectivity; neither is a neutral ranking of intellectual worth.

**Proposed implication:** Coverage decisions and unreviewed queues should remain visible beside graph measures.

**Proposed test:** Compare highly connected entries with the release history and ask whether prominence follows evidence, prior attention or both.

### Navigation changes what appears important

**Historical measurement:** The release gives every entry a full reading surface and a constellation view with one selected centre, direct relations and two-step relations.

**Historical interpretation:** A centre selected for a question is not the centre of the field. Interface focus and graph degree can manufacture apparent importance.

**Proposed implication:** The map treats the selected entry as a temporary star and its orbits as question-relative positions.

**Proposed test:** Change the selected entry and layer; the constellation should reorganise without presenting the new centre as canonically primary.

### Links are commitments about possible movement

**Historical measurement:** Navigational cards, search suggestions, surprise routes, map nodes, map connections and entry actions expose stable destinations.

**Historical interpretation:** A control which looks like a link but cannot be copied, opened in a new tab or inspected conceals the structure of the atlas.

**Proposed implication:** Navigation uses links; buttons are reserved for actions whose result cannot sensibly exist as a URL.

**Proposed test:** Right-click or modified-click each navigational surface and confirm that its destination remains coherent in a separate tab.

### The graph is unusually useful to AI — and unusually easy for AI to overread

**Historical measurement:** The atlas provides typed relations, status, source IDs and explicit caveats, but depth and source granularity vary sharply across entries.

**Historical interpretation:** Structured relation types reduce the usual language-model tendency to collapse every association into ‘related to’. The remaining danger is confident completion: turning bibliographic inclusion into influence, a provisional edge into fact, or missing data into a smooth narrative.

**Proposed implication:** AI outputs should expose the exact entries, relation types and sources used; distinguish retrieval from inference; and state when the graph is silent.

**Proposed test:** A useful AI answer should become less fluent, not more, when the evidence is thin or contradictory.

### A line on one map is not the same claim as a line on another

**Historical measurement:** Release 0.20 preserves 1,320 source-reported major-influence links, 307 outward web destinations and 1,856 keyword-labelled citation signals in three separate comparator layers.

**Historical interpretation:** The visual grammar of a line conceals materially different assertions: historical or conceptual influence, a route to further reading, and an aggregate bibliographic signal are not interchangeable.

**Proposed implication:** Comparator imports must retain their source-defined relation meaning and must not be flattened into one generic relationship vocabulary.

**Proposed test:** A reader should be able to state what a link means, and what it does not establish, without consulting the source map's code or private development history.

### Overlap is not agreement

**Historical measurement:** Of 650 Systemic Evolution nodes, 5 are confirmed matches, 57 are partial and 588 remain unresolved; 66 distinct atlas entries are linked through the cumulative reconciliation.

**Historical interpretation:** A plausible name match does not show that two maps use the same boundary, definition or historical claim. Low overlap can expose different vocabularies and purposes as readily as missing coverage.

**Proposed implication:** Reconciliation should preserve confirmed, partial and unresolved states instead of forcing every source node into an apparently equivalent atlas entry.

**Proposed test:** Manually review the highest-connectivity unresolved nodes and record whether each result is identity, broader/narrower scope, a rival term or genuinely absent coverage.

### Preserving every link makes disagreement inspectable

**Historical measurement:** All 307 destinations in the current Castellani image map are retained, including 28 places where its visible label and destination metadata disagree.

**Historical interpretation:** Silently correcting or dropping awkward links would make the derivative cleaner but erase evidence about the source's present state. Complete preservation is useful precisely because it exposes what still needs checking.

**Proposed implication:** Store the source-published value and any later correction separately; preservation must never be presented as endorsement or independent verification.

**Proposed test:** Audit all 307 destinations, distinguish dead links from label mismatches and substantive errors, and return confirmed corrections upstream.

### Aggregation sets an evidential ceiling

**Historical measurement:** The counted-map projection contains 98 concepts, 89 with evidence and 1,856 aggregate signals, while publishing zero raw licensed reference strings; the private corpus and an undocumented shrink step prevent independent rerunning.

**Historical interpretation:** The aggregate can reveal concentrations worth investigating, but it cannot by itself establish direct idea-to-idea influence or allow an independent reader to reproduce the transformation.

**Proposed implication:** Use the signals to prioritise source review, not as canonical relations, and recover the transformation or replace the experiment with a lawful public corpus.

**Proposed test:** Rerun a documented public-corpus version and compare which high-weight signals persist under different vocabularies and thresholds.

### Release metadata is part of the evidence

**Historical measurement:** Reader releases 0.20.3 and 0.20.4 changed public behaviour and source routes while the canonical release field and maintained AI report still said 0.20-prior-maps-alpha.

**Historical interpretation:** A version label is not decoration. If the visible reader and the declared release describe different states, auditability has already broken before anyone inspects a source.

**Proposed implication:** Any public change which alters what a reader can see, follow or infer must advance one maintained release state and regenerate its observations.

**Proposed test:** The badge, canonical data, browser data, citation record and AI-observation report should all name the same release after deployment.

### Interface clutter is an accumulation effect

**Historical measurement:** Successive reader passes added a living mark, release status, curatorship, theme control and a random Little RedQuadrant rule to the same header without redesigning the composition as a whole.

**Historical interpretation:** Each addition can be locally reasonable while their combination becomes globally noisy. The interface has exactly the same coordination problem as any other evolving system.

**Proposed implication:** Reader changes need composition-level review, not only feature-level acceptance. Controls should be given hierarchy, fixed spatial jobs and an explicit reason to remain above the fold.

**Proposed test:** A reader should be able to identify the project, its purpose and the main navigation before noticing release administration or display controls.

### A display layer can manufacture an isolate

**Historical measurement:** Donella Meadows already had documentary authorship paths, but the default substantive map suppressed those paths and made her appear isolated until a narrow source-established Meadows-to-Leverage-Points relation was added.

**Historical interpretation:** Visible isolation can be a property of the chosen layer and relation vocabulary rather than a property of the person or idea being shown.

**Proposed implication:** Isolation counts and visual gaps must always be read with the active layer stated; documentary absence and substantive disconnection are different claims.

**Proposed test:** For a sample of apparent isolates, compare the substantive, documentary and all-relations views before treating isolation as a research finding.

### A live corpus is not ingested coverage

**Historical measurement:** The current SCiO resource catalogue and SysBoK/Kumu routes are now linked and registered, while the catalogue has not been normalised item by item and the live Kumu node-and-link graph has not been silently promoted into the canonical atlas.

**Historical interpretation:** Knowing where the current corpus is and making it inspectable is useful work, but it is not the same achievement as reading, reconciling and evidencing every item in it.

**Proposed implication:** Corpus registration, item-level ingestion, reconciliation and canonical promotion should remain separate publication states.

**Proposed test:** A reader should be able to distinguish a live source route from an atlas statement independently supported by that source.

### Linking a source graph is not canonising it

**Historical measurement:** SysBoK-derived material now carries routes to both SCiO's project page and the live Kumu model while retaining SCiO's own work-in-progress status and its Precedents and Dependent Derivatives semantics.

**Historical interpretation:** Better provenance can increase access to another graph without pretending that its links have already passed the evidential tests of this one.

**Proposed implication:** Comparator and source graphs should travel with visible credit and original relation meanings until individual claims have been reconciled.

**Proposed test:** Inspect a SysBoK-backed item and confirm that its source graph is one click away while its relations are not automatically relabelled as canonical Tangle relations.

### Permission attaches to a version

**Historical measurement:** Benjamin Hadorn granted the requested project-specific use scope on 26 August 2026, then reviewed and approved the exact package identified by SHA-256 on 31 August 2026.

**Historical interpretation:** Permission is not a permanent adjective which can be pasted onto a changing dataset. It is a dated relationship between a grantor, a scope, conditions and an identifiable version.

**Proposed implication:** The source artefact, derivative, review manifest and publication decision must remain distinct records. Later graph-data changes reopen the review gate.

**Proposed test:** A reader should be able to identify the exact approved package, its checksum, attribution conditions and approval date without treating silence by another copied recipient as approval.

### A bibliography has an audience

**Historical measurement:** The Barrett–Shepard introduction explicitly frames its selection for social scientists and distinguishes six categories. Its bibliography pages are absent from the supplied post.

**Historical interpretation:** The source explains a boundary, but cannot supply item-level coverage that is not present in the available text.

**Proposed implication:** Catalogue the available entries and the missing pages separately.

**Proposed test:** Can every claimed ingested item be found in the actual supplied material?

### An awkward date belongs in the record

**Historical measurement:** The short list described as 1956 includes a 1957 publication. Fano’s single entry names two reports, and Current Biography supplies no article title.

**Historical interpretation:** Silently regularising dates or titles would replace documentary evidence with a cleaner story.

**Proposed implication:** Retain source wording alongside reconciliation and review status.

**Proposed test:** Check that source entries survive even where a canonical identity remains unresolved.

### A catalogue entry is a distinct unit of work

**Historical measurement:** The intake accounts for 48 entries, four selected-passage reviews, one archive metadata check, and one unidentified reference.

**Historical interpretation:** Adding searchable records increases access to material while leaving a larger close-reading task open.

**Proposed implication:** Show review depth beside each entry and keep bibliography membership outside influence relations.

**Proposed test:** Filter by evidence reviewed; verify that catalogue-only entries do not appear as fully read.

### An entrance changes who can use the atlas

**Historical measurement:** The systems-thinking entrance presents a worked example and inquiry before exposing the larger graph. The rules are retained on a static page and removed from the atlas header.

**Historical interpretation:** The route into a knowledge collection affects who can participate without prior familiarity.

**Proposed implication:** Provide useful static content and followable links alongside richer interactive views.

**Proposed test:** Read the gateway and source catalogue with JavaScript unavailable; follow each named route.

### A checkable exercise is not accreditation

**Historical measurement:** 26 original practice pages cover every core approach and theory row in the inspected public SCiO portfolio, with different depth limits.

**Historical interpretation:** Mechanical model checks can expose errors without establishing competence in organisational application.

**Proposed implication:** Preserve attempts, revisions, scope limits and the need for observed practice.

**Proposed test:** Can a learner distinguish a case check from a professional assessment?

### Access, reading, and review are different forms of progress

**Historical measurement:** This pass read 5 complete researcher PDFs (32 pages), the 12-module OCAD pro forma, and the ISSS resource list (57 bibliographic entries). All 85 notebook comments and 14 open issues have a disposition.

**Historical interpretation:** A longer bibliography increases discoverability. It does not show that the works have been read or that the claims have received human review. New graph claims retain candidate status.

**Proposed implication:** Prioritise primary-source verification and human review where a new distinction affects practice. Do not use link or node counts as a proxy for confidence.

**Proposed test:** Sample the new claims against their page locators; ask a human editor to accept, qualify, or reject them. Check whether a reader can distinguish original text, secondary reconstruction, and editorial application.

