#!/usr/bin/env python3
"""Extend retained historical validation allow-lists to recognise 0.18."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OLD = '"0.17-public-intake-lineage-alpha"'
NEW = '"0.18-navigable-tangle-alpha"'
READING_RELEASES_17 = 'if release in {"0.15-ing-reading-practice-alpha", "0.16-grammar-connections-presentation-alpha", "0.17-public-intake-lineage-alpha"}:'
READING_RELEASES_18 = 'if release in {"0.15-ing-reading-practice-alpha", "0.16-grammar-connections-presentation-alpha", "0.17-public-intake-lineage-alpha", "0.18-navigable-tangle-alpha"}:'

changed = []
already = []
for path in sorted((ROOT / "scripts").glob("validate*.py")):
    text = path.read_text(encoding="utf-8")
    if NEW in text:
        already.append(path.name)
    else:
        lines = text.splitlines(keepends=True)
        patched = False
        for index, line in enumerate(lines):
            if "ALLOWED_RELEASES" not in line or OLD not in line:
                continue
            if "{" not in line or "}" not in line:
                raise SystemExit(f"Unsupported multi-line ALLOWED_RELEASES declaration in {path.name}")
            lines[index] = line.replace(OLD, f"{OLD}, {NEW}", 1)
            patched = True
            break
        if patched:
            text = "".join(lines)
            changed.append(path.name)

    if path.name == "validate_iteration_12.py":
        if READING_RELEASES_18 not in text:
            if READING_RELEASES_17 not in text:
                raise SystemExit("The 0.12 reading-list status condition has changed unexpectedly")
            text = text.replace(READING_RELEASES_17, READING_RELEASES_18, 1)
            if path.name not in changed:
                changed.append(path.name)

    path.write_text(text, encoding="utf-8")

if not changed and not already:
    raise SystemExit("No historical validator allow-list recognised for 0.18 compatibility")

print("0.18 validator compatibility:")
print("- extended: " + (", ".join(changed) if changed else "none"))
print("- already compatible: " + (", ".join(already) if already else "none"))
