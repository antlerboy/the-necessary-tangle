#!/usr/bin/env python3
"""Extend retained historical validation allow-lists to recognise 0.18."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OLD = '"0.17-public-intake-lineage-alpha"'
NEW = '"0.18-navigable-tangle-alpha"'

changed = []
already = []
for path in sorted((ROOT / "scripts").glob("validate*.py")):
    text = path.read_text(encoding="utf-8")
    if NEW in text:
        already.append(path.name)
        continue
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
        path.write_text("".join(lines), encoding="utf-8")
        changed.append(path.name)

if not changed and not already:
    raise SystemExit("No historical validator allow-list recognised for 0.18 compatibility")

print("0.18 validator compatibility:")
print("- extended: " + (", ".join(changed) if changed else "none"))
print("- already compatible: " + (", ".join(already) if already else "none"))
