#!/usr/bin/env python3
"""Validate release 0.12 practitioner coverage, semantics and contribution intake."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "public-data.json"
DOCS = ROOT / "docs"
EXPECTED_RELEASE = "0.12-practitioner-intake-alpha"
EXPECTED_PUBLIC_COUNT = 442
EXPECTED_PROFILE_COUNT = 58
EXPECTED_JOURNEY_COUNT = 14
EXPECTED_SOURCE_COUNT = 114
COMMENT_URL = "https://github.com/antlerboy/the-necessary-tangle/issues/2"
ISSUE_21 = "https://github.com/antlerboy/the-necessary-tangle/issues/21"
READING_LIST = "https://stream.syscoi.com/2024/10/01/updated-rough-draft-systems-complexity-cybernetics-reading-list/"

REQUIRED_PUBLIC_IDS = {
    "organisation_scio_systems_and_complexity_in_organisation",
    "person_ivo_velitchkov",
    "publication_essential_balances",
    "concept_requisite_inefficiency",
    "concept_natural_drift",
    "person_jorge_mpodozis",
    "concept_explicit_semantics",
    "tool_nodica",
    "person_patrick_hoverstadt",
    "publication_grammar_of_systems_ii",
    "publication_fractal_organisation_manual",
    "person_lucy_loh",
    "person_michael_c_jackson",
    "publication_critical_systems_thinking_practitioners_guide",
    "publication_opening_the_box",
    "publication_systems_approaches_making_change",
    "person_arthur_battram",
    "publication_navigating_complexity_battram",
    "knowledge_domain_systems_laws",
    "method_or_methodology_patterns_of_strategy",
}

REQUIRED_PROFILE_IDS = REQUIRED_PUBLIC_IDS - {
    "person_lucy_loh",
    "person_jorge_mpodozis",
}

REQUIRED_SOURCE_IDS = {
    "src_velitchkov_home_current",
    "src_scio_essential_balances_2020",
    "src_scio_requisite_inefficiency_2014",
    "src_nodica_repo_2026",
    "src_maturana_mpodozis_natural_drift_2000",
    "src_scio_fractal_organisation_manual_2026",
    "src_scio_patterns_strategy_book_2016",
    "src_scio_critical_systems_thinking_2024",
    "src_scio_opening_box_2024",
    "src_scio_systems_approaches_making_change_2020",
    "src_scio_courses_current",
    "src_scio_navigating_complexity_2014",
    "src_cybcom_archive_current",
    "src_asc_archives_current",
}

REQUIRED_EDGE_IDS = {
    "e_12_ivo_essential_author",
    "e_12_req_ineff_coined",
    "e_12_natural_drift_viability",
    "e_12_natural_drift_maturana",
    "e_12_nodica_semantics",
    "e_12_grammar_patrick",
    "e_12_grammar_laws",
    "e_12_fractal_vsm",
    "e_12_pos_patrick",
    "e_12_pos_lucy",
    "e_12_cst_book_jackson",
    "e_12_change_hoverstadt",
    "e_12_battram_book",
}

PRIVATE_PATTERNS = (
    "sharepoint.com",
    "graph.microsoft",
    "mail.google",
    "gmail.com/mail",
    "sandbox:/",
    "file://",
    "localhost",
    "127.0.0.1",
    "/mnt/data",
    "redquadrantltd.sharepoint",
    "c:\\users\\",
    "c:/users/",
)
SECRET_PATTERNS = (
    re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"(?i)(?:api[_-]?key|client[_-]?secret|access[_-]?token)\s*[:=]\s*['\"][^'\"]{12,}['\"]"),
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
    nodes = {node["id"]: node for node in data.get("nodes", []) if node.get("id")}
    public_nodes = [
        node for node in data.get("nodes", [])
        if node.get("public_visibility") == "public" and canonical(node["id"]) == node["id"]
    ]
    public_ids = {node["id"] for node in public_nodes}
    profiles = {profile.get("node_id"): profile for profile in data.get("profiles", []) if profile.get("node_id")}
    journeys = {journey.get("id"): journey for journey in data.get("journeys", []) if journey.get("id")}
    sources = {source.get("id"): source for source in data.get("sources", []) if source.get("id")}
    edges = {edge.get("id"): edge for edge in data.get("edges", []) if edge.get("id")}

    if meta.get("release") != EXPECTED_RELEASE:
        errors.append(f"meta.release must be {EXPECTED_RELEASE}")
    if len(public_nodes) != EXPECTED_PUBLIC_COUNT or meta.get("public_entry_count") != EXPECTED_PUBLIC_COUNT:
        errors.append(f"expected exactly {EXPECTED_PUBLIC_COUNT} canonical public entries")
    developed = len(set(profiles) & public_ids)
    if developed != EXPECTED_PROFILE_COUNT or meta.get("profile_count") != EXPECTED_PROFILE_COUNT:
        errors.append(f"expected exactly {EXPECTED_PROFILE_COUNT} developed profiles")
    if len(journeys) != EXPECTED_JOURNEY_COUNT or meta.get("journey_count") != EXPECTED_JOURNEY_COUNT:
        errors.append(f"expected exactly {EXPECTED_JOURNEY_COUNT} guided journeys")
    if len(sources) != EXPECTED_SOURCE_COUNT or meta.get("source_count") != EXPECTED_SOURCE_COUNT:
        errors.append(f"expected exactly {EXPECTED_SOURCE_COUNT} sources")

    for node_id in sorted(REQUIRED_PUBLIC_IDS):
        node = nodes.get(node_id)
        if not node:
            errors.append(f"missing required 0.12 entry: {node_id}")
            continue
        if node_id not in public_ids:
            errors.append(f"required 0.12 entry is not canonical public: {node_id}")
        if not parse(node.get("source_ids")):
            errors.append(f"required 0.12 entry has no source IDs: {node_id}")
    for node_id in sorted(REQUIRED_PROFILE_IDS):
        if node_id not in profiles:
            errors.append(f"required 0.12 entry lacks a developed profile: {node_id}")

    for source_id in sorted(REQUIRED_SOURCE_IDS):
        source = sources.get(source_id)
        if not source:
            errors.append(f"missing required 0.12 source: {source_id}")
            continue
        if not str(source.get("url", "")).startswith("https://"):
            errors.append(f"0.12 source lacks a public HTTPS URL: {source_id}")
        if not source.get("notes") or not source.get("review_status"):
            errors.append(f"0.12 source lacks review metadata: {source_id}")

    for edge_id in sorted(REQUIRED_EDGE_IDS):
        edge = edges.get(edge_id)
        if not edge:
            errors.append(f"missing required 0.12 typed relation: {edge_id}")
            continue
        for field in ("source", "target", "relation_type", "relation_family", "plain_phrase", "claim_status", "source_ids"):
            if not edge.get(field):
                errors.append(f"0.12 relation {edge_id} lacks {field}")
        if edge.get("relation_type") == "legacy_association_unspecified":
            errors.append(f"0.12 relation uses legacy unspecified semantics: {edge_id}")

    natural_edge = edges.get("e_12_natural_drift_viability", {})
    if natural_edge.get("claim_status") not in {"accepted_with_scope", "contested", "accepted"}:
        errors.append("natural-drift relation needs an explicit scoped/contested status")

    journey = journeys.get("journey_viability_balance_and_strategy")
    if not journey or len(journey.get("steps", [])) < 8:
        errors.append("viability, balance and strategy guided journey is missing or too short")

    contributions = data.get("accepted_contributions", [])
    contribution = next((item for item in contributions if item.get("issue_number") == 21), None)
    if not contribution:
        errors.append("Ivo Velitchkov's site submission #21 is absent from accepted_contributions")
    else:
        if contribution.get("github_login") != "kvistgaard" or contribution.get("status") != "incorporated_with_independent_sources":
            errors.append("site submission #21 has incorrect attribution or disposition")
        if not {"concept_viability", "concept_natural_drift", "person_ivo_velitchkov"}.issubset(set(contribution.get("resulting_entry_ids", []))):
            errors.append("site submission #21 is not connected to the resulting entries")
    if meta.get("accepted_contribution_count") != 1:
        errors.append("accepted contribution count must be one for 0.12")

    intake = data.get("contribution_intake", {})
    if intake.get("version") != "three-feed-intake-v1" or meta.get("feedback_intake_version") != "three-feed-intake-v1":
        errors.append("three-feed contribution intake metadata is missing")
    if {feed.get("id") for feed in intake.get("feeds", [])} != {"running_feedback", "site_submissions", "research_issues"}:
        errors.append("contribution intake must reconcile running feedback, site submissions and research issues")
    if set(intake.get("labels", [])) != {"site-submission", "awaiting-curator-review"}:
        errors.append("contribution intake labels are missing")

    semantics = data.get("semantic_contract", {})
    if semantics.get("version") != "explicit-semantics-v1" or meta.get("semantic_contract_version") != "explicit-semantics-v1":
        errors.append("explicit semantic contract metadata is missing")
    required_relation_fields = {"source", "target", "relation_type", "relation_family", "directed", "plain_phrase", "claim_status", "confidence", "source_ids", "scope_conditions"}
    if not required_relation_fields.issubset(set(semantics.get("relation_fields", []))):
        errors.append("semantic contract omits required relation fields")
    if semantics.get("comparator", {}).get("url") != "https://kvistgaard.github.io/nodica/index.html":
        errors.append("Nodica comparator is missing from the semantic contract")

    reading = data.get("reading_list_coverage", {})
    if reading.get("status") != "headline_recommendations_developed_full_audit_open":
        errors.append("reading-list coverage status is missing or overclaims completeness")
    headline = {item.get("node_id"): item.get("status") for item in reading.get("headline_items", [])}
    for node_id in (
        "publication_grammar_of_systems_ii",
        "publication_critical_systems_thinking_practitioners_guide",
        "publication_opening_the_box",
        "publication_essential_balances",
    ):
        if headline.get(node_id) != "developed":
            errors.append(f"headline reading-list recommendation is not developed: {node_id}")
    reading_source = sources.get("src_taylor_reading_list_current", {})
    if reading_source.get("url") != READING_LIST:
        errors.append("reading-list source URL is stale")

    scio = data.get("scio_coverage", {})
    if scio.get("approach_family_count") != 13 or scio.get("intervention_skill_count") != 47:
        errors.append("SCiO coverage inventory must retain 13 approach families and 47 intervention skills")
    if scio.get("organisation_node_id") != "organisation_scio_systems_and_complexity_in_organisation":
        errors.append("SCiO organisation entry is not linked from coverage metadata")

    if len(data.get("source_mining_register", [])) < 21:
        errors.append("source mining register did not absorb the latest feedback programmes")

    index = (DOCS / "index.html").read_text(encoding="utf-8")
    app = (DOCS / "assets" / "app.js").read_text(encoding="utf-8")
    css = (DOCS / "assets" / "site-enhancements.css").read_text(encoding="utf-8")
    workflow = (ROOT / ".github" / "workflows" / "triage-site-submissions.yml").read_text(encoding="utf-8")

    for marker in (
        'id="startSmallTitle"',
        'id="mapOrientationPanel"',
        'class="plain-panel wide contribution-intake-panel"',
        'class="plain-panel wide feedback-people-callout"',
        'class="plain-panel wide explicit-semantics-callout"',
        'person_ivo_velitchkov',
        'person_patrick_hoverstadt',
        'journey_viability_balance_and_strategy',
        'documentation/explicit-semantics.md',
        'documentation/contribution-intake.md',
        READING_LIST,
    ):
        if marker not in index:
            errors.append(f"public interface missing 0.12 marker: {marker}")
    if index.count(COMMENT_URL) != 1 or 'data-curator-dot="comments"' not in index:
        errors.append("the discreet running-feedback dot must remain exactly once")
    if "https://www.antlerboy.com/reading-list" in index:
        errors.append("stale reading-list URL remains in the public page")

    for marker in (
        "'## Intake marker'",
        "'site-submission'",
        "const labels = 'site-submission,awaiting-curator-review';",
        "labelled GitHub issue",
    ):
        if marker not in app:
            errors.append(f"site issue creation is missing intake marker: {marker}")
    for marker in (".start-small-section", ".map-orientation-panel", ".contribution-intake-panel", ".explicit-semantics-callout"):
        if marker not in css:
            errors.append(f"0.12 CSS missing: {marker}")

    for marker in (
        "issues: write",
        "site-submission",
        "awaiting-curator-review",
        "Prepared from The Necessary Tangle",
        "github.paginate",
        "workflow_dispatch",
    ):
        if marker not in workflow:
            errors.append(f"submission triage workflow missing: {marker}")

    required_docs = {
        "explicit-semantics.md": 900,
        "contribution-intake.md": 700,
        "scio-coverage.md": 700,
        "reading-list-coverage.md": 700,
        "feedback-ledger.md": 900,
    }
    for name, minimum in required_docs.items():
        path = ROOT / "documentation" / name
        if not path.exists() or path.stat().st_size < minimum:
            errors.append(f"documentation/{name} is missing or implausibly small")

    public_text = "\n".join(
        path.read_text(encoding="utf-8", errors="ignore")
        for path in [DATA_PATH, DOCS / "index.html", DOCS / "assets" / "app.js"]
    )
    folded = public_text.casefold()
    for pattern in PRIVATE_PATTERNS:
        if pattern.casefold() in folded:
            errors.append(f"private/local marker leaked into public release: {pattern}")
    for pattern in SECRET_PATTERNS:
        if pattern.search(public_text):
            errors.append(f"secret-like value leaked into public release: {pattern.pattern}")

    if ISSUE_21 not in json.dumps(contributions):
        errors.append("accepted contribution record lacks the public issue link")
    if ISSUE_21 in json.dumps(sources):
        errors.append("the contribution issue was incorrectly used as scholarly evidence")

    if errors:
        print("ITERATION 0.12 VALIDATION FAILED", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("ITERATION 0.12 VALIDATION PASSED")
    print(f"- canonical public entries: {len(public_nodes)}")
    print(f"- developed profiles: {developed}")
    print(f"- sources: {len(sources)}")
    print(f"- journeys: {len(journeys)}")
    print("- Ivo Velitchkov submission: incorporated with independent sources")
    print("- Patrick Hoverstadt and principal works: developed")
    print("- explicit semantics: documented and inspectable")
    print("- contribution intake: running thread + labelled submissions + research issues")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
