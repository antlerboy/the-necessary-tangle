#!/usr/bin/env python3
"""Write the concise, validator-compatible operating spine for release 0.18."""
import json
from pathlib import Path

from apply_relational_depth_16 import write_relational_document

ROOT = Path(__file__).resolve().parents[1]

STATE = """# Tangle state

Last verified: 23 August 2026

## Public release

- Release: `0.18-navigable-tangle-alpha`
- Public site: https://transduction.systems/
- Canonical dataset: `data/public-data.json`
- Machine relationship snapshot: `data/relationship-quality.json`
- Public reader dataset: `docs/assets/public-data.json`
- Public knowledge index: `documentation/public-knowledge.md`
- unFIX comparator concepts resolved: 32

## Current shape

Release 0.18 makes the public atlas easier to read and traverse. Entries now use a full reading surface, their typed connections appear near the definition, the map is larger and pannable from the whole canvas, and a two-step constellation view distinguishes the selected entry, direct relations and two-step context.

The release also records the source-backed Linda Booth Sweeney updates, maps the 32 concepts in Jurgen Appelo's published unFIX synthesis, and publishes honest coverage states for the figures and institutions requested after 0.17. A named item may be developed, represented, or held in a research queue; presence is not presented as depth.

## Current limits

The atlas remains a bounded public evidence graph, not an exhaustive map of systems, cybernetics and complexity. The Monoskop archive, Foundational Papers in Complexity Science, SysCoI/model.report, the RedQuadrant reading list and company-knowledge discovery remain continuing programmes. Their boundaries and unfinished work stay visible.

## Release controls

Run `make validate` before publication. It rebuilds the full historical release chain, validates the operating spine, graph, evidence, reader assets and JavaScript, then applies the 0.18-specific checks.
"""

NEXT = """# Next work

Status: release 0.18 is complete. No production change is authorised without a new ticket.

## Outcome

Keep the atlas useful as a tangle of warranted connections rather than letting breadth, novelty or interface work outrun source quality and reader comprehension.

## In scope

- review live feedback and submitted tickets after 0.18;
- deepen entries currently marked `research_queue` or `represented` when public sources justify it;
- continue the named long-running corpus programmes as separately bounded passes;
- test the full-page reader, map panning, constellation scale, real-link behaviour and mobile layout with actual readers;
- correct broken or misleading source routes as they are found.

## Out of scope

- claiming exhaustive coverage of systems, cybernetics or complexity;
- bulk-generating biographies or relationships from names alone;
- merging inferred similarity with source-backed influence or lineage;
- hiding thin coverage behind visual density;
- redesigning away the cream, red, black and magic-dot identity without an explicit ticket.

## Acceptance checks

- one primary reader outcome per ticket;
- source-backed claims retain source identifiers and meaningful locators;
- new public entries expose typed connections or an honest thin/research state;
- ordinary navigational controls are genuine links where the destination can be represented by a URL;
- `make validate` passes on the complete generated release;
- the public deployment is checked at https://transduction.systems/ after merge.

## Stop conditions

Stop a pass when its stated corpus, names or interaction path has been checked, the acceptance tests pass and the remaining work would require a new evidence search or a different reader outcome. Do not turn a bounded pass into an unreviewed overnight expansion.

## Model route

Use Luna for lightweight extraction and routine checks, Terra for bounded research and implementation, and Sol for architecture, adversarial review or disputed synthesis. Keep research and build work in separate contexts when the source set or claim boundary is material.
"""

(ROOT / "documentation" / "TANGLE_STATE.md").write_text(STATE, encoding="utf-8")
(ROOT / "documentation" / "NEXT_WORK.md").write_text(NEXT, encoding="utf-8")
data = json.loads((ROOT / "data" / "public-data.json").read_text(encoding="utf-8"))
write_relational_document(data)

index_path = ROOT / "docs" / "index.html"
index = index_path.read_text(encoding="utf-8")
index = index.replace(
    '<button type="button" class="text-button surprise-me footer-surprise">Surprise me</button>',
    '<a href="#view=item&id=concept_viability&from=surprise" class="text-button surprise-me footer-surprise">Surprise me</a>',
)
index_path.write_text(index, encoding="utf-8")

release_js_path = ROOT / "docs" / "assets" / "iteration-18.js"
release_js = release_js_path.read_text(encoding="utf-8")
release_js = release_js.replace(
    "group.dataset.orbit = distance === 0 ? 'core' : distance === 1 ? 'inner' : 'outer';",
    "group.setAttribute('data-orbit', distance === 0 ? 'core' : distance === 1 ? 'inner' : 'outer');",
)
release_js_path.write_text(release_js, encoding="utf-8")

unfix_path = ROOT / "documentation" / "unfix-32-coverage.md"
unfix = unfix_path.read_text(encoding="utf-8")
if "## Comparator status" not in unfix:
    unfix = unfix.replace(
        "Generated for release `0.18-navigable-tangle-alpha` on 2026-08-23.\n",
        "Generated for release `0.18-navigable-tangle-alpha` on 2026-08-23.\n\n## Comparator status\n",
        1,
    )
unfix_path.write_text(unfix, encoding="utf-8")
print("Finalised the 0.18 operating spine.")
