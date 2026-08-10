# Public data model

The canonical public dataset is generated into `data/public-data.json` and copied into `docs/assets/` by the build.

## Main records

- `nodes` — concepts, people, methods, laws, practices, publications, organisations and events;
- `edges` — typed, directed or undirected connection statements;
- `relation_types` — the controlled meanings available for an edge;
- `sources` — bibliographic and public-link records;
- `evidence` — exact source locators and concise evidential summaries;
- `claims` — the inherited machine-facing name for inspectable statements which may be supported, disputed or superseded;
- `profiles` — fuller public accounts of selected entries;
- `journeys` — curated routes through entries;
- `canonical_redirects` — duplicate and variant records redirected to one maintained entry;
- `corpus_register` — bounded research programmes and their current status;
- `canonical_source_register` — preferred sources for specified evidential jobs, with tier, status and use;
- `emergent_categories` — provisional graph communities plus their curatorial names and member identifiers;
- `coverage_gap_categories` — under-connected territories exposed by the current graph;
- `graph_snapshot` — reproducible counts for the substantive public graph;
- `participation_roles` — project roles, repository permissions and publication authority;
- `automation_contribution_rule` — sponsorship, provenance and review requirements for LLM and automated work.

## Canonical names and aliases

Each public thing has one maintained identifier and label. Acronyms, former names, alternate spellings and common variants are aliases. Search uses these aliases; they must not become duplicate entries.

## Connection vocabulary

Connection types distinguish conceptual dependence, history, influence, human lineage, institutions, practice, comparison and contestation. Generic ‘related to’ links are not published.

An edge is a particular typed statement. More than one edge may connect the same pair where the meanings differ. Release 0.7 therefore reports both substantive edge records and unique undirected pairs used for clustering.

## Emergent categories

The build does not infer that a category is a natural kind. `scripts/analyse_emergent_categories.py` projects canonical public entries and substantive public-public edges into a simple undirected graph, runs the pinned community-detection pass and checks the resulting membership sets against `emergent_categories`.

The algorithm groups. The curator names and interprets. The machine-readable analysis records both stages and the parameters used.

## Public and private boundary

Private sources may be used for discovery outside this repository. Public records must contain only public links or proper bibliographic/archive citations marked ‘No public link’. Private SharePoint, mail, local paths and confidential material must not enter this dataset.
