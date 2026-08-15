#!/usr/bin/env python3
"""Publish the privacy-safe Damian Allen / Doncaster systems-practice lineage.

The overlay is idempotent. Private Gmail and attachment metadata contains no
message identifiers, addresses, private URLs or verbatim correspondence.
"""

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
GENERATED = "2026-08-15"
BASE_RELEASE = "0.16-grammar-connections-presentation-alpha"
EXTENSION_VERSION = "doncaster-lineage-2026-08-15"


def enc(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False)


def dec(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    if not value:
        return []
    try:
        decoded = json.loads(value)
    except (TypeError, json.JSONDecodeError):
        return []
    return [str(item) for item in decoded] if isinstance(decoded, list) else []


def upsert(items: list[dict[str, Any]], incoming: list[dict[str, Any]], key: str) -> None:
    positions = {item.get(key): index for index, item in enumerate(items)}
    for item in incoming:
        if item[key] in positions:
            items[positions[item[key]]] = item
        else:
            positions[item[key]] = len(items)
            items.append(item)


PRIVATE_NOTE = (
    "Authorized private research source. Public metadata is paraphrased; message identifiers, "
    "addresses, private URLs and unnecessary extracts are omitted."
)


# id, title, type, url, date, creators, notes, access, tier, publisher
SOURCE_ROWS = [
    ("src_doncaster_interview_2026", "Interview with Damian Allen on systems practice in Doncaster", "private_interview_transcript", "", "2026-05-06", ["Damian Allen", "Benjamin P Taylor"], PRIVATE_NOTE, "private", "A", ""),
    ("src_damian_lineage_diagram_2026", "Lineages of Systems Practice — Damian Allen", "private_practitioner_lineage_diagram", "", "2026-05", ["Damian Allen"], PRIVATE_NOTE + " This is a first-person lineage claim, not independent proof of influence.", "private", "A", ""),
    ("src_damian_correspondence_2026", "Damian Allen follow-up correspondence on lineage and UTSI", "private_correspondence", "", "2026-05 and 2026-08", ["Damian Allen"], PRIVATE_NOTE + " Unpublished theoretical claims remain provisional.", "private", "A", ""),
    ("src_doncaster_key_messages_2026", "Approved key messages and draft public copy from the Doncaster interview", "private_approved_editorial_material", "", "2026-05", ["Damian Allen", "Benjamin P Taylor"], PRIVATE_NOTE + " Used for approved synthesis and cautions, not independent evaluation.", "private", "A", ""),
    ("src_don_council_leadership", "Chief Executive and Directors — City of Doncaster Council", "official_council_page", "https://www.doncaster.gov.uk/services/the-council-democracy/chief-executive-and-directors", "", ["City of Doncaster Council"], "Official current role record for Damian Allen.", "public", "A", "City of Doncaster Council"),
    ("src_don_corporate_plan_2026", "City of Doncaster Council Corporate Plan 2026–27", "official_council_plan", "https://www.doncaster.gov.uk/Documents/DocumentView/Stream/Media/Default/Council%20and%20Democracy/Documents/City%20of%20Doncaster%20Council%20Corporate%20Plan%202026-27.pdf", "2026", ["City of Doncaster Council"], "Official plan describing Thrive as a way of working and framework for integrated neighbourhood working.", "public", "A", "City of Doncaster Council"),
    ("src_don_corporate_plan_2024", "City of Doncaster Council Corporate Plan 2024–25", "official_council_plan", "https://www.doncaster.gov.uk/documents/DocumentView/Stream/Media/Default/Council%20and%20Democracy/Documents/Corporate%20Policy%20And%20Performance/2024%202025%20Corporate%20Plan.pdf", "2024", ["City of Doncaster Council"], "Official plan recording Choose Kindness within the council's programme of work.", "public", "A", "City of Doncaster Council"),
    ("src_don_public_health_report", "City of Doncaster Public Health Annual Report 2024", "official_public_health_report", "https://www.doncaster.gov.uk/Documents/DocumentView/Stream/Media/Default/HealthWellbeing/DES-1888-Public-Health-Annual-Report.pdf", "2024", ["City of Doncaster Council"], "Official report describing Thrive through relational practice, community work and the Liberated Method.", "public", "A", "City of Doncaster Council"),
    ("src_don_hls_story", "Human Learning Systems — the story so far", "official_project_history", "https://www.humanlearning.systems/the-story-so-far/", "", ["Human Learning Systems"], "Official project history.", "public", "B", "Human Learning Systems"),
    ("src_don_hls_liberated", "Human Learning Systems and the Liberated Method", "practice_report", "https://www.humanlearning.systems/uploads/HLSandLiberatedMethod.pdf", "", ["Toby Lowe", "Mark Smith", "Hannah Hesselgreaves"], "Practice report joining Human Learning Systems with the Liberated Method.", "public", "A", "Human Learning Systems"),
    ("src_don_harnessing_complexity", "Harnessing Complexity for Better Outcomes in Public and Non-profit Services", "university_publication_record", "https://e-space.mmu.ac.uk/637313/", "2023", ["Max French", "Hannah Hesselgreaves", "Rob Wilson", "Melissa Hawkins", "Toby Lowe"], "Official record. Strongest probable, but not certain, match for Damian's unnamed accessible complexity book.", "public", "A", "Policy Press"),
    ("src_don_three_horizons", "Three Horizons: The Patterning of Hope", "official_book_page", "https://www.internationalfuturesforum.com/p/three-horizons-the-patterning-of-hope", "", ["Bill Sharpe"], "Official International Futures Forum book page.", "public", "A", "International Futures Forum"),
    ("src_don_regenerative_cultures", "Designing Regenerative Cultures", "official_publisher_page", "https://www.triarchypress.net/drc.html", "2016; revised 2022", ["Daniel Christian Wahl"], "Publisher record covering place, scale, social innovation, Three Horizons and regenerative economy.", "public", "A", "Triarchy Press"),
    ("src_don_gregg_behr", "Gregg Behr — Remake Learning", "official_practitioner_profile", "https://remakelearning.org/directory/gregg-behr/", "", ["Remake Learning"], "Official founder and co-chair profile.", "public", "B", "Remake Learning"),
    ("src_don_remake_playbook", "Remake Learning Playbook", "official_practice_guide", "https://playbook.remakelearning.org/", "", ["Remake Learning"], "Official guide for building learning ecosystems.", "public", "A", "Remake Learning"),
    ("src_don_abcd", "The Four Essential Elements of an Asset-Based Community Development Process", "institute_practice_paper", "https://resources.depaul.edu/abcd-institute/publications/publications-by-topic/Documents/4_Essential_Elements_of_ABCD_Process.pdf", "2018", ["John McKnight", "Cormac Russell"], "Primary practice paper setting out four elements of ABCD.", "public", "A", "ABCD Institute at DePaul University"),
    ("src_don_midgley_profile", "Professor Gerald Midgley — University of Hull", "official_university_profile", "https://www.hull.ac.uk/staff-directory/gerald-midgley", "", ["University of Hull"], "Official profile for Midgley's systems and systemic-intervention work.", "public", "A", "University of Hull"),
    ("src_don_systemic_intervention", "Systemic Intervention: Philosophy, Methodology, and Practice", "university_repository_record", "https://hull-repository.worktribe.com/output/385209", "2000", ["Gerald Midgley"], "University repository record; it does not verify the separate Nested Minimum Viable Systems phrase.", "public", "A", "Kluwer Academic / Plenum"),
    ("src_don_fullan", "Leadership & Sustainability: System Thinkers in Action", "official_author_book_page", "https://michaelfullan.ca/books/leadership-sustainability/", "2004", ["Michael Fullan"], "Likely public context for Damian's systems-thinker-in-action recollection.", "public", "A", "Corwin Press"),
    ("src_don_bruce_edmonds", "Complexity and Scientific Modelling", "research_centre_paper", "https://cfpm.org/cpmrep118.html", "", ["Bruce Edmonds"], "MMU Centre for Policy Modelling paper containing the published aphorism and supporting a probable identity normalization.", "public", "A", "Centre for Policy Modelling"),
    ("src_don_robert_geyer", "Professor Robert Geyer — Lancaster University", "official_university_profile", "https://www.lancaster.ac.uk/humanities-arts-and-social-sciences/people/robert-geyer", "", ["Lancaster University"], "Official profile listing work on complexity and public policy.", "public", "A", "Lancaster University"),
    ("src_don_lineages_article", "Lineages of Systems Practices", "practice_field_article", "https://www.schoolofsystemchange.org/blog/lineages-of-systems-practices", "2026-01-29", ["Laura Winn", "Saskia Rysenbry"], "An explicitly partial, non-exhaustive lineage article inviting non-extractive lineage practice.", "public", "A", "School of System Change"),
    ("src_don_jenny_andersson", "Jenny Andersson — Really Regenerative", "official_practitioner_profile", "https://reallyregenerative.org/jenny-andersson/", "", ["Really Regenerative CIC"], "Official profile for place-based regenerative practice.", "public", "B", "Really Regenerative CIC"),
    ("src_don_place_regeneration", "Place-based Regeneration: Capabilities for Transformative Change", "practice_research_report", "https://reallyregenerative.org/wp-content/uploads/2025/09/Place-based-Regeneration-Capabilities-for-Transformative-Change-Report-2025-compressed-1.pdf", "2025", ["Really Regenerative CIC"], "Practice research on place-based regenerative capabilities.", "public", "B", "Really Regenerative CIC"),
    ("src_don_simon_duffy", "Simon Duffy — Citizen Network", "official_practitioner_profile", "https://citizen-network.org/about/people/simon-duffy", "", ["Citizen Network"], "Official profile for Duffy's citizenship practice.", "public", "B", "Citizen Network"),
    ("src_don_neighbourhoods", "Neighbourhoods of Care", "practice_network_page", "https://citizen-network.org/library/neighbourhoods-of-care.html", "", ["Citizen Network"], "Citizen Network page naming Doncaster among neighbourhood-based work.", "public", "B", "Citizen Network"),
    ("src_don_rupert_suckling", "Dr Rupert Suckling — Well North", "official_practitioner_profile", "https://wellnorth.co.uk/about-us/our-team/our-executive/dr-rupert-suckling", "", ["Well North"], "Official profile recording Suckling's Doncaster and Well North work.", "public", "B", "Well North"),
    ("src_don_bourdieu", "The Forms of Capital", "bibliographic_record", "", "1986", ["Pierre Bourdieu"], "Bibliographic record; no open primary copy is asserted here.", "published_no_public_link", "A", "Greenwood Press"),
    ("src_don_bronfenbrenner", "The Ecology of Human Development", "bibliographic_record", "", "1979", ["Urie Bronfenbrenner"], "Bibliographic record; no open primary copy is asserted here.", "published_no_public_link", "A", "Harvard University Press"),
]


def source_records() -> list[dict[str, Any]]:
    output = []
    for sid, title, kind, url, date, creators, notes, access, tier, publisher in SOURCE_ROWS:
        output.append({
            "id": sid, "title": title, "source_type": kind, "quality_tier": tier,
            "access": access, "url": url, "date": date, "notes": notes,
            "creators": enc(creators), "doi": "", "isbn": "", "publisher": publisher,
            "licence": "source_terms" if url else "", "archived_url": "", "content_hash": "",
            "review_status": "checked_for_doncaster_lineage", "last_checked": GENERATED,
            "public_link_status": "public_link" if url else "no_public_link",
        })
    return output


# id, label, type, description, source ids, aliases, publication level
NODE_ROWS = [
    ("person_damian_allen", "Damian Allen", "person", "Chief Executive of City of Doncaster Council whose stated practice lineage joins ecology, philosophy, learning, systems, complexity, cybernetics, design, place, regeneration and relational public services.", ["src_don_council_leadership", "src_doncaster_interview_2026", "src_damian_lineage_diagram_2026", "src_damian_correspondence_2026"], [], "profile"),
    ("person_michael_fullan", "Michael Fullan", "person", "Education scholar whose 'system thinkers in action' formulation is recalled by Damian as an early recognition of theory enacted through practice.", ["src_doncaster_interview_2026", "src_don_fullan"], [], "described"),
    ("person_gregg_behr", "Gregg Behr", "person", "Founder and co-chair of Remake Learning, named by Damian in relation to learning anywhere, learning from everyone and place-based small bets.", ["src_doncaster_interview_2026", "src_don_gregg_behr"], [], "described"),
    ("person_toby_lowe", "Toby Lowe", "person", "Public-service researcher and Human Learning Systems practitioner named by Damian as a collaborator on relational public services.", ["src_doncaster_interview_2026", "src_damian_correspondence_2026", "src_don_hls_liberated"], [], "described"),
    ("person_mark_smith_hls", "Mark Smith", "person", "Human Learning Systems practitioner named by Damian as a collaborator on the relational public-service approach used in Thrive.", ["src_doncaster_interview_2026", "src_damian_correspondence_2026", "src_don_hls_liberated"], ["Mark Smith (Human Learning Systems)"], "described"),
    ("person_hannah_hesselgreaves", "Hannah Hesselgreaves", "person", "Public-service complexity researcher and Human Learning Systems co-author named in Damian's account.", ["src_doncaster_interview_2026", "src_don_hls_liberated", "src_don_harnessing_complexity"], [], "described"),
    ("person_tony_hodgson", "Tony Hodgson", "person", "Systems practitioner whom Damian credits, alongside Bill Sharpe, in his practical Three Horizons lineage.", ["src_doncaster_interview_2026", "src_damian_correspondence_2026", "src_don_three_horizons"], [], "described"),
    ("person_bill_sharpe", "Bill Sharpe", "person", "Author of Three Horizons: The Patterning of Hope and a named source in Damian's futures-practice lineage.", ["src_doncaster_interview_2026", "src_don_three_horizons"], [], "described"),
    ("person_cormac_russell", "Cormac Russell", "person", "Asset-Based Community Development practitioner and co-author named in Damian's Doncaster practice lineage and public-service account.", ["src_doncaster_interview_2026", "src_don_abcd"], [], "described"),
    ("person_simon_duffy", "Simon Duffy", "person", "Citizen Network founder whose citizenship and neighbourhood perspective is named in Damian's account.", ["src_doncaster_interview_2026", "src_don_simon_duffy", "src_don_neighbourhoods"], [], "described"),
    ("person_daniel_christian_wahl", "Daniel Christian Wahl", "person", "Author and regenerative-cultures practitioner named by Damian as an influence and collaborator.", ["src_doncaster_interview_2026", "src_damian_correspondence_2026", "src_don_regenerative_cultures"], ["Daniel Wahl"], "described"),
    ("person_rupert_suckling", "Rupert Suckling", "person", "Public-health leader whom Damian credits with bringing Well North into work that became Well Doncaster.", ["src_doncaster_interview_2026", "src_don_rupert_suckling"], [], "described"),
    ("person_bruce_edmonds", "Bruce Edmonds", "person", "Complexity researcher at Manchester Metropolitan University's Centre for Policy Modelling; a probable normalization of Damian's recollection 'Bruce Edwards'.", ["src_damian_correspondence_2026", "src_don_bruce_edmonds"], ["Bruce Edwards (Damian Allen recollection; probable misnaming)"], "described"),
    ("person_robert_geyer", "Robert Geyer", "person", "Lancaster scholar of complexity and public policy whom Damian names as an early-2000s collaborator.", ["src_damian_correspondence_2026", "src_don_robert_geyer"], [], "described"),
    ("person_pierre_bourdieu", "Pierre Bourdieu", "person", "Sociologist and author of The Forms of Capital, whose framework Damian explicitly names as a theoretical commitment.", ["src_damian_correspondence_2026", "src_don_bourdieu"], [], "described"),
    ("person_urie_bronfenbrenner", "Urie Bronfenbrenner", "person", "Developmental psychologist whose ecological systems theory Damian explicitly names as a theoretical commitment.", ["src_damian_correspondence_2026", "src_don_bronfenbrenner"], [], "described"),
    ("person_laura_winn", "Laura Winn", "person", "Systems-change practitioner and co-author of Lineages of Systems Practices, explicitly named by Damian.", ["src_damian_correspondence_2026", "src_don_lineages_article"], [], "described"),
    ("person_saskia_rysenbry", "Saskia Rysenbry", "person", "Systems-change practitioner and co-author of Lineages of Systems Practices, explicitly named by Damian.", ["src_damian_correspondence_2026", "src_don_lineages_article"], [], "described"),
    ("person_jenny_andersson", "Jenny Andersson", "person", "Really Regenerative practitioner named by Damian in connection with place-based regenerative projects.", ["src_damian_correspondence_2026", "src_don_jenny_andersson", "src_don_place_regeneration"], [], "described"),
    ("person_bertrand_russell", "Bertrand Russell", "person", "Philosopher and public intellectual appearing by name in Damian's self-authored philosophy lineage strand and timeline.", ["src_damian_lineage_diagram_2026"], [], "described"),
    ("person_lev_vygotsky", "Lev Vygotsky", "person", "Psychologist associated with socially situated learning who appears by name in Damian's self-authored learning-theory lineage strand.", ["src_damian_lineage_diagram_2026"], [], "described"),
    ("person_william_james", "William James", "person", "Psychologist and philosopher appearing by name alongside Vygotsky in Damian's self-authored learning-theory lineage strand.", ["src_damian_lineage_diagram_2026"], [], "described"),
    ("practice_doncaster_thrive", "Doncaster Thrive", "practice", "A place-based Doncaster way of working that combines relational public services, community assets, wellbeing, locality structures and adaptive learning; it is explicitly described as more than a programme.", ["src_don_corporate_plan_2026", "src_don_public_health_report", "src_doncaster_interview_2026"], [], "profile"),
    ("practice_relational_public_services", "Relational public services", "practice", "Public-service practice that treats trust, context, tacit knowledge and human relationships as operating conditions rather than delivery decoration.", ["src_doncaster_interview_2026", "src_doncaster_key_messages_2026", "src_don_hls_liberated"], [], "described"),
    ("practice_asset_based_community_development", "Asset-Based Community Development", "practice", "Community practice that starts from local assets, relationships and capacities while recognizing that capacity is uneven and may need support.", ["src_doncaster_interview_2026", "src_don_abcd"], ["ABCD"], "profile"),
    ("practice_place_based", "Place-based practice", "practice", "Practice that works with the history, relationships, capacities and authorizing conditions of a particular place instead of transplanting a universal model.", ["src_doncaster_interview_2026", "src_doncaster_key_messages_2026", "src_don_place_regeneration"], [], "described"),
    ("concept_authorizing_environment", "Authorizing environment", "concept", "The political, executive, policy and organizational conditions that make adaptive, relational practice possible and durable.", ["src_doncaster_interview_2026", "src_doncaster_key_messages_2026"], ["Authorising environment"], "described"),
    ("practice_organizational_learning", "Organizational learning", "practice", "The deliberate design of feedback, inquiry and adaptation into an organization's operating system.", ["src_doncaster_interview_2026", "src_doncaster_key_messages_2026", "src_damian_lineage_diagram_2026"], ["Organisational learning"], "described"),
    ("practice_regenerative_cultures", "Regenerative cultures", "practice", "A design and practice orientation concerned with renewing the life-supporting capacity of places and communities.", ["src_damian_lineage_diagram_2026", "src_don_regenerative_cultures"], [], "described"),
    ("method_three_horizons", "Three Horizons", "method_or_methodology", "A futures-practice framework for relating a dominant present, emerging alternatives and a longer-horizon pattern of transformation.", ["src_doncaster_interview_2026", "src_don_three_horizons"], [], "profile"),
    ("practice_human_learning_systems", "Human Learning Systems", "practice", "A public-service approach organized around human relationships, learning and systems conditions in complex environments.", ["src_don_hls_story", "src_don_hls_liberated", "src_doncaster_interview_2026"], ["HLS"], "profile"),
    ("practice_learning_ecosystems", "Learning ecosystems", "practice", "Place-based networks in which schools, families, businesses, civic organizations and informal settings create multiple routes for learning.", ["src_doncaster_interview_2026", "src_don_remake_playbook"], [], "described"),
    ("practice_innovation_ecosystems", "Innovation ecosystems", "practice", "Networks that support experimentation, exchange, shared learning and cumulative innovation across organizational and sector boundaries.", ["src_damian_lineage_diagram_2026", "src_doncaster_interview_2026"], [], "described"),
    ("practice_social_innovation", "Social innovation", "practice", "Collaborative development of practices and arrangements intended to change social outcomes and system conditions.", ["src_damian_lineage_diagram_2026", "src_don_regenerative_cultures"], [], "described"),
    ("practice_design_thinking", "Design thinking", "practice", "A human-centred, prototyping-oriented practice strand in Damian's lineage diagram, connecting inquiry with bounded experimentation and adaptation.", ["src_damian_lineage_diagram_2026"], ["Human-centred design", "Human-centered design"], "described"),
    ("tradition_evolutionary_ecology", "Evolutionary ecology", "tradition", "Damian's early ecology strand, grounded in zoology, population dynamics and evolving organism–environment relations.", ["src_damian_lineage_diagram_2026"], [], "described"),
    ("concept_population_dynamics", "Population dynamics", "concept", "Study of how populations change through interacting rates and environmental conditions; Damian traces an early systems sensibility to this work.", ["src_damian_lineage_diagram_2026"], [], "described"),
    ("concept_community_ecology", "Community ecology", "concept", "Study of interacting populations and ecological communities, appearing in Damian's MSc Environment strand.", ["src_damian_lineage_diagram_2026"], [], "described"),
    ("tradition_philosophy_damian", "Philosophy in Damian Allen's lineage", "tradition", "A self-reported strand naming Stephen Jay Gould and Bertrand Russell; it records Damian's grouping rather than defining philosophy as a whole.", ["src_damian_lineage_diagram_2026"], [], "described"),
    ("tradition_learning_theory", "Learning theory", "tradition", "A lineage strand naming Vygotsky and James and connecting learning to socially situated practice.", ["src_damian_lineage_diagram_2026", "src_damian_correspondence_2026"], [], "described"),
    ("tradition_organizational_theory", "Organizational theory", "tradition", "A lineage strand connecting Damian's experience of ICI and schools to later public-service organizational design.", ["src_damian_lineage_diagram_2026", "src_doncaster_key_messages_2026"], ["Organisational theory"], "described"),
    ("tradition_complexity_theory", "Complexity theory", "tradition", "A lineage strand connecting Santa Fe, agent models and public-service complexity in Damian's account.", ["src_damian_lineage_diagram_2026", "src_damian_correspondence_2026", "src_don_robert_geyer"], [], "described"),
    ("practice_circular_economy", "Circular economy", "practice", "An economy-oriented practice strand that Damian places alongside regenerative thinking without treating circularity and regeneration as synonyms.", ["src_damian_correspondence_2026", "src_don_regenerative_cultures"], [], "described"),
    ("practice_permaculture", "Permaculture", "practice", "A regenerative design practice named in Damian's lineage diagram as one route into his wider regenerative-cultures work.", ["src_damian_lineage_diagram_2026", "src_don_regenerative_cultures"], [], "described"),
    ("concept_contributory_state", "Contributory state", "concept", "Damian's term for a public-service settlement organized around contribution, reciprocity and pay-it-forward relations rather than transaction alone.", ["src_doncaster_interview_2026", "src_doncaster_key_messages_2026"], [], "described"),
    ("practice_choose_kindness", "Choose Kindness", "practice", "A Doncaster practice proposition explicitly bounded by the caution that kindness must not replace rights, resources or accountability.", ["src_doncaster_interview_2026", "src_doncaster_key_messages_2026", "src_don_corporate_plan_2024"], ["Kindness"], "described"),
    ("concept_systems_intelligence", "Systems intelligence", "concept", "The capacity to perceive and act within relational, nested and changing systems, used by Damian to connect practical judgment with multiple systems traditions.", ["src_doncaster_interview_2026", "src_damian_lineage_diagram_2026", "src_damian_correspondence_2026"], [], "described"),
    ("concept_municipal_brain", "Municipal brain", "concept", "Damian's speculative metaphor for a council's future capacity to connect distributed knowledge, systems intelligence, augmented knowledge and responsible AI.", ["src_doncaster_interview_2026"], [], "described"),
    ("concept_nested_minimum_viable_systems", "Nested Minimum Viable Systems", "concept", "A phrase Damian attributes to work with Gerald Midgley. No corroborating public publication or stable formal definition was located.", ["src_doncaster_interview_2026", "src_damian_correspondence_2026"], ["NMVS"], "research_stub"),
    ("theory_unified_systems_intelligence", "Unified Theory of Systems Intelligence", "theory", "Damian's unpublished proto-theory proposing a synthesis of systems and cognitive-science frameworks, possibly using coupled nonlinear differential equations. It is not presented as established or validated.", ["src_damian_lineage_diagram_2026", "src_damian_correspondence_2026"], ["UTSI"], "research_stub"),
    ("practice_well_doncaster", "Well Doncaster", "practice", "Doncaster's community-health practice lineage, described by Damian as carrying Well North and ABCD into local work.", ["src_doncaster_interview_2026", "src_don_rupert_suckling"], [], "described"),
    ("practice_remake_learning", "Remake Learning", "practice", "A place-based learning network and practice model founded by Gregg Behr and adapted in Damian's account through a parallel Doncaster festival.", ["src_doncaster_interview_2026", "src_don_gregg_behr", "src_don_remake_playbook"], [], "described"),
    ("practice_small_bets", "Small bets", "practice", "A stance of starting from present conditions, working with available people and making bounded experiments that generate learning.", ["src_doncaster_interview_2026", "src_don_remake_playbook"], [], "described"),
    ("practice_team_doncaster", "Team Doncaster", "practice", "The place partnership through which Damian describes Doncaster's mission, locality structure and shared work across organizations.", ["src_doncaster_interview_2026", "src_don_corporate_plan_2026"], [], "described"),
    ("concept_socially_situated_action", "Socially situated action", "concept", "Damian's proposition that action is embedded in place and nested social context rather than separable from it.", ["src_damian_correspondence_2026"], [], "described"),
    ("concept_forms_of_capital", "Forms of capital", "concept", "Bourdieu's distinction among economic, cultural and social capital, with symbolic capital arising through recognized legitimacy; Damian explicitly names it.", ["src_damian_correspondence_2026", "src_don_bourdieu"], [], "described"),
    ("concept_ecological_systems_theory", "Ecological systems theory", "concept", "Bronfenbrenner's account of development across nested environmental systems; Damian explicitly names it.", ["src_damian_correspondence_2026", "src_don_bronfenbrenner"], [], "described"),
    ("publication_designing_regenerative_cultures", "Designing Regenerative Cultures", "publication", "Daniel Christian Wahl's book on regenerative design and cultural change, explicitly named in Damian's lineage.", ["src_don_regenerative_cultures", "src_damian_correspondence_2026"], [], "profile"),
    ("publication_three_horizons", "Three Horizons: The Patterning of Hope", "publication", "Bill Sharpe's book presenting the Three Horizons pattern for transformative futures practice.", ["src_don_three_horizons", "src_doncaster_interview_2026"], [], "profile"),
    ("publication_hls_liberated", "Human Learning Systems and the Liberated Method", "publication", "A practice report by Toby Lowe, Mark Smith and Hannah Hesselgreaves connecting Human Learning Systems to the Liberated Method.", ["src_don_hls_liberated"], [], "described"),
    ("publication_harnessing_complexity", "Harnessing Complexity for Better Outcomes in Public and Non-profit Services", "publication", "The strongest located candidate for Damian's unnamed accessible complexity book; the identification remains probable rather than certain.", ["src_don_harnessing_complexity", "src_doncaster_interview_2026"], [], "described"),
    ("publication_remake_learning_playbook", "Remake Learning Playbook", "publication", "A public practice guide for building connected, place-based learning ecosystems through network stewardship and collaborative experimentation.", ["src_don_remake_playbook"], [], "described"),
    ("publication_fullan_leadership", "Leadership & Sustainability: System Thinkers in Action", "publication", "Michael Fullan's 2004 leadership book and the likely public context for Damian's recollection of a systems thinker in action.", ["src_don_fullan", "src_doncaster_interview_2026"], [], "described"),
    ("publication_forms_of_capital", "The Forms of Capital", "publication", "Pierre Bourdieu's account of forms of capital, explicitly named in Damian's correspondence.", ["src_don_bourdieu", "src_damian_correspondence_2026"], [], "described"),
    ("publication_ecology_human_development", "The Ecology of Human Development", "publication", "Urie Bronfenbrenner's book on nested ecological systems, explicitly named in Damian's correspondence.", ["src_don_bronfenbrenner", "src_damian_correspondence_2026"], [], "described"),
    ("publication_lineages_systems_practices", "Lineages of Systems Practices", "publication", "Laura Winn and Saskia Rysenbry's intentionally partial lineage article, explicitly named by Damian.", ["src_don_lineages_article", "src_damian_correspondence_2026"], [], "described"),
    ("publication_systemic_intervention_midgley", "Systemic Intervention: Philosophy, Methodology, and Practice", "publication", "Gerald Midgley's book; it provides public context but does not verify Nested Minimum Viable Systems.", ["src_don_systemic_intervention", "src_don_midgley_profile"], [], "described"),
    ("publication_four_elements_abcd", "The Four Essential Elements of an Asset-Based Community Development Process", "publication", "John McKnight and Cormac Russell's practice paper setting out four essential elements of an Asset-Based Community Development process.", ["src_don_abcd"], [], "described"),
    ("publication_complexity_public_policy_geyer", "Complexity and Public Policy", "publication", "Robert Geyer's book on complexity and public policy, relevant to Damian's early public-service complexity collaboration.", ["src_don_robert_geyer", "src_damian_correspondence_2026"], [], "described"),
]


def node_records() -> list[dict[str, Any]]:
    output = []
    for index, (nid, label, kind, description, sources, aliases, level) in enumerate(NODE_ROWS):
        provisional = level == "research_stub"
        output.append({
            "id": nid, "label": label, "entity_type": kind, "description": description,
            "aliases": enc(aliases), "boundary_ring": "0", "inclusion_reason": "damian_allen_doncaster_lineage_2026",
            "status": "candidate" if provisional else "accepted", "source_ids": enc(sources),
            "set_tags": enc(["systems", "practice", "doncaster_lineage"]), "espoused_labels": "[]", "observed_clusters": "[]",
            "canonical_definition": description, "valid_from": "", "valid_to": "", "external_ids": "{}", "geographies": enc(["Doncaster"] if "doncaster" in nid else []),
            "licence": "", "review_status": "provisional_self_reported" if provisional else "doncaster_lineage_source_checked",
            "reviewed_by": "Benjamin P Taylor", "reviewed_at": GENERATED,
            "x": round(0.48 + ((index % 9) - 4) * 0.052, 6), "y": round(-0.68 + (index // 9) * 0.06, 6),
            "canonical_id": nid, "public_visibility": "public", "publication_level": level,
            "public_stub_text": "", "public_source_count": 0, "no_public_link_count": 0,
        })
    return output


def edge(
    eid: str, source: str, target: str, relation_type: str, family: str,
    phrase: str, source_ids: list[str], locator: str, notes: str, *,
    status: str = "accepted", mode: str = "asserted", confidence: float = 0.90,
    scope: str = "", inference: str = "", directed: bool = True,
) -> dict[str, Any]:
    return {
        "id": eid, "source": source, "target": target, "relation_type": relation_type,
        "relation_family": family, "directed": "true" if directed else "false",
        "dependency_kind": "", "confidence": f"{confidence:.2f}", "claim_status": status,
        "source_ids": enc(source_ids), "evidence_ids": "[]", "source_locator": locator,
        "valid_from": "", "valid_to": "", "scope_conditions": scope,
        "assertion_mode": mode, "inference_method": inference, "claim_id": "",
        "reviewed_by": "Benjamin P Taylor", "reviewed_at": GENERATED,
        "notes": notes, "plain_phrase": phrase,
        "public_review_label": (
            "provisional interpretation — inspect locator and uncertainty"
            if status != "accepted" or mode == "interpreted" else "source-backed relationship"
        ),
    }


def build_edges() -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    interview = ["src_doncaster_interview_2026"]
    diagram = ["src_damian_lineage_diagram_2026"]
    correspondence = ["src_damian_correspondence_2026"]

    # First-person people lineage. These edges establish the claim, not causal proof.
    people = [
        ("fullan", "person_michael_fullan", "interview transcript, 11:00", interview, "Damian recalls Fullan's phrase as early validation of theory enacted through practice."),
        ("behr", "person_gregg_behr", "interview transcript, 36:24", interview, "Damian names Behr while explaining the place-based learning principles adapted in Doncaster."),
        ("lowe", "person_toby_lowe", "interview transcript, 42:40; pre-interview statement, relational approaches paragraph", interview + correspondence, "Damian explicitly names sustained work with Lowe on relational public services."),
        ("smith", "person_mark_smith_hls", "pre-interview statement, relational approaches paragraph", correspondence, "Damian explicitly names sustained work with Smith on relational public services."),
        ("hesselgreaves", "person_hannah_hesselgreaves", "interview transcript, 42:40", interview, "Damian names Hesselgreaves in the HLS and public-service complexity context."),
        ("hodgson", "person_tony_hodgson", "interview transcript, 42:40–43:21", interview, "Damian names Hodgson in his practical Three Horizons lineage."),
        ("sharpe", "person_bill_sharpe", "interview transcript, 42:40–43:21", interview, "Damian names Sharpe in his practical Three Horizons lineage."),
        ("russell_abcd", "person_cormac_russell", "interview transcript, 43:21", interview, "Damian names Russell when describing the ABCD route into Doncaster practice."),
        ("duffy", "person_simon_duffy", "interview transcript, 43:42", interview, "Damian names Duffy's citizenship perspective in connection with neighbourhood practice."),
        ("wahl", "person_daniel_christian_wahl", "interview transcript, 43:58 onward; pre-interview statement, regenerative cultures paragraph", interview + correspondence, "Damian explicitly names Wahl's work and prior collaboration."),
        ("suckling", "person_rupert_suckling", "interview transcript, 43:58 onward", interview, "Damian credits Suckling with bringing Well North into Doncaster's community-health lineage."),
        ("midgley", "person_gerald_midgley", "interview transcript, 43:58 onward; pre-interview statement, Nested Minimum Viable Systems sentence", interview + correspondence, "Damian names Midgley in relation to systemic practice and a provisional nested-systems formulation."),
        ("geyer", "person_robert_geyer", "follow-up correspondence, early-2000s complexity paragraph", correspondence, "Damian explicitly names Geyer as a collaborator on complexity in public services."),
        ("bourdieu", "person_pierre_bourdieu", "follow-up correspondence, theoretical commitments paragraph", correspondence, "Damian explicitly states his commitment to Bourdieu's forms-of-capital framework."),
        ("bronfenbrenner", "person_urie_bronfenbrenner", "follow-up correspondence, theoretical commitments paragraph", correspondence, "Damian explicitly states his commitment to Bronfenbrenner's ecological systems theory."),
        ("winn", "person_laura_winn", "follow-up correspondence, lineages article paragraph", correspondence, "Damian explicitly names Winn's lineage article."),
        ("rysenbry", "person_saskia_rysenbry", "follow-up correspondence, lineages article paragraph", correspondence, "Damian explicitly names Rysenbry's lineage article."),
        ("andersson", "person_jenny_andersson", "follow-up correspondence, regenerative place projects paragraph", correspondence, "Damian explicitly names Andersson and Really Regenerative's place-based work."),
        ("gould", "person_fpcs_s_j_gould", "lineage diagram, slide 1, ‘Philosophy’ box", diagram, "Gould appears by name in Damian's self-authored philosophy strand."),
        ("bertrand_russell", "person_bertrand_russell", "lineage diagram, slide 1, ‘Philosophy’ box", diagram, "Russell appears by name in Damian's self-authored philosophy strand."),
        ("vygotsky", "person_lev_vygotsky", "lineage diagram, slide 1, ‘Learning Theory’ box", diagram, "Vygotsky appears by name in Damian's self-authored learning-theory strand."),
        ("james", "person_william_james", "lineage diagram, slide 1, ‘Learning Theory’ box", diagram, "James appears by name in Damian's self-authored learning-theory strand."),
        ("weaver", "person_fpcs_w_weaver", "lineage diagram, slide 1, ‘Information Theory’ box", diagram, "Weaver appears by name in Damian's self-authored information-theory strand."),
        ("shannon", "person_claude_e_shannon", "lineage diagram, slide 1, ‘Information Theory’ box", diagram, "Shannon appears by name in Damian's self-authored information-theory strand."),
        ("beer", "person_stafford_beer", "lineage diagram, slide 1, ‘Cybernetics’ box", diagram, "Beer appears by name in Damian's self-authored cybernetics strand."),
        ("ashby", "person_w_ross_ashby", "lineage diagram, slide 1, ‘Cybernetics’ box", diagram, "Ashby appears by name in Damian's self-authored cybernetics strand."),
    ]
    for slug, target, locator, sources, notes in people:
        output.append(edge(
            f"e_don_lineage_{slug}", "person_damian_allen", target,
            "claims_lineage_from", "identity", "claims lineage from", sources, locator, notes,
            confidence=0.94,
            scope="First-person lineage claim; it records Damian's intellectual development and does not independently prove direct causal influence.",
        ))
    output.append(edge(
        "e_don_lineage_bruce_edmonds", "person_damian_allen", "person_bruce_edmonds",
        "claims_lineage_from", "identity", "probably identifies as an early collaborator",
        correspondence + ["src_don_bruce_edmonds"], "follow-up correspondence, early-2000s complexity paragraph; Centre for Policy Modelling paper, aphorism",
        "Damian recalls 'Bruce Edwards'; MMU context and the aphorism point strongly, but not conclusively, to Bruce Edmonds.",
        status="provisional_identity_normalisation", mode="interpreted", confidence=0.68,
        scope="Preserves Damian's original recollection and makes the normalization challengeable.",
        inference="Matched institution, research topic and near-identical published aphorism.",
    ))

    # Every named diagram strand remains distinct and source-located.
    strands = [
        ("evolutionary_ecology", "tradition_evolutionary_ecology", "‘Evolutionary Ecology’ box"),
        ("population_dynamics", "concept_population_dynamics", "‘Evolutionary Ecology’ box"),
        ("community_ecology", "concept_community_ecology", "‘MSc Environment’ box"),
        ("philosophy", "tradition_philosophy_damian", "‘Philosophy’ box"),
        ("information", "concept_information_theory", "‘Information Theory’ box"),
        ("learning", "tradition_learning_theory", "‘Learning Theory’ box"),
        ("organization", "tradition_organizational_theory", "‘Organizational Theory’ box"),
        ("soft_systems", "method_or_methodology_soft_systems_methodology_ssm", "‘Systems Theory’ box"),
        ("complexity", "tradition_complexity_theory", "‘Complexity Theory’ box"),
        ("agent_models", "method_or_methodology_agent_based_modelling", "‘Complexity Theory’ box"),
        ("system_dynamics", "method_or_methodology_system_dynamics", "‘Systems Dynamics’ box"),
        ("cybernetics", "tradition_cybernetics", "‘Cybernetics’ box"),
        ("design", "practice_design_thinking", "‘Design Thinking’ box"),
        ("place", "practice_place_based", "‘Place-Based Practice’ box"),
        ("social_innovation", "practice_social_innovation", "‘Social Innovation’ box"),
        ("regenerative", "practice_regenerative_cultures", "‘Regenerative Cultures’ box"),
        ("permaculture", "practice_permaculture", "‘Regenerative Cultures’ box"),
        ("relational", "practice_relational_public_services", "‘Relational Theory’ box"),
        ("systems_intelligence", "concept_systems_intelligence", "‘UTSI’ box and diagram subtitle"),
    ]
    for slug, target, box in strands:
        output.append(edge(
            f"e_don_strand_{slug}", "person_damian_allen", target,
            "claims_lineage_from", "identity", "claims lineage from", diagram,
            f"lineage diagram, slide 1, {box}",
            "This relationship records a named strand in Damian's self-authored lineage diagram.", confidence=0.95,
            scope="First-person lineage claim; not independent proof of influence or completeness.",
        ))

    strand_members = [
        ("gould", "person_fpcs_s_j_gould", "tradition_philosophy_damian", "‘Philosophy’ box"),
        ("russell", "person_bertrand_russell", "tradition_philosophy_damian", "‘Philosophy’ box"),
        ("vygotsky", "person_lev_vygotsky", "tradition_learning_theory", "‘Learning Theory’ box"),
        ("james", "person_william_james", "tradition_learning_theory", "‘Learning Theory’ box"),
        ("weaver", "person_fpcs_w_weaver", "concept_information_theory", "‘Information Theory’ box"),
        ("shannon", "person_claude_e_shannon", "concept_information_theory", "‘Information Theory’ box"),
        ("beer", "person_stafford_beer", "tradition_cybernetics", "‘Cybernetics’ box"),
        ("ashby", "person_w_ross_ashby", "tradition_cybernetics", "‘Cybernetics’ box"),
    ]
    for slug, person, strand, box in strand_members:
        output.append(edge(
            f"e_don_strand_member_{slug}", person, strand, "part_of", "classification",
            "appears in Damian's lineage strand", diagram, f"lineage diagram, slide 1, {box}",
            "This reproduces Damian's diagram grouping; it is not a complete classification of the person's work.",
            scope="Damian Allen's self-authored lineage diagram only.",
        ))

    # Public documentary authorship.
    authored = [
        ("drc", "publication_designing_regenerative_cultures", "person_daniel_christian_wahl", "src_don_regenerative_cultures", "publisher page, bibliographic section"),
        ("three_horizons", "publication_three_horizons", "person_bill_sharpe", "src_don_three_horizons", "official book page, bibliographic section"),
        ("hls_lowe", "publication_hls_liberated", "person_toby_lowe", "src_don_hls_liberated", "report title page"),
        ("hls_smith", "publication_hls_liberated", "person_mark_smith_hls", "src_don_hls_liberated", "report title page"),
        ("hls_hesselgreaves", "publication_hls_liberated", "person_hannah_hesselgreaves", "src_don_hls_liberated", "report title page"),
        ("complexity_lowe", "publication_harnessing_complexity", "person_toby_lowe", "src_don_harnessing_complexity", "university record, authors section"),
        ("complexity_hesselgreaves", "publication_harnessing_complexity", "person_hannah_hesselgreaves", "src_don_harnessing_complexity", "university record, authors section"),
        ("fullan", "publication_fullan_leadership", "person_michael_fullan", "src_don_fullan", "official book page, title and author"),
        ("capital", "publication_forms_of_capital", "person_pierre_bourdieu", "src_don_bourdieu", "bibliographic record, chapter authorship"),
        ("ecology", "publication_ecology_human_development", "person_urie_bronfenbrenner", "src_don_bronfenbrenner", "bibliographic record, book authorship"),
        ("lineages_winn", "publication_lineages_systems_practices", "person_laura_winn", "src_don_lineages_article", "article byline"),
        ("lineages_rysenbry", "publication_lineages_systems_practices", "person_saskia_rysenbry", "src_don_lineages_article", "article byline"),
        ("systemic", "publication_systemic_intervention_midgley", "person_gerald_midgley", "src_don_systemic_intervention", "repository record, author field"),
        ("abcd", "publication_four_elements_abcd", "person_cormac_russell", "src_don_abcd", "paper title page"),
        ("geyer", "publication_complexity_public_policy_geyer", "person_robert_geyer", "src_don_robert_geyer", "official profile, publications section"),
    ]
    for slug, work, author, sid, locator in authored:
        output.append(edge(
            f"e_don_authored_{slug}", work, author, "authored_by", "documentary", "authored by",
            [sid], locator, "The named source explicitly records the work's authorship.", confidence=0.98,
        ))

    # Work-to-concept routes prevent publications and authors from becoming dead ends.
    content = [
        ("drc_regen", "publication_designing_regenerative_cultures", "practice_regenerative_cultures", "develops", "conceptual", "develops", "src_don_regenerative_cultures", "publisher page, contents and themes"),
        ("drc_horizons", "publication_designing_regenerative_cultures", "method_three_horizons", "presents", "documentary", "presents", "src_don_regenerative_cultures", "publisher contents, Three Horizons discussion"),
        ("horizons_method", "publication_three_horizons", "method_three_horizons", "develops", "conceptual", "develops", "src_don_three_horizons", "official book page, method summary"),
        ("hls_report", "publication_hls_liberated", "practice_human_learning_systems", "presents", "documentary", "presents", "src_don_hls_liberated", "report, sections 1–3"),
        ("playbook", "publication_remake_learning_playbook", "practice_learning_ecosystems", "translates_for_practice", "practice", "translates for practice", "src_don_remake_playbook", "playbook, network-building sections"),
        ("abcd_method", "publication_four_elements_abcd", "practice_asset_based_community_development", "develops", "conceptual", "develops", "src_don_abcd", "paper, four-element framework"),
        ("capital_concept", "publication_forms_of_capital", "concept_forms_of_capital", "develops", "conceptual", "develops", "src_don_bourdieu", "chapter, forms-of-capital distinction"),
        ("ecology_concept", "publication_ecology_human_development", "concept_ecological_systems_theory", "develops", "conceptual", "develops", "src_don_bronfenbrenner", "book, ecological systems account"),
        ("geyer_complexity", "publication_complexity_public_policy_geyer", "tradition_complexity_theory", "translates_for_practice", "practice", "translates for public policy", "src_don_robert_geyer", "official profile, publications section"),
    ]
    for slug, source, target, rel, family, phrase, sid, locator in content:
        output.append(edge(
            f"e_don_content_{slug}", source, target, rel, family, phrase, [sid], locator,
            "The public source establishes the work's substantive connection to the named practice or concept.", confidence=0.88,
        ))

    practice = [
        ("thrive_relational", "practice_doncaster_thrive", "practice_relational_public_services", "integrates", "conceptual", "integrates", ["src_don_corporate_plan_2026", "src_don_public_health_report", "src_doncaster_interview_2026"], "Corporate Plan 2026–27, Thrive section; interview transcript, 14:06", "Thrive makes relational practice part of its operating approach."),
        ("thrive_abcd", "practice_doncaster_thrive", "practice_asset_based_community_development", "integrates", "conceptual", "integrates", ["src_doncaster_interview_2026", "src_don_public_health_report"], "interview transcript, 14:06 and 43:21", "Damian describes ABCD as one of Thrive's practical strands."),
        ("thrive_hls", "practice_doncaster_thrive", "practice_human_learning_systems", "uses", "practice", "uses", ["src_doncaster_interview_2026", "src_don_public_health_report"], "interview transcript, 27:10; Public Health Annual Report, Thrive section", "HLS underpins the relational and adaptive learning approach in Damian's account."),
        ("thrive_place", "practice_doncaster_thrive", "practice_place_based", "operationalises", "practice", "puts into practical form", ["src_doncaster_interview_2026", "src_don_corporate_plan_2026"], "interview transcript, 14:06–17:29; Corporate Plan, integrated neighbourhood working section", "Locality structures give place-based practice an organizational form."),
        ("thrive_learning", "practice_doncaster_thrive", "practice_organizational_learning", "operationalises", "practice", "puts into practical form", ["src_doncaster_interview_2026", "src_doncaster_key_messages_2026"], "interview transcript, 27:10; key messages, learning section", "Learning and adaptation are part of the operating system, not an after-action add-on."),
        ("team_thrive", "practice_team_doncaster", "practice_doncaster_thrive", "applies", "practice", "applies", ["src_doncaster_interview_2026", "src_don_corporate_plan_2026"], "interview transcript, 14:06–17:29", "Damian locates Thrive within the Team Doncaster place partnership and locality structure."),
        ("thrive_authorizing", "practice_doncaster_thrive", "concept_authorizing_environment", "uses", "practice", "depends in practice on", ["src_doncaster_interview_2026", "src_doncaster_key_messages_2026"], "interview transcript, 40:51 and 46:05", "Damian treats a stable political and officer authorizing environment as a practical condition for durability."),
        ("thrive_bets", "practice_doncaster_thrive", "practice_small_bets", "uses", "practice", "uses", ["src_doncaster_interview_2026", "src_doncaster_key_messages_2026"], "interview transcript, 11:00", "Small bounded experiments allow learning without transplanting a total model."),
        ("thrive_horizons", "practice_doncaster_thrive", "method_three_horizons", "applies", "practice", "applies", interview, "interview transcript, 30:49 and 42:40–43:21", "Damian describes adapting Three Horizons in Edlington and clear-hold-build work."),
        ("thrive_regenerative", "practice_doncaster_thrive", "practice_regenerative_cultures", "uses", "practice", "draws practice from", interview + correspondence, "interview transcript, 43:58 onward; pre-interview statement, regenerative cultures paragraph", "Regenerative thinking is a named route into Doncaster's place practice."),
        ("thrive_social_innovation", "practice_doncaster_thrive", "practice_social_innovation", "operationalises", "practice", "puts collaborative change into practice", ["src_damian_lineage_diagram_2026", "src_doncaster_interview_2026"], "lineage diagram, slide 1, ‘Social Innovation’ box; interview transcript, 14:06–17:29", "Team Doncaster and locality partnerships provide one practical setting for the named social-innovation strand."),
        ("hls_relational", "practice_human_learning_systems", "practice_relational_public_services", "operationalises", "practice", "puts into practical form", ["src_don_hls_liberated", "src_doncaster_interview_2026"], "HLS and Liberated Method report, sections 1–3; interview transcript, 27:10", "HLS supplies an explicit practice route for relational work under complexity."),
        ("hls_learning", "practice_human_learning_systems", "practice_organizational_learning", "uses", "practice", "uses", ["src_don_hls_liberated", "src_doncaster_interview_2026"], "HLS and Liberated Method report, learning sections; interview transcript, 27:10", "Learning is an organizing principle of HLS and its use in Damian's account."),
        ("well_abcd", "practice_well_doncaster", "practice_asset_based_community_development", "applies", "practice", "applies", interview, "interview transcript, 43:58 onward", "Damian describes Well Doncaster as a community-health manifestation of ABCD and Well North."),
        ("suckling_well", "person_rupert_suckling", "practice_well_doncaster", "developed", "historical", "helped bring into practice", interview + ["src_don_rupert_suckling"], "interview transcript, 43:58 onward", "Damian credits Suckling with bringing Well North into the work that became Well Doncaster."),
        ("behr_remake", "person_gregg_behr", "practice_remake_learning", "founded", "human", "founded", ["src_don_gregg_behr"], "official profile, role section", "The official profile identifies Behr as Remake Learning's founder."),
        ("thrive_remake", "practice_doncaster_thrive", "practice_remake_learning", "adapts", "influence", "adapts", interview, "interview transcript, 36:24", "Damian describes a parallel Doncaster festival; institutional identity with the Pittsburgh network is not implied."),
        ("remake_ecosystem", "practice_remake_learning", "practice_learning_ecosystems", "operationalises", "practice", "puts into practical form", ["src_don_remake_playbook"], "playbook, network-building sections", "Remake Learning operationalises a place-based learning-ecosystem approach."),
        ("learning_innovation", "practice_learning_ecosystems", "practice_innovation_ecosystems", "complements", "conceptual", "complements", interview + diagram, "interview transcript, 36:24; lineage diagram, slide 1, social-innovation sequence", "Damian names both ecosystem routes; the edge records complementarity rather than equivalence."),
        ("bets_learning", "practice_small_bets", "practice_organizational_learning", "operationalises", "practice", "creates a bounded route for", interview + ["src_doncaster_key_messages_2026"], "interview transcript, 11:00", "Small bets create feedback for learning and adaptation."),
        ("design_bets", "practice_design_thinking", "practice_small_bets", "complements", "practice", "complements", diagram + interview, "lineage diagram, slide 1, ‘Design Thinking’ box; interview transcript, 11:00", "Prototyping and bounded experiments are compatible practice routes, without claiming identity."),
        ("kindness_contributory", "practice_choose_kindness", "concept_contributory_state", "operationalises", "practice", "puts one ethical aspect into practice", interview + ["src_doncaster_key_messages_2026", "src_don_corporate_plan_2024"], "interview transcript, 47:05; Corporate Plan 2024–25, Choose Kindness section", "Choose Kindness connects to reciprocity and contribution but is not the whole contributory-state proposition."),
        ("contributory_reciprocity", "concept_contributory_state", "law_or_principle_law_of_reciprocity_of_connections", "uses", "practice", "uses a reciprocity proposition", interview, "interview transcript, 47:05", "Damian foregrounds reciprocity and pay-it-forward relations; derivation from the Grammar law is not claimed."),
        ("situated_place", "concept_socially_situated_action", "practice_place_based", "explanatory_prerequisite", "conceptual", "helps explain", correspondence, "follow-up correspondence, socially situated action paragraph", "Damian argues that action is embedded in place and nested social context."),
        ("ecology_situated", "concept_ecological_systems_theory", "concept_socially_situated_action", "complements", "conceptual", "complements", correspondence + ["src_don_bronfenbrenner"], "follow-up correspondence, theoretical commitments paragraph", "Nested ecological levels offer one route for thinking about situated action; identity is not claimed."),
        ("regenerative_circular", "practice_regenerative_cultures", "practice_circular_economy", "complements", "conceptual", "complements", correspondence + ["src_don_regenerative_cultures"], "pre-interview statement, regenerative and circular economy list", "Damian holds both in one repertoire; the edge explicitly avoids treating them as synonyms."),
        ("regenerative_permaculture", "practice_regenerative_cultures", "practice_permaculture", "integrates", "conceptual", "integrates", diagram + ["src_don_regenerative_cultures"], "lineage diagram, slide 1, ‘Regenerative Cultures’ box", "Permaculture is named inside Damian's regenerative-cultures strand."),
        ("regenerative_place", "practice_regenerative_cultures", "practice_place_based", "uses", "practice", "uses sensitivity to place", ["src_don_regenerative_cultures", "src_don_place_regeneration"], "publisher contents, place and scale themes; 2025 report, capabilities sections", "Both public sources make place and scale material to regenerative practice."),
        ("andersson_place", "person_jenny_andersson", "practice_place_based", "specialises_in", "practice", "specialises in", ["src_don_jenny_andersson", "src_don_place_regeneration"], "official profile; report, capabilities sections", "Andersson's public work is organized around place-based regenerative practice."),
        ("ecology_population", "tradition_evolutionary_ecology", "concept_population_dynamics", "includes", "classification", "includes", diagram, "lineage diagram, slide 1, ‘Evolutionary Ecology’ box", "Population dynamics is explicitly included in Damian's evolutionary-ecology strand."),
        ("ecology_community", "tradition_evolutionary_ecology", "concept_community_ecology", "complements", "conceptual", "complements", diagram, "lineage diagram, slide 1, ecology and MSc Environment boxes", "The diagram places population/evolutionary ecology and community ecology in Damian's early sequence."),
        ("complexity_abm", "tradition_complexity_theory", "method_or_methodology_agent_based_modelling", "uses", "practice", "uses", diagram, "lineage diagram, slide 1, ‘Complexity Theory’ box", "Agent models are explicitly named inside the complexity-theory strand."),
        ("municipal_intelligence", "concept_municipal_brain", "concept_systems_intelligence", "uses", "practice", "uses", interview, "interview transcript, 43:58 onward", "The municipal-brain metaphor is a possible future use of distributed systems intelligence and augmented knowledge."),
    ]
    for slug, source, target, rel, family, phrase, sources, locator, notes in practice:
        output.append(edge(
            f"e_don_practice_{slug}", source, target, rel, family, phrase, sources, locator, notes,
            directed=rel != "complements", confidence=0.90,
            scope="Practice account or documented design; not by itself an independent outcome evaluation." if source == "practice_doncaster_thrive" else "",
        ))

    # Direct collaboration claims from Damian's interview/correspondence.
    collaborations = [
        ("lowe", "person_toby_lowe", "pre-interview statement, relational approaches paragraph"),
        ("smith", "person_mark_smith_hls", "pre-interview statement, relational approaches paragraph"),
        ("wahl", "person_daniel_christian_wahl", "pre-interview statement, regenerative cultures paragraph"),
        ("midgley", "person_gerald_midgley", "pre-interview statement, Nested Minimum Viable Systems sentence"),
        ("geyer", "person_robert_geyer", "follow-up correspondence, early-2000s complexity paragraph"),
    ]
    for slug, target, locator in collaborations:
        output.append(edge(
            f"e_don_collaboration_{slug}", "person_damian_allen", target,
            "collaborated_with", "human", "collaborated with", correspondence, locator,
            "Damian explicitly describes work with the named person; the edge does not generalize beyond that account.",
            directed=False, confidence=0.92,
        ))
    output.append(edge(
        "e_don_collaboration_bruce", "person_damian_allen", "person_bruce_edmonds",
        "collaborated_with", "human", "probably collaborated with", correspondence + ["src_don_bruce_edmonds"],
        "follow-up correspondence, early-2000s complexity paragraph; Centre for Policy Modelling paper, institutional context",
        "Damian wrote 'Bruce Edwards'; the collaborator identity is probable, not confirmed.", directed=False,
        status="provisional_identity_normalisation", mode="interpreted", confidence=0.68,
        inference="Institution, topic and aphorism match.",
    ))

    # Two attributed concepts remain visibly unverified.
    output.append(edge(
        "e_don_hodgson_three_horizons", "person_tony_hodgson", "method_three_horizons",
        "claimed_to_have_influenced", "influence", "is credited by Damian in the development lineage of",
        interview + correspondence, "interview transcript, 42:40–43:21",
        "Damian credits Hodgson alongside Sharpe. The public book record establishes Sharpe's authorship, not Hodgson's exact role.",
        status="provisional_self_reported_attribution", confidence=0.68,
        scope="Further primary history is required before promoting the historical claim.",
    ))
    output.append(edge(
        "e_don_midgley_nmvs", "person_gerald_midgley", "concept_nested_minimum_viable_systems",
        "claimed_to_have_influenced", "influence", "is credited by Damian in the development of",
        interview + correspondence, "pre-interview statement, Nested Minimum Viable Systems sentence",
        "Damian attributes the phrase and collaborative work to Midgley; no public title or stable definition was located.",
        status="provisional_self_reported_unverified", confidence=0.58,
        scope="Do not present as a published Midgley framework without a primary locator.",
    ))

    # UTSI is deliberately represented as an unpublished synthesis target, never an accepted field theory.
    utsi_inputs = [
        ("evolutionary", "tradition_evolutionary_ecology", "lineage diagram, slide 1, ‘Evolutionary Ecology’ box"),
        ("information", "concept_information_theory", "lineage diagram, slide 1, ‘Information Theory’ box"),
        ("learning", "tradition_learning_theory", "lineage diagram, slide 1, ‘Learning Theory’ box"),
        ("organization", "tradition_organizational_theory", "lineage diagram, slide 1, ‘Organizational Theory’ box"),
        ("soft_systems", "method_or_methodology_soft_systems_methodology_ssm", "lineage diagram, slide 1, ‘Systems Theory’ box"),
        ("complexity", "tradition_complexity_theory", "lineage diagram, slide 1, ‘Complexity Theory’ box"),
        ("system_dynamics", "method_or_methodology_system_dynamics", "lineage diagram, slide 1, ‘Systems Dynamics’ box"),
        ("cybernetics", "tradition_cybernetics", "lineage diagram, slide 1, ‘Cybernetics’ box"),
        ("design", "practice_design_thinking", "lineage diagram, slide 1, ‘Design Thinking’ box"),
        ("place", "practice_place_based", "lineage diagram, slide 1, ‘Place-Based Practice’ box"),
        ("social_innovation", "practice_social_innovation", "lineage diagram, slide 1, ‘Social Innovation’ box"),
        ("regenerative", "practice_regenerative_cultures", "lineage diagram, slide 1, ‘Regenerative Cultures’ box"),
        ("relational", "practice_relational_public_services", "lineage diagram, slide 1, ‘Relational Theory’ box"),
        ("ecological_systems", "concept_ecological_systems_theory", "follow-up correspondence, theoretical commitments and UTSI paragraphs"),
        ("capital", "concept_forms_of_capital", "follow-up correspondence, theoretical commitments and UTSI paragraphs"),
    ]
    for slug, target, locator in utsi_inputs:
        output.append(edge(
            f"e_don_utsi_{slug}", "theory_unified_systems_intelligence", target,
            "integrates", "conceptual", "proposes to integrate", diagram + correspondence, locator,
            "This records Damian's stated synthesis target, not a published, derived, tested or validated integration.",
            status="provisional_self_reported_unpublished", confidence=0.55,
            scope="Unpublished proto-theory. The diagram says 11 frameworks but visibly contains more than 11 labelled strands; the count ambiguity is unresolved.",
        ))
    output.extend([
        edge(
            "e_don_utsi_damian", "theory_unified_systems_intelligence", "person_damian_allen",
            "developed", "historical", "is being developed by", correspondence,
            "follow-up correspondence, UTSI paragraph", "Damian identifies UTSI as his own developing synthesis.",
            status="provisional_self_reported_unpublished", confidence=0.86,
            scope="Authorship of an unpublished proto-theory; no claim of scholarly validation or field acceptance.",
        ),
        edge(
            "e_don_utsi_systems_intelligence", "theory_unified_systems_intelligence", "concept_systems_intelligence",
            "formalises", "conceptual", "proposes to formalise", correspondence,
            "follow-up correspondence, UTSI paragraph", "Damian proposes a mathematical synthesis using coupled nonlinear differential equations, but no derivation or model artefact was supplied.",
            status="provisional_self_reported_unpublished", confidence=0.45,
            scope="Proposal only; not a verified mathematical formalisation.",
        ),
    ])

    # Approved adversarial cautions stop relational rhetoric becoming its own evidence.
    output.extend([
        edge(
            "e_don_caution_relational_power", "practice_relational_public_services", "concept_authorizing_environment",
            "constrains", "conceptual", "requires changes in", ["src_doncaster_key_messages_2026"],
            "approved draft posts, adversarial test paragraph",
            "Relational language can precede changes in power, money and measurement; the test is what authority and resources moved.",
            scope="Approved editorial caution, not an evaluation finding about achieved Doncaster outcomes.",
        ),
        edge(
            "e_don_caution_kindness_rights", "practice_choose_kindness", "concept_contributory_state",
            "constrains", "conceptual", "is bounded by accountability within", ["src_doncaster_key_messages_2026"],
            "approved draft posts, kindness caution paragraph",
            "Kindness must not become a substitute for rights, resources or accountability.",
            scope="Normative boundary, not empirical evidence of implementation success.",
        ),
        edge(
            "e_don_probable_complexity_book", "person_damian_allen", "publication_harnessing_complexity",
            "cites", "influence", "probably refers to", interview + ["src_don_harnessing_complexity"],
            "interview transcript, 42:40; university record, title and authors",
            "Title, date, topic and named co-authors make this the strongest candidate, but Mark Smith is not an author and Damian supplied no title.",
            status="provisional_probable_referent", mode="interpreted", confidence=0.66,
            scope="Do not convert into a certain citation without confirmation or a direct bibliographic locator.",
            inference="Matched date, topic and named HLS author cluster against the official university record.",
        ),
    ])

    return output


def profile(
    node_id: str, title: str, definition: str, summary: str, why: str,
    distinctions: list[str], lineage: list[str], practice: list[str],
    misreadings: list[str], checks: list[str], sources: list[str], status: str,
) -> dict[str, Any]:
    return {
        "node_id": node_id, "title": title, "profile_status": status,
        "canonical_definition": definition, "summary": summary, "why_it_matters": why,
        "key_distinctions": enc(distinctions), "historical_lineage": enc(lineage),
        "logical_antecedents": enc(lineage), "dependent_subsequents": enc(practice),
        "practice_connections": enc(practice), "espoused_lineages": enc(["Damian Allen interview, diagram and correspondence"]),
        "observed_clusters": enc(["Doncaster municipal practice", "place-based relational public services"]),
        "common_misreadings": enc(misreadings), "open_checks": enc(checks),
        "source_ids": enc(sources), "evidence_ids": "[]", "last_researched": GENERATED,
        "review_status": status, "reviewed_by": "Benjamin P Taylor", "reviewed_at": GENERATED,
        "editorial_note": "Private material is paraphrased and locator-limited. Inference, recollection, public corroboration and unpublished theory remain distinguishable.",
    }


PROFILES = [
    profile(
        "person_damian_allen", "Damian Allen",
        "Chief Executive of City of Doncaster Council and a systems practitioner whose stated lineage joins ecology, philosophy, learning, systems, complexity, cybernetics, design, place, regeneration and relational public services.",
        "Allen describes a practice-first lineage: theory disciplines action, but models must be adapted to place, authorizing conditions, relationships and learning. His account connects Thrive, HLS, ABCD, Three Horizons, regenerative cultures, Remake Learning and cybernetics.",
        "It is a rare first-person account of how multiple intellectual families are translated into municipal practice. Separating sources, claims and uncertainties keeps it useful without turning recollection into neutral history.",
        ["first-person lineage versus independently verified influence", "practice adaptation versus model transplantation", "relational vocabulary versus changed power and resources", "systems intelligence versus a validated formal theory"],
        ["evolutionary ecology", "philosophy", "information and learning theory", "systems and complexity", "cybernetics", "design and place", "regenerative and relational practice"],
        ["Doncaster Thrive", "Human Learning Systems", "ABCD", "Three Horizons", "Remake Learning", "Unified Theory of Systems Intelligence (unpublished)"],
        ["The diagram is not independent proof of every influence.", "The many strands are not one settled grand theory.", "Practice claims are not evidence of achieved outcomes without evaluation."],
        ["Confirm Bruce Edmonds normalization.", "Resolve the exact complexity-book citation.", "Clarify Tony Hodgson's historical role in Three Horizons.", "Locate a public primary record for Nested Minimum Viable Systems.", "Reconcile the visible strand count with the stated 11 frameworks."],
        ["src_don_council_leadership", "src_doncaster_interview_2026", "src_damian_lineage_diagram_2026", "src_damian_correspondence_2026", "src_doncaster_key_messages_2026"],
        "first_person_lineage_source_checked",
    ),
    profile(
        "practice_doncaster_thrive", "Doncaster Thrive",
        "A place-based way of working in Doncaster combining relational public services, community assets, wellbeing, locality structures and adaptive learning.",
        "The council describes Thrive as how it works, not a standalone programme. Damian connects it to HLS, ABCD, localities, organizational learning, Three Horizons, small bets and regenerative practice.",
        "It is a municipal case where conceptual lineages are translated into structures, roles and learning routines rather than collected as labels.",
        ["way of working versus programme", "with/by place versus for/to place", "adaptation versus transplantation", "learning system versus fixed delivery model"],
        ["relational public services", "Human Learning Systems", "ABCD", "place-based practice"],
        ["Team Doncaster", "Well Doncaster", "Three Horizons", "small bets", "organizational learning"],
        ["Relational language does not prove that power, money or measurement changed.", "Community assets do not remove the need to build capacity."],
        ["Add independent outcome evaluation.", "Track what authority and resources moved.", "Test durability through political and officer change."],
        ["src_don_corporate_plan_2026", "src_don_public_health_report", "src_doncaster_interview_2026", "src_doncaster_key_messages_2026"],
        "official_and_interview_sources_checked",
    ),
    profile(
        "practice_human_learning_systems", "Human Learning Systems",
        "A public-service approach organized around human relationships, learning and systems conditions in complex environments.",
        "HLS supplies one explicit route into Doncaster Thrive. Damian uses it to explain why adaptive learning and relationality must be designed into public-service work.",
        "It connects complexity arguments to practical public-service design while keeping relationships and learning central.",
        ["learning versus compliance", "system conditions versus isolated performance", "human relationships versus transaction"],
        ["public-service complexity", "relational practice", "Liberated Method"],
        ["Toby Lowe", "Mark Smith", "Hannah Hesselgreaves", "Doncaster Thrive"],
        ["HLS is not evidence that every relational intervention succeeds.", "Learning language does not remove accountability."],
        ["Add critical and evaluative literature beyond project self-description."],
        ["src_don_hls_story", "src_don_hls_liberated", "src_don_harnessing_complexity"],
        "official_practice_sources_checked",
    ),
    profile(
        "theory_unified_systems_intelligence", "Unified Theory of Systems Intelligence",
        "Damian Allen's unpublished proto-theory proposing a synthesis of systems and cognitive-science frameworks, with a possible coupled nonlinear differential-equation formulation.",
        "UTSI is maintained as an inspectable research lead, not an established theory. No public paper, derivation, parameterization, validation or critique was supplied.",
        "The idea exposes how Damian currently tries to connect his lineages. Its value here is the explicit synthesis claim and testable gaps, not premature authority.",
        ["proto-theory versus established theory", "named synthesis target versus demonstrated integration", "mathematical aspiration versus supplied model", "11-framework claim versus more than 11 visible strands"],
        ["Damian Allen lineage diagram", "systems intelligence", "systems and cognitive-science frameworks"],
        ["Doncaster Thrive", "place-based practice", "systems intelligence"],
        ["UTSI is not a recognized field theory.", "The graph does not validate a coupled-equation model.", "The diagram's frameworks are not necessarily commensurable."],
        ["Obtain a public working paper or model specification.", "Define variables and coupling assumptions.", "Reconcile framework count.", "Invite adversarial review from each source tradition."],
        ["src_damian_lineage_diagram_2026", "src_damian_correspondence_2026"],
        "provisional_self_reported_unpublished",
    ),
]


JOURNEY = {
    "id": "journey_doncaster_thrive_lineage",
    "title": "From midge swarms to municipal practice",
    "summary": "Follow Damian Allen's self-described lineage into Doncaster Thrive, then test where public sources, practice claims and unresolved theory diverge.",
    "audience": "Readers interested in place-based public-service systems practice and the provenance of Doncaster Thrive.",
    "duration_minutes": 18,
    "steps": [
        {"node_id": "person_damian_allen", "heading": "Begin with a first-person lineage", "narrative": "Damian's diagram joins ecology, philosophy, learning, systems, complexity, cybernetics, design, place and relational practice. These are his claims, not a neutral canon."},
        {"node_id": "practice_doncaster_thrive", "heading": "Translate lineage into a way of working", "narrative": "Thrive is presented as a municipal operating approach built around neighbourhoods, relationships, assets, wellbeing and learning—not a detachable programme."},
        {"node_id": "practice_human_learning_systems", "heading": "Make learning and relationship structural", "narrative": "HLS explains one route from complexity to public-service practice, while efficacy still requires independent evaluation."},
        {"node_id": "practice_asset_based_community_development", "heading": "Start with community assets—and uneven capacity", "narrative": "ABCD changes who is treated as knowledgeable and capable, while retaining the need for capacity, rights and resources."},
        {"node_id": "method_three_horizons", "heading": "Hold present, transition and future together", "narrative": "Damian describes adapting Three Horizons. Sharpe's book is public; Hodgson's exact historical role remains a first-person attribution."},
        {"node_id": "practice_remake_learning", "heading": "Use place networks and small bets", "narrative": "Remake Learning supplies a networked route. Doncaster's parallel festival is an adaptation, not an assertion of institutional identity."},
        {"node_id": "practice_regenerative_cultures", "heading": "Keep place, scale and regeneration in view", "narrative": "Wahl and Andersson connect regenerative design to place; circular economy remains a neighbour, not a synonym."},
        {"node_id": "tradition_cybernetics", "heading": "Return to feedback, variety and viable organization", "narrative": "Beer and Ashby are explicit in Damian's diagram, joining municipal practice to a deeper cybernetic route."},
        {"node_id": "theory_unified_systems_intelligence", "heading": "Stop at the evidence boundary", "narrative": "UTSI is an unpublished proto-theory. The synthesis, mathematics and framework count remain open to disproof."},
        {"node_id": "practice_choose_kindness", "heading": "End with an adversarial test", "narrative": "Relational and kindness language must be tested against power, decisions, money, rights, accountability, resident experience and durability."},
    ],
}


EXISTING_LINEAGE_IDS = [
    "person_fpcs_s_j_gould", "person_fpcs_w_weaver", "person_claude_e_shannon",
    "person_stafford_beer", "person_w_ross_ashby", "person_gerald_midgley",
    "concept_information_theory", "method_or_methodology_system_dynamics",
    "method_or_methodology_soft_systems_methodology_ssm", "tradition_cybernetics",
    "method_or_methodology_agent_based_modelling", "comparator_corpus_santa_fe_institute_complexity_explorer",
]


def add_source(item: dict[str, Any], source_id: str) -> None:
    ids = dec(item.get("source_ids"))
    if source_id not in ids:
        ids.append(source_id)
    item["source_ids"] = enc(ids)


def duplicate_triples(edges: list[dict[str, Any]]) -> list[tuple[str, str, str]]:
    counts = Counter((item.get("source"), item.get("relation_type"), item.get("target")) for item in edges)
    return [key for key, count in counts.items() if count > 1]


def refresh_counts(data: dict[str, Any]) -> None:
    sources = {item["id"]: item for item in data.get("sources", [])}
    for item in data.get("nodes", []):
        records = [sources[sid] for sid in dec(item.get("source_ids")) if sid in sources]
        item["public_source_count"] = sum(row.get("public_link_status") == "public_link" for row in records)
        item["no_public_link_count"] = sum(row.get("public_link_status") == "no_public_link" for row in records)


def main() -> None:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    measured_before = {
        "nodes": len(data.get("nodes", [])), "edges": len(data.get("edges", [])),
        "sources": len(data.get("sources", [])), "profiles": len(data.get("profiles", [])),
        "journeys": len(data.get("journeys", [])),
        "exact_duplicate_triples": len(duplicate_triples(data.get("edges", []))),
        "explicit_doncaster_lineage_entries": sum("doncaster_lineage" in dec(item.get("set_tags")) for item in data.get("nodes", [])),
    }
    before = data.get("doncaster_lineage_review", {}).get("before") or measured_before

    upsert(data["sources"], source_records(), "id")
    upsert(data["nodes"], node_records(), "id")
    by_node = {item["id"]: item for item in data["nodes"]}
    missing_existing = sorted(set(EXISTING_LINEAGE_IDS) - set(by_node))
    if missing_existing:
        raise RuntimeError(f"Expected existing lineage endpoint(s) missing: {missing_existing}")

    # Deepen existing thin entries instead of duplicating them.
    by_node["person_fpcs_s_j_gould"].update({
        "label": "Stephen Jay Gould", "aliases": enc(["S. J. Gould"]),
        "description": "Evolutionary biologist and historian of science who appears in Damian Allen's self-authored philosophy lineage strand.",
        "canonical_definition": "Evolutionary biologist and historian of science who appears in Damian Allen's self-authored philosophy lineage strand.",
    })
    by_node["person_fpcs_w_weaver"].update({
        "label": "Warren Weaver", "aliases": enc(["W. Weaver"]),
        "description": "Mathematician and science administrator associated with communication theory and named in Damian Allen's information-theory strand.",
        "canonical_definition": "Mathematician and science administrator associated with communication theory and named in Damian Allen's information-theory strand.",
    })
    for nid in EXISTING_LINEAGE_IDS:
        add_source(by_node[nid], "src_damian_lineage_diagram_2026")
    add_source(by_node["person_gerald_midgley"], "src_damian_correspondence_2026")
    add_source(by_node["person_gerald_midgley"], "src_don_midgley_profile")

    data["edges"] = [item for item in data.get("edges", []) if not str(item.get("id", "")).startswith("e_don_")]
    incoming = build_edges()
    known = set(by_node)
    missing = sorted({endpoint for item in incoming for endpoint in (item["source"], item["target"]) if endpoint not in known})
    if missing:
        raise RuntimeError(f"Doncaster relationship endpoint(s) missing: {missing}")
    data["edges"].extend(incoming)
    duplicates = duplicate_triples(data["edges"])
    if duplicates:
        raise RuntimeError(f"Doncaster extension created duplicate triples: {duplicates[:12]}")

    upsert(data["profiles"], PROFILES, "node_id")
    upsert(data["journeys"], [JOURNEY], "id")
    refresh_counts(data)
    data["relational_depth"] = calculate_relational_depth(data)
    data["graph_snapshot"] = calculate_graph_snapshot(data)
    aggregate = data["relational_depth"]["aggregate"]
    data["meta"].update({
        "release": BASE_RELEASE, "generated": "2026-08-14",
        "doncaster_lineage_extension": EXTENSION_VERSION,
        "doncaster_lineage_generated": GENERATED,
        "iteration_focus": "Damian Allen and Doncaster practice lineage: first-person provenance, works, concepts, applications and explicit uncertainty",
        "node_count": len(data["nodes"]), "edge_count": len(data["edges"]),
        "source_count": len(data["sources"]), "profile_count": len(data["profiles"]),
        "journey_count": len(data["journeys"]), "public_entry_count": aggregate["public_entries"],
        "described_entry_count": aggregate["public_entries"],
        "public_link_source_count": sum(item.get("public_link_status") == "public_link" for item in data["sources"]),
        "no_public_link_source_count": sum(item.get("public_link_status") == "no_public_link" for item in data["sources"]),
        "reader_connected_entry_count": aggregate["reader_connected_entries"],
        "semantic_connected_entry_count": aggregate["semantic_connected_entries"],
        "rich_entry_count": aggregate["connection_bands"].get("rich", 0),
        "developing_entry_count": aggregate["connection_bands"].get("developing", 0),
        "thin_entry_count": aggregate["connection_bands"].get("thin", 0),
        "unconnected_entry_count": aggregate["connection_bands"].get("unconnected", 0),
        "doncaster_lineage_audit_url": "https://github.com/antlerboy/the-necessary-tangle/blob/main/documentation/doncaster-lineage-audit.md",
    })
    if data.get("ai_observations"):
        data["ai_observations"]["metrics"] = graph_metrics(data)

    coverage = [
        {"label": label, "node_id": nid, "kind": kind, "coverage": "added"}
        for nid, label, kind, *_rest in NODE_ROWS
    ] + [
        {"label": by_node[nid]["label"], "node_id": nid, "kind": by_node[nid]["entity_type"], "coverage": "existing entry connected or deepened"}
        for nid in EXISTING_LINEAGE_IDS
    ]
    review = {
        "date": GENERATED,
        "scope": "Damian Allen interview, lineage diagram, approved key messages, correspondence, connected-corpus discovery check and claim-specific public corroboration.",
        "privacy_rule": "Private records are represented by authorized paraphrase and source locators; message identifiers, addresses, private URLs and unnecessary extracts are excluded.",
        "before": before,
        "after": {
            "nodes": len(data["nodes"]), "edges": len(data["edges"]), "sources": len(data["sources"]),
            "profiles": len(data["profiles"]), "journeys": len(data["journeys"]),
            "exact_duplicate_triples": len(duplicate_triples(data["edges"])),
            "named_lineage_items_explicit": len(coverage), "new_typed_relationships": len(incoming),
            "private_source_records": sum(item[7] == "private" for item in SOURCE_ROWS),
        },
        "coverage": coverage,
        "source_inventory": [
            {"source_id": row[0], "title": row[1], "access": row[7], "public_link_status": "public_link" if row[3] else "no_public_link"}
            for row in SOURCE_ROWS
        ],
        "connected_corpus_check": {
            "mail": "interview transcript, lineage diagram, approved copy and follow-up correspondence located and reviewed",
            "document_storage": "targeted title and Doncaster searches found no additional authoritative lineage artefact beyond the supplied attachments",
        },
        "epistemic_boundaries": [
            {"topic": "Bruce Edmonds", "status": "provisional identity normalization", "reason": "Damian wrote Bruce Edwards; MMU context and the published aphorism point strongly to Edmonds."},
            {"topic": "Complexity book", "status": "probable referent", "reason": "Harnessing Complexity matches the date, topic and most named authors, but no title was supplied and Mark Smith is not an author."},
            {"topic": "Tony Hodgson and Three Horizons", "status": "self-reported attribution", "reason": "Damian credits Hodgson; the public book page establishes Bill Sharpe's authorship, not Hodgson's exact role."},
            {"topic": "Nested Minimum Viable Systems", "status": "self-reported; no public corroboration located", "reason": "Damian attributes collaborative work to Gerald Midgley; no stable publication or definition was found."},
            {"topic": "Unified Theory of Systems Intelligence", "status": "unpublished proto-theory", "reason": "No public paper, formal derivation, parameters, validation or independent critique was supplied."},
            {"topic": "UTSI framework count", "status": "unresolved internal ambiguity", "reason": "The diagram says 11 frameworks but visibly contains more than 11 labelled strands."},
            {"topic": "Thrive outcomes", "status": "practice intent and practitioner account, not independent evaluation", "reason": "Official and interview sources establish design and rationale; outcome verification remains separate."},
        ],
        "adversarial_tests": [
            "Relational vocabulary must be tested against changed power, money, measurement and resident experience.",
            "Kindness must not substitute for rights, resources or accountability.",
            "Community assets do not remove uneven capacity or the need to invest in it.",
            "Named intellectual adjacency does not establish equivalence, historical dependence or validated synthesis.",
        ],
    }
    data["doncaster_lineage_review"] = review
    write_relational_document(data)
    write_data(data)

    quality = quality_result(data)
    quality["adversarial_review"] = data.get("adversarial_review", {})
    quality["doncaster_lineage_review"] = review
    rendered = json.dumps(quality, ensure_ascii=False, indent=2) + "\n"
    QUALITY_PATH.write_text(rendered, encoding="utf-8")
    QUALITY_PUBLIC_PATH.write_text(rendered, encoding="utf-8")
    print(json.dumps({"before": before, "after": review["after"]}, indent=2))


if __name__ == "__main__":
    main()
