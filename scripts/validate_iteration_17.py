#!/usr/bin/env python3
"""Validate release 0.17 public intake, serendipity and canon/lineage work."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from apply_iteration_17 import GENERATED, PUBLIC_URL, RELEASE
from apply_iteration_09 import graph_metrics
from apply_relational_depth_16 import calculate_relational_depth

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "public-data.json"
VERSION = "0.18.0-public"

REQUIRED_NODES = {
    "person_magnus_ramage",
    "person_karen_shipp",
    "concept_canon_formation",
    "concept_epistemic_closure",
    "concept_epistemic_injustice",
    "concept_epistemic_exclusion",
    "practice_lineage_recovery",
    "concept_structurelessness",
    "publication_tyranny_of_structurelessness",
    "publication_epistemic_injustice",
    "person_jo_freeman",
    "person_miranda_fricker",
    "concept_decolonial_systems_thinking",
}

REQUIRED_SOURCES = {
    "src_ou_magnus_ramage_profile_2026",
    "src_springer_systems_thinkers_2ed_2020",
    "src_oro_systems_thinkers_2020",
    "src_oro_boundaries_disciplines_2006",
    "src_hull_centre_systems_studies_2026",
    "src_ou_mike_jackson_cst_2022",
    "src_freeman_tyranny_structurelessness",
    "src_oup_fricker_epistemic_injustice_2007",
    "src_tangle_issue2_canon_feedback_2026",
    "src_tangle_issue21_viability_submission_2026",
}

REQUIRED_RELATIONS = {
    "researches",
    "participates_in_canon_formation",
    "can_exclude",
    "recovers",
    "appropriated_from",
    "excluded_from_canon",
    "canonised_as",
    "responds_to",
}

REQUIRED_EDGES = {
    "e17_ramage_authored_systems_thinkers",
    "e17_shipp_authored_systems_thinkers",
    "e17_systems_thinkers_canon",
    "e17_ramage_researches_decolonial",
    "e17_ramage_open_university",
    "e17_shipp_open_university",
    "e17_jackson_develops_cst",
    "e17_jackson_hull_centre",
    "e17_fricker_authored_epistemic_injustice",
    "e17_book_develops_epistemic_injustice",
    "e17_freeman_authored_tyranny",
    "e17_tyranny_critiques_structurelessness",
    "e17_closure_can_exclude",
    "e17_canon_can_exclude",
    "e17_recovery_responds_exclusion",
    "e17_lineage_documentation_supports_recovery",
    "e17_structurelessness_checks_openness",
}

VISIBILITY_NAMES = {
    "Allenna Leonard",
    "Angela Espinosa",
    "Nora Bateson",
    "Sandra Janoff",
    "Christine Oliver",
    "Diane Bowling",
    "Isabel Menzies Lyth",
    "Mary Douglas",
    "Elaine Brown",
    "Harish Jose",
    "Taiichi Ohno",
    "Chögyam Trungpa",
    "Michael C. Jackson",
    "Magnus Ramage",
    "Karen Shipp",
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


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def main() -> int:
    errors: list[str] = []
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    meta = data.get("meta", {})
    redirects = data.get("canonical_redirects", {})
    nodes = {node.get("id"): node for node in data.get("nodes", []) if node.get("id")}
    public_ids = {
        node_id
        for node_id, node in nodes.items()
        if node.get("public_visibility") == "public"
        and redirects.get(node_id, node_id) == node_id
    }
    sources = {source.get("id") for source in data.get("sources", []) if source.get("id")}
    relations = {item.get("relation_type") for item in data.get("relation_types", [])}
    edges = {edge.get("id"): edge for edge in data.get("edges", []) if edge.get("id")}
    profiles = {profile.get("node_id"): profile for profile in data.get("profiles", []) if profile.get("node_id")}

    if meta.get("release") not in {RELEASE, "0.18-navigable-tangle-alpha", "0.19-living-marks-alpha", "0.20-prior-maps-alpha", "0.21"}:
        errors.append(f"meta.release must be {RELEASE}")
    if meta.get("generated") not in {GENERATED, "2026-08-23", "2026-08-25", "2026-08-31"}:
        errors.append(f"meta.generated must be {GENERATED}")
    if meta.get("project_url") != PUBLIC_URL:
        errors.append("custom-domain project URL is stale")

    missing_nodes = REQUIRED_NODES - public_ids
    if missing_nodes:
        errors.append(f"required 0.17 public nodes are missing: {sorted(missing_nodes)}")
    missing_sources = REQUIRED_SOURCES - sources
    if missing_sources:
        errors.append(f"required 0.17 public sources are missing: {sorted(missing_sources)}")
    missing_relations = REQUIRED_RELATIONS - relations
    if missing_relations:
        errors.append(f"required canon/recovery relation types are missing: {sorted(missing_relations)}")
    missing_edges = REQUIRED_EDGES - set(edges)
    if missing_edges:
        errors.append(f"required typed 0.17 connections are missing: {sorted(missing_edges)}")

    for edge_id in REQUIRED_EDGES & set(edges):
        edge = edges[edge_id]
        if edge.get("source") not in public_ids or edge.get("target") not in public_ids:
            errors.append(f"0.17 edge has a non-public endpoint: {edge_id}")
        if edge.get("relation_type") not in relations:
            errors.append(f"0.17 edge uses an unregistered relation: {edge_id}")
        if not edge.get("plain_phrase") or not edge.get("scope_conditions") or not parse(edge.get("source_ids")):
            errors.append(f"0.17 edge is not inspectable: {edge_id}")

    systems_thinkers = next((node for node in nodes.values() if node.get("label") == "Systems Thinkers"), None)
    jackson = next((node for node in nodes.values() if node.get("label") == "Michael C. Jackson"), None)
    if not systems_thinkers or systems_thinkers.get("publication_level") != "profile" or systems_thinkers.get("id") not in profiles:
        errors.append("Systems Thinkers has not been developed as a full entry")
    if not jackson or jackson.get("publication_level") != "profile" or jackson.get("id") not in profiles:
        errors.append("Michael C. Jackson has not been developed as a full entry")
    for node_id in ("person_magnus_ramage", "person_karen_shipp", "concept_canon_formation", "concept_epistemic_closure", "concept_epistemic_injustice", "practice_lineage_recovery", "concept_structurelessness", "concept_decolonial_systems_thinking"):
        if node_id not in profiles:
            errors.append(f"required 0.17 profile is missing: {node_id}")

    journeys = {journey.get("id"): journey for journey in data.get("journeys", []) if journey.get("id")}
    journey = journeys.get("journey_who_counts_as_a_systems_thinker")
    if not journey or len(journey.get("steps", [])) != 9:
        errors.append("canon and lineage guided journey is missing or incomplete")
    elif any(step.get("node_id") not in public_ids for step in journey.get("steps", [])):
        errors.append("canon and lineage guided journey contains a non-public step")

    submissions = data.get("site_submissions", {})
    items = submissions.get("items", [])
    if submissions.get("release") not in {RELEASE, "0.18-navigable-tangle-alpha", "0.19-living-marks-alpha", "0.20-prior-maps-alpha", "0.21"} or submissions.get("marker") != "Prepared from The Necessary Tangle":
        errors.append("site-submission projection metadata is missing or stale")
    if meta.get("site_submission_count") != len(items) or len(items) != 1:
        errors.append("the 0.17 release should surface the single structured submission found at publication time")
    else:
        item = items[0]
        if item.get("issue_number") != 21 or item.get("status") != "incorporated":
            errors.append("issue 21 is not represented with its incorporated status")
        if len(item.get("result_links", [])) < 3:
            errors.append("issue 21 does not expose its resulting atlas entries")

    visibility = data.get("canon_visibility_review", {})
    review_items = visibility.get("items", [])
    names = {item.get("name") for item in review_items}
    if visibility.get("release") != RELEASE or names != VISIBILITY_NAMES:
        errors.append("the public canon visibility review is incomplete or stale")
    for item in review_items:
        forbidden = {"ethnicity", "race", "religion", "gender", "nationality", "heritage"} & set(item)
        if forbidden:
            errors.append(f"canon visibility review infers or stores sensitive identity fields for {item.get('name')}: {sorted(forbidden)}")
        if "do not infer" not in str(item.get("next_work", "")).lower():
            errors.append(f"canon review item lacks the non-inference safeguard: {item.get('name')}")

    recalculated = calculate_relational_depth(data)
    if data.get("relational_depth") != recalculated:
        errors.append("relational-depth measures are stale after the 0.17 additions")
    aggregate = recalculated.get("aggregate", {})
    if meta.get("reader_connected_entry_count") != aggregate.get("reader_connected_entries"):
        errors.append("reader-connected entry count in metadata is stale")
    metrics = graph_metrics(data)
    if meta.get("public_entry_count") != metrics.get("public_entries"):
        errors.append("public-entry count in metadata is stale")
    if meta.get("profile_count") != len(profiles):
        errors.append("profile count in metadata is stale")
    if meta.get("source_count") != len(data.get("sources", [])):
        errors.append("source count in metadata is stale")
    if meta.get("journey_count") != len(data.get("journeys", [])):
        errors.append("journey count in metadata is stale")
    if meta.get("surprise_me_eligible_count", 0) < 50:
        errors.append("Surprise me has an implausibly small eligible pool")

    docs_json = json.loads(read("docs/assets/public-data.json"))
    if docs_json != data:
        errors.append("browser JSON is not identical to canonical public data")
    submissions_json = json.loads(read("docs/assets/site-submissions.json"))
    if submissions_json != submissions:
        errors.append("submission snapshot asset is not identical to canonical projection data")

    index = read("docs/index.html")
    for marker in (
        'href="/submissions/"',
        'id="surpriseMeNav"',
        'id="surpriseMeHero"',
        'class="plain-panel wide canon-lineage-panel"',
        'href="/canon-and-lineage/"',
        f"assets/styles.css?v={VERSION}",
        f"assets/site-enhancements.css?v={VERSION}",
        f"assets/iteration-17.css?v={VERSION}",
        f"assets/app.js?v={VERSION}",
        f"assets/iteration-17.js?v={VERSION}",
    ):
        if marker not in index:
            errors.append(f"0.17 home reader marker is missing: {marker}")

    surprise_js = read("docs/assets/iteration-17.js")
    for marker in ("window.crypto.getRandomValues", "['profile', 'described']", "from=surprise", "excludedTypes"):
        if marker not in surprise_js:
            errors.append(f"Surprise me behaviour is missing: {marker}")
    try:
        subprocess.run(["node", "--check", str(ROOT / "docs" / "assets" / "iteration-17.js")], check=True, capture_output=True, text=True)
    except FileNotFoundError:
        errors.append("node is unavailable for the 0.17 JavaScript syntax check")
    except subprocess.CalledProcessError as exc:
        errors.append(f"iteration-17.js does not parse: {exc.stderr.strip()}")

    submissions_page = ROOT / "docs" / "submissions" / "index.html"
    canon_page = ROOT / "docs" / "canon-and-lineage" / "index.html"
    if not submissions_page.exists() or submissions_page.stat().st_size < 7000:
        errors.append("public submissions page is missing or implausibly small")
    else:
        text = submissions_page.read_text(encoding="utf-8")
        for marker in ("Submissions and responses", "submissionFallback", "api.github.com/search/issues", "Issue", "Live GitHub register", "incorporated"):
            if marker not in text:
                errors.append(f"submissions page is missing: {marker}")
    if not canon_page.exists() or canon_page.stat().st_size < 5000:
        errors.append("canon and lineage page is missing or implausibly small")
    else:
        text = canon_page.read_text(encoding="utf-8")
        for marker in ("Who gets to count as a systems thinker?", "The map is also a confession", "The absence of a line is preferable", "People named in the current challenge"):
            if marker not in text:
                errors.append(f"canon and lineage page is missing: {marker}")

    workflow = read(".github/workflows/triage-site-submissions.yml")
    for marker in ("issue_comment:", "workflow_dispatch:", "site-submission", "awaiting-curator-review", "investigating", "incorporated", "partly-incorporated", "disputed", "deferred", "declined", "incorporated in release"):
        if marker not in workflow:
            errors.append(f"site-submission triage workflow is missing: {marker}")

    required_docs = {
        "documentation/site-submissions.md": ["GitHub Issues remains the canonical record", "Status vocabulary", "Issue 21"],
        "documentation/canon-lineage-and-identity.md": ["Editorial rule", "Closure and power", "Canon and recovery relations"],
        "documentation/company-knowledge-discovery-first-pass.md": ["Second bounded pass — 19 August 2026", "exhaustive file-by-file coverage is not established"],
        "documentation/feedback-ledger.md": ["Release 0.17 — public intake, serendipity and canon visibility"],
    }
    for path, markers in required_docs.items():
        file_path = ROOT / path
        if not file_path.exists():
            errors.append(f"required 0.17 documentation is missing: {path}")
            continue
        text = file_path.read_text(encoding="utf-8")
        for marker in markers:
            if marker not in text:
                errors.append(f"{path} is missing: {marker}")

    citation = read("CITATION.cff")
    readme = read("README.md")
    changelog = read("CHANGELOG.md")
    if f"version: {meta.get('release')}" not in citation or f"date-released: {meta.get('generated')}" not in citation or f"url: {PUBLIC_URL}" not in citation:
        errors.append("citation metadata does not identify release 0.17")
    if ("## Release 0.21" not in readme and "## Release 0.20" not in readme and "## Release 0.19" not in readme and "## Release 0.18" not in readme and "Release 0.17 contains" not in readme) or "https://transduction.systems/" not in readme:
        errors.append("README does not explain the 0.17 release and public routes")
    if f"## {RELEASE} — 19 August 2026" not in changelog:
        errors.append("0.17 changelog entry is missing")

    # The private discovery pass may shape work, but no private locator may enter public output.
    public_text = "\n".join([
        json.dumps(data, ensure_ascii=False),
        read("docs/index.html"),
        read("docs/submissions/index.html"),
        read("docs/canon-and-lineage/index.html"),
        read("documentation/company-knowledge-discovery-first-pass.md"),
        read("documentation/canon-lineage-and-identity.md"),
    ])
    for forbidden in ("redquadrantltd.sharepoint.com", "graph.microsoft.com/v1.0/drives", "redquadrantltd-my.sharepoint.com"):
        if forbidden in public_text:
            errors.append(f"private connected-source locator leaked into public output: {forbidden}")

    if errors:
        print("0.17 validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(json.dumps({
        "release": RELEASE,
        "public_entries": meta.get("public_entry_count"),
        "profiles": meta.get("profile_count"),
        "sources": meta.get("source_count"),
        "journeys": meta.get("journey_count"),
        "site_submissions": meta.get("site_submission_count"),
        "surprise_me_eligible": meta.get("surprise_me_eligible_count"),
        "canon_visibility_review": meta.get("canon_visibility_review_count"),
        "reader_connected_entries": meta.get("reader_connected_entry_count"),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
