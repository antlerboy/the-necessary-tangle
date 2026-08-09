# Publishing on GitHub Pages

The repository includes a deployment workflow in `.github/workflows/pages.yml`.

## One-time repository settings

1. Open the repository’s **Settings**.
2. Open **Pages**.
3. Under **Build and deployment**, set **Source** to **GitHub Actions**.
4. Open **General** under repository settings and enable **Discussions**.

After the files are on `main`, the Pages workflow validates the public build and deploys the `docs/` folder.

The intended public address is:

https://antlerboy-benjamintaylor.github.io/the-necessary-tangle/

## Future updates

A push to `main` runs validation and publishes the current `docs/` folder. Pull requests run the validation workflow without publishing.

## Custom domain

A custom domain can be added later without changing the site architecture. Keep the GitHub Pages address working as the fallback and verify any custom domain through GitHub before use.
