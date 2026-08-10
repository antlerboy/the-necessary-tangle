#!/usr/bin/env python3
"""Patch the public interface for release 0.11 semantic map interaction."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "docs" / "index.html"
APP = ROOT / "docs" / "assets" / "app.js"

CSS_LINK = '<link rel="stylesheet" href="assets/map-v11.css">'
JS_LINK = '<script src="assets/map-v11.js"></script>'
FEEDBACK_DOT = (
    '<a class="feedback-dot" '
    'href="https://github.com/antlerboy/the-necessary-tangle/issues/2" '
    'target="_blank" rel="noopener" '
    'aria-label="Open the curator’s running feedback thread" '
    'title="Running feedback">Running feedback</a>'
)

ABOUT_FEEDBACK = '''
        <article class="plain-panel wide feedback-ledger-panel">
          <p class="eyebrow">The map observes its own revision</p>
          <h2>What happened to the feedback</h2>
          <p>The public comments have been turned into a ledger rather than silently declared complete. It distinguishes what has been implemented, what received only a first pass, and what remains a bounded research programme. Large corpus requests stay open until the item-level work exists.</p>
          <p><a class="feedback-audit-link" href="https://github.com/antlerboy/the-necessary-tangle/blob/main/documentation/feedback-ledger.md" target="_blank" rel="noopener">Inspect the running feedback ledger →</a></p>
        </article>
'''

MAP_NOTE = '''
      <div class="semantic-map-introduction">
        <p><strong>Move between overview and detail.</strong> Zoom changes how much is named, not merely how large the clutter becomes. Double-click an entry for its neighbourhood; hover to see immediate company; use the minimap to keep your bearings. Press <kbd>+</kbd>/<kbd>−</kbd> to zoom, <kbd>0</kbd> to fit, <kbd>L</kbd> to change label density and <kbd>F</kbd> for fullscreen.</p>
      </div>
'''

MAP_API = r'''

  window.TangleMap = Object.assign(window.TangleMap || {}, {
    semanticMapVersion: '0.11',
    getTransform: () => ({ ...mapTransform }),
    setTransform: (next = {}) => {
      const scale = Math.min(8, Math.max(0.16, Number(next.scale ?? mapTransform.scale) || 1));
      mapTransform = {
        x: Number(next.x ?? mapTransform.x) || 0,
        y: Number(next.y ?? mapTransform.y) || 0,
        scale
      };
      applyMapTransform();
      document.dispatchEvent(new CustomEvent('tangle:map-transform', { detail: { ...mapTransform } }));
    },
    fit: () => document.getElementById('mapFit')?.click(),
    reset: () => document.getElementById('mapReset')?.click(),
    getFocus: () => mapFocus || null
  });
'''


def clean(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.rstrip().splitlines()) + "\n"


def patch_index() -> None:
    text = INDEX.read_text(encoding="utf-8")

    if CSS_LINK not in text:
        marker = '<link rel="stylesheet" href="assets/site-enhancements.css">'
        if marker in text:
            text = text.replace(marker, marker + "\n  " + CSS_LINK, 1)
        else:
            text = text.replace("</head>", "  " + CSS_LINK + "\n</head>", 1)

    if JS_LINK not in text:
        text = text.replace("</body>", "  " + JS_LINK + "\n</body>", 1)

    # Restore the deliberately discreet bottom-right route requested by the curator.
    if 'class="feedback-dot"' not in text:
        text = text.replace("</body>", "  " + FEEDBACK_DOT + "\n</body>", 1)

    if 'class="semantic-map-introduction"' not in text:
        marker = '<div class="map-layout">'
        if marker not in text:
            raise RuntimeError("Could not locate the map layout")
        text = text.replace(marker, MAP_NOTE + "\n      " + marker, 1)

    if 'class="feedback-ledger-panel"' not in text:
        marker = '<article class="plain-panel wide"><h2>Coverage programme</h2>'
        if marker in text:
            text = text.replace(marker, ABOUT_FEEDBACK + "\n        " + marker, 1)
        else:
            marker = '<article class="plain-panel wide"><h2>Documentation</h2>'
            if marker not in text:
                raise RuntimeError("Could not locate an About insertion point")
            text = text.replace(marker, ABOUT_FEEDBACK + "\n        " + marker, 1)

    if 'documentation/feedback-ledger.md' not in text:
        roadmap = '<a class="button" href="https://github.com/antlerboy/the-necessary-tangle/blob/main/documentation/roadmap.md" target="_blank" rel="noopener">Roadmap</a>'
        addition = roadmap + '<a class="button" href="https://github.com/antlerboy/the-necessary-tangle/blob/main/documentation/feedback-ledger.md" target="_blank" rel="noopener">Feedback ledger</a>'
        if roadmap in text:
            text = text.replace(roadmap, addition, 1)

    # Keep the map description aligned with the interaction which is actually present.
    text = text.replace(
        'Open the full public map or centre on one entry. The layout keeps its bearings and moves with your selection; select a line to inspect the statement, status and sources.',
        'Open the full public map or centre on one entry. Semantic zoom progressively reveals labels, the minimap preserves overview, and focus keeps enough context to show where you have moved. Select a line to inspect the statement, status and sources.',
    )

    INDEX.write_text(clean(text), encoding="utf-8")


def patch_app() -> None:
    app = APP.read_text(encoding="utf-8")
    if "semanticMapVersion: '0.11'" not in app:
        pattern = re.compile(r"(  function applyMapTransform\(\) \{.*?\n  \})(?=\n\n  function)", re.S)
        match = pattern.search(app)
        if not match:
            raise RuntimeError("Could not locate applyMapTransform in app.js")
        app = app[: match.end()] + MAP_API + app[match.end() :]
    APP.write_text(clean(app), encoding="utf-8")


def main() -> None:
    patch_index()
    patch_app()
    print("Applied 0.11 semantic-map controls and restored the running-feedback dot")


if __name__ == "__main__":
    main()
