#!/usr/bin/env python3
"""Let retained interface patches recognise the later 0.11 map implementation."""
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "scripts" / "patch_expansion_08.py"
text = path.read_text(encoding="utf-8")
old = '''    if new_activate not in app:
        app = replace_once(app, old_activate, new_activate, "activateMapNode block")
'''
new = '''    if new_activate not in app and "function activateMapNode(id, options = {})" not in app:
        app = replace_once(app, old_activate, new_activate, "activateMapNode block")
'''
if old not in text and new not in text:
    raise RuntimeError("Could not locate the retained activateMapNode patch")
path.write_text(text.replace(old, new, 1), encoding="utf-8")
print("Made the retained 0.8 map patch tolerant of the later 0.11 focus-history implementation")
