# What this map cannot yet tell you

Written at v0.1, from the first build. These are properties of the corpus and
the method, not defects to be tidied away later.

## 1. The corpus decides the map

The first corpus was assembled from author-name batches seeded on the *Map of
Systemic Evolution*, and it showed: the applied, computational and
social-science literatures were almost entirely missing, because the sampling
had gone looking for people rather than topics.

Six topic-scoped exports have since been added. The corpus is now 85,832
documents and 13,792,287 reference rows, and the journal profile has shifted
accordingly — *Physica A*, *Physical Review E*, *IEEE Access*, *Sustainability*,
the *International Journal of Environmental Research and Public Health* and the
*Journal of Business Research* now sit alongside *Kybernetes* and *Systems
Research and Behavioral Science*.

The effect was large. Evidenced concepts went from 43 to **89 of 98**, and
areas that previously returned zero works — swarm behaviour, intersectionality,
genetic algorithms, robotics and multi-agent systems, graph theory, data
mining, connectionism, complexity in health — are now among the better-evidenced
entries on the map.

15,406 works match at least one concept. The map rests on those, not on the
field. A concept marked `candidate` still means *not present in this corpus at
this threshold*, never *this literature is small*.

## 2. Broad terms out-compete precise ones

The largest literatures are now network science (3,891 works), swarm behaviour
(1,980), machine learning and AI (1,927) and case-based complexity (1,526).
Systems thinking, which dominated the first build at 377, now sits seventh at
429.

That reordering is itself a warning. It did not happen because the field changed
between builds; it happened because the corpus did. Size on this map measures
how much of the sampled literature uses a phrase in its title, which is a real
finding about how research labels itself, and not a measurement of which ideas
matter most.

The method also favours phrases that appear in titles at all. An idea discussed
without being named — requisite variety in a paper about regulation, say — is
invisible to it.

## 3. A quarter of the edges lean on very few bibliographies

291 of 1,856 edges are flagged `concentrated`: one citing work supplies half or
more of the supporting references. Those edges are real
in the sense that the citations exist, and weak in the sense that a single
author's reference list drew the line.

The flag is in the data so a reader can see it. It is not a reason to delete the
edge; it is a reason not to read it as a property of the field.

## 4. The vocabulary is the gate, and it has edges

An earlier build used a hand-written topic filter to decide which works could be
considered at all. It quietly decided which literatures were visible: human-
computer interaction and constructivism returned zero works not because the
corpus lacked them but because the filter's wording excluded them before
counting began. The filter is gone — a work is now on topic because it matches a
concept being tested.

What remains is alias coverage. Nine concepts still fall below threshold, four at
zero: Constructivism, Boundaries and observers, Variety engineering, Recursion, Complexity and psychology, Complexity policy, Complexity political science, Complexity in education, Philosophy of complexity. For some this is genuine absence from the
corpus. For others — constructivism, boundaries and observers, variety
engineering — the aliases are probably too narrow, and the literature is being
missed rather than being absent. Widening them is a separate, checkable pass.

## 5. Title matching is coarse

Concepts are matched against work titles and reference strings, not abstracts or
keywords — those are licensed Scopus fields and stay out of this repository. A
paper about requisite variety that never says so in its title is invisible here.
This trades recall for a clean rights position, deliberately.

## 6. Citation is the only relation so far

`literature_cites` counts references. It says nothing about influence, teaching,
agreement, derivation or logical dependence, and the map should not be read as
if it did. Those are separate claims needing separate evidence and their own
relation types.

Direction is reliable — citation runs from later work to earlier — so the map
can support "this literature drew on that one". It cannot support "this idea
came from that one" without further work.

## 7. Pre-1970 is structurally thin

Scopus indexes cited references only from 1970. The foundational layer —
Wiener 1948, Bertalanffy 1949, Ashby 1952 and 1956, Bogdanov 1922 — appears here
only as something later work cites, never as work that cites. Any apparent
sparseness before 1970 is a property of the index.

## What would move each of these

| Limitation | What fixes it |
| --- | --- |
| Corpus bias | Journal-scoped and topic-scoped exports, not author-scoped |
| Hub artefacts | Splitting broad concepts into narrower ones with their own tests |
| Concentrated edges | More citing works, from a wider export |
| Coarse matching | An abstract-level pass held outside the repository |
| One relation type | Curated conceptual edges, each separately sourced |
| Pre-1970 thinness | OpenAlex, which indexes the works themselves |
