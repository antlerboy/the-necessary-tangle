#!/usr/bin/env python3
"""Prepare the 0.8 seed, idempotent build wiring and release notes.

This is a one-shot release-construction helper. It reads the diagnostic ledgers
on the expansion branch and the mounted superseded branch, writes the durable
seed used by normal builds, then patches the earlier 0.7 build steps so they
remain valid after later growth.
"""
from __future__ import annotations

import json
import runpy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OLD_ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/oldwork")


def write_seed() -> None:
    ledger = json.loads((ROOT / "analysis" / "old-branch-candidate-ledger.json").read_text())
    authors = json.loads((ROOT / "analysis" / "fpcs-author-candidates.json").read_text())
    old_data = json.loads((OLD_ROOT / "data" / "public-data.json").read_text())
    papers = runpy.run_path(str(OLD_ROOT / "scripts" / "apply_research_iteration.py"))["FPCS_PAPERS"]

    relation_types_by_id = {
        item["relation_type"]: item for item in old_data.get("relation_types", [])
    }
    used_relation_types = sorted({
        edge.get("relation_type") for edge in ledger.get("edges", [])
        if edge.get("relation_type")
    })
    missing = [
        relation_type for relation_type in used_relation_types
        if relation_type not in relation_types_by_id
    ]
    if missing:
        raise SystemExit(f"Missing candidate relation-type records: {missing}")

    existing_author_ids = {
        item["label"]: item["existing_id"] for item in authors.get("existing", [])
    }
    if len(papers) != 89:
        raise SystemExit(f"Expected 89 official papers, found {len(papers)}")
    if len(authors.get("candidates", [])) != 107:
        raise SystemExit(
            f"Expected 107 new author candidates, found {len(authors.get('candidates', []))}"
        )
    if len(existing_author_ids) != 12:
        raise SystemExit(f"Expected 12 existing-author matches, found {len(existing_author_ids)}")

    seed = {
        "source_branch": "release-0.7-constellation-alpha",
        "warning": "Evidence-gated candidate seed only; the superseded branch itself is not merged.",
        "candidate_nodes": ledger.get("nodes", []),
        "candidate_edges": ledger.get("edges", []),
        "sources": ledger.get("sources", []),
        "relation_types": [
            relation_types_by_id[relation_type] for relation_type in used_relation_types
        ],
        "fpcs_papers": papers,
        "existing_author_ids": existing_author_ids,
        "expected_new_author_forms": [
            item["label"] for item in authors.get("candidates", [])
        ],
    }
    path = ROOT / "data" / "expansion-08-seed.json"
    path.write_text(json.dumps(seed, ensure_ascii=False, indent=2) + "\n")
    print(
        f"Seeded {len(seed['candidate_nodes'])} branch candidates, "
        f"{len(seed['candidate_edges'])} candidate edges, {len(papers)} papers and "
        f"{len(seed['expected_new_author_forms'])} new author forms."
    )


def patch_makefile() -> None:
    path = ROOT / "Makefile"
    text = path.read_text()
    if "\tpython3 scripts/apply_expansion_08.py\n" not in text:
        text = text.replace(
            "\tpython3 scripts/apply_constellation_07.py\n",
            "\tpython3 scripts/apply_constellation_07.py\n"
            "\tpython3 scripts/apply_expansion_08.py\n",
            1,
        )
    if "\tpython3 scripts/patch_expansion_08.py\n" not in text:
        text = text.replace(
            "\tpython3 scripts/patch_constellation_07.py\n",
            "\tpython3 scripts/patch_constellation_07.py\n"
            "\tpython3 scripts/patch_expansion_08.py\n",
            1,
        )
    if "\tpython3 scripts/validate_expansion_08.py\n" not in text:
        text = text.replace(
            "\tpython3 scripts/validate_constellation.py\n",
            "\tpython3 scripts/validate_constellation.py\n"
            "\tpython3 scripts/validate_expansion_08.py\n",
            1,
        )
    for required in (
        "scripts/apply_expansion_08.py",
        "scripts/patch_expansion_08.py",
        "scripts/validate_expansion_08.py",
    ):
        if required not in text:
            raise SystemExit(f"Could not wire {required} into Makefile")
    path.write_text(text)


