#!/usr/bin/env python3
"""Retain enduring inherited lenses and the release-0.18 interface observations."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "public-data.json"
DOCS_JSON = ROOT / "docs" / "assets" / "public-data.json"
DOCS_JS = ROOT / "docs" / "assets" / "public-data.js"

RETAINED = [
    {
        "id": "canonical_sources_have_jobs",
        "title": "Canonical sources have jobs",
        "kind": "source-role observation",
        "measurement": "The canonical source register distinguishes author archives, official organisations, primary works, publisher records and independent counterweights.",
        "interpretation": "Calling a source canonical does not make it universally authoritative; it identifies the job for which it is the preferred route.",
        "implication": "Each source record should state what it can establish and what it cannot.",
        "test": "Sample canonical sources and verify that their registered use matches the claims that cite them.",
    },
    {
        "id": "first_party_needs_counterweight",
        "title": "First-party sources need counterweight",
        "kind": "source-balance observation",
        "measurement": "Many profiles begin with author, institutional or publisher sources because these best establish names, dates, declared concepts and official lineages.",
        "interpretation": "First-party evidence is indispensable for self-description but weak for criticism, contested influence and assessment of consequences.",
        "implication": "Developed entries should add independent scholarship or practitioner evidence where interpretation matters.",
        "test": "Review high-connectivity profiles and identify claims resting only on the subject's own account.",
    },
    {
        "id": "reading_list_depth",
        "title": "A reading-list item is not yet a reading",
        "kind": "coverage observation",
        "measurement": "The reading-list inventory distinguishes developed profiles, represented items and inventory-only records.",
        "interpretation": "Bibliographic presence records attention and intent; it does not imply that a work has been critically read into the atlas.",
        "implication": "Item-level status must remain visible and the wider reading-list programme must stay explicitly partial.",
        "test": "Check that inventory-only works do not inherit summaries or relations from title similarity alone.",
    },
    {
        "id": "ing_lineage_infrastructure",
        "title": "Lineage needs infrastructure",
        "kind": "historical observation",
        "measurement": "The David Ing and systems-in-plural routes connect people, publications, traditions and institutional settings rather than treating a lineage as a list of names.",
        "interpretation": "Intellectual transmission happens through teaching, collaboration, organisations, conferences and practice as well as citation.",
        "implication": "Lineage work should model carriers and settings alongside conceptual influence.",
        "test": "Inspect a lineage journey and confirm that it includes at least one institutional or practice-bearing connection.",
    },
    {
        "id": "core_practice_not_four_tools",
        "title": "Core systems practice is not four tools",
        "kind": "practice-boundary observation",
        "measurement": "The core practice spine holds several approaches together without collapsing them into a single method sequence.",
        "interpretation": "A compact orientation can aid action while still preserving different purposes, assumptions and forms of evidence.",
        "implication": "Guided routes should expose choice and boundary conditions rather than imply one universal workflow.",
        "test": "Check whether a reader can see why two adjacent approaches would lead to different interventions in the same situation.",
    },
    {
        "id": "attention_is_not_importance",
        "title": "Attention is not importance",
        "kind": "second-order observation",
        "measurement": "Reading lists, submitted tickets and available corpora shape which people and ideas receive depth first.",
        "interpretation": "Editorial attention creates visibility and connectivity; neither is a neutral ranking of intellectual worth.",
        "implication": "Coverage decisions and unreviewed queues should remain visible beside graph measures.",
        "test": "Compare highly connected entries with the release history and ask whether prominence follows evidence, prior attention or both.",
    },
    {
        "id": "navigation_changes_importance",
        "title": "Navigation changes what appears important",
        "kind": "interface measurement plus epistemic interpretation",
        "measurement": "The release gives every entry a full reading surface and a constellation view with one selected centre, direct relations and two-step relations.",
        "interpretation": "A centre selected for a question is not the centre of the field. Interface focus and graph degree can manufacture apparent importance.",
        "implication": "The map treats the selected entry as a temporary star and its orbits as question-relative positions.",
        "test": "Change the selected entry and layer; the constellation should reorganise without presenting the new centre as canonically primary.",
    },
    {
        "id": "links_are_commitments",
        "title": "Links are commitments about possible movement",
        "kind": "interaction-design observation",
        "measurement": "Navigational cards, search suggestions, surprise routes, map nodes, map connections and entry actions expose stable destinations.",
        "interpretation": "A control which looks like a link but cannot be copied, opened in a new tab or inspected conceals the structure of the atlas.",
        "implication": "Navigation uses links; buttons are reserved for actions whose result cannot sensibly exist as a URL.",
        "test": "Right-click or modified-click each navigational surface and confirm that its destination remains coherent in a separate tab.",
    },
]


def main() -> None:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    report = data.setdefault("ai_observations", {})
    observations = report.setdefault("observations", [])
    by_id = {item.get("id"): item for item in observations}
    for item in RETAINED:
        by_id[item["id"]] = item
    report["observations"] = list(by_id.values())
    rendered = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    DATA.write_text(rendered, encoding="utf-8")
    DOCS_JSON.write_text(rendered, encoding="utf-8")
    DOCS_JS.write_text("window.TANGLE_DATA = " + json.dumps(data, ensure_ascii=False) + ";\n", encoding="utf-8")
    print(f"Retained {len(RETAINED)} inherited and release-specific observation lenses; {len(report['observations'])} total.")


if __name__ == "__main__":
    main()
