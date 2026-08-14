#!/usr/bin/env python3
"""Apply the bounded evidence-led overnight review after the 0.16 generator.

The upstream release scripts intentionally rebuild the public graph from maintained
source files. This final, idempotent overlay records reviewed edge replacements and
recalculates every structural quality measure so clean builds and the live site agree.
"""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

from apply_relational_depth_16 import calculate_relational_depth, write_data
from apply_iteration_09 import graph_metrics
from refresh_graph_snapshot import calculate as calculate_graph_snapshot

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "public-data.json"
QUALITY_PATH = ROOT / "data" / "relationship-quality.json"
QUALITY_PUBLIC_PATH = ROOT / "docs" / "assets" / "relationship-quality.json"
RELATIONAL_DOC = ROOT / "documentation" / "relational-depth.md"

SOURCE_RECORDS: list[dict[str, Any]] = json.loads(r'''[
  {
    "id": "src_stacey_emergence_knowledge_2000",
    "title": "The emergence of knowledge in organisations",
    "source_type": "institutional_research_record",
    "quality_tier": "A",
    "access": "public",
    "url": "https://researchprofiles.herts.ac.uk/en/publications/the-emergence-of-knowledge-in-organisations/",
    "date": "2000",
    "notes": "University of Hertfordshire research record and abstract for Stacey's peer-reviewed article. The abstract presents complex responsive processes as an account of knowledge continuously reproduced and potentially transformed in interaction.",
    "creators": "[\"Ralph D. Stacey\"]",
    "doi": "10.1207/S15327000EM0204_05",
    "isbn": "",
    "publisher": "University of Hertfordshire / Emergence",
    "licence": "source_terms",
    "archived_url": "",
    "content_hash": "",
    "review_status": "checked_primary_institutional_record",
    "last_checked": "2026-08-14",
    "public_link_status": "public_link"
  },
  {
    "id": "src_mowles_design_complex_organisations_2016",
    "title": "What does it mean to ‘design’ complex organizations?",
    "source_type": "author_explanatory_article",
    "quality_tier": "B",
    "access": "public",
    "url": "https://complexityandmanagement.com/2016/11/03/what-does-it-mean-to-design-complex-organizations/",
    "date": "2016-11-03",
    "notes": "Chris Mowles's public explanation distinguishes self-organisation in complex responsive processes from self-management and defines it as local interaction among agents. Used for that stated distinction, not as field-wide consensus.",
    "creators": "[\"Chris Mowles\"]",
    "doi": "",
    "isbn": "",
    "publisher": "Complexity & Management Centre",
    "licence": "source_terms",
    "archived_url": "",
    "content_hash": "",
    "review_status": "checked_author_source",
    "last_checked": "2026-08-14",
    "public_link_status": "public_link"
  },
  {
    "id": "src_principia_self_organisation_guide",
    "title": "Self-Organization: The Emerging Science of Spontaneous Order",
    "source_type": "primary_project_theory_page",
    "quality_tier": "B",
    "access": "public",
    "url": "https://pespmc1.vub.ac.be/SELFORG.html",
    "date": "",
    "notes": "Project-authored guide to self-organisation. Used for its explicit account of variation amplified by positive feedback and stabilised by negative feedback, not as a field-wide consensus definition.",
    "creators": "[\"Principia Cybernetica Project editors\"]",
    "doi": "",
    "isbn": "",
    "publisher": "Principia Cybernetica Project",
    "licence": "source_terms",
    "archived_url": "",
    "content_hash": "",
    "review_status": "checked_internal_page",
    "last_checked": "2026-08-14",
    "public_link_status": "public_link"
  },
  {
    "id": "src_principia_project_history",
    "title": "History of the Principia Cybernetica Project",
    "source_type": "primary_project_history",
    "quality_tier": "B",
    "access": "public",
    "url": "https://pespmc1.vub.ac.be/HISTORY.html",
    "date": "",
    "notes": "Project-authored chronology covering the Turchin, Joslyn and Heylighen collaboration, CYBSYS-L discussions, conferences, semantic-network experiments and spin-offs. It is first-party institutional memory, not independent intellectual history.",
    "creators": "[\"Principia Cybernetica Project editors\"]",
    "doi": "",
    "isbn": "",
    "publisher": "Principia Cybernetica Project",
    "licence": "source_terms",
    "archived_url": "",
    "content_hash": "",
    "review_status": "checked_internal_page",
    "last_checked": "2026-08-14",
    "public_link_status": "public_link"
  },
  {
    "id": "src_principia_nutshell",
    "title": "Principia Cybernetica in a Nutshell",
    "source_type": "primary_project_overview",
    "quality_tier": "B",
    "access": "public",
    "url": "https://pespmc1.vub.ac.be/NUTSHELL.html",
    "date": "",
    "notes": "Project overview covering typed nodes and links, constructivist epistemology, metasystem transitions and the intended semantic-network architecture.",
    "creators": "[\"Principia Cybernetica Project editors\"]",
    "doi": "",
    "isbn": "",
    "publisher": "Principia Cybernetica Project",
    "licence": "source_terms",
    "archived_url": "",
    "content_hash": "",
    "review_status": "checked_internal_page",
    "last_checked": "2026-08-14",
    "public_link_status": "public_link"
  },
  {
    "id": "src_ing_ackoff_influence_1999",
    "title": "Studying the Sense & Respond Model and the Influence of Russell Ackoff's System of Thinking",
    "source_type": "primary_author_publication_record",
    "quality_tier": "A",
    "access": "public",
    "url": "https://coevolving.com/commons/1999_villanova_ackoff_80th_ing_sense_respond_influence",
    "date": "1999-05-05",
    "notes": "Author record, abstract and full paper locator. It explicitly describes which Ackoff works shaped Ing's appreciation of enterprise design; recorded as a traversal result because the current graph has no Ackoff entity to connect without expanding scope.",
    "creators": "[\"David Ing\"]",
    "doi": "",
    "isbn": "",
    "publisher": "Coevolving Innovations",
    "licence": "CC BY-NC-SA 4.0",
    "archived_url": "",
    "content_hash": "",
    "review_status": "checked_primary_author_record",
    "last_checked": "2026-08-14",
    "public_link_status": "public_link"
  },
  {
    "id": "src_ing_systems_changes_learning_2023",
    "title": "Systems Changes Learning: Recasting and reifying rhythmic shifts",
    "source_type": "primary_author_publication_record",
    "quality_tier": "A",
    "access": "public",
    "url": "https://coevolving.com/commons/2023-02-recasting-and-reifying-rhythmic-shifts",
    "date": "2023-02-28",
    "notes": "Author record, abstract and published article for contextural action learning, rhythmic shifts and the doing-thinking-making triad.",
    "creators": "[\"David Ing\"]",
    "doi": "10.54808/JSCI.20.07.11",
    "isbn": "",
    "publisher": "Journal of Systemics, Cybernetics and Informatics / Coevolving Innovations",
    "licence": "CC BY-NC-SA 4.0",
    "archived_url": "",
    "content_hash": "",
    "review_status": "checked_primary_author_record",
    "last_checked": "2026-08-14",
    "public_link_status": "public_link"
  },
  {
    "id": "src_ashby_digital_journal",
    "title": "Journal of W. Ross Ashby",
    "source_type": "primary_digital_archive",
    "quality_tier": "A",
    "access": "public",
    "url": "https://ashby.info/journal/index.html",
    "date": "1928-1972",
    "notes": "Digitised primary archive of 7,189 journal pages in 25 volumes, with 1,600 index cards, timeline, keyword index, references and more than 2,300 summaries. Archive structure was traversed; no new theory edge was inferred from index co-occurrence.",
    "creators": "[\"W. Ross Ashby\", \"Jill Ashby\"]",
    "doi": "",
    "isbn": "",
    "publisher": "W. Ross Ashby Digital Archive / British Library holdings",
    "licence": "archive_terms",
    "archived_url": "",
    "content_hash": "",
    "review_status": "checked_archive_structure",
    "last_checked": "2026-08-14",
    "public_link_status": "public_link"
  },
  {
    "id": "src_asc_cybernetics_history",
    "title": "Foundations: A Brief History of Cybernetics",
    "source_type": "professional_society_history",
    "quality_tier": "B",
    "access": "public",
    "url": "https://asc-cybernetics.org/foundations/history.htm",
    "date": "",
    "notes": "ASC institutional history with explicit caveats about multiple, contested histories. Used to locate feedback and circularity within a historical account, not to settle priority or a neutral canon.",
    "creators": "[\"American Society for Cybernetics\"]",
    "doi": "",
    "isbn": "",
    "publisher": "American Society for Cybernetics",
    "licence": "source_terms",
    "archived_url": "",
    "content_hash": "",
    "review_status": "checked_internal_history",
    "last_checked": "2026-08-14",
    "public_link_status": "public_link"
  },
  {
    "id": "src_isss_meeting_history",
    "title": "ISSS Meeting History",
    "source_type": "professional_society_history",
    "quality_tier": "B",
    "access": "public",
    "url": "https://www.isss.org/meeting-history/",
    "date": "1954-present",
    "notes": "Institutional chronology of formation, name changes and annual meetings. Useful for documented organisational history; it does not by itself establish conceptual influence among participants.",
    "creators": "[\"International Society for the Systems Sciences\"]",
    "doi": "",
    "isbn": "",
    "publisher": "International Society for the Systems Sciences",
    "licence": "source_terms",
    "archived_url": "",
    "content_hash": "",
    "review_status": "checked_internal_history",
    "last_checked": "2026-08-14",
    "public_link_status": "public_link"
  },
  {
    "id": "src_ifsr_conversations_legacy",
    "title": "IFSR Conversations Legacy",
    "source_type": "federation_programme_archive",
    "quality_tier": "B",
    "access": "public",
    "url": "https://ifsr.org/systems-research/ifsr-conversations-legacy/",
    "date": "",
    "notes": "Official programme history describing small, non-hierarchical, cross-tradition dialogues as second-order reflective practice. Used for programme design, not as evidence that every conversation achieved integration or consensus.",
    "creators": "[\"International Federation for Systems Research\"]",
    "doi": "",
    "isbn": "",
    "publisher": "International Federation for Systems Research",
    "licence": "source_terms",
    "archived_url": "",
    "content_hash": "",
    "review_status": "checked_programme_history",
    "last_checked": "2026-08-14",
    "public_link_status": "public_link"
  },
  {
    "id": "src_system_dynamics_society_definition",
    "title": "Study of System Dynamics",
    "source_type": "professional_society_method_guide",
    "quality_tier": "B",
    "access": "public",
    "url": "https://systemdynamics.org/what-is-system-dynamics-old/",
    "date": "",
    "notes": "Society guide defining models through stocks, flows and endogenous causal feedback structure, with a literature trail to Richardson, Sterman and group model building. Used for method structure, not proof of efficacy.",
    "creators": "[\"System Dynamics Society\"]",
    "doi": "",
    "isbn": "",
    "publisher": "System Dynamics Society",
    "licence": "source_terms",
    "archived_url": "",
    "content_hash": "",
    "review_status": "checked_method_guide",
    "last_checked": "2026-08-14",
    "public_link_status": "public_link"
  },
  {
    "id": "src_sfi_complexity_about",
    "title": "What is Complex Systems Science?",
    "source_type": "research_institute_self_description",
    "quality_tier": "B",
    "access": "public",
    "url": "https://www.santafe.edu/about",
    "date": "",
    "notes": "SFI institutional account of interacting and adapting agents, evolutionary processes and emergent macro behaviour across domains. Canonical for SFI's scope, not the whole field's consensus.",
    "creators": "[\"Santa Fe Institute\"]",
    "doi": "",
    "isbn": "",
    "publisher": "Santa Fe Institute",
    "licence": "source_terms",
    "archived_url": "",
    "content_hash": "",
    "review_status": "checked_institutional_scope",
    "last_checked": "2026-08-14",
    "public_link_status": "public_link"
  }
]''')
EDGE_PATCHES: dict[str, dict[str, Any]] = json.loads(r'''{
  "e_07_principia_05": {
    "relation_type": "operationalises",
    "relation_family": "practice",
    "directed": "true",
    "confidence": "0.9",
    "source_ids": "[\"src_principia_intro\"]",
    "source_locator": "Introduction to Principia Cybernetica, paragraphs beginning “Using computer technology…” and “Readers can navigate…” (INTRO.html)",
    "scope_conditions": "The project authors describe this semantic-network implementation as an application of their self-organisation theory; this does not establish that every semantic network self-organises.",
    "inference_method": "close reading of the project-authored introduction",
    "notes": "The project says its linked semantic network and adaptive algorithms support collaborative variation and selection, applying its theory to the practical development of the philosophical system.",
    "plain_phrase": "puts into practical form the project's account of",
    "public_review_label": "source-established project claim"
  },
  "e_09_complex_responsive_emergence": {
    "relation_type": "explains",
    "directed": "true",
    "confidence": "0.83",
    "claim_status": "provisional",
    "source_ids": "[\"src_stacey_emergence_knowledge_2000\",\"src_stacey_complex_responsive_processes_2001\"]",
    "source_locator": "University of Hertfordshire record, abstract; Emergence 2(4), pp. 23–39",
    "scope_conditions": "This is an account of emergent organisational knowledge through interaction, not a general theory of every form of emergence.",
    "assertion_mode": "interpreted",
    "inference_method": "close reading of the institutional abstract and bibliographic comparison with the book",
    "notes": "Stacey's abstract describes knowledge as continuously reproduced and potentially transformed in interaction; the edge interprets that as a specific organisational account of emergence.",
    "plain_phrase": "explains the emergence of organisational knowledge through",
    "public_review_label": "interpreted from author abstract"
  },
  "e_09_complex_responsive_self_organisation": {
    "relation_type": "specialises",
    "directed": "true",
    "confidence": "0.9",
    "source_ids": "[\"src_mowles_design_complex_organisations_2016\"]",
    "source_locator": "Section “A critique from an alternative understanding of the complexity sciences”, paragraph beginning “In all three cases…”",
    "scope_conditions": "The source explicitly narrows self-organisation in social life to local interaction and rejects equating it with self-management.",
    "inference_method": "close reading of the author explanation",
    "notes": "Mowles states that, in this complex-responsive-process account, self-organisation means local interaction among agents and implies no necessary rejection of hierarchy, management or leadership.",
    "plain_phrase": "gives a social-process account of",
    "public_review_label": "source-established author distinction"
  },
  "e_09_murmurations_complex_responsive": {
    "target": "practice_systems_practice",
    "relation_type": "presents",
    "relation_family": "documentary",
    "directed": "true",
    "confidence": "0.97",
    "source_ids": "[\"src_murmurations_about\"]",
    "source_locator": "About the Journal, paragraphs 22–36, especially the scope and reflexive-inquiry statements",
    "scope_conditions": "The official scope establishes a venue for systemic practitioners and practice-based reflexive inquiry; it does not establish adherence to complex responsive processes.",
    "inference_method": "close reading of the official journal scope",
    "notes": "The journal describes itself as a venue for relationally attuned systemic practitioners and asks contributors to speak from within as well as about practice.",
    "plain_phrase": "publishes reflexive inquiry from within",
    "public_review_label": "source-established journal scope"
  },
  "e_12_explicit_semantic_network": {
    "relation_type": "formalises",
    "directed": "true",
    "confidence": "0.94",
    "source_locator": "Nodica README, opening paragraphs and “Configuration” → “Settings” and “Labels”",
    "scope_conditions": "The claim concerns Nodica's RDF configuration and labelled predicates, not every semantic network.",
    "inference_method": "repository documentation inspection",
    "notes": "Nodica says graph appearance and behaviour are expressed in RDF; its configuration vocabulary and predicate labels make node, edge and display semantics explicit.",
    "plain_phrase": "formalises the node, edge and display vocabulary of",
    "public_review_label": "source-established software semantics"
  },
  "e_12_natural_drift_viability": {
    "target": "tradition_evolutionary_cybernetics",
    "relation_type": "challenges",
    "relation_family": "contestation",
    "directed": "true",
    "confidence": "0.91",
    "claim_status": "accepted",
    "source_ids": "[\"src_maturana_mpodozis_natural_drift_2000\",\"src_principia_intro\"]",
    "source_locator": "Maturana & Mpodozis abstract, paragraphs 35–36; Principia introduction, paragraphs 4–5",
    "scope_conditions": "Natural drift challenges natural selection as the generative mechanism of evolutionary history. This comparison does not imply that it rejects every claim in evolutionary cybernetics.",
    "assertion_mode": "interpreted",
    "inference_method": "direct comparison of two explicit mechanism claims",
    "notes": "Principia describes evolution as self-organisation based on variation and natural selection; Maturana and Mpodozis argue that natural selection is a consequence of natural drift rather than the mechanism generating evolutionary history.",
    "plain_phrase": "challenges the selection mechanism assumed by",
    "public_review_label": "interpreted tension between primary claims"
  },
  "e_12_req_ineff_viability": {
    "relation_type": "constrains",
    "directed": "true",
    "confidence": "0.94",
    "source_locator": "Resource description, paragraphs beginning “Driven by market forces…” and “Both organisms and the social systems…”",
    "scope_conditions": "This records Velitchkov's proposal that excess variety may be required for long-run viability; it is not presented as a generally established theorem.",
    "inference_method": "close reading of the official talk description",
    "notes": "The SCiO description says removing all apparent inefficiency can undermine survival and that excess variety is needed for requisite variety and long-run viability.",
    "plain_phrase": "states an excess-variety condition on",
    "public_review_label": "source-established practitioner proposal"
  },
  "e_14_bounded_boundary": {
    "source": "concept_boundary",
    "target": "concept_bounded_applicability",
    "relation_type": "definitional_prerequisite",
    "confidence": "0.96",
    "source_locator": "Cynefin wiki, opening definition (paragraphs 6–10) and “How it Works” (paragraphs 49–52)",
    "scope_conditions": "The source's bounded-applicability claim concerns the validity of approaches within contexts; it does not make every boundary equally useful or legitimate.",
    "inference_method": "close reading of the first-party framework definition",
    "notes": "The maintained Cynefin account defines bounded applicability through the boundaries within which context-specific approaches are valid.",
    "plain_phrase": "is a definitional prerequisite for",
    "public_review_label": "source-established framework definition"
  },
  "e_08_fpcs_coauthor_006_02": {
    "source_locator": "Official table of contents, Volume 1 entry “Behavior, Purpose, and Teleology”",
    "notes": "The two people are listed as co-authors of “Behavior, Purpose, and Teleology”; this assertion is work-specific."
  },
  "e_08_fpcs_coauthor_008_01": {
    "source_locator": "Official table of contents, Volume 1 entry “The Role of Models in Science”",
    "notes": "The two people are listed as co-authors of “The Role of Models in Science”; this assertion is work-specific."
  }
}''')


