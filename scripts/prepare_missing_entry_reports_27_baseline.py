#!/usr/bin/env python3
"""Stage release 0.27 out before historical release validators run."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data/public-data.json"
MARK = "missing_entry_reports_20260920"

data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
removed_sources = {
    source["id"] for source in data["sources"] if source.get("connection_pass") == MARK
}
data["sources"] = [
    source for source in data["sources"] if source["id"] not in removed_sources
]
data["edges"] = [
    edge for edge in data["edges"] if edge.get("connection_pass") != MARK
]
data["profiles"] = [
    profile
    for profile in data["profiles"]
    if profile.get("profile_status") != "source_scoped_report_review_complete"
]
for node in data["nodes"]:
    source_ids = node.get("source_ids", "[]")
    if isinstance(source_ids, str):
        node["source_ids"] = json.dumps(
            [sid for sid in json.loads(source_ids) if sid not in removed_sources],
            ensure_ascii=False,
        )
    if node["id"] == "person_gerald_midgley":
        node.update(
            label="Gerald Midgley",
            description="Systems researcher associated with systemic intervention, boundary critique, methodological pluralism and the study of marginalisation.",
            canonical_definition="",
            review_status="research_pass_needs_editor",
            publication_level="described",
            public_stub_text="",
            public_source_count=2,
            no_public_link_count=2,
        )
data.pop(MARK, None)
for row in data.get("september_connections", {}).get("queue", []):
    row.pop("report_outcome", None)
DATA_PATH.write_text(
    json.dumps(data, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
    newline="\n",
)
for filename in ["docs/updates/index.html", "docs/reading-list.html"]:
    path = ROOT / filename
    if not path.exists():
        continue
    text = path.read_text(encoding="utf-8")
    text = re.sub(
        r"<!-- missing-entry-reports-27 -->.*?<!-- /missing-entry-reports-27 -->",
        "",
        text,
        flags=re.S,
    )
    path.write_text(text, encoding="utf-8", newline="\n")
generated = ROOT / "docs/updates/2026-09-20/index.html"
if generated.exists():
    generated.unlink()
print("Staged the release 0.27 missing-entry report pass out of historical validation")
