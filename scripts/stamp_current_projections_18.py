#!/usr/bin/env python3
"""Stamp maintained projections which are regenerated as part of release 0.18."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "public-data.json"
DOCS_JSON = ROOT / "docs" / "assets" / "public-data.json"
DOCS_JS = ROOT / "docs" / "assets" / "public-data.js"
RELEASE = "0.18-navigable-tangle-alpha"
GENERATED = "2026-08-23"


def main() -> None:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    inventory = data.get("reading_list_inventory")
    if not isinstance(inventory, dict):
        raise SystemExit("reading_list_inventory is missing")
    inventory["release"] = RELEASE
    if "generated" in inventory:
        inventory["generated"] = GENERATED

    rendered = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    DATA.write_text(rendered, encoding="utf-8")
    DOCS_JSON.write_text(rendered, encoding="utf-8")
    DOCS_JS.write_text("window.TANGLE_DATA = " + json.dumps(data, ensure_ascii=False) + ";\n", encoding="utf-8")
    print("Stamped the maintained reading-list inventory for release 0.18.")


if __name__ == "__main__":
    main()