def patch_release_overrides() -> None:
    path = ROOT / "scripts" / "apply_release_overrides.py"
    text = path.read_text()
    text = text.replace(
        'RELEASE = "0.7-constellation-alpha"',
        'RELEASE = "0.8-expansion-alpha"',
    )
    text = text.replace('GENERATED = "2026-08-09"', 'GENERATED = "2026-08-10"', 1)
    path.write_text(text)


def patch_constellation_builder() -> None:
    path = ROOT / "scripts" / "apply_constellation_07.py"
    text = path.read_text()
    old = """    expected = {
        \"public_node_count\": 204, \"substantive_edge_count\": 96, \"substantive_pair_count\": 94,
        \"connected_node_count\": 77, \"isolated_node_count\": 127, \"component_count\": 129,
        \"largest_component_node_count\": 75,
    }
    for k, v in expected.items():
        if data[\"graph_snapshot\"].get(k) != v:
            raise SystemExit(f\"Reconstructed 0.7 graph mismatch: {k}={data['graph_snapshot'].get(k)!r}, expected {v!r}\")
"""
    new = """    core_minimums = {
        \"public_node_count\": 204, \"substantive_edge_count\": 96,
        \"substantive_pair_count\": 94, \"connected_node_count\": 77,
        \"largest_component_node_count\": 75,
    }
    for key, minimum in core_minimums.items():
        if data[\"graph_snapshot\"].get(key, 0) < minimum:
            raise SystemExit(
                f\"Reconstructed 0.7 core regression: {key}={data['graph_snapshot'].get(key)!r}, minimum {minimum!r}\"
            )
"""
    if old in text:
        text = text.replace(old, new, 1)
    elif "core_minimums = {" not in text:
        raise SystemExit("Could not patch apply_constellation_07.py for later growth")
    path.write_text(text)


def patch_expansion_builder() -> None:
    path = ROOT / "scripts" / "apply_expansion_08.py"
    text = path.read_text()
    text = text.replace(
        "    author_ids: dict[str, str] = {}\n"
        "    new_author_ids: set[str] = set()\n",
        "    author_ids: dict[str, str] = {}\n"
        "    new_author_ids: set[str] = set()\n"
        "    expansion_author_ids: set[str] = set()\n",
        1,
    )
    text = text.replace(
        "        author_ids[author] = author_id\n\n"
        "    # Place new author entries near the papers with which the official inventory associates them.\n"
        "    new_author_labels = sorted(\n"
        "        (node_id, nodes[node_id][\"label\"]) for node_id in new_author_ids\n"
        "    )",
        "        author_ids[author] = author_id\n"
        "        if nodes.get(author_id, {}).get(\"inclusion_reason\") == \"official_collection_author_inventory\":\n"
        "            expansion_author_ids.add(author_id)\n\n"
        "    # Place expansion author entries near the papers with which the official inventory associates them.\n"
        "    new_author_labels = sorted(\n"
        "        (node_id, nodes[node_id][\"label\"]) for node_id in expansion_author_ids\n"
        "    )",
        1,
    )
    text = text.replace(
        "        \"new_bibliographic_people\": len(new_author_ids),\n"
        "        \"existing_people_reused\": len(set(author_ids.values()) - new_author_ids),\n"
        "        \"collection_volumes\": 4,\n"
        "        \"reviewed_branch_candidates\": len(imported_public_ids) - len(new_author_ids) - 4,",
        "        \"new_bibliographic_people\": len(expansion_author_ids),\n"
        "        \"existing_people_reused\": len(set(author_ids.values()) - expansion_author_ids),\n"
        "        \"collection_volumes\": 4,\n"
        "        \"reviewed_branch_candidates\": sum(\n"
        "            1 for candidate in candidate_nodes\n"
        "            if candidate.get(\"id\") != REDIRECTED_EVOLUTIONARY_ID\n"
        "        ),",
        1,
    )
    text = text.replace(
        'f"{len(papers)} papers and {len(new_author_ids)} new author records."',
        'f"{len(papers)} papers and {len(expansion_author_ids)} expansion author records."',
        1,
    )
    required = (
        "expansion_author_ids: set[str] = set()",
        '"new_bibliographic_people": len(expansion_author_ids)',
        "for node_id in expansion_author_ids",
    )
    if not all(marker in text for marker in required):
        raise SystemExit("Could not make apply_expansion_08.py idempotent")
    path.write_text(text)


