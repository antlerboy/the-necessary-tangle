#!/usr/bin/env python3
"""Validate that 0.20.5 is one coherent public release state."""
from __future__ import annotations

import json
from pathlib import Path

from apply_release_205 import GENERATED, RELEASE

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_OBSERVATIONS = {
    "release_metadata_is_part_of_the_evidence",
    "interface_accumulation_is_a_system_effect",
    "display_layers_can_manufacture_isolation",
    "a_live_corpus_is_not_ingested_coverage",
    "linking_a_source_graph_is_not_canonising_it",
}


def main() -> int:
    errors: list[str] = []
    canonical = json.loads((ROOT / "data/public-data.json").read_text(encoding="utf-8"))
    browser = json.loads((ROOT / "docs/assets/public-data.json").read_text(encoding="utf-8"))
    meta = canonical.get("meta", {})
    observations = canonical.get("ai_observations", {})

    if meta.get("release") != RELEASE or meta.get("generated") != GENERATED:
        errors.append(f"canonical metadata is not {RELEASE} / {GENERATED}")
    if browser != canonical:
        errors.append("browser JSON differs from canonical data after 0.20.5")
    if observations.get("release") != RELEASE or observations.get("generated") != GENERATED:
        errors.append("AI observation report does not name the current release")

    observation_ids = {item.get("id") for item in observations.get("observations", [])}
    missing = REQUIRED_OBSERVATIONS - observation_ids
    if missing:
        errors.append(f"0.20.5 AI observations missing: {sorted(missing)}")

    citation = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    if f"version: {RELEASE}" not in citation or f"date-released: {GENERATED}" not in citation:
        errors.append("CITATION.cff is not aligned with 0.20.5")

    ai_doc = (ROOT / "documentation/ai-observations.md").read_text(encoding="utf-8")
    for marker in (
        f"Generated for release `{RELEASE}` on {GENERATED}.",
        "Release metadata is part of the evidence",
        "Interface clutter is an accumulation effect",
        "A display layer can manufacture an isolate",
        "A live corpus is not ingested coverage",
        "Linking a source graph is not canonising it",
    ):
        if marker not in ai_doc:
            errors.append(f"AI documentation missing: {marker}")

    index = (ROOT / "docs/index.html").read_text(encoding="utf-8")
    for marker in (
        '<div class="brand-stack">',
        '<span id="releaseBadge">Release 0.20.5</span>',
        'assets/iteration-20.js?v=0.20.5-header',
        '<strong>Updated for 0.20.5:</strong>',
    ):
        if marker not in index:
            errors.append(f"reader HTML missing: {marker}")

    header_js = (ROOT / "docs/assets/iteration-20.js").read_text(encoding="utf-8")
    for marker in (
        "grid-template-columns: minmax(0, 1fr) auto",
        ".brand-mark:not(:fullscreen)",
        ".site-header > .header-meta span:first-child",
        "border: 0;",
    ):
        if marker not in header_js:
            errors.append(f"header composition rule missing: {marker}")

    if errors:
        print("Release 0.20.5 validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        f"Validated {RELEASE}: release metadata, citation, AI observations and compact header are aligned"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
