#!/usr/bin/env python3
"""Apply release 0.14: Dave Snowden, Cynefin and canonical source roles."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from apply_iteration_09 import graph_metrics

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "public-data.json"
DOCS_ASSETS = ROOT / "docs" / "assets"
DOCUMENTATION = ROOT / "documentation"
RELEASE = "0.14-snowden-cynefin-alpha"
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


RELATION_TYPE_UPSERTS = [
    {
        "relation_type": "founded",
        "relation_family": "human",
        "directed": "true",
        "inverse": "founded_by",
        "minimum_evidence": "Official organisational or biographical record",
        "strict_dependency": "no",
        "plain_phrase": "founded",
    },
    {
        "relation_type": "maintains",
        "relation_family": "documentary",
        "directed": "true",
        "inverse": "maintained_by",
        "minimum_evidence": "Official host, project or repository record",
        "strict_dependency": "no",
        "plain_phrase": "maintains",
    },
    {
        "relation_type": "includes",
        "relation_family": "classification",
        "directed": "true",
        "inverse": "included_in",
        "minimum_evidence": "Primary or official scope statement",
        "strict_dependency": "no",
        "plain_phrase": "includes",
    },
]


SOURCE_UPSERTS: list[dict[str, Any]] = [
    {
        "id": "src_cynefin_dave_profile_2026",
        "title": "Dave Snowden — The Cynefin Company profile",
        "source_type": "official_professional_profile",
        "quality_tier": "A",
        "access": "public",
        "url": "https://thecynefin.co/team/dave-snowden/",
        "date": "current; checked 2026-08-11",
        "notes": "Canonical first-party source for Dave Snowden's present roles and the organisation's own account of his creation of Cynefin and origination of SenseMaker. It does not independently establish influence, efficacy or priority beyond those declared facts.",
        "creators": enc(["The Cynefin Company"]),
        "doi": "",
        "isbn": "",
        "publisher": "The Cynefin Company",
        "licence": "site_terms",
        "archived_url": "",
        "content_hash": "",
        "review_status": "checked",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_cynefin_dave_blog_archive_2026",
        "title": "Dave Snowden author archive — The Cynefin Company",
        "source_type": "primary_author_blog_archive",
        "quality_tier": "A",
        "access": "public",
        "url": "https://thecynefin.co/author/dave-snowden/",
        "date": "current archive; checked 2026-08-11",
        "notes": "Canonical first-party route to Snowden's dated public essays. Individual posts support his own evolving terminology and positions; the archive as a whole is not independent corroboration or one internally uniform theory text.",
        "creators": enc(["Dave Snowden"]),
        "doi": "",
        "isbn": "",
        "publisher": "The Cynefin Company",
        "licence": "site_terms",
        "archived_url": "",
        "content_hash": "",
        "review_status": "checked",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_cynefin_company_home_2026",
        "title": "The Cynefin Company",
        "source_type": "official_organisation_site",
        "quality_tier": "A",
        "access": "public",
        "url": "https://thecynefin.co/",
        "date": "current; checked 2026-08-11",
        "notes": "Canonical first-party source for the organisation's current identity, offers and public library. Use independent sources for evaluative claims about impact or standing.",
        "creators": enc(["The Cynefin Company"]),
        "doi": "",
        "isbn": "",
        "publisher": "The Cynefin Company",
        "licence": "site_terms",
        "archived_url": "",
        "content_hash": "",
        "review_status": "checked",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_cynefin_io_main_2026",
        "title": "Cynefin.io — Naturalising Sense-Making wiki",
        "source_type": "official_collaborative_wiki",
        "quality_tier": "B",
        "access": "public",
        "url": "https://cynefin.io/wiki/Main_Page",
        "date": "current; checked 2026-08-11",
        "notes": "Canonical project wiki and discovery source for current naturalising sense-making terminology, methods and internal cross-links. Pages are collaboratively editable and should be cited with page title, revision and stronger sources for disputed history or efficacy. The wiki states CC BY-SA availability unless a page says otherwise.",
        "creators": enc(["Cynefin.io contributors"]),
        "doi": "",
        "isbn": "",
        "publisher": "Cynefin.io",
        "licence": "CC BY-SA unless otherwise indicated",
        "archived_url": "",
        "content_hash": "",
        "review_status": "checked",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_cynefin_io_framework_2026",
        "title": "Cynefin — Cynefin.io",
        "source_type": "official_collaborative_wiki_page",
        "quality_tier": "B",
        "access": "public",
        "url": "https://cynefin.io/wiki/Cynefin",
        "date": "current page; checked 2026-08-11",
        "notes": "First-party maintained account of Cynefin as a decision-support framework based on bounded applicability, its domains, dynamics and development. Appropriate for the framework's own definitions; pair with the named papers for historical and scholarly claims.",
        "creators": enc(["Cynefin.io contributors"]),
        "doi": "",
        "isbn": "",
        "publisher": "Cynefin.io",
        "licence": "CC BY-SA unless otherwise indicated",
        "archived_url": "",
        "content_hash": "",
        "review_status": "checked",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_cynefin_io_anthro_complexity_2026",
        "title": "Anthro-complexity — Cynefin.io",
        "source_type": "official_collaborative_wiki_page",
        "quality_tier": "B",
        "access": "public",
        "url": "https://cynefin.io/wiki/Anthro-complexity",
        "date": "current page; checked 2026-08-11",
        "notes": "First-party maintained account of anthro-complexity as a body of theory and practice concerning human sense-making and action. Use it for declared scope and vocabulary, not as independent adjudication of contested theoretical claims.",
        "creators": enc(["Cynefin.io contributors"]),
        "doi": "",
        "isbn": "",
        "publisher": "Cynefin.io",
        "licence": "CC BY-SA unless otherwise indicated",
        "archived_url": "",
        "content_hash": "",
        "review_status": "checked",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_cynefin_io_naturalising_2026",
        "title": "Naturalising sense-making — Cynefin.io",
        "source_type": "official_collaborative_wiki_page",
        "quality_tier": "B",
        "access": "public",
        "url": "https://cynefin.io/index.php/Naturalising_sense-making",
        "date": "current page; checked 2026-08-11",
        "notes": "First-party maintained definition of naturalising sense-making, including its use of natural science as a constraint and its links to Cynefin, SenseMaker and anthro-complexity.",
        "creators": enc(["Cynefin.io contributors"]),
        "doi": "",
        "isbn": "",
        "publisher": "Cynefin.io",
        "licence": "CC BY-SA unless otherwise indicated",
        "archived_url": "",
        "content_hash": "",
        "review_status": "checked",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_cynefin_sensemaker_official_2026",
        "title": "SenseMaker — The Cynefin Company",
        "source_type": "official_product_and_method_page",
        "quality_tier": "A",
        "access": "public",
        "url": "https://thecynefin.co/sensemaker/",
        "date": "current; checked 2026-08-11",
        "notes": "Canonical first-party description of SenseMaker and its use of self-interpreted micro-narratives. Use project reports and independent evaluations for claims about results in particular settings.",
        "creators": enc(["The Cynefin Company"]),
        "doi": "",
        "isbn": "",
        "publisher": "The Cynefin Company",
        "licence": "site_terms",
        "archived_url": "",
        "content_hash": "",
        "review_status": "checked",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_cynefin_estuarine_mapping_2022",
        "title": "Estuarine Mapping — The Cynefin Company",
        "source_type": "primary_author_method_page",
        "quality_tier": "A",
        "access": "public",
        "url": "https://thecynefin.co/estuarine-mapping/",
        "date": "2022",
        "notes": "Primary public introduction to Estuarine Mapping and its treatment of constraints and change. Later method material may supersede details; date and version should remain visible.",
        "creators": enc(["Dave Snowden"]),
        "doi": "",
        "isbn": "",
        "publisher": "The Cynefin Company",
        "licence": "site_terms",
        "archived_url": "",
        "content_hash": "",
        "review_status": "checked",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_cynefin_complex_acts_2002",
        "title": "Complex Acts of Knowing: Paradox and Descriptive Self-Awareness",
        "source_type": "primary_article_record",
        "quality_tier": "A",
        "access": "public",
        "url": "https://thecynefin.co/library/complex-acts-of-knowing-paradox-and-descriptive-self-awareness/",
        "date": "2002",
        "notes": "Official library record for Snowden's article, with bibliographic details and DOI. Use the article itself for arguments and exact terminology.",
        "creators": enc(["Dave Snowden"]),
        "doi": "10.1108/13673270210424639",
        "isbn": "",
        "publisher": "Journal of Knowledge Management",
        "licence": "article licence as stated by host",
        "archived_url": "",
        "content_hash": "",
        "review_status": "checked",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_cynefin_new_dynamics_2003",
        "title": "The New Dynamics of Strategy: Sense-making in a Complex and Complicated World",
        "source_type": "primary_article_record",
        "quality_tier": "A",
        "access": "public_metadata",
        "url": "https://thecynefin.co/library/the-new-dynamics-of-strategy-sense-making-in-a-complex-and-complicated-world/",
        "date": "2003",
        "notes": "Official library record for the article by Cynthia F. Kurtz and David J. Snowden. The article is a principal scholarly source for early Cynefin dynamics and narrative sense-making.",
        "creators": enc(["Cynthia F. Kurtz", "David J. Snowden"]),
        "doi": "10.1147/sj.423.0462",
        "isbn": "",
        "publisher": "IBM Systems Journal",
        "licence": "publisher_terms",
        "archived_url": "",
        "content_hash": "",
        "review_status": "checked",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_hbr_leaders_framework_2007",
        "title": "A Leader's Framework for Decision Making",
        "source_type": "publisher_article_record",
        "quality_tier": "A",
        "access": "public_metadata",
        "url": "https://hbr.org/2007/11/a-leaders-framework-for-decision-making",
        "date": "2007-11",
        "notes": "Harvard Business Review record for the article by David J. Snowden and Mary E. Boone. It is a widely circulated practice-facing account of Cynefin; use it alongside earlier and later framework sources rather than as the entire theory.",
        "creators": enc(["David J. Snowden", "Mary E. Boone"]),
        "doi": "",
        "isbn": "",
        "publisher": "Harvard Business Review",
        "licence": "publisher_terms",
        "archived_url": "",
        "content_hash": "",
        "review_status": "checked",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_jrc_complexity_crisis_2021",
        "title": "Managing complexity (and chaos) in times of crisis: a field guide for decision makers inspired by the Cynefin framework",
        "source_type": "official_publication_record",
        "quality_tier": "A",
        "access": "public",
        "url": "https://publications.jrc.ec.europa.eu/repository/handle/JRC123629",
        "date": "2021-02-12",
        "notes": "European Commission Joint Research Centre record and public field guide by Dave Snowden and Alessandro Rancati. It supports the guide's authorship, four-stage crisis approach and explicit attention to boundaries, sensing networks, distributed engagement and options.",
        "creators": enc(["Dave Snowden", "Alessandro Rancati"]),
        "doi": "10.2760/353",
        "isbn": "978-92-76-28844-2",
        "publisher": "Publications Office of the European Union",
        "licence": "public EU document",
        "archived_url": "",
        "content_hash": "",
        "review_status": "checked",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_cynefin_field_guide_library_2021",
        "title": "Managing complexity and chaos in times of crisis — Cynefin library record",
        "source_type": "official_project_library_record",
        "quality_tier": "B",
        "access": "public",
        "url": "https://thecynefin.co/library/managing-complexity-and-chaos-in-times-of-crisis/",
        "date": "2021",
        "notes": "First-party project record for the EU field guide and its relation to Cynefin practice. The JRC record is preferred for bibliographic facts and public-document status.",
        "creators": enc(["The Cynefin Company"]),
        "doi": "10.2760/353",
        "isbn": "",
        "publisher": "The Cynefin Company",
        "licence": "site_terms",
        "archived_url": "",
        "content_hash": "",
        "review_status": "checked",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_cynefin_weaving_book_2020",
        "title": "Cynefin: Weaving Sense-Making into the Fabric of Our World",
        "source_type": "official_book_record",
        "quality_tier": "A",
        "access": "public_metadata_and_preview",
        "url": "https://thecynefin.co/library/cynefin-weaving-sense-making-into-the-fabric-of-our-world/",
        "date": "2020",
        "notes": "Official publication record for the multi-author Cynefin volume, used for the framework's retrospective history and later articulation. Chapter-level claims should identify the particular contributor.",
        "creators": enc(["Dave Snowden and contributors"]),
        "doi": "",
        "isbn": "978-1-7353799-0-6",
        "publisher": "Cognitive Edge",
        "licence": "publisher_terms; selected open preview material",
        "archived_url": "",
        "content_hash": "",
        "review_status": "checked",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
]


NODE_SPECS: list[dict[str, Any]] = [
    {
        "id": "person_dave_snowden",
        "label": "Dave Snowden",
        "entity_type": "person",
        "description": "Researcher and practitioner who created the Cynefin framework, originated SenseMaker and developed naturalising sense-making and anthro-complexity as connected bodies of theory and practice.",
        "aliases": ["David J. Snowden", "David John Snowden"],
        "source_ids": ["src_cynefin_dave_profile_2026", "src_cynefin_complex_acts_2002", "src_cynefin_new_dynamics_2003"],
        "x": 0.78,
        "y": 0.16,
    },
    {
        "id": "person_cynthia_f_kurtz",
        "label": "Cynthia F. Kurtz",
        "entity_type": "person",
        "description": "Researcher and writer on participatory narrative inquiry and sense-making, and co-author of The New Dynamics of Strategy.",
        "aliases": ["Cynthia Kurtz"],
        "source_ids": ["src_cynefin_new_dynamics_2003"],
        "x": 0.96,
        "y": 0.38,
    },
    {
        "id": "person_mary_e_boone",
        "label": "Mary E. Boone",
        "entity_type": "person",
        "description": "Author and leadership practitioner who co-authored A Leader's Framework for Decision Making with Dave Snowden.",
        "aliases": ["Mary Boone"],
        "source_ids": ["src_hbr_leaders_framework_2007"],
        "x": 1.04,
        "y": 0.18,
    },
    {
        "id": "person_alessandro_rancati",
        "label": "Alessandro Rancati",
        "entity_type": "person",
        "description": "European Commission Joint Research Centre co-author of the field guide Managing complexity (and chaos) in times of crisis.",
        "aliases": [],
        "source_ids": ["src_jrc_complexity_crisis_2021"],
        "x": 1.10,
        "y": -0.02,
    },
    {
        "id": "organisation_the_cynefin_company",
        "label": "The Cynefin Company",
        "entity_type": "organisation",
        "description": "Organisation developing and applying Cynefin, SenseMaker and naturalising sense-making across strategy, decision-making, research and practice.",
        "aliases": ["Cognitive Edge"],
        "source_ids": ["src_cynefin_company_home_2026", "src_cynefin_dave_profile_2026"],
        "x": 0.66,
        "y": -0.06,
    },
    {
        "id": "corpus_dave_snowden_blog",
        "label": "Dave Snowden's public blog archive",
        "entity_type": "corpus",
        "description": "Dated first-person essays documenting the development, application, revision and polemics of Snowden's work over time.",
        "aliases": ["Cognitive Edge blog", "The Cynefin Company blog — Dave Snowden"],
        "source_ids": ["src_cynefin_dave_blog_archive_2026"],
        "x": 0.46,
        "y": 0.30,
    },
    {
        "id": "corpus_cynefin_io_wiki",
        "label": "Cynefin.io",
        "entity_type": "corpus",
        "description": "Collaborative wiki for naturalising sense-making concepts, methods, cases, reading and Cynefin Centre programmes.",
        "aliases": ["Naturalising Sense-Making wiki", "Cynefin wiki"],
        "source_ids": ["src_cynefin_io_main_2026"],
        "x": 0.44,
        "y": 0.00,
    },
    {
        "id": "method_or_methodology_cynefin_framework",
        "label": "Cynefin framework",
        "entity_type": "method_or_methodology",
        "description": "Decision-support framework for discerning context and choosing approaches on the basis of bounded applicability, distinguishing ordered, complex, chaotic and aporetic conditions and their dynamics.",
        "aliases": ["Cynefin", "Cynefin Framework"],
        "source_ids": ["src_cynefin_io_framework_2026", "src_cynefin_complex_acts_2002", "src_cynefin_new_dynamics_2003", "src_hbr_leaders_framework_2007"],
        "x": 0.30,
        "y": 0.16,
    },
    {
        "id": "tool_sensemaker",
        "label": "SenseMaker",
        "entity_type": "tool",
        "description": "Research and decision-support environment for collecting self-interpreted micro-narratives and making distributed patterns available for inquiry and action.",
        "aliases": ["SenseMaker®"],
        "source_ids": ["src_cynefin_sensemaker_official_2026", "src_cynefin_dave_profile_2026"],
        "x": 0.48,
        "y": -0.24,
    },
    {
        "id": "tradition_anthro_complexity",
        "label": "Anthro-complexity",
        "entity_type": "tradition",
        "description": "A body of theory and practice concerned with complexity in human systems, foregrounding meaning, intentionality, identity, narrative and the limits of treating people as interchangeable agents.",
        "aliases": ["Anthro-Complexity"],
        "source_ids": ["src_cynefin_io_anthro_complexity_2026", "src_cynefin_dave_profile_2026"],
        "x": 0.14,
        "y": -0.02,
    },
    {
        "id": "approach_family_naturalising_sense_making",
        "label": "Naturalising sense-making",
        "entity_type": "approach_family",
        "description": "School of sense-making that uses natural science as a constraint on theory and praxis while asking how people know enough about a situation to act.",
        "aliases": ["Naturalising Sense-Making", "naturalised sense-making"],
        "source_ids": ["src_cynefin_io_naturalising_2026", "src_cynefin_dave_profile_2026"],
        "x": 0.12,
        "y": 0.25,
    },
    {
        "id": "concept_bounded_applicability",
        "label": "Bounded applicability",
        "entity_type": "concept",
        "description": "Principle that approaches have conditions under which they are useful and should not be treated as context-free universal solutions.",
        "aliases": [],
        "source_ids": ["src_cynefin_io_framework_2026"],
        "x": 0.12,
        "y": 0.48,
    },
    {
        "id": "method_or_methodology_estuarine_mapping",
        "label": "Estuarine Mapping",
        "entity_type": "method_or_methodology",
        "description": "Strategy and change method that maps constraints and the energy or effort required to shift them, favouring navigation and modulation over fixed end-state planning.",
        "aliases": ["Estuarine mapping"],
        "source_ids": ["src_cynefin_estuarine_mapping_2022"],
        "x": 0.34,
        "y": -0.44,
    },
    {
        "id": "method_or_methodology_distributed_ethnography",
        "label": "Distributed ethnography",
        "entity_type": "method_or_methodology",
        "description": "Participative research approach in which many people contribute situated observations or micro-narratives and interpret their own material, reducing sole dependence on an external analyst's coding scheme.",
        "aliases": [],
        "source_ids": ["src_cynefin_sensemaker_official_2026", "src_cynefin_dave_profile_2026"],
        "x": 0.62,
        "y": -0.44,
    },
    {
        "id": "publication_complex_acts_of_knowing",
        "label": "Complex Acts of Knowing",
        "entity_type": "publication",
        "description": "Snowden's 2002 article on paradox, descriptive self-awareness, knowledge management and the early Cynefin framework.",
        "aliases": ["Complex Acts of Knowing: Paradox and Descriptive Self-Awareness"],
        "source_ids": ["src_cynefin_complex_acts_2002"],
        "x": 0.72,
        "y": 0.52,
    },
    {
        "id": "publication_new_dynamics_of_strategy",
        "label": "The New Dynamics of Strategy",
        "entity_type": "publication",
        "description": "2003 article by Cynthia F. Kurtz and David J. Snowden connecting narrative, sense-making and Cynefin dynamics in complex and complicated contexts.",
        "aliases": ["The New Dynamics of Strategy: Sense-making in a Complex and Complicated World"],
        "source_ids": ["src_cynefin_new_dynamics_2003"],
        "x": 0.92,
        "y": 0.56,
    },
    {
        "id": "publication_leaders_framework_decision_making",
        "label": "A Leader's Framework for Decision Making",
        "entity_type": "publication",
        "description": "2007 Harvard Business Review article by David J. Snowden and Mary E. Boone translating Cynefin into a leadership and decision-making account for practice.",
        "aliases": ["A Leader’s Framework for Decision Making"],
        "source_ids": ["src_hbr_leaders_framework_2007"],
        "x": 1.12,
        "y": 0.48,
    },
    {
        "id": "publication_managing_complexity_chaos_field_guide",
        "label": "Managing complexity (and chaos) in times of crisis",
        "entity_type": "publication",
        "description": "European Commission Joint Research Centre field guide by Dave Snowden and Alessandro Rancati, using Cynefin to support crisis assessment, sensing, repurposing and learning.",
        "aliases": ["EU Cynefin field guide"],
        "source_ids": ["src_jrc_complexity_crisis_2021", "src_cynefin_field_guide_library_2021"],
        "x": 1.16,
        "y": 0.26,
    },
    {
        "id": "publication_cynefin_weaving_sensemaking",
        "label": "Cynefin: Weaving Sense-Making into the Fabric of Our World",
        "entity_type": "publication",
        "description": "Multi-author 2020 volume presenting retrospective, conceptual and practice accounts of Cynefin and its development.",
        "aliases": ["Cynefin — Weaving Sense-Making into the Fabric of Our World"],
        "source_ids": ["src_cynefin_weaving_book_2020"],
        "x": 0.90,
        "y": 0.72,
    },
]


PROFILE_SPECS: dict[str, dict[str, Any]] = {
    "person_dave_snowden": {
        "summary": "Dave Snowden's work joins context-sensitive decision support, narrative research, knowledge management and complexity-informed practice. Its central public constellation includes Cynefin, SenseMaker, naturalising sense-making, anthro-complexity, Estuarine Mapping and a long-running essay archive.",
        "why_it_matters": "The work offers a substantial alternative to universal methods and linear diagnosis in organisations. Its value is clearer when the named frameworks, tools, papers and source roles are separated rather than collapsed into a single brand or personality.",
        "key_distinctions": ["framework vs model or method", "complex vs complicated", "first-party account vs independent evaluation", "natural science as constraint vs metaphorical borrowing", "narrative capture vs external coding alone"],
        "historical_lineage": ["knowledge management", "organisational decision support", "narrative methods", "complex adaptive systems", "naturalising sense-making"],
        "logical_antecedents": ["context", "constraints", "uncertainty", "sense-making", "human meaning and identity"],
        "dependent_subsequents": ["Cynefin", "SenseMaker", "anthro-complexity", "Estuarine Mapping", "distributed ethnography"],
        "practice_connections": ["strategy", "crisis decision-making", "organisational design", "participative narrative research", "complex facilitation"],
        "common_misreadings": ["Cynefin is the whole of Snowden's work", "Cynefin assigns every problem permanently to a box", "complexity means no structure or discipline", "official source material independently proves efficacy"],
        "open_checks": ["add independent histories and critical evaluations", "map documented teaching and collaboration lineages", "distinguish changes across Cynefin's versions", "develop cases with outcome evidence"],
    },
    "person_cynthia_f_kurtz": {
        "summary": "Cynthia F. Kurtz is a researcher and writer on participatory narrative inquiry and sense-making, and co-author of the early Cynefin paper The New Dynamics of Strategy.",
        "why_it_matters": "Cynefin's early scholarly development was collaborative. Representing Kurtz separately prevents a shared paper and narrative research contribution from becoming a one-person genealogy.",
        "key_distinctions": ["co-authorship vs later ownership", "participatory narrative inquiry vs story collection alone"],
        "historical_lineage": ["organisational narrative", "participatory inquiry", "knowledge management"],
        "logical_antecedents": ["narrative", "interpretation", "context"],
        "dependent_subsequents": ["The New Dynamics of Strategy", "participatory narrative inquiry"],
        "practice_connections": ["organisational research", "community inquiry", "narrative methods"],
        "common_misreadings": ["early Cynefin writing had a sole author", "narrative work is anecdote without method"],
        "open_checks": ["add Kurtz's later primary work", "map the wider narrative-practice lineage"],
    },
    "person_mary_e_boone": {
        "summary": "Mary E. Boone co-authored A Leader's Framework for Decision Making, a prominent practice-facing presentation of Cynefin for leaders.",
        "why_it_matters": "The HBR article shaped wide managerial circulation of Cynefin. Authorship and popularisation should be represented distinctly from the framework's earlier development.",
        "key_distinctions": ["co-authorship vs framework creation", "popularisation vs complete theoretical account"],
        "historical_lineage": ["leadership practice", "management publishing"],
        "logical_antecedents": ["decision-making", "context", "leadership"],
        "dependent_subsequents": ["A Leader's Framework for Decision Making"],
        "practice_connections": ["leadership development", "decision support"],
        "common_misreadings": ["the HBR article is the full Cynefin corpus"],
        "open_checks": ["add biographical and practice sources", "trace documented uptake without inferring it from citation alone"],
    },
    "person_alessandro_rancati": {
        "summary": "Alessandro Rancati co-authored the European Commission Joint Research Centre field guide on managing complexity and chaos in crisis.",
        "why_it_matters": "The field guide is an institutional and collaborative translation of Cynefin into crisis practice, not simply another single-author exposition.",
        "key_distinctions": ["institutional co-production vs individual authorship", "field guidance vs universal prescription"],
        "historical_lineage": ["European Commission Joint Research Centre", "crisis decision support"],
        "logical_antecedents": ["crisis", "sensing", "boundaries", "distributed engagement"],
        "dependent_subsequents": ["Managing complexity and chaos in times of crisis"],
        "practice_connections": ["public policy", "crisis response", "resilience"],
        "common_misreadings": ["a field guide guarantees transfer across every crisis"],
        "open_checks": ["add project cases and evaluation", "map JRC collaboration history"],
    },
    "organisation_the_cynefin_company": {
        "summary": "The Cynefin Company is the organisational home for current development, teaching and application of Cynefin, SenseMaker and associated naturalising sense-making methods.",
        "why_it_matters": "Organisations carry methods through products, training, communities, archives and revision. The organisational source is canonical for current self-description but cannot stand as independent evidence of its own impact.",
        "key_distinctions": ["organisation vs intellectual tradition", "current host vs sole historical source", "official description vs independent evaluation"],
        "historical_lineage": ["Cognitive Edge", "The Cynefin Company", "Cynefin Centre"],
        "logical_antecedents": ["institutional maintenance", "research and development", "practice community"],
        "dependent_subsequents": ["public library", "training", "SenseMaker", "blog archive"],
        "practice_connections": ["strategy", "organisational decision-making", "research", "facilitation"],
        "common_misreadings": ["the organisation and the whole field are the same", "a current product page supplies independent outcome evidence"],
        "open_checks": ["map organisational chronology", "separate company, centre and community roles", "add independent evaluations"],
    },
    "corpus_dave_snowden_blog": {
        "summary": "The author archive is a dated first-person record of Dave Snowden's developing distinctions, methods, applications, arguments and revisions.",
        "why_it_matters": "A long-running blog can reveal conceptual change and chronology that polished retrospective summaries conceal. It is strongest as evidence of what the author said when, not as independent proof that a claim is correct.",
        "key_distinctions": ["primary author record vs independent scholarship", "dated essay vs settled canon", "discovery corpus vs evidence for every outbound claim"],
        "historical_lineage": ["Cognitive Edge blog", "The Cynefin Company blog"],
        "logical_antecedents": ["chronology", "authorship", "public argument"],
        "dependent_subsequents": ["concept histories", "method revisions", "source trails"],
        "practice_connections": ["research discovery", "terminology tracing", "current practice commentary"],
        "common_misreadings": ["every post has equal status", "repetition is independent corroboration", "later terminology can be projected backwards without qualification"],
        "open_checks": ["build item-level index", "capture stable dates and permalinks", "pair major claims with papers and independent accounts"],
    },
    "corpus_cynefin_io_wiki": {
        "summary": "Cynefin.io is the collaborative project wiki for naturalising sense-making, with concept, method, framework, case and support pages.",
        "why_it_matters": "It is the best current route into the project's own semantic network and terminology. As a mutable collaborative wiki, it needs page-level revisions and independent sources for disputed history, priority or effectiveness.",
        "key_distinctions": ["canonical project vocabulary vs universal authority", "wiki page vs primary paper", "current synthesis vs historical wording", "open licence vs unrestricted third-party reuse"],
        "historical_lineage": ["Cynefin Centre", "naturalising sense-making", "collaborative wiki practice"],
        "logical_antecedents": ["linked concepts", "versioned pages", "community maintenance"],
        "dependent_subsequents": ["Cynefin pages", "method descriptions", "reading pathways"],
        "practice_connections": ["learning", "method discovery", "source tracing", "community contribution"],
        "common_misreadings": ["the wiki is one authored monograph", "editable means unreliable in every respect", "canonical for terminology means independent for evaluation"],
        "open_checks": ["record revision IDs for substantial claims", "audit references on high-traffic pages", "map open and branded content boundaries"],
    },
    "method_or_methodology_cynefin_framework": {
        "summary": "Cynefin is a context-discrimination and decision-support framework. It asks which causal conditions and constraints are present, which approaches are applicable, and when a shift in context requires a change of method.",
        "why_it_matters": "It counters the habit of treating one method as universally valid. Its domains are most useful when treated dynamically and provisionally rather than as labels attached permanently to problems.",
        "key_distinctions": ["framework vs model or method", "clear and complicated order vs complexity vs chaos", "domain vs permanent problem type", "categorisation vs sense-making", "static diagram vs dynamics"],
        "historical_lineage": ["knowledge management", "Complex Acts of Knowing", "The New Dynamics of Strategy", "A Leader's Framework for Decision Making", "later liminal Cynefin"],
        "logical_antecedents": ["bounded applicability", "constraints", "causality", "context", "sense-making"],
        "dependent_subsequents": ["domain-specific heuristics", "Cynefin dynamics", "crisis guidance", "complex facilitation"],
        "practice_connections": ["decision support", "strategy", "leadership", "crisis response", "method selection"],
        "common_misreadings": ["Cynefin sorts every issue once and for all", "complex is a synonym for difficult", "the quadrants are maturity levels", "anything uncertain belongs in complexity", "the framework itself supplies a complete intervention"],
        "open_checks": ["map version history precisely", "represent liminal domains and aporia", "add empirical applications and criticism", "compare with other contingency and problem-structuring frameworks"],
    },
    "tool_sensemaker": {
        "summary": "SenseMaker supports distributed capture and self-interpretation of micro-narratives so that patterns can be explored without reducing all meaning to an external coding scheme.",
        "why_it_matters": "It links narrative and quantitative pattern exploration while retaining participants' own interpretation. Claims about a tool's design should remain distinct from evidence about what it achieved in a particular intervention.",
        "key_distinctions": ["self-signification vs researcher coding alone", "micro-narrative vs survey response", "pattern exploration vs predictive certainty", "tool capability vs project outcome"],
        "historical_lineage": ["narrative knowledge management", "distributed ethnography", "Cynefin"],
        "logical_antecedents": ["narrative", "distributed participation", "interpretation", "pattern"],
        "dependent_subsequents": ["narrative landscapes", "participative monitoring", "weak-signal inquiry"],
        "practice_connections": ["evaluation", "community research", "strategy", "monitoring", "organisational listening"],
        "common_misreadings": ["software removes interpretation", "large narrative collections are automatically representative", "visual patterns explain themselves"],
        "open_checks": ["add technical and methodological documentation", "include independent evaluations", "map ethical and data-governance questions"],
    },
    "tradition_anthro_complexity": {
        "summary": "Anthro-complexity addresses complexity in human systems without treating people as simple agents analogous to insects, particles or interchangeable units. It foregrounds meaning, play, making, narrative, identity and intentionality.",
        "why_it_matters": "Human beings can act on descriptions, change identity, contest purposes and alter the rules. These capacities affect what can be carried across from computational or biological complexity models.",
        "key_distinctions": ["human sense-making vs agent simulation", "meaning and identity vs behaviour alone", "natural science constraint vs direct social analogy", "anthro-complexity vs all complexity science"],
        "historical_lineage": ["naturalising sense-making", "complex adaptive systems", "anthropology", "narrative practice"],
        "logical_antecedents": ["identity", "intentionality", "intelligence", "narrative", "abstraction"],
        "dependent_subsequents": ["human-system intervention principles", "complex facilitation", "SenseMaker practice"],
        "practice_connections": ["organisational decision-making", "public policy", "participative research", "strategy"],
        "common_misreadings": ["human systems are exempt from material constraint", "computational complexity is rejected rather than bounded", "anthro-complexity is the only account of social complexity"],
        "open_checks": ["add peer-reviewed and independent accounts", "compare with complex responsive processes and social complexity traditions", "clarify relation to cybernetics and systems dynamics"],
    },
    "approach_family_naturalising_sense_making": {
        "summary": "Naturalising sense-making uses natural science as a constraint while asking how people make sufficient sense of a situation to act. It is the broad approach within which Cynefin, SenseMaker and anthro-complexity are placed by their developers.",
        "why_it_matters": "It makes an epistemic claim about disciplined use of science, not merely a collection of branded tools. The constraint language also calls for scrutiny: which sciences, which findings, and how translation to human practice is warranted.",
        "key_distinctions": ["constraint vs decorative metaphor", "sufficiency for action vs total explanation", "school of sense-making vs universal epistemology", "first-party definition vs independent assessment"],
        "historical_lineage": ["knowledge management", "narrative-based sense-making", "complexity-informed practice", "anthro-complexity"],
        "logical_antecedents": ["sense-making", "natural science", "constraint", "pragmatic action"],
        "dependent_subsequents": ["Cynefin", "SenseMaker", "anthro-complexity", "Estuarine Mapping"],
        "practice_connections": ["decision support", "organisational design", "research", "facilitation"],
        "common_misreadings": ["naturalising means reduction to biology or physics", "scientific constraint guarantees correctness", "the school is coterminous with complexity science"],
        "open_checks": ["trace the five-schools account", "identify explicit scientific dependencies", "add rival sense-making traditions and criticism"],
    },
    "concept_bounded_applicability": {
        "summary": "Bounded applicability says that a method or explanation earns validity within specified conditions rather than by being asserted as a context-free solution.",
        "why_it_matters": "It is a useful antidote to method fundamentalism. It also imposes work: the boundary, evidence and transition conditions must be made explicit rather than invoked as a general escape clause.",
        "key_distinctions": ["context-sensitive validity vs relativism", "boundary conditions vs disclaimer", "usefulness here vs truth everywhere"],
        "historical_lineage": ["Cynefin", "contingency and contextual reasoning", "systems boundary work"],
        "logical_antecedents": ["context", "boundary", "causal conditions"],
        "dependent_subsequents": ["method selection", "domain transitions", "scope conditions"],
        "practice_connections": ["choosing methods", "reviewing assumptions", "ending failed transfer"],
        "common_misreadings": ["every claim is equally valid somewhere", "scope never needs evidence", "contexts are fixed and self-evident"],
        "open_checks": ["compare with boundary critique", "connect to affordances and context of use", "develop examples of invalid transfer"],
    },
    "method_or_methodology_estuarine_mapping": {
        "summary": "Estuarine Mapping represents constraints and the energy required to change them, supporting strategy as navigation through a shifting possibility space rather than movement towards a fully specified future state.",
        "why_it_matters": "It directs attention to what can be modulated now, what is costly or slow to change, and how the landscape changes as action proceeds.",
        "key_distinctions": ["navigation vs end-state planning", "constraints vs goals alone", "energy to change vs importance", "current method version vs every earlier sketch"],
        "historical_lineage": ["Cynefin dynamics", "constraint mapping", "naturalising sense-making"],
        "logical_antecedents": ["constraints", "affordances", "energy", "direction of travel"],
        "dependent_subsequents": ["portfolio of interventions", "continuous remapping", "strategy under uncertainty"],
        "practice_connections": ["strategy", "change", "policy", "portfolio management"],
        "common_misreadings": ["the map predicts the future", "all constraints should be removed", "energy estimates are objective facts"],
        "open_checks": ["record subsequent versions", "add worked public cases", "compare with force-field, Wardley and systems maps"],
    },
    "method_or_methodology_distributed_ethnography": {
        "summary": "Distributed ethnography spreads observation and interpretation across many situated participants rather than reserving both to a small external research team.",
        "why_it_matters": "It can increase contextual variety and reduce some analyst-imposed categories, while raising new sampling, ethics, inclusion and interpretation questions.",
        "key_distinctions": ["distributed contribution vs representative sample", "participant interpretation vs absence of research design", "ethnographic sensibility vs software feature"],
        "historical_lineage": ["ethnography", "participatory research", "narrative inquiry", "SenseMaker"],
        "logical_antecedents": ["situated observation", "participation", "self-interpretation"],
        "dependent_subsequents": ["distributed narrative datasets", "participative sensing"],
        "practice_connections": ["community research", "organisational listening", "monitoring and evaluation"],
        "common_misreadings": ["distribution removes power", "self-interpretation eliminates researcher choices", "volume supplies validity"],
        "open_checks": ["add methodological papers", "map ethics and consent", "compare with conventional and digital ethnography"],
    },
    "publication_complex_acts_of_knowing": {
        "summary": "Complex Acts of Knowing is an early primary text linking knowledge management, descriptive self-awareness and the development of Cynefin.",
        "why_it_matters": "It provides a dated scholarly anchor for claims that otherwise drift into retrospective brand history.",
        "key_distinctions": ["early framework wording vs later Cynefin", "primary article vs retrospective summary"],
        "historical_lineage": ["knowledge management", "early Cynefin"],
        "logical_antecedents": ["knowledge", "paradox", "sense-making"],
        "dependent_subsequents": ["Cynefin development", "descriptive self-awareness"],
        "practice_connections": ["knowledge management", "organisational decision support"],
        "common_misreadings": ["later domain language appears unchanged in the early article"],
        "open_checks": ["add article-level summary with locators", "compare with later versions"],
    },
    "publication_new_dynamics_of_strategy": {
        "summary": "The New Dynamics of Strategy is an early co-authored scholarly account of narrative, sense-making and movement among Cynefin contexts.",
        "why_it_matters": "It grounds both the collaborative development and the dynamic, rather than merely classificatory, character of early Cynefin practice.",
        "key_distinctions": ["complex vs complicated", "dynamics vs static taxonomy", "co-authored development vs sole authorship"],
        "historical_lineage": ["IBM knowledge management", "narrative inquiry", "Cynefin"],
        "logical_antecedents": ["sense-making", "narrative", "context"],
        "dependent_subsequents": ["Cynefin dynamics", "strategy practice"],
        "practice_connections": ["strategy", "organisational narrative", "decision support"],
        "common_misreadings": ["the diagram is the whole argument", "the domains are static sectors"],
        "open_checks": ["summarise with exact page locators", "trace later revisions", "map reception and criticism"],
    },
    "publication_leaders_framework_decision_making": {
        "summary": "A Leader's Framework for Decision Making translates Cynefin for a broad management audience and connects different contexts with different leadership responses.",
        "why_it_matters": "It is a major route of circulation. Its accessibility is a strength, but it should not substitute for the wider theoretical and methodological corpus.",
        "key_distinctions": ["practice translation vs complete theory", "leadership response vs deterministic recipe"],
        "historical_lineage": ["Cynefin", "Harvard Business Review", "leadership practice"],
        "logical_antecedents": ["context", "decision-making", "leadership"],
        "dependent_subsequents": ["managerial use of Cynefin", "popularisation"],
        "practice_connections": ["leadership", "crisis decisions", "strategy"],
        "common_misreadings": ["the article fixes one response for every domain", "publication reach proves effectiveness"],
        "open_checks": ["add documented applications", "map critiques and later corrections"],
    },
    "publication_managing_complexity_chaos_field_guide": {
        "summary": "The JRC field guide offers a four-stage crisis approach informed by Cynefin: assess and respond, build sensing networks, repurpose structures for innovation, and formalise learning and resilience.",
        "why_it_matters": "It is a public institutional translation into crisis practice, with explicit attention to boundaries, informal structures, options and distributed engagement.",
        "key_distinctions": ["field guide vs universal procedure", "complexity vs chaos", "sensing network vs central information pipeline"],
        "historical_lineage": ["Cynefin", "European Commission Joint Research Centre", "crisis practice"],
        "logical_antecedents": ["context assessment", "boundaries", "sensing", "options"],
        "dependent_subsequents": ["crisis action stages", "institutional learning"],
        "practice_connections": ["government", "crisis response", "resilience", "innovation"],
        "common_misreadings": ["four stages imply a linear programme", "a guide removes the need for situated judgement"],
        "open_checks": ["add evaluations and cases", "compare with emergency-management doctrine", "trace later revisions"],
    },
    "publication_cynefin_weaving_sensemaking": {
        "summary": "The 2020 Cynefin volume gathers retrospective and practice accounts from Dave Snowden and other contributors around the framework's first two decades.",
        "why_it_matters": "It is a canonical internal retrospective and an important source for declared history. Chapter authorship must remain visible, and retrospective memory should be checked against dated records.",
        "key_distinctions": ["multi-author collection vs single-author work", "retrospective history vs contemporaneous record", "open preview vs whole-book rights"],
        "historical_lineage": ["twenty-one years of Cynefin", "community and practice reflections"],
        "logical_antecedents": ["Cynefin history", "sense-making", "practice"],
        "dependent_subsequents": ["later Cynefin teaching", "retrospective framing"],
        "practice_connections": ["orientation", "training", "method history"],
        "common_misreadings": ["all chapters speak with one voice", "retrospective sequence is uncontested history"],
        "open_checks": ["map chapter authors and claims", "compare with dated papers and blog posts"],
    },
}


EDGE_SPECS: list[tuple[str, str, str, str, str, str, list[str], str]] = [
    ("e_14_dave_cynefin", "person_dave_snowden", "method_or_methodology_cynefin_framework", "developed", "historical", "developed", ["src_cynefin_dave_profile_2026", "src_cynefin_complex_acts_2002"], "The official profile identifies Snowden as creator; dated primary articles document development."),
    ("e_14_dave_sensemaker", "person_dave_snowden", "tool_sensemaker", "developed", "historical", "originated", ["src_cynefin_dave_profile_2026", "src_cynefin_sensemaker_official_2026"], "The official profile says Snowden originated SenseMaker's design."),
    ("e_14_dave_company", "person_dave_snowden", "organisation_the_cynefin_company", "founded", "human", "founded", ["src_cynefin_dave_profile_2026", "src_cynefin_company_home_2026"], "The official profile identifies Snowden as founder and Chief Scientific Officer."),
    ("e_14_company_blog", "organisation_the_cynefin_company", "corpus_dave_snowden_blog", "maintains", "documentary", "maintains", ["src_cynefin_dave_blog_archive_2026", "src_cynefin_company_home_2026"], "The author archive is hosted and maintained on the organisation's site."),
    ("e_14_dave_blog", "corpus_dave_snowden_blog", "person_dave_snowden", "authored_by", "documentary", "is authored by", ["src_cynefin_dave_blog_archive_2026"], "The archive collects dated posts under Snowden's authorship."),
    ("e_14_wiki_naturalising", "corpus_cynefin_io_wiki", "approach_family_naturalising_sense_making", "described_by", "evidence", "describes", ["src_cynefin_io_main_2026", "src_cynefin_io_naturalising_2026"], "Cynefin.io identifies itself as the Naturalising Sense-Making wiki."),
    ("e_14_wiki_cynefin", "corpus_cynefin_io_wiki", "method_or_methodology_cynefin_framework", "described_by", "evidence", "describes", ["src_cynefin_io_framework_2026"], "The dedicated wiki page supplies the project's current framework account."),
    ("e_14_wiki_anthro", "corpus_cynefin_io_wiki", "tradition_anthro_complexity", "described_by", "evidence", "describes", ["src_cynefin_io_anthro_complexity_2026"], "The dedicated wiki page supplies the project's current anthro-complexity account."),
    ("e_14_naturalising_anthro", "approach_family_naturalising_sense_making", "tradition_anthro_complexity", "includes", "classification", "includes", ["src_cynefin_io_anthro_complexity_2026", "src_cynefin_io_naturalising_2026"], "The wiki describes anthro-complexity as a subset of naturalising sense-making."),
    ("e_14_naturalising_cynefin", "approach_family_naturalising_sense_making", "method_or_methodology_cynefin_framework", "includes", "classification", "includes", ["src_cynefin_io_naturalising_2026", "src_cynefin_io_framework_2026"], "The project places Cynefin within naturalising sense-making."),
    ("e_14_naturalising_sensemaker", "approach_family_naturalising_sense_making", "tool_sensemaker", "includes", "classification", "includes", ["src_cynefin_io_naturalising_2026"], "The project places SenseMaker within naturalising sense-making practice."),
    ("e_14_cynefin_bounded", "method_or_methodology_cynefin_framework", "concept_bounded_applicability", "uses", "conceptual", "uses", ["src_cynefin_io_framework_2026"], "The framework's own account identifies bounded applicability as a core principle."),
    ("e_14_bounded_boundary", "concept_bounded_applicability", "concept_boundary", "conceptually_related_to", "conceptual", "requires explicit boundaries around", ["src_cynefin_io_framework_2026"], "Applicability depends on making context and limits explicit."),
    ("e_14_cynefin_complexity", "method_or_methodology_cynefin_framework", "concept_complexity", "uses", "conceptual", "distinguishes a context of", ["src_cynefin_io_framework_2026"], "Cynefin distinguishes complex from ordered and chaotic contexts."),
    ("e_14_cynefin_chaos", "method_or_methodology_cynefin_framework", "concept_chaos", "uses", "conceptual", "distinguishes a context of", ["src_cynefin_io_framework_2026"], "Cynefin treats chaos as distinct from complexity."),
    ("e_14_cynefin_practice", "method_or_methodology_cynefin_framework", "practice_systems_practice", "operationalises", "practice", "supports", ["src_cynefin_io_framework_2026", "src_hbr_leaders_framework_2007"], "The framework supports context-sensitive selection and change of practice."),
    ("e_14_anthro_complexity", "tradition_anthro_complexity", "concept_complexity", "specialises", "conceptual", "specialises complexity for human systems", ["src_cynefin_io_anthro_complexity_2026"], "Anthro-complexity is the project's account of complexity in human systems."),
    ("e_14_anthro_identity", "tradition_anthro_complexity", "concept_identity", "uses", "conceptual", "foregrounds", ["src_cynefin_io_anthro_complexity_2026"], "Identity is one of the 3Is in the project's account."),
    ("e_14_sensemaker_ethnography", "tool_sensemaker", "method_or_methodology_distributed_ethnography", "operationalises", "practice", "supports", ["src_cynefin_dave_profile_2026", "src_cynefin_sensemaker_official_2026"], "The official profile describes SenseMaker as a distributed ethnography tool."),
    ("e_14_ethnography_practice", "method_or_methodology_distributed_ethnography", "practice_systems_practice", "operationalises", "practice", "supports inquiry in", ["src_cynefin_sensemaker_official_2026"], "Distributed narrative inquiry supplies situated material for systems practice."),
    ("e_14_estuarine_dave", "person_dave_snowden", "method_or_methodology_estuarine_mapping", "developed", "historical", "developed", ["src_cynefin_estuarine_mapping_2022"], "The primary method page is authored by Snowden."),
    ("e_14_estuarine_boundary", "method_or_methodology_estuarine_mapping", "concept_boundary", "uses", "conceptual", "maps constraints and boundaries", ["src_cynefin_estuarine_mapping_2022"], "The method works through the constraints shaping a possibility space."),
    ("e_14_complex_acts_dave", "publication_complex_acts_of_knowing", "person_dave_snowden", "authored_by", "documentary", "was authored by", ["src_cynefin_complex_acts_2002"], "The official article record identifies Snowden as author."),
    ("e_14_complex_acts_cynefin", "publication_complex_acts_of_knowing", "method_or_methodology_cynefin_framework", "develops", "conceptual", "develops", ["src_cynefin_complex_acts_2002"], "The paper is a dated primary source for early Cynefin."),
    ("e_14_new_dynamics_dave", "publication_new_dynamics_of_strategy", "person_dave_snowden", "authored_by", "documentary", "was co-authored by", ["src_cynefin_new_dynamics_2003"], "The publication record names David J. Snowden."),
    ("e_14_new_dynamics_kurtz", "publication_new_dynamics_of_strategy", "person_cynthia_f_kurtz", "authored_by", "documentary", "was co-authored by", ["src_cynefin_new_dynamics_2003"], "The publication record names Cynthia F. Kurtz."),
    ("e_14_kurtz_snowden", "person_cynthia_f_kurtz", "person_dave_snowden", "coauthored_with", "human", "co-authored with", ["src_cynefin_new_dynamics_2003"], "They co-authored The New Dynamics of Strategy."),
    ("e_14_new_dynamics_cynefin", "publication_new_dynamics_of_strategy", "method_or_methodology_cynefin_framework", "develops", "conceptual", "develops the dynamics of", ["src_cynefin_new_dynamics_2003"], "The article develops early Cynefin dynamics rather than only a static classification."),
    ("e_14_hbr_dave", "publication_leaders_framework_decision_making", "person_dave_snowden", "authored_by", "documentary", "was co-authored by", ["src_hbr_leaders_framework_2007"], "The HBR record names David J. Snowden."),
    ("e_14_hbr_boone", "publication_leaders_framework_decision_making", "person_mary_e_boone", "authored_by", "documentary", "was co-authored by", ["src_hbr_leaders_framework_2007"], "The HBR record names Mary E. Boone."),
    ("e_14_hbr_cynefin", "publication_leaders_framework_decision_making", "method_or_methodology_cynefin_framework", "translates_for_practice", "practice", "translates for leadership practice", ["src_hbr_leaders_framework_2007"], "The article presents Cynefin to a broad leadership audience."),
    ("e_14_field_dave", "publication_managing_complexity_chaos_field_guide", "person_dave_snowden", "authored_by", "documentary", "was co-authored by", ["src_jrc_complexity_crisis_2021"], "The JRC record names Dave Snowden."),
    ("e_14_field_rancati", "publication_managing_complexity_chaos_field_guide", "person_alessandro_rancati", "authored_by", "documentary", "was co-authored by", ["src_jrc_complexity_crisis_2021"], "The JRC record names Alessandro Rancati."),
    ("e_14_field_cynefin", "publication_managing_complexity_chaos_field_guide", "method_or_methodology_cynefin_framework", "applies", "practice", "applies", ["src_jrc_complexity_crisis_2021"], "The field guide explicitly draws on Cynefin for crisis decision support."),
    ("e_14_book_dave", "publication_cynefin_weaving_sensemaking", "person_dave_snowden", "authored_by", "documentary", "includes work by", ["src_cynefin_weaving_book_2020"], "The official record identifies Snowden and multiple contributors."),
    ("e_14_book_cynefin", "publication_cynefin_weaving_sensemaking", "method_or_methodology_cynefin_framework", "presents", "documentary", "presents retrospective accounts of", ["src_cynefin_weaving_book_2020"], "The volume presents retrospective and practice accounts of Cynefin."),
    ("e_14_dave_naturalising", "person_dave_snowden", "approach_family_naturalising_sense_making", "developed", "historical", "developed", ["src_cynefin_dave_profile_2026", "src_cynefin_io_naturalising_2026"], "The official profile and wiki place Snowden's work at the centre of the approach."),
    ("e_14_dave_anthro", "person_dave_snowden", "tradition_anthro_complexity", "developed", "historical", "developed", ["src_cynefin_dave_profile_2026", "src_cynefin_io_anthro_complexity_2026"], "The official sources identify anthro-complexity as a substantial strand of Snowden's work."),
    ("e_14_company_sensemaker", "organisation_the_cynefin_company", "tool_sensemaker", "maintains", "documentary", "develops and maintains", ["src_cynefin_company_home_2026", "src_cynefin_sensemaker_official_2026"], "SenseMaker is presented and supported by The Cynefin Company."),
]


JOURNEY = {
    "id": "journey_snowden_cynefin_sources_and_practice",
    "title": "Snowden, Cynefin and the jobs sources can do",
    "subtitle": "A route through a practitioner constellation, its core works and the different evidential roles of blog, wiki, paper, publisher and public institution.",
    "summary": "Starts with Dave Snowden's body of work, separates its people, frameworks, tools and publications, and shows why canonical first-party sources are indispensable but not self-validating.",
    "audience": "Readers seeking a grounded route into Cynefin and naturalising sense-making without turning one diagram, website or personality into the whole account.",
    "duration_minutes": 17,
    "steps": [
        {"node_id": "person_dave_snowden", "heading": "Enter through a body of work", "narrative": "Snowden's expertise spans knowledge management, decision support, narrative research, naturalising sense-making, anthro-complexity and methods for acting under uncertainty."},
        {"node_id": "publication_complex_acts_of_knowing", "heading": "Anchor the early account", "narrative": "A dated primary article gives firmer historical ground than projecting today's terminology backwards."},
        {"node_id": "publication_new_dynamics_of_strategy", "heading": "Keep collaboration and dynamics visible", "narrative": "The co-authored paper with Cynthia F. Kurtz connects narrative, strategy and movement among contexts."},
        {"node_id": "method_or_methodology_cynefin_framework", "heading": "Use Cynefin as decision support", "narrative": "Cynefin discriminates contexts and supports method choice; it is not a permanent taxonomy of problem types."},
        {"node_id": "concept_bounded_applicability", "heading": "Ask where an approach applies", "narrative": "Context-sensitive validity is more demanding than either universal prescription or anything-goes relativism."},
        {"node_id": "approach_family_naturalising_sense_making", "heading": "Place the framework in the broader school", "narrative": "Naturalising sense-making uses natural science as a constraint and asks what is sufficient for action."},
        {"node_id": "tradition_anthro_complexity", "heading": "Take human meaning and identity seriously", "narrative": "Anthro-complexity warns against transferring models of particles, insects or interchangeable agents directly into human systems."},
        {"node_id": "tool_sensemaker", "heading": "Move into distributed narrative inquiry", "narrative": "SenseMaker makes participant-interpreted micro-narratives available for pattern inquiry; its design and its results in any project are separate claims."},
        {"node_id": "method_or_methodology_estuarine_mapping", "heading": "Navigate constraints rather than promise an end state", "narrative": "Estuarine Mapping treats strategy as movement through changing constraints and possibilities."},
        {"node_id": "publication_leaders_framework_decision_making", "heading": "Recognise a major translation into practice", "narrative": "The HBR article broadened managerial access, but it is one practice-facing account rather than the entire corpus."},
        {"node_id": "publication_managing_complexity_chaos_field_guide", "heading": "See institutional co-production", "narrative": "The JRC field guide translates Cynefin into public crisis practice and keeps its collaborative authorship visible."},
        {"node_id": "corpus_dave_snowden_blog", "heading": "Use the blog for chronology and live argument", "narrative": "The archive shows what Snowden argued and changed over time; it does not independently validate those arguments."},
        {"node_id": "corpus_cynefin_io_wiki", "heading": "Use the wiki as the current semantic network", "narrative": "Cynefin.io is canonical for the project's current vocabulary and connections, while page revisions and stronger sources remain necessary for contested claims."},
    ],
}


def node_record(spec: dict[str, Any]) -> dict[str, Any]:
    sources = spec["source_ids"]
    tags = ["complexity", "sensemaking", "expertise", "release_0_14"]
    if spec["entity_type"] in {"method_or_methodology", "tool", "practice"}:
        tags.append("practice")
    return {
        "id": spec["id"],
        "label": spec["label"],
        "entity_type": spec["entity_type"],
        "description": spec["description"],
        "aliases": enc(spec.get("aliases", [])),
        "boundary_ring": "0",
        "inclusion_reason": "snowden_cynefin_canonical_sources_release_0_14",
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
        "publication_level": "profile",
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
        "editorial_note": "Developed from public primary, institutional, publisher and project sources. First-party source roles and independent evidential limits are stated explicitly.",
    }


def edge_record(spec: tuple[str, str, str, str, str, str, list[str], str]) -> dict[str, Any]:
    edge_id, source, target, relation_type, relation_family, phrase, source_ids, notes = spec
    return {
        "id": edge_id,
        "source": source,
        "target": target,
        "relation_type": relation_type,
        "relation_family": relation_family,
        "directed": "true",
        "dependency_kind": "",
        "confidence": "0.88",
        "claim_status": "accepted",
        "source_ids": enc(source_ids),
        "evidence_ids": "[]",
        "source_locator": "Release 0.14 public primary, official, institutional and publisher sources",
        "valid_from": "",
        "valid_to": "",
        "scope_conditions": "The statement is limited to the named sources and their evidential role. First-party definition, authorship, historical development, application and independent evaluation remain distinct claims.",
        "assertion_mode": "asserted",
        "inference_method": "curatorial synthesis of public sources",
        "claim_id": "",
        "reviewed_by": "Benjamin P Taylor",
        "reviewed_at": GENERATED,
        "notes": notes,
        "plain_phrase": phrase,
        "public_review_label": "supported working statement",
    }


def make_observations(data: dict[str, Any]) -> dict[str, Any]:
    metrics = graph_metrics(data)
    entries = metrics["public_entries"]
    profiles = metrics["developed_profiles"]
    typed = metrics["typed_edges"]
    substantive = metrics["substantive_edges"]
    profile_share = round(100 * profiles / entries, 1) if entries else 0
    substantive_share = round(100 * substantive / typed, 1) if typed else 0
    people = metrics["people_total"]
    initials = metrics["initial_form_people"]
    initials_share = round(100 * initials / people, 1) if people else 0
    source_concentration = metrics.get("source_concentration", [])
    top_source = source_concentration[0] if source_concentration else {"title": "No source", "uses": 0}
    entity_counts = metrics.get("entity_counts", {})
    snowden_nodes = {spec["id"] for spec in NODE_SPECS}
    snowden_edges = [edge for edge in data.get("edges", []) if str(edge.get("id", "")).startswith("e_14_")]
    snowden_sources = {source["id"] for source in SOURCE_UPSERTS}
    first_party = {
        "src_cynefin_dave_profile_2026", "src_cynefin_dave_blog_archive_2026", "src_cynefin_company_home_2026",
        "src_cynefin_io_main_2026", "src_cynefin_io_framework_2026", "src_cynefin_io_anthro_complexity_2026",
        "src_cynefin_io_naturalising_2026", "src_cynefin_sensemaker_official_2026", "src_cynefin_estuarine_mapping_2022",
        "src_cynefin_complex_acts_2002", "src_cynefin_new_dynamics_2003", "src_cynefin_field_guide_library_2021",
        "src_cynefin_weaving_book_2020",
    }
    independent_or_institutional = snowden_sources - first_party
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
            "interpretation": "Authorship, hosting and collection membership answer different questions from dependence, influence, critique and use. A dense provenance layer is not evidence of conceptual agreement.",
            "implication": "Layer controls and ordinary-language relation phrases should remain central to the interface.",
            "test": "Readers should be able to say which relation family they are viewing and what changed when they switch it.",
        },
        {
            "id": "canonical_sources_have_jobs",
            "title": "Canonical sources have particular jobs",
            "kind": "source-role analysis",
            "measurement": f"This release registers {len(snowden_sources)} sources for the Snowden-Cynefin constellation: {len(first_party)} first-party project, author or publication records and {len(independent_or_institutional)} external publisher or public-institution records.",
            "interpretation": "A blog can establish what its author argued and when. A project wiki can establish current vocabulary. A publisher or institutional record can establish bibliographic facts. None of these roles automatically supplies independent evaluation of influence or effectiveness.",
            "implication": "Every substantial statement should name both its source and the evidential job that source can reasonably do.",
            "test": "A reader should be able to distinguish definition, chronology, authorship, application and evaluation without relying on host prestige.",
        },
        {
            "id": "expertise_needs_relations",
            "title": "Expertise becomes useful through inspectable constellations",
            "kind": "release measurement plus editorial interpretation",
            "measurement": f"The Snowden-Cynefin pass adds {len(snowden_nodes)} developed entries and {len(snowden_edges)} typed relations among people, works, frameworks, tools, traditions, organisations and source corpora.",
            "interpretation": "A person page or a branded diagram says little by itself. Expertise becomes navigable when works, collaborators, distinctions, methods, institutions and practice relations remain separately inspectable.",
            "implication": "Other practitioner profiles should be developed as evidence-backed constellations rather than biographies or title lists.",
            "test": "A reader should be able to enter through Dave Snowden, Cynefin, SenseMaker, a paper or the wiki and recover a coherent but non-identical route through the same evidence.",
        },
        {
            "id": "first_party_needs_counterweight",
            "title": "First-party depth needs independent counterweight",
            "kind": "source-composition measurement plus epistemic caution",
            "measurement": f"{len(first_party)} of the {len(snowden_sources)} newly registered sources are maintained by the author, project or organisation represented; {len(independent_or_institutional)} are external publisher or public-institution records.",
            "interpretation": "First-party sources are indispensable for current definitions, chronology and intent. They are structurally weak for adjudicating priority, influence, effectiveness and criticism of the same work.",
            "implication": "The next pass should add independent histories, comparative scholarship, evaluations and substantive criticism without replacing the primary record.",
            "test": "Claims about uptake, results or standing should cite evidence outside the represented organisation as well as its own account.",
        },
        {
            "id": "catalogue_is_not_critique",
            "title": "Cataloguing is not critical coverage",
            "kind": "inventory measurement plus epistemic caution",
            "measurement": f"The graph contains {entity_counts.get('publication', 0)} publications and {entity_counts.get('method_or_methodology', 0)} methods or methodologies, while {profiles} entries of all types have developed profiles.",
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
            "interpretation": "A cluster is produced by current edges, exclusions, resolution and seed. It should not be mistaken for a discovered natural taxonomy.",
            "implication": "Recompute neighbourhoods when the substantive graph changes materially and preserve the method and change record.",
            "test": "Readers should be able to inspect why entries share a neighbourhood and when that assignment changed.",
        },
        {
            "id": "bridge_concepts",
            "title": "Bridge concepts deserve disproportionate scrutiny",
            "kind": "network measurement plus editorial inference",
            "measurement": "Feedback, recursion, boundary, viability, requisite variety, the Viable System Model and now context-sensitive sense-making continue to join otherwise separate parts of the atlas.",
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
        "method_note": "Measurements are recalculated from the public graph on every complete build. Interpretations, implications and tests are kept separate and remain open to challenge.",
        "metrics": metrics,
        "observations": observations,
        "publication_controls": [item.get("id") for item in data.get("publication_controls", []) if item.get("id")],
        "publication_controls_url": "https://github.com/antlerboy/the-necessary-tangle/blob/main/documentation/publication-safety.md",
        "next_tests": [
            "Add independent evaluation and criticism to first-party source constellations.",
            "Recompute neighbourhoods from the current substantive graph and publish the method and change record.",
            "Resolve initial-only people before adding interpretive lineage edges.",
            "Connect methods and intervention skills to documented cases rather than competence lists alone.",
            "Report inventory breadth, profile depth and critical review separately.",
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


def write_source_documents() -> None:
    (DOCUMENTATION / "snowden-cynefin-sources.md").write_text(
        """# Dave Snowden, Cynefin and source roles

