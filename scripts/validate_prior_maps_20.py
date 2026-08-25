#!/usr/bin/env python3
"""Validate the 0.20 prior-map publication and its rights/evidence boundary."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

from apply_prior_maps_20 import GENERATED, READER_HOTFIX_VERSION, RELEASE

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def load(path: str) -> dict:
    return json.loads(read(path))


def walk_keys(value: object) -> list[str]:
    keys: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            keys.append(str(key))
            keys.extend(walk_keys(child))
    elif isinstance(value, list):
        for child in value:
            keys.extend(walk_keys(child))
    return keys


def main() -> int:
    errors: list[str] = []
    atlas = load("data/public-data.json")
    systemic = load("data/comparator-systemic-evolution.json")
    reconciliation = load("data/systemic-evolution-reconciliation.json")
    castellani = load("data/comparator-castellani-links.json")
    counted = load("data/counted-map-public.json")

    meta = atlas.get("meta", {})
    if meta.get("release") != RELEASE or meta.get("generated") != GENERATED:
        errors.append(f"canonical release metadata must be {RELEASE} / {GENERATED}")
    if meta.get("comparator_count") != 3:
        errors.append("meta.comparator_count must be 3")

    browser = load("docs/assets/public-data.json")
    if browser != atlas:
        errors.append("browser public-data JSON differs from canonical data")
    for name in (
        "comparator-systemic-evolution.json",
        "systemic-evolution-reconciliation.json",
        "comparator-castellani-links.json",
        "counted-map-public.json",
    ):
        if (ROOT / "data" / name).read_bytes() != (ROOT / "docs" / "assets" / name).read_bytes():
            errors.append(f"published comparator asset differs from data/{name}")

    if systemic.get("meta", {}).get("node_count") != 650 or len(systemic.get("nodes", [])) != 650:
        errors.append("Systemic Evolution must retain all 650 source nodes")
    if systemic.get("meta", {}).get("edge_count") != 1320 or len(systemic.get("edges", [])) != 1320:
        errors.append("Systemic Evolution must retain all 1,320 source links")
    direction_counts = Counter(edge.get("direction_status") for edge in systemic.get("edges", []))
    if direction_counts != Counter({"source_to_target": 1262, "bidirectional": 58}):
        errors.append(f"Systemic Evolution direction census changed: {dict(direction_counts)}")
    for edge in systemic.get("edges", []):
        if edge.get("relation_type") != "reported_major_influence":
            errors.append(f"Systemic edge {edge.get('comparator_edge_id')} has the wrong source meaning")
            break
        if edge.get("accuracy_status") != "source_reported_not_independently_verified":
            errors.append(f"Systemic edge {edge.get('comparator_edge_id')} is not visibly unverified")
            break
        if edge.get("specific_relation_status") != "not_stated_by_source":
            errors.append(f"Systemic edge {edge.get('comparator_edge_id')} overstates edge-specific evidence")
            break

    systemic_text = json.dumps(systemic, ensure_ascii=False).lower()
    if "directed edges illustrate major influences" not in systemic_text:
        errors.append("source-reported major-influence wording is missing")
    if "no edge meaning" in systemic_text or "no colour legend" in systemic_text:
        errors.append("superseded no-meaning/no-legend description remains in comparator data")
    for realm in (
        "general system", "cybernetics", "physical sciences", "mathematics", "computers and informatics",
        "biology and medicine", "symbolic systems", "social systems", "ecology", "philosophy",
        "systems analysis", "engineering",
    ):
        if realm not in read("documentation/comparator-systemic-evolution.md").lower() and realm == "general system":
            errors.append("published source legend does not explain the general-system/white caveat")

    summary = reconciliation.get("meta", {}).get("summary", {})
    expected_summary = {
        "source_nodes_retained": 650,
        "source_links_retained": 1320,
        "source_nodes_confirmed": 5,
        "source_nodes_partially_reconciled": 57,
        "source_nodes_unresolved": 588,
        "distinct_atlas_entries_linked": 66,
        "source_links_both_endpoints_mapped": 47,
        "source_links_one_endpoint_mapped": 231,
        "source_links_no_endpoints_mapped": 1042,
        "source_links_with_independent_atlas_relation": 1,
        "canonical_atlas_relations_created_from_source_links": 0,
    }
    if summary != expected_summary:
        errors.append(f"cumulative reconciliation summary changed: {summary}")
    if len(reconciliation.get("nodes", [])) != 650 or len(reconciliation.get("links", [])) != 1320:
        errors.append("reconciliation must contain every source node and link")

    cmeta = castellani.get("meta", {})
    links = castellani.get("links", [])
    if (len(links), cmeta.get("link_count"), cmeta.get("unique_destination_count")) != (307, 307, 307):
        errors.append("Castellani projection must retain 307 links and 307 destinations")
    if sum(bool(link.get("label_disagreement")) for link in links) != 28:
        errors.append("Castellani label-disagreement census must remain 28")
    for link in links:
        if urlparse(str(link.get("href", ""))).scheme not in {"http", "https"}:
            errors.append(f"unsafe Castellani destination scheme: {link.get('href')}")
            break
        if link.get("accuracy_status") != "source_link_not_independently_checked":
            errors.append(f"Castellani link {link.get('source_link_id')} lacks the unverified status")
            break
    if len({link.get("source_link_id") for link in links}) != 307:
        errors.append("Castellani source-link identifiers are not unique")

    counted_meta = counted.get("meta", {})
    if counted_meta.get("concept_count") != 98 or len(counted.get("concepts", [])) != 98:
        errors.append("counted-map concept count must remain 98")
    if counted_meta.get("evidenced_concept_count") != 89:
        errors.append("counted-map evidenced-concept count must remain 89")
    if counted_meta.get("edge_count") != 1856 or len(counted.get("edges", [])) != 1856:
        errors.append("counted-map must retain all 1,856 aggregate signals")
    if counted_meta.get("raw_reference_string_count_published") != 0:
        errors.append("counted-map must publish zero raw reference strings")
    forbidden_keys = {"reference", "references", "citing_eid", "eid", "abstract", "affiliations", "keywords"}
    exposed = sorted(forbidden_keys.intersection(key.lower() for key in walk_keys(counted)))
    if exposed:
        errors.append(f"counted-map exposes forbidden licensed/private fields: {exposed}")
    counted_text = json.dumps(counted, ensure_ascii=False).lower()
    if "claude" + ".ai" in counted_text:
        errors.append("counted-map exposes a private Claude URL")
    for edge in counted.get("edges", []):
        if edge.get("relation_type") != "keyword_labelled_citation_signal" or edge.get("accuracy_status") != "aggregate_signal_not_independently_reproduced":
            errors.append(f"counted-map signal {edge.get('id')} overstates its semantics")
            break

    atlas_nodes = {node.get("id") for node in atlas.get("nodes", [])}
    atlas_edges = {edge.get("id") for edge in atlas.get("edges", [])}
    gap_nodes = {node_id for node_id in atlas_nodes if str(node_id).startswith("knowledge_domain_")}
    required_gap_ids = {
        "knowledge_domain_complexity_and_public_health", "knowledge_domain_complexity_and_healthcare",
        "knowledge_domain_computational_social_science", "knowledge_domain_digital_social_science",
        "knowledge_domain_qualitative_complexity", "knowledge_domain_applied_complexity",
        "knowledge_domain_complexity_and_geography", "knowledge_domain_complexity_management_and_planning",
        "knowledge_domain_psychology_and_systems_theory", "knowledge_domain_social_systems_theory",
        "knowledge_domain_evolutionary_game_theory", "knowledge_domain_graph_theory",
        "knowledge_domain_scaling_in_complex_systems", "knowledge_domain_computational_science",
        "knowledge_domain_computational_biology", "knowledge_domain_computational_complexity_theory",
        "knowledge_domain_big_data",
    }
    if not required_gap_ids.issubset(gap_nodes):
        errors.append(f"Castellani gap domains missing: {sorted(required_gap_ids - gap_nodes)}")
    required_gap_edges = {"e_castellani_" + node_id.removeprefix("knowledge_domain_") + "_member" for node_id in required_gap_ids}
    if not required_gap_edges.issubset(atlas_edges):
        errors.append(f"Castellani documentary edges missing: {sorted(required_gap_edges - atlas_edges)}")

    required_sources = {
        "src_schwarz_streams", "src_uranos_systemic_evolution",
        "src_castellani_map_complexity_sciences", "src_nigel_systems_map_fork_2026",
    }
    source_ids = {source.get("id") for source in atlas.get("sources", [])}
    if not required_sources.issubset(source_ids):
        errors.append(f"prior-map source records missing: {sorted(required_sources - source_ids)}")

    required_pages = {
        "docs/prior-maps/index.html": ["Preservation is not endorsement", "1,856", "Nigel Williams"],
        "docs/prior-maps/systemic-evolution/index.html": ["All 1,320", "major influences between topics", "Cumulative reconciliation ledger", "Benjamin Hadorn"],
        "docs/prior-maps/castellani/index.html": ["All 307", "without claiming they are all current", "28"],
        "docs/prior-maps/counted-map/index.html": ["keyword-labelled citation signal", "1,856", "zero"],
        "docs/contributors/nigel-williams/index.html": ["Nigel Williams", "What has been incorporated", "not inaccurately"],
        "documentation/external-map-link-policy.md": ["Retain every available link", "never becomes a canonical atlas relation"],
        "documentation/comparator-systemic-evolution.md": ["major influences", "1,320", "zero canonical relations"],
        "documentation/NEXT_WORK.md": ["release 0.20 is complete", "No further production change is authorised"],
        "documentation/TANGLE_STATE.md": [RELEASE, "Canonical relations created merely from comparator imports: 0"],
        "README.md": ["## Release 0.20", "/prior-maps/systemic-evolution/"],
        "CHANGELOG.md": [RELEASE],
        "CITATION.cff": [f"version: {RELEASE}", f"date-released: {GENERATED}"],
        "RIGHTS.md": ["Benjamin Hadorn's permission", "raw cited-reference strings"],
        "ACKNOWLEDGEMENTS.md": ["Nigel Williams", "Eric Schwarz (1996)", "IIGSS (2000–01)", "Benjamin Hadorn (2016)"],
        "documentation/ai-observations.md": [
            "A line on one map is not the same claim as a line on another",
            "Overlap is not agreement",
            "Preserving every link makes disagreement inspectable",
            "Aggregation sets an evidential ceiling",
        ],
    }
    for path, markers in required_pages.items():
        body = read(path)
        for marker in markers:
            if marker not in body:
                errors.append(f"required marker missing from {path}: {marker}")

    repository_text = "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for path in ROOT.rglob("*")
        if path.is_file() and ".git" not in path.parts and path.suffix in {".md", ".html", ".js", ".json", ".py"}
    ).lower()
    if "https://" + "claude.ai" in repository_text:
        errors.append("a private Claude artefact URL remains in public repository content")
    if read("docs/index.html").count("data-update-thread-dot") != 1:
        errors.append("the update-thread dot is missing or duplicated")
    if 'href="/prior-maps/"' not in read("docs/index.html"):
        errors.append("the main reader does not expose the prior-map hub")
    index = read("docs/index.html")
    if f"assets/iteration-18.js?v={READER_HOTFIX_VERSION}" not in index:
        errors.append("the Surprise-me script does not have the 0.20 hotfix cache key")
    if "Updated for 0.20:" not in index or "Updated for 0.18:" in index:
        errors.append("the public AI-observations notice is stale")
    surprise_js = read("docs/assets/iteration-18.js")
    if "normaliseLegacySurpriseRoute" not in surprise_js or "params.set('from', 'home')" not in surprise_js:
        errors.append("legacy from=surprise routes are not normalised before application routing")
    observation_ids = {item.get("id") for item in atlas.get("ai_observations", {}).get("observations", [])}
    required_observation_ids = {
        "comparator_links_have_different_meanings",
        "overlap_is_not_agreement",
        "link_preservation_exposes_disagreement",
        "aggregation_sets_an_evidential_ceiling",
    }
    if not required_observation_ids.issubset(observation_ids):
        errors.append(f"0.20 AI observations missing: {sorted(required_observation_ids - observation_ids)}")

    if errors:
        print("Release 0.20 prior-map validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(
        f"Validated {RELEASE}: 650/1,320 Systemic Evolution, 307 Castellani, "
        "98/1,856 counted-map, zero comparator-derived canonical relations"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
