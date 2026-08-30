#!/usr/bin/env python3
"""Apply release 0.20.5 after the maintained 0.20 prior-map build.

0.20.3 and 0.20.4 changed reader behaviour and public source surfaces without
advancing the canonical release metadata or regenerating the maintained AI
observations. This step reunifies those states and makes the current release
truthful again.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from apply_iteration_09 import graph_metrics, make_ai_observations

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "public-data.json"
DOCS_ASSETS = ROOT / "docs" / "assets"
AI_DOC = ROOT / "documentation" / "ai-observations.md"
CITATION = ROOT / "CITATION.cff"

RELEASE = "0.20.5"
GENERATED = "2026-08-30"

RELEASE_OBSERVATIONS = [
    {
        "id": "release_metadata_is_part_of_the_evidence",
        "title": "Release metadata is part of the evidence",
        "kind": "second-order publication observation",
        "measurement": (
            "Reader releases 0.20.3 and 0.20.4 changed public behaviour and source routes while the canonical "
            "release field and maintained AI report still said 0.20-prior-maps-alpha."
        ),
        "interpretation": (
            "A version label is not decoration. If the visible reader and the declared release describe different "
            "states, auditability has already broken before anyone inspects a source."
        ),
        "implication": (
            "Any public change which alters what a reader can see, follow or infer must advance one maintained "
            "release state and regenerate its observations."
        ),
        "test": (
            "The badge, canonical data, browser data, citation record and AI-observation report should all name "
            "the same release after deployment."
        ),
    },
    {
        "id": "interface_accumulation_is_a_system_effect",
        "title": "Interface clutter is an accumulation effect",
        "kind": "interface and systems observation",
        "measurement": (
            "Successive reader passes added a living mark, release status, curatorship, theme control and a random "
            "Little RedQuadrant rule to the same header without redesigning the composition as a whole."
        ),
        "interpretation": (
            "Each addition can be locally reasonable while their combination becomes globally noisy. The interface "
            "has exactly the same coordination problem as any other evolving system."
        ),
        "implication": (
            "Reader changes need composition-level review, not only feature-level acceptance. Controls should be "
            "given hierarchy, fixed spatial jobs and an explicit reason to remain above the fold."
        ),
        "test": (
            "A reader should be able to identify the project, its purpose and the main navigation before noticing "
            "release administration or display controls."
        ),
    },
    {
        "id": "display_layers_can_manufacture_isolation",
        "title": "A display layer can manufacture an isolate",
        "kind": "graph-interface observation",
        "measurement": (
            "Donella Meadows already had documentary authorship paths, but the default substantive map suppressed "
            "those paths and made her appear isolated until a narrow source-established Meadows-to-Leverage-Points "
            "relation was added."
        ),
        "interpretation": (
            "Visible isolation can be a property of the chosen layer and relation vocabulary rather than a property "
            "of the person or idea being shown."
        ),
        "implication": (
            "Isolation counts and visual gaps must always be read with the active layer stated; documentary absence "
            "and substantive disconnection are different claims."
        ),
        "test": (
            "For a sample of apparent isolates, compare the substantive, documentary and all-relations views before "
            "treating isolation as a research finding."
        ),
    },
    {
        "id": "a_live_corpus_is_not_ingested_coverage",
        "title": "A live corpus is not ingested coverage",
        "kind": "source-boundary observation",
        "measurement": (
            "The current SCiO resource catalogue and SysBoK/Kumu routes are now linked and registered, while the "
            "catalogue has not been normalised item by item and the live Kumu node-and-link graph has not been "
            "silently promoted into the canonical atlas."
        ),
        "interpretation": (
            "Knowing where the current corpus is and making it inspectable is useful work, but it is not the same "
            "achievement as reading, reconciling and evidencing every item in it."
        ),
        "implication": (
            "Corpus registration, item-level ingestion, reconciliation and canonical promotion should remain "
            "separate publication states."
        ),
        "test": (
            "A reader should be able to distinguish a live source route from an atlas statement independently "
            "supported by that source."
        ),
    },
    {
        "id": "linking_a_source_graph_is_not_canonising_it",
        "title": "Linking a source graph is not canonising it",
        "kind": "provenance observation",
        "measurement": (
            "SysBoK-derived material now carries routes to both SCiO's project page and the live Kumu model while "
            "retaining SCiO's own work-in-progress status and its Precedents and Dependent Derivatives semantics."
        ),
        "interpretation": (
            "Better provenance can increase access to another graph without pretending that its links have already "
            "passed the evidential tests of this one."
        ),
        "implication": (
            "Comparator and source graphs should travel with visible credit and original relation meanings until "
            "individual claims have been reconciled."
        ),
        "test": (
            "Inspect a SysBoK-backed item and confirm that its source graph is one click away while its relations are "
            "not automatically relabelled as canonical Tangle relations."
        ),
    },
]


def render_public_data(data: dict[str, Any]) -> None:
    rendered = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    DATA_PATH.write_text(rendered, encoding="utf-8")
    DOCS_ASSETS.mkdir(parents=True, exist_ok=True)
    (DOCS_ASSETS / "public-data.json").write_text(rendered, encoding="utf-8")
    (DOCS_ASSETS / "public-data.js").write_text(
        "window.TANGLE_DATA = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n",
        encoding="utf-8",
    )


def update_ai(data: dict[str, Any]) -> None:
    report = data.get("ai_observations")
    if not isinstance(report, dict):
        raise SystemExit("Maintained AI observations are missing")

    metrics = graph_metrics(data)
    fresh = make_ai_observations(metrics)
    fresh_by_id = {item.get("id"): item for item in fresh.get("observations", []) if item.get("id")}
    existing = report.get("observations", [])
    merged = [fresh_by_id.pop(item.get("id"), item) for item in existing]
    merged.extend(fresh_by_id.values())

    release_by_id = {item["id"]: item for item in RELEASE_OBSERVATIONS}
    merged = [release_by_id.pop(item.get("id"), item) for item in merged]
    merged.extend(release_by_id.values())

    report.update({"release": RELEASE, "generated": GENERATED, "metrics": metrics, "observations": merged})

    lines = [
        "# AI observations",
        "",
        f"Generated for release `{RELEASE}` on {GENERATED}.",
        "",
        "Release 0.20.5 reunifies the public reader, source surfaces, release metadata and maintained observations after the 0.20.3 and 0.20.4 reader/source passes.",
        "",
        "Measurements come from the generated public graph. Interpretations concern this atlas and its current source and interface choices; they are not measurements of the field itself.",
        "",
    ]
    for item in merged:
        lines.extend([
            f"## {item.get('title', item.get('id', 'Observation'))}",
            "",
            f"**Kind:** {item.get('kind', '')}",
            "",
            f"**Measurement:** {item.get('measurement', '')}",
            "",
            f"**Interpretation:** {item.get('interpretation', '')}",
            "",
            f"**Implication:** {item.get('implication', '')}",
            "",
            f"**Test:** {item.get('test', '')}",
            "",
        ])
    AI_DOC.write_text("\n".join(lines), encoding="utf-8")


def update_citation() -> None:
    text = CITATION.read_text(encoding="utf-8")
    text = re.sub(r"^version:\s*.*$", f"version: {RELEASE}", text, flags=re.MULTILINE)
    text = re.sub(r"^date-released:\s*.*$", f"date-released: {GENERATED}", text, flags=re.MULTILINE)
    CITATION.write_text(text, encoding="utf-8")


def main() -> None:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    meta = data.setdefault("meta", {})
    meta["release"] = RELEASE
    meta["generated"] = GENERATED
    meta["release_note"] = (
        "Release-state correction and reader composition pass: current AI observations, SCiO/SysBoK source routes, "
        "and a simplified header composition."
    )
    update_ai(data)
    render_public_data(data)
    update_citation()
    print(f"Applied release {RELEASE}: metadata, browser data, citation and AI observations aligned")


if __name__ == "__main__":
    main()
