# The Necessary Tangle

**A living evidence atlas of systems, complexity and cybernetics.**

**Every connection must say what it means.**

The Necessary Tangle is a public, navigable account of ideas, people, methods, publications, institutions and traditions in systems, complexity and cybernetics. It distinguishes relationships that ordinary family trees often collapse together: logical dependence, historical sequence, explicit influence, teaching, collaboration, citation, practical use, comparison and dispute.

Created and edited by [Benjamin P Taylor](https://chosen-path.org/).

**Publishing this prepared release:** see [PUBLISH_NOW.md](PUBLISH_NOW.md).

## Public site

The GitHub Pages site is designed to be published at:

**https://antlerboy-benjamintaylor.github.io/the-necessary-tangle/**

It includes:

- fuzzy search across names, aliases and acronyms;
- readable entries with sources and evidence;
- guided journeys through connected ideas;
- a clickable map with inspectable lines;
- question-led exploration and prepared public context for ChatGPT;
- structured routes for corrections, challenges, sources and discussion.

## Status

This is a public alpha. It has broad seed coverage and a smaller number of evidence-deepened entries. Breadth is not presented as completeness, and editorial acceptance is not presented as final consensus.

The current public build contains only public-safe material. Private email, company systems, internal documents and private URLs are excluded.

## Start here

Readers: open the [public site](https://antlerboy-benjamintaylor.github.io/the-necessary-tangle/).

Contributors: read [CONTRIBUTING.md](CONTRIBUTING.md), then use the repository’s Issues or Discussions.

Maintainers: read [documentation/maintenance.md](documentation/maintenance.md) and [documentation/publishing.md](documentation/publishing.md).

## Build and validation

The site is plain HTML, CSS and JavaScript. Python scripts prepare and validate the public data.

```bash
make validate
make serve
```

GitHub Actions validates proposed changes and deploys the `docs/` folder to GitHub Pages.

## Repository structure

```text
docs/               public GitHub Pages site
data/               canonical public dataset
documentation/      public method and maintainer documentation
scripts/            build and validation scripts
.github/             contribution forms and deployment workflows
```

## Origins and acknowledgements

The project develops the connected-body-of-knowledge approach of the original SCiO Systems Thinking Body of Knowledge and later SCiO competency work. It draws on the Grammar of Systems corpus, public archives and scholarship, professional bodies, teaching traditions and practitioner knowledge.

Particular acknowledgement is due to Tony Korycki and contributors to the earlier SysBoK work; Patrick Hoverstadt and colleagues who developed and published the Grammar of Systems; Igor Perko for a major researchers-network comparator; and the many authors, teachers, practitioners and archivists cited in the atlas.

This is an independent project. It is not an official canon or position of SCiO or any other named organisation.

## Rights

The repository’s original software is available under the MIT licence described in [LICENSE-SOFTWARE.md](LICENSE-SOFTWARE.md). The atlas text, data and editorial structure remain all rights reserved until a public content and data licence is chosen. See [RIGHTS.md](RIGHTS.md).
