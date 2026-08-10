#!/usr/bin/env python3
"""Apply the final 0.8 UI corrections before publication."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

patch_path = ROOT / "scripts" / "patch_expansion_08.py"
text = patch_path.read_text()
old_regex = '''    text = re.sub(
        r'\\s*<p><a href="https://github\\.com/antlerboy/the-necessary-tangle/issues/2" class="curator-notebook-link"[^>]*>.*?</a></p>',
        '',
        text,
        count=1,
        flags=re.S,
    )
'''
new_regex = '''    text = re.sub(
        r'\\s*<p>\\s*<a[^>]*class="curator-notebook-link"[^>]*>.*?</a>\\s*</p>',
        '',
        text,
        flags=re.S,
    )
'''
if old_regex in text:
    text = text.replace(old_regex, new_regex, 1)
elif 'r\'\\s*<p>\\s*<a[^>]*class="curator-notebook-link"' not in text:
    raise SystemExit("Could not broaden the visible notebook-link removal")

map_marker = '''    text = text.replace(
        'Search for an entry to centre the map. Select an item to refocus. Select a line to inspect the statement, its status and its sources.',
        'Open the full public map or centre on one entry. The layout keeps its bearings and moves with your selection; select a line to inspect the statement, status and sources.',
    )
'''
map_replacement = map_marker + '''    text = text.replace(
        '<option value="all">Full public map</option>',
        '<option value="all" selected>Full public map</option>',
    )
'''
if '<option value="all" selected>Full public map</option>' not in text:
    if map_marker not in text:
        raise SystemExit("Could not set the full-map default in the patch source")
    text = text.replace(map_marker, map_replacement, 1)
patch_path.write_text(text)

validator_path = ROOT / "scripts" / "validate_expansion_08.py"
validator = validator_path.read_text()
old_checks = '''    if 'data-view-link="map" data-map-mode="all">Full public map</button>' not in index:
        errors.append("the home page does not open the full public map explicitly")
    if "Curator's running notebook and feedback issue" in index:
        errors.append("the curator running notebook remains too prominent")
    if 'class="discreet-note-link"' not in index:
        errors.append("the discreet curator-note wrapper is missing")
    if 'class="curator-notebook-link"' not in index or '/issues/2' not in index:
        errors.append("the curator notebook is no longer reachable")
'''
new_checks = '''    if 'data-view-link="map" data-map-mode="all">Full public map</button>' not in index:
        errors.append("the home page does not open the full public map explicitly")
    if '<option value="all" selected>Full public map</option>' not in index:
        errors.append("the map itself does not default to the full public map")
    if "Curator's running notebook and feedback issue" in index or ">Curator notebook</a>" in index:
        errors.append("the curator running notebook remains too prominent")
    if 'class="discreet-note-link"' not in index:
        errors.append("the discreet curator-note wrapper is missing")
    if index.count('class="curator-notebook-link"') != 1 or '/issues/2' not in index:
        errors.append("the curator notebook must be reachable through exactly one discreet link")
'''
if old_checks in validator:
    validator = validator.replace(old_checks, new_checks, 1)
elif "the map itself does not default to the full public map" not in validator:
    raise SystemExit("Could not strengthen the 0.8 UI validation")
validator_path.write_text(validator)
print("Fixed the full-map default and reduced the curator notebook to one discreet link")
