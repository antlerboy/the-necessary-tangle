# Publishing on GitHub Pages

The Necessary Tangle is published from the canonical repository:

https://github.com/antlerboy/the-necessary-tangle

The live public site is:

https://antlerboy.github.io/the-necessary-tangle/

## Repository settings

GitHub Pages uses **GitHub Actions** as its build source. Repository Issues and Discussions should remain enabled because they provide the public correction and dialogue routes.

## Normal publication

A push to `main` runs `.github/workflows/pages.yml`. The workflow:

1. builds and enriches the public dataset;
2. applies the current public-site wording and release metadata;
3. generates the public conversational knowledge file;
4. validates names, URLs, source safety, data references and required interface elements;
5. checks JavaScript syntax;
6. deploys the `docs/` folder to GitHub Pages.

Pull requests run the validation workflow without publishing.

## After publication

Check at least:

- search and autocomplete, including a close misspelling such as `viabilty`;
- an entry page and its sources;
- a guided journey;
- node and line selection on the map;
- a question in the Ask view;
- the correction and discussion routes;
- the About page, licence and acknowledgements;
- phone and desktop layouts.

## Custom domain

A custom domain can be added later without changing the site architecture. Keep the GitHub Pages address working as the fallback and verify a custom domain through the canonical `antlerboy` account before changing DNS.
