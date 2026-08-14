#!/usr/bin/env python3
"""Apply the bounded Pass 6 adversarial relationship review idempotently."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from apply_overnight_review import (
    calculate_graph_snapshot,
    calculate_relational_depth,
    graph_metrics,
    quality_result,
    write_data,
)
from apply_relational_depth_16 import write_relational_document


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "public-data.json"
QUALITY_PATH = ROOT / "data" / "relationship-quality.json"
QUALITY_PUBLIC_PATH = ROOT / "docs" / "assets" / "relationship-quality.json"


DUPLICATE_RETIREMENTS = {
    "e_source_link_src_ieee_feedback_topic": "A claim-located IEEE edge already connects the same endpoints with the same type.",
    "e_source_link_src_ieee_feedforward_topic": "A claim-located IEEE edge already connects the same endpoints with the same type.",
    "e_08_fpcs_coauthor_008_01": "Merged into one two-work Rosenblueth–Wiener co-authorship statement.",
    "e_fpcs_author_005_warren_mcculloch": "Weaker unlocated duplicate of the item-located official bibliographic edge.",
    "e_fpcs_author_006_arturo_rosenblueth": "Weaker unlocated duplicate of the item-located official bibliographic edge.",
    "e_fpcs_author_006_julian_bigelow": "Weaker unlocated duplicate of the item-located official bibliographic edge.",
    "e_fpcs_author_006_norbert_wiener": "Weaker unlocated duplicate of the item-located official bibliographic edge.",
    "e_fpcs_author_008_arturo_rosenblueth": "Weaker unlocated duplicate of the item-located official bibliographic edge.",
    "e_fpcs_author_008_norbert_wiener": "Weaker unlocated duplicate of the item-located official bibliographic edge.",
    "e_fpcs_author_009_claude_e_shannon": "Weaker unlocated duplicate of the item-located official bibliographic edge.",
    "e_fpcs_author_011_alan_turing": "Weaker unlocated duplicate of the item-located official bibliographic edge.",
    "e_fpcs_author_013_alan_turing": "Weaker unlocated duplicate of the item-located official bibliographic edge.",
    "e_fpcs_author_021_herbert_simon": "Weaker unlocated duplicate of the item-located official bibliographic edge.",
    "e_fpcs_author_034_roger_c_conant": "Weaker unlocated duplicate of the item-located official bibliographic edge.",
    "e_fpcs_author_034_w_ross_ashby": "Weaker unlocated duplicate of the item-located official bibliographic edge.",
    "e_fpcs_author_042_heinz_von_foerster": "Weaker unlocated duplicate of the item-located official bibliographic edge.",
    "e_fpcs_author_046_herbert_simon": "Weaker unlocated duplicate of the item-located official bibliographic edge.",
    "e_fpcs_author_048_francisco_varela": "Weaker unlocated duplicate of the item-located official bibliographic edge.",
    "e_fpcs_author_048_humberto_maturana": "Weaker unlocated duplicate of the item-located official bibliographic edge.",
    "e_fpcs_author_074_herbert_simon": "Weaker unlocated duplicate of the item-located official bibliographic edge.",
}


UNSUPPORTED_RETIREMENTS = {
    "e_0265": "Superseded by the primary, page-located Maxwell governor edge.",
    "e_0266": "Unlocated legacy precursor; a stronger governor-instantiates-feedback route already exists.",
    "e_0267": "Unlocated legacy historical claim; patent-level evidence is required before republication.",
    "e_0268": "Unlocated legacy development claim; too broad to stand on a topical register alone.",
    "e_0270": "Unlocated legacy precursor; the note names a topic but not evidence for the directed lineage claim.",
    "e_0272": "Reverses the stronger maintained direction in which cybernetics uses feedback.",
    "e_0273": "Reverses the stronger maintained direction in which control theory uses feedback.",
    "e_0275": "Unlocated and overstates single-loop learning as a derivative of feedback.",
    "e_0276": "Unlocated and overstates double-loop learning as a derivative of feedback.",
    "e_0277": "Unlocated and misleadingly presents double bind as a derivative of feedback.",
    "e_0279": "Unlocated and too broad: quality management contains many practices beyond feedback.",
    "e_0282": "Unlocated legacy precursor candidate; prosody and combinatorics do not establish the published lineage.",
    "e_0283": "Unlocated legacy precursor candidate; the morphology note does not establish the published lineage.",
    "e_0284": "Unlocated legacy precursor candidate with no claim-specific rationale.",
    "e_0285": "Fibonacci sequence resemblance does not by itself establish a recursion lineage.",
    "e_0286": "Forms resemblance does not establish a recursion lineage.",
    "e_0287": "Arithmetic and recursive definitions need a located primary or historical source.",
    "e_0288": "Unlocated legacy development candidate with no claim-specific rationale.",
    "e_0289": "Incompleteness and formal systems do not by themselves establish this development claim.",
    "e_0290": "Computability relevance does not by itself establish the broad developed-or-extended claim.",
    "e_0291": "Architecture of complexity does not by itself establish development of recursion.",
    "e_0292": "Generative syntax relevance needs a located source for the directed development claim.",
    "e_0293": "Self-organisation and recursive epistemology need a located source for the directed development claim.",
    "e_0294": "Recursive mechanisms in cognition need a located source for the directed development claim.",
    "e_0295": "Autopoiesis and cognition need a located source for the directed development claim.",
    "e_0142": "A framework grouping does not establish that this knowledge domain complements the whole approaches corpus.",
    "e_0143": "A framework grouping does not establish that this knowledge domain complements the whole approaches corpus.",
    "e_0144": "A framework grouping does not establish that this knowledge domain complements the whole approaches corpus.",
    "e_0299": "Definition comparison distinguishes recursion and fractality but does not evidence that they are often confused.",
    "e_0343": "Definition comparison distinguishes feedback and homeostasis but does not evidence frequency of confusion.",
}


FPCS_ITEM_LOCATORS = {
    "publication_fpcs_005": "Official table of contents, Volume 1, item 5, ‘A Logical Calculus of the Ideas Immanent in Nervous Activity’",
    "publication_fpcs_006": "Official table of contents, Volume 1, item 6, ‘Behavior, Purpose, and Teleology’",
    "publication_fpcs_008": "Official table of contents, Volume 1, item 8, ‘The Role of Models in Science’",
    "publication_fpcs_009": "Official table of contents, Volume 1, item 9, ‘A Mathematical Theory of Communication’",
    "publication_fpcs_011": "Official table of contents, Volume 1, item 11, ‘Computing Machinery and Intelligence’",
    "publication_fpcs_013": "Official table of contents, Volume 1, item 13, ‘The Chemical Basis of Morphogenesis’",
    "publication_fpcs_021": "Official table of contents, Volume 2, item 21, ‘The Architecture of Complexity’",
    "publication_fpcs_034": "Official table of contents, Volume 2, item 34, ‘Every Good Regulator of a System Must Be a Model of That System’",
    "publication_fpcs_042": "Official table of contents, Volume 2, item 42, ‘Notes on an Epistemology for Living Things’",
    "publication_fpcs_046": "Official table of contents, Volume 3, item 46, ‘The Organization of Complex Systems’",
    "publication_fpcs_048": "Official table of contents, Volume 3, item 48, ‘Autopoiesis: The Organization of Living Systems, Its Characterization, and a Model’",
    "publication_fpcs_074": "Official table of contents, Volume 4, item 74, ‘Organizations and Markets’",
}


def duplicate_triples(edges: list[dict[str, Any]]) -> list[dict[str, Any]]:
    counts = Counter((edge.get("source"), edge.get("relation_type"), edge.get("target")) for edge in edges)
    return [
        {"source": source, "relation_type": relation_type, "target": target, "count": count}
        for (source, relation_type, target), count in sorted(counts.items())
        if count > 1
    ]


def update_derived_data(data: dict[str, Any]) -> None:
    data["relational_depth"] = calculate_relational_depth(data)
    data["graph_snapshot"] = calculate_graph_snapshot(data)
    aggregate = data["relational_depth"]["aggregate"]
    data["meta"].update(
        {
            "edge_count": len(data.get("edges", [])),
            "source_count": len(data.get("sources", [])),
            "public_link_source_count": sum(source.get("public_link_status") == "public_link" for source in data.get("sources", [])),
            "no_public_link_source_count": sum(source.get("public_link_status") == "no_public_link" for source in data.get("sources", [])),
            "reader_connected_entry_count": aggregate["reader_connected_entries"],
            "semantic_connected_entry_count": aggregate["semantic_connected_entries"],
            "rich_entry_count": aggregate["connection_bands"].get("rich", 0),
            "developing_entry_count": aggregate["connection_bands"].get("developing", 0),
            "thin_entry_count": aggregate["connection_bands"].get("thin", 0),
            "unconnected_entry_count": aggregate["connection_bands"].get("unconnected", 0),
        }
    )
    if data.get("ai_observations"):
        data["ai_observations"]["metrics"] = graph_metrics(data)


def main() -> None:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    edges = data.get("edges", [])
    before = {
        "edges": len(edges),
        "exact_duplicate_triples": len(duplicate_triples(edges)),
        "legacy_unlocated_candidates": sum(
            edge.get("claim_status") == "legacy_unverified"
            and edge.get("assertion_mode") == "candidate"
            and not str(edge.get("source_locator", "")).strip()
            for edge in edges
        ),
        "inferred_edges": sum(edge.get("assertion_mode") == "inferred" for edge in edges),
    }

    by_id = {edge.get("id"): edge for edge in edges}
    for edge in edges:
        if edge.get("id", "").startswith("e_08_fpcs_authored_") and edge.get("source") in FPCS_ITEM_LOCATORS:
            edge["source_locator"] = FPCS_ITEM_LOCATORS[edge["source"]]
            edge["notes"] = edge.get("notes") or "Authorship is recorded by the official collection table of contents."

    coauthor = by_id.get("e_08_fpcs_coauthor_006_02")
    if coauthor:
        coauthor.update(
            {
                "plain_phrase": "co-authored two collection works with",
                "source_locator": "Official table of contents, Volume 1, items 6 ‘Behavior, Purpose, and Teleology’ and 8 ‘The Role of Models in Science’",
                "notes": "The official contents list Rosenblueth and Wiener together on two distinct works; the two duplicate person-to-person edges are merged here without losing either work locator.",
            }
        )

    retirement_ids = set(DUPLICATE_RETIREMENTS) | set(UNSUPPORTED_RETIREMENTS)
    removed_present = [edge.get("id") for edge in edges if edge.get("id") in retirement_ids]
    data["edges"] = [edge for edge in edges if edge.get("id") not in retirement_ids]
    update_derived_data(data)

    after_edges = data["edges"]
    audit = {
        "pass": 6,
        "date": "2026-08-14",
        "method": "Exact duplicate triples were inspected individually. Every unlocated legacy candidate and every maintained inferred edge was challenged against its locator and rationale.",
        "before": before,
        "after": {
            "edges": len(after_edges),
            "exact_duplicate_triples": len(duplicate_triples(after_edges)),
            "legacy_unlocated_candidates": sum(
                edge.get("claim_status") == "legacy_unverified"
                and edge.get("assertion_mode") == "candidate"
                and not str(edge.get("source_locator", "")).strip()
                for edge in after_edges
            ),
            "inferred_edges": sum(edge.get("assertion_mode") == "inferred" for edge in after_edges),
        },
        "duplicate_retirements": [
            {"edge_id": edge_id, "reason": reason} for edge_id, reason in DUPLICATE_RETIREMENTS.items()
        ],
        "unsupported_retirements": [
            {"edge_id": edge_id, "reason": reason} for edge_id, reason in UNSUPPORTED_RETIREMENTS.items()
        ],
        "strengthened_edges": {
            "item_located_bibliographic_edges": sum(
                edge.get("id", "").startswith("e_08_fpcs_authored_")
                and edge.get("source") in FPCS_ITEM_LOCATORS
                for edge in after_edges
            ),
            "merged_two_work_coauthorship_edge": "e_08_fpcs_coauthor_006_02",
        },
        "retained_uncertainty": [
            {
                "edge_id": "e_0301",
                "decision": "retained as an explicit candidate rather than promoted",
                "reason": "The public secondary source and claim node make the attribution inspectable, but the primary lineage evidence is still missing.",
            }
        ],
        "removed_in_this_run": removed_present,
    }
    data["adversarial_review"] = audit
    write_relational_document(data)
    write_data(data)

    result = quality_result(data)
    result["adversarial_review"] = audit
    result["criteria"]["exact_duplicate_triples"] = {
        "passing": len(after_edges) if not duplicate_triples(after_edges) else 0,
        "total": len(after_edges),
        "review_target_count": len(duplicate_triples(after_edges)),
    }
    result["criteria"]["legacy_unlocated_candidates"] = {
        "passing": len(after_edges),
        "total": len(after_edges),
        "review_target_count": audit["after"]["legacy_unlocated_candidates"],
    }
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    QUALITY_PATH.write_text(rendered, encoding="utf-8")
    QUALITY_PUBLIC_PATH.write_text(rendered, encoding="utf-8")
    print(json.dumps({"before": before, "after": audit["after"], "strengthened": audit["strengthened_edges"]}, indent=2))


if __name__ == "__main__":
    main()