This release treats Dave Snowden's work as a constellation of people, publications, frameworks, tools, organisations, practices and evolving public arguments.

## Canonical first-party sources

### Dave Snowden's author archive

The author archive at The Cynefin Company is the preferred route to dated public essays by Snowden. It can establish what he argued, named or revised at a particular time. It is not independent corroboration of influence, priority or effectiveness, and individual posts should be cited rather than treating the archive as one uniform work.

### Cynefin.io

Cynefin.io is the preferred route to the project's current vocabulary, internal concept links, methods and support material. It is a collaborative and mutable wiki. Substantial claims should record the page and revision and should use named papers, public institutional records or independent scholarship for contested history and evaluation.

### The Cynefin Company

The organisation's site is authoritative for its current identity, products, training, public library and declared roles. It does not independently establish the value or results of its own methods.

## Dated primary and publication records

The principal dated anchors in this pass are:

- Dave Snowden, *Complex Acts of Knowing: Paradox and Descriptive Self-Awareness* (2002);
- Cynthia F. Kurtz and David J. Snowden, *The New Dynamics of Strategy* (2003);
- David J. Snowden and Mary E. Boone, *A Leader's Framework for Decision Making* (2007);
- Dave Snowden and contributors, *Cynefin: Weaving Sense-Making into the Fabric of Our World* (2020);
- Dave Snowden and Alessandro Rancati, *Managing complexity (and chaos) in times of crisis* (2021).

