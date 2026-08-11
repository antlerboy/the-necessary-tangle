#!/usr/bin/env python3
"""Apply release 0.9: feedback iteration, AI observations and social complexity sources."""
from __future__ import annotations

import json
import math
import re
from collections import Counter, defaultdict, deque
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "public-data.json"
DOCS_ASSETS = ROOT / "docs" / "assets"
DOCUMENTATION = ROOT / "documentation"
RELEASE = "0.9-observations-alpha"
GENERATED = "2026-08-10"

NEW_SOURCES: list[dict[str, Any]] = [
    {
        "id": "src_mowles_resources_social_complexity",
        "title": "Resources on the complexity of social life",
        "source_type": "public_curated_resource_guide",
        "quality_tier": "C",
        "access": "public",
        "url": "https://chrismowles.substack.com/p/resources-on-the-complexity-of-social",
        "date": "2026",
        "notes": "Chris Mowles's public resource guide is used as a discovery route into social and organisational complexity. Items reached through it still require their own source records and review.",
        "creators": "[\"Chris Mowles\"]",
        "doi": "",
        "isbn": "",
        "publisher": "Complexity and Management / Substack",
        "licence": "source_terms",
        "archived_url": "",
        "content_hash": "",
        "review_status": "registered_for_source_mining",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_mowles_complexity_key_idea_2022",
        "title": "Complexity: A Key Idea for Business and Society",
        "source_type": "publisher_book_page",
        "quality_tier": "B",
        "access": "public_metadata",
        "url": "https://www.routledge.com/Complexity-A-Key-Idea-for-Business-and-Society/Mowles/p/book/9780367425685",
        "date": "2022",
        "notes": "Publisher record for Chris Mowles's book. The page supports bibliographic facts and the author's stated framing; it is not a substitute for page-level use of the book.",
        "creators": "[\"Chris Mowles\"]",
        "doi": "",
        "isbn": "9780367425685",
        "publisher": "Routledge",
        "licence": "publisher_terms",
        "archived_url": "",
        "content_hash": "",
        "review_status": "checked",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_mowles_complex_not_quite_2014",
        "title": "Complex, but not quite complex enough: The turn to the complexity sciences in evaluation scholarship",
        "source_type": "publisher_article_page",
        "quality_tier": "B",
        "access": "public_abstract",
        "url": "https://journals.sagepub.com/doi/10.1177/1356389014527885",
        "date": "2014",
        "notes": "Peer-reviewed article in Evaluation. It criticises indiscriminate appeals to complexity science in evaluation and argues for a more radically social interpretation of emergence and interaction.",
        "creators": "[\"Chris Mowles\"]",
        "doi": "10.1177/1356389014527885",
        "isbn": "",
        "publisher": "SAGE / Evaluation",
        "licence": "publisher_terms",
        "archived_url": "",
        "content_hash": "",
        "review_status": "checked",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_stacey_complex_responsive_processes_2001",
        "title": "Complex Responsive Processes in Organizations: Learning and Knowledge Creation",
        "source_type": "publisher_book_page",
        "quality_tier": "B",
        "access": "public_metadata",
        "url": "https://www.routledge.com/Complex-Responsive-Processes-in-Organizations-Learning-and-Knowledge-Creation/Stacey/p/book/9780415249195",
        "date": "2001",
        "notes": "Publisher record for Ralph Stacey's book introducing complex responsive processes of relating as an alternative to information-processing accounts of organisational knowledge.",
        "creators": "[\"Ralph D. Stacey\"]",
        "doi": "",
        "isbn": "9780415249195",
        "publisher": "Routledge",
        "licence": "publisher_terms",
        "archived_url": "",
        "content_hash": "",
        "review_status": "checked",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_mowles_organising_complex_responsive_2022",
        "title": "Organising as complex responsive processes of relating",
        "source_type": "public_author_page",
        "quality_tier": "B",
        "access": "public",
        "url": "https://complexityandmanagement.com/2022/02/07/organising-as-complex-responsive-processes-of-relating/",
        "date": "2022-02-07",
        "notes": "Chris Mowles's public account of the continuing community of inquiry around complex responsive processes and organising.",
        "creators": "[\"Chris Mowles\"]",
        "doi": "",
        "isbn": "",
        "publisher": "Complexity and Management Centre",
        "licence": "source_terms",
        "archived_url": "",
        "content_hash": "",
        "review_status": "checked",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_mowles_practice_complexity_nhs_2010",
        "title": "The practice of complexity: Review, change and service improvement in an NHS department",
        "source_type": "institutional_repository_article",
        "quality_tier": "A",
        "access": "public",
        "url": "https://uhra.herts.ac.uk/id/eprint/63/",
        "date": "2010",
        "notes": "Institutional repository record and public manuscript for an applied account of complex responsive processes in NHS review and service improvement.",
        "creators": "[\"Chris Mowles\", \"Anna van der Gaag\", \"John Fox\"]",
        "doi": "10.1108/14777261011047318",
        "isbn": "",
        "publisher": "University of Hertfordshire Research Archive",
        "licence": "source_terms",
        "archived_url": "",
        "content_hash": "",
        "review_status": "checked",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_murmurations_about",
        "title": "About Murmurations: Journal of Transformative Systemic Practice",
        "source_type": "official_journal_page",
        "quality_tier": "A",
        "access": "public",
        "url": "https://murmurations.cloud/index.php/pub/about",
        "date": "",
        "notes": "Official journal description, scope, publishing model, archive arrangements, ISSN, DOI prefix and licensing statement.",
        "creators": "[\"Murmurations editorial collective\"]",
        "doi": "",
        "isbn": "",
        "publisher": "Everything is Connected Press",
        "licence": "CC BY-NC-ND 4.0",
        "archived_url": "",
        "content_hash": "",
        "review_status": "checked",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
]

SOURCE_MINING_REGISTER = [
    {
        "id": "mine_mowles_social_complexity",
        "label": "Chris Mowles and the Complexity and Management community",
        "url": "https://chrismowles.substack.com/p/resources-on-the-complexity-of-social",
        "status": "active_first_pass",
        "role": "A route into radically social accounts of complexity, complex responsive processes, practical judgement, power and organisational life.",
        "caveat": "Author-curated discovery material. Follow through to books, articles, repositories and rival accounts before asserting genealogy or consensus.",
        "next_step": "Inventory the resource guide and develop the Mowles, Stacey, Griffin, Shaw and Hertfordshire community constellation.",
    },
    {
        "id": "mine_murmurations",
        "label": "Murmurations: Journal of Transformative Systemic Practice",
        "url": "https://murmurations.cloud/index.php/pub",
        "status": "registered_first_pass",
        "role": "Open-access practitioner research on relational, systemic, social-constructionist and reflexive practice across therapy, organisations, leadership and community work.",
        "caveat": "The journal's scope is adjacent to, not identical with, systems science or complexity science. Article-level relevance must be judged rather than assumed.",
        "next_step": "Index titles, abstracts, authors, DOI records and revival-paper conversations; admit only materially relevant items.",
    },
    {
        "id": "mine_monoskop",
        "label": "Monoskop",
        "url": "https://monoskop.org/",
        "status": "registered",
        "role": "Discovery corpus for cybernetics, systems art, media theory, intellectual history, people and bibliographies.",
        "caveat": "A discovery source, not automatic evidence for claims on linked pages.",
        "next_step": "Begin with high-yield people and movements, then replace discovery links with primary or scholarly sources.",
    },
    {
        "id": "mine_syscoi",
        "label": "Systems Community of Inquiry archive",
        "url": "https://stream.syscoi.com/",
        "status": "registered",
        "role": "Evidence of circulation, discussion, interpretation and practitioner attention.",
        "caveat": "Posting or discussion does not prove priority, influence or acceptance.",
        "next_step": "Inventory posts and outbound sources, preserving chronology and differentiating curation from lineage.",
    },
    {
        "id": "mine_model_report",
        "label": "Preserved model.report archive",
        "url": "https://syscoi.com/model.report/model.report/newest.html",
        "status": "registered",
        "role": "Historical practitioner-community archive and source-discovery trail.",
        "caveat": "The archive is incomplete and static; missing context and deleted functionality must remain visible.",
        "next_step": "Recover chronology, participants, outbound links and conversations where the archive permits it.",
    },
    {
        "id": "mine_ashby_archive",
        "label": "W. Ross Ashby Digital Archive",
        "url": "https://ashby.info/",
        "status": "canonical_source",
        "role": "Primary records, chronology, notebooks and correspondence for Ashby and early cybernetics.",
        "caveat": "An archive enables source discovery; interpretation still needs locators and historical context.",
        "next_step": "Deepen Ashby, requisite variety, homeostasis, ultrastability and good-regulator lineages.",
    },
    {
        "id": "mine_asc_library",
        "label": "American Society for Cybernetics library",
        "url": "https://asc-cybernetics.org/",
        "status": "canonical_source",
        "role": "Professional archive and discovery point for first- and second-order cybernetics.",
        "caveat": "Institutional curation is evidence of field memory, not a neutral or complete canon.",
        "next_step": "Register public papers, talks, biographies and conference records item by item.",
    },
    {
        "id": "mine_isss",
        "label": "International Society for the Systems Sciences history and World of Systems",
        "url": "https://www.isss.org/",
        "status": "to_scope",
        "role": "Institutional history, systems-science lineages, proceedings and public educational material.",
        "caveat": "Society histories may privilege their own institutional continuity and terminology.",
        "next_step": "Identify stable public history, proceedings and concept pages; compare with rival institutional accounts.",
    },
    {
        "id": "mine_ifsr",
        "label": "IFSR Conversations and publications",
        "url": "https://www.ifsr.org/",
        "status": "to_scope",
        "role": "Cross-tradition conversations, proceedings and systems research networks.",
        "caveat": "Conversation outputs require participant, date and document-level provenance.",
        "next_step": "Inventory public conversations and map documented collaborations and conceptual disputes.",
    },
    {
        "id": "mine_system_dynamics_society",
        "label": "System Dynamics Society bibliography and conference proceedings",
        "url": "https://systemdynamics.org/",
        "status": "to_scope",
        "role": "Primary institutional source for system dynamics methods, history, teaching and applications.",
        "caveat": "Institutional sources should be paired with critical histories and evaluations of practice.",
        "next_step": "Develop Forrester, modelling practice, policy use and methodological criticism.",
    },
    {
        "id": "mine_sfi",
        "label": "Santa Fe Institute and Complexity Explorer",
        "url": "https://www.santafe.edu/",
        "status": "registered",
        "role": "Complexity-science research, people, publications, courses and institutional history.",
        "caveat": "SFI is a central institution, not the whole field; its selections and vocabulary shape what becomes visible.",
        "next_step": "Replace the current table-of-contents monoculture with paper-level and author-level sources.",
    },
    {
        "id": "mine_necsi",
        "label": "New England Complex Systems Institute",
        "url": "https://necsi.edu/",
        "status": "to_scope",
        "role": "Complex-systems research, education, applications and public explanations.",
        "caveat": "Public explainers vary in evidential depth; use original papers for strong claims.",
        "next_step": "Identify distinctive concepts, methods and application lineages not already covered by SFI sources.",
    },
    {
        "id": "mine_prior_maps",
        "label": "Prior maps and bodies of knowledge",
        "url": "https://github.com/antlerboy/the-necessary-tangle/issues/6",
        "status": "active_comparator_programme",
        "role": "Comparators for scope, category choices, line semantics and evidential transparency.",
        "caveat": "Maps are arguments made for purposes. Similarity to another map is not independent validation.",
        "next_step": "Publish the comparison table and record what this atlas still does worse.",
    },
    {
        "id": "mine_practice_sources",
        "label": "Practice-source discovery",
        "url": "https://github.com/antlerboy/the-necessary-tangle/blob/main/documentation/publication-standards.md",
        "status": "public_evidence_required",
        "role": "Identify prior work, references, names and candidate practice sources.",
        "caveat": "Discovery leads are not evidence. Public evidence or complete public bibliographic citations must support anything published.",
        "next_step": "Assess each lead against the public-source rule before adding an entry or relation.",
    },
]

NEW_NODE_SPECS = [
    {
        "id": "person_chris_mowles",
        "label": "Chris Mowles",
        "entity_type": "person",
        "description": "A scholar and practitioner of complexity and management whose work argues for a radically social account of organisational continuity and change, with attention to interaction, power, uncertainty and practical judgement.",
        "source_ids": [
            "src_mowles_resources_social_complexity",
            "src_mowles_complexity_key_idea_2022",
            "src_mowles_complex_not_quite_2014",
            "src_mowles_practice_complexity_nhs_2010",
        ],
        "x": 0.13,
        "y": 0.31,
    },
    {
        "id": "tradition_complex_responsive_processes",
        "label": "Complex responsive processes",
        "entity_type": "tradition",
        "description": "A perspective on organising in which continuity, novelty, identity and power emerge in local interaction among interdependent people rather than being the straightforward implementation of a system-wide plan.",
        "source_ids": [
            "src_stacey_complex_responsive_processes_2001",
            "src_mowles_organising_complex_responsive_2022",
            "src_mowles_complex_not_quite_2014",
        ],
        "x": 0.08,
        "y": 0.25,
    },
    {
        "id": "publication_murmurations_journal",
        "label": "Murmurations: Journal of Transformative Systemic Practice",
        "entity_type": "publication",
        "description": "An independent, peer-reviewed, open-access journal for relationally attuned systemic social-constructionist practitioners and practitioner-researchers across therapy, organisations, leadership, education, health and community work.",
        "source_ids": ["src_murmurations_about"],
        "x": 0.21,
        "y": 0.36,
    },
    {
        "id": "publication_complexity_key_idea_business_society",
        "label": "Complexity: A Key Idea for Business and Society",
        "entity_type": "publication",
        "description": "Chris Mowles's 2022 book distinguishing several meanings of complexity and developing a social theory of action that resists treating complexity as another instrument for prediction and control.",
        "source_ids": ["src_mowles_complexity_key_idea_2022"],
        "x": 0.17,
        "y": 0.27,
    },
]

PROFILE_SPECS = {
    "person_chris_mowles": {
        "summary": "Chris Mowles develops a critical and practice-facing account of complexity in social and organisational life. His work presses against the idea that complexity thinking supplies managers with a better control technology.",
        "why_it_matters": "The atlas is much stronger on formal and cybernetic concepts than on the difficulty of moving from models of natural complex systems to accounts of human interaction. Mowles provides a documented challenge to that transfer and a route into power, politics, improvisation and practical judgement.",
        "key_distinctions": [
            "Complexity as a description of social life is not the same as complexity science used as a managerial toolkit.",
            "Unpredictability does not remove responsibility or practical judgement.",
            "Organisations are ongoing patterns of interaction, not containers standing apart from the people who constitute them.",
        ],
        "historical_lineage": [
            "The work continues the University of Hertfordshire community of inquiry associated with Ralph Stacey and complex responsive processes.",
            "It draws critically on complexity sciences while also using pragmatic, sociological, psychodynamic and organisational traditions.",
        ],
        "logical_antecedents": ["Complexity", "Emergence", "Power", "Interaction"],
        "dependent_subsequents": ["Complex responsive processes", "Practical judgement", "Relational accounts of organising"],
        "practice_connections": [
            "Leadership and management development",
            "Evaluation and public-service change",
            "Reflexive inquiry into organisational experience",
        ],
        "common_misreadings": [
            "That accepting unpredictability means giving up on deliberate action.",
            "That complex responsive processes is simply another systems model of an organisation.",
            "That a critique of control is a claim that power disappears.",
        ],
        "open_checks": [
            "Develop the wider Hertfordshire community constellation and document disagreement within and around it.",
            "Compare Mowles's use of complexity with systems-practice, critical-systems and complexity-leadership traditions.",
        ],
        "source_ids": [
            "src_mowles_resources_social_complexity",
            "src_mowles_complexity_key_idea_2022",
            "src_mowles_complex_not_quite_2014",
            "src_mowles_practice_complexity_nhs_2010",
        ],
    },
    "tradition_complex_responsive_processes": {
        "summary": "Complex responsive processes treats organising as the ongoing patterning of local interaction. Broader organisational patterns constrain and enable action, but they do not operate as an external system that a manager can stand outside and control.",
        "why_it_matters": "It exposes a fault line inside systems | cybernetics | complexity: whether models of systems and self-organisation illuminate human organising or quietly reintroduce an engineer standing outside the situation.",
        "key_distinctions": [
            "Local interaction and population-wide pattern are mutually constitutive.",
            "Power is present in ordinary interaction rather than added later as a contextual variable.",
            "Emergence does not imply harmony, decentralisation or benign self-organisation.",
        ],
        "historical_lineage": [
            "Developed in the University of Hertfordshire Complexity and Management community, especially through Ralph Stacey and colleagues.",
            "Uses complexity sciences as resources for analogy while explicitly disputing some systems metaphors for human action.",
        ],
        "logical_antecedents": ["Emergence", "Self-organisation", "Interaction", "Power", "Paradox"],
        "dependent_subsequents": ["Complexity approaches to leadership", "Reflexive management inquiry", "Practice-based accounts of change"],
        "practice_connections": [
            "Attending to live interaction rather than treating plans as causes of later outcomes.",
            "Developing practical judgement through reflexive inquiry.",
            "Taking conflict, identity and power seriously in accounts of organisational change.",
        ],
        "common_misreadings": [
            "That local interaction means small-scale interaction is all that matters.",
            "That no one controls the whole means no one has more power than anyone else.",
            "That emergence explains an outcome without a detailed account of interaction and history.",
        ],
        "open_checks": [
            "Represent its critiques of systems thinking without caricaturing the many systems traditions it addresses.",
            "Trace its relationship to pragmatism, group analysis, Elias, Mead and Hegel using primary and scholarly sources.",
        ],
        "source_ids": [
            "src_stacey_complex_responsive_processes_2001",
            "src_mowles_organising_complex_responsive_2022",
            "src_mowles_complex_not_quite_2014",
        ],
    },
    "publication_murmurations_journal": {
        "summary": "Murmurations publishes open-access practitioner research in systemic, relational and social-constructionist practice. It provides a route into practice domains and voices that a concept-first systems map easily neglects.",
        "why_it_matters": "The atlas currently contains many methods and intervention skills with almost no substantive practice connections. A journal organised around practitioner inquiry can help connect ideas to situated work without pretending that publication in the journal settles a claim.",
        "key_distinctions": [
            "The journal is a publication venue and community, not one coherent theory.",
            "Systemic social constructionist practice overlaps with but is not identical to systems science or cybernetics.",
            "Open access improves inspectability but does not remove the need for article-level appraisal.",
        ],
        "historical_lineage": ["Published by Everything is Connected Press with an independent editorial and review model."],
        "logical_antecedents": ["Systemic practice", "Social constructionism", "Reflexivity", "Relational practice"],
        "dependent_subsequents": ["Article-level practice examples", "Practitioner-researcher constellations", "Revival-paper conversations"],
        "practice_connections": ["Therapy", "Leadership and organisational consultancy", "Education", "Health and social care", "Community practice"],
        "common_misreadings": [
            "That every article belongs in the core atlas because the journal calls itself systemic.",
            "That a journal's stated scope demonstrates a conceptual or historical connection for each paper.",
        ],
        "open_checks": ["Inventory relevant articles, authors, DOI records and cited sources; record exclusions as well as admissions."],
        "source_ids": ["src_murmurations_about"],
    },
    "publication_complexity_key_idea_business_society": {
        "summary": "A book-length critical orientation to several meanings of complexity and their implications for business, society, organising, communication and action.",
        "why_it_matters": "The atlas risks treating complexity science as a single body of ideas and then transferring those ideas directly into social practice. This book makes the plurality of meanings and the limits of that transfer visible.",
        "key_distinctions": [
            "Mathematical, natural-scientific and social complexity are not interchangeable.",
            "Models can sharpen judgement without determining action.",
            "Predictable unpredictability is not a licence for vague claims about anything being complex.",
        ],
        "historical_lineage": ["Written from the complex-responsive-processes community of inquiry and a critical-management perspective."],
        "logical_antecedents": ["Complexity", "Emergence", "Complex responsive processes"],
        "dependent_subsequents": ["Critical complexity practice", "Complexity approaches to leadership and evaluation"],
        "practice_connections": ["Management", "Leadership", "Evaluation", "Organisational change"],
        "common_misreadings": ["That it offers a universal complexity method for managers."],
        "open_checks": ["Add chapter-level locators and connect each distinct form of complexity to primary sources and critics."],
        "source_ids": ["src_mowles_complexity_key_idea_2022"],
    },
}

JOURNEY_SPECS = [
    {
        "id": "journey_human_lineage",
        "title": "How ideas travel through people",
        "subtitle": "Teaching, collaboration, institutions and influence are different lines",
        "summary": "A route through the human lineage layer without turning every contact into influence.",
        "audience": "reader of intellectual history",
        "duration_minutes": 12,
        "steps": [
            ("Norbert Wiener", "Begin with a named contributor", "A person's work can be historically central without making that person the sole origin of a field."),
            ("W. Ross Ashby", "Separate parallel development", "Shared problems and correspondence can coexist with independent lines of work. The evidence must say which relation is being claimed."),
            ("Heinz von Foerster", "Add institutions and gatherings", "Laboratories, conferences and editorial settings often carry ideas between people more accurately than a chain of person-to-person arrows."),
            ("Stafford Beer", "Trace adoption and transformation", "A practitioner can inherit concepts, reshape them and build methods whose practical lineage differs from their formal antecedents."),
            ("Viable System Model (VSM)", "End at a method, not a family myth", "The method gathers formal, historical, organisational and practical strands. The atlas should show those different strands rather than compress them into one heroic genealogy."),
        ],
    },
    {
        "id": "journey_power_boundary_intervention",
        "title": "Power enters before the intervention",
        "subtitle": "Boundary, purpose, observer and critique",
        "summary": "A route showing why power is built into systems practice before anyone chooses a method.",
        "audience": "critical systems practitioner",
        "duration_minutes": 11,
        "steps": [
            ("Observer", "Locate who can notice and name", "Observers do not arrive with equal sensors, standing or consequences. Observation is already situated in relations of authority and dependence."),
            ("Boundary", "Ask who and what is made relevant", "A boundary distributes attention, resources, responsibility and exclusion. It is not merely a neutral outline around an object."),
            ("Purpose", "Find the criterion being privileged", "Different purposes make different systems visible and give different people the right to define success."),
            ("Critical Systems Heuristics (CSH)", "Make boundary judgements discussable", "Critical questioning can expose who ought to decide, who benefits, whose expertise counts and who bears the effects."),
            ("Systemic Intervention", "Treat method choice as part of the situation", "Intervention changes the relationships through which the situation is known. The practitioner is not outside the consequences of the inquiry."),
        ],
    },
    {
        "id": "journey_corpus_to_field",
        "title": "How a collection becomes a field — or pretends to",
        "subtitle": "Bibliography, selection, canon and connection",
        "summary": "A route through the difference between inventorying a collection and understanding a field.",
        "audience": "researcher and curator",
        "duration_minutes": 10,
        "steps": [
            ("Foundational Papers in Complexity Science", "Start with the editorial object", "A collection is a selected argument about what counts as foundational. Inventorying it makes the selection inspectable; it does not ratify it."),
            ("Complexity", "Name the wider field", "The field contains institutions, rival programmes, mathematical formalisms, empirical domains and histories that no one collection can exhaust."),
            ("Emergence", "Follow a recurring concept", "A shared word may connect papers, but its formal meaning and explanatory role can differ sharply across domains."),
            ("Self-organisation", "Test the apparent family resemblance", "Similar language can hide different mechanisms, levels and normative assumptions. A useful map records those differences."),
            ("Adaptation", "Move from bibliography to argument", "A developed entry needs definitions, disputes, evidence and uses — not merely an appearance in a table of contents."),
        ],
    },
    {
        "id": "journey_social_complexity",
        "title": "Social complexity without the control-room fantasy",
        "subtitle": "Models, interaction, power and practical judgement",
        "summary": "A route from complexity science to a radically social account of organising and practice.",
        "audience": "leader, evaluator and change practitioner",
        "duration_minutes": 13,
        "steps": [
            ("Complexity", "Take the sciences seriously", "Nonlinearity, interaction and emergence provide real explanatory resources. They do not travel into social life without translation."),
            ("Complex responsive processes", "Put interaction at the centre", "Continuity and change arise in the interweaving of intentions, identities and power relations rather than the execution of a plan held outside the system."),
            ("Chris Mowles", "Meet a critical practitioner-scholar", "Mowles uses complexity to sharpen practical judgement while resisting its conversion into another managerial technology of prediction and control."),
            ("Complexity: A Key Idea for Business and Society", "Distinguish the meanings of complexity", "The book treats complexity as plural and asks what changes when the subject is human social action rather than only a natural or computational system."),
            ("Murmurations: Journal of Transformative Systemic Practice", "Return to situated practice", "Practitioner inquiry supplies cases, tensions and voices through which relational and systemic claims can be tested rather than merely repeated."),
        ],
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
        "boundary_ring": "1",
        "inclusion_reason": "public_source_and_depth_pass",
        "status": "accepted",
        "source_ids": encode(source_ids),
        "set_tags": encode(["complexity", "practice", "release_0_9_source_depth"]),
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
        "no_public_link_count": 0,
    }


def profile_record(node_id: str, spec: dict[str, Any]) -> dict[str, Any]:
    return {
        "node_id": node_id,
        "summary": spec["summary"],
        "why_it_matters": spec["why_it_matters"],
        "key_distinctions": encode(spec["key_distinctions"]),
        "historical_lineage": encode(spec["historical_lineage"]),
        "logical_antecedents": encode(spec["logical_antecedents"]),
        "dependent_subsequents": encode(spec["dependent_subsequents"]),
        "practice_connections": encode(spec["practice_connections"]),
        "common_misreadings": encode(spec["common_misreadings"]),
        "open_checks": encode(spec["open_checks"]),
        "source_ids": encode(spec["source_ids"]),
        "evidence_ids": "[]",
        "review_status": "curator_checked_public_sources",
        "reviewed_by": "Benjamin P Taylor",
        "reviewed_at": GENERATED,
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
        "confidence": "0.88",
        "claim_status": "accepted",
        "source_ids": encode(source_ids),
        "evidence_ids": "[]",
        "source_locator": "Release 0.9 public source pass",
        "valid_from": "",
        "valid_to": "",
        "scope_conditions": "First-pass wording based on the named public sources; stronger historical or conceptual claims remain open to review.",
        "assertion_mode": "asserted",
        "inference_method": "curatorial synthesis of public publisher, journal and institutional records",
        "claim_id": "",
        "reviewed_by": "Benjamin P Taylor",
        "reviewed_at": GENERATED,
        "notes": notes,
        "plain_phrase": phrase,
        "public_review_label": "supported",
    }


def graph_metrics(data: dict[str, Any]) -> dict[str, Any]:
    redirects = data.get("canonical_redirects", {})
    canonical = lambda value: redirects.get(value, value)
    nodes = {
        node["id"]: node for node in data.get("nodes", [])
        if node.get("public_visibility") == "public" and canonical(node["id"]) == node["id"]
    }
    node_ids = set(nodes)
    edges = []
    for edge in data.get("edges", []):
        source = canonical(edge.get("source"))
        target = canonical(edge.get("target"))
        if source in node_ids and target in node_ids and source != target:
            edges.append({**edge, "source": source, "target": target})

    def substantive(edge: dict[str, Any]) -> bool:
        return (
            edge.get("relation_family") not in {"classification", "evidence", "documentary", "legacy"}
            and edge.get("relation_type") != "legacy_association_unspecified"
            and edge.get("claim_status") != "legacy_unresolved"
        )

    substantive_edges = [edge for edge in edges if substantive(edge)]
    adjacency = {node_id: set() for node_id in node_ids}
    all_adjacency = {node_id: set() for node_id in node_ids}
    for edge in edges:
        all_adjacency[edge["source"]].add(edge["target"])
        all_adjacency[edge["target"]].add(edge["source"])
    for edge in substantive_edges:
        adjacency[edge["source"]].add(edge["target"])
        adjacency[edge["target"]].add(edge["source"])

    def component_sizes(graph: dict[str, set[str]]) -> list[int]:
        remaining = set(graph)
        sizes = []
        while remaining:
            start = remaining.pop()
            queue = [start]
            size = 1
            while queue:
                current = queue.pop()
                for other in graph[current]:
                    if other in remaining:
                        remaining.remove(other)
                        queue.append(other)
                        size += 1
            sizes.append(size)
        return sorted(sizes, reverse=True)

    source_by_id = {source["id"]: source for source in data.get("sources", [])}
    source_usage = Counter()
    for node in nodes.values():
        source_usage.update(set(parse(node.get("source_ids"))))
    for edge in edges:
        source_usage.update(set(parse(edge.get("source_ids"))))
    source_top = []
    ranked_sources = sorted(source_usage.items(), key=lambda item: (-item[1], item[0]))[:10]
    for source_id, count in ranked_sources:
        source = source_by_id.get(source_id, {})
        source_top.append({
            "source_id": source_id,
            "title": source.get("title", source_id),
            "uses": count,
            "url": source.get("url", ""),
        })

    entity_counts = Counter(node.get("entity_type", "unknown") for node in nodes.values())
    isolate_counts = Counter(
        nodes[node_id].get("entity_type", "unknown")
        for node_id, neighbours in adjacency.items() if not neighbours
    )
    connected = {node_id for node_id, neighbours in adjacency.items() if neighbours}
    profile_ids = {profile.get("node_id") for profile in data.get("profiles", [])}
    initial_people = [
        node for node in nodes.values()
        if node.get("entity_type") == "person"
        and re.match(r"^(?:[A-Z]\.(?:\s*|$)){1,4}", node.get("label", ""))
    ]
    category_members = {
        node_id
        for category in data.get("emergent_categories", [])
        for node_id in (category.get("member_node_ids") or category.get("members") or [])
    }
    layer_families = {
        "conceptual": {"conceptual"},
        "human_lineage": {"human", "influence", "historical"},
        "practice": {"practice"},
        "contestation": {"contestation"},
        "provenance": {"classification", "evidence", "documentary"},
        "legacy": {"legacy"},
    }
    layer_counts = {}
    for name, families in layer_families.items():
        selected = [edge for edge in edges if edge.get("relation_family") in families]
        incident = {edge["source"] for edge in selected} | {edge["target"] for edge in selected}
        layer_counts[name] = {"edges": len(selected), "nodes": len(incident)}

    degrees = sorted(
        (
            {
                "id": node_id,
                "label": nodes[node_id].get("label", node_id),
                "entity_type": nodes[node_id].get("entity_type", "unknown"),
                "degree": len(neighbours),
            }
            for node_id, neighbours in adjacency.items()
        ),
        key=lambda item: (-item["degree"], item["label"].casefold()),
    )
    substantive_components = component_sizes(adjacency)
    all_components = component_sizes(all_adjacency)
    return {
        "public_entries": len(nodes),
        "developed_profiles": len(profile_ids & node_ids),
        "entity_counts": dict(sorted(entity_counts.items())),
        "sources": len(source_by_id),
        "sources_with_public_links": sum(bool(source.get("url")) for source in source_by_id.values()),
        "typed_edges": len(edges),
        "substantive_edges": len(substantive_edges),
        "substantive_connected_nodes": len(connected),
        "substantive_isolated_nodes": len(node_ids - connected),
        "substantive_components": len(substantive_components),
        "largest_substantive_component": substantive_components[0] if substantive_components else 0,
        "largest_all_edge_component": all_components[0] if all_components else 0,
        "isolates_by_type": dict(sorted(isolate_counts.items())),
        "layers": layer_counts,
        "top_substantive_degree": degrees[:12],
        "source_concentration": source_top,
        "initial_form_people": len(initial_people),
        "people_total": entity_counts.get("person", 0),
        "published_neighbourhoods": len(data.get("emergent_categories", [])),
        "published_neighbourhood_members": len(category_members),
        "connected_nodes_outside_neighbourhoods": len(connected - category_members),
    }


def make_ai_observations(metrics: dict[str, Any]) -> dict[str, Any]:
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

    observations = [
        {
            "id": "breadth_outpaces_depth",
            "title": "Breadth has outrun depth",
            "kind": "measurement plus interpretation",
            "measurement": f"The atlas has {entries} public entries and {profiles} developed profiles. Only {profile_share}% of entries have the fuller profile structure.",
            "interpretation": "It is now better at showing that something belongs in the territory than at explaining what the thing means, why it matters, where it is contested and how it enters practice.",
            "implication": "Next depth work should follow reader demand, bridge concepts and high-risk ambiguities rather than adding another undifferentiated tranche of names.",
            "test": "This observation weakens when developed profiles and item-level source coverage grow without sacrificing the breadth inventory.",
        },
        {
            "id": "two_graph_regimes",
            "title": "One interface contains two different graphs",
            "kind": "measurement plus design inference",
            "measurement": f"There are {typed} typed public edges, but {substantive} are conceptual, historical, human, practice or contestation relations. The substantive share is {substantive_share}%.",
            "interpretation": "Authorship, collection membership and other provenance lines answer different questions from influence, dependence or use. Combining them without visible layers makes bibliographic density look like intellectual agreement.",
            "implication": "The interface should let readers choose conceptual, human-lineage, practice, contestation and provenance layers explicitly.",
            "test": "Readers should be able to explain what became visible or hidden when they change layer, without learning database vocabulary first.",
        },
        {
            "id": "practice_is_peripheral",
            "title": "Practice is named more often than it is connected",
            "kind": "measurement plus curatorial inference",
            "measurement": "The isolate count is concentrated among intervention skills, laws, tools, methods and publications rather than the small conceptual core.",
            "interpretation": "The source programme has imported lists of capabilities and publications faster than it has documented how ideas are enacted, taught, combined, resisted and changed in use.",
            "implication": "Practice cases, practitioner journals, project histories and teaching lineages should now receive deliberate connection work.",
            "test": "The practice layer should develop multiple well-sourced routes between concepts, methods, settings, people and consequences.",
        },
        {
            "id": "source_monoculture",
            "title": "Auditability is not yet source diversity",
            "kind": "measurement plus evidential risk",
            "measurement": f"The most reused source is ‘{top_source['title']}’, attached to {top_source['uses']} public nodes or edges.",
            "interpretation": "A table of contents can establish titles, authors and collection placement. It cannot establish the meaning, influence or quality of every work it lists. Repetition of one source creates an appearance of corroboration without independent evidence.",
            "implication": "Paper-level primary records, publisher pages, DOI metadata, archives, reviews and critical accounts must replace collection-level evidence where stronger statements are made.",
            "test": "Source concentration should fall as the number and independence of item-level sources rise.",
        },
        {
            "id": "identity_resolution",
            "title": "The people layer contains an identity-resolution debt",
            "kind": "measurement plus data-quality risk",
            "measurement": f"{initials} of {people} people — {initials_share}% — are currently represented by initial-form labels.",
            "interpretation": "Initials are enough to inventory an authorship string, but not enough to guarantee a unique person. They invite duplicate records, mistaken mergers and false career or influence connections.",
            "implication": "Add full names, ORCID or other authority identifiers, affiliations and paper-level checks before deepening those people into intellectual profiles.",
            "test": "No initial-only person should acquire interpretive or lineage edges without successful identity resolution.",
        },
        {
            "id": "neighbourhoods_are_stale",
            "title": "The published neighbourhoods are a historical snapshot, not the present graph",
            "kind": "measurement plus model warning",
            "measurement": f"Six published neighbourhoods contain {metrics['published_neighbourhood_members']} unique nodes, while {metrics['substantive_connected_nodes']} nodes are now connected; {metrics['connected_nodes_outside_neighbourhoods']} connected nodes sit outside the old grouping pass.",
            "interpretation": "An algorithmic cluster is produced by the current edges, exclusions, resolution setting and seed. It is not a natural school waiting to be discovered.",
            "implication": "Recompute neighbourhoods at each suitable release, record the algorithm and version, and retain change over time rather than silently replacing one partition with another.",
            "test": "A reader should be able to inspect why two entries share a neighbourhood and see when that grouping changed.",
        },
        {
            "id": "bridge_concepts",
            "title": "A few bridge concepts carry much of the atlas's traffic",
            "kind": "network measurement plus editorial inference",
            "measurement": "Feedback, recursion, the Viable System Model, boundary, requisite variety and related bridge entries have markedly higher substantive degree than most of the graph.",
            "interpretation": "The wording and omissions in those entries influence many possible routes through the atlas. They are single points of interpretive failure as well as useful orientation points.",
            "implication": "Give bridge entries multi-source review, rival definitions, domain distinctions and explicit limits before relying on them as navigation hubs.",
            "test": "Alternative routes and counter-accounts should reduce dependence on any one bridge without hiding genuine centrality.",
        },
        {
            "id": "map_of_attention",
            "title": "The gaps map the curator's attention as much as they map the field",
            "kind": "second-order observation",
            "measurement": f"{metrics['substantive_isolated_nodes']} entries are isolated in the substantive graph, while the largest substantive component contains {metrics['largest_substantive_component']} entries.",
            "interpretation": "Isolation does not mean an idea is naturally peripheral. It often means the current source set, relation vocabulary or research history has not yet made its connections visible.",
            "implication": "Treat isolates as hypotheses about missing work, not as evidence that the field itself has no connections there.",
            "test": "Source programmes from different traditions should alter which entries appear central, peripheral or absent.",
        },
        {
            "id": "ai_failure_modes",
            "title": "The graph is unusually useful to AI — and unusually easy for AI to overread",
            "kind": "experience-based AI observation",
            "measurement": "The atlas provides typed relations, status, source IDs and explicit caveats, but depth and source granularity vary sharply across entries.",
            "interpretation": "Structured relation types reduce the usual language-model tendency to collapse every association into ‘related to’. The remaining danger is confident completion: turning bibliographic inclusion into influence, a provisional edge into fact, or missing data into a smooth narrative.",
            "implication": "AI outputs should expose the exact entries, relation types and sources used; distinguish retrieval from inference; and state when the graph is silent.",
            "test": "A useful AI answer should become less fluent, not more, when the evidence is thin or contradictory.",
        },
    ]

    risks = [
        {
            "risk": "False authority and reputational overclaim",
            "mechanism": "A polished interface can make brief, provisional or collection-derived entries look settled.",
            "controls": "Visible depth and status labels; source locators; explicit rival accounts; release notes that state what was not done.",
        },
        {
            "risk": "False genealogy",
            "mechanism": "Citation, co-presence, chronology, teaching, collaboration and influence can be collapsed into one implied family tree.",
            "controls": "Typed relations; minimum evidence by relation; disputed and unresolved states; no inferred influence from co-occurrence alone.",
        },
        {
            "risk": "Privacy and confidential-source leakage",
            "mechanism": "Private SharePoint, email or client material can enter public data through research notes, URLs, excerpts or generated summaries.",
            "controls": "Separate private lead logs; public-source replacement; automated private-URL scanning; human review before merge; complete deletion from history when secrets appear.",
        },
        {
            "risk": "Copyright and licence error",
            "mechanism": "Open access, public availability and permission to republish are not the same thing.",
            "controls": "Link and summarise; store bibliographic facts and short evidence summaries; record source terms; do not relicense third-party works.",
        },
        {
            "risk": "Identity collision",
            "mechanism": "Initials, alternate names and shared names can merge different people or split one person into several records.",
            "controls": "Authority identifiers, affiliation and publication checks, canonical redirects, and no interpretive edges before resolution.",
        },
        {
            "risk": "Source monoculture and boundary capture",
            "mechanism": "A few corpora define what the atlas notices, making their omissions look like properties of the field.",
            "controls": "Source-mining register; comparator programme; coverage reporting by tradition and domain; deliberate rival and critical sources.",
        },
        {
            "risk": "Automated feedback loops",
            "mechanism": "AI-generated descriptions may be re-ingested, cited or paraphrased until an unsupported statement acquires the appearance of independent repetition.",
            "controls": "Named human sponsor; provenance to non-generated sources; mark AI assistance; never treat generated text as corroboration.",
        },
        {
            "risk": "Vandalism or premature contributor access",
            "mechanism": "A public collaboration request can be mistaken for direct editorial authority.",
            "controls": "Issues and pull requests by default; branch protection; required validation; curator approval; granular roles only in an organisation account.",
        },
        {
            "risk": "Security and operational disclosure",
            "mechanism": "Workflow files, logs, repository history or backups can reveal tokens, internal hostnames and infrastructure detail.",
            "controls": "Least-privilege tokens; secret scanning; protected environments; encrypted off-platform backups; routine restore tests; no credentials in repository data.",
        },
        {
            "risk": "Public permanence",
            "mechanism": "Deletion from the current branch does not guarantee removal from forks, caches, clones or repository history.",
            "controls": "Assume publication is durable; minimise personal data; use GitHub's sensitive-data removal process promptly when required.",
        },
    ]

    return {
        "generated": GENERATED,
        "release": RELEASE,
        "author": "Benjamin P Taylor, curator",
        "method_note": "These observations combine reproducible counts from the public graph with model-assisted interpretation. Measurements, interpretations and proposed tests are kept separate. They are not autonomous editorial decisions and should be challenged against the data and sources.",
        "metrics": metrics,
        "observations": observations,
        "public_risks": risks,
        "next_tests": [
            "Recompute provisional neighbourhoods from the current substantive graph and publish the algorithm and change log.",
            "Resolve initial-only people before adding interpretive lineage edges.",
            "Develop the highest-traffic bridge entries with rival accounts and item-level sources.",
            "Connect intervention skills and methods to documented practice cases rather than generic competence lists.",
            "Run a source-diversity audit before the next major breadth expansion.",
        ],
    }


def write_documentation(data: dict[str, Any]) -> None:
    DOCUMENTATION.mkdir(parents=True, exist_ok=True)
    observations = data["ai_observations"]
    metrics = observations["metrics"]
    lines = [
        "# AI observations", "",
        f"Generated for release `{RELEASE}` on {GENERATED}.", "",
        observations["method_note"], "",
        "## Measured state", "",
        f"- {metrics['public_entries']} public entries; {metrics['developed_profiles']} developed profiles.",
        f"- {metrics['typed_edges']} typed public edges; {metrics['substantive_edges']} substantive edges.",
        f"- {metrics['substantive_connected_nodes']} substantively connected entries and {metrics['substantive_isolated_nodes']} substantive isolates.",
        f"- {metrics['sources']} sources, of which {metrics['sources_with_public_links']} have public links.", "",
    ]
    for observation in observations["observations"]:
        lines.extend([
            f"## {observation['title']}", "",
            f"**Basis:** {observation['kind']}.", "",
            f"**Measured:** {observation['measurement']}", "",
            f"**Interpretation:** {observation['interpretation']}", "",
            f"**Implication:** {observation['implication']}", "",
            f"**Test:** {observation['test']}", "",
        ])
    lines.extend(["# Risks of publishing the atlas", ""])
    for risk in observations["public_risks"]:
        lines.extend([
            f"## {risk['risk']}", "",
            risk["mechanism"], "",
            f"Controls: {risk['controls']}", "",
        ])
    (DOCUMENTATION / "ai-observations.md").write_text("\n".join(lines), encoding="utf-8")

    source_lines = [
        "# Sources to mine", "",
        "This is a live research queue, not a list of sources whose contents have already been accepted into the atlas. Each item states its use and its limits.", "",
    ]
    for item in data["source_mining_register"]:
        source_lines.extend([
            f"## {item['label']}", "",
            f"Status: `{item['status']}`", "",
            f"Public starting point: {item['url']}", "",
            f"Use: {item['role']}", "",
            f"Caution: {item['caveat']}", "",
            f"Next: {item['next_step']}", "",
        ])
    (DOCUMENTATION / "sources-to-mine.md").write_text("\n".join(source_lines), encoding="utf-8")

    risk_lines = [
        "# Publication risks and controls", "",
        "The public atlas is useful partly because its statements, sources and editorial choices are inspectable. The same visibility creates risks that must be designed for rather than appended as a disclaimer.", "",
    ]
    for risk in observations["public_risks"]:
        risk_lines.extend([
            f"## {risk['risk']}", "",
            f"How it happens: {risk['mechanism']}", "",
            f"Current controls: {risk['controls']}", "",
        ])
    (DOCUMENTATION / "publication-risks.md").write_text("\n".join(risk_lines), encoding="utf-8")


def main() -> None:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    data["sources"] = upsert_sources(data.get("sources", []))

    nodes = {node["id"]: dict(node) for node in data.get("nodes", [])}
    for spec in NEW_NODE_SPECS:
        nodes[spec["id"]] = {**nodes.get(spec["id"], {}), **node_record(spec)}
    data["nodes"] = list(nodes.values())

    profiles = {profile["node_id"]: dict(profile) for profile in data.get("profiles", []) if profile.get("node_id")}
    for node_id, spec in PROFILE_SPECS.items():
        profiles[node_id] = {**profiles.get(node_id, {}), **profile_record(node_id, spec)}
    data["profiles"] = list(profiles.values())

    label_to_id = {fold(node.get("label", "")): node_id for node_id, node in nodes.items()}
    required_labels = [
        "Emergence", "Self-organisation", "Complexity", "Norbert Wiener", "W. Ross Ashby",
        "Heinz von Foerster", "Stafford Beer", "Viable System Model (VSM)", "Observer", "Boundary",
        "Purpose", "Critical Systems Heuristics (CSH)", "Systemic Intervention",
        "Foundational Papers in Complexity Science", "Adaptation",
    ]
    missing = [label for label in required_labels if fold(label) not in label_to_id]
    if missing:
        raise SystemExit(f"Iteration 0.9 cannot resolve required public entries: {missing}")

    def nid(label: str) -> str:
        return label_to_id[fold(label)]

    edges = {edge["id"]: dict(edge) for edge in data.get("edges", [])}
    for edge_id in [edge_id for edge_id in edges if edge_id.startswith("e_09_")]:
        del edges[edge_id]
    new_edges = [
        edge_record(
            "e_09_mowles_authored_complexity_key_idea",
            "publication_complexity_key_idea_business_society",
            "person_chris_mowles",
            "authored_by", "documentary", "authored by",
            ["src_mowles_complexity_key_idea_2022"],
            "The publisher record names Chris Mowles as author.",
        ),
        edge_record(
            "e_09_mowles_complex_responsive",
            "person_chris_mowles",
            "tradition_complex_responsive_processes",
            "developed_or_extended", "influence", "developed or extended",
            ["src_mowles_organising_complex_responsive_2022", "src_mowles_complexity_key_idea_2022"],
            "Mowles describes his work as part of the continuing community of inquiry developing complex responsive processes.",
        ),
        edge_record(
            "e_09_complex_responsive_emergence",
            "tradition_complex_responsive_processes",
            nid("Emergence"),
            "conceptually_related_to", "conceptual", "conceptually related to",
            ["src_stacey_complex_responsive_processes_2001", "src_mowles_complex_not_quite_2014"],
            "The perspective uses emergence while disputing explanations that detach global pattern from local human interaction.",
            "false",
        ),
        edge_record(
            "e_09_complex_responsive_self_organisation",
            "tradition_complex_responsive_processes",
            nid("Self-organisation"),
            "conceptually_related_to", "conceptual", "conceptually related to",
            ["src_stacey_complex_responsive_processes_2001"],
            "The founding account places self-organising interaction at the centre of organisational knowledge while challenging direct transfer of natural-system models.",
            "false",
        ),
        edge_record(
            "e_09_book_complex_responsive",
            "publication_complexity_key_idea_business_society",
            "tradition_complex_responsive_processes",
            "developed_or_extended", "influence", "developed or extended",
            ["src_mowles_complexity_key_idea_2022"],
            "The book develops a contemporary account of complexity and organising from this community of inquiry.",
        ),
        edge_record(
            "e_09_murmurations_complex_responsive",
            "publication_murmurations_journal",
            "tradition_complex_responsive_processes",
            "conceptually_related_to", "conceptual", "conceptually related to",
            ["src_murmurations_about", "src_mowles_resources_social_complexity"],
            "The journal's relational systemic practice overlaps with some concerns of complex responsive processes, but the journal is broader and is not treated as an organ of that tradition.",
            "false",
        ),
        edge_record(
            "e_09_mowles_complexity_science",
            "person_chris_mowles",
            nid("Complexity"),
            "critiques", "contestation", "critiques",
            ["src_mowles_complex_not_quite_2014", "src_mowles_complexity_key_idea_2022"],
            "Mowles criticises over- and under-claiming when complexity sciences are transferred into evaluation and social explanation; this is a critique of uses, not a rejection of the sciences.",
        ),
    ]
    for edge in new_edges:
        edges[edge["id"]] = edge
    data["edges"] = list(edges.values())

    journeys = {journey["id"]: dict(journey) for journey in data.get("journeys", []) if journey.get("id")}
    for spec in JOURNEY_SPECS:
        steps = []
        for label, heading, narrative in spec["steps"]:
            key = fold(label)
            if key not in label_to_id:
                raise SystemExit(f"Journey {spec['id']} cannot resolve {label}")
            steps.append({"node_id": label_to_id[key], "heading": heading, "narrative": narrative})
        journeys[spec["id"]] = {
            "id": spec["id"],
            "title": spec["title"],
            "subtitle": spec["subtitle"],
            "summary": spec["summary"],
            "audience": spec["audience"],
            "duration_minutes": spec["duration_minutes"],
            "steps": steps,
        }
    data["journeys"] = list(journeys.values())

    data["source_mining_register"] = SOURCE_MINING_REGISTER
    metrics = graph_metrics(data)
    data["ai_observations"] = make_ai_observations(metrics)

    # Preserve the bounded 0.8 increase when this later overlay is rebuilt repeatedly.
    if data.get("expansion_08"):
        data["expansion_08"]["net_new_public_entries"] = 203
    meta = data.setdefault("meta", {})
    meta["expansion_08_added_count"] = 203
    meta.update({
        "release": RELEASE,
        "generated": GENERATED,
        "status": "public alpha on GitHub Pages",
        "iteration_focus": "AI observations, visible layers, developed social-complexity sources and navigable links",
        "ai_observations_url": "https://antlerboy.github.io/the-necessary-tangle/#view=ai-observations",
    })
    redirects = data.get("canonical_redirects", {})
    public_nodes = [
        node for node in data["nodes"]
        if node.get("public_visibility") == "public" and redirects.get(node["id"], node["id"]) == node["id"]
    ]
    meta["public_entry_count"] = len(public_nodes)
    meta["described_entry_count"] = len(public_nodes)
    meta["profile_count"] = len({profile["node_id"] for profile in data["profiles"] if profile.get("node_id") in {node["id"] for node in public_nodes}})
    meta["journey_count"] = len(data["journeys"])
    meta["source_count"] = len(data["sources"])
    meta["public_link_source_count"] = sum(bool(source.get("url")) for source in data["sources"])
    meta["no_public_link_source_count"] = sum(not bool(source.get("url")) for source in data["sources"])
    meta["source_mining_register_count"] = len(SOURCE_MINING_REGISTER)

    write_documentation(data)
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
        f"{meta['journey_count']} journeys and {meta['source_count']} sources."
    )


if __name__ == "__main__":
    main()
