#!/usr/bin/env python3
"""Validate release 0.18 navigability, source additions and coverage audits."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from apply_iteration_09 import graph_metrics
from apply_iteration_18 import GENERATED, NAMED_COVERAGE, RELEASE, UNFIX_CONCEPTS
from apply_relational_depth_16 import calculate_relational_depth

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "public-data.json"
VERSION = "0.18.0-public"

REQUIRED_SOURCES = {
    "src_linda_booth_sweeney_profile_2026",
    "src_massbook_noisy_puddle_award_2025",
    "src_linda_noisy_puddle_2026",
    "src_linda_do_bees_pee_2026",
    "src_unfix_32_key_concepts_2024",
    "src_tangle_issue2_post017_usability_2026",
}
REQUIRED_RELATIONS = {"includes_in_synthesis", "teaches_through", "illustrates", "introduces"}
REQUIRED_EDGES = {
    "e18_linda_authored_noisy_puddle",
    "e18_linda_authored_do_bees_pee",
    "e18_linda_teaches_through_noisy",
    "e18_noisy_interconnectedness",
    "e18_bees_circular_economy",
    "e18_appelo_authored_unfix32",
}
BANNED_STANDALONE_PATTERNS = {
    r"\bDamian\b(?!\s+Allen\b)": "isolated Damian reference",
    r"\bas requested\b": "hidden request context",
    r"\byou asked\b": "hidden request context",
    r"\byour prompt\b": "hidden prompt context",
    r"\bthe user asked\b": "hidden user context",
    r"\bthe user's prompt\b": "hidden user context",
}


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


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []
        self.buttons: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        values = dict(attrs)
        if tag == "a" and values.get("href"):
            self.links.append(values["href"])
        if tag == "button":
            self.buttons.append(values)


def canonical_id(data: dict, node_id: str) -> str:
    seen = set()
    redirects = data.get("canonical_redirects", {})
    current = node_id
    while current in redirects and current not in seen:
        seen.add(current)
        current = redirects[current]
    return current


def public_text_payload(data: dict) -> str:
    selected = {key: data.get(key) for key in ("nodes", "profiles", "journeys", "claims", "ai_observations")}
    pages = [
        read("docs/index.html"),
        read("docs/coverage/named/index.html"),
        read("docs/coverage/unfix-32/index.html"),
    ]
    return json.dumps(selected, ensure_ascii=False) + "\n" + "\n".join(pages)


def validate_static_links(data: dict, errors: list[str]) -> None:
    public_ids = {
        node.get("id")
        for node in data.get("nodes", [])
        if node.get("id") and node.get("public_visibility") == "public" and canonical_id(data, node.get("id")) == node.get("id")
    }
    for path in ("docs/index.html", "docs/coverage/named/index.html", "docs/coverage/unfix-32/index.html"):
        parser = LinkParser()
        parser.feed(read(path))
        for href in parser.links:
            if not href.startswith("#") and not href.startswith("/#"):
                continue
            fragment = href.split("#", 1)[1]
            params = parse_qs(fragment)
            if params.get("view", [""])[0] == "item":
                raw = params.get("id", [""])[0]
                resolved = canonical_id(data, raw)
                if resolved not in public_ids:
                    errors.append(f"broken internal item link in {path}: {href}")
        for button in parser.buttons:
            classes = set((button.get("class") or "").split())
            if classes & {"open-card", "surprise-me", "map-entry", "ask-entry", "contribute-entry"}:
                errors.append(f"navigational control remains a button in {path}: {sorted(classes)}")


def main() -> int:
    errors: list[str] = []
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    meta = data.get("meta", {})
    nodes = {node.get("id"): node for node in data.get("nodes", []) if node.get("id")}
    public_ids = {
        node_id for node_id, node in nodes.items()
        if node.get("public_visibility") == "public" and canonical_id(data, node_id) == node_id
    }
    sources = {source.get("id") for source in data.get("sources", []) if source.get("id")}
    relations = {item.get("relation_type") for item in data.get("relation_types", [])}
    edges = {edge.get("id"): edge for edge in data.get("edges", []) if edge.get("id")}
    profiles = {profile.get("node_id"): profile for profile in data.get("profiles", []) if profile.get("node_id")}

    if meta.get("release") != RELEASE:
        errors.append(f"meta.release must be {RELEASE}")
    if meta.get("generated") != GENERATED:
        errors.append(f"meta.generated must be {GENERATED}")
    if meta.get("map_interaction_contract") != "navigable-map-v2":
        errors.append("map interaction contract is missing")
    if meta.get("unfix_coverage_count") != 32:
        errors.append("unFIX coverage count must be 32")
    if meta.get("named_coverage_count") != len(NAMED_COVERAGE):
        errors.append("named coverage count is stale")

    missing_sources = REQUIRED_SOURCES - sources
    if missing_sources:
        errors.append(f"required 0.18 sources missing: {sorted(missing_sources)}")
    missing_relations = REQUIRED_RELATIONS - relations
    if missing_relations:
        errors.append(f"required 0.18 relation types missing: {sorted(missing_relations)}")
    missing_edges = REQUIRED_EDGES - set(edges)
    if missing_edges:
        errors.append(f"required 0.18 edges missing: {sorted(missing_edges)}")

    for edge_id in REQUIRED_EDGES & set(edges):
        edge = edges[edge_id]
        if canonical_id(data, edge.get("source")) not in public_ids or canonical_id(data, edge.get("target")) not in public_ids:
            errors.append(f"0.18 edge has non-public endpoint: {edge_id}")
        if edge.get("relation_type") not in relations:
            errors.append(f"0.18 edge uses an unregistered relation: {edge_id}")
        if not edge.get("plain_phrase") or not edge.get("scope_conditions") or not parse(edge.get("source_ids")):
            errors.append(f"0.18 edge is not inspectable: {edge_id}")

    for requested in ("person_linda_booth_sweeney", "publication_the_noisy_puddle", "publication_do_bees_pee", "publication_unfix_32_key_concepts"):
        resolved = canonical_id(data, requested)
        if resolved not in public_ids:
            errors.append(f"required public entry missing: {requested}")
        if requested != "publication_unfix_32_key_concepts" and resolved not in profiles:
            errors.append(f"required 0.18 profile missing: {requested}")

    unfix = data.get("unfix_32_coverage", {})
    items = unfix.get("items", [])
    if unfix.get("release") != RELEASE or len(items) != len(UNFIX_CONCEPTS) or len(items) != 32:
        errors.append("unFIX 32 coverage object is incomplete or stale")
    expected_labels = {label for label, _, _ in UNFIX_CONCEPTS}
    if {item.get("concept") for item in items} != expected_labels:
        errors.append("unFIX concept labels do not match the maintained 32-item set")
    for item in items:
        if canonical_id(data, item.get("node_id")) not in public_ids:
            errors.append(f"unFIX item does not resolve publicly: {item.get('concept')}")
        edge_id = f"e18_unfix32_{re.sub(r'[^a-z0-9]+', '_', item.get('concept', '').casefold()).strip('_')}"
        if edge_id not in edges:
            errors.append(f"unFIX documentary edge missing: {edge_id}")

    named = data.get("named_coverage_review", {})
    named_items = named.get("items", [])
    if named.get("release") != RELEASE or len(named_items) != len(NAMED_COVERAGE):
        errors.append("named coverage review is incomplete or stale")
    expected_names = {label for label, _ in NAMED_COVERAGE}
    if {item.get("name") for item in named_items} != expected_names:
        errors.append("named coverage review does not match the requested names")
    for item in named_items:
        resolved = canonical_id(data, item.get("node_id"))
        if resolved not in public_ids:
            errors.append(f"named item does not resolve publicly: {item.get('name')}")
        node = nodes.get(resolved)
        aliases = {value.casefold() for value in parse(node.get("aliases"), [])} if node else set()
        expected_aliases = next((aliases for label, aliases in NAMED_COVERAGE if label == item.get("name")), [])
        for alias in expected_aliases:
            if alias.casefold() not in aliases and alias.casefold() != str(node.get("label", "")).casefold():
                errors.append(f"search alias missing for {item.get('name')}: {alias}")

    for alias, label in (("Donna Meadows", "Donella H. Meadows"), ("Russ Ackoff", "Russell L. Ackoff"), ("Alasdair MacInyre", "Alasdair MacIntyre"), ("Luhann", "Niklas Luhmann"), ("Rapaport", "Anatol Rapoport"), ("Barabasi", "Albert-László Barabási")):
        item = next((row for row in named_items if row.get("name") == label), None)
        if not item:
            errors.append(f"alias test target missing: {label}")
            continue
        node = nodes.get(canonical_id(data, item.get("node_id")))
        if alias.casefold() not in {value.casefold() for value in parse(node.get("aliases"), [])}:
            errors.append(f"required alias missing: {alias}")

    recalculated = calculate_relational_depth(data)
    if data.get("relational_depth") != recalculated:
        errors.append("relational-depth measures are stale after 0.18")
    metrics = graph_metrics(data)
    if meta.get("public_entry_count") != metrics.get("public_entries"):
        errors.append("public entry count is stale")
    if meta.get("profile_count") != len(profiles):
        errors.append("profile count is stale")
    if meta.get("source_count") != len(data.get("sources", [])):
        errors.append("source count is stale")

    docs_json = json.loads(read("docs/assets/public-data.json"))
    if docs_json != data:
        errors.append("browser public-data JSON differs from canonical data")
    if json.loads(read("docs/assets/unfix-32-coverage.json")) != unfix:
        errors.append("unFIX coverage asset differs from canonical projection")
    if json.loads(read("docs/assets/named-coverage-review.json")) != named:
        errors.append("named coverage asset differs from canonical projection")

    index = read("docs/index.html")
    app = read("docs/assets/app.js")
    release_js = read("docs/assets/iteration-18.js")
    release_css = read("docs/assets/iteration-18.css")
    for marker in (
        f"assets/iteration-18.css?v={VERSION}",
        f"assets/iteration-18.js?v={VERSION}",
        "It’s the connections which are perhaps the most important.",
        "Find out more about how this works.",
        'value="constellation"',
        'class="brand-mark tangle-mark"',
        'href="/coverage/named/"',
        'href="/coverage/unfix-32/"',
        '<a href="#view=item&id=concept_viability&from=surprise" id="surpriseMeNav"',
    ):
        if marker not in index:
            errors.append(f"0.18 reader marker missing: {marker}")
    for marker in (
        "let mapPointerDragged = false",
        "mode === 'constellation' ? 2",
        "class=\"graph-node-link\"",
        "class=\"graph-edge-link\"",
        "event.button !== 0 || event.metaKey",
        "mapPointerDragged = true",
        "/* 0.18 navigable map and link contract */",
    ):
        if marker not in app:
            errors.append(f"base application 0.18 patch missing: {marker}")
    for marker in ("chooseSurprise", "entry-orientation", "connections-priority", "data-orbit", "contextmenu"):
        if marker not in release_js:
            errors.append(f"iteration-18.js behaviour missing: {marker}")
    for marker in ("width: 100vw", "min-height: min(76dvh, 920px)", ".map-layout", ".tangle-mark", ".coverage-table"):
        if marker not in release_css:
            errors.append(f"iteration-18.css rule missing: {marker}")

    for script in ("docs/assets/app.js", "docs/assets/iteration-17.js", "docs/assets/iteration-18.js"):
        try:
            subprocess.run(["node", "--check", str(ROOT / script)], check=True, capture_output=True, text=True)
        except FileNotFoundError:
            errors.append("node is unavailable for JavaScript syntax checks")
            break
        except subprocess.CalledProcessError as exc:
            errors.append(f"JavaScript does not parse ({script}): {exc.stderr.strip()}")

    validate_static_links(data, errors)

    payload = public_text_payload(data)
    for pattern, label in BANNED_STANDALONE_PATTERNS.items():
        match = re.search(pattern, payload, flags=re.IGNORECASE)
        if match:
            errors.append(f"public output contains {label}: {match.group(0)!r}")
    if "Damian Allen Allen" in payload:
        errors.append("public output contains duplicated Damian Allen name")

    required_docs = {
        "documentation/iteration-18-usability-and-coverage.md": ["navigable tangle", "Acceptance checks", "Deliberate limits"],
        "documentation/named-practitioner-coverage.md": ["Named practitioner and institution coverage", "Research queue"],
        "documentation/unfix-32-coverage.md": ["unFIX 32-concept coverage", "Comparator"],
        "documentation/ai-observations.md": [RELEASE, "Navigation changes what appears important", "Links are commitments about possible movement"],
        "documentation/DESIGN_AND_CONTENT_RULES.md": ["Navigational link contract", "Public prose must stand alone"],
        "documentation/feedback-ledger.md": ["Release 0.18 — navigability, standalone prose and named coverage"],
        "documentation/TANGLE_STATE.md": [RELEASE, "unFIX comparator concepts resolved"],
        "documentation/NEXT_WORK.md": ["release 0.18 is complete", "No production change is authorised"],
    }
    for path, markers in required_docs.items():
        target = ROOT / path
        if not target.exists():
            errors.append(f"required 0.18 document missing: {path}")
            continue
        text = target.read_text(encoding="utf-8")
        for marker in markers:
            if marker not in text:
                errors.append(f"{path} missing marker: {marker}")

    citation = read("CITATION.cff")
    changelog = read("CHANGELOG.md")
    readme = read("README.md")
    if f"version: {RELEASE}" not in citation or f"date-released: {GENERATED}" not in citation:
        errors.append("citation metadata does not identify release 0.18")
    if f"## {RELEASE} — 23 August 2026" not in changelog:
        errors.append("0.18 changelog entry is missing")
    if "## Release 0.18" not in readme or "coverage/named/" not in readme or "coverage/unfix-32/" not in readme:
        errors.append("README does not identify the 0.18 release and coverage routes")

    if errors:
        print("Release 0.18 validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(
        f"Release 0.18 validated: {meta.get('public_entry_count')} public entries, "
        f"{meta.get('profile_count')} profiles, 32 unFIX concepts and {len(named_items)} named coverage items."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