EDGE_PATCHES.update(json.loads(r'''{
  "e_07_principia_01": {
    "relation_type": "specialises",
    "relation_family": "conceptual",
    "directed": "true",
    "confidence": "0.92",
    "source_ids": "[\"src_principia_mstt\",\"src_principia_nutshell\"]",
    "source_locator": "Metasystem Transition Theory, opening definition and examples; Principia in a Nutshell, Metasystem Transition Theory section",
    "scope_conditions": "The project describes a metasystem transition as the emergence of a higher level of control. This is Principia's technical specialisation of emergence, not a synonym for every emergent phenomenon.",
    "inference_method": "close reading of two project-authored internal theory pages",
    "notes": "A metasystem transition is presented as the formation of a higher-level system that controls lower-level systems; the edge now states that specific cross-scale claim.",
    "plain_phrase": "specialises emergence as a new higher level of control within",
    "public_review_label": "source-established project definition"
  },
  "e_0274": {
    "relation_type": "definitional_prerequisite",
    "relation_family": "conceptual",
    "directed": "true",
    "dependency_kind": "definitional",
    "confidence": "0.94",
    "claim_status": "accepted",
    "source_ids": "[\"src_system_dynamics_society_definition\"]",
    "source_locator": "Study of System Dynamics, opening method description and paragraph beginning 'The model is usually a computer simulation model'",
    "scope_conditions": "Feedback is a defining structural commitment of system dynamics models, alongside stocks and flows; this does not imply that feedback alone constitutes system dynamics.",
    "assertion_mode": "asserted",
    "inference_method": "close reading of the professional society method guide",
    "notes": "The Society describes system dynamics models through accumulations, flows and the endogenous causal feedback structure determining those flows.",
    "plain_phrase": "is a definitional prerequisite for",
    "public_review_label": "source-established method structure"
  },
  "e_0342": {
    "confidence": "0.88",
    "claim_status": "provisional",
    "source_ids": "[\"src_wiener_cybernetics_1948\",\"src_asc_cybernetics_history\"]",
    "source_locator": "ASC Foundations history, sections 'Circularity' and 'Feedback'; Wiener 1948 MIT Press description (exact primary chapter still pending)",
    "scope_conditions": "ASC's institutional history treats feedback and circularity as focal to cybernetics, while also warning that cybernetics has multiple contested histories. The primary Wiener locator remains incomplete.",
    "inference_method": "comparison of professional-society history with the maintained publisher record",
    "notes": "The additional history supports feedback's focal place while preserving the existing provisional status and the unresolved primary-page locator.",
    "plain_phrase": "is focal to the circular account of",
    "public_review_label": "provisional historical synthesis"
  },
  "e15_pattern_manual_develops_service_systems": {
    "confidence": "0.97",
    "source_ids": "[\"src_ing_pattern_manual_2016\"]",
    "source_locator": "Pattern Manual paper, pp. 12-14, comparison of Alexandrian form with voices on issues, affording values and spatio-temporal frames",
    "scope_conditions": "The paper advances a proposal for discussion and explicitly frames it as an adaptation and extension, not a settled standard.",
    "inference_method": "close reading of the author paper and publication record",
    "notes": "The proposed format changes the unit of a pattern from context-problem-solution to voices/issues, affording values and spatio-temporal frames for service systems.",
    "plain_phrase": "develops a pattern form for",
    "public_review_label": "source-established author proposal"
  },
  "e15_ing_develops_service_systems": {
    "confidence": "0.97",
    "source_ids": "[\"src_ing_pattern_manual_2016\",\"src_ing_coevolving_publications_2026\"]",
    "source_locator": "Coevolving Publications index, Service Systems section; Pattern Manual paper, title, abstract and pp. 12-14",
    "scope_conditions": "Authorship and development are established from Ing's own publication record; this does not establish sole authorship of the wider field.",
    "inference_method": "author-index chronology and work-level verification",
    "notes": "The index documents a sustained sequence of service-systems-thinking work and the paper states the specific pattern-language development.",
    "plain_phrase": "develops a documented strand of",
    "public_review_label": "source-established authorship and development"
  },
  "e15_ing_develops_systems_changes": {
    "confidence": "0.97",
    "source_ids": "[\"src_ing_systems_changes_learning_2022\",\"src_ing_systems_changes_learning_2023\"]",
    "source_locator": "2023 author record, abstract and citation; published article pp. 11-73; 2022 Systems Changes presentation",
    "scope_conditions": "These first-party records establish Ing's authorship and formulation, not independent validation of the approach.",
    "inference_method": "author-index chronology and published-work verification",
    "notes": "The 2023 record locates the contextural-action-learning, rhythmic-shifts and doing-thinking-making formulation in a published article.",
    "plain_phrase": "develops and publishes",
    "public_review_label": "source-established authorship and development"
  }
}'''))

