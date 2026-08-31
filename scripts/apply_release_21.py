#!/usr/bin/env python3
"""Apply release 0.21: publish the reviewed Systemic Evolution package."""
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
AI_DOC = ROOT / "documentation" / "ai-observations.md"
CITATION = ROOT / "CITATION.cff"
REVIEW_ROOT = ROOT / "sources" / "systemic-evolution" / "review-1"

RELEASE = "0.21"
GENERATED = "2026-08-31"
PACKAGE_ID = "systemic-evolution-2026-08-26-review-1"
PACKAGE_SHA256 = "cc0aaa4adc58a91c56f04555d5cd6885d025cdf4d546e4da8e7a692ce55c3cf6"
COMPARATOR_SHA256 = "1b7c468dcaf89b654fad5923291284a382eb80221b5d366c53fb5c4c744742b2"
RECONCILIATION_SHA256 = "26b89b5123af4873e2e3c8b0aaa371aac03446b4ed4dd2e3396f1ab07143ba8c"

RELEASE_OBSERVATION = {
    "id": "permission_attaches_to_a_version",
    "title": "Permission attaches to a version",
    "kind": "rights and provenance observation",
    "measurement": (
        "Benjamin Hadorn granted the requested project-specific use scope on 26 August 2026, then reviewed and "
        "approved the exact package identified by SHA-256 on 31 August 2026."
    ),
    "interpretation": (
        "Permission is not a permanent adjective which can be pasted onto a changing dataset. It is a dated "
        "relationship between a grantor, a scope, conditions and an identifiable version."
    ),
    "implication": (
        "The source artefact, derivative, review manifest and publication decision must remain distinct records. "
        "Later graph-data changes reopen the review gate."
    ),
    "test": (
        "A reader should be able to identify the exact approved package, its checksum, attribution conditions and "
        "approval date without treating silence by another copied recipient as approval."
    ),
}

README_20 = (
    "## Release 0.20\n\n"
    "Release 0.20 publishes a source-faithful prior-maps hub. It retains all 1,320 reported links in the "
    "permissioned *Map of Systemic Evolution*, all 307 clickable references in Brian Castellani's current map, "
    "and all 1,856 aggregate signals in Nigel Williams's counted-map experiment. Each layer states what its links "
    "can and cannot mean, and none is silently promoted into the canonical atlas."
)
README_21 = (
    "## Release 0.21\n\n"
    "Release 0.21 publishes Benjamin Hadorn's source-owner-reviewed iteration of the *Map of Systemic Evolution*. "
    "It retains all 650 source nodes and 1,320 source-reported major-influence links, adds focused and complete "
    "layouts plus a text alternative, and identifies the exact approved package with immutable checksums. The "
    "scope grant, reviewed files, and publication decision remain separate records, and no comparator link is "
    "silently promoted into the canonical atlas."
)

OLD_ACKNOWLEDGEMENT = (
    "The *Map of Systemic Evolution* is credited through its full published lineage: Eric Schwarz (1996), the "
    "1998 extension drawing on Will Durant, IIGSS (2000–01), and Benjamin Hadorn (2016). Benjamin Hadorn gave "
    "permission for the map's appropriate use in this project. Nigel Williams is credited for the deterministic "
    "GraphML extraction, comparator analysis, Castellani gap pass, counted-map experiment and build fixes "
    "incorporated in release 0.20. Brian Castellani retains authorship and the terms of his current *Map of the "
    "Complexity Sciences*."
)
NEW_ACKNOWLEDGEMENT = (
    "The *Map of Systemic Evolution* is credited through its full published lineage: Eric Schwarz (1996), the "
    "1998 extension drawing on Will Durant, IIGSS (2000–01), and Benjamin Hadorn (2016), with required attribution "
    "to Eric Schwarz, Benjamin Hadorn, and Beat Hirsbrunner. Benjamin Hadorn granted the requested project-specific "
    "use scope on 26 August 2026, then reviewed the exact checksummed package and approved publication of the "
    "enhanced version on 31 August 2026. Beat Hirsbrunner was copied on the review exchange, but no separate "
    "response from him is recorded. Nigel Williams is credited for the deterministic GraphML extraction, "
    "comparator analysis, Castellani gap pass, counted-map experiment, and build fixes incorporated in release "
    "0.20. Brian Castellani retains authorship and the terms of his current *Map of the Complexity Sciences*."
)

