#!/usr/bin/env python3
"""Apply release 0.19: living marks and a bounded Complexity Podcast corpus intake."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from apply_iteration_09 import graph_metrics, make_ai_observations
from apply_iteration_17 import (
    edge_record,
    enc,
    find_node,
    node_record,
    parse,
    profile_record,
    relation_record,
    source_record,
    upsert,
)
from apply_relational_depth_16 import calculate_relational_depth

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "public-data.json"
DOCS_ASSETS = ROOT / "docs" / "assets"
RELEASE = "0.19-living-marks-alpha"
GENERATED = "2026-08-25"
PUBLIC_URL = "https://transduction.systems/"
EPISODE_COUNT = 119
MARK_COUNT = 10


def source_19(*args: Any, **kwargs: Any) -> dict[str, Any]:
    record = source_record(*args, **kwargs)
    record["last_checked"] = GENERATED
    record["review_status"] = "checked"
    return record


SOURCES = [
    source_19(
        "src_sfi_complexity_podcast_archive_2026",
        "Podcast Archive — Complexity",
        "official_institutional_archive",
        "https://web-prod.santafe.edu/culture/podcast-archive",
        "The Santa Fe Institute's official podcast archive establishes COMPLEXITY as an SFI podcast and states that full transcripts for every episode are available through Simplecast.",
        ["Santa Fe Institute"],
        "Santa Fe Institute",
        "checked 2026-08-25",
    ),
    source_19(
        "src_sfi_complexity_simplecast_2026",
        "COMPLEXITY",
        "official_podcast_archive",
        "https://complexity.simplecast.com/",
        "The public Simplecast archive supplies episode pages, notes and transcript pages. A transcript establishes what was said in that episode; it does not independently establish the truth, priority or influence of the claim.",
        ["Santa Fe Institute"],
        "Santa Fe Institute / Simplecast",
        "2019-2024; checked 2026-08-25",
    ),
    source_19(
        "src_sfi_complexity_rss_2026",
        "COMPLEXITY RSS feed",
        "official_syndication_feed",
        "https://feeds.simplecast.com/OzDH_At2",
        "The official syndication feed is the machine-readable episode inventory. The 0.19 intake records 119 current feed items without converting every appearance or show-note link into a graph claim.",
        ["Santa Fe Institute"],
        "Santa Fe Institute / Simplecast",
        "2019-2024; checked 2026-08-25",
        quality="B",
    ),
]


def ensure_podcast_node(data: dict[str, Any]) -> str:
    node_id = find_node(data, "The Complexity Podcast")
    source_ids = [record["id"] for record in SOURCES]
    description = (
        "The official Santa Fe Institute podcast and transcript archive: a dated public record of conversations "
        "across complexity science, its applications and disputes. The corpus is evidence of what participants said "
        "and what SFI chose to publish, not automatic proof of a statement's truth or a guest's influence."
    )
    if not node_id:
        node_id = "publication_the_complexity_podcast"
        node = node_record(
            node_id,
            "The Complexity Podcast",
            "publication",
            description,
            source_ids,
            -620.0,
            -430.0,
            ["complexity-science", "podcast", "transcript-corpus", "source-corpus"],
            aliases=["COMPLEXITY podcast", "Santa Fe Institute Complexity podcast"],
            level="profile",
        )
        node.update({
            "inclusion_reason": "post_0_18_curator_corpus_request",
            "set_tags": enc(["systems", "complexity", "podcast", "transcript-corpus", "source-corpus", "release_0_19"]),
            "review_status": "curator_checked_public_sources",
            "reviewed_by": "Benjamin P Taylor",
            "reviewed_at": GENERATED,
            "public_source_count": len(source_ids),
        })
        upsert(data.setdefault("nodes", []), [node], "id")
    else:
        node = next(item for item in data.get("nodes", []) if item.get("id") == node_id)
        node["description"] = description
        node["canonical_definition"] = description
        node["source_ids"] = enc(list(dict.fromkeys([*parse(node.get("source_ids"), []), *source_ids])))
        node["aliases"] = enc(list(dict.fromkeys([*parse(node.get("aliases"), []), "COMPLEXITY podcast", "Santa Fe Institute Complexity podcast"])))
        node["set_tags"] = enc(list(dict.fromkeys([*parse(node.get("set_tags"), []), "transcript-corpus", "source-corpus", "release_0_19"])))
        node["publication_level"] = "profile"
        node["public_source_count"] = len(parse(node.get("source_ids"), []))
        node["reviewed_at"] = GENERATED

    profile = profile_record(
        node_id,
        description,
        "It is a substantial public, transcript-backed record of how one leading complexity-science institution frames questions, hosts disagreement and connects research domains over time.",
        [
            "An episode transcript supports a located account of what was said; it is not independent corroboration.",
            "A guest appearance documents participation, not intellectual priority, endorsement or field-wide importance.",
            "Show notes are discovery routes. Their linked papers and books must be checked directly before supporting stronger claims.",
            "The complete corpus can be registered before every episode has received a deep interpretive pass.",
        ],
        [
            "Published by the Santa Fe Institute from 2019 to 2024.",
            "The official archive points readers to a full transcript for every episode at Simplecast.",
            "Release 0.19 records the complete feed as a bounded corpus and starts a question-led review rather than a bulk edge-generation exercise.",
        ],
        ["Complexity science", "Public scholarship", "Transcript-backed source corpora"],
        ["Episode-level claims with timestamp or transcript locators", "Named works and institutional links checked at their primary sources"],
        [
            "Use transcript search to locate explicit definitions, disagreements, intellectual debts and practical examples.",
            "Use the RSS feed for inventory and dates, and the transcript page for the actual claim.",
        ],
        [
            "Treating the whole corpus as one coherent theory.",
            "Turning proximity to SFI into a proxy for truth or importance.",
            "Adding generic connections merely because two terms occur in the same conversation.",
        ],
        [
            "Complete an episode-level inventory with stable transcript URLs and guests.",
            "Deep-read priority episodes against existing atlas gaps before adding new claims.",
            "Record disagreements and source-role limits alongside any resulting edge.",
        ],
        source_ids,
        context="A public source corpus at the intersection of institutional communication, research conversation and field formation.",
        editorial_note="Registered as a complete corpus in 0.19; episode-level interpretation remains deliberately staged and source-located.",
    )
    profile["last_researched"] = GENERATED
    upsert(data.setdefault("profiles", []), [profile], "node_id")
    return node_id


def refresh_ai_observation_metrics(data: dict[str, Any]) -> None:
    """Regenerate the inherited measurement panel and maintained observation note."""
    report = data.get("ai_observations")
    if not isinstance(report, dict):
        return
    metrics = graph_metrics(data)
    regenerated = make_ai_observations(metrics)
    fresh_by_id = {
        item.get("id"): item for item in regenerated.get("observations", [])
        if item.get("id")
    }
    existing = report.get("observations", [])
    merged = [fresh_by_id.pop(item.get("id"), item) for item in existing]
    merged.extend(fresh_by_id.values())
    report["release"] = RELEASE
    report["generated"] = GENERATED
    report["metrics"] = metrics
    report["observations"] = merged

    lines = [
        "# AI observations",
        "",
        f"Generated for release `{RELEASE}` on {GENERATED}.",
        "",
        "This release retains the observation lenses introduced through `0.18-navigable-tangle-alpha`, while regenerating every graph measurement against the current public artefact.",
        "",
        str(report.get("method_note") or "These observations concern the atlas and its current source and interface choices, not the field itself."),
        "",
    ]
    for observation in merged:
        lines.extend([
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
        ])
    (ROOT / "documentation" / "ai-observations.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def update_release_documents(data: dict[str, Any]) -> None:
    metrics = graph_metrics(data)
    state = f"""# Tangle state

