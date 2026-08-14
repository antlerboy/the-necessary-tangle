#!/usr/bin/env python3
"""Validate the Pass 6 adversarial relationship result."""

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / "data" / "public-data.json").read_text(encoding="utf-8"))
quality = json.loads((ROOT / "data" / "relationship-quality.json").read_text(encoding="utf-8"))
index = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
reading = (ROOT / "docs" / "reading-list.html").read_text(encoding="utf-8")
relational_doc = (ROOT / "documentation" / "relational-depth.md").read_text(encoding="utf-8")
edges = data.get("edges", [])
ids = {edge.get("id") for edge in edges}

counts = Counter((edge.get("source"), edge.get("relation_type"), edge.get("target")) for edge in edges)
duplicates = [key for key, count in counts.items() if count > 1]
legacy_unlocated = [
    edge.get("id")
    for edge in edges
    if edge.get("claim_status") == "legacy_unverified"
    and edge.get("assertion_mode") == "candidate"
    and not str(edge.get("source_locator", "")).strip()
]
inferred = [edge.get("id") for edge in edges if edge.get("assertion_mode") == "inferred"]
fpcs_located = [
    edge
    for edge in edges
    if edge.get("id", "").startswith("e_08_fpcs_authored_")
    and "item " in str(edge.get("source_locator", ""))
]

checks = {
    "edge count reduced to 1670": len(edges) == 1670,
    "no exact duplicate triples": not duplicates,
    "no unlocated legacy candidates": not legacy_unlocated,
    "no untested inferred edges": not inferred,
    "19 bibliographic edges item-located": len(fpcs_located) == 19,
    "two-work coauthorship merged": "e_08_fpcs_coauthor_008_01" not in ids
    and any(edge.get("id") == "e_08_fpcs_coauthor_006_02" and "items 6" in edge.get("source_locator", "") for edge in edges),
    "candidate attribution kept provisional": any(
        edge.get("id") == "e_0301" and edge.get("claim_status") == "provisional_needs_primary_check"
        for edge in edges
    ),
    "machine audit present": quality.get("adversarial_review", {}).get("after", {}).get("exact_duplicate_triples") == 0,
    "magic dot validator retained": (ROOT / "scripts" / "validate_overnight_experience.py").exists(),
    "reading list has landmarks and updates dot": '<main id="reading-main"' in reading
    and '<nav class="reading-nav"' in reading
    and 'aria-label="Open updates"' in reading,
    "reading list constrains mobile table": ".reading-table-wrap" in reading and "table-layout:fixed" in reading,
    "heading hierarchy repaired": '<h2 class="hidden" id="browseResultsHeading">' in index
    and '<h2 class="control-heading">Find a path</h2>' in index,
    "relational document matches adversarial graph": "486 of 496 entries" in relational_doc
    and "316 have at least one non-documentary" in relational_doc,
}

failed = [label for label, ok in checks.items() if not ok]
if failed:
    raise SystemExit("Pass 6 adversarial validation failed: " + ", ".join(failed))
print("Pass 6 adversarial validation passed (13 checks).")
