#!/usr/bin/env python3
"""Incorporate the Map of the Complexity Sciences where it fills atlas gaps.

Second comparator under corpus_comparator_maps (issue 6). Brian Castellani's
map is read against both the atlas and the Map of Systemic Evolution, and the
applied-complexity domains that neither holds are registered here.

What this adds, and what it deliberately does not:

- It adds knowledge-domain entries for fields the atlas lacks, each sourced to
  the map and each carrying exactly one evidenced relationship: that it appears
  in the map. Appearing in a map is a documentary fact. It is not influence,
  endorsement, teaching or conceptual dependence, and the scope condition on
  every edge says so.
- It does not add the 116 individually named contemporary researchers the map
  also carries. Registering that many unconnected people would raise entry
  counts without adding a single evidenced relationship, which is the coverage
  inflation the relational-depth programme exists to prevent. They are recorded
  as a research queue instead.
- Entries enter at publication_level research_stub and public_visibility
  metadata, the repository's existing pattern for sourced-but-undeveloped
  material, so they are registered without being presented as developed public
  entries.

Idempotent.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "public-data.json"
DOCS_ASSETS = ROOT / "docs" / "assets"

SOURCE_ID = "src_castellani_map_complexity_sciences"
CORPUS_ID = "comparator_corpus_castellani_complexity_map_and_atlas"
LIVE_URL = "https://www.art-sciencefactory.com/complexity-map_feb09.html"

# Fields carried by the Map of the Complexity Sciences which neither the atlas
# nor the Map of Systemic Evolution holds. Labels follow the map; the gloss is
# this project's, written to say what the field is rather than to assert a
# relationship.
GAP_DOMAINS: list[tuple[str, str, str]] = [
    ("complexity_and_public_health", "Complexity and public health",
     "Applies complex-systems reasoning to population health: feedback between exposure, behaviour and institutions, and why single-cause models mislead in policy."),
    ("complexity_and_healthcare", "Complexity and healthcare",
     "Treats care delivery as an adaptive system of clinicians, patients, pathways and incentives, rather than a process to be optimised in isolation."),
    ("computational_social_science", "Computational social science",
     "Studies social processes through large-scale data, simulation and formal models, spanning agent-based modelling, network analysis and digital trace data."),
    ("digital_social_science", "Digital social science",
     "Investigates social life as it is conducted through and shaped by digital platforms, including the methods that read platform data as evidence."),
    ("qualitative_complexity", "Qualitative complexity",
     "Applies complexity ideas through interpretive and case-based inquiry rather than formal modelling, and argues that some system behaviour is only reachable that way."),
    ("applied_complexity", "Applied complexity",
     "The practitioner-facing use of complexity ideas in organisations, policy and intervention design, distinct from complexity as a research programme."),
    ("complexity_and_geography", "Complexity and geography",
     "Studies spatial systems - cities, regions, migration, land use - as emergent and path-dependent rather than as equilibrium distributions."),
    ("complexity_management_and_planning", "Complexity, management and planning",
     "Addresses planning and management under conditions where outcomes are emergent, so that plans function as interventions in a system rather than as predictions."),
    ("psychology_and_systems_theory", "Psychology and systems theory",
     "Reads psychological processes as embedded in systems of relationship, environment and feedback rather than as properties of an isolated individual."),
    ("social_systems_theory", "Social systems theory",
     "Treats society as composed of self-referential communicating systems; associated above all with Niklas Luhmann's account of social autopoiesis."),
    ("evolutionary_game_theory", "Evolutionary game theory",
     "Studies strategy as it spreads through a population by replication and selection rather than by individual rational choice."),
    ("graph_theory", "Graph theory",
     "The mathematics of vertices and edges underlying network science, from connectivity and paths to spectral and random-graph results."),
    ("scaling_in_complex_systems", "Scaling in complex systems",
     "Investigates how measurable properties change with system size, including allometric and power-law relationships across organisms, cities and firms."),
    ("computational_science", "Computational science",
     "Uses simulation and numerical method as a mode of scientific inquiry in its own right, alongside theory and experiment."),
    ("computational_biology", "Computational biology",
     "Models biological organisation computationally, from molecular networks to development and ecology."),
    ("computational_complexity_theory", "Computational complexity theory",
     "Classifies problems by the resources their solution requires. Distinct from complexity science, and often confused with it."),
    ("big_data", "Big data",
     "The methods and infrastructure for analysing datasets whose scale changes what questions can be asked, and the epistemic claims made for them."),
]

STUB = ("Research stub. {label} is registered because the Map of the Complexity Sciences "
        "carries it and neither this atlas nor the Map of Systemic Evolution did. A "
        "sourced public account has not yet been written.")

SCOPE = ("Appearing in a comparator map is a documentary fact about that map. It is not "
         "evidence of influence, endorsement, teaching, priority or conceptual dependence, "
         "each of which needs its own source.")


def node_record(slug: str, label: str, gloss: str) -> dict[str, Any]:
    node_id = f"knowledge_domain_{slug}"
    return {
        "id": node_id,
        "label": label,
        "entity_type": "knowledge_domain",
        "description": gloss,
        "aliases": "[]",
        "boundary_ring": "1",
        "inclusion_reason": "comparator_castellani_map",
        "status": "accepted",
        "source_ids": json.dumps([SOURCE_ID]),
        "set_tags": json.dumps(["complexity", "comparator"]),
        "espoused_labels": "[]",
        "observed_clusters": "[]",
        "canonical_definition": "",
        "valid_from": "",
        "valid_to": "",
        "external_ids": "{}",
        "geographies": "[]",
        "licence": "",
        "review_status": "research_pass_needs_editor",
        "reviewed_by": "",
        "reviewed_at": "",
        "x": 0.0,
        "y": 0.0,
        "canonical_id": node_id,
        "public_visibility": "metadata",
        "publication_level": "research_stub",
        "public_stub_text": STUB.format(label=label),
        "public_source_count": 1,
        "no_public_link_count": 0,
    }


def edge_record(slug: str, label: str) -> dict[str, Any]:
    return {
        "id": f"e_castellani_{slug}_member",
        "source": f"knowledge_domain_{slug}",
        "target": CORPUS_ID,
        "relation_type": "member_of",
        "relation_family": "classification",
        "directed": "true",
        "dependency_kind": "",
        "confidence": "0.95",
        "claim_status": "accepted",
        "source_ids": json.dumps([SOURCE_ID]),
        "evidence_ids": "[]",
        "source_locator": "Map of the Complexity Sciences, current web edition, node label",
        "valid_from": "",
        "valid_to": "",
        "scope_conditions": SCOPE,
        "assertion_mode": "asserted",
        "inference_method": "direct reading of the comparator map",
        "claim_id": "",
        "reviewed_by": "",
        "reviewed_at": "",
        "notes": "",
        "plain_phrase": "appears in",
        "public_review_label": "documented comparator appearance",
    }


def main() -> int:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    nodes = data["nodes"]
    edges = data["edges"]
    by_id = {n["id"]: i for i, n in enumerate(nodes)}
    edge_ids = {e["id"] for e in edges}

    added_nodes = added_edges = 0
    for slug, label, gloss in GAP_DOMAINS:
        record = node_record(slug, label, gloss)
        if record["id"] in by_id:
            nodes[by_id[record["id"]]] = record
        else:
            nodes.append(record)
            added_nodes += 1
        edge = edge_record(slug, label)
        if edge["id"] in edge_ids:
            for index, existing in enumerate(edges):
                if existing["id"] == edge["id"]:
                    edges[index] = edge
                    break
        else:
            edges.append(edge)
            added_edges += 1

    # The registered source pointed only at a 2012 static export; record the
    # live edition actually read.
    for source in data.get("sources", []):
        if source.get("id") == SOURCE_ID:
            source["url"] = LIVE_URL
            source["archived_url"] = (
                "https://commons.wikimedia.org/wiki/File:Map_of_the_Complexity_Sciences.svg"
            )
            source["notes"] = (
                "Brian Castellani's conceptual and historical map of the complexity "
                "sciences. The May 2026 web edition exposes 307 clickable areas; the "
                "Wikimedia file recorded as archived_url is an earlier "
                "static export. Used as a comparator for coverage. Its lines carry no "
                "stated relation type. Every current outward link is retained separately "
                "as source-published and not independently checked."
            )
            source["last_checked"] = "2026-08-20"

    for entry in data.get("corpus_register", []):
        if entry.get("id") == "corpus_comparator_maps":
            entry["status"] = "two_comparators_reviewed_programme_continuing"

    meta = data["meta"]
    meta["castellani_map_url"] = LIVE_URL
    meta["castellani_map_current_source_link_count"] = 307
    meta["castellani_map_prior_gap_analysis_basis_count"] = 300
    meta["castellani_map_prior_gap_analysis_note"] = (
        "The 17-domain gap pass used the earlier 300-entry edition. Its old overlap "
        "counts are not presented as current May 2026 figures."
    )
    meta["castellani_map_domains_incorporated"] = len(GAP_DOMAINS)
    meta["castellani_map_people_queued"] = 116
    meta["comparator_count"] = 2
    meta["node_count"] = len(nodes)
    meta["edge_count"] = len(edges)

    rendered = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    DATA_PATH.write_text(rendered, encoding="utf-8")
    DOCS_ASSETS.mkdir(parents=True, exist_ok=True)
    (DOCS_ASSETS / "public-data.json").write_text(rendered, encoding="utf-8")
    (DOCS_ASSETS / "public-data.js").write_text(
        "window.TANGLE_DATA = "
        + json.dumps(data, ensure_ascii=False, separators=(",", ":"))
        + ";\n",
        encoding="utf-8",
    )
    print(
        f"Incorporated the Map of the Complexity Sciences: {len(GAP_DOMAINS)} gap domains "
        f"registered ({added_nodes} new nodes, {added_edges} new edges), "
        "116 named researchers queued rather than added."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
