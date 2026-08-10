#!/usr/bin/env python3
"""Ensure the curator comment thread has exactly one discreet bottom-right dot."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "docs" / "index.html"
ISSUE_URL = "https://github.com/antlerboy/the-necessary-tangle/issues/2"
DOT = (
    '<a class="curator-secret-dot" data-curator-dot="comments" '
    f'href="{ISSUE_URL}" target="_blank" rel="noopener" '
    'aria-label="Open the curator comment thread" title="Curator comments">'
    '<span aria-hidden="true"></span></a>'
)


def clean(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.rstrip().splitlines()) + "\n"


def main() -> None:
    text = INDEX.read_text(encoding="utf-8")

    # Remove any earlier form of the issue link. Older releases used a visible
    # notebook link and later map patches may already have inserted the dot.
    anchor = re.compile(
        r'<a\b[^>]*href=["\']https://github\.com/antlerboy/the-necessary-tangle/issues/2["\'][^>]*>.*?</a>',
        re.I | re.S,
    )
    text = anchor.sub("", text)
    text = re.sub(r'<p>\s*</p>', '', text, flags=re.I)
    text = re.sub(r'<span\b[^>]*class=["\'][^"\']*discreet-note-link[^"\']*["\'][^>]*>\s*</span>', '', text, flags=re.I)

    if "</body>" not in text:
        raise RuntimeError("Could not locate the end of the public page")
    text = text.replace("</body>", DOT + "\n</body>", 1)
    INDEX.write_text(clean(text), encoding="utf-8")

    rendered = INDEX.read_text(encoding="utf-8")
    if rendered.count('data-curator-dot="comments"') != 1 or rendered.count(ISSUE_URL) != 1:
        raise RuntimeError("Could not normalise the curator comment dot to one link")
    print("Normalised the curator comment thread to one discreet bottom-right dot")


if __name__ == "__main__":
    main()
