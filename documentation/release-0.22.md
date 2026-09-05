# Release 0.22: a readable entrance and source-accounted enrichment

Release prepared 5 September 2026 in response to the current request and
the two additions in [running feedback issue #2](https://github.com/antlerboy/the-necessary-tangle/issues/2).
Benjamin P Taylor explicitly authorised publication and future direct publication
of requested site changes on 5 September 2026. The public
[digest](https://transduction.systems/updates/0.22/) summarises the change and next work.

## Reader changes

The static `/systems-thinking/` page starts from recurring situations, gives
a worked waiting-list example and a ten-minute inquiry, and offers routes
into six kinds of systems practice. It introduces systems thinking,
cybernetics, and complexity without requiring prior familiarity with the
atlas. It includes a contents list, semantic headings, focus indicators,
responsive typography, dark-mode styles, and a print treatment. Its useful
content and navigation do not require JavaScript.

The atlas gains a clear entrance link, an early-cybernetics callout, refreshed
release metadata, and three journeys. The header rule is retired. All 256
RedQuadrant rules are retained as static text with stable anchors, local JSON,
and a portable random-rule component for the two receiving sites. See the
[receiving-site handoff](redquadrant-rules-handoff.md).

## Source accounting and credit

The Wiener reading lists and Barrett–Shepard introduction were shared by
**Sean Manion, @TheUnjournaling** and transcribed on Systems Community of
Inquiry. The source compilers and publication authors have separate credits.

| Supplied section | Entries retained |
| --- | ---: |
| Selected readings, 21 March 1952 | 8 |
| Short bibliography described as 1956 | 20 |
| Popular treatments, approximately 1951 | 15 |
| Popular pieces by Wiener | 5 |
| **Total source rows** | **48** |

These give 46 work keys: 45 resolved works and one unidentified Current
Biography issue reference. Wiener’s two books recur in different lists. The
Macy seventh conference and a later combined conference range remain distinct
references. Fano's combined citation is not misrepresented as two inspected
reports. Cherry's 1957 book remains visible in the list described as 1956.

The Barrett–Shepard post provides three introduction pages and six categories,
but none of the bibliography's hundreds of entries. The two works named in
that introduction are retained with the compilers' different assessments.
The missing pages are needed for the requested complete bibliography pass.

Four selected primary-text reviews deepen Fano's TR 65, Ashby's *Design for a
Brain*, the Shannon–Weaver 1949 volume, and Wiener's *Too Damn Close*. An
archive metadata check expands the 1946 Ashby article title. The machine
catalogue gives URLs and passage locators beside each reviewed entry. This
pass does not claim to have read all the listed works or whole books.

## Richness and boundaries

The release grows from 635 to 719 canonical public entries, 128 to 137
developed profiles, 216 to 224 public source records, 1,882 to 1,987 typed
statements, and 21 to 24 journeys. New profiles distinguish technical,
semantic, and effectiveness questions; information coding; ultrastability;
and essential variables. Journeys connect these ideas to practical inquiry
and the choices involved in constructing a field's bibliography.

Bibliography membership and explicit credits are documentary relations.
Primary passages support narrower conceptual relations; no new generic
'related to' edges, invented historical influence, or false human review
credits are introduced. Candidate records remain subject to curator review.
The approved Systemic Evolution package and other comparator imports retain
their existing evidence and permission boundaries.

## Build and verification

`make validate` now rebuilds the historical baseline before running its
version-specific gates, then applies 0.22 and runs the current public-data,
work-spine, release-integrity, and interaction checks. `make build` emits
0.22. Pages uses the same complete gate and records the deployed commit
afterwards, so its former 0.21 preparation steps cannot downgrade a release.

The current gate checks exact source counts and rule texts, review depth,
identity and reference integrity, data projection equality, primary-source
credits, static routes, preserved comparator checksums, and JavaScript
behaviour for search/filter/reset and random-rule/failure fallback. Static
checks do not constitute a browser or assistive-technology audit.

## Remaining decisions and work

1. Publish the validated release and verify its gateway, digest, and deployment identity.
2. Obtain the missing Barrett–Shepard bibliography pages and continue primary
   reading of the catalogue-only works; keep coverage labels honest.
3. Apply the queued, site-specific rules integrations in their next updates.
4. Configure systemsthinking.info's redirect after the gateway is published.

The source intake and release-state templates live in `sources/`; generated
public pages and data are rebuilt from them. The historical reader input is
`sources/release-22/reader-base.html`; change it or the current overlay rather
than making an unrecorded edit to the generated `docs/index.html`. The source wording remains
available alongside reconciliation, so later corrections can be traced.
