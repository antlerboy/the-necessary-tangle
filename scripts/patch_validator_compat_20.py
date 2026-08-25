#!/usr/bin/env python3
"""Teach retained release validators to recognise the 0.20 successor.

Historical behavioural assertions remain in force. Only current-release/date
and current operating-document expectations are extended.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RELEASE_19 = "0.19-living-marks-alpha"
RELEASE_20 = "0.20-prior-maps-alpha"


def replace_required(text: str, old: str, new: str, label: str) -> str:
    if new in text:
        return text
    if old not in text:
        raise SystemExit(f"Validator compatibility marker changed unexpectedly: {label}")
    return text.replace(old, new, 1)


def write(path: Path, text: str) -> bool:
    old = path.read_text(encoding="utf-8")
    if old == text:
        return False
    path.write_text(text, encoding="utf-8")
    return True


def extend_literal_sets(text: str) -> str:
    text = text.replace(
        f'"{RELEASE_19}"}}',
        f'"{RELEASE_19}", "{RELEASE_20}"}}',
    )
    text = text.replace(
        f"'{RELEASE_19}'}}",
        f"'{RELEASE_19}', '{RELEASE_20}'}}",
    )
    text = text.replace(
        f'"{RELEASE_19}",\n    }}',
        f'"{RELEASE_19}", "{RELEASE_20}",\n    }}',
    )
    return text


def main() -> int:
    sentinel_path = ROOT / "scripts" / "validate_iteration_19.py"
    if 'SUCCESSOR_RELEASE = "0.20-prior-maps-alpha"' in sentinel_path.read_text(encoding="utf-8"):
        print("0.20 validator compatibility: already compatible")
        return 0

    changed: list[str] = []
    for path in sorted((ROOT / "scripts").glob("validate*.py")):
        if path.name in {"validate_iteration_18.py", "validate_iteration_19.py", "validate_prior_maps_20.py"}:
            continue
        old = path.read_text(encoding="utf-8")
        new = extend_literal_sets(old)
        if path.name == "validate_iteration_13.py":
            new = replace_required(
                new,
                f'"2026-08-25" if meta.get("release") == "{RELEASE_19}"',
                f'"2026-08-25" if meta.get("release") in {{"{RELEASE_19}", "{RELEASE_20}"}}',
                "0.13 generation date",
            )
        elif path.name == "validate_iteration_14.py":
            new = replace_required(
                new,
                f'"2026-08-25" if meta.get("release") == "{RELEASE_19}"',
                f'"2026-08-25" if meta.get("release") in {{"{RELEASE_19}", "{RELEASE_20}"}}',
                "0.14 generation date",
            )
        elif path.name == "validate_iteration_15.py":
            new = replace_required(
                new,
                f"'2026-08-25' if meta['release']=='{RELEASE_19}'",
                f"'2026-08-25' if meta['release'] in {{'{RELEASE_19}','{RELEASE_20}'}}",
                "0.15 generation date",
            )
        elif path.name == "validate_iteration_17.py":
            new = replace_required(
                new,
                '("## Release 0.19" not in readme and "## Release 0.18" not in readme and "Release 0.17 contains" not in readme)',
                '("## Release 0.20" not in readme and "## Release 0.19" not in readme and "## Release 0.18" not in readme and "Release 0.17 contains" not in readme)',
                "0.17 README successor",
            )
        if write(path, new):
            changed.append(path.name)

    path18 = ROOT / "scripts" / "validate_iteration_18.py"
    text18 = path18.read_text(encoding="utf-8")
    text18 = replace_required(
        text18,
        'GENERATED_19 = "2026-08-25"\n',
        'GENERATED_19 = "2026-08-25"\nRELEASE_20 = "0.20-prior-maps-alpha"\nGENERATED_20 = "2026-08-25"\n',
        "0.18 successor constants",
    )
    text18 = replace_required(
        text18,
        "if meta.get(\"release\") not in {RELEASE, RELEASE_19}:",
        "if meta.get(\"release\") not in {RELEASE, RELEASE_19, RELEASE_20}:",
        "0.18 successor release",
    )
    text18 = replace_required(
        text18,
        'errors.append(f"meta.release must be {RELEASE} or {RELEASE_19}")',
        'errors.append(f"meta.release must be {RELEASE}, {RELEASE_19} or {RELEASE_20}")',
        "0.18 successor release message",
    )
    text18 = replace_required(
        text18,
        "if meta.get(\"generated\") not in {GENERATED, GENERATED_19}:",
        "if meta.get(\"generated\") not in {GENERATED, GENERATED_19, GENERATED_20}:",
        "0.18 successor date",
    )
    text18 = replace_required(
        text18,
        '"documentation/TANGLE_STATE.md": [RELEASE, "unFIX comparator concepts resolved"],',
        '"documentation/TANGLE_STATE.md": [RELEASE_20, "prior-map"],',
        "0.18 state successor",
    )
    text18 = replace_required(
        text18,
        '"documentation/NEXT_WORK.md": ["release 0.19 is complete", "No production change is authorised"],',
        '"documentation/NEXT_WORK.md": ["release 0.20 is complete", "No further production change is authorised"],',
        "0.18 next-work successor",
    )
    text18 = replace_required(
        text18,
        '("## Release 0.18" not in readme and "## Release 0.19" not in readme)',
        '("## Release 0.18" not in readme and "## Release 0.19" not in readme and "## Release 0.20" not in readme)',
        "0.18 README successor",
    )
    if write(path18, text18):
        changed.append(path18.name)

    path19 = ROOT / "scripts" / "validate_iteration_19.py"
    text19 = path19.read_text(encoding="utf-8")
    text19 = replace_required(
        text19,
        "from apply_iteration_19 import EPISODE_COUNT, GENERATED, MARK_COUNT, RELEASE\n",
        "from apply_iteration_19 import EPISODE_COUNT, GENERATED, MARK_COUNT, RELEASE\n\nSUCCESSOR_RELEASE = \"0.20-prior-maps-alpha\"\nSUCCESSOR_GENERATED = \"2026-08-25\"\n",
        "0.19 successor constants",
    )
    text19 = replace_required(
        text19,
        "if meta.get(\"release\") != RELEASE:\n        errors.append(f\"meta.release must be {RELEASE}\")",
        "if meta.get(\"release\") not in {RELEASE, SUCCESSOR_RELEASE}:\n        errors.append(f\"meta.release must be {RELEASE} or {SUCCESSOR_RELEASE}\")",
        "0.19 successor release",
    )
    text19 = replace_required(
        text19,
        "if meta.get(\"generated\") != GENERATED:\n        errors.append(f\"meta.generated must be {GENERATED}\")",
        "if meta.get(\"generated\") not in {GENERATED, SUCCESSOR_GENERATED}:\n        errors.append(f\"meta.generated must be {GENERATED} or {SUCCESSOR_GENERATED}\")",
        "0.19 successor date",
    )
    text19 = replace_required(
        text19,
        '"documentation/TANGLE_STATE.md": [RELEASE, "Living visual marks"],',
        '"documentation/TANGLE_STATE.md": [SUCCESSOR_RELEASE, "prior-map"],',
        "0.19 state successor",
    )
    text19 = replace_required(
        text19,
        '"documentation/NEXT_WORK.md": ["release 0.19 is complete", "No production change is authorised"],',
        '"documentation/NEXT_WORK.md": ["release 0.20 is complete", "No further production change is authorised"],',
        "0.19 next-work successor",
    )
    text19 = replace_required(
        text19,
        '"CITATION.cff": [f"version: {RELEASE}", f"date-released: {GENERATED}"],',
        '"CITATION.cff": [f"version: {meta.get(\'release\')}", f"date-released: {meta.get(\'generated\')}"],',
        "0.19 citation successor",
    )
    text19 = replace_required(
        text19,
        '"README.md": ["Release 0.19", "/corpora/complexity-podcast/"],',
        '"README.md": ["Release 0.20", "/corpora/complexity-podcast/"],',
        "0.19 README successor",
    )
    if write(path19, text19):
        changed.append(path19.name)

    if not changed:
        raise SystemExit("No validators were extended for 0.20")
    print("0.20 validator compatibility:")
    print("- extended: " + ", ".join(changed))
    print("- historical behavioural checks retained")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
