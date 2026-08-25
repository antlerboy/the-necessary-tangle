# Map of Systemic Evolution comparator

Release: `0.20-prior-maps-alpha`

Public page: <https://transduction.systems/prior-maps/systemic-evolution/>

## Source and provenance

The source page is
<https://uranos.ch/index.php/research-menu/cybernetcis>. It records this history:

- originated in 1996 by Eric Schwarz;
- extended in 1998 with material from Will Durant's *The Story of Philosophy*;
- elaborated in 2000–01 for the International Institute for General Systems
  Studies;
- extended in 2016 by Benjamin Hadorn.

Benjamin Hadorn confirmed permission for appropriate use on 25 August 2026.
The full provenance remains attached and the source owners' terms continue to
apply.

The map was already published in Benjamin P Taylor's 2019 SysCoI collection of
former systems maps and histories. Nigel Williams subsequently extracted and
analysed the GraphML in his `systems-map` fork and built the first comparator
implementation. Those are distinct contributions and are credited separately.

## What the source says its links mean

The source page states that nodes denote topics such as scientific work or
research areas and that directed edges illustrate **major influences between
topics**. It also publishes a colour legend for scientific realms.

The GraphML contains 650 labelled nodes and 1,320 links: 1,262 single-headed and
58 double-headed. No individual edge carries label text, a citation or a more
specific influence type. Release 0.20 therefore records every edge as:

- `relation_type: reported_major_influence`;
- `accuracy_status: source_reported_not_independently_verified`;
- `specific_relation_status: not_stated_by_source`.

This corrects an earlier fork draft which said the source supplied no meaning or
legend. The GraphML alone did not; the public source page did.

## Colour legend

| Colour | Published realm | Extracted nodes |
| --- | --- | ---: |
| grey | philosophy | 139 |
| black | physical sciences | 106 |
| orange | social systems | 84 |
| green | biology and medicine | 73 |
| blue | mathematics | 73 |
| yellow | symbolic systems | 52 |
| dark red | computers and informatics | 49 |
| purple | engineering | 19 |
| red | cybernetics | 18 |
| cyan | systems analysis | 18 |
| light green | ecology | 18 |
| `#666699` | not identified in the published legend | 1 |

The source legend also names white as general system. White is the fill of 618
of 650 extracted nodes, so fill cannot safely be treated as a one-to-one realm
classification without further confirmation from the maintainers.

## Cumulative reconciliation

The first human-reviewed pass links five source nodes directly and 57 compound
or narrower/broader source nodes partially to 66 distinct Tangle entries. 588
remain unresolved.

Of the 1,320 source links:

- 47 have both endpoints at least partly reconciled;
- 231 have one endpoint reconciled;
- 1,042 have neither;
- one reconciled pair also carries an independently sourced canonical Tangle
  relation;
- zero canonical relations were created merely because the source map draws a
  link.

The full node-and-link ledger is
`data/systemic-evolution-reconciliation.json`.

## Reproduction

`scripts/import_comparator_graphml.py` extracts the supplied yEd GraphML.
`scripts/build_systemic_evolution_reconciliation.py` applies the reviewed
mapping and reports any identity drift. `scripts/validate_prior_maps_20.py`
protects the counts, source semantics, permission record and non-promotion
boundary.
