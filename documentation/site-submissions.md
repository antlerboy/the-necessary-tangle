# Public submissions and responses

The public page is <https://transduction.systems/submissions/>.

GitHub Issues remains the canonical record. The page is a generated and live-refreshed projection so that a reader can see proposals, statuses, curator responses and resulting entries without knowing GitHub's interface.

## Intake rule

A website submission creates a public issue containing the marker `Prepared from The Necessary Tangle`. Nothing changes the atlas automatically. The curator checks identity, duplication, wording, evidence, rights, public safety and compatibility with the data model.

## Status vocabulary

- awaiting review;
- investigating;
- incorporated;
- partly incorporated;
- disputed;
- deferred;
- declined.

A closed issue is not silently presented as accepted. A contribution which originates a useful change remains attributed even where its wording is not used as evidence.

## Reference implementation

Issue 21 proposed a distinction between viability, fitness and natural drift. Release 0.12 incorporated the underlying distinction after checking independent sources. Release 0.17 surfaces the proposal, public response and resulting entries on the website.

## Automation

The triage workflow creates and maintains the `site-submission` and status labels. The public page also reads the GitHub API at view time, with the numbered-release snapshot as a fallback. This avoids a second editorial database while retaining a usable public page.
