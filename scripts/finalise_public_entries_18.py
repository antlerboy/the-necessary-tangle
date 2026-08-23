#!/usr/bin/env python3
"""Finish source-bounded public wording and observations for release 0.18."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from apply_iteration_09 import graph_metrics

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "public-data.json"
DOCS_JSON = ROOT / "docs" / "assets" / "public-data.json"
DOCS_JS = ROOT / "docs" / "assets" / "public-data.js"

DESCRIPTIONS = {
    "concept_unfix_system_archetypes": (
        "In Jurgen Appelo's unFIX synthesis, system archetypes are recurring structures of feedback and delay "
        "used to recognise familiar patterns of system behaviour. This entry records inclusion in that synthesis; "
        "its wider lineage and competing formulations remain to be researched."
    ),
    "concept_unfix_causal_loop_diagrams": (
        "In Jurgen Appelo's unFIX synthesis, causal loop diagrams are visual models of reinforcing and balancing "
        "feedback among variables. This entry records inclusion in that synthesis and does not claim an exhaustive "
        "account of the method or its history."
    ),
    "concept_unfix_mental_models": (
        "In Jurgen Appelo's unFIX synthesis, mental models are the assumptions and internal representations through "
        "which people interpret situations and choose actions. This entry records inclusion in that synthesis pending "
        "a fuller sourced treatment."
    ),
    "concept_unfix_hierarchy": (
        "In Jurgen Appelo's unFIX synthesis, hierarchy names nested levels of authority, responsibility or system "
        "organisation. This source-bounded entry records the concept's inclusion without treating hierarchy as either "
        "inherently good or inherently bad."
    ),
    "concept_unfix_dynamic_complexity": (
        "In Jurgen Appelo's unFIX synthesis, dynamic complexity arises when causes and effects are separated in time "
        "or space and feedback makes consequences difficult to infer. This entry records inclusion in that synthesis "
        "rather than a complete theoretical treatment."
    ),
    "concept_unfix_network_theory": (
        "In Jurgen Appelo's unFIX synthesis, network theory examines actors or elements through their patterns of "
        "connection, position and flow. This entry records inclusion in that synthesis; its detailed theoretical "
        "lineages and applications remain open work."
    ),
    "concept_unfix_scaling_laws": (
        "In Jurgen Appelo's unFIX synthesis, scaling laws describe how system properties change, often non-linearly, "
        "with size. This entry records inclusion in that synthesis and is not a complete account of biological, urban "
        "or organisational scaling."
    ),
}


def parse(value: Any, fallback: Any | None = None) -> Any:
    if fallback is None:
        fallback = []
    if isinstance(value, (list, dict)):
        return value
    if not value:
        return fallback
    try:
        return json.loads(value)
    except (TypeError, json.JSONDecodeError):
        return fallback


def encoded(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False)


def observations_for(data: dict[str, Any]) -> list[dict[str, str]]:
    metrics = graph_metrics(data)
    snapshot = data.get("graph_snapshot", {})
    entries = metrics.get("public_entries", data.get("meta", {}).get("public_entry_count", 0))
    profiles = metrics.get("developed_profiles", data.get("meta", {}).get("profile_count", 0))
    typed = metrics.get("typed_edges", len(data.get("edges", [])))
    substantive = metrics.get("substantive_edges", snapshot.get("substantive_edge_count", 0))
    isolated = snapshot.get("isolated_node_count", 0)
    largest = snapshot.get("largest_component_node_count", 0)
    return [
        {
            "id": "breadth_outpaces_depth",
            "title": "Breadth still outruns depth",
            "kind": "measurement plus interpretation",
            "measurement": f"The atlas has {entries} public entries and {profiles} developed profiles.",
            "interpretation": "A named entry and a developed critical account remain different editorial products.",
            "implication": "Depth work should follow contested bridges, practitioner use and consequential ambiguity rather than raw entry count.",
            "test": "Track the share of public entries with developed profiles and sourced relations across several relation families.",
        },
        {
            "id": "two_graph_regimes",
            "title": "The atlas contains two graph regimes",
            "kind": "semantic measurement",
            "measurement": f"The release contains {typed} typed records, of which the public graph snapshot counts {substantive} as substantive relations.",
            "interpretation": "Documentary and classificatory structure helps retrieval, while substantive relations carry most of the explanatory burden.",
            "implication": "Interface density must not make a catalogue edge look equivalent to a historical, conceptual or practice claim.",
            "test": "Inspect a sample of map edges and confirm that the visible wording exposes relation type and evidence role.",
        },
        {
            "id": "expertise_needs_relations",
            "title": "Expertise needs relations, not biography alone",
            "kind": "editorial observation",
            "measurement": "The named-coverage review separates developed, represented and research-queue states.",
            "interpretation": "A person's significance becomes useful in the atlas when their work, concepts, disagreements and practice consequences are connected explicitly.",
            "implication": "Do not promote requested names to developed profiles merely because they are canonical or famous.",
            "test": "Check that each developed person profile has sourced work-level and concept-level relations rather than only a short biography.",
        },
        {
            "id": "catalogue_is_not_critique",
            "title": "A catalogue is not a critique",
            "kind": "boundary observation",
            "measurement": "Release 0.18 records all 32 terms in one published unFIX synthesis but marks the shared source and bounded status.",
            "interpretation": "Enumerating a framework's vocabulary does not test its definitions, ancestry, omissions or internal tensions.",
            "implication": "Coverage pages should state whether a pass is inventory, interpretation, comparison or critique.",
            "test": "Confirm that the unFIX coverage page does not present the 32-item inventory as independent validation of the concepts.",
        },
        {
            "id": "practice_is_peripheral",
            "title": "Practice remains less connected than the canon",
            "kind": "graph interpretation",
            "measurement": f"The substantive graph leaves {isolated} public entries outside a substantive component.",
            "interpretation": "Bibliographic breadth grows more easily than warranted accounts of how ideas alter action in context.",
            "implication": "Future depth passes should connect methods to cases, conditions, consequences and failure modes.",
            "test": "Review isolated and one-family entries by entity type, then prioritise practice-facing gaps with usable sources.",
        },
        {
            "id": "source_monoculture",
            "title": "A single synthesis creates source monoculture",
            "kind": "source-quality observation",
            "measurement": "The 32 unFIX concept records initially share one declared synthesis source, which itself describes AI-assisted preparation and subsequent human editing.",
            "interpretation": "Shared provenance is honest and useful for discovery, but it cannot establish 32 independent bodies of evidence.",
            "implication": "Concepts should acquire primary or authoritative sources individually before their claims become stronger.",
            "test": "Count how many unFIX entries later gain distinct source records and whether their definitions change as a result.",
        },
        {
            "id": "identity_resolution",
            "title": "Identity resolution is substantive editorial work",
            "kind": "information-quality observation",
            "measurement": "Search aliases now include common short forms, surnames and known misspellings while canonical redirects preserve one public identity.",
            "interpretation": "Search failure can masquerade as conceptual absence; careless aliasing can instead merge genuinely different people or ideas.",
            "implication": "Aliases need explicit canonical targets and review, especially for surnames and near-homonyms.",
            "test": "Search for Donna and Donella Meadows, Russ and Russell Ackoff, surnames and common misspellings and verify the canonical result.",
        },
        {
            "id": "neighbourhoods_are_stale",
            "title": "A neighbourhood is a view, not a permanent fact",
            "kind": "map observation",
            "measurement": "The constellation view computes direct and two-step orbits from the currently visible substantive graph.",
            "interpretation": "As evidence and relation types change, a person's apparent intellectual neighbourhood should change too.",
            "implication": "Saved journeys may guide attention, but generated constellations should not be frozen into taxonomies.",
            "test": "Add or remove a warranted bridge and confirm that the two-step constellation changes without manual recategorisation.",
        },
        {
            "id": "bridge_concepts",
            "title": "Bridge concepts hold the central component together",
            "kind": "graph measurement plus interpretation",
            "measurement": f"The largest substantive component contains {largest} public entries.",
            "interpretation": "A small number of concepts and practices connect otherwise separate traditions, people and methods.",
            "implication": "Bridge entries deserve stronger definitions, competing interpretations and source diversity because errors there propagate widely.",
            "test": "Remove high-betweenness entries in a copy of the graph and inspect which traditions split apart.",
        },
        {
            "id": "map_of_attention",
            "title": "The map is also a map of editorial attention",
            "kind": "second-order observation",
            "measurement": f"Release 0.18 contains {isolated} substantively isolated public entries alongside a largest component of {largest}.",
            "interpretation": "Graph position reflects available sources, curation choices and past questions as well as the intellectual field itself.",
            "implication": "Centrality must never be presented as a neutral measure of importance.",
            "test": "Compare centrality with the release history and source programmes to identify where editorial effort created apparent prominence.",
        },
        {
            "id": "automated_overreading",
            "title": "Automation readily overreads weak evidence",
            "kind": "publication-safety observation",
            "measurement": "This release keeps source roles, claim status and open research programmes visible while using scripts to generate and validate the site.",
            "interpretation": "Automation is good at consistency and propagation; it is also good at propagating an unjustified inference everywhere at once.",
            "implication": "Generated breadth needs adversarial checks, source boundaries and explicit stop conditions.",
            "test": "Trace a sample of generated relations back to locators and verify that no discovery source has silently become evidence for a stronger claim.",
        },
        {
            "id": "presence_is_not_depth",
            "title": "Presence is not depth",
            "kind": "coverage-state observation",
            "measurement": "Requested names are published as developed, represented or research-queue entries rather than being forced into one apparent level of completeness.",
            "interpretation": "A searchable name is an index achievement, not evidence that the atlas explains the person's work, lineage or disputes.",
            "implication": "Prominence should follow sourced relational depth rather than the fact that a name was requested.",
            "test": "Confirm that research-queue entries do not appear as developed profiles or acquire unsupported influence claims.",
        },
        {
            "id": "source_duplication",
            "title": "Source duplication hides claim compression",
            "kind": "source-boundary observation",
            "measurement": "Linda Booth Sweeney's author profile, official site and award record are stored as distinct source roles rather than duplicate records for one URL.",
            "interpretation": "One page may support several claims, but cloning it as several sources overstates independence and obscures what each citation does.",
            "implication": "Source records should identify a distinct public route and a bounded evidential use.",
            "test": "Check for duplicate URLs and inspect whether each Sweeney relation cites the source that actually supports it.",
        },
        {
            "id": "open_corpus_programmes",
            "title": "Unfinished corpus work belongs in the public model",
            "kind": "programme-boundary observation",
            "measurement": "Monoskop, Foundational Papers in Complexity Science, SysCoI/model.report, the reading list and company-knowledge discovery remain separately named open programmes.",
            "interpretation": "A bounded pass can be complete while the wider field remains unfinished; conflating the scales turns project management into an epistemic claim.",
            "implication": "Each future pass needs a stated corpus, method, stop condition and visible residual queue.",
            "test": "Check that release notes state what was examined and leave the remainder visible rather than calling the whole programme complete.",
        },
    ]


def main() -> None:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    by_id = {node.get("id"): node for node in data.get("nodes", [])}

    missing = sorted(set(DESCRIPTIONS) - set(by_id))
    if missing:
        raise SystemExit("Missing expected 0.18 entries: " + ", ".join(missing))

    for node_id, description in DESCRIPTIONS.items():
        node = by_id[node_id]
        node["description"] = description
        node["canonical_definition"] = description
        node["public_stub_text"] = description

    system_entry = by_id.get("concept_unfix_system")
    if not system_entry:
        raise SystemExit("Missing expected 0.18 entry: concept_unfix_system")
    aliases = [alias for alias in parse(system_entry.get("aliases"), []) if str(alias).casefold() != "systems"]
    system_entry["aliases"] = encoded(aliases)

    source = next((item for item in data.get("sources", []) if item.get("id") == "src_linda_do_bees_pee_2026"), None)
    if not source:
        raise SystemExit("Missing expected source: src_linda_do_bees_pee_2026")
    source["url"] = "https://www.lindaboothsweeney.com/"
    source["notes"] = (
        "Author-maintained site presenting Do Bees Pee? as a new children's book and describing its treatment of "
        "closed-loop ecological processes and circular-economy thinking. The separate author-profile source records "
        "the HarperCollins and June 2026 listing."
    )

    report = data.setdefault("ai_observations", {})
    report["release"] = data.get("meta", {}).get("release")
    report["generated"] = data.get("meta", {}).get("generated")
    report["metrics"] = graph_metrics(data)
    report["observations"] = observations_for(data)

    rendered = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    DATA_PATH.write_text(rendered, encoding="utf-8")
    DOCS_JSON.write_text(rendered, encoding="utf-8")
    DOCS_JS.write_text("window.TANGLE_DATA = " + json.dumps(data, ensure_ascii=False) + ";\n", encoding="utf-8")
    print(
        f"Finalised {len(DESCRIPTIONS)} unFIX descriptions, source roles and "
        f"{len(report['observations'])} AI observations; removed the generic Systems alias."
    )


if __name__ == "__main__":
    main()
