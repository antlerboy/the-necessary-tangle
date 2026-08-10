# Maintaining the project

## Normal edit cycle

1. Review the Issue or Discussion.
2. Identify the maintained entry and the exact statement at stake.
3. Check the source and locator.
4. Edit `data/public-data.json` or the generating source used for that release.
5. Run `make validate`.
6. Open the site locally with `make serve` and inspect the changed entry, connections and search behaviour.
7. Commit the change with a clear message.
8. Merge through a reviewed pull request. `CODEOWNERS` keeps the curator in the review path; branch protection should require the validation workflow before merge.
9. Publish a numbered release for substantive curatorial batches.

## Build commands

```bash
python3 -m pip install -r requirements-analysis.txt
make build
make analyse
make validate
make serve
```

## Public/private boundary

Only public-safe data belongs in this repository. Keep private research notes and internal source material elsewhere. Do not add the earlier private curatorial workbench to this repository.

## Adding aliases

Add genuine alternate names, spelling variants and acronyms. Do not add generic words copied from labels such as ‘system’, ‘model’, ‘concept’ or ‘method’. Validation rejects ambiguous or generic aliases.

## No-op changes

A proposed edit whose ‘before’ and ‘after’ records are identical must not be recorded as a substantive revision. Treat it as a usability event or close it without changing the canonical data.
