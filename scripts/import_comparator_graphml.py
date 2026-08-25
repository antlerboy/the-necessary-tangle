#!/usr/bin/env python3
"""Extract the Map of Systemic Evolution into a comparator dataset.

Packet A of documentation/comparator-systemic-evolution-plan.md.

This is a deterministic extraction.  The URANOS source page states one generic
meaning for every directed line: it illustrates a major influence between
topics.  The extraction preserves that source claim without treating it as an
independently verified or more specifically typed Necessary Tangle relation.

The source file remains third-party material, used with Benjamin Hadorn's
permission and full attribution. Pass its path explicitly:

    python3 scripts/import_comparator_graphml.py /path/to/systemic_evolution.graphml

Output: data/comparator-systemic-evolution.json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT_PATH = ROOT / "data" / "comparator-systemic-evolution.json"

NS = {
    "g": "http://graphml.graphdrawing.org/xmlns",
    "y": "http://www.yworks.com/xml/graphml",
}

EXPECTED_NODES = 650
EXPECTED_EDGES = 1320

# Official scientific-realm legend published with the map.  Realm colour is a
# classification, not a more specific meaning for an individual influence.
STREAM_LABELS = {
    "#999999": "philosophy",
    "#FFCC00": "social systems",
    "#008000": "biology and medicine",
    "#0000FF": "mathematics",
    "#000000": "physical sciences",
    "#FFFF00": "symbolic systems",
    "#800000": "computers and informatics",
    "#FF0000": "cybernetics",
    "#00CCFF": "systems analysis",
    "#00FF00": "ecology",
    "#FF00FF": "engineering",
    "#666699": "not identified in the published legend",
}


def text_of(element: ET.Element | None) -> str:
    if element is None:
        return ""
    return "".join(element.itertext())


def normalise_label(raw: str) -> str:
    """Collapse yEd's line wrapping without losing the original text."""
    lines = [line.strip() for line in raw.split("\n") if line.strip()]
    return re.sub(r"\s+", " ", " ".join(lines)).strip()


def parse_year(label: str) -> str:
    """Return a bracketed or trailing year exactly as the source writes it."""
    bracketed = re.search(r"\[([^\]]*)\]", label)
    if bracketed:
        return bracketed.group(1).strip()
    trailing = re.search(r"c?\.?\s*\d{3,4}\s*[-–]\s*\d{3,4}\s*(?:BC)?\s*$", label)
    return trailing.group(0).strip() if trailing else ""


def extract_nodes(root: ET.Element) -> list[dict[str, Any]]:
    records = []
    for node in root.findall(".//g:node", NS):
        shape = node.find(".//y:ShapeNode", NS)
        label_el = node.find(".//y:NodeLabel", NS)
        geometry = shape.find("y:Geometry", NS) if shape is not None else None
        border = shape.find("y:BorderStyle", NS) if shape is not None else None
        fill = shape.find("y:Fill", NS) if shape is not None else None
        shape_type = shape.find("y:Shape", NS) if shape is not None else None

        raw_label = text_of(label_el)
        border_colour = border.get("color") if border is not None else None
        records.append(
            {
                "source_node_id": node.get("id"),
                "raw_label": raw_label,
                "label": normalise_label(raw_label),
                "year_as_written": parse_year(normalise_label(raw_label)),
                "border_colour": border_colour,
                "border_width": border.get("width") if border is not None else None,
                "border_type": border.get("type") if border is not None else None,
                "fill_colour": fill.get("color") if fill is not None else None,
                "shape": shape_type.get("type") if shape_type is not None else None,
                "font_size": label_el.get("fontSize") if label_el is not None else None,
                "x": float(geometry.get("x")) if geometry is not None else None,
                "y": float(geometry.get("y")) if geometry is not None else None,
                "width": float(geometry.get("width")) if geometry is not None else None,
                "height": float(geometry.get("height")) if geometry is not None else None,
                "official_realm": STREAM_LABELS.get(border_colour, "unclassified"),
                "source_url": text_of(node.find("g:data[@key='d4']", NS)).strip(),
                "source_description": text_of(node.find("g:data[@key='d5']", NS)).strip(),
            }
        )
    return records