OLD_RIGHTS = (
    "The *Map of Systemic Evolution* comparator is reproduced with Benjamin Hadorn's permission and retains the "
    "full Schwarz–Durant–IIGSS–Hadorn provenance; that permission does not relicense the underlying map. Brian "
    "Castellani's current web map remains under its source terms, while the earlier 2012 Wikimedia SVG is marked "
    "there as CC BY-SA 3.0. Nigel Williams's counted-map projection publishes aggregate facts and permitted DOI "
    "handles only; licensed Scopus records, EIDs and raw cited-reference strings are not republished."
)

STATE_20_SHAPE = (
    "Release 0.20 publishes three distinct comparator views without flattening them\n"
    "into the canonical atlas. The Systemic Evolution page retains the full\n"
    "Schwarz–Durant–IIGSS–Hadorn provenance and shows the cumulative reconciliation.\n"
    "The Castellani page preserves all current outward links while exposing source\n"
    "label disagreements. The counted-map page retains aggregate signals while\n"
    "excluding the private Scopus corpus and raw licensed reference strings."
)
STATE_21_SHAPE = (
    "Release 0.21 publishes the exact source-owner-reviewed Systemic Evolution\n"
    "reader and dataset without flattening them into the canonical atlas. The page\n"
    "retains the full Schwarz–Durant–IIGSS–Hadorn provenance, identifies the reviewed\n"
    "archive by checksum, and shows the cumulative reconciliation.\n"
    "The Castellani page preserves all current outward links while exposing source\n"
    "label disagreements. The counted-map page retains aggregate signals while\n"
    "excluding the private Scopus corpus and raw licensed reference strings.\n\n"
    "Benjamin Hadorn granted the requested use scope on 26 August 2026 and approved\n"
    "the exact enhanced package on 31 August 2026. The immutable review manifest and\n"
    "the later approval record remain separate. No separate response from Beat\n"
    "Hirsbrunner is recorded, and later graph-data changes reopen the review gate."
)

NEXT_20_STATUS = (
    "Status: release 0.20 is complete. Release 0.20.2 is the bounded reader hotfix;\n"
    "human review governs publication. No further production change is authorised\n"
    "without a bounded ticket."
)
NEXT_21_STATUS = (
    "Status: release 0.21 is complete. Human review governs publication.\n"
    "No further production change is authorised without a bounded ticket."
)
NEXT_20_OUTCOME = (
    "The first prior-map publication pass is live: every available link in the three\n"
    "implemented comparator views is preserved under an explicit source meaning and\n"
    "accuracy status, and no imported line is silently promoted into the canonical\n"
    "atlas."
)
NEXT_21_OUTCOME = (
    "The source-owner-reviewed Systemic Evolution iteration is live: its exact\n"
    "approved reader and dataset are published with checksums, full attribution,\n"
    "focused and complete layouts, and a text alternative. Every available link in\n"
    "the three implemented comparator views remains under an explicit source meaning\n"
    "and accuracy status, and no imported line is silently promoted into the\n"
    "canonical atlas."
)
NEXT_21_CHECKS = (
    "- provenance and permission recorded for Benjamin Hadorn and Nigel Williams;\n"
    "- Benjamin Hadorn's 26 August scope grant and 31 August package approval are\n"
    "  recorded separately without treating a copied recipient's silence as approval;\n"
    "- the exact reviewed Systemic Evolution package is published with its archive\n"
    "  checksum, immutable review manifest, and separate approval record;\n"
    "- focused one- and two-step neighbourhoods, the complete source layout, realm\n"
    "  and mapping filters, keyboard controls, and a text alternative are available;"
)


