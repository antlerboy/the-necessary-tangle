# What the three prior maps have that we do not

A coverage check, not a courtesy. Each prior map was read for the areas it
names, those areas were added to our vocabulary, and the corpus was allowed to
decide which of them reach our map. Nothing was added by assertion.

## The 2021 Map of the Complexity Sciences (Castellani & Gerrits)

68 areas read off the map. **21 our vocabulary already tested. 47 it did not.**
Those 47 were added and the build re-run.

### 15 reached the map on their own literature

| Area | Works | Span |
| --- | --- | --- |
| Systems biology | 144 | 2002–2026 |
| Systems science | 90 | 1974–2026 |
| Big data and data science | 29 | 2012–2026 |
| Dynamical systems theory | 23 | 1989–2025 |
| Fractal geometry | 22 | 1985–2024 |
| Nonlinear dynamics | 14 | 1988–2026 |
| Robustness and control | 7 | 2006–2024 |
| Multi-scale modelling | 6 | 2009–2022 |
| Case-based complexity | 5 | 2020–2025 |
| Computational social science | 4 | 2015–2024 |
| Economic complexity | 4 | 2010–2021 |
| Scaling laws | 3 | 2014–2026 |
| Qualitative and mixed methods | 3 | 2006–2021 |
| Computational biology and chemistry | 3 | 2010–2022 |
| Biosystems engineering | 3 | 2008–2024 |

None arrived isolated: 210 edges join them to the concepts already on the map,
and 34 run between them. The strongest are systems science to general system
theory (169 references, 87 citing works) and systems biology to general system
theory (161 references, 137 citing works).

### 23 did not — and then six topic-scoped exports were added

On the author-seeded corpus, 23 of Castellani's areas fell below threshold and
twelve returned zero works: graph theory, computational complexity theory,
genetic algorithms, robotics and multi-agent systems, data mining, digital
social research, complexity and psychology, complexity policy, complexity
political science, intersectionality, complexity in health and healthcare,
complexity in education.

That list was almost exactly Castellani's applied, computational and
social-science strands, and it measured where our sampling was blind rather than
where the literature was thin. Six topic-scoped exports were run against it,
taking the corpus from 34,883 documents to 85,832 and from 6.18M reference rows
to 13.79M.

The gap closed almost entirely. Of the twelve that returned nothing, nine are
now on the map:

| Area | Works | Was |
| --- | --- | --- |
| Swarm behaviour | 1,980 | 2 |
| Intersectionality | 927 | 0 |
| Robotics and multi-agent systems | 238 | 0 |
| Genetic algorithms | 228 | 0 |
| Graph theory | 99 | 0 |
| Data mining | 51 | 0 |
| Connectionism | 30 | 0 |
| Complexity in health and healthcare | 27 | 0 |
| Computational complexity theory | 7 | 0 |

Swarm behaviour and intersectionality are now among the largest literatures on
the map. Neither existed on it a build ago.

Four of Castellani's areas remain absent: complexity policy, complexity
political science, complexity and psychology, and complexity in education. Two
of those returned exactly two works, so they are close. Whether the remainder is
genuine absence or too-narrow aliases is an open, checkable question — see
`LIMITATIONS.md` section 4.

The wider lesson is the one worth keeping: a comparator map found a hole in our
sampling that our own data could not reveal, we sampled against it, and the map
grew from 43 evidenced concepts to 89.

## The Map of Systemic Evolution (Schwarz 1996 → Hadorn 2016)

Its distinctive holdings are the deep pre-1950 lineage — astronomy from Babylon
through Ptolemy and Brahe, rational mechanics, instrument-making from Archimedes
to Babbage — and non-Anglophone traditions: Tektology, pansystems, general
tropodynamics, interpretive systemology, ergonology.

We have deliberately not chased most of it, for a stated reason: that stratum is
a 1998 import from Will Durant's popular history of philosophy, unsourced at
node level, and Scopus indexes cited references only from 1970, so a citation
map cannot reach it. Tektology is in our vocabulary and sits below threshold.
The rest is a job for authority files and archival sources, not bibliometrics.

## The Necessary Tangle (Taylor)

We take its rule, not its content: every published connection must state its
meaning, and citation, teaching, collaboration and influence are different
claims. That principle is the reason our only relation type is
`literature_cites` and why every edge carries its scope conditions.

## What we have that none of them do

The systems practice and management tradition is thin or absent in Castellani
and patchy in Hadorn. On our map, evidenced from the corpus: Viable System
Model, soft systems methodology, critical systems thinking, systems practice,
operational research, action research, organisational learning, socio-technical
systems, sociocybernetics, dialectical systems theory, grey systems, and
requisite variety.

And the thing none of the three can do at all: every line here states what it
means and carries the count, the number of distinct citing works and the DOIs
behind it.
