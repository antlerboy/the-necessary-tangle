#!/usr/bin/env python3
"""Validate the public repository and GitHub Pages build."""
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "public-data.json"
DOCS = ROOT / "docs"

PROJECT = "The Necessary Tangle"
REPOSITORY_URL = "https://github.com/antlerboy/the-necessary-tangle"
PROJECT_URL = "https://antlerboy.github.io/the-necessary-tangle/"
AUTHOR_URL = "https://www.antlerboy.com/"
BAD_NAME_RE = re.compile(r"(?<!Necessary )\bThe Tangle\b")
PRIVATE_PATTERNS = (
    "sharepoint", "graph.microsoft", "mail.google", "gmail", "sandbox:/",
    "file://", "localhost", "127.0.0.1", "/mnt/data", "redquadrantltd.sharepoint",
)
ALIAS_STOPWORDS = {
    "a", "an", "and", "approach", "analysis", "concept", "evidence", "intervention",
    "law", "method", "methodology", "model", "of", "or", "person", "practice", "principle",
    "skill", "system", "systems", "technology", "the", "theory", "tool", "tradition",
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


def norm(value: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", value.casefold())).strip()


def main() -> int:
    errors: list[str] = []
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    meta = data.get("meta", {})
    redirects = data.get("canonical_redirects", {})
    canonical = lambda node_id: redirects.get(node_id, node_id)

    if meta.get("project") != PROJECT:
        errors.append(f"meta.project must be exactly {PROJECT!r}")
    if meta.get("repository_url") != REPOSITORY_URL:
        errors.append("meta.repository_url is not the canonical public repository")
    if meta.get("project_url") != PROJECT_URL:
        errors.append("meta.project_url is not the canonical public site")
    if meta.get("author_role") != "curator":
        errors.append("meta.author_role must be curator")
    if meta.get("author_url") != AUTHOR_URL:
        errors.append("meta.author_url must point to antlerboy.com")
    if meta.get("content_licence") != "CC BY-SA 4.0":
        errors.append("meta.content_licence must be CC BY-SA 4.0")
    if "systems | cybernetics | complexity" not in meta.get("subtitle", ""):
        errors.append("meta.subtitle must use systems | cybernetics | complexity")

    nodes = data.get("nodes", [])
    node_ids = {node["id"] for node in nodes}
    public_nodes = [
        node for node in nodes
        if node.get("public_visibility") == "public" and canonical(node["id"]) == node["id"]
    ]
    public_ids = {node["id"] for node in public_nodes}
    sources = {source["id"]: source for source in data.get("sources", [])}
    evidence_ids = {item["id"] for item in data.get("evidence", [])}
    relation_types = {item["relation_type"] for item in data.get("relation_types", [])}

    if len(public_nodes) != meta.get("public_entry_count"):
        errors.append("meta.public_entry_count does not match canonical public nodes")

    labels: defaultdict[str, list[str]] = defaultdict(list)
    aliases: defaultdict[str, set[str]] = defaultdict(set)
    for node in public_nodes:
        definition = node.get("canonical_definition") or node.get("description") or node.get("public_stub_text")
        if not definition or len(str(definition).split()) < 12:
            errors.append(f"Public entry lacks a usable description: {node['id']}")
        labels[norm(node["label"])].append(node["id"])
        for alias in parse(node.get("aliases")):
            alias_norm = norm(alias)
            if alias_norm in ALIAS_STOPWORDS:
                errors.append(f"Generic alias on {node['id']}: {alias!r}")
            if len(alias_norm) < 3:
                errors.append(f"Alias too short on {node['id']}: {alias!r}")
            aliases[alias_norm].add(node["id"])
        for source_id in parse(node.get("source_ids")):
            if source_id not in sources:
                errors.append(f"Unknown source {source_id} on {node['id']}")

    for key, ids in labels.items():
        if len(ids) > 1:
            errors.append(f"Duplicate canonical public label {key!r}: {ids}")
    for key, ids in aliases.items():
        if key and len(ids) > 1:
            errors.append(f"Alias resolves to multiple public entries {key!r}: {sorted(ids)}")

    for source in sources.values():
        url = str(source.get("url") or "")
        lower = url.casefold()
        if url and not re.match(r"^https?://", url):
            errors.append(f"Non-public URL scheme in source {source['id']}: {url}")
        if any(pattern in lower for pattern in PRIVATE_PATTERNS):
            errors.append(f"Private-looking URL in source {source['id']}: {url}")

    for edge in data.get("edges", []):
        if edge.get("source") not in node_ids or edge.get("target") not in node_ids:
            errors.append(f"Edge has unknown endpoint: {edge['id']}")
        if edge.get("relation_type") not in relation_types:
            errors.append(f"Edge has unknown relation type: {edge['id']} -> {edge.get('relation_type')}")
        for source_id in parse(edge.get("source_ids")):
            if source_id not in sources:
                errors.append(f"Unknown source {source_id} on edge {edge['id']}")
        for evidence_id in parse(edge.get("evidence_ids")):
            if evidence_id not in evidence_ids:
                errors.append(f"Unknown evidence {evidence_id} on edge {edge['id']}")

    for profile in data.get("profiles", []):
        if profile.get("node_id") not in public_ids:
            errors.append(f"Profile does not point to canonical public entry: {profile.get('node_id')}")
        for source_id in parse(profile.get("source_ids")):
            if source_id not in sources:
                errors.append(f"Unknown profile source {source_id}: {profile.get('node_id')}")

    for journey in data.get("journeys", []):
        for step in journey.get("steps", []):
            step_id = canonical(step.get("node_id"))
            if step_id not in public_ids:
                errors.append(f"Journey {journey['id']} refers to non-public entry {step.get('node_id')}")

    corpus_register = data.get("corpus_register", [])
    if len(corpus_register) < 6:
        errors.append("Expected at least six named corpus or coverage programmes")
    for corpus in corpus_register:
        if not corpus.get("label") or not corpus.get("status") or not corpus.get("issue_url"):
            errors.append(f"Incomplete corpus register item: {corpus.get('id')}")
        for source_id in corpus.get("source_ids", []):
            if source_id not in sources:
                errors.append(f"Unknown corpus source {source_id}: {corpus.get('id')}")

    docs_json = json.loads((DOCS / "assets" / "public-data.json").read_text(encoding="utf-8"))
    if docs_json != data:
        errors.append("docs/assets/public-data.json does not match data/public-data.json")
    js_text = (DOCS / "assets" / "public-data.js").read_text(encoding="utf-8").strip()
    prefix = "window.TANGLE_DATA = "
    if not js_text.startswith(prefix) or not js_text.endswith(";"):
        errors.append("docs/assets/public-data.js has an unexpected wrapper")
    else:
        try:
            js_data = json.loads(js_text[len(prefix):-1])
            if js_data != data:
                errors.append("docs/assets/public-data.js does not match data/public-data.json")
        except json.JSONDecodeError as exc:
            errors.append(f"docs/assets/public-data.js contains invalid JSON: {exc}")

    public_text_files = [
        *DOCS.rglob("*.html"),
        *DOCS.rglob("*.js"),
        *DOCS.rglob("*.css"),
        *DOCS.rglob("*.txt"),
        ROOT / "README.md",
        ROOT / "CONTRIBUTING.md",
        ROOT / "GOVERNANCE.md",
        ROOT / "RIGHTS.md",
        ROOT / "ACKNOWLEDGEMENTS.md",
        ROOT / "LICENSE-CONTENT.md",
        *list((ROOT / "documentation").glob("*.md")),
    ]
    for path in public_text_files:
        if not path.exists() or path.name.startswith("public-data"):
            continue
        text = path.read_text(encoding="utf-8")
        if BAD_NAME_RE.search(text):
            errors.append(f"Shortened public name found in {path.relative_to(ROOT)}")
        if "antlerboy-benjamintaylor" in text:
            errors.append(f"Obsolete GitHub owner found in {path.relative_to(ROOT)}")
        if path.is_relative_to(DOCS):
            if "Netlify" in text:
                errors.append(f"Obsolete Netlify reference found in {path.relative_to(ROOT)}")
            lower = text.casefold()
            if any(pattern in lower for pattern in PRIVATE_PATTERNS):
                errors.append(f"Private path or URL found in {path.relative_to(ROOT)}")

    index = (DOCS / "index.html").read_text(encoding="utf-8")
    required_ids = [
        "heroSearch", "browseCards", "journeyRunner", "graphSvg", "graphNodes",
        "askForm", "contributionForm", "entryDrawer", "drawerBody",
    ]
    for element_id in required_ids:
        if f'id="{element_id}"' not in index:
            errors.append(f"Public page is missing required element #{element_id}")
    if '<title>The Necessary Tangle</title>' not in index:
        errors.append("HTML title does not use the exact public name")
    if "Curated by" not in index or AUTHOR_URL not in index:
        errors.append("Public page does not identify and link the curator")
    if "systems | cybernetics | complexity" not in index:
        errors.append("Public page does not use the agreed field framing")
    if "Creative Commons Attribution-ShareAlike 4.0" not in index:
        errors.append("Public page does not expose the content licence")
    if 'class="hero-panel release-panel"' not in index:
        errors.append("This release panel is not an explicit link")

    enhancements_css = (DOCS / "assets" / "site-enhancements.css").read_text(encoding="utf-8")
    if "text-align: left" not in enhancements_css:
        errors.append("Left-aligned public text override is missing")
    enhancements_js = (DOCS / "assets" / "site-enhancements.js").read_text(encoding="utf-8")
    if "card.is-clickable" not in enhancements_js:
        errors.append("Whole-card click enhancement is missing")

    law_entries = [node for node in public_nodes if node.get("entity_type") == "law_or_principle"]
    if len(law_entries) < 33:
        errors.append(f"Expected at least 33 law or principle entries, found {len(law_entries)}")
    for node in law_entries:
        if re.search(r"Grammar of Systems item\s+\d+", node.get("description", ""), re.I):
            errors.append(f"Placeholder Grammar description remains: {node['id']}")

    if errors:
        print("PUBLIC VALIDATION FAILED", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        "PUBLIC VALIDATION PASSED\n"
        f"- exact public name: {PROJECT}\n"
        f"- canonical public entries: {len(public_nodes)}\n"
        f"- developed profiles: {len(data.get('profiles', []))}\n"
        f"- sources: {len(sources)} ({sum(bool(s.get('url')) for s in sources.values())} with public links)\n"
        f"- named coverage programmes: {len(corpus_register)}\n"
        f"- edges checked: {len(data.get('edges', []))}\n"
        f"- guided journeys checked: {len(data.get('journeys', []))}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