Last verified: 25 August 2026

## Public release

- Release: `{RELEASE}`
- Public site: {PUBLIC_URL}
- Canonical dataset: `data/public-data.json`
- Machine relationship snapshot: `data/relationship-quality.json`
- Public reader dataset: `docs/assets/public-data.json`
- Public knowledge index: `documentation/public-knowledge.md`
- Living visual marks: {MARK_COUNT}
- Complexity Podcast feed items registered: {EPISODE_COUNT}

## Current shape

Release 0.19 keeps the stable name, navigation and cream/red reading environment but replaces the fixed header badge with a living family of curator-supplied still and moving marks. One mark is selected on each fresh load. Motion is silent, short and replaced by a still when the reader requests reduced motion.

The release also registers the complete Santa Fe Institute *COMPLEXITY* podcast, RSS feed and transcript archive as a bounded source corpus. It states what each source can establish and does not turn {EPISODE_COUNT} episodes into {EPISODE_COUNT} shallow or generic graph claims.

The generated release currently contains {metrics.get('public_entries')} canonical public entries, {len(data.get('profiles', []))} developed profiles and {len(data.get('sources', []))} public source records.

The retained navigability baseline is `0.18-navigable-tangle-alpha`; unFIX comparator concepts resolved against the maintained 32-item set.

