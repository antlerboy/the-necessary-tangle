#!/usr/bin/env python3
"""Validate release 0.14 Snowden, Cynefin, source roles and discreet update access."""
from __future__ import annotations

import base64
import json
import re
import sys
from pathlib import Path

from apply_iteration_09 import graph_metrics

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "public-data.json"
DOCS = ROOT / "docs"
RELEASE = "0.14-snowden-cynefin-alpha"
GENERATED = "2026-08-11"
FORWARD_RELEASES = {"0.15-ing-reading-practice-alpha", "0.16-grammar-connections-presentation-alpha", "0.17-public-intake-lineage-alpha", "0.18-navigable-tangle-alpha", "0.19-living-marks-alpha", "0.20-prior-maps-alpha", "0.21"}
FORWARD_GENERATED = "2026-08-14"
UPDATE_URL = "https://github.com/antlerboy/the-necessary-tangle/" + "issues/" + "2"

REQUIRED_NODES = {
    "person_dave_snowden", "person_cynthia_f_kurtz", "person_mary_e_boone", "person_alessandro_rancati",
    "organisation_the_cynefin_company", "corpus_dave_snowden_blog", "corpus_cynefin_io_wiki",
    "method_or_methodology_cynefin_framework", "tool_sensemaker", "tradition_anthro_complexity",
    "approach_family_naturalising_sense_making", "concept_bounded_applicability",
    "method_or_methodology_estuarine_mapping", "method_or_methodology_distributed_ethnography",
    "publication_complex_acts_of_knowing", "publication_new_dynamics_of_strategy",
    "publication_leaders_framework_decision_making", "publication_managing_complexity_chaos_field_guide",
    "publication_cynefin_weaving_sensemaking",
}
REQUIRED_SOURCES = {
    "src_cynefin_dave_profile_2026", "src_cynefin_dave_blog_archive_2026", "src_cynefin_company_home_2026",
    "src_cynefin_io_main_2026", "src_cynefin_io_framework_2026", "src_cynefin_io_anthro_complexity_2026",
    "src_cynefin_io_naturalising_2026", "src_cynefin_sensemaker_official_2026",
    "src_cynefin_estuarine_mapping_2022", "src_cynefin_complex_acts_2002",
    "src_cynefin_new_dynamics_2003", "src_hbr_leaders_framework_2007", "src_jrc_complexity_crisis_2021",
    "src_cynefin_field_guide_library_2021", "src_cynefin_weaving_book_2020",
}
REQUIRED_OBSERVATIONS = {
    "breadth_outpaces_depth", "two_graph_regimes", "canonical_sources_have_jobs", "expertise_needs_relations",
    "first_party_needs_counterweight", "catalogue_is_not_critique", "practice_is_peripheral",
    "source_monoculture", "identity_resolution", "neighbourhoods_are_stale", "bridge_concepts",
    "map_of_attention", "automated_overreading",
}
FORBIDDEN_PATTERNS = tuple(
    base64.b64decode(value).decode("utf-8")
    for value in (
        "XGJDaGF0R1BUXGI=",
        "XGJPcGVuQUlcYg==",
        "dGhpcyBjb252ZXJzYXRpb24=",
        "dGhlc2UgY29udmVyc2F0aW9ucw==",
        "b3VyIGNvbnZlcnNhdGlvbg==",
        "Y2hhdCB0cmFuc2NyaXB0",
        "cnVubmluZyBmZWVkYmFjayB0aHJlYWQ=",
        "cnVubmluZyBjb21tZW50IHRocmVhZA==",
        "cnVubmluZyBub3RlYm9vaw==",
        "c2l0ZSBzdWJtaXNzaW9uICMyMQ==",
        "aXNzdWUgIzIx",
        "cHJpdmF0ZSB3b3JraW5nIGV4Y2hhbmdlcw==",
        "ZWRpdG9yaWFsIGJhY2tzdG9yeQ==",
        "YnJva2VuIGludGFrZSBsb29w",
        "bWlzc2VkIGJ5IGFuIGVhcmxpZXIgcmVsZWFzZQ==",
        "UGF0cmljayBIb3ZlcnN0YWR0J3MgYWJzZW5jZQ==",
        "SXZvIFZlbGl0Y2hrb3YncyBzaXRlIHN1Ym1pc3Npb24=",
        "d2Ugb21pdHRlZA==",
        "eW91IGFza2Vk",
        "YXMgcmVxdWVzdGVk",
        "c3VwZXJzZWRlZCAyOTUtZW50cnkgYnJhbmNo",
        "cmVjb3ZlcmVkIGZyb20gdGhlIHN1cGVyc2VkZWQ=",
    )
)
SECRET_PATTERNS = (
    re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
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
    nodes = {node.get("id"): node for node in data.get("nodes", []) if node.get("id")}
    profiles = {profile.get("node_id"): profile for profile in data.get("profiles", []) if profile.get("node_id")}
    sources = {source.get("id"): source for source in data.get("sources", []) if source.get("id")}
    edges = {edge.get("id"): edge for edge in data.get("edges", []) if edge.get("id")}
    journeys = {journey.get("id"): journey for journey in data.get("journeys", []) if journey.get("id")}
    public_nodes = [
        node for node in data.get("nodes", [])
        if node.get("public_visibility") == "public" and redirects.get(node["id"], node["id"]) == node["id"]
    ]
    public_ids = {node["id"] for node in public_nodes}
    developed = len(set(profiles) & public_ids)

    if meta.get("release") not in {RELEASE, *FORWARD_RELEASES}:
        errors.append(f"meta.release must be {RELEASE} or a recognised forward release")
    expected_generated = "2026-08-31" if meta.get("release") == "0.21" else ("2026-08-25" if meta.get("release") in {"0.19-living-marks-alpha", "0.20-prior-maps-alpha"} else ("2026-08-23" if meta.get("release") == "0.18-navigable-tangle-alpha" else ("2026-08-19" if meta.get("release") == "0.17-public-intake-lineage-alpha" else (GENERATED if meta.get("release") == RELEASE else FORWARD_GENERATED))))
    if meta.get("generated") != expected_generated:
        errors.append(f"meta.generated must be {expected_generated}")
    for label, actual, minimum in [
        ("public entries", len(public_nodes), 483),
        ("developed profiles", developed, 99),
        ("sources", len(sources), 140),
        ("journeys", len(journeys), 16),
        ("raw typed edge records", len(data.get("edges", [])), 994),
    ]:
        if actual < minimum:
            errors.append(f"expected at least {minimum} {label}, found {actual}")
    if meta.get("public_entry_count") != len(public_nodes):
        errors.append("meta public-entry count is stale")
    if meta.get("profile_count") != developed:
        errors.append("meta profile count is stale")
    if meta.get("source_count") != len(sources):
        errors.append("meta source count is stale")
    if meta.get("journey_count") != len(journeys):
        errors.append("meta journey count is stale")

    for node_id in sorted(REQUIRED_NODES):
        node = nodes.get(node_id)
        profile = profiles.get(node_id)
        if not node:
            errors.append(f"missing 0.14 entry: {node_id}")
            continue
        if node_id not in public_ids or node.get("publication_level") != "profile":
            errors.append(f"0.14 entry is not a canonical developed public entry: {node_id}")
        if not profile:
            errors.append(f"0.14 entry lacks a profile: {node_id}")
            continue
        for field in (
            "summary", "why_it_matters", "key_distinctions", "historical_lineage", "logical_antecedents",
            "dependent_subsequents", "practice_connections", "common_misreadings", "open_checks", "source_ids",
        ):
            if not profile.get(field):
                errors.append(f"0.14 profile {node_id} lacks {field}")
        linked = set(parse(node.get("source_ids"))) | set(parse(profile.get("source_ids")))
        if not linked or not linked.issubset(sources):
            errors.append(f"0.14 entry has missing or unknown sources: {node_id}")

    for source_id in sorted(REQUIRED_SOURCES):
        source = sources.get(source_id)
        if not source:
            errors.append(f"missing 0.14 source: {source_id}")
            continue
        if not str(source.get("url", "")).startswith("https://"):
            errors.append(f"0.14 source lacks a public HTTPS URL: {source_id}")
        if source.get("review_status") != "checked" or source.get("last_checked") != GENERATED:
            errors.append(f"0.14 source lacks current checked metadata: {source_id}")
        if not source.get("notes"):
            errors.append(f"0.14 source lacks role and limitation notes: {source_id}")

    new_edges = [edge for edge_id, edge in edges.items() if str(edge_id).startswith("e_14_")]
    if len(new_edges) != 39:
        errors.append(f"expected 39 0.14 relations, found {len(new_edges)}")
    for edge in new_edges:
        for field in (
            "source", "target", "relation_type", "relation_family", "plain_phrase", "claim_status",
            "confidence", "source_ids", "scope_conditions", "notes",
        ):
            if not edge.get(field):
                errors.append(f"0.14 relation {edge.get('id')} lacks {field}")
        if edge.get("relation_type") == "legacy_association_unspecified":
            errors.append(f"0.14 relation uses unresolved legacy semantics: {edge.get('id')}")
        if not set(parse(edge.get("source_ids"))).issubset(sources):
            errors.append(f"0.14 relation cites an unknown source: {edge.get('id')}")

    journey = journeys.get("journey_snowden_cynefin_sources_and_practice")
    if not journey or len(journey.get("steps", [])) < 13:
        errors.append("Snowden and Cynefin source journey is missing or too short")
    elif any(step.get("node_id") not in public_ids or not step.get("heading") or not step.get("narrative") for step in journey.get("steps", [])):
        errors.append("Snowden and Cynefin source journey has incomplete steps")

    dave_text = json.dumps(profiles.get("person_dave_snowden", {}), ensure_ascii=False).casefold()
    for term in ("cynefin", "sensemaker", "naturalising sense-making", "anthro-complexity"):
        if term not in dave_text:
            errors.append(f"Dave Snowden profile lacks expertise term: {term}")
    source_doc = ROOT / "documentation" / "snowden-cynefin-sources.md"
    if not source_doc.exists() or source_doc.stat().st_size < 2200:
        errors.append("Snowden and Cynefin source-role document is missing or too small")
    else:
        source_doc_text = source_doc.read_text(encoding="utf-8").casefold()
        for term in ("author archive", "cynefin.io", "independent", "first-party", "joint research centre"):
            if term not in source_doc_text:
                errors.append(f"source-role document lacks: {term}")

    canonical = {item.get("source_id"): item for item in data.get("canonical_source_register", []) if item.get("source_id")}
    for source_id in ("src_cynefin_dave_blog_archive_2026", "src_cynefin_io_main_2026", "src_cynefin_company_home_2026", "src_jrc_complexity_crisis_2021"):
        if source_id not in canonical:
            errors.append(f"canonical source register lacks {source_id}")
    mining = {item.get("id"): item for item in data.get("source_mining_register", []) if item.get("id")}
    if mining.get("mine_snowden_cynefin", {}).get("status") != "active_canonical_source_pass":
        errors.append("Snowden-Cynefin continuing source programme is missing")

    report = data.get("ai_observations", {})
    if report.get("release") != meta.get("release") or report.get("generated") != meta.get("generated"):
        errors.append("AI observations were not regenerated for the current release")
    observations = report.get("observations", [])
    if not REQUIRED_OBSERVATIONS.issubset({item.get("id") for item in observations}):
        errors.append("0.14 AI observation set is incomplete or stale")
    for observation in observations:
        for field in ("title", "kind", "measurement", "interpretation", "implication", "test"):
            if not observation.get(field):
                errors.append(f"AI observation {observation.get('id')} lacks {field}")
    if report.get("metrics") != graph_metrics(data):
        errors.append("AI observation metrics do not match the current graph")
    ai_doc = ROOT / "documentation" / "ai-observations.md"
    if not ai_doc.exists() or f"Generated for release `{meta.get('release')}` on {meta.get('generated')}." not in ai_doc.read_text(encoding="utf-8"):
        errors.append("maintained AI observation document is stale")

    index = DOCS / "index.html"
    css = DOCS / "assets" / "site-enhancements.css"
    index_text = index.read_text(encoding="utf-8")
    css_text = css.read_text(encoding="utf-8")
    exact_anchor = f'<a class="update-thread-dot" data-update-thread-dot href="{UPDATE_URL}" target="_blank" rel="noopener" aria-label="Open updates"></a>'
    if index_text.count(exact_anchor) != 1:
        errors.append("the discreet bottom-right update route is missing or duplicated")
    if index_text.count(UPDATE_URL) != 1:
        errors.append("the update-thread URL must occur exactly once in the rendered page")
    if ".update-thread-dot" not in css_text or "position: fixed" not in css_text:
        errors.append("the bottom-right update route lacks fixed discreet styling")
    for marker in (
        "person_dave_snowden", "method_or_methodology_cynefin_framework",
        "journey_snowden_cynefin_sources_and_practice", "cynefin-source-panel",
        "documentation/snowden-cynefin-sources.md",
    ):
        if marker not in index_text:
            errors.append(f"0.14 public interface is missing {marker}")

    public_paths = sorted({
        DATA_PATH,
        *DOCS.rglob("*.html"), *DOCS.rglob("*.js"), *DOCS.rglob("*.css"), *DOCS.rglob("*.json"),
        *(ROOT / "documentation").glob("*.md"),
        ROOT / "README.md", ROOT / "ACKNOWLEDGEMENTS.md", ROOT / "CHANGELOG.md", ROOT / "CITATION.cff",
    }, key=lambda path: str(path))
    chunks = []
    for path in public_paths:
        text = path.read_text(encoding="utf-8", errors="ignore")
        if path == index:
            text = text.replace(exact_anchor, "")
        chunks.append(text)
    public_text = "\n".join(chunks)
    for pattern in FORBIDDEN_PATTERNS:
        if re.search(pattern, public_text, flags=re.I):
            errors.append(f"public repository contains internal or conversation-derived framing: {pattern}")
    for pattern in SECRET_PATTERNS:
        if pattern.search(public_text):
            errors.append(f"public repository contains secret-like material: {pattern.pattern}")
    for marker in ("sandbox:/", "file://", "/mnt/data", "c:\\users\\", "c:/users/", "redquadrantltd.sharepoint"):
        if marker.casefold() in public_text.casefold():
            errors.append(f"public repository contains local or private marker: {marker}")

    citation = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    if f"version: {meta.get('release')}" not in citation or f"date-released: {meta.get('generated')}" not in citation:
        errors.append("citation metadata does not identify the current release")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    release_phrase = {
        RELEASE: "Release 0.14 contains",
        "0.15-ing-reading-practice-alpha": "Release 0.15 contains",
        "0.16-grammar-connections-presentation-alpha": "Release 0.16 contains",
    }.get(meta.get("release"), "")
    if release_phrase not in readme or "snowden-cynefin-sources.md" not in readme:
        errors.append("README does not preserve the 0.14 source account and identify the current release")
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    if "## 0.14-snowden-cynefin-alpha" not in changelog:
        errors.append("changelog lacks 0.14")

    if errors:
        print("ITERATION 0.14 VALIDATION FAILED", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("ITERATION 0.14 VALIDATION PASSED")
    print(f"- canonical public entries: {len(public_nodes)}")
    print(f"- developed profiles: {developed}")
    print(f"- sources: {len(sources)}")
    print(f"- journeys: {len(journeys)}")
    print(f"- raw typed edge records: {len(data.get('edges', []))}")
    print(f"- new Snowden-Cynefin relations: {len(new_edges)}")
    print(f"- AI observations regenerated: {len(observations)}")
    print("- one discreet fixed update route present")
    print("- no internal conversation or editorial-backstory framing in public files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