NEW_EDGES: list[dict[str, Any]] = json.loads(r'''[
  {
    "id": "e_overnight_principia_positive_feedback_self_org",
    "source": "concept_positive_feedback",
    "target": "concept_self_organisation",
    "relation_type": "explains",
    "relation_family": "causal_mechanism",
    "directed": "true",
    "dependency_kind": "mechanism",
    "confidence": "0.9",
    "claim_status": "accepted",
    "source_ids": "[\"src_principia_self_organisation_guide\"]",
    "evidence_ids": "[]",
    "source_locator": "Self-Organization guide, section 'The basic mechanism of self-organization', paragraphs on positive and negative feedback",
    "valid_from": "",
    "valid_to": "",
    "scope_conditions": "This is the feedback mechanism in Principia's project-authored account; it is not asserted as the only mechanism in every theory of self-organisation.",
    "assertion_mode": "asserted",
    "inference_method": "close reading of the internal theory page",
    "claim_id": "",
    "reviewed_by": "Benjamin P Taylor",
    "reviewed_at": "2026-08-14",
    "notes": "The guide says positive feedback amplifies deviations and supports the growth of new configurations before negative feedback stabilises them.",
    "plain_phrase": "amplifies variation within the project's account of",
    "public_review_label": "source-established project mechanism"
  },
  {
    "id": "e_overnight_principia_negative_feedback_self_org",
    "source": "concept_negative_feedback",
    "target": "concept_self_organisation",
    "relation_type": "explains",
    "relation_family": "causal_mechanism",
    "directed": "true",
    "dependency_kind": "mechanism",
    "confidence": "0.9",
    "claim_status": "accepted",
    "source_ids": "[\"src_principia_self_organisation_guide\"]",
    "evidence_ids": "[]",
    "source_locator": "Self-Organization guide, section 'The basic mechanism of self-organization', paragraphs on positive and negative feedback",
    "valid_from": "",
    "valid_to": "",
    "scope_conditions": "This is the feedback mechanism in Principia's project-authored account; it is not asserted as the only mechanism in every theory of self-organisation.",
    "assertion_mode": "asserted",
    "inference_method": "close reading of the internal theory page",
    "claim_id": "",
    "reviewed_by": "Benjamin P Taylor",
    "reviewed_at": "2026-08-14",
    "notes": "The guide pairs amplifying positive feedback with negative feedback that counters deviations and stabilises a new configuration.",
    "plain_phrase": "stabilises variation within the project's account of",
    "public_review_label": "source-established project mechanism"
  },
  {
    "id": "e_overnight_pattern_manual_multiple_perspectives",
    "source": "publication_pattern_manual_service_systems_thinking",
    "target": "concept_multiple_perspectives",
    "relation_type": "operationalises",
    "relation_family": "practice",
    "directed": "true",
    "dependency_kind": "",
    "confidence": "0.92",
    "claim_status": "accepted",
    "source_ids": "[\"src_ing_pattern_manual_2016\"]",
    "evidence_ids": "[]",
    "source_locator": "Pattern Manual paper, p. 13, paragraph beginning 'Extending issues to explicitly identify voices'",
    "valid_from": "",
    "valid_to": "",
    "scope_conditions": "The paper operationalises perspectives as named voices around an issue; it does not guarantee that every affected perspective will be represented.",
    "assertion_mode": "asserted",
    "inference_method": "close reading of the author paper",
    "claim_id": "",
    "reviewed_by": "Benjamin P Taylor",
    "reviewed_at": "2026-08-14",
    "notes": "Ing makes voices explicit in the service-systems pattern form so collective and individual perspectives are represented before action decisions.",
    "plain_phrase": "operationalises named voices as",
    "public_review_label": "source-established design move"
  },
  {
    "id": "e_overnight_systems_changes_action_learning",
    "source": "approach_family_systems_changes_learning",
    "target": "intervention_skill_action_learning",
    "relation_type": "specialises",
    "relation_family": "practice",
    "directed": "true",
    "dependency_kind": "",
    "confidence": "0.94",
    "claim_status": "accepted",
    "source_ids": "[\"src_ing_systems_changes_learning_2023\"]",
    "evidence_ids": "[]",
    "source_locator": "2023 author record, abstract; published article pp. 11-73, contextural action learning and three learning levels",
    "valid_from": "",
    "valid_to": "",
    "scope_conditions": "This records the paper's contextural-action-learning formulation, not equivalence with all action-learning traditions.",
    "assertion_mode": "asserted",
    "inference_method": "close reading of the author abstract and published article record",
    "claim_id": "",
    "reviewed_by": "Benjamin P Taylor",
    "reviewed_at": "2026-08-14",
    "notes": "The approach is explicitly framed as contextural action learning, developed through educating attention, learning for co-relating and learning for articulating.",
    "plain_phrase": "specialises a contextural form of",
    "public_review_label": "source-established author formulation"
  },
  {
    "id": "e_overnight_service_systems_multiple_perspectives",
    "source": "approach_family_service_systems_thinking",
    "target": "concept_multiple_perspectives",
    "relation_type": "methodological_prerequisite",
    "relation_family": "conceptual",
    "directed": "true",
    "dependency_kind": "methodological",
    "confidence": "0.9",
    "claim_status": "accepted",
    "source_ids": "[\"src_ing_pattern_manual_2016\",\"src_ing_coevolving_publications_2026\"]",
    "evidence_ids": "[]",
    "source_locator": "Pattern Manual paper, pp. 12-14; Coevolving publication record abstract describing voices on issues",
    "valid_from": "",
    "valid_to": "",
    "scope_conditions": "The requirement is specific to Ing's proposed service-systems-thinking pattern form.",
    "assertion_mode": "asserted",
    "inference_method": "comparison of the paper and author publication record",
    "claim_id": "",
    "reviewed_by": "Benjamin P Taylor",
    "reviewed_at": "2026-08-14",
    "notes": "The proposal begins with plural voices on issues before decisions about action, making multiple perspectives constitutive of this version of the approach.",
    "plain_phrase": "requires explicit voices to represent",
    "public_review_label": "source-established method requirement"
  },
  {
    "id": "e_overnight_sfi_emergence_complexity",
    "source": "concept_emergence",
    "target": "concept_complexity",
    "relation_type": "explains",
    "relation_family": "conceptual",
    "directed": "true",
    "dependency_kind": "",
    "confidence": "0.82",
    "claim_status": "provisional",
    "source_ids": "[\"src_sfi_complexity_about\",\"src_complexity_explorer_intro\"]",
    "evidence_ids": "[]",
    "source_locator": "SFI About, section 'What is Complex Systems Science?'; Complexity Explorer syllabus, units 1-10",
    "valid_from": "",
    "valid_to": "",
    "scope_conditions": "SFI presents surprising emergent macro behaviour as a recurring feature of interacting adaptive agents; complexity is broader than emergence and not every complex system exhibits the same form.",
    "assertion_mode": "interpreted",
    "inference_method": "interpretive synthesis of two official SFI scope statements",
    "claim_id": "",
    "reviewed_by": "Benjamin P Taylor",
    "reviewed_at": "2026-08-14",
    "notes": "The edge records SFI's cross-scale framing while avoiding the stronger and unsupported claim that emergence defines all complexity.",
    "plain_phrase": "characterises macro-level behaviour studied within",
    "public_review_label": "interpreted institutional framing"
  },
  {
    "id": "e_overnight_sfi_comparator_covers_self_org",
    "source": "comparator_corpus_santa_fe_institute_complexity_explorer",
    "target": "concept_self_organisation",
    "relation_type": "includes",
    "relation_family": "documentary",
    "directed": "true",
    "dependency_kind": "",
    "confidence": "0.99",
    "claim_status": "accepted",
    "source_ids": "[\"src_complexity_explorer_intro\"]",
    "evidence_ids": "[]",
    "source_locator": "Introduction to Complexity syllabus, unit 7 'Models of Biological Self-Organization'",
    "valid_from": "",
    "valid_to": "",
    "scope_conditions": "This is a curriculum-coverage claim, not a claim that the course's treatment is exhaustive.",
    "assertion_mode": "asserted",
    "inference_method": "syllabus inspection",
    "claim_id": "",
    "reviewed_by": "Benjamin P Taylor",
    "reviewed_at": "2026-08-14",
    "notes": "The official syllabus dedicates a unit to models of biological self-organisation.",
    "plain_phrase": "has a dedicated syllabus unit covering",
    "public_review_label": "source-established curriculum scope"
  },
  {
    "id": "e_overnight_ifsr_convening_perspectives",
    "source": "practice_systems_convening",
    "target": "concept_multiple_perspectives",
    "relation_type": "operationalises",
    "relation_family": "practice",
    "directed": "true",
    "dependency_kind": "",
    "confidence": "0.72",
    "claim_status": "provisional",
    "source_ids": "[\"src_ifsr_conversations_legacy\",\"src_taylor_boundaries_convening_2025\"]",
    "evidence_ids": "[]",
    "source_locator": "IFSR Conversations Legacy, programme-design paragraphs on non-hierarchical cross-tradition dialogue; Systems convening slides, slide 4",
    "valid_from": "",
    "valid_to": "",
    "scope_conditions": "The IFSR programme is an example interpreted through the atlas's systems-convening concept. The source does not use that label and does not demonstrate that dialogue resolves differences.",
    "assertion_mode": "interpreted",
    "inference_method": "cross-source comparison of programme design with the maintained practice definition",
    "claim_id": "",
    "reviewed_by": "Benjamin P Taylor",
    "reviewed_at": "2026-08-14",
    "notes": "Small, non-hierarchical conversations across traditions provide a concrete but limited example of creating conditions for multiple perspectives.",
    "plain_phrase": "can create a bounded space for",
    "public_review_label": "interpreted programme example"
  }
]''')

