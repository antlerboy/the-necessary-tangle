#!/usr/bin/env python3
"""Validate release 0.13 expertise depth, regenerated observations and clean publication."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from apply_iteration_09 import graph_metrics

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "public-data.json"
DOCS = ROOT / "docs"
EXPECTED_RELEASE = "0.13-expertise-observations-alpha"
ALLOWED_RELEASES = {EXPECTED_RELEASE, "0.14-snowden-cynefin-alpha", "0.15-ing-reading-practice-alpha", "0.16-grammar-connections-presentation-alpha", "0.17-public-intake-lineage-alpha"}
EXPECTED_DATE = "2026-08-11"

REQUIRED_NODE_IDS = {
    "person_peter_checkland",
    "publication_systems_thinking_systems_practice",
    "person_werner_ulrich",
    "publication_mini_primer_critical_systems_heuristics",
    "concept_boundary_critique",
    "person_ray_ison",
    "person_ed_straw",
    "publication_hidden_power_systems_thinking",
    "concept_systemic_governance",
    "person_raul_espejo",
    "person_alfonso_reyes",
    "publication_organizational_systems_vsm",
    "method_or_methodology_viplan",
    "person_donella_meadows",
    "person_diana_wright",
    "publication_thinking_in_systems",
    "publication_leverage_points_meadows",
    "publication_dancing_with_systems",
    "concept_leverage_points",
    "person_barry_oshry",
    "publication_organic_systems_framework",
    "method_or_methodology_organic_systems_framework",
    "method_or_methodology_soft_systems_methodology_ssm",
    "method_or_methodology_critical_systems_heuristics_csh",
}
PROFILE_NODE_IDS = REQUIRED_NODE_IDS - {"person_ed_straw", "person_diana_wright"}
REQUIRED_SOURCE_IDS = {
    "src_lancaster_checkland_stsp_1999",
    "src_wiley_checkland_stsp_1999",
    "src_ulrich_csh_mini_primer_2023",
    "src_ou_ray_ison_profile_2026",
    "src_routledge_hidden_power_2020",
    "src_springer_organizational_systems_2011",
    "src_prh_thinking_in_systems_2008",
    "src_meadows_dancing_with_systems",
    "src_meadows_leverage_points",
    "src_triarchy_organic_systems_framework_2019",
    "src_triarchy_barry_oshry_profile",
}
REQUIRED_EDGE_IDS = {
    "e_13_stsp_checkland", "e_13_checkland_ssm", "e_13_stsp_ssm", "e_13_stsp_practice",
    "e_13_primer_ulrich", "e_13_ulrich_csh", "e_13_primer_csh", "e_13_csh_boundary_critique",
    "e_13_boundary_critique_boundary", "e_13_hidden_ison", "e_13_hidden_straw", "e_13_ison_governance",
    "e_13_hidden_governance", "e_13_hidden_practice", "e_13_orgsys_espejo", "e_13_orgsys_reyes",
    "e_13_orgsys_vsm", "e_13_orgsys_viplan", "e_13_espejo_viplan", "e_13_viplan_vsm",
    "e_13_thinking_meadows", "e_13_thinking_wright", "e_13_thinking_feedback", "e_13_thinking_sd",
    "e_13_leverage_meadows", "e_13_leverage_concept", "e_13_leverage_feedback", "e_13_dancing_meadows",
    "e_13_dancing_practice", "e_13_osf_pub_oshry", "e_13_oshry_osf", "e_13_osf_pub_method",
    "e_13_osf_practice", "e_13_osf_boundary", "e_13_ivo_viability_expertise", "e_13_ivo_semantics_expertise",
    "e_13_patrick_vsm_expertise", "e_13_patrick_strategy_expertise",
}
OBSERVATION_IDS = {
    "breadth_outpaces_depth", "two_graph_regimes", "expertise_needs_relations", "catalogue_is_not_critique",
    "practice_is_peripheral", "source_monoculture", "identity_resolution", "neighbourhoods_are_stale",
    "bridge_concepts", "map_of_attention", "automated_overreading",
}
FORBIDDEN_PUBLIC_PATTERNS = (
    "data-curator-dot",
    "curator-secret-dot",
    "curator-notebook-link",
    "discreet-note-link",
    "model-assisted",
    "machine-assisted second-order",
)
PRIVATE_PATTERNS = (
    "sharepoint.com", "graph.microsoft", "mail.google", "gmail.com/mail",
    "sandbox:/", "file://", "localhost", "127.0.0.1", "/mnt/data",
    "redquadrantltd.sharepoint", "c:\\users\\", "c:/users/",
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
    profiles = {profile.get("node_id"): profile for profile in data.get("profiles", []) if profile.get("node_id")}
    sources = {source.get("id"): source for source in data.get("sources", []) if source.get("id")}
    edges = {edge.get("id"): edge for edge in data.get("edges", []) if edge.get("id")}
    journeys = {journey.get("id"): journey for journey in data.get("journeys", []) if journey.get("id")}
    public_nodes = [
        node for node in data.get("nodes", [])
        if node.get("public_visibility") == "public" and canonical(node["id"]) == node["id"]
    ]
    public_ids = {node["id"] for node in public_nodes}
    developed = len(set(profiles) & public_ids)

    if meta.get("release") not in ALLOWED_RELEASES:
        errors.append(f"meta.release must be one of {sorted(ALLOWED_RELEASES)}")
    expected_date = "2026-08-19" if meta.get("release") == "0.17-public-intake-lineage-alpha" else ("2026-08-14" if meta.get("release") in {"0.15-ing-reading-practice-alpha", "0.16-grammar-connections-presentation-alpha", "0.17-public-intake-lineage-alpha"} else EXPECTED_DATE)
    if meta.get("generated") != expected_date:
        errors.append(f"meta.generated must be {expected_date}")
    for label, actual, minimum in [
        ("public entries", len(public_nodes), 464),
        ("developed profiles", developed, 80),
        ("sources", len(sources), 125),
        ("journeys", len(journeys), 15),
        ("typed edges", len(data.get("edges", [])), 635),
    ]:
        if actual < minimum:
            errors.append(f"expected at least {minimum} {label}, found {actual}")
    if meta.get("public_entry_count") != len(public_nodes):
        errors.append("meta public-entry count is stale")
    if meta.get("profile_count") != developed:
        errors.append("meta profile count is stale")
    if meta.get("source_count") != len(sources):
        errors.append("meta source count is stale")
    if meta.get("journey_count") != len(journeys):
        errors.append("meta journey count is stale")

    for node_id in sorted(REQUIRED_NODE_IDS):
        node = nodes.get(node_id)
        if not node:
            errors.append(f"missing expertise entry: {node_id}")
            continue
        if node_id not in public_ids:
            errors.append(f"expertise entry is not canonical public: {node_id}")
        profile = profiles.get(node_id)
        if node_id in PROFILE_NODE_IDS:
            if node.get("publication_level") != "profile":
                errors.append(f"expertise entry is not developed: {node_id}")
            if not profile:
                errors.append(f"expertise entry has no profile: {node_id}")
                continue
            for field in ("summary", "why_it_matters", "key_distinctions", "practice_connections", "common_misreadings", "open_checks"):
                if not profile.get(field):
                    errors.append(f"expertise profile lacks {field}: {node_id}")
        linked = set(parse(node.get("source_ids"))) | set(parse((profile or {}).get("source_ids")))
        if not linked:
            errors.append(f"expertise entry has no sources: {node_id}")
        unknown = linked - set(sources)
        if unknown:
            errors.append(f"expertise entry cites unknown sources: {node_id} -> {sorted(unknown)}")

    for source_id in sorted(REQUIRED_SOURCE_IDS):
        source = sources.get(source_id)
        if not source:
            errors.append(f"missing expertise source: {source_id}")
            continue
        if not str(source.get("url", "")).startswith("https://"):
            errors.append(f"expertise source lacks public HTTPS URL: {source_id}")
        if not source.get("notes") or source.get("review_status") != "checked":
            errors.append(f"expertise source lacks checked review metadata: {source_id}")
        if source.get("last_checked") != EXPECTED_DATE:
            errors.append(f"expertise source check date is stale: {source_id}")

    for edge_id in sorted(REQUIRED_EDGE_IDS):
        edge = edges.get(edge_id)
        if not edge:
            errors.append(f"missing expertise relation: {edge_id}")
            continue
        for field in ("source", "target", "relation_type", "relation_family", "plain_phrase", "claim_status", "confidence", "source_ids", "scope_conditions"):
            if not edge.get(field):
                errors.append(f"expertise relation {edge_id} lacks {field}")
        if edge.get("relation_type") == "legacy_association_unspecified":
            errors.append(f"expertise relation uses legacy semantics: {edge_id}")
        if not set(parse(edge.get("source_ids"))).issubset(sources):
            errors.append(f"expertise relation cites unknown source: {edge_id}")

    journey = journeys.get("journey_inquiry_governance_and_intervention")
    if not journey or len(journey.get("steps", [])) < 13:
        errors.append("inquiry, governance and intervention journey is missing or too short")
    elif any(step.get("node_id") not in public_ids or not step.get("heading") or not step.get("narrative") for step in journey.get("steps", [])):
        errors.append("inquiry, governance and intervention journey has incomplete steps")

    ivo = profiles.get("person_ivo_velitchkov", {})
    patrick = profiles.get("person_patrick_hoverstadt", {})
    ivo_text = json.dumps(ivo, ensure_ascii=False).casefold()
    patrick_text = json.dumps(patrick, ensure_ascii=False).casefold()
    if not all(term in ivo_text for term in ("viable organisation", "requisite inefficiency", "semantic")):
        errors.append("Ivo Velitchkov is not framed through his expertise")
    if not all(term in patrick_text for term in ("viable system model", "systems laws", "strategy")):
        errors.append("Patrick Hoverstadt is not framed through his expertise")
    for text, label in ((ivo_text, "Ivo Velitchkov"), (patrick_text, "Patrick Hoverstadt")):
        if any(term in text for term in ("omission", "missed", "submission", "running thread", "editorial failure")):
            errors.append(f"{label} profile retains process-centred wording")

    report = data.get("ai_observations", {})
    if report.get("release") != meta.get("release") or report.get("generated") != meta.get("generated"):
        errors.append("AI observations were not regenerated for the current release")
    observations = report.get("observations", [])
    if not OBSERVATION_IDS.issubset({item.get("id") for item in observations}):
        errors.append("AI observation set is incomplete or stale")
    for observation in observations:
        for field in ("title", "kind", "measurement", "interpretation", "implication", "test"):
            if not observation.get(field):
                errors.append(f"AI observation {observation.get('id')} lacks {field}")
    recalculated = graph_metrics(data)
    if report.get("metrics") != recalculated:
        errors.append("AI observation metrics do not match the current graph")
    ai_doc = ROOT / "documentation" / "ai-observations.md"
    expected_ai_line = f"Generated for release `{meta.get('release')}` on {meta.get('generated')}."
    if not ai_doc.exists() or expected_ai_line not in ai_doc.read_text(encoding="utf-8"):
        errors.append("maintained AI observation document is stale or missing")

    if data.get("accepted_contributions"):
        errors.append("public data publishes editorial-process contribution records")
    intake = data.get("contribution_intake", {})
    if intake.get("version") != "proposal-intake-v2":
        errors.append("proposal intake version is missing")
    if {feed.get("id") for feed in intake.get("feeds", [])} != {"site_submissions", "research_issues", "pull_requests"}:
        errors.append("proposal intake feeds are incomplete")

    index = DOCS / "index.html"
    app = DOCS / "assets" / "app.js"
    config = DOCS / "assets" / "site-config.js"
    css = DOCS / "assets" / "site-enhancements.css"
    public_paths = sorted({
        DATA_PATH,
        *DOCS.rglob("*.html"), *DOCS.rglob("*.js"), *DOCS.rglob("*.css"), *DOCS.rglob("*.json"),
        *(ROOT / "documentation").glob("*.md"),
        ROOT / "ACKNOWLEDGEMENTS.md", ROOT / "README.md", ROOT / "CHANGELOG.md", ROOT / "CITATION.cff",
    }, key=lambda path: str(path))
    for path in public_paths:
        if not path.exists():
            errors.append(f"required public file is missing: {path.relative_to(ROOT)}")
    public_text = "\n".join(path.read_text(encoding="utf-8", errors="ignore") for path in public_paths if path.exists())
    folded = public_text.casefold()
    if re.search(r"running\s+(?:feedback|comment|working)\s+(?:thread|note(?:book)?)", public_text, flags=re.I):
        errors.append("public release contains editorial-process narrative")
    for pattern in FORBIDDEN_PUBLIC_PATTERNS:
        if pattern.casefold() in folded:
            errors.append(f"public release contains internal or self-referential marker: {pattern}")
    for pattern in PRIVATE_PATTERNS:
        if pattern.casefold() in folded:
            errors.append(f"public release contains private or local marker: {pattern}")
    for pattern in SECRET_PATTERNS:
        if pattern.search(public_text):
            errors.append(f"public release contains secret-like value: {pattern.pattern}")

    index_text = index.read_text(encoding="utf-8")
    app_text = app.read_text(encoding="utf-8")
    css_text = css.read_text(encoding="utf-8")
    for marker in (
        'class="plain-panel wide expertise-callout"',
        'class="plain-panel wide proposal-intake-panel"',
        'journey_inquiry_governance_and_intervention',
        'person_ivo_velitchkov', 'person_patrick_hoverstadt', 'person_donella_meadows',
        'id="view-ai-observations"', 'id="aiObservationMetrics"', 'id="aiObservationsList"',
    ):
        if marker not in index_text:
            errors.append(f"0.13 public interface is missing: {marker}")
    if "copyAskContext" not in app_text or "renderAsk" not in app_text:
        errors.append("question-led atlas context is missing")
    for marker in (".expertise-callout", ".proposal-intake-panel"):
        if marker not in css_text:
            errors.append(f"0.13 CSS is missing: {marker}")

    citation_text = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    if f"version: {meta.get('release')}" not in citation_text or f"date-released: {meta.get('generated')}" not in citation_text:
        errors.append("citation metadata does not identify the current release")

    if meta.get("release") != "0.17-public-intake-lineage-alpha" and (ROOT / "documentation" / "feedback-ledger.md").exists():
        errors.append("obsolete process-ledger document remains")
    if list((ROOT / "documentation").glob("public-knowledge-for-*.md")):
        errors.append("legacy service-specific public knowledge file remains")
    for path, minimum in {
        "documentation/ai-observations.md": 2500,
        "documentation/public-knowledge.md": 10000,
        "documentation/expertise-additions.md": 800,
        "documentation/contribution-intake.md": 700,
        "documentation/publication-standards.md": 500,
    }.items():
        target = ROOT / path
        if not target.exists() or target.stat().st_size < minimum:
            errors.append(f"{path} is missing or implausibly small")

    if errors:
        print("ITERATION 0.13 VALIDATION FAILED", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("ITERATION 0.13 ENDURING VALIDATION PASSED")
    print(f"- canonical public entries: {len(public_nodes)}")
    print(f"- developed profiles: {developed}")
    print(f"- sources: {len(sources)}")
    print(f"- journeys: {len(journeys)}")
    print(f"- typed edges: {len(data.get('edges', []))}")
    print(f"- AI observations regenerated: {len(observations)}")
    print("- Ivo Velitchkov and Patrick Hoverstadt framed through expertise and public work")
    print("- public interface contains no internal working routes or service-specific continuation prompts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
