#!/usr/bin/env python3
"""Publish release 0.20: source-faithful prior-map comparison.

The comparator datasets remain separate from the canonical atlas graph.  This
overlay registers their provenance and public review status, publishes the
dedicated routes, and updates release metadata and documentation.  It does not
promote imported lines into canonical Tangle relations.
"""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path
from typing import Any

from apply_iteration_09 import graph_metrics, make_ai_observations

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "public-data.json"
DOCS_ASSETS = ROOT / "docs" / "assets"
RELEASE = "0.20-prior-maps-alpha"
GENERATED = "2026-08-25"
PUBLIC_URL = "https://transduction.systems/"

SYSTEMIC_SOURCE = "https://uranos.ch/index.php/research-menu/cybernetcis"
SYSTEMIC_PAGE = "https://transduction.systems/prior-maps/systemic-evolution/"
CASTELLANI_SOURCE = "https://art-sciencefactory.com/complexity-map_feb09.html"
CASTELLANI_PAGE = "https://transduction.systems/prior-maps/castellani/"
COUNTED_PAGE = "https://transduction.systems/prior-maps/counted-map/"
NIGEL_PAGE = "https://transduction.systems/contributors/nigel-williams/"


def encoded(items: list[str]) -> str:
    return json.dumps(items, ensure_ascii=False)


def upsert(items: list[dict[str, Any]], records: list[dict[str, Any]], key: str) -> None:
    positions = {item.get(key): index for index, item in enumerate(items)}
    for record in records:
        value = record.get(key)
        if value in positions:
            items[positions[value]] = record
        else:
            positions[value] = len(items)
            items.append(record)


def source_record(
    source_id: str,
    title: str,
    source_type: str,
    url: str,
    notes: str,
    creators: list[str],
    *,
    date: str = "2026-08-25",
    publisher: str = "",
    licence: str = "",
    archived_url: str = "",
) -> dict[str, Any]:
    return {
        "id": source_id,
        "title": title,
        "source_type": source_type,
        "quality_tier": "C",
        "access": "public",
        "url": url,
        "date": date,
        "notes": notes,
        "creators": encoded(creators),
        "doi": "",
        "isbn": "",
        "publisher": publisher,
        "licence": licence,
        "archived_url": archived_url,
        "content_hash": "",
        "review_status": "checked",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    }


