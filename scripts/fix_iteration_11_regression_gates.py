#!/usr/bin/env python3
"""Allow the deliberately restored curator comment dot in release 0.11."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_once(path: Path, old: str, new: str, label: str) -> None:
    text = path.read_text(encoding="utf-8")
    if new in text:
        return
    if old not in text:
        raise RuntimeError(f"Could not patch {label}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def main() -> None:
    replace_once(
        ROOT / "scripts" / "validate_constellation.py",
        '''    if meta.get("release") in {"0.7-constellation-alpha", "0.8-expansion-alpha", "0.9-observations-alpha"}:
        if 'class="curator-notebook-link"' not in index or '/issues/2' not in index:
            errors.append("curator notebook link is missing")
    elif '/issues/2' in index:
        errors.append("retired public curator-notebook route remains in the release")
''',
        '''    if meta.get("release") in {"0.7-constellation-alpha", "0.8-expansion-alpha", "0.9-observations-alpha"}:
        if 'class="curator-notebook-link"' not in index or '/issues/2' not in index:
            errors.append("curator notebook link is missing")
    elif meta.get("release") == "0.10-practice-safety-alpha" and '/issues/2' in index:
        errors.append("retired public curator-notebook route remains in the 0.10 release")
    elif meta.get("release") == "0.11-visual-map-alpha":
        if index.count('data-curator-dot="comments"') != 1 or index.count('/issues/2') != 1:
            errors.append("the restored curator comment dot is missing or duplicated")
''',
        "constellation curator-dot gate",
    )

    replace_once(
        ROOT / "scripts" / "validate_expansion_08.py",
        '''    if meta.get("release") in {"0.8-expansion-alpha", "0.9-observations-alpha"}:
        if 'class="discreet-note-link"' not in index:
            errors.append("the discreet curator-note wrapper is missing")
        if index.count('class="curator-notebook-link"') != 1 or '/issues/2' not in index:
            errors.append("the curator notebook must be reachable through exactly one discreet link")
    elif '/issues/2' in index:
        errors.append("the retired public curator-notebook route remains")
''',
        '''    if meta.get("release") in {"0.8-expansion-alpha", "0.9-observations-alpha"}:
        if 'class="discreet-note-link"' not in index:
            errors.append("the discreet curator-note wrapper is missing")
        if index.count('class="curator-notebook-link"') != 1 or '/issues/2' not in index:
            errors.append("the curator notebook must be reachable through exactly one discreet link")
    elif meta.get("release") == "0.10-practice-safety-alpha" and '/issues/2' in index:
        errors.append("the retired public curator-notebook route remains in 0.10")
    elif meta.get("release") == "0.11-visual-map-alpha":
        if index.count('data-curator-dot="comments"') != 1 or index.count('/issues/2') != 1:
            errors.append("the restored curator comment dot is missing or duplicated")
''',
        "0.8 curator-dot regression gate",
    )

    print("Updated retained regression gates for the restored 0.11 curator comment dot")


if __name__ == "__main__":
    main()
