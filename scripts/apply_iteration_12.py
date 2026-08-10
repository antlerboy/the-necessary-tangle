#!/usr/bin/env python3
"""Apply release 0.12: practitioner omissions, explicit semantics and contribution intake."""
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
RELEASE = "0.12-practitioner-intake-alpha"
GENERATED = "2026-08-10"


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


SOURCE_UPSERTS: list[dict[str, Any]] = [
    {
        "id": "src_velitchkov_home_current",
        "title": "Ivo Velitchkov",
        "source_type": "primary_author_page",
        "quality_tier": "A",
        "access": "public",
        "url": "https://velitchkov.eu/",
        "date": "",
        "notes": "Ivo Velitchkov's public home page links his books, blogs, public slide decks and other work. It establishes authorship and discovery routes, not independent evaluation.",
        "creators": "[\"Ivo Velitchkov\"]",
        "doi": "",
        "isbn": "",
        "publisher": "Ivo Velitchkov",
        "licence": "source_terms",
        "archived_url": "",
        "content_hash": "",
        "review_status": "checked",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_scio_essential_balances_2020",
        "title": "Essential Balances: Stop Looking and Start Seeing What Makes Organizations Work",
        "source_type": "official_professional_body_book_page",
        "quality_tier": "B",
        "access": "public_metadata",
        "url": "https://www.systemspractice.org/resources/essential-balances-stop-looking-and-start-seeing-what-makes-organizations-work",
        "date": "2020-11",
        "notes": "SCiO bibliographic and descriptive page for Ivo Velitchkov's book. It supports the three named balances and publication metadata; page-level claims still require the book itself.",
        "creators": "[\"Ivo Velitchkov\"]",
        "doi": "",
        "isbn": "978-1838338619",
        "publisher": "KVISTGAARD",
        "licence": "publisher_terms",
        "archived_url": "",
        "content_hash": "",
        "review_status": "checked",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_scio_requisite_inefficiency_2014",
        "title": "Requisite inefficiency",
        "source_type": "official_professional_body_talk_page",
        "quality_tier": "B",
        "access": "public",
        "url": "https://www.systemspractice.org/resources/requisite-inefficiency",
        "date": "2014-09",
        "notes": "SCiO record of Ivo Velitchkov's proposal that some apparent inefficiency preserves excess variety needed for longer-term viability.",
        "creators": "[\"Ivo Velitchkov\"]",
        "doi": "",
        "isbn": "",
        "publisher": "SCiO",
        "licence": "site_terms",
        "archived_url": "",
        "content_hash": "",
        "review_status": "checked",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_nodica_repo_2026",
        "title": "Nodica: RDF graph visualisation with image-filled nodes",
        "source_type": "primary_software_repository",
        "quality_tier": "A",
        "access": "public",
        "url": "https://github.com/kvistgaard/nodica",
        "date": "2026",
        "notes": "Primary source repository for Ivo Velitchkov's Nodica RDF graph visualisation. Used to establish the project's stated purpose, implementation and licence, not to endorse every semantic choice.",
        "creators": "[\"Ivo Velitchkov\"]",
        "doi": "",
        "isbn": "",
        "publisher": "GitHub",
        "licence": "MIT",
        "archived_url": "",
        "content_hash": "",
        "review_status": "checked",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_maturana_mpodozis_natural_drift_2000",
        "title": "The origin of species by means of natural drift",
        "source_type": "peer_reviewed_article",
        "quality_tier": "A",
        "access": "public",
        "url": "https://revistaschilenas.uchile.cl/handle/2250/62395",
        "date": "2000",
        "notes": "Primary scholarly article in which Humberto Maturana and Jorge Mpodozis propose natural drift as the generative mechanism of evolutionary diversification and treat natural selection as a consequence rather than the mechanism. This is a particular theoretical account, not field-wide consensus.",
        "creators": "[\"Humberto Maturana\", \"Jorge Mpodozis\"]",
        "doi": "10.4067/S0716-078X2000000200005",
        "isbn": "",
        "publisher": "Revista Chilena de Historia Natural",
        "licence": "source_terms",
        "archived_url": "",
        "content_hash": "",
        "review_status": "checked_with_contestation_note",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_scio_fractal_organisation_manual_2026",
        "title": "The Fractal Organisation Manual: How to diagnose & design organisations using the Viable System Model",
        "source_type": "official_professional_body_book_page",
        "quality_tier": "B",
        "access": "public_metadata",
        "url": "https://www.systemspractice.org/resources/fractal-organisation-manual-how-diagnose-design-organisations-using-viable-system-model",
        "date": "2026-04",
        "notes": "SCiO book page for Patrick Hoverstadt's practice manual, described as distilling thirty years of VSM diagnosis, design and governance work.",
        "creators": "[\"Patrick Hoverstadt\"]",
        "doi": "",
        "isbn": "979-8250847018",
        "publisher": "SCiO",
        "licence": "publisher_terms",
        "archived_url": "",
        "content_hash": "",
        "review_status": "checked",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_scio_patterns_strategy_book_2016",
        "title": "Patterns of Strategy",
        "source_type": "official_professional_body_book_page",
        "quality_tier": "B",
        "access": "public_metadata",
        "url": "https://www.systemspractice.org/resources/patterns-strategy-0",
        "date": "2016-12",
        "notes": "SCiO bibliographic page for Patrick Hoverstadt and Lucy Loh's book, which presents eighty strategy patterns for examining collaboration and competition in a strategic ecosystem.",
        "creators": "[\"Patrick Hoverstadt\", \"Lucy Loh\"]",
        "doi": "",
        "isbn": "978-1138242678",
        "publisher": "Routledge",
        "licence": "publisher_terms",
        "archived_url": "",
        "content_hash": "",
        "review_status": "checked",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_scio_critical_systems_thinking_2024",
        "title": "Critical Systems Thinking: A Practitioner's Guide",
        "source_type": "official_professional_body_book_page",
        "quality_tier": "B",
        "access": "public_metadata",
        "url": "https://www.systemspractice.org/resources/critical-systems-thinking-practitioners-guide",
        "date": "2024-06",
        "notes": "SCiO bibliographic and descriptive page for Michael C. Jackson's guide to critical systems thinking and critical systems practice.",
        "creators": "[\"Michael C. Jackson\"]",
        "doi": "",
        "isbn": "978-1394203574",
        "publisher": "Wiley",
        "licence": "publisher_terms",
        "archived_url": "",
        "content_hash": "",
        "review_status": "checked",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_scio_opening_box_2024",
        "title": "Opening the Box: Systems Thinking for Transformative Conversations",
        "source_type": "official_professional_body_book_page",
        "quality_tier": "B",
        "access": "public_metadata",
        "url": "https://www.systemspractice.org/resources/opening-box-systems-thinking-transformative-conversations",
        "date": "2024-09",
        "notes": "SCiO page for a short dialogical introduction to four layers of systems thinking: parts and wholes, nascent development, coherence and metamorphosis.",
        "creators": "[\"Jan De Visch\", \"Miguel Pantaleon\", \"Namrata Arora\", \"Tony Korycki\"]",
        "doi": "",
        "isbn": "",
        "publisher": "SCiO Publications",
        "licence": "publisher_terms",
        "archived_url": "",
        "content_hash": "",
        "review_status": "checked",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_scio_systems_approaches_making_change_2020",
        "title": "Systems Approaches to Making Change: A Practical Guide",
        "source_type": "official_professional_body_book_page",
        "quality_tier": "B",
        "access": "public_metadata",
        "url": "https://www.systemspractice.org/resources/systems-approaches-making-change-practical-guide",
        "date": "2020-02",
        "notes": "SCiO book page for Martin Reynolds, Sue Holwell and Patrick Hoverstadt's practical guide to five systems approaches for making systemic improvement.",
        "creators": "[\"Martin Reynolds\", \"Sue Holwell\", \"Patrick Hoverstadt\"]",
        "doi": "",
        "isbn": "978-1447174714",
        "publisher": "Springer",
        "licence": "publisher_terms",
        "archived_url": "",
        "content_hash": "",
        "review_status": "checked",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_scio_courses_current",
        "title": "SCiO all courses",
        "source_type": "official_professional_body_catalogue",
        "quality_tier": "A",
        "access": "public",
        "url": "https://www.systemspractice.org/courses",
        "date": "2026",
        "notes": "Current public catalogue of SCiO systems-practice and intervention courses. It is used to audit method and trainer coverage, not to establish the independent validity of a method.",
        "creators": "[\"SCiO - Systems and Complexity in Organisation\"]",
        "doi": "",
        "isbn": "",
        "publisher": "SCiO",
        "licence": "site_terms",
        "archived_url": "",
        "content_hash": "",
        "review_status": "checked",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_scio_navigating_complexity_2014",
        "title": "Navigating Complexity",
        "source_type": "official_professional_body_talk_page",
        "quality_tier": "B",
        "access": "public",
        "url": "https://www.systemspractice.org/resources/navigating-complexity",
        "date": "2014-04",
        "notes": "SCiO resource page for Arthur Battram's Navigating Complexity and his practice-oriented account of managing as if people mattered.",
        "creators": "[\"Arthur Battram\"]",
        "doi": "",
        "isbn": "185835899X",
        "publisher": "The Industrial Society / SCiO resource page",
        "licence": "source_terms",
        "archived_url": "",
        "content_hash": "",
        "review_status": "checked",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_cybcom_archive_current",
        "title": "CYBCOM - Cybernetic Communications Discussion Group",
        "source_type": "public_community_archive",
        "quality_tier": "C",
        "access": "public",
        "url": "https://groups.google.com/g/cybcom",
        "date": "1997-",
        "notes": "Public discussion archive and source-discovery corpus. Messages can establish circulation and conversation, not automatically priority, accuracy or influence.",
        "creators": "[]",
        "doi": "",
        "isbn": "",
        "publisher": "CYBCOM / Google Groups",
        "licence": "archive_terms",
        "archived_url": "",
        "content_hash": "",
        "review_status": "registered_for_source_mining",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_asc_archives_current",
        "title": "American Society for Cybernetics archives",
        "source_type": "professional_archive",
        "quality_tier": "A",
        "access": "public",
        "url": "https://asc-cybernetics.org/archives/",
        "date": "",
        "notes": "ASC index of cyberneticians' archives, audio and video collections, newsletters and related publications. It is a discovery register requiring item-level provenance.",
        "creators": "[\"American Society for Cybernetics\"]",
        "doi": "",
        "isbn": "",
        "publisher": "American Society for Cybernetics",
        "licence": "site_terms",
        "archived_url": "",
        "content_hash": "",
        "review_status": "registered_for_source_mining",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
]

SOURCE_PATCHES: dict[str, dict[str, Any]] = {
    "src_grammar_2ed_2025": {
        "creators": "[\"Patrick Hoverstadt\"]",
        "isbn": "979-8298960878",
        "publisher": "SCiO",
        "licence": "publisher_terms",
        "notes": "Current second-edition metadata. The book presents nine systems-thinking patterns and 33 systems laws and principles.",
        "last_checked": GENERATED,
    },
    "src_grammar_presentation_2022": {
        "creators": "[\"Patrick Hoverstadt\"]",
        "publisher": "SCiO",
        "licence": "site_terms",
        "last_checked": GENERATED,
    },
    "src_taylor_reading_list_current": {
        "url": "https://stream.syscoi.com/2024/10/01/updated-rough-draft-systems-complexity-cybernetics-reading-list/",
        "title": "Updated rough draft systems | complexity | cybernetics reading list",
        "publisher": "Systems Community of Inquiry",
        "notes": "Benjamin P Taylor's deliberately partial, practice-facing reading list. The current top recommendations include Grammar of Systems, Critical Systems Thinking: A Practitioner's Guide, Opening the Box and Essential Balances. It is an orientation and discovery source, not a neutral canon.",
        "last_checked": GENERATED,
    },
}

NODE_SPECS: list[dict[str, Any]] = [
    {
        "id": "organisation_scio_systems_and_complexity_in_organisation",
        "label": "SCiO — Systems and Complexity in Organisation",
        "entity_type": "organisation",
        "description": "A practitioner-owned professional body that develops and supports systems practice through a competency framework, SysBoK, accreditation, events, communities and professional-development courses.",
        "aliases": ["SCiO", "Systems and Complexity in Organisation"],
        "source_ids": ["src_scio_professional_body_current", "src_scio_accreditation_current", "src_scio_courses_current"],
        "x": -0.07,
        "y": 0.48,
        "profile": True,
    },
    {
        "id": "person_ivo_velitchkov",
        "label": "Ivo Velitchkov",
        "entity_type": "person",
        "description": "A systems and cybernetics practitioner, enterprise architect and author whose work includes Essential Balances, requisite inefficiency, personal knowledge graphs and explicit semantic graph visualisation.",
        "aliases": [],
        "source_ids": ["src_velitchkov_home_current", "src_scio_essential_balances_2020", "src_scio_requisite_inefficiency_2014", "src_nodica_repo_2026"],
        "x": -0.15,
        "y": 0.26,
        "profile": True,
    },
    {
        "id": "publication_essential_balances",
        "label": "Essential Balances",
        "entity_type": "publication",
        "description": "Ivo Velitchkov's book on three recurrent organisational tensions: autonomy and cohesion, stability and diversity, and exploration and exploitation, treated as dynamic balances rather than choices to settle once.",
        "aliases": ["Essential Balances: Stop Looking and Start Seeing What Makes Organizations Work"],
        "source_ids": ["src_scio_essential_balances_2020", "src_velitchkov_home_current"],
        "x": -0.10,
        "y": 0.21,
        "profile": True,
    },
    {
        "id": "concept_requisite_inefficiency",
        "label": "Requisite inefficiency",
        "entity_type": "concept",
        "description": "The proposal that some slack, redundancy or apparently unused variety is necessary if a system is to retain the capacity to respond and remain viable under conditions not already anticipated.",
        "aliases": [],
        "source_ids": ["src_scio_requisite_inefficiency_2014"],
        "x": -0.24,
        "y": 0.18,
        "profile": True,
    },
    {
        "id": "concept_natural_drift",
        "label": "Natural drift",
        "entity_type": "concept",
        "description": "Maturana and Mpodozis's account of evolution as the conservation and diversification of organism–niche relations through structural drift, with natural selection treated as a consequence of that history rather than its directing mechanism.",
        "aliases": ["natural phylogenic drift", "natural evolutionary drift"],
        "source_ids": ["src_maturana_mpodozis_natural_drift_2000"],
        "x": 0.04,
        "y": 0.12,
        "profile": True,
    },
    {
        "id": "person_jorge_mpodozis",
        "label": "Jorge Mpodozis",
        "entity_type": "person",
        "description": "A Chilean biologist who co-authored the natural-drift account of evolutionary diversification with Humberto Maturana.",
        "aliases": [],
        "source_ids": ["src_maturana_mpodozis_natural_drift_2000"],
        "x": 0.09,
        "y": 0.08,
        "profile": False,
    },
    {
        "id": "concept_explicit_semantics",
        "label": "Explicit semantics",
        "entity_type": "concept",
        "description": "The practice of making the meaning of data types, relations, direction, evidence status and scope machine-readable and inspectable rather than leaving interpretation to labels, layout or convention alone.",
        "aliases": ["semantic explicitness"],
        "source_ids": ["src_nodica_repo_2026", "src_scio_sysbok_current"],
        "x": 0.20,
        "y": 0.13,
        "profile": True,
    },
    {
        "id": "tool_nodica",
        "label": "Nodica",
        "entity_type": "tool",
        "description": "An open-source RDF graph visualisation developed by Ivo Velitchkov, used here as a comparator for explicit semantics and graph navigation rather than as the atlas's underlying implementation.",
        "aliases": [],
        "source_ids": ["src_nodica_repo_2026"],
        "x": 0.25,
        "y": 0.17,
        "profile": True,
    },
    {
        "id": "person_patrick_hoverstadt",
        "label": "Patrick Hoverstadt",
        "entity_type": "person",
        "description": "A systems practitioner, author and educator known for applied work on the Viable System Model, systems laws and principles, organisation design, Patterns of Strategy and Mosaic Transformation.",
        "aliases": [],
        "source_ids": ["src_grammar_2ed_2025", "src_scio_fractal_organisation_manual_2026", "src_scio_patterns_strategy_book_2016", "src_scio_what_vsm_2024", "src_scio_mosaic_2013"],
        "x": -0.34,
        "y": -0.03,
        "profile": True,
    },
    {
        "id": "publication_grammar_of_systems_ii",
        "label": "The Grammar of Systems II",
        "entity_type": "publication",
        "description": "Patrick Hoverstadt's guide to nine systems-thinking patterns and 33 systems laws and principles, intended to make the foundations of systems thinking usable in inquiry, design, strategy and transformation.",
        "aliases": ["Grammar of Systems", "The Grammar of Systems II: From Order to Chaos and Back Again"],
        "source_ids": ["src_grammar_2ed_2025", "src_grammar_presentation_2022"],
        "x": -0.41,
        "y": -0.02,
        "profile": True,
    },
    {
        "id": "publication_fractal_organisation_manual",
        "label": "The Fractal Organisation Manual",
        "entity_type": "publication",
        "description": "Patrick Hoverstadt's practice manual for using the Viable System Model in organisational diagnosis, design, governance and the development of organisational agility.",
        "aliases": ["The Fractal Organisation Manual: How to diagnose & design organisations using the Viable System Model"],
        "source_ids": ["src_scio_fractal_organisation_manual_2026"],
        "x": -0.37,
        "y": -0.09,
        "profile": True,
    },
    {
        "id": "person_lucy_loh",
        "label": "Lucy Loh",
        "entity_type": "person",
        "description": "A systems and strategy practitioner who co-developed Patterns of Strategy with Patrick Hoverstadt and co-authored the book presenting the approach.",
        "aliases": [],
        "source_ids": ["src_scio_patterns_strategy_book_2016"],
        "x": -0.51,
        "y": -0.18,
        "profile": True,
    },
    {
        "id": "person_michael_c_jackson",
        "label": "Michael C. Jackson",
        "entity_type": "person",
        "description": "A systems scholar and author whose work develops critical systems thinking, creative holism and critical systems practice for selecting and combining systems approaches under conditions of complexity and pluralism.",
        "aliases": ["Mike Jackson", "Michael Jackson (systems scholar)"],
        "source_ids": ["src_scio_critical_systems_thinking_2024"],
        "x": 0.17,
        "y": 0.32,
        "profile": True,
    },
    {
        "id": "publication_critical_systems_thinking_practitioners_guide",
        "label": "Critical Systems Thinking: A Practitioner's Guide",
        "entity_type": "publication",
        "description": "Michael C. Jackson's guide to critical systems thinking and critical systems practice, treating methodological diversity as a resource for working with multidimensional complexity rather than as a choice of one universal method.",
        "aliases": [],
        "source_ids": ["src_scio_critical_systems_thinking_2024"],
        "x": 0.23,
        "y": 0.34,
        "profile": True,
    },
    {
        "id": "publication_opening_the_box",
        "label": "Opening the Box",
        "entity_type": "publication",
        "description": "A short dialogical introduction to systems thinking organised around four layers: parts and wholes, nascent development, coherence and metamorphosis, written to support transformative conversations.",
        "aliases": ["Opening the Box: Systems Thinking for Transformative Conversations"],
        "source_ids": ["src_scio_opening_box_2024"],
        "x": 0.31,
        "y": 0.36,
        "profile": True,
    },
    {
        "id": "person_jan_de_visch",
        "label": "Jan De Visch",
        "entity_type": "person",
        "description": "A systems practitioner and co-author of Opening the Box, working on dialogical, developmental and regenerative approaches to organisational systems and collaboration.",
        "aliases": [],
        "source_ids": ["src_scio_opening_box_2024"],
        "x": 0.35,
        "y": 0.40,
        "profile": False,
    },
    {
        "id": "person_miguel_pantaleon",
        "label": "Miguel Pantaleon",
        "entity_type": "person",
        "description": "A systems practitioner and co-author of Opening the Box, contributing to its four-layer account of systems thinking and transformative conversation.",
        "aliases": [],
        "source_ids": ["src_scio_opening_box_2024"],
        "x": 0.39,
        "y": 0.38,
        "profile": False,
    },
    {
        "id": "person_namrata_arora",
        "label": "Namrata Arora",
        "entity_type": "person",
        "description": "A systems practitioner and co-author of Opening the Box, contributing to its accessible dialogical presentation of systems thinking.",
        "aliases": [],
        "source_ids": ["src_scio_opening_box_2024"],
        "x": 0.42,
        "y": 0.34,
        "profile": False,
    },
    {
        "id": "person_tony_korycki",
        "label": "Tony Korycki",
        "entity_type": "person",
        "description": "A systems practitioner, educator and SCiO contributor associated with the early SysBoK, Critical Systems Heuristics, systems laws practice and Opening the Box.",
        "aliases": [],
        "source_ids": ["src_korycki_2014", "src_scio_opening_box_2024", "src_scio_sysbok_current"],
        "x": 0.30,
        "y": 0.43,
        "profile": True,
    },
    {
        "id": "publication_systems_approaches_making_change",
        "label": "Systems Approaches to Making Change",
        "entity_type": "publication",
        "description": "A practical guide by Martin Reynolds, Sue Holwell and Patrick Hoverstadt presenting a range of systems approaches for making systemic improvement in complex situations of change and uncertainty.",
        "aliases": ["Systems Approaches to Making Change: A Practical Guide"],
        "source_ids": ["src_scio_systems_approaches_making_change_2020"],
        "x": 0.06,
        "y": 0.39,
        "profile": True,
    },
    {
        "id": "person_martin_reynolds",
        "label": "Martin Reynolds",
        "entity_type": "person",
        "description": "A systems scholar and practitioner associated with critical systems thinking, environmental responsibility and the teaching and application of multiple systems approaches.",
        "aliases": [],
        "source_ids": ["src_scio_systems_approaches_making_change_2020"],
        "x": 0.02,
        "y": 0.43,
        "profile": False,
    },
    {
        "id": "person_sue_holwell",
        "label": "Sue Holwell",
        "entity_type": "person",
        "description": "A systems practitioner and educator associated with Soft Systems Methodology, systems practice and the co-editing and co-authorship of practical systems-approach guides.",
        "aliases": [],
        "source_ids": ["src_scio_systems_approaches_making_change_2020"],
        "x": 0.08,
        "y": 0.44,
        "profile": False,
    },
    {
        "id": "person_arthur_battram",
        "label": "Arthur Battram",
        "entity_type": "person",
        "description": "A complexity practitioner and author whose work translated complexity ideas into organisational and local-government practice, including Navigating Complexity and the Learning from Complexity materials.",
        "aliases": [],
        "source_ids": ["src_scio_navigating_complexity_2014"],
        "x": 0.48,
        "y": 0.18,
        "profile": True,
    },
    {
        "id": "publication_navigating_complexity_battram",
        "label": "Navigating Complexity",
        "entity_type": "publication",
        "description": "Arthur Battram's practice-facing guide to complexity theory in business and management, developed from work that brought complexity ideas into organisational and local-government settings.",
        "aliases": ["Navigating Complexity: The Essential Guide to Complexity Theory in Business and Management"],
        "source_ids": ["src_scio_navigating_complexity_2014"],
        "x": 0.52,
        "y": 0.22,
        "profile": True,
    },
]

PROFILE_SPECS: dict[str, dict[str, Any]] = {
    "organisation_scio_systems_and_complexity_in_organisation": {
        "summary": "SCiO is represented here as a professional and practitioner institution, not as the owner of one systems doctrine. Its public work includes competency, accreditation, SysBoK, events and a growing course catalogue.",
        "why_it_matters": "The atlas previously contained SCiO documents and method lists without a public organisational entry. That made the sources look detached from the community and institutional work that produced and maintains them.",
        "key_distinctions": ["professional body vs single school", "competency framework vs settled canon", "course provision vs independent validation", "community memory vs complete history"],
        "historical_lineage": ["practitioner network", "SysBoK and competency work", "professional accreditation", "international chapters and training"],
        "logical_antecedents": ["systems practice", "professional competence", "intervention skill", "reflective judgement"],
        "dependent_subsequents": ["SCiO competency framework", "SysBoK", "professional accreditation", "course catalogue"],
        "practice_connections": ["systems-practitioner development", "method training", "peer learning", "professional standards"],
        "common_misreadings": ["SCiO represents a single official systems theory", "appearance in a SCiO catalogue proves a method", "the competency list is complete and final"],
        "open_checks": ["map the people and institutions behind the competency framework", "audit the current course catalogue against the atlas each release", "distinguish SCiO institutional history from the broader field"],
    },
    "person_ivo_velitchkov": {
        "summary": "Ivo Velitchkov works across systems and cybernetics, organisation, enterprise architecture and knowledge representation. His contributions are especially useful where viable organisation, dynamic balance, surplus variety and explicit semantics meet.",
        "why_it_matters": "His omission exposed two failures: the atlas underweighted the curator's practitioner sources, and site-generated contributions were not reconciled with the running feedback thread. Both are now treated as release-level defects.",
        "key_distinctions": ["viability vs fitness", "balance vs static compromise", "necessary slack vs waste", "explicit semantics vs visually implied meaning"],
        "historical_lineage": ["management cybernetics", "autopoiesis and viability", "enterprise architecture", "personal knowledge graphs and RDF"],
        "logical_antecedents": ["viability", "requisite variety", "autonomy", "cohesion", "semantic network"],
        "dependent_subsequents": ["Essential Balances", "requisite inefficiency", "Nodica", "personal knowledge graph work"],
        "practice_connections": ["enterprise architecture", "organisational diagnosis", "strategy", "knowledge representation"],
        "common_misreadings": ["balance means equal quantities", "inefficiency is always a defect", "graph visualisation alone supplies semantics"],
        "open_checks": ["itemise Velitchkov's public slide decks and publications", "trace the relation between Essential Balances and earlier cybernetic sources", "compare Nodica's RDF model with this atlas's typed JSON graph"],
    },
    "publication_essential_balances": {
        "summary": "Essential Balances invites readers to notice three recurrent organisational tensions and cultivate the ability to keep adjusting them rather than seek one permanently correct point.",
        "why_it_matters": "It provides a practitioner bridge between management cybernetics and ordinary organisational judgement, while resisting the tendency to treat one pole of a tension as the solution.",
        "key_distinctions": ["autonomy and cohesion", "stability and diversity", "exploration and exploitation", "dynamic adjustment vs midpoint compromise"],
        "historical_lineage": ["management cybernetics", "organisational paradox", "ambidexterity and exploration/exploitation"],
        "logical_antecedents": ["autonomy", "cohesion", "viability", "variety"],
        "dependent_subsequents": ["organisational diagnostic habits", "balance-aware intervention"],
        "practice_connections": ["leadership reflection", "organisation design", "strategy", "team and institutional diagnosis"],
        "common_misreadings": ["balance means eliminating tension", "the three balances are independent", "one snapshot can establish the right balance"],
        "open_checks": ["add page-level citations from the book", "compare with Barry Oshry and Stafford Beer without collapsing the traditions", "document cases and criticism"],
    },
    "concept_requisite_inefficiency": {
        "summary": "Requisite inefficiency names the possibility that unused capacity, redundancy, variation or slack may be regulatory resource rather than waste.",
        "why_it_matters": "Efficiency programmes can remove the very variety needed to absorb disturbance, learn, experiment and respond. The concept forces an explicit question: inefficient relative to which purpose, boundary and timescale?",
        "key_distinctions": ["slack vs waste", "short-term utilisation vs long-term viability", "redundancy vs duplication without purpose", "efficiency for one part vs capacity of the whole"],
        "historical_lineage": ["Ashby's requisite variety", "management cybernetics", "organisational resilience and slack"],
        "logical_antecedents": ["requisite variety", "viability", "adaptation", "timescale"],
        "dependent_subsequents": ["capacity buffers", "experimentation", "resilient organisation"],
        "practice_connections": ["resource decisions", "operational excellence", "resilience", "portfolio and workforce design"],
        "common_misreadings": ["all inefficiency is good", "buffers need no purpose", "efficiency and viability are opposites"],
        "open_checks": ["seek independent applications and criticism", "distinguish related concepts such as slack, redundancy and reserve variety"],
    },
    "concept_natural_drift": {
        "summary": "Natural drift is Maturana and Mpodozis's evolutionary account centred on the conservation and diversification of organism–niche relations. It explicitly contests accounts which make natural selection the directing mechanism.",
        "why_it_matters": "Ivo Velitchkov's site submission asked the atlas to distinguish viability from fitness and the viable from the fittest. The independent source supports adding the theory, but not presenting it as settled evolutionary biology.",
        "key_distinctions": ["viability vs comparative fitness", "structural drift vs externally directing pressure", "organism–niche relation vs organism alone", "theory proposal vs consensus"],
        "historical_lineage": ["Maturana and Mpodozis", "autopoiesis", "structural coupling", "biology of cognition"],
        "logical_antecedents": ["autopoiesis", "adaptation", "structural coupling", "lineage"],
        "dependent_subsequents": ["natural phylogenic drift", "co-drift", "survival of the viable formulation"],
        "practice_connections": ["caution in importing evolutionary metaphors into organisations", "distinguishing persistence from optimisation"],
        "common_misreadings": ["natural drift is ordinary genetic drift", "the article abolishes selection as an observed consequence", "the theory can be transferred directly to organisations"],
        "open_checks": ["add contemporary biological criticism and reception", "separate the 1992 and 2000 formulations", "trace uses in cybernetics without laundering metaphor into fact"],
    },
    "concept_explicit_semantics": {
        "summary": "Explicit semantics makes the commitments of a graph inspectable: what kinds of entities exist, what a relation means, whether it is directed, what supports it, how certain it is and where it applies.",
        "why_it_matters": "A visually attractive line can create a false genealogy if its meaning is left implicit. The atlas already has typed relations; this release documents the semantic contract and makes it part of validation rather than a private implementation detail.",
        "key_distinctions": ["semantic type vs visual style", "relation meaning vs spatial proximity", "evidence source vs discovery source", "canonical identity vs label", "graph semantics vs algorithmic neighbourhood"],
        "historical_lineage": ["semantic networks", "RDF and knowledge graphs", "typed graph data", "systems bodies of knowledge"],
        "logical_antecedents": ["distinction", "identity", "relation", "scope", "provenance"],
        "dependent_subsequents": ["machine-readable graph", "validation rules", "inspectable evidence lines"],
        "practice_connections": ["data modelling", "knowledge graph design", "editorial review", "AI retrieval and constrained inference"],
        "common_misreadings": ["an ontology is neutral", "RDF automatically makes claims true", "a graph layout is the semantics"],
        "open_checks": ["publish JSON Schema or SHACL-compatible constraints", "test semantic export and round-trip", "compare with Nodica and other graph tools"],
    },
    "tool_nodica": {
        "summary": "Nodica is an RDF graph visualisation project with image-filled nodes. It is used here as a live comparator for semantic graph presentation and as evidence that the contributor's question about explicit semantics was not merely rhetorical.",
        "why_it_matters": "The Necessary Tangle uses typed data but has not yet published a standard RDF export. Nodica makes the gap visible and supplies a practical comparison point without requiring the atlas to copy its interface or technology.",
        "key_distinctions": ["visualisation tool vs knowledge corpus", "RDF data vs this atlas's JSON model", "comparator vs dependency"],
        "historical_lineage": ["RDF", "semantic web", "knowledge graph visualisation"],
        "logical_antecedents": ["explicit semantics", "semantic network", "graph visualisation"],
        "dependent_subsequents": ["RDF display", "image-rich graph browsing"],
        "practice_connections": ["knowledge graph exploration", "semantic data presentation"],
        "common_misreadings": ["the atlas now runs on Nodica", "RDF removes editorial judgement", "the two projects have identical purposes"],
        "open_checks": ["compare data-model features explicitly", "prototype a public RDF export from the atlas", "test interoperability rather than infer it"],
    },
    "person_patrick_hoverstadt": {
        "summary": "Patrick Hoverstadt is represented as a practitioner-author whose work joins management cybernetics, systems laws, organisation design, strategy and transformation.",
        "why_it_matters": "The atlas already contained his methods, book corpus and SCiO resources while omitting the person. That broke the stated purpose of tracing human as well as conceptual lineages.",
        "key_distinctions": ["VSM application vs VSM authorship", "systems laws vs slogans", "strategy as relational fit vs static plan", "organisation design vs organisational charting"],
        "historical_lineage": ["Stafford Beer and the Viable System Model", "management cybernetics", "strategy and organisational design", "SCiO professional practice"],
        "logical_antecedents": ["viability", "requisite variety", "structural coupling", "systems laws"],
        "dependent_subsequents": ["Grammar of Systems II", "Fractal Organisation Manual", "Patterns of Strategy", "Mosaic Transformation"],
        "practice_connections": ["organisation diagnosis", "organisation design", "strategy", "transformation", "systems education"],
        "common_misreadings": ["Patrick originated the VSM", "a systems law is context-free prescription", "Patterns of Strategy is conventional strategic planning"],
        "open_checks": ["develop project case evidence", "trace collaborations around SCiO and Patterns of Strategy", "distinguish first and second editions of Grammar of Systems"],
    },
    "publication_grammar_of_systems_ii": {
        "summary": "The Grammar of Systems II presents nine patterns of systems thinking and 33 laws and principles as a practical foundation for reasoning about order, change, complexity and uncertainty.",
        "why_it_matters": "Its laws were already itemised in the atlas, but the publication and author were hidden in metadata. This release makes the book, its person and the existing law corpus visible together.",
        "key_distinctions": ["thinking pattern vs law or principle", "law vs deterministic prediction", "structural complexity vs dynamic complexity"],
        "historical_lineage": ["general systems and cybernetics", "management cybernetics", "systems laws and principles"],
        "logical_antecedents": ["emergence", "holism", "modelling", "feedback", "complexity", "uncertainty"],
        "dependent_subsequents": ["systems-laws courses", "practitioner diagnostics", "the atlas's 33 law entries"],
        "practice_connections": ["systems education", "diagnosis", "transformation design", "strategy"],
        "common_misreadings": ["the 33 items are universal equations", "naming a law supplies a diagnosis", "one book exhausts systems thinking"],
        "open_checks": ["add page-level locators", "compare the first and second editions", "record criticism and alternative formulations"],
    },
    "publication_fractal_organisation_manual": {
        "summary": "The Fractal Organisation Manual turns long practice with the Viable System Model into explicit approaches for organisational diagnosis, design, governance and agility.",
        "why_it_matters": "The atlas was strong on VSM concepts but weak on current practitioner manuals and documented method transfer. This book is an important bridge from model to use.",
        "key_distinctions": ["recursive organisation vs repeated organisation chart", "diagnosis vs design", "governance vs central control"],
        "historical_lineage": ["Stafford Beer", "Viable System Model", "The Fractal Organization", "applied organisational cybernetics"],
        "logical_antecedents": ["viability", "recursion", "autonomy", "cohesion", "requisite variety"],
        "dependent_subsequents": ["VSM diagnostic approaches", "VSM design approaches", "governance approaches"],
        "practice_connections": ["organisation design", "governance", "agility", "multi-organisational diagnosis"],
        "common_misreadings": ["fractal means visually self-similar boxes", "the VSM specifies one organisation structure", "diagnosis can ignore purpose and environment"],
        "open_checks": ["review the full text", "map its nine practical approaches", "add independently described cases"],
    },
    "person_lucy_loh": {
        "summary": "Lucy Loh co-developed Patterns of Strategy and co-authored its main publication, bringing systemic and management-science practice to strategic fit and manoeuvre.",
        "why_it_matters": "Crediting a method to only one visible practitioner would reproduce the very false lineage problem the atlas is meant to resist.",
        "key_distinctions": ["co-development vs secondary association", "relational strategy vs internal planning"],
        "historical_lineage": ["systems practice", "management science", "structural coupling and strategic fit"],
        "logical_antecedents": ["strategy", "structural coupling", "power", "time"],
        "dependent_subsequents": ["Patterns of Strategy"],
        "practice_connections": ["strategy development", "competitive and collaborative ecosystems"],
        "common_misreadings": ["Patterns of Strategy is solely Patrick Hoverstadt's work"],
        "open_checks": ["develop Lucy Loh's broader practitioner profile and case history"],
    },
    "person_michael_c_jackson": {
        "summary": "Michael C. Jackson develops critical systems thinking and critical systems practice as ways of working constructively with the field's methodological plurality.",
        "why_it_matters": "The atlas contains many methods but can still imply that selecting a method is a technical matching exercise. Jackson's work places philosophy, power, pluralism and critical reflection inside the choice and combination of approaches.",
        "key_distinctions": ["pluralism vs eclecticism", "method critique vs method rejection", "critical systems practice vs one methodology"],
        "historical_lineage": ["critical systems thinking", "creative holism", "systems methodologies"],
        "logical_antecedents": ["methodological pluralism", "power", "emancipation", "systems practice"],
        "dependent_subsequents": ["critical systems practice", "Critical Systems Thinking: A Practitioner's Guide"],
        "practice_connections": ["method selection", "multi-methodology", "leadership and wicked problems"],
        "common_misreadings": ["pluralism means using everything", "critical means merely negative", "methodologies can be combined without philosophical consequences"],
        "open_checks": ["add primary texts across Jackson's career", "represent major critiques and later developments"],
    },
    "publication_critical_systems_thinking_practitioners_guide": {
        "summary": "A contemporary guide to the foundations, mindset, methodologies and practical conduct of critical systems practice.",
        "why_it_matters": "It is one of the curator's four strongest current reading recommendations and directly addresses how a practitioner can use methodological diversity without hiding ethical and political choices.",
        "key_distinctions": ["critical systems thinking vs generic critical thinking", "critical systems practice vs multi-method recipe", "complexity dimensions vs one problem type"],
        "historical_lineage": ["critical systems thinking", "creative holism", "systems methodologies"],
        "logical_antecedents": ["systems practice", "pluralism", "power", "methodology critique"],
        "dependent_subsequents": ["critical systems practice"],
        "practice_connections": ["wicked problems", "leadership", "methodological choice and combination"],
        "common_misreadings": ["the book recommends one best method", "critical systems practice can be reduced to a matrix"],
        "open_checks": ["add page-level sources and cases", "map each methodology discussed to existing entries"],
    },
    "publication_opening_the_box": {
        "summary": "Opening the Box is a compact, dialogical route into systems thinking through four proposed layers and a sustained challenge to surface-level explanation.",
        "why_it_matters": "It is designed for people who may find the field forbidding. Ivo Velitchkov's usability feedback makes that purpose especially relevant to the atlas itself.",
        "key_distinctions": ["parts and wholes", "nascent development", "coherence", "metamorphosis", "dialogue vs textbook exposition"],
        "historical_lineage": ["systems thinking", "dialogical learning", "SCiO practitioner community"],
        "logical_antecedents": ["whole and part", "emergence", "coherence", "change"],
        "dependent_subsequents": ["transformative systems conversations"],
        "practice_connections": ["systems education", "facilitation", "leadership conversation", "food-system inquiry"],
        "common_misreadings": ["the four layers are a complete ontology", "accessibility means simplification without loss"],
        "open_checks": ["map the four layers to existing entries", "record practitioner use and critique"],
    },
    "person_tony_korycki": {
        "summary": "Tony Korycki connects systems-practice education, Critical Systems Heuristics, systems-law practice, SCiO's early SysBoK work and accessible public communication.",
        "why_it_matters": "The repository already cited a Tony Korycki SysBoK source but had no public person entry. This hid a contributor behind a document node.",
        "key_distinctions": ["body-of-knowledge contribution vs sole authorship", "systems law practice vs recital", "critical heuristic vs generic checklist"],
        "historical_lineage": ["SCiO", "critical systems heuristics", "systems-practice education"],
        "logical_antecedents": ["boundary critique", "systems laws", "intervention skill"],
        "dependent_subsequents": ["Opening the Box", "SCiO SysBoK contributions"],
        "practice_connections": ["systems education", "supply-chain diagnosis", "critical reflection"],
        "common_misreadings": ["a competency-framework contributor owns the whole framework"],
        "open_checks": ["develop the wider contributor network around the SCiO SysBoK"],
    },
    "publication_systems_approaches_making_change": {
        "summary": "A practice guide presenting multiple systems approaches as resources for improving complex situations rather than as rival brands from which one must be chosen permanently.",
        "why_it_matters": "It connects Patrick Hoverstadt's work to Martin Reynolds and Sue Holwell and gives the atlas a public route from systems-method diversity to practical change.",
        "key_distinctions": ["approach repertoire vs universal method", "systemic improvement vs implementation programme", "practice guide vs complete field history"],
        "historical_lineage": ["Open University systems practice", "critical systems thinking", "management cybernetics"],
        "logical_antecedents": ["systems practice", "methodological pluralism", "complex situations"],
        "dependent_subsequents": ["systems-practice teaching", "combined method use"],
        "practice_connections": ["change and intervention", "method choice", "professional development"],
        "common_misreadings": ["five approaches cover the whole field", "tools are interchangeable without assumptions"],
        "open_checks": ["review the full contents and map each approach precisely", "add case-level evidence"],
    },
    "person_arthur_battram": {
        "summary": "Arthur Battram translated complexity ideas into organisational and local-government practice while resisting both command-and-control simplification and fashionable complexity incantation.",
        "why_it_matters": "Benjamin's own material repeatedly credits Battram as a practical source and critical companion. His absence was another sign that the atlas had underweighted the curator's actual practitioner constellation.",
        "key_distinctions": ["complexity as practice resource vs management fashion", "people-centred management vs machine assumptions"],
        "historical_lineage": ["complexity theory", "organisational learning", "local-government management"],
        "logical_antecedents": ["complexity", "self-organisation", "learning"],
        "dependent_subsequents": ["Navigating Complexity", "Learning from Complexity materials"],
        "practice_connections": ["local government", "organisational change", "management development"],
        "common_misreadings": ["complexity licenses managerial passivity", "natural management is a complete method"],
        "open_checks": ["itemise the Learning from Complexity pack", "add public bibliographic and archival sources", "trace influence in UK public services"],
    },
    "publication_navigating_complexity_battram": {
        "summary": "A late-1990s guide that brought complexity theory into business and management practice, associated with Arthur Battram's work in local government and organisational development.",
        "why_it_matters": "It is a longstanding source in Benjamin's own thinking and helps explain a practitioner lineage which is not captured by complexity-science paper collections alone.",
        "key_distinctions": ["complexity theory vs complication", "practical translation vs original scientific research"],
        "historical_lineage": ["complexity science popularisation", "organisational learning", "UK management practice"],
        "logical_antecedents": ["complexity", "emergence", "self-organisation"],
        "dependent_subsequents": ["complexity-informed management practice"],
        "practice_connections": ["management", "local government", "organisation change"],
        "common_misreadings": ["the book is a current scientific synthesis", "a business guide settles complexity theory"],
        "open_checks": ["obtain and review the full text", "record edition metadata and citations", "compare with contemporary complexity-management texts"],
    },
}

# Existing entries that become more useful in this release.
UPGRADE_IDS = {
    "method_or_methodology_patterns_of_strategy",
    "knowledge_domain_systems_laws",
}

JOURNEY = {
    "id": "journey_viability_balance_and_strategy",
    "title": "From viable to useful: balance, semantics and strategy",
    "subtitle": "A contributor-led route through viability, slack, natural drift, explicit meaning and applied cybernetics.",
    "summary": "Starts with Ivo Velitchkov's viability challenge, follows the organisational balances and semantic questions it opens, then connects them to Patrick Hoverstadt's applied work.",
    "audience": "Practitioners asking what viability demands beyond efficiency and how a typed graph should show the difference.",
    "duration_minutes": 16,
    "steps": [
        ("Viability", "Viable is not simply fittest", "Viability concerns continuing as a recognisable whole under change. It is not automatically the same as comparative evolutionary fitness, short-term survival or maximum efficiency."),
        ("Natural drift", "A specific evolutionary challenge", "Maturana and Mpodozis propose natural drift as the generative process and selection as a consequence. The atlas includes this as a contested theory, not as biological consensus."),
        ("Ivo Velitchkov", "The contributor and practitioner", "Ivo's site submission exposed both a missing conceptual distinction and a broken intake loop. His wider work links viability to organisational balance and semantic representation."),
        ("Essential Balances", "Keep tensions alive", "Autonomy and cohesion, stability and diversity, exploration and exploitation are not dilemmas to eliminate but conditions to keep sensing and adjusting."),
        ("Requisite inefficiency", "Do not optimise away the response", "Slack and redundancy can carry the unused variety that becomes essential when conditions change."),
        ("Explicit semantics", "Say what the line means", "A graph should expose entity type, relation type, direction, evidence, status and scope. Visual closeness is not enough."),
        ("Nodica", "A live semantic comparator", "Nodica provides an RDF-based graph visualisation comparator. The atlas remains a different project but now documents the comparison and its own semantic contract."),
        ("Patrick Hoverstadt", "Practitioner lineage made visible", "Patrick's existing methods and sources were present without the person. The human lineage now connects VSM, systems laws, strategy and transformation."),
        ("The Grammar of Systems II", "Patterns and laws", "The Grammar distinguishes thinking patterns from laws and principles, offering a structured route into systemic reasoning."),
        ("Patterns of Strategy", "Strategy in relationship", "Patterns of Strategy models strategic fit, power, time and response across an ecosystem rather than treating strategy as an internal plan."),
    ],
}


def node_record(spec: dict[str, Any]) -> dict[str, Any]:
    sources = spec["source_ids"]
    return {
        "id": spec["id"],
        "label": spec["label"],
        "entity_type": spec["entity_type"],
        "description": spec["description"],
        "aliases": enc(spec.get("aliases", [])),
        "boundary_ring": "0",
        "inclusion_reason": "feedback_and_practitioner_coverage_release_0_12",
        "status": "accepted",
        "source_ids": enc(sources),
        "set_tags": enc(["systems", "practice", "human_lineage", "release_0_12"]),
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
        "editorial_note": "Developed in release 0.12 from public sources and feedback triage. The entry remains open to correction, rival accounts and stronger evidence.",
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
        "source_locator": "Release 0.12 public practitioner and publication sources",
        "valid_from": "",
        "valid_to": "",
        "scope_conditions": "The wording is limited to the named public sources. Bibliographic inclusion and organisational association do not establish wider intellectual influence.",
        "assertion_mode": "asserted",
        "inference_method": "curatorial synthesis of public primary, scholarly and professional-body sources",
        "claim_id": "",
        "reviewed_by": "Benjamin P Taylor",
        "reviewed_at": GENERATED,
        "notes": notes,
        "plain_phrase": phrase,
        "public_review_label": "supported working statement" if claim_status == "accepted" else "contested working statement",
    }


def write_docs(data: dict[str, Any]) -> None:
    DOCUMENTATION.mkdir(parents=True, exist_ok=True)

    (DOCUMENTATION / "explicit-semantics.md").write_text("""# Explicit semantics

The Necessary Tangle uses an explicitly typed graph. The semantics are not the positions of dots on a screen.

## Entity types

Each maintained entry has a stable identifier, a public label, an entity type, a publication level and a canonical identity. A person, publication, concept, practice, organisation and method are different kinds of thing even when their names are similar.

## Relation types

Every connection has a named relation type and a plain-language phrase. The record also states whether it is directed. `authored by`, `teacher of`, `historical precursor`, `formal prerequisite`, `uses`, `critiques` and `often confused with` are not interchangeable forms of `related to`.

## Evidence and status

A connection records source identifiers, evidence locators where available, confidence, statement status, scope conditions, review status and the method by which the statement was formed. A discovery source can lead to evidence without itself proving the statement.

## Identity and redirects

Canonical identifiers remain stable when labels change. Alternate names and spelling variants are aliases. A canonical redirect records that two records resolve to one maintained identity; it is not a claim that the terms have always been historically identical.

## Graph views

Map layers filter relation families. Algorithmic neighbourhoods are provisional descriptions of the current graph, not natural schools. Spatial proximity, colour and clustering do not add unstated semantic relations.

## Nodica comparison

[Nodica](https://github.com/kvistgaard/nodica) is an RDF graph visualisation and a useful comparator. The Necessary Tangle currently publishes typed JSON records and does not claim RDF compatibility. A future interoperability test should export the graph, preserve relation direction and provenance, and round-trip it without losing the editorial distinctions above.

## Next technical step

Publish a machine-readable schema and test an RDF/JSON-LD export. The test is not whether another tool can draw the nodes. It is whether meaning, direction, evidence, status, scope and canonical identity survive the translation.
""", encoding="utf-8")

    (DOCUMENTATION / "contribution-intake.md").write_text("""# Contribution intake

Site submissions do not edit the atlas. They create public GitHub issues for review.

## Three feeds checked before a release

1. The curator's running feedback issue.
2. Every site-generated issue carrying the `site-submission` label or the generated submission marker.
3. Standing research and coverage issues.

A release must reconcile all three. A summary of the running thread alone is not a complete feedback pass.

## Automated triage

The `Triage site submissions` workflow recognises the marker added by the public form, applies `site-submission` and `awaiting-curator-review`, and sweeps existing open issues when the workflow is introduced or changed. The labels identify intake; they do not accept the proposed content.

## Editorial states

- `awaiting-curator-review`: received, not yet assessed.
- `needs-source`: a useful question or proposal without adequate public evidence.
- `accepted-for-research`: accepted as a research lead, not yet a public statement.
- `incorporated`: represented in a validated release with an explanatory comment.
- closed as declined, duplicate or out of scope: decision and reason remain public.

## Ivo Velitchkov's viability submission

Issue #21 was successfully created by the website. It was initially missed because the release process read the running feedback thread but did not sweep separate site-generated issues. Release 0.12 fixes the intake process and incorporates the question through independently sourced entries for viability and natural drift. The issue is credited as the prompt, not used as scholarly evidence.
""", encoding="utf-8")

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
    nodes = {node["id"]: node for node in data["nodes"]}
    rows = []
    for node_id in approach_ids:
        node = nodes[node_id]
        rows.append(f"| {node['label']} | {node['publication_level']} | {node['public_source_count']} |")
    (DOCUMENTATION / "scio-coverage.md").write_text("""# SCiO coverage

SCiO is represented as a professional body, source corpus, practitioner network and training provider. Appearance in its competency framework or course catalogue establishes that SCiO currently recognises or teaches an approach; it does not prove that approach or make SCiO the sole authority on it.

## Thirteen approach families in the current competency-derived inventory

| Approach | Atlas depth | Public source count |
|---|---:|---:|
""" + "\n".join(rows) + """

## Intervention skills

The atlas also carries 47 intervention-skill entries inherited from the competency-resource pass. Most remain brief entries. Their existence prevents the method map from pretending that tools alone make an intervention, but source and practice depth are still uneven.

## People and works deepened in 0.12

The release adds or develops Patrick Hoverstadt, Lucy Loh, Michael C. Jackson, Tony Korycki, Martin Reynolds, Sue Holwell, Ivo Velitchkov and the four authors of Opening the Box. It adds developed publications for Grammar of Systems II, Essential Balances, Critical Systems Thinking, Opening the Box, Systems Approaches to Making Change and The Fractal Organisation Manual.

## What remains

- Audit every live SCiO course and trainer against the graph.
- Replace inherited competency-resource citations with method-level primary and critical sources.
- Develop thin entries for the twelve approach families which are not yet profiles.
- Map the human and institutional history of SysBoK and the competency framework.
- Distinguish SCiO's current curriculum from the wider systems | cybernetics | complexity field.
""", encoding="utf-8")

    (DOCUMENTATION / "reading-list-coverage.md").write_text("""# Reading-list coverage

Benjamin P Taylor's reading list is deliberately partial and idiosyncratic. It is treated as a curator-orientation source, not as a neutral canon.

## Four current top recommendations

| Work | 0.12 status |
|---|---|
| The Grammar of Systems II — Patrick Hoverstadt | Developed publication and author profile; systems-law corpus linked. |
| Critical Systems Thinking: A Practitioner's Guide — Michael C. Jackson | Developed publication and author profile. |
| Opening the Box — Jan De Visch, Miguel Pantaleon, Namrata Arora and Tony Korycki | Developed publication; all four authors represented. |
| Essential Balances — Ivo Velitchkov | Developed publication and author profile. |

## The rest of the list

The list is longer than one release and changes over time. Release 0.12 establishes a maintained coverage audit rather than declaring the whole list complete. Each future pass should record: present or absent; brief or developed; public sources; method and person links; and the reason for deferral or exclusion.

## Related private material

Apprenticeship workbooks and company resources are discovery sources only. They may identify names and references, but public statements must be supported by public evidence or a complete public bibliographic citation. No private URLs or extracts belong in this repository.
""", encoding="utf-8")

    (DOCUMENTATION / "feedback-ledger.md").write_text("""# Running-feedback ledger

This ledger records status, not applause. `Implemented` means visible in a validated release. `First pass` means bounded work exists and depth remains open. `Open` means the research has not been done.

## Implemented or restored

- Curator language, canonical antlerboy links, systems | cybernetics | complexity framing and left-aligned text.
- Clickable cards and ordinary right-clickable internal links.
- CC BY-SA 4.0 content licensing and fuller acknowledgements.
- Discreet bottom-right route to the running feedback thread.
- Contribution and membership routes with named human responsibility for agent-assisted work.
- Full public map default, typed layers, pointer-centred zoom, minimap, focus history, fullscreen and semantic label disclosure.
- Principia Cybernetica first pass and canonical-source register.
- Chris Mowles, complex responsive processes and Murmurations first pass.
- Four additional guided journeys and the six systems-work distinctions.
- Prominent routes to SysCoI, SCiO capability/training and Benjamin's reading list.
- Publication controls, automated public-payload checks and content backups.
- Ivo Velitchkov, Patrick Hoverstadt and their principal works requested in the running thread.
- Explicit semantics documentation and a documented Nodica comparison.
- Site-submission triage across generated issues as well as the running thread.

## First passes with depth still open

- Foundational Papers inventory: itemised breadth exists; independent paper and author depth remains uneven.
- SCiO methods and intervention skills: inventory exists; most entries remain brief.
- Benjamin's reading list: four current headline recommendations are developed; full list audit remains open.
- Arthur Battram and Navigating Complexity: public first pass added; full text and lineage work remain open.
- CYBCOM and ASC archives: registered as discovery corpora; systematic ingestion remains open.

## Open programmes

- Relevant Monoskop review.
- Systematic SysCoI and model.report archive ingestion.
- Comparison of prior maps and bodies of knowledge.
- Gold-standard human lineages for teaching, mentoring, collaboration and institutional transmission.
- Private apprenticeship-workbook and company-knowledge discovery with public-source replacement.
- Roger James's NotebookLM/open-source collection: exact public corpus and permissions still need identification.
- Cybernetics Society mailing-list and archive pass, alongside CYBCOM and ASC.
- Full reading-list audit and development of thin methods, people and works.
- Reader testing of the map and the new start-here route, including Ivo Velitchkov's observation that the whole can feel scary.

## Intake rule

Before each release, check issue #2, all open `site-submission` issues and the standing research issues. Do not describe feedback as complete until all three feeds have been reconciled.
""", encoding="utf-8")


def main() -> None:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))

    # Sources: match by id; preserve inherited records while correcting known metadata.
    sources = {source["id"]: dict(source) for source in data.get("sources", []) if source.get("id")}
    for source_id, patch in SOURCE_PATCHES.items():
        if source_id not in sources:
            raise SystemExit(f"Required source missing for 0.12 patch: {source_id}")
        sources[source_id] = {**sources[source_id], **patch}
    for source in SOURCE_UPSERTS:
        sources[source["id"]] = {**sources.get(source["id"], {}), **source}
    data["sources"] = list(sources.values())

    nodes = {node["id"]: dict(node) for node in data.get("nodes", []) if node.get("id")}
    for spec in NODE_SPECS:
        nodes[spec["id"]] = {**nodes.get(spec["id"], {}), **node_record(spec)}

    # Promote existing Systems Laws and Patterns of Strategy records to public developed entries.
    systems_laws = nodes.get("knowledge_domain_systems_laws")
    if not systems_laws:
        raise SystemExit("Missing inherited Systems laws entry")
    systems_laws.update({
        "description": "Systems laws and principles are recurrent statements about patterns, constraints and dynamics in systems. They support disciplined inquiry but do not operate as context-free prescriptions or deterministic predictions.",
        "canonical_definition": "A maintained domain of named systems patterns, laws and principles whose wording, scope and practical use must be inspected rather than invoked as slogans.",
        "source_ids": enc(["src_grammar_2ed_2025", "src_grammar_presentation_2022", "src_scio_courses_current"]),
        "public_visibility": "public",
        "publication_level": "profile",
        "review_status": "curator_checked_public_sources",
        "reviewed_by": "Benjamin P Taylor",
        "reviewed_at": GENERATED,
        "public_source_count": 3,
        "no_public_link_count": 0,
        "canonical_id": "knowledge_domain_systems_laws",
    })

    patterns = nodes.get("method_or_methodology_patterns_of_strategy")
    if not patterns:
        raise SystemExit("Missing inherited Patterns of Strategy entry")
    patterns.update({
        "description": "Patterns of Strategy is a systemic approach co-developed by Patrick Hoverstadt and Lucy Loh for modelling strategic fit, power, time and response among an organisation and the actors in its ecosystem.",
        "canonical_definition": "A relational strategy methodology using a repertoire of recurring strategic patterns to examine and alter fit among an organisation, competitors, partners, regulators and markets.",
        "source_ids": enc(["src_scio_patterns_strategy_book_2016", "src_scio_patterns_strategy_2024"]),
        "publication_level": "profile",
        "review_status": "curator_checked_public_sources",
        "reviewed_by": "Benjamin P Taylor",
        "reviewed_at": GENERATED,
        "public_source_count": 2,
        "no_public_link_count": 0,
    })
    data["nodes"] = list(nodes.values())

    profiles = {profile["node_id"]: dict(profile) for profile in data.get("profiles", []) if profile.get("node_id")}
    for spec in NODE_SPECS:
        if spec.get("profile"):
            profiles[spec["id"]] = {**profiles.get(spec["id"], {}), **profile_record(nodes[spec["id"]], PROFILE_SPECS[spec["id"]])}

    # Existing profiles deepened by the incoming contribution and practitioner pass.
    viability = profiles.get("concept_viability")
    if not viability:
        raise SystemExit("Missing viability profile")
    viability.update({
        "key_distinctions": enc([
            "viability vs short-term survival",
            "viability vs efficiency",
            "viability vs comparative evolutionary fitness",
            "identity continuity vs structural fixity",
            "present regulation vs future adaptation",
            "whole viability vs local optimisation",
        ]),
        "historical_lineage": enc(["Ashby and requisite variety", "Stafford Beer's management cybernetics", "VSM and recursive viability", "Maturana and Mpodozis's natural-drift account", "later organisational applications"]),
        "common_misreadings": enc(["viability means profit", "viability means survival of the fittest", "viability means never failing", "a VSM diagram proves viability", "central command creates cohesion"]),
        "open_checks": enc(["Beer primary texts", "Espejo and organisational cybernetics", "viability measures", "natural-drift reception and criticism", "public-service applications"]),
        "source_ids": enc(["src_beer_diagnosing_system_1985", "src_metaphorum_vsm_current", "src_taylor_vsm_lecture_2025", "src_maturana_mpodozis_natural_drift_2000", "src_scio_essential_balances_2020"]),
        "last_researched": GENERATED,
        "review_status": "curator_checked_public_sources",
        "reviewed_by": "Benjamin P Taylor",
        "reviewed_at": GENERATED,
        "editorial_note": "Deepened after Ivo Velitchkov's site submission. The submission identified the question; independent public sources support the published wording.",
    })
    nodes["concept_viability"]["source_ids"] = viability["source_ids"]
    nodes["concept_viability"]["public_source_count"] = 5
    nodes["concept_viability"]["review_status"] = "curator_checked_public_sources"
    nodes["concept_viability"]["reviewed_by"] = "Benjamin P Taylor"
    nodes["concept_viability"]["reviewed_at"] = GENERATED

    patterns_profile = {
        "summary": "Patterns of Strategy models strategy as a dynamic relation among an organisation and other actors, using recurring patterns to explore fit, likely response and strategic manoeuvre.",
        "why_it_matters": "It gives the atlas a strategy method which is relational, dynamic and action-oriented rather than a static internal plan, and makes Lucy Loh's co-development visible alongside Patrick Hoverstadt's.",
        "key_distinctions": ["strategic fit vs internal plan", "ecosystem relation vs market snapshot", "manoeuvre vs implementation schedule", "co-development vs single-author attribution"],
        "historical_lineage": ["Viable System Model", "game and drama theory", "Bateson", "Boyd", "Maturana's structural coupling"],
        "logical_antecedents": ["structural coupling", "power", "time", "strategy", "environment"],
        "dependent_subsequents": ["eighty strategy patterns", "strategy radar", "strategic scenario and riposte work"],
        "practice_connections": ["competitive strategy", "collaborative strategy", "regulatory and partner ecosystems", "strategic foresight"],
        "common_misreadings": ["it is a collection of generic templates", "strategy belongs inside the organisation", "one actor controls the ecosystem"],
        "open_checks": ["add book-level page locators", "document cases and criticism", "map the eighty patterns without confusing them with the nine Grammar patterns"],
    }
    profiles["method_or_methodology_patterns_of_strategy"] = profile_record(patterns, patterns_profile)

    laws_profile = {
        "summary": "Systems laws and principles name recurrent constraints and dynamics that can sharpen inquiry. Their practical value depends on wording, boundary, context and the question being asked.",
        "why_it_matters": "The atlas already had 33 public law entries, but the containing domain was hidden as metadata. Making it public helps readers distinguish a law corpus from a book, a method and a practitioner.",
        "key_distinctions": ["law or principle vs deterministic equation", "pattern vs prescription", "named regularity vs evidence in a case"],
        "historical_lineage": ["general systems theory", "cybernetics", "systems dynamics", "Grammar of Systems"],
        "logical_antecedents": ["system", "relation", "constraint", "feedback", "complexity"],
        "dependent_subsequents": ["systems-law corpus", "systems-thinking practice disciplines"],
        "practice_connections": ["diagnosis", "modelling", "challenge to assumptions", "systems education"],
        "common_misreadings": ["a named law proves a conclusion", "all systems laws have the same status", "context can be ignored"],
        "open_checks": ["record provenance and rival formulations for all 33 entries", "distinguish scientific law, theorem, heuristic and practitioner principle"],
    }
    profiles["knowledge_domain_systems_laws"] = profile_record(systems_laws, laws_profile)
    data["profiles"] = list(profiles.values())

    label_to_id = {fold(node.get("label", "")): node_id for node_id, node in nodes.items()}

    def nid(label: str) -> str:
        key = fold(label)
        if key not in label_to_id:
            raise SystemExit(f"Iteration 0.12 cannot resolve public entry: {label}")
        return label_to_id[key]

    edges = {edge["id"]: dict(edge) for edge in data.get("edges", []) if edge.get("id")}
    for edge_id in [edge_id for edge_id in edges if edge_id.startswith("e_12_")]:
        del edges[edge_id]
    new_edges = [
        edge_record("e_12_scio_self_practice", "organisation_scio_systems_and_complexity_in_organisation", "practice_systems_practice", "self_identifies_with", "identity", "self identifies with", ["src_scio_professional_body_current"], "SCiO publicly describes its purpose as developing and supporting systems-thinking practice."),
        edge_record("e_12_vsm_taught_scio", "method_or_methodology_viable_system_model_vsm", "organisation_scio_systems_and_complexity_in_organisation", "taught_in", "practice", "is taught in", ["src_scio_courses_current", "src_scio_what_vsm_2024"], "The current SCiO catalogue includes a multi-level VSM course sequence."),
        edge_record("e_12_pos_taught_scio", "method_or_methodology_patterns_of_strategy", "organisation_scio_systems_and_complexity_in_organisation", "taught_in", "practice", "is taught in", ["src_scio_courses_current"], "The current SCiO catalogue includes a multi-level Patterns of Strategy sequence."),
        edge_record("e_12_csh_taught_scio", "method_or_methodology_critical_systems_heuristics_csh", "organisation_scio_systems_and_complexity_in_organisation", "taught_in", "practice", "is taught in", ["src_scio_courses_current"], "SCiO currently lists Critical Systems Heuristics training."),
        edge_record("e_12_ssm_taught_scio", "method_or_methodology_soft_systems_methodology_ssm", "organisation_scio_systems_and_complexity_in_organisation", "taught_in", "practice", "is taught in", ["src_scio_courses_current"], "SCiO currently lists Soft Systems Methodology training."),
        edge_record("e_12_sd_taught_scio", "method_or_methodology_system_dynamics", "organisation_scio_systems_and_complexity_in_organisation", "taught_in", "practice", "is taught in", ["src_scio_courses_current"], "SCiO currently lists System Dynamics training."),
        edge_record("e_12_ivo_essential_author", "publication_essential_balances", "person_ivo_velitchkov", "authored_by", "documentary", "was authored by", ["src_scio_essential_balances_2020"], "The official book page identifies Ivo Velitchkov as author."),
        edge_record("e_12_req_ineff_coined", "concept_requisite_inefficiency", "person_ivo_velitchkov", "coined_by", "historical", "was coined by", ["src_scio_requisite_inefficiency_2014"], "The SCiO record presents the phrase as Ivo Velitchkov's proposal."),
        edge_record("e_12_req_ineff_variety", "concept_requisite_inefficiency", nid("Requisite variety"), "explanatory_prerequisite", "conceptual", "has explanatory prerequisite", ["src_scio_requisite_inefficiency_2014"], "The proposal depends on retaining sufficient variety to respond over time."),
        edge_record("e_12_req_ineff_viability", "concept_requisite_inefficiency", "concept_viability", "conceptually_related_to", "conceptual", "is conceptually related to", ["src_scio_requisite_inefficiency_2014"], "The concept is framed as protecting long-term viability from excessive short-term efficiency.", "false"),
        edge_record("e_12_essential_autonomy", "publication_essential_balances", "concept_autonomy", "uses", "practice", "uses", ["src_scio_essential_balances_2020"], "Autonomy is one pole of the first named balance."),
        edge_record("e_12_essential_cohesion", "publication_essential_balances", "concept_cohesion", "uses", "practice", "uses", ["src_scio_essential_balances_2020"], "Cohesion is the other pole of the first named balance."),
        edge_record("e_12_ivo_viability", "person_ivo_velitchkov", "concept_viability", "developed_or_extended", "influence", "developed or extended", ["src_scio_essential_balances_2020", "src_scio_requisite_inefficiency_2014"], "Velitchkov develops viability-related organisational distinctions through balance and reserve variety."),
        edge_record("e_12_natural_drift_maturana", "concept_natural_drift", "person_humberto_maturana", "formulated_by", "historical", "was formulated by", ["src_maturana_mpodozis_natural_drift_2000"], "The article is co-authored by Humberto Maturana."),
        edge_record("e_12_natural_drift_mpodozis", "concept_natural_drift", "person_jorge_mpodozis", "formulated_by", "historical", "was formulated by", ["src_maturana_mpodozis_natural_drift_2000"], "The article is co-authored by Jorge Mpodozis."),
        edge_record("e_12_natural_drift_viability", "concept_natural_drift", "concept_viability", "conceptually_related_to", "conceptual", "is conceptually related to", ["src_maturana_mpodozis_natural_drift_2000"], "The theory emphasises conservation of organisation and adaptation as conditions of continued living.", "false", "0.78", "contested"),
        edge_record("e_12_explicit_semantic_network", "concept_explicit_semantics", "concept_semantic_network", "conceptually_related_to", "conceptual", "is conceptually related to", ["src_nodica_repo_2026"], "Explicit semantics is a design requirement for a semantic graph, not a claim that every semantic network uses one standard.", "false"),
        edge_record("e_12_nodica_semantics", "tool_nodica", "concept_explicit_semantics", "operationalises", "practice", "puts into practical form", ["src_nodica_repo_2026"], "Nodica visualises RDF graph data and is used as a concrete comparator for semantic explicitness."),
        edge_record("e_12_nodica_ivo", "tool_nodica", "person_ivo_velitchkov", "developed_or_extended", "influence", "was developed or extended by", ["src_nodica_repo_2026"], "The primary repository is owned and developed by Ivo Velitchkov."),
        edge_record("e_12_grammar_patrick", "publication_grammar_of_systems_ii", "person_patrick_hoverstadt", "authored_by", "documentary", "was authored by", ["src_grammar_2ed_2025"], "The second edition identifies Patrick Hoverstadt as author."),
        edge_record("e_12_grammar_laws", "publication_grammar_of_systems_ii", "knowledge_domain_systems_laws", "formalises", "conceptual", "formalises", ["src_grammar_2ed_2025", "src_grammar_presentation_2022"], "The publication organises nine thinking patterns and 33 systems laws and principles."),
        edge_record("e_12_grammar_theory", "publication_grammar_of_systems_ii", "tradition_systems_theory", "uses", "practice", "uses", ["src_grammar_2ed_2025"], "The book presents a practical route through systems-thinking foundations rather than a new single systems theory."),
        edge_record("e_12_fractal_patrick", "publication_fractal_organisation_manual", "person_patrick_hoverstadt", "authored_by", "documentary", "was authored by", ["src_scio_fractal_organisation_manual_2026"], "The official page identifies Patrick Hoverstadt as author."),
        edge_record("e_12_fractal_vsm", "publication_fractal_organisation_manual", "method_or_methodology_viable_system_model_vsm", "operationalises", "practice", "puts into practical form", ["src_scio_fractal_organisation_manual_2026"], "The manual provides diagnosis, design and governance approaches using VSM."),
        edge_record("e_12_pos_patrick", "method_or_methodology_patterns_of_strategy", "person_patrick_hoverstadt", "co_developed_with", "human", "was co-developed with", ["src_scio_patterns_strategy_book_2016", "src_scio_patterns_strategy_2024"], "Patrick Hoverstadt is identified as co-developer and co-author."),
        edge_record("e_12_pos_lucy", "method_or_methodology_patterns_of_strategy", "person_lucy_loh", "co_developed_with", "human", "was co-developed with", ["src_scio_patterns_strategy_book_2016"], "Lucy Loh is identified as co-developer and co-author."),
        edge_record("e_12_cst_book_jackson", "publication_critical_systems_thinking_practitioners_guide", "person_michael_c_jackson", "authored_by", "documentary", "was authored by", ["src_scio_critical_systems_thinking_2024"], "The official page identifies Michael C. Jackson as author."),
        edge_record("e_12_cst_book_practice", "publication_critical_systems_thinking_practitioners_guide", "practice_systems_practice", "operationalises", "practice", "puts into practical form", ["src_scio_critical_systems_thinking_2024"], "The book presents critical systems practice as a way to use methodological diversity."),
        edge_record("e_12_cst_book_multi", "publication_critical_systems_thinking_practitioners_guide", "method_or_methodology_multi_methodology_including_sosm", "uses", "practice", "uses", ["src_scio_critical_systems_thinking_2024"], "The guide addresses the critical selection and combination of systems methodologies."),
        edge_record("e_12_opening_jan", "publication_opening_the_box", "person_jan_de_visch", "authored_by", "documentary", "was authored by", ["src_scio_opening_box_2024"], "Official publication metadata lists Jan De Visch."),
        edge_record("e_12_opening_miguel", "publication_opening_the_box", "person_miguel_pantaleon", "authored_by", "documentary", "was authored by", ["src_scio_opening_box_2024"], "Official publication metadata lists Miguel Pantaleon."),
        edge_record("e_12_opening_namrata", "publication_opening_the_box", "person_namrata_arora", "authored_by", "documentary", "was authored by", ["src_scio_opening_box_2024"], "Official publication metadata lists Namrata Arora."),
        edge_record("e_12_opening_tony", "publication_opening_the_box", "person_tony_korycki", "authored_by", "documentary", "was authored by", ["src_scio_opening_box_2024"], "Official publication metadata lists Tony Korycki."),
        edge_record("e_12_opening_practice", "publication_opening_the_box", "practice_systems_practice", "operationalises", "practice", "puts into practical form", ["src_scio_opening_box_2024"], "The book is explicitly designed to support systems-thinking conversation and application."),
        edge_record("e_12_change_reynolds", "publication_systems_approaches_making_change", "person_martin_reynolds", "authored_by", "documentary", "was authored by", ["src_scio_systems_approaches_making_change_2020"], "Official publication metadata lists Martin Reynolds."),
        edge_record("e_12_change_holwell", "publication_systems_approaches_making_change", "person_sue_holwell", "authored_by", "documentary", "was authored by", ["src_scio_systems_approaches_making_change_2020"], "Official publication metadata lists Sue Holwell."),
        edge_record("e_12_change_hoverstadt", "publication_systems_approaches_making_change", "person_patrick_hoverstadt", "authored_by", "documentary", "was authored by", ["src_scio_systems_approaches_making_change_2020"], "Official publication metadata lists Patrick Hoverstadt."),
        edge_record("e_12_change_practice", "publication_systems_approaches_making_change", "practice_systems_practice", "operationalises", "practice", "puts into practical form", ["src_scio_systems_approaches_making_change_2020"], "The book presents systems approaches as practical resources for improvement."),
        edge_record("e_12_battram_book", "publication_navigating_complexity_battram", "person_arthur_battram", "authored_by", "documentary", "was authored by", ["src_scio_navigating_complexity_2014"], "The SCiO resource identifies Arthur Battram and his book."),
        edge_record("e_12_battram_complexity", "publication_navigating_complexity_battram", nid("Complexity"), "operationalises", "practice", "puts into practical form", ["src_scio_navigating_complexity_2014"], "The publication translates complexity ideas into organisational practice rather than serving as primary complexity science."),
    ]
    for edge in new_edges:
        edges[edge["id"]] = edge
    data["edges"] = list(edges.values())

    journey_steps = []
    for label, heading, narrative in JOURNEY["steps"]:
        journey_steps.append({"node_id": nid(label), "heading": heading, "narrative": narrative})
    journeys = {journey["id"]: dict(journey) for journey in data.get("journeys", []) if journey.get("id")}
    journeys[JOURNEY["id"]] = {**{k: v for k, v in JOURNEY.items() if k != "steps"}, "steps": journey_steps}
    data["journeys"] = list(journeys.values())

    data["accepted_contributions"] = [
        {
            "id": "contribution_issue_21_viability",
            "issue_number": 21,
            "issue_url": "https://github.com/antlerboy/the-necessary-tangle/issues/21",
            "contributor": "Ivo Velitchkov",
            "github_login": "kvistgaard",
            "submitted_at": "2026-08-10",
            "status": "incorporated_with_independent_sources",
            "prompt": "Distinguish viability from fitness and consider natural drift.",
            "resulting_entry_ids": ["concept_viability", "concept_natural_drift", "person_ivo_velitchkov"],
            "evidence_rule": "The public issue supplied the question and attribution. Independent public sources support the published content.",
        }
    ]
    data["contribution_intake"] = {
        "version": "three-feed-intake-v1",
        "release": RELEASE,
        "feeds": [
            {"id": "running_feedback", "label": "Curator running feedback", "url": "https://github.com/antlerboy/the-necessary-tangle/issues/2"},
            {"id": "site_submissions", "label": "Site-generated contribution issues", "url": "https://github.com/antlerboy/the-necessary-tangle/issues?q=is%3Aissue+label%3Asite-submission"},
            {"id": "research_issues", "label": "Standing research and coverage issues", "url": "https://github.com/antlerboy/the-necessary-tangle/issues?q=is%3Aissue+label%3Aresearch"},
        ],
        "submission_marker": "Prepared from The Necessary Tangle",
        "labels": ["site-submission", "awaiting-curator-review"],
        "release_rule": "All three feeds must be reconciled before a release is described as having picked up all feedback.",
    }
    data["semantic_contract"] = {
        "version": "explicit-semantics-v1",
        "entity_fields": ["id", "label", "entity_type", "canonical_id", "publication_level", "source_ids"],
        "relation_fields": ["source", "target", "relation_type", "relation_family", "directed", "plain_phrase", "claim_status", "confidence", "source_ids", "scope_conditions"],
        "identity_rule": "Labels and aliases are reader-facing; canonical identifiers and redirects govern identity.",
        "visual_rule": "Position, colour and algorithmic neighbourhood do not assert an unstated relation.",
        "evidence_rule": "Discovery, authorship, teaching, influence, conceptual dependence and practical use remain distinct.",
        "documentation_url": "https://github.com/antlerboy/the-necessary-tangle/blob/main/documentation/explicit-semantics.md",
        "comparator": {"label": "Nodica", "url": "https://kvistgaard.github.io/nodica/index.html", "relationship": "public comparator, not implementation dependency"},
    }
    data["reading_list_coverage"] = {
        "source_id": "src_taylor_reading_list_current",
        "status": "headline_recommendations_developed_full_audit_open",
        "headline_items": [
            {"node_id": "publication_grammar_of_systems_ii", "status": "developed"},
            {"node_id": "publication_critical_systems_thinking_practitioners_guide", "status": "developed"},
            {"node_id": "publication_opening_the_box", "status": "developed"},
            {"node_id": "publication_essential_balances", "status": "developed"},
        ],
        "documentation_url": "https://github.com/antlerboy/the-necessary-tangle/blob/main/documentation/reading-list-coverage.md",
    }
    data["scio_coverage"] = {
        "status": "competency_inventory_present_selected_people_and_works_deepened",
        "organisation_node_id": "organisation_scio_systems_and_complexity_in_organisation",
        "approach_family_count": 13,
        "intervention_skill_count": 47,
        "course_catalogue_source_id": "src_scio_courses_current",
        "documentation_url": "https://github.com/antlerboy/the-necessary-tangle/blob/main/documentation/scio-coverage.md",
        "warning": "SCiO curriculum coverage is not a claim that SCiO or this atlas exhausts the field.",
    }

    mining = {item["id"]: dict(item) for item in data.get("source_mining_register", []) if item.get("id")}
    for item in [
        {
            "id": "mine_taylor_reading_list",
            "label": "Benjamin P Taylor's reading list",
            "url": sources["src_taylor_reading_list_current"]["url"],
            "status": "headline_items_developed_full_audit_open",
            "role": "Curator-oriented route into books, papers and practice sources which shape the atlas's intended centre of gravity.",
            "caveat": "It is deliberately partial and idiosyncratic, not a neutral canon.",
            "next_step": "Audit every listed item against people, publications, methods, sources and profile depth.",
        },
        {
            "id": "mine_scio_courses_people_works",
            "label": "SCiO methods, trainers, authors and works",
            "url": "https://www.systemspractice.org/courses",
            "status": "inventory_present_systematic_depth_audit_open",
            "role": "Current practitioner curriculum and institutional source for methods, courses and trainers.",
            "caveat": "Course inclusion records SCiO's curriculum, not independent validation or the whole field.",
            "next_step": "Reconcile every live course, trainer and associated work with the graph and public sources.",
        },
        {
            "id": "mine_apprenticeship_workbooks",
            "label": "Systems Thinking Practitioner apprenticeship workbooks",
            "url": "https://github.com/antlerboy/the-necessary-tangle/issues/8",
            "status": "private_discovery_public_source_replacement_required",
            "role": "Identify cited people, methods, sources and practical distinctions used in the curator's teaching materials.",
            "caveat": "Private workbooks are discovery sources only; no private URL or extract belongs in the public atlas.",
            "next_step": "Build a private citation inventory and replace each public candidate with a legitimate public source.",
        },
        {
            "id": "mine_cybcom_archive",
            "label": "CYBCOM archive",
            "url": "https://groups.google.com/g/cybcom",
            "status": "registered_not_yet_systematically_ingested",
            "role": "Long-running public cybernetics discussion archive and source-discovery trail.",
            "caveat": "A message establishes circulation or discussion, not truth, priority or influence.",
            "next_step": "Define a bounded date/topic pass and preserve message-level provenance.",
        },
        {
            "id": "mine_asc_archives",
            "label": "American Society for Cybernetics archives",
            "url": "https://asc-cybernetics.org/archives/",
            "status": "registered_first_pass",
            "role": "Index of archival collections, newsletters, recordings and publications for cybernetics lineages.",
            "caveat": "The index is a discovery route; each item needs its own provenance and rights check.",
            "next_step": "Prioritise people already in the atlas and replace generic archive references with item-level records.",
        },
        {
            "id": "mine_battram_navigating_complexity",
            "label": "Arthur Battram and Navigating Complexity",
            "url": "https://www.systemspractice.org/resources/navigating-complexity",
            "status": "public_first_pass_complete_depth_open",
            "role": "Practitioner lineage for complexity-informed organisation and UK local-government work.",
            "caveat": "A SCiO resource page and bibliographic record do not replace full-text review.",
            "next_step": "Review the book and Learning from Complexity pack, then map concepts, cases and influence carefully.",
        },
        {
            "id": "mine_roger_james_notebooklm",
            "label": "Roger James's NotebookLM systems-thinkers source set",
            "url": "https://github.com/antlerboy/the-necessary-tangle/issues/2",
            "status": "identity_and_public_corpus_to_confirm",
            "role": "Potential open-source collection of systems thinkers and source material raised in curator feedback.",
            "caveat": "The exact public corpus, ownership and reuse conditions have not yet been identified.",
            "next_step": "Obtain the canonical public link and permission context before ingesting or citing it.",
        },
    ]:
        mining[item["id"]] = item
    data["source_mining_register"] = list(mining.values())

    if data.get("expansion_08"):
        data["expansion_08"]["net_new_public_entries"] = 203

    meta = data.setdefault("meta", {})
    meta.update({
        "release": RELEASE,
        "generated": GENERATED,
        "status": "public alpha on GitHub Pages",
        "iteration_focus": "practitioner omissions, viability and natural drift, explicit semantics, reading-list and SCiO coverage, and reliable contribution intake",
        "reading_list_url": sources["src_taylor_reading_list_current"]["url"],
        "explicit_semantics_url": "https://github.com/antlerboy/the-necessary-tangle/blob/main/documentation/explicit-semantics.md",
        "contribution_intake_url": "https://github.com/antlerboy/the-necessary-tangle/blob/main/documentation/contribution-intake.md",
        "contribution_queue_url": "https://github.com/antlerboy/the-necessary-tangle/issues?q=is%3Aissue+label%3Asite-submission",
        "scio_coverage_url": "https://github.com/antlerboy/the-necessary-tangle/blob/main/documentation/scio-coverage.md",
        "reading_list_coverage_url": "https://github.com/antlerboy/the-necessary-tangle/blob/main/documentation/reading-list-coverage.md",
        "feedback_intake_version": "three-feed-intake-v1",
        "semantic_contract_version": "explicit-semantics-v1",
        "accepted_contribution_count": len(data["accepted_contributions"]),
        "source_mining_register_count": len(data["source_mining_register"]),
    })

    redirects = data.get("canonical_redirects", {})
    public_nodes = [
        node for node in data["nodes"]
        if node.get("public_visibility") == "public" and redirects.get(node["id"], node["id"]) == node["id"]
    ]
    public_ids = {node["id"] for node in public_nodes}
    meta["public_entry_count"] = len(public_nodes)
    meta["described_entry_count"] = len(public_nodes)
    meta["stub_entry_count"] = 0
    meta["profile_count"] = len({profile["node_id"] for profile in data["profiles"] if profile.get("node_id") in public_ids})
    meta["journey_count"] = len(data["journeys"])
    meta["source_count"] = len(data["sources"])
    meta["public_link_source_count"] = sum(bool(source.get("url")) for source in data["sources"])
    meta["no_public_link_source_count"] = sum(not bool(source.get("url")) for source in data["sources"])

    report = make_ai_observations(graph_metrics(data))
    report["release"] = RELEASE
    report.pop("public_risks", None)
    report["publication_controls"] = [item["id"] for item in data.get("publication_controls", [])]
    report["publication_controls_url"] = "https://github.com/antlerboy/the-necessary-tangle/blob/main/documentation/publication-safety.md"
    report["method_note"] = (
        "These observations combine reproducible counts from the public graph with model-assisted interpretation. "
        "Measurements, interpretations and proposed tests are kept separate. Release 0.12 also treats contribution intake "
        "as part of the observed system: missed submissions are process defects, not invisible contributor failures."
    )
    data["ai_observations"] = report

    write_docs(data)

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
        f"{meta['journey_count']} journeys, {meta['source_count']} sources, "
        f"{len(data['accepted_contributions'])} incorporated contribution and {len(data['source_mining_register'])} mining programmes."
    )


if __name__ == "__main__":
    main()
