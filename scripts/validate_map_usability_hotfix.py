#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
index = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
app = (ROOT / "docs" / "assets" / "app.js").read_text(encoding="utf-8")
css = (ROOT / "docs" / "assets" / "site-enhancements.css").read_text(encoding="utf-8")
doc = (ROOT / "documentation" / "visual-map.md").read_text(encoding="utf-8")

assert '#view=journeys&id=journey_david_ing_systems_in_plural&step=0' in index
assert '#view=item&id=person_david_ing&from=home' not in index
assert '#view=map&layer=substantive&depth=all&focus=concept_viability' in index
assert '<option value="all" selected>Full public overview</option>' in index
assert '<option value="substantive" selected>Reader map' in index
assert 'id="mapFocusStatus"' in index and 'class="map-shape-key"' in index
assert '<span id="mapScaleMode" class="map-scale-mode" aria-live="polite">Full overview</span>' in index
assert 'assets/app.js?v=0.15-mapfix2' in index

for marker in [
    'function graphNodeMark',
    "const labelBudget =",
    "if (family === 'all') return new Set(allowed);",
    "'context-edge'",
    "['path', 'profiles', 'all'].includes",
    "Full overview · ${nodes.length} entries",
    "depth === 'all' ? 'Full overview'",
    "Move through ${allRelations.length}",
]:
    assert marker in app, marker

family_filter = "        if ($('mapFamily').value !== 'all' && edge.relation_family !== $('mapFamily').value) continue;\n"
assert family_filter * 2 not in app
for marker in [
    "/* 0.15 map and guided-journey usability hotfix */",
    ".journey-choice { display: grid",
    ".journey-choice.active",
    ".step-track button.active",
    ".step-card {",
    ".graph-label {",
    ".graph-node-group.context-node",
    ".graph-edge.focus-edge",
    'grid-template-areas: "controls canvas" "controls inspector"',
]:
    assert marker in css, marker
assert "label-light full-public overview" in doc

print("MAP USABILITY HOTFIX VALIDATION PASSED")