## Current limits

The podcast corpus is registered, not exhaustively interpreted. Episode-level claims still require transcript locators and, where relevant, checking against the primary papers or books named in show notes. The other long-running corpus and lineage programmes remain open.

## Release controls

Run `make build` when regenerating publication files, then run `make validate` against the generated release. Validation checks the operating spine, graph, evidence, reader assets, living-mark manifest, reduced-motion contract and JavaScript.
"""
    (ROOT / "documentation" / "TANGLE_STATE.md").write_text(state, encoding="utf-8")

    next_work = """# Next work

Status: release 0.19 is complete. No production change is authorised without a new ticket. Release 0.18 is complete and remains the historical navigability baseline.

## Outcome

Turn the registered source corpora into deeper, located and contestable knowledge without allowing inventory work to manufacture authority or generic graph density.

## In scope

- review live feedback and submitted tickets after 0.19;
- build the episode-level Complexity Podcast inventory and deep-read bounded thematic tranches;
- deepen entries currently marked `research_queue` or `represented` when public sources justify it;
- continue the named long-running corpus programmes as separately bounded passes;
- test the living marks, full-page reader, map, real-link behaviour and mobile layout with actual readers;
- correct broken or misleading source routes as they are found.

## Out of scope

- claiming that registering a corpus means interpreting it;
- treating a podcast appearance, institutional association or show-note link as proof of influence;
- bulk-generating biographies or relationships from names alone;
- merging inferred similarity with source-backed influence or lineage;
- hiding thin coverage behind visual density;
- redesigning away the cream, red, black and magic-dot identity without an explicit ticket.

## Acceptance checks

- one primary reader outcome per ticket;
- source-backed claims retain source identifiers and meaningful locators;
- new public entries expose typed connections or an honest thin/research state;
- ordinary navigational controls are genuine links where the destination can be represented by a URL;
- `make validate` passes on the complete generated release;
- the public deployment is checked at https://transduction.systems/ after merge.

## Stop conditions

Stop a pass when its stated corpus, names or interaction path has been checked, the acceptance tests pass and the remaining work would require a new evidence search or a different reader outcome. Do not turn a bounded pass into an unreviewed expansion.

## Model route

Use Luna for lightweight extraction and routine checks, Terra for bounded research and implementation, and Sol for architecture, adversarial review or disputed synthesis. Keep research and build work in separate contexts when the source set or claim boundary is material.
"""
    (ROOT / "documentation" / "NEXT_WORK.md").write_text(next_work, encoding="utf-8")

    feedback_path = ROOT / "documentation" / "feedback-ledger.md"
    feedback = feedback_path.read_text(encoding="utf-8")
    marker = "## Release 0.19 — living marks and Complexity Podcast corpus intake"
    if marker not in feedback:
        feedback = feedback.rstrip() + f"""


{marker}