def write_json(path: Path, value: object, *, indent: int = 2) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=indent) + "\n", encoding="utf-8")


def replace_optional(text: str, old: str, new: str, label: str) -> str:
    if new in text:
        return text
    if old not in text:
        raise SystemExit(f"Release-document source drifted; expected {label} marker was not found")
    return text.replace(old, new, 1)


def update_release_documents() -> None:
    readme_path = ROOT / "README.md"
    readme = replace_optional(readme_path.read_text(encoding="utf-8"), README_20, README_21, "README release")
    readme_path.write_text(readme, encoding="utf-8")

    acknowledgement_path = ROOT / "ACKNOWLEDGEMENTS.md"
    acknowledgements = replace_optional(
        acknowledgement_path.read_text(encoding="utf-8"),
        OLD_ACKNOWLEDGEMENT,
        NEW_ACKNOWLEDGEMENT,
        "Systemic Evolution acknowledgement",
    )
    acknowledgement_path.write_text(acknowledgements, encoding="utf-8")

    rights_path = ROOT / "RIGHTS.md"
    rights = rights_path.read_text(encoding="utf-8")
    if OLD_RIGHTS in rights and "project-specific permission from Benjamin Hadorn" in rights:
        rights = rights.replace(OLD_RIGHTS + "\n\n", "", 1)
    if "project-specific permission from Benjamin Hadorn" not in rights:
        raise SystemExit("Release-document source drifted; current Systemic Evolution rights record is missing")
    rights_path.write_text(rights, encoding="utf-8")

    state_path = ROOT / "documentation" / "TANGLE_STATE.md"
    state = state_path.read_text(encoding="utf-8")
    state = replace_optional(state, "Last verified: 25 August 2026", "Last verified: 31 August 2026", "state date")
    state = replace_optional(state, "- Release: `0.20-prior-maps-alpha`", "- Release: `0.21`", "state release")
    state = replace_optional(
        state,
        "- Map of Systemic Evolution: 650 nodes; 1,320 source-reported links",
        "- Map of Systemic Evolution: 650 nodes; 1,320 source-reported links\n"
        f"- Systemic Evolution review archive SHA-256: `{PACKAGE_SHA256}`",
        "state archive checksum",
    )
    state = replace_optional(state, STATE_20_SHAPE, STATE_21_SHAPE, "state release shape")
    state_path.write_text(state, encoding="utf-8")

    next_path = ROOT / "documentation" / "NEXT_WORK.md"
    next_work = next_path.read_text(encoding="utf-8")
    next_work = replace_optional(next_work, NEXT_20_STATUS, NEXT_21_STATUS, "next-work status")
    next_work = replace_optional(next_work, NEXT_20_OUTCOME, NEXT_21_OUTCOME, "next-work outcome")
    next_work = replace_optional(
        next_work,
        "- provenance and permission recorded for Benjamin Hadorn and Nigel Williams.",
        NEXT_21_CHECKS,
        "next-work review checks",
    )
    next_path.write_text(next_work, encoding="utf-8")


def publish_reviewed_reader() -> None:
    copies = {
        REVIEW_ROOT / "site" / "prior-maps" / "systemic-evolution" / "index.html":
            ROOT / "docs" / "prior-maps" / "systemic-evolution" / "index.html",
        REVIEW_ROOT / "site" / "assets" / "systemic-evolution-map.js":
            DOCS_ASSETS / "systemic-evolution-map.js",
        REVIEW_ROOT / "site" / "assets" / "prior-maps.css":
            DOCS_ASSETS / "prior-maps.css",
        REVIEW_ROOT / "review-manifest.json":
            DOCS_ASSETS / "systemic-evolution-review-manifest.json",
        REVIEW_ROOT / "PUBLICATION_APPROVAL.json":
            DOCS_ASSETS / "systemic-evolution-publication-approval.json",
    }
    for source, destination in copies.items():
        if not source.is_file():
            raise SystemExit(f"Reviewed release source is missing: {source.relative_to(ROOT)}")
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)


