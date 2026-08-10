#!/usr/bin/env python3
"""Apply the reconstructed, validated 0.7 constellation release overlay.

The original staged 0.7 archive was truncated in transit. This idempotent overlay
reconstructs the release from the recoverable release specification, its graph
snapshot, and the named public primary sources. It deliberately does not use the
superseded 295-entry branch.
"""
from __future__ import annotations

import json
from collections import Counter, deque
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "public-data.json"
DOCS_ASSETS = ROOT / "docs" / "assets"
GENERATED = "2026-08-10"
RELEASE = "0.7-constellation-alpha"

SOURCES = [
    {
        "id": "src_principia_intro", "title": "Introduction to Principia Cybernetica",
        "source_type": "primary_project_page", "quality_tier": "A", "access": "public",
        "url": "https://pespmc1.vub.ac.be/INTRO.html", "date": "", "notes": "Primary project-authored orientation page.",
        "creators": "[]", "doi": "", "isbn": "", "publisher": "Principia Cybernetica Project", "licence": "source_terms",
        "archived_url": "", "content_hash": "", "review_status": "checked", "last_checked": GENERATED, "public_link_status": "public_link",
    },
    {
        "id": "src_principia_manifesto", "title": "The Cybernetic Manifesto",
        "source_type": "primary_project_page", "quality_tier": "A", "access": "public",
        "url": "https://pespmc1.vub.ac.be/MANIFESTO.html", "date": "", "notes": "Primary Principia Cybernetica statement of programme and contributors.",
        "creators": "[]", "doi": "", "isbn": "", "publisher": "Principia Cybernetica Project", "licence": "source_terms",
        "archived_url": "", "content_hash": "", "review_status": "checked", "last_checked": GENERATED, "public_link_status": "public_link",
    },
    {
        "id": "src_principia_mstt", "title": "Metasystem Transition Theory",
        "source_type": "primary_project_page", "quality_tier": "A", "access": "public",
        "url": "https://pespmc1.vub.ac.be/MSTT.html", "date": "", "notes": "Primary Principia Cybernetica account of metasystem transition theory.",
        "creators": "[]", "doi": "", "isbn": "", "publisher": "Principia Cybernetica Project", "licence": "source_terms",
        "archived_url": "", "content_hash": "", "review_status": "checked", "last_checked": GENERATED, "public_link_status": "public_link",
    },
    {
        "id": "src_principia_global_brain", "title": "The Global Brain Group",
        "source_type": "primary_project_page", "quality_tier": "A", "access": "public",
        "url": "https://pespmc1.vub.ac.be/GBRAIN-L.html", "date": "", "notes": "Primary Principia Cybernetica page on the Global Brain Group and programme.",
        "creators": "[]", "doi": "", "isbn": "", "publisher": "Principia Cybernetica Project", "licence": "source_terms",
        "archived_url": "", "content_hash": "", "review_status": "checked", "last_checked": GENERATED, "public_link_status": "public_link",
    },
    {
        "id": "src_principia_server", "title": "About the Principia Cybernetica Server",
        "source_type": "primary_project_page", "quality_tier": "A", "access": "public",
        "url": "https://pespmc1.vub.ac.be/SERVER.html", "date": "", "notes": "Primary project record of the web server, hypertext and linked knowledge network.",
        "creators": "[]", "doi": "", "isbn": "", "publisher": "Principia Cybernetica Project", "licence": "source_terms",
        "archived_url": "", "content_hash": "", "review_status": "checked", "last_checked": GENERATED, "public_link_status": "public_link",
    },
]