These sources do different jobs. The early articles establish dated arguments and collaboration. The HBR article is a practice-facing translation. The multi-author volume is a retrospective internal account. The Joint Research Centre guide is a public institutional application.

## What remains open

The next source pass should add independent histories, evaluations, comparative scholarship and substantive criticism. It should also distinguish Cynefin versions and dynamics more precisely, map the wider contributor and teaching lineage, and connect methods to documented cases and consequences.
""",
        encoding="utf-8",
    )

    register_path = DOCUMENTATION / "canonical-source-register.md"
    register = register_path.read_text(encoding="utf-8")
    section = """\n### Dave Snowden author archive\n\nRole: primary author archive.\n\nUse dated posts for Snowden's own terminology, chronology, revisions and public arguments. Cite individual posts. Do not treat repetition across the archive as independent corroboration.\n\n### Cynefin.io\n\nRole: official collaborative project wiki and semantic discovery corpus.\n\nUse it for the project's current definitions, internal links, methods and revision history. Record page and revision where material claims depend on mutable content. Pair disputed history, priority and efficacy claims with dated primary works and independent sources.\n\n### The Cynefin Company library and site\n\nRole: first-party organisation record and publication gateway.\n\nUse it for current organisational identity, public library records, products and declared method descriptions. Use publisher, institutional and independent records for bibliographic adjudication and evaluation.\n\n### European Commission Joint Research Centre field guide\n\nRole: public institutional publication and application record.\n\nUse the JRC record and guide for authorship, bibliographic detail and the documented crisis decision-support approach. Treat transfer to other settings as a separate evidential question.\n"""
    if "### Dave Snowden author archive" not in register:
        register = register.replace("\n## Source-use rules\n", section + "\n## Source-use rules\n")
    register_path.write_text(register, encoding="utf-8")

    mine_path = DOCUMENTATION / "sources-to-mine.md"
    mine = mine_path.read_text(encoding="utf-8")
    section2 = """\n## Dave Snowden author archive and Cynefin.io\n\nStatus: `active_canonical_source_pass`\n\nPublic starting points: https://thecynefin.co/author/dave-snowden/ and https://cynefin.io/wiki/Main_Page\n\nUse: The blog supplies dated first-person argument and development history. The wiki supplies current project terminology, linked concepts, methods and references.\n\nCaution: Both are first-party and mutable. They are canonical for what the project says, not independent proof of influence, efficacy, priority or consensus.\n\nNext: Build item-level indexes, retain dates and revision IDs, and pair major claims with primary publications, public institutional records, comparative scholarship and criticism.\n"""
    if "## Dave Snowden author archive and Cynefin.io" not in mine:
        mine = mine.replace("\n## Prior maps and bodies of knowledge\n", section2 + "\n## Prior maps and bodies of knowledge\n")
    mine_path.write_text(mine, encoding="utf-8")


