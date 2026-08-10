#!/usr/bin/env python3
"""Wire and upgrade the durable build for the 0.9 feedback release."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if new in text:
        return text
    if old not in text:
        raise RuntimeError(f"Could not find {label}")
    return text.replace(old, new, 1)


def wire_makefile() -> None:
    path = ROOT / "Makefile"
    text = path.read_text()
    if "\tpython3 scripts/apply_iteration_09.py\n" not in text:
        text = text.replace(
            "\tpython3 scripts/apply_expansion_08.py\n",
            "\tpython3 scripts/apply_expansion_08.py\n\tpython3 scripts/apply_iteration_09.py\n",
            1,
        )
    if "\tpython3 scripts/refresh_graph_snapshot.py\n" not in text:
        text = text.replace(
            "\tpython3 scripts/apply_iteration_09.py\n",
            "\tpython3 scripts/apply_iteration_09.py\n\tpython3 scripts/refresh_graph_snapshot.py\n",
            1,
        )
    if "\tpython3 scripts/patch_iteration_09.py\n" not in text:
        text = text.replace(
            "\tpython3 scripts/patch_expansion_08.py\n",
            "\tpython3 scripts/patch_expansion_08.py\n\tpython3 scripts/patch_iteration_09.py\n",
            1,
        )
    if "\tpython3 scripts/validate_iteration_09.py\n" not in text:
        text = text.replace(
            "\tpython3 scripts/validate_expansion_08.py\n",
            "\tpython3 scripts/validate_expansion_08.py\n\tpython3 scripts/validate_iteration_09.py\n",
            1,
        )
    path.write_text(text)


def patch_entry_names() -> None:
    path = ROOT / "scripts" / "apply_iteration_09.py"
    text = path.read_text()
    text = text.replace('"Complexity science"', '"Complexity"')
    text = text.replace('"Complex adaptive system"', '"Adaptation"')
    path.write_text(text)


def patch_constellation_validator() -> None:
    path = ROOT / "scripts" / "validate_constellation.py"
    text = path.read_text()
    text = text.replace(
        'ALLOWED_RELEASES = {"0.7-constellation-alpha", "0.8-expansion-alpha"}',
        'ALLOWED_RELEASES = {"0.7-constellation-alpha", "0.8-expansion-alpha", "0.9-observations-alpha"}',
    )
    if '"0.9-observations-alpha"' not in text:
        raise RuntimeError("Could not add 0.9 to the constellation release gate")
    path.write_text(text)


def patch_expansion_validator() -> None:
    path = ROOT / "scripts" / "validate_expansion_08.py"
    text = path.read_text()
    text = text.replace(
        'EXPECTED_RELEASE = "0.8-expansion-alpha"',
        'ALLOWED_RELEASES = {"0.8-expansion-alpha", "0.9-observations-alpha"}',
    )
    text = text.replace(
        'if meta.get("release") != EXPECTED_RELEASE:\n        errors.append(f"meta.release must be {EXPECTED_RELEASE}")',
        'if meta.get("release") not in ALLOWED_RELEASES:\n        errors.append(f"meta.release must be one of {sorted(ALLOWED_RELEASES)}")',
    )

    old_growth = "\n".join([
        '    if len(public_nodes) != EXPECTED_PUBLIC_COUNT:',
        '        errors.append(f"expected {EXPECTED_PUBLIC_COUNT} canonical public entries, found {len(public_nodes)}")',
        '    if meta.get("public_entry_count") != len(public_nodes):',
        '        errors.append("meta.public_entry_count does not match canonical public entries")',
        '    added = len(public_nodes) - BASELINE_COUNT',
        '    if added < MINIMUM_ADDED:',
        '        errors.append(f"only {added} net new public entries; expected at least {MINIMUM_ADDED}")',
        '    if meta.get("expansion_08_added_count") != added:',
        '        errors.append("meta.expansion_08_added_count does not match the calculated increase")',
        '    if expansion.get("net_new_public_entries") != added:',
        '        errors.append("expansion_08.net_new_public_entries does not match the calculated increase")',
        '',
    ])
    new_growth = "\n".join([
        '    if len(public_nodes) < EXPECTED_PUBLIC_COUNT:',
        '        errors.append(f"expected at least {EXPECTED_PUBLIC_COUNT} canonical public entries, found {len(public_nodes)}")',
        '    if meta.get("public_entry_count") != len(public_nodes):',
        '        errors.append("meta.public_entry_count does not match canonical public entries")',
        '    expected_added = EXPECTED_PUBLIC_COUNT - BASELINE_COUNT',
        '    added = expansion.get("net_new_public_entries")',
        '    if added != expected_added or added < MINIMUM_ADDED:',
        '        errors.append(f"0.8 must retain {expected_added} net new public entries; found {added}")',
        '    if meta.get("expansion_08_added_count") != expected_added:',
        '        errors.append("meta.expansion_08_added_count no longer records the 0.8 increase")',
        '',
    ])
    if old_growth in text:
        text = text.replace(old_growth, new_growth, 1)
    elif 'expected at least {EXPECTED_PUBLIC_COUNT}' not in text:
        raise RuntimeError("Could not make the 0.8 count gate growth-tolerant")

    old_home = "\n".join([
        '    if \'data-view-link="map" data-map-mode="all">Full public map</button>\' not in index:',
        '        errors.append("the home page does not open the full public map explicitly")',
        '',
    ])
    new_home = "\n".join([
        '    home_map_markers = [',
        '        \'data-view-link="map" data-map-mode="all">Full public map</button>\',',
        '        \'data-view-link="map" data-map-mode="all">Full public map</a>\',',
        '    ]',
        '    if not any(marker in index for marker in home_map_markers):',
        '        errors.append("the home page does not open the full public map explicitly")',
        '',
    ])
    if old_home in text:
        text = text.replace(old_home, new_home, 1)

    old_markers = "\n".join([
        '    for marker in [',
        '        "mapVisibleEdge", "previousAngle", "animateMapTransition", "moveMapToFocus",',
        '        "button.dataset.mapMode === \'all\'", "renderMap({ fit: !keepsWholeMap, focus: keepsWholeMap })",',
        '    ]:',
        '        if marker not in app:',
        '            errors.append(f"adaptive-map marker missing from app.js: {marker}")',
        '',
    ])
    new_markers = "\n".join([
        '    for marker in [',
        '        "mapVisibleEdge", "previousAngle", "animateMapTransition", "moveMapToFocus",',
        '        "renderMap({ fit: !keepsWholeMap, focus: keepsWholeMap })",',
        '    ]:',
        '        if marker not in app:',
        '            errors.append(f"adaptive-map marker missing from app.js: {marker}")',
        '    if "button.dataset.mapMode === \'all\'" not in app and "followInternalAnchor" not in app:',
        '        errors.append("the full-map navigation hook is missing")',
        '',
    ])
    if old_markers in text:
        text = text.replace(old_markers, new_markers, 1)

    required = [
        "ALLOWED_RELEASES",
        "expected at least {EXPECTED_PUBLIC_COUNT}",
        "home_map_markers",
        "followInternalAnchor",
    ]
    missing = [marker for marker in required if marker not in text]
    if missing:
        raise RuntimeError(f"0.8 growth-compatible validator patch incomplete: {missing}")
    path.write_text(text)


def patch_changelog() -> None:
    path = ROOT / "CHANGELOG.md"
    text = path.read_text()
    entry = "\n".join([
        "## 0.9-observations-alpha — 10 August 2026",
        "",
        "- Added a public AI observations page separating reproducible measurements, interpretation, implications and tests.",
        "- Added a publication-risk register and a maintained source-mining queue.",
        "- Added developed entries for Chris Mowles, complex responsive processes, Murmurations and *Complexity: A Key Idea for Business and Society*.",
        "- Added seven public source records and four guided journeys.",
        "- Exposed conceptual, human-lineage, practice, contestation and provenance layers directly from About and the map.",
        "- Converted internal navigation affordances to real links so they can be opened in new tabs.",
        "- Made mouse-wheel zoom follow the pointer and removed the older double-zoom behaviour.",
        "- Enforced left alignment across content panels and expanded compressed About statements.",
        "",
    ]) + "\n"
    if "## 0.9-observations-alpha" not in text:
        first_break = text.find("\n\n")
        text = text[: first_break + 2] + entry + text[first_break + 2 :]
    path.write_text(text)


def main() -> None:
    wire_makefile()
    patch_entry_names()
    patch_constellation_validator()
    patch_expansion_validator()
    patch_changelog()
    print("Prepared the durable 0.9 release build and regression gates")


if __name__ == "__main__":
    main()
