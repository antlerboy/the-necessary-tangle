# The Necessary Tangle

**A living evidence atlas of systems | cybernetics | complexity.**

**Every connection must say what it means.**

The Necessary Tangle is a public, navigable account of ideas, people, methods, publications, institutions, practices and traditions. It distinguishes logical dependence, historical sequence, explicit influence, teaching, collaboration, citation, practical use, comparison and dispute.

Curated by [Benjamin P Taylor](https://www.antlerboy.com/).

## Public site

**https://antlerboy.github.io/the-necessary-tangle/**

Release `0.7-constellations-alpha` includes:

- 295 readable public entries;
- a complete bibliographic first pass across all 89 historical papers in *Foundational Papers in Complexity Science*;
- a connected first pass through the Principia Cybernetica project, website, dictionary, people and key concepts;
- a canonical public source register which states what each source is and is not good for;
- provisional observed neighbourhoods and an explicit report of the weakly connected research periphery;
- richer map layers, labels, colour modes, visible controls and pointer-centred wheel zoom;
- public membership roles and a curator-approved application route;
- a protocol for agent-assisted contributions under named human responsibility.

The paper inventory is not yet 89 full scholarly summaries. The neighbourhoods are not a discovered natural taxonomy. The membership form grants no automatic access.

## Start here

Readers: open the [public site](https://antlerboy.github.io/the-necessary-tangle/).

Contributors: read [CONTRIBUTING.md](CONTRIBUTING.md), [documentation/participation-and-access.md](documentation/participation-and-access.md) and [AGENTS.md](AGENTS.md) where relevant.

Maintainers: read [documentation/maintenance.md](documentation/maintenance.md) and [documentation/publishing.md](documentation/publishing.md).

## Build and validation

The site is plain HTML, CSS and JavaScript. Python scripts prepare, enrich and validate the public data.

```bash
make validate
make serve
```

GitHub Actions validates proposed changes and deploys the `docs/` folder to GitHub Pages.

## Current research structure

The graph currently produces a few coherent neighbourhoods around feedback and learning; recursion and self-reference; viability and variety; boundaries and intervention; and observation and emergence. A small Principia Cybernetica cluster also appears. Most other non-publication entries remain isolated under the published analysis rules.

That pattern is useful chiefly as a diagnosis of the atlas. It points to missing evidence and relation work, not hundreds of natural schools. See [documentation/emergent-neighbourhoods.md](documentation/emergent-neighbourhoods.md).

The wider work is tracked in [documentation/coverage-programme.md](documentation/coverage-programme.md).

## Origins and rights

The immediate provocation is David Ing’s formulation, as Benjamin records it: ‘we need to map the constellation of influences around practitioners’.

The project develops the connected-body-of-knowledge approach of the original SCiO Systems Thinking Body of Knowledge and later competency work. See [ACKNOWLEDGEMENTS.md](ACKNOWLEDGEMENTS.md).

Original atlas text, public data and curatorial material are licensed under [Creative Commons Attribution-ShareAlike 4.0 International](LICENSE-CONTENT.md), unless otherwise marked. Original software is licensed under the MIT licence in [LICENSE-SOFTWARE.md](LICENSE-SOFTWARE.md). Third-party works retain their own terms.