def publish_exact_reviewed_datasets() -> None:
    comparator_path = ROOT / "data" / "comparator-systemic-evolution.json"
    comparator = json.loads(comparator_path.read_text(encoding="utf-8"))
    old_meta = comparator.get("meta", {})
    permission = {
        "granted_by": "Benjamin Hadorn",
        "granted_at": "2026-08-26",
        "scope": (
            "the reproduction, parsing, visualisation, annotation, correction, extension, derivative publication "
            "and independently checked incorporation requested by Benjamin P Taylor"
        ),
        "conditions": [
            "Full attribution to the original material and its extensions, including Eric Schwarz, Benjamin Hadorn and Beat Hirsbrunner.",
            "Every adapted, extended or modified graph or dataset must be provided to the maintainers for review and verification before publication.",
        ],
        "separate_permissions_required": False,
        "licence_note": (
            "The response permits sharing derivatives under the stated conditions but does not expressly "
            "relicense the original as CC BY-SA 4.0."
        ),
        "record": "https://github.com/antlerboy/the-necessary-tangle/issues/2#issuecomment-5424930678",
    }
    ordered_meta = {
        "dataset": old_meta["dataset"],
        "title": old_meta["title"],
        "role": old_meta["role"],
        "provenance": old_meta["provenance"],
        "published_at": old_meta["published_at"],
        "source_file_name": "systemic_evolution.graphml",
        "source_size_bytes": 1370282,
        "source_sha256": "c42241d61c76b5113fcbe65a6243cd7fcf3fe6d85b7fcb57b328594c94d9d104",
        "required_attribution": ["Eric Schwarz", "Benjamin Hadorn", "Beat Hirsbrunner"],
        "rights": (
            "Project-specific permission granted by Benjamin Hadorn on 2026-08-26 for the requested activities, "
            "subject to full attribution and review and verification of every modified graph or dataset before "
            "publication. The original is not represented as generally CC BY-SA licensed."
        ),
        "permission": permission,
        "semantics": old_meta["semantics"],
        "colour_legend": old_meta["colour_legend"],
        "node_count": old_meta["node_count"],
        "edge_count": old_meta["edge_count"],
        "labelled_edge_count": old_meta["labelled_edge_count"],
        "node_colour_census": old_meta["node_colour_census"],
        "contribution_credit": old_meta["contribution_credit"],
        "reconciliation_summary": old_meta["reconciliation_summary"],
    }
    comparator["meta"] = ordered_meta
    write_json(comparator_path, comparator, indent=1)
    shutil.copyfile(comparator_path, DOCS_ASSETS / comparator_path.name)

    reconciliation_path = ROOT / "data" / "systemic-evolution-reconciliation.json"
    reconciliation = json.loads(reconciliation_path.read_text(encoding="utf-8"))
    rmeta = reconciliation["meta"]
    rmeta["generated"] = "2026-08-26"
    scope_event = {
        "date": "2026-08-26",
        "event": (
            "Benjamin Hadorn confirmed the complete requested use scope, subject to full attribution and "
            "source-owner review and verification of modifications before publication."
        ),
    }
    history = rmeta.setdefault("cumulative_history", [])
    if scope_event not in history:
        history.append(scope_event)
    write_json(reconciliation_path, reconciliation, indent=2)
    shutil.copyfile(reconciliation_path, DOCS_ASSETS / reconciliation_path.name)