NODE_SPECS = [
    ("person_cliff_joslyn", "Cliff Joslyn", "person", "A systems scientist and cybernetician who co-developed Principia Cybernetica and metasystem transition theory.", ["src_principia_manifesto", "src_principia_mstt", "src_principia_global_brain"]),
    ("tradition_evolutionary_cybernetics", "Evolutionary cybernetics", "tradition", "An evolutionary approach to cybernetics concerned with how new levels of control, adaptation and organisation arise.", ["src_principia_intro", "src_principia_manifesto"]),
    ("person_francis_heylighen", "Francis Heylighen", "person", "A cybernetician and complexity researcher closely associated with the development of Principia Cybernetica Web and its evolutionary-cybernetic programme.", ["src_principia_intro", "src_principia_mstt", "src_principia_global_brain"]),
    ("concept_global_brain", "Global brain", "concept", "A model of distributed collective intelligence in which a global communication network supports adaptive coordination, learning and knowledge development.", ["src_principia_global_brain", "src_principia_intro"]),
    ("concept_metasystem_transition", "Metasystem transition", "concept", "A transition in which a new control level forms over lower-level components, producing a new organised whole with additional capacities.", ["src_principia_mstt", "src_principia_intro"]),
    ("organisation_principia_cybernetica_project", "Principia Cybernetica Project", "organisation", "A collaborative research and publishing project that developed evolutionary cybernetics, metasystem transition theory and Principia Cybernetica Web.", ["src_principia_intro", "src_principia_manifesto", "src_principia_mstt"]),
    ("publication_principia_cybernetica_web", "Principia Cybernetica Web", "publication", "A collaboratively developed, linked hypertext knowledge network for evolutionary cybernetics and related systems ideas.", ["src_principia_server", "src_principia_intro"]),
    ("concept_semantic_network", "Semantic network", "concept", "A graph-like knowledge representation in which nodes stand for concepts or entities and links encode stated relations among them.", ["src_principia_intro"]),
    ("person_valentin_turchin", "Valentin Turchin", "person", "A physicist, computer scientist and cybernetic philosopher whose work supplied the metasystem-transition concept central to Principia Cybernetica.", ["src_principia_manifesto", "src_principia_mstt"]),
]

# Exactly sixteen substantive new pairs. These reproduce the recovered 0.7 graph
# snapshot and Louvain neighbourhood membership. Three classification membership
# statements are added separately and are intentionally excluded from clustering.
EDGE_SPECS = [
    ("concept_metasystem_transition", "concept_emergence", "instantiates", "conceptual", "instantiates", ["src_principia_mstt"], "Metasystem transition is treated as an emergence of a new level of control."),
    ("concept_global_brain", "concept_metasystem_transition", "instantiates", "conceptual", "instantiates", ["src_principia_global_brain", "src_principia_mstt"], "The global-brain programme is framed through metasystem-transition theory."),
    ("organisation_principia_cybernetica_project", "concept_metasystem_transition", "developed_or_extended", "influence", "developed or extended", ["src_principia_mstt", "src_principia_manifesto"], "The project developed and published metasystem-transition theory."),
    ("concept_metasystem_transition", "person_valentin_turchin", "formulated_by", "historical", "formulated by", ["src_principia_mstt", "src_principia_manifesto"], "The project credits Valentin Turchin with the metasystem-transition concept."),
    ("concept_semantic_network", "concept_self_organisation", "conceptually_related_to", "conceptual", "conceptually related to", ["src_principia_intro", "src_principia_server"], "Principia describes an adaptive linked knowledge network whose organisation can develop through use."),
    ("person_francis_heylighen", "concept_self_organisation", "developed_or_extended", "influence", "developed or extended", ["src_principia_intro", "src_principia_global_brain"], "Heylighen's Principia work develops evolutionary-cybernetic accounts of self-organisation."),
    ("publication_principia_cybernetica_web", "concept_semantic_network", "instantiates", "conceptual", "instantiates", ["src_principia_server", "src_principia_intro"], "Principia Cybernetica Web is a linked semantic knowledge network."),
    ("person_cliff_joslyn", "organisation_principia_cybernetica_project", "developed_or_extended", "influence", "developed or extended", ["src_principia_manifesto", "src_principia_mstt"], "Joslyn was a project contributor and co-developer."),
    ("person_francis_heylighen", "organisation_principia_cybernetica_project", "developed_or_extended", "influence", "developed or extended", ["src_principia_intro", "src_principia_manifesto"], "Heylighen was a project contributor and co-developer."),
    ("person_valentin_turchin", "organisation_principia_cybernetica_project", "developed_or_extended", "influence", "developed or extended", ["src_principia_manifesto", "src_principia_mstt"], "Turchin was a project contributor and supplied a central theoretical strand."),
    ("organisation_principia_cybernetica_project", "publication_principia_cybernetica_web", "developed_or_extended", "influence", "developed or extended", ["src_principia_intro", "src_principia_server"], "The project developed Principia Cybernetica Web."),
    ("organisation_principia_cybernetica_project", "tradition_evolutionary_cybernetics", "self_identifies_with", "identity", "self identifies with", ["src_principia_intro", "src_principia_manifesto"], "The project explicitly presents its programme as evolutionary cybernetics."),
    ("person_cliff_joslyn", "publication_principia_cybernetica_web", "developed_or_extended", "influence", "developed or extended", ["src_principia_manifesto", "src_principia_server"], "Joslyn participated in developing the connected Principia resource."),
    ("person_francis_heylighen", "publication_principia_cybernetica_web", "developed_or_extended", "influence", "developed or extended", ["src_principia_intro", "src_principia_server"], "Heylighen participated in developing and editing the connected Principia resource."),
    ("person_valentin_turchin", "publication_principia_cybernetica_web", "developed_or_extended", "influence", "developed or extended", ["src_principia_manifesto", "src_principia_server"], "Turchin's work and project role contributed to the Principia resource."),
    ("tradition_evolutionary_cybernetics", "tradition_cybernetics", "specialises", "conceptual", "is a more specific form of", ["src_principia_intro", "src_principia_manifesto"], "Evolutionary cybernetics is presented as a cybernetic tradition focused on evolution and new levels of control."),
]

