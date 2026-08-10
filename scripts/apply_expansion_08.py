#!/usr/bin/env python3
"""Apply the 0.8 evidence-gated breadth expansion.

This pass imports the defensible bibliographic material from the superseded
295-entry branch without merging that branch. It adds the 89 publications in
the official Foundational Papers in Complexity Science inventory, their authors
as explicitly shallow bibliographic person entries, four volume containers and
three reviewed framing records. It is deliberately an inventory layer, not a
claim that every paper or author has received a full intellectual profile.
"""
from __future__ import annotations

import hashlib
import json
import math
import re
import unicodedata
from collections import Counter, defaultdict, deque
from itertools import combinations
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "public-data.json"
SEED_PATH = ROOT / "data" / "expansion-08-seed.json"
DOCS_ASSETS = ROOT / "docs" / "assets"

RELEASE = "0.8-expansion-alpha"
GENERATED = "2026-08-10"
BASELINE_PUBLIC_COUNT = 204
MINIMUM_NEW_ENTRIES = 200
CORPUS_ID = "corpus_foundational_papers_2024"
REDIRECTED_EVOLUTIONARY_ID = "concept_evolutionary_cybernetics"
CANONICAL_EVOLUTIONARY_ID = "tradition_evolutionary_cybernetics"


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


def encode(values: list[str]) -> str:
    return json.dumps(list(dict.fromkeys(values)), ensure_ascii=False)


def fold(value: str) -> str:
    return "".join(
        ch for ch in unicodedata.normalize("NFKD", value)
        if not unicodedata.combining(ch)
    ).casefold()


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", fold(value)).strip("_")


def split_authors(value: str) -> list[str]:
    value = value.replace(", and ", ", ").replace(" and ", ", ")
    return [part.strip() for part in value.split(",") if part.strip()]


def stable_fraction(value: str, offset: int = 0) -> float:
    digest = hashlib.sha256(f"{offset}:{value}".encode("utf-8")).digest()
    return int.from_bytes(digest[:4], "big") / 2**32


def merge_source_ids(record: dict[str, Any], source_ids: list[str]) -> None:
    record["source_ids"] = encode([*parse(record.get("source_ids")), *source_ids])


def graph_snapshot(data: dict[str, Any]) -> dict[str, Any]:
    redirects = data.get("canonical_redirects", {})
    canonical = lambda value: redirects.get(value, value)
    public = {
        node["id"]: node
        for node in data.get("nodes", [])
        if node.get("public_visibility") == "public"
        and canonical(node["id"]) == node["id"]
    }
    excluded = {"classification", "evidence", "documentary", "legacy"}
    neighbours = {node_id: set() for node_id in public}
    edge_records = 0
    pairs: set[tuple[str, str]] = set()
    for edge in data.get("edges", []):
        source = canonical(edge.get("source"))
        target = canonical(edge.get("target"))
        substantive = (
            edge.get("relation_family") not in excluded
            and edge.get("relation_type") != "legacy_association_unspecified"
            and edge.get("claim_status") != "legacy_unresolved"
        )
        if source not in public or target not in public or source == target or not substantive:
            continue
        edge_records += 1
        pairs.add(tuple(sorted((source, target))))
        neighbours[source].add(target)
        neighbours[target].add(source)

    isolates = {node_id for node_id, adjacent in neighbours.items() if not adjacent}
    remaining = set(public)
    component_sizes: list[int] = []
    while remaining:
        start = remaining.pop()
        queue = deque([start])
        size = 1
        while queue:
            current = queue.popleft()
            for other in neighbours[current]:
                if other in remaining:
                    remaining.remove(other)
                    queue.append(other)
                    size += 1
        component_sizes.append(size)
    component_sizes.sort(reverse=True)
    return {
        "public_node_count": len(public),
        "substantive_edge_count": edge_records,
        "substantive_pair_count": len(pairs),
        "connected_node_count": len(public) - len(isolates),
        "isolated_node_count": len(isolates),
        "component_count": len(component_sizes),
        "largest_component_node_count": component_sizes[0] if component_sizes else 0,
        "isolates_by_entity_type": dict(
            Counter(public[node_id].get("entity_type", "unknown") for node_id in isolates)
        ),
    }


