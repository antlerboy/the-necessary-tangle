#!/usr/bin/env python3
"""Validate the enduring 0.7 constellation core inside later releases."""
from __future__ import annotations

import json
import sys
from collections import Counter, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "public-data.json"
ALLOWED_RELEASES = {"0.7-constellation-alpha", "0.8-expansion-alpha", "0.9-observations-alpha", "0.10-practice-safety-alpha", "0.11-visual-map-alpha", "0.12-practitioner-intake-alpha", "0.13-expertise-observations-alpha", "0.14-snowden-cynefin-alpha", "0.15-ing-reading-practice-alpha", "0.16-grammar-connections-presentation-alpha", "0.17-public-intake-lineage-alpha", "0.18-navigable-tangle-alpha", "0.19-living-marks-alpha"}
PRINCIPIA_IDS = {
    "person_cliff_joslyn", "tradition_evolutionary_cybernetics", "person_francis_heylighen",
    "concept_global_brain", "concept_metasystem_transition", "organisation_principia_cybernetica_project",
    "publication_principia_cybernetica_web", "concept_semantic_network", "person_valentin_turchin",
}
CORE_MINIMUMS = {
    "public_node_count": 204,
    "substantive_edge_count": 96,
    "substantive_pair_count": 94,
    "connected_node_count": 77,
    "largest_component_node_count": 75,
}
ROLE_IDS = ["participant", "contributor", "research_collaborator", "domain_steward", "curator"]


def parse(value, fallback=None):
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


def graph_snapshot(data):
    redirects = data.get("canonical_redirects", {})
    canonical = lambda value: redirects.get(value, value)
    public = {
        node["id"]: node for node in data.get("nodes", [])
        if node.get("public_visibility") == "public" and canonical(node["id"]) == node["id"]
    }
    excluded = {"classification", "evidence", "documentary", "legacy"}
    neighbours = {node_id: set() for node_id in public}
    edges = 0
    pairs = set()
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
        edges += 1
        pairs.add(tuple(sorted((source, target))))
        neighbours[source].add(target)
        neighbours[target].add(source)
    isolates = {node_id for node_id, adjacent in neighbours.items() if not adjacent}
    remaining = set(public)
    sizes = []
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
        sizes.append(size)
    sizes.sort(reverse=True)
    return {
        "public_node_count": len(public),
        "substantive_edge_count": edges,
        "substantive_pair_count": len(pairs),
        "connected_node_count": len(public) - len(isolates),
        "isolated_node_count": len(isolates),
        "component_count": len(sizes),
        "largest_component_node_count": sizes[0] if sizes else 0,
        "isolates_by_entity_type": dict(
            Counter(public[node_id].get("entity_type", "unknown") for node_id in isolates)
        ),
    }, public, neighbours


