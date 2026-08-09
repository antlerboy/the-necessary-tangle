#!/usr/bin/env python3
"""Generate a public-only knowledge file for conversational use."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "public-data.json"
OUTPUT_PATH = ROOT / "documentation" / "public-knowledge-for-chatgpt.md"


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


def label(value: str) -> str:
    return value.replace("_", " ").strip().capitalize()


def main() -> None:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    meta = data.get("meta", {})
    redirects = data.get("canonical_redirects", {})
    canonical = lambda node_id: redirects.get(node_id, node_id)
    sources = {source["id"]: source for source in data.get("sources", [])}
    profiles = {profile["node_id"]: profile for profile in data.get("profiles", [])}
    nodes = [
        node for node in data.get("nodes", [])
        if node.get("public_visibility") == "public" and canonical(node["id"]) == node["id"]
    ]
    nodes.sort(key=lambda node: node["label"].casefold())

    author = meta.get("author", "Benjamin P Taylor")
    author_url = meta.get("author_url", "https://www.antlerboy.com/")
    subtitle = meta.get("subtitle", "A living evidence atlas of systems | cybernetics | complexity")

    lines = [
        "# The Necessary Tangle: public knowledge file",
        "",
        f"Curated by {author} — {author_url}",
        f"Generated from public release {meta.get('release', 'not stated')}.",
        "",
        subtitle + ".",
        "Every connection must say what it means. Historical sequence, logical dependence, influence, teaching, collaboration, practical use, comparison and dispute are not interchangeable.",
        "",
        "Use this file as orientation and public source context, not as final scholarly consensus. Preserve the stated status and uncertainty of statements. Do not infer influence, mentorship or priority from resemblance alone.",
        "",
        "## Public source policy",
        "",
        "Every URL in this file is public. Published books and archive items without an open web copy are marked ‘No public link’. Private email, internal documents and company-system URLs are not included.",
        "",
    ]

    for node in nodes:
        profile = profiles.get(node["id"])
        definition = (
            (profile or {}).get("canonical_definition")
            or node.get("canonical_definition")
            or node.get("description")
            or node.get("public_stub_text")
            or "No public description yet."
        )
        lines.extend([
            f"## {node['label']}",
            "",
            f"Type: {label(node.get('entity_type', 'entry'))}",
            f"Public depth: {node.get('publication_level', 'not stated').replace('_', ' ')}",
            "",
            definition.strip(),
            "",
        ])

        if profile:
            fields = [
                ("Summary", "summary"),
                ("Why it matters", "why_it_matters"),
                ("Key distinctions", "key_distinctions"),
                ("Historical development", "historical_lineage"),
                ("Ideas it depends on", "logical_antecedents"),
                ("What develops from it", "dependent_subsequents"),
                ("Connections to practice", "practice_connections"),
                ("Common confusions", "common_misreadings"),
                ("Open questions and checks", "open_checks"),
            ]
            for heading, key in fields:
                value = profile.get(key)
                if not value:
                    continue
                parsed = parse(value)
                lines.extend([f"### {heading}", ""])
                if isinstance(parsed, list) and parsed:
                    lines.extend([f"- {item}" for item in parsed])
                else:
                    lines.append(str(value).strip())
                lines.append("")

        source_ids = []
        for source_id in parse(node.get("source_ids")) + parse((profile or {}).get("source_ids")):
            if source_id not in source_ids:
                source_ids.append(source_id)
        if source_ids:
            lines.extend(["### Sources", ""])
            for source_id in source_ids:
                source = sources.get(source_id)
                if not source:
                    continue
                target = source.get("url") or "No public link"
                lines.append(f"- {source['title']} — {target}")
            lines.append("")

    corpus_register = data.get("corpus_register", [])
    if corpus_register:
        lines.extend([
            "# Registered coverage programmes",
            "",
            "These are explicit next-work programmes, not claims that the corpora have already been fully reviewed or ingested.",
            "",
        ])
        for corpus in corpus_register:
            lines.extend([
                f"## {corpus.get('label', corpus.get('id', 'Coverage programme'))}",
                "",
                f"Status: {corpus.get('status', 'not stated').replace('_', ' ')}",
                f"Tracking issue: {corpus.get('issue_url', 'not stated')}",
                f"Completion test: {corpus.get('completion_test', 'not stated')}",
                "",
            ])

    OUTPUT_PATH.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH.relative_to(ROOT)} with {len(nodes)} public entries.")


if __name__ == "__main__":
    main()
