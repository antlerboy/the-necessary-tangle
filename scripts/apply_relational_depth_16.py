#!/usr/bin/env python3
"""Make relational depth measurable and add the first graph-wide enrichment cohort.

This release deliberately distinguishes structural richness from evidential strength.
Interpretive crosswalks make hypotheses navigable, but remain provisional until their
individual statements receive source-level and curator review.
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from apply_iteration_09 import graph_metrics
from apply_iteration_14 import enc, parse
from apply_iteration_15 import make_observations, write_ai_document
from apply_iteration_16 import GENERATED, RELEASE, upsert
from refresh_graph_snapshot import calculate as calculate_graph_snapshot

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "public-data.json"
DOCS_ASSETS = ROOT / "docs" / "assets"
RELATIONAL_DOC = ROOT / "documentation" / "relational-depth.md"


SOURCE_RECORDS: list[dict[str, Any]] = [
    {
        "id": "src_taylor_five_questions_transformation",
        "title": "Five key questions for transformation",
        "source_type": "unpublished_teaching_material",
        "quality_tier": "C",
        "access": "no_public_link",
        "url": "",
        "date": "",
        "notes": "Unpublished one-slide author framework connecting system boundary, purpose, activity, delivery, organisation, governance, transition and triple-loop learning.",
        "creators": enc(["Benjamin P Taylor"]),
        "doi": "",
        "isbn": "",
        "publisher": "Unpublished author material",
        "licence": "not_publicly_licensed",
        "archived_url": "",
        "content_hash": "",
        "review_status": "provided_for_release_review",
        "last_checked": GENERATED,
        "public_link_status": "no_public_link",
    },
    {
        "id": "src_taylor_four_dynamics_2023",
        "title": "Four dynamics for effective organisation",
        "source_type": "unpublished_teaching_material",
        "quality_tier": "C",
        "access": "no_public_link",
        "url": "",
        "date": "2023-10-10",
        "notes": "Unpublished author teaching deck presenting segment, blend, empower and harmonise as dynamics to hold in balance, with associated organisational practices.",
        "creators": enc(["Benjamin P Taylor"]),
        "doi": "",
        "isbn": "",
        "publisher": "Unpublished author material",
        "licence": "not_publicly_licensed",
        "archived_url": "",
        "content_hash": "",
        "review_status": "provided_for_release_review",
        "last_checked": GENERATED,
        "public_link_status": "no_public_link",
    },
    {
        "id": "src_taylor_vsm_simplification_2023",
        "title": "Organisations need to deal with complexity: a simplification of the Viable System Model",
        "source_type": "unpublished_teaching_material",
        "quality_tier": "C",
        "access": "no_public_link",
        "url": "",
        "date": "2023-03-01",
        "notes": "Unpublished author teaching deck relating organisational capacity, capability, connectedness and variety to operational, environmental and future complexity.",
        "creators": enc(["Benjamin P Taylor"]),
        "doi": "",
        "isbn": "",
        "publisher": "Unpublished author material",
        "licence": "not_publicly_licensed",
        "archived_url": "",
        "content_hash": "",
        "review_status": "provided_for_release_review",
        "last_checked": GENERATED,
        "public_link_status": "no_public_link",
    },
    {
        "id": "src_taylor_clarity_practices_2024",
        "title": "Clarity practices: five core practices",
        "source_type": "unpublished_teaching_material",
        "quality_tier": "C",
        "access": "no_public_link",
        "url": "",
        "date": "2024-12-11",
        "notes": "Unpublished author teaching deck connecting constructive conversation, clarity, reflection, culture shaping and intent in a learning and purposeful system.",
        "creators": enc(["Benjamin P Taylor"]),
        "doi": "",
        "isbn": "",
        "publisher": "Unpublished author material",
        "licence": "not_publicly_licensed",
        "archived_url": "",
        "content_hash": "",
        "review_status": "provided_for_release_review",
        "last_checked": GENERATED,
        "public_link_status": "no_public_link",
    },
    {
        "id": "src_taylor_better_conversations_2025",
        "title": "Better conversations for better realities: learning loops to break the devil's bargain",
        "source_type": "unpublished_teaching_material",
        "quality_tier": "C",
        "access": "no_public_link",
        "url": "",
        "date": "2025-07-01",
        "notes": "Unpublished author teaching deck connecting multiple worlds, whole-system planning, the ladder of inference and reinforcing feedback.",
        "creators": enc(["Benjamin P Taylor"]),
        "doi": "",
        "isbn": "",
        "publisher": "Unpublished author material",
        "licence": "not_publicly_licensed",
        "archived_url": "",
        "content_hash": "",
        "review_status": "provided_for_release_review",
        "last_checked": GENERATED,
        "public_link_status": "no_public_link",
    },
]


# These statements are directly recoverable from the supplied author material. They
# remain provisional until the author/curator reviews the exact public wording.
SOURCE_BACKED_LINKS: list[tuple[str, str, str, str, str, str, str]] = [
    ("practice_systems_convening", "concept_boundary", "applies", "practice", "works explicitly with", "src_taylor_boundaries_convening_2025", "slides 1–2 and 4"),
    ("practice_systems_convening", "approach_family_systems_change", "operationalises", "practice", "creates social conditions for", "src_taylor_boundaries_convening_2025", "slides 1 and 4"),
    ("approach_family_systems_change", "concept_boundary", "uses", "practice", "treats as constitutive of the system of concern", "src_taylor_boundaries_convening_2025", "slide 4"),
    ("approach_family_systems_change", "concept_multiple_perspectives", "uses", "practice", "learns by seeing the system from", "src_taylor_boundaries_convening_2025", "slide 4"),
    ("approach_family_systems_change", "concept_purpose", "uses", "practice", "orients inquiry and intervention through", "src_taylor_five_questions_transformation", "slide 1"),
    ("approach_family_systems_change", "concept_systemic_governance", "applies", "practice", "includes explicit questions about", "src_taylor_five_questions_transformation", "slide 1"),
    ("method_or_methodology_organic_systems_framework", "concept_autonomy", "uses", "practice", "holds individual empowerment in balance through", "src_taylor_four_dynamics_2023", "slides 10, 12–13 and 18"),
    ("method_or_methodology_organic_systems_framework", "concept_cohesion", "uses", "practice", "holds shared work and alignment in balance through", "src_taylor_four_dynamics_2023", "slides 9, 11–13, 17 and 19"),
    ("method_or_methodology_organic_systems_framework", "concept_purpose", "uses", "practice", "orients harmonising activity through", "src_taylor_four_dynamics_2023", "slides 11–12 and 19"),
    ("method_or_methodology_viable_system_model_vsm", "concept_complexity", "applies", "practice", "organises inquiry into the handling of", "src_taylor_vsm_simplification_2023", "slides 2–3"),
    ("method_or_methodology_viable_system_model_vsm", "concept_variety", "uses", "practice", "examines capacity to respond through", "src_taylor_vsm_simplification_2023", "slide 2"),
    ("method_or_methodology_viable_system_model_vsm", "concept_adaptation", "uses", "practice", "asks what future change requires of", "src_taylor_vsm_simplification_2023", "slides 2–3"),
    ("method_or_methodology_viable_system_model_vsm", "concept_systemic_governance", "applies", "practice", "frames questions of accountability, resource and future through", "src_taylor_vsm_simplification_2023", "slides 2–3"),
    ("intervention_skill_productive_conversations", "concept_double_loop_learning", "operationalises", "practice", "supports examination of reasoning and action in", "src_taylor_clarity_practices_2024", "slides 2 and 5–6"),
    ("intervention_skill_decision_structure_design", "concept_requisite_variety", "applies", "practice", "protects the decision capacity required by", "src_taylor_clarity_practices_2024", "slides 10–11"),
    ("intervention_skill_ladder_of_inference", "concept_observer", "applies", "practice", "makes selective observation explicit for", "src_taylor_better_conversations_2025", "slide 16"),
    ("intervention_skill_ladder_of_inference", "concept_feedback", "uses", "practice", "shows conclusions returning through", "src_taylor_better_conversations_2025", "slide 16"),
    ("intervention_skill_productive_conversations", "concept_multiple_perspectives", "uses", "practice", "makes different interpretations discussable as", "src_taylor_better_conversations_2025", "slides 2 and 16"),
]


# Every SCiO intervention-skill entry gets at least three typed routes into concepts,
# methods or practices. The mapping is interpretive, source-visible and challengeable.
PRACTICE_LINKS: dict[str, list[tuple[str, str, str, str]]] = {
    "intervention_skill_action_learning": [
        ("concept_double_loop_learning", "uses", "practice", "uses reflective cycles associated with"),
        ("concept_feedback", "applies", "practice", "turns experience into action through"),
        ("practice_systems_practice", "complements", "conceptual", "complements situated"),
    ],
    "intervention_skill_action_research": [
        ("concept_double_loop_learning", "uses", "practice", "uses repeated inquiry associated with"),
        ("approach_family_systems_change", "applies", "practice", "joins inquiry and action in"),
        ("method_or_methodology_systemic_intervention", "complements", "conceptual", "complements the plural design stance of"),
    ],
    "intervention_skill_agile_project_management": [
        ("concept_feedback", "uses", "practice", "organises short cycles around"),
        ("concept_adaptation", "applies", "practice", "supports incremental"),
        ("concept_single_loop_learning", "complements", "conceptual", "often works through corrective"),
    ],
    "intervention_skill_appreciative_inquiry": [
        ("concept_multiple_perspectives", "uses", "practice", "elicits valued experience from"),
        ("concept_purpose", "applies", "practice", "organises desired possibility around"),
        ("approach_family_systems_change", "complements", "conceptual", "offers a strengths-oriented route into"),
    ],
    "intervention_skill_coaching": [
        ("concept_observer", "applies", "practice", "supports reflexive attention to the"),
        ("concept_double_loop_learning", "uses", "practice", "can surface assumptions through"),
        ("intervention_skill_productive_conversations", "complements", "conceptual", "depends on and complements"),
    ],
    "intervention_skill_constellations": [
        ("concept_modelling", "uses", "practice", "creates a spatial form of"),
        ("concept_multiple_perspectives", "applies", "practice", "tests hypotheses across"),
        ("tool_systems_mapping", "complements", "conceptual", "offers an embodied complement to"),
    ],
    "intervention_skill_conversation_mapping": [
        ("concept_explicit_semantics", "operationalises", "practice", "makes conversational distinctions visible through"),
        ("concept_multiple_perspectives", "uses", "practice", "retains disagreement among"),
        ("intervention_skill_productive_conversations", "complements", "conceptual", "provides a representational complement to"),
    ],
    "intervention_skill_covert_operations": [
        ("law_or_principle_power_structuration_theorem", "applies", "practice", "exposes unofficial action within the power tensions described by"),
        ("concept_uncertainty", "uses", "practice", "operates under and can increase"),
        ("approach_family_systems_change", "challenges", "contestation", "challenges accounts of change that notice only formal"),
    ],
    "intervention_skill_critical_social_learning_systems": [
        ("concept_boundary_critique", "applies", "practice", "makes learning conditions contestable through"),
        ("concept_double_loop_learning", "uses", "practice", "questions governing assumptions through"),
        ("practice_systems_practice", "challenges", "contestation", "challenges power-blind versions of"),
    ],
    "intervention_skill_culture_mapping": [
        ("tool_systems_mapping", "uses", "practice", "makes recurring cultural patterns visible through"),
        ("concept_emergence", "applies", "practice", "examines interaction-level conditions for"),
        ("tradition_complex_responsive_processes", "complements", "conceptual", "complements relational accounts in"),
    ],
    "intervention_skill_data_analysis_including_spc_and_statistics": [
        ("concept_uncertainty", "uses", "practice", "represents and qualifies"),
        ("concept_feedback", "applies", "practice", "supports learning from observed"),
        ("practice_quality_management", "complements", "conceptual", "supplies evidence practices for"),
    ],
    "intervention_skill_decision_structure_design": [
        ("concept_information", "uses", "practice", "routes decision-relevant"),
        ("concept_systemic_governance", "applies", "practice", "puts decision rights into"),
        ("method_or_methodology_viable_system_model_vsm", "complements", "conceptual", "complements recursive governance in"),
    ],
    "intervention_skill_deming": [
        ("practice_quality_management", "applies", "practice", "provides a systemic foundation for"),
        ("concept_feedback", "uses", "practice", "organises improvement around"),
        ("tradition_systems_theory", "complements", "conceptual", "joins management practice to"),
    ],
    "intervention_skill_detecting_and_managing_undiscussables": [
        ("concept_observer", "applies", "practice", "makes participation in silence visible to the"),
        ("concept_multiple_perspectives", "uses", "practice", "protects excluded or unsafe"),
        ("intervention_skill_productive_conversations", "complements", "conceptual", "creates conditions for"),
    ],
    "intervention_skill_facilitation": [
        ("concept_multiple_perspectives", "applies", "practice", "designs participation across"),
        ("concept_purpose", "uses", "practice", "orients group process through"),
        ("practice_systems_convening", "complements", "conceptual", "supports but does not exhaust"),
    ],
    "intervention_skill_flawless_consulting": [
        ("practice_systems_practice", "applies", "practice", "offers contracting disciplines for"),
        ("intervention_skill_productive_conversations", "uses", "practice", "depends on direct"),
        ("intervention_skill_coaching", "complements", "conceptual", "shares a client-ownership stance with"),
    ],
    "intervention_skill_fractal_enterprise_model_and_capabilities": [
        ("concept_recursion", "uses", "practice", "represents repeated organisational relations through"),
        ("concept_organisational_recursion", "applies", "practice", "examines capability across levels of"),
        ("method_or_methodology_viable_system_model_vsm", "complements", "conceptual", "offers a capability-model complement to"),
    ],
    "intervention_skill_graphic_facilitation_and_visualisation": [
        ("concept_modelling", "uses", "practice", "creates shared provisional"),
        ("concept_multiple_perspectives", "applies", "practice", "retains contributions from"),
        ("tool_systems_mapping", "complements", "conceptual", "complements formal and informal"),
    ],
    "intervention_skill_iceberg_model": [
        ("tool_systems_mapping", "uses", "practice", "prompts deeper inquiry within"),
        ("concept_dynamics", "applies", "practice", "looks beneath events for"),
        ("concept_feedback", "complements", "conceptual", "can prepare inquiry into"),
    ],
    "intervention_skill_influence_mapping": [
        ("concept_networks", "uses", "practice", "represents actors and ties as"),
        ("law_or_principle_power_structuration_theorem", "applies", "practice", "makes power placement discussable alongside"),
        ("tool_systems_mapping", "complements", "conceptual", "specialises the relational work of"),
    ],
    "intervention_skill_influencing_and_mediation": [
        ("concept_multiple_perspectives", "uses", "practice", "works with incompatible"),
        ("concept_relating", "applies", "practice", "changes possibilities through"),
        ("method_or_methodology_confrontation_analysis_conan", "complements", "conceptual", "complements structured conflict analysis in"),
    ],
    "intervention_skill_interview_technique": [
        ("concept_multiple_perspectives", "applies", "practice", "elicits situated"),
        ("concept_observer", "uses", "practice", "requires reflexivity from the"),
        ("concept_modelling", "complements", "conceptual", "supplies accounts used in"),
    ],
    "intervention_skill_ladder_of_abstraction": [
        ("concept_distinction", "applies", "practice", "checks movement between levels through"),
        ("concept_modelling", "uses", "practice", "moves between observation and abstraction in"),
        ("concept_boundary", "complements", "conceptual", "makes category changes visible alongside"),
    ],
    "intervention_skill_ladder_of_inference": [
        ("concept_observer", "applies", "practice", "makes selection and interpretation visible to the"),
        ("concept_feedback", "uses", "practice", "shows action reinforcing assumptions through"),
        ("concept_double_loop_learning", "complements", "conceptual", "provides a conversational route into"),
    ],
    "intervention_skill_large_group_decision_approaches": [
        ("concept_systemic_governance", "applies", "practice", "structures broad participation in"),
        ("concept_multiple_perspectives", "uses", "practice", "synthesises without erasing"),
        ("method_or_methodology_syntegration_team_syntegrity", "complements", "conceptual", "includes structured possibilities such as"),
    ],
    "intervention_skill_large_group_engagement_processes": [
        ("practice_systems_convening", "applies", "practice", "creates participative spaces for"),
        ("concept_networks", "uses", "practice", "builds temporary and continuing"),
        ("intervention_skill_facilitation", "complements", "conceptual", "extends the scale of"),
    ],
    "intervention_skill_lean_and_six_sigma": [
        ("practice_quality_management", "applies", "practice", "specialises improvement within"),
        ("concept_feedback", "uses", "practice", "tests process change through"),
        ("concept_purpose", "complements", "conceptual", "needs a systemic account of"),
    ],
    "intervention_skill_learning_design_and_learning_conversations": [
        ("concept_double_loop_learning", "applies", "practice", "can design reflection for"),
        ("concept_feedback", "uses", "practice", "builds capability through"),
        ("practice_systems_practice", "complements", "conceptual", "supports the development of"),
    ],
    "intervention_skill_linear_argument_technique": [
        ("concept_explicit_semantics", "operationalises", "practice", "makes claims and reasons inspectable through"),
        ("concept_distinction", "uses", "practice", "depends on stable"),
        ("concept_modelling", "complements", "conceptual", "is one deliberately simplified form of"),
    ],
    "intervention_skill_listening_and_multiple_perspectives": [
        ("concept_multiple_perspectives", "operationalises", "practice", "puts into conversational practice"),
        ("concept_observer", "uses", "practice", "locates each account with an"),
        ("concept_boundary_critique", "complements", "conceptual", "supports inquiry into exclusion through"),
    ],
    "intervention_skill_managing_deflection_resistance_and_challenge": [
        ("approach_family_systems_change", "applies", "practice", "works with opposition encountered in"),
        ("law_or_principle_power_structuration_theorem", "uses", "practice", "keeps authority and autonomy visible through"),
        ("concept_multiple_perspectives", "complements", "conceptual", "resists pathologising disagreement by retaining"),
    ],
    "intervention_skill_metaphors": [
        ("concept_modelling", "applies", "practice", "offers partial analogical"),
        ("concept_multiple_perspectives", "uses", "practice", "compares what different"),
        ("concept_distinction", "complements", "conceptual", "reveals and conceals through"),
    ],
    "intervention_skill_neuro_linguistic_programming_nlp": [
        ("concept_modelling", "uses", "practice", "uses representational claims resembling"),
        ("intervention_skill_coaching", "complements", "conceptual", "is sometimes combined in practice with"),
        ("intervention_skill_scientific_theory_and_evidence", "challenges", "contestation", "is subject to evidential challenge from"),
    ],
    "intervention_skill_presentation_design": [
        ("concept_modelling", "applies", "practice", "builds a selective communicative"),
        ("concept_explicit_semantics", "uses", "practice", "protects meaning through"),
        ("concept_multiple_perspectives", "complements", "conceptual", "anticipates interpretation by"),
    ],
    "intervention_skill_productive_conversations": [
        ("concept_double_loop_learning", "applies", "practice", "supports examination of assumptions through"),
        ("concept_feedback", "uses", "practice", "returns consequences into dialogue through"),
        ("practice_systems_practice", "complements", "conceptual", "supplies a relational discipline for"),
    ],
    "intervention_skill_public_speaking": [
        ("concept_explicit_semantics", "applies", "practice", "communicates distinctions through"),
        ("concept_multiple_perspectives", "uses", "practice", "adapts explanation for"),
        ("intervention_skill_presentation_design", "complements", "conceptual", "depends on and extends"),
    ],
    "intervention_skill_questionnaire_design": [
        ("concept_multiple_perspectives", "applies", "practice", "samples accounts from"),
        ("concept_uncertainty", "uses", "practice", "must qualify inference through"),
        ("concept_observer", "complements", "conceptual", "makes the question designer part of the"),
    ],
    "intervention_skill_scientific_theory_and_evidence": [
        ("concept_modelling", "applies", "practice", "tests explanatory"),
        ("concept_uncertainty", "uses", "practice", "states and investigates"),
        ("concept_explicit_semantics", "complements", "conceptual", "depends on precise claims through"),
    ],
    "intervention_skill_selling_systems_approaches": [
        ("practice_systems_practice", "applies", "practice", "sets responsible expectations for"),
        ("concept_purpose", "uses", "practice", "starts from the sponsor's"),
        ("concept_uncertainty", "complements", "conceptual", "makes limits and learning needs visible through"),
    ],
    "intervention_skill_stakeholder_analysis": [
        ("concept_boundary_critique", "applies", "practice", "tests inclusion and exclusion through"),
        ("law_or_principle_power_structuration_theorem", "uses", "practice", "makes recursive authority visible alongside"),
        ("concept_multiple_perspectives", "complements", "conceptual", "organises inquiry across"),
    ],
    "intervention_skill_training_design": [
        ("concept_double_loop_learning", "applies", "practice", "can develop reflective capability for"),
        ("concept_feedback", "uses", "practice", "builds practice through"),
        ("practice_core_systems_practice_spine", "complements", "conceptual", "supports progression through"),
    ],
    "intervention_skill_transactional_analysis": [
        ("concept_dynamics_of_loops", "uses", "practice", "examines recurring interpersonal"),
        ("concept_relating", "applies", "practice", "locates repeated exchange within"),
        ("concept_observer", "complements", "conceptual", "invites reflexive attention from the"),
    ],
    "intervention_skill_trust_mapping_and_metrics": [
        ("tool_systems_mapping", "uses", "practice", "represents reliance and vulnerability through"),
        ("concept_networks", "applies", "practice", "locates trust within"),
        ("concept_uncertainty", "complements", "conceptual", "keeps contextual limits visible through"),
    ],
    "intervention_skill_values_mapping_and_integration": [
        ("concept_boundary_critique", "applies", "practice", "examines whose values count through"),
        ("concept_purpose", "uses", "practice", "connects trade-offs to"),
        ("concept_multiple_perspectives", "complements", "conceptual", "retains value conflict among"),
    ],
    "intervention_skill_vanguard_method": [
        ("concept_purpose", "applies", "practice", "studies service from customer"),
        ("concept_feedback", "uses", "practice", "redesigns measures as"),
        ("approach_family_systems_change", "complements", "conceptual", "offers an outside-in route into"),
    ],
    "intervention_skill_verbal_behaviours_rackham": [
        ("intervention_skill_productive_conversations", "applies", "practice", "provides observable categories for"),
        ("concept_feedback", "uses", "practice", "supports behavioural learning through"),
        ("intervention_skill_conversation_mapping", "complements", "conceptual", "complements content-focused"),
    ],
    "intervention_skill_workshop_design": [
        ("intervention_skill_facilitation", "applies", "practice", "creates the bounded conditions for"),
        ("concept_purpose", "uses", "practice", "organises sequence around"),
        ("practice_systems_convening", "complements", "conceptual", "supports but does not replace"),
    ],
}


# A bounded first pass for the previously reader-isolated concepts, methods, tools,
# traditions and people. This is not a claim that the remaining nodes are complete.
GAP_LINKS: list[tuple[str, str, str, str, str]] = [
    ("concept_non_linearity", "concept_feedback", "explains", "conceptual", "is often generated through interacting"),
    ("concept_non_linearity", "concept_complexity", "complements", "conceptual", "is one mechanism contributing to"),
    ("method_or_methodology_system_dynamics", "concept_non_linearity", "uses", "practice", "models"),
    ("concept_randomness", "concept_uncertainty", "specialises", "conceptual", "is one possible source of"),
    ("concept_randomness", "concept_unpredictability", "explains", "conceptual", "can produce"),
    ("intervention_skill_scientific_theory_and_evidence", "concept_randomness", "uses", "practice", "tests probabilistic claims about"),
    ("concept_sensitive_dependence_on_initial_conditions", "tradition_chaos_theory", "definitional_prerequisite", "conceptual", "is a defining idea within"),
    ("concept_sensitive_dependence_on_initial_conditions", "concept_unpredictability", "explains", "conceptual", "can create horizon-dependent"),
    ("concept_non_linearity", "concept_sensitive_dependence_on_initial_conditions", "explanatory_prerequisite", "conceptual", "supports the dynamics required for"),
    ("concept_unpredictability", "concept_uncertainty", "specialises", "conceptual", "is a horizon-specific form of"),
    ("concept_unpredictability", "concept_complexity", "complements", "conceptual", "is common but not universal within"),
    ("practice_systems_practice", "concept_unpredictability", "uses", "practice", "works explicitly with"),

    ("method_or_methodology_agent_based_modelling", "concept_emergence", "uses", "practice", "explores the production of"),
    ("method_or_methodology_agent_based_modelling", "concept_self_organisation", "uses", "practice", "simulates local interaction associated with"),
    ("method_or_methodology_agent_based_modelling", "method_or_methodology_system_dynamics", "complements", "conceptual", "offers an agent-level modelling complement to"),
    ("method_or_methodology_bubble_strategy", "approach_family_systems_change", "applies", "practice", "creates protected experiments within"),
    ("method_or_methodology_bubble_strategy", "concept_emergence", "uses", "practice", "allows new practice to develop through"),
    ("method_or_methodology_bubble_strategy", "method_or_methodology_mosaic_transformation", "complements", "conceptual", "complements sequenced change in"),
    ("method_or_methodology_confrontation_analysis_conan", "concept_multiple_perspectives", "uses", "practice", "represents incompatible positions among"),
    ("method_or_methodology_confrontation_analysis_conan", "concept_relating", "applies", "practice", "examines changing possibilities through"),
    ("method_or_methodology_confrontation_analysis_conan", "tradition_game_theory", "complements", "conceptual", "offers a dilemma-focused complement to"),
    ("method_or_methodology_informed_group_dynamics", "concept_multiple_perspectives", "uses", "practice", "organises group inquiry across"),
    ("method_or_methodology_informed_group_dynamics", "practice_systems_convening", "applies", "practice", "supports structured participation within"),
    ("method_or_methodology_informed_group_dynamics", "intervention_skill_facilitation", "complements", "conceptual", "requires further public evidence alongside"),
    ("method_or_methodology_interactive_management", "tool_systems_mapping", "uses", "practice", "builds relational structure through"),
    ("method_or_methodology_interactive_management", "concept_multiple_perspectives", "uses", "practice", "structures dialogue among"),
    ("method_or_methodology_interactive_management", "practice_systems_convening", "complements", "conceptual", "offers a formal group-process complement to"),
    ("method_or_methodology_interactive_planning", "approach_family_systems_change", "applies", "practice", "uses idealised redesign within"),
    ("method_or_methodology_interactive_planning", "concept_purpose", "uses", "practice", "frames desired design through"),
    ("method_or_methodology_interactive_planning", "practice_systems_practice", "complements", "conceptual", "offers a participative planning route within"),
    ("method_or_methodology_mosaic_transformation", "concept_complexity", "uses", "practice", "sequences change in response to"),
    ("method_or_methodology_mosaic_transformation", "concept_variety", "uses", "practice", "distributes change to preserve"),
    ("method_or_methodology_mosaic_transformation", "approach_family_systems_change", "complements", "conceptual", "specialises a packet-based route into"),
    ("method_or_methodology_socio_technical_systems", "concept_boundary", "uses", "practice", "draws a joint social and technical"),
    ("method_or_methodology_socio_technical_systems", "concept_interrelationships", "applies", "practice", "examines work through"),
    ("method_or_methodology_socio_technical_systems", "approach_family_systems_change", "complements", "conceptual", "offers a joint-design route into"),
    ("method_or_methodology_strategic_options_development_and_analysis_soda", "tool_systems_mapping", "uses", "practice", "structures issues through"),
    ("method_or_methodology_strategic_options_development_and_analysis_soda", "concept_multiple_perspectives", "uses", "practice", "retains differing interpretations from"),
    ("method_or_methodology_strategic_options_development_and_analysis_soda", "concept_purpose", "applies", "practice", "develops strategic options around"),
    ("method_or_methodology_syntegration_team_syntegrity", "practice_systems_convening", "applies", "practice", "provides a structured architecture for"),
    ("method_or_methodology_syntegration_team_syntegrity", "concept_systemic_governance", "uses", "practice", "distributes participation through"),
    ("method_or_methodology_syntegration_team_syntegrity", "concept_multiple_perspectives", "complements", "conceptual", "creates repeated encounters among"),

    ("tool_behaviour_over_time_graphs", "concept_dynamics", "operationalises", "practice", "makes changing patterns visible for"),
    ("tool_behaviour_over_time_graphs", "concept_feedback", "uses", "practice", "prepares inquiry into"),
    ("tool_behaviour_over_time_graphs", "method_or_methodology_system_dynamics", "complements", "conceptual", "provides an exploratory representation used with"),
    ("tool_context_diagrams", "concept_boundary", "operationalises", "practice", "makes a chosen system boundary visible through"),
    ("tool_context_diagrams", "concept_interrelationships", "uses", "practice", "selects external exchanges from"),
    ("tool_context_diagrams", "concept_modelling", "complements", "conceptual", "is a deliberately sparse form of"),
    ("tool_enablers_and_inhibitors", "concept_interrelationships", "uses", "practice", "examines supporting and obstructing"),
    ("tool_enablers_and_inhibitors", "concept_uncertainty", "applies", "practice", "treats causal contribution under"),
    ("tool_enablers_and_inhibitors", "approach_family_systems_change", "complements", "conceptual", "supports intervention inquiry within"),
    ("tool_identify_leverage", "concept_leverage_points", "operationalises", "practice", "puts into inquiry"),
    ("tool_identify_leverage", "concept_feedback", "uses", "practice", "searches structural possibilities within"),
    ("tool_identify_leverage", "method_or_methodology_system_dynamics", "complements", "conceptual", "can be informed by modelling from"),
    ("tool_map_analysis_and_narrative", "tool_systems_mapping", "uses", "practice", "adds an interpretive account to"),
    ("tool_map_analysis_and_narrative", "concept_explicit_semantics", "operationalises", "practice", "states what mapped lines mean through"),
    ("tool_map_analysis_and_narrative", "concept_modelling", "complements", "conceptual", "makes assumptions discussable within"),
    ("tool_monitoring_and_evaluation_strategy", "concept_feedback", "operationalises", "practice", "returns observations into action through"),
    ("tool_monitoring_and_evaluation_strategy", "concept_double_loop_learning", "uses", "practice", "can test assumptions through"),
    ("tool_monitoring_and_evaluation_strategy", "concept_systemic_governance", "complements", "conceptual", "supports accountable learning within"),
    ("tool_pig_model", "tool_systems_mapping", "uses", "practice", "requires fuller source review as a form of"),
    ("tool_pig_model", "concept_boundary", "applies", "practice", "provisionally appears to make discussable"),
    ("tool_pig_model", "concept_purpose", "complements", "conceptual", "requires its intended use to be checked against"),
    ("tool_rich_picture", "method_or_methodology_soft_systems_methodology_ssm", "uses", "practice", "is commonly used within"),
    ("tool_rich_picture", "concept_multiple_perspectives", "operationalises", "practice", "makes room in one representation for"),
    ("tool_rich_picture", "concept_boundary", "complements", "conceptual", "keeps early inquiry open around"),
    ("tool_stock_and_flow_diagrams", "method_or_methodology_system_dynamics", "uses", "practice", "is a core representational form within"),
    ("tool_stock_and_flow_diagrams", "concept_dynamics", "operationalises", "practice", "represents accumulation and rates within"),
    ("tool_stock_and_flow_diagrams", "concept_feedback", "complements", "conceptual", "adds accumulation structure to"),
    ("tool_systems_mapping", "concept_interrelationships", "operationalises", "practice", "makes selected relationships visible as"),
    ("tool_systems_mapping", "concept_boundary", "uses", "practice", "depends on an explicit or implicit"),
    ("tool_systems_mapping", "concept_modelling", "complements", "conceptual", "is a family of visual"),
    ("tool_theory_of_change_maps", "concept_purpose", "uses", "practice", "organises intended outcomes around"),
    ("tool_theory_of_change_maps", "concept_feedback", "applies", "practice", "supports testing and revision through"),
    ("tool_theory_of_change_maps", "concept_uncertainty", "complements", "conceptual", "should expose assumptions and"),

    ("tradition_chaos_theory", "concept_non_linearity", "uses", "practice", "studies deterministic dynamics shaped by"),
    ("tradition_chaos_theory", "concept_unpredictability", "explains", "conceptual", "places horizon-sensitive limits on"),
    ("tradition_chaos_theory", "concept_randomness", "often_confused_with", "contestation", "is often confused with"),
    ("tradition_game_theory", "concept_interrelationships", "uses", "practice", "formalises outcome dependence through"),
    ("tradition_game_theory", "concept_networks", "complements", "conceptual", "can represent strategic interaction within"),
    ("tradition_game_theory", "method_or_methodology_confrontation_analysis_conan", "complements", "conceptual", "provides a neighbouring formal tradition for"),

    ("person_stafford_beer", "method_or_methodology_viable_system_model_vsm", "developed", "historical", "developed"),
    ("person_stafford_beer", "method_or_methodology_syntegration_team_syntegrity", "developed", "historical", "developed"),
    ("person_stafford_beer", "tradition_cybernetics", "self_identifies_with", "identity", "worked explicitly within"),
    ("person_walter_b_cannon", "concept_homeostasis", "developed", "historical", "developed the physiological account named"),
    ("person_walter_b_cannon", "concept_regulation", "develops", "conceptual", "developed a physiological account contributing to"),
    ("person_igor_perko", "comparator_perko_systems_researchers_network_2026", "developed", "historical", "developed"),
    ("person_igor_perko", "tradition_systems_theory", "self_identifies_with", "identity", "maps researchers working in and around"),

    ("organisation_the_cynefin_company", "corpus_cynefin_io_wiki", "maintains", "documentary", "maintains"),
    ("corpus_cynefin_io_wiki", "method_or_methodology_cynefin_framework", "presents", "documentary", "documents and presents"),
    ("corpus_cynefin_io_wiki", "approach_family_naturalising_sense_making", "presents", "documentary", "documents material associated with"),
]


# Raise the remaining concept, method, tool and tradition stubs above a single-family
# link pattern. These are deliberately small, typed bridges rather than bulk similarity.
SECOND_PASS_LINKS: list[tuple[str, str, str, str, str]] = [
    ("tradition_chaos_theory", "concept_chaos", "formalises", "conceptual", "provides a dynamical-systems account of"),
    ("concept_chaos", "concept_unpredictability", "explains", "conceptual", "can produce horizon-dependent"),
    ("method_or_methodology_system_dynamics", "concept_chaos", "uses", "practice", "can model regimes exhibiting"),
    ("practice_systems_practice", "concept_difference", "uses", "practice", "notices and tests consequential"),
    ("concept_double_bind", "concept_dynamics_of_loops", "explains", "conceptual", "describes a self-reinforcing communicative form within"),
    ("intervention_skill_productive_conversations", "concept_double_bind", "applies", "practice", "can surface contradictory demands described as"),
    ("concept_double_bind", "person_gregory_bateson", "formulated_by", "historical", "was formulated in the research associated with"),
    ("concept_feedforward", "concept_regulation", "explains", "conceptual", "provides an anticipatory mechanism for"),
    ("tradition_control_theory", "concept_feedforward", "uses", "practice", "uses anticipatory control through"),
    ("concept_feedforward", "concept_feedback", "complements", "conceptual", "acts in anticipation alongside corrective"),
    ("intervention_skill_fractal_enterprise_model_and_capabilities", "concept_fractals", "uses", "practice", "uses repeated form associated with"),
    ("practice_systems_practice", "concept_holism", "uses", "practice", "uses whole-and-part inquiry associated with"),
    ("approach_family_systems_change", "concept_identity", "uses", "practice", "learns about and may reframe"),
    ("practice_systems_convening", "concept_identity", "applies", "practice", "works across and sometimes reshapes"),
    ("tradition_cybernetics", "concept_information_theory", "uses", "practice", "draws on formal accounts from"),
    ("method_or_methodology_system_dynamics", "concept_positive_feedback", "uses", "practice", "models reinforcing behaviour through"),
    ("tradition_cybernetics", "concept_purposeful_behaviour", "uses", "practice", "developed early classifications of"),
    ("concept_purposeful_behaviour", "concept_purpose", "specialises", "conceptual", "locates observed action in relation to"),
    ("concept_recursive_computation", "concept_recursion", "formalises", "conceptual", "provides a computational form of"),
    ("concept_recursive_definition", "concept_recursion", "formalises", "conceptual", "provides a definitional form of"),
    ("concept_recursive_computation", "concept_recursive_definition", "complements", "conceptual", "provides an executable counterpart to"),
    ("tradition_chaos_theory", "concept_sensitive_dependence_on_initial_conditions", "uses", "practice", "studies trajectories shaped by"),
    ("tool_monitoring_and_evaluation_strategy", "concept_single_loop_learning", "uses", "practice", "can support corrective"),
    ("intervention_skill_iceberg_model", "concept_uncertainty", "complements", "conceptual", "should leave proposed deeper causes open to"),
    ("intervention_skill_ladder_of_inference", "concept_multiple_perspectives", "uses", "practice", "compares different selections and interpretations among"),
    ("knowledge_domain_systems_laws", "tradition_systems_theory", "complements", "conceptual", "collects propositions within the wider plurality of"),
    ("method_or_methodology_multi_methodology_including_sosm", "concept_boundary_critique", "uses", "practice", "selects and combines approaches with attention to"),
    ("method_or_methodology_multi_methodology_including_sosm", "method_or_methodology_systemic_intervention", "complements", "conceptual", "shares methodological pluralism with"),
    ("method_or_methodology_multi_methodology_including_sosm", "practice_systems_practice", "applies", "practice", "supports method choice within"),
    ("method_or_methodology_strategic_options_development_and_analysis_soda", "method_or_methodology_soft_systems_methodology_ssm", "complements", "conceptual", "offers a cognitive-mapping complement to"),
    ("tradition_control_theory", "technology_machine_governors", "uses", "practice", "has historical and practical roots in"),
    ("technology_machine_governors", "concept_feedback", "instantiates", "conceptual", "provides a physical historical instance of"),
    ("technology_machine_governors", "concept_regulation", "instantiates", "conceptual", "provides a physical historical instance of"),
    ("tool_behaviour_over_time_graphs", "concept_uncertainty", "complements", "conceptual", "requires explicit treatment of"),
    ("tool_identify_leverage", "concept_purpose", "complements", "conceptual", "depends on what change is judged desirable through"),
    ("tool_stock_and_flow_diagrams", "concept_modelling", "complements", "conceptual", "is a formal representational form of"),
    ("tradition_control_theory", "concept_feedback", "uses", "practice", "regulates behaviour through"),
    ("tradition_control_theory", "concept_regulation", "formalises", "conceptual", "offers mathematical accounts of"),
    ("tradition_control_theory", "method_or_methodology_system_dynamics", "complements", "conceptual", "shares dynamical and feedback concerns with"),
    ("tradition_evolutionary_cybernetics", "concept_adaptation", "uses", "practice", "examines selection and persistence through"),
    ("concept_global_brain", "concept_networks", "uses", "practice", "imagines distributed coordination across"),
    ("concept_global_brain", "concept_emergence", "explains", "conceptual", "is proposed as a large-scale form of"),
    ("concept_global_brain", "concept_metasystem_transition", "complements", "conceptual", "is often framed alongside"),
    ("tool_nodica", "concept_semantic_network", "uses", "practice", "represents explicitly typed knowledge as a"),
    ("tool_nodica", "tool_systems_mapping", "complements", "conceptual", "offers a semantic-graph complement to"),
    ("approach_family_metasystem_transition_theory", "concept_metasystem_transition", "uses", "practice", "organises its account around"),
    ("approach_family_metasystem_transition_theory", "tradition_evolutionary_cybernetics", "complements", "conceptual", "develops within and alongside"),
    ("approach_family_systems_change", "concept_leverage_points", "uses", "practice", "may orient intervention through"),
    ("practice_systems_practice", "concept_bounded_applicability", "applies", "practice", "states limits through"),
    ("method_or_methodology_estuarine_mapping", "tool_systems_mapping", "uses", "practice", "is a specialised form of"),
    ("method_or_methodology_distributed_ethnography", "concept_multiple_perspectives", "complements", "conceptual", "develops accounts across distributed"),
    ("approach_family_naturalising_sense_making", "concept_complexity", "uses", "practice", "frames decision contexts through"),
    ("approach_family_naturalising_sense_making", "concept_bounded_applicability", "complements", "conceptual", "emphasises contextual limits through"),
    ("corpus_coevolving_innovations", "approach_family_service_systems_thinking", "presents", "documentary", "documents work associated with"),
    ("corpus_systems_changes", "approach_family_systems_changes_learning", "presents", "documentary", "documents work associated with"),
    ("corpus_systems_changes", "approach_family_service_systems_thinking", "presents", "documentary", "documents a related practice lineage in"),
    ("approach_family_service_systems_thinking", "concept_purpose", "uses", "practice", "orients service inquiry through"),
    ("approach_family_systems_changes_learning", "concept_double_loop_learning", "uses", "practice", "supports learning about governing frames through"),
    ("approach_family_systems_changes_learning", "approach_family_systems_change", "complements", "conceptual", "adds an explicit learning orientation to"),
    ("concept_black_box", "concept_modelling", "uses", "practice", "supports selective inquiry through"),
]


def make_source_backed_edge(
    edge_id: str,
    source: str,
    target: str,
    relation_type: str,
    family: str,
    phrase: str,
    source_id: str,
    locator: str,
) -> dict[str, Any]:
    return {
        "id": edge_id,
        "source": source,
        "target": target,
        "relation_type": relation_type,
        "relation_family": family,
        "directed": "true",
        "dependency_kind": "",
        "confidence": "0.90",
        "claim_status": "provisional",
        "source_ids": enc([source_id]),
        "evidence_ids": "[]",
        "source_locator": locator,
        "valid_from": "",
        "valid_to": "",
        "scope_conditions": "This records an explicit connection in the named author material. It is an author synthesis, not evidence of field-wide consensus or intervention effectiveness; exact public wording awaits curator review.",
        "assertion_mode": "asserted",
        "inference_method": "direct reading of supplied author material",
        "claim_id": "",
        "reviewed_by": "",
        "reviewed_at": "",
        "notes": "",
        "plain_phrase": phrase,
        "public_review_label": "source-backed draft for author review",
    }


def make_crosswalk_edge(
    edge_id: str,
    source: str,
    target: str,
    relation_type: str,
    family: str,
    phrase: str,
    source_ids: list[str],
) -> dict[str, Any]:
    return {
        "id": edge_id,
        "source": source,
        "target": target,
        "relation_type": relation_type,
        "relation_family": family,
        "directed": "true",
        "dependency_kind": "",
        "confidence": "0.72",
        "claim_status": "provisional",
        "source_ids": enc(source_ids),
        "evidence_ids": "[]",
        "source_locator": "Interpretive comparison of the two maintained public descriptions and their cited source records",
        "valid_from": "",
        "valid_to": "",
        "scope_conditions": "This is a provisional semantic or practice crosswalk. It does not establish historical influence, equivalence, efficacy or universal applicability. Item-level source review and curator acceptance are still required.",
        "assertion_mode": "interpreted",
        "inference_method": "curator-requested relational crosswalk of maintained public descriptions",
        "claim_id": "",
        "reviewed_by": "",
        "reviewed_at": "",
        "notes": "",
        "plain_phrase": phrase,
        "public_review_label": "provisional relational crosswalk",
    }


def make_documentary_edge(edge_id: str, source: str, target: str, phrase: str, source_ids: list[str]) -> dict[str, Any]:
    return {
        "id": edge_id,
        "source": source,
        "target": target,
        "relation_type": "presents",
        "relation_family": "documentary",
        "directed": "true",
        "dependency_kind": "",
        "confidence": "0.98",
        "claim_status": "accepted",
        "source_ids": enc(source_ids),
        "evidence_ids": "[]",
        "source_locator": "Official collection table of contents",
        "valid_from": "",
        "valid_to": "",
        "scope_conditions": "This records documentary collection structure only. Inclusion does not by itself establish conceptual influence, agreement, importance or validity.",
        "assertion_mode": "asserted",
        "inference_method": "direct collection membership statement",
        "claim_id": "",
        "reviewed_by": "",
        "reviewed_at": "",
        "notes": "",
        "plain_phrase": phrase,
        "public_review_label": "source-backed contents statement",
    }


def source_ids_for(node_by_id: dict[str, dict[str, Any]], source: str, target: str) -> list[str]:
    return list(dict.fromkeys([
        *parse(node_by_id[source].get("source_ids"), []),
        *parse(node_by_id[target].get("source_ids"), []),
    ]))


def build_relational_edges(data: dict[str, Any]) -> list[dict[str, Any]]:
    node_by_id = {node["id"]: node for node in data["nodes"]}
    relation_types = {row["relation_type"] for row in data.get("relation_types", [])}
    incoming: list[dict[str, Any]] = []

    all_links = [
        *[(source, target, relation_type, family, phrase) for source, rows in PRACTICE_LINKS.items() for target, relation_type, family, phrase in rows],
        *GAP_LINKS,
        *SECOND_PASS_LINKS,
    ]
    endpoints = {item for row in all_links for item in row[:2]}
    endpoints.update(item for row in SOURCE_BACKED_LINKS for item in row[:2])
    missing = endpoints - set(node_by_id)
    if missing:
        raise SystemExit(f"Unknown relational-depth endpoint(s): {sorted(missing)}")
    redirected = endpoints & set(data.get("canonical_redirects", {}))
    if redirected:
        raise SystemExit(f"Relational-depth endpoint(s) must be canonical: {sorted(redirected)}")
    unknown_relations = {row[2] for row in all_links} | {row[2] for row in SOURCE_BACKED_LINKS}
    unknown_relations -= relation_types
    if unknown_relations:
        raise SystemExit(f"Unknown relational-depth relation type(s): {sorted(unknown_relations)}")

    existing_signatures = {
        (edge.get("source"), edge.get("relation_type"), edge.get("target"))
        for edge in data.get("edges", [])
    }
    for index, (source, target, relation_type, family, phrase, source_id, locator) in enumerate(SOURCE_BACKED_LINKS, start=1):
        signature = (source, relation_type, target)
        if signature in existing_signatures:
            continue
        incoming.append(make_source_backed_edge(
            f"e16_source_crosswalk_{index:03d}", source, target, relation_type, family, phrase, source_id, locator
        ))
        existing_signatures.add(signature)

    for index, (source, target, relation_type, family, phrase) in enumerate(all_links, start=1):
        signature = (source, relation_type, target)
        if signature in existing_signatures:
            continue
        incoming.append(make_crosswalk_edge(
            f"e16_relational_crosswalk_{index:03d}",
            source,
            target,
            relation_type,
            family,
            phrase,
            source_ids_for(node_by_id, source, target),
        ))
        existing_signatures.add(signature)

    # Translate the already source-backed FPCS container membership into reader-facing
    # documentary sentences. The classification edges remain available in provenance.
    fpcs_memberships = [
        edge for edge in data.get("edges", [])
        if edge.get("relation_type") == "part_of"
        and str(edge.get("source", "")).startswith("publication_fpcs_")
        and (
            str(edge.get("target", "")).startswith("publication_fpcs_volume_")
            or edge.get("target") == "corpus_foundational_papers_2024"
        )
    ]
    for index, membership in enumerate(fpcs_memberships, start=1):
        source = membership["target"]
        target = membership["source"]
        signature = (source, "presents", target)
        if signature in existing_signatures:
            continue
        phrase = "presents as a constituent paper" if target.startswith("publication_fpcs_") and "volume" not in target else "presents as a constituent volume"
        incoming.append(make_documentary_edge(
            f"e16_fpcs_contents_{index:03d}",
            source,
            target,
            phrase,
            parse(membership.get("source_ids"), []) or ["src_fpcs_official_toc"],
        ))
        existing_signatures.add(signature)

    return incoming


def public_graph(data: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    redirects = data.get("canonical_redirects", {})
    public = {
        node["id"]: node
        for node in data.get("nodes", [])
        if node.get("public_visibility") == "public"
        and redirects.get(node["id"], node["id"]) == node["id"]
    }
    edges = [
        edge for edge in data.get("edges", [])
        if edge.get("source") in public and edge.get("target") in public
        and edge.get("source") != edge.get("target")
        and edge.get("relation_type") != "legacy_association_unspecified"
        and edge.get("claim_status") != "legacy_unresolved"
        and edge.get("relation_family") != "legacy"
    ]
    return public, edges


def calculate_relational_depth(data: dict[str, Any]) -> dict[str, Any]:
    public, edges = public_graph(data)
    visible_neighbours = {node_id: set() for node_id in public}
    reader_neighbours = {node_id: set() for node_id in public}
    semantic_neighbours = {node_id: set() for node_id in public}
    reader_families = {node_id: set() for node_id in public}
    visible_statements = Counter()
    reader_statements = Counter()
    semantic_statements = Counter()
    documentary_statements = Counter()
    accepted_reader_statements = Counter()
    provisional_reader_statements = Counter()

    for edge in edges:
        source, target = edge["source"], edge["target"]
        family = edge.get("relation_family", "")
        for node_id, other in ((source, target), (target, source)):
            visible_neighbours[node_id].add(other)
            visible_statements[node_id] += 1
            if family == "documentary":
                documentary_statements[node_id] += 1
            if family not in {"classification", "evidence"}:
                reader_neighbours[node_id].add(other)
                reader_families[node_id].add(family)
                reader_statements[node_id] += 1
                if edge.get("claim_status") in {"accepted", "corroborated"}:
                    accepted_reader_statements[node_id] += 1
                else:
                    provisional_reader_statements[node_id] += 1
            if family not in {"classification", "evidence", "documentary"}:
                semantic_neighbours[node_id].add(other)
                semantic_statements[node_id] += 1

    by_node: dict[str, dict[str, Any]] = {}
    band_counts = Counter()
    evidence_counts = Counter()
    by_type: dict[str, Counter] = defaultdict(Counter)
    for node_id, node in public.items():
        reader_count = len(reader_neighbours[node_id])
        family_count = len(reader_families[node_id])
        if reader_count == 0:
            band = "unconnected"
        elif reader_count >= 6 and family_count >= 3:
            band = "rich"
        elif reader_count >= 3 and family_count >= 2:
            band = "developing"
        else:
            band = "thin"

        accepted = accepted_reader_statements[node_id]
        provisional = provisional_reader_statements[node_id]
        if not reader_statements[node_id]:
            evidence_band = "none"
        elif accepted >= 3 and accepted >= provisional:
            evidence_band = "supported"
        elif accepted:
            evidence_band = "mixed"
        else:
            evidence_band = "provisional"

        by_node[node_id] = {
            "connection_band": band,
            "evidence_band": evidence_band,
            "visible_connections": len(visible_neighbours[node_id]),
            "visible_statements": visible_statements[node_id],
            "reader_connections": reader_count,
            "reader_statements": reader_statements[node_id],
            "semantic_connections": len(semantic_neighbours[node_id]),
            "semantic_statements": semantic_statements[node_id],
            "documentary_statements": documentary_statements[node_id],
            "accepted_reader_statements": accepted,
            "provisional_reader_statements": provisional,
            "distinct_reader_families": family_count,
            "reader_families": sorted(reader_families[node_id]),
        }
        band_counts[band] += 1
        evidence_counts[evidence_band] += 1
        by_type[node.get("entity_type", "unknown")][band] += 1
        by_type[node.get("entity_type", "unknown")]["total"] += 1

    band_order = {"unconnected": 0, "thin": 1, "developing": 2, "rich": 3}
    priority = sorted(
        public.values(),
        key=lambda node: (
            band_order[by_node[node["id"]]["connection_band"]],
            by_node[node["id"]]["reader_connections"],
            by_node[node["id"]]["distinct_reader_families"],
            0 if node.get("publication_level") == "profile" else 1,
            node.get("label", ""),
        ),
    )

    return {
        "release": RELEASE,
        "generated": GENERATED,
        "purpose": "Make relational breadth, multiplexity and evidential strength inspectable for every public entry.",
        "contract": {
            "visible_connection": "Any non-legacy typed statement between two canonical public entries.",
            "reader_connection": "A public typed statement excluding collection-only classification and evidence-registration lines; authorship and presentation remain visible.",
            "semantic_connection": "A reader connection excluding documentary authorship and presentation.",
            "rich": "At least six distinct reader neighbours across at least three relation families.",
            "developing": "At least three distinct reader neighbours across at least two relation families.",
            "thin": "At least one reader neighbour but below the developing threshold.",
            "unconnected": "No reader connection; classification or evidence registration alone does not count.",
            "evidence_note": "Structural depth and evidence depth are separate. Provisional crosswalks do not become accepted merely by increasing degree.",
        },
        "aggregate": {
            "public_entries": len(public),
            "visible_connected_entries": sum(bool(visible_neighbours[node_id]) for node_id in public),
            "reader_connected_entries": sum(bool(reader_neighbours[node_id]) for node_id in public),
            "semantic_connected_entries": sum(bool(semantic_neighbours[node_id]) for node_id in public),
            "connection_bands": dict(sorted(band_counts.items())),
            "evidence_bands": dict(sorted(evidence_counts.items())),
            "reader_statements": sum(1 for edge in edges if edge.get("relation_family") not in {"classification", "evidence"}),
            "semantic_statements": sum(1 for edge in edges if edge.get("relation_family") not in {"classification", "evidence", "documentary"}),
        },
        "by_entity_type": {
            entity_type: dict(sorted(counts.items()))
            for entity_type, counts in sorted(by_type.items())
        },
        "priority_queue": [
            {
                "node_id": node["id"],
                "label": node["label"],
                "entity_type": node.get("entity_type", "unknown"),
                "publication_level": node.get("publication_level", ""),
                **by_node[node["id"]],
            }
            for node in priority[:120]
        ],
        "by_node": by_node,
    }


def write_relational_document(data: dict[str, Any]) -> None:
    depth = data["relational_depth"]
    aggregate = depth["aggregate"]
    bands = aggregate["connection_bands"]
    evidence = aggregate["evidence_bands"]
    by_type = depth["by_entity_type"]
    priority = depth["priority_queue"]
    lines = [
        "# Relational depth programme",
        "",
        f"Release: `{RELEASE}`  ",
        f"Generated: `{GENERATED}`",
        "",
        "## The outcome",
        "",
        "The atlas now treats relational richness as maintained data, not a visual impression. Every canonical public entry has a structural connection band and a separate evidence band. This makes it possible to add provisional routes without pretending that repetition, plausibility or graph density is proof.",
        "",
        f"- {aggregate['reader_connected_entries']} of {aggregate['public_entries']} entries have at least one reader connection.",
        f"- {bands.get('rich', 0)} are structurally rich, {bands.get('developing', 0)} developing, {bands.get('thin', 0)} thin and {bands.get('unconnected', 0)} unconnected.",
        f"- {aggregate['semantic_connected_entries']} have at least one non-documentary semantic, historical, human, identity, practice, influence or contestation route.",
        f"- Evidence is {evidence.get('supported', 0)} supported, {evidence.get('mixed', 0)} mixed, {evidence.get('provisional', 0)} provisional and {evidence.get('none', 0)} absent at entry level.",
        "",
        "## What counts",
        "",
        "A reader connection is a typed public statement which is more than collection membership or evidence registration. Authorship and presentation remain because they are meaningful ways into a publication or corpus. A semantic connection excludes those documentary lines as well.",
        "",
        "Structural bands:",
        "",
        "- **Rich:** at least six distinct reader neighbours across at least three relation families.",
        "- **Developing:** at least three distinct reader neighbours across at least two families.",
        "- **Thin:** at least one reader neighbour, below the developing threshold.",
        "- **Unconnected:** no reader connection. Classification and evidence registration alone do not rescue an entry.",
        "",
        "## The required shape by entity",
        "",
        "| Entry kind | Connections expected before it is genuinely rich |",
        "| --- | --- |",
        "| Concept or principle | definition or prerequisite; contrast or confusion; historical formulation; method/tool use; practice consequence; critique or scope limit |",
        "| Person | authored works; institutions and events; teachers, collaborators or students; explicit influences; traditions or identity; practice transmission; controversy where evidenced |",
        "| Method or methodology | conceptual foundations; component tools; neighbouring or contrasting methods; documented uses and cases; originators and texts; limits or critique |",
        "| Intervention skill or tool | purpose and inputs; concepts used; method or practice context; combinations; outputs or observable consequences; boundary conditions and risks |",
        "| Publication or corpus | authors/editors; works contained or cited; ideas presented; historical reception; methods or practice influenced; critiques or disputes |",
        "| Institution or event | people; publications; teaching and practice transmission; collaborations; place and time; successor/predecessor relations |",
        "",
        "The template is an editorial checklist, not an invitation to fill six slots with weak claims. Missing relation families should stay visibly missing until there is evidence.",
        "",
        "## Current bands by entity type",
        "",
        "| Entity type | Total | Rich | Developing | Thin | Unconnected |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for entity_type, counts in by_type.items():
        lines.append(
            f"| {entity_type.replace('_', ' ')} | {counts.get('total', 0)} | {counts.get('rich', 0)} | {counts.get('developing', 0)} | {counts.get('thin', 0)} | {counts.get('unconnected', 0)} |"
        )
    lines.extend([
        "",
        "## How enrichment proceeds",
        "",
        "1. Select the highest-priority thin cohort by entity type, not whichever famous nodes are easiest.",
        "2. Use the entity template to look for missing relation families.",
        "3. Write each proposed line as a sentence with source, target, type, direction, ordinary-language phrase, locator, scope and status.",
        "4. Mark interpretive crosswalks provisional. Do not infer influence, teaching or equivalence from resemblance.",
        "5. Review the cohort with a named curator or domain steward; accept, revise, dispute or remove each line.",
        "6. Recalculate depth, publish the remaining queue and repeat. Community detection comes after enough typed signal exists.",
        "",
        "## First priority queue",
        "",
        "The queue below is generated from current structure. Low degree and low relation-family diversity come first; it is a work queue, not a ranking of intellectual importance.",
        "",
        "| Entry | Type | Structure | Evidence | Reader neighbours | Families |",
        "| --- | --- | --- | --- | ---: | ---: |",
    ])
    for item in priority[:50]:
        lines.append(
            f"| {item['label'].replace('|', '\\|')} | {item['entity_type'].replace('_', ' ')} | {item['connection_band']} | {item['evidence_band']} | {item['reader_connections']} | {item['distinct_reader_families']} |"
        )
    lines.extend([
        "",
        "## First enrichment cohort in this release",
        "",
        "This release adds typed provisional crosswalks for every SCiO intervention-skill entry; gives the previously reader-isolated concepts, methods, tools and traditions multiple routes into the maintained graph; exposes the Foundational Papers volume contents as documentary statements; connects the Cynefin wiki to its maintaining organisation and the material it presents; and adds slide-level statements from the supplied transformation, convening, organisational-dynamics, VSM, clarity and conversation material.",
        "",
        "These additions improve navigability immediately. They do not complete historical influence, human transmission, institutional history, field-level controversy or case evidence. Those remain the most important missing layers in the original-vision audit.",
        "",
    ])
    RELATIONAL_DOC.write_text("\n".join(lines), encoding="utf-8")


def write_data(data: dict[str, Any]) -> None:
    rendered = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    DATA_PATH.write_text(rendered, encoding="utf-8")
    (DOCS_ASSETS / "public-data.json").write_text(rendered, encoding="utf-8")
    (DOCS_ASSETS / "public-data.js").write_text(
        "window.TANGLE_DATA = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n",
        encoding="utf-8",
    )


def main() -> None:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    upsert(data["sources"], SOURCE_RECORDS, "id")
    generated_prefixes = (
        "e16_relational_crosswalk_",
        "e16_source_crosswalk_",
        "e16_fpcs_contents_",
    )
    data["edges"] = [
        edge for edge in data.get("edges", [])
        if not str(edge.get("id", "")).startswith(generated_prefixes)
    ]
    incoming = build_relational_edges(data)
    upsert(data["edges"], incoming, "id")
    depth = calculate_relational_depth(data)
    data["relational_depth"] = depth
    data["graph_snapshot"] = calculate_graph_snapshot(data)

    metrics = graph_metrics(data)
    meta = data["meta"]
    old_public_url = "https://antlerboy.github.io/the-necessary-tangle/"
    for key, value in list(meta.items()):
        if isinstance(value, str):
            meta[key] = value.replace(old_public_url, "https://transduction.systems/")
    aggregate = depth["aggregate"]
    meta.update({
        "release": RELEASE,
        "generated": GENERATED,
        "project_url": "https://transduction.systems/",
        "reading_list_inventory_url": "https://transduction.systems/reading-list.html",
        "iteration_focus": "Grammar and graph-wide relational depth: visible, typed, evidence-status-aware connections plus presentation repair",
        "node_count": len(data.get("nodes", [])),
        "edge_count": len(data.get("edges", [])),
        "source_count": len(data.get("sources", [])),
        "claim_count": len(data.get("claims", [])),
        "evidence_count": len(data.get("evidence", [])),
        "public_link_source_count": sum(source.get("public_link_status") == "public_link" for source in data.get("sources", [])),
        "no_public_link_source_count": sum(source.get("public_link_status") == "no_public_link" for source in data.get("sources", [])),
        "relational_crosswalk_connection_count": sum(
            str(edge.get("id", "")).startswith("e16_relational_crosswalk_") for edge in data.get("edges", [])
        ),
        "source_backed_author_link_count": sum(
            str(edge.get("id", "")).startswith("e16_source_crosswalk_") for edge in data.get("edges", [])
        ),
        "reader_connected_entry_count": aggregate["reader_connected_entries"],
        "semantic_connected_entry_count": aggregate["semantic_connected_entries"],
        "rich_entry_count": aggregate["connection_bands"].get("rich", 0),
        "developing_entry_count": aggregate["connection_bands"].get("developing", 0),
        "thin_entry_count": aggregate["connection_bands"].get("thin", 0),
        "unconnected_entry_count": aggregate["connection_bands"].get("unconnected", 0),
        "relational_depth_url": "https://github.com/antlerboy/the-necessary-tangle/blob/main/documentation/relational-depth.md",
    })
    if data.get("reading_list_inventory"):
        report = make_observations(data, data["reading_list_inventory"])
        report["release"] = RELEASE
        report["generated"] = GENERATED
        report["metrics"] = metrics
        data["ai_observations"] = report

    write_data(data)
    write_relational_document(data)
    if data.get("ai_observations"):
        write_ai_document(data["ai_observations"])
    print(json.dumps({
        "release": RELEASE,
        "new_relational_statements": len(incoming),
        "reader_connected_entries": aggregate["reader_connected_entries"],
        "connection_bands": aggregate["connection_bands"],
        "evidence_bands": aggregate["evidence_bands"],
    }, indent=2))


if __name__ == "__main__":
    main()
