# Explicit semantics

The Necessary Tangle uses an explicitly typed graph. The semantics are not the positions of dots on a screen.

## Entity types

Each maintained entry has a stable identifier, a public label, an entity type, a publication level and a canonical identity. A person, publication, concept, practice, organisation and method are different kinds of thing even when their names are similar.

## Relation types

Every connection has a named relation type and a plain-language phrase. The record also states whether it is directed. `authored by`, `teacher of`, `historical precursor`, `formal prerequisite`, `uses`, `critiques` and `often confused with` are not interchangeable forms of `related to`.

## Evidence and status

A connection records source identifiers, evidence locators where available, confidence, statement status, scope conditions, review status and the method by which the statement was formed. A discovery source can lead to evidence without itself proving the statement.

## Identity and redirects

Canonical identifiers remain stable when labels change. Alternate names and spelling variants are aliases. A canonical redirect records that two records resolve to one maintained identity; it is not a claim that the terms have always been historically identical.

## Graph views

Map layers filter relation families. Algorithmic neighbourhoods are provisional descriptions of the current graph, not natural schools. Spatial proximity, colour and clustering do not add unstated semantic relations.

## Nodica comparison

[Nodica](https://github.com/kvistgaard/nodica) is an RDF graph visualisation and a useful comparator. The Necessary Tangle currently publishes typed JSON records and does not claim RDF compatibility. A future interoperability test should export the graph, preserve relation direction and provenance, and round-trip it without losing the editorial distinctions above.

## Next technical step

Publish a machine-readable schema and test an RDF/JSON-LD export. The test is not whether another tool can draw the nodes. It is whether meaning, direction, evidence, status, scope and canonical identity survive the translation.
