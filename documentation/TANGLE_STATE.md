# Tangle state

Last verified: 25 August 2026

## Public release

- Release: `0.20-prior-maps-alpha`
- Public site: https://transduction.systems/
- Machine relationship snapshot: `data/relationship-quality.json`
- Prior-map hub: https://transduction.systems/prior-maps/
- Map of Systemic Evolution: 650 nodes; 1,320 source-reported links
- Castellani current source links: 307
- Counted-map aggregate links: 1,856
- Canonical relations created merely from comparator imports: 0

## Current shape

Release 0.20 publishes three distinct comparator views without flattening them
into the canonical atlas. The Systemic Evolution page retains the full
Schwarz–Durant–IIGSS–Hadorn provenance and shows the cumulative reconciliation.
The Castellani page preserves all current outward links while exposing source
label disagreements. The counted-map page retains aggregate signals while
excluding the private Scopus corpus and raw licensed reference strings.

The generated release contains 635 canonical public
entries, 128 developed profiles, 216
public source records, 762 total graph records and
1882 canonical graph statements.

## Current limits

The comparator links are source claims or aggregate signals, not a guarantee of
accuracy. Most Systemic Evolution nodes remain unreconciled, Castellani's links
have not been individually checked, and the counted-map aggregate cannot yet be
independently rerun from a public source corpus.

## Release controls

Run `make build`, then `make validate`. Check the public deployment, the main
reader and all four prior-map/contribution routes after merge.
