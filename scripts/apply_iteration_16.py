#!/usr/bin/env python3
"""Apply release 0.16: connect the Grammar corpus and record the vision audit."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from apply_iteration_09 import graph_metrics
from apply_iteration_14 import enc, parse
from apply_iteration_15 import make_observations, write_ai_document

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "public-data.json"
DOCS_ASSETS = ROOT / "docs" / "assets"
RELEASE = "0.16-grammar-connections-presentation-alpha"
GENERATED = "2026-08-14"

GRAMMAR_BOOK = "publication_grammar_of_systems_ii"
GRAMMAR_SOURCES = ["src_grammar_2ed_2025", "src_grammar_presentation_2022"]

LAW_IDS = [
    "law_or_principle_law_of_calling",
    "law_or_principle_viability_principle",
    "law_or_principle_homeostasis_principle",
    "law_or_principle_system_stability_principle",
    "law_or_principle_law_of_requisite_variety",
    "law_or_principle_first_circular_causality_principle",
    "law_or_principle_second_circular_causality_principle",
    "law_or_principle_law_of_crossing",
    "law_or_principle_network_power_law",
    "law_or_principle_system_survival_theorem",
    "law_or_principle_system_resonance_principle",
    "law_or_principle_power_structuration_theorem",
    "law_or_principle_conservation_of_adaptation_principle",
    "law_or_principle_darkness_principle",
    "law_or_principle_adams_third_law",
    "law_or_principle_self_organised_criticality",
    "law_or_principle_complexity_instability_principle",
    "law_or_principle_order_osmosis_principle",
    "law_or_principle_first_black_box_principle",
    "law_or_principle_second_black_box_principle",
    "law_or_principle_self_organising_principle",
    "law_or_principle_law_of_reciprocity_of_connections",
    "law_or_principle_redundancy_of_potential_command_principle",
    "law_or_principle_root_structuring_theorem",
    "law_or_principle_structural_viability_theorem",
    "law_or_principle_steady_state_principle",
    "law_or_principle_law_of_sufficient_complexity",
    "law_or_principle_fractal_principle",
    "law_or_principle_relaxation_time_principle",
    "law_or_principle_scaling_stasis_principle",
    "law_or_principle_conant_ashby_theorem",
    "law_or_principle_feedback_dominance_theorem",
    "law_or_principle_principle_of_emergence",
]


def upsert(rows: list[dict[str, Any]], incoming: list[dict[str, Any]], key: str) -> None:
    positions = {row[key]: index for index, row in enumerate(rows)}
    for item in incoming:
        if item[key] in positions:
            rows[positions[item[key]]] = item
        else:
            positions[item[key]] = len(rows)
            rows.append(item)


def described_node() -> dict[str, Any]:
    description = (
        "A black box is a system treated through observable inputs, outputs and behaviour while its internal "
        "organisation remains unknown, inaccessible or deliberately bracketed. The move is selective: what counts "
        "as input, output and relevant behaviour still depends on purpose, boundary and observer."
    )
    return {
        "id": "concept_black_box",
        "label": "Black box",
        "entity_type": "concept",
        "description": description,
        "aliases": enc(["black-box model", "black box modelling"]),
        "boundary_ring": "0",
        "inclusion_reason": "grammar_connection_crosswalk_release_0_16",
        "status": "accepted",
        "source_ids": enc(["src_ashby_intro_cybernetics_1956", *GRAMMAR_SOURCES]),
        "set_tags": enc(["systems", "cybernetics", "grammar_of_systems", "release_0_16"]),
        "espoused_labels": "[]",
        "observed_clusters": "[]",
        "canonical_definition": description,
        "valid_from": "",
        "valid_to": "",
        "external_ids": "{}",
        "geographies": "[]",
        "licence": "",
        "review_status": "provisional_conceptual_crosswalk",
        "reviewed_by": "",
        "reviewed_at": "",
        "x": -0.18,
        "y": -0.28,
        "canonical_id": "concept_black_box",
        "public_visibility": "public",
        "publication_level": "described",
        "public_stub_text": "",
        "public_source_count": 3,
        "no_public_link_count": 0,
    }


def edge(
    edge_id: str,
    source: str,
    target: str,
    relation_type: str,
    family: str,
    phrase: str,
    source_ids: list[str],
    *,
    accepted: bool = False,
) -> dict[str, Any]:
    if accepted:
        return {
            "id": edge_id,
            "source": source,
            "target": target,
            "relation_type": relation_type,
            "relation_family": family,
            "directed": "true",
            "dependency_kind": "",
            "confidence": "0.96",
            "claim_status": "accepted",
            "source_ids": enc(source_ids),
            "evidence_ids": "[]",
            "source_locator": "The Grammar of Systems presentation and second-edition contents",
            "valid_from": "",
            "valid_to": "",
            "scope_conditions": "This states collection placement only. It does not make the book the sole source or final authority for the principle.",
            "assertion_mode": "asserted",
            "inference_method": "direct source-set membership",
            "claim_id": "",
            "reviewed_by": "Benjamin P Taylor",
            "reviewed_at": "2026-08-10",
            "notes": "",
            "plain_phrase": phrase,
            "public_review_label": "source-backed collection statement",
        }
    return {
        "id": edge_id,
        "source": source,
        "target": target,
        "relation_type": relation_type,
        "relation_family": family,
        "directed": "true",
        "dependency_kind": "",
        "confidence": "0.76",
        "claim_status": "provisional",
        "source_ids": enc(source_ids),
        "evidence_ids": "[]",
        "source_locator": "Crosswalk from the maintained law description and cited Grammar sources to the target entry's maintained definition",
        "valid_from": "",
        "valid_to": "",
        "scope_conditions": (
            "This is an interpretive conceptual crosswalk. It does not assert direct historical influence, formal "
            "equivalence or universal validity. The wording should be challenged or strengthened with page-level evidence."
        ),
        "assertion_mode": "interpreted",
        "inference_method": "curator-requested semantic crosswalk of public descriptions",
        "claim_id": "",
        "reviewed_by": "",
        "reviewed_at": "",
        "notes": "",
        "plain_phrase": phrase,
        "public_review_label": "provisional conceptual crosswalk",
    }


# Each tuple is source, target, relation type, family, and the sentence fragment shown to readers.
# Administrative corpus membership does not count: these are public-to-public conceptual or practice routes.
CONNECTIONS: list[tuple[str, str, str, str, str]] = [
    ("law_or_principle_law_of_calling", "concept_boundary", "develops", "conceptual", "makes the act of drawing a system boundary explicit through"),
    ("concept_distinction", "law_or_principle_law_of_calling", "explanatory_prerequisite", "conceptual", "is an explanatory prerequisite for"),
    ("concept_observer", "law_or_principle_law_of_calling", "explanatory_prerequisite", "conceptual", "is an explanatory prerequisite for"),
    ("law_or_principle_law_of_calling", "concept_boundary_critique", "develops", "conceptual", "opens the critical boundary questions developed through"),
    ("method_or_methodology_critical_systems_heuristics_csh", "law_or_principle_law_of_calling", "applies", "practice", "turns boundary naming into critical inquiry through"),

    ("law_or_principle_viability_principle", "concept_viability", "formalises", "conceptual", "offers a systems-law formulation of"),
    ("concept_autonomy", "law_or_principle_viability_principle", "explanatory_prerequisite", "conceptual", "is an explanatory prerequisite for"),
    ("concept_cohesion", "law_or_principle_viability_principle", "explanatory_prerequisite", "conceptual", "is an explanatory prerequisite for"),
    ("law_or_principle_viability_principle", "law_or_principle_homeostasis_principle", "complements", "conceptual", "balances adaptation with regulation alongside"),
    ("method_or_methodology_viable_system_model_vsm", "law_or_principle_viability_principle", "uses", "practice", "uses as a design concern"),
    ("law_or_principle_viability_principle", "concept_holism", "develops", "conceptual", "develops the Grammar pattern of"),

    ("law_or_principle_homeostasis_principle", "concept_homeostasis", "formalises", "conceptual", "offers a systems-law formulation of"),
    ("concept_regulation", "law_or_principle_homeostasis_principle", "explanatory_prerequisite", "conceptual", "is an explanatory prerequisite for"),
    ("concept_negative_feedback", "law_or_principle_homeostasis_principle", "explains", "conceptual", "supplies one regulatory mechanism for"),
    ("method_or_methodology_viable_system_model_vsm", "law_or_principle_homeostasis_principle", "uses", "practice", "uses as a viability concern"),
    ("law_or_principle_homeostasis_principle", "concept_dynamics_of_loops", "develops", "conceptual", "develops the Grammar pattern of"),

    ("law_or_principle_system_stability_principle", "concept_dynamics", "explains", "conceptual", "distinguishes persistent pattern within"),
    ("concept_observer", "law_or_principle_system_stability_principle", "explanatory_prerequisite", "conceptual", "is required to recognise the pattern described by"),
    ("concept_difference", "law_or_principle_system_stability_principle", "explanatory_prerequisite", "conceptual", "is required to notice persistence and change in"),
    ("law_or_principle_system_stability_principle", "law_or_principle_steady_state_principle", "complements", "conceptual", "distinguishes recognisable persistence from the maintained balance described by"),
    ("law_or_principle_system_stability_principle", "concept_holism", "develops", "conceptual", "develops the Grammar pattern of"),

    ("concept_variety", "law_or_principle_law_of_requisite_variety", "explanatory_prerequisite", "conceptual", "is an explanatory prerequisite for"),
    ("concept_regulation", "law_or_principle_law_of_requisite_variety", "explanatory_prerequisite", "conceptual", "sets the regulation problem addressed by"),
    ("concept_variety_attenuation", "law_or_principle_law_of_requisite_variety", "operationalises", "practice", "puts one response to the constraint into practical form for"),
    ("concept_variety_amplification", "law_or_principle_law_of_requisite_variety", "operationalises", "practice", "puts another response to the constraint into practical form for"),
    ("law_or_principle_law_of_requisite_variety", "concept_complexity", "develops", "conceptual", "develops the Grammar pattern of"),

    ("law_or_principle_first_circular_causality_principle", "concept_positive_feedback", "formalises", "conceptual", "offers a systems-law formulation of"),
    ("concept_feedback", "law_or_principle_first_circular_causality_principle", "explanatory_prerequisite", "conceptual", "is an explanatory prerequisite for"),
    ("law_or_principle_first_circular_causality_principle", "concept_dynamics_of_loops", "develops", "conceptual", "develops the Grammar pattern of"),
    ("law_or_principle_first_circular_causality_principle", "law_or_principle_second_circular_causality_principle", "complements", "conceptual", "describes amplification alongside the correction described by"),
    ("method_or_methodology_system_dynamics", "law_or_principle_first_circular_causality_principle", "uses", "practice", "models reinforcing-loop behaviour described by"),

    ("law_or_principle_second_circular_causality_principle", "concept_negative_feedback", "formalises", "conceptual", "offers a systems-law formulation of"),
    ("concept_feedback", "law_or_principle_second_circular_causality_principle", "explanatory_prerequisite", "conceptual", "is an explanatory prerequisite for"),
    ("law_or_principle_second_circular_causality_principle", "concept_dynamics_of_loops", "develops", "conceptual", "develops the Grammar pattern of"),
    ("law_or_principle_second_circular_causality_principle", "concept_homeostasis", "explains", "conceptual", "describes a corrective process which may sustain"),
    ("method_or_methodology_system_dynamics", "law_or_principle_second_circular_causality_principle", "uses", "practice", "models balancing-loop behaviour described by"),

    ("law_or_principle_law_of_crossing", "concept_boundary", "develops", "conceptual", "develops the change of position involved in crossing"),
    ("concept_observer", "law_or_principle_law_of_crossing", "explanatory_prerequisite", "conceptual", "is an explanatory prerequisite for"),
    ("concept_distinction", "law_or_principle_law_of_crossing", "explanatory_prerequisite", "conceptual", "is an explanatory prerequisite for"),
    ("law_or_principle_law_of_crossing", "concept_boundary_critique", "develops", "conceptual", "opens the critical boundary questions developed through"),
    ("law_or_principle_law_of_crossing", "concept_difference", "develops", "conceptual", "develops the Grammar pattern of"),
    ("law_or_principle_law_of_crossing", "concept_transduction", "explains", "conceptual", "provides a boundary-crossing lens for"),

    ("law_or_principle_network_power_law", "concept_networks", "explains", "conceptual", "explains the growth of possible connections within"),
    ("concept_interrelationships", "law_or_principle_network_power_law", "explanatory_prerequisite", "conceptual", "is an explanatory prerequisite for"),
    ("law_or_principle_network_power_law", "concept_complexity", "explains", "conceptual", "describes one source of structural"),
    ("law_or_principle_network_power_law", "concept_relating", "develops", "conceptual", "develops the Grammar pattern of"),
    ("law_or_principle_network_power_law", "law_or_principle_complexity_instability_principle", "complements", "conceptual", "supplies a connection-growth mechanism for"),

    ("concept_adaptation", "law_or_principle_system_survival_theorem", "explanatory_prerequisite", "conceptual", "is an explanatory prerequisite for"),
    ("law_or_principle_system_survival_theorem", "concept_viability", "constrains", "conceptual", "sets a comparative rate condition on"),
    ("concept_dynamics", "law_or_principle_system_survival_theorem", "explanatory_prerequisite", "conceptual", "is an explanatory prerequisite for"),
    ("law_or_principle_system_survival_theorem", "law_or_principle_structural_viability_theorem", "complements", "conceptual", "compares whole-system adaptation rates alongside the recursive rates in"),
    ("law_or_principle_system_survival_theorem", "concept_uncertainty", "develops", "conceptual", "requires explicit time horizon and develops the Grammar pattern of"),

    ("law_or_principle_system_resonance_principle", "concept_relating", "develops", "conceptual", "develops the Grammar pattern of"),
    ("concept_transduction", "law_or_principle_system_resonance_principle", "explanatory_prerequisite", "conceptual", "helps explain signal transformation in"),
    ("law_or_principle_system_resonance_principle", "concept_information", "constrains", "conceptual", "describes a structural condition affecting transmission of"),
    ("concept_boundary", "law_or_principle_system_resonance_principle", "explanatory_prerequisite", "conceptual", "sets the interface examined by"),
    ("law_or_principle_system_resonance_principle", "law_or_principle_law_of_crossing", "complements", "conceptual", "adds structural fit to the positional change described by"),

    ("concept_autonomy", "law_or_principle_power_structuration_theorem", "explanatory_prerequisite", "conceptual", "is one side of the balance examined by"),
    ("concept_cohesion", "law_or_principle_power_structuration_theorem", "explanatory_prerequisite", "conceptual", "is one side of the balance examined by"),
    ("concept_organisational_recursion", "law_or_principle_power_structuration_theorem", "explanatory_prerequisite", "conceptual", "supplies the levels across which"),
    ("law_or_principle_power_structuration_theorem", "concept_holism", "develops", "conceptual", "develops the Grammar pattern of"),
    ("method_or_methodology_viable_system_model_vsm", "law_or_principle_power_structuration_theorem", "uses", "practice", "addresses the recursive power balance described by"),
    ("law_or_principle_power_structuration_theorem", "law_or_principle_redundancy_of_potential_command_principle", "complements", "conceptual", "balances recursive authority alongside the distributed command potential in"),

    ("law_or_principle_conservation_of_adaptation_principle", "concept_adaptation", "formalises", "conceptual", "offers a systems-law formulation of"),
    ("law_or_principle_conservation_of_adaptation_principle", "concept_viability", "explains", "conceptual", "explains ongoing system-environment adjustment required for"),
    ("law_or_principle_conservation_of_adaptation_principle", "concept_complexity", "develops", "conceptual", "develops the Grammar pattern of"),
    ("law_or_principle_conservation_of_adaptation_principle", "law_or_principle_system_survival_theorem", "complements", "conceptual", "states an ongoing adaptation demand alongside the rate limit in"),
    ("law_or_principle_conservation_of_adaptation_principle", "law_or_principle_structural_viability_theorem", "complements", "conceptual", "connects environmental adaptation with the cross-level fit in"),

    ("law_or_principle_darkness_principle", "concept_uncertainty", "formalises", "conceptual", "offers a systems-law formulation of"),
    ("law_or_principle_darkness_principle", "concept_modelling", "constrains", "conceptual", "limits the completeness claims which can be made from"),
    ("concept_observer", "law_or_principle_darkness_principle", "explanatory_prerequisite", "conceptual", "is an explanatory prerequisite for"),
    ("concept_boundary", "law_or_principle_darkness_principle", "explanatory_prerequisite", "conceptual", "makes selective knowledge visible in"),
    ("law_or_principle_darkness_principle", "concept_modelling", "develops", "conceptual", "develops the Grammar pattern of"),
    ("law_or_principle_darkness_principle", "law_or_principle_first_black_box_principle", "complements", "conceptual", "sets a knowledge limit alongside the selective bracketing in"),

    ("concept_interrelationships", "law_or_principle_adams_third_law", "explanatory_prerequisite", "conceptual", "is an explanatory prerequisite for"),
    ("law_or_principle_adams_third_law", "concept_complexity", "explains", "conceptual", "describes a composition failure within"),
    ("law_or_principle_adams_third_law", "concept_holism", "develops", "conceptual", "develops the Grammar pattern of"),
    ("law_or_principle_adams_third_law", "concept_uncertainty", "develops", "conceptual", "develops the Grammar pattern of"),
    ("law_or_principle_network_power_law", "law_or_principle_adams_third_law", "explains", "conceptual", "supplies one connection-growth mechanism for the composition risk in"),

    ("law_or_principle_self_organised_criticality", "concept_self_organisation", "specialises", "conceptual", "describes a more specific critical regime within"),
    ("concept_complexity", "law_or_principle_self_organised_criticality", "explanatory_prerequisite", "conceptual", "is an explanatory prerequisite for"),
    ("law_or_principle_self_organised_criticality", "concept_emergence", "explains", "conceptual", "describes one route to abrupt system-level"),
    ("law_or_principle_self_organised_criticality", "concept_dynamics_of_loops", "develops", "conceptual", "develops the Grammar pattern of"),
    ("law_or_principle_self_organised_criticality", "law_or_principle_complexity_instability_principle", "complements", "conceptual", "describes endogenous critical build-up alongside"),

    ("concept_interrelationships", "law_or_principle_complexity_instability_principle", "explanatory_prerequisite", "conceptual", "is an explanatory prerequisite for"),
    ("law_or_principle_network_power_law", "law_or_principle_complexity_instability_principle", "explains", "conceptual", "supplies a connection-growth mechanism for"),
    ("law_or_principle_complexity_instability_principle", "concept_complexity", "develops", "conceptual", "develops the Grammar pattern of"),
    ("law_or_principle_complexity_instability_principle", "concept_dynamics", "develops", "conceptual", "develops the Grammar pattern of"),
    ("law_or_principle_complexity_instability_principle", "law_or_principle_root_structuring_theorem", "complements", "conceptual", "states the interdependence problem addressed by the grouping heuristic in"),

    ("concept_difference", "law_or_principle_order_osmosis_principle", "explanatory_prerequisite", "conceptual", "is required to compare the neighbouring systems in"),
    ("law_or_principle_order_osmosis_principle", "concept_relating", "develops", "conceptual", "develops the Grammar pattern of"),
    ("law_or_principle_order_osmosis_principle", "concept_complexity", "explains", "conceptual", "describes one possible asymmetry between neighbouring systems under"),
    ("law_or_principle_order_osmosis_principle", "law_or_principle_system_stability_principle", "complements", "conceptual", "describes movement between differently stable systems alongside"),
    ("law_or_principle_order_osmosis_principle", "concept_systemic_governance", "explains", "conceptual", "raises a resource-migration problem for"),

    ("law_or_principle_first_black_box_principle", "concept_black_box", "develops", "conceptual", "gives a functional-use formulation of"),
    ("concept_boundary", "law_or_principle_first_black_box_principle", "explanatory_prerequisite", "conceptual", "sets the interface examined by"),
    ("law_or_principle_first_black_box_principle", "concept_modelling", "develops", "conceptual", "develops the Grammar pattern of"),
    ("law_or_principle_first_black_box_principle", "concept_uncertainty", "develops", "conceptual", "develops the Grammar pattern of"),
    ("law_or_principle_first_black_box_principle", "law_or_principle_second_black_box_principle", "complements", "conceptual", "brackets mechanism alongside the output-variety test in"),

    ("law_or_principle_second_black_box_principle", "concept_black_box", "develops", "conceptual", "gives an output-variety formulation of"),
    ("concept_variety", "law_or_principle_second_black_box_principle", "explanatory_prerequisite", "conceptual", "is an explanatory prerequisite for"),
    ("law_or_principle_second_black_box_principle", "concept_modelling", "develops", "conceptual", "develops the Grammar pattern of"),
    ("law_or_principle_second_black_box_principle", "concept_uncertainty", "develops", "conceptual", "develops the Grammar pattern of"),
    ("law_or_principle_second_black_box_principle", "law_or_principle_law_of_requisite_variety", "complements", "conceptual", "offers an output-variety observation alongside the regulatory constraint in"),

    ("law_or_principle_self_organising_principle", "concept_self_organisation", "formalises", "conceptual", "offers a systems-law formulation of"),
    ("law_or_principle_self_organising_principle", "concept_emergence", "explains", "conceptual", "describes one process which may generate"),
    ("law_or_principle_self_organising_principle", "concept_complexity", "develops", "conceptual", "develops the Grammar pattern of"),
    ("law_or_principle_self_organising_principle", "concept_holism", "develops", "conceptual", "develops the Grammar pattern of"),
    ("law_or_principle_self_organising_principle", "law_or_principle_principle_of_emergence", "complements", "conceptual", "describes a process alongside the whole-level property in"),

    ("law_or_principle_law_of_reciprocity_of_connections", "concept_feedback", "generalises", "conceptual", "broadens one-way action into reciprocal consequences expressed through"),
    ("law_or_principle_law_of_reciprocity_of_connections", "concept_interrelationships", "explains", "conceptual", "explains why action may return through"),
    ("law_or_principle_law_of_reciprocity_of_connections", "concept_relating", "develops", "conceptual", "develops the Grammar pattern of"),
    ("law_or_principle_law_of_reciprocity_of_connections", "concept_dynamics_of_loops", "develops", "conceptual", "develops the Grammar pattern of"),
    ("law_or_principle_law_of_reciprocity_of_connections", "law_or_principle_first_circular_causality_principle", "generalises", "conceptual", "provides a broader reciprocity claim than"),

    ("concept_networks", "law_or_principle_redundancy_of_potential_command_principle", "explanatory_prerequisite", "conceptual", "supplies the distributed decision setting for"),
    ("concept_information", "law_or_principle_redundancy_of_potential_command_principle", "explanatory_prerequisite", "conceptual", "is an explanatory prerequisite for"),
    ("concept_autonomy", "law_or_principle_redundancy_of_potential_command_principle", "explanatory_prerequisite", "conceptual", "is an explanatory prerequisite for distributed action in"),
    ("law_or_principle_redundancy_of_potential_command_principle", "concept_systemic_governance", "explains", "conceptual", "describes a distributed information condition for"),
    ("law_or_principle_redundancy_of_potential_command_principle", "concept_complexity", "develops", "conceptual", "develops the Grammar pattern of"),
    ("method_or_methodology_viable_system_model_vsm", "law_or_principle_redundancy_of_potential_command_principle", "uses", "practice", "addresses distributed command potential described by"),

    ("law_or_principle_root_structuring_theorem", "concept_organisational_recursion", "explains", "conceptual", "offers a grouping heuristic for"),
    ("concept_recursion", "law_or_principle_root_structuring_theorem", "explanatory_prerequisite", "conceptual", "is an explanatory prerequisite for"),
    ("concept_complexity", "law_or_principle_root_structuring_theorem", "explanatory_prerequisite", "conceptual", "sets the structuring problem addressed by"),
    ("law_or_principle_root_structuring_theorem", "law_or_principle_network_power_law", "complements", "conceptual", "offers a grouping response to connection growth in"),
    ("law_or_principle_root_structuring_theorem", "concept_holism", "develops", "conceptual", "develops the Grammar pattern of"),
    ("method_or_methodology_viable_system_model_vsm", "law_or_principle_root_structuring_theorem", "uses", "practice", "uses recursive grouping consonant with"),

    ("law_or_principle_structural_viability_theorem", "concept_viability", "constrains", "conceptual", "sets a cross-level rate condition on"),
    ("concept_adaptation", "law_or_principle_structural_viability_theorem", "explanatory_prerequisite", "conceptual", "is an explanatory prerequisite for"),
    ("concept_organisational_recursion", "law_or_principle_structural_viability_theorem", "explanatory_prerequisite", "conceptual", "supplies the levels compared by"),
    ("method_or_methodology_viable_system_model_vsm", "law_or_principle_structural_viability_theorem", "uses", "practice", "addresses cross-level viability described by"),
    ("law_or_principle_structural_viability_theorem", "concept_dynamics", "develops", "conceptual", "develops the Grammar pattern of"),
    ("law_or_principle_structural_viability_theorem", "law_or_principle_scaling_stasis_principle", "complements", "conceptual", "sets a cross-level adaptation condition alongside"),

    ("law_or_principle_steady_state_principle", "concept_dynamics", "explains", "conceptual", "defines a maintained balance within"),
    ("concept_homeostasis", "law_or_principle_steady_state_principle", "explanatory_prerequisite", "conceptual", "is an explanatory prerequisite for"),
    ("concept_negative_feedback", "law_or_principle_steady_state_principle", "explains", "conceptual", "supplies one possible stabilising process for"),
    ("concept_organisational_recursion", "law_or_principle_steady_state_principle", "explanatory_prerequisite", "conceptual", "supplies the whole-and-part levels compared by"),
    ("law_or_principle_steady_state_principle", "concept_dynamics_of_loops", "develops", "conceptual", "develops the Grammar pattern of"),

    ("law_or_principle_law_of_sufficient_complexity", "concept_complexity", "explains", "conceptual", "treats system behaviour as arising from constituted"),
    ("concept_interrelationships", "law_or_principle_law_of_sufficient_complexity", "explanatory_prerequisite", "conceptual", "is an explanatory prerequisite for"),
    ("law_or_principle_law_of_sufficient_complexity", "concept_emergence", "explains", "conceptual", "provides a structural reading of"),
    ("approach_family_systems_change", "law_or_principle_law_of_sufficient_complexity", "uses", "practice", "uses structure-sensitive change consonant with"),
    ("law_or_principle_law_of_sufficient_complexity", "law_or_principle_adams_third_law", "complements", "conceptual", "links constituted structure to the composition risk in"),
    ("law_or_principle_law_of_sufficient_complexity", "concept_holism", "develops", "conceptual", "develops the Grammar pattern of"),

    ("law_or_principle_fractal_principle", "concept_fractals", "develops", "conceptual", "translates recurring form into an organisational reading of"),
    ("concept_recursion", "law_or_principle_fractal_principle", "explanatory_prerequisite", "conceptual", "is an explanatory prerequisite for"),
    ("law_or_principle_fractal_principle", "concept_organisational_recursion", "explains", "conceptual", "describes recurring form across levels of"),
    ("method_or_methodology_viable_system_model_vsm", "law_or_principle_fractal_principle", "uses", "practice", "uses recursive organisation consonant with"),
    ("law_or_principle_fractal_principle", "law_or_principle_root_structuring_theorem", "complements", "conceptual", "adds recurring form to the grouping heuristic in"),
    ("law_or_principle_fractal_principle", "concept_holism", "develops", "conceptual", "develops the Grammar pattern of"),

    ("concept_dynamics", "law_or_principle_relaxation_time_principle", "explanatory_prerequisite", "conceptual", "is an explanatory prerequisite for"),
    ("concept_homeostasis", "law_or_principle_relaxation_time_principle", "explanatory_prerequisite", "conceptual", "sets the recovery process examined by"),
    ("concept_regulation", "law_or_principle_relaxation_time_principle", "explanatory_prerequisite", "conceptual", "is an explanatory prerequisite for"),
    ("law_or_principle_relaxation_time_principle", "law_or_principle_system_stability_principle", "constrains", "conceptual", "sets a recovery-time condition on"),
    ("method_or_methodology_system_dynamics", "law_or_principle_relaxation_time_principle", "uses", "practice", "models delay and recovery relevant to"),
    ("law_or_principle_relaxation_time_principle", "concept_dynamics_of_loops", "develops", "conceptual", "develops the Grammar pattern of"),

    ("concept_adaptation", "law_or_principle_scaling_stasis_principle", "explanatory_prerequisite", "conceptual", "is the capacity constrained by"),
    ("concept_complexity", "law_or_principle_scaling_stasis_principle", "explanatory_prerequisite", "conceptual", "is an explanatory prerequisite for"),
    ("concept_interrelationships", "law_or_principle_scaling_stasis_principle", "explanatory_prerequisite", "conceptual", "supplies the internal constraint growth described by"),
    ("law_or_principle_scaling_stasis_principle", "concept_viability", "constrains", "conceptual", "describes a scale-related constraint on"),
    ("law_or_principle_scaling_stasis_principle", "law_or_principle_system_survival_theorem", "complements", "conceptual", "adds growth-related adaptation limits to"),
    ("law_or_principle_scaling_stasis_principle", "concept_complexity", "develops", "conceptual", "develops the Grammar pattern of"),

    ("concept_modelling", "law_or_principle_conant_ashby_theorem", "explanatory_prerequisite", "conceptual", "is an explanatory prerequisite for"),
    ("law_or_principle_conant_ashby_theorem", "concept_regulation", "formalises", "conceptual", "formalises a model condition for"),
    ("method_or_methodology_viable_system_model_vsm", "law_or_principle_conant_ashby_theorem", "uses", "practice", "uses the regulator-model concern expressed by"),
    ("law_or_principle_darkness_principle", "law_or_principle_conant_ashby_theorem", "constrains", "conceptual", "limits claims of complete knowledge when interpreting"),
    ("law_or_principle_conant_ashby_theorem", "concept_modelling", "develops", "conceptual", "develops the Grammar pattern of"),

    ("concept_feedback", "law_or_principle_feedback_dominance_theorem", "explanatory_prerequisite", "conceptual", "is an explanatory prerequisite for"),
    ("concept_dynamics", "law_or_principle_feedback_dominance_theorem", "explanatory_prerequisite", "conceptual", "supplies the changing behavioural context examined by"),
    ("law_or_principle_feedback_dominance_theorem", "concept_dynamics_of_loops", "develops", "conceptual", "develops the Grammar pattern of"),
    ("method_or_methodology_system_dynamics", "law_or_principle_feedback_dominance_theorem", "uses", "practice", "tests structure-dominated behaviour described by"),
    ("law_or_principle_feedback_dominance_theorem", "law_or_principle_first_circular_causality_principle", "complements", "conceptual", "adds dominance over input variation to"),
    ("law_or_principle_feedback_dominance_theorem", "concept_modelling", "develops", "conceptual", "warns against input-only explanation and develops the Grammar pattern of"),

    ("law_or_principle_principle_of_emergence", "concept_emergence", "formalises", "conceptual", "offers a systems-law formulation of"),
    ("law_or_principle_principle_of_emergence", "concept_holism", "develops", "conceptual", "develops the Grammar pattern of"),
    ("law_or_principle_principle_of_emergence", "concept_complexity", "develops", "conceptual", "develops the Grammar pattern of"),
    ("law_or_principle_principle_of_emergence", "concept_self_organisation", "often_confused_with", "contestation", "is often confused with"),
    ("law_or_principle_principle_of_emergence", "concept_uncertainty", "develops", "conceptual", "develops the Grammar pattern of"),
    ("law_or_principle_principle_of_emergence", "law_or_principle_self_organising_principle", "complements", "conceptual", "distinguishes whole-level property from the organising process in"),
]


JOURNEY = {
    "id": "journey_grammar_principles_in_connection",
    "title": "The Grammar is a web, not a list",
    "summary": "Use eight laws and principles to move through all nine Grammar thinking patterns and into the wider evidence graph.",
    "audience": "Readers who have met the 33 laws as a list and want to see what they depend on, illuminate and connect to in practice.",
    "duration_minutes": 16,
    "steps": [
        {"node_id": "law_or_principle_law_of_calling", "heading": "A system begins with a distinction", "narrative": "Calling something a system draws a boundary and exposes the observer's choice. Boundaries are made for a purpose, not merely found."},
        {"node_id": "law_or_principle_system_stability_principle", "heading": "Persistence requires noticing difference", "narrative": "A system is recognisable through patterns which persist across observations, even while its parts and activity change."},
        {"node_id": "law_or_principle_network_power_law", "heading": "Connections multiply faster than elements", "narrative": "Relating creates possibility and structural complexity. Counting parts alone hides the combinatorial burden of their possible relationships."},
        {"node_id": "law_or_principle_feedback_dominance_theorem", "heading": "Loops can dominate inputs", "narrative": "Behaviour may arise more from feedback structure than from the initial shove. This is why changing inputs can leave the pattern intact."},
        {"node_id": "law_or_principle_principle_of_emergence", "heading": "Whole-level properties need organisation", "narrative": "Emergence is not magic and not a synonym for self-organisation. It directs attention to interaction, level and pattern."},
        {"node_id": "law_or_principle_viability_principle", "heading": "The whole persists through balances", "narrative": "Autonomy and cohesion, stability and adaptation, present operation and future change have to be held together rather than optimised separately."},
        {"node_id": "law_or_principle_darkness_principle", "heading": "Models are selective", "narrative": "Incomplete knowledge is not an excuse to stop. It is a reason to state boundaries, uncertainty and the purpose of the model."},
        {"node_id": "law_or_principle_law_of_reciprocity_of_connections", "heading": "Action returns through relationship", "narrative": "In a connected system, action on another changes the conditions of the actor. The map closes by returning relating to loops."},
    ],
}


def build_edges(data: dict[str, Any]) -> list[dict[str, Any]]:
    node_by_id = {node["id"]: node for node in data["nodes"]}
    missing = ({item for row in CONNECTIONS for item in row[:2]} | set(LAW_IDS) | {GRAMMAR_BOOK}) - set(node_by_id)
    if missing:
        raise SystemExit(f"Unknown 0.16 connection endpoint(s): {sorted(missing)}")

    output: list[dict[str, Any]] = []
    for law_id in LAW_IDS:
        law_sources = parse(node_by_id[law_id].get("source_ids"), [])
        output.append(
            edge(
                f"e16_grammar_presents_{law_id.removeprefix('law_or_principle_')}",
                GRAMMAR_BOOK,
                law_id,
                "presents",
                "documentary",
                "presents as one of its 33 laws and principles",
                law_sources,
                accepted=True,
            )
        )

    for index, (source, target, relation_type, family, phrase) in enumerate(CONNECTIONS, start=1):
        law_id = source if source in LAW_IDS else target if target in LAW_IDS else ""
        law_sources = parse(node_by_id[law_id].get("source_ids"), []) if law_id else GRAMMAR_SOURCES
        output.append(edge(f"e16_grammar_crosswalk_{index:03d}", source, target, relation_type, family, phrase, law_sources))
    return output


def update_grammar_profile(data: dict[str, Any]) -> None:
    for profile in data.get("profiles", []):
        if profile.get("node_id") != GRAMMAR_BOOK:
            continue
        profile["why_it_matters"] = (
            "The 33 laws are useful only if they can be inspected as connected propositions rather than collected as slogans. "
            "This release makes the book-to-law structure explicit and adds a provisional, challengeable crosswalk from every "
            "law into concepts, other principles and practices already maintained in the atlas."
        )
        profile["practice_connections"] = enc([
            "systems education",
            "diagnosis",
            "transformation design",
            "strategy",
            "concept-to-practice navigation through the public graph",
        ])
        profile["open_checks"] = enc([
            "add page-level locators for every law-to-concept connection",
            "compare the first and second editions",
            "record criticism and alternative formulations",
            "review each provisional crosswalk with Grammar practitioners and domain stewards",
        ])
        profile["last_researched"] = GENERATED
        profile["editorial_note"] = (
            "The 33 source-membership statements are source-backed. The added semantic crosswalk is deliberately provisional: "
            "it exposes an interpretation for review rather than asserting historical influence or formal equivalence."
        )


def main() -> None:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    upsert(data["nodes"], [described_node()], "id")
    upsert(data["edges"], build_edges(data), "id")
    upsert(data["journeys"], [JOURNEY], "id")
    update_grammar_profile(data)

    for inherited_section in ("reading_list_inventory", "reading_list_coverage", "core_systems_practice"):
        if data.get(inherited_section):
            data[inherited_section]["release"] = RELEASE

    metrics = graph_metrics(data)
    meta = data["meta"]
    meta.update({
        "release": RELEASE,
        "generated": GENERATED,
        "project_url": "https://transduction.systems/",
        "reading_list_inventory_url": "https://transduction.systems/reading-list.html",
        "iteration_focus": "rich Grammar of Systems connections, restored entry presentation and an audit against the original vision",
        "public_entry_count": metrics["public_entries"],
        "described_entry_count": metrics["public_entries"],
        "profile_count": len(data.get("profiles", [])),
        "source_count": len(data.get("sources", [])),
        "journey_count": len(data.get("journeys", [])),
        "grammar_crosswalk_status": "all_33_laws_have_public_semantic_connections_provisional_review_open",
        "grammar_crosswalk_connection_count": len(CONNECTIONS),
        "original_vision_audit_url": "https://github.com/antlerboy/the-necessary-tangle/blob/main/documentation/original-vision-audit.md",
    })
    if data.get("reading_list_inventory"):
        report = make_observations(data, data["reading_list_inventory"])
        report["release"] = RELEASE
        report["generated"] = GENERATED
        report["metrics"] = metrics
        data["ai_observations"] = report

    rendered = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    DATA_PATH.write_text(rendered, encoding="utf-8")
    (DOCS_ASSETS / "public-data.json").write_text(rendered, encoding="utf-8")
    (DOCS_ASSETS / "public-data.js").write_text(
        "window.TANGLE_DATA = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n",
        encoding="utf-8",
    )
    if data.get("ai_observations"):
        write_ai_document(data["ai_observations"])
    print(
        f"Applied {RELEASE}: {meta['public_entry_count']} public entries, "
        f"{len(CONNECTIONS)} Grammar crosswalk connections and {meta['journey_count']} journeys"
    )


if __name__ == "__main__":
    main()
