#!/usr/bin/env python3
"""Normalise the rebuilt map-scale control before the historical hotfix runs."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "docs" / "index.html"
APP = ROOT / "docs" / "assets" / "app.js"

DESIRED = '<label>Scale<select id="mapDepth"><option value="1">Immediate connections</option><option value="2">Two steps</option><option value="path">Path and immediate neighbours</option><option value="profiles">Developed-entry overview</option><option value="all" selected>Full public overview</option></select></label>'
PATTERN = re.compile(r'<label>(?:View|Scale)<select id="mapDepth">.*?</select></label>', re.DOTALL)


def main() -> None:
    text = INDEX.read_text(encoding="utf-8")
    if DESIRED in text:
        print("Map-scale control already normalised")
        return
    text, count = PATTERN.subn(DESIRED, text, count=1)
    if count != 1:
        raise RuntimeError(f"Expected one mapDepth control, found {count}")
    INDEX.write_text(text, encoding="utf-8")
    print("Normalised rebuilt map-scale control for the historical hotfix")

    app = APP.read_text(encoding="utf-8")
    with_constellation = """    if (label) {
      const depth = $('mapDepth')?.value;
      label.textContent = depth === 'all' ? 'Full overview' : depth === 'profiles' ? 'Developed overview' : depth === 'constellation' ? 'Constellation' : band === 'overview' ? 'Whole map' : band === 'detail' ? 'Detail' : 'Neighbourhood';
    }"""
    historical = """    if (label) {
      const depth = $('mapDepth')?.value;
      label.textContent = depth === 'all' ? 'Full overview' : depth === 'profiles' ? 'Developed overview' : band === 'overview' ? 'Whole map' : band === 'detail' ? 'Detail' : 'Neighbourhood';
    }"""
    if with_constellation in app:
        app = app.replace(with_constellation, historical, 1)
        APP.write_text(app, encoding="utf-8")
        print("Temporarily normalised the post-0.18 semantic zoom label")
    elif historical in app:
        print("Semantic zoom label already compatible")
    else:
        raise RuntimeError("Could not locate the semantic zoom label for historical compatibility")


if __name__ == "__main__":
    main()
