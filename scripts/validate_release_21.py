#!/usr/bin/env python3
"""Validate release 0.21 and the source-owner-reviewed publication boundary."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from apply_release_21 import (
    COMPARATOR_SHA256,
    GENERATED,
    PACKAGE_ID,
    PACKAGE_SHA256,
    RECONCILIATION_SHA256,
    RELEASE,
)

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def load(path: str) -> dict:
    return json.loads(read(path))


def sha256(path: str) -> str:
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def main() -> int:
    errors: list[str] = []
    atlas = load("data/public-data.json")
    browser = load("docs/assets/public-data.json")
    meta = atlas.get("meta", {})
    if meta.get("release") != RELEASE or meta.get("generated") != GENERATED:
        errors.append(f"canonical metadata is not {RELEASE} / {GENERATED}")
    if browser != atlas:
        errors.append("browser public data differs from canonical release data")
    if meta.get("systemic_evolution_review_package") != PACKAGE_ID:
        errors.append("release metadata does not identify the reviewed package")
    if meta.get("systemic_evolution_review_archive_sha256") != PACKAGE_SHA256:
        errors.append("release metadata does not carry the reviewed archive checksum")
    if meta.get("systemic_evolution_review_status") != "exact_package_approved_for_publication":
        errors.append("release metadata does not record source-owner approval")
    for key in ("reading_list_inventory", "reading_list_coverage", "core_systems_practice"):
        if atlas.get(key, {}).get("release") != RELEASE:
            errors.append(f"maintained projection still identifies an earlier release: {key}")

    comparator_path = "data/comparator-systemic-evolution.json"
    reconciliation_path = "data/systemic-evolution-reconciliation.json"
    if sha256(comparator_path) != COMPARATOR_SHA256:
        errors.append("published comparator JSON is not the exact reviewed file")
    if sha256(reconciliation_path) != RECONCILIATION_SHA256:
        errors.append("published reconciliation JSON is not the exact reviewed file")
    for name in ("comparator-systemic-evolution.json", "systemic-evolution-reconciliation.json"):
        if (ROOT / "data" / name).read_bytes() != (ROOT / "docs" / "assets" / name).read_bytes():
            errors.append(f"public comparator asset differs from data/{name}")

    comparator = load(comparator_path)
    cmeta = comparator.get("meta", {})
    if len(comparator.get("nodes", [])) != 650 or len(comparator.get("edges", [])) != 1320:
        errors.append("reviewed comparator does not retain 650 nodes and 1,320 links")
    if cmeta.get("source_sha256") != "c42241d61c76b5113fcbe65a6243cd7fcf3fe6d85b7fcb57b328594c94d9d104":
        errors.append("original GraphML checksum is missing or changed")
    if cmeta.get("required_attribution") != ["Eric Schwarz", "Benjamin Hadorn", "Beat Hirsbrunner"]:
        errors.append("required source-owner attribution is incomplete")
    permission = cmeta.get("permission", {})
    if permission.get("granted_at") != "2026-08-26" or permission.get("granted_by") != "Benjamin Hadorn":
        errors.append("scope permission date or grantor is wrong")
    if cmeta.get("reconciliation_summary", {}).get("canonical_atlas_relations_created_from_source_links") != 0:
        errors.append("a comparator link has been promoted merely by import")

    manifest = load("docs/assets/systemic-evolution-review-manifest.json")
    approval = load("docs/assets/systemic-evolution-publication-approval.json")
    if manifest.get("package_id") != PACKAGE_ID or manifest.get("publication_status") != "awaiting_source_owner_review":
        errors.append("immutable review manifest no longer represents the package submitted for review")
    if approval.get("package_id") != PACKAGE_ID or approval.get("decision") != "approved_for_publication":
        errors.append("separate publication approval is missing or points to another package")
    if approval.get("review_archive", {}).get("sha256") != PACKAGE_SHA256:
        errors.append("publication approval does not identify the exact reviewed archive")
    if approval.get("source_owner_reviewed_at") != GENERATED or approval.get("reviewed_by") != "Benjamin Hadorn":
        errors.append("source-owner review date or reviewer is wrong")
    if "no separate response" not in approval.get("beat_hirsbrunner_status", "").lower():
        errors.append("approval record does not preserve the Beat Hirsbrunner response boundary")

    exact_assets = {
        "docs/assets/systemic-evolution-map.js": "sources/systemic-evolution/review-1/site/assets/systemic-evolution-map.js",
        "docs/assets/prior-maps.css": "sources/systemic-evolution/review-1/site/assets/prior-maps.css",
        "docs/assets/systemic-evolution-review-manifest.json": "sources/systemic-evolution/review-1/review-manifest.json",
        "docs/assets/systemic-evolution-publication-approval.json": "sources/systemic-evolution/review-1/PUBLICATION_APPROVAL.json",
    }
    for public_path, reviewed_path in exact_assets.items():
        if (ROOT / public_path).read_bytes() != (ROOT / reviewed_path).read_bytes():
            errors.append(f"public asset differs from its reviewed or canonical record: {public_path}")

    page = read("docs/prior-maps/systemic-evolution/index.html")
    page_markers = (
        "Source-owner review completed.",
        "/assets/systemic-evolution-release-21.css?v=0.21.0-published",
        "systemicView",
        "systemicDepth",
        "systemicRealm",
        "Browse the current view as text",
        "Complete source layout",
        PACKAGE_SHA256,
        "/assets/systemic-evolution-publication-approval.json",
        "approved use of the enhanced version in this way",
    )
    for marker in page_markers:
        if marker not in page:
            errors.append(f"Systemic Evolution reader is missing: {marker}")
    if "systemic_evolution-2016-original.graphml" in page:
        errors.append("reader links to an unshipped individual GraphML file")

    publication_css = read("docs/assets/systemic-evolution-release-21.css")
    if ".pm-text-view-grid > * { min-width: 0; }" not in publication_css:
        errors.append("mobile text-view tables are not contained within their grid column")
    if "@media (max-width: 620px) { .pm-shell { overflow-x: hidden; } }" not in publication_css:
        errors.append("mobile table overflow is not clipped at the reader shell")

    script = read("docs/assets/systemic-evolution-map.js")
    for marker in (
        "visibleNodeIds",
        "systemicVisibleLinks",
        "systemicZoomIn",
        "history.replaceState",
        "addEventListener('keydown'",
    ):
        if marker not in script:
            errors.append(f"reviewed map interaction is missing: {marker}")

    index = read("docs/index.html")
    for marker in (
        '<span id="releaseBadge">Release 0.21</span>',
        "assets/iteration-20.js?v=0.21-reviewed-systemic-evolution",
        "<strong>Updated for 0.21:</strong>",
        "source-owner-reviewed Systemic Evolution reader",
    ):
        if marker not in index:
            errors.append(f"main reader release surface is missing: {marker}")

    citation = read("CITATION.cff")
    if f"version: {RELEASE}" not in citation or f"date-released: {GENERATED}" not in citation:
        errors.append("citation record is not aligned with release 0.21")
    ai_doc = read("documentation/ai-observations.md")
    if f"Generated for release `{RELEASE}` on {GENERATED}." not in ai_doc or "Permission attaches to a version" not in ai_doc:
        errors.append("maintained observations do not describe the reviewed release")

    documentation_markers = {
        "documentation/comparator-systemic-evolution.md": ["26 August", "31 August", PACKAGE_SHA256],
        "RIGHTS.md": ["31 August 2026", "Beat Hirsbrunner", "does not relicense"],
        "ACKNOWLEDGEMENTS.md": ["reviewed the exact checksummed package", "Beat Hirsbrunner"],
        "documentation/TANGLE_STATE.md": ["Release: `0.21`", "source-owner-reviewed"],
        "documentation/NEXT_WORK.md": ["release 0.21 is complete", "No further production change is authorised"],
        "README.md": ["## Release 0.21", "source-owner-reviewed"],
        "CHANGELOG.md": ["## 0.21 — 31 August 2026", "exact checksummed"],
    }
    for path, markers in documentation_markers.items():
        body = read(path)
        for marker in markers:
            if marker not in body:
                errors.append(f"release documentation is missing from {path}: {marker}")

    if errors:
        print("Release 0.21 validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        f"Validated {RELEASE}: exact reviewed package {PACKAGE_SHA256[:12]}…, "
        "650 nodes, 1,320 links and zero comparator-derived canonical relations"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
