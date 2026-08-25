#!/usr/bin/env python3
"""Create a rights-safe public projection of Nigel Williams's counted map.

The private Scopus corpus and raw cited-reference strings are never copied.
The public projection retains aggregate concept counts, bibliographic DOI
handles, and every aggregate link with its thresholds and concentration flag.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "counted-map-public.json"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--concepts", required=True)
    parser.add_argument("--edges", required=True)
    parser.add_argument("--out", default=str(OUT))
    args = parser.parse_args()

    concepts_source = json.loads(Path(args.concepts).read_text(encoding="utf-8"))
    edges_source = json.loads(Path(args.edges).read_text(encoding="utf-8"))
    concepts = []
    for node in concepts_source["concepts"]:
        concepts.append(
            {
                "id": node["id"],
                "label": node["label"],
                "seeded_from": node.get("seeded_from", ""),
                "work_count": node["work_count"],
                "first_year": node.get("first_year"),
                "last_year": node.get("last_year"),
                "status": node["status"],
                "exemplar_works": [
                    {
                        "doi": work.get("doi", ""),
                        "title": work.get("title", ""),
                        "year": work.get("year", ""),
                        "cited_by": work.get("cited_by", 0),
                    }
                    for work in node.get("exemplar_works", [])
                ],
            }
        )

    edges = []
    for index, edge in enumerate(edges_source["edges"], start=1):
        edges.append(
            {
                "id": f"counted_link_{index:04d}",
                "source": edge["source"],
                "target": edge["target"],
                "relation_type": "keyword_labelled_citation_signal",
                "plain_phrase": (
                    "records whose titles match the source term contain cited-reference "
                    "strings matching the target term"
                ),
                "directed": True,
                "weight": edge["weight"],
                "citing_work_count": edge["citing_work_count"],
                "top_citing_share": edge["top_citing_share"],
                "concentrated": edge["concentrated"],
                "first_year": edge.get("first_year"),
                "last_year": edge.get("last_year"),
                "accuracy_status": "aggregate_signal_not_independently_reproduced",
                "scope_conditions": (
                    "Keyword matching in one licensed corpus. This does not establish "
                    "conceptual influence, agreement, derivation, importance, or a clean "
                    "citation between two unambiguous literatures."
                ),
            }
        )

    source_meta = concepts_source["meta"]
    output = {
        "meta": {
            "dataset": "counted-map-public",
            "title": "The Counted Map — aggregate public projection",
            "contributor": "Nigel Williams",
            "contributor_url": "https://github.com/NigelWilliamUOP",
            "source_repository": "https://github.com/NigelWilliamUOP/systems-map",
            "method": (
                "Concepts were matched in Scopus record titles; target terms were matched "
                "in their cited-reference strings. Links survive only above the stated "
                "weight and distinct-citing-record thresholds."
            ),
            "interpretation": (
                "A link is a keyword-labelled citation signal in this corpus, not a claim "
                "that one idea influenced, entailed, agreed with, or derived from another."
            ),
            "rights_projection": (
                "Aggregate counts, years and DOI handles only. The private corpus, Scopus "
                "fields, EIDs and raw cited-reference strings are excluded."
            ),
            "reproduction_status": (
                "The build code is included, but the source corpus and shrink step are not "
                "public; the published aggregate has therefore not been independently rerun."
            ),
            "thresholds": source_meta["thresholds"],
            "concept_count": len(concepts),
            "evidenced_concept_count": sum(c["status"] == "evidenced" for c in concepts),
            "edge_count": len(edges),
            "concept_matched_work_count": source_meta["concept_matched_work_count"],
            "source_document_count": 85832,
            "source_reference_row_count": 13792287,
            "raw_reference_string_count_published": 0,
        },
        "concepts": concepts,
        "edges": edges,
    }

    if len(concepts) != 98 or len(edges) != 1856:
        raise SystemExit(
            f"Unexpected source shape: {len(concepts)} concepts and {len(edges)} links"
        )
    if any("evidence" in edge or "reference" in edge for edge in edges):
        raise SystemExit("Licensed evidence fields leaked into the public projection")

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {len(concepts)} concepts and all {len(edges)} aggregate links.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
