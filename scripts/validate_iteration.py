#!/usr/bin/env python3
"""Validate release-specific work introduced in 0.7-constellations-alpha."""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "public-data.json"
DOCS = ROOT / "docs"

RELEASE = "0.7-constellations-alpha"
FPCS_TOC = "https://www.foundationalpapersincomplexityscience.org/tables-of-contents"
PRINCIPIA = "https://pespmc1.vub.ac.be/"


def parse(value):
    if isinstance(value, (list, dict)):
        return value
    if not value:
        return []
    try:
        return json.loads(value)
    except (TypeError, json.JSONDecodeError):
        return []


def main() -> int:
    errors: list[str] = []
    data = json.loads(DATA.read_text(encoding="utf-8"))
    meta = data.get("meta", {})

    if meta.get("release") != RELEASE:
        errors.append(f"Expected release {RELEASE}, found {meta.get('release')!r}")
    if meta.get("author_role") != "curator":
        errors.append("The public role must be curator")

    for collection in ("nodes", "edges", "sources"):
        ids = [item.get("id") for item in data.get(collection, [])]
        duplicates = [key for key, count in Counter(ids).items() if key and count > 1]
        if duplicates:
            errors.append(f"Duplicate {collection} ids: {duplicates[:8]}")

    source_by_id = {item["id"]: item for item in data.get("sources", [])}
    node_by_id = {item["id"]: item for item in data.get("nodes", [])}
    edge_by_id = {item["id"]: item for item in data.get("edges", [])}

    papers = data.get("foundational_papers", [])
    if len(papers) != 89:
        errors.append(f"Expected 89 foundational papers, found {len(papers)}")
    if sorted(item.get("number") for item in papers) != list(range(1, 90)):
        errors.append("Foundational paper numbers must be unique and complete from 1 to 89")
    if sorted({item.get("volume") for item in papers}) != [1, 2, 3, 4]:
        errors.append("Foundational papers must cover all four volumes")
    for paper in papers:
        node = node_by_id.get(paper.get("node_id"))
        if not node or node.get("entity_type") != "publication":
            errors.append(f"Paper {paper.get('number')} has no publication node")
        edge_id = f"e_fpcs_part_{paper.get('number', 0):03d}"
        if edge_id not in edge_by_id:
            errors.append(f"Paper {paper.get('number')} has no collection edge")
    fpcs_source = source_by_id.get("src_fpcs_official_toc")
    if not fpcs_source or fpcs_source.get("url") != FPCS_TOC:
        errors.append("The official Foundational Papers contents source is missing")
    if "src_foundational_papers_complexity_science" in source_by_id:
        errors.append("The obsolete Foundational Papers PDF registration remains")

    principia_ids = {
        "organisation_principia_cybernetica_project",
        "publication_principia_cybernetica_web",
        "comparator_corpus_principia_cybernetica_web_dictionary",
        "concept_evolutionary_cybernetics",
        "concept_metasystem_transition",
        "approach_family_metasystem_transition_theory",
        "concept_global_brain",
        "person_francis_heylighen",
        "person_valentin_turchin",
        "person_cliff_joslyn",
    }
    missing_principia = sorted(principia_ids - node_by_id.keys())
    if missing_principia:
        errors.append(f"Missing Principia first-pass nodes: {missing_principia}")
    if source_by_id.get("src_principia_home", {}).get("url") != PRINCIPIA:
        errors.append("Official Principia project source is missing")
    principia_edges = [edge for edge in data.get("edges", []) if edge.get("id", "").startswith("e_principia_")]
    if len(principia_edges) < 12:
        errors.append(f"Expected a connected Principia first pass, found {len(principia_edges)} edges")

    register = data.get("canonical_source_register", [])
    if len(register) < 12:
        errors.append(f"Expected at least 12 canonical source records, found {len(register)}")
    for item in register:
        if item.get("source_id") not in source_by_id:
            errors.append(f"Canonical register references unknown source {item.get('source_id')}")
        for key in ("category", "scope", "good_for", "not_enough_for"):
            if not item.get(key):
                errors.append(f"Canonical source item {item.get('source_id')} lacks {key}")

    observed = data.get("emergent_neighbourhoods", {})
    neighbourhoods = observed.get("neighbourhoods", [])
    if len(neighbourhoods) < 6:
        errors.append(f"Expected at least six observed neighbourhoods, found {len(neighbourhoods)}")
    if observed.get("isolated_entry_count", 0) < 1:
        errors.append("The neighbourhood diagnostic must report isolated entries")
    seen_nodes: set[str] = set()
    for neighbourhood in neighbourhoods:
        if not neighbourhood.get("label") or not neighbourhood.get("node_ids"):
            errors.append(f"Incomplete neighbourhood {neighbourhood.get('id')}")
        overlap = seen_nodes.intersection(neighbourhood.get("node_ids", []))
        if overlap:
            errors.append(f"Nodes occur in more than one named neighbourhood: {sorted(overlap)[:8]}")
        seen_nodes.update(neighbourhood.get("node_ids", []))

    corpus_ids = {item.get("id") for item in data.get("corpus_register", [])}
    for expected in ("corpus_foundational_complexity_papers", "corpus_principia_cybernetica", "corpus_canonical_public_sources"):
        if expected not in corpus_ids:
            errors.append(f"Missing coverage register item {expected}")

    docs_data = json.loads((DOCS / "assets" / "public-data.json").read_text(encoding="utf-8"))
    if docs_data != data:
        errors.append("docs/assets/public-data.json does not match canonical data")

    index = (DOCS / "index.html").read_text(encoding="utf-8")
    required_ids = (
        "view-collections", "neighbourhoodCards", "paperCards", "principiaCards",
        "canonicalSourceCards", "view-membership", "membershipForm", "mapLayer",
        "mapLabels", "mapColour", "mapZoomOut", "mapZoomIn", "mapEdgeCount",
    )
    for element_id in required_ids:
        if f'id="{element_id}"' not in index:
            errors.append(f"Public page lacks #{element_id}")
    if "issues/2" not in index or "curator-notebook-link" not in index:
        errors.append("The curator's notebook affordance is missing")

    public_files = [
        ROOT / "README.md", ROOT / "GOVERNANCE.md", ROOT / "CONTRIBUTING.md",
        ROOT / "AGENTS.md", DOCS / "index.html", DOCS / "assets" / "app.js",
        *list((ROOT / "documentation").glob("*.md")),
    ]
    obsolete_role_patterns = (
        r"Created and edited by Benjamin",
        r"Creator and editor",
        r"Founding editor",
        r"Benjamin P Taylor is the creator",
    )
    for path in public_files:
        if not path.exists():
            errors.append(f"Expected public file missing: {path.relative_to(ROOT)}")
            continue
        text = path.read_text(encoding="utf-8")
        for pattern in obsolete_role_patterns:
            if re.search(pattern, text, re.I):
                errors.append(f"Obsolete role wording in {path.relative_to(ROOT)}: {pattern}")

    app = (DOCS / "assets" / "app.js").read_text(encoding="utf-8")
    for marker in ("currentMapLayer", "mapEdgeAllowed", "zoomMapAt", "renderCollections", "initMembership"):
        if marker not in app:
            errors.append(f"Application is missing {marker}")
    if "event.clientX" not in app or "event.clientY" not in app:
        errors.append("Wheel zoom is not pointer-centred")

    for path in (
        ROOT / "AGENTS.md",
        ROOT / "documentation" / "participation-and-access.md",
        ROOT / "documentation" / "emergent-neighbourhoods.md",
        ROOT / "documentation" / "canonical-source-register.md",
        ROOT / ".github" / "ISSUE_TEMPLATE" / "06-membership.yml",
    ):
        if not path.exists():
            errors.append(f"Missing iteration document: {path.relative_to(ROOT)}")

    if errors:
        print("ITERATION VALIDATION FAILED", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        "ITERATION VALIDATION PASSED\n"
        f"- release: {RELEASE}\n"
        f"- public entries: {meta.get('public_entry_count')}\n"
        f"- foundational papers: {len(papers)}\n"
        f"- Principia edges: {len(principia_edges)}\n"
        f"- canonical sources: {len(register)}\n"
        f"- named neighbourhoods: {len(neighbourhoods)}\n"
        f"- isolated analytic entries: {observed.get('isolated_entry_count')}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