SOURCE_PATCHES: dict[str, dict[str, Any]] = {
    "src_complexity_explorer_intro": {
        "url": "https://www.complexityexplorer.org/courses/185-introduction-to-complexity",
        "publisher": "Santa Fe Institute Complexity Explorer",
        "notes": "Official ten-unit syllabus covering dynamics, chaos, information, self-organisation, agent-based modelling, networks and scaling. Used for curriculum coverage, not proof that the curriculum exhausts complexity science.",
        "review_status": "checked_internal_syllabus",
        "last_checked": "2026-08-14",
    },
    "src_taylor_reading_list_current": {
        "date": "2024-10-01",
        "quality_tier": "B",
        "notes": "Curator framing for the supplied 110-item inventory. It states that the list is partial and context-dependent and names a small set of practical starting points. It is evidence of intended coverage, not evidence for relationships among the listed works.",
        "review_status": "checked_primary_curator_record",
        "last_checked": "2026-08-14",
    },
}

SOURCE_RETIRED_IDS = {"src_taylor_reading_list_2024"}

SOURCE_MINING_UPDATES: dict[str, dict[str, str]] = json.loads(r'''{
  "mine_ashby_archive": {
    "status": "deep_structure_traversed_bounded_claims_only",
    "next_step": "Use journal page images and index-card locators for future claim-level work; do not infer influence from index co-occurrence."
  },
  "mine_asc_library": {
    "status": "history_and_archive_routes_traversed",
    "next_step": "Pair the society history with primary documents before settling priority, and retain its warning that cybernetics has multiple histories."
  },
  "mine_asc_archives": {
    "status": "working_group_and_uiuc_routes_traversed",
    "next_step": "Open collection-level records only when a current person or claim needs a document-level locator."
  },
  "mine_isss": {
    "status": "meeting_history_and_proceedings_routes_traversed",
    "next_step": "Use the chronology for organisational history only; verify conceptual influence in papers or correspondence."
  },
  "mine_ifsr": {
    "status": "conversations_legacy_and_publication_routes_traversed",
    "next_step": "Add conversation outputs only with participant, date and document-level provenance; do not treat dialogue as consensus."
  },
  "mine_system_dynamics_society": {
    "status": "method_guide_bibliography_and_proceedings_traversed",
    "next_step": "Pair the institutional method account with critical evaluation and primary modelling texts."
  },
  "mine_sfi": {
    "status": "about_research_course_and_working_paper_routes_traversed",
    "next_step": "Replace broad institutional framing with paper-level evidence for any stronger mechanism claim."
  },
  "mine_taylor_reading_list": {
    "status": "all_110_items_reconciled_80_inventory_only",
    "next_step": "Prioritise curator-named practical starting points and preserve the list's partial, context-dependent framing."
  }
}''')

