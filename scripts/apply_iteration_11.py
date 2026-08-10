#!/usr/bin/env python3
"""Apply release 0.11: whole-to-detail map navigation and curator comment access."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "public-data.json"
RELEASE = "0.11-visual-map-alpha"
GENERATED = "2026-08-10"


def main() -> None:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    meta = data.setdefault("meta", {})
    meta["release"] = RELEASE
    meta["generated"] = GENERATED

    report = data.get("ai_observations")
    if isinstance(report, dict):
        report["release"] = RELEASE

    data["map_experience"] = {
        "release": RELEASE,
        "model": "whole-to-detail conceptual navigation",
        "principles": [
            "Preserve orientation while moving between the whole graph, a neighbourhood and a selected entry.",
            "Make zoom change the amount of visible detail rather than merely making the same clutter larger.",
            "Keep relation type, evidence and uncertainty inspectable from the same map.",
            "Use a minimap, navigation history and fit controls to reduce getting lost.",
            "Retain keyboard, pointer, touch and reduced-motion routes through the same public graph.",
        ],
        "inspiration": {
            "label": "Visual Meaning Shared Meaning Platform",
            "url": "https://visual-meaning.com/our-platform/",
            "note": "Interaction inspiration only: zoom and pan across a conceptual whole, then click through to meaning and evidence. The Necessary Tangle remains its own public data model and interface.",
        },
    }

    DATA_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Applied {RELEASE}: whole-to-detail map metadata and curator comment route.")


if __name__ == "__main__":
    main()