def extract_edges(root: ET.Element) -> list[dict[str, Any]]:
    records = []
    for index, edge in enumerate(root.findall(".//g:edge", NS)):
        line = edge.find(".//y:LineStyle", NS)
        arrows = edge.find(".//y:Arrows", NS)
        label_el = edge.find(".//y:EdgeLabel", NS)
        source_arrow = arrows.get("source") if arrows is not None else None
        target_arrow = arrows.get("target") if arrows is not None else None
        if source_arrow == "standard" and target_arrow == "standard":
            direction_status = "bidirectional"
            phrase = "the source map depicts major influence in both directions"
        elif source_arrow == "standard":
            direction_status = "target_to_source"
            phrase = "the source map depicts a major influence from the target topic to the source topic"
        else:
            direction_status = "source_to_target"
            phrase = "the source map depicts a major influence from the source topic to the target topic"
        records.append(
            {
                "comparator_edge_id": edge.get("id") or f"e{index}",
                "source_node_id": edge.get("source"),
                "target_node_id": edge.get("target"),
                "line_colour": line.get("color") if line is not None else None,
                "line_width": line.get("width") if line is not None else None,
                "line_style": line.get("type") if line is not None else None,
                "source_arrow": source_arrow,
                "target_arrow": target_arrow,
                "direction_status": direction_status,
                "edge_label_in_source": text_of(label_el).strip(),
                "official_realm": STREAM_LABELS.get(
                    line.get("color") if line is not None else None,
                    "unclassified",
                ),
                "relation_type": "reported_major_influence",
                "plain_phrase": phrase,
                "meaning": "major_influence_between_topics",
                "accuracy_status": "source_reported_not_independently_verified",
                "specific_relation_status": "not_stated_by_source",
            }
        )
    return records


def build(graphml_path: Path) -> dict[str, Any]:
    root = ET.parse(graphml_path).getroot()
    nodes = extract_nodes(root)
    edges = extract_edges(root)

    labelled_edges = [e for e in edges if e["edge_label_in_source"]]
    colour_census: dict[str, int] = {}
    for node in nodes:
        colour_census[node["border_colour"]] = colour_census.get(node["border_colour"], 0) + 1

    return {
        "meta": {
            "dataset": "comparator-systemic-evolution",
            "title": "Map of Systemic Evolution",
            "role": "comparator corpus, not atlas content",
            "provenance": [
                "Originated 1996 by Dr Eric Schwarz, Neuchatel, Switzerland.",
                "Extended 1998, including items from 'The Story of Philosophy' by Will Durant.",
                "Elaborated 2000-2001 for the International Institute for General Systems Studies.",
                "Extended 2016 by Benjamin Hadorn, Fribourg, Switzerland.",
            ],
            "published_at": "https://uranos.ch/index.php/research-menu/cybernetcis",
            "rights": (
                "Used with Benjamin Hadorn's permission confirmed 2026-08-25, with "
                "the full Schwarz-Durant-IIGSS-Hadorn provenance retained. The source "
                "site's own copyright notice and terms continue to apply."
            ),
            "semantics": (
                "The URANOS page states that directed edges illustrate major influences "
                "between topics. Every edge retains that generic source meaning and is "
                "marked source-reported, not independently verified. No more specific "
                "influence type or edge-level evidence is supplied."
            ),
            "colour_legend": (
                "Realm names follow the legend published on the URANOS source page. "
                "Colour classifies a scientific realm; it does not make an individual "
                "edge more specifically typed or verified."
            ),
            "node_count": len(nodes),
            "edge_count": len(edges),
            "labelled_edge_count": len(labelled_edges),
            "node_colour_census": dict(sorted(colour_census.items(), key=lambda kv: -kv[1])),
        },
        "nodes": nodes,
        "edges": edges,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("graphml", help="path to systemic_evolution.graphml")
    parser.add_argument("--out", default=str(OUT_PATH))
    args = parser.parse_args()

    path = Path(args.graphml).expanduser()
    if not path.is_file():
        print(f"Not found: {path}", file=sys.stderr)
        return 2

    data = build(path)
    errors = []
    if data["meta"]["node_count"] != EXPECTED_NODES:
        errors.append(f"expected {EXPECTED_NODES} nodes, got {data['meta']['node_count']}")
    if data["meta"]["edge_count"] != EXPECTED_EDGES:
        errors.append(f"expected {EXPECTED_EDGES} edges, got {data['meta']['edge_count']}")
    if data["meta"]["labelled_edge_count"]:
        errors.append(
            f"{data['meta']['labelled_edge_count']} edges carry a label; the extractor "
            "assumed none do and the semantics note must be revisited"
        )
    if any(e["relation_type"] != "reported_major_influence" for e in data["edges"]):
        errors.append("an edge does not preserve the source's generic major-influence meaning")
    if errors:
        for message in errors:
            print(f"FAILED: {message}", file=sys.stderr)
        return 1

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(data, indent=1, ensure_ascii=False, sort_keys=False) + "\n",
        encoding="utf-8",
    )
    print(
        f"Wrote {out.relative_to(ROOT) if out.is_relative_to(ROOT) else out}: "
        f"{data['meta']['node_count']} nodes, {data['meta']['edge_count']} edges, "
        f"all preserved as source-reported major influences."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
