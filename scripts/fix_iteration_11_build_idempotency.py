#!/usr/bin/env python3
"""Make retained interface patches coexist with the later 0.11 map."""
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


def preserve_semantic_map_app(filename: str, message: str) -> None:
    path = ROOT / "scripts" / filename
    old = '''def main() -> None:
    patch_index()
    patch_app()
    patch_css()
'''
    new = f'''def main() -> None:
    patch_index()
    if APP.exists() and "semanticZoomBand" in APP.read_text(encoding="utf-8"):
        print("Preserved the 0.11 map application while refreshing {message}")
    else:
        patch_app()
    patch_css()
'''
    replace_once(path, old, new, f"semantic-map preservation in {filename}")


def main() -> None:
    makefile = ROOT / "Makefile"
    text = makefile.read_text(encoding="utf-8")
    normalise_line = "\tpython3 scripts/normalise_iteration_11_dot.py\n"
    if normalise_line not in text:
        marker = "\tpython3 scripts/patch_iteration_11.py\n"
        if marker not in text:
            raise RuntimeError("Could not wire curator-dot normalisation after the 0.11 patch")
        text = text.replace(marker, marker + normalise_line, 1)
        makefile.write_text(text, encoding="utf-8")

    constellation = ROOT / "scripts" / "patch_constellation_07.py"
    replace_once(
        constellation,
        '''    if 'class="curator-notebook-link"' not in text:
        text = text.replace('</footer>', '<p><a class="curator-notebook-link" href="https://github.com/antlerboy/the-necessary-tangle/issues/2">Curator notebook</a></p></footer>', 1)
''',
        '''    if 'class="curator-notebook-link"' not in text and 'data-curator-dot="comments"' not in text:
        text = text.replace('</footer>', '<p><a class="curator-notebook-link" href="https://github.com/antlerboy/the-necessary-tangle/issues/2">Curator notebook</a></p></footer>', 1)
''',
        "0.7 notebook compatibility guard",
    )
    replace_once(
        constellation,
        '''    if "function zoomMapAt" not in app:
        app = app.rstrip() + "\n" + APPEND_JS.strip() + "\n"
''',
        '''    if "function zoomMapAt" not in app and "semanticZoomBand" not in app:
        app = app.rstrip() + "\n" + APPEND_JS.strip() + "\n"
''',
        "0.7 legacy zoom compatibility guard",
    )

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

    preserve_semantic_map_app(
        "patch_expansion_08.py",
        "the 0.8 page and styles",
    )
    preserve_semantic_map_app(
        "patch_iteration_09.py",
        "the 0.9 page and styles",
    )
    preserve_semantic_map_app(
        "patch_iteration_10.py",
        "the 0.10 page and styles",
    )
    print("Made retained page patches repeatable without replacing the 0.11 map application")


if __name__ == "__main__":
    main()
