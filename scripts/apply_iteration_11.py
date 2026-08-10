#!/usr/bin/env python3
"""Apply release 0.11: semantic map interaction and feedback ledger."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "public-data.json"
DOCS_ASSETS = ROOT / "docs" / "assets"
RELEASE = "0.11-semantic-map-alpha"
GENERATED = "2026-08-10"

FEEDBACK_LEDGER: list[dict[str, Any]] = [
    {
        "id": "feedback_public_identity",
        "label": "Public identity, curatorship and language",
        "status": "implemented",
        "summary": "Use the exact project name, systems | cybernetics | complexity framing, curator language, canonical antlerboy links, left-aligned text, fuller acknowledgements and an explicit CC BY-SA boundary.",
        "evidence": ["releases_0_6_to_0_10", "documentation_feedback_ledger"],
    },
    {
        "id": "feedback_clickable_affordances",
        "label": "Clickable affordances and ordinary links",
        "status": "implemented",
        "summary": "Cards and navigation which look clickable are links; internal routes can be opened in a new tab or copied.",
        "evidence": ["release_0_9"],
    },
    {
        "id": "feedback_secret_dot",
        "label": "Discreet route to the running feedback thread",
        "status": "restored_in_0_11",
        "summary": "A discreet fixed dot at the bottom right links to the public running-feedback issue.",
        "evidence": ["release_0_11"],
    },
    {
        "id": "feedback_membership_agents",
        "label": "Membership and agent-assisted contribution",
        "status": "implemented_as_proposal_and_review_model",
        "summary": "Readers, proposers, contributors, reviewers and stewards use issues and pull requests; automated work needs a named human sponsor and curator acceptance.",
        "evidence": ["release_0_7", "release_0_10", "issue_10"],
    },
    {
        "id": "feedback_map",
        "label": "Richer zoomable map",
        "status": "deepened_in_0_11",
        "summary": "The map now combines pointer-centred zoom with semantic label disclosure, a minimap, focus history, hover neighbourhoods, fullscreen mode and keyboard controls.",
        "evidence": ["release_0_8", "release_0_9", "release_0_11", "issue_11"],
    },
    {
        "id": "feedback_principia_sources_categories",
        "label": "Principia, canonical sources and emerging categories",
        "status": "first_pass_complete_more_work_open",
        "summary": "Principia Cybernetica has a typed first pass; canonical-source and source-mining registers are public; provisional graph neighbourhoods remain explicitly non-canonical.",
        "evidence": ["release_0_7", "release_0_9", "issue_12"],
    },
    {
        "id": "feedback_fpcs",
        "label": "Foundational Papers in Complexity Science",
        "status": "inventory_complete_depth_open",
        "summary": "All 89 papers, four volumes and 107 newly represented authors were inventoried in 0.8. Item-level interpretation, independent sources and deeper conceptual mapping remain open.",
        "evidence": ["release_0_8", "issue_3"],
    },
    {
        "id": "feedback_monoskop",
        "label": "Relevant Monoskop material",
        "status": "scoped_open_programme",
        "summary": "Monoskop is registered as a discovery corpus. The bounded, item-level review and replacement with primary or scholarly sources remains open.",
        "evidence": ["issue_4"],
    },
    {
        "id": "feedback_syscoi_model_report",
        "label": "SysCoI and model.report archives",
        "status": "registered_and_public_path_added_deeper_pass_open",
        "summary": "The archives are registered as circulation and discovery evidence; SysCoI is linked prominently. Chronology, participation and outbound-source ingestion remain open.",
        "evidence": ["release_0_9", "release_0_10", "issue_5"],
    },
    {
        "id": "feedback_prior_maps",
        "label": "Prior maps and bodies of knowledge",
        "status": "comparator_programme_open",
        "summary": "Comparator work is declared and sourced, including the Castellani map and Benjamin P Taylor's critique. The systematic comparison table remains open.",
        "evidence": ["issue_6"],
    },
    {
        "id": "feedback_human_lineage",
        "label": "Practitioner influence constellations",
        "status": "layer_and_journey_present_gold_standard_constellations_open",
        "summary": "Human-lineage relations and a guided journey are public. Several deeply sourced practitioner constellations and an espoused-versus-observed comparison remain open.",
        "evidence": ["release_0_9", "issue_7"],
    },
    {
        "id": "feedback_company_knowledge",
        "label": "Private company-knowledge discovery",
        "status": "private_discovery_rule_implemented_research_open",
        "summary": "Private material may generate leads but cannot enter the public release. Public-source replacement and a private lead log remain the operating rule.",
        "evidence": ["issue_8", "publication_controls"],
    },
    {
        "id": "feedback_mowles_murmurations",
        "label": "Chris Mowles and Murmurations",
        "status": "first_pass_complete",
        "summary": "Developed public entries and sources were added for Chris Mowles, complex responsive processes, Murmurations and a key publication.",
        "evidence": ["release_0_9"],
    },
    {
        "id": "feedback_sources_and_journeys",
        "label": "Source-mining register and richer guided routes",
        "status": "implemented_continuing",
        "summary": "A maintained source-mining register and five additional guided journeys were added across releases 0.9 and 0.10.",
        "evidence": ["release_0_9", "release_0_10"],
    },
    {
        "id": "feedback_layers",
        "label": "Expose conceptual, human, practice, contestation and provenance layers",
        "status": "implemented",
        "summary": "Layers are available from About and directly in the map, with ordinary language explaining what each line can and cannot mean.",
        "evidence": ["release_0_9"],
    },
    {
        "id": "feedback_publication_risk",
        "label": "Manage the risks of publication",
        "status": "controls_implemented_private_detail_retained_off_site",
        "summary": "Public-only payloads, provenance, scanning, curator review, licence boundaries, validation and backups are enforced. Detailed working risk notes remain private rather than becoming another public spectacle.",
        "evidence": ["release_0_10", "security_policy"],
    },
    {
        "id": "feedback_six_systems_terms",
        "label": "Distinguish systems theory, practice, leadership, change, convening and weaving",
        "status": "implemented",
        "summary": "Six developed entries, typed connections and a guided journey were added without imposing a false hierarchy.",
        "evidence": ["release_0_10"],
    },
    {
        "id": "feedback_public_pathways",
        "label": "Prominent pathways to community, capability, training and reading",
        "status": "implemented",
        "summary": "The home page links prominently to SysCoI, SCiO capability and accreditation, SCiO professional development and Benjamin P Taylor's reading list.",
        "evidence": ["release_0_10"],
    },
]

MAP_INTERACTION = {
    "version": "semantic-map-v1",
    "release": RELEASE,
    "principles": [
        "semantic zoom reveals detail progressively rather than merely making clutter larger",
        "focus should preserve enough context to keep the reader's bearings",
        "typed relationships remain inspectable at every scale",
        "the overview and the local neighbourhood are alternate observations of one graph",
        "reader-controlled disclosure is preferable to a single supposedly correct view",
    ],
    "features": [
        "pointer-centred wheel zoom",
        "progressive label density",
        "overview minimap with viewport rectangle",
        "focus breadcrumb and back trail",
        "double-click neighbourhood focus",
        "hover neighbourhood emphasis",
        "fullscreen map",
        "keyboard zoom and fit controls",
    ],
}


def canonical_public_nodes(data: dict[str, Any]) -> list[dict[str, Any]]:
    redirects = data.get("canonical_redirects", {})
    return [
        node
        for node in data.get("nodes", [])
        if node.get("public_visibility") == "public"
        and redirects.get(node.get("id"), node.get("id")) == node.get("id")
    ]


def write_payloads(data: dict[str, Any]) -> None:
    rendered = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    DATA_PATH.write_text(rendered, encoding="utf-8")
    DOCS_ASSETS.mkdir(parents=True, exist_ok=True)
    (DOCS_ASSETS / "public-data.json").write_text(rendered, encoding="utf-8")
    (DOCS_ASSETS / "public-data.js").write_text(
        "window.TANGLE_DATA = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n",
        encoding="utf-8",
    )


def main() -> None:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    public_nodes = canonical_public_nodes(data)
    public_ids = {node["id"] for node in public_nodes}
    profiles = data.get("profiles", {})
    journeys = data.get("journeys", [])

    meta = data.setdefault("meta", {})
    meta.update(
        {
            "release": RELEASE,
            "generated": GENERATED,
            "map_interaction_version": MAP_INTERACTION["version"],
            "feedback_ledger_count": len(FEEDBACK_LEDGER),
            "public_entry_count": len(public_nodes),
            "described_entry_count": len(public_nodes),
            "profile_count": len(set(profiles) & public_ids) if isinstance(profiles, dict) else meta.get("profile_count", 0),
            "journey_count": len(journeys),
            "source_count": len(data.get("sources", [])),
        }
    )

    data["feedback_ledger"] = FEEDBACK_LEDGER
    data["map_interaction"] = MAP_INTERACTION
    write_payloads(data)
    print(
        f"Applied {RELEASE}: {meta['public_entry_count']} entries, "
        f"{meta['profile_count']} profiles, {meta['journey_count']} journeys and "
        f"{len(FEEDBACK_LEDGER)} feedback commitments."
    )


if __name__ == "__main__":
    main()
