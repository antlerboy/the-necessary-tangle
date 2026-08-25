#!/usr/bin/env python3
"""Validate release 0.10 systems-work distinctions and publication controls."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "public-data.json"
DOCS = ROOT / "docs"
EXPECTED_RELEASE = "0.10-practice-safety-alpha"
ALLOWED_RELEASES = {EXPECTED_RELEASE, "0.11-visual-map-alpha", "0.12-practitioner-intake-alpha", "0.13-expertise-observations-alpha", "0.14-snowden-cynefin-alpha", "0.15-ing-reading-practice-alpha", "0.16-grammar-connections-presentation-alpha", "0.17-public-intake-lineage-alpha", "0.18-navigable-tangle-alpha", "0.19-living-marks-alpha", "0.20-prior-maps-alpha"}
EXPECTED_PUBLIC_COUNT = 417
EXPECTED_PROFILE_COUNT = 38
EXPECTED_JOURNEY_COUNT = 13
EXPECTED_MIN_SOURCES = 100
NEW_NODE_IDS = {
    "approach_family_systems_leadership",
    "approach_family_systems_change",
    "tradition_systems_theory",
    "practice_systems_practice",
    "practice_systems_convening",
    "practice_systems_weaving",
}
NEW_SOURCE_IDS = {
    "src_taylor_systems_leadership_schema_2021",
    "src_taylor_systems_terms_2022",
    "src_wenger_trayner_systems_convening",
    "src_scio_professional_body_current",
    "src_scio_professional_development_current",
    "src_network_weaver_current",
    "src_taylor_reading_list_current",
}
REQUIRED_EDGE_IDS = {
    "e_10_leadership_change_confusion",
    "e_10_leadership_uses_practice",
    "e_10_change_uses_practice",
    "e_10_practice_uses_theory",
    "e_10_convening_complements_practice",
    "e_10_weaving_complements_convening",
    "e_10_weaving_applies_networks",
}
PROMINENT_LINKS = {
    "https://www.syscoi.com/": "Systems Community of Inquiry",
    "https://www.systemspractice.org/professional-accreditation": "SCiO capability",
    "https://www.systemspractice.org/professional-development": "SCiO training",
    "https://stream.syscoi.com/2024/10/01/updated-rough-draft-systems-complexity-cybernetics-reading-list/": "Benjamin's reading list",
}
PRIVATE_PATTERNS = (
    "sharepoint.com",
    "graph.microsoft",
    "mail.google",
    "gmail.com/mail",
    "sandbox:/",
    "file://",
    "localhost",
    "127.0.0.1",
    "/mnt/data",
    "redquadrantltd.sharepoint",
    "c:\\users\\",
    "c:/users/",
)
SECRET_PATTERNS = (
    re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"(?i)(?:api[_-]?key|client[_-]?secret|access[_-]?token)\s*[:=]\s*['\"][^'\"]{12,}['\"]"),
)


def parse(value, fallback=None):
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


def main() -> int:
    errors: list[str] = []
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    meta = data.get("meta", {})
    redirects = data.get("canonical_redirects", {})
    canonical = lambda node_id: redirects.get(node_id, node_id)
    nodes = {node["id"]: node for node in data.get("nodes", []) if node.get("id")}
    public_nodes = [
        node for node in data.get("nodes", [])
        if node.get("public_visibility") == "public" and canonical(node["id"]) == node["id"]
    ]
    public_ids = {node["id"] for node in public_nodes}
    profiles = {profile.get("node_id"): profile for profile in data.get("profiles", []) if profile.get("node_id")}
    sources = {source["id"]: source for source in data.get("sources", []) if source.get("id")}
    journeys = {journey.get("id"): journey for journey in data.get("journeys", []) if journey.get("id")}
    edges = {edge.get("id"): edge for edge in data.get("edges", []) if edge.get("id")}

    if meta.get("release") not in ALLOWED_RELEASES:
        errors.append(f"meta.release must be one of {sorted(ALLOWED_RELEASES)}")
    if len(public_nodes) < EXPECTED_PUBLIC_COUNT or meta.get("public_entry_count", 0) < EXPECTED_PUBLIC_COUNT:
        errors.append(f"expected at least {EXPECTED_PUBLIC_COUNT} canonical public entries")
    developed = len(set(profiles) & public_ids)
    if developed < EXPECTED_PROFILE_COUNT or meta.get("profile_count", 0) < EXPECTED_PROFILE_COUNT:
        errors.append(f"expected at least {EXPECTED_PROFILE_COUNT} developed profiles")
    if len(journeys) < EXPECTED_JOURNEY_COUNT or meta.get("journey_count", 0) < EXPECTED_JOURNEY_COUNT:
        errors.append(f"expected at least {EXPECTED_JOURNEY_COUNT} guided journeys")
    if len(sources) < EXPECTED_MIN_SOURCES or meta.get("source_count", 0) < EXPECTED_MIN_SOURCES:
        errors.append(f"expected at least {EXPECTED_MIN_SOURCES} sources")

    for node_id in sorted(NEW_NODE_IDS):
        node = nodes.get(node_id)
        if not node:
            errors.append(f"missing new systems-work entry: {node_id}")
            continue
        if node_id not in public_ids or node.get("publication_level") != "profile":
            errors.append(f"new systems-work entry is not a public profile: {node_id}")
        profile = profiles.get(node_id)
        if not profile:
            errors.append(f"new systems-work entry has no profile: {node_id}")
            continue
        for field in ("summary", "why_it_matters", "key_distinctions", "common_misreadings", "open_checks"):
            if not profile.get(field):
                errors.append(f"new profile is missing {field}: {node_id}")
        linked = set(parse(node.get("source_ids"))) | set(parse(profile.get("source_ids")))
        if len(linked) < 2:
            errors.append(f"new systems-work entry needs at least two sources: {node_id}")
        unknown = linked - set(sources)
        if unknown:
            errors.append(f"new systems-work entry has unknown sources: {node_id} -> {sorted(unknown)}")

    for source_id in sorted(NEW_SOURCE_IDS):
        source = sources.get(source_id)
        if not source:
            errors.append(f"missing new source: {source_id}")
            continue
        if not str(source.get("url", "")).startswith("https://"):
            errors.append(f"new source lacks a public HTTPS URL: {source_id}")
        if not source.get("notes") or not source.get("review_status"):
            errors.append(f"new source lacks use/caution metadata: {source_id}")

    for edge_id in sorted(REQUIRED_EDGE_IDS):
        edge = edges.get(edge_id)
        if not edge:
            errors.append(f"missing required typed distinction: {edge_id}")
            continue
        if edge.get("relation_type") == "legacy_association_unspecified":
            errors.append(f"new distinction uses a legacy relation: {edge_id}")
        if not parse(edge.get("source_ids")):
            errors.append(f"new distinction has no sources: {edge_id}")

    journey = journeys.get("journey_six_systems_things")
    if not journey:
        errors.append("six-systems-things guided journey is missing")
    else:
        steps = journey.get("steps", [])
        if [step.get("node_id") for step in steps] != [
            "tradition_systems_theory",
            "practice_systems_practice",
            "approach_family_systems_leadership",
            "approach_family_systems_change",
            "practice_systems_convening",
            "practice_systems_weaving",
        ]:
            errors.append("six-systems-things journey has the wrong sequence")

    controls = data.get("publication_controls", [])
    if len(controls) != 6 or meta.get("publication_control_count") != 6:
        errors.append("expected six explicit publication controls")
    if len({item.get("id") for item in controls}) != len(controls):
        errors.append("publication controls contain duplicate IDs")
    report = data.get("ai_observations", {})
    if report.get("release") not in ALLOWED_RELEASES:
        errors.append("AI observations release is stale")
    if "public_risks" in report:
        errors.append("detailed working risk register remains in public data")
    if report.get("metrics", {}).get("public_entries", 0) < EXPECTED_PUBLIC_COUNT:
        errors.append("AI observation metrics have regressed below the 0.10 floor")

    index = (DOCS / "index.html").read_text(encoding="utf-8")
    app = (DOCS / "assets" / "app.js").read_text(encoding="utf-8")
    css = (DOCS / "assets" / "site-enhancements.css").read_text(encoding="utf-8")

    for url, label in PROMINENT_LINKS.items():
        if url not in index:
            errors.append(f"prominent public pathway missing: {label}")
    for marker in (
        'id="resourcePathwaysTitle"',
        'class="resource-pathway-grid"',
        'id="sixSystemsTitle"',
        'class="six-systems-grid"',
        'journey_six_systems_things',
        'class="plain-panel wide publication-safety-panel"',
    ):
        if marker not in index:
            errors.append(f"public interface missing 0.10 marker: {marker}")
    for marker in (".resource-pathway-grid", ".six-systems-grid", ".publication-safety-panel"):
        if marker not in css:
            errors.append(f"0.10 CSS missing: {marker}")

    forbidden_public_markers = [
        "aiRiskList",
        "Risks of making the atlas public",
        "documentation/publication-risks.md",
    ]
    for marker in forbidden_public_markers:
        if marker.casefold() in index.casefold() or marker.casefold() in app.casefold():
            errors.append(f"retired public working-note/risk marker remains: {marker}")

    required_files = [
        ROOT / "documentation" / "publication-safety.md",
        ROOT / "documentation" / "six-systems-things.md",
        ROOT / "documentation" / "ai-observations.md",
        ROOT / "SECURITY.md",
        ROOT / ".github" / "CODEOWNERS",
        ROOT / ".github" / "pull_request_template.md",
    ]
    for path in required_files:
        if not path.exists() or path.stat().st_size < 40:
            errors.append(f"missing or implausibly small release-control file: {path.relative_to(ROOT)}")
    if (ROOT / "documentation" / "publication-risks.md").exists():
        errors.append("detailed publication-risk working file remains in public repository")

    public_payloads = [
        DATA_PATH.read_text(encoding="utf-8"),
        index,
        app,
        (ROOT / "documentation" / "ai-observations.md").read_text(encoding="utf-8"),
        (ROOT / "documentation" / "publication-safety.md").read_text(encoding="utf-8"),
    ]
    for pattern in PRIVATE_PATTERNS:
        if any(pattern.casefold() in payload.casefold() for payload in public_payloads):
            errors.append(f"public release contains a private-path pattern: {pattern}")
    for secret_pattern in SECRET_PATTERNS:
        if any(secret_pattern.search(payload) for payload in public_payloads):
            errors.append(f"public release matches a credential pattern: {secret_pattern.pattern}")

    if errors:
        print("ITERATION 0.10 VALIDATION FAILED", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("ITERATION 0.10 VALIDATION PASSED")
    print(f"- canonical public entries: {len(public_nodes)}")
    print(f"- developed profiles: {developed}")
    print(f"- sources: {len(sources)}")
    print(f"- journeys: {len(journeys)}")
    print(f"- publication controls: {len(controls)}")
    print("- prominent pathways: SysCoI, SCiO capability, SCiO training, Benjamin's reading list")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
