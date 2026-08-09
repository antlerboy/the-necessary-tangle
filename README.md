# The Necessary Tangle

**A living evidence atlas of systems | cybernetics | complexity.**

**Every connection must say what it means.**

The Necessary Tangle is a public, navigable account of ideas, people, methods, publications, institutions, practices and traditions in systems | cybernetics | complexity. It distinguishes relationships that ordinary family trees often collapse together: logical dependence, historical sequence, explicit influence, teaching, collaboration, citation, practical use, comparison and dispute.

Curated by [Benjamin P Taylor](https://www.antlerboy.com/).

## Public site

**https://antlerboy.github.io/the-necessary-tangle/**

The site includes:

- fuzzy search across canonical names, aliases and acronyms;
- readable entries with sources and evidence;
- guided journeys through connected ideas;
- a clickable map with inspectable lines;
- question-led exploration and prepared public context for ChatGPT;
- structured routes for corrections, challenges, sources and discussion;
- embedded explanations of coverage, method, rights and current limitations.

## Status

This is a public alpha. It has broad seed coverage and a smaller number of evidence-deepened entries. Breadth is not presented as completeness, and editorial acceptance is not presented as final consensus.

The strongest current material is around boundaries and observers; feedback and regulation; variety, viability and the Viable System Model; recursion; emergence; and self-organisation. Human and institutional lineage, the complexity corpus and practice transmission need much more work.

The [coverage programme](documentation/coverage-programme.md) now makes the next corpus and lineage passes explicit, including the *Foundational Papers in Complexity Science*, relevant Monoskop material, the SysCoI and model.report archives, prior maps and bodies of knowledge, practitioner influence constellations, and private company-knowledge discovery with public-source replacement.

## Start here

Readers: open the [public site](https://antlerboy.github.io/the-necessary-tangle/).

Contributors: read [CONTRIBUTING.md](CONTRIBUTING.md), then use the repository's Issues or Discussions.

Maintainers: read [documentation/maintenance.md](documentation/maintenance.md) and [documentation/publishing.md](documentation/publishing.md).

## Build and validation

The site is plain HTML, CSS and JavaScript. Python scripts prepare, enrich and validate the public data.

```bash
make validate
make serve
```

GitHub Actions validates proposed changes and deploys the `docs/` folder to GitHub Pages.

## Repository structure

```text
docs/               public GitHub Pages site
data/               canonical public dataset
documentation/      public method, coverage and maintainer documentation
scripts/            build, release-enrichment and validation scripts
.github/             contribution forms and deployment workflows
```

## Origins and acknowledgements

The immediate provocation is David Ing's formulation, as Benjamin records it: ‘we need to map the constellation of influences around practitioners’.

The project develops the connected-body-of-knowledge approach of the original SCiO Systems Thinking Body of Knowledge and later competency work. It draws on the Grammar of Systems corpus, public archives and scholarship, professional bodies, teaching traditions, practitioner knowledge, and earlier attempts to map the field.

See [ACKNOWLEDGEMENTS.md](ACKNOWLEDGEMENTS.md) for the fuller account. This is an independent project, not an official canon or position of SCiO or any other named organisation.

## Rights

Original atlas text, public data and editorial material are licensed under [Creative Commons Attribution-ShareAlike 4.0 International](LICENSE-CONTENT.md), unless otherwise marked. Original software is licensed under the MIT licence in [LICENSE-SOFTWARE.md](LICENSE-SOFTWARE.md). Third-party works remain under their own terms. See [RIGHTS.md](RIGHTS.md).
