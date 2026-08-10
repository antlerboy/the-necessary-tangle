#!/usr/bin/env python3
"""Recalculate the public graph snapshot after all release overlays have run."""
from __future__ import annotations

import json
from collections import Counter, deque
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "public-data.json"
DOCS_ASSETS = ROOT / "docs" / "assets"


def calculate(data: dict[str, Any]) -> dict[str, Any]:
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

    isolated = {node_id for node_id, adjacent in neighbours.items() if not adjacent}
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
        "connected_node_count": len(public) - len(isolated),
        "isolated_node_count": len(isolated),
        "component_count": len(component_sizes),
        "largest_component_node_count": component_sizes[0] if component_sizes else 0,
        "isolates_by_entity_type": dict(
            Counter(public[node_id].get("entity_type", "unknown") for node_id in isolated)
        ),
    }


def write(data: dict[str, Any]) -> None:
    rendered = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    DATA_PATH.write_text(rendered, encoding="utf-8")
    DOCS_ASSETS.mkdir(parents=True, exist_ok=True)
    (DOCS_ASSETS / "public-data.json").write_text(rendered, encoding="utf-8")
    (DOCS_ASSETS / "public-data.js").write_text(
        "window.TANGLE_DATA = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n",
        encoding="utf-8",
    )


def main() -> None:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    data["graph_snapshot"] = calculate(data)
    write(data)
    print("Refreshed public graph snapshot:", json.dumps(data["graph_snapshot"], sort_keys=True))


if __name__ == "__main__":
    main()
