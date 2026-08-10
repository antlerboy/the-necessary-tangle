#!/usr/bin/env python3
"""Reproduce the first community pass used for release 0.7.

The algorithm detects communities. A curator names and interprets them. The two
operations are deliberately separate: a cluster is an output of a bounded graph,
not a natural kind or a self-explaining intellectual school.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    import networkx as nx
except ImportError as exc:  # pragma: no cover - useful error outside CI
    raise SystemExit(
        "networkx is required for this optional analysis. "
        "Run: python3 -m pip install -r requirements-analysis.txt"
    ) from exc

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "public-data.json"
OUTPUT_PATH = ROOT / "documentation" / "emergent-categories-analysis.json"
SEED = 1
RESOLUTION = 1.0
EXCLUDED_FAMILIES = {"classification", "evidence", "documentary", "legacy"}


def substantive(edge: dict[str, Any]) -> bool:
    return (
        edge.get("relation_family") not in EXCLUDED_FAMILIES
        and edge.get("relation_type") != "legacy_association_unspecified"
        and edge.get("claim_status") != "legacy_unresolved"
    )


def analyse(data: dict[str, Any]) -> dict[str, Any]:
    redirects = data.get("canonical_redirects", {})
    canonical = lambda value: redirects.get(value, value)
    nodes = {
        node["id"]: node
        for node in data.get("nodes", [])
        if node.get("public_visibility") == "public"
        and canonical(node["id"]) == node["id"]
    }

    graph = nx.Graph()
    graph.add_nodes_from(nodes)
    edge_record_count = 0
    for edge in data.get("edges", []):
        source = canonical(edge.get("source"))
        target = canonical(edge.get("target"))
        if source not in nodes or target not in nodes or source == target or not substantive(edge):
            continue
        edge_record_count += 1
        graph.add_edge(source, target)

    communities = list(
        nx.community.louvain_communities(
            graph,
            seed=SEED,
            resolution=RESOLUTION,
            weight=None,
        )
    )
    communities.sort(
        key=lambda members: (
            -len(members),
            min(nodes[node_id]["label"].casefold() for node_id in members),
        )
    )

    curated = data.get("emergent_categories", [])
    curated_sets = {item["id"]: set(item.get("member_node_ids", [])) for item in curated}
    used_curated: set[str] = set()
    rendered = []
    for index, members in enumerate(communities, start=1):
        if len(members) == 1:
            continue
        best_id = None
        best_jaccard = -1.0
        for category_id, expected in curated_sets.items():
            if category_id in used_curated:
                continue
            union = members | expected
            score = len(members & expected) / len(union) if union else 1.0
            if score > best_jaccard:
                best_id = category_id
                best_jaccard = score
        if best_id:
            used_curated.add(best_id)
        category = next((item for item in curated if item["id"] == best_id), None)
        ranked = sorted(
            members,
            key=lambda node_id: (-graph.degree(node_id), nodes[node_id]["label"].casefold()),
        )
        rendered.append(
            {
                "detected_index": index,
                "detected_size": len(members),
                "curated_category_id": best_id,
                "curated_label": (category or {}).get("label"),
                "jaccard": round(best_jaccard, 6),
                "exact_member_match": best_jaccard == 1.0,
                "hubs": [
                    {
                        "id": node_id,
                        "label": nodes[node_id]["label"],
                        "degree": graph.degree(node_id),
                    }
                    for node_id in ranked[:6]
                ],
                "member_node_ids": sorted(members),
            }
        )

    components = sorted(nx.connected_components(graph), key=len, reverse=True)
    snapshot = data.get("graph_snapshot", {})
    report = {
        "release": data.get("meta", {}).get("release"),
        "method": {
            "graph": "canonical public entries and substantive public-public connections",
            "projection": "simple undirected unweighted graph; parallel typed statements collapse to one pair for clustering",
            "excluded_relation_families": sorted(EXCLUDED_FAMILIES),
            "excluded_relation_type": "legacy_association_unspecified",
            "excluded_status": "legacy_unresolved",
            "algorithm": "NetworkX louvain_communities",
            "networkx_version": nx.__version__,
            "seed": SEED,
            "resolution": RESOLUTION,
            "interpretation_rule": "The algorithm groups; the curator names and interprets. Categories remain provisional and boundary-dependent.",
        },
        "counts": {
            "public_nodes": graph.number_of_nodes(),
            "substantive_edge_records": edge_record_count,
            "unique_undirected_pairs": graph.number_of_edges(),
            "connected_nodes": sum(1 for node_id in graph if graph.degree(node_id) > 0),
            "isolated_nodes": nx.number_of_isolates(graph),
            "components": nx.number_connected_components(graph),
            "largest_component_nodes": len(components[0]) if components else 0,
            "detected_non_singleton_communities": len(rendered),
        },
        "snapshot_consistency": {
            "public_nodes": snapshot.get("public_node_count") == graph.number_of_nodes(),
            "substantive_edge_records": snapshot.get("substantive_edge_count") == edge_record_count,
            "unique_undirected_pairs": snapshot.get("substantive_pair_count") == graph.number_of_edges(),
            "connected_nodes": snapshot.get("connected_node_count") == sum(1 for node_id in graph if graph.degree(node_id) > 0),
            "isolated_nodes": snapshot.get("isolated_node_count") == nx.number_of_isolates(graph),
            "components": snapshot.get("component_count") == nx.number_connected_components(graph),
            "largest_component_nodes": snapshot.get("largest_component_node_count") == (len(components[0]) if components else 0),
        },
        "curated_category_consistency": {
            "all_detected_groups_exactly_matched": all(item["exact_member_match"] for item in rendered),
            "all_curated_groups_used": len(used_curated) == len(curated_sets),
        },
        "communities": rendered,
    }
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help=f"write {OUTPUT_PATH.relative_to(ROOT)}")
    parser.add_argument("--check", action="store_true", help="fail when snapshot or curated memberships no longer match")
    args = parser.parse_args()

    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    report = analyse(data)
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.write:
        OUTPUT_PATH.write_text(rendered, encoding="utf-8")
        print(f"Wrote {OUTPUT_PATH.relative_to(ROOT)}")
    else:
        print(rendered, end="")

    if args.check:
        checks = list(report["snapshot_consistency"].values()) + list(report["curated_category_consistency"].values())
        if not all(checks):
            print("Emergent-category analysis no longer matches the published 0.7 snapshot.", file=sys.stderr)
            return 1
        print("Emergent-category analysis matches the published 0.7 snapshot.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