def relation_record(
    relation_type: str,
    relation_family: str,
    directed: str,
    inverse: str,
    minimum_evidence: str,
    plain_phrase: str,
) -> dict[str, str]:
    return {
        "relation_type": relation_type,
        "relation_family": relation_family,
        "directed": directed,
        "inverse": inverse,
        "minimum_evidence": minimum_evidence,
        "strict_dependency": "no",
        "plain_phrase": plain_phrase,
    }


def edge_record(
    edge_id: str,
    source: str,
    target: str,
    relation_type: str,
    relation_family: str,
    plain_phrase: str,
    source_ids: list[str],
    notes: str,
    confidence: str = "0.96",
    claim_status: str = "accepted",
) -> dict[str, Any]:
    return {
        "id": edge_id,
        "source": source,
        "target": target,
        "relation_type": relation_type,
        "relation_family": relation_family,
        "directed": "false" if relation_type == "coauthored_with" else "true",
        "dependency_kind": "",
        "confidence": confidence,
        "claim_status": claim_status,
        "source_ids": encode(source_ids),
        "evidence_ids": "[]",
        "source_locator": "Official Foundational Papers in Complexity Science table of contents",
        "valid_from": "",
        "valid_to": "",
        "scope_conditions": "Bibliographic first pass: records authorship or collection structure, not a full evaluation of the work or influence.",
        "assertion_mode": "asserted",
        "inference_method": "",
        "claim_id": "",
        "reviewed_by": "Benjamin P Taylor",
        "reviewed_at": GENERATED,
        "notes": notes,
        "plain_phrase": plain_phrase,
        "public_review_label": "official bibliographic record",
    }


def author_node(author: str, papers: list[dict[str, Any]], source_id: str) -> dict[str, Any]:
    titles = [paper["title"] for paper in papers]
    if len(titles) == 1:
        works = f"‘{titles[0]}’"
    elif len(titles) == 2:
        works = f"‘{titles[0]}’ and ‘{titles[1]}’"
    else:
        works = ", ".join(f"‘{title}’" for title in titles[:-1]) + f", and ‘{titles[-1]}’"
    description = (
        f"A bibliographic first-pass person entry for {author}, listed by the official "
        f"Foundational Papers in Complexity Science table of contents as an author of {works}. "
        "This records collection authorship only; it is not yet a full intellectual profile."
    )
    node_id = f"person_fpcs_{slug(author)}"
    return {
        "id": node_id,
        "label": author,
        "entity_type": "person",
        "description": description,
        "aliases": "[]",
        "boundary_ring": "1",
        "inclusion_reason": "official_collection_author_inventory",
        "status": "accepted",
        "source_ids": encode([source_id]),
        "set_tags": encode([
            "foundational_papers_complexity_science",
            "bibliographic_first_pass",
            "release_0_8_expansion",
        ]),
        "espoused_labels": "[]",
        "observed_clusters": "[]",
        "canonical_definition": "",
        "valid_from": "",
        "valid_to": "",
        "external_ids": "{}",
        "geographies": "[]",
        "licence": "",
        "review_status": "official_toc_bibliographic_first_pass",
        "reviewed_by": "Benjamin P Taylor",
        "reviewed_at": GENERATED,
        "x": 0.0,
        "y": 0.0,
        "canonical_id": node_id,
        "public_visibility": "public",
        "publication_level": "described",
        "public_stub_text": "",
        "public_source_count": 1,
        "no_public_link_count": 0,
    }