- Fixed badge: replaced on the main public site by a random still or short moving mark selected from the curator's `SysCoCyBok/logoso` family.
- Stability: the wordmark, navigation, favicon, cream/red palette and bottom-right update dot remain fixed.
- Motion and access: videos are silent, inline and lightweight; reduced-motion readers receive the corresponding still poster.
- Failure mode: the 0.18 inline tangle SVG remains as a no-script and failed-request fallback.
- Visual rationale: documented as a family of cats-as-scientists, structural coupling, impossible forms and perceptual shifts rather than a single corporate emblem.
- Complexity Podcast: the official SFI archive, Simplecast transcripts and RSS feed are registered as a {EPISODE_COUNT}-item bounded corpus.
- Corpus limits: transcript and show-note source roles are explicit; no guest appearance or co-occurrence is treated as proof of truth, priority or influence.
""" + "\n"
        feedback_path.write_text(feedback, encoding="utf-8")

    changelog_path = ROOT / "CHANGELOG.md"
    changelog = changelog_path.read_text(encoding="utf-8")
    if "## 0.19-living-marks-alpha" not in changelog:
        entry = f"""## {RELEASE} — 25 August 2026

- Replaced the fixed header emblem with a random family of five still and five short moving marks while retaining the stable wordmark and navigation.
- Added silent autoplay, poster fallbacks, reduced-motion behaviour and a checked-in living-mark manifest.
- Registered the complete Santa Fe Institute *COMPLEXITY* podcast, RSS inventory and transcript archive as a bounded source corpus.
- Added a developed podcast entry, source-role account and public corpus page without manufacturing generic episode relations.
- Preserved the cream/red identity, stable favicon and bottom-right update-thread dot.

"""
        changelog = changelog.replace("# Changelog\n\n", "# Changelog\n\n" + entry, 1)
        changelog_path.write_text(changelog, encoding="utf-8")

    readme_path = ROOT / "README.md"
    readme = readme_path.read_text(encoding="utf-8")
    release_intro = f"""## Release 0.19

Release 0.19 gives the atlas a living visual identity. Each fresh load selects one of ten curator-supplied still or moving marks while the wordmark, navigation and reading environment stay stable. Motion is silent and falls back to a still for reduced-motion readers. The release also registers the complete Santa Fe Institute *COMPLEXITY* podcast and transcript archive as a bounded source corpus, with explicit limits on what an episode, transcript or show-note link can establish.

Public routes:

- https://transduction.systems/
- https://transduction.systems/corpora/complexity-podcast/
- https://transduction.systems/coverage/named/
- https://transduction.systems/coverage/unfix-32/


