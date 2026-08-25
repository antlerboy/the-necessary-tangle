#!/usr/bin/env python3
"""Normalise and reconcile the Map of Systemic Evolution comparator.

The mapping below is deliberately small and human-reviewed.  A mapped source
node may be a compound label, so a confirmed target means that named component
has been reconciled; it does not mean the whole source label is identical to a
single atlas entry.  Unlisted nodes remain visibly unresolved.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
COMPARATOR = ROOT / "data" / "comparator-systemic-evolution.json"
ATLAS = ROOT / "data" / "public-data.json"
OUT = ROOT / "data" / "systemic-evolution-reconciliation.json"

REALMS = {
    "#999999": "philosophy",
    "#FFCC00": "social systems",
    "#008000": "biology and medicine",
    "#0000FF": "mathematics",
    "#000000": "physical sciences",
    "#FFFF00": "symbolic systems",
    "#800000": "computers and informatics",
    "#FF0000": "cybernetics",
    "#00CCFF": "systems analysis",
    "#00FF00": "ecology",
    "#FF00FF": "engineering",
    "#666699": "not identified in the published legend",
}


def targets(*items: tuple[str, str]) -> list[dict[str, str]]:
    return [{"atlas_id": atlas_id, "match_kind": match_kind} for atlas_id, match_kind in items]


# source id: (coverage status, targets, reviewer note)
MAPPINGS: dict[str, tuple[str, list[dict[str, str]], str]] = {
    "n0": ("partial", targets(("person_ludwig_von_bertalanffy", "same_person")), "The person is reconciled; the compound theory label remains broader."),
    "n3": ("partial", targets(("person_heinz_von_foerster", "same_person")), "The person is reconciled; the dated compound topic is not collapsed into him."),
    "n4": ("confirmed", targets(("tradition_control_theory", "same_named_tradition")), "Same named tradition."),
    "n5": ("partial", targets(("person_norbert_wiener", "same_person")), "The person is reconciled; Cybernetics remains a separate atlas tradition."),
    "n6": ("partial", targets(("person_w_ross_ashby", "same_person")), "The person is reconciled; the source's compound topic is retained."),
    "n7": ("partial", targets(("person_stafford_beer", "same_person"), ("method_or_methodology_viable_system_model_vsm", "same_named_method")), "Two components of the compound source node are reconciled."),
    "n8": ("partial", targets(("person_jay_w_forrester", "same_person"), ("person_donella_meadows", "same_person"), ("method_or_methodology_system_dynamics", "same_named_method")), "Three components of the compound source node are reconciled."),
    "n13": ("partial", targets(("person_warren_mcculloch", "same_person")), "The named person is reconciled."),
    "n16": ("partial", targets(("tradition_control_theory", "broader_atlas_tradition")), "Perceptual Control Theory is narrower than the atlas entry."),
    "n22": ("confirmed", targets(("tradition_game_theory", "same_named_tradition")), "Same named tradition."),
    "n29": ("partial", targets(("person_russell_l_ackoff", "same_person"), ("person_stafford_beer", "same_person")), "The two named people are reconciled; Operational Research is not yet a canonical atlas entry."),
    "n36": ("partial", targets(("tradition_systems_theory", "broader_atlas_tradition")), "General Systems Theory is mapped to a broader atlas tradition."),
    "n38": ("partial", targets(("person_anatol_rapoport", "same_person")), "The named person is reconciled."),
    "n49": ("confirmed", targets(("concept_self_organisation", "same_named_concept")), "Same named concept, allowing spelling variation."),
    "n50": ("partial", targets(("publication_fpcs_050", "same_named_work"), ("person_fpcs_h_haken", "same_person")), "The Haken work and its author are represented as bibliographic first-pass entries."),
    "n65": ("partial", targets(("person_niklas_luhmann", "same_person")), "The person is reconciled; the compound theory remains distinct."),
    "n78": ("partial", targets(("concept_autonomy", "component_concept")), "Autonomy is one component of the source label."),
    "n83": ("partial", targets(("person_fpcs_c_s_holling", "same_person")), "The named person is reconciled."),
    "n92": ("partial", targets(("person_peter_checkland", "same_person"), ("method_or_methodology_soft_systems_methodology_ssm", "same_named_method")), "The method and named person are reconciled."),
    "n93": ("partial", targets(("person_michael_c_jackson", "same_person"), ("person_werner_ulrich", "same_person"), ("tradition_critical_systems_thinking", "same_named_tradition")), "Three components are reconciled; Robert Flood remains unresolved."),
    "n95": ("partial", targets(("method_or_methodology_systemic_intervention", "adjacent_not_identical_method")), "Systemic Intervention is adjacent to, but not identical with, Total Systems Intervention."),
    "n103": ("partial", targets(("person_lynn_margulis", "same_person")), "The named person is reconciled."),
    "n104": ("partial", targets(("person_james_lovelock", "same_person")), "The named person is reconciled."),
    "n111": ("partial", targets(("person_humberto_maturana", "same_person"), ("person_francisco_varela", "same_person")), "Both named people are reconciled; the compound systems label remains distinct."),
    "n119": ("partial", targets(("person_ludwig_wittgenstein", "same_person")), "The named person is reconciled."),
    "n143": ("partial", targets(("person_gregory_bateson", "same_person")), "The named person is reconciled."),
    "n159": ("partial", targets(("person_margaret_mead", "same_person")), "The named person is reconciled."),
    "n160": ("partial", targets(("person_kenneth_e_boulding", "same_person")), "The named person is reconciled."),
    "n245": ("partial", targets(("person_claude_bernard", "same_person")), "The named person is reconciled."),
    "n249": ("partial", targets(("person_stuart_kauffman", "same_person")), "The named person is reconciled."),
    "n257": ("partial", targets(("tradition_systems_theory", "broader_atlas_tradition")), "The theory is represented broadly; Yi Lin is unresolved."),
    "n270": ("confirmed", targets(("concept_metasystem_transition", "same_named_concept")), "Same named concept."),
    "n273": ("partial", targets(("concept_unfix_hierarchy", "broader_atlas_concept")), "Hierarchy Theory is narrower than the atlas's current hierarchy concept."),
    "n274": ("partial", targets(("method_or_methodology_socio_technical_systems", "same_named_method")), "The method is reconciled; Harold Linstone remains unresolved."),
    "n290": ("partial", targets(("person_russell_l_ackoff", "same_person")), "The named person is reconciled."),
    "n291": ("partial", targets(("person_c_west_churchman", "same_person")), "The named person is reconciled."),
    "n320": ("partial", targets(("person_william_james", "same_person")), "The named person is reconciled."),
    "n346": ("partial", targets(("person_fpcs_a_j_lotka", "same_person")), "The named person is reconciled."),
    "n370": ("partial", targets(("person_giuseppe_peano", "same_person")), "The named person is reconciled."),
    "n407": ("partial", targets(("person_archimedes", "same_person")), "The named person is reconciled."),
    "n490": ("partial", targets(("person_john_von_neumann", "same_person")), "The named person is reconciled."),
    "n491": ("partial", targets(("person_david_hilbert", "same_person")), "The named person is reconciled."),
    "n502": ("partial", targets(("person_kurt_gödel", "same_person")), "The named person is reconciled."),
    "n511": ("partial", targets(("person_herbert_simon", "same_person")), "The named person is reconciled."),
    "n512": ("confirmed", targets(("concept_information_theory", "same_named_concept")), "Same named concept."),
    "n515": ("partial", targets(("person_bertrand_russell", "same_person")), "The named person is reconciled."),
    "n516": ("partial", targets(("person_james_clerk_maxwell", "same_person")), "The named person is reconciled."),
    "n532": ("partial", targets(("concept_uncertainty", "broader_atlas_concept")), "Intrinsic uncertainty is narrower than the atlas's general uncertainty entry."),
    "n539": ("partial", targets(("concept_non_linearity", "same_core_concept")), "The source labels systems; the atlas labels the property."),
    "n540": ("partial", targets(("concept_non_linearity", "component_concept")), "Non-linearity is one component of the source label."),
    "n545": ("partial", targets(("concept_information_theory", "same_named_concept")), "The concept is reconciled; Léon Brillouin is unresolved."),
    "n564": ("partial", targets(("organisation_santa_fe_institute", "same_organisation")), "The named organisation is reconciled."),
    "n568": ("partial", targets(("tradition_complexity_theory", "broader_atlas_tradition")), "Algorithmic complexity is narrower than the atlas's current complexity-theory entry."),
    "n579": ("partial", targets(("tradition_chaos_theory", "same_named_tradition"), ("person_fpcs_m_j_feigenbaum", "same_person")), "The theory and named person are represented."),
    "n582": ("partial", targets(("person_ilya_prigogine", "same_person")), "The named person is reconciled."),
    "n587": ("partial", targets(("concept_uncertainty", "broader_atlas_concept")), "Generalised uncertainty is narrower than the atlas's current concept."),
    "n599": ("partial", targets(("person_fritjof_capra", "same_person")), "The named person is reconciled."),
    "n612": ("partial", targets(("person_george_spencer_brown", "same_person")), "The named person is reconciled."),
    "n619": ("partial", targets(("person_louis_h_kauffman", "same_person")), "The named person is reconciled."),
    "n625": ("partial", targets(("practice_design_thinking", "adjacent_atlas_practice")), "Human-centred design is adjacent to, not identical with, Design thinking."),
    "n648": ("partial", targets(("method_or_methodology_agent_based_modelling", "same_named_method"), ("person_robert_axelrod", "same_person")), "The method and one named person are reconciled; Thomas Schelling remains unresolved."),
    "n649": ("partial", targets(("person_edgar_morin", "same_person")), "The named person is reconciled."),
}


def main() -> int:
    comparator = json.loads(COMPARATOR.read_text(encoding="utf-8"))
    atlas = json.loads(ATLAS.read_text(encoding="utf-8"))
    atlas_nodes = {node["id"]: node for node in atlas["nodes"]}
    source_nodes = {node["source_node_id"]: node for node in comparator["nodes"]}

    missing_source = sorted(set(MAPPINGS) - set(source_nodes))
    missing_atlas = sorted(
        target["atlas_id"]
        for _, mapping_targets, _ in MAPPINGS.values()
        for target in mapping_targets
        if target["atlas_id"] not in atlas_nodes
    )
    if missing_source or missing_atlas:
        raise SystemExit(f"Mapping drift: source={missing_source}, atlas={missing_atlas}")

    meta = comparator["meta"]
    meta.update(
        {
            "role": "permissioned source-attributed comparator layer",
            "permission": "Benjamin Hadorn confirmed appropriate use on 2026-08-25.",
            "rights": (
                "Used with Benjamin Hadorn's permission, with the full "
                "Schwarz-Durant-IIGSS-Hadorn provenance retained. Source copyright "
                "and terms continue to apply."
            ),
            "semantics": (
                "The URANOS page says directed edges illustrate major influences "
                "between topics. Every edge preserves that generic source claim and "
                "is marked not independently verified; no more specific edge meaning "
                "or edge-level evidence is supplied."
            ),
            "colour_legend": (
                "Realm names follow the source page. Colour is a realm classification, "
                "not a substitute for edge-specific evidence."
            ),
            "contribution_credit": (
                "Nigel Williams extracted and analysed the GraphML and built the first "
                "comparator implementation; Benjamin P Taylor supplied the earlier "
                "SysCoI registration, permissions and editorial reconciliation."
            ),
        }
    )
    meta.pop("colour_stream_caveat", None)

    mapping_rows = []
    for node in comparator["nodes"]:
        source_id = node["source_node_id"]
        status, mapped_targets, note = MAPPINGS.get(
            source_id, ("unresolved", [], "No human-reviewed atlas mapping recorded yet.")
        )
        node["official_realm"] = REALMS.get(node.get("border_colour"), "unclassified")
        node.pop("colour_stream_label", None)
        enriched_targets = [
            {
                **target,
                "atlas_label": atlas_nodes[target["atlas_id"]]["label"],
                "atlas_entity_type": atlas_nodes[target["atlas_id"]].get("entity_type", ""),
            }
            for target in mapped_targets
        ]
        node["reconciliation_status"] = status
        node["atlas_targets"] = enriched_targets
        mapping_rows.append(
            {
                "source_node_id": source_id,
                "source_label": node["label"],
                "status": status,
                "atlas_targets": enriched_targets,
                "review_note": note,
                "reviewed_by": "Benjamin P Taylor",
                "reviewed_at": "2026-08-25" if mapped_targets else "",
            }
        )

    atlas_pairs: dict[frozenset[str], list[str]] = {}
    for edge in atlas["edges"]:
        key = frozenset((edge["source"], edge["target"]))
        atlas_pairs.setdefault(key, []).append(edge["id"])

    mapped = {row["source_node_id"]: row for row in mapping_rows}
    edge_rows = []
    for edge in comparator["edges"]:
        edge["official_realm"] = REALMS.get(edge.get("line_colour"), "unclassified")
        edge["relation_type"] = "reported_major_influence"
        if edge.get("source_arrow") == "standard" and edge.get("target_arrow") == "standard":
            edge["direction_status"] = "bidirectional"
            edge["plain_phrase"] = "the source map depicts major influence in both directions"
        elif edge.get("source_arrow") == "standard":
            edge["direction_status"] = "target_to_source"
            edge["plain_phrase"] = (
                "the source map depicts a major influence from the target topic to the source topic"
            )
        else:
            edge["direction_status"] = "source_to_target"
            edge["plain_phrase"] = (
                "the source map depicts a major influence from the source topic to the target topic"
            )
        edge["meaning"] = "major_influence_between_topics"
        edge["accuracy_status"] = "source_reported_not_independently_verified"
        edge["specific_relation_status"] = "not_stated_by_source"
        source_targets = [t["atlas_id"] for t in mapped[edge["source_node_id"]]["atlas_targets"]]
        target_targets = [t["atlas_id"] for t in mapped[edge["target_node_id"]]["atlas_targets"]]
        canonical = sorted(
            {
                edge_id
                for source_id in source_targets
                for target_id in target_targets
                for edge_id in atlas_pairs.get(frozenset((source_id, target_id)), [])
            }
        )
        endpoint_status = (
            "both" if source_targets and target_targets else "one" if source_targets or target_targets else "none"
        )
        edge["reconciliation_status"] = endpoint_status
        edge["canonical_atlas_edge_ids"] = canonical
        edge_rows.append(
            {
                "source_edge_id": edge["comparator_edge_id"],
                "source_node_id": edge["source_node_id"],
                "target_node_id": edge["target_node_id"],
                "endpoint_mapping": endpoint_status,
                "source_atlas_ids": source_targets,
                "target_atlas_ids": target_targets,
                "canonical_atlas_edge_ids": canonical,
                "source_claim": "reported major influence",
                "direction_status": edge["direction_status"],
                "accuracy_status": "source_reported_not_independently_verified",
                "promotion_status": (
                    "independent_atlas_relation_exists" if canonical else "not_promoted_as_atlas_relation"
                ),
            }
        )

    distinct_atlas_ids = sorted(
        {target["atlas_id"] for row in mapping_rows for target in row["atlas_targets"]}
    )
    summary = {
        "source_nodes_retained": len(mapping_rows),
        "source_links_retained": len(edge_rows),
        "source_nodes_confirmed": sum(row["status"] == "confirmed" for row in mapping_rows),
        "source_nodes_partially_reconciled": sum(row["status"] == "partial" for row in mapping_rows),
        "source_nodes_unresolved": sum(row["status"] == "unresolved" for row in mapping_rows),
        "distinct_atlas_entries_linked": len(distinct_atlas_ids),
        "source_links_both_endpoints_mapped": sum(row["endpoint_mapping"] == "both" for row in edge_rows),
        "source_links_one_endpoint_mapped": sum(row["endpoint_mapping"] == "one" for row in edge_rows),
        "source_links_no_endpoints_mapped": sum(row["endpoint_mapping"] == "none" for row in edge_rows),
        "source_links_with_independent_atlas_relation": sum(bool(row["canonical_atlas_edge_ids"]) for row in edge_rows),
        "canonical_atlas_relations_created_from_source_links": 0,
    }
    if summary["source_nodes_retained"] != 650 or summary["source_links_retained"] != 1320:
        raise SystemExit(f"Comparator shape changed: {summary}")

    meta["reconciliation_summary"] = summary
    COMPARATOR.write_text(json.dumps(comparator, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    output: dict[str, Any] = {
        "meta": {
            "dataset": "systemic-evolution-reconciliation",
            "generated": "2026-08-25",
            "source": "Map of Systemic Evolution",
            "source_url": "https://uranos.ch/index.php/research-menu/cybernetcis",
            "method": "human-reviewed conservative mapping of named components",
            "caution": (
                "Mapping records identity or scope correspondence only. It neither "
                "verifies the source map's influence claim nor creates an atlas relation."
            ),
            "summary": summary,
            "cumulative_history": [
                {
                    "date": "2019-06-10",
                    "event": "The map and its history were added to the curator's SysCoI prior-map collection.",
                },
                {
                    "release": "0.8-expansion-alpha",
                    "event": "The map was registered as a comparator corpus in The Necessary Tangle.",
                },
                {
                    "release": "0.20-prior-maps-alpha",
                    "event": (
                        "All 650 nodes and 1,320 source-reported links were retained in a "
                        "permissioned comparator layer and the first human-reviewed mapping "
                        "cohort was published."
                    ),
                },
            ],
        },
        "nodes": mapping_rows,
        "links": edge_rows,
    }
    OUT.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