def volume_node(volume: int, source_id: str, anchor: tuple[float, float]) -> dict[str, Any]:
    node_id = f"publication_fpcs_volume_{volume}"
    return {
        "id": node_id,
        "label": f"Foundational Papers in Complexity Science, volume {volume}",
        "entity_type": "publication",
        "description": (
            f"Volume {volume} of the Foundational Papers in Complexity Science collection, "
            "represented as a bibliographic container for the historical papers listed in the official table of contents."
        ),
        "aliases": "[]",
        "boundary_ring": "1",
        "inclusion_reason": "official_collection_volume",
        "status": "accepted",
        "source_ids": encode([source_id]),
        "set_tags": encode([
            "foundational_papers_complexity_science",
            f"fpcs_volume_{volume}",
            "release_0_8_expansion",
        ]),
        "espoused_labels": "[]",
        "observed_clusters": "[]",
        "canonical_definition": "",
        "valid_from": "",
        "valid_to": "",
        "external_ids": "{}",
        "geographies": "[]",
        "licence": "",
        "review_status": "official_toc_bibliographic_inventory",
        "reviewed_by": "Benjamin P Taylor",
        "reviewed_at": GENERATED,
        "x": anchor[0],
        "y": anchor[1],
        "canonical_id": node_id,
        "public_visibility": "public",
        "publication_level": "described",
        "public_stub_text": "",
        "public_source_count": 1,
        "no_public_link_count": 0,
    }