"""
    readme = re.sub(r"## Release 0\.18\n.*?\n\n(?=\*\*A living evidence atlas)", release_intro, readme, count=1, flags=re.S)
    if "Release 0.19 contains" not in readme:
        status_line = f"Release 0.19 contains {metrics.get('public_entries')} canonical public entries, {len(data.get('profiles', []))} developed profiles and {len(data.get('sources', []))} public source records. It adds the living-mark family and the bounded *COMPLEXITY* podcast corpus intake.\n\n"
        readme = readme.replace("## Status\n\n", "## Status\n\n" + status_line, 1)
    readme_path.write_text(readme, encoding="utf-8")

    citation_path = ROOT / "CITATION.cff"
    citation = citation_path.read_text(encoding="utf-8")
    citation = re.sub(r"^version:\s*.*$", f"version: {RELEASE}", citation, flags=re.M)
    citation = re.sub(r"^date-released:\s*.*$", f"date-released: {GENERATED}", citation, flags=re.M)
    citation_path.write_text(citation, encoding="utf-8")


def main() -> None:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    upsert(data.setdefault("sources", []), SOURCES, "id")
    podcast_id = ensure_podcast_node(data)

    sfi_id = find_node(data, "Santa Fe Institute")
    if not sfi_id:
        sfi_id = "organisation_santa_fe_institute"
        sfi = node_record(
            sfi_id,
            "Santa Fe Institute",
            "organisation",
            "An independent research institute dedicated to the study of complex adaptive systems.",
            ["src_sfi_complexity_podcast_archive_2026"],
            -740.0,
            -520.0,
            ["complexity-science", "research-institute"],
            aliases=["SFI"],
            level="described",
        )
        sfi.update({
            "inclusion_reason": "official_publisher_of_registered_corpus",
            "set_tags": enc(["complexity", "institution", "release_0_19"]),
            "reviewed_at": GENERATED,
        })
        upsert(data.setdefault("nodes", []), [sfi], "id")

    upsert(data.setdefault("relation_types", []), [
        relation_record(
            "publishes_source_corpus",
            "provenance",
            "is published by",
            "official publisher or institutional archive record",
            "publishes as a public source corpus",
        )
    ], "relation_type")
    upsert(data.setdefault("edges", []), [
        edge_record(
            "e19_sfi_publishes_complexity_podcast",
            sfi_id,
            podcast_id,
            "publishes_source_corpus",
            "provenance",
            "publishes as a public source corpus",
            ["src_sfi_complexity_podcast_archive_2026", "src_sfi_complexity_simplecast_2026"],
            "SFI Podcast Archive: Complexity; Simplecast series landing page",
            "This establishes institutional publication and transcript availability. It does not establish the truth or influence of any episode claim.",
        )
    ], "id")

    data["complexity_podcast_corpus"] = {
        "release": RELEASE,
        "status": "complete_corpus_registered_initial_review",
        "episode_count": EPISODE_COUNT,
        "date_range": "2019-2024",
        "official_archive_source_id": "src_sfi_complexity_podcast_archive_2026",
        "transcript_archive_source_id": "src_sfi_complexity_simplecast_2026",
        "rss_source_id": "src_sfi_complexity_rss_2026",
        "method": "Use the RSS feed for inventory, the episode transcript for located speech, and primary works for stronger scholarly claims.",
        "caution": "A guest appearance or co-occurrence is not evidence of influence, agreement, priority or truth.",
        "deep_review_status": "staged_by_question_and_existing_atlas_gap",
    }

    # These are maintained current-state projections, not frozen historical snapshots.
    # Restamp them when the release changes so their content and status remain internally coherent.
    for projection_name in ("reading_list_inventory", "reading_list_coverage", "core_systems_practice"):
        projection = data.get(projection_name)
        if isinstance(projection, dict):
            projection["release"] = RELEASE
            if "generated" in projection:
                projection["generated"] = GENERATED

    refresh_ai_observation_metrics(data)
    data["relational_depth"] = calculate_relational_depth(data)
    relational_aggregate = data.get("relational_depth", {}).get("aggregate", {})
    metrics = graph_metrics(data)
    meta = data.setdefault("meta", {})
    meta.update({
        "release": RELEASE,
        "generated": GENERATED,
        "project_url": PUBLIC_URL,
        "public_entry_count": metrics.get("public_entries"),
        "profile_count": len(data.get("profiles", [])),
        "source_count": len(data.get("sources", [])),
        "journey_count": len(data.get("journeys", [])),
        "living_mark_count": MARK_COUNT,
        "complexity_podcast_episode_count": EPISODE_COUNT,
        "visual_identity_contract": "living-marks-v1",
        "reader_connected_entry_count": relational_aggregate.get("reader_connected_entries", 0),
        "semantic_connected_entry_count": metrics.get("substantive_connected_nodes"),
        "semantic_gap_entry_count": metrics.get("substantive_isolated_nodes"),
        "typed_edge_count": metrics.get("typed_edges"),
        "substantive_edge_count": metrics.get("substantive_edges"),
    })

    DATA_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    DOCS_ASSETS.mkdir(parents=True, exist_ok=True)
    (DOCS_ASSETS / "public-data.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    update_release_documents(data)
    print(f"Applied {RELEASE}: {metrics.get('public_entries')} public entries, {len(data.get('sources', []))} sources")


if __name__ == "__main__":
    main()