EXTERNAL_CORPUS_REVIEW: list[dict[str, Any]] = json.loads(r'''[
  {
    "id": "external_principia",
    "corpus": "Principia Cybernetica",
    "pages_traversed": ["INTRO.html", "CYBSPRIN.html", "SELFORG.html", "MST.html", "MSTT.html", "HISTORY.html", "NUTSHELL.html", "NAV.html"],
    "reference_trails": ["project history -> CYBSYS-L debates and conferences", "self-organisation guide -> feedback mechanism", "overview -> typed semantic-network architecture"],
    "relationship_ids": ["e_07_principia_01", "e_07_principia_05", "e_overnight_principia_positive_feedback_self_org", "e_overnight_principia_negative_feedback_self_org"],
    "disagreement": "The project makes natural selection generative in its evolutionary account; natural drift disputes that mechanism and remains represented as a tension.",
    "uncertainty": "Project-authored pages are primary for self-description but not independent validation or a neutral history.",
    "decision": "Four narrow mechanism or architecture claims retained; no edge added from page adjacency alone."
  },
  {
    "id": "external_david_ing",
    "corpus": "David Ing / Coevolving Innovations",
    "pages_traversed": ["publications index", "Pattern Manual publication record and PDF", "Systems Changes Learning 2023 record and article", "1999 Ackoff influence record and paper trail", "digests index"],
    "reference_trails": ["Pattern Manual -> Alexander and service-systems pattern form", "Systems Changes Learning -> contextural action learning", "1999 paper -> three named Ackoff works"],
    "relationship_ids": ["e15_pattern_manual_develops_service_systems", "e15_ing_develops_service_systems", "e15_ing_develops_systems_changes", "e_overnight_pattern_manual_multiple_perspectives", "e_overnight_systems_changes_action_learning", "e_overnight_service_systems_multiple_perspectives"],
    "disagreement": "The Pattern Manual explicitly proposes revisions to the Alexandrian context-problem-solution form rather than treating it as directly portable.",
    "uncertainty": "First-party publication records establish authorship and intended concepts, not uptake or efficacy.",
    "decision": "Existing authorship edges located more precisely and three work-level conceptual routes added."
  },
  {
    "id": "external_reading_list",
    "corpus": "Benjamin P Taylor reading list",
    "pages_traversed": ["public curator post", "supplied 110-item inventory", "all inventory status records"],
    "reference_trails": ["curator post -> named practical starting points", "inventory -> existing people, works, methods and source records"],
    "relationship_ids": [],
    "disagreement": "The curator explicitly rejects a context-free canonical ordering; the inventory is therefore not treated as a ranking or genealogy.",
    "uncertainty": "80 items remain inventory-only and need item-level reading before relationship claims.",
    "decision": "Coverage reconciled; no title-derived edges added."
  },
  {
    "id": "external_ashby",
    "corpus": "W. Ross Ashby Digital Archive",
    "pages_traversed": ["journal index", "25-volume bookshelf", "timeline and summaries routes", "alphabetical and other indexes", "bibliography", "504-reference list", "letters index", "archive catalogue", "biography sections"],
    "reference_trails": ["keyword cards -> journal page images", "journal references -> alphabetical bibliography", "catalogue -> British Library shelfmarks"],
    "relationship_ids": [],
    "disagreement": "The archive itself warns that Ashby later judged some early notes inaccurate.",
    "uncertainty": "Index presence and correspondence establish documentary proximity, not influence or agreement.",
    "decision": "Primary archive structure recorded; no new semantic edge inferred."
  },
  {
    "id": "external_asc",
    "corpus": "American Society for Cybernetics",
    "pages_traversed": ["Foundations history contents", "control, system, communication, knowledge, circularity and feedback sections", "Archives Working Group", "newsletter and Zotero routes", "UIUC archive route"],
    "reference_trails": ["history sections -> people and primary traditions", "working group -> Ashby, ISSS and UIUC collections"],
    "relationship_ids": ["e_0342"],
    "disagreement": "The history explicitly describes cybernetics as having multiple intertwined and contested histories.",
    "uncertainty": "Institutional curation can privilege its own lineage; the Wiener primary-page locator remains pending.",
    "decision": "One existing historical edge strengthened but kept provisional."
  },
  {
    "id": "external_isss",
    "corpus": "International Society for the Systems Sciences",
    "pages_traversed": ["meeting history", "1954 formation record", "society name-change chronology", "annual themes", "proceedings and journal routes"],
    "reference_trails": ["formation record -> von Bertalanffy, Boulding, Rapoport and Gerard", "meeting table -> proceedings"],
    "relationship_ids": [],
    "disagreement": "Institutional continuity does not establish a single coherent intellectual lineage.",
    "uncertainty": "Participant co-presence and meeting chronology do not prove influence.",
    "decision": "Organisational provenance retained; no semantic edge added."
  },
  {
    "id": "external_ifsr",
    "corpus": "International Federation for Systems Research Conversations",
    "pages_traversed": ["Conversations legacy", "programme principles", "publication routes", "federation overview"],
    "reference_trails": ["legacy page -> conversation outputs and participants", "programme design -> second-order reflective practice"],
    "relationship_ids": ["e_overnight_ifsr_convening_perspectives"],
    "disagreement": "Dialogue across traditions is not evidence that disagreements were resolved.",
    "uncertainty": "The systems-convening label is an atlas interpretation, not IFSR terminology.",
    "decision": "One low-confidence interpreted practice example added with explicit scope."
  },
  {
    "id": "external_system_dynamics",
    "corpus": "System Dynamics Society",
    "pages_traversed": ["Study of System Dynamics method guide", "bibliography and literature-review routes", "MIT collection route", "conference proceedings examples on stocks, flows, feedback and model boundaries"],
    "reference_trails": ["method guide -> Richardson, Sterman and group model building", "bibliography -> conference proceedings"],
    "relationship_ids": ["e_0274"],
    "disagreement": "An endogenous-feedback account does not establish that qualitative diagrams or models are valid or effective in every setting.",
    "uncertainty": "Institutional sources require critical histories and evaluation for efficacy claims.",
    "decision": "One legacy-unverified edge upgraded to a precise method-structure claim."
  },
  {
    "id": "external_sfi",
    "corpus": "Santa Fe Institute / Complexity Explorer",
    "pages_traversed": ["SFI About and history", "research overview", "Introduction to Complexity syllabus and FAQ", "Complexity Explorer resource index", "working papers on emergence and evolution"],
    "reference_trails": ["course syllabus -> dynamics, self-organisation, agent-based modelling and networks", "working papers -> technical papers and PDFs"],
    "relationship_ids": ["e_overnight_sfi_emergence_complexity", "e_overnight_sfi_comparator_covers_self_org"],
    "disagreement": "SFI is a major complexity-science institution but not a proxy for the whole field or a warrant for importing every complexity concept into social practice.",
    "uncertainty": "The emergence-to-complexity edge is an institutional framing and remains explicitly interpreted and provisional.",
    "decision": "One documentary curriculum edge and one scoped conceptual framing added."
  }
]''')