def load_required(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise SystemExit(f"Required prior-map dataset is missing: {path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def update_sources_and_registers(data: dict[str, Any]) -> None:
    sources = data.setdefault("sources", [])
    upsert(
        sources,
        [
            source_record(
                "src_uranos_systemic_evolution",
                "Map of Systemic Evolution",
                "primary_comparator_map",
                SYSTEMIC_SOURCE,
                (
                    "Primary publication and provenance page. It says the directed edges illustrate major "
                    "influences between topics and publishes the scientific-realm colour legend. Benjamin "
                    "Hadorn confirmed permission for appropriate use on 25 August 2026; original terms remain."
                ),
                ["Eric Schwarz", "Benjamin Hadorn"],
                date="1996-2016",
                publisher="URANOS",
            ),
            source_record(
                "src_nigel_systems_map_fork_2026",
                "NigelWilliamUOP/systems-map",
                "permissioned_public_contribution_fork",
                "https://github.com/NigelWilliamUOP/systems-map",
                (
                    "Public fork containing the GraphML extraction, comparator analysis, Castellani gap pass, "
                    "counted-map experiment and build fixes incorporated in release 0.20. Nigel Williams "
                    "confirmed permission to incorporate all relevant changes with appropriate credit on "
                    "25 August 2026. Private corpus material and raw licensed reference strings are excluded."
                ),
                ["Nigel Williams"],
                publisher="GitHub",
            ),
        ],
        "id",
    )

    source_by_id = {source.get("id"): source for source in sources}
    stream = source_by_id.get("src_schwarz_streams")
    if stream:
        stream.update(
            {
                "notes": (
                    "Benjamin P Taylor's 2019 SysCoI registration of the map and its history. The map "
                    "originated with Eric Schwarz in 1996, was extended with Durant material in 1998, "
                    "elaborated for IIGSS in 2000-01, and extended by Benjamin Hadorn in 2016."
                ),
                "creators": encoded(["Benjamin P Taylor"]),
                "last_checked": GENERATED,
            }
        )

    castellani = source_by_id.get("src_castellani_map_complexity_sciences")
    if castellani:
        castellani.update(
            {
                "url": CASTELLANI_SOURCE,
                "archived_url": "https://commons.wikimedia.org/wiki/File:Map_of_the_Complexity_Sciences.svg",
                "date": "May 2026",
                "notes": (
                    "Brian Castellani's current public image map. All 307 clickable outward references are "
                    "retained as source-published and not independently checked; 28 visible alt/title "
                    "disagreements are exposed rather than silently corrected. Drawn lines remain visible but "
                    "untyped. The archived URL is an earlier 2012 SVG licensed CC BY-SA 3.0."
                ),
                "creators": encoded(["Brian Castellani"]),
                "publisher": "Sociology and Complexity Science Blog / Art & Science Factory",
                "licence": "Current web edition: source terms; archived 2012 SVG: CC BY-SA 3.0",
                "review_status": "comparator_links_published",
                "last_checked": GENERATED,
            }
        )

    nodes = {node.get("id"): node for node in data.get("nodes", [])}
    systemic_node = nodes.get("comparator_corpus_schwarz_some_streams_of_systemic_thought_map")
    if systemic_node:
        description = (
            "A permissioned comparator projection of the Map of Systemic Evolution. It retains all 650 "
            "source nodes and all 1,320 directed, source-reported major-influence links separately from the "
            "canonical atlas, with cumulative reconciliation and explicit non-verification status."
        )
        systemic_node.update(
            {
                "description": description,
                "canonical_definition": description,
                "source_ids": encoded(
                    ["src_schwarz_streams", "src_uranos_systemic_evolution", "src_nigel_systems_map_fork_2026"]
                ),
                "review_status": "permissioned_comparator_published",
                "reviewed_by": "Benjamin P Taylor",
                "reviewed_at": GENERATED,
                "public_stub_text": description,
                "public_source_count": 3,
            }
        )

    castellani_node = nodes.get("comparator_corpus_castellani_complexity_map_and_atlas")
    if castellani_node:
        ids = json.loads(castellani_node.get("source_ids") or "[]")
        castellani_node["source_ids"] = encoded(list(dict.fromkeys([*ids, "src_nigel_systems_map_fork_2026"])))
        castellani_node["review_status"] = "current_links_published_gap_pass_complete"
        castellani_node["reviewed_by"] = "Benjamin P Taylor"
        castellani_node["reviewed_at"] = GENERATED

    for entry in data.get("corpus_register", []):
        if entry.get("id") != "corpus_comparator_maps":
            continue
        entry.update(
            {
                "status": "three_comparators_published_programme_continuing",
                "source_ids": [
                    "src_schwarz_streams",
                    "src_uranos_systemic_evolution",
                    "src_castellani_map_complexity_sciences",
                    "src_nigel_systems_map_fork_2026",
                    "src_castellani_critique_2019",
                ],
                "completion_test": (
                    "Every available source link retained under a stated meaning and accuracy status; "
                    "cumulative reconciliation published; further maps handled in bounded passes."
                ),
            }
        )

    reviews = [
        {
            "id": "external_systemic_evolution_map",
            "corpus": "Map of Systemic Evolution",
            "pages_traversed": ["URANOS source and history", "650-node GraphML", "1,320-link comparator projection"],
            "reference_trails": ["SysCoI 2019 prior-map registration -> URANOS source", "Nigel systems-map fork -> deterministic GraphML extraction"],
            "relationship_ids": [],
            "disagreement": "Source lines report major influence, but no individual line supplies a citation or more specific relation type.",
            "uncertainty": "All source links remain not independently verified and none is promoted merely by import.",
            "decision": "Retain all 650 nodes and 1,320 links in a permissioned comparator layer; publish the complete reconciliation ledger.",
        },
        {
            "id": "external_castellani_map_2026",
            "corpus": "Map of the Complexity Sciences, May 2026",
            "pages_traversed": ["current public image map", "all 307 HTML image-map areas", "earlier 2012 Commons SVG"],
            "reference_trails": ["current image-map area -> source-published outward destination"],
            "relationship_ids": [f"e_castellani_{slug}_member" for slug in (
                "complexity_and_public_health", "complexity_and_healthcare", "computational_social_science",
                "digital_social_science", "qualitative_complexity", "applied_complexity", "complexity_and_geography",
                "complexity_management_and_planning", "psychology_and_systems_theory", "social_systems_theory",
                "evolutionary_game_theory", "graph_theory", "scaling_in_complex_systems", "computational_science",
                "computational_biology", "computational_complexity_theory", "big_data"
            )],
            "disagreement": "Twenty-eight alt/title label disagreements are visible in the source HTML and are not silently repaired here.",
            "uncertainty": "All outward destinations are retained but not individually checked; drawn lines have no published relation type.",
            "decision": "Publish all 307 clickable references and retain 17 gap domains as documentary research stubs.",
        },
        {
            "id": "external_nigel_counted_map",
            "corpus": "The Counted Map",
            "pages_traversed": ["Nigel systems-map fork", "98-concept vocabulary", "aggregate 1,856-link result", "build and limitation notes"],
            "reference_trails": ["source-title keyword match -> cited-reference keyword match -> thresholded aggregate signal"],
            "relationship_ids": [],
            "disagreement": "The fork's shorthand suggested direct idea-to-idea citation; the actual extraction supports only a keyword-labelled citation signal.",
            "uncertainty": "The licensed corpus and shrink step are unavailable, so the aggregate has not been independently rerun.",
            "decision": "Publish all aggregate links, thresholds, counts, years and DOI handles; exclude private corpus data, EIDs and raw reference strings.",
        },
    ]
    upsert(data.setdefault("external_corpus_review", []), reviews, "id")


def update_meta(data: dict[str, Any], systemic: dict[str, Any], reconciliation: dict[str, Any], castellani: dict[str, Any], counted: dict[str, Any]) -> None:
    summary = reconciliation["meta"]["summary"]
    meta = data.setdefault("meta", {})
    meta.update(
        {
            "release": RELEASE,
            "generated": GENERATED,
            "iteration_focus": "source-faithful prior-map comparison, cumulative reconciliation and contribution credit",
            "node_count": len(data.get("nodes", [])),
            "edge_count": len(data.get("edges", [])),
            "source_count": len(data.get("sources", [])),
            "external_corpus_review_count": len(data.get("external_corpus_review", [])),
            "comparator_count": 3,
            "prior_maps_url": "https://transduction.systems/prior-maps/",
            "external_map_link_policy_url": "https://github.com/antlerboy/the-necessary-tangle/blob/main/documentation/external-map-link-policy.md",
            "systemic_evolution_source_url": SYSTEMIC_SOURCE,
            "systemic_evolution_page_url": SYSTEMIC_PAGE,
            "systemic_evolution_node_count": systemic["meta"]["node_count"],
            "systemic_evolution_link_count": systemic["meta"]["edge_count"],
            "systemic_evolution_reconciled_node_count": summary["source_nodes_confirmed"] + summary["source_nodes_partially_reconciled"],
            "systemic_evolution_distinct_atlas_entry_count": summary["distinct_atlas_entries_linked"],
            "systemic_evolution_canonical_relations_created": 0,
            "castellani_map_url": CASTELLANI_SOURCE,
            "castellani_map_page_url": CASTELLANI_PAGE,
            "castellani_map_current_source_link_count": castellani["meta"]["link_count"],
            "castellani_map_unique_destination_count": castellani["meta"]["unique_destination_count"],
            "castellani_map_label_disagreement_count": castellani["meta"]["label_disagreement_count"],
            "castellani_map_domains_incorporated": 17,
            "counted_map_page_url": COUNTED_PAGE,
            "counted_map_concept_count": counted["meta"]["concept_count"],
            "counted_map_evidenced_concept_count": counted["meta"]["evidenced_concept_count"],
            "counted_map_link_count": counted["meta"]["edge_count"],
            "counted_map_raw_reference_string_count_published": 0,
            "nigel_williams_contribution_url": NIGEL_PAGE,
        }
    )


def stamp_maintained_projections(data: dict[str, Any]) -> None:
    for key in ("reading_list_inventory", "reading_list_coverage", "core_systems_practice"):
        projection = data.get(key)
        if not isinstance(projection, dict):
            raise SystemExit(f"Maintained projection is missing: {key}")
        projection["release"] = RELEASE
        if "generated" in projection:
            projection["generated"] = GENERATED

    report = data.get("ai_observations")
    if not isinstance(report, dict):
        raise SystemExit("Maintained AI observations are missing")
    metrics = graph_metrics(data)
    fresh = make_ai_observations(metrics)
    fresh_by_id = {
        item.get("id"): item for item in fresh.get("observations", []) if item.get("id")
    }
    existing = report.get("observations", [])
    merged = [fresh_by_id.pop(item.get("id"), item) for item in existing]
    merged.extend(fresh_by_id.values())
    report.update({"release": RELEASE, "generated": GENERATED, "metrics": metrics, "observations": merged})

    lines = [
        "# AI observations",
        "",
        f"Generated for release `{RELEASE}` on {GENERATED}.",
        "",
        "Release 0.20 preserves the maintained observation lenses and the `0.18-navigable-tangle-alpha` navigability baseline while regenerating graph measurements after the bounded prior-map intake.",
        "",
        str(report.get("method_note") or "These observations concern the atlas and its source and interface choices, not the field itself."),
        "",
    ]
    for observation in merged:
        lines.extend(
            [
                f"## {observation.get('title', observation.get('id', 'Observation'))}",
                "",
                f"**Kind:** {observation.get('kind', '')}",
                "",
                f"**Measurement:** {observation.get('measurement', '')}",
                "",
                f"**Interpretation:** {observation.get('interpretation', '')}",
                "",
                f"**Implication:** {observation.get('implication', '')}",
                "",
                f"**Test:** {observation.get('test', '')}",
                "",
            ]
        )
    (ROOT / "documentation" / "ai-observations.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def publish_data(data: dict[str, Any]) -> None:
    rendered = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    DATA_PATH.write_text(rendered, encoding="utf-8")
    DOCS_ASSETS.mkdir(parents=True, exist_ok=True)
    (DOCS_ASSETS / "public-data.json").write_text(rendered, encoding="utf-8")
    (DOCS_ASSETS / "public-data.js").write_text(
        "window.TANGLE_DATA = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n",
        encoding="utf-8",
    )
    for name in (
        "comparator-systemic-evolution.json",
        "systemic-evolution-reconciliation.json",
        "comparator-castellani-links.json",
        "counted-map-public.json",
    ):
        shutil.copyfile(ROOT / "data" / name, DOCS_ASSETS / name)


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if new in text:
        return text
    if old not in text:
        raise SystemExit(f"Release-document marker changed unexpectedly: {label}")
    return text.replace(old, new, 1)


def update_documents(data: dict[str, Any]) -> None:
    meta = data["meta"]
    next_work = f"""# Next work

Status: release 0.20 is complete. No further production change is authorised without a bounded ticket.

## Outcome delivered

The first prior-map publication pass is live: every available link in the three
implemented comparator views is preserved under an explicit source meaning and
accuracy status, and no imported line is silently promoted into the canonical
atlas.

## Outcome

Continue the prior-map programme through bounded, source-specific passes while
keeping imported source claims separate from canonical Tangle relations.

## In scope

- manual reconciliation of a finite, prioritised source-node cohort;
- independent evidence review for selected source-reported links;
- link-health and label audits against current source pages;
- reproducible public-corpus alternatives for aggregate experiments;
- mobile, performance and accessibility tests for the published comparator views.

## Out of scope

- promoting a source-map link merely because it exists;
- implying that all retained external destinations are current or accurate;
- publishing private or licensed corpus rows;
- open-ended ingestion without a finite source set and stop condition.

## Acceptance checks

- each pass names its source set, intended reader outcome and completion test;
- every promoted canonical relation has an independent source and review record;
- source corrections remain distinguishable from source-published values;
- `make build` and `make validate` pass before deployment.

## Completed acceptance checks

- all 650 Systemic Evolution nodes and 1,320 source-reported links retained;
- cumulative reconciliation distinguishes 5 confirmed, 57 partial and 588
  unresolved source nodes;
- all 307 Castellani image-map links retained, including 28 exposed label
  disagreements;
- all 1,856 counted-map aggregate signals retained without private corpus data,
  EIDs or raw cited-reference strings;
- dedicated map, contribution and policy pages published;
- provenance and permission recorded for Benjamin Hadorn and Nigel Williams.

## Next bounded programmes

- manually reconcile the highest-connectivity unresolved Systemic Evolution nodes;
- independently evidence and type selected reported-influence links;
- check Castellani's 307 destinations and return apparent mismatches upstream;
- recover or replace the counted-map shrink pipeline with a reproducible public corpus;
- apply the same full-link contract to the remaining registered prior maps;
- test dense comparator canvases for mobile performance and accessibility.

## Stop conditions

Each follow-on pass needs its own finite source set and acceptance test. Do not
turn source-map adjacency, lexical co-occurrence or visual proximity into a
canonical relation without a separate evidence review.

## Model route

Use Luna for mechanical extraction and link checking, Terra for bounded
implementation and evidence passes, and Sol for disputed synthesis or major
architecture changes. Keep research and build work in separate contexts where
the claim boundary is material.
"""
    (ROOT / "documentation" / "NEXT_WORK.md").write_text(next_work, encoding="utf-8")

    state = f"""# Tangle state

Last verified: 25 August 2026

## Public release

- Release: `{RELEASE}`
- Public site: {PUBLIC_URL}
- Machine relationship snapshot: `data/relationship-quality.json`
- Prior-map hub: https://transduction.systems/prior-maps/
- Map of Systemic Evolution: 650 nodes; 1,320 source-reported links
- Castellani current source links: 307
- Counted-map aggregate links: 1,856
- Canonical relations created merely from comparator imports: 0

## Current shape

Release 0.20 publishes three distinct comparator views without flattening them
into the canonical atlas. The Systemic Evolution page retains the full
Schwarz–Durant–IIGSS–Hadorn provenance and shows the cumulative reconciliation.
The Castellani page preserves all current outward links while exposing source
label disagreements. The counted-map page retains aggregate signals while
excluding the private Scopus corpus and raw licensed reference strings.

The generated release contains {meta.get('public_entry_count')} canonical public
entries, {len(data.get('profiles', []))} developed profiles, {len(data.get('sources', []))}
public source records, {len(data.get('nodes', []))} total graph records and
{len(data.get('edges', []))} canonical graph statements.

## Current limits

The comparator links are source claims or aggregate signals, not a guarantee of
accuracy. Most Systemic Evolution nodes remain unreconciled, Castellani's links
have not been individually checked, and the counted-map aggregate cannot yet be
independently rerun from a public source corpus.

## Release controls

Run `make build`, then `make validate`. Check the public deployment, the main
reader and all four prior-map/contribution routes after merge.
"""
    (ROOT / "documentation" / "TANGLE_STATE.md").write_text(state, encoding="utf-8")

    changelog_path = ROOT / "CHANGELOG.md"
    changelog = changelog_path.read_text(encoding="utf-8")
    if f"## {RELEASE}" not in changelog:
        entry = f"""## {RELEASE} — 25 August 2026

- Published all 650 nodes and 1,320 source-reported major-influence links from the permissioned *Map of Systemic Evolution* comparator.
- Added a cumulative node-and-link reconciliation ledger without promoting imported links into the canonical atlas.
- Retained all 307 current Castellani image-map references and exposed 28 source-label disagreements.
- Incorporated Nigel Williams's relevant comparator, gap-analysis, build and counted-map work with a dedicated contribution record.
- Published all 1,856 counted-map aggregate signals while excluding private corpus data, EIDs and raw Scopus reference strings.
- Added a source-link policy which separates preservation, checking and canonical promotion.

"""
        changelog = changelog.replace("# Changelog\n\n", "# Changelog\n\n" + entry, 1)
        changelog_path.write_text(changelog, encoding="utf-8")

    readme_path = ROOT / "README.md"
    readme = readme_path.read_text(encoding="utf-8")
    release_intro = """## Release 0.20

Release 0.20 publishes a source-faithful prior-maps hub. It retains all 1,320 reported links in the permissioned *Map of Systemic Evolution*, all 307 clickable references in Brian Castellani's current map, and all 1,856 aggregate signals in Nigel Williams's counted-map experiment. Each layer states what its links can and cannot mean, and none is silently promoted into the canonical atlas.

Public routes:

- https://transduction.systems/
- https://transduction.systems/prior-maps/
- https://transduction.systems/prior-maps/systemic-evolution/
- https://transduction.systems/prior-maps/castellani/
- https://transduction.systems/prior-maps/counted-map/
- https://transduction.systems/contributors/nigel-williams/
- https://transduction.systems/corpora/complexity-podcast/
- https://transduction.systems/coverage/named/
- https://transduction.systems/coverage/unfix-32/


"""
    readme, count = re.subn(r"## Release 0\.(?:19|20)\n.*?\n\n(?=\*\*A living evidence atlas)", release_intro, readme, count=1, flags=re.S)
    if count != 1 and "## Release 0.20" not in readme:
        raise SystemExit("README release section changed unexpectedly")
    status = (
        f"Release 0.20 contains {meta.get('public_entry_count')} canonical public entries, "
        f"{len(data.get('profiles', []))} developed profiles and {len(data.get('sources', []))} public source "
        "records. Its comparator layers preserve 1,320 Systemic Evolution links, 307 Castellani references "
        "and 1,856 counted-map signals without treating import as verification.\n\n"
    )
    if "Release 0.20 contains" not in readme:
        readme = readme.replace("## Status\n\n", "## Status\n\n" + status, 1)
    readme_path.write_text(readme, encoding="utf-8")

    citation_path = ROOT / "CITATION.cff"
    citation = citation_path.read_text(encoding="utf-8")
    citation = re.sub(r"^version:\s*.*$", f"version: {RELEASE}", citation, flags=re.M)
    citation = re.sub(r"^date-released:\s*.*$", f"date-released: {GENERATED}", citation, flags=re.M)
    citation_path.write_text(citation, encoding="utf-8")

    acknowledgements_path = ROOT / "ACKNOWLEDGEMENTS.md"
    acknowledgements = acknowledgements_path.read_text(encoding="utf-8")
    old_ack = (
        "Igor Perko's researchers-network work provides a substantial comparator for mapping people and "
        "intellectual lineages. Brian Castellani's maps of the complexity sciences and other published maps "
        "provide material and challenge. Principia Cybernetica, the Foundational Papers in Complexity Science "
        "collection, Monoskop, SysCoI, model.report and professional-body resource guides are treated as distinct "
        "sources with different evidential limits."
    )
    new_ack = (
        old_ack
        + "\n\nThe *Map of Systemic Evolution* is credited through its full published lineage: Eric Schwarz "
        "(1996), the 1998 extension drawing on Will Durant, IIGSS (2000–01), and Benjamin Hadorn (2016). "
        "Benjamin Hadorn gave permission for the map's appropriate use in this project. Nigel Williams is "
        "credited for the deterministic GraphML extraction, comparator analysis, Castellani gap pass, counted-map "
        "experiment and build fixes incorporated in release 0.20. Brian Castellani retains authorship and the "
        "terms of his current *Map of the Complexity Sciences*."
    )
    acknowledgements = replace_once(acknowledgements, old_ack, new_ack, "comparators acknowledgement")
    acknowledgements_path.write_text(acknowledgements, encoding="utf-8")

    rights_path = ROOT / "RIGHTS.md"
    rights = rights_path.read_text(encoding="utf-8")
    marker = "Do not assume that a source linked from the atlas is open for redistribution merely because the atlas itself is open."
    addition = marker + """

The *Map of Systemic Evolution* comparator is reproduced with Benjamin Hadorn's permission and retains the full Schwarz–Durant–IIGSS–Hadorn provenance; that permission does not relicense the underlying map. Brian Castellani's current web map remains under its source terms, while the earlier 2012 Wikimedia SVG is marked there as CC BY-SA 3.0. Nigel Williams's counted-map projection publishes aggregate facts and permitted DOI handles only; licensed Scopus records, EIDs and raw cited-reference strings are not republished.
"""
    rights = replace_once(rights, marker, addition.rstrip(), "third-party map rights")
    rights_path.write_text(rights, encoding="utf-8")

    index_path = ROOT / "docs" / "index.html"
    index = index_path.read_text(encoding="utf-8")
    old_card = '<a class="coverage-card" href="https://github.com/antlerboy/the-necessary-tangle/issues/6" target="_blank" rel="noopener"><strong>Prior maps and bodies of knowledge</strong><span>Compare purposes, categories, boundaries, lines and evidence, including Castellani\'s map and Benjamin\'s critique.</span></a>'
    new_card = '<a class="coverage-card" href="/prior-maps/"><strong>Prior maps and bodies of knowledge</strong><span>Explore three live comparator layers, their complete source links, cumulative reconciliation and evidential limits.</span></a>'
    index = replace_once(index, old_card, new_card, "home prior-maps card")
    footer_marker = '<a class="text-button" href="/submissions/">Public submissions</a>'
    footer_addition = footer_marker + '<a class="text-button" href="/prior-maps/">Prior maps</a>'
    index = replace_once(index, footer_marker, footer_addition, "prior-maps footer route")
    index_path.write_text(index, encoding="utf-8")

    sitemap = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://transduction.systems/</loc><lastmod>2026-08-25</lastmod></url>
  <url><loc>https://transduction.systems/prior-maps/</loc><lastmod>2026-08-25</lastmod></url>
  <url><loc>https://transduction.systems/prior-maps/systemic-evolution/</loc><lastmod>2026-08-25</lastmod></url>
  <url><loc>https://transduction.systems/prior-maps/castellani/</loc><lastmod>2026-08-25</lastmod></url>
  <url><loc>https://transduction.systems/prior-maps/counted-map/</loc><lastmod>2026-08-25</lastmod></url>
  <url><loc>https://transduction.systems/contributors/nigel-williams/</loc><lastmod>2026-08-25</lastmod></url>
</urlset>
"""
    (ROOT / "docs" / "sitemap.xml").write_text(sitemap, encoding="utf-8")


def main() -> int:
    data = load_required(DATA_PATH)
    systemic = load_required(ROOT / "data" / "comparator-systemic-evolution.json")
    reconciliation = load_required(ROOT / "data" / "systemic-evolution-reconciliation.json")
    castellani = load_required(ROOT / "data" / "comparator-castellani-links.json")
    counted = load_required(ROOT / "data" / "counted-map-public.json")

    update_sources_and_registers(data)
    update_meta(data, systemic, reconciliation, castellani, counted)
    stamp_maintained_projections(data)
    publish_data(data)
    update_documents(data)
    print(
        f"Applied {RELEASE}: {systemic['meta']['node_count']} Systemic Evolution nodes / "
        f"{systemic['meta']['edge_count']} links, {castellani['meta']['link_count']} Castellani links, "
        f"{counted['meta']['edge_count']} counted-map signals"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
