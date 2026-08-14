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
    upsert(data["sources"], SOURCE_RECORDS)
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
            "reader_connected_entry_count": aggregate["reader_connected_entries"],
            "semantic_connected_entry_count": aggregate["semantic_connected_entries"],
            "rich_entry_count": aggregate["connection_bands"].get("rich", 0),
            "developing_entry_count": aggregate["connection_bands"].get("developing", 0),
            "thin_entry_count": aggregate["connection_bands"].get("thin", 0),
            "unconnected_entry_count": aggregate["connection_bands"].get("unconnected", 0),
        }
    )
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
