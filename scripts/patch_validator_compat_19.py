#!/usr/bin/env python3
"""Extend retained historical validation contracts to recognise release 0.19.

The validators continue to check the behaviour introduced by their own releases.
This script only teaches them that 0.19 is a legitimate successor and supplies the
new release date where a validator explicitly checks successor metadata.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OLD = '"0.18-navigable-tangle-alpha"'
NEW = '"0.19-living-marks-alpha"'
RELEASE_19 = "0.19-living-marks-alpha"
GENERATED_19 = "2026-08-25"


def replace_required(text: str, old: str, new: str, label: str) -> str:
    if new in text:
        return text
    if old not in text:
        raise SystemExit(f"The {label} contract has changed unexpectedly")
    return text.replace(old, new, 1)


def extend_one_line_allowed_release(text: str, path: Path) -> str:
    if NEW in text:
        return text
    lines = text.splitlines(keepends=True)
    for index, line in enumerate(lines):
        if "ALLOWED_RELEASES" not in line or OLD not in line:
            continue
        if "{" not in line or "}" not in line:
            raise SystemExit(f"Unsupported multi-line ALLOWED_RELEASES declaration in {path.name}")
        lines[index] = line.replace(OLD, f"{OLD}, {NEW}", 1)
        return "".join(lines)
    return text


def patch_constellation(text: str) -> str:
    marker = '        "0.18-navigable-tangle-alpha",\n    }\n    map_marker = "semanticZoomBand"'
    replacement = '        "0.18-navigable-tangle-alpha", "0.19-living-marks-alpha",\n    }\n    map_marker = "semanticZoomBand"'
    return replace_required(text, marker, replacement, "constellation semantic-zoom successor")


def patch_iteration_12(text: str) -> str:
    old = 'if release in {"0.15-ing-reading-practice-alpha", "0.16-grammar-connections-presentation-alpha", "0.17-public-intake-lineage-alpha", "0.18-navigable-tangle-alpha"}:'
    new = 'if release in {"0.15-ing-reading-practice-alpha", "0.16-grammar-connections-presentation-alpha", "0.17-public-intake-lineage-alpha", "0.18-navigable-tangle-alpha", "0.19-living-marks-alpha"}:'
    return replace_required(text, old, new, "0.12 reading-list successor")


def patch_iteration_13(text: str) -> str:
    old_date = 'expected_date = "2026-08-23" if meta.get("release") == "0.18-navigable-tangle-alpha" else ("2026-08-19" if meta.get("release") == "0.17-public-intake-lineage-alpha" else ("2026-08-14" if meta.get("release") in {"0.15-ing-reading-practice-alpha", "0.16-grammar-connections-presentation-alpha", "0.17-public-intake-lineage-alpha"} else EXPECTED_DATE))'
    new_date = 'expected_date = "2026-08-25" if meta.get("release") == "0.19-living-marks-alpha" else ("2026-08-23" if meta.get("release") == "0.18-navigable-tangle-alpha" else ("2026-08-19" if meta.get("release") == "0.17-public-intake-lineage-alpha" else ("2026-08-14" if meta.get("release") in {"0.15-ing-reading-practice-alpha", "0.16-grammar-connections-presentation-alpha", "0.17-public-intake-lineage-alpha"} else EXPECTED_DATE)))'
    text = replace_required(text, old_date, new_date, "0.13 generation date")
    old_ledger = 'if meta.get("release") not in {"0.17-public-intake-lineage-alpha", "0.18-navigable-tangle-alpha"} and (ROOT / "documentation" / "feedback-ledger.md").exists():'
    new_ledger = 'if meta.get("release") not in {"0.17-public-intake-lineage-alpha", "0.18-navigable-tangle-alpha", "0.19-living-marks-alpha"} and (ROOT / "documentation" / "feedback-ledger.md").exists():'
    return replace_required(text, old_ledger, new_ledger, "0.13 feedback-ledger successor")


def patch_iteration_14(text: str) -> str:
    old_forward = 'FORWARD_RELEASES = {"0.15-ing-reading-practice-alpha", "0.16-grammar-connections-presentation-alpha", "0.17-public-intake-lineage-alpha", "0.18-navigable-tangle-alpha"}'
    new_forward = 'FORWARD_RELEASES = {"0.15-ing-reading-practice-alpha", "0.16-grammar-connections-presentation-alpha", "0.17-public-intake-lineage-alpha", "0.18-navigable-tangle-alpha", "0.19-living-marks-alpha"}'
    text = replace_required(text, old_forward, new_forward, "0.14 forward-release set")
    old_date = 'expected_generated = "2026-08-23" if meta.get("release") == "0.18-navigable-tangle-alpha" else ("2026-08-19" if meta.get("release") == "0.17-public-intake-lineage-alpha" else (GENERATED if meta.get("release") == RELEASE else FORWARD_GENERATED))'
    new_date = 'expected_generated = "2026-08-25" if meta.get("release") == "0.19-living-marks-alpha" else ("2026-08-23" if meta.get("release") == "0.18-navigable-tangle-alpha" else ("2026-08-19" if meta.get("release") == "0.17-public-intake-lineage-alpha" else (GENERATED if meta.get("release") == RELEASE else FORWARD_GENERATED)))'
    return replace_required(text, old_date, new_date, "0.14 generation date")


def patch_iteration_15(text: str) -> str:
    old = "meta=D['meta']; assert meta['release'] in {'0.15-ing-reading-practice-alpha','0.16-grammar-connections-presentation-alpha', '0.17-public-intake-lineage-alpha', '0.18-navigable-tangle-alpha'}; assert meta['generated']==('2026-08-23' if meta['release']=='0.18-navigable-tangle-alpha' else ('2026-08-19' if meta['release']=='0.17-public-intake-lineage-alpha' else '2026-08-14'))"
    new = "meta=D['meta']; assert meta['release'] in {'0.15-ing-reading-practice-alpha','0.16-grammar-connections-presentation-alpha', '0.17-public-intake-lineage-alpha', '0.18-navigable-tangle-alpha', '0.19-living-marks-alpha'}; assert meta['generated']==('2026-08-25' if meta['release']=='0.19-living-marks-alpha' else ('2026-08-23' if meta['release']=='0.18-navigable-tangle-alpha' else ('2026-08-19' if meta['release']=='0.17-public-intake-lineage-alpha' else '2026-08-14')))"
    return replace_required(text, old, new, "0.15 successor metadata")


def patch_iteration_16(text: str) -> str:
    old_release = 'if meta.get("release") not in {RELEASE, "0.17-public-intake-lineage-alpha", "0.18-navigable-tangle-alpha"}:'
    new_release = 'if meta.get("release") not in {RELEASE, "0.17-public-intake-lineage-alpha", "0.18-navigable-tangle-alpha", "0.19-living-marks-alpha"}:'
    text = replace_required(text, old_release, new_release, "0.16 successor release")
    old_date = 'if meta.get("generated") not in {GENERATED, "2026-08-19", "2026-08-23"}:'
    new_date = 'if meta.get("generated") not in {GENERATED, "2026-08-19", "2026-08-23", "2026-08-25"}:'
    return replace_required(text, old_date, new_date, "0.16 successor date")


def patch_iteration_17(text: str) -> str:
    old_release = 'if meta.get("release") not in {RELEASE, "0.18-navigable-tangle-alpha"}:'
    new_release = 'if meta.get("release") not in {RELEASE, "0.18-navigable-tangle-alpha", "0.19-living-marks-alpha"}:'
    text = replace_required(text, old_release, new_release, "0.17 successor release")
    old_date = 'if meta.get("generated") not in {GENERATED, "2026-08-23"}:'
    new_date = 'if meta.get("generated") not in {GENERATED, "2026-08-23", "2026-08-25"}:'
    text = replace_required(text, old_date, new_date, "0.17 successor date")
    old_submissions = 'if submissions.get("release") not in {RELEASE, "0.18-navigable-tangle-alpha"} or submissions.get("marker") != "Prepared from The Necessary Tangle":'
    new_submissions = 'if submissions.get("release") not in {RELEASE, "0.18-navigable-tangle-alpha", "0.19-living-marks-alpha"} or submissions.get("marker") != "Prepared from The Necessary Tangle":'
    text = replace_required(text, old_submissions, new_submissions, "0.17 submissions successor")
    old_readme = 'if ("## Release 0.18" not in readme and "Release 0.17 contains" not in readme) or "https://transduction.systems/" not in readme:'
    new_readme = 'if ("## Release 0.19" not in readme and "## Release 0.18" not in readme and "Release 0.17 contains" not in readme) or "https://transduction.systems/" not in readme:'
    return replace_required(text, old_readme, new_readme, "0.17 README successor")


def patch_iteration_18(text: str) -> str:
    if 'RELEASE_19 = "0.19-living-marks-alpha"' not in text:
        marker = 'VERSION = "0.18.0-public"\n'
        text = replace_required(
            text,
            marker,
            marker + f'RELEASE_19 = "{RELEASE_19}"\nGENERATED_19 = "{GENERATED_19}"\n',
            "0.18 successor constants",
        )
    old_release = 'if meta.get("release") != RELEASE:\n        errors.append(f"meta.release must be {RELEASE}")'
    new_release = 'if meta.get("release") not in {RELEASE, RELEASE_19}:\n        errors.append(f"meta.release must be {RELEASE} or {RELEASE_19}")'
    text = replace_required(text, old_release, new_release, "0.18 successor release")
    old_date = 'if meta.get("generated") != GENERATED:\n        errors.append(f"meta.generated must be {GENERATED}")'
    new_date = 'if meta.get("generated") not in {GENERATED, GENERATED_19}:\n        errors.append(f"meta.generated must be {GENERATED} or {GENERATED_19}")'
    text = replace_required(text, old_date, new_date, "0.18 successor date")

    text = text.replace(
        '"documentation/NEXT_WORK.md": ["release 0.18 is complete", "No production change is authorised"],',
        '"documentation/NEXT_WORK.md": ["release 0.19 is complete", "No production change is authorised"],',
        1,
    )
    text = text.replace(
        'if f"version: {RELEASE}" not in citation or f"date-released: {GENERATED}" not in citation:',
        'if f"version: {meta.get(\'release\')}" not in citation or f"date-released: {meta.get(\'generated\')}" not in citation:',
        1,
    )
    text = text.replace(
        'if "## Release 0.18" not in readme or "coverage/named/" not in readme or "coverage/unfix-32/" not in readme:',
        'if ("## Release 0.18" not in readme and "## Release 0.19" not in readme) or "coverage/named/" not in readme or "coverage/unfix-32/" not in readme:',
        1,
    )
    return text


PATCHERS = {
    "validate_constellation.py": patch_constellation,
    "validate_iteration_12.py": patch_iteration_12,
    "validate_iteration_13.py": patch_iteration_13,
    "validate_iteration_14.py": patch_iteration_14,
    "validate_iteration_15.py": patch_iteration_15,
    "validate_iteration_16.py": patch_iteration_16,
    "validate_iteration_17.py": patch_iteration_17,
    "validate_iteration_18.py": patch_iteration_18,
}


def main() -> None:
    changed: list[str] = []
    recognised: list[str] = []
    for path in sorted((ROOT / "scripts").glob("validate*.py")):
        text = path.read_text(encoding="utf-8")
        original = text
        text = extend_one_line_allowed_release(text, path)
        if path.name in PATCHERS:
            text = PATCHERS[path.name](text)
            recognised.append(path.name)
        if text != original:
            path.write_text(text, encoding="utf-8")
            changed.append(path.name)

    missing = sorted(set(PATCHERS) - set(recognised))
    if missing:
        raise SystemExit("Missing retained validators: " + ", ".join(missing))
    if not changed:
        print("0.19 validator compatibility: already compatible")
        return

    print("0.19 validator compatibility:")
    print("- extended: " + ", ".join(changed))
    print("- behavioural checks retained; only successor release/date recognition changed")


if __name__ == "__main__":
    main()
