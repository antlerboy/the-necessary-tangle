#!/usr/bin/env python3
"""Validate the 0.16 Grammar connections, presentation repair and vision audit."""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

from apply_iteration_09 import graph_metrics
from apply_iteration_16 import CONNECTIONS, GRAMMAR_BOOK, LAW_IDS, RELEASE
from apply_relational_depth_16 import (
    PRACTICE_LINKS,
    SOURCE_RECORDS,
    calculate_relational_depth,
)

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "public-data.json"
GENERATED = "2026-08-14"
PUBLIC_URL = "https://transduction.systems/"
PATTERN_IDS = {
    "concept_boundary",
    "concept_complexity",
    "concept_difference",
    "concept_dynamics_of_loops",
    "concept_emergence",
    "concept_holism",
    "concept_modelling",
    "concept_relating",
    "concept_uncertainty",
}


def parse(value):
    if isinstance(value, (list, dict)):
        return value
    if not value:
        return []
    try:
        return json.loads(value)
    except (TypeError, json.JSONDecodeError):
        return []


def main() -> int:
    errors: list[str] = []
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    meta = data.get("meta", {})
    nodes = {node.get("id"): node for node in data.get("nodes", []) if node.get("id")}
    public_ids = {
        node_id for node_id, node in nodes.items()
        if node.get("public_visibility") == "public"
        and data.get("canonical_redirects", {}).get(node_id, node_id) == node_id
    }
    edges = data.get("edges", [])
    relation_types = {item.get("relation_type") for item in data.get("relation_types", [])}

    if meta.get("release") != RELEASE:
        errors.append(f"meta.release must be {RELEASE}")
    if meta.get("generated") != GENERATED:
        errors.append(f"meta.generated must be {GENERATED}")
    if meta.get("project_url") != PUBLIC_URL:
        errors.append("custom public URL is not canonical in release metadata")
    if set(LAW_IDS) - public_ids:
        errors.append(f"Grammar laws missing from the public graph: {sorted(set(LAW_IDS) - public_ids)}")
    if len(LAW_IDS) != 33:
        errors.append("the release law register must contain exactly 33 laws and principles")
    if "concept_black_box" not in public_ids:
        errors.append("the Black box concept is missing")

    crosswalk = [edge for edge in edges if str(edge.get("id", "")).startswith("e16_grammar_crosswalk_")]
    presents = [edge for edge in edges if str(edge.get("id", "")).startswith("e16_grammar_presents_")]
    if len(crosswalk) != len(CONNECTIONS) or len(crosswalk) < 160:
        errors.append(f"expected the complete rich Grammar crosswalk, found {len(crosswalk)} statements")
    if meta.get("grammar_crosswalk_connection_count") != len(crosswalk):
        errors.append("Grammar crosswalk count in release metadata is stale")
    if len(presents) != 33:
        errors.append(f"expected 33 book-to-law presentation statements, found {len(presents)}")

    incident = Counter()
    for edge in crosswalk:
        if edge.get("source") not in public_ids or edge.get("target") not in public_ids:
            errors.append(f"crosswalk has a non-public endpoint: {edge.get('id')}")
        if edge.get("relation_type") not in relation_types:
            errors.append(f"crosswalk uses an unregistered relation type: {edge.get('id')}")
        if edge.get("claim_status") != "provisional" or edge.get("public_review_label") != "provisional conceptual crosswalk":
            errors.append(f"crosswalk does not expose provisional status: {edge.get('id')}")
        if not edge.get("plain_phrase") or not edge.get("scope_conditions") or not parse(edge.get("source_ids")):
            errors.append(f"crosswalk statement is not inspectable: {edge.get('id')}")
        for law_id in LAW_IDS:
            if law_id in {edge.get("source"), edge.get("target")}:
                incident[law_id] += 1

    for law_id in LAW_IDS:
        if incident[law_id] < 4:
            errors.append(f"Grammar law lacks rich semantic connections: {law_id} ({incident[law_id]})")
        matching = [
            edge for edge in presents
            if edge.get("source") == GRAMMAR_BOOK and edge.get("target") == law_id
        ]
        if len(matching) != 1 or matching[0].get("claim_status") != "accepted" or matching[0].get("relation_type") != "presents":
            errors.append(f"source-backed book membership is missing for {law_id}")

    patterns_reached = {
        endpoint
        for edge in crosswalk
        for endpoint in (edge.get("source"), edge.get("target"))
        if endpoint in PATTERN_IDS
    }
    if patterns_reached != PATTERN_IDS:
        errors.append(f"crosswalk does not reach all nine Grammar patterns: {sorted(PATTERN_IDS - patterns_reached)}")

    journeys = {item.get("id"): item for item in data.get("journeys", []) if item.get("id")}
    journey = journeys.get("journey_grammar_principles_in_connection")
    if not journey or len(journey.get("steps", [])) != 8:
        errors.append("Grammar web guided journey is missing or incomplete")
    elif any(step.get("node_id") not in public_ids for step in journey.get("steps", [])):
        errors.append("Grammar journey contains a non-public step")

    if data.get("ai_observations", {}).get("release") != RELEASE:
        errors.append("AI observations do not identify the current release")
    if data.get("ai_observations", {}).get("metrics") != graph_metrics(data):
        errors.append("AI observation metrics do not match the 0.16 graph")
    for inherited in ("reading_list_inventory", "reading_list_coverage", "core_systems_practice"):
        if data.get(inherited, {}).get("release") != RELEASE:
            errors.append(f"{inherited} still identifies an earlier release")

    relational = data.get("relational_depth", {})
    recalculated = calculate_relational_depth(data)
    if relational != recalculated:
        errors.append("relational-depth measures do not match the current public graph")
    aggregate = relational.get("aggregate", {})
    if aggregate.get("reader_connected_entries") != len(public_ids):
        errors.append("not every canonical public entry has a reader connection")
    if aggregate.get("connection_bands", {}).get("unconnected", 0) != 0:
        errors.append("the relational-depth queue still contains unconnected entries")
    if meta.get("reader_connected_entry_count") != len(public_ids):
        errors.append("reader-connected entry count in release metadata is stale")
    if meta.get("relational_crosswalk_connection_count", 0) < 280:
        errors.append("the graph-wide relational crosswalk is incomplete")
    if meta.get("source_backed_author_link_count", 0) < 15:
        errors.append("the supplied author material has not produced the expected source-backed drafts")
    source_ids = {source.get("id") for source in data.get("sources", [])}
    if {source["id"] for source in SOURCE_RECORDS} - source_ids:
        errors.append("one or more supplied author source records are missing")
    depth_by_node = relational.get("by_node", {})
    if set(PRACTICE_LINKS) - set(depth_by_node):
        errors.append("one or more intervention skills are missing from relational-depth measures")
    for node_id in PRACTICE_LINKS:
        depth = depth_by_node.get(node_id, {})
        if depth.get("reader_connections", 0) < 3 or depth.get("distinct_reader_families", 0) < 2:
            errors.append(f"intervention skill lacks multiple typed routes: {node_id}")
    fpcs_contents = [edge for edge in edges if str(edge.get("id", "")).startswith("e16_fpcs_contents_")]
    if len(fpcs_contents) < 93 or any(edge.get("relation_family") != "documentary" for edge in fpcs_contents):
        errors.append("Foundational Papers contents are not exposed as documentary reader statements")

    docs_json = json.loads((ROOT / "docs" / "assets" / "public-data.json").read_text(encoding="utf-8"))
    if docs_json != data:
        errors.append("browser JSON is not identical to canonical public data")

    index = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    app = (ROOT / "docs" / "assets" / "app.js").read_text(encoding="utf-8")
    css = (ROOT / "docs" / "assets" / "site-enhancements.css").read_text(encoding="utf-8")
    base_css = (ROOT / "docs" / "assets" / "styles.css").read_text(encoding="utf-8")
    for marker in (
        f'<link rel="canonical" href="{PUBLIC_URL}">',
        "journey_grammar_principles_in_connection",
        "documentation/original-vision-audit.md",
        "documentation/relational-depth.md",
        'id="browseConnectionDepth"',
        'id="relationalDepthMetrics"',
        "assets/styles.css?v=0.16.2-visual",
        "assets/site-enhancements.css?v=0.16.2-visual",
        "assets/app.js?v=0.16.2-visual",
    ):
        if marker not in index:
            errors.append(f"0.16 interface marker is missing: {marker}")
    if "function publicEntryEdge(edge)" not in app or ".filter(publicEntryEdge)" not in app:
        errors.append("full entries still suppress meaningful documentary public connections")
    for marker in ("relationalDepthByNode", "browseConnectionDepth", "connectionBandLabel", "!['classification', 'documentary', 'evidence', 'legacy']", "focusEdges.length <= 6"):
        if marker not in app:
            errors.append(f"relational-depth reader behaviour is missing: {marker}")
    for marker in ("/* 0.16 relational presentation", ".badge.status-profile", ".badge.status-stub", ".relational-depth-panel"):
        if marker not in css:
            errors.append(f"presentation repair is missing: {marker}")
    for marker in (".metrics {", ".smart-search {", ".card-grid.three", ".ask-shell {", ".contribution-form {", ".hidden {", "@media print"):
        if marker not in base_css:
            errors.append(f"coherent base presentation is missing: {marker}")

    update_url = "https://github.com/antlerboy/the-necessary-tangle/issues/2"
    if index.count(update_url) != 1 or ".update-thread-dot {" not in css or "position: fixed" not in css:
        errors.append("the discreet bottom-right update dot has not been preserved")

    audit = ROOT / "documentation" / "original-vision-audit.md"
    if not audit.exists() or audit.stat().st_size < 7000:
        errors.append("original vision audit is missing or implausibly small")
    else:
        audit_text = audit.read_text(encoding="utf-8")
        for marker in ("Non-negotiable design commitments", "Delivery assessment", "Ordered work", "Definition of the original vision"):
            if marker not in audit_text:
                errors.append(f"vision audit is missing: {marker}")

    relational_doc = ROOT / "documentation" / "relational-depth.md"
    if not relational_doc.exists() or relational_doc.stat().st_size < 6000:
        errors.append("relational-depth programme is missing or implausibly small")
    else:
        relational_text = relational_doc.read_text(encoding="utf-8")
        for marker in ("The required shape by entity", "How enrichment proceeds", "What a corpus pass means", "First priority queue", "Structural bands"):
            if marker not in relational_text:
                errors.append(f"relational-depth programme is missing: {marker}")

    citation = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    if f"version: {RELEASE}" not in citation or f"url: {PUBLIC_URL}" not in citation:
        errors.append("citation metadata does not identify release 0.16 and the custom domain")
    if "Release 0.16 contains" not in readme or "original-vision-audit.md" not in readme or "relational-depth.md" not in readme:
        errors.append("README does not identify the current release and vision audit")
    if readme.count("The [reading-list depth map]") != 1:
        errors.append("README contains a duplicated reading-list depth paragraph")

    if errors:
        print("0.16 validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(json.dumps({
        "release": RELEASE,
        "public_entries": meta.get("public_entry_count"),
        "grammar_laws": len(LAW_IDS),
        "grammar_crosswalk_statements": len(crosswalk),
        "minimum_semantic_connections_per_law": min(incident.values()),
        "grammar_patterns_reached": len(patterns_reached),
        "reader_connected_entries": aggregate.get("reader_connected_entries"),
        "connection_bands": aggregate.get("connection_bands"),
        "relational_crosswalk_statements": meta.get("relational_crosswalk_connection_count"),
        "guided_journeys": meta.get("journey_count"),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
