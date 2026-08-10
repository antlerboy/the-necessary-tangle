#!/usr/bin/env python3
"""Validate release 0.9 feedback, AI observations, layers and source depth."""
from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "public-data.json"
DOCS = ROOT / "docs"
ALLOWED_RELEASES = {"0.9-observations-alpha", "0.10-practice-safety-alpha", "0.11-visual-map-alpha", "0.12-practitioner-intake-alpha"}
EXPECTED_PUBLIC_COUNT = 411
EXPECTED_MIN_PROFILES = 32
EXPECTED_JOURNEYS = 12
EXPECTED_MIN_SOURCES = 93
NEW_NODE_IDS = {
    "person_chris_mowles",
    "tradition_complex_responsive_processes",
    "publication_murmurations_journal",
    "publication_complexity_key_idea_business_society",
}
NEW_SOURCE_IDS = {
    "src_mowles_resources_social_complexity",
    "src_mowles_complexity_key_idea_2022",
    "src_mowles_complex_not_quite_2014",
    "src_stacey_complex_responsive_processes_2001",
    "src_mowles_organising_complex_responsive_2022",
    "src_mowles_practice_complexity_nhs_2010",
    "src_murmurations_about",
}
NEW_JOURNEY_IDS = {
    "journey_human_lineage",
    "journey_power_boundary_intervention",
    "journey_corpus_to_field",
    "journey_social_complexity",
}
PRIVATE_PATTERNS = (
    "sharepoint.com", "graph.microsoft", "mail.google", "gmail", "sandbox:/",
    "file://", "localhost", "127.0.0.1", "/mnt/data", "redquadrantltd.sharepoint",
)


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


