#!/usr/bin/env python3
"""Make the 0.11 patch remove the obsolete whole-SVG zoom implementation."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "scripts" / "patch_iteration_11.py"

INSERT = '''    legacy_whole_svg_zoom = """  let tangleZoom = 1;

  function zoomMapAt(factor, originX = 50, originY = 50) {
    const svg = document.getElementById('graphSvg');
    if (!svg) return;
    tangleZoom = Math.max(0.55, Math.min(2.5, tangleZoom * factor));
    svg.style.transformOrigin = `${originX}% ${originY}%`;
    svg.style.transform = `scale(${tangleZoom})`;
    const status = document.getElementById('mapZoomStatus');
    if (status) status.textContent = `${Math.round(tangleZoom * 100)}%`;
  }

"""
    app = app.replace(legacy_whole_svg_zoom, "", 1)

'''


def main() -> None:
    text = PATH.read_text(encoding="utf-8")
    marker = '    APP.write_text(clean(app), encoding="utf-8")'
    if "legacy_whole_svg_zoom" not in text:
        if marker not in text:
            raise RuntimeError("Could not locate the app.js write point")
        text = text.replace(marker, INSERT + marker, 1)
    PATH.write_text(text, encoding="utf-8")
    print("Made the 0.11 patch remove the obsolete whole-SVG zoom code")


if __name__ == "__main__":
    main()
