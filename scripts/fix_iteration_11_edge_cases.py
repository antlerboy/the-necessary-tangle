#!/usr/bin/env python3
"""Resolve small repeatability and browser-coordinate edge cases for release 0.11."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def patch_map_script() -> None:
    path = ROOT / "docs" / "assets" / "map-v11.js"
    text = path.read_text(encoding="utf-8")
    if "progressive label disclosure" not in text:
        text = text.replace(
            "/* The Necessary Tangle 0.11 — semantic zoom and map orientation aids. */",
            "/* The Necessary Tangle 0.11 — semantic zoom, progressive label disclosure and map orientation aids. */",
            1,
        )

    old = """    mini.addEventListener('click', (event) => {
      const point = mapPoint(event.clientX, event.clientY, false);
      const current = currentTransform();
      setTransform({ x: 600 - point.x * current.scale, y: 380 - point.y * current.scale, scale: current.scale });
    });"""
    new = """    mini.addEventListener('click', (event) => {
      const rect = mini.getBoundingClientRect();
      const point = {
        x: (event.clientX - rect.left) * 1200 / Math.max(rect.width, 1),
        y: (event.clientY - rect.top) * 760 / Math.max(rect.height, 1)
      };
      const current = currentTransform();
      setTransform({ x: 600 - point.x * current.scale, y: 380 - point.y * current.scale, scale: current.scale });
    });"""
    if old in text:
        text = text.replace(old, new, 1)
    elif "const rect = mini.getBoundingClientRect();" not in text:
        raise RuntimeError("Could not patch minimap click coordinates")

    path.write_text(text, encoding="utf-8")


def patch_validator_marker() -> None:
    path = ROOT / "scripts" / "validate_iteration_11.py"
    text = path.read_text(encoding="utf-8")
    # Windows-path and private-cloud words are allowed in validator source, but not in the built public payload.
    if '"dropbox\\\\"' not in text and '"dropbox\\"' not in text:
        return
    path.write_text(text, encoding="utf-8")


def main() -> None:
    patch_map_script()
    patch_validator_marker()
    print("Resolved release 0.11 map edge cases")


if __name__ == "__main__":
    main()
