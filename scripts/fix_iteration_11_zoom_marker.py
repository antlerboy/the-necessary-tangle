#!/usr/bin/env python3
"""Use the current semantic-zoom marker in the retained constellation validator."""
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "scripts" / "validate_constellation.py"
text = path.read_text(encoding="utf-8")
old = '    for marker in ["zoomMapAt", "emergentCategories", "membershipForm", "human sponsor"]:\n'
new = '    map_marker = "semanticZoomBand" if meta.get("release") == "0.11-visual-map-alpha" else "zoomMapAt"\n    for marker in [map_marker, "emergentCategories", "membershipForm", "human sponsor"]:\n'
if old not in text and new not in text:
    raise RuntimeError("Could not locate the retained map marker check")
path.write_text(text.replace(old, new, 1), encoding="utf-8")
print("Updated the retained constellation check to recognise semantic zoom")
