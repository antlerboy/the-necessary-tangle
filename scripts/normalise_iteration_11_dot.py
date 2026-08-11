#!/usr/bin/env python3
"""Remove obsolete hidden footer routes from the generated public page."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "docs" / "index.html"


def clean(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.rstrip().splitlines()) + "\n"


def main() -> None:
    text = INDEX.read_text(encoding="utf-8")
    text = re.sub(
        r'<a\b(?=[^>]*(?:data-curator-dot|curator-notebook-link|curator-secret-dot|discreet-note-link))[^>]*>.*?</a>',
        '',
        text,
        flags=re.I | re.S,
    )
    text = re.sub(r'<a\b[^>]*href=["\']\s*["\'][^>]*>\s*</a>', '', text, flags=re.I | re.S)
    text = re.sub(r'<p>\s*</p>', '', text, flags=re.I)
    text = re.sub(r'\n{3,}', '\n\n', text)
    INDEX.write_text(clean(text), encoding="utf-8")
    print("Normalised public footer routes")


if __name__ == "__main__":
    main()