def parse_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    try:
        parsed = json.loads(value or "[]")
        return parsed if isinstance(parsed, list) else []
    except (TypeError, json.JSONDecodeError):
        return []


def upsert(records: list[dict[str, Any]], incoming: list[dict[str, Any]]) -> None:
    positions = {record.get("id"): index for index, record in enumerate(records)}
    for record in incoming:
        if record["id"] in positions:
            records[positions[record["id"]]] = record
        else:
            positions[record["id"]] = len(records)
            records.append(record)


def apply_source_patches(data: dict[str, Any]) -> None:
    found: set[str] = set()
    for source in data.get("sources", []):
        patch = SOURCE_PATCHES.get(source.get("id"))
        if patch:
            source.update(patch)
            found.add(source["id"])
    missing = sorted(set(SOURCE_PATCHES) - found)
    if missing:
        raise RuntimeError(f"Source patches missing from generated data: {missing}")


def apply_external_corpus_review(data: dict[str, Any]) -> None:
    upsert(data["edges"], NEW_EDGES)
    data["external_corpus_review"] = EXTERNAL_CORPUS_REVIEW
    found: set[str] = set()
    for record in data.get("source_mining_register", []):
        patch = SOURCE_MINING_UPDATES.get(record.get("id"))
        if patch:
            record.update(patch)
            found.add(record["id"])
    missing = sorted(set(SOURCE_MINING_UPDATES) - found)
    if missing:
        raise RuntimeError(f"Source-mining records missing from generated data: {missing}")


