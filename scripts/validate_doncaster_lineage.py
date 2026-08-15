#!/usr/bin/env python3
"""Validate the Doncaster lineage extension and its privacy/epistemic boundaries."""

import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / "data" / "public-data.json").read_text(encoding="utf-8"))
quality = json.loads((ROOT / "data" / "relationship-quality.json").read_text(encoding="utf-8"))
rendered = (ROOT / "data" / "public-data.json").read_text(encoding="utf-8")
audit_doc = (ROOT / "documentation" / "doncaster-lineage-audit.md").read_text(encoding="utf-8")

nodes = {item["id"]: item for item in data.get("nodes", [])}
sources = {item["id"]: item for item in data.get("sources", [])}
edges = data.get("edges", [])
don_edges = [item for item in edges if str(item.get("id", "")).startswith("e_don_")]
review = data.get("doncaster_lineage_review", {})
coverage = review.get("coverage", [])
coverage_ids = {item.get("node_id") for item in coverage}
triples = Counter((item.get("source"), item.get("relation_type"), item.get("target")) for item in edges)

private_sources = [item for item in sources.values() if item.get("id") in {
    "src_doncaster_interview_2026", "src_damian_lineage_diagram_2026",
    "src_damian_correspondence_2026", "src_doncaster_key_messages_2026",
}]
utsi_edges = [item for item in don_edges if item.get("source") == "theory_unified_systems_intelligence"]
epistemic_topics = {item.get("topic") for item in review.get("epistemic_boundaries", [])}

checks = {
    "extension applied": data.get("meta", {}).get("doncaster_lineage_extension") == "doncaster-lineage-2026-08-15",
    "Damian profile present": any(item.get("node_id") == "person_damian_allen" for item in data.get("profiles", [])),
    "Thrive profile present": any(item.get("node_id") == "practice_doncaster_thrive" for item in data.get("profiles", [])),
    "HLS profile present": any(item.get("node_id") == "practice_human_learning_systems" for item in data.get("profiles", [])),
    "UTSI profile is provisional": any(
        item.get("node_id") == "theory_unified_systems_intelligence"
        and item.get("profile_status") == "provisional_self_reported_unpublished"
        for item in data.get("profiles", [])
    ),
    "guided journey present": any(item.get("id") == "journey_doncaster_thrive_lineage" for item in data.get("journeys", [])),
    "coverage matrix has 81 items": len(coverage) == 81 and coverage_ids <= set(nodes),
    "139 new typed relationships": len(don_edges) == 139,
    "every relationship is typed and directed-declared": all(
        item.get("relation_type") and item.get("relation_family") and item.get("directed") in {"true", "false"}
        for item in don_edges
    ),
    "every relationship has rationale and source locator": all(
        str(item.get("notes", "")).strip()
        and str(item.get("source_locator", "")).strip()
        and json.loads(item.get("source_ids", "[]"))
        for item in don_edges
    ),
    "no generic related-to edges": all(
        item.get("relation_type") != "conceptually_related_to"
        and "related to" not in str(item.get("plain_phrase", "")).lower()
        for item in don_edges
    ),
    "UTSI edges remain unpublished and provisional": len(utsi_edges) >= 17 and all(
        item.get("claim_status") == "provisional_self_reported_unpublished" for item in utsi_edges
    ),
    "four private sources are metadata-only": len(private_sources) == 4 and all(
        item.get("access") == "private"
        and item.get("public_link_status") == "no_public_link"
        and not item.get("url")
        for item in private_sources
    ),
    "private identifiers are absent": "mail.google.com" not in rendered
    and "@doncaster.gov.uk" not in rendered
    and not re.search(r'attachment_id|thread_id|message_id', rendered, re.IGNORECASE),
    "key uncertainties are machine-readable": {
        "Bruce Edmonds", "Complexity book", "Tony Hodgson and Three Horizons",
        "Nested Minimum Viable Systems", "Unified Theory of Systems Intelligence",
        "UTSI framework count", "Thrive outcomes",
    } <= epistemic_topics,
    "no exact duplicate triples": all(count == 1 for count in triples.values()),
    "machine quality mirror present": quality.get("doncaster_lineage_review", {}).get("after", {}).get("new_typed_relationships") == 139,
    "audit document is candid": all(text in audit_doc for text in [
        "probable identity normalization", "unpublished proto-theory",
        "not an independent outcome evaluation", "more than 11",
    ]),
}

failed = [label for label, ok in checks.items() if not ok]
if failed:
    raise SystemExit("Doncaster lineage validation failed: " + ", ".join(failed))
print(f"Doncaster lineage validation passed ({len(checks)} checks; {len(don_edges)} relationships; {len(coverage)} coverage items).")
