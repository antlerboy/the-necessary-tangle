# Explicit semantics in The Necessary Tangle

The atlas does not treat every line as ‘related to’. Its public graph uses explicit semantics at several levels.

## Nodes

Each node has a stable identifier, human label, entity type, publication level, visibility, description, source set and review state. Entity types distinguish people, concepts, methods, practices, traditions, institutions, publications, tools, laws and other roles in the graph.

## Connections

Each connection states:

- source and target;
- relation type and broader relation family;
- whether direction matters;
- a plain-language phrase;
- evidential and review status;
- source and evidence identifiers;
- scope conditions, notes and temporal qualifiers where relevant.

Authorship, collaboration, teaching, documented influence, conceptual dependence, classification, practical use and historical sequence are therefore not interchangeable.

## Evidence and uncertainty

A typed line is still a curatorial statement, not a fact made certain by putting it in JSON. The source record, locator, confidence, status and scope remain inspectable. Missing lines can mean missing evidence, work not yet done, or an editorial boundary. They do not prove that no relationship exists.

## Emergent neighbourhoods

Graph neighbourhoods are computed observations over a selected set of substantive connections. They are provisional views, not canonical schools. Changing the relation filter, evidence threshold, algorithm or release can change the neighbourhoods.

## RDF and Nodica

The current public export is JSON rather than a formal RDF publication. Its identifiers and typed predicates are designed so that an RDF or JSON-LD mapping can be produced without inventing the semantics afterwards. Ivo Velitchkov’s Nodica is registered as a useful comparator because it works directly with RDF graph visualisation and demonstrates a different route from explicit semantic data to a navigable public graph.

A later semantic-web release should publish:

- a documented namespace;
- JSON-LD context and RDF export;
- predicate definitions, domains and ranges;
- provenance using maintained vocabularies where they fit;
- validation shapes;
- versioned mappings from the current relation vocabulary.

The aim is machine-readable precision without pretending the ontology has escaped curatorial judgement.
