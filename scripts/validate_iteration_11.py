#!/usr/bin/env python3
"""Validate release 0.11 semantic-map and feedback commitments."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "public-data.json"
DOCS = ROOT / "docs"
EXPECTED_RELEASE = "0.11-semantic-map-alpha"
EXPECTED_ENTRIES = 417
EXPECTED_PROFILES = 38
EXPECTED_JOURNEYS = 13
EXPECTED_SOURCES = 100
REQUIRED_FEEDBACK_IDS = {
    "feedback_public_identity",
    "feedback_clickable_affordances",
    "feedback_secret_dot",
    "feedback_membership_agents",
    "feedback_map",
    "feedback_principia_sources_categories",
    "feedback_fpcs",
    "feedback_monoskop",
    "feedback_syscoi_model_report",
    "feedback_prior_maps",
    "feedback_human_lineage",
    "feedback_company_knowledge",
    "feedback_mowles_murmurations",
    "feedback_sources_and_journeys",
    "feedback_layers",
    "feedback_publication_risk",
    "feedback_six_systems_terms",
    "feedback_public_pathways",
}


def main() -> int:
    errors: list[str] = []
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    meta = data.get("meta", {})
    redirects = data.get("canonical_redirects", {})
    canonical = lambda node_id: redirects.get(node_id, node_id)
    public_nodes = [
        node
        for node in data.get("nodes", [])
        if node.get("public_visibility") == "public" and canonical(node.get("id")) == node.get("id")
    ]
    public_ids = {node.get("id") for node in public_nodes}
    profiles = data.get("profiles", {})
    journeys = data.get("journeys", [])
    sources = data.get("sources", [])

    if meta.get("release") != EXPECTED_RELEASE:
        errors.append(f"meta.release must be {EXPECTED_RELEASE}")
    if len(public_nodes) != EXPECTED_ENTRIES or meta.get("public_entry_count") != EXPECTED_ENTRIES:
        errors.append(f"expected {EXPECTED_ENTRIES} canonical public entries")
    profile_count = len(set(profiles) & public_ids) if isinstance(profiles, dict) else meta.get("profile_count")
    if profile_count != EXPECTED_PROFILES or meta.get("profile_count") != EXPECTED_PROFILES:
        errors.append(f"expected {EXPECTED_PROFILES} developed profiles")
    if len(journeys) != EXPECTED_JOURNEYS or meta.get("journey_count") != EXPECTED_JOURNEYS:
        errors.append(f"expected {EXPECTED_JOURNEYS} guided journeys")
    if len(sources) != EXPECTED_SOURCES or meta.get("source_count") != EXPECTED_SOURCES:
        errors.append(f"expected {EXPECTED_SOURCES} sources")

    feedback = data.get("feedback_ledger", [])
    feedback_ids = {item.get("id") for item in feedback}
    missing_feedback = REQUIRED_FEEDBACK_IDS - feedback_ids
    if missing_feedback:
        errors.append(f"feedback ledger is missing commitments: {sorted(missing_feedback)}")
    if len(feedback_ids) != len(feedback):
        errors.append("feedback ledger contains duplicate or missing IDs")
    if meta.get("feedback_ledger_count") != len(feedback):
        errors.append("meta.feedback_ledger_count is stale")
    for item in feedback:
        for field in ("id", "label", "status", "summary", "evidence"):
            if not item.get(field):
                errors.append(f"feedback item is missing {field}: {item.get('id')}")

    interaction = data.get("map_interaction", {})
    if interaction.get("version") != "semantic-map-v1" or meta.get("map_interaction_version") != "semantic-map-v1":
        errors.append("semantic map version is missing")
    required_features = {
        "progressive label density",
        "overview minimap with viewport rectangle",
        "focus breadcrumb and back trail",
        "double-click neighbourhood focus",
        "hover neighbourhood emphasis",
        "fullscreen map",
        "keyboard zoom and fit controls",
    }
    if not required_features.issubset(set(interaction.get("features", []))):
        errors.append("map interaction feature declaration is incomplete")

    index = (DOCS / "index.html").read_text(encoding="utf-8")
    app = (DOCS / "assets" / "app.js").read_text(encoding="utf-8")
    map_js_path = DOCS / "assets" / "map-v11.js"
    map_css_path = DOCS / "assets" / "map-v11.css"
    map_js = map_js_path.read_text(encoding="utf-8") if map_js_path.exists() else ""
    map_css = map_css_path.read_text(encoding="utf-8") if map_css_path.exists() else ""

    thread_url = "https://github.com/antlerboy/the-necessary-tangle/issues/2"
    if index.count(thread_url) != 1:
        errors.append("the running-feedback thread must appear exactly once in the public page")
    for marker in [
        'class="feedback-dot"',
        'aria-label="Open the curator’s running feedback thread"',
        'href="assets/map-v11.css"',
        'src="assets/map-v11.js"',
        'class="semantic-map-introduction"',
        'documentation/feedback-ledger.md',
    ]:
        if marker not in index:
            errors.append(f"public page is missing 0.11 marker: {marker}")
    if "Curator notebook" in index or "Curator's running notebook" in index:
        errors.append("the discreet feedback route has become a prominent notebook label again")

    for marker in [
        "semanticMapVersion: '0.11'",
        "getTransform: () => ({ ...mapTransform })",
        "setTransform: (next = {})",
        "document.dispatchEvent(new CustomEvent('tangle:map-transform'",
    ]:
        if marker not in app:
            errors.append(f"app.js is missing semantic-map API marker: {marker}")

    for marker in [
        "progressive label disclosure",
        "function rebuildMiniMap()",
        "function updateViewport()",
        "function focusHash(id, depth = '1')",
        "function applyHover(id)",
        "function beginDrag(event, element, id)",
        "semanticLabelMode",
        "semanticFocusTrail",
        "mapMiniViewport",
        "requestFullscreen",
        "event.key.toLocaleLowerCase() === 'l'",
    ]:
        if marker not in map_js:
            errors.append(f"map-v11.js is missing: {marker}")
    for marker in [
        ".feedback-dot",
        ".semantic-map-toolbar",
        ".map-minimap",
        '[data-semantic-label="hide"]',
        ".semantic-dimmed",
        ".semantic-fullscreen",
    ]:
        if marker not in map_css:
            errors.append(f"map-v11.css is missing: {marker}")

    ledger_path = ROOT / "documentation" / "feedback-ledger.md"
    map_doc_path = ROOT / "documentation" / "map-interaction.md"
    for path in (ledger_path, map_doc_path):
        if not path.exists() or path.stat().st_size < 1800:
            errors.append(f"missing or implausibly small documentation: {path.relative_to(ROOT)}")
    if ledger_path.exists():
        ledger = ledger_path.read_text(encoding="utf-8")
        for phrase in [
            "Foundational Papers in Complexity Science",
            "Monoskop",
            "SysCoI and model.report",
            "Practitioner influence constellations",
            "Chris Mowles and Murmurations",
            "Publication risks",
            "Secret route to the comment thread",
        ]:
            if phrase not in ledger:
                errors.append(f"feedback ledger omitted a thread theme: {phrase}")

    if len(data.get("publication_controls", [])) < 6:
        errors.append("publication controls regressed")
    if not (ROOT / "SECURITY.md").exists() or not (ROOT / ".github" / "CODEOWNERS").exists():
        errors.append("publication-safety repository controls regressed")

    # The map extension must be loaded after the main application so its public API exists.
    app_position = index.find('src="assets/app.js"')
    semantic_position = index.find('src="assets/map-v11.js"')
    if app_position < 0 or semantic_position < app_position:
        errors.append("map-v11.js must load after app.js")

    # Do not allow private-system traces to enter through the feedback audit.
    public_payload = "\n".join([DATA_PATH.read_text(encoding="utf-8"), index, map_js])
    for pattern in ["sharepoint.com/", "@redquadrant.com", "C:\\Users\\", "onedrive\\", "dropbox\\"]:
        if pattern.casefold() in public_payload.casefold():
            errors.append(f"private-system pattern leaked into the public payload: {pattern}")

    if errors:
        print("ITERATION 0.11 VALIDATION FAILED", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("ITERATION 0.11 VALIDATION PASSED")
    print(f"- canonical public entries: {len(public_nodes)}")
    print(f"- developed profiles: {profile_count}")
    print(f"- feedback commitments: {len(feedback)}")
    print(f"- semantic map features: {len(interaction.get('features', []))}")
    print("- running feedback dot: restored")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
