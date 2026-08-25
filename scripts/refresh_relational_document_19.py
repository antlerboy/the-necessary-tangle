#!/usr/bin/env python3
"""Regenerate the relational-depth document from the current public graph."""
from __future__ import annotations

import json
from pathlib import Path

from apply_relational_depth_16 import write_relational_document

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "public-data.json"


def main() -> None:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    if not isinstance(data.get("relational_depth"), dict):
        raise SystemExit("Current relational-depth measures are missing")
    write_relational_document(data)
    aggregate = data["relational_depth"].get("aggregate", {})
    print(
        "Refreshed relational-depth document for "
        f"{aggregate.get('reader_connected_entries')} reader-connected entries."
    )


if __name__ == "__main__":
    main()