def apply_edge_patches(data: dict[str, Any]) -> None:
    found: set[str] = set()
    for edge in data.get("edges", []):
        patch = EDGE_PATCHES.get(edge.get("id"))
        if patch:
            edge.update(patch)
            found.add(edge["id"])
    missing = sorted(set(EDGE_PATCHES) - found)
    if missing:
        raise RuntimeError(f"Reviewed edge patches missing from generated graph: {missing}")


def repeated_assertions(edges: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[tuple[str, ...], list[dict[str, Any]]] = {}
    for edge in edges:
        key = (
            str(edge.get("source", "")),
            str(edge.get("target", "")),
            str(edge.get("relation_type", "")),
            str(edge.get("claim_status", "")),
            str(edge.get("assertion_mode", "")),
            str(edge.get("source_locator", "")),
        )
        groups.setdefault(key, []).append(edge)
    return [
        {
            "edge_ids": [edge["id"] for edge in group],
            "source": group[0]["source"],
            "target": group[0]["target"],
            "relation_type": group[0]["relation_type"],
        }
        for group in groups.values()
        if len(group) > 1
    ]


def quality_result(data: dict[str, Any]) -> dict[str, Any]:
    edges = data.get("edges", [])
    depth = data["relational_depth"]
    by_node = depth["by_node"]
    precision_pattern = re.compile(
        r"(?:\bpp?\.?\s*\d|\bpages?\s+\d|\bchapter\s+\d|"
        r"\bsections?\s+|\bslides?\s+\d|\bparagraphs?\b|"
        r"\bappendix\b|\bfigure\s+\d|\btable\s+\d|\bentry\b)",
        re.IGNORECASE,
    )
    generic = [
        {
            "id": edge["id"],
            "source": edge["source"],
            "target": edge["target"],
            "relation_type": edge.get("relation_type", ""),
            "plain_phrase": edge.get("plain_phrase", ""),
            "claim_status": edge.get("claim_status", ""),
            "assertion_mode": edge.get("assertion_mode", ""),
            "source_ids": parse_list(edge.get("source_ids")),
            "source_locator": edge.get("source_locator", ""),
        }
        for edge in edges
        if edge.get("relation_type") == "conceptually_related_to"
        or "related to" in str(edge.get("plain_phrase", "")).lower()
    ]
    repeated = repeated_assertions(edges)
    directed = sum(str(edge.get("directed")) == "true" for edge in edges)
    rationale = sum(
        bool(str(edge.get("notes", "")).strip())
        or bool(str(edge.get("scope_conditions", "")).strip())
        or bool(str(edge.get("inference_method", "")).strip())
        for edge in edges
    )
    locator = sum(bool(str(edge.get("source_locator", "")).strip()) for edge in edges)
    precise = sum(
        bool(precision_pattern.search(str(edge.get("source_locator", ""))))
        for edge in edges
    )
    current = {
        "public_entries": depth["aggregate"]["public_entries"],
        "all_nodes": len(data.get("nodes", [])),
        "all_edges": len(edges),
        "sources": len(data.get("sources", [])),
        "claims": len(data.get("claims", [])),
        "evidence_records": len(data.get("evidence", [])),
        "profiles": len(data.get("profiles", [])),
        "journeys": len(data.get("journeys", [])),
        "external_corpora_reviewed": len(data.get("external_corpus_review", [])),
        "reader_connected_entries": depth["aggregate"]["reader_connected_entries"],
        "semantic_connected_entries": depth["aggregate"]["semantic_connected_entries"],
        "semantic_gap_entries": depth["aggregate"]["public_entries"] - depth["aggregate"]["semantic_connected_entries"],
        "connection_bands": depth["aggregate"]["connection_bands"],
        "evidence_bands": depth["aggregate"]["evidence_bands"],
        "reader_statements": depth["aggregate"]["reader_statements"],
        "semantic_statements": depth["aggregate"]["semantic_statements"],
    }
    return {
        "schema_version": "1.1",
        "generated": "2026-08-14",
        "release": data["meta"]["release"],
        "purpose": "Machine-readable relationship-quality result after the evidence-led relationship review.",
        "contract": {
            "human_readable_rationale": "A relation has a plain phrase and either notes, scope conditions or an inference method.",
            "typed_and_directed": "A relation has an explicit relation type, family and direction decision; legitimate undirected relations are reported separately.",
            "source_located": "Source identifiers, locator presence and precision-shaped locator text are measured separately.",
            "epistemic_status": "Claim status, assertion mode and public review label distinguish accepted, provisional, contested and interpreted statements.",
            "generic_relation": "A conceptually_related_to type or public phrase containing related to is a review target.",
            "diverse_routes": "Reader-visible nodes are measured by distinct relation families; three or more is the stronger-route threshold.",
        },
        "baseline": {
            "public_entries": 496,
            "all_edges": 1712,
            "sources": 153,
            "reader_connected_entries": 496,
            "semantic_connected_entries": 329,
            "semantic_gap_entries": 167,
            "connection_bands": {"developing": 236, "rich": 35, "thin": 225},
            "reader_statements": 1161,
            "semantic_statements": 747,
        },
        "current": current,
        "changes_from_baseline": {
            "generic_relation_review_targets": {"before": 8, "after": len(generic)},
            "repeated_assertion_groups": {"before": 1, "after": len(repeated)},
            "sources": {"before": 153, "after": len(data.get("sources", []))},
            "semantic_connected_entries": {
                "before": 329,
                "after": current["semantic_connected_entries"],
                "note": "A generic journal-to-tradition edge was replaced by a narrower documentary scope claim; unsupported semantic reach was not preserved.",
            },
            "substantive_edge_count": {
                "before": 750,
                "after": data["graph_snapshot"]["substantive_edge_count"],
            },
            "isolated_semantic_nodes": {
                "before": 167,
                "after": data["graph_snapshot"]["isolated_node_count"],
            },
        },
        "criteria": {
            "typed": {
                "passing": sum(bool(str(edge.get("relation_type", "")).strip()) and bool(str(edge.get("relation_family", "")).strip()) for edge in edges),
                "total": len(edges),
            },
            "directed": {"passing": directed, "total": len(edges), "undirected": len(edges) - directed},
            "human_readable_phrase": {
                "passing": sum(bool(str(edge.get("plain_phrase", "")).strip()) for edge in edges),
                "total": len(edges),
            },
            "explicit_rationale": {"passing": rationale, "total": len(edges)},
            "source_identifier": {
                "passing": sum(bool(parse_list(edge.get("source_ids"))) for edge in edges),
                "total": len(edges),
            },
            "locator_present": {"passing": locator, "total": len(edges)},
            "precision_shaped_locator": {
                "passing": precise,
                "total": len(edges),
                "note": "Conservative text-pattern measure; manual review is still required.",
            },
            "epistemic_fields_present": {
                "passing": sum(
                    bool(str(edge.get("claim_status", "")).strip())
                    and bool(str(edge.get("assertion_mode", "")).strip())
                    and bool(str(edge.get("public_review_label", "")).strip())
                    for edge in edges
                ),
                "total": len(edges),
            },
            "generic_related_to": {
                "passing": len(edges) - len(generic),
                "total": len(edges),
                "review_target_count": len(generic),
            },
            "three_or_more_relation_families": {
                "passing": sum(record["distinct_reader_families"] >= 3 for record in by_node.values()),
                "total": current["public_entries"],
            },
            "one_relation_family": {
                "count": sum(record["distinct_reader_families"] == 1 for record in by_node.values()),
                "total": current["public_entries"],
            },
            "external_corpus_records": {
                "passing": sum(
                    bool(record.get("pages_traversed"))
                    and "uncertainty" in record
                    and "decision" in record
                    for record in data.get("external_corpus_review", [])
                ),
                "total": len(data.get("external_corpus_review", [])),
            },
        },
        "generic_relation_review": generic,
        "repeated_assertion_review": repeated,
        "largest_thin_cohorts": [
            {"entity_type": "person", "thin": 112, "total": 169},
            {"entity_type": "publication", "thin": 108, "total": 121},
        ],
        "priority_queue": depth["priority_queue"],
        "limitations": [
            "A source identifier can point to a broad collection and does not by itself establish a precise evidential warrant.",
            "Undirected co-authorship and similarity relations can be legitimate; direction is a semantic decision, not a blanket pass/fail rule.",
            "The audit does not claim that all edges are substantive; maintained reader and semantic subsets remain the relevant depth measures.",
            "Pass 2 accepts a one-entry reduction in semantic reach where the previous journal-to-tradition edge was supported only by resemblance and discovery context.",
        ],
    }



def write_review_note(result: dict[str, Any]) -> None:
    text = RELATIONAL_DOC.read_text(encoding="utf-8")
    marker = "\n## Evidence-led relationship review\n"
    text = text.split(marker, 1)[0].rstrip()
    current = result["current"]
    changes = result["changes_from_baseline"]
    lines = [
        marker.rstrip(),
        "",
        "The 2026-08-14 relationship pass re-audited every public entry and reviewed all generic or repetitive assertions against their cited sources.",
        "",
        f"- Generic relation review targets: {changes['generic_relation_review_targets']['before']} → {changes['generic_relation_review_targets']['after']}.",
        f"- Repeated assertion groups: {changes['repeated_assertion_groups']['before']} → {changes['repeated_assertion_groups']['after']}.",
        f"- Reader-connected entries: {current['reader_connected_entries']}.",
        f"- Semantically connected entries: {current['semantic_connected_entries']}.",
        f"- Rich / developing / thin: {current['connection_bands'].get('rich', 0)} / {current['connection_bands'].get('developing', 0)} / {current['connection_bands'].get('thin', 0)}.",
        "",
        "One generic journal-to-tradition edge was deliberately narrowed to a documentary scope claim. Semantic reach therefore falls by one rather than preserving an unsupported relationship.",
        "",
    ]
    RELATIONAL_DOC.write_text(text + "\n\n" + "\n".join(lines), encoding="utf-8")

def main() -> None:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    data["sources"] = [
        source for source in data.get("sources", [])
        if source.get("id") not in SOURCE_RETIRED_IDS
    ]
    upsert(data["sources"], SOURCE_RECORDS)
    apply_source_patches(data)
    apply_external_corpus_review(data)
    apply_edge_patches(data)
    data["relational_depth"] = calculate_relational_depth(data)
    data["graph_snapshot"] = calculate_graph_snapshot(data)
    aggregate = data["relational_depth"]["aggregate"]
    data["meta"].update(
        {
            "edge_count": len(data.get("edges", [])),
            "source_count": len(data.get("sources", [])),
            "public_link_source_count": sum(source.get("public_link_status") == "public_link" for source in data.get("sources", [])),
            "no_public_link_source_count": sum(source.get("public_link_status") == "no_public_link" for source in data.get("sources", [])),
            "source_mining_register_count": len(data.get("source_mining_register", [])),
            "external_corpus_review_count": len(data.get("external_corpus_review", [])),
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
    write_data(data)
    result = quality_result(data)
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    QUALITY_PATH.write_text(rendered, encoding="utf-8")
    QUALITY_PUBLIC_PATH.parent.mkdir(parents=True, exist_ok=True)
    QUALITY_PUBLIC_PATH.write_text(rendered, encoding="utf-8")
    write_review_note(result)
    print(json.dumps({"quality": result["criteria"], "current": result["current"]}, indent=2))


if __name__ == "__main__":
    main()