def update_atlas_release() -> None:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    meta = data.setdefault("meta", {})
    meta.update({
        "release": RELEASE,
        "generated": GENERATED,
        "iteration_focus": "source-owner-reviewed publication of the Systemic Evolution comparator",
        "release_note": (
            "Publishes the exact reviewed Systemic Evolution reader and data package, with focused and complete "
            "layouts, accessible text navigation, immutable review checksums and a separate approval record."
        ),
        "systemic_evolution_review_package": PACKAGE_ID,
        "systemic_evolution_review_archive_sha256": PACKAGE_SHA256,
        "systemic_evolution_source_owner_reviewed_at": GENERATED,
        "systemic_evolution_review_status": "exact_package_approved_for_publication",
    })

    for key in ("reading_list_inventory", "reading_list_coverage", "core_systems_practice"):
        projection = data.get(key)
        if not isinstance(projection, dict):
            raise SystemExit(f"Maintained projection is missing: {key}")
        projection["release"] = RELEASE

    for source in data.get("sources", []):
        if source.get("id") != "src_uranos_systemic_evolution":
            continue
        source.update({
            "notes": (
                "Primary publication and provenance page. It says the directed edges illustrate major influences "
                "between topics and publishes the scientific-realm colour legend. Benjamin Hadorn granted the "
                "requested project-specific use scope on 26 August 2026 and approved the exact checksummed "
                "enhanced package on 31 August 2026. The attribution, review and source-term conditions remain."
            ),
            "review_status": "source_owner_reviewed_derivative_published",
            "last_checked": GENERATED,
        })

    for node in data.get("nodes", []):
        if node.get("id") != "comparator_corpus_schwarz_some_streams_of_systemic_thought_map":
            continue
        node.update({
            "review_status": "source_owner_reviewed_comparator_published",
            "reviewed_by": "Benjamin P Taylor",
            "reviewed_at": GENERATED,
        })

    report = data.get("ai_observations")
    if not isinstance(report, dict):
        raise SystemExit("Maintained AI observations are missing")
    fresh = make_ai_observations(graph_metrics(data))
    fresh_by_id = {item.get("id"): item for item in fresh.get("observations", []) if item.get("id")}
    observations = [fresh_by_id.pop(item.get("id"), item) for item in report.get("observations", [])]
    observations.extend(fresh_by_id.values())
    observations = [item for item in observations if item.get("id") != RELEASE_OBSERVATION["id"]]
    observations.append(RELEASE_OBSERVATION)
    report.update({
        "release": RELEASE,
        "generated": GENERATED,
        "metrics": graph_metrics(data),
        "observations": observations,
    })

    rendered = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    DATA_PATH.write_text(rendered, encoding="utf-8")
    (DOCS_ASSETS / "public-data.json").write_text(rendered, encoding="utf-8")
    (DOCS_ASSETS / "public-data.js").write_text(
        "window.TANGLE_DATA = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n",
        encoding="utf-8",
    )

    lines = [
        "# AI observations",
        "",
        f"Generated for release `{RELEASE}` on {GENERATED}.",
        "",
        (
            "Release 0.21 publishes the source-owner-reviewed Systemic Evolution package and keeps the scope "
            "grant, exact derivative, review manifest and publication approval as separate records."
        ),
        "",
        (
            "Measurements come from the generated public graph. Interpretations concern this atlas and its "
            "current source, rights and interface choices; they are not measurements of the field itself."
        ),
        "",
    ]
    for item in observations:
        lines.extend([
            f"## {item.get('title', item.get('id', 'Observation'))}",
            "",
            f"**Kind:** {item.get('kind', '')}",
            "",
            f"**Measurement:** {item.get('measurement', '')}",
            "",
            f"**Interpretation:** {item.get('interpretation', '')}",
            "",
            f"**Implication:** {item.get('implication', '')}",
            "",
            f"**Test:** {item.get('test', '')}",
            "",
        ])
    AI_DOC.write_text("\n".join(lines), encoding="utf-8")

    citation = CITATION.read_text(encoding="utf-8")
    citation = re.sub(r"^version:\s*.*$", f"version: {RELEASE}", citation, flags=re.MULTILINE)
    citation = re.sub(r"^date-released:\s*.*$", f"date-released: {GENERATED}", citation, flags=re.MULTILINE)
    CITATION.write_text(citation, encoding="utf-8")


def main() -> None:
    publish_reviewed_reader()
    publish_exact_reviewed_datasets()
    update_atlas_release()
    update_release_documents()
    print(
        f"Applied release {RELEASE}: exact reviewed reader/data, package {PACKAGE_SHA256[:12]}…, "
        "and dated publication approval"
    )


if __name__ == "__main__":
    main()
