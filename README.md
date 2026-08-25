# The Necessary Tangle

## Release 0.19

Release 0.19 gives the atlas a living visual identity. Each fresh load selects one of ten curator-supplied still or moving marks while the wordmark, navigation and reading environment stay stable. Motion is silent and falls back to a still for reduced-motion readers. The release also registers the complete Santa Fe Institute *COMPLEXITY* podcast and transcript archive as a bounded source corpus, with explicit limits on what an episode, transcript or show-note link can establish.

Public routes:

- https://transduction.systems/
- https://transduction.systems/corpora/complexity-podcast/
- https://transduction.systems/coverage/named/
- https://transduction.systems/coverage/unfix-32/


**A living evidence atlas of systems | cybernetics | complexity.**

**Every connection must say what it means.**

The Necessary Tangle is a public, navigable account of ideas, people, methods, publications, institutions, practices and traditions in systems | cybernetics | complexity. It distinguishes relationships that ordinary family trees often collapse together: logical dependence, historical sequence, explicit influence, teaching, collaboration, citation, practical use, comparison and dispute.

Curated by [Benjamin P Taylor](https://www.antlerboy.com/).

## Public site

**https://transduction.systems/**

The site includes:

- fuzzy search across canonical names, aliases and acronyms;
- readable entries with sources and evidence;
- guided journeys through connected ideas;
- a clickable map with inspectable lines;
- question-led exploration and inspectable, copyable public context;
- structured routes for corrections, challenges, sources and discussion;
- embedded explanations of coverage, method, rights and current limitations.

## Status

Release 0.19 contains 635 canonical public entries, 128 developed profiles and 214 public source records. It adds the living-mark family and the bounded *COMPLEXITY* podcast corpus intake.

This is a public alpha. Release 0.16 contains 633 canonical public entries, including 127 developed profiles, 211 sources and 21 guided journeys. Breadth is not presented as completeness, and editorial acceptance is not presented as final consensus.

Release 0.17 contains 633 canonical public entries, 127 developed profiles, 211 sources and 21 guided journeys. It adds a public submissions-and-responses page, a genuine ‘Surprise me’ route across readable content, and a canon-and-lineage review which develops Michael C. Jackson, Magnus Ramage, Karen Shipp and *Systems Thinkers* while making the atlas's own visibility and identity rules explicit.

Release 0.16 makes the 33 *Grammar of Systems* laws and principles visible as a connected web rather than a disconnected list. The book-to-law statements are source-backed; the new law-to-concept, law-to-law and law-to-practice crosswalk is explicitly provisional and open to page-level evidence and challenge.

The [relational-depth programme](documentation/relational-depth.md) now measures every public entry by distinct reader neighbours and relation families, separately from the evidential strength of those statements. The first graph-wide cohort removes reader-isolated entries, connects all maintained intervention skills, and leaves thin people, publications and corpora visible as an ordered research queue rather than disguising them with generic “related to” links.

The strongest current material is around boundaries and observers; feedback and regulation; variety, viability and the Viable System Model; systems laws and strategy; context-sensitive sense-making and Cynefin; applied practitioner lineages; recursion; emergence; and self-organisation. Human and institutional lineage, the complexity corpus and practice transmission still need much more work.

The [coverage programme](documentation/coverage-programme.md) makes the next corpus and lineage passes explicit, including the *Foundational Papers in Complexity Science*, relevant Monoskop material, the SysCoI and model.report archives, prior maps and bodies of knowledge, practitioner influence constellations, and practice sources which can be supported by public evidence.

The [original vision audit](documentation/original-vision-audit.md) compares the current atlas with the commissioning conversation and original specification, and turns the remaining gap into ordered acceptance criteria.

The [Dave Snowden and Cynefin source account](documentation/snowden-cynefin-sources.md) distinguishes the evidential roles of author archive, project wiki, primary papers, publisher records and public institutional applications.

The [reading-list depth map](https://transduction.systems/reading-list.html) exposes all 110 captured items and distinguishes developed profiles, thinner representation and inventory-only coverage.

## Start here

Readers: open the [public site](https://transduction.systems/).

Continue into the living field through the [Systems Community of Inquiry](https://www.syscoi.com/), [SCiO capability and accreditation](https://www.systemspractice.org/professional-accreditation), [SCiO professional development](https://www.systemspractice.org/professional-development), and [Benjamin P Taylor's reading list](https://stream.syscoi.com/2024/10/01/updated-rough-draft-systems-complexity-cybernetics-reading-list/).

Contributors: read [CONTRIBUTING.md](CONTRIBUTING.md), then use the repository's Issues or Discussions. Site-generated issues are labelled and reviewed alongside research issues and pull requests before release; see [documentation/contribution-intake.md](documentation/contribution-intake.md).

Readers who want to inspect what a line means should start with [documentation/explicit-semantics.md](documentation/explicit-semantics.md). Current gaps against Benjamin's reading list and the SCiO curriculum are recorded in [documentation/reading-list-coverage.md](documentation/reading-list-coverage.md) and [documentation/scio-coverage.md](documentation/scio-coverage.md).

Maintainers: read [documentation/maintenance.md](documentation/maintenance.md) and [documentation/publishing.md](documentation/publishing.md).

AI-assisted work starts with [AGENTS.md](AGENTS.md), then the concise [current state](documentation/TANGLE_STATE.md), [design and content rules](documentation/DESIGN_AND_CONTENT_RULES.md), [next authorised work](documentation/NEXT_WORK.md) and [cost-effective work protocol](documentation/WORK_PROTOCOL.md). This operating spine is deliberately smaller than the full documentation set.

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

Public contributions and responses are visible at <https://transduction.systems/submissions/>; the canon and lineage review is at <https://transduction.systems/canon-and-lineage/>.
