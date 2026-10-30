# ISSS wiki reading and inventory — 30 October 2026

Benjamin requested that the ISSS wiki be worked through thoroughly, in the public
update notebook: https://github.com/antlerboy/the-necessary-tangle/issues/2#issuecomment-6519254955.
His subsequent request authorised these updates and corrections for publication.

## Evidence and actual coverage

The public MediaWiki API (`https://wiki.isss.org/api.php`) supplied a complete
main-namespace `allpages` inventory with continuation exhausted. Eighteen
40-page-or-smaller batches retrieved `info`, current `revisions` (main-slot
content, IDs and timestamps) and `categories`. Every returned page ID matches
the inventory. The source’s `siteinfo` confirmed CC BY 4.0 and its own 248-article
counter. There are 704 main-namespace pages: 502 non-redirect pages and 202
redirects. File, category, template, user and talk namespaces were not inventoried.
Do not describe the 704 as substantive articles or independent works.

`inventory.json` preserves exact source revisions, contributor-history URLs,
source-text SHA256 digests, source-listed credits/dates, categories, shortened
wiki descriptions, redirect resolution, placeholders and reading status. All 704
revision texts were retrieved. Substantive full wiki-page reading is recorded
only for the 19 IDs in `full_reading_page_ids`. These supply the seven original
question-led routes in `routes.json`. Other pages remain source-text intake,
not a claim of completed substantive review. No linked book, paper, slide deck
or recording was read or watched for this packet. No universal corpus review,
independent verification or human editorial acceptance is asserted.

The 194 unfinished person templates are retained as incomplete sources, not
imported as biographies. The 202 redirects are retained for reconciliation, not
counted as more works. Main search excludes redirects, unfinished biographies,
general navigation pages, conference archives and recording collections. Duplicate
mini-symposium pages sharing the same primary Vimeo recording have one main-search
record. The complete inventory retains both pages and their source statements.
Wiki descriptions are credited to ISSS Wiki contributors; work authors and
presenters retain separate source-listed credits. The archive is CC BY 4.0;
underlying works retain their own terms.

## Reader result and reconciliation

`/reading/isss-wiki/` adds seven reading questions, exact source locators,
explicit access and reading limits, five named source gaps and a searchable,
paginated complete index. The existing 57-entry student bibliography at
`/learning/isss/` remains a separate route. The existing differentiation and
integration resource is linked rather than duplicated as a new atlas entry.
Source inconsistencies remain visible: Kineman’s citation versus the infobox
typo, tentative group leadership, the Flanagan January date disagreement,
unpopulated biography fields and planned versus evidenced 2026 outcomes.

The atlas remains release 0.35 with the same graph, profiles and source-owner
artefacts. Editorial reading links do not establish new graph relationships.
Current publication identity, validation and live acceptance belong to the
established Publish workflow and `deployment.json`. The existing backup workflow
is preserved.

## Acceptance and stop

Run the idempotent companion build and full `make validate`, then
`scripts/test_isss_wiki_browser.js` at desktop/mobile sizes before publication and
against the live deployment. Check the exact deployed commit, guide source
locators, complete inventory, all 19 reading statuses, filter counts, shareable
records, main library integration, learning navigation, keyboard entry and Open
updates. Stop after publication and live verification; correct only named failed
checks. Deeper reading of other wiki pages and primary works remains a separate
finite cohort, not silently completed by retrieval.
