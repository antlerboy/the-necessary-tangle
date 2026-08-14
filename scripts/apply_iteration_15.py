#!/usr/bin/env python3
"""Apply release 0.15: David Ing, reading-list depth and core systems practice."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from apply_iteration_09 import graph_metrics
from apply_iteration_14 import enc

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / 'data' / 'public-data.json'
INVENTORY_SOURCE = ROOT / 'data' / 'reading-list-inventory-source.json'
DOCS_ASSETS = ROOT / 'docs' / 'assets'
DOCUMENTATION = ROOT / 'documentation'
RELEASE = '0.15-ing-reading-practice-alpha'
GENERATED = '2026-08-14'


def source(id: str, title: str, source_type: str, url: str, notes: str, creators: list[str], publisher: str = '') -> dict[str, Any]:
    return {
        'id': id, 'title': title, 'source_type': source_type, 'quality_tier': 'A', 'access': 'public',
        'url': url, 'date': f'checked {GENERATED}', 'notes': notes, 'creators': enc(creators), 'doi': '', 'isbn': '',
        'publisher': publisher, 'licence': 'site terms unless otherwise stated', 'archived_url': '', 'content_hash': '',
        'review_status': 'checked', 'last_checked': GENERATED, 'public_link_status': 'public_link',
    }


SOURCE_UPSERTS = [
    source('src_ing_coevolving_publications_2026', 'David Ing — Coevolving Innovations publications', 'primary_author_publication_index', 'https://coevolving.com/commons/publications', 'Primary index for David Ing’s systems, service-systems and education publications and presentations. Useful for chronology and authorship; not independent evaluation.', ['David Ing'], 'Coevolving Innovations'),
    source('src_ing_pattern_manual_2016', 'Pattern Manual for Service Systems Thinking', 'primary_publication_record', 'https://coevolving.com/commons/20161028-pattern-manual-for-service-systems-thinking', 'Primary record of Ing’s 2016 proposal to adapt generative pattern-language practice for service systems thinking, including the alternative pattern form of voices, values and spatio-temporal frames.', ['David Ing'], 'Coevolving Innovations'),
    source('src_ing_systems_changes_learning_2022', 'When Unfreeze-Move-Refreeze Isn’t Working', 'primary_publication_record', 'https://systemschanges.com/online/presentations/20220711-when-unfreeze-move-refreeze-isnt-working', 'Primary account of Systems Changes Learning, including rhythmic shifts, texture/contexture, propensity, contextual-dyadic thinking and action learning.', ['David Ing'], 'Systems Changes'),
    source('src_ing_knowing_better_2022', 'Knowing Better via Systems Thinking', 'primary_publication_record', 'https://systemschanges.com/online/presentations/20221010-knowing-better-via-systems-thinking', 'Primary account that explicitly places contemporary systems approaches in longer systems-sciences traditions and uses that lineage as part of teaching systems thinking.', ['David Ing'], 'Systems Changes'),
    source('src_isss_ing_presidential_address_2011', 'David Ing — ISSS presidential address', 'institutional_archive', 'https://www.isss.org/presidential-addresses/', 'ISSS archive for Ing’s 2011 incoming presidential address, ‘Service Systems, Natural Systems: Sciences in Synthesis’, documenting his leadership role and service-systems synthesis.', ['International Society for the Systems Sciences'], 'ISSS'),
    source('src_systems_thinkers_springer', 'Systems Thinkers — Springer record', 'publisher_record', 'https://link.springer.com/book/10.1007/978-1-84882-525-3', 'Publisher record for Magnus Ramage and Karen Shipp’s systems-thinkers text, developed from an Open University course and organised around people and traditions in the systems field.', ['Magnus Ramage', 'Karen Shipp'], 'Springer'),
    source('src_von_foerster_understanding_springer', 'Understanding Understanding — Springer record', 'publisher_record', 'https://link.springer.com/book/10.1007/b97451', 'Publisher record for Heinz von Foerster’s essays on cybernetics, cognition, knowledge and the observer.', ['Heinz von Foerster'], 'Springer'),
    source('src_block_flawless_wiley', 'Flawless Consulting — Wiley record', 'publisher_record', 'https://www.wiley.com/en-us/Flawless+Consulting%3A+A+Guide+to+Getting+Your+Expertise+Used%2C+4th+Edition-p-9781394177318', 'Publisher record for Peter Block’s consulting practice, focused on helping expertise get used through contracting, discovery, feedback, engagement and implementation.', ['Peter Block'], 'Wiley'),
]


def node(id: str, label: str, entity_type: str, description: str, source_ids: list[str], x: float, y: float, tags: list[str] | None = None) -> dict[str, Any]:
    tags = tags or []
    return {
        'id': id, 'label': label, 'entity_type': entity_type, 'description': description, 'aliases': '[]', 'boundary_ring': '0',
        'inclusion_reason': 'iteration_0_15_depth_and_practice', 'status': 'accepted', 'source_ids': enc(source_ids),
        'set_tags': enc(['systems', 'practice', 'release_0_15', *tags]), 'espoused_labels': '[]', 'observed_clusters': '[]',
        'canonical_definition': description, 'valid_from': '', 'valid_to': '', 'external_ids': '{}', 'geographies': '[]', 'licence': '',
        'review_status': 'curator_checked_public_sources', 'reviewed_by': 'Benjamin P Taylor', 'reviewed_at': GENERATED,
        'x': x, 'y': y, 'canonical_id': id, 'public_visibility': 'public', 'publication_level': 'profile', 'public_stub_text': '',
        'public_source_count': len(source_ids), 'no_public_link_count': 0,
    }


NODE_UPSERTS = [
    node('person_david_ing', 'David Ing', 'person', 'Systems researcher, educator and practitioner whose work connects service systems, systems thinking education, pattern language, systems changes and the documentation of systems lineages.', ['src_ing_coevolving_publications_2026','src_isss_ing_presidential_address_2011'], 0.38, -0.09, ['lineage','education']),
    node('corpus_coevolving_innovations', 'Coevolving Innovations', 'corpus', 'David Ing’s long-running public corpus of publications, teaching materials, conference records and reflective writing on systems and service systems.', ['src_ing_coevolving_publications_2026'], 0.47, -0.06, ['corpus','lineage']),
    node('corpus_systems_changes', 'Systems Changes', 'corpus', 'Public corpus for Systems Changes Learning: an action-learning programme on systems changes, living systems, temporality, contextual-dyadic thinking and practice.', ['src_ing_systems_changes_learning_2022','src_ing_knowing_better_2022'], 0.49, -0.13, ['corpus','learning']),
    node('approach_family_service_systems_thinking', 'Service systems thinking', 'approach_family', 'An approach developed across service science and systems practice that treats services as relational, value-co-creating systems and adapts systems and pattern-language ideas to service contexts.', ['src_ing_pattern_manual_2016','src_ing_coevolving_publications_2026'], 0.31, -0.04, ['service-systems']),
    node('approach_family_systems_changes_learning', 'Systems Changes Learning', 'approach_family', 'A learning approach associated with David Ing and collaborators that treats changes in living systems through rhythmic shifts, texture/contexture, propensity and knowing from within rather than a simple unfreeze-change-refreeze sequence.', ['src_ing_systems_changes_learning_2022'], 0.34, -0.16, ['learning','living-systems']),
    node('publication_pattern_manual_service_systems_thinking', 'Pattern Manual for Service Systems Thinking', 'publication', 'David Ing’s 2016 proposal to translate lessons from generative pattern languages into service systems thinking, reframing patterns around voices on issues, affording values and spatio-temporal frames.', ['src_ing_pattern_manual_2016'], 0.25, -0.08, ['publication','pattern-language']),
    node('practice_systems_lineage_documentation', 'Systems lineage documentation', 'practice', 'The practice of preserving how ideas, people, institutions, teaching events and publications connect over time, while distinguishing documented contact or citation from stronger claims of intellectual influence.', ['src_ing_coevolving_publications_2026','src_ing_knowing_better_2022','src_isss_ing_presidential_address_2011'], 0.40, 0.01, ['lineage','documentation']),
    node('publication_systems_thinkers_ramage_shipp', 'Systems Thinkers', 'publication', 'Magnus Ramage and Karen Shipp’s people-centred account of systems traditions, developed from Open University teaching and useful as a map of thinkers, contexts and lineages rather than a single unified school.', ['src_systems_thinkers_springer','src_taylor_reading_list_current'], -0.21, 0.33, ['reading-list','history']),
    node('publication_steps_to_ecology_of_mind', 'Steps to an Ecology of Mind', 'publication', 'Gregory Bateson’s collection of essays linking anthropology, psychiatry, cybernetics, learning, communication, evolution and epistemology.', ['src_bateson_steps_ecology_1972','src_taylor_reading_list_current'], -0.31, 0.19, ['reading-list','cybernetics']),
    node('publication_understanding_understanding', 'Understanding Understanding', 'publication', 'Heinz von Foerster’s collected essays on cybernetics and cognition, centring the observer, knowing, self-reference and the ethical implications of constructing descriptions.', ['src_von_foerster_understanding_springer','src_taylor_reading_list_current'], -0.36, 0.27, ['reading-list','cybernetics']),
    node('publication_flawless_consulting', 'Flawless Consulting: A Guide to Getting Your Expertise Used', 'publication', 'Peter Block’s practice text on the consulting relationship, including contracting, discovery, feedback, engagement and implementation as conditions for getting expertise used.', ['src_block_flawless_wiley','src_taylor_reading_list_current'], 0.12, 0.39, ['reading-list','intervention']),
    node('practice_core_systems_practice_spine', 'Core systems practice spine', 'practice', 'A practice spine connecting systems concepts and laws, choice and combination of systems approaches, modelling, intervention, stakeholder engagement and reflexive learning. It is a competence structure, not one methodology.', ['src_skills_england_st0787_v12','src_scio_accreditation_current','src_scio_professional_development_current'], 0.02, 0.02, ['professional-practice','apprenticeship']),
]

PROFILE_SPECS: dict[str, dict[str, Any]] = {
    'person_david_ing': {
        'summary': 'Ing’s work is useful in two ways at once: he develops service-systems and systems-changes approaches, and he leaves unusually inspectable public trails through systems scholarship, teaching and institutions.',
        'why_it_matters': 'The atlas needs lineages that are documented rather than merely asserted. Ing’s publication archives, teaching records and ISSS work connect contemporary practice to longer systems traditions while also contributing his own approaches.',
        'key_distinctions': ['service systems are relational rather than reducible to service transactions','systems changes are not assumed to follow unfreeze-change-refreeze','documented association is weaker than demonstrated intellectual influence','systems traditions are plural and historically situated'],
        'historical_lineage': ['ISSS leadership and systems-sciences community','service systems science','systems thinking education','pattern-language research','Systems Changes Learning Circle'],
        'logical_antecedents': ['systems sciences','service science','Gregory Bateson’s ecological epistemology','Christopher Alexander’s pattern language','learning and action inquiry'],
        'dependent_subsequents': ['service systems thinking teaching','Systems Changes Learning','pattern-language experiments for services','lineage-rich public systems archives'],
        'practice_connections': ['teaching systems thinking','learning circles','service-system inquiry','public documentation of conferences and sources'],
        'common_misreadings': ['Treating Ing only as a documenter misses substantive service-systems and systems-changes work.','Treating a documented connection as proof of influence overstates what an archive can establish.'],
        'open_checks': ['Add more independent scholarship evaluating the service-systems and systems-changes contributions.'],
    },
    'corpus_coevolving_innovations': {
        'summary': 'A public archive of Ing’s systems publications, courses, talks and reflective records.',
        'why_it_matters': 'It provides chronology and lineage evidence that is often missing from systems accounts.',
        'key_distinctions': ['primary record versus independent evaluation','event documentation versus influence claim'],
        'historical_lineage': ['David Ing’s research and teaching','ISSS and systems communities'], 'logical_antecedents': ['systems scholarship','open web publishing'], 'dependent_subsequents': ['service systems thinking materials','lineage research'], 'practice_connections': ['source discovery','teaching history','conference documentation'], 'common_misreadings': ['Archive density is not proof of conceptual centrality.'], 'open_checks': ['Continue adding independent corroboration for major lineage claims.'],
    },
    'corpus_systems_changes': {
        'summary': 'A public research-and-learning corpus that develops a temporally sensitive account of systems changes in living systems.', 'why_it_matters': 'It offers a contrasting grammar to stage-based change models and keeps doing, thinking and making together.', 'key_distinctions': ['changes rather than a singular planned change','rhythmic shifts rather than static states','contexture rather than decontextualised variables','propensity rather than prediction'], 'historical_lineage': ['Systems Changes Learning Circle','Bateson','Tim Ingold','contextual-dyadic philosophy'], 'logical_antecedents': ['living systems','ecological epistemology','action learning'], 'dependent_subsequents': ['workshops and learning circles','systems-changes practices'], 'practice_connections': ['collective inquiry','reframing change','temporality'], 'common_misreadings': ['It is not simply another change-management sequence.'], 'open_checks': ['Add comparative accounts from other living-systems and process traditions.'],
    },
    'approach_family_service_systems_thinking': {
        'summary': 'A systems approach to services that foregrounds relations, value, context and co-production and uses generative patterns as one means of making practices discussable.', 'why_it_matters': 'It connects systems inquiry to the design and operation of services without assuming the service is a bounded product.', 'key_distinctions': ['service system versus product/service object','value co-creation versus unilateral delivery','pattern language as generative inquiry rather than recipe'], 'historical_lineage': ['service science','systems sciences','pattern language'], 'logical_antecedents': ['Christopher Alexander','service-dominant and service-systems thinking'], 'dependent_subsequents': ['service systems pattern work'], 'practice_connections': ['service design','pattern workshops','systems education'], 'common_misreadings': ['A pattern is not a context-free best practice.'], 'open_checks': ['Strengthen comparison with service design and service-dominant logic.'],
    },
    'approach_family_systems_changes_learning': {
        'summary': 'An action-learning approach for attending to changes in living systems through rhythm, texture/contexture and propensity.', 'why_it_matters': 'It resists both static system descriptions and staged change assumptions.', 'key_distinctions': ['living temporality versus frozen state','propensity versus deterministic forecast','knowing from within versus detached diagnosis'], 'historical_lineage': ['Systems Changes Learning Circle','Bateson','Ingold'], 'logical_antecedents': ['ecological epistemology','action learning'], 'dependent_subsequents': ['learning-circle practices'], 'practice_connections': ['change inquiry','group learning','contextual diagnosis'], 'common_misreadings': ['The vocabulary is not a relabelling of Lewinian stage change.'], 'open_checks': ['Add case evidence beyond author-maintained sources.'],
    },
    'publication_pattern_manual_service_systems_thinking': {
        'summary': 'A proposal for carrying generative pattern-language learning into service systems.', 'why_it_matters': 'It shows how a method can be translated between domains only by changing its ontology and pattern form.', 'key_distinctions': ['context-problem-solution versus voices-values-spatio-temporal frames','translation versus copying'], 'historical_lineage': ['Alexander and pattern language','service systems thinking'], 'logical_antecedents': ['generative pattern languages','service systems'], 'dependent_subsequents': ['service-systems pattern work'], 'practice_connections': ['pattern workshops','service design'], 'common_misreadings': ['It does not claim the built-environment pattern form can simply be reused unchanged.'], 'open_checks': ['Trace later adoption and critique.'],
    },
    'practice_systems_lineage_documentation': {
        'summary': 'A documentary practice for making intellectual and practitioner histories inspectable without turning every contact into a genealogy.', 'why_it_matters': 'Systems fields are unusually vulnerable to compressed origin stories. Public trails of events, citations, courses and collaborations permit stronger and weaker lineage claims to be separated.', 'key_distinctions': ['contact versus influence','citation versus adoption','shared institution versus shared theory','primary archive versus independent history'], 'historical_lineage': ['history of ideas','archival practice','systems-community documentation'], 'logical_antecedents': ['source criticism','provenance'], 'dependent_subsequents': ['better lineage maps','contestable historical claims'], 'practice_connections': ['research','curation','teaching'], 'common_misreadings': ['A dense network of documented associations is not itself a school.'], 'open_checks': ['Add more archival and oral-history sources from outside current well-documented networks.'],
    },
    'publication_systems_thinkers_ramage_shipp': {
        'summary': 'A people-centred introduction to systems traditions and their historical development.', 'why_it_matters': 'It helps readers meet systems thinking as plural lineages rather than a single doctrine and provides a bridge between biographies, ideas and traditions.', 'key_distinctions': ['traditions versus one systems school','historical person-centred account versus method manual'], 'historical_lineage': ['Open University systems teaching'], 'logical_antecedents': ['systems history','systems education'], 'dependent_subsequents': ['systems curricula','lineage orientation'], 'practice_connections': ['teaching','reading-list orientation'], 'common_misreadings': ['Its inclusion of a thinker does not imply agreement among thinkers.'], 'open_checks': ['Connect individual chapters to primary works as coverage deepens.'],
    },
    'publication_steps_to_ecology_of_mind': {
        'summary': 'Bateson’s essays connect communication, learning, psychiatry, anthropology, evolution and cybernetics through recurring concern with relation, pattern and epistemology.', 'why_it_matters': 'Many later systems and complexity practices borrow Batesonian vocabulary while losing the epistemological argument that makes it difficult.', 'key_distinctions': ['relation versus isolated thing','levels of learning','ecology of ideas','difference and information'], 'historical_lineage': ['cybernetics','anthropology','communication theory'], 'logical_antecedents': ['Wiener-era cybernetics','anthropological fieldwork'], 'dependent_subsequents': ['family therapy','second-order cybernetics','ecological and systemic epistemologies'], 'practice_connections': ['learning','framing','communication','double bind'], 'common_misreadings': ['Bateson is not simply a source of systems aphorisms.'], 'open_checks': ['Develop essay-level entries where they are used as bridge concepts.'],
    },
    'publication_understanding_understanding': {
        'summary': 'Von Foerster’s essays develop a cybernetics in which observation, knowing and description cannot be treated as external to the system being discussed.', 'why_it_matters': 'It provides a direct route into second-order cybernetics and the ethical consequences of taking the observer seriously.', 'key_distinctions': ['observed systems versus observing systems','description versus world-in-itself','responsibility of the observer'], 'historical_lineage': ['Biological Computer Laboratory','second-order cybernetics'], 'logical_antecedents': ['cybernetics','constructivist epistemology'], 'dependent_subsequents': ['second-order systems practice','constructivist approaches'], 'practice_connections': ['reflexivity','ethics','observer-aware inquiry'], 'common_misreadings': ['Constructed descriptions do not imply that any description is equally useful or consequence-free.'], 'open_checks': ['Add essay-level links to ethics, self-reference and computation.'],
    },
    'publication_flawless_consulting': {
        'summary': 'Block treats consulting as a relationship and contracting practice rather than the transfer of expert answers.', 'why_it_matters': 'Systems interventions fail as often through contracting, ownership and implementation relations as through weak technical models.', 'key_distinctions': ['consulting relationship versus expert delivery','authentic contracting versus covert control','engagement versus compliance'], 'historical_lineage': ['organisation development','consulting practice'], 'logical_antecedents': ['helping relationships','organisation development'], 'dependent_subsequents': ['consulting and facilitation practice'], 'practice_connections': ['contracting','feedback','implementation','stakeholder work'], 'common_misreadings': ['It is not a systems methodology; it supports the intervention relationship around one.'], 'open_checks': ['Link to helping, facilitation and power traditions.'],
    },
    'practice_core_systems_practice_spine': {
        'summary': 'The professional spine joins concepts and laws, method choice, modelling, intervention, engagement and reflexive learning. CSH, SSM, System Dynamics and VSM are major approaches within that practice, not substitutes for the whole of it.', 'why_it_matters': 'A practitioner can know a method and still lack systemic practice. The occupational standard explicitly combines systems concepts, multiple approaches, modelling, engagement, intervention and reflexive participation.', 'key_distinctions': ['systems knowledge versus method competence','model versus situation','approach choice versus method loyalty','intervention versus analysis','reflexive participation versus detached expertise'], 'historical_lineage': ['SCiO competency framework','Systems Thinking Practitioner occupational standard','practice traditions across CSH, SSM, System Dynamics and VSM'], 'logical_antecedents': ['systems concepts and laws','professional judgement','multiple perspectives','boundary critique'], 'dependent_subsequents': ['multi-methodology','systems intervention','professional accreditation'], 'practice_connections': ['CSH','SSM','System Dynamics','VSM','stakeholder engagement','modelling','learning'], 'common_misreadings': ['The four named approaches are not a complete list of systems practice.','Core systems practice is not merely drawing maps or choosing a branded framework.'], 'open_checks': ['Keep provider-specific module packaging distinct from the public occupational standard and SCiO competence structure.'],
    },
}


def profile(n: dict[str, Any], spec: dict[str, Any]) -> dict[str, Any]:
    return {
        'node_id': n['id'], 'title': n['label'], 'profile_status': 'curator_checked_public_sources', 'canonical_definition': n['description'],
        'summary': spec['summary'], 'why_it_matters': spec['why_it_matters'], 'key_distinctions': enc(spec['key_distinctions']),
        'historical_lineage': enc(spec['historical_lineage']), 'logical_antecedents': enc(spec['logical_antecedents']),
        'dependent_subsequents': enc(spec['dependent_subsequents']), 'practice_connections': enc(spec['practice_connections']),
        'espoused_lineages': '[]', 'observed_clusters': '[]', 'common_misreadings': enc(spec['common_misreadings']), 'open_checks': enc(spec['open_checks']),
        'source_ids': n['source_ids'], 'evidence_ids': '[]', 'last_researched': GENERATED, 'review_status': 'curator_checked_public_sources',
        'reviewed_by': 'Benjamin P Taylor', 'reviewed_at': GENERATED,
        'editorial_note': 'Public account based on named sources; documentary provenance, interpretation and evaluative claims are kept distinct.',
    }


def edge(id: str, src: str, dst: str, relation_type: str, family: str, phrase: str, source_ids: list[str], notes: str = '') -> dict[str, Any]:
    return {
        'id': id, 'source': src, 'target': dst, 'relation_type': relation_type, 'relation_family': family, 'directed': 'true',
        'dependency_kind': '', 'confidence': '0.88', 'claim_status': 'accepted', 'source_ids': enc(source_ids), 'evidence_ids': '[]',
        'source_locator': 'Release 0.15 public sources', 'valid_from': '', 'valid_to': '',
        'scope_conditions': 'Limited to the named sources. Documentary connection, conceptual influence, teaching use and effectiveness are distinct claims.',
        'assertion_mode': 'asserted', 'inference_method': 'curatorial synthesis of public sources', 'claim_id': '', 'reviewed_by': 'Benjamin P Taylor',
        'reviewed_at': GENERATED, 'notes': notes, 'plain_phrase': phrase, 'public_review_label': 'supported working statement',
    }


EDGE_UPSERTS = [
    edge('e15_ing_authors_pattern_manual','publication_pattern_manual_service_systems_thinking','person_david_ing','authored_by','documentary','was authored by',['src_ing_pattern_manual_2016']),
    edge('e15_ing_maintains_coevolving','person_david_ing','corpus_coevolving_innovations','maintains','documentary','maintains',['src_ing_coevolving_publications_2026']),
    edge('e15_ing_develops_service_systems','person_david_ing','approach_family_service_systems_thinking','developed','human','developed',['src_ing_pattern_manual_2016','src_ing_coevolving_publications_2026']),
    edge('e15_ing_develops_systems_changes','person_david_ing','approach_family_systems_changes_learning','developed','human','developed',['src_ing_systems_changes_learning_2022']),
    edge('e15_systems_changes_documented_in','approach_family_systems_changes_learning','corpus_systems_changes','first_documented_in','documentary','is documented in',['src_ing_systems_changes_learning_2022']),
    edge('e15_pattern_manual_develops_service_systems','publication_pattern_manual_service_systems_thinking','approach_family_service_systems_thinking','develops','conceptual','develops',['src_ing_pattern_manual_2016']),
    edge('e15_ing_practises_lineage_documentation','person_david_ing','practice_systems_lineage_documentation','uses','practice','uses',['src_ing_coevolving_publications_2026','src_ing_knowing_better_2022']),
    edge('e15_coevolving_supports_lineage','practice_systems_lineage_documentation','corpus_coevolving_innovations','supported_by','practice','is supported by',['src_ing_coevolving_publications_2026']),
    edge('e15_systems_thinkers_supports_lineage','practice_systems_lineage_documentation','publication_systems_thinkers_ramage_shipp','supported_by','conceptual','is supported by',['src_systems_thinkers_springer']),
    edge('e15_steps_authored_bateson','publication_steps_to_ecology_of_mind','person_gregory_bateson','authored_by','documentary','was authored by',['src_bateson_steps_ecology_1972']),
    edge('e15_understanding_authored_vonfoerster','publication_understanding_understanding','person_heinz_von_foerster','authored_by','documentary','was authored by',['src_von_foerster_understanding_springer']),
    edge('e15_flawless_supports_intervention','intervention_skill_flawless_consulting','publication_flawless_consulting','supported_by','practice','is supported by',['src_block_flawless_wiley']),
    edge('e15_core_spine_systems_practice','practice_core_systems_practice_spine','practice_systems_practice','specialises','practice','provides a professional spine for',['src_skills_england_st0787_v12','src_scio_accreditation_current']),
    edge('e15_core_spine_systems_laws','practice_core_systems_practice_spine','knowledge_domain_systems_laws','uses','practice','uses',['src_skills_england_st0787_v12','src_scio_professional_development_current']),
    edge('e15_core_spine_csh','practice_core_systems_practice_spine','method_or_methodology_critical_systems_heuristics_csh','includes','classification','includes as a major approach',['src_skills_england_st0787_v12']),
    edge('e15_core_spine_ssm','practice_core_systems_practice_spine','method_or_methodology_soft_systems_methodology_ssm','includes','classification','includes as a major approach',['src_skills_england_st0787_v12']),
    edge('e15_core_spine_sd','practice_core_systems_practice_spine','method_or_methodology_system_dynamics','includes','classification','includes as a major approach',['src_skills_england_st0787_v12']),
    edge('e15_core_spine_vsm','practice_core_systems_practice_spine','method_or_methodology_viable_system_model_vsm','includes','classification','includes as a major approach',['src_skills_england_st0787_v12']),
    edge('e15_core_spine_multimethod','practice_core_systems_practice_spine','approach_family_multi_methodology_including_sosm','uses','practice','uses judgement about combining approaches',['src_scio_professional_development_current','src_skills_england_st0787_v12']),
]

JOURNEYS = [
    {
        'id': 'journey_david_ing_systems_in_plural', 'title': 'David Ing: systems in plural',
        'summary': 'Move through David Ing’s own systems work and the documentary practices that make systems lineages inspectable.',
        'audience': 'Readers interested in service systems, systems learning, change over time and how systems traditions are documented.', 'duration_minutes': 15,
        'steps': [
            {'node_id':'person_david_ing','heading':'Start with the practitioner-researcher','narrative':'Ing contributes his own systems work while also preserving unusually rich trails through systems communities and teaching.'},
            {'node_id':'corpus_coevolving_innovations','heading':'Use the public archive','narrative':'Coevolving records publications, courses, talks and collaborations over time.'},
            {'node_id':'approach_family_service_systems_thinking','heading':'Move into service systems','narrative':'Service systems thinking treats value and service as relational and contextual rather than as isolated outputs.'},
            {'node_id':'publication_pattern_manual_service_systems_thinking','heading':'See a method translated between domains','narrative':'The pattern-manual work changes the pattern form rather than simply importing a built-environment template.'},
            {'node_id':'corpus_systems_changes','heading':'Shift from systems change to systems changes','narrative':'Systems Changes Learning attends to temporality, rhythm, contexture and propensity in living systems.'},
            {'node_id':'approach_family_systems_changes_learning','heading':'Keep learning and action together','narrative':'The approach is organised as ongoing learning rather than a fixed-stage change programme.'},
            {'node_id':'practice_systems_lineage_documentation','heading':'Document lineages without inventing genealogies','narrative':'Events, citations and institutions can establish contact and context; influence needs stronger evidence.'},
            {'node_id':'publication_systems_thinkers_ramage_shipp','heading':'Compare another people-centred map','narrative':'Ramage and Shipp provide a different route through thinkers and traditions, useful for triangulating lineages.'},
        ],
    },
    {
        'id':'journey_core_systems_practice_reading','title':'Core systems practice: concepts, approaches, models and intervention',
        'summary':'A practice route through the competence spine behind professional systems work, with the four widely named approaches kept in relation rather than treated as rival brands.',
        'audience':'Practitioners, apprentices and readers trying to connect the reading list to actual systems practice.', 'duration_minutes':18,
        'steps': [
            {'node_id':'practice_core_systems_practice_spine','heading':'Start with practice, not a favourite method','narrative':'Systems practice joins concepts, judgement, modelling, engagement, intervention and learning.'},
            {'node_id':'knowledge_domain_systems_laws','heading':'Use concepts and laws as working constraints','narrative':'Feedback, variety, emergence, boundaries and related concepts inform method use without replacing situated judgement.'},
            {'node_id':'method_or_methodology_critical_systems_heuristics_csh','heading':'Interrogate boundaries and legitimacy','narrative':'CSH keeps boundary judgements, affected parties, expertise and legitimacy explicit.'},
            {'node_id':'method_or_methodology_soft_systems_methodology_ssm','heading':'Model purposeful activity and worldviews','narrative':'SSM organises inquiry into problematic situations without pretending the conceptual model is the real world.'},
            {'node_id':'method_or_methodology_system_dynamics','heading':'Model feedback, stocks, flows and delay','narrative':'System Dynamics makes dynamic hypotheses testable and forces attention to behaviour over time.'},
            {'node_id':'method_or_methodology_viable_system_model_vsm','heading':'Model viability and recursive organisation','narrative':'VSM asks how organisations handle variety, autonomy, cohesion, intelligence and policy across recursive levels.'},
            {'node_id':'approach_family_multi_methodology_including_sosm','heading':'Combine approaches deliberately','narrative':'Professional practice requires understanding strengths, limits and complementarities rather than method loyalty.'},
            {'node_id':'publication_systems_thinkers_ramage_shipp','heading':'Recover the histories behind the toolbox','narrative':'The reading list should reconnect methods to the thinkers, problems and traditions from which they emerged.'},
            {'node_id':'publication_steps_to_ecology_of_mind','heading':'Keep epistemology alive','narrative':'Bateson keeps relation, learning and the ecology of ideas in view.'},
            {'node_id':'publication_understanding_understanding','heading':'Put the observer back in','narrative':'Von Foerster makes reflexivity and responsibility unavoidable.'},
            {'node_id':'publication_flawless_consulting','heading':'Remember the intervention relationship','narrative':'Even good systems models fail when contracting, ownership and engagement fail.'},
        ],
    },
]

# Explicit matches from the current public reading list to canonical atlas entries.
READING_LIST_MAP = {
  38:'publication_grammar_of_systems_ii',39:'publication_opening_the_box',40:'publication_critical_systems_thinking_practitioners_guide',
  41:'publication_cst_management_complexity',42:'publication_essential_balances',43:'publication_systems_thinkers_ramage_shipp',
  44:'publication_systems_approaches_making_change',45:'publication_hidden_power_systems_thinking',46:'publication_mini_primer_critical_systems_heuristics',
  47:'method_or_methodology_patterns_of_strategy',48:'publication_systems_thinking_systems_practice',49:'publication_thinking_in_systems',
  50:'publication_dancing_with_systems',51:'publication_leverage_points_meadows',54:'practice_systems_convening',58:'publication_fractal_organisation_manual',
  69:'publication_organizational_systems_vsm',74:'publication_steps_to_ecology_of_mind',78:'publication_understanding_understanding',
  84:'publication_navigating_complexity_battram',98:'tradition_complex_responsive_processes',101:'publication_complexity_key_idea_business_society',
  103:'publication_managing_complexity_chaos_field_guide',104:'publication_new_dynamics_of_strategy',105:'publication_leaders_framework_decision_making',
  115:'publication_flawless_consulting',127:'method_or_methodology_organic_systems_framework',130:'publication_organic_systems_framework',
  137:'concept_double_loop_learning',140:'approach_family_systems_leadership',149:'organisation_scio_systems_and_complexity_in_organisation',
}


def upsert(rows: list[dict[str, Any]], incoming: list[dict[str, Any]], key: str) -> None:
    pos={row[key]:i for i,row in enumerate(rows)}
    for item in incoming:
        if item[key] in pos: rows[pos[item[key]]] = item
        else: pos[item[key]]=len(rows); rows.append(item)


def update_existing_profiles(data: dict[str, Any]) -> None:
    # Deepen the systems-practice profile without turning provider module packaging into a universal taxonomy.
    for p in data['profiles']:
        if p.get('node_id') == 'practice_systems_practice':
            p['summary'] = 'Situated inquiry and action using systems concepts, approaches, models and intervention judgement. Professional practice includes choosing and combining approaches, working with stakeholders and power, testing consequences, learning and reflecting on the practitioner’s own participation.'
            p['why_it_matters'] = 'Systems practice is wider than systems mapping and wider than any single methodology. The occupational standard and SCiO competence structure join systems concepts, multiple approaches, modelling, intervention, engagement and reflexive professional practice.'
            p['key_distinctions'] = enc(['practice versus tool use','model versus situation','method competence versus method loyalty','analysis versus intervention','first-order description versus reflexive participation'])
            s=set(json.loads(p.get('source_ids','[]'))); s.update(['src_skills_england_st0787_v12','src_scio_accreditation_current','src_scio_professional_development_current']); p['source_ids']=enc(sorted(s))
            p['last_researched']=GENERATED; p['reviewed_at']=GENERATED


def build_inventory(data: dict[str, Any]) -> dict[str, Any]:
    src=json.loads(INVENTORY_SOURCE.read_text(encoding='utf-8'))
    node_by_id={n['id']:n for n in data['nodes']}
    profile_ids={p.get('node_id') for p in data['profiles']}
    items=[]
    for item in src['items']:
        idx=item['source_paragraph']; nid=READING_LIST_MAP.get(idx)
        if nid and nid in node_by_id:
            status='developed_profile' if nid in profile_ids else 'represented'
            label=node_by_id[nid]['label']
        else:
            status='inventory_only'; label=''
        items.append({**item,'node_id':nid or '','canonical_label':label,'coverage_status':status})
    counts={k:sum(1 for i in items if i['coverage_status']==k) for k in ['developed_profile','represented','inventory_only']}
    return {**src,'release':RELEASE,'generated':GENERATED,'counts':counts,'item_count':len(items),'items':items,
            'coverage_note':'Every captured item is visible. Developed profile means the atlas has a sourced interpretive profile; represented means a canonical entry exists but remains thinner; inventory only means the item is recorded without pretending it has been critically developed.'}


def make_observations(data: dict[str, Any], inventory: dict[str, Any]) -> dict[str, Any]:
    metrics=graph_metrics(data); entries=metrics['public_entries']; profiles=metrics['developed_profiles']
    counts=inventory['counts']; ing_ids={n['id'] for n in data['nodes'] if 'release_0_15' in n.get('set_tags','') and ('ing' in n['id'] or n['id'] in {'corpus_coevolving_innovations','corpus_systems_changes','approach_family_service_systems_thinking','approach_family_systems_changes_learning','practice_systems_lineage_documentation','publication_pattern_manual_service_systems_thinking'})}
    observations=list(data.get('ai_observations',{}).get('observations',[]))
    # Remove prior release-specific versions of these if the build is repeated.
    ids={'reading_list_depth','ing_lineage_infrastructure','core_practice_not_four_tools','attention_is_not_importance'}
    observations=[o for o in observations if o.get('id') not in ids]
    observations.extend([
      {'id':'reading_list_depth','title':'Reading-list inventory and interpretive depth are different measures','kind':'coverage measurement plus epistemic caution','measurement':f"The captured reading list contains {inventory['item_count']} items: {counts['developed_profile']} map to developed profiles, {counts['represented']} are represented more thinly, and {counts['inventory_only']} remain inventory-only.",'interpretation':'A complete inventory is useful because it makes omissions measurable. It is not the same thing as having read, compared and critically developed every work.','implication':'Continue converting inventory-only items into sourced profiles by section and competence relevance, while keeping the maturity state visible.','test':'No public coverage claim should collapse inventory, description, developed profile and critical comparison into one percentage.'},
      {'id':'ing_lineage_infrastructure','title':'Lineage documentation is part of field infrastructure','kind':'source-structure interpretation','measurement':f"The David Ing pass adds {len(ing_ids)} developed entries spanning person, corpora, approaches, publication and documentary practice.",'interpretation':'A field is reproduced not only through canonical texts but through courses, conferences, collaborations, archives and remembered routes between them. Ing’s public record makes much of that infrastructure inspectable.','implication':'Treat documentary lineages as evidence objects with claim strength, not as decorative biographies.','test':'A lineage edge should say whether it records contact, citation, teaching, collaboration or stronger conceptual influence.'},
      {'id':'core_practice_not_four_tools','title':'Core systems practice is not four branded tools','kind':'competence-structure interpretation','measurement':'The professional spine connects systems concepts and laws, four widely named approaches (CSH, SSM, System Dynamics and VSM), multi-methodology, modelling, intervention, engagement and reflexive practice.','interpretation':'Method familiarity is necessary but insufficient. Practice lies partly in deciding what to model, whose boundaries matter, how approaches can be combined, and how action changes the situation and the practitioner.','implication':'Coverage of methods should be paired with cases, intervention skills and reflections on scope, power, ethics and learning.','test':'A reader following a method entry should be able to reach both its conceptual basis and its intervention consequences.'},
      {'id':'attention_is_not_importance','title':'Interface and source attention can manufacture apparent centrality','kind':'second-order observation','measurement':f"The atlas now has {entries} public entries and {profiles} developed profiles, so navigation and research depth still select a small fraction for prominent treatment.",'interpretation':'Prominence can arise because a source corpus is unusually accessible or recently researched. That is not the same as importance in the field.','implication':'Keep homepage routes plural, rotate research programmes and inspect source concentration before treating graph centrality as intellectual centrality.','test':'Changing the research corpus and interface defaults should not radically rewrite the apparent canon without an explicit change record.'},
    ])
    return {'release':RELEASE,'generated':GENERATED,'method':'Measurements are derived from the current public graph and reading-list inventory; interpretations, implications and proposed tests are explicitly separated.','metrics':graph_metrics(data),'observations':observations}


def write_ai_document(report: dict[str, Any]) -> None:
    lines=['# AI observations','',f"Generated for release `{report['release']}` on {report['generated']}.",'',report['method'],'']
    for o in report['observations']:
        lines += [f"## {o['title']}",'',f"**Kind:** {o['kind']}",'',f"**Measurement:** {o['measurement']}",'',f"**Interpretation:** {o['interpretation']}",'',f"**Implication:** {o['implication']}",'',f"**Test:** {o['test']}",'']
    (DOCUMENTATION/'ai-observations.md').write_text('\n'.join(lines).rstrip()+'\n',encoding='utf-8')


def write_reading_document(inventory: dict[str, Any]) -> None:
    c=inventory['counts']
    text=f'''# Reading-list coverage\n\nRelease `{RELEASE}` treats the public systems | complexity | cybernetics reading list as an item-level corpus rather than a single external link.\n\nCaptured items: **{inventory['item_count']}**. Developed profiles: **{c['developed_profile']}**. Represented more thinly: **{c['represented']}**. Inventory-only: **{c['inventory_only']}**.\n\nThe maturity labels matter. Inventory means the work is recorded in the curatorial list. It does not imply that its argument, evidence, reception or limitations have been researched. A developed profile is a sourced interpretive account. Critical comparison remains a further step.\n\nThe public reading-list page exposes every captured item, its section and its current atlas depth. This makes the remaining work inspectable rather than hiding it behind a claim of completeness.\n\n## Practice connection\n\nThe list explicitly points readers to SCiO professional practice and says core systems practice and intervention skills are both required. This release therefore connects reading-list depth to the professional systems-practice spine rather than treating books as a detached canon.\n'''
    (DOCUMENTATION/'reading-list-coverage.md').write_text(text,encoding='utf-8')


def write_core_practice_document() -> None:
    text=f'''# Core systems practice\n\nRelease `{RELEASE}` represents core systems practice as a connected competence spine, not as a fifth methodology.\n\nThe public Systems Thinking Practitioner occupational standard combines systems concepts and laws, multiple systems approaches, systems modelling, intervention and engagement, and reflexive participation. It explicitly names Critical Systems Heuristics, Soft Systems Methodology, System Dynamics and the Viable System Model among widely used approaches. SCiO professional material likewise treats method knowledge alongside intervention competence and professional judgement.\n\nThe atlas therefore gives direct routes through:\n\n- systems concepts and laws;\n- Critical Systems Heuristics;\n- Soft Systems Methodology;\n- System Dynamics;\n- the Viable System Model;\n- multi-methodology and method choice;\n- modelling, stakeholder engagement and intervention;\n- reflexive learning and professional development.\n\nProvider-specific workshop names and sequencing can change. The public atlas does not present one provider's internal timetable as the universal structure of the profession.\n'''
    (DOCUMENTATION/'core-systems-practice.md').write_text(text,encoding='utf-8')


def main() -> None:
    data=json.loads(DATA_PATH.read_text(encoding='utf-8'))
    stale_source_ids={'src_taylor_systems_reading_list_2024','src_bateson_steps_chicago'}
    data['sources']=[s for s in data['sources'] if s.get('id') not in stale_source_ids]
    upsert(data['sources'],SOURCE_UPSERTS,'id')
    upsert(data['nodes'],NODE_UPSERTS,'id')
    by_id={n['id']:n for n in data['nodes']}
    new_profiles=[profile(by_id[nid],spec) for nid,spec in PROFILE_SPECS.items()]
    upsert(data['profiles'],new_profiles,'node_id')
    upsert(data['edges'],EDGE_UPSERTS,'id')
    # Keep generated output stable from the first clean build.
    data['edges'].sort(key=lambda edge: edge.get('id', ''))
    upsert(data['journeys'],JOURNEYS,'id')
    update_existing_profiles(data)
    inventory=build_inventory(data)
    data['reading_list_inventory']=inventory
    data['reading_list_coverage']={'release':RELEASE,'status':'item_level_inventory_with_developed_subset_full_critical_audit_open','item_count':inventory['item_count'],'developed_profile_count':inventory['counts']['developed_profile'],'represented_count':inventory['counts']['represented'],'inventory_only_count':inventory['counts']['inventory_only'],'public_page':'reading-list.html'}
    data['core_systems_practice']={'release':RELEASE,'node_id':'practice_core_systems_practice_spine','major_approaches':['method_or_methodology_critical_systems_heuristics_csh','method_or_methodology_soft_systems_methodology_ssm','method_or_methodology_system_dynamics','method_or_methodology_viable_system_model_vsm'],'competence_sources':['src_skills_england_st0787_v12','src_scio_accreditation_current','src_scio_professional_development_current']}
    meta=data['meta']; meta.update({'release':RELEASE,'generated':GENERATED,'iteration_focus':'David Ing, item-level reading-list depth and the professional core systems-practice spine','reading_list_inventory_url':'https://antlerboy.github.io/the-necessary-tangle/reading-list.html','core_systems_practice_url':'https://github.com/antlerboy/the-necessary-tangle/blob/main/documentation/core-systems-practice.md'})
    # Recalculate simple release counts after upserts. refresh_graph_snapshot handles graph topology later.
    metrics=graph_metrics(data)
    meta['public_entry_count']=metrics['public_entries']; meta['described_entry_count']=metrics['public_entries']; meta['profile_count']=len(data['profiles']); meta['source_count']=len(data['sources']); meta['journey_count']=len(data['journeys']); meta['public_link_source_count']=sum(1 for s in data['sources'] if s.get('public_link_status')=='public_link')
    data['ai_observations']=make_observations(data,inventory)
    rendered=json.dumps(data,ensure_ascii=False,indent=2)+'\n'
    DATA_PATH.write_text(rendered,encoding='utf-8')
    (DOCS_ASSETS/'public-data.json').write_text(rendered,encoding='utf-8')
    (DOCS_ASSETS/'public-data.js').write_text('window.TANGLE_DATA = '+json.dumps(data,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8')
    (ROOT/'data'/'reading-list-inventory.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    write_ai_document(data['ai_observations']); write_reading_document(inventory); write_core_practice_document()
    print(f"Applied {RELEASE}: {meta['public_entry_count']} public entries, {meta['profile_count']} profiles, {inventory['item_count']} reading-list items")

if __name__=='__main__': main()
