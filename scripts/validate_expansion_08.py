#!/usr/bin/env python3
"""Validate the 0.8 breadth expansion and adaptive public map."""
from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "public-data.json"
SEED_PATH = ROOT / "data" / "expansion-08-seed.json"
DOCS = ROOT / "docs"
ALLOWED_RELEASES = {"0.8-expansion-alpha", "0.9-observations-alpha", "0.10-practice-safety-alpha", "0.11-visual-map-alpha", "0.12-practitioner-intake-alpha", "0.13-expertise-observations-alpha", "0.14-snowden-cynefin-alpha"}
BASELINE_COUNT = 204
MINIMUM_ADDED = 200
EXPECTED_PUBLIC_COUNT = 407
EXPECTED_PAPERS = 89
EXPECTED_NEW_PEOPLE = 107
EXPECTED_VOLUMES = 4
CORPUS_ID = "corpus_foundational_papers_2024"
FRAMING_IDS = {
    CORPUS_ID,
    "approach_family_metasystem_transition_theory",
    "comparator_corpus_principia_cybernetica_web_dictionary",
}


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


def normalise(value: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", value.casefold())).strip()


def main() -> int:
    errors = []
    if not SEED_PATH.exists():
        errors.append("data/expansion-08-seed.json is missing")

    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    meta = data.get("meta", {})
    expansion = data.get("expansion_08", {})
    redirects = data.get("canonical_redirects", {})
    canonical = lambda node_id: redirects.get(node_id, node_id)
    nodes = {node["id"]: node for node in data.get("nodes", [])}
    public_nodes = [
        node for node in data.get("nodes", [])
        if node.get("public_visibility") == "public" and canonical(node["id"]) == node["id"]
    ]
    public_ids = {node["id"] for node in public_nodes}
    sources = {source["id"] for source in data.get("sources", [])}
    edges = data.get("edges", [])

    if meta.get("release") not in ALLOWED_RELEASES:
        errors.append(f"meta.release must be one of {sorted(ALLOWED_RELEASES)}")
    if len(public_nodes) < EXPECTED_PUBLIC_COUNT:
        errors.append(f"expected at least {EXPECTED_PUBLIC_COUNT} canonical public entries, found {len(public_nodes)}")
    if meta.get("public_entry_count") != len(public_nodes):
        errors.append("meta.public_entry_count does not match canonical public entries")
    expected_added = EXPECTED_PUBLIC_COUNT - BASELINE_COUNT
    added = expansion.get("net_new_public_entries")
    if added != expected_added or added < MINIMUM_ADDED:
        errors.append(f"0.8 must retain {expected_added} net new public entries; found {added}")
    if meta.get("expansion_08_added_count") != expected_added:
        errors.append("meta.expansion_08_added_count no longer records the 0.8 increase")
    if expansion.get("official_papers") != EXPECTED_PAPERS:
        errors.append("expansion_08.official_papers must be 89")
    if expansion.get("new_bibliographic_people") != EXPECTED_NEW_PEOPLE:
        errors.append("expansion_08.new_bibliographic_people must be 107")
    if expansion.get("collection_volumes") != EXPECTED_VOLUMES:
        errors.append("expansion_08.collection_volumes must be 4")

    paper_ids = {f"publication_fpcs_{number:03d}" for number in range(1, EXPECTED_PAPERS + 1)}
    missing_papers = paper_ids - public_ids
    if missing_papers:
        errors.append(f"missing official collection paper entries: {sorted(missing_papers)}")
    volume_ids = {f"publication_fpcs_volume_{number}" for number in range(1, EXPECTED_VOLUMES + 1)}
    missing_volumes = volume_ids - public_ids
    if missing_volumes:
        errors.append(f"missing collection volume entries: {sorted(missing_volumes)}")
    missing_framing = FRAMING_IDS - public_ids
    if missing_framing:
        errors.append(f"missing reviewed framing entries: {sorted(missing_framing)}")

    if redirects.get("concept_evolutionary_cybernetics") != "tradition_evolutionary_cybernetics":
        errors.append("the duplicate evolutionary-cybernetics concept is not redirected to the canonical tradition")
    if "concept_evolutionary_cybernetics" in public_ids:
        errors.append("the duplicate evolutionary-cybernetics concept remains canonical and public")

    expansion_people = [
        node for node in public_nodes
        if node.get("entity_type") == "person"
        and "official_collection_author_inventory" in str(node.get("inclusion_reason"))
    ]
    if len(expansion_people) != EXPECTED_NEW_PEOPLE:
        errors.append(f"expected {EXPECTED_NEW_PEOPLE} new bibliographic people, found {len(expansion_people)}")

    expansion_ids = paper_ids | volume_ids | FRAMING_IDS | {node["id"] for node in expansion_people}
    for node_id in sorted(expansion_ids):
        node = nodes.get(node_id)
        if not node:
            continue
        description = node.get("canonical_definition") or node.get("description") or node.get("public_stub_text") or ""
        if len(str(description).split()) < 12:
            errors.append(f"expansion entry has an unusably short description: {node_id}")
        source_ids = parse(node.get("source_ids"))
        if not source_ids:
            errors.append(f"expansion entry has no source IDs: {node_id}")
        unknown_sources = set(source_ids) - sources
        if unknown_sources:
            errors.append(f"expansion entry has unknown sources: {node_id} -> {sorted(unknown_sources)}")
        if node.get("publication_level") not in {"described", "profile"}:
            errors.append(f"expansion entry is not readable in the public atlas: {node_id}")

    labels = defaultdict(list)
    for node in public_nodes:
        labels[normalise(node.get("label", ""))].append(node["id"])
    duplicates = {label: ids for label, ids in labels.items() if label and len(ids) > 1}
    if duplicates:
        errors.append(f"duplicate canonical public labels remain: {duplicates}")

    relation_types = {item.get("relation_type") for item in data.get("relation_types", [])}
    for relation_type in {"authored_by", "coauthored_with", "part_of"}:
        if relation_type not in relation_types:
            errors.append(f"missing expansion relation type: {relation_type}")

    authored_by = defaultdict(list)
    paper_volume = defaultdict(list)
    volume_corpus = defaultdict(list)
    for edge in edges:
        if edge.get("relation_type") == "authored_by" and edge.get("source") in paper_ids:
            authored_by[edge["source"]].append(edge)
        if (
            edge.get("relation_type") == "part_of"
            and edge.get("source") in paper_ids
            and edge.get("target") in volume_ids
        ):
            paper_volume[edge["source"]].append(edge)
        if edge.get("relation_type") == "part_of" and edge.get("source") in volume_ids and edge.get("target") == CORPUS_ID:
            volume_corpus[edge["source"]].append(edge)
    for paper_id in sorted(paper_ids):
        if not authored_by[paper_id]:
            errors.append(f"paper has no authored_by relation: {paper_id}")
        if len(paper_volume[paper_id]) != 1:
            errors.append(f"paper must belong to exactly one collection volume: {paper_id}")
    for volume_id in sorted(volume_ids):
        if len(volume_corpus[volume_id]) != 1:
            errors.append(f"volume must belong to the collection exactly once: {volume_id}")

    index = (DOCS / "index.html").read_text(encoding="utf-8")
    home_map_markers = [
        'data-view-link="map" data-map-mode="all">Full public map</button>',
        'data-view-link="map" data-map-mode="all">Full public map</a>',
    ]
    if not any(marker in index for marker in home_map_markers):
        errors.append("the home page does not open the full public map explicitly")
    if '<option value="all" selected>Full public map</option>' not in index:
        errors.append("the map itself does not default to the full public map")
    if meta.get("release") == "0.13-expertise-observations-alpha" and any(
        marker in index for marker in ("data-curator-dot=", "curator-secret-dot", "curator-notebook-link", "discreet-note-link")
    ):
        errors.append("an obsolete hidden working route remains in the public page")

    app = (DOCS / "assets" / "app.js").read_text(encoding="utf-8")
    for marker in [
        "mapVisibleEdge", "previousAngle", "animateMapTransition", "moveMapToFocus",
        "renderMap({ fit: !keepsWholeMap, focus: keepsWholeMap })",
    ]:
        if marker not in app:
            errors.append(f"adaptive-map marker missing from app.js: {marker}")
    if "button.dataset.mapMode === 'all'" not in app and "followInternalAnchor" not in app:
        errors.append("the full-map navigation hook is missing")
    css = (DOCS / "assets" / "site-enhancements.css").read_text(encoding="utf-8")
    css_markers = ["graph-edge.contextual", "graph-node-group"]
    if meta.get("release") in {"0.8-expansion-alpha", "0.9-observations-alpha"}:
        css_markers.append("discreet-note-link")
    for marker in css_markers:
        if marker not in css:
            errors.append(f"0.8 map CSS marker missing: {marker}")

    snapshot = data.get("graph_snapshot", {})
    if snapshot.get("public_node_count") != len(public_nodes):
        errors.append("graph_snapshot.public_node_count does not match the public graph")

    type_counts = Counter(node.get("entity_type", "unknown") for node in public_nodes)
    if errors:
        print("EXPANSION 0.8 VALIDATION FAILED", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("EXPANSION 0.8 VALIDATION PASSED")
    print(f"- canonical public entries: {len(public_nodes)}")
    print(f"- net new entries over 0.7: {added}")
    print(f"- official collection papers: {len(paper_ids)}")
    print(f"- new bibliographic people: {len(expansion_people)}")
    print(f"- collection volumes: {len(volume_ids)}")
    print(f"- entry types: {dict(sorted(type_counts.items()))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
