#!/usr/bin/env python3
"""Apply release 0.10: clearer systems-work distinctions and publication controls."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from apply_iteration_09 import graph_metrics, make_ai_observations

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "public-data.json"
DOCS_ASSETS = ROOT / "docs" / "assets"
DOCUMENTATION = ROOT / "documentation"
RELEASE = "0.10-practice-safety-alpha"
GENERATED = "2026-08-10"

NEW_SOURCES: list[dict[str, Any]] = [
    {
        "id": "src_taylor_systems_leadership_schema_2021",
        "title": "A schema for better understanding systems leadership and systems change",
        "source_type": "public_curator_article",
        "quality_tier": "B",
        "access": "public",
        "url": "https://stream.syscoi.com/2021/06/21/a-schema-for-better-understanding-systems-leadership-and-systems-change/",
        "date": "2021-06-21",
        "notes": "Benjamin P Taylor's public working classification of six forms of systems leadership and its overlap with systems change. It is used as an explicit curatorial account, not as field-wide consensus.",
        "creators": "[\"Benjamin P Taylor\"]",
        "doi": "",
        "isbn": "",
        "publisher": "Systems Community of Inquiry",
        "licence": "source_terms",
        "archived_url": "",
        "content_hash": "",
        "review_status": "checked",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_taylor_systems_terms_2022",
        "title": "What do systems leadership and systems change mean to you?",
        "source_type": "public_curator_article",
        "quality_tier": "B",
        "access": "public",
        "url": "https://chosen-path.org/2022/07/11/what-do-systems-leadership-and-systems-change-mean-to-you-what-questions-would-you-like-me-to-answer/",
        "date": "2022-07-11",
        "notes": "A public statement of Benjamin P Taylor's distinctions among systems leadership, systems change, systems theory, systems practice and systems convening. It is treated as a curatorial framing open to challenge.",
        "creators": "[\"Benjamin P Taylor\"]",
        "doi": "",
        "isbn": "",
        "publisher": "chosen path",
        "licence": "source_terms",
        "archived_url": "",
        "content_hash": "",
        "review_status": "checked",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_wenger_trayner_systems_convening",
        "title": "Systems convening: the art of convening diverse voices across difficult boundaries",
        "source_type": "primary_author_page",
        "quality_tier": "A",
        "access": "public",
        "url": "https://www.wenger-trayner.com/systems-convening/",
        "date": "",
        "notes": "Primary public account by Beverly and Etienne Wenger-Trayner of systems convening as social-learning leadership across boundaries. Their FAQ explicitly says the work did not spring from systems theory.",
        "creators": "[\"Beverly Wenger-Trayner\", \"Etienne Wenger-Trayner\"]",
        "doi": "",
        "isbn": "",
        "publisher": "Wenger-Trayner",
        "licence": "CC 4.0 source terms",
        "archived_url": "",
        "content_hash": "",
        "review_status": "checked",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_scio_professional_body_current",
        "title": "What is SCiO?",
        "source_type": "official_professional_body_page",
        "quality_tier": "A",
        "access": "public",
        "url": "https://www.systemspractice.org/professional-body",
        "date": "",
        "notes": "Official SCiO account of its role, competency framework, professional standards and support for systems practitioners.",
        "creators": "[\"SCiO - Systems and Complexity in Organisation\"]",
        "doi": "",
        "isbn": "",
        "publisher": "SCiO",
        "licence": "source_terms",
        "archived_url": "",
        "content_hash": "",
        "review_status": "checked",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_scio_professional_development_current",
        "title": "SCiO Professional Development",
        "source_type": "official_training_page",
        "quality_tier": "A",
        "access": "public",
        "url": "https://www.systemspractice.org/professional-development",
        "date": "",
        "notes": "Official SCiO page describing systems-practice and intervention training, delivery formats and the relationship between methods and intervention skills.",
        "creators": "[\"SCiO - Systems and Complexity in Organisation\"]",
        "doi": "",
        "isbn": "",
        "publisher": "SCiO",
        "licence": "source_terms",
        "archived_url": "",
        "content_hash": "",
        "review_status": "checked",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_network_weaver_current",
        "title": "Network Weaving",
        "source_type": "official_practice_resource_page",
        "quality_tier": "B",
        "access": "public",
        "url": "https://networkweaver.com/network-weaving/",
        "date": "",
        "notes": "Public orientation to network weaving and the Network Weaver resource library. It supports the network-building meaning of weaving; it is not evidence that all uses of 'systems weaving' share one definition.",
        "creators": "[\"Network Weaver\"]",
        "doi": "",
        "isbn": "",
        "publisher": "Network Weaver",
        "licence": "source_terms",
        "archived_url": "",
        "content_hash": "",
        "review_status": "checked",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_taylor_reading_list_current",
        "title": "Benjamin P Taylor's systems | complexity | cybernetics reading list",
        "source_type": "public_curated_reading_list",
        "quality_tier": "C",
        "access": "public",
        "url": "https://www.antlerboy.com/reading-list",
        "date": "",
        "notes": "Benjamin P Taylor's public, deliberately partial reading list. It is an orientation and discovery source, not a neutral or exhaustive canon.",
        "creators": "[\"Benjamin P Taylor\"]",
        "doi": "",
        "isbn": "",
        "publisher": "antlerboy.com",
        "licence": "source_terms",
        "archived_url": "",
        "content_hash": "",
        "review_status": "checked",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
]

NODE_SPECS = [
    {
        "id": "approach_family_systems_leadership",
        "label": "Systems leadership",
        "entity_type": "approach_family",
        "description": "An overloaded family of approaches ranging from leading an institutional 'system' more effectively, through creating more legitimate authority, to helping people develop new ways of organising. The phrase does not by itself specify the system, the leadership relation or whose purposes count.",
        "source_ids": ["src_taylor_systems_leadership_schema_2021", "src_taylor_systems_terms_2022", "src_scio_professional_body_current"],
        "x": -0.10,
        "y": 0.36,
    },
    {
        "id": "approach_family_systems_change",
        "label": "Systems change",
        "entity_type": "approach_family",
        "description": "An overloaded family of practices concerned with altering patterns, structures, relations, purposes or conditions across a system of concern. Systems are already changing, so the phrase needs a boundary, direction, account of agency, legitimacy and theory of change.",
        "source_ids": ["src_taylor_systems_leadership_schema_2021", "src_taylor_systems_terms_2022", "src_taylor_boundaries_convening_2025"],
        "x": -0.04,
        "y": 0.38,
    },
    {
        "id": "tradition_systems_theory",
        "label": "Systems theory",
        "entity_type": "tradition",
        "description": "A family of explanatory traditions concerned with systems, wholes, relations, organisation, feedback, boundaries, emergence and related phenomena. It is not one unified theory and does not automatically supply a method for intervention.",
        "source_ids": ["src_scio_sysbok_current", "src_scio_professional_body_current", "src_taylor_systems_terms_2022"],
        "x": 0.02,
        "y": 0.34,
    },
    {
        "id": "practice_systems_practice",
        "label": "Systems practice",
        "entity_type": "practice",
        "description": "The situated use of systems ideas, methods and judgement to inquire and act in a problematic situation. It includes choosing boundaries, combining approaches, learning from consequences and allowing the inquiry to change the practitioner as well as the situation.",
        "source_ids": ["src_scio_professional_body_current", "src_scio_professional_development_current", "src_scio_accreditation_current", "src_taylor_systems_terms_2022"],
        "x": 0.08,
        "y": 0.39,
    },
    {
        "id": "practice_systems_convening",
        "label": "Systems convening",
        "entity_type": "practice",
        "description": "Social-learning leadership that creates and sustains learning across boundaries in a social landscape. It need not derive from systems theory and is not a general synonym for partnership working, facilitation or institutional coordination.",
        "source_ids": ["src_wenger_trayner_systems_convening", "src_taylor_boundaries_convening_2025", "src_taylor_systems_terms_2022"],
        "x": 0.14,
        "y": 0.36,
    },
    {
        "id": "practice_systems_weaving",
        "label": "Systems weaving",
        "entity_type": "practice",
        "description": "Relational and network-building work that notices, connects and strengthens people, groups and resources so new collaboration and self-organisation become possible. It overlaps with systems convening but usually puts more emphasis on network health and connection.",
        "source_ids": ["src_network_weaver_current", "src_taylor_systems_terms_2022", "src_taylor_boundaries_convening_2025"],
        "x": 0.20,
        "y": 0.40,
    },
]

PROFILE_SPECS: dict[str, dict[str, Any]] = {
    "approach_family_systems_leadership": {
        "summary": "Systems leadership is not one approach. It can mean better leadership of a set of institutions, better systems thinking by leaders, more legitimate shared authority, facilitation of system development, or support for new possibilities. These aims can conflict.",
        "why_it_matters": "The label often creates false agreement. People may support 'systems leadership' while imagining very different distributions of authority, legitimacy, accountability and control.",
        "key_distinctions": [
            "leadership of an institutional system vs leadership informed by systems thinking",
            "improving system effectiveness vs challenging the legitimacy of existing power",
            "leading change vs helping a system explore and develop itself",
            "formal authority vs influence without authority",
        ],
        "historical_lineage": [
            "public-service partnership and place leadership",
            "systems thinking and organisational cybernetics",
            "collective, adaptive and facilitative leadership traditions",
            "systems-change movements and social innovation",
        ],
        "logical_antecedents": ["Boundary", "Purpose", "Power", "Legitimacy", "Systems practice"],
        "dependent_subsequents": ["Shared governance", "Place leadership", "Collective action", "Systems change"],
        "practice_connections": [
            "state which system and purposes are in focus",
            "make authority and accountability explicit",
            "distinguish coordination from genuine redistribution of power",
            "test effectiveness and legitimacy together",
        ],
        "common_misreadings": [
            "that adding 'systems' makes ordinary leadership systemic",
            "that collaboration removes conflict or hierarchy",
            "that one leader can stand outside and lead the whole system",
            "that all six meanings point in the same direction",
        ],
        "open_checks": [
            "develop rival classifications and international usage",
            "add cases where systems leadership improved coordination but damaged legitimacy, and vice versa",
        ],
        "source_ids": ["src_taylor_systems_leadership_schema_2021", "src_taylor_systems_terms_2022", "src_scio_professional_body_current"],
    },
    "approach_family_systems_change": {
        "summary": "Systems change is a family name for efforts to alter enduring patterns, relations, structures, purposes or conditions across a system of concern. The system, the desired direction and the authority to judge improvement must be stated rather than smuggled in.",
        "why_it_matters": "The phrase can reify 'the system' as a concrete object waiting to be redesigned. It can also hide the fact that systems are always changing and that deliberate intervention is only one source of change.",
        "key_distinctions": [
            "change in a system vs changing a system of concern",
            "system improvement vs changes in legitimacy or purpose",
            "planned intervention vs emergence and cultural evolution",
            "integration of fragmentation vs replacement with a new order",
        ],
        "historical_lineage": [
            "organisation development and planned change",
            "systems practice and systemic intervention",
            "social innovation and movement traditions",
            "complexity-informed accounts of emergence and adaptation",
        ],
        "logical_antecedents": ["Boundary", "Purpose", "Intervention", "Learning", "Power"],
        "dependent_subsequents": ["System development", "Transformation", "Institutional change", "Cultural evolution"],
        "practice_connections": [
            "name the current and desired patterns without pretending either is complete",
            "identify who can act and who bears the effects",
            "treat interventions as probes which generate learning",
            "track unintended and cross-level consequences",
        ],
        "common_misreadings": [
            "that a system is static before a programme changes it",
            "that a map identifies a controllable whole",
            "that beneficial intention establishes beneficial consequence",
            "that scale alone makes change systemic",
        ],
        "open_checks": [
            "compare systems-change schools by ontology, power and intervention logic",
            "build cases of failed and counterproductive systems change",
        ],
        "source_ids": ["src_taylor_systems_leadership_schema_2021", "src_taylor_systems_terms_2022", "src_taylor_boundaries_convening_2025"],
    },
    "tradition_systems_theory": {
        "summary": "Systems theory is better read as a contested family of theories than as a single doctrine. Different traditions explain organisation, relation, boundary, feedback, emergence, hierarchy, viability or communication in materially different ways.",
        "why_it_matters": "Practice becomes muddled when a broad theoretical vocabulary is treated as one agreed worldview, or when explanatory models are converted into prescriptions without showing the translation.",
        "key_distinctions": [
            "one theory vs a family of traditions",
            "explanation vs intervention method",
            "formal, biological, social and organisational domains",
            "first-order modelling vs reflexive and second-order accounts",
        ],
        "historical_lineage": [
            "general systems theory",
            "cybernetics and information",
            "operations research and systems engineering",
            "complexity, autopoiesis and second-order cybernetics",
        ],
        "logical_antecedents": ["Relation", "Organisation", "Boundary", "Observer"],
        "dependent_subsequents": ["Systems methods", "Systems practice", "Systems science", "Cybersystemics"],
        "practice_connections": [
            "say which theoretical tradition is being used",
            "state the domain and limits of analogy",
            "show the move from explanation to action",
            "retain rival accounts where the field is not settled",
        ],
        "common_misreadings": [
            "that all systems theories are compatible",
            "that theory automatically provides a method",
            "that using system language removes observer dependence",
            "that a formal model supplies its own purpose and ethics",
        ],
        "open_checks": [
            "develop a comparative history of major systems-theory traditions",
            "map incompatible uses of system, organisation, information and complexity",
        ],
        "source_ids": ["src_scio_sysbok_current", "src_scio_professional_body_current", "src_taylor_systems_terms_2022"],
    },
    "practice_systems_practice": {
        "summary": "Systems practice is inquiry and action under conditions where boundary, purpose, method, evidence and the practitioner's own participation matter. It is not the mechanical application of a systems diagram or named methodology.",
        "why_it_matters": "The field is often presented as a tool catalogue. Practice requires judgement about framing, participation, power, method combination, consequences and learning in the actual situation.",
        "key_distinctions": [
            "practice vs possession of a tool",
            "method following vs methodological judgement",
            "mapping vs intervention",
            "technical competence vs ethical and reflexive capability",
        ],
        "historical_lineage": [
            "systems methodologies and operational research",
            "critical and soft systems traditions",
            "cybernetic management and organisational learning",
            "professional standards and apprenticeship practice",
        ],
        "logical_antecedents": ["Systems theory", "Boundary", "Purpose", "Observer", "Learning"],
        "dependent_subsequents": ["Systemic intervention", "Multi-methodology", "Reflective practice", "Professional capability"],
        "practice_connections": [
            "work with at least several approaches and know their limits",
            "choose scope, scale and participation explicitly",
            "make reasoning and evidence inspectable",
            "learn from the consequences of intervention",
        ],
        "common_misreadings": [
            "that systems practice is simply systems mapping",
            "that the practitioner can remain outside the situation",
            "that more tools create better judgement",
            "that professionalisation removes contest and uncertainty",
        ],
        "open_checks": [
            "connect capability statements to documented cases and failure modes",
            "compare professional standards with practitioner-defined accounts of good work",
        ],
        "source_ids": ["src_scio_professional_body_current", "src_scio_professional_development_current", "src_scio_accreditation_current", "src_taylor_systems_terms_2022"],
    },
    "practice_systems_convening": {
        "summary": "Systems convening is social-learning leadership across boundaries. Conveners create new conversations and learning partnerships across a landscape, working with legitimacy, identity, agency, power and value creation.",
        "why_it_matters": "It names work that is often real but invisible. It also needs protection from becoming a loose synonym for any cross-organisational meeting, network or partnership role.",
        "key_distinctions": [
            "learning capability across a landscape vs competence inside one group",
            "convening legitimacy vs formal authority",
            "creating conditions for learning vs directing an agreed programme",
            "systems convening vs systems theory or a systems methodology",
        ],
        "historical_lineage": [
            "social learning theory",
            "communities and landscapes of practice",
            "boundary crossing and brokerage",
            "practitioner accounts of cross-system change",
        ],
        "logical_antecedents": ["Boundary", "Social learning", "Legitimacy", "Identity", "Power"],
        "dependent_subsequents": ["Cross-boundary learning", "New partnerships", "Agency", "Practice change"],
        "practice_connections": [
            "craft a convening call",
            "grow legitimacy across different worlds",
            "work with boundaries, identity, agency and power",
            "articulate value without claiming to control the result",
        ],
        "common_misreadings": [
            "that it is any form of facilitation or partnership working",
            "that it requires training in systems theory",
            "that convening is politically neutral",
            "that bringing everyone together guarantees agreement",
        ],
        "open_checks": [
            "map cases where systems convening failed or lost legitimacy",
            "compare systems convening with network weaving, brokerage and collective-impact roles",
        ],
        "source_ids": ["src_wenger_trayner_systems_convening", "src_taylor_boundaries_convening_2025", "src_taylor_systems_terms_2022"],
    },
    "practice_systems_weaving": {
        "summary": "Systems weaving is used here for practical work which strengthens relationships, closes useful triangles, connects resources and helps networks become more capable of self-organisation and coordinated action.",
        "why_it_matters": "It brings attention to the relational infrastructure of change. The term is less standardised than network weaving and can easily become decorative language unless the actual connections and effects are shown.",
        "key_distinctions": [
            "network health vs one-off stakeholder engagement",
            "connection and brokerage vs formal coordination",
            "weaving vs convening a specific learning space",
            "enabling self-organisation vs centrally directing a network",
        ],
        "historical_lineage": [
            "network weaving and community network practice",
            "social-capital and brokerage traditions",
            "movement and ecosystem organising",
            "systems-change practice",
        ],
        "logical_antecedents": ["Networks", "Relation", "Trust", "Agency"],
        "dependent_subsequents": ["Collaboration", "Self-organisation", "Network leadership", "Collective action"],
        "practice_connections": [
            "notice disconnected people and resources",
            "make strategic introductions and close triangles",
            "support shared infrastructure and communication",
            "watch who remains excluded from the network",
        ],
        "common_misreadings": [
            "that more connections are always better",
            "that a visible network has no power centre",
            "that weaving is a substitute for purpose or accountability",
            "that systems weaving has one settled definition",
        ],
        "open_checks": [
            "clarify how practitioners distinguish systems weaving from network weaving",
            "add evidence on network overload, exclusion and brokerage power",
        ],
        "source_ids": ["src_network_weaver_current", "src_taylor_systems_terms_2022", "src_taylor_boundaries_convening_2025"],
    },
}

JOURNEY = {
    "id": "journey_six_systems_things",
    "title": "Six systems things which are not the same thing",
    "subtitle": "Theory, practice, leadership, change, convening and weaving",
    "summary": "A short route through six terms which are routinely collapsed into one agreeable blur.",
    "audience": "practitioner, commissioner and systems-curious reader",
    "duration_minutes": 14,
    "steps": [
        ("Systems theory", "Begin with explanation", "Systems theory names a family of explanatory traditions. It does not arrive as one doctrine and does not choose a purpose or intervention for you."),
        ("Systems practice", "Move into situated action", "Practice is the work of choosing boundaries, methods and participation in context, then learning from what the intervention does to the situation and to the practitioner."),
        ("Systems leadership", "Ask what sort of authority is being exercised", "The phrase may mean better coordination, better systems thinking by leaders, changed authority, facilitative development or support for new possibilities. Those are not interchangeable."),
        ("Systems change", "Make the desired change and its legitimacy explicit", "Systems are already changing. A systems-change claim needs to say which patterns matter, who can act, who judges improvement and who bears the effects."),
        ("Systems convening", "Build learning across boundaries", "Systems convening comes from social learning. It creates new conversations across a landscape and works with legitimacy, identity, agency and power."),
        ("Systems weaving", "Strengthen the relational infrastructure", "Systems weaving connects people, groups and resources so networks become more capable. It overlaps with convening but is not identical to it."),
    ],
}

PUBLICATION_CONTROLS = [
    {
        "id": "public_only_payload",
        "label": "Public-only release payload",
        "description": "The generated website and data exclude private research URLs and private extracts. Private material may identify leads but cannot enter the public release by assertion.",
    },
    {
        "id": "source_level_provenance",
        "label": "Source-level provenance",
        "description": "Entries and connections retain source IDs, status and wording so bibliography, interpretation and evidence are not silently collapsed.",
    },
    {
        "id": "automated_release_scan",
        "label": "Automated release scan",
        "description": "Validation checks public files for private-path patterns, credentials, unsafe notebook links, stale counts and missing provenance before publication.",
    },
    {
        "id": "curator_release_control",
        "label": "Curator-controlled release",
        "description": "Contributors and tools may propose changes through issues and pull requests. Benjamin P Taylor remains responsible for accepting and publishing releases.",
    },
    {
        "id": "licence_boundary",
        "label": "Licence boundary",
        "description": "Original atlas material is licensed separately from third-party sources. Public availability is not treated as permission to republish a work.",
    },
    {
        "id": "versioned_backup",
        "label": "Versioned validation and backup",
        "description": "Every public release is built from versioned sources, validated, deployed through GitHub Pages and accompanied by a content backup with checksum.",
    },
]


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


def encode(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False)


def fold(value: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", value.casefold())).strip()


def upsert_sources(existing: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_id = {item["id"]: dict(item) for item in existing if item.get("id")}
    by_url = {
        str(item.get("url") or "").rstrip("/"): item["id"]
        for item in existing if item.get("id") and item.get("url")
    }
    for source in NEW_SOURCES:
        key = str(source.get("url") or "").rstrip("/")
        target_id = by_url.get(key) or source["id"]
        by_id[target_id] = {**by_id.get(target_id, {}), **source, "id": target_id}
        if key:
            by_url[key] = target_id
    return list(by_id.values())


def node_record(spec: dict[str, Any]) -> dict[str, Any]:
    source_ids = spec["source_ids"]
    return {
        "id": spec["id"],
        "label": spec["label"],
        "entity_type": spec["entity_type"],
        "description": spec["description"],
        "aliases": "[]",
        "boundary_ring": "0",
        "inclusion_reason": "planned_systems_work_distinctions",
        "status": "accepted",
        "source_ids": encode(source_ids),
        "set_tags": encode(["systems", "practice", "leadership", "release_0_10"]),
        "espoused_labels": "[]",
        "observed_clusters": "[]",
        "canonical_definition": "",
        "valid_from": "",
        "valid_to": "",
        "external_ids": "{}",
        "geographies": "[]",
        "licence": "",
        "review_status": "curator_checked_public_sources",
        "reviewed_by": "Benjamin P Taylor",
        "reviewed_at": GENERATED,
        "x": spec["x"],
        "y": spec["y"],
        "canonical_id": spec["id"],
        "public_visibility": "public",
        "publication_level": "profile",
        "public_stub_text": "",
        "public_source_count": len(source_ids),
        "no_public_link_count": sum(1 for source_id in source_ids if source_id == "src_taylor_boundaries_convening_2025"),
    }


def profile_record(node_id: str, spec: dict[str, Any]) -> dict[str, Any]:
    return {
        "node_id": node_id,
        "title": next(item["label"] for item in NODE_SPECS if item["id"] == node_id),
        "profile_status": "curator_checked_public_sources",
        "canonical_definition": next(item["description"] for item in NODE_SPECS if item["id"] == node_id),
        "summary": spec["summary"],
        "why_it_matters": spec["why_it_matters"],
        "key_distinctions": encode(spec["key_distinctions"]),
        "historical_lineage": encode(spec["historical_lineage"]),
        "logical_antecedents": encode(spec["logical_antecedents"]),
        "dependent_subsequents": encode(spec["dependent_subsequents"]),
        "practice_connections": encode(spec["practice_connections"]),
        "espoused_lineages": "[]",
        "observed_clusters": "[]",
        "common_misreadings": encode(spec["common_misreadings"]),
        "open_checks": encode(spec["open_checks"]),
        "source_ids": encode(spec["source_ids"]),
        "evidence_ids": "[]",
        "last_researched": GENERATED,
        "review_status": "curator_checked_public_sources",
        "reviewed_by": "Benjamin P Taylor",
        "reviewed_at": GENERATED,
        "editorial_note": "A developed working distinction for this release. The term remains contested and should be tested against rival usage and practice.",
    }


def edge_record(
    edge_id: str,
    source: str,
    target: str,
    relation_type: str,
    relation_family: str,
    phrase: str,
    source_ids: list[str],
    notes: str,
    directed: str = "true",
) -> dict[str, Any]:
    return {
        "id": edge_id,
        "source": source,
        "target": target,
        "relation_type": relation_type,
        "relation_family": relation_family,
        "directed": directed,
        "dependency_kind": "",
        "confidence": "0.86",
        "claim_status": "accepted",
        "source_ids": encode(source_ids),
        "evidence_ids": "[]",
        "source_locator": "Release 0.10 public systems-work distinctions",
        "valid_from": "",
        "valid_to": "",
        "scope_conditions": "Working distinction based on the named public sources and curator materials; rival usage remains admissible.",
        "assertion_mode": "asserted",
        "inference_method": "curatorial synthesis of public primary, professional-body and practitioner sources",
        "claim_id": "",
        "reviewed_by": "Benjamin P Taylor",
        "reviewed_at": GENERATED,
        "notes": notes,
        "plain_phrase": phrase,
        "public_review_label": "supported working distinction",
    }


def write_ai_documentation(data: dict[str, Any]) -> None:
    report = data["ai_observations"]
    metrics = report["metrics"]
    lines = [
        "# AI observations", "",
        f"Generated for release `{RELEASE}` on {GENERATED}.", "",
        report["method_note"], "",
        "## Measured state", "",
        f"- {metrics['public_entries']} public entries; {metrics['developed_profiles']} developed profiles.",
        f"- {metrics['typed_edges']} typed public edges; {metrics['substantive_edges']} substantive edges.",
        f"- {metrics['substantive_connected_nodes']} substantively connected entries and {metrics['substantive_isolated_nodes']} substantive isolates.",
        f"- {metrics['sources']} sources, of which {metrics['sources_with_public_links']} have public links.", "",
    ]
    for observation in report.get("observations", []):
        lines.extend([
            f"## {observation['title']}", "",
            f"**Basis:** {observation['kind']}.", "",
            f"**Measured:** {observation['measurement']}", "",
            f"**Interpretation:** {observation['interpretation']}", "",
            f"**Implication:** {observation['implication']}", "",
            f"**Test:** {observation['test']}", "",
        ])
    lines.extend([
        "## Publication controls", "",
        "The detailed working risk register is kept outside the public release. The public site exposes the controls which shape publication, not a catalogue of exploitable operational weaknesses.", "",
        "See [publication safety and controls](publication-safety.md).", "",
    ])
    (DOCUMENTATION / "ai-observations.md").write_text("\n".join(lines), encoding="utf-8")


def write_systems_distinctions() -> None:
    lines = [
        "# Six systems things which are not the same thing", "",
        "These are working distinctions. The point is not to freeze language but to stop six different kinds of work disappearing into one agreeable phrase.", "",
    ]
    for spec in NODE_SPECS:
        profile = PROFILE_SPECS[spec["id"]]
        lines.extend([
            f"## {spec['label']}", "",
            spec["description"], "",
            profile["summary"], "",
            "Key distinctions:", "",
            *[f"- {item}" for item in profile["key_distinctions"]],
            "",
        ])
    lines.extend([
        "## Read them together", "",
        "Systems theory helps explain. Systems practice turns explanation, method and judgement into situated inquiry and action. Systems leadership concerns authority and influence across some system of concern. Systems change concerns what patterns are to change, by whose agency and with what legitimacy. Systems convening develops learning across boundaries. Systems weaving strengthens the relational and network infrastructure through which collective action may become possible.", "",
        "The boundaries remain contestable. That is a reason to state them, not a reason to leave the words fused together.", "",
    ])
    (DOCUMENTATION / "six-systems-things.md").write_text("\n".join(lines), encoding="utf-8")


def write_publication_safety() -> None:
    lines = [
        "# Publication safety and controls", "",
        "The Necessary Tangle is public by design. Public inspectability improves challenge and provenance, while publication creates privacy, security, copyright, identity and reputational risks. The detailed working risk register is therefore maintained outside the public release. This page states the controls readers and contributors can rely on.", "",
    ]
    for item in PUBLICATION_CONTROLS:
        lines.extend([f"## {item['label']}", "", item["description"], ""])
    lines.extend([
        "## Reporting a problem", "",
        "Use the contribution route for ordinary corrections. Do not post credentials, private documents or sensitive personal information in a public issue. Security concerns should be reported through the repository security area rather than reproduced publicly.", "",
        "## Limits", "",
        "These controls reduce risk; they do not make public publication reversible. Forks, caches and downloaded copies may persist. The safest control remains not publishing material which should not become durable public information.", "",
    ])
    (DOCUMENTATION / "publication-safety.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    data["sources"] = upsert_sources(data.get("sources", []))

    nodes = {node["id"]: dict(node) for node in data.get("nodes", []) if node.get("id")}
    for spec in NODE_SPECS:
        nodes[spec["id"]] = {**nodes.get(spec["id"], {}), **node_record(spec)}
    data["nodes"] = list(nodes.values())

    profiles = {profile["node_id"]: dict(profile) for profile in data.get("profiles", []) if profile.get("node_id")}
    for node_id, spec in PROFILE_SPECS.items():
        profiles[node_id] = {**profiles.get(node_id, {}), **profile_record(node_id, spec)}
    data["profiles"] = list(profiles.values())

    label_to_id = {fold(node.get("label", "")): node_id for node_id, node in nodes.items()}
    required_labels = ["Boundary", "Purpose", "Adaptation", "Networks", "Systemic Intervention"]
    missing = [label for label in required_labels if fold(label) not in label_to_id]
    if missing:
        raise SystemExit(f"Iteration 0.10 cannot resolve required public entries: {missing}")

    def nid(label: str) -> str:
        return label_to_id[fold(label)]

    edges = {edge["id"]: dict(edge) for edge in data.get("edges", []) if edge.get("id")}
    for edge_id in [edge_id for edge_id in edges if edge_id.startswith("e_10_")]:
        del edges[edge_id]
    new_edges = [
        edge_record("e_10_leadership_change_confusion", "approach_family_systems_leadership", "approach_family_systems_change", "often_confused_with", "contestation", "is often confused with", ["src_taylor_systems_leadership_schema_2021", "src_taylor_systems_terms_2022"], "The public sources describe substantial overlap but distinguish leadership relations from the patterns or conditions being changed.", "false"),
        edge_record("e_10_leadership_uses_practice", "approach_family_systems_leadership", "practice_systems_practice", "uses", "practice", "uses", ["src_taylor_systems_terms_2022", "src_scio_professional_body_current"], "Systems leadership may use systems practice, but the leadership label alone does not establish competence in it."),
        edge_record("e_10_leadership_applies_boundary", "approach_family_systems_leadership", nid("Boundary"), "applies", "practice", "applies", ["src_taylor_systems_leadership_schema_2021"], "Any account of systems leadership selects a system boundary and distributes authority across it."),
        edge_record("e_10_leadership_applies_purpose", "approach_family_systems_leadership", nid("Purpose"), "applies", "practice", "applies", ["src_taylor_systems_leadership_schema_2021"], "Different purposes make different leadership problems and constituencies visible."),
        edge_record("e_10_change_uses_practice", "approach_family_systems_change", "practice_systems_practice", "uses", "practice", "uses", ["src_taylor_systems_terms_2022", "src_scio_professional_body_current"], "Systems-change work may use systems practice to inquire, intervene and learn rather than treating change as a pre-specified implementation."),
        edge_record("e_10_change_adaptation_confusion", "approach_family_systems_change", nid("Adaptation"), "often_confused_with", "contestation", "is often confused with", ["src_taylor_systems_terms_2022"], "Change is not automatically adaptive; adaptation is relative to an environment, timescale and viability condition.", "false"),
        edge_record("e_10_practice_uses_theory", "practice_systems_practice", "tradition_systems_theory", "uses", "practice", "uses", ["src_scio_professional_body_current", "src_scio_sysbok_current"], "Systems practice draws on several theoretical traditions rather than implementing one unified systems theory."),
        edge_record("e_10_practice_applies_boundary", "practice_systems_practice", nid("Boundary"), "applies", "practice", "applies", ["src_scio_accreditation_current", "src_taylor_systems_terms_2022"], "Choosing scope, scale, stakeholders and system levels is a core practical responsibility."),
        edge_record("e_10_practice_generalises_systemic_intervention", "practice_systems_practice", nid("Systemic Intervention"), "generalises", "conceptual", "is a broader form of", ["src_scio_professional_body_current", "src_midgley_systemic_intervention_2023"], "Systems practice is broader than the named Systemic Intervention methodology and may contain it among several approaches."),
        edge_record("e_10_convening_complements_practice", "practice_systems_convening", "practice_systems_practice", "complements", "conceptual", "complements", ["src_wenger_trayner_systems_convening", "src_taylor_systems_terms_2022"], "Systems convening and systems practice can reinforce one another, but systems convening arose from social learning rather than systems theory.", "false"),
        edge_record("e_10_convening_applies_boundary", "practice_systems_convening", nid("Boundary"), "applies", "practice", "applies", ["src_wenger_trayner_systems_convening", "src_taylor_boundaries_convening_2025"], "The primary account centres learning across persistent boundaries and the legitimacy to convene across them."),
        edge_record("e_10_convening_leadership_confusion", "practice_systems_convening", "approach_family_systems_leadership", "often_confused_with", "contestation", "is often confused with", ["src_wenger_trayner_systems_convening", "src_taylor_systems_leadership_schema_2021"], "Systems convening is one particular form of social-learning leadership, not a synonym for the entire systems-leadership family.", "false"),
        edge_record("e_10_weaving_complements_convening", "practice_systems_weaving", "practice_systems_convening", "complements", "conceptual", "complements", ["src_network_weaver_current", "src_wenger_trayner_systems_convening"], "Both work across relationships and boundaries; weaving emphasises network connection while convening emphasises learning capability across a landscape.", "false"),
        edge_record("e_10_weaving_applies_networks", "practice_systems_weaving", nid("Networks"), "applies", "practice", "applies", ["src_network_weaver_current"], "Network weaving works explicitly with the quality, diversity and pattern of connections in a network."),
        edge_record("e_10_weaving_combined_change", "practice_systems_weaving", "approach_family_systems_change", "commonly_combined_with", "practice", "commonly combined with", ["src_network_weaver_current", "src_taylor_systems_terms_2022"], "Weaving is often used in systems-change efforts as relational infrastructure, but it is not sufficient evidence of change by itself.", "false"),
    ]
    for edge in new_edges:
        edges[edge["id"]] = edge
    data["edges"] = list(edges.values())

    journey_steps = []
    for label, heading, narrative in JOURNEY["steps"]:
        key = fold(label)
        if key not in label_to_id:
            raise SystemExit(f"Journey cannot resolve {label}")
        journey_steps.append({"node_id": label_to_id[key], "heading": heading, "narrative": narrative})
    journeys = {journey["id"]: dict(journey) for journey in data.get("journeys", []) if journey.get("id")}
    journeys[JOURNEY["id"]] = {**{k: v for k, v in JOURNEY.items() if k != "steps"}, "steps": journey_steps}
    data["journeys"] = list(journeys.values())

    data["publication_controls"] = PUBLICATION_CONTROLS
    metrics = graph_metrics(data)
    report = make_ai_observations(metrics)
    report["release"] = RELEASE
    report.pop("public_risks", None)
    report["publication_controls"] = [item["id"] for item in PUBLICATION_CONTROLS]
    report["publication_controls_url"] = "https://github.com/antlerboy/the-necessary-tangle/blob/main/documentation/publication-safety.md"
    report["method_note"] = (
        "These observations combine reproducible counts from the public graph with model-assisted interpretation. "
        "Measurements, interpretations and proposed tests are kept separate. Detailed risk working notes are kept "
        "outside the public release; the public record shows the controls which govern publication."
    )
    data["ai_observations"] = report

    if data.get("expansion_08"):
        data["expansion_08"]["net_new_public_entries"] = 203
    meta = data.setdefault("meta", {})
    meta["expansion_08_added_count"] = 203
    meta.update({
        "release": RELEASE,
        "generated": GENERATED,
        "status": "public alpha on GitHub Pages",
        "iteration_focus": "systems-work distinctions, practice depth, public pathways and implemented publication controls",
        "publication_safety_url": "https://github.com/antlerboy/the-necessary-tangle/blob/main/documentation/publication-safety.md",
        "systems_distinctions_url": "https://antlerboy.github.io/the-necessary-tangle/#view=journeys&id=journey_six_systems_things&step=0",
        "syscoi_url": "https://www.syscoi.com/",
        "scio_capability_url": "https://www.systemspractice.org/professional-accreditation",
        "scio_training_url": "https://www.systemspractice.org/professional-development",
        "reading_list_url": "https://www.antlerboy.com/reading-list",
    })
    redirects = data.get("canonical_redirects", {})
    public_nodes = [
        node for node in data["nodes"]
        if node.get("public_visibility") == "public" and redirects.get(node["id"], node["id"]) == node["id"]
    ]
    public_ids = {node["id"] for node in public_nodes}
    meta["public_entry_count"] = len(public_nodes)
    meta["described_entry_count"] = len(public_nodes)
    meta["profile_count"] = len({profile["node_id"] for profile in data["profiles"] if profile.get("node_id") in public_ids})
    meta["journey_count"] = len(data["journeys"])
    meta["source_count"] = len(data["sources"])
    meta["public_link_source_count"] = sum(bool(source.get("url")) for source in data["sources"])
    meta["no_public_link_source_count"] = sum(not bool(source.get("url")) for source in data["sources"])
    meta["publication_control_count"] = len(PUBLICATION_CONTROLS)

    DOCUMENTATION.mkdir(parents=True, exist_ok=True)
    write_ai_documentation(data)
    write_systems_distinctions()
    write_publication_safety()
    risk_path = DOCUMENTATION / "publication-risks.md"
    if risk_path.exists():
        risk_path.unlink()

    rendered = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    DATA_PATH.write_text(rendered, encoding="utf-8")
    DOCS_ASSETS.mkdir(parents=True, exist_ok=True)
    (DOCS_ASSETS / "public-data.json").write_text(rendered, encoding="utf-8")
    (DOCS_ASSETS / "public-data.js").write_text(
        "window.TANGLE_DATA = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n",
        encoding="utf-8",
    )
    print(
        f"Applied {RELEASE}: {meta['public_entry_count']} entries, {meta['profile_count']} developed profiles, "
        f"{meta['journey_count']} journeys, {meta['source_count']} sources and {meta['publication_control_count']} publication controls."
    )


if __name__ == "__main__":
    main()
