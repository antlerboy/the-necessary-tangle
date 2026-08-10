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
    'aria-label="Open the curator\'s running comments" title="Curator comments">'
    '<span aria-hidden="true"></span></a>'
)


def clean(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.rstrip().splitlines()) + "\n"


def main() -> None:
    text = INDEX.read_text(encoding="utf-8")

    # Earlier releases used several forms of this route. Remove every old
    # anchor form before adding the one durable bottom-right affordance.
    old_link = re.compile(
        r'<a\b(?=[^>]*(?:the-necessary-tangle/issues/2|data-curator-dot|curator-notebook-link))[^>]*>.*?</a>',
        re.I | re.S,
    )
    text = old_link.sub("", text)

    # A bare occurrence can survive in stale generated markup. It is not a
    # public route and should not remain alongside the single normalised link.
    text = text.replace(ISSUE_URL, "")
    text = re.sub(r'<a\b[^>]*href=["\']\s*["\'][^>]*>\s*</a>', '', text, flags=re.I | re.S)
    text = re.sub(r'<p>\s*</p>', '', text, flags=re.I)
    text = re.sub(r'<span\b[^>]*class=["\'][^"\']*discreet-note-link[^"\']*["\'][^>]*>\s*</span>', '', text, flags=re.I)

    if "</body>" not in text:
        raise RuntimeError("Could not locate the end of the public page")
    text = text.replace("</body>", DOT + "\n</body>", 1)
    INDEX.write_text(clean(text), encoding="utf-8")

    rendered = INDEX.read_text(encoding="utf-8")
    dot_count = rendered.count('data-curator-dot="comments"')
    url_count = rendered.count(ISSUE_URL)
    if dot_count != 1 or url_count != 1:
        raise RuntimeError(
            f"Could not normalise the curator comment dot: dots={dot_count}, urls={url_count}"
        )
    if 'aria-label="Open the curator\'s running comments"' not in rendered:
        raise RuntimeError("The curator comment dot lacks its accessible name")
    print("Normalised the curator comment thread to one discreet bottom-right dot")


if __name__ == "__main__":
    main()
