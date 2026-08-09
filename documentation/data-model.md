# Public data model

The public dataset is stored in `data/public-data.json` and copied into `docs/assets/` by the build script.

## Main records

- `nodes` — concepts, people, methods, laws, practices, publications, organisations and events;
- `edges` — typed, directed or undirected connections;
- `sources` — bibliographic and public-link records;
- `evidence` — exact source locators and concise evidential summaries;
- `claims` — inspectable statements which may be supported, disputed or superseded;
- `profiles` — fuller public accounts of selected entries;
- `journeys` — curated routes through entries;
- `canonical_redirects` — duplicate and variant records redirected to one maintained entry.

## Canonical names and aliases

Each public thing has one maintained identifier and label. Acronyms, former names, alternate spellings and common variants are aliases. Search uses these aliases; they must not become duplicate entries.

## Connection vocabulary

Connection types distinguish conceptual dependence, history, influence, human lineage, institutions, practice, comparison and contestation. Generic ‘related to’ links are not published.
