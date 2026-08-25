#!/usr/bin/env python3
"""Stamp inherited maintained projections with the current release."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "public-data.json"
DOCS_JSON = ROOT / "docs" / "assets" / "public-data.json"
DOCS_JS = ROOT / "docs" / "assets" / "public-data.js"
PROJECTIONS = ("reading_list_inventory", "reading_list_coverage", "core_systems_practice")


def main() -> None:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    release = data.get("meta", {}).get("release")
    generated = data.get("meta", {}).get("generated")
    if not release or not generated:
        raise SystemExit("Current release metadata is missing")

    for key in PROJECTIONS:
        projection = data.get(key)
        if not isinstance(projection, dict):
            raise SystemExit(f"{key} is missing")
        projection["release"] = release
        if "generated" in projection:
            projection["generated"] = generated

    rendered = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    DATA.write_text(rendered, encoding="utf-8")
    DOCS_JSON.write_text(rendered, encoding="utf-8")
    DOCS_JS.write_text(
        "window.TANGLE_DATA = " + json.dumps(data, ensure_ascii=False) + ";\n",
        encoding="utf-8",
    )
    print(f"Stamped inherited projections for {release}.")


if __name__ == "__main__":
    main()
