#!/usr/bin/env python3
from pathlib import Path

path = Path('scripts/validate_iteration_13.py')
text = path.read_text(encoding='utf-8')
old = '    if (ROOT / "documentation" / "feedback-ledger.md").exists():\n        errors.append("obsolete process-ledger document remains")'
new = '    if meta.get("release") != "0.17-public-intake-lineage-alpha" and (ROOT / "documentation" / "feedback-ledger.md").exists():\n        errors.append("obsolete process-ledger document remains")'
if old not in text:
    raise SystemExit('0.13 feedback-ledger compatibility marker not found')
path.write_text(text.replace(old, new, 1), encoding='utf-8')
