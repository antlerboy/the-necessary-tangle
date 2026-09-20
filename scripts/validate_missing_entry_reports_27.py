#!/usr/bin/env python3
"""Validate release 0.27 report coverage, evidence boundaries, and projections."""
from pathlib import Path
import hashlib
import json

from apply_release_21 import COMPARATOR_SHA256, RECONCILIATION_SHA256
from refresh_graph_snapshot import calculate

ROOT = Path(__file__).resolve().parents[1]
PACKET = json.loads(
    (ROOT / "sources/missing-entry-reports-2026-09-20/review.json").read_text(encoding="utf-8")
)
DATA = json.loads((ROOT / "data/public-data.json").read_text(encoding="utf-8"))
DOCS_DATA = json.loads((ROOT / "docs/assets/public-data.json").read_text(encoding="utf-8"))
EXPECTED = [69, 70, 72, 73, 74, 75, 76, 77, 80, 81, 82, 83, 84, 85, 86]

assert DATA == DOCS_DATA
assert DATA["meta"]["release"] == PACKET["release"] == "0.27"
assert DATA["graph_snapshot"] == calculate(DATA)
assert DATA["missing_entry_reports_20260920"]["issues"] == EXPECTED
assert [item["issue"] for item in PACKET["profiles"]] == EXPECTED

nodes = {node["id"]: node for node in DATA["nodes"]}
profiles = {profile["node_id"]: profile for profile in DATA["profiles"]}
sources = {source["id"] for source in DATA["sources"]}
queue = {row["number"]: row for row in DATA["september_connections"]["queue"]}

for item in PACKET["profiles"]:
    issue = item["issue"]
    node = nodes[item["node_id"]]
    profile = profiles[item["node_id"]]
    report_source = f"src_reports27_issue_{issue}"
    assert node["publication_level"] == "profile"
    assert node["review_status"] == "source_scoped_report_review_complete"
    assert profile["profile_status"] == "source_scoped_report_review_complete"
    assert profile["report_issue"] == issue
    assert profile["report_outcome"] == item["outcome"]
    assert json.loads(profile["open_checks"])
    assert json.loads(profile["common_misreadings"])
    assert report_source in json.loads(profile["source_ids"])
    assert set(json.loads(profile["source_ids"])) <= sources
    assert queue[issue]["canonical_id"] == item["node_id"]
    assert queue[issue]["status"] == "report_review_published"
    assert queue[issue]["review_url"] == "https://transduction.systems/updates/2026-09-20/"

release_edges = [edge for edge in DATA["edges"] if edge.get("connection_pass") == "missing_entry_reports_20260920"]
assert len(release_edges) == len(PACKET["relations"]) == 7
for edge in release_edges:
    assert edge["source"] in nodes and edge["target"] in nodes
    assert edge["source"] != edge["target"]
    assert edge["relation_type"] != "related_to"
    assert edge["source_locator"] and edge["scope_conditions"]
    assert set(json.loads(edge["source_ids"])) <= sources
    assert edge["claim_status"] == "candidate"

page = (ROOT / "docs/updates/2026-09-20/index.html").read_text(encoding="utf-8")
for item in PACKET["profiles"]:
    assert f'issues/{item["issue"]}' in page
    assert f'id={item["node_id"]}' in page
assert "How these appeared to be missing" in page
assert "Process correction" in page
assert "Open updates" in page
assert "https://transduction.systems/updates/2026-09-20/" in (
    ROOT / "docs/sitemap.xml"
).read_text(encoding="utf-8")

for name, expected in [
    ("comparator-systemic-evolution.json", COMPARATOR_SHA256),
    ("systemic-evolution-reconciliation.json", RECONCILIATION_SHA256),
]:
    original = (ROOT / "data" / name).read_bytes()
    assert hashlib.sha256(original).hexdigest() == expected
    assert original == (ROOT / "docs/assets" / name).read_bytes()

print("Release 0.27 gate passed: 15 reports, 15 profiles, bounded claims, queue closure, and preserved reviewed assets")
