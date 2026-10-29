# Next work

Status: implemented — Said to someone edition 1.1, authorised by Benjamin P Taylor on 29 October 2026. Release validation and publication evidence are recorded in the associated pull request and GitHub Pages workflow.

## Outcome

Expand https://transduction.systems/saidtosomeone/ beyond its ten selected entries into a source-led register covering every numbered item of Heinz von Foerster's 1995 anthology, its additional circularity material, and further sayings and reported variants established by public papers, interviews, and firsthand accounts. Make the large TNT logo animate and change using the same living-mark behaviour as the main site.

## Authority and scope

The user's explicit follow-up is the authorised work packet under AGENTS.md. Named areas: sources/saidtosomeone/, docs/saidtosomeone/, scripts/build_saidtosomeone.py, scripts/test_saidtosomeone_browser.js, .github/workflows/validate.yml, .github/workflows/pages.yml, existing sources/living-mark-*.js and docs/assets/living-marks/ for reuse, main-site markup/styles needed to understand the existing controls, Makefile, validation/browser checks as needed, docs/index.html, docs/library/index.html, docs/sitemap.xml, README.md, CHANGELOG.md, and documentation/NEXT_WORK.md and TANGLE_STATE.md. The companion page has its own numbered edition; atlas dataset release 0.34 remains unchanged.

No arbitrary numerical cap. Coverage is measured against inspected collections and documented sources, not claimed for everything Heinz ever said. Exact quotations, wording variants, paraphrases, borrowed attributions, reports, and unsupported circulating claims remain distinct. Preserve third-party source permissions: a complete anthology topic index can link to original wordings and diagrams without wholesale reproduction. Preserve the four stories, media and reading routes, Benjamin's imagined Don Van Vliet conversation, and exactly one disclosed marginal invention with the visible 'contains hallucinations' warning. Use the existing mark assets and interaction design. Preserve reduced-motion support and the bottom-right Open updates control.

## Acceptance checks

Run make validate and the relevant browser checks. Verify full anthology item coverage, unique stable IDs, source-level quote budgets and locators, source ledger consistency, build reproducibility, valid internal paths and anchors, responsive layout, accessible controls, both animation and mark-changing actions, reduced motion, and exact live publication after the existing GitHub Pages workflow succeeds. Publication must refer to the tested commit.

## Execution and stop conditions

Independent research tasks cover the anthology/primary texts and reported sayings. A separate logo task can reuse the existing implementation while the owner integrates content and verifies publication. One implementation pass and one verification pass; corrections address named failures. No wider atlas review, private disclosure, or external correspondence. Stop after successful required checks and live publication. Record concrete remaining source gaps without inventing contents or treating an inaccessible source as verified.

## Verification record

Primary-source and reported-speech reviews completed independently. The register has 54 entries with linked locators, 40 source records, a complete index of the 29-item anthology and its supplementary material, and four further numbered-series indexes. Source corrections were integrated before release. Structural checks passed for unique IDs, internal paths and anchors, source mappings, and source-level quotation limits. The builder produces identical companion outputs on repeated runs.

The browser preview verified animation/pause, motif changes by button and keyboard, combined search and evidence filters, and phone/tablet/desktop layouts without horizontal overflow. The new browser regression checks these behaviours and reduced-motion defaults in PR validation, the pre-publication build, and the live deployment. Required `make validate` and the full browser suite remain release gates; the workflow records their result for the tested commit.