def main() -> int:
    errors = []
    data = json.loads(DATA.read_text(encoding="utf-8"))
    meta = data.get("meta", {})
    nodes = {node["id"]: node for node in data.get("nodes", [])}
    sources = {source["id"] for source in data.get("sources", [])}

    if meta.get("release") not in ALLOWED_RELEASES:
        errors.append(f"release must be one of {sorted(ALLOWED_RELEASES)}")
    if meta.get("author_role") != "curator":
        errors.append("author_role must be curator")
    if "do not call him creator or editor" not in meta.get("curation_language_rule", ""):
        errors.append("curation language rule is missing")

    for node_id in sorted(PRINCIPIA_IDS):
        node = nodes.get(node_id)
        if not node:
            errors.append(f"missing Principia core entry: {node_id}")
            continue
        if node.get("public_visibility") != "public":
            errors.append(f"Principia core entry is not public: {node_id}")
        if not parse(node.get("source_ids")):
            errors.append(f"Principia core entry has no sources: {node_id}")

    actual, public, neighbours = graph_snapshot(data)
    for key, minimum in CORE_MINIMUMS.items():
        if actual.get(key, 0) < minimum:
            errors.append(f"graph regression: {key}={actual.get(key)!r}, minimum {minimum!r}")
    recorded = data.get("graph_snapshot", {})
    for key, value in actual.items():
        if recorded.get(key) != value:
            errors.append(f"recorded graph_snapshot differs for {key}")

    categories = data.get("emergent_categories", [])
    if len(categories) != 6:
        errors.append(f"expected six retained 0.7 neighbourhoods, found {len(categories)}")
    category_members = []
    for category in categories:
        members = category.get("member_node_ids") or category.get("members") or []
        if not members:
            errors.append(f"empty retained neighbourhood: {category.get('id')}")
        unknown = set(members) - set(public)
        if unknown:
            errors.append(f"retained neighbourhood has unknown members: {category.get('id')} -> {sorted(unknown)}")
        category_members.extend(members)
    if len(category_members) != len(set(category_members)):
        errors.append("retained 0.7 neighbourhood membership overlaps")

    if len(data.get("coverage_gap_categories", [])) < 3:
        errors.append("expected at least three coverage-gap categories")
    canonical_sources = data.get("canonical_source_register", [])
    if len(canonical_sources) < 9:
        errors.append("expected at least nine canonical source registrations")
    for item in canonical_sources:
        if item.get("source_id") not in sources:
            errors.append(f"canonical source register has unknown source: {item.get('source_id')}")
        for field in ("tier", "status", "use"):
            if not item.get(field):
                errors.append(f"canonical source registration missing {field}: {item.get('source_id')}")

    roles = data.get("participation_roles", [])
    if [role.get("id") for role in roles] != ROLE_IDS:
        errors.append("participation roles are missing or out of order")
    rule = data.get("automation_contribution_rule", {})
    if not rule.get("requires") or rule.get("may_merge_or_release_independently") is not False:
        errors.append("automation contribution rule must require human sponsorship/review and forbid autonomous release")

    index = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    for element_id in [
        "mapCategory", "mapShowLabels", "mapZoomOut", "mapZoomIn",
        "mapZoomStatus", "mapCategoryNote", "membershipForm", "membershipStatus",
    ]:
        if f'id="{element_id}"' not in index:
            errors.append(f"missing constellation interface element #{element_id}")
    if meta.get("release") == "0.13-expertise-observations-alpha" and any(
        marker in index for marker in ("data-curator-dot=", "curator-secret-dot", "curator-notebook-link", "discreet-note-link")
    ):
        errors.append("an obsolete hidden working route remains in the public page")

    app = (ROOT / "docs" / "assets" / "app.js").read_text(encoding="utf-8")
    semantic_zoom_releases = {
        "0.11-visual-map-alpha", "0.12-practitioner-intake-alpha", "0.13-expertise-observations-alpha",
        "0.14-snowden-cynefin-alpha", "0.15-ing-reading-practice-alpha",
        "0.16-grammar-connections-presentation-alpha", "0.17-public-intake-lineage-alpha",
        "0.18-navigable-tangle-alpha", "0.19-living-marks-alpha",
    }
    map_marker = "semanticZoomBand" if meta.get("release") in semantic_zoom_releases else "zoomMapAt"
    for marker in [map_marker, "emergentCategories", "membershipForm", "human sponsor"]:
        if marker not in app:
            errors.append(f"app.js missing constellation marker: {marker}")
    if "document.querySelector('.curator-notebook')" in app:
        errors.append("obsolete curator-notebook query remains in app.js")

    css_path = ROOT / "docs" / "assets" / "site-enhancements.css"
    css = css_path.read_text(encoding="utf-8") if css_path.exists() else ""
    css_markers = ["category-halo", "membership-grid"]
    for marker in css_markers:
        if marker not in css:
            errors.append(f"site-enhancements.css missing constellation marker: {marker}")

    template = ROOT / ".github" / "ISSUE_TEMPLATE" / "membership.yml"
    if not template.exists():
        errors.append("membership issue template is missing")

    if errors:
        print("CONSTELLATION CORE VALIDATION FAILED", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("CONSTELLATION CORE VALIDATION PASSED")
    print(json.dumps(actual, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
