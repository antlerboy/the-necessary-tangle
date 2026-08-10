#!/usr/bin/env python3
"""Tighten the volume-membership check before the final 0.8 build."""
from pathlib import Path

path = Path(__file__).resolve().parent / "validate_expansion_08.py"
text = path.read_text()
old = '''        if edge.get("relation_type") == "part_of" and edge.get("source") in paper_ids:
            paper_volume[edge["source"]].append(edge)
'''
new = '''        if (
            edge.get("relation_type") == "part_of"
            and edge.get("source") in paper_ids
            and edge.get("target") in volume_ids
        ):
            paper_volume[edge["source"]].append(edge)
'''
if old in text:
    text = text.replace(old, new, 1)
elif "and edge.get(\"target\") in volume_ids" not in text:
    raise SystemExit("Could not tighten the paper-to-volume validation")
path.write_text(text)
print("Tightened paper-to-volume validation")
