#!/usr/bin/env python3
"""Validate the enduring expertise, semantics and public-intake features introduced by 0.12."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "public-data.json"
DOCS = ROOT / "docs"
ALLOWED_RELEASES = {"0.12-practitioner-intake-alpha", "0.13-expertise-observations-alpha", "0.14-snowden-cynefin-alpha", "0.15-ing-reading-practice-alpha", "0.16-grammar-connections-presentation-alpha", "0.17-public-intake-lineage-alpha"}
READING_LIST = "https://stream.syscoi.com/2024/10/01/updated-rough-draft-systems-complexity-cybernetics-reading-list/"

REQUIRED_PUBLIC_IDS = {
    "organisation_scio_systems_and_complexity_in_organisation",
    "person_ivo_velitchkov", "publication_essential_balances",
    "concept_requisite_inefficiency", "concept_natural_drift",
    "concept_explicit_semantics", "tool_nodica",
    "person_patrick_hoverstadt", "publication_grammar_of_systems_ii",
    "publication_fractal_organisation_manual", "person_lucy_loh",
    "person_michael_c_jackson", "publication_critical_systems_thinking_practitioners_guide",
    "publication_opening_the_box", "publication_systems_approaches_making_change",
    "person_arthur_battram", "publication_navigating_complexity_battram",
    "knowledge_domain_systems_laws", "method_or_methodology_patterns_of_strategy",
}
REQUIRED_PROFILE_IDS = REQUIRED_PUBLIC_IDS - {"person_lucy_loh"}
REQUIRED_SOURCE_IDS = {
    "src_velitchkov_home_current", "src_scio_essential_balances_2020",
    "src_scio_requisite_inefficiency_2014", "src_nodica_repo_2026",
    "src_maturana_mpodozis_natural_drift_2000",
    "src_scio_fractal_organisation_manual_2026",
    "src_scio_patterns_strategy_book_2016", "src_scio_critical_systems_thinking_2024",
    "src_scio_opening_box_2024", "src_scio_systems_approaches_making_change_2020",
    "src_scio_courses_current", "src_scio_navigating_complexity_2014",
}
REQUIRED_EDGE_IDS = {
    "e_12_ivo_essential_author", "e_12_req_ineff_coined",
    "e_12_natural_drift_viability", "e_12_natural_drift_maturana",
    "e_12_nodica_semantics", "e_12_grammar_patrick", "e_12_grammar_laws",
    "e_12_fractal_vsm", "e_12_pos_patrick", "e_12_pos_lucy",
    "e_12_cst_book_jackson", "e_12_change_hoverstadt", "e_12_battram_book",
}
PRIVATE_PATTERNS = (
    "sharepoint.com", "graph.microsoft", "mail.google", "gmail.com/mail",
    "sandbox:/", "file://", "localhost", "127.0.0.1", "/mnt/data",
    "redquadrantltd.sharepoint", "c:\\users\\", "c:/users/",
)
SECRET_PATTERNS = (
    re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"(?i)(?:api[_-]?key|client[_-]?secret|access[_-]?token)\s*[:=]\s*['\"][^'\"]{12,}['\"]"),
)


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
    release = meta.get("release")
    if release not in ALLOWED_RELEASES:
        errors.append(f"unexpected release: {release}")

    redirects = data.get("canonical_redirects", {})
    canonical = lambda node_id: redirects.get(node_id, node_id)
    nodes = {node["id"]: node for node in data.get("nodes", []) if node.get("id")}
    public_ids = {
        node["id"] for node in data.get("nodes", [])
        if node.get("public_visibility") == "public" and canonical(node["id"]) == node["id"]
    }
    profiles = {item.get("node_id"): item for item in data.get("profiles", []) if item.get("node_id")}
    sources = {item.get("id"): item for item in data.get("sources", []) if item.get("id")}
    edges = {item.get("id"): item for item in data.get("edges", []) if item.get("id")}
    journeys = {item.get("id"): item for item in data.get("journeys", []) if item.get("id")}

    for label, actual, minimum in (
        ("public entries", len(public_ids), 442),
        ("developed profiles", len(set(profiles) & public_ids), 58),
        ("sources", len(sources), 114),
        ("journeys", len(journeys), 14),
    ):
        if actual < minimum:
            errors.append(f"0.12 feature floor regressed for {label}: {actual} < {minimum}")

    for node_id in sorted(REQUIRED_PUBLIC_IDS):
        node = nodes.get(node_id)
        if not node or node_id not in public_ids:
            errors.append(f"missing canonical public 0.12 entry: {node_id}")
        elif not parse(node.get("source_ids")):
            errors.append(f"0.12 entry has no source IDs: {node_id}")
    for node_id in sorted(REQUIRED_PROFILE_IDS):
        if node_id not in profiles:
            errors.append(f"0.12 entry lacks a developed profile: {node_id}")
    for source_id in sorted(REQUIRED_SOURCE_IDS):
        source = sources.get(source_id)
        if not source:
            errors.append(f"missing 0.12 source: {source_id}")
        elif not str(source.get("url", "")).startswith("https://"):
            errors.append(f"0.12 source lacks a public HTTPS URL: {source_id}")
    for edge_id in sorted(REQUIRED_EDGE_IDS):
        edge = edges.get(edge_id)
        if not edge:
            errors.append(f"missing 0.12 typed relation: {edge_id}")
        elif any(not edge.get(field) for field in ("source", "target", "relation_type", "relation_family", "plain_phrase", "source_ids")):
            errors.append(f"0.12 relation is incomplete: {edge_id}")

    journey = journeys.get("journey_viability_balance_and_strategy")
    if not journey or len(journey.get("steps", [])) < 8:
        errors.append("viability, balance and strategy journey is missing or too short")

    semantics = data.get("semantic_contract", {})
    if semantics.get("version") != "explicit-semantics-v1":
        errors.append("explicit semantic contract is missing")
    required_relation_fields = {"source", "target", "relation_type", "relation_family", "directed", "plain_phrase", "claim_status", "confidence", "source_ids", "scope_conditions"}
    if not required_relation_fields.issubset(set(semantics.get("relation_fields", []))):
        errors.append("semantic contract omits required relation fields")

    intake = data.get("contribution_intake", {})
    if release == "0.13-expertise-observations-alpha":
        if data.get("accepted_contributions"):
            errors.append("public data contains editorial-process contribution records")
        if intake.get("version") != "proposal-intake-v2" or meta.get("proposal_intake_version") != "proposal-intake-v2":
            errors.append("proposal-intake metadata is missing")
        if {feed.get("id") for feed in intake.get("feeds", [])} != {"site_submissions", "research_issues", "pull_requests"}:
            errors.append("proposal intake routes are incomplete")

    reading = data.get("reading_list_coverage", {})
    if sources.get("src_taylor_reading_list_current", {}).get("url") != READING_LIST:
        errors.append("reading-list source URL is stale")
    allowed_reading_status = {"headline_recommendations_developed_full_audit_open"}
    if release in {"0.15-ing-reading-practice-alpha", "0.16-grammar-connections-presentation-alpha", "0.17-public-intake-lineage-alpha"}:
        allowed_reading_status.add("item_level_inventory_with_developed_subset_full_critical_audit_open")
    if reading.get("status") not in allowed_reading_status:
        errors.append("reading-list coverage status is missing or overclaims completeness")
    scio = data.get("scio_coverage", {})
    if scio.get("approach_family_count") != 13 or scio.get("intervention_skill_count") != 47:
        errors.append("SCiO coverage inventory has regressed")

    index = (DOCS / "index.html").read_text(encoding="utf-8")
    css = (DOCS / "assets" / "site-enhancements.css").read_text(encoding="utf-8")
    for marker in (
        'id="startSmallTitle"', 'id="mapOrientationPanel"',
        'class="plain-panel wide explicit-semantics-callout"',
        'person_ivo_velitchkov', 'person_patrick_hoverstadt',
        'journey_viability_balance_and_strategy',
        'documentation/explicit-semantics.md', 'documentation/contribution-intake.md',
    ):
        if marker not in index:
            errors.append(f"public interface is missing enduring 0.12 feature: {marker}")
    for marker in (".start-small-section", ".map-orientation-panel", ".explicit-semantics-callout"):
        if marker not in css:
            errors.append(f"release CSS is missing: {marker}")

    required_docs = {
        "explicit-semantics.md": 700,
        "contribution-intake.md": 500,
        "scio-coverage.md": 600,
        "reading-list-coverage.md": 600,
        "publication-standards.md": 500,
    }
    for name, minimum in required_docs.items():
        path = ROOT / "documentation" / name
        if not path.exists() or path.stat().st_size < minimum:
            errors.append(f"documentation/{name} is missing or implausibly small")

    public_text = "\n".join(path.read_text(encoding="utf-8", errors="ignore") for path in (DATA_PATH, DOCS / "index.html", DOCS / "assets" / "app.js"))
    folded = public_text.casefold()
    for pattern in PRIVATE_PATTERNS:
        if pattern.casefold() in folded:
            errors.append(f"private or local marker leaked into public release: {pattern}")
    for pattern in SECRET_PATTERNS:
        if pattern.search(public_text):
            errors.append(f"secret-like value leaked into public release: {pattern.pattern}")

    if errors:
        print("ITERATION 0.12 ENDURING VALIDATION FAILED", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("ITERATION 0.12 ENDURING VALIDATION PASSED")
    print(f"- canonical public entries: {len(public_ids)}")
    print(f"- developed profiles: {len(set(profiles) & public_ids)}")
    print(f"- sources: {len(sources)}")
    print(f"- journeys: {len(journeys)}")
    print("- Ivo Velitchkov and Patrick Hoverstadt expertise coverage retained")
    print("- explicit semantics and public proposal intake retained")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
