# Maintaining the project

## Normal edit cycle

1. Review the Issue or Discussion.
2. Identify the maintained entry and the exact statement at stake.
3. Check the source and locator.
4. Edit `data/public-data.json` or the generating source used for that release.
5. Run `make validate`.
6. Open the site locally with `make serve` and inspect the changed entry, connections and search behaviour.
7. Commit the change with a clear message.
8. Merge through a pull request where practical.
9. Publish a numbered release for substantive editorial batches.

## Build commands

```bash
make build
make validate
make serve
```

The build applies the base public-data enrichment, release-specific public metadata and corpus registrations, public-site wording, and the generated conversational knowledge file before validation.

## Public/private boundary

Only public-safe data belongs in this repository. Keep private research notes and internal source material elsewhere. Do not add the earlier private editorial workbench to this repository.

## Adding aliases

Add genuine alternate names, spelling variants and acronyms. Do not add generic words copied from labels such as ‘system’, ‘model’, ‘concept’ or ‘method’. Validation rejects ambiguous or generic aliases.

## No-op changes

A proposed edit whose ‘before’ and ‘after’ records are identical must not be recorded as a substantive revision. Treat it as a usability event or close it without changing the canonical data.
