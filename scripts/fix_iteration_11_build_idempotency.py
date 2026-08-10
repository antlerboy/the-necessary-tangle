#!/usr/bin/env python3
"""Make retained interface patches stop once the 0.11 map is already present."""
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


def add_semantic_zoom_guard(filename: str, message: str) -> None:
    path = ROOT / "scripts" / filename
    old = '''def main() -> None:
    patch_index()
    patch_app()
    patch_css()
'''
    new = f'''def main() -> None:
    if APP.exists() and "semanticZoomBand" in APP.read_text(encoding="utf-8"):
        print("Skipped {message}; the 0.11 map is already built")
        return
    patch_index()
    patch_app()
    patch_css()
'''
    replace_once(path, old, new, f"semantic-zoom guard in {filename}")


def main() -> None:
    expansion = ROOT / "scripts" / "patch_expansion_08.py"
    replace_once(
        expansion,
        '''    if new_activate not in app:
        app = replace_once(app, old_activate, new_activate, "activateMapNode block")
''',
        '''    if new_activate not in app and "function activateMapNode(id, options = {})" not in app:
        app = replace_once(app, old_activate, new_activate, "activateMapNode block")
''',
        "retained activateMapNode patch",
    )

    add_semantic_zoom_guard(
        "patch_expansion_08.py",
        "0.8 adaptive-map patch",
    )
    add_semantic_zoom_guard(
        "patch_iteration_09.py",
        "0.9 interface patch",
    )
    add_semantic_zoom_guard(
        "patch_iteration_10.py",
        "0.10 interface patch",
    )
    print("Made retained interface patches repeatable after the 0.11 map is present")


if __name__ == "__main__":
    main()