def write_documentation() -> None:
    note = """# Release 0.8: bibliographic breadth and a map that moves

Release `0.8-expansion-alpha` adds 203 canonical public entries to the 204-entry 0.7 baseline, taking The Necessary Tangle to 407 entries.

The breadth comes from one bounded and inspectable source programme:

- 89 publications listed in the official *Foundational Papers in Complexity Science* table of contents;
- 107 authors not previously represented as public people in the atlas;
- four collection-volume records;
- three reviewed framing records recovered from the superseded 295-entry working branch.

The superseded branch was used as a candidate ledger, not merged. One duplicate evolutionary-cybernetics entry was redirected to the maintained tradition entry. Existing people were reused rather than duplicated.

## Depth and limits

These are bibliographic first-pass entries. A paper entry records its title, authors, year and collection placement. A newly added person entry records that the official collection lists that author for one or more papers. Neither is a finished intellectual profile. Collection inclusion is an editorial selection, not proof of correctness, importance or influence.

The new typed records include authorship, co-authorship and collection structure. They make the breadth navigable and give later concept, practice and lineage research named objects to connect. They do not manufacture conceptual relations from mere co-occurrence.

## Map behaviour

The home-page map action now opens the full public map. In that view, documentary authorship and collection-structure lines appear faintly alongside the substantive conceptual graph. Selecting an entry moves the map smoothly to it without discarding the whole-map context. Focused neighbourhood views retain their previous bearings as they re-form around a new selection.

## Curator notes

The running curator notebook remains reachable as a deliberately discreet dot link. It is an operational feedback surface, not part of the public site's main navigational hierarchy.
"""
    (ROOT / "documentation" / "expansion-08.md").write_text(note)

    changelog = ROOT / "CHANGELOG.md"
    text = changelog.read_text()
    entry = """## 0.8-expansion-alpha — 10 August 2026

- Added 203 canonical public entries: 89 Foundational Papers publications, 107 new bibliographic people, four collection volumes and three reviewed framing records.
- Reused 12 existing people and redirected the duplicate evolutionary-cybernetics candidate rather than inflating the count.
- Added typed authorship, co-authorship and collection-structure records.
- Made the home-page map action open the full public map and added adaptive movement on selection.
- Moved the curator running notebook to a discreet operational link.
- Added idempotent expansion and regression validation to the normal build.

"""
    if "## 0.8-expansion-alpha" not in text:
        first_break = text.find("\n\n")
        text = text[: first_break + 2] + entry + text[first_break + 2 :]
    changelog.write_text(text)

    coverage = ROOT / "documentation" / "coverage-programme.md"
    text = coverage.read_text()
    old = (
        "The collection must be treated item by item. The work is to inventory every included paper and editorial introduction, "
        "record publication details and public links, summarise each item, map the concepts and people it supports, and distinguish "
        "the collection editors' framing from the statements in the originals.\n\n"
        "Completion means a readable contents guide, item-level summaries and links, mapped relationships, and an explicit account "
        "of omissions and inaccessible originals. The collection is a major corpus, not a neutral or exhaustive canon."
    )
    new = (
        "Release 0.8 completes the first official-table-of-contents inventory: all 89 historical papers, 119 author forms "
        "(107 newly represented people and 12 reused existing entries), four collection volumes, and typed authorship and "
        "collection-structure records are now public.\n\n"
        "This is bibliographic breadth, not completion. The next work is to trace each paper to an original or authoritative public "
        "record where possible, distinguish the collection editors' framing from the originals, summarise each paper, map the "
        "concepts and arguments it supports, and record serious counter-accounts. The collection is a major corpus, not a neutral "
        "or exhaustive canon."
    )
    if old in text:
        text = text.replace(old, new, 1)
    coverage.write_text(text)


def main() -> None:
    write_seed()
    patch_makefile()
    patch_release_overrides()
    patch_constellation_builder()
    patch_expansion_builder()
    write_documentation()
    print("Prepared the reproducible 0.8 expansion release")


if __name__ == "__main__":
    main()
