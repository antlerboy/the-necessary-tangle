#!/usr/bin/env python3
"""Patch the generated public interface for release 0.19."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "docs" / "index.html"
VERSION = "0.19.0-public"

PANEL = '''
        <article class="plain-panel wide living-mark-note">
          <p class="eyebrow">A living identity</p>
          <h2>The mark is a family, not a badge</h2>
          <p>The name and navigation stay put. The visual mark changes on each fresh load: cats as scientists, structural coupling, impossible forms and shifts of perception. The variation is not decorative churn. It is a small reminder that identity can remain recognisable without pretending to be singular or fixed.</p>
          <p>Moving marks are silent and short. Readers who request reduced motion receive a still. <a href="https://github.com/antlerboy/the-necessary-tangle/blob/main/documentation/visual-identity.md" target="_blank" rel="noopener">Read the visual-identity contract</a> or <a href="/corpora/complexity-podcast/">inspect the new transcript corpus intake</a>.</p>
        </article>
'''


def main() -> None:
    text = INDEX.read_text(encoding="utf-8")

    css = f'  <link rel="stylesheet" href="assets/iteration-19.css?v={VERSION}">\n'
    if "assets/iteration-19.css" not in text:
        text = text.replace('  <link rel="stylesheet" href="assets/iteration-18.css?v=0.18.0-public">\n', '  <link rel="stylesheet" href="assets/iteration-18.css?v=0.18.0-public">\n' + css, 1)

    text = text.replace(
        '<span class="brand-mark tangle-mark" aria-hidden="true">',
        '<span class="brand-mark tangle-mark" data-living-mark aria-hidden="true" title="A living mark selected for this visit">',
        1,
    )

    if "The mark is a family, not a badge" not in text:
        anchor = '        <article class="plain-panel wide feedback-coverage-panel">'
        text = text.replace(anchor, PANEL + "\n" + anchor, 1)

    js = f'  <script src="assets/iteration-19.js?v={VERSION}"></script>\n'
    if "assets/iteration-19.js" not in text:
        text = text.replace('  <script src="assets/iteration-18.js?v=0.18.0-public"></script>\n', '  <script src="assets/iteration-18.js?v=0.18.0-public"></script>\n' + js, 1)

    INDEX.write_text(text, encoding="utf-8")
    print("Patched release 0.19 public interface")


if __name__ == "__main__":
    main()
