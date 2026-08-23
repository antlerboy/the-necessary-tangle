#!/usr/bin/env python3
"""Finish source-bounded public wording for release 0.18 entries."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "public-data.json"
DOCS_JSON = ROOT / "docs" / "assets" / "public-data.json"
DOCS_JS = ROOT / "docs" / "assets" / "public-data.js"

DESCRIPTIONS = {
    "concept_unfix_system_archetypes": (
        "In Jurgen Appelo's unFIX synthesis, system archetypes are recurring structures of feedback and delay "
        "used to recognise familiar patterns of system behaviour. This entry records inclusion in that synthesis; "
        "its wider lineage and competing formulations remain to be researched."
    ),
    "concept_unfix_causal_loop_diagrams": (
        "In Jurgen Appelo's unFIX synthesis, causal loop diagrams are visual models of reinforcing and balancing "
        "feedback among variables. This entry records inclusion in that synthesis and does not claim an exhaustive "
        "account of the method or its history."
    ),
    "concept_unfix_mental_models": (
        "In Jurgen Appelo's unFIX synthesis, mental models are the assumptions and internal representations through "
        "which people interpret situations and choose actions. This entry records inclusion in that synthesis pending "
        "a fuller sourced treatment."
    ),
    "concept_unfix_hierarchy": (
        "In Jurgen Appelo's unFIX synthesis, hierarchy names nested levels of authority, responsibility or system "
        "organisation. This source-bounded entry records the concept's inclusion without treating hierarchy as either "
        "inherently good or inherently bad."
    ),
    "concept_unfix_dynamic_complexity": (
        "In Jurgen Appelo's unFIX synthesis, dynamic complexity arises when causes and effects are separated in time "
        "or space and feedback makes consequences difficult to infer. This entry records inclusion in that synthesis "
        "rather than a complete theoretical treatment."
    ),
    "concept_unfix_network_theory": (
        "In Jurgen Appelo's unFIX synthesis, network theory examines actors or elements through their patterns of "
        "connection, position and flow. This entry records inclusion in that synthesis; its detailed theoretical "
        "lineages and applications remain open work."
    ),
    "concept_unfix_scaling_laws": (
        "In Jurgen Appelo's unFIX synthesis, scaling laws describe how system properties change, often non-linearly, "
        "with size. This entry records inclusion in that synthesis and is not a complete account of biological, urban "
        "or organisational scaling."
    ),
}


def parse(value: Any, fallback: Any | None = None) -> Any:
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


def encoded(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False)


def main() -> None:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    by_id = {node.get("id"): node for node in data.get("nodes", [])}

    missing = sorted(set(DESCRIPTIONS) - set(by_id))
    if missing:
        raise SystemExit("Missing expected 0.18 entries: " + ", ".join(missing))

    for node_id, description in DESCRIPTIONS.items():
        node = by_id[node_id]
        node["description"] = description
        node["canonical_definition"] = description
        node["public_stub_text"] = description

    system_entry = by_id.get("concept_unfix_system")
    if not system_entry:
        raise SystemExit("Missing expected 0.18 entry: concept_unfix_system")
    aliases = [alias for alias in parse(system_entry.get("aliases"), []) if str(alias).casefold() != "systems"]
    system_entry["aliases"] = encoded(aliases)

    rendered = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    DATA_PATH.write_text(rendered, encoding="utf-8")
    DOCS_JSON.write_text(rendered, encoding="utf-8")
    DOCS_JS.write_text("window.TANGLE_DATA = " + json.dumps(data, ensure_ascii=False) + ";\n", encoding="utf-8")
    print(f"Finalised {len(DESCRIPTIONS)} unFIX entry descriptions and removed the generic Systems alias.")


if __name__ == "__main__":
    main()
