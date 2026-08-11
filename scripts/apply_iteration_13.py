#!/usr/bin/env python3
"""Apply release 0.13: expertise-led depth, refreshed observations and clean public framing."""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

from apply_iteration_09 import graph_metrics

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "public-data.json"
DOCS_ASSETS = ROOT / "docs" / "assets"
DOCUMENTATION = ROOT / "documentation"
RELEASE = "0.13-expertise-observations-alpha"
GENERATED = "2026-08-11"


def enc(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False)


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


def fold(value: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", value.casefold())).strip()



RELATION_TYPE_UPSERTS: list[dict[str, str]] = [
    {"relation_type": "developed", "relation_family": "historical", "directed": "true", "inverse": "developed_by", "minimum_evidence": "Primary or official source identifying development", "strict_dependency": "no", "plain_phrase": "developed"},
    {"relation_type": "develops", "relation_family": "conceptual", "directed": "true", "inverse": "developed_in", "minimum_evidence": "Primary work or official description", "strict_dependency": "no", "plain_phrase": "develops"},
    {"relation_type": "explains", "relation_family": "conceptual", "directed": "true", "inverse": "explained_in", "minimum_evidence": "Primary work or official description", "strict_dependency": "no", "plain_phrase": "explains"},
    {"relation_type": "presents", "relation_family": "documentary", "directed": "true", "inverse": "presented_in", "minimum_evidence": "Official publication record or the work itself", "strict_dependency": "no", "plain_phrase": "presents"},
    {"relation_type": "edited_by", "relation_family": "documentary", "directed": "true", "inverse": "editor_of", "minimum_evidence": "Official publication record", "strict_dependency": "no", "plain_phrase": "edited by"},
    {"relation_type": "translates_for_practice", "relation_family": "practice", "directed": "true", "inverse": "translated_into_practice_by", "minimum_evidence": "Practice-facing publication or documented use", "strict_dependency": "no", "plain_phrase": "translates for practice"},
    {"relation_type": "specialises_in", "relation_family": "practice", "directed": "true", "inverse": "area_of_expertise_for", "minimum_evidence": "Public body of work or professional record", "strict_dependency": "no", "plain_phrase": "specialises in"},
    {"relation_type": "co_developed", "relation_family": "historical", "directed": "true", "inverse": "co_developed_by", "minimum_evidence": "Official publication or method record", "strict_dependency": "no", "plain_phrase": "co-developed"},
]

SOURCE_UPSERTS: list[dict[str, Any]] = [
    {
        "id": "src_lancaster_checkland_stsp_1999",
        "title": "Systems Thinking, Systems Practice: includes a 30-year retrospective",
        "source_type": "official_university_research_record",
        "quality_tier": "A",
        "access": "public_metadata",
        "url": "https://research.lancaster-university.uk/en/publications/systems-thinking-systems-practice-includes-a-30-year-retrospectiv/",
        "date": "1999",
        "notes": "Lancaster University's research record establishes Peter Checkland's authorship, the 1999 retrospective edition, publisher and bibliographic details.",
        "creators": "[\"Peter Checkland\"]",
        "doi": "",
        "isbn": "978-0-471-98606-5",
        "publisher": "John Wiley and Sons Ltd",
        "licence": "source_terms",
        "archived_url": "",
        "content_hash": "",
        "review_status": "checked",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_wiley_checkland_stsp_1999",
        "title": "Systems Thinking, Systems Practice — Wiley publisher page",
        "source_type": "official_publisher_book_page",
        "quality_tier": "A",
        "access": "public_metadata",
        "url": "https://www.wiley-vch.de/en/areas-interest/finance-economics-law/systems-thinking-systems-practice-978-0-471-98606-5",
        "date": "1999-07",
        "notes": "The publisher describes the book as the culmination of action research using systems ideas in ill-structured real-world situations and records the 30-year retrospective edition.",
        "creators": "[\"Peter Checkland\"]",
        "doi": "",
        "isbn": "978-0-471-98606-5",
        "publisher": "John Wiley and Sons Ltd",
        "licence": "publisher_terms",
        "archived_url": "",
        "content_hash": "",
        "review_status": "checked",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_ulrich_csh_mini_primer_2023",
        "title": "A Mini-Primer of Critical Systems Heuristics",
        "source_type": "primary_author_method_page",
        "quality_tier": "A",
        "access": "public",
        "url": "https://wulrich.com/csh.html",
        "date": "2005; updated 2023-05-20",
        "notes": "Werner Ulrich's maintained primary account defines Critical Systems Heuristics as reflective practice centred on systematic boundary critique and twelve critical boundary questions.",
        "creators": "[\"Werner Ulrich\"]",
        "doi": "",
        "isbn": "",
        "publisher": "Werner Ulrich",
        "licence": "noncommercial_distribution_and_citation_with_attribution",
        "archived_url": "",
        "content_hash": "",
        "review_status": "checked",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_ou_ray_ison_profile_2026",
        "title": "Ray Ison — Open University profile",
        "source_type": "official_university_profile",
        "quality_tier": "A",
        "access": "public",
        "url": "https://profiles.open.ac.uk/ray-ison",
        "date": "current",
        "notes": "The Open University profile records Ray Ison's work in Systems Thinking in Practice, systems praxeology, social learning, systemic governance and systems education.",
        "creators": "[\"The Open University\"]",
        "doi": "",
        "isbn": "",
        "publisher": "The Open University",
        "licence": "site_terms",
        "archived_url": "",
        "content_hash": "",
        "review_status": "checked",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_routledge_hidden_power_2020",
        "title": "The Hidden Power of Systems Thinking: Governance in a Climate Emergency",
        "source_type": "official_publisher_book_page",
        "quality_tier": "A",
        "access": "public_metadata",
        "url": "https://www.routledge.com/The-Hidden-Power-of-Systems-Thinking-Governance-in-a-Climate-Emergency/Ison-Straw/p/book/9781138493995",
        "date": "2020",
        "notes": "Routledge's page records Ray Ison and Ed Straw as authors and describes the book's focus on systems thinking, systemic governing and institutional change in the climate emergency.",
        "creators": "[\"Ray Ison\", \"Ed Straw\"]",
        "doi": "",
        "isbn": "978-1-138-49399-5",
        "publisher": "Routledge",
        "licence": "publisher_terms",
        "archived_url": "",
        "content_hash": "",
        "review_status": "checked",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_springer_organizational_systems_2011",
        "title": "Organizational Systems: Managing Complexity with the Viable System Model",
        "source_type": "official_publisher_book_page",
        "quality_tier": "A",
        "access": "public_metadata",
        "url": "https://link.springer.com/book/10.1007/978-3-642-19109-1",
        "date": "2011",
        "notes": "Springer's page records Raul Espejo and Alfonso Reyes as authors and describes the book's treatment of organisational cybernetics, the Viable System Model, Viplan, diagnosis, design and implementation.",
        "creators": "[\"Raul Espejo\", \"Alfonso Reyes\"]",
        "doi": "10.1007/978-3-642-19109-1",
        "isbn": "978-3-642-19109-1",
        "publisher": "Springer Berlin Heidelberg",
        "licence": "publisher_terms",
        "archived_url": "",
        "content_hash": "",
        "review_status": "checked",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_prh_thinking_in_systems_2008",
        "title": "Thinking in Systems: A Primer",
        "source_type": "official_publisher_book_page",
        "quality_tier": "A",
        "access": "public_metadata",
        "url": "https://www.penguinrandomhouse.com/books/801035/thinking-in-systems-by-donella-meadows/",
        "date": "2008-12-05",
        "notes": "The publisher records Donella Meadows as author and Diana Wright as editor and describes the book as a practice-facing introduction to systems structures, feedback and intervention.",
        "creators": "[\"Donella Meadows\", \"Diana Wright\"]",
        "doi": "",
        "isbn": "978-1-60358-055-7",
        "publisher": "Chelsea Green",
        "licence": "publisher_terms",
        "archived_url": "",
        "content_hash": "",
        "review_status": "checked",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_meadows_dancing_with_systems",
        "title": "Dancing With Systems",
        "source_type": "primary_author_archive",
        "quality_tier": "A",
        "access": "public",
        "url": "https://donellameadows.org/archives/dancing-with-systems/",
        "date": "2004; archived current",
        "notes": "The Donella Meadows Project publishes the essay and its practical disciplines for acting with feedback-rich, nonlinear and partly unpredictable systems.",
        "creators": "[\"Donella Meadows\"]",
        "doi": "",
        "isbn": "",
        "publisher": "The Donella Meadows Project",
        "licence": "source_terms",
        "archived_url": "",
        "content_hash": "",
        "review_status": "checked",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_meadows_leverage_points",
        "title": "Leverage Points: Places to Intervene in a System",
        "source_type": "primary_author_archive",
        "quality_tier": "A",
        "access": "public",
        "url": "https://donellameadows.org/archives/leverage-points-places-to-intervene-in-a-system/",
        "date": "1999; archived current",
        "notes": "The Donella Meadows Project publishes Meadows's ordered list of places to intervene, together with her cautions about context, resistance, uncertainty and paradigm flexibility.",
        "creators": "[\"Donella Meadows\"]",
        "doi": "",
        "isbn": "",
        "publisher": "The Donella Meadows Project",
        "licence": "source_terms",
        "archived_url": "",
        "content_hash": "",
        "review_status": "checked",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_triarchy_organic_systems_framework_2019",
        "title": "The Organic Systems Framework",
        "source_type": "official_publisher_book_page",
        "quality_tier": "A",
        "access": "public_metadata",
        "url": "https://www.triarchypress.net/osf.html",
        "date": "2019",
        "notes": "Triarchy Press describes Barry Oshry's Organic Systems Framework as a pattern language for whole-system relationships and processes, including differentiation, integration, individuation and homogenisation.",
        "creators": "[\"Barry Oshry\"]",
        "doi": "",
        "isbn": "978-1-911193-61-6",
        "publisher": "Triarchy Press",
        "licence": "publisher_terms",
        "archived_url": "",
        "content_hash": "",
        "review_status": "checked",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_triarchy_barry_oshry_profile",
        "title": "Barry Oshry — author profile",
        "source_type": "official_publisher_author_profile",
        "quality_tier": "A",
        "access": "public",
        "url": "https://www.triarchypress.net/barry-oshry.html",
        "date": "current",
        "notes": "Triarchy Press describes Oshry's work on human systems, system-blindness and system-sight and lists his principal programmes and publications.",
        "creators": "[\"Triarchy Press\"]",
        "doi": "",
        "isbn": "",
        "publisher": "Triarchy Press",
        "licence": "site_terms",
        "archived_url": "",
        "content_hash": "",
        "review_status": "checked",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
]


NODE_SPECS: list[dict[str, Any]] = [
    {
        "id": "person_peter_checkland",
        "label": "Peter Checkland",
        "entity_type": "person",
        "description": "A systems scholar and practitioner who developed Soft Systems Methodology through action research on messy, contested situations and the relation between systems thinking and systems practice.",
        "aliases": [],
        "source_ids": ["src_lancaster_checkland_stsp_1999", "src_wiley_checkland_stsp_1999"],
        "x": 0.18,
        "y": 0.16,
        "profile": True,
    },
    {
        "id": "publication_systems_thinking_systems_practice",
        "label": "Systems Thinking, Systems Practice",
        "entity_type": "publication",
        "description": "Peter Checkland's account of the action-research programme from which Soft Systems Methodology developed, joining systems ideas to inquiry in ill-structured real-world situations.",
        "aliases": ["Systems Thinking, Systems Practice: includes a 30-year retrospective"],
        "source_ids": ["src_lancaster_checkland_stsp_1999", "src_wiley_checkland_stsp_1999"],
        "x": 0.23,
        "y": 0.14,
        "profile": True,
    },
    {
        "id": "person_werner_ulrich",
        "label": "Werner Ulrich",
        "entity_type": "person",
        "description": "A systems scholar whose Critical Systems Heuristics develops practical and philosophical resources for examining boundary judgements, knowledge claims, values and the standing of those affected.",
        "aliases": [],
        "source_ids": ["src_ulrich_csh_mini_primer_2023"],
        "x": 0.08,
        "y": 0.26,
        "profile": True,
    },
    {
        "id": "publication_mini_primer_critical_systems_heuristics",
        "label": "A Mini-Primer of Critical Systems Heuristics",
        "entity_type": "publication",
        "description": "Werner Ulrich's maintained introduction to Critical Systems Heuristics, boundary critique and the twelve questions used to examine reference systems and claims to improvement.",
        "aliases": ["A Mini-Primer of CSH"],
        "source_ids": ["src_ulrich_csh_mini_primer_2023"],
        "x": 0.12,
        "y": 0.29,
        "profile": True,
    },
    {
        "id": "concept_boundary_critique",
        "label": "Boundary critique",
        "entity_type": "concept",
        "description": "Boundary critique is the systematic examination of judgements about what and whom a situation, inquiry or proposal treats as relevant, including the facts, values, interests and voices those judgements admit or exclude.",
        "aliases": ["critical boundary reflection"],
        "source_ids": ["src_ulrich_csh_mini_primer_2023"],
        "x": 0.02,
        "y": 0.22,
        "profile": True,
    },
    {
        "id": "person_ray_ison",
        "label": "Ray Ison",
        "entity_type": "person",
        "description": "A systems scholar and educator whose work develops Systems Thinking in Practice, systems praxeology, social learning, institutional innovation and systemic governance.",
        "aliases": ["Raymond Ison"],
        "source_ids": ["src_ou_ray_ison_profile_2026", "src_routledge_hidden_power_2020", "src_ison_cybersystemics_2025", "src_ou_stip_2025"],
        "x": 0.31,
        "y": 0.25,
        "profile": True,
    },
    {
        "id": "person_ed_straw",
        "label": "Ed Straw",
        "entity_type": "person",
        "description": "A governance practitioner and co-author of The Hidden Power of Systems Thinking, contributing experience of government, public administration, institutional reform and systemic governing.",
        "aliases": [],
        "source_ids": ["src_routledge_hidden_power_2020"],
        "x": 0.37,
        "y": 0.29,
        "profile": False,
    },
    {
        "id": "publication_hidden_power_systems_thinking",
        "label": "The Hidden Power of Systems Thinking",
        "entity_type": "publication",
        "description": "Ray Ison and Ed Straw's account of systems thinking in governance, focused on institutional obstacles, systemic governing and practical principles for acting amid climate and biodiversity emergencies.",
        "aliases": ["The Hidden Power of Systems Thinking: Governance in a Climate Emergency"],
        "source_ids": ["src_routledge_hidden_power_2020"],
        "x": 0.35,
        "y": 0.23,
        "profile": True,
    },
    {
        "id": "concept_systemic_governance",
        "label": "Systemic governance",
        "entity_type": "concept",
        "description": "Systemic governance treats governing as the design and continuing adaptation of relationships, institutions, learning processes and accountabilities across interacting systems rather than as command from one centre.",
        "aliases": ["systemic governing"],
        "source_ids": ["src_ou_ray_ison_profile_2026", "src_routledge_hidden_power_2020"],
        "x": 0.27,
        "y": 0.31,
        "profile": True,
    },
    {
        "id": "person_raul_espejo",
        "label": "Raul Espejo",
        "entity_type": "person",
        "description": "An organisational cybernetician and practitioner whose work develops the Viable System Model, Viplan, variety engineering and methods for organisational diagnosis, design and implementation.",
        "aliases": ["Raúl Espejo"],
        "source_ids": ["src_springer_organizational_systems_2011"],
        "x": -0.29,
        "y": 0.11,
        "profile": True,
    },
    {
        "id": "person_alfonso_reyes",
        "label": "Alfonso Reyes",
        "entity_type": "person",
        "description": "A systems scholar and co-author of Organizational Systems, contributing to its account of complexity, organisational cybernetics, the Viable System Model and systemic methodology.",
        "aliases": [],
        "source_ids": ["src_springer_organizational_systems_2011"],
        "x": -0.23,
        "y": 0.13,
        "profile": True,
    },
    {
        "id": "publication_organizational_systems_vsm",
        "label": "Organizational Systems",
        "entity_type": "publication",
        "description": "Raul Espejo and Alfonso Reyes's synthesis of organisational cybernetics, the Viable System Model, Viplan, variety engineering and methodology for diagnosis, design and implementation.",
        "aliases": ["Organizational Systems: Managing Complexity with the Viable System Model"],
        "source_ids": ["src_springer_organizational_systems_2011"],
        "x": -0.25,
        "y": 0.07,
        "profile": True,
    },
    {
        "id": "method_or_methodology_viplan",
        "label": "Viplan",
        "entity_type": "method_or_methodology",
        "description": "Viplan is Raul Espejo's method and methodology for using organisational cybernetics and the Viable System Model in diagnosis, design and implementation work.",
        "aliases": ["Viplan method", "Viplan methodology"],
        "source_ids": ["src_springer_organizational_systems_2011"],
        "x": -0.19,
        "y": 0.08,
        "profile": True,
    },
    {
        "id": "person_donella_meadows",
        "label": "Donella Meadows",
        "entity_type": "person",
        "description": "A systems analyst, author and educator whose work joined system dynamics, environmental analysis and practical disciplines for understanding, intervening in and living with complex systems.",
        "aliases": ["Dana Meadows", "Donella H. Meadows"],
        "source_ids": ["src_prh_thinking_in_systems_2008", "src_meadows_dancing_with_systems", "src_meadows_leverage_points"],
        "x": 0.48,
        "y": 0.02,
        "profile": True,
    },
    {
        "id": "person_diana_wright",
        "label": "Diana Wright",
        "entity_type": "person",
        "description": "The editor who prepared Donella Meadows's unfinished manuscript for publication as Thinking in Systems, preserving and organising its practice-facing introduction to systems thinking.",
        "aliases": [],
        "source_ids": ["src_prh_thinking_in_systems_2008"],
        "x": 0.54,
        "y": 0.01,
        "profile": False,
    },
    {
        "id": "publication_thinking_in_systems",
        "label": "Thinking in Systems",
        "entity_type": "publication",
        "description": "Donella Meadows's concise introduction to stocks, flows, feedback, delays, resilience, self-organisation and the practical discipline of seeing systems without assuming prediction and control.",
        "aliases": ["Thinking in Systems: A Primer"],
        "source_ids": ["src_prh_thinking_in_systems_2008"],
        "x": 0.45,
        "y": 0.07,
        "profile": True,
    },
    {
        "id": "publication_leverage_points_meadows",
        "label": "Leverage Points: Places to Intervene in a System",
        "entity_type": "publication",
        "description": "Donella Meadows's ordered account of places to intervene in systems, ranging from parameters and feedback structures to goals, paradigms and the capacity to remain unattached to paradigms.",
        "aliases": ["Leverage Points essay"],
        "source_ids": ["src_meadows_leverage_points"],
        "x": 0.51,
        "y": 0.10,
        "profile": True,
    },
    {
        "id": "publication_dancing_with_systems",
        "label": "Dancing With Systems",
        "entity_type": "publication",
        "description": "Donella Meadows's practical disciplines for acting with feedback-rich and partly unpredictable systems: observe, listen, expose assumptions, learn, protect information and work for the good of the whole.",
        "aliases": [],
        "source_ids": ["src_meadows_dancing_with_systems"],
        "x": 0.56,
        "y": 0.06,
        "profile": True,
    },
    {
        "id": "concept_leverage_points",
        "label": "Leverage points",
        "entity_type": "concept",
        "description": "Leverage points are places where changing a system's information, feedback, rules, goals, structure or paradigms may alter its behaviour; their effect depends on direction, context and resistance.",
        "aliases": ["places to intervene in a system"],
        "source_ids": ["src_meadows_leverage_points"],
        "x": 0.46,
        "y": 0.14,
        "profile": True,
    },
    {
        "id": "person_barry_oshry",
        "label": "Barry Oshry",
        "entity_type": "person",
        "description": "A human-systems practitioner and author whose work develops system-sight through recurring relational positions, whole-system processes, power, love, differentiation and integration.",
        "aliases": [],
        "source_ids": ["src_triarchy_barry_oshry_profile", "src_triarchy_organic_systems_framework_2019"],
        "x": 0.05,
        "y": -0.24,
        "profile": True,
    },
    {
        "id": "publication_organic_systems_framework",
        "label": "The Organic Systems Framework",
        "entity_type": "publication",
        "description": "Barry Oshry's concise case for a framework of recurring whole-system relationships and processes, including individuation, integration, differentiation and homogenisation.",
        "aliases": ["The Organic Systems Framework: A New Paradigm for Understanding and Intervening in Organizational Life"],
        "source_ids": ["src_triarchy_organic_systems_framework_2019"],
        "x": 0.09,
        "y": -0.27,
        "profile": True,
    },
    {
        "id": "method_or_methodology_organic_systems_framework",
        "label": "Organic Systems Framework",
        "entity_type": "method_or_methodology",
        "description": "The Organic Systems Framework is Barry Oshry's pattern language for seeing human systems as wholes and examining how recurring positions and whole-system processes shape experience and action.",
        "aliases": ["OSF"],
        "source_ids": ["src_triarchy_organic_systems_framework_2019", "src_triarchy_barry_oshry_profile"],
        "x": 0.02,
        "y": -0.29,
        "profile": True,
    },
]


PROFILE_SPECS: dict[str, dict[str, Any]] = {
    "person_peter_checkland": {
        "summary": "Peter Checkland developed Soft Systems Methodology through sustained action research in situations where purposes, boundaries and improvements are contested rather than given.",
        "why_it_matters": "His work makes a basic systems distinction operational: systems can be used as devices for inquiry into a situation without assuming that the situation itself is one objectively specified system.",
        "key_distinctions": ["system as ontology vs system as epistemological device", "hard problem solving vs inquiry into problem situations", "model of purposeful activity vs model of the world"],
        "historical_lineage": ["systems engineering", "action research at Lancaster", "Soft Systems Methodology", "later systems practice"],
        "logical_antecedents": ["purpose", "boundary", "worldview", "learning", "human activity system"],
        "dependent_subsequents": ["Soft Systems Methodology", "rich pictures", "root definitions", "conceptual activity models"],
        "practice_connections": ["organisational inquiry", "public-service problem structuring", "participative learning", "feasible and desirable change"],
        "common_misreadings": ["SSM is a softer version of optimisation", "a conceptual model describes the real organisation", "consensus is required before action"],
        "open_checks": ["add Learning for Action", "map Checkland's collaborators and students", "develop criticism and later adaptations"],
    },
    "publication_systems_thinking_systems_practice": {
        "summary": "Systems Thinking, Systems Practice records the action-research programme that produced SSM and keeps theory and practice in a recursive relation rather than treating application as a final implementation stage.",
        "why_it_matters": "It is a primary route into why SSM was developed, what it was designed to avoid and how systems thinking changes when inquiry concerns people with different purposes and interpretations.",
        "key_distinctions": ["problem vs problem situation", "systematic vs systemic", "real-world action vs conceptual modelling"],
        "historical_lineage": ["systems engineering", "Lancaster action research", "Soft Systems Methodology"],
        "logical_antecedents": ["systems thinking", "action research", "purposeful activity", "worldview"],
        "dependent_subsequents": ["SSM modes of use", "Learning for Action", "systems practice teaching"],
        "practice_connections": ["problem structuring", "organisational learning", "participative inquiry"],
        "common_misreadings": ["the book supplies a fixed seven-step recipe", "models are proposed designs of reality"],
        "open_checks": ["add page-level locators", "distinguish 1981 and retrospective editions", "map critical responses"],
    },
    "person_werner_ulrich": {
        "summary": "Werner Ulrich developed Critical Systems Heuristics as a framework for reflective and critical practice centred on boundary judgements and the relation between expertise, values and those affected.",
        "why_it_matters": "CSH gives boundary critique a disciplined form. It makes the normative assumptions of claims to knowledge and improvement discussable without requiring everyone to become a technical specialist.",
        "key_distinctions": ["involved vs affected", "is vs ought", "boundary judgement vs neutral fact", "critique vs denunciation"],
        "historical_lineage": ["C. West Churchman", "practical philosophy", "critical systems thinking", "Critical Systems Heuristics"],
        "logical_antecedents": ["boundary", "purpose", "legitimacy", "knowledge", "power"],
        "dependent_subsequents": ["twelve boundary questions", "emancipatory boundary critique", "citizen competence"],
        "practice_connections": ["policy appraisal", "evaluation", "participatory inquiry", "professional and citizen critique"],
        "common_misreadings": ["CSH finds the correct boundary", "only marginalised groups can use boundary critique", "the twelve questions are a survey instrument"],
        "open_checks": ["map Churchman lineage", "add primary book sources", "develop applications and criticism"],
    },
    "publication_mini_primer_critical_systems_heuristics": {
        "summary": "The mini-primer gives a concise primary account of CSH, its philosophical basis, boundary critique and the uses of the twelve boundary questions.",
        "why_it_matters": "It is a public, maintained source that states what CSH is and is not, reducing reliance on second-hand summaries and method labels.",
        "key_distinctions": ["heuristic vs algorithm", "reflection vs boundary critique", "cooperative vs emancipatory use"],
        "historical_lineage": ["Critical Heuristics of Social Planning", "CSH primers and later revisions"],
        "logical_antecedents": ["practical philosophy", "systems thinking", "boundary judgement"],
        "dependent_subsequents": ["boundary categories", "twelve boundary questions", "critical professional practice"],
        "practice_connections": ["action research", "policy and programme evaluation", "citizen challenge"],
        "common_misreadings": ["a mini-primer replaces the full methodology", "boundary questions generate one correct answer"],
        "open_checks": ["add companion primer to boundary critique", "record revision history", "link page-level claims"],
    },
    "concept_boundary_critique": {
        "summary": "Boundary critique asks how judgements about relevance shape what counts as fact, value, improvement, expertise and legitimate participation.",
        "why_it_matters": "Every systems intervention draws a boundary. Making that boundary discussable is a condition for responsible inquiry, especially when benefits and harms fall on people who did not define the system of concern.",
        "key_distinctions": ["boundary vs perimeter", "relevance vs existence", "involved vs affected", "fact and value as boundary-conditioned"],
        "historical_lineage": ["Churchman's systems approach", "Ulrich's Critical Systems Heuristics", "systemic intervention"],
        "logical_antecedents": ["boundary", "purpose", "stakeholder", "legitimacy"],
        "dependent_subsequents": ["twelve boundary questions", "systemic marginalisation", "critical evaluation"],
        "practice_connections": ["framing policy questions", "testing beneficiaries and victims", "reviewing expertise claims"],
        "common_misreadings": ["wider is always better", "all boundaries can be eliminated", "boundary critique guarantees inclusion"],
        "open_checks": ["connect Midgley's systemic marginalisation", "add cases of boundary change", "map rival boundary practices"],
    },
    "person_ray_ison": {
        "summary": "Ray Ison's work treats systems thinking as an enacted practice involving situation, practitioner, concepts, methods, traditions and institutional conditions.",
        "why_it_matters": "Systems praxeology and systemic governance keep attention on how ways of knowing and acting are performed, learned and institutionalised rather than treating systems thinking as a detachable tool kit.",
        "key_distinctions": ["systems thinking about practice vs Systems Thinking in Practice", "governance vs government", "social learning vs knowledge transfer"],
        "historical_lineage": ["Open University systems teaching", "systems agriculture", "social learning", "systems praxeology", "systemic governance"],
        "logical_antecedents": ["practice", "learning", "institution", "governance", "reflexivity"],
        "dependent_subsequents": ["STiP pedagogy", "systems praxeology", "systemic governance research"],
        "practice_connections": ["climate adaptation", "water governance", "public administration", "systems education"],
        "common_misreadings": ["STiP is a collection of methods", "governance means government machinery", "social learning is consultation"],
        "open_checks": ["add Systems Practice editions", "map collaborators and programmes", "develop cybersystemics work"],
    },
    "publication_hidden_power_systems_thinking": {
        "summary": "The Hidden Power of Systems Thinking connects systems practice to failures and possibilities of governance under climate and biodiversity emergency.",
        "why_it_matters": "It moves systems thinking from diagnosis of complex problems to the design of governing relationships, institutions, constitutional arrangements and learning capacity.",
        "key_distinctions": ["government vs governance", "institutional reform vs isolated intervention", "whole-system change vs programme delivery"],
        "historical_lineage": ["Systems Thinking in Practice", "systemic governance", "public administration and institutional reform"],
        "logical_antecedents": ["governance", "systems practice", "institution", "climate emergency"],
        "dependent_subsequents": ["principles for systemic governing", "institutional innovation", "governance capability"],
        "practice_connections": ["public administration", "constitutional design", "climate governance", "collective action"],
        "common_misreadings": ["systems thinking itself supplies political legitimacy", "governance can be redesigned from one centre"],
        "open_checks": ["map the stated principles", "add reviews and critical responses", "connect public-service cases"],
    },
    "concept_systemic_governance": {
        "summary": "Systemic governance concerns the institutions, relations and learning processes through which multiple actors govern together across boundaries and levels.",
        "why_it_matters": "Complex public issues exceed the variety and authority of any single organisation. Governance has to distribute sensing, action and accountability while preserving the capacity to learn and adapt.",
        "key_distinctions": ["governance vs government", "coordination vs command", "distributed agency vs absence of accountability"],
        "historical_lineage": ["systems practice", "institutional innovation", "social learning", "cybernetics of governance"],
        "logical_antecedents": ["boundary", "agency", "accountability", "learning", "variety"],
        "dependent_subsequents": ["systemic governing principles", "multi-level institutional design", "collective learning arrangements"],
        "practice_connections": ["place-based governance", "climate adaptation", "public-service systems", "cross-sector collaboration"],
        "common_misreadings": ["systemic means comprehensive central planning", "network governance needs no authority", "collaboration removes conflict"],
        "open_checks": ["connect governance traditions", "add public cases", "distinguish democratic legitimacy from functional viability"],
    },
    "person_raul_espejo": {
        "summary": "Raul Espejo develops organisational cybernetics as a practice of understanding and designing identities, relations, regulatory capacity and organisational structures.",
        "why_it_matters": "His work extends the VSM into methods for diagnosis, design and implementation, including Viplan and detailed treatment of variety engineering.",
        "key_distinctions": ["VSM model vs Viplan methodology", "identity vs structure", "complexity absorption vs information volume"],
        "historical_lineage": ["Project Cybersyn", "Stafford Beer", "organisational cybernetics", "Viplan"],
        "logical_antecedents": ["viability", "requisite variety", "identity", "autonomy", "cohesion"],
        "dependent_subsequents": ["Viplan", "variety engineering", "organisational diagnosis and design"],
        "practice_connections": ["organisation design", "public and private enterprise", "democratic governance", "implementation"],
        "common_misreadings": ["Viplan is another VSM diagram", "identity can be read directly from an organisation chart"],
        "open_checks": ["add primary Viplan papers", "map Cybersyn role carefully", "connect later organisational cybernetics"],
    },
    "person_alfonso_reyes": {
        "summary": "Alfonso Reyes co-developed Organizational Systems as a synthesis of complexity, organisational cybernetics, VSM and methodology.",
        "why_it_matters": "His co-authorship is part of the book's intellectual and practical provenance and should not disappear behind a single-author account of organisational cybernetics.",
        "key_distinctions": ["co-authorship vs editorial assistance", "systemic methodology vs model application"],
        "historical_lineage": ["organisational cybernetics", "VSM", "systems methodology"],
        "logical_antecedents": ["complexity", "organisation", "methodology"],
        "dependent_subsequents": ["Organizational Systems", "teaching and application of VSM"],
        "practice_connections": ["organisational analysis", "systems education", "institutional design"],
        "common_misreadings": ["the book is solely Espejo's work", "VSM application is methodologically neutral"],
        "open_checks": ["develop independent profile sources", "map wider publications and collaborations"],
    },
    "publication_organizational_systems_vsm": {
        "summary": "Organizational Systems combines concepts, VSM, Viplan and systemic methodology into an integrated account of organisational diagnosis and design.",
        "why_it_matters": "It provides a major practice-facing bridge from Beer's VSM to methods of organisational cybernetics, including implementation problems and variety engineering.",
        "key_distinctions": ["VSM vs Viplan", "method vs methodology", "diagnosis vs design vs implementation"],
        "historical_lineage": ["Stafford Beer", "organisational cybernetics", "Espejo's Viplan work"],
        "logical_antecedents": ["VSM", "complexity", "identity", "variety engineering"],
        "dependent_subsequents": ["Viplan applications", "organisational cybernetics teaching", "diagnosis and design practice"],
        "practice_connections": ["organisation design", "governance", "change implementation"],
        "common_misreadings": ["it is only a VSM textbook", "organisation can be diagnosed without clarifying identity"],
        "open_checks": ["add chapter-level locators", "map reviews and critiques", "connect cases"],
    },
    "method_or_methodology_viplan": {
        "summary": "Viplan combines organisational cybernetics, identity work and the VSM in a method and methodology for diagnosis, design and implementation.",
        "why_it_matters": "It makes the move from a cybernetic model to organised inquiry and intervention explicit, reducing the common error of treating the VSM diagram itself as a complete method.",
        "key_distinctions": ["VSM model vs Viplan method", "method vs methodology", "identity clarification vs structural redesign"],
        "historical_lineage": ["Stafford Beer", "Raul Espejo", "organisational cybernetics"],
        "logical_antecedents": ["VSM", "identity", "requisite variety", "recursion"],
        "dependent_subsequents": ["organisational diagnosis", "organisation design", "implementation methodology"],
        "practice_connections": ["governance design", "organisational transformation", "capability diagnosis"],
        "common_misreadings": ["Viplan is a drawing template", "all organisations have one obvious system in focus"],
        "open_checks": ["add primary method sources", "document variants and cases", "compare with other VSM methodologies"],
    },
    "person_donella_meadows": {
        "summary": "Donella Meadows connected rigorous system dynamics with lucid public explanation and practical disciplines for intervention, learning and responsible action.",
        "why_it_matters": "Her work brings feedback, stocks, flows, delays, resilience and leverage into public and organisational practice while repeatedly warning against the fantasy of complete prediction and control.",
        "key_distinctions": ["understanding vs control", "event vs behaviour over time", "parameter change vs structural leverage", "measurement vs value"],
        "historical_lineage": ["MIT system dynamics", "Limits to Growth", "sustainability analysis", "systems education"],
        "logical_antecedents": ["stocks and flows", "feedback", "delay", "nonlinearity", "goal"],
        "dependent_subsequents": ["Thinking in Systems", "Leverage Points", "Dancing With Systems"],
        "practice_connections": ["policy modelling", "sustainability", "organisational learning", "intervention design"],
        "common_misreadings": ["leverage points are a universal recipe", "systems analysis enables control", "only quantifiable variables matter"],
        "open_checks": ["develop system-dynamics lineage", "connect Limits to Growth", "map criticism and later applications"],
    },
    "publication_thinking_in_systems": {
        "summary": "Thinking in Systems introduces system structures and behaviours through ordinary examples while retaining the discipline of stocks, flows, feedback, delays and resilience.",
        "why_it_matters": "It is a widely used route into systems thinking that combines technical clarity with cautions about boundaries, values, surprise and control.",
        "key_distinctions": ["stock vs flow", "reinforcing vs balancing feedback", "event vs pattern", "resilience vs efficiency"],
        "historical_lineage": ["system dynamics", "Donella Meadows's teaching and essays", "Diana Wright's editorial work"],
        "logical_antecedents": ["feedback", "stock", "flow", "delay", "system boundary"],
        "dependent_subsequents": ["public systems literacy", "leverage-point practice", "systems education"],
        "practice_connections": ["policy", "management", "environmental systems", "personal and community action"],
        "common_misreadings": ["all systems can be reduced to one diagram", "the text offers prediction rather than disciplined inquiry"],
        "open_checks": ["map chapter concepts", "connect to primary essays", "add critiques from non-system-dynamics traditions"],
    },
    "publication_leverage_points_meadows": {
        "summary": "Leverage Points orders potential interventions from parameters through feedback and rules to goals, paradigms and the ability to move among paradigms.",
        "why_it_matters": "The essay is useful precisely because it combines a memorable hierarchy with repeated cautions: leverage depends on direction and context, systems resist change, and the list is not a recipe.",
        "key_distinctions": ["leverage point vs preferred solution", "location vs direction", "parameter vs information vs rule vs goal"],
        "historical_lineage": ["system dynamics", "Jay Forrester", "Donella Meadows's policy and teaching work"],
        "logical_antecedents": ["feedback", "information flow", "rule", "goal", "paradigm"],
        "dependent_subsequents": ["intervention heuristics", "paradigm practice", "systems-change discourse"],
        "practice_connections": ["policy design", "organisational change", "sustainability intervention"],
        "common_misreadings": ["higher is always easier", "the list identifies one best intervention", "paradigm change can be commanded"],
        "open_checks": ["map all twelve levels", "connect empirical cases", "compare with other intervention frameworks"],
    },
    "publication_dancing_with_systems": {
        "summary": "Dancing With Systems presents practical disciplines for acting with systems whose behaviour cannot be fully predicted or controlled.",
        "why_it_matters": "It connects systems knowledge to conduct: observation, humility, learning, information integrity, responsibility, time horizons and care for the whole.",
        "key_distinctions": ["participation vs control", "learning vs bluffing", "important vs merely quantifiable"],
        "historical_lineage": ["system dynamics practice", "Meadows's modelling and teaching", "Thinking in Systems"],
        "logical_antecedents": ["feedback", "uncertainty", "learning", "responsibility"],
        "dependent_subsequents": ["systems practice disciplines", "adaptive intervention", "systems ethics"],
        "practice_connections": ["management", "government", "community action", "personal practice"],
        "common_misreadings": ["dancing means passivity", "uncertainty means analysis is useless", "humility means avoiding judgement"],
        "open_checks": ["connect each discipline to practice cases", "compare with cybernetic ethics", "map relation to Thinking in Systems"],
    },
    "concept_leverage_points": {
        "summary": "Leverage points are intervention locations in a system's structure, information, feedback, rules, goals and paradigms.",
        "why_it_matters": "They direct attention away from the visibility of an intervention towards the system property it changes and the direction in which it changes it.",
        "key_distinctions": ["point vs direction", "parameter vs structure", "goal vs paradigm", "leverage vs ease"],
        "historical_lineage": ["system dynamics", "Forrester", "Meadows's synthesis"],
        "logical_antecedents": ["feedback", "information", "rule", "goal", "paradigm"],
        "dependent_subsequents": ["systems intervention heuristics", "systems-change practice"],
        "practice_connections": ["policy", "strategy", "organisation design", "social change"],
        "common_misreadings": ["a leverage point is automatically beneficial", "the highest level is always the correct target"],
        "open_checks": ["map twelve levels", "add counterexamples", "compare with intervention points in other traditions"],
    },
    "person_barry_oshry": {
        "summary": "Barry Oshry develops experiential and conceptual resources for moving from system-blindness to system-sight in human systems.",
        "why_it_matters": "His work explains how recurring relational positions and whole-system processes generate predictable experiences without reducing people to personality types or formal roles.",
        "key_distinctions": ["position vs personality", "system-blindness vs system-sight", "differentiation vs individuation", "integration vs homogenisation"],
        "historical_lineage": ["human systems practice", "Power Lab", "Organization Workshop", "Organic Systems Framework"],
        "logical_antecedents": ["context", "position", "power", "whole and part", "relationship"],
        "dependent_subsequents": ["Tops, Middles, Bottoms and Customers", "Power and Love", "Organic Systems Framework"],
        "practice_connections": ["leadership development", "organisation development", "partnership", "power and system dynamics"],
        "common_misreadings": ["Tops, Middles and Bottoms are personality types", "system position removes personal responsibility", "integration means agreement"],
        "open_checks": ["map primary books and programmes", "connect empirical research", "develop relation to schismogenesis and power"],
    },
    "publication_organic_systems_framework": {
        "summary": "The Organic Systems Framework argues for a coherent pattern language of whole-system relationships and processes in human systems.",
        "why_it_matters": "It supplies a compact account of individuation, integration, differentiation and homogenisation and connects those processes to recurring positions, power and partnership.",
        "key_distinctions": ["whole-system process vs role behaviour", "differentiation vs individuation", "integration vs homogenisation"],
        "historical_lineage": ["Oshry's experiential programmes", "human systems thinking", "organisation development"],
        "logical_antecedents": ["whole", "part", "position", "relationship", "context"],
        "dependent_subsequents": ["research and application of OSF", "system-sight practice"],
        "practice_connections": ["organisation workshops", "leadership", "partnership", "system diagnosis"],
        "common_misreadings": ["paradigm is used merely as a synonym for idea", "the framework predicts individual behaviour"],
        "open_checks": ["map the full framework", "add research applications", "compare with other human-systems accounts"],
    },
    "method_or_methodology_organic_systems_framework": {
        "summary": "The Organic Systems Framework is a pattern language for seeing recurring relations and processes in human systems and using that system-sight to alter action.",
        "why_it_matters": "It provides a non-individualising explanation of recurrent experiences of burden, oppression, alienation and vulnerability while retaining room for agency and responsibility.",
        "key_distinctions": ["position vs person", "systemic condition vs moral excuse", "whole-system process vs local event"],
        "historical_lineage": ["Barry Oshry's programmes", "human systems practice", "Organic Systems Framework"],
        "logical_antecedents": ["context", "position", "relationship", "whole"],
        "dependent_subsequents": ["system-sight", "partnership interventions", "whole-system diagnosis"],
        "practice_connections": ["leadership development", "organisation development", "power analysis", "partnership"],
        "common_misreadings": ["positions are permanent roles", "systemic explanation absolves conduct", "the four conditions exhaust social life"],
        "open_checks": ["connect power-and-systems practice", "add workshop evidence", "map complementarities and disputes"],
    },
}


JOURNEY = {
    "id": "journey_inquiry_governance_and_intervention",
    "title": "Inquiry, governance and intervention",
    "subtitle": "A route through SSM, boundary critique, organisational cybernetics, systemic governance, leverage and human systems.",
    "summary": "Moves from inquiry into contested situations through explicit boundary judgement and organisational design to systemic governance, intervention and whole-system conduct.",
    "audience": "Practitioners choosing among systems approaches and asking what each makes possible, what it assumes and what it leaves to other traditions.",
    "duration_minutes": 18,
    "steps": [
        ("Peter Checkland", "Begin with inquiry", "Checkland's action research treats messy situations as occasions for learning rather than as fully specified systems awaiting optimisation."),
        ("Soft Systems Methodology (SSM)", "Model purposeful activity", "SSM uses explicit worldviews and purposeful activity models to structure comparison and learning without claiming that the model is the world."),
        ("Werner Ulrich", "Ask who defines relevance", "Ulrich makes the normative assumptions of systems practice inspectable through Critical Systems Heuristics."),
        ("Boundary critique", "Examine the reference system", "Boundary critique tests who benefits, who decides, what counts as knowledge and which people and consequences are treated as outside."),
        ("Raul Espejo", "Move from model to organisational cybernetics", "Espejo extends management cybernetics into methods for clarifying identity, diagnosis, design and implementation."),
        ("Viplan", "Organise diagnosis and design", "Viplan makes the method of using VSM explicit rather than treating a VSM diagram as a sufficient intervention."),
        ("Ray Ison", "Treat systems thinking as practice", "Ison's systems praxeology keeps practitioner, situation, methods, traditions and institutional conditions in view."),
        ("Systemic governance", "Distribute governing capacity", "Systemic governance concerns relations, institutions, learning and accountability across interacting systems, not command by a single centre."),
        ("Donella Meadows", "Intervene without fantasies of control", "Meadows combines structural analysis with humility, learning, information integrity and attention to the good of the whole."),
        ("Leverage points", "Distinguish intervention levels", "Parameters, feedback, information, rules, goals and paradigms are different intervention locations. Direction and context matter as much as location."),
        ("Barry Oshry", "See position and whole-system process", "Oshry explains recurrent human experience through positions and whole-system processes rather than personality alone."),
        ("Ivo Velitchkov", "Preserve variety and make meaning explicit", "Velitchkov's work links viability, organisational balance, requisite inefficiency and explicit semantic representation."),
        ("Patrick Hoverstadt", "Join cybernetics, laws, design and strategy", "Hoverstadt's practice connects VSM, systems laws, organisation design and relational strategy."),
    ],
}


def node_record(spec: dict[str, Any]) -> dict[str, Any]:
    sources = spec["source_ids"]
    tags = ["systems", "human_lineage", "expertise", "release_0_13"]
    if spec["entity_type"] in {"method_or_methodology", "practice"}:
        tags.append("practice")
    return {
        "id": spec["id"],
        "label": spec["label"],
        "entity_type": spec["entity_type"],
        "description": spec["description"],
        "aliases": enc(spec.get("aliases", [])),
        "boundary_ring": "0",
        "inclusion_reason": "expertise_and_public_sources_release_0_13",
        "status": "accepted",
        "source_ids": enc(sources),
        "set_tags": enc(tags),
        "espoused_labels": "[]",
        "observed_clusters": "[]",
        "canonical_definition": spec["description"],
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
        "publication_level": "profile" if spec.get("profile") else "described",
        "public_stub_text": "",
        "public_source_count": len(sources),
        "no_public_link_count": 0,
    }


def profile_record(node: dict[str, Any], spec: dict[str, Any]) -> dict[str, Any]:
    return {
        "node_id": node["id"],
        "title": node["label"],
        "profile_status": "curator_checked_public_sources",
        "canonical_definition": node["description"],
        "summary": spec["summary"],
        "why_it_matters": spec["why_it_matters"],
        "key_distinctions": enc(spec["key_distinctions"]),
        "historical_lineage": enc(spec["historical_lineage"]),
        "logical_antecedents": enc(spec["logical_antecedents"]),
        "dependent_subsequents": enc(spec["dependent_subsequents"]),
        "practice_connections": enc(spec["practice_connections"]),
        "espoused_lineages": "[]",
        "observed_clusters": "[]",
        "common_misreadings": enc(spec["common_misreadings"]),
        "open_checks": enc(spec["open_checks"]),
        "source_ids": node["source_ids"],
        "evidence_ids": "[]",
        "last_researched": GENERATED,
        "review_status": "curator_checked_public_sources",
        "reviewed_by": "Benjamin P Taylor",
        "reviewed_at": GENERATED,
        "editorial_note": "Developed from public primary, institutional and publisher sources. Open to correction, rival interpretation and stronger evidence.",
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
    confidence: str = "0.88",
    claim_status: str = "accepted",
) -> dict[str, Any]:
    return {
        "id": edge_id,
        "source": source,
        "target": target,
        "relation_type": relation_type,
        "relation_family": relation_family,
        "directed": directed,
        "dependency_kind": "",
        "confidence": confidence,
        "claim_status": claim_status,
        "source_ids": enc(source_ids),
        "evidence_ids": "[]",
        "source_locator": "Release 0.13 public primary, institutional and publisher sources",
        "valid_from": "",
        "valid_to": "",
        "scope_conditions": "The wording is limited to the named public sources. Authorship, methodological development, conceptual dependence and practical use remain distinct claims.",
        "assertion_mode": "asserted",
        "inference_method": "curatorial synthesis of public primary, institutional and publisher sources",
        "claim_id": "",
        "reviewed_by": "Benjamin P Taylor",
        "reviewed_at": GENERATED,
        "notes": notes,
        "plain_phrase": phrase,
        "public_review_label": "supported working statement" if claim_status == "accepted" else "contested working statement",
    }


def make_observations(metrics: dict[str, Any], data: dict[str, Any]) -> dict[str, Any]:
    entries = metrics["public_entries"]
    profiles = metrics["developed_profiles"]
    typed = metrics["typed_edges"]
    substantive = metrics["substantive_edges"]
    people = metrics["people_total"]
    initials = metrics["initial_form_people"]
    profile_share = round(100 * profiles / entries, 1) if entries else 0
    substantive_share = round(100 * substantive / typed, 1) if typed else 0
    initials_share = round(100 * initials / people, 1) if people else 0
    top_source = metrics["source_concentration"][0] if metrics["source_concentration"] else {"title": "No source", "uses": 0}
    entity_counts = metrics.get("entity_counts", {})
    publications = entity_counts.get("publication", 0)
    methods = entity_counts.get("method_or_methodology", 0)
    new_expertise_ids = {spec["id"] for spec in NODE_SPECS}
    new_expertise_edges = [edge for edge in data.get("edges", []) if str(edge.get("id", "")).startswith("e_13_")]
    observations = [
        {
            "id": "breadth_outpaces_depth",
            "title": "Breadth still outruns depth",
            "kind": "measurement plus interpretation",
            "measurement": f"The atlas has {entries} public entries and {profiles} developed profiles. {profile_share}% of entries have the fuller profile structure.",
            "interpretation": "The atlas remains stronger as a territory marker than as a uniformly deep critical reference. A named entry and a developed account are different editorial products.",
            "implication": "Depth work should follow contested bridge concepts, practitioner use and high-consequence ambiguities rather than raw entry counts.",
            "test": "The gap should narrow through sourced profiles and practice relations without pretending that every item deserves equal depth.",
        },
        {
            "id": "two_graph_regimes",
            "title": "Provenance and argument form different graphs",
            "kind": "measurement plus design inference",
            "measurement": f"There are {typed} typed public edges; {substantive} are conceptual, historical, human, practice or contestation relations. The substantive share is {substantive_share}%.",
            "interpretation": "Authorship and collection membership answer different questions from dependence, influence, critique and use. A dense provenance layer is not evidence of conceptual agreement.",
            "implication": "Layer controls and ordinary-language relation phrases should remain central to the interface.",
            "test": "Readers should be able to say which relation family they are viewing and what changed when they switch it.",
        },
        {
            "id": "expertise_needs_relations",
            "title": "Expertise becomes useful through inspectable relations",
            "kind": "release measurement plus editorial interpretation",
            "measurement": f"This release adds {len(new_expertise_ids)} developed or described expertise entries and {len(new_expertise_edges)} typed relations among people, works, concepts, methods and practice.",
            "interpretation": "A person record alone says little. Expertise becomes navigable when named works, methods, conceptual distinctions, collaborators and practice connections are represented separately and linked with evidence.",
            "implication": "Future expert profiles should be developed as constellations rather than biographies or lists of titles.",
            "test": "A reader should be able to enter through a person, work or method and recover the same evidence-backed constellation by different routes.",
        },
        {
            "id": "catalogue_is_not_critique",
            "title": "Cataloguing is not critical coverage",
            "kind": "inventory measurement plus epistemic caution",
            "measurement": f"The graph contains {publications} publications and {methods} maintained methods or methodologies, while only {profiles} entries of all types have developed profiles.",
            "interpretation": "Bibliographic presence establishes that a work belongs in scope. It does not establish the work's argument, influence, quality, limitations or relation to practice.",
            "implication": "Coverage claims need explicit maturity levels: inventoried, described, developed, compared and critically reviewed.",
            "test": "Public coverage reports should state both structural inclusion and interpretive depth, never one aggregate percentage.",
        },
        {
            "id": "practice_is_peripheral",
            "title": "Practice remains thinner than the method inventory",
            "kind": "measurement plus curatorial inference",
            "measurement": "The isolate pattern remains concentrated among intervention skills, laws, tools, methods and publications rather than the small conceptual core.",
            "interpretation": "Lists of methods and capabilities have accumulated faster than evidence about how they are taught, combined, resisted and changed in use.",
            "implication": "Practice cases, project histories, teaching lineages and comparative method use should receive deliberate connection work.",
            "test": "The practice layer should develop multiple sourced routes between concepts, methods, settings, people and consequences.",
        },
        {
            "id": "source_monoculture",
            "title": "Auditability is not source diversity",
            "kind": "measurement plus evidential risk",
            "measurement": f"The most reused source is ‘{top_source['title']}’, attached to {top_source['uses']} public nodes or edges.",
            "interpretation": "One source can establish repeated bibliographic facts without independently corroborating meanings, influence or quality. Reuse can look like consensus when it is only shared provenance.",
            "implication": "Primary works, publisher metadata, archives, reviews and critical accounts should be combined at the smallest supportable statement.",
            "test": "Source concentration should fall for developed claims even where collection-level sources remain useful for inventory.",
        },
        {
            "id": "identity_resolution",
            "title": "The people layer still carries identity-resolution debt",
            "kind": "measurement plus data-quality risk",
            "measurement": f"{initials} of {people} people — {initials_share}% — are represented by initial-form labels.",
            "interpretation": "Initials can record an authorship string but cannot guarantee a unique person. They invite duplicate records, mistaken mergers and false lineage claims.",
            "implication": "Add full names, authority identifiers, affiliations and paper-level checks before deepening those records.",
            "test": "No initial-only person should acquire interpretive or lineage edges without successful identity resolution.",
        },
        {
            "id": "neighbourhoods_are_stale",
            "title": "Published neighbourhoods are hypotheses, not natural schools",
            "kind": "measurement plus model warning",
            "measurement": f"Published neighbourhoods contain {metrics['published_neighbourhood_members']} unique nodes, while {metrics['substantive_connected_nodes']} nodes are now connected; {metrics['connected_nodes_outside_neighbourhoods']} connected nodes sit outside the older grouping pass.",
            "interpretation": "A cluster is produced by the current edges, exclusions, resolution and seed. It should not be mistaken for a discovered natural taxonomy.",
            "implication": "Recompute neighbourhoods when the substantive graph changes materially and preserve the method and change record.",
            "test": "Readers should be able to inspect why entries share a neighbourhood and when that assignment changed.",
        },
        {
            "id": "bridge_concepts",
            "title": "Bridge concepts deserve disproportionate scrutiny",
            "kind": "network measurement plus editorial inference",
            "measurement": "Feedback, recursion, boundary, viability, requisite variety and the Viable System Model continue to have markedly higher substantive degree than most entries.",
            "interpretation": "A bridge entry shapes many possible reading routes. Loose wording there propagates farther than a weakness in a peripheral record.",
            "implication": "Bridge entries need rival definitions, scope conditions, primary sources and practice examples before they are used as navigation hubs.",
            "test": "Alternative routes and counter-accounts should reduce dependence on any one bridge without hiding genuine centrality.",
        },
        {
            "id": "map_of_attention",
            "title": "The gaps map curatorial attention as much as the field",
            "kind": "second-order observation",
            "measurement": f"{metrics['substantive_isolated_nodes']} entries are isolated in the substantive graph, while the largest substantive component contains {metrics['largest_substantive_component']} entries.",
            "interpretation": "Isolation often records missing source work, relation vocabulary or research attention; it does not show that an idea is naturally peripheral.",
            "implication": "Treat isolates as hypotheses about missing work and test them with sources from different traditions.",
            "test": "A broader and more varied source programme should alter which entries appear central, peripheral or absent.",
        },
        {
            "id": "automated_overreading",
            "title": "Structured data reduces ambiguity but does not remove overreading",
            "kind": "data-model observation",
            "measurement": "The atlas records typed relations, status, source IDs and scope conditions, while source granularity and profile depth still vary sharply.",
            "interpretation": "Explicit semantics reduce the tendency to collapse every connection into ‘related to’. They cannot stop a reader or automated system from turning inventory into influence or provisional wording into settled fact.",
            "implication": "Any generated account should expose the entries, relation types and sources used and state when the graph is silent or contested.",
            "test": "Outputs should become more qualified, not more fluent, when evidence is thin or contradictory.",
        },
    ]
    return {
        "generated": GENERATED,
        "release": RELEASE,
        "author": "Benjamin P Taylor, curator",
        "method_note": "Measurements are recalculated from the public graph on every build. Interpretations, implications and tests are kept separate and remain open to challenge.",
        "metrics": metrics,
        "observations": observations,
        "publication_controls": [item.get("id") for item in data.get("publication_controls", []) if item.get("id")],
        "publication_controls_url": "https://github.com/antlerboy/the-necessary-tangle/blob/main/documentation/publication-safety.md",
        "next_tests": [
            "Recompute neighbourhoods from the current substantive graph and publish the algorithm and change record.",
            "Resolve initial-only people before adding interpretive lineage edges.",
            "Develop the highest-traffic bridge entries with rival accounts and item-level sources.",
            "Connect methods and intervention skills to documented cases rather than competence lists alone.",
            "Report inventory breadth and critical depth separately in every major coverage claim.",
        ],
    }


def write_ai_document(report: dict[str, Any]) -> None:
    metrics = report["metrics"]
    lines = [
        "# AI observations",
        "",
        f"Generated for release `{report['release']}` on {report['generated']}.",
        "",
        report["method_note"],
        "",
        "## Measured state",
        "",
        f"- {metrics['public_entries']} public entries; {metrics['developed_profiles']} developed profiles.",
        f"- {metrics['typed_edges']} typed public edges; {metrics['substantive_edges']} substantive edges.",
        f"- {metrics['substantive_connected_nodes']} substantively connected entries and {metrics['substantive_isolated_nodes']} substantive isolates.",
        f"- {metrics['sources']} sources, of which {metrics['sources_with_public_links']} have public links.",
        "",
    ]
    for observation in report["observations"]:
        lines.extend([
            f"## {observation['title']}",
            "",
            f"**Basis:** {observation['kind']}.",
            "",
            f"**Measured:** {observation['measurement']}",
            "",
            f"**Interpretation:** {observation['interpretation']}",
            "",
            f"**Implication:** {observation['implication']}",
            "",
            f"**Test:** {observation['test']}",
            "",
        ])
    lines.extend([
        "## Publication controls",
        "",
        "The public record exposes the controls which govern publication: public-only payloads, source-level provenance, explicit status, human review, licence boundaries, automated scans, release validation and versioned backups.",
        "",
        "See [publication safety and controls](publication-safety.md).",
        "",
    ])
    (DOCUMENTATION / "ai-observations.md").write_text("\n".join(lines), encoding="utf-8")


def write_expertise_document() -> None:
    (DOCUMENTATION / "expertise-additions.md").write_text(
        """# Expertise-led additions in release 0.13

People are developed through their public work, concepts, methods, sources and practice relations.

## Management cybernetics and organisational design

- Ivo Velitchkov: viability, Essential Balances, requisite inefficiency and explicit semantic graphs.
- Patrick Hoverstadt: the Viable System Model, systems laws, organisation design, Patterns of Strategy and transformation.
- Raul Espejo and Alfonso Reyes: organisational cybernetics, Viplan and *Organizational Systems*.

## Inquiry, boundary and practice

- Peter Checkland: Soft Systems Methodology and *Systems Thinking, Systems Practice*.
- Werner Ulrich: Critical Systems Heuristics, boundary critique and the twelve boundary questions.
- Ray Ison and Ed Straw: Systems Thinking in Practice, systems praxeology and systemic governance.

## Intervention and human systems

- Donella Meadows and Diana Wright: *Thinking in Systems*, *Leverage Points* and *Dancing With Systems*.
- Barry Oshry: system-sight, recurring relational positions and the Organic Systems Framework.

Each developed entry records its sources, key distinctions, lineage, practice connections, common confusions and open checks. Authorship, methodological development, conceptual dependence and practical use are represented as different relation types.
""",
        encoding="utf-8",
    )


def write_intake_document() -> None:
    (DOCUMENTATION / "contribution-intake.md").write_text(
        """# Contribution intake

Public contributions enter through visible GitHub issues or pull requests. Nothing submitted through the website changes the atlas automatically.

## Intake routes

1. Structured site submissions, labelled `site-submission` and `awaiting-curator-review`.
2. Research and coverage issues maintained in the repository.
3. Pull requests containing source, data, documentation or software changes.

## Decision rule

A proposal is checked for identity, duplication, wording, evidence, rights, public safety and compatibility with the data model. It may be accepted, revised, retained as disputed, deferred or declined. Submitting a proposal does not confer editorial authority.

## Evidence rule

A contributor may identify a question, source or correction. Public statements still require public evidence or a complete bibliographic citation. Authorship, influence, conceptual dependence, teaching, criticism and practical use remain distinct claims.

## Attribution

Accepted material is attributed where appropriate. Expertise is represented through inspectable work and evidence.
""",
        encoding="utf-8",
    )


def write_publication_standards() -> None:
    legacy = DOCUMENTATION / "feedback-ledger.md"
    if legacy.exists():
        legacy.unlink()
    (DOCUMENTATION / "publication-standards.md").write_text(
        """# Publication standards

## Evidence

- People are represented through their work, expertise and inspectable public sources.
- A source is attached only to the statement it can support.
- Authorship, influence, teaching, criticism, conceptual dependence and practical use remain distinct relations.
- Inventory coverage is not described as critical, interpretive or full-text coverage.
- Unpublished material may identify leads but is not itself public evidence.

## Release control

- Public data excludes private paths, credentials and unlicensed extracts.
- AI observations are regenerated from current graph measures on every build.
- Each release must pass the complete validator set and JavaScript checks.
- Publication remains a named human responsibility.
""",
        encoding="utf-8",
    )


def write_scio_document(data: dict[str, Any]) -> None:
    approach_ids = [
        "method_or_methodology_confrontation_analysis_conan",
        "method_or_methodology_critical_systems_heuristics_csh",
        "method_or_methodology_informed_group_dynamics",
        "method_or_methodology_interactive_management",
        "method_or_methodology_interactive_planning",
        "method_or_methodology_mosaic_transformation",
        "method_or_methodology_multi_methodology_including_sosm",
        "method_or_methodology_patterns_of_strategy",
        "method_or_methodology_socio_technical_systems",
        "method_or_methodology_soft_systems_methodology_ssm",
        "method_or_methodology_syntegration_team_syntegrity",
        "method_or_methodology_system_dynamics",
        "method_or_methodology_viable_system_model_vsm",
    ]
    nodes = {node["id"]: node for node in data.get("nodes", []) if node.get("id")}
    rows = []
    for node_id in approach_ids:
        node = nodes[node_id]
        rows.append(f"| {node['label']} | {node['publication_level']} | {node['public_source_count']} |")
    text = """# SCiO coverage

SCiO is represented as a professional body, source corpus, practitioner network and training provider. Appearance in its competency framework or course catalogue establishes that SCiO recognises or teaches an approach; it does not prove that approach or make SCiO the sole authority on it.

## Thirteen approach families in the current competency-derived inventory

| Approach | Atlas depth | Public source count |
|---|---:|---:|
""" + "\n".join(rows) + """

## Intervention skills

The atlas carries 47 intervention-skill entries inherited from the competency-resource pass. Most remain brief entries. Their existence prevents the method map from pretending that tools alone make an intervention, but source and practice depth remain uneven.

## Developed expertise

The developed layer includes Patrick Hoverstadt, Lucy Loh, Michael C. Jackson, Tony Korycki, Martin Reynolds, Sue Holwell, Ivo Velitchkov, Peter Checkland, Werner Ulrich, Ray Ison, Ed Straw, Raul Espejo, Alfonso Reyes, Donella Meadows, Diana Wright, Barry Oshry and the authors of *Opening the Box*. Their publications, concepts, methods and practice relations are represented separately.

## What remains

- Audit live courses and trainer lineages against the graph.
- Replace competency-resource citations with method-level primary and critical sources.
- Develop thin approach and intervention-skill entries through documented practice.
- Map the human and institutional history of professional capability frameworks.
- Distinguish current professional curricula from the wider systems | cybernetics | complexity field.
"""
    (DOCUMENTATION / "scio-coverage.md").write_text(text, encoding="utf-8")


def scrub_existing(data: dict[str, Any]) -> None:
    nodes = {node["id"]: node for node in data.get("nodes", []) if node.get("id")}
    profiles = {profile["node_id"]: profile for profile in data.get("profiles", []) if profile.get("node_id")}

    for node in nodes.values():
        reason = str(node.get("inclusion_reason", ""))
        if reason.startswith("running_") and reason.endswith("_source_and_depth_pass"):
            node["inclusion_reason"] = "public_source_and_depth_pass"
        elif "practitioner" in reason and reason.endswith("_release_0_12"):
            node["inclusion_reason"] = "practitioner_expertise_coverage_release_0_12"
        tags = parse(node.get("set_tags"))
        if isinstance(tags, list):
            node["set_tags"] = enc([
                "release_0_9_source_depth" if tag.startswith("release_0_9_") else tag
                for tag in tags
            ])

    for profile in profiles.values():
        note = str(profile.get("editorial_note", ""))
        if "release 0.12" in note.casefold() or "release 0.9" in note.casefold():
            profile["editorial_note"] = "Developed from the cited public sources. Open to correction, rival interpretation and stronger evidence."
    opening_box = profiles.get("publication_opening_the_box")
    if opening_box:
        opening_box["why_it_matters"] = "Its compact dialogical form gives readers a route into systems thinking without treating accessibility as a licence to flatten distinctions or remove uncertainty."
        opening_box["editorial_note"] = "Developed from the cited public publication and practitioner sources. Open to correction, rival interpretation and stronger evidence."

    for source in data.get("sources", []):
        if source.get("id") == "src_jobson_definitions_2017":
            source["notes"] = "Unpublished professional framework note; bibliographic record only."
        source_type = str(source.get("source_type", ""))
        if source_type.startswith("private_"):
            source["source_type"] = "unpublished_" + source_type.removeprefix("private_")
            source["publisher"] = "Unpublished author material"
            source["licence"] = "not_publicly_licensed"

    if "person_ivo_velitchkov" in nodes:
        nodes["person_ivo_velitchkov"].update({
            "inclusion_reason": "expertise_and_public_sources_release_0_13",
            "set_tags": enc(["systems", "cybernetics", "practice", "human_lineage", "expertise"]),
            "reviewed_at": GENERATED,
        })
    if "person_patrick_hoverstadt" in nodes:
        nodes["person_patrick_hoverstadt"].update({
            "inclusion_reason": "expertise_and_public_sources_release_0_13",
            "set_tags": enc(["systems", "management_cybernetics", "practice", "human_lineage", "expertise"]),
            "reviewed_at": GENERATED,
        })

    ivo = profiles.get("person_ivo_velitchkov")
    if ivo:
        ivo.update({
            "why_it_matters": "Velitchkov's work joins management cybernetics, viable organisation, dynamic balance, surplus variety, enterprise architecture and explicit semantic representation. It provides substantive routes between organisational practice and knowledge-graph design.",
            "editorial_note": "Developed from public author, publication, professional-body and software sources. Open to correction, rival interpretation and stronger evidence.",
            "last_researched": GENERATED,
            "reviewed_at": GENERATED,
        })
    patrick = profiles.get("person_patrick_hoverstadt")
    if patrick:
        patrick.update({
            "why_it_matters": "Hoverstadt's work connects the Viable System Model, systems laws, organisation diagnosis and design, relational strategy and transformation. It is a major practice-facing body of management cybernetics.",
            "editorial_note": "Developed from public publication, professional-body and method sources. Open to correction, rival interpretation and stronger evidence.",
            "last_researched": GENERATED,
            "reviewed_at": GENERATED,
        })
    viability = profiles.get("concept_viability")
    if viability:
        viability.update({
            "editorial_note": "Developed from public management-cybernetics, systems-practice and evolutionary-theory sources. Distinct theoretical traditions are not collapsed into one consensus account.",
            "last_researched": GENERATED,
            "reviewed_at": GENERATED,
        })
    drift = profiles.get("concept_natural_drift")
    if drift:
        drift.update({
            "why_it_matters": "Natural drift offers a specific theoretical account of evolutionary diversification in which conservation of organisation and structural change are central. It is included as a scoped and contestable account, not as field-wide biological consensus.",
            "editorial_note": "Developed from the cited primary scholarly source and presented with an explicit contestation note.",
            "last_researched": GENERATED,
            "reviewed_at": GENERATED,
        })

    data["nodes"] = list(nodes.values())
    data["profiles"] = list(profiles.values())

    data["accepted_contributions"] = []
    data["contribution_intake"] = {
        "version": "proposal-intake-v2",
        "release": RELEASE,
        "feeds": [
            {"id": "site_submissions", "label": "Structured site submissions", "url": "https://github.com/antlerboy/the-necessary-tangle/issues?q=is%3Aissue+label%3Asite-submission"},
            {"id": "research_issues", "label": "Research and coverage issues", "url": "https://github.com/antlerboy/the-necessary-tangle/issues?q=is%3Aissue+label%3Aresearch"},
            {"id": "pull_requests", "label": "Proposed repository changes", "url": "https://github.com/antlerboy/the-necessary-tangle/pulls"},
        ],
        "submission_marker": "Prepared from The Necessary Tangle",
        "labels": ["site-submission", "awaiting-curator-review"],
        "release_rule": "A proposal changes the atlas only after public evidence, review, validation and an accepted release commit.",
    }

    journeys = {journey["id"]: journey for journey in data.get("journeys", []) if journey.get("id")}
    if "journey_viability_balance_and_strategy" in journeys:
        journey = journeys["journey_viability_balance_and_strategy"]
        journey.update({
            "title": "Viability, balance, semantics and strategy",
            "subtitle": "A route through viable organisation, requisite inefficiency, explicit meaning and relational strategy.",
            "summary": "Connects Ivo Velitchkov's work on viability and organisational balance with Patrick Hoverstadt's management cybernetics, systems laws and strategy practice.",
            "audience": "Practitioners asking what viability demands beyond efficiency and how organisational balance, semantic clarity and strategic relation interact.",
        })
        for step in journey.get("steps", []):
            if step.get("node_id") == "person_ivo_velitchkov":
                step["heading"] = "Viability, balance and explicit meaning"
                step["narrative"] = "Velitchkov's work connects viable organisation to Essential Balances, requisite inefficiency and explicit semantic graphs."
            if step.get("node_id") == "person_patrick_hoverstadt":
                step["heading"] = "Management cybernetics in practice"
                step["narrative"] = "Hoverstadt's work connects VSM, systems laws, organisation design, strategy and transformation."
    data["journeys"] = list(journeys.values())

    mining = []
    for item in data.get("source_mining_register", []):
        if item.get("id") == "mine_roger_james_notebooklm":
            continue
        patched = dict(item)
        if patched.get("id") in {"mine_apprenticeship_workbooks", "mine_company_knowledge"}:
            patched["url"] = "https://github.com/antlerboy/the-necessary-tangle/issues?q=is%3Aissue+label%3Aresearch"
            patched["role"] = "Identify publicly citable people, methods, sources and practical distinctions used in systems-practice teaching and organisational work."
            patched["caveat"] = "Only public evidence or complete public bibliographic citations may support published statements."
            if patched.get("id") == "mine_company_knowledge":
                patched["label"] = "Systems-practice organisational source discovery"
        mining.append(patched)
    data["source_mining_register"] = mining


def main() -> None:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    scrub_existing(data)

    sources = {source["id"]: dict(source) for source in data.get("sources", []) if source.get("id")}
    for source in SOURCE_UPSERTS:
        sources[source["id"]] = {**sources.get(source["id"], {}), **source}
    data["sources"] = list(sources.values())

    relation_types = {item["relation_type"]: dict(item) for item in data.get("relation_types", []) if item.get("relation_type")}
    for relation_type in RELATION_TYPE_UPSERTS:
        relation_types[relation_type["relation_type"]] = {**relation_types.get(relation_type["relation_type"], {}), **relation_type}
    data["relation_types"] = list(relation_types.values())

    nodes = {node["id"]: dict(node) for node in data.get("nodes", []) if node.get("id")}
    for spec in NODE_SPECS:
        nodes[spec["id"]] = {**nodes.get(spec["id"], {}), **node_record(spec)}
    data["nodes"] = list(nodes.values())

    profiles = {profile["node_id"]: dict(profile) for profile in data.get("profiles", []) if profile.get("node_id")}
    for spec in NODE_SPECS:
        if spec.get("profile"):
            profiles[spec["id"]] = {**profiles.get(spec["id"], {}), **profile_record(nodes[spec["id"]], PROFILE_SPECS[spec["id"]])}

    # Deepen the existing SSM and CSH method entries around their principal developers and primary public sources.
    for method_id, person_id, source_ids, summary, why, distinctions, lineage, antecedents, consequents, practice, confusions, checks in [
        (
            "method_or_methodology_soft_systems_methodology_ssm",
            "person_peter_checkland",
            ["src_lancaster_checkland_stsp_1999", "src_wiley_checkland_stsp_1999", "src_scio_cf_resources_2022"],
            "Soft Systems Methodology is a learning-oriented process for inquiring into messy situations through rich pictures, explicit worldviews, purposeful activity models and structured comparison.",
            "SSM separates systemic inquiry from the claim that the situation itself is one objectively specifiable system. It is designed for plural purposes and contested improvement.",
            ["problem vs problem situation", "systematic vs systemic", "model as inquiry device vs model of reality"],
            ["systems engineering", "Peter Checkland's Lancaster action research", "Systems Thinking, Systems Practice"],
            ["purpose", "worldview", "boundary", "learning"],
            ["rich pictures", "root definitions", "purposeful activity models", "accommodations for action"],
            ["public-service inquiry", "organisational learning", "participative problem structuring"],
            ["SSM is a fixed seven-step recipe", "SSM avoids judgement or action", "conceptual models describe real organisations"],
            ["add primary method texts", "map later adaptations and criticism", "connect documented cases"],
        ),
        (
            "method_or_methodology_critical_systems_heuristics_csh",
            "person_werner_ulrich",
            ["src_ulrich_csh_mini_primer_2023", "src_scio_cf_resources_2022"],
            "Critical Systems Heuristics is a framework for reflective and critical practice which makes boundary judgements and their consequences discussable.",
            "CSH provides a disciplined way to examine who benefits, who decides, what counts as knowledge and how those affected can challenge claims to improvement.",
            ["is vs ought", "involved vs affected", "boundary judgement vs neutral fact", "heuristic vs algorithm"],
            ["C. West Churchman", "Werner Ulrich", "critical systems thinking"],
            ["boundary", "purpose", "legitimacy", "knowledge", "power"],
            ["twelve boundary questions", "boundary critique", "citizen competence"],
            ["policy appraisal", "evaluation", "participative inquiry", "professional critique"],
            ["CSH discovers the correct boundary", "the twelve questions are a checklist survey", "only emancipatory projects can use CSH"],
            ["add primary book sources", "connect systemic marginalisation", "develop cases and criticism"],
        ),
    ]:
        node = nodes.get(method_id)
        if not node:
            raise SystemExit(f"Required inherited method missing: {method_id}")
        combined_sources = []
        for source_id in parse(node.get("source_ids")) + source_ids:
            if source_id not in combined_sources:
                combined_sources.append(source_id)
        node.update({
            "source_ids": enc(combined_sources),
            "publication_level": "profile",
            "review_status": "curator_checked_public_sources",
            "reviewed_by": "Benjamin P Taylor",
            "reviewed_at": GENERATED,
            "public_source_count": len(combined_sources),
        })
        spec = {
            "summary": summary,
            "why_it_matters": why,
            "key_distinctions": distinctions,
            "historical_lineage": lineage,
            "logical_antecedents": antecedents,
            "dependent_subsequents": consequents,
            "practice_connections": practice,
            "common_misreadings": confusions,
            "open_checks": checks,
        }
        profiles[method_id] = profile_record(node, spec)
    data["nodes"] = list(nodes.values())
    data["profiles"] = list(profiles.values())

    label_to_id = {fold(node.get("label", "")): node_id for node_id, node in nodes.items()}

    def nid(label: str) -> str:
        key = fold(label)
        if key not in label_to_id:
            raise SystemExit(f"Iteration 0.13 cannot resolve public entry: {label}")
        return label_to_id[key]

    edges = {edge["id"]: dict(edge) for edge in data.get("edges", []) if edge.get("id")}
    for edge_id in [edge_id for edge_id in edges if edge_id.startswith("e_13_")]:
        del edges[edge_id]
    new_edges = [
        edge_record("e_13_stsp_checkland", "publication_systems_thinking_systems_practice", "person_peter_checkland", "authored_by", "documentary", "was authored by", ["src_lancaster_checkland_stsp_1999", "src_wiley_checkland_stsp_1999"], "Official university and publisher records identify Peter Checkland as author."),
        edge_record("e_13_checkland_ssm", "person_peter_checkland", "method_or_methodology_soft_systems_methodology_ssm", "developed", "historical", "developed", ["src_wiley_checkland_stsp_1999"], "The publisher account describes SSM as emerging from Checkland and collaborators' action research."),
        edge_record("e_13_stsp_ssm", "publication_systems_thinking_systems_practice", "method_or_methodology_soft_systems_methodology_ssm", "develops", "conceptual", "develops", ["src_wiley_checkland_stsp_1999"], "The book records the research programme and methodology."),
        edge_record("e_13_stsp_practice", "publication_systems_thinking_systems_practice", "practice_systems_practice", "operationalises", "practice", "puts into practical form", ["src_wiley_checkland_stsp_1999"], "The book explicitly joins systems ideas and real-world practice."),
        edge_record("e_13_primer_ulrich", "publication_mini_primer_critical_systems_heuristics", "person_werner_ulrich", "authored_by", "documentary", "was authored by", ["src_ulrich_csh_mini_primer_2023"], "The primary author page identifies Werner Ulrich and provides the suggested citation."),
        edge_record("e_13_ulrich_csh", "person_werner_ulrich", "method_or_methodology_critical_systems_heuristics_csh", "developed", "historical", "developed", ["src_ulrich_csh_mini_primer_2023"], "Ulrich's primary account traces CSH to his 1983 work."),
        edge_record("e_13_primer_csh", "publication_mini_primer_critical_systems_heuristics", "method_or_methodology_critical_systems_heuristics_csh", "explains", "conceptual", "explains", ["src_ulrich_csh_mini_primer_2023"], "The mini-primer is a maintained primary introduction to CSH."),
        edge_record("e_13_csh_boundary_critique", "method_or_methodology_critical_systems_heuristics_csh", "concept_boundary_critique", "uses", "practice", "uses", ["src_ulrich_csh_mini_primer_2023"], "Ulrich describes systematic boundary critique as CSH's methodological core."),
        edge_record("e_13_boundary_critique_boundary", "concept_boundary_critique", "concept_boundary", "specialises", "conceptual", "specialises", ["src_ulrich_csh_mini_primer_2023"], "Boundary critique concerns the judgements through which relevant systems and claims are delimited."),
        edge_record("e_13_hidden_ison", "publication_hidden_power_systems_thinking", "person_ray_ison", "authored_by", "documentary", "was authored by", ["src_routledge_hidden_power_2020"], "Routledge identifies Ray Ison as co-author."),
        edge_record("e_13_hidden_straw", "publication_hidden_power_systems_thinking", "person_ed_straw", "authored_by", "documentary", "was authored by", ["src_routledge_hidden_power_2020"], "Routledge identifies Ed Straw as co-author."),
        edge_record("e_13_ison_governance", "person_ray_ison", "concept_systemic_governance", "developed", "historical", "develops", ["src_ou_ray_ison_profile_2026", "src_routledge_hidden_power_2020"], "The official profile and publisher page associate Ison's work with systemic governance."),
        edge_record("e_13_hidden_governance", "publication_hidden_power_systems_thinking", "concept_systemic_governance", "develops", "conceptual", "develops", ["src_routledge_hidden_power_2020"], "The book develops principles and institutional implications for systemic governing."),
        edge_record("e_13_hidden_practice", "publication_hidden_power_systems_thinking", "practice_systems_practice", "operationalises", "practice", "puts into practical form", ["src_routledge_hidden_power_2020"], "The publisher describes the book as an applied systems-thinking account of governance and change."),
        edge_record("e_13_orgsys_espejo", "publication_organizational_systems_vsm", "person_raul_espejo", "authored_by", "documentary", "was authored by", ["src_springer_organizational_systems_2011"], "Springer identifies Raul Espejo as co-author."),
        edge_record("e_13_orgsys_reyes", "publication_organizational_systems_vsm", "person_alfonso_reyes", "authored_by", "documentary", "was authored by", ["src_springer_organizational_systems_2011"], "Springer identifies Alfonso Reyes as co-author."),
        edge_record("e_13_orgsys_vsm", "publication_organizational_systems_vsm", "method_or_methodology_viable_system_model_vsm", "develops", "conceptual", "develops", ["src_springer_organizational_systems_2011"], "The book clarifies application of the VSM to diagnosis and design."),
        edge_record("e_13_orgsys_viplan", "publication_organizational_systems_vsm", "method_or_methodology_viplan", "presents", "documentary", "presents", ["src_springer_organizational_systems_2011"], "Springer's contents describe the Viplan method and methodology."),
        edge_record("e_13_espejo_viplan", "person_raul_espejo", "method_or_methodology_viplan", "developed", "historical", "developed", ["src_springer_organizational_systems_2011"], "Springer describes Viplan as Espejo's method and methodology."),
        edge_record("e_13_viplan_vsm", "method_or_methodology_viplan", "method_or_methodology_viable_system_model_vsm", "operationalises", "practice", "puts into practical form", ["src_springer_organizational_systems_2011"], "Viplan organises diagnosis, design and implementation using organisational cybernetics and VSM."),
        edge_record("e_13_thinking_meadows", "publication_thinking_in_systems", "person_donella_meadows", "authored_by", "documentary", "was authored by", ["src_prh_thinking_in_systems_2008"], "The publisher identifies Donella Meadows as author."),
        edge_record("e_13_thinking_wright", "publication_thinking_in_systems", "person_diana_wright", "edited_by", "documentary", "was edited by", ["src_prh_thinking_in_systems_2008"], "The publisher identifies Diana Wright as editor."),
        edge_record("e_13_thinking_feedback", "publication_thinking_in_systems", "concept_feedback_loops", "explains", "conceptual", "explains", ["src_prh_thinking_in_systems_2008"], "The publisher describes feedback loops among the book's core systems concepts."),
        edge_record("e_13_thinking_sd", "publication_thinking_in_systems", "method_or_methodology_system_dynamics", "translates_for_practice", "practice", "translates for practice", ["src_prh_thinking_in_systems_2008"], "The book brings system-dynamics concepts into accessible practice-facing form."),
        edge_record("e_13_leverage_meadows", "publication_leverage_points_meadows", "person_donella_meadows", "authored_by", "documentary", "was authored by", ["src_meadows_leverage_points"], "The Donella Meadows Project identifies Meadows as author."),
        edge_record("e_13_leverage_concept", "publication_leverage_points_meadows", "concept_leverage_points", "develops", "conceptual", "develops", ["src_meadows_leverage_points"], "The essay presents and qualifies an ordered set of places to intervene."),
        edge_record("e_13_leverage_feedback", "concept_leverage_points", "concept_feedback_loops", "uses", "conceptual", "uses", ["src_meadows_leverage_points"], "Feedback structure and strength are among the named intervention levels."),
        edge_record("e_13_dancing_meadows", "publication_dancing_with_systems", "person_donella_meadows", "authored_by", "documentary", "was authored by", ["src_meadows_dancing_with_systems"], "The Donella Meadows Project identifies Meadows as author."),
        edge_record("e_13_dancing_practice", "publication_dancing_with_systems", "practice_systems_practice", "operationalises", "practice", "puts into practical form", ["src_meadows_dancing_with_systems"], "The essay presents disciplines for acting with systems under uncertainty."),
        edge_record("e_13_osf_pub_oshry", "publication_organic_systems_framework", "person_barry_oshry", "authored_by", "documentary", "was authored by", ["src_triarchy_organic_systems_framework_2019"], "The publisher identifies Barry Oshry as author."),
        edge_record("e_13_oshry_osf", "person_barry_oshry", "method_or_methodology_organic_systems_framework", "developed", "historical", "developed", ["src_triarchy_organic_systems_framework_2019", "src_triarchy_barry_oshry_profile"], "The publisher and author profile describe OSF as Oshry's framework."),
        edge_record("e_13_osf_pub_method", "publication_organic_systems_framework", "method_or_methodology_organic_systems_framework", "presents", "documentary", "presents", ["src_triarchy_organic_systems_framework_2019"], "The book presents the Organic Systems Framework and its core processes."),
        edge_record("e_13_osf_practice", "method_or_methodology_organic_systems_framework", "practice_systems_practice", "operationalises", "practice", "puts into practical form", ["src_triarchy_organic_systems_framework_2019", "src_triarchy_barry_oshry_profile"], "OSF is described as a framework for understanding and intervening in organisational life."),
        edge_record("e_13_osf_boundary", "method_or_methodology_organic_systems_framework", "concept_boundary", "uses", "conceptual", "uses", ["src_triarchy_organic_systems_framework_2019"], "OSF treats system experience in relation to whole, part and context."),
        edge_record("e_13_ivo_viability_expertise", "person_ivo_velitchkov", "concept_viability", "specialises_in", "practice", "specialises in", ["src_velitchkov_home_current", "src_scio_essential_balances_2020"], "Velitchkov's public work develops viable organisation and organisational balance."),
        edge_record("e_13_ivo_semantics_expertise", "person_ivo_velitchkov", "concept_explicit_semantics", "specialises_in", "practice", "specialises in", ["src_nodica_repo_2026"], "Nodica and related graph work make explicit semantics a substantive part of Velitchkov's expertise."),
        edge_record("e_13_patrick_vsm_expertise", "person_patrick_hoverstadt", "method_or_methodology_viable_system_model_vsm", "specialises_in", "practice", "specialises in", ["src_scio_fractal_organisation_manual_2026", "src_scio_what_vsm_2024"], "Hoverstadt's books and teaching apply VSM to organisation diagnosis and design."),
        edge_record("e_13_patrick_strategy_expertise", "person_patrick_hoverstadt", "method_or_methodology_patterns_of_strategy", "co_developed", "historical", "co-developed", ["src_scio_patterns_strategy_book_2016"], "The publication record identifies Hoverstadt and Lucy Loh as co-authors of Patterns of Strategy."),
    ]
    for edge in new_edges:
        edges[edge["id"]] = edge
    data["edges"] = list(edges.values())

    steps = [{"node_id": nid(label), "heading": heading, "narrative": narrative} for label, heading, narrative in JOURNEY["steps"]]
    journeys = {journey["id"]: dict(journey) for journey in data.get("journeys", []) if journey.get("id")}
    journeys[JOURNEY["id"]] = {**{key: value for key, value in JOURNEY.items() if key != "steps"}, "steps": steps}
    data["journeys"] = list(journeys.values())

    meta = data.setdefault("meta", {})
    meta.update({
        "release": RELEASE,
        "generated": GENERATED,
        "status": "public alpha on GitHub Pages",
        "iteration_focus": "expertise-led development, refreshed AI observations, deeper systems-practice connections and clean public framing",
        "proposal_intake_version": "proposal-intake-v2",
        "accepted_contribution_count": 0,
        "expertise_additions_url": "https://github.com/antlerboy/the-necessary-tangle/blob/main/documentation/expertise-additions.md",
        "public_knowledge_url": "https://github.com/antlerboy/the-necessary-tangle/blob/main/documentation/public-knowledge.md",
    })

    redirects = data.get("canonical_redirects", {})
    public_nodes = [node for node in data["nodes"] if node.get("public_visibility") == "public" and redirects.get(node["id"], node["id"]) == node["id"]]
    public_ids = {node["id"] for node in public_nodes}
    meta["public_entry_count"] = len(public_nodes)
    meta["described_entry_count"] = len(public_nodes)
    meta["stub_entry_count"] = 0
    meta["profile_count"] = len({profile["node_id"] for profile in data["profiles"] if profile.get("node_id") in public_ids})
    meta["journey_count"] = len(data["journeys"])
    meta["source_count"] = len(data["sources"])
    meta["public_link_source_count"] = sum(bool(source.get("url")) for source in data["sources"])
    meta["no_public_link_source_count"] = sum(not bool(source.get("url")) for source in data["sources"])
    meta["source_mining_register_count"] = len(data.get("source_mining_register", []))

    report = make_observations(graph_metrics(data), data)
    data["ai_observations"] = report

    DOCUMENTATION.mkdir(parents=True, exist_ok=True)
    write_ai_document(report)
    write_expertise_document()
    write_intake_document()
    write_publication_standards()
    write_scio_document(data)

    public_payload = json.dumps(data, ensure_ascii=False)
    hidden_markers = ("data-curator-" + "dot", "curator-" + "notebook-link")
    if any(marker in public_payload for marker in hidden_markers):
        raise SystemExit("Public data contains an obsolete hidden working route")

    rendered = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    DATA_PATH.write_text(rendered, encoding="utf-8")
    DOCS_ASSETS.mkdir(parents=True, exist_ok=True)
    (DOCS_ASSETS / "public-data.json").write_text(rendered, encoding="utf-8")
    (DOCS_ASSETS / "public-data.js").write_text(
        "window.TANGLE_DATA = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n",
        encoding="utf-8",
    )
    print(
        f"Applied {RELEASE}: {meta['public_entry_count']} entries, {meta['profile_count']} profiles, "
        f"{meta['journey_count']} journeys, {meta['source_count']} sources and {len(new_edges)} new expertise relations."
    )


if __name__ == "__main__":
    main()
