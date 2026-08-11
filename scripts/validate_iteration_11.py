#!/usr/bin/env python3
"""Validate enduring whole-to-detail map navigation features."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "public-data.json"
DOCS = ROOT / "docs"
EXPECTED_RELEASE = "0.11-visual-map-alpha"
ALLOWED_RELEASES = {EXPECTED_RELEASE, "0.12-practitioner-intake-alpha", "0.13-expertise-observations-alpha"}
EXPECTED_PUBLIC_COUNT = 417
EXPECTED_PROFILE_COUNT = 38
EXPECTED_JOURNEY_COUNT = 13
EXPECTED_MIN_SOURCES = 100

def main() -> int:
    errors: list[str] = []
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    meta = data.get("meta", {})
    redirects = data.get("canonical_redirects", {})
    canonical = lambda node_id: redirects.get(node_id, node_id)
    public_nodes = [
        node for node in data.get("nodes", [])
        if node.get("public_visibility") == "public" and canonical(node["id"]) == node["id"]
    ]
    public_ids = {node["id"] for node in public_nodes}
    profiles = {profile.get("node_id") for profile in data.get("profiles", []) if profile.get("node_id")}
    journeys = {journey.get("id") for journey in data.get("journeys", []) if journey.get("id")}
    sources = {source.get("id") for source in data.get("sources", []) if source.get("id")}

    if meta.get("release") not in ALLOWED_RELEASES:
        errors.append(f"meta.release must be one of {sorted(ALLOWED_RELEASES)}")
    if len(public_nodes) < EXPECTED_PUBLIC_COUNT or meta.get("public_entry_count", 0) < EXPECTED_PUBLIC_COUNT:
        errors.append(f"expected at least {EXPECTED_PUBLIC_COUNT} canonical public entries")
    if len(profiles & public_ids) < EXPECTED_PROFILE_COUNT or meta.get("profile_count", 0) < EXPECTED_PROFILE_COUNT:
        errors.append(f"expected at least {EXPECTED_PROFILE_COUNT} developed profiles")
    if len(journeys) < EXPECTED_JOURNEY_COUNT or meta.get("journey_count", 0) < EXPECTED_JOURNEY_COUNT:
        errors.append(f"expected at least {EXPECTED_JOURNEY_COUNT} guided journeys")
    if len(sources) < EXPECTED_MIN_SOURCES or meta.get("source_count", 0) < EXPECTED_MIN_SOURCES:
        errors.append(f"expected at least {EXPECTED_MIN_SOURCES} sources")

    experience = data.get("map_experience", {})
    if experience.get("release") != EXPECTED_RELEASE:
        errors.append("map_experience release metadata is stale")
    if experience.get("model") != "whole-to-detail conceptual navigation":
        errors.append("map_experience model is missing")
    if len(experience.get("principles", [])) < 5:
        errors.append("map_experience needs at least five explicit principles")
    if experience.get("inspiration", {}).get("url") != "https://visual-meaning.com/our-platform/":
        errors.append("Visual Meaning interaction reference is missing")
    if data.get("ai_observations", {}).get("release") not in ALLOWED_RELEASES:
        errors.append("AI observations release is stale")

    index = (DOCS / "index.html").read_text(encoding="utf-8")
    app = (DOCS / "assets" / "app.js").read_text(encoding="utf-8")
    css = (DOCS / "assets" / "site-enhancements.css").read_text(encoding="utf-8")

    html_markers = [
        'id="graphWrap"',
        'id="mapBack"',
        'id="mapForward"',
        'id="mapZoomRange"',
        'id="mapScaleMode"',
        'id="mapFullscreen"',
        'id="mapMiniMap"',
        'id="miniEdges"',
        'id="miniNodes"',
        'id="miniViewport"',
        'class="map-canvas-help"',
    ]
    for marker in html_markers:
        if marker not in index:
            errors.append(f"map/comment interface missing: {marker}")
    if meta.get("release") == "0.13-expertise-observations-alpha" and any(
        marker in index for marker in ("data-curator-dot=", "curator-secret-dot", "curator-notebook-link", "discreet-note-link")
    ):
        errors.append("an obsolete hidden working route remains in the public page")

    app_markers = [
        "let mapFocusHistory = [mapFocus]",
        "function updateMapHistoryButtons()",
        "function navigateMapHistory(delta)",
        "function semanticZoomBand",
        "function updateMapSemanticZoom()",
        "function renderMapMiniMap(positions, edges)",
        "function updateMiniViewport()",
        "data-label-priority",
        "graph-edge-label",
        "mapZoomRange",
        "mapMiniMap",
        "requestFullscreen",
        "fullscreenchange",
        "svg.addEventListener('dblclick'",
        "wrap.addEventListener('keydown'",
    ]
    for marker in app_markers:
        if marker not in app:
            errors.append(f"app.js missing 0.11 map behaviour: {marker}")
    if app.count("svg.addEventListener('wheel'") != 1:
        errors.append("map must have exactly one wheel-zoom handler")
    if "svg.style.transform" in app:
        errors.append("obsolete whole-SVG zoom remains")

    css_markers = [
        ".map-canvas-toolbar",
        ".map-minimap-shell",
        "#miniViewport",
        ".graph-edge-label",
        ".map-zoom-overview",
        ".map-zoom-neighbourhood",
        ".map-zoom-detail",
        ".graph-wrap:fullscreen",
    ]
    for marker in css_markers:
        if marker not in css:
            errors.append(f"site-enhancements.css missing 0.11 marker: {marker}")

    documentation = ROOT / "documentation" / "visual-map.md"
    if not documentation.exists() or documentation.stat().st_size < 700:
        errors.append("documentation/visual-map.md is missing or implausibly small")

    if errors:
        print("ITERATION 0.11 VALIDATION FAILED", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("ITERATION 0.11 VALIDATION PASSED")
    print(f"- canonical public entries: {len(public_nodes)}")
    print(f"- developed profiles: {len(profiles & public_ids)}")
    print(f"- sources: {len(sources)}")
    print(f"- journeys: {len(journeys)}")
    print("- whole-to-detail map: semantic zoom, minimap, history, slider, fullscreen and keyboard controls")
    print("- map interaction: semantic zoom, minimap, history and keyboard controls preserved")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
