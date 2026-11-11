# Current packet: two editions of Making things change

## Resource-link correction, 11 November 2026

Benjamin P Taylor authorised correction and republication of the first edition.
The corrected v0.01.1 BT PDF preserves the first edition's text and artwork,
restores twelve external resource links, and records the correction date on the
last page. Its verified SHA-256 is
2ef341ab0a6da91b6d70a273b7c27d683e91e371d1db3dcaa6ae30f5d0231b34
(6,331,082 bytes; 32 pages). The manifest identifies the public source and exact
download filename. The original static download address remains an alias to the
corrected bytes. The revised v0.02 edition is unchanged. The existing guide
browser check also verifies the alias's hash. Publication and live verification
are established by the Publish workflow and deployment.json.

## Original publication packet

Authorised by Benjamin P Taylor on 11 November 2026. Publish the first and revised
32-page guides together at /library/making-things-change/, with v0.02 first,
explicit draft status, source dates, exact filenames, and verified PDF hashes.
Add routes from the homepage, systems-thinking introduction, and source library.
Reconcile the existing SysCoI resource for post 29454; preserve its identity and
provenance. No graph additions, conceptual relationships, or historical claims.

Implementation: sources/making-things-change/guide.json and
scripts/build_making_things_change.py, with the final Makefile overlay.
Acceptance: make validate; desktop and narrow-screen inspection of the guide
and its two downloads; successful publication and live PDF hash checks.
The bottom-right Open updates control and existing access remain unchanged.

Status: source implementation complete. The Publish workflow supplies the full
validation, desktop/mobile download checks, deployment identity, and live
verification. Consult that result and deployment.json for publication status.

