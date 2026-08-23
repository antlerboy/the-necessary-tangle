#!/usr/bin/env python3
"""Finish source-bounded public wording and metrics for release 0.18."""
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

ADDITIONAL_OBSERVATIONS = [
    {
        "kind": "graph measurement plus editorial interpretation",
        "title": "An entry can be present and still be structurally peripheral",
        "measurement": "Release 0.18 distinguishes public presence, developed profiles, typed connections and graph isolation rather than collapsing them into one coverage claim.",
        "interpretation": "A searchable name is an index achievement. It is not evidence that the atlas yet explains that person's work, lineage or disagreements.",
        "implication": "Research-queue and represented states remain visible, and prominence should follow sourced relational depth rather than the fact that a name was requested.",
        "test": "Review the named-coverage table and confirm that thin entries do not appear as developed profiles or acquire unsupported influence claims.",
    },
    {
        "kind": "source-boundary observation",
        "title": "Source duplication is a warning about claim compression",
        "measurement": "Linda Booth Sweeney's author profile and book information are recorded as distinct source roles rather than duplicate records pointing at the same URL.",
        "interpretation": "One page may support several claims, but duplicating it as if it were several independent sources overstates evidence and obscures what each citation is doing.",
        "implication": "Source records identify a distinct public route and state the bounded use made of it; repeated claims may cite the same source identifier.",
        "test": "The public source register should contain no new duplicate URLs and each Linda Booth Sweeney relation should show the relevant source role.",
    },
    {
        "kind": "programme-boundary observation",
        "title": "Unfinished corpus work is part of the public model",
        "measurement": "The Monoskop archive, Foundational Papers in Complexity Science, SysCoI/model.report, the reading list and company-knowledge discovery remain separately named programmes rather than being labelled complete.",
        "interpretation": "A bounded pass can be complete while the wider field remains radically unfinished. Conflating those two scales turns project management into an epistemic claim.",
        "implication": "Each future pass needs a stated corpus, method, stop condition and visible residual queue.",
        "test": "A release note should say exactly what was checked and leave the remaining programme visible rather than silently absorbing it into a generic backlog.",
    },
]


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

    source = next((item for item in data.get("sources", []) if item.get("id") == "src_linda_do_bees_pee_2026"), None)
    if not source:
        raise SystemExit("Missing expected source: src_linda_do_bees_pee_2026")
    source["url"] = "https://www.lindaboothsweeney.com/"
    source["notes"] = (
        "Author-maintained site presenting Do Bees Pee? as a new children's book and describing its treatment of "
        "closed-loop ecological processes and circular-economy thinking. The separate author-profile source records "
        "the HarperCollins and June 2026 listing."
    )

    redirects = data.get("canonical_redirects", {})
    canonical = lambda node_id: redirects.get(node_id, node_id)
    public_ids = {
        node.get("id") for node in data.get("nodes", [])
        if node.get("public_visibility") == "public" and canonical(node.get("id")) == node.get("id")
    }
    canonical_edges = []
    for edge in data.get("edges", []):
        source_id = canonical(edge.get("source"))
        target_id = canonical(edge.get("target"))
        if source_id in public_ids and target_id in public_ids and source_id != target_id:
            canonical_edges.append({**edge, "source": source_id, "target": target_id})
    substantive_edges = [
        edge for edge in canonical_edges
        if edge.get("relation_family") not in {"classification", "evidence", "documentary", "legacy"}
        and edge.get("relation_type") != "legacy_association_unspecified"
        and edge.get("claim_status") != "legacy_unresolved"
    ]

    report = data.setdefault("ai_observations", {})
    metrics = report.setdefault("metrics", {})
    metrics["typed_edges"] = len(canonical_edges)
    metrics["substantive_edges"] = len(substantive_edges)
    observations = report.setdefault("observations", [])
    existing_titles = {item.get("title") for item in observations}
    observations.extend(item for item in ADDITIONAL_OBSERVATIONS if item["title"] not in existing_titles)

    rendered = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    DATA_PATH.write_text(rendered, encoding="utf-8")
    DOCS_JSON.write_text(rendered, encoding="utf-8")
    DOCS_JS.write_text("window.TANGLE_DATA = " + json.dumps(data, ensure_ascii=False) + ";\n", encoding="utf-8")
    print(
        f"Finalised {len(DESCRIPTIONS)} unFIX descriptions, source roles and "
        f"{len(observations)} AI observations; removed the generic Systems alias."
    )


if __name__ == "__main__":
    main()
