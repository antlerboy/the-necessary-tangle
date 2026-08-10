#!/usr/bin/env python3
"""Make the 0.10 safety gate retain its controls without banning the restored 0.11 feedback route."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RELEASE_10 = "0.10-practice-safety-alpha"
RELEASE_11 = "0.11-semantic-map-alpha"


def main() -> None:
    path = ROOT / "scripts" / "validate_iteration_10.py"
    text = path.read_text(encoding="utf-8")

    text = text.replace(
        f'EXPECTED_RELEASE = "{RELEASE_10}"',
        f'ALLOWED_RELEASES = {{"{RELEASE_10}", "{RELEASE_11}"}}',
    )
    text = text.replace(
        'if meta.get("release") != EXPECTED_RELEASE:\n        errors.append(f"meta.release must be {EXPECTED_RELEASE}")',
        'if meta.get("release") not in ALLOWED_RELEASES:\n        errors.append(f"meta.release must be one of {sorted(ALLOWED_RELEASES)}")',
    )

    lines = text.splitlines()
    patched: list[str] = []
    for line in lines:
        stripped = line.strip()
        is_feedback_absence_rule = (
            stripped.startswith("if ")
            and stripped.endswith(":")
            and any(token in stripped for token in ("issues/2", "feedback-dot", "running feedback", "running-feedback"))
            and f'meta.get("release") == "{RELEASE_10}"' not in stripped
        )
        if is_feedback_absence_rule:
            indent = line[: len(line) - len(line.lstrip())]
            expression = stripped[3:-1]
            line = f'{indent}if meta.get("release") == "{RELEASE_10}" and ({expression}):'
        patched.append(line)
    text = "\n".join(patched) + "\n"

    if RELEASE_11 not in text or "ALLOWED_RELEASES" not in text:
        raise RuntimeError("0.10 validator does not admit release 0.11")
    path.write_text(text, encoding="utf-8")
    print("Made the 0.10 safety validator compatible with the restored 0.11 feedback route")


if __name__ == "__main__":
    main()