def main() -> int:
    errors: list[str] = []
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    meta = data.get("meta", {})
    redirects = data.get("canonical_redirects", {})
    canonical = lambda node_id: redirects.get(node_id, node_id)
    nodes = {node["id"]: node for node in data.get("nodes", [])}
    public_nodes = [
        node for node in data.get("nodes", [])
        if node.get("public_visibility") == "public" and canonical(node["id"]) == node["id"]
    ]
    public_ids = {node["id"] for node in public_nodes}
    profiles = {profile.get("node_id"): profile for profile in data.get("profiles", []) if profile.get("node_id")}
    sources = {source["id"]: source for source in data.get("sources", [])}
    source_ids = set(sources)
    journeys = {journey.get("id"): journey for journey in data.get("journeys", []) if journey.get("id")}
    edges = data.get("edges", [])

    if meta.get("release") not in ALLOWED_RELEASES:
        errors.append(f"meta.release must be one of {sorted(ALLOWED_RELEASES)}")
    if len(public_nodes) < EXPECTED_PUBLIC_COUNT:
        errors.append(f"expected at least {EXPECTED_PUBLIC_COUNT} canonical public entries, found {len(public_nodes)}")
    if meta.get("public_entry_count") != len(public_nodes):
        errors.append("meta.public_entry_count does not match canonical public entries")
    if meta.get("profile_count", 0) < EXPECTED_MIN_PROFILES:
        errors.append(f"expected at least {EXPECTED_MIN_PROFILES} developed profiles")
    if len(journeys) < EXPECTED_JOURNEYS or meta.get("journey_count", 0) < EXPECTED_JOURNEYS:
        errors.append(f"expected at least {EXPECTED_JOURNEYS} guided journeys")
    if len(sources) < EXPECTED_MIN_SOURCES:
        errors.append(f"expected at least {EXPECTED_MIN_SOURCES} sources, found {len(sources)}")

    for node_id in sorted(NEW_NODE_IDS):
        node = nodes.get(node_id)
        if not node:
            errors.append(f"missing new developed entry: {node_id}")
            continue
        if node.get("public_visibility") != "public" or node.get("publication_level") != "profile":
            errors.append(f"new entry is not a public profile: {node_id}")
        if node_id not in profiles:
            errors.append(f"new entry has no developed profile: {node_id}")
        linked = set(parse(node.get("source_ids"))) | set(parse(profiles.get(node_id, {}).get("source_ids")))
        if not linked:
            errors.append(f"new entry has no sources: {node_id}")
        unknown = linked - source_ids
        if unknown:
            errors.append(f"new entry has unknown sources {sorted(unknown)}: {node_id}")

    for source_id in sorted(NEW_SOURCE_IDS):
        source = sources.get(source_id)
        if not source:
            errors.append(f"missing feedback source: {source_id}")
            continue
        if not source.get("url") or not str(source.get("url")).startswith("https://"):
            errors.append(f"feedback source lacks a public HTTPS link: {source_id}")
        if not source.get("notes") or not source.get("review_status"):
            errors.append(f"feedback source lacks use/caution metadata: {source_id}")

    source_urls = [str(source.get("url") or "").rstrip("/") for source in sources.values() if source.get("url")]
    known_baseline_duplicate_urls = {
        "https://metaphorum.org/staffords-work/viable-system-model",
        "https://pespmc1.vub.ac.be/INTRO.html",
    }
    duplicate_urls = [
        url for url, count in Counter(source_urls).items()
        if count > 1 and url not in known_baseline_duplicate_urls
    ]
    if duplicate_urls:
        errors.append(f"new or unexpected duplicate public source URLs: {duplicate_urls}")

    for journey_id in sorted(NEW_JOURNEY_IDS):
        journey = journeys.get(journey_id)
        if not journey:
            errors.append(f"missing new guided journey: {journey_id}")
            continue
        steps = journey.get("steps", [])
        if len(steps) < 5:
            errors.append(f"new journey needs at least five steps: {journey_id}")
        for step in steps:
            if canonical(step.get("node_id")) not in public_ids:
                errors.append(f"journey step points to a missing public node: {journey_id}/{step.get('node_id')}")
            if not step.get("heading") or not step.get("narrative"):
                errors.append(f"journey step is incomplete: {journey_id}")

    register = data.get("source_mining_register", [])
    if len(register) < 14:
        errors.append("source_mining_register must contain at least fourteen scoped source programmes")
    register_ids = [item.get("id") for item in register]
    if len(register_ids) != len(set(register_ids)):
        errors.append("source_mining_register contains duplicate IDs")
    for item in register:
        for field in ("id", "label", "url", "status", "role", "caveat", "next_step"):
            if not item.get(field):
                errors.append(f"source-mining item is missing {field}: {item.get('id')}")

    report = data.get("ai_observations", {})
    metrics = report.get("metrics", {})
    if report.get("release") not in ALLOWED_RELEASES:
        errors.append("ai_observations.release is wrong")
    if len(report.get("observations", [])) < 9:
        errors.append("AI observations page needs at least nine distinct observations")
    if meta.get("release") == "0.9-observations-alpha" and len(report.get("public_risks", [])) < 10:
        errors.append("0.9 publication risk register needs at least ten risks")
    if meta.get("release") == "0.10-practice-safety-alpha" and "public_risks" in report:
        errors.append("0.10 must not publish the detailed working risk register")
    if metrics.get("public_entries") != len(public_nodes):
        errors.append("AI metrics public-entry count is stale")
    if metrics.get("developed_profiles") != len(set(profiles) & public_ids):
        errors.append("AI metrics profile count is stale")

    canonical_edges = []
    for edge in edges:
        source = canonical(edge.get("source"))
        target = canonical(edge.get("target"))
        if source in public_ids and target in public_ids and source != target:
            canonical_edges.append({**edge, "source": source, "target": target})
        for source_id in parse(edge.get("source_ids")):
            if source_id not in source_ids:
                errors.append(f"edge {edge.get('id')} cites unknown source {source_id}")
    if metrics.get("typed_edges") != len(canonical_edges):
        errors.append("AI metrics typed-edge count is stale")
    substantive = [
        edge for edge in canonical_edges
        if edge.get("relation_family") not in {"classification", "evidence", "documentary", "legacy"}
        and edge.get("relation_type") != "legacy_association_unspecified"
        and edge.get("claim_status") != "legacy_unresolved"
    ]
    if metrics.get("substantive_edges") != len(substantive):
        errors.append("AI metrics substantive-edge count is stale")

    # Preserve the 0.8 breadth release and its evidence boundary.
    expansion = data.get("expansion_08", {})
    if expansion.get("net_new_public_entries") != 203:
        errors.append("0.8 expansion count regressed")
    if expansion.get("official_papers") != 89 or expansion.get("new_bibliographic_people") != 107:
        errors.append("0.8 paper/author inventory regressed")

    index = (DOCS / "index.html").read_text(encoding="utf-8")
    app = (DOCS / "assets" / "app.js").read_text(encoding="utf-8")
    css = (DOCS / "assets" / "site-enhancements.css").read_text(encoding="utf-8")

    for marker in [
        'id="view-ai-observations"', 'id="aiObservationMetrics"', 'id="aiObservationsList"',
        'id="sourceMiningList"', 'href="#view=ai-observations"',
        'id="mapLayer"', 'value="human"', 'value="conceptual"', 'class="layer-grid"',
    ]:
        if marker not in index:
            errors.append(f"public interface is missing: {marker}")
    if meta.get("release") == "0.9-observations-alpha" and 'id="aiRiskList"' not in index:
        errors.append("0.9 risk list interface is missing")
    if meta.get("release") == "0.10-practice-safety-alpha" and 'id="aiRiskList"' in index:
        errors.append("0.10 still publishes the detailed risk-list interface")
    if re.search(r'<button[^>]+\bdata-view(?:-link)?=', index):
        errors.append("static view navigation still uses buttons rather than right-clickable anchors")
    if "Curator's running notebook and feedback issue" in index:
        errors.append("the running notebook has become prominent again")
    if meta.get("release") == "0.9-observations-alpha" and 'class="discreet-note-link"' not in index:
        errors.append("the discreet running-notebook affordance is missing")
    if meta.get("release") == "0.10-practice-safety-alpha" and ('/issues/2' in index or '/issues/2' in app):
        errors.append("the retired public running-notebook route remains")

    for marker in [
        "function renderAIObservations()", "function edgeInLayer(edge)", "function followInternalAnchor",
        "mapLayerDescription", "function zoomAt(factor", "internalHref('item'", "['mapDepth', 'mapLayer'",
    ]:
        if marker not in app:
            errors.append(f"app.js is missing iteration 0.9 behaviour: {marker}")
    for forbidden in [
        '<button class="text-button entry-link', '<button class="chip open-card',
        '<button class="text-button open-card', "document.getElementById('mapZoomIn')?.addEventListener",
    ]:
        if forbidden in app:
            errors.append(f"obsolete non-link or double-zoom behaviour remains: {forbidden}")
    for marker in ["0.9 feedback iteration", ".observation-card", ".layer-card", "text-align: left !important"]:
        if marker not in css:
            errors.append(f"iteration 0.9 CSS is missing: {marker}")

    documentation_paths = [
        ROOT / "documentation" / "ai-observations.md",
        ROOT / "documentation" / "sources-to-mine.md",
    ]
    if meta.get("release") == "0.9-observations-alpha":
        documentation_paths.append(ROOT / "documentation" / "publication-risks.md")
    else:
        documentation_paths.append(ROOT / "documentation" / "publication-safety.md")
    for path in documentation_paths:
        if not path.exists() or path.stat().st_size < 500:
            errors.append(f"missing or implausibly small documentation file: {path.relative_to(ROOT)}")

    payloads = [DATA_PATH.read_text(encoding="utf-8"), index, app]
    for pattern in PRIVATE_PATTERNS:
        if any(pattern.casefold() in payload.casefold() for payload in payloads):
            errors.append(f"public release contains a private-path pattern: {pattern}")

    if errors:
        print("ITERATION 0.9 VALIDATION FAILED", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    type_counts = Counter(node.get("entity_type", "unknown") for node in public_nodes)
    print("ITERATION 0.9 VALIDATION PASSED")
    print(f"- canonical public entries: {len(public_nodes)}")
    print(f"- developed profiles: {len(set(profiles) & public_ids)}")
    print(f"- sources: {len(sources)}")
    print(f"- journeys: {len(journeys)}")
    print(f"- AI observations: {len(report.get('observations', []))}")
    print(f"- public risks: {len(report.get('public_risks', [])) if "public_risks" in report else "retired from public release"}")
    print(f"- source-mining programmes: {len(register)}")
    print(f"- entry types: {dict(sorted(type_counts.items()))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
