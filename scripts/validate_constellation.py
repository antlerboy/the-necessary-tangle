#!/usr/bin/env python3
"""Validate the 0.7 constellation release contract."""
from __future__ import annotations

import json
import sys
from collections import Counter, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "public-data.json"
EXPECTED_RELEASE = "0.7-constellation-alpha"
PRINCIPIA_IDS = {
    "person_cliff_joslyn", "tradition_evolutionary_cybernetics", "person_francis_heylighen",
    "concept_global_brain", "concept_metasystem_transition", "organisation_principia_cybernetica_project",
    "publication_principia_cybernetica_web", "concept_semantic_network", "person_valentin_turchin",
}
EXPECTED = {
    "public_node_count": 204,
    "substantive_edge_count": 96,
    "substantive_pair_count": 94,
    "connected_node_count": 77,
    "isolated_node_count": 127,
    "component_count": 129,
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
    public = {n["id"]: n for n in data.get("nodes", []) if n.get("public_visibility") == "public" and canonical(n["id"]) == n["id"]}
    excluded = {"classification", "evidence", "documentary", "legacy"}
    neighbours = {nid: set() for nid in public}
    edges = 0
    pairs = set()
    for e in data.get("edges", []):
        s, t = canonical(e.get("source")), canonical(e.get("target"))
        substantive = e.get("relation_family") not in excluded and e.get("relation_type") != "legacy_association_unspecified" and e.get("claim_status") != "legacy_unresolved"
        if s not in public or t not in public or s == t or not substantive:
            continue
        edges += 1
        pairs.add(tuple(sorted((s, t))))
        neighbours[s].add(t); neighbours[t].add(s)
    isolates = {nid for nid, ns in neighbours.items() if not ns}
    remaining = set(public); sizes = []
    while remaining:
        start = remaining.pop(); q = deque([start]); size = 1
        while q:
            x = q.popleft()
            for y in neighbours[x]:
                if y in remaining:
                    remaining.remove(y); q.append(y); size += 1
        sizes.append(size)
    sizes.sort(reverse=True)
    return {
        "public_node_count": len(public), "substantive_edge_count": edges,
        "substantive_pair_count": len(pairs), "connected_node_count": len(public) - len(isolates),
        "isolated_node_count": len(isolates), "component_count": len(sizes),
        "largest_component_node_count": sizes[0] if sizes else 0,
        "isolates_by_entity_type": dict(Counter(public[nid].get("entity_type", "unknown") for nid in isolates)),
    }, neighbours


def main() -> int:
    errors = []
    data = json.loads(DATA.read_text(encoding="utf-8"))
    meta = data.get("meta", {})
    nodes = {n["id"]: n for n in data.get("nodes", [])}
    sources = {s["id"] for s in data.get("sources", [])}

    if meta.get("release") != EXPECTED_RELEASE:
        errors.append(f"release must be {EXPECTED_RELEASE}")
    if meta.get("author_role") != "curator":
        errors.append("author_role must be curator")
    if "do not call him creator or editor" not in meta.get("curation_language_rule", ""):
        errors.append("curation language rule is missing")

    for nid in sorted(PRINCIPIA_IDS):
        node = nodes.get(nid)
        if not node:
            errors.append(f"missing Principia entry: {nid}")
            continue
        if node.get("public_visibility") != "public":
            errors.append(f"Principia entry is not public: {nid}")
        if not parse(node.get("source_ids")):
            errors.append(f"Principia entry has no sources: {nid}")

    actual, neighbours = graph_snapshot(data)
    for key, value in EXPECTED.items():
        if actual.get(key) != value:
            errors.append(f"graph {key}={actual.get(key)!r}, expected {value!r}")
    recorded = data.get("graph_snapshot", {})
    for key, value in actual.items():
        if recorded.get(key) != value:
            errors.append(f"recorded graph_snapshot differs for {key}")

    categories = data.get("emergent_categories", [])
    if len(categories) != 6:
        errors.append(f"expected six emergent categories, found {len(categories)}")
    category_members = []
    for category in categories:
        members = category.get("member_node_ids") or category.get("members") or []
        category_members.extend(members)
    if len(category_members) != len(set(category_members)):
        errors.append("emergent category membership overlaps")
    connected = {nid for nid, ns in neighbours.items() if ns}
    if set(category_members) != connected:
        errors.append("emergent categories do not cover exactly the connected public graph")

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
    for element_id in ["mapCategory", "mapShowLabels", "mapZoomOut", "mapZoomIn", "mapZoomStatus", "mapCategoryNote", "membershipForm", "membershipStatus"]:
        if f'id="{element_id}"' not in index:
            errors.append(f"missing 0.7 interface element #{element_id}")
    if 'class="curator-notebook-link"' not in index or '/issues/2' not in index:
        errors.append("curator notebook link is missing")

    app = (ROOT / "docs" / "assets" / "app.js").read_text(encoding="utf-8")
    for marker in ["zoomMapAt", "emergentCategories", "membershipForm", "human sponsor"]:
        if marker not in app:
            errors.append(f"app.js missing 0.7 marker: {marker}")
    if "document.querySelector('.curator-notebook')" in app:
        errors.append("obsolete curator-notebook query remains in app.js")

    css_path = ROOT / "docs" / "assets" / "site-enhancements.css"
    css = css_path.read_text(encoding="utf-8") if css_path.exists() else ""
    for marker in ["category-halo", "membership-grid", "curator-notebook-link"]:
        if marker not in css:
            errors.append(f"site-enhancements.css missing 0.7 marker: {marker}")

    template = ROOT / ".github" / "ISSUE_TEMPLATE" / "membership.yml"
    if not template.exists():
        errors.append("membership issue template is missing")

    if errors:
        print("CONSTELLATION 0.7 VALIDATION FAILED", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("CONSTELLATION 0.7 VALIDATION PASSED")
    print(json.dumps(actual, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
