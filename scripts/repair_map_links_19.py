#!/usr/bin/env python3
"""Reapply the complete 0.18 map-link contract when its marker is stale."""
from __future__ import annotations

from patch_iteration_18 import APP, patch_app

MARKER = "/* 0.18 navigable map and link contract */"


def main() -> None:
    text = APP.read_text(encoding="utf-8")
    needs_repair = "graph-node-link" not in text or "graph-edge-link" not in text
    if not needs_repair:
        print("Map node and edge links already satisfy the 0.18 contract.")
        return

    # The historical patch used one aggregate marker as its idempotency guard.
    # A later rebuild preserved that marker while restoring an older app body.
    # Remove the stale guard, rerun the idempotent patch, then verify the links.
    APP.write_text(text.replace(MARKER, "", 1), encoding="utf-8")
    patch_app()
    repaired = APP.read_text(encoding="utf-8")
    missing = [name for name in ("graph-node-link", "graph-edge-link", MARKER) if name not in repaired]
    if missing:
        raise SystemExit("Map-link repair did not restore: " + ", ".join(missing))
    print("Restored navigable map-node and map-edge anchors.")


if __name__ == "__main__":
    main()
