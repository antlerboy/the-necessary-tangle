#!/usr/bin/env python3
"""Validate our map's data. Run after build_map.py."""
from __future__ import annotations
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "map" / "data"
FORBIDDEN = {"abstract", "author_keywords", "index_keywords", "affiliations",
             "authors_with_affiliations", "funding_details", "funding_texts",
             "reference", "citing_eid"}


def main() -> int:
    errors: list[str] = []
    concepts = json.loads((DATA / "concepts.json").read_text(encoding="utf-8"))
    edges = json.loads((DATA / "edges.json").read_text(encoding="utf-8"))
    cmap = {c["id"]: c for c in concepts["concepts"]}
    th = concepts["meta"]["thresholds"]

    for c in concepts["concepts"]:
        if not c["label"] or not c["id"].startswith("concept_"):
            errors.append(f"malformed concept {c['id']}")
        if c["status"] == "evidenced" and c["work_count"] < th["min_works"]:
            errors.append(f"{c['id']} marked evidenced below the work threshold")
        if c["status"] == "candidate" and c["work_count"] >= th["min_works"]:
            errors.append(f"{c['id']} meets the threshold but is marked candidate")

    for e in edges["edges"]:
        pair = f"{e['source']}->{e['target']}"
        if e["source"] not in cmap or e["target"] not in cmap:
            errors.append(f"{pair} has an endpoint that is not a concept")
        if e["source"] == e["target"]:
            errors.append(f"{pair} is a self-loop")
        if e["relation_type"] != "keyword_labelled_citation_signal":
            errors.append(f"{pair} uses an undeclared relation type {e['relation_type']}")
        if e["weight"] < th["min_edge_weight"] or e["citing_work_count"] < th["min_citing_works"]:
            errors.append(f"{pair} is below the edge thresholds")
        if not e.get("scope_conditions"):
            errors.append(f"{pair} has no scope conditions")
        for example in e.get("evidence", []):
            if set(example) - {"citing_doi", "citing_year"}:
                errors.append(f"{pair} carries a non-public evidence field")
        if e["concentrated"] != (e["top_citing_share"] >= 0.5):
            errors.append(f"{pair} has an inconsistent concentration flag")

    blob = json.dumps(concepts) + json.dumps(edges)
    for key in FORBIDDEN:
        if f'"{key}"' in blob:
            errors.append(f"licensed Scopus field '{key}' has leaked into map data")

    if errors:
        for e in errors[:40]:
            print(f"FAILED: {e}", file=sys.stderr)
        print(f"\n{len(errors)} problem(s)", file=sys.stderr)
        return 1

    ev = sum(1 for c in concepts["concepts"] if c["status"] == "evidenced")
    conc = sum(1 for e in edges["edges"] if e["concentrated"])
    print(f"map validation passed: {len(cmap)} concepts ({ev} evidenced), "
          f"{len(edges['edges'])} edges ({conc} flagged concentrated), "
          f"no licensed fields present.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
