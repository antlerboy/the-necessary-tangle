# Reader entrance and public source routes, 13 October 2026

Benjamin P Taylor authorised this bounded update in the current request: update TNT and make the About pages intelligible to external readers. Related public requests are issue #2 comments 6132533563 and 6132538217.

## Outcome

A reader-first About entrance, two self-contained guides, eleven attributed map and collection routes, and eight selected Design Horizon source routes.

## Evidence and limits

The review.json record contains only public-safe citations, brief source descriptions, locators, access status and editorial questions. Live Design Horizon entries and About were inspected on 13 October. Resource destination pages were read for the stated scope. Retrieved map copies were identified and deduplicated; original public sources or bibliographic routes replace restricted copies. Native collection enumeration failed, so full inventory isn't claimed. An image-only retrieved paper was identified by its title page; it isn't counted as a field map.

No new canonical graph claims are made. Editorial atlas cross-links are navigation, not statements of historical influence. The approved Systemic Evolution comparator is unchanged.

## Implementation and checks

Source templates and review.json are applied at the final build stage by scripts/apply_update_32.py. The prior reader entrance is restored before historical gates by scripts/prepare_update_32_baseline.py. make validate passed the complete historical/current gate; validate_update_32 checks internal source-route targets, privacy, reviewed comparator hashes and repeatability. CI runs the dedicated reader checks at desktop and mobile widths before and after deployment.

## Remaining work

Complete collection enumeration and unindexed-image discovery; check unavailable originals and ambiguous map editions; read linked works at statement level before adding graph relationships. Restricted source material needs a public equivalent or source-owner permission.