def main() -> None:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))

    sources = {source["id"]: dict(source) for source in data.get("sources", []) if source.get("id")}
    for source in SOURCE_UPSERTS:
        sources[source["id"]] = {**sources.get(source["id"], {}), **source}
    data["sources"] = list(sources.values())

    relation_types = {item["relation_type"]: dict(item) for item in data.get("relation_types", []) if item.get("relation_type")}
    for item in RELATION_TYPE_UPSERTS:
        relation_types[item["relation_type"]] = {**relation_types.get(item["relation_type"], {}), **item}
    data["relation_types"] = list(relation_types.values())

    nodes = {node["id"]: dict(node) for node in data.get("nodes", []) if node.get("id")}
    for spec in NODE_SPECS:
        nodes[spec["id"]] = {**nodes.get(spec["id"], {}), **node_record(spec)}
    data["nodes"] = list(nodes.values())

    profiles = {profile["node_id"]: dict(profile) for profile in data.get("profiles", []) if profile.get("node_id")}
    for spec in NODE_SPECS:
        profiles[spec["id"]] = {**profiles.get(spec["id"], {}), **profile_record(nodes[spec["id"]], PROFILE_SPECS[spec["id"]])}
    data["profiles"] = list(profiles.values())

    edges = {edge["id"]: dict(edge) for edge in data.get("edges", []) if edge.get("id")}
    for edge_id in [edge_id for edge_id in edges if edge_id.startswith("e_14_")]:
        del edges[edge_id]
    for spec in EDGE_SPECS:
        edges[spec[0]] = edge_record(spec)
    data["edges"] = list(edges.values())

    journeys = {journey["id"]: dict(journey) for journey in data.get("journeys", []) if journey.get("id")}
    journeys[JOURNEY["id"]] = JOURNEY
    data["journeys"] = list(journeys.values())

    canonical = {item.get("source_id"): dict(item) for item in data.get("canonical_source_register", []) if item.get("source_id")}
    for item in [
        {"source_id": "src_cynefin_dave_blog_archive_2026", "tier": "primary_author_archive", "status": "checked", "use": "Snowden's dated public arguments, terminology and revisions"},
        {"source_id": "src_cynefin_io_main_2026", "tier": "official_collaborative_wiki", "status": "checked", "use": "Current project vocabulary, concepts, methods and source discovery"},
        {"source_id": "src_cynefin_company_home_2026", "tier": "official_organisation_record", "status": "checked", "use": "Current organisational identity, library and method hosting"},
        {"source_id": "src_jrc_complexity_crisis_2021", "tier": "public_institutional_publication", "status": "checked", "use": "Public field-guide authorship, bibliographic record and crisis application"},
    ]:
        canonical[item["source_id"]] = item
    data["canonical_source_register"] = list(canonical.values())

    mining = {item.get("id"): dict(item) for item in data.get("source_mining_register", []) if item.get("id")}
    mining["mine_snowden_cynefin"] = {
        "id": "mine_snowden_cynefin",
        "label": "Dave Snowden author archive and Cynefin.io",
        "url": "https://thecynefin.co/author/dave-snowden/",
        "status": "active_canonical_source_pass",
        "role": "Dated primary argument, current project terminology, method discovery and source trails.",
        "caveat": "First-party and mutable. Canonical for project self-description, not independent proof of efficacy, priority, influence or consensus.",
        "next_step": "Build item-level blog and wiki indexes with dates or revision IDs, then pair major claims with publications, institutional records, comparison and criticism.",
    }
    data["source_mining_register"] = list(mining.values())

    meta = data.setdefault("meta", {})
    meta.update({
        "release": RELEASE,
        "generated": GENERATED,
        "status": "public alpha on GitHub Pages",
        "iteration_focus": "Dave Snowden and Cynefin as an expertise and source-role constellation, with first-party and independent evidence kept distinct",
        "snowden_cynefin_sources_url": "https://github.com/antlerboy/the-necessary-tangle/blob/main/documentation/snowden-cynefin-sources.md",
        "canonical_source_register_url": "https://github.com/antlerboy/the-necessary-tangle/blob/main/documentation/canonical-source-register.md",
        "source_mining_register_count": len(data["source_mining_register"]),
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

    report = make_observations(data)
    data["ai_observations"] = report

    DOCUMENTATION.mkdir(parents=True, exist_ok=True)
    write_ai_document(report)
    write_source_documents()

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
        f"{meta['journey_count']} journeys, {meta['source_count']} sources and {len(EDGE_SPECS)} new typed relations."
    )


if __name__ == "__main__":
    main()
