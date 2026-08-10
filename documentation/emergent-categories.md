# Emergent categories: first graph pass

This note records what the public evidence graph groups together at release `0.7-constellation-alpha` and, equally, what it fails to connect.

It is a snapshot of the atlas, not a taxonomy of reality.

## Method

The pass used canonical public entries and substantive public-public connections. Classification, documentary, source/evidence and unresolved legacy links were excluded. Edge direction and confidence were not used in the first clustering calculation.

After the Principia Cybernetica additions the graph contains:

- 204 public entries;
- 96 substantive typed connection records across 94 unique node pairs;
- 77 entries with at least one substantive connection;
- 127 isolated entries;
- 129 connected components;
- one dominant component of 75 entries, one two-entry component and 127 singletons.

The clustering projection collapses parallel typed statements to a simple, undirected, unweighted graph of 94 node pairs. NetworkX `louvain_communities` 3.6.1 was run with seed `1` and resolution `1.0`. This produced six non-singleton groups and 127 singleton groups. The six non-singleton groups were then named by inspecting their hubs, neighbours and relation wording. The machine-readable result is in [`emergent-categories-analysis.json`](emergent-categories-analysis.json), and the reproducing script is `scripts/analyse_emergent_categories.py`.

That last step matters. The algorithm partitions a graph; it does not supply an interpretation. The category names are curatorial statements about the calculated groups.

## Present neighbourhoods

### Feedback, regulation and learning

Feedback is the main hub connecting negative and positive feedback, homeostasis, control theory, purposeful behaviour, feedforward, single- and double-loop learning, quality management and system dynamics. Wiener, Black, Maxwell and Bernard supply parts of the historical line.

Evolutionary cybernetics currently joins this group through the general cybernetics entry. That makes it a bridge but also shows how one extra relation can move a whole tradition between communities.

### Recursion and formal construction

Recursion is a large hub connecting recursive definition and computation, fractals and a wide historical cast including Turing, Gödel, Hilbert, Dedekind, Peano, Chomsky, Panini, Pingala, Maturana and Varela.

This is structurally striking but epistemically suspect. Most of the spokes have degree one. The cluster may encode an inherited narrative around recursion more than a demonstrated web of direct relations among its members.

### Viability, variety and regulatory laws

The Viable System Model, regulation, requisite variety, variety amplification and attenuation, viability, adaptation, autonomy, cohesion, identity and organisational recursion now group with the Law of Requisite Variety, the Conant–Ashby theorem, W. Ross Ashby and Roger Conant.

This is a useful change from the earlier graph. Formal regulatory statements and organisational design are beginning to appear as one connected neighbourhood rather than two source-defined clusters. The bridge still needs more direct evidence about how particular VSM formulations use the law and theorem.

### Observer, self-organisation and connected knowledge

The Principia Cybernetica first pass forms a distinct neighbourhood around the project and its web, metasystem transition, semantic network and global brain, joined to observer, self-organisation, emergence and Heinz von Foerster.

This is both an intellectual cluster and a cluster about how knowledge is organised. It makes a predecessor project part of the subject matter rather than leaving it as a detached comparator.

### Boundary, information and transduction

Boundary connects information, information theory, distinction, purpose, transduction and systemic intervention. Shannon and Midgley appear as human anchors.

In the previous snapshot, observer, self-organisation and emergence sat within this group. The Principia pass pulled those nodes into the connected-knowledge neighbourhood. That is not a discovery that they have ‘really moved’. It is evidence that the graph is still sparse enough for a modest batch of relations to change its topology substantially.

### McCulloch–von Domarus fragment

Warren McCulloch and Eilhard von Domarus form a two-node component through one recorded human connection.

It is shown because small fragments reveal where lineage work has begun. It should not be read as a category of equal weight to the five larger neighbourhoods.

## The larger finding: under-connection

The current graph is sparse. In release 0.7, 127 of 204 public entries have no substantive public connection.

The largest isolated groups by entity type remain practice-heavy:

- intervention skills;
- laws or principles;
- concepts;
- methods or methodologies;
- tools;
- people;
- traditions.

This does not show that practice is naturally separate from theory. It shows that the project has so far been better at collecting and describing practice labels than at evidencing their conceptual, historical and human connections.

The next relation-building work should therefore favour bridges over more isolated dots:

- method to concept;
- method to documented use;
- teacher to learner;
- practitioner to declared influences;
- institution or event to collaborators;
- law or principle to the primary text and practical setting in which it is used;
- competing accounts of the same lineage.

## Why the categories are not ‘the answer’

The cluster pattern changes when any of these change:

- the boundary of the atlas;
- source coverage;
- the evidence threshold;
- relation-type definitions;
- inclusion or exclusion of provisional links;
- edge direction and weight;
- the clustering algorithm and resolution;
- the curator's language for naming a mathematical cluster.

The atlas is one of the observers in its own map. Its categories are traces of interaction among the field, the sources, the data model, the algorithm and the curator.

## Tests for the next pass

The grouping will become more credible if:

- clusters persist under several reasonable algorithms and relation filters;
- the strongest links have exact primary-source locators;
- domain stewards recognise the pattern while identifying its distortions;
- rival classifications can be represented without forcing a single partition;
- bridge-building work reduces isolation without merely adding vague ‘related to’ lines;
- the interface lets readers compare espoused categories with observed graph neighbourhoods.
