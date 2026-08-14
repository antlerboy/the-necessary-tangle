#!/usr/bin/env python3
"""Validate the bounded Pass 5 relationship-disclosure change."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = (ROOT / "docs" / "assets" / "app.js").read_text(encoding="utf-8")
STYLES = (ROOT / "docs" / "assets" / "styles.css").read_text(encoding="utf-8")
INDEX = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")


checks = {
    "basis helper": "function relationshipBasis(edge)" in APP,
    "inference distinguished": "Inferred connection" in APP,
    "interpretation distinguished": "Curatorial interpretation" in APP,
    "source-established distinguished": "Source-established" in APP,
    "stored assertion mode exposed": "Stored assertion mode:" in APP,
    "claim locator exposed": "Claim-level locator:" in APP,
    "quiet relationship key": "relationship-key" in APP and "relationship-key" in STYLES,
    "magic dot preserved": 'aria-label="Open updates"' in INDEX,
}

failed = [label for label, ok in checks.items() if not ok]
if failed:
    raise SystemExit("Pass 5 validation failed: " + ", ".join(failed))
print("Pass 5 experience validation passed (8 checks).")
