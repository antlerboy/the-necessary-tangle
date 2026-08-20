#!/usr/bin/env python3
"""Apply release 0.17: public intake, serendipity, canon and lineage."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from apply_iteration_09 import graph_metrics
from apply_relational_depth_16 import calculate_relational_depth

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "public-data.json"
DOCS_ASSETS = ROOT / "docs" / "assets"
RELEASE = "0.17-public-intake-lineage-alpha"
GENERATED = "2026-08-19"
PUBLIC_URL = "https://transduction.systems/"


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


def upsert(rows: list[dict[str, Any]], incoming: list[dict[str, Any]], key: str) -> None:
    positions = {row.get(key): index for index, row in enumerate(rows) if row.get(key)}
    for item in incoming:
        identity = item[key]
        if identity in positions:
            rows[positions[identity]].update(item)
        else:
            positions[identity] = len(rows)
            rows.append(item)


def merge_encoded(record: dict[str, Any], key: str, values: list[str]) -> None:
    record[key] = enc(list(dict.fromkeys([*parse(record.get(key), []), *values])))


def find_node(data: dict[str, Any], label: str, fallback: str | None = None) -> str | None:
    wanted = label.casefold().strip()
    for node in data.get("nodes", []):
        if str(node.get("label", "")).casefold().strip() == wanted:
            return node.get("id")
        aliases = [str(item).casefold().strip() for item in parse(node.get("aliases"), [])]
        if wanted in aliases:
            return node.get("id")
    return fallback


def source_record(
    source_id: str,
    title: str,
    source_type: str,
    url: str,
    notes: str,
    creators: list[str],
    publisher: str,
    date: str = "",
    *,
    doi: str = "",
    isbn: str = "",
    quality: str = "A",
) -> dict[str, Any]:
    return {
        "id": source_id,
        "title": title,
        "source_type": source_type,
        "quality_tier": quality,
        "access": "public" if url else "bibliographic_only",
        "url": url,
        "date": date or f"checked {GENERATED}",
        "notes": notes,
        "creators": enc(creators),
        "doi": doi,
        "isbn": isbn,
        "publisher": publisher,
        "licence": "source terms unless otherwise stated",
        "archived_url": "",
        "content_hash": "",
        "review_status": "checked",
        "last_checked": GENERATED,
        "public_link_status": "public_link" if url else "no_public_link",
    }


def node_record(
    node_id: str,
    label: str,
    entity_type: str,
    description: str,
    source_ids: list[str],
    x: float,
    y: float,
    tags: list[str],
    *,
    aliases: list[str] | None = None,
    level: str = "profile",
) -> dict[str, Any]:
    return {
        "id": node_id,
        "label": label,
        "entity_type": entity_type,
        "description": description,
        "aliases": enc(aliases or []),
        "boundary_ring": "0",
        "inclusion_reason": "feedback_led_release_0_17",
        "status": "accepted",
        "source_ids": enc(source_ids),
        "set_tags": enc(["systems", "lineage", "release_0_17", *tags]),
        "espoused_labels": "[]",
        "observed_clusters": "[]",
        "canonical_definition": description,
        "valid_from": "",
        "valid_to": "",
        "external_ids": "{}",
        "geographies": "[]",
        "licence": "",
        "review_status": "curator_checked_public_sources",
        "reviewed_by": "Benjamin P Taylor",
        "reviewed_at": GENERATED,
        "x": x,
        "y": y,
        "canonical_id": node_id,
        "public_visibility": "public",
        "publication_level": level,
        "public_stub_text": "",
        "public_source_count": len(source_ids),
        "no_public_link_count": 0,
    }


def profile_record(
    node_id: str,
    summary: str,
    why: str,
    distinctions: list[str],
    lineage: list[str],
    antecedents: list[str],
    subsequents: list[str],
    practice: list[str],
    misreadings: list[str],
    checks: list[str],
    source_ids: list[str],
    *,
    context: str = "",
    editorial_note: str = "",
) -> dict[str, Any]:
    return {
        "node_id": node_id,
        "summary": summary,
        "canonical_definition": summary,
        "why_it_matters": why,
        "key_distinctions": enc(distinctions),
        "historical_lineage": enc(lineage),
        "logical_antecedents": enc(antecedents),
        "dependent_subsequents": enc(subsequents),
        "practice_connections": enc(practice),
        "common_misreadings": enc(misreadings),
        "open_checks": enc(checks),
        "source_ids": enc(source_ids),
        "context_and_lineage": context,
        "editorial_note": editorial_note,
        "last_researched": GENERATED,
    }


def relation_record(
    relation_type: str,
    family: str,
    inverse: str,
    minimum_evidence: str,
    phrase: str,
    *,
    directed: str = "true",
) -> dict[str, str]:
    return {
        "relation_type": relation_type,
        "relation_family": family,
        "directed": directed,
        "inverse": inverse,
        "minimum_evidence": minimum_evidence,
        "strict_dependency": "no",
        "plain_phrase": phrase,
    }


def edge_record(
    edge_id: str,
    source: str,
    target: str,
    relation_type: str,
    family: str,
    phrase: str,
    source_ids: list[str],
    locator: str,
    scope: str,
    *,
    status: str = "accepted",
    mode: str = "asserted",
    confidence: str = "0.94",
    review_label: str = "source-backed statement",
) -> dict[str, Any]:
    return {
        "id": edge_id,
        "source": source,
        "target": target,
        "relation_type": relation_type,
        "relation_family": family,
        "directed": "true",
        "dependency_kind": "",
        "confidence": confidence,
        "claim_status": status,
        "source_ids": enc(source_ids),
        "evidence_ids": "[]",
        "source_locator": locator,
        "valid_from": "",
        "valid_to": "",
        "scope_conditions": scope,
        "assertion_mode": mode,
        "inference_method": "" if mode == "asserted" else "curatorial comparison of the cited public sources",
        "claim_id": "",
        "reviewed_by": "Benjamin P Taylor" if status == "accepted" else "",
        "reviewed_at": GENERATED if status == "accepted" else "",
        "notes": "",
        "plain_phrase": phrase,
        "public_review_label": review_label,
    }


SOURCES = [
    source_record(
        "src_ou_magnus_ramage_profile_2026",
        "Dr Magnus Ramage — Open University profile",
        "official_institutional_profile",
        "https://profiles.open.ac.uk/magnus-ramage",
        "Official profile establishing Ramage's Open University role and his research on systems history, information, decolonial and critical approaches, and systems thinking from the margins. It is a primary institutional record, not independent evaluation.",
        ["The Open University", "Magnus Ramage"],
        "The Open University",
        "checked 2026-08-19",
    ),
    source_record(
        "src_springer_systems_thinkers_2ed_2020",
        "Systems Thinkers, second edition",
        "publisher_record",
        "https://link.springer.com/book/10.1007/978-1-4471-7475-2",
        "Springer record for the 2020 second edition, its thirty biographical chapters, authorship, scope and bibliographic metadata.",
        ["Magnus Ramage", "Karen Shipp"],
        "Springer London",
        "2020",
        doi="10.1007/978-1-4471-7475-2",
        isbn="978-1-4471-7475-2",
    ),
    source_record(
        "src_oro_systems_thinkers_2020",
        "Systems Thinkers (2nd edition) — Open Research Online",
        "official_institutional_repository_record",
        "https://oro.open.ac.uk/69810/",
        "Open University repository record describing the book as a biographical history of systems thinking which connects lives, ideas and practice.",
        ["Magnus Ramage", "Karen Shipp"],
        "The Open University",
        "2020",
        doi="10.1007/978-1-4471-7475-2",
    ),
    source_record(
        "src_oro_boundaries_disciplines_2006",
        "On boundaries and disciplines: constructing a set of key systems thinkers",
        "institutional_repository_article_record",
        "https://oro.open.ac.uk/5446/",
        "Open University repository record for Ramage and Shipp's article on the choices and boundary questions involved in constructing a set of key systems thinkers.",
        ["Magnus Ramage", "Karen Shipp"],
        "The Systemist / The Open University",
        "2006",
    ),
    source_record(
        "src_hull_centre_systems_studies_2026",
        "Centre for Systems Studies",
        "official_institutional_page",
        "https://www.hull.ac.uk/research/centres/centre-for-systems-studies",
        "University of Hull page for the Centre for Systems Studies and its continuing systems-thinking mission and practice programme.",
        ["University of Hull"],
        "University of Hull",
        "checked 2026-08-19",
    ),
    source_record(
        "src_ou_mike_jackson_cst_2022",
        "Critical Systems Thinking and Practice: what has been done and what needs doing",
        "official_institutional_event_record",
        "https://university.open.ac.uk/stem/engineering-and-innovation/news/22nd-june-third-50th-birthday-celebrations-systems-teaching-ou",
        "Open University account of Michael C. Jackson's role in developing the critical systems thinking and practice research programme at Hull, including its relation to the wider UK systems field.",
        ["The Open University", "Michael C. Jackson"],
        "The Open University",
        "2022",
    ),
    source_record(
        "src_freeman_tyranny_structurelessness",
        "The Tyranny of Structurelessness",
        "primary_author_text",
        "https://www.jofreeman.com/joreen/tyranny.htm",
        "Jo Freeman's author-hosted text arguing that groups cannot abolish structure, only leave it implicit, and that invisible structure can conceal unaccountable power.",
        ["Jo Freeman"],
        "Jo Freeman",
        "1970-1973",
    ),
    source_record(
        "src_oup_fricker_epistemic_injustice_2007",
        "Epistemic Injustice: Power and the Ethics of Knowing",
        "publisher_record",
        "https://academic.oup.com/book/32817",
        "Oxford Academic record for Miranda Fricker's account of testimonial and hermeneutical injustice and the relation between knowing, prejudice and social power.",
        ["Miranda Fricker"],
        "Oxford University Press",
        "2007",
        doi="10.1093/acprof:oso/9780198237907.001.0001",
        isbn="9780198237907",
    ),
    source_record(
        "src_tangle_issue2_canon_feedback_2026",
        "The Necessary Tangle running feedback: canon, closure and patriarchy",
        "public_curator_discussion",
        "https://github.com/antlerboy/the-necessary-tangle/issues/2#issuecomment-5345119282",
        "Public curator note recording the challenge about a predominantly white male visual canon and the resulting editorial requirement to expose canonisation, exclusion, appropriation and recovery rather than repair the map through portraits alone.",
        ["Benjamin P Taylor", "Ida Rose Florez"],
        "The Necessary Tangle",
        "2026-08",
        quality="B",
    ),
    source_record(
        "src_tangle_issue21_viability_submission_2026",
        "Viability — consider adding viability vs fitness",
        "public_contribution_issue",
        "https://github.com/antlerboy/the-necessary-tangle/issues/21",
        "The first structured website submission. It originated the request to distinguish viability, fitness and natural drift; the published content was subsequently checked against independent sources.",
        ["Ivo Velitchkov"],
        "The Necessary Tangle",
        "2026-08-10",
        quality="B",
    ),
]


def main() -> None:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    upsert(data.setdefault("sources", []), SOURCES, "id")

    open_university_id = find_node(data, "The Open University", "organisation_the_open_university")
    hull_centre_id = find_node(data, "Centre for Systems Studies", "organisation_centre_for_systems_studies_hull")
    critical_id = (
        find_node(data, "Critical systems thinking")
        or find_node(data, "Critical Systems Thinking")
        or "tradition_critical_systems_thinking"
    )
    lineage_doc_id = find_node(data, "Systems lineage documentation", "practice_systems_lineage_documentation")

    new_nodes = [
        node_record(
            "person_magnus_ramage", "Magnus Ramage", "person",
            "An Open University systems scholar and educator whose work connects the history of systems thinking, sociotechnical information systems, critical and decolonial approaches, and the construction of systems canons.",
            ["src_ou_magnus_ramage_profile_2026", "src_springer_systems_thinkers_2ed_2020", "src_oro_boundaries_disciplines_2006"],
            -0.06, 0.37, ["systems-history", "critical-systems", "open-university"], aliases=["Dr Magnus Ramage"],
        ),
        node_record(
            "person_karen_shipp", "Karen Shipp", "person",
            "An educator and facilitator who developed interactive systems learning at The Open University and co-authored Systems Thinkers, connecting biographies, ideas, practice and the problem of selecting a systems canon.",
            ["src_springer_systems_thinkers_2ed_2020", "src_oro_systems_thinkers_2020", "src_oro_boundaries_disciplines_2006"],
            -0.01, 0.41, ["systems-history", "education", "open-university"],
        ),
        node_record(
            "concept_canon_formation", "Canon formation", "concept",
            "The social and editorial processes through which some people, works and traditions become the recognised centre of a field while others become marginal, derivative, invisible or difficult to retrieve.",
            ["src_oro_boundaries_disciplines_2006", "src_tangle_issue2_canon_feedback_2026"],
            0.07, 0.45, ["canon", "power", "lineage"],
        ),
        node_record(
            "concept_epistemic_closure", "Epistemic closure", "concept",
            "The operational closure by which a knowledge system distinguishes admissible questions, evidence, categories and knowers. Closure is necessary for coherence, but becomes dangerous when those affected cannot perturb or revise its distinctions.",
            ["src_tangle_issue2_canon_feedback_2026", "src_oup_fricker_epistemic_injustice_2007"],
            0.13, 0.46, ["epistemology", "boundaries", "power"],
        ),
        node_record(
            "concept_epistemic_injustice", "Epistemic injustice", "concept",
            "Wrong done to someone in their capacity as a knower, including credibility being unfairly reduced and gaps in shared interpretive resources that prevent experience being made intelligible.",
            ["src_oup_fricker_epistemic_injustice_2007"],
            0.18, 0.43, ["epistemology", "justice", "power"],
        ),
        node_record(
            "concept_epistemic_exclusion", "Epistemic exclusion", "concept",
            "Exclusion from shaping, contributing to or being recognised within a knowledge practice. It may operate through credibility, categories, access, institutional position, citation, language or the prior definition of what counts as evidence.",
            ["src_oup_fricker_epistemic_injustice_2007", "src_tangle_issue2_canon_feedback_2026"],
            0.23, 0.46, ["epistemology", "exclusion", "canon"],
        ),
        node_record(
            "practice_lineage_recovery", "Lineage recovery", "practice",
            "The evidence-led practice of recovering neglected people, traditions, institutions and transmissions while stating whether the relation is authorship, teaching, collaboration, appropriation, exclusion, canonisation or later rediscovery.",
            ["src_tangle_issue2_canon_feedback_2026", "src_oro_boundaries_disciplines_2006"],
            0.27, 0.40, ["lineage", "recovery", "evidence"],
        ),
        node_record(
            "concept_structurelessness", "Structurelessness", "concept",
            "The claim or aspiration that a group can operate without structure. Freeman's critique is that structure persists informally, often making power less visible and less accountable rather than removing it.",
            ["src_freeman_tyranny_structurelessness"],
            0.31, 0.34, ["organisation", "power", "feminist-practice"],
        ),
        node_record(
            "publication_tyranny_of_structurelessness", "The Tyranny of Structurelessness", "publication",
            "Jo Freeman's feminist organising essay on the impossibility of structurelessness and the way informal structures can conceal elites, access rules and unaccountable power.",
            ["src_freeman_tyranny_structurelessness"],
            0.36, 0.35, ["publication", "feminist-practice", "power"],
        ),
        node_record(
            "publication_epistemic_injustice", "Epistemic Injustice: Power and the Ethics of Knowing", "publication",
            "Miranda Fricker's account of testimonial and hermeneutical injustice, connecting social power to whose testimony is credited and whose experience can be made intelligible.",
            ["src_oup_fricker_epistemic_injustice_2007"],
            0.29, 0.48, ["publication", "epistemology", "justice"],
        ),
        node_record(
            "person_jo_freeman", "Jo Freeman", "person",
            "A feminist scholar, organiser and author whose critique of structurelessness shows how the denial of formal structure may leave informal power unexamined.",
            ["src_freeman_tyranny_structurelessness"],
            0.41, 0.37, ["feminist-practice", "organisation"], level="described",
        ),
        node_record(
            "person_miranda_fricker", "Miranda Fricker", "person",
            "A philosopher whose work on epistemic injustice examines the ethical and political wrongs that arise within practices of testimony, interpretation and knowing.",
            ["src_oup_fricker_epistemic_injustice_2007"],
            0.34, 0.50, ["epistemology", "justice"], level="described",
        ),
        node_record(
            "concept_decolonial_systems_thinking", "Decolonial systems thinking", "concept",
            "Work which examines how colonial histories, institutions, categories and knowledge hierarchies shape systems practice, and seeks forms of inquiry in which marginalised standpoints can alter the boundary and the account of the system.",
            ["src_ou_magnus_ramage_profile_2026", "src_tangle_issue2_canon_feedback_2026"],
            0.03, 0.49, ["decolonial", "critical-systems", "power"],
        ),
    ]

    if not find_node(data, "The Open University"):
        new_nodes.append(node_record(
            open_university_id, "The Open University", "organisation",
            "A UK distance-learning university with a long history of systems teaching, systems scholarship and practice-based systems education.",
            ["src_ou_magnus_ramage_profile_2026", "src_oro_systems_thinkers_2020"],
            -0.12, 0.44, ["institution", "education"], level="described",
        ))
    if not find_node(data, "Centre for Systems Studies"):
        new_nodes.append(node_record(
            hull_centre_id, "Centre for Systems Studies", "organisation",
            "The University of Hull centre associated with the development, dissemination and application of systems thinking, including the critical systems thinking and practice programme.",
            ["src_hull_centre_systems_studies_2026", "src_ou_mike_jackson_cst_2022"],
            0.14, 0.28, ["institution", "critical-systems"], level="described",
        ))
    if not find_node(data, "Critical systems thinking") and not find_node(data, "Critical Systems Thinking"):
        new_nodes.append(node_record(
            critical_id, "Critical systems thinking", "tradition",
            "A tradition associated particularly with Michael C. Jackson and colleagues which treats methodological pluralism, power, emancipation and critical reflection as central to systems inquiry and practice.",
            ["src_scio_critical_systems_thinking_2024", "src_ou_mike_jackson_cst_2022"],
            0.12, 0.34, ["critical-systems", "methodological-pluralism"],
        ))

    upsert(data.setdefault("nodes", []), new_nodes, "id")
    node_by_id = {node["id"]: node for node in data["nodes"]}

    systems_thinkers_id = find_node(data, "Systems Thinkers", "publication_systems_thinkers_ramage_shipp")
    jackson_id = find_node(data, "Michael C. Jackson", "person_michael_c_jackson")
    for node_id, description, source_ids, tags in [
        (
            systems_thinkers_id,
            "Magnus Ramage and Karen Shipp's biographical history of thirty systems thinkers. It links lives, ideas and practice while making visible that any such selection constructs a boundary and a provisional canon rather than discovering a final list.",
            ["src_springer_systems_thinkers_2ed_2020", "src_oro_systems_thinkers_2020", "src_oro_boundaries_disciplines_2006"],
            ["canon", "systems-history", "open-university"],
        ),
        (
            jackson_id,
            "A systems scholar and practitioner central to the development of critical systems thinking, creative holism and critical systems practice, including the purposeful selection and combination of methods under conditions of complexity, pluralism and power.",
            ["src_scio_critical_systems_thinking_2024", "src_ou_mike_jackson_cst_2022", "src_hull_centre_systems_studies_2026"],
            ["critical-systems", "methodological-pluralism", "hull"],
        ),
    ]:
        if node_id and node_id in node_by_id:
            node_by_id[node_id]["description"] = description
            node_by_id[node_id]["canonical_definition"] = description
            merge_encoded(node_by_id[node_id], "source_ids", source_ids)
            merge_encoded(node_by_id[node_id], "set_tags", ["release_0_17", *tags])
            node_by_id[node_id]["publication_level"] = "profile"
            node_by_id[node_id]["reviewed_at"] = GENERATED
            node_by_id[node_id]["public_source_count"] = len(parse(node_by_id[node_id].get("source_ids"), []))

    profiles = [
        profile_record(
            "person_magnus_ramage",
            "Ramage connects systems history, sociotechnical information systems, critical inquiry and the active problem of who is allowed to count as a systems thinker.",
            "His work makes canon construction part of systems practice rather than treating a list of recognised figures as neutral inheritance.",
            ["biographical history versus a final canon", "documented selection versus natural category", "critical and decolonial inquiry versus adding decorative diversity", "sociotechnical systems versus technology-only explanation"],
            ["The Open University Systems Group", "systems thinking education", "sociotechnical information systems", "critical and decolonial curriculum work"],
            ["systems history", "boundary critique", "sociotechnical systems", "critical systems thinking"],
            ["Systems Thinkers", "systems thinking from the margins", "decolonial systems education"],
            ["systems education", "canon review", "critical technology inquiry", "curriculum design"],
            ["Treating Systems Thinkers as an objective ranking misses the authors' own boundary questions.", "Treating decolonisation as demographic decoration leaves the knowledge rules unchanged."],
            ["Add published outputs from the systems-thinking-from-the-margins work when available.", "Trace the Open University teaching lineage in more detail."],
            ["src_ou_magnus_ramage_profile_2026", "src_springer_systems_thinkers_2ed_2020", "src_oro_boundaries_disciplines_2006"],
            context="Institutional and intellectual context: The Open University; systems history; sociotechnical information systems; critical and decolonial approaches. No ethnicity is inferred or assigned.",
            editorial_note="The profile records publicly stated intellectual and institutional context. Heritage and identity are included only where self-described, publicly sourced and relevant to the work.",
        ),
        profile_record(
            "person_karen_shipp",
            "Shipp brought long experience of interactive and transformative systems education into the Systems Thinkers project and its people-centred account of the field.",
            "Her role prevents the book being treated as Ramage's individual classification exercise and connects canon construction to actual teaching practice at The Open University.",
            ["co-authorship versus supporting role", "education and facilitation versus abstract history", "life-and-practice account versus disembodied ideas"],
            ["The Open University Systems Group", "interactive systems education", "facilitation", "Systems Thinkers project"],
            ["systems education", "biographical inquiry", "facilitation"],
            ["Systems Thinkers", "people-centred systems history"],
            ["learning design", "facilitation", "systems-history teaching"],
            ["Reducing Shipp to a secondary co-author repeats the visibility problem the canon review is intended to expose."],
            ["Locate further public records of Shipp's systems teaching and facilitation work."],
            ["src_springer_systems_thinkers_2ed_2020", "src_oro_systems_thinkers_2020", "src_oro_boundaries_disciplines_2006"],
            context="Institutional and intellectual context: The Open University Systems Group; interactive and transformative learning; facilitation. No personal heritage is inferred.",
        ),
        profile_record(
            systems_thinkers_id,
            "A biographical history of thirty systems thinkers which relates lives, ideas, institutions and practice while providing a visible, challengeable selection of the field.",
            "The book is both an unusually useful map and an example of canon formation. Its authors explicitly examined the disciplinary and boundary choices involved in selecting key systems thinkers.",
            ["biographical history versus timeless taxonomy", "thirty selected thinkers versus an exhaustive field", "life and practice versus ideas alone", "selection evidence versus later canonisation"],
            ["Open University systems teaching", "early cybernetics", "general systems theory", "systems practice and critical systems"],
            ["systems traditions", "biographical method", "boundary choice"],
            ["systems-history teaching", "canon review", "lineage recovery"],
            ["reading routes", "teaching history", "comparison of traditions", "challenging omissions"],
            ["The book is not a final ranking of the field.", "The presence of a thinker is not evidence that every later practitioner was influenced by them."],
            ["Map all thirty chapters and their source extracts.", "Compare the 2009 and 2020 selections and revisions.", "Record serious omissions and rival canons as evidence, not as a corrected master list."],
            ["src_springer_systems_thinkers_2ed_2020", "src_oro_systems_thinkers_2020", "src_oro_boundaries_disciplines_2006"],
            editorial_note="The book's selection is represented as a documented and useful canon-making act, not as the natural boundary of systems thinking.",
        ),
        profile_record(
            jackson_id,
            "Jackson's critical systems programme treats the diversity of systems approaches as a resource to be selected and combined critically rather than a contest to identify one universally correct method.",
            "It provides a central route from philosophy and methodological pluralism into practical intervention, while keeping power, interests and emancipation discussable.",
            ["critical pluralism versus method relativism", "creative holism versus indiscriminate method mixing", "complexity and pluralism versus one-dimensional diagnosis", "method selection versus brand loyalty"],
            ["Hull Centre for Systems Studies", "UK systems movement", "critical systems thinking", "critical systems practice"],
            ["systems methodologies", "critical theory", "methodological pluralism", "power and emancipation"],
            ["critical systems practice", "creative holism", "multimethodology"],
            ["method selection", "multimethod intervention", "critical reflection", "complex organisational inquiry"],
            ["Critical systems thinking is not merely a catalogue of methods.", "Pluralism does not mean every method or combination is equally warranted."],
            ["Add page-level links between Jackson's frameworks, individual methodologies and documented applications.", "Develop criticism of the programme from within and outside critical systems traditions."],
            ["src_scio_critical_systems_thinking_2024", "src_ou_mike_jackson_cst_2022", "src_hull_centre_systems_studies_2026"],
            context="Institutional and intellectual context: the Hull critical systems programme and the wider UK systems movement. This is an intellectual lineage, not an inferred personal identity.",
        ),
        profile_record(
            "concept_canon_formation",
            "Canon formation is the production of a recognised centre and periphery in a field through selection, teaching, citation, institutional power and repetition.",
            "The atlas cannot criticise other maps for false neutrality while leaving its own visibility choices implicit.",
            ["canon versus exhaustive field", "visibility versus intellectual value", "citation versus influence", "recovery versus decorative inclusion"],
            ["historiography", "disciplinary boundary making", "curriculum and anthology construction"],
            ["selection", "institutional authority", "publication and teaching"],
            ["epistemic exclusion", "lineage recovery", "rival genealogies"],
            ["coverage audits", "source comparison", "teaching-history research", "public challenge"],
            ["A canon is not simply a list of the objectively best people.", "Replacing one closed list with another does not remove boundary choices."],
            ["Add explicit cases of exclusion, appropriation, canonisation and recovery only where public evidence supports the precise relation."],
            ["src_oro_boundaries_disciplines_2006", "src_tangle_issue2_canon_feedback_2026"],
        ),
        profile_record(
            "concept_epistemic_closure",
            "Knowledge practices need closure enough to distinguish signal from noise, but closure also determines which people, experiences and perturbations can change the account.",
            "The relevant question is not whether a system is open or closed in the abstract, but who can affect its boundary and whether it can revise the categories through which it learns.",
            ["operational closure versus social exclusion", "coherence versus impermeability", "openness versus accountability", "perturbation versus token consultation"],
            ["cybernetic epistemology", "boundary critique", "social epistemology"],
            ["distinction", "observer", "boundary", "criteria of admissibility"],
            ["epistemic exclusion", "learning failure", "canon rigidity"],
            ["boundary review", "participatory inquiry", "evidence policy"],
            ["Closure is not inherently patriarchal or oppressive.", "Indiscriminate openness does not abolish informal power."],
            ["Develop historical cases linking particular systems of closure to patriarchal, colonial or professional power without making closure itself the cause."],
            ["src_tangle_issue2_canon_feedback_2026", "src_oup_fricker_epistemic_injustice_2007", "src_freeman_tyranny_structurelessness"],
        ),
        profile_record(
            "concept_epistemic_injustice",
            "Epistemic injustice names wrongs within knowing: prejudice can reduce a person's credibility, and unequal interpretive resources can prevent experience becoming intelligible.",
            "It gives the atlas a sharper way to examine whose evidence is admitted and which absences are produced by the field's own categories.",
            ["testimonial injustice", "hermeneutical injustice", "ignorance versus structured absence", "representation versus authority to know"],
            ["social epistemology", "virtue epistemology", "feminist philosophy"],
            ["testimony", "interpretive resources", "social power"],
            ["epistemic exclusion", "corrective epistemic practices"],
            ["participation design", "source policy", "canon review"],
            ["Adding more speakers does not by itself change credibility rules or interpretive resources."],
            ["Connect to standpoint, situated knowledge and decolonial epistemologies through primary sources."],
            ["src_oup_fricker_epistemic_injustice_2007"],
        ),
        profile_record(
            "practice_lineage_recovery",
            "Lineage recovery finds and types neglected transmissions without turning every resemblance, shared identity or later citation into influence.",
            "It makes the history of visibility part of the atlas rather than treating omissions as empty space around an otherwise neutral canon.",
            ["recovery versus retrospective invention", "appropriation versus influence", "teaching versus citation", "identity context versus identity inference"],
            ["archival research", "feminist and decolonial historiography", "systems lineage documentation"],
            ["typed relations", "public evidence", "boundary critique"],
            ["revised canons", "rival genealogies", "documented exclusions"],
            ["archive work", "oral history", "citation tracing", "curriculum review"],
            ["Recovery is not achieved by adding portraits to an unchanged structure.", "Shared heritage is not evidence of conceptual influence."],
            ["Develop gold-standard examples of exclusion, appropriation, canonisation and recovery with page-level evidence."],
            ["src_tangle_issue2_canon_feedback_2026", "src_oro_boundaries_disciplines_2006"],
        ),
        profile_record(
            "concept_structurelessness",
            "Structurelessness is an impossible organisational condition when people continue to interact; the practical choice is whether structure and authority are explicit, revisable and accountable.",
            "It prevents the response to closed canons becoming a fantasy that removing all boundaries will remove power.",
            ["formal versus informal structure", "openness versus hidden elite", "authority versus accountability"],
            ["women's liberation organising", "feminist organisational critique"],
            ["interaction", "informal networks", "resource and information asymmetry"],
            ["explicit governance", "accountable participation"],
            ["group design", "participation policy", "systems convening"],
            ["Formal structure is not the only source of domination.", "A boundary can enable participation when its rules are visible and revisable."],
            ["Connect the argument to contemporary decentralised and networked organising through strong sources."],
            ["src_freeman_tyranny_structurelessness"],
        ),
        profile_record(
            "concept_decolonial_systems_thinking",
            "Decolonial systems thinking asks how colonial histories and knowledge hierarchies shape the system, observer, method and canon, and whether marginalised standpoints can alter those terms.",
            "It shifts inclusion from demographic display to the construction of knowledge, institutional authority and the right to redefine the problem.",
            ["decolonisation versus diversification", "standpoint versus demographic proxy", "historical power versus abstract plurality"],
            ["decolonial thought", "critical systems thinking", "systems thinking from the margins"],
            ["colonial history", "epistemic power", "boundary critique"],
            ["revised systems education", "lineage recovery", "alternative genealogies"],
            ["curriculum review", "participatory boundary critique", "source and canon audits"],
            ["Decolonial systems thinking is not a label for any systems work done outside Europe or North America.", "Personal identity alone does not establish a decolonial argument."],
            ["Add primary published work from practitioners and scholars who explicitly identify their work as decolonial systems thinking."],
            ["src_ou_magnus_ramage_profile_2026", "src_tangle_issue2_canon_feedback_2026"],
        ),
    ]
    upsert(data.setdefault("profiles", []), profiles, "node_id")

    relation_types = [
        relation_record("researches", "practice", "is_researched_by", "An official profile, publication record or equivalent source naming the research area.", "researches"),
        relation_record("participates_in_canon_formation", "historical", "is_shaped_as_a_canon_by", "A source showing deliberate selection, curriculum, anthology or recognised boundary construction.", "participates in forming a canon through"),
        relation_record("can_exclude", "contestation", "can_be_excluded_by", "A precise argument or documented case; not demographic inference.", "can exclude through"),
        relation_record("recovers", "human", "is_recovered_by", "Archival, bibliographic, oral-history or institutional evidence of earlier participation and later neglect or recovery.", "recovers"),
        relation_record("appropriated_from", "influence", "was_appropriated_into", "Direct evidence of taking, translation or reuse, including the asymmetry and source context.", "was appropriated from"),
        relation_record("excluded_from_canon", "contestation", "canon_excluded", "Evidence that a person, work or tradition was omitted, discounted or made unavailable by a particular canon-making practice.", "was excluded from a canon by"),
        relation_record("canonised_as", "historical", "was_canonised_by", "Documented repeated selection or institutional recognition sufficient to support the precise wording.", "canonised as"),
        relation_record("responds_to", "practice", "is_addressed_by", "A source or explicit, reviewable curatorial account of the problem a practice addresses.", "responds to"),
    ]
    upsert(data.setdefault("relation_types", []), relation_types, "relation_type")

    existing_relations = {item.get("relation_type") for item in data["relation_types"]}
    def relation(name: str, family: str, inverse: str, evidence: str, phrase: str) -> None:
        if name not in existing_relations:
            data["relation_types"].append(relation_record(name, family, inverse, evidence, phrase))
            existing_relations.add(name)
    relation("authored", "documentary", "authored_by", "A publication record or the work itself.", "authored")
    relation("develops", "conceptual", "developed_by", "A primary source which explicitly develops the stated concept or approach.", "develops")
    relation("critiques", "contestation", "is_criticised_by", "A primary or scholarly source containing the critique.", "critiques")
    relation("associated_with", "human", "associated_with", "An official institutional or biographical record.", "is institutionally associated with")

    critical_id = find_node(data, "Critical systems thinking", critical_id)
    edges = [
        edge_record("e17_ramage_authored_systems_thinkers", "person_magnus_ramage", systems_thinkers_id, "authored", "documentary", "co-authored", ["src_springer_systems_thinkers_2ed_2020", "src_oro_systems_thinkers_2020"], "Springer authors and Open University repository record", "Authorship only; it does not establish that every selection or interpretation in the book is uncontested."),
        edge_record("e17_shipp_authored_systems_thinkers", "person_karen_shipp", systems_thinkers_id, "authored", "documentary", "co-authored", ["src_springer_systems_thinkers_2ed_2020", "src_oro_systems_thinkers_2020"], "Springer authors and Open University repository record", "Authorship only; it does not establish that every selection or interpretation in the book is uncontested."),
        edge_record("e17_systems_thinkers_canon", systems_thinkers_id, "concept_canon_formation", "participates_in_canon_formation", "historical", "makes a documented selection of key systems thinkers and therefore participates in forming a canon through", ["src_oro_boundaries_disciplines_2006", "src_springer_systems_thinkers_2ed_2020"], "2006 article title and abstract; second-edition scope and contents", "This does not dismiss the book as arbitrary. It states that a useful selection remains a selection with boundaries.", mode="interpreted", review_label="source-backed curatorial interpretation"),
        edge_record("e17_ramage_researches_decolonial", "person_magnus_ramage", "concept_decolonial_systems_thinking", "researches", "practice", "researches critical and decolonial approaches to", ["src_ou_magnus_ramage_profile_2026"], "Open University profile, research and scholarship interests", "The profile states a research interest and work in progress; it does not establish a completed decolonial systems doctrine."),
        edge_record("e17_ramage_open_university", "person_magnus_ramage", open_university_id, "associated_with", "human", "teaches and researches at", ["src_ou_magnus_ramage_profile_2026"], "Open University official profile", "Current institutional affiliation as checked on the generated date."),
        edge_record("e17_shipp_open_university", "person_karen_shipp", open_university_id, "associated_with", "human", "developed systems learning at", ["src_springer_systems_thinkers_2ed_2020"], "Springer author biography", "Historical institutional association described by the publisher record."),
        edge_record("e17_jackson_develops_cst", jackson_id, critical_id, "develops", "conceptual", "is a central developer of", ["src_ou_mike_jackson_cst_2022", "src_scio_critical_systems_thinking_2024"], "Open University event account and SCiO publication record", "This states a central documented role, not sole authorship of the whole critical systems tradition."),
        edge_record("e17_jackson_hull_centre", jackson_id, hull_centre_id, "associated_with", "human", "developed and practised systems work through", ["src_hull_centre_systems_studies_2026", "src_ou_mike_jackson_cst_2022"], "University of Hull centre page and Open University event account", "Institutional association and programme history only."),
        edge_record("e17_fricker_authored_epistemic_injustice", "person_miranda_fricker", "publication_epistemic_injustice", "authored", "documentary", "authored", ["src_oup_fricker_epistemic_injustice_2007"], "Oxford Academic publication record", "Bibliographic authorship."),
        edge_record("e17_book_develops_epistemic_injustice", "publication_epistemic_injustice", "concept_epistemic_injustice", "develops", "conceptual", "develops the distinction of", ["src_oup_fricker_epistemic_injustice_2007"], "Oxford Academic abstract and contents", "Uses the book's own conceptual vocabulary."),
        edge_record("e17_freeman_authored_tyranny", "person_jo_freeman", "publication_tyranny_of_structurelessness", "authored", "documentary", "authored", ["src_freeman_tyranny_structurelessness"], "Author-hosted text and publication history", "Bibliographic authorship."),
        edge_record("e17_tyranny_critiques_structurelessness", "publication_tyranny_of_structurelessness", "concept_structurelessness", "critiques", "contestation", "critiques the organisational claim of", ["src_freeman_tyranny_structurelessness"], "Author-hosted text, formal and informal structures section", "The critique arose from feminist movement organising and should not be detached from that setting."),
        edge_record("e17_closure_can_exclude", "concept_epistemic_closure", "concept_epistemic_exclusion", "can_exclude", "contestation", "can produce", ["src_tangle_issue2_canon_feedback_2026", "src_oup_fricker_epistemic_injustice_2007"], "Public curator reflection read alongside Fricker's account of epistemic exclusion", "Provisional systems interpretation: closure is not inherently oppressive; exclusion depends on how admissibility and revision are organised.", status="provisional", mode="interpreted", confidence="0.76", review_label="provisional conceptual interpretation"),
        edge_record("e17_canon_can_exclude", "concept_canon_formation", "concept_epistemic_exclusion", "can_exclude", "contestation", "can produce", ["src_oro_boundaries_disciplines_2006", "src_oup_fricker_epistemic_injustice_2007", "src_tangle_issue2_canon_feedback_2026"], "Boundary-selection article, epistemic-injustice account and public editorial reflection", "Provisional bridge between disciplinary selection and social epistemology; particular cases require their own evidence.", status="provisional", mode="interpreted", confidence="0.74", review_label="provisional conceptual interpretation"),
        edge_record("e17_recovery_responds_exclusion", "practice_lineage_recovery", "concept_epistemic_exclusion", "responds_to", "practice", "is an evidence-led response to", ["src_tangle_issue2_canon_feedback_2026", "src_oro_boundaries_disciplines_2006"], "Public editorial requirement and systems-thinkers boundary article", "The practice does not presume every absence is an exclusion; it investigates the history and relation type."),
        edge_record("e17_lineage_documentation_supports_recovery", lineage_doc_id, "practice_lineage_recovery", "develops", "practice", "provides typed documentary methods for", ["src_oro_boundaries_disciplines_2006", "src_tangle_issue2_canon_feedback_2026"], "Public systems-lineage and editorial sources", "This is an atlas practice connection, not a claim that one named author originated lineage recovery."),
        edge_record("e17_structurelessness_checks_openness", "concept_structurelessness", "concept_epistemic_closure", "critiques", "contestation", "complicates a simple open-versus-closed reading of", ["src_freeman_tyranny_structurelessness", "src_tangle_issue2_canon_feedback_2026"], "Freeman's formal/informal structure argument and public editorial reflection", "Interpretive transfer from group structure to knowledge governance; it does not make the concepts equivalent.", status="provisional", mode="interpreted", confidence="0.72", review_label="provisional conceptual interpretation"),
    ]
    upsert(data.setdefault("edges", []), edges, "id")

    journey = {
        "id": "journey_who_counts_as_a_systems_thinker",
        "title": "Who gets to count as a systems thinker?",
        "summary": "Move from a useful biographical canon through its boundary choices, epistemic closure and exclusion, critical pluralism, decolonial questions and evidence-led lineage recovery.",
        "audience": "Readers who want the map to expose its own visibility rules rather than merely add a more diverse row of portraits.",
        "duration_minutes": 18,
        "steps": [
            {"node_id": systems_thinkers_id, "heading": "A map which admits it is a selection", "narrative": "Systems Thinkers offers an unusually useful people-centred history. Its authors also examined what it means to construct a set of key thinkers."},
            {"node_id": "person_karen_shipp", "heading": "Teaching is part of intellectual history", "narrative": "Shipp's educational and facilitative contribution matters because fields travel through learning designs and relationships, not publications alone."},
            {"node_id": "concept_canon_formation", "heading": "Repetition makes a centre", "narrative": "Lists, syllabuses, conferences, institutions and maps make some lineages easy to see and others difficult to retrieve."},
            {"node_id": "concept_epistemic_closure", "heading": "Every knowledge system closes", "narrative": "Coherence needs distinctions. The sharper question is who can alter them and what experiences are allowed to count as a learning signal."},
            {"node_id": "concept_epistemic_injustice", "heading": "People can be wronged as knowers", "narrative": "Credibility and interpretive resources are distributed unequally. Inclusion without changed knowledge rules may leave the same system intact."},
            {"node_id": critical_id, "heading": "Pluralism needs judgement", "narrative": "Critical systems thinking treats methods and perspectives as plural while retaining the obligation to examine power, interests and consequences."},
            {"node_id": "person_magnus_ramage", "heading": "Study the field from its margins", "narrative": "Ramage's systems history and current critical and decolonial interests turn canon review into active systems scholarship."},
            {"node_id": "concept_structurelessness", "heading": "Openness does not abolish power", "narrative": "Freeman's warning matters here: removing formal boundaries can leave informal structures more powerful and less accountable."},
            {"node_id": "practice_lineage_recovery", "heading": "Recover relations, not decorations", "narrative": "The work is to establish authorship, teaching, appropriation, exclusion, canonisation and recovery precisely enough to withstand challenge."},
        ],
    }
    upsert(data.setdefault("journeys", []), [journey], "id")

    submission = {
        "issue_number": 21,
        "title": "Viability — Consider adding viability vs fitness",
        "contributor": "Ivo Velitchkov (GitHub: kvistgaard)",
        "created_at": "2026-08-10",
        "status": "incorporated",
        "proposal": "Distinguish viability from fitness and connect viability to Maturana and Varela's natural-drift account rather than treating evolution only as survival of the fittest.",
        "curator_response": "Incorporated in release 0.12 after checking the distinction against independent primary and institutional sources. The submitted wording remains the originating contribution, not its own evidence.",
        "issue_url": "https://github.com/antlerboy/the-necessary-tangle/issues/21",
        "result_links": [
            {"label": "Viability", "url": "https://transduction.systems/#view=item&id=concept_viability"},
            {"label": "Natural drift", "url": "https://transduction.systems/#view=item&id=concept_natural_drift"},
            {"label": "Ivo Velitchkov", "url": "https://transduction.systems/#view=item&id=person_ivo_velitchkov"},
        ],
    }
    data["site_submissions"] = {
        "release": RELEASE,
        "generated": GENERATED,
        "canonical_system": "GitHub Issues",
        "canonical_query_url": "https://github.com/antlerboy/the-necessary-tangle/issues?q=is%3Aissue+%22Prepared+from+The+Necessary+Tangle%22+sort%3Acreated-desc",
        "marker": "Prepared from The Necessary Tangle",
        "status_vocabulary": ["awaiting review", "investigating", "incorporated", "partly incorporated", "disputed", "deferred", "declined"],
        "items": [submission],
        "note": "This is a generated public projection. The GitHub issue and its comments remain the canonical record.",
    }

    visibility_names = [
        "Allenna Leonard", "Angela Espinosa", "Nora Bateson", "Sandra Janoff", "Christine Oliver",
        "Diane Bowling", "Isabel Menzies Lyth", "Mary Douglas", "Elaine Brown", "Harish Jose",
        "Taiichi Ohno", "Chögyam Trungpa", "Michael C. Jackson", "Magnus Ramage", "Karen Shipp",
    ]
    public_nodes = {
        node["id"]: node for node in data["nodes"]
        if node.get("public_visibility") == "public"
        and data.get("canonical_redirects", {}).get(node["id"], node["id"]) == node["id"]
    }
    review_items = []
    for name in visibility_names:
        node_id = find_node(data, name)
        node = public_nodes.get(node_id or "")
        review_items.append({
            "name": name,
            "node_id": node_id if node else "",
            "status": (
                "developed entry" if node and node.get("publication_level") == "profile"
                else "brief entry" if node and node.get("publication_level") == "described"
                else "outline only" if node
                else "not yet represented"
            ),
            "next_work": "Review public sources, intellectual traditions, institutions, transmissions and visibility history; do not infer ethnicity or heritage from name, portrait or geography.",
        })
    data["canon_visibility_review"] = {
        "release": RELEASE,
        "generated": GENERATED,
        "question": "Who becomes visible as a knower, teacher, practitioner or originator, and who can alter the boundary of the field?",
        "policy": "Record publicly sourced intellectual, institutional, geographical, linguistic and self-described identity context only where it helps explain the work. Never infer ethnicity, religion, nationality, gender or heritage. Demographic variety does not substitute for typed histories of exclusion, appropriation, canonisation and recovery.",
        "items": review_items,
    }

    data["relational_depth"] = calculate_relational_depth(data)
    metrics = graph_metrics(data)
    eligible_surprises = [
        node for node in data["nodes"]
        if node.get("public_visibility") == "public"
        and data.get("canonical_redirects", {}).get(node["id"], node["id"]) == node["id"]
        and node.get("status") == "accepted"
        and node.get("publication_level") in {"profile", "described"}
        and node.get("entity_type") not in {"corpus", "source", "evidence", "claim"}
        and len(str(node.get("description", ""))) >= 80
    ]
    meta = data.setdefault("meta", {})
    relational_aggregate = data.get("relational_depth", {}).get("aggregate", {})
    meta.update({
        "release": RELEASE,
        "generated": GENERATED,
        "project_url": PUBLIC_URL,
        "iteration_focus": "public submissions and responses, serendipitous exploration, canon and lineage visibility, and expanded critical systems history",
        "public_entry_count": metrics["public_entries"],
        "described_entry_count": metrics["public_entries"],
        "profile_count": len(data.get("profiles", [])),
        "source_count": len(data.get("sources", [])),
        "journey_count": len(data.get("journeys", [])),
        "site_submission_count": len(data["site_submissions"]["items"]),
        "canon_visibility_review_count": len(review_items),
        "surprise_me_eligible_count": len(eligible_surprises),
        "reader_connected_entry_count": relational_aggregate.get("reader_connected_entries", 0),
        "public_submissions_url": "https://transduction.systems/submissions/",
        "canon_lineage_url": "https://transduction.systems/canon-and-lineage/",
    })
    for inherited in ("reading_list_inventory", "reading_list_coverage", "core_systems_practice"):
        if data.get(inherited):
            data[inherited]["release"] = RELEASE
    if data.get("ai_observations"):
        data["ai_observations"]["release"] = RELEASE
        data["ai_observations"]["generated"] = GENERATED
        data["ai_observations"]["metrics"] = metrics

    rendered = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    DATA_PATH.write_text(rendered, encoding="utf-8")
    DOCS_ASSETS.mkdir(parents=True, exist_ok=True)
    (DOCS_ASSETS / "public-data.json").write_text(rendered, encoding="utf-8")
    (DOCS_ASSETS / "public-data.js").write_text(
        "window.TANGLE_DATA = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n",
        encoding="utf-8",
    )
    (DOCS_ASSETS / "site-submissions.json").write_text(
        json.dumps(data["site_submissions"], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "release": RELEASE,
        "public_entries": meta["public_entry_count"],
        "profiles": meta["profile_count"],
        "sources": meta["source_count"],
        "journeys": meta["journey_count"],
        "site_submissions": meta["site_submission_count"],
        "surprise_me_eligible": meta["surprise_me_eligible_count"],
    }, indent=2))


if __name__ == "__main__":
    main()
