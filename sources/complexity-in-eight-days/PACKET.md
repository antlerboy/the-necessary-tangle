# Complexity in Eight Days source addition

Authorised by Benjamin P Taylor on 9 November 2026. The requested outcome is a source entry for Fred Amonya's lecture notes on transduction.systems.

## Scope

Add the original ResearchGate reference, an attributed reading of the inspected 33-page PDF, precise page and section locators, and editorial routes to existing concepts. Publish one companion reading page and one searchable source-register record. Preserve existing atlas graph claims, source-owner-reviewed material, and the current audience. Do not redistribute the PDF or imply a verified publication date or open licence.

## Source and interpretation

The original source URL, PDF metadata limits, inspected-copy checksum, and concept locators are in `source.json`. The notes treat modelling choices explicitly. They do not supply a general definition of a system or a historical comparison of systems thinking and cybernetics. The comparison with Ashby's *An Introduction to Cybernetics* (1956), sections 6/13–6/14, is editorial; no influence or priority claim is made.

## Files and verification

The source packet, `scripts/build_complexity_eight_days.py`, its final Makefile build step, generated `/reading/complexity-in-eight-days/` page, source catalogue, source-index link, sitemap, and marked NEXT_WORK notice comprise this change. Run `make validate` with the same pinned `_systemsmap` dependency as the existing Pages workflow, inspect the new page at desktop and mobile widths, confirm source-register search and links, and verify publication identity. Existing workflow checks remain in force.

The clean rebuild exposed an existing release-0.30 sitemap failure: the practice-page rebuild can remove the events URL before the release overlay updates it. The narrow correction in `scripts/apply_update_30.py` ensures that existing route is inserted when absent. Its existing validator continues to require the exact route and date; no validation rule is relaxed.

Stop after these checks and successful publication. Publication does not establish independent editorial or scholarly review. No further research programme is implied.