def main() -> None:
    if not SEED_PATH.exists():
        raise SystemExit(f"Missing expansion seed: {SEED_PATH.relative_to(ROOT)}")
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    seed = json.loads(SEED_PATH.read_text(encoding="utf-8"))

    sources = {source["id"]: dict(source) for source in data.get("sources", [])}
    for source in seed.get("sources", []):
        sources[source["id"]] = {**sources.get(source["id"], {}), **source}
    toc_source = next(
        (source for source in sources.values() if "tables-of-contents" in str(source.get("url", ""))),
        None,
    )
    if not toc_source:
        toc_source = {
            "id": "src_fpcs_official_toc",
            "title": "Foundational Papers in Complexity Science — tables of contents",
            "source_type": "official_collection_table_of_contents",
            "quality_tier": "A",
            "access": "public",
            "url": "https://www.foundationalpapersincomplexityscience.org/tables-of-contents",
            "date": "2024",
            "notes": "Official collection inventory used for paper titles, author forms, volume placement and years.",
            "creators": "[]",
            "doi": "",
            "isbn": "",
            "publisher": "Foundational Papers in Complexity Science",
            "licence": "source_terms",
            "archived_url": "",
            "content_hash": "",
            "review_status": "checked",
            "last_checked": GENERATED,
            "public_link_status": "public_link",
        }
        sources[toc_source["id"]] = toc_source
    toc_source_id = toc_source["id"]
    data["sources"] = list(sources.values())

    relation_types = {
        item["relation_type"]: dict(item) for item in data.get("relation_types", [])
    }
    for item in seed.get("relation_types", []):
        relation_types[item["relation_type"]] = {
            **relation_types.get(item["relation_type"], {}),
            **item,
        }
    required_relations = [
        relation_record(
            "authored_by", "documentary", "true", "author_of",
            "Official publication record or the work itself", "authored by",
        ),
        relation_record(
            "coauthored_with", "human", "false", "coauthored_with",
            "Official publication record", "co-authored with",
        ),
        relation_record(
            "part_of", "classification", "true", "has_part",
            "Official collection structure", "is part of",
        ),
    ]
    for item in required_relations:
        relation_types[item["relation_type"]] = {
            **relation_types.get(item["relation_type"], {}),
            **item,
        }
    data["relation_types"] = list(relation_types.values())

    redirects = data.setdefault("canonical_redirects", {})
    redirects[REDIRECTED_EVOLUTIONARY_ID] = CANONICAL_EVOLUTIONARY_ID

    nodes = {node["id"]: dict(node) for node in data.get("nodes", [])}
    candidate_nodes = seed.get("candidate_nodes", [])
    imported_public_ids: set[str] = set()
    for candidate in candidate_nodes:
        candidate = dict(candidate)
        candidate_id = candidate["id"]
        if candidate_id == REDIRECTED_EVOLUTIONARY_ID:
            target = nodes.get(CANONICAL_EVOLUTIONARY_ID)
            if target:
                merge_source_ids(target, parse(candidate.get("source_ids")))
                target["aliases"] = encode([
                    *parse(target.get("aliases")),
                    candidate.get("label", "Evolutionary cybernetics"),
                ])
            continue
        candidate["canonical_id"] = candidate_id
        candidate["public_visibility"] = "public"
        candidate["publication_level"] = candidate.get("publication_level") or "described"
        candidate["reviewed_by"] = "Benjamin P Taylor"
        candidate["reviewed_at"] = GENERATED
        candidate["set_tags"] = encode([
            *parse(candidate.get("set_tags")),
            "release_0_8_expansion",
            "reviewed_superseded_branch_candidate",
        ])
        nodes[candidate_id] = {**nodes.get(candidate_id, {}), **candidate}
        imported_public_ids.add(candidate_id)

    papers = sorted(seed.get("fpcs_papers", []), key=lambda paper: int(paper["number"]))
    if len(papers) != 89:
        raise SystemExit(f"Expected 89 official papers, found {len(papers)}")

    anchors = {
        1: (-0.72, -0.62),
        2: (0.72, -0.62),
        3: (-0.72, 0.62),
        4: (0.72, 0.62),
    }
    for volume, anchor in anchors.items():
        node = volume_node(volume, toc_source_id, anchor)
        nodes[node["id"]] = {**nodes.get(node["id"], {}), **node}
        imported_public_ids.add(node["id"])

    papers_by_volume: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for paper in papers:
        papers_by_volume[int(paper["volume"])].append(paper)

    publication_position: dict[str, tuple[float, float]] = {}
    for volume, volume_papers in sorted(papers_by_volume.items()):
        anchor_x, anchor_y = anchors[volume]
        for index, paper in enumerate(volume_papers):
            ring = index % 2
            radius = 0.25 + ring * 0.13
            angle = -math.pi / 2 + 2 * math.pi * index / max(len(volume_papers), 1)
            position = (
                anchor_x + math.cos(angle) * radius,
                anchor_y + math.sin(angle) * radius,
            )
            publication_id = f"publication_fpcs_{int(paper['number']):03d}"
            publication_position[publication_id] = position
            publication = nodes.get(publication_id)
            if not publication:
                publication = {
                    "id": publication_id,
                    "label": paper["title"],
                    "entity_type": "publication",
                    "description": (
                        f"A bibliographic inventory entry for ‘{paper['title']}’ ({paper.get('year') or 'date not stated'}) "
                        f"by {paper['authors']}, listed in volume {paper['volume']} of the official Foundational Papers in Complexity Science table of contents. "
                        "Collection inclusion records an editorial selection, not endorsement or complete scholarly evaluation."
                    ),
                    "aliases": "[]",
                    "boundary_ring": "1",
                    "inclusion_reason": "official_collection_inventory",
                    "status": "accepted",
                    "source_ids": encode([toc_source_id]),
                    "set_tags": "[]",
                    "espoused_labels": "[]",
                    "observed_clusters": "[]",
                    "canonical_definition": "",
                    "valid_from": "",
                    "valid_to": "",
                    "external_ids": "{}",
                    "geographies": "[]",
                    "licence": "",
                    "review_status": "official_toc_bibliographic_inventory",
                    "reviewed_by": "Benjamin P Taylor",
                    "reviewed_at": GENERATED,
                    "canonical_id": publication_id,
                    "public_visibility": "public",
                    "publication_level": "described",
                    "public_stub_text": "",
                    "public_source_count": 1,
                    "no_public_link_count": 0,
                }
            publication["x"], publication["y"] = position
            publication["set_tags"] = encode([
                *parse(publication.get("set_tags")),
                "foundational_papers_complexity_science",
                f"fpcs_volume_{volume}",
                "release_0_8_expansion",
            ])
            merge_source_ids(publication, [toc_source_id])
            nodes[publication_id] = publication
            imported_public_ids.add(publication_id)

    existing_author_ids = seed.get("existing_author_ids", {})
    papers_by_author: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for paper in papers:
        for author in split_authors(paper["authors"]):
            papers_by_author[author].append(paper)

    author_ids: dict[str, str] = {}
    new_author_ids: set[str] = set()
    expansion_author_ids: set[str] = set()
    label_to_id = {
        fold(node.get("label", "")): node_id
        for node_id, node in nodes.items()
        if node.get("public_visibility") == "public"
        and redirects.get(node_id, node_id) == node_id
    }
    for author, authored_papers in sorted(papers_by_author.items(), key=lambda item: fold(item[0])):
        author_id = existing_author_ids.get(author) or label_to_id.get(fold(author))
        if not author_id:
            generated = author_node(author, authored_papers, toc_source_id)
            author_id = generated["id"]
            nodes[author_id] = {**nodes.get(author_id, {}), **generated}
            new_author_ids.add(author_id)
            imported_public_ids.add(author_id)
        author_ids[author] = author_id
        if nodes.get(author_id, {}).get("inclusion_reason") == "official_collection_author_inventory":
            expansion_author_ids.add(author_id)

    # Place expansion author entries near the papers with which the official inventory associates them.
    new_author_labels = sorted(
        (node_id, nodes[node_id]["label"]) for node_id in expansion_author_ids
    )
    for author_id, label in new_author_labels:
        author_form = next(author for author, mapped_id in author_ids.items() if mapped_id == author_id)
        positions = [
            publication_position[f"publication_fpcs_{int(paper['number']):03d}"]
            for paper in papers_by_author[author_form]
        ]
        centre_x = sum(position[0] for position in positions) / len(positions)
        centre_y = sum(position[1] for position in positions) / len(positions)
        angle = stable_fraction(label) * 2 * math.pi
        radius = 0.16 + stable_fraction(label, 1) * 0.16
        nodes[author_id]["x"] = centre_x + math.cos(angle) * radius
        nodes[author_id]["y"] = centre_y + math.sin(angle) * radius

    data["nodes"] = list(nodes.values())

    edges = {edge["id"]: dict(edge) for edge in data.get("edges", [])}
    node_ids = set(nodes)
    imported_seed_edges = 0
    for candidate in seed.get("candidate_edges", []):
        candidate = dict(candidate)
        source = redirects.get(candidate.get("source"), candidate.get("source"))
        target = redirects.get(candidate.get("target"), candidate.get("target"))
        if source not in node_ids or target not in node_ids or source == target:
            continue
        candidate["source"] = source
        candidate["target"] = target
        candidate["reviewed_by"] = "Benjamin P Taylor"
        candidate["reviewed_at"] = GENERATED
        candidate["notes"] = (
            str(candidate.get("notes") or "").strip()
            + " Candidate relation recovered from the superseded iteration and retained after endpoint and source validation."
        ).strip()
        edge_id = candidate["id"]
        if edge_id in edges and (
            edges[edge_id].get("source"), edges[edge_id].get("target")
        ) != (source, target):
            edge_id = f"e_08_seed_{slug(edge_id)}"
            candidate["id"] = edge_id
        edges[edge_id] = {**edges.get(edge_id, {}), **candidate}
        imported_seed_edges += 1

    authorship_edges = 0
    coauthor_edges = 0
    structure_edges = 0
    for paper in papers:
        number = int(paper["number"])
        publication_id = f"publication_fpcs_{number:03d}"
        volume_id = f"publication_fpcs_volume_{int(paper['volume'])}"
        edge_id = f"e_08_fpcs_paper_volume_{number:03d}"
        edges[edge_id] = edge_record(
            edge_id, publication_id, volume_id, "part_of", "classification", "is part of",
            [toc_source_id], f"Paper {number} is listed in volume {paper['volume']} of the official collection."
        )
        structure_edges += 1

        paper_author_ids = []
        for index, author in enumerate(split_authors(paper["authors"]), 1):
            author_id = author_ids[author]
            paper_author_ids.append(author_id)
            edge_id = f"e_08_fpcs_authored_{number:03d}_{index:02d}"
            edges[edge_id] = edge_record(
                edge_id, publication_id, author_id, "authored_by", "documentary", "authored by",
                [toc_source_id], f"The official collection table of contents lists {author} as an author of this paper."
            )
            authorship_edges += 1

        for pair_index, (left, right) in enumerate(combinations(sorted(set(paper_author_ids)), 2), 1):
            edge_id = f"e_08_fpcs_coauthor_{number:03d}_{pair_index:02d}"
            edges[edge_id] = edge_record(
                edge_id, left, right, "coauthored_with", "human", "co-authored with",
                [toc_source_id], f"The two people are listed as co-authors of ‘{paper['title']}’."
            )
            coauthor_edges += 1

    for volume in range(1, 5):
        volume_id = f"publication_fpcs_volume_{volume}"
        edge_id = f"e_08_fpcs_volume_corpus_{volume}"
        edges[edge_id] = edge_record(
            edge_id, volume_id, CORPUS_ID, "part_of", "classification", "is part of",
            [toc_source_id], f"Volume {volume} is part of the Foundational Papers in Complexity Science collection."
        )
        structure_edges += 1

    data["edges"] = list(edges.values())

    snapshot = graph_snapshot(data)
    data["graph_snapshot"] = snapshot
    redirects = data.get("canonical_redirects", {})
    public_ids = {
        node["id"] for node in data["nodes"]
        if node.get("public_visibility") == "public"
        and redirects.get(node["id"], node["id"]) == node["id"]
    }
    added_count = len(public_ids) - BASELINE_PUBLIC_COUNT
    if added_count < MINIMUM_NEW_ENTRIES:
        raise SystemExit(
            f"Expansion produced only {added_count} net new public entries; expected at least {MINIMUM_NEW_ENTRIES}"
        )

    data["expansion_08"] = {
        "baseline_public_count": BASELINE_PUBLIC_COUNT,
        "net_new_public_entries": added_count,
        "official_papers": len(papers),
        "new_bibliographic_people": len(expansion_author_ids),
        "existing_people_reused": len(set(author_ids.values()) - expansion_author_ids),
        "collection_volumes": 4,
        "reviewed_branch_candidates": sum(
            1 for candidate in candidate_nodes
            if candidate.get("id") != REDIRECTED_EVOLUTIONARY_ID
        ),
        "candidate_edges_retained": imported_seed_edges,
        "authorship_edges": authorship_edges,
        "coauthor_edges": coauthor_edges,
        "collection_structure_edges": structure_edges,
        "status": "bibliographic breadth pass; intellectual profiles and paper-level analysis remain uneven",
    }

    meta = data.setdefault("meta", {})
    meta.update({
        "release": RELEASE,
        "generated": GENERATED,
        "status": "public alpha on GitHub Pages",
        "coverage_status": (
            "Expanded bibliographic breadth with the 89-paper Foundational Papers inventory and its authors. "
            "These new records are explicit first-pass orientation entries, not finished scholarly profiles."
        ),
        "public_entry_count": len(public_ids),
        "described_entry_count": sum(
            1 for node in data["nodes"]
            if node.get("public_visibility") == "public"
            and redirects.get(node["id"], node["id"]) == node["id"]
            and node.get("publication_level") in {"described", "profile"}
        ),
        "source_count": len(data["sources"]),
        "public_link_source_count": sum(bool(source.get("url")) for source in data["sources"]),
        "no_public_link_source_count": sum(not bool(source.get("url")) for source in data["sources"]),
        "expansion_08_added_count": added_count,
    })

    rendered = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    DATA_PATH.write_text(rendered, encoding="utf-8")
    DOCS_ASSETS.mkdir(parents=True, exist_ok=True)
    (DOCS_ASSETS / "public-data.json").write_text(rendered, encoding="utf-8")
    (DOCS_ASSETS / "public-data.js").write_text(
        "window.TANGLE_DATA = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n",
        encoding="utf-8",
    )
    print(
        f"Applied {RELEASE}: {len(public_ids)} public entries, {added_count} net new from the 204-entry baseline; "
        f"{len(papers)} papers and {len(expansion_author_ids)} expansion author records."
    )


if __name__ == "__main__":
    main()
