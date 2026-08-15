# Tangle state

Last verified: 2026-08-15

Current release: `0.16-grammar-connections-presentation-alpha`

Public site: <https://transduction.systems/>

Quality snapshot generated: 2026-08-14

This is the concise restart point for implementation work. It records current
facts, not aspirations. Detailed rationale remains in the linked documents.

## Current shape

The Necessary Tangle is a public, static, versioned multiplex evidence graph of
systems | cybernetics | complexity. It is not a taxonomy, encyclopaedia, reading
list, social graph or decorative network, although it offers views with some of
those forms.

The current machine-readable quality snapshot reports:

| Measure | Current |
| --- | ---: |
| Canonical public entries | 565 |
| All graph nodes | 675 |
| Typed edges | 1,809 |
| Sources | 195 |
| Developed profiles | 115 |
| Guided journeys | 20 |
| Reader-connected entries | 555 |
| Semantically connected entries | 382 |
| Semantic-gap entries | 183 |
| Thin or unconnected entries | 274 |

The authoritative machine result is `data/relationship-quality.json`. If these
figures change, update this summary in the same reviewed change.

## What is working

- Typed, inspectable statements with direction, relation family, status, sources
  and evidence fields.
- Search, readable entries, guided journeys, path finding and question-sized map
  views.
- Static reproducible publication with extensive data and interface validation.
- A strong restrained visual foundation and a protected bottom-right ‘Open
  updates’ magic dot.
- Explicit public contribution, challenge and human review routes.

## Current priority gap

The principal mismatch is evidential depth rather than breadth. Documentary
connectivity can mask weak semantic connection; locators and rationales remain
uneven; many people and publications have only one relation family. The live gap
register identifies `R1`, `R2`, `R4`, `C1` and `P1` as the highest-priority
relationship and provenance gaps.

Do not infer that the first item in an automatically generated queue is therefore
the next editorial priority. Human selection of a bounded cohort is required.

## Authoritative references

- Non-negotiable rules: `documentation/DESIGN_AND_CONTENT_RULES.md`
- Current authorised packet: `documentation/NEXT_WORK.md`
- Cost-conscious execution: `documentation/WORK_PROTOCOL.md`
- Recovered specification: `documentation/original-vision-audit.md`
- Measured gaps: `docs/spec-gap-register.md`
- Source boundary: `documentation/source-policy.md`
- Publication gate: `documentation/publication-standards.md`
- Visual audit: `documentation/experience-visual-audit.md`

## Build and verification

```bash
make validate
make serve
```

`make validate` is necessary but not sufficient for reader-facing work. Inspect
the affected path at desktop and mobile widths before requesting human review.