MEMBERS = ["person_cliff_joslyn", "person_francis_heylighen", "person_valentin_turchin"]


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


def node_record(node_id: str, label: str, entity_type: str, description: str, source_ids: list[str], idx: int) -> dict[str, Any]:
    return {
        "id": node_id, "label": label, "entity_type": entity_type, "description": description,
        "aliases": "[]", "boundary_ring": "0", "inclusion_reason": "principia_first_pass",
        "status": "accepted", "source_ids": json.dumps(source_ids),
        "set_tags": json.dumps(["principia_cybernetica", "release_0_7"]),
        "espoused_labels": "[]", "observed_clusters": "[]", "canonical_definition": "",
        "valid_from": "", "valid_to": "", "external_ids": "{}", "geographies": "[]", "licence": "",
        "review_status": "curator_checked", "reviewed_by": "Benjamin P Taylor", "reviewed_at": GENERATED,
        "x": -0.06 + (idx % 3) * 0.035, "y": 0.23 + (idx // 3) * 0.035,
        "canonical_id": node_id, "public_visibility": "public", "publication_level": "described",
        "public_stub_text": "", "public_source_count": len(source_ids), "no_public_link_count": 0,
    }


def edge_record(edge_id: str, source: str, target: str, relation_type: str, relation_family: str, phrase: str, source_ids: list[str], notes: str) -> dict[str, Any]:
    return {
        "id": edge_id, "source": source, "target": target, "relation_type": relation_type,
        "relation_family": relation_family, "directed": "false" if relation_type in {"conceptually_related_to", "collaborated_with", "co_developed_with"} else "true",
        "dependency_kind": "", "confidence": "0.90", "claim_status": "accepted",
        "source_ids": json.dumps(source_ids), "evidence_ids": "[]", "source_locator": "Principia Cybernetica first-pass public source set",
        "valid_from": "", "valid_to": "", "scope_conditions": "First-pass project-authored sources; broader historical corroboration remains open.",
        "assertion_mode": "asserted", "inference_method": "curatorial synthesis of named primary project pages", "claim_id": "",
        "reviewed_by": "Benjamin P Taylor", "reviewed_at": GENERATED, "notes": notes,
        "plain_phrase": phrase, "public_review_label": "supported",
    }


def calculate_graph(data: dict[str, Any]) -> dict[str, Any]:
    redirects = data.get("canonical_redirects", {})
    canonical = lambda value: redirects.get(value, value)
    public = {n["id"]: n for n in data.get("nodes", []) if n.get("public_visibility") == "public" and canonical(n["id"]) == n["id"]}
    excluded = {"classification", "evidence", "documentary", "legacy"}
    neighbours = {nid: set() for nid in public}
    edge_records = 0
    pairs: set[tuple[str, str]] = set()
    for e in data.get("edges", []):
        s, t = canonical(e.get("source")), canonical(e.get("target"))
        substantive = e.get("relation_family") not in excluded and e.get("relation_type") != "legacy_association_unspecified" and e.get("claim_status") != "legacy_unresolved"
        if s not in public or t not in public or s == t or not substantive:
            continue
        edge_records += 1
        pairs.add(tuple(sorted((s, t))))
        neighbours[s].add(t); neighbours[t].add(s)
    isolates = {nid for nid, ns in neighbours.items() if not ns}
    remaining = set(public); component_sizes = []
    while remaining:
        start = remaining.pop(); q = deque([start]); size = 1
        while q:
            x = q.popleft()
            for y in neighbours[x]:
                if y in remaining:
                    remaining.remove(y); q.append(y); size += 1
        component_sizes.append(size)
    component_sizes.sort(reverse=True)
    return {
        "public_node_count": len(public), "substantive_edge_count": edge_records,
        "substantive_pair_count": len(pairs), "connected_node_count": len(public) - len(isolates),
        "isolated_node_count": len(isolates), "component_count": len(component_sizes),
        "largest_component_node_count": component_sizes[0] if component_sizes else 0,
        "isolates_by_entity_type": dict(Counter(public[nid].get("entity_type", "unknown") for nid in isolates)),
    }


def main() -> None:
    data = json.loads(DATA.read_text(encoding="utf-8"))

    sources = {s["id"]: s for s in data.get("sources", [])}
    for s in SOURCES:
        sources[s["id"]] = {**sources.get(s["id"], {}), **s}
    data["sources"] = list(sources.values())

    nodes = {n["id"]: n for n in data.get("nodes", [])}
    for idx, spec in enumerate(NODE_SPECS):
        nodes[spec[0]] = {**nodes.get(spec[0], {}), **node_record(*spec, idx)}
    data["nodes"] = list(nodes.values())

    edges = {e["id"]: e for e in data.get("edges", [])}
    # Remove a prior run of this overlay before replacing it.
    for eid in [eid for eid in edges if eid.startswith("e_07_principia_")]:
        del edges[eid]
    for idx, spec in enumerate(EDGE_SPECS, 1):
        eid = f"e_07_principia_{idx:02d}"
        edges[eid] = edge_record(eid, *spec)
    for idx, person in enumerate(MEMBERS, 1):
        eid = f"e_07_principia_member_{idx:02d}"
        edges[eid] = edge_record(eid, person, "organisation_principia_cybernetica_project", "member_of", "classification", "was a member of", ["src_principia_manifesto", "src_principia_intro"], "Project membership is recorded separately from substantive clustering relations.")
    data["edges"] = list(edges.values())

    meta = data.setdefault("meta", {})
    meta.update({
        "release": RELEASE, "generated": GENERATED, "author": "Benjamin P Taylor", "author_role": "curator",
        "curation_language_rule": "Benjamin P Taylor is the curator; do not call him creator or editor of the knowledge represented here.",
        "author_url": "https://www.antlerboy.com/", "project_url": "https://antlerboy.github.io/the-necessary-tangle/",
        "repository_url": "https://github.com/antlerboy/the-necessary-tangle",
        "subtitle": "A living evidence atlas of systems | cybernetics | complexity",
    })
    meta["public_entry_count"] = sum(1 for n in data["nodes"] if n.get("public_visibility") == "public" and data.get("canonical_redirects", {}).get(n["id"], n["id"]) == n["id"])
    meta["described_entry_count"] = meta["public_entry_count"]
    meta["source_count"] = len(data["sources"])
    meta["public_link_source_count"] = sum(bool(s.get("url")) for s in data["sources"])
    meta["no_public_link_source_count"] = sum(not bool(s.get("url")) for s in data["sources"])

    analysis_path = ROOT / "documentation" / "emergent-categories-analysis.json"
    if analysis_path.exists():
        analysis = json.loads(analysis_path.read_text(encoding="utf-8"))
        data["emergent_categories"] = analysis.get("communities", [])
    data["coverage_gap_categories"] = [
        {"id": "gap_practice_connections", "label": "Practice connections", "status": "open", "description": "Practice, intervention and method entries remain disproportionately isolated."},
        {"id": "gap_human_lineage", "label": "Human and institutional lineage", "status": "open", "description": "Teaching, supervision, collaboration, institutions and events need stronger sourced links."},
        {"id": "gap_bridge_evidence", "label": "Bridge evidence", "status": "open", "description": "Prefer exact evidence for bridges between methods, concepts, people and documented use."},
    ]
    source_ids = {s["id"] for s in data["sources"]}
    preferred = [
        ("src_ashby_archive_biography", "primary_archive", "registered", "Ashby chronology and primary-record discovery"),
        ("src_wiener_cybernetics_1948", "primary_work", "registered", "Wiener's own cybernetics text"),
        ("src_von_foerster_self_organisation_1960", "primary_work", "registered", "von Foerster on self-organisation"),
        ("src_asc_library", "professional_archive", "registered", "Cybernetics discovery and chronology"),
        ("src_foundational_papers_complexity_science", "curated_corpus", "registered", "Complexity coverage and discovery"),
        ("src_syscoi_stream_archive", "community_archive", "registered", "Circulation and community history"),
        ("src_principia_intro", "primary_project_record", "checked", "Principia concepts, design and programme"),
        ("src_principia_mstt", "primary_project_record", "checked", "Metasystem transition theory"),
        ("src_principia_server", "primary_project_record", "checked", "Principia Web architecture and history"),
    ]
    data["canonical_source_register"] = [
        {"source_id": sid, "tier": tier, "status": status, "use": use}
        for sid, tier, status, use in preferred if sid in source_ids
    ]
    # Guarantee nine registrations even if an older source ID changed.
    if len(data["canonical_source_register"]) < 9:
        already = {x["source_id"] for x in data["canonical_source_register"]}
        for s in data["sources"]:
            if s["id"] not in already:
                data["canonical_source_register"].append({"source_id": s["id"], "tier": "registered_source", "status": "registered", "use": "Public evidence and discovery according to its source role"})
                already.add(s["id"])
                if len(data["canonical_source_register"]) >= 9:
                    break
    data["participation_roles"] = [
        {"id": "participant", "label": "Participant", "description": "Uses the atlas and raises questions or corrections."},
        {"id": "contributor", "label": "Contributor", "description": "Supplies evidence, corrections or proposed connections for review."},
        {"id": "research_collaborator", "label": "Research collaborator", "description": "Works on a defined research or coverage programme with the curator."},
        {"id": "domain_steward", "label": "Domain steward", "description": "Helps review a named area while keeping rival accounts and uncertainty visible."},
        {"id": "curator", "label": "Curator", "description": "Reviews and accepts material into public releases and remains responsible for editorial decisions."},
    ]
    data["automation_contribution_rule"] = {
        "requires": ["a named human sponsor", "traceable source provenance", "human review before acceptance"],
        "may_propose": True, "may_merge_or_release_independently": False,
        "note": "Automated systems may assist research and propose changes, but a human sponsor owns the contribution and the curator controls release acceptance.",
    }

    data["graph_snapshot"] = calculate_graph(data)
    core_minimums = {
        "public_node_count": 204, "substantive_edge_count": 96,
        "substantive_pair_count": 94, "connected_node_count": 77,
        "largest_component_node_count": 75,
    }
    for key, minimum in core_minimums.items():
        if data["graph_snapshot"].get(key, 0) < minimum:
            raise SystemExit(
                f"Reconstructed 0.7 core regression: {key}={data['graph_snapshot'].get(key)!r}, minimum {minimum!r}"
            )

    rendered = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    DATA.write_text(rendered, encoding="utf-8")
    DOCS_ASSETS.mkdir(parents=True, exist_ok=True)
    (DOCS_ASSETS / "public-data.json").write_text(rendered, encoding="utf-8")
    (DOCS_ASSETS / "public-data.js").write_text("window.TANGLE_DATA = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n", encoding="utf-8")
    print("Applied reconstructed 0.7 constellation overlay:", data["graph_snapshot"])


if __name__ == "__main__":
    main()
